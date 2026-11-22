"""Tests: Models - Step 2, preprocessing, on a made-up Gold.

- Extremes clipped to the train quantiles
- Gaps filled with the value of the same sex and age group, or the overall one
- Logarithm only for the skewed variables
- Full pipeline of each level: no gaps, the first answer of each text variable as reference (no column),
  squares of the scaled U-shaped variables, numeric features scaled on train
- Columns found by name: another order or extra columns give the same features
- Unknown text answer → error, not taken as the reference answer
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.config.model_levels import LEVEL_COLUMNS
from bioage.config.study import CATEGORICAL_LEVELS, CLIP_QUANTILES
from bioage.models.s2_preprocessing import (
    GroupImputer,
    QuantileClipper,
    build_preprocessor,
    fill_value,
    log_skewed,
)


def test_clipper_limits_to_train_quantiles(made_up_gold: pd.DataFrame) -> None:
    clipper = QuantileClipper(["glucose"]).fit(made_up_gold)
    low, high = made_up_gold["glucose"].quantile(list(CLIP_QUANTILES))
    clipped = clipper.transform(pd.DataFrame({"glucose": [0, 85, 1000]}))["glucose"]
    assert clipped.tolist() == pytest.approx([low, 85, high])


def test_imputer_uses_same_sex_and_age_group(made_up_gold: pd.DataFrame) -> None:
    imputer = GroupImputer(["glucose", "smoking"]).fit(made_up_gold)
    person = pd.DataFrame({"age": [45], "sex": ["male"], "glucose": [np.nan], "smoking": [np.nan]})
    group = made_up_gold[(made_up_gold["sex"] == "male") & made_up_gold["age"].between(40, 49)]
    filled = imputer.transform(person).iloc[0]
    assert filled["glucose"] == pytest.approx(group["glucose"].median())
    assert filled["smoking"] == group["smoking"].mode().iloc[0]


def test_imputer_keeps_given_values_and_falls_back_to_overall(made_up_gold: pd.DataFrame) -> None:
    imputer = GroupImputer(["glucose"]).fit(made_up_gold[made_up_gold["age"] < 70])
    people = pd.DataFrame({"age": [45, 75], "sex": ["female", "female"], "glucose": [123.0, np.nan]})
    filled = imputer.transform(people)["glucose"]
    assert filled.tolist() == pytest.approx([123, made_up_gold.loc[made_up_gold["age"] < 70, "glucose"].median()])


def test_fill_value_follows_the_column_not_the_series_name() -> None:
    answers = pd.Series(["never", "current", "never"], name="anything")
    assert fill_value(answers, "smoking") == "never"
    assert fill_value(pd.Series([1.0, 2.0, 9.0]), "glucose") == 2.0


def test_log_only_for_skewed_variables() -> None:
    numeric = pd.DataFrame({"glucose": [99.0], "sodium": [140.0]})
    assert log_skewed(numeric).iloc[0].tolist() == pytest.approx([np.log(100), 140])


@pytest.mark.parametrize("level", LEVEL_COLUMNS)
def test_full_pipeline_leaves_no_gaps(made_up_gold: pd.DataFrame, level: str) -> None:
    columns = LEVEL_COLUMNS[level]
    features = build_preprocessor(columns).fit_transform(made_up_gold[columns])
    assert features.notna().all().all() and np.isfinite(features.to_numpy()).all()
    for column in set(columns) & set(CATEGORICAL_LEVELS):
        reference, *others = CATEGORICAL_LEVELS[column]
        assert f"{column}_{reference}" not in features
        assert all(f"{column}_{answer}" in features for answer in others)
    assert features["bmi_squared"].tolist() == pytest.approx((features["bmi"] ** 2).tolist())
    assert len(features) == len(made_up_gold)


def test_numeric_features_scaled_on_train(made_up_gold: pd.DataFrame) -> None:
    columns = LEVEL_COLUMNS["routine"]
    features = build_preprocessor(columns).fit_transform(made_up_gold[columns])
    numeric = [column for column in columns if column not in CATEGORICAL_LEVELS]
    assert features[numeric].mean().abs().max() < 1e-9
    assert features[numeric].std(ddof=0).tolist() == pytest.approx([1.0] * len(numeric))


def test_columns_found_by_name(made_up_gold: pd.DataFrame) -> None:
    columns = LEVEL_COLUMNS["questionnaire"]
    preprocessor = build_preprocessor(columns).fit(made_up_gold[columns])
    expected = preprocessor.transform(made_up_gold[columns])
    shuffled = made_up_gold[list(reversed(columns))].assign(extra=1)
    pd.testing.assert_frame_equal(preprocessor.transform(shuffled), expected)


def test_unknown_answer_is_an_error(made_up_gold: pd.DataFrame) -> None:
    columns = LEVEL_COLUMNS["questionnaire"]
    preprocessor = build_preprocessor(columns).fit(made_up_gold[columns])
    person = made_up_gold[columns].iloc[[0]].assign(smoking="sometimes")
    with pytest.raises(ValueError):
        preprocessor.transform(person)
