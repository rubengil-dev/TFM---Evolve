"""
Preprocessing pipeline on a made-up Gold:
    - Extremes clipped to the train quantiles
    - Gaps filled with the value of the same sex and age group, or the overall one
    - Full pipeline: no gaps left, one column per feature
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from src.config.model_sets import LEVEL_COLUMNS
from src.config.study import CLIP_QUANTILES
from src.models.s2_preprocessing import GroupImputer, QuantileClipper, build_preprocessor, fill_value


def test_clipper_limits_to_train_quantiles(made_up_gold):
    """Values beyond the train quantiles → the quantile; values inside untouched."""
    clipper = QuantileClipper(["glucose"]).fit(made_up_gold)
    low, high = made_up_gold["glucose"].quantile(list(CLIP_QUANTILES))
    clipped = clipper.transform(pd.DataFrame({"glucose": [0, 85, 1000]}))["glucose"]
    assert clipped.tolist() == pytest.approx([low, 85, high])


def test_imputer_uses_same_sex_and_age_group(made_up_gold):
    """A gap → median (numeric) or most frequent answer (text) of train people of the same sex and age group."""
    imputer = GroupImputer(["glucose", "smoking"]).fit(made_up_gold)
    person = pd.DataFrame({"age": [45], "sex": ["male"], "glucose": [np.nan], "smoking": [np.nan]})
    group = made_up_gold[(made_up_gold["sex"] == "male") & made_up_gold["age"].between(40, 49)]
    filled = imputer.transform(person).iloc[0]
    assert filled["glucose"] == pytest.approx(group["glucose"].median())
    assert filled["smoking"] == group["smoking"].mode().iloc[0]


def test_imputer_keeps_given_values_and_falls_back_to_overall(made_up_gold):
    """Given values untouched; a group without train people → overall value."""
    imputer = GroupImputer(["glucose"]).fit(made_up_gold[made_up_gold["age"] < 70])
    people = pd.DataFrame({"age": [45, 75], "sex": ["female", "female"], "glucose": [123.0, np.nan]})
    filled = imputer.transform(people)["glucose"]
    assert filled.tolist() == pytest.approx([123, made_up_gold.loc[made_up_gold["age"] < 70, "glucose"].median()])


def test_imputer_gives_no_drinks_to_never_drinkers(made_up_gold):
    """Never drinks → 0 drinks per day, whatever the group median."""
    imputer = GroupImputer(["alcohol_frequency", "alcohol_drinks"]).fit(made_up_gold)
    person = pd.DataFrame({"age": [45], "sex": ["male"], "alcohol_frequency": ["never"], "alcohol_drinks": [np.nan]})
    assert imputer.transform(person)["alcohol_drinks"].iloc[0] == 0


def test_fill_value_follows_the_column_not_the_series_name():
    """The kind of column is passed explicitly: a text column gets its most frequent answer."""
    answers = pd.Series(["never", "current", "never"], name="anything")
    assert fill_value(answers, "smoking") == "never"
    assert fill_value(pd.Series([1.0, 2.0, 9.0]), "glucose") == 2.0


@pytest.mark.parametrize("level", LEVEL_COLUMNS)
def test_full_pipeline_leaves_no_gaps(made_up_gold, level):
    """Every level: no gaps, finite numbers, first category without a column and squared terms added."""
    columns = LEVEL_COLUMNS[level]
    features = build_preprocessor(columns).fit_transform(made_up_gold[columns])
    assert features.notna().all().all() and np.isfinite(features.to_numpy()).all()
    assert "sex_male" in features and "sex_female" not in features
    assert "bmi_squared" in features
    assert len(features) == len(made_up_gold)
