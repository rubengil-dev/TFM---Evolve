"""Tests: Models - Step 6, years of each group, on a made-up Gold.

- Reference: the weighted average of what each group adds, within each sex, is the one of the curve
- The groups add up to biological age - age, also with gaps
- Years of a group: what it adds over the average, at the rate of the person
- No data of a group → no years; it depends on the variables of the level
- More of a risk → more years, only in its group
- Years per unit of hazard: the person's own, or the slope of the curve if they are typical
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.app.predict import predict_age, predict_groups
from bioage.config.app import BLOOD_GROUPS, OTHER
from bioage.config.model_levels import LEVEL_COLUMNS
from bioage.modeling.s4_biological_age import age_terms, log_cumulative_hazard, read_hazard, risk_at_horizon
from bioage.modeling.s6_group_years import group_hazards, model_groups, years_per_hazard
from bioage.pipeline.s5_build_model import build_level


@pytest.fixture
def gold(made_up_gold: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(1)
    older_die_more = ((made_up_gold["age"] - 10) / 80).clip(0, 1)
    return made_up_gold.assign(death=rng.binomial(1, older_die_more))


@pytest.fixture
def bundle(gold: pd.DataFrame) -> dict:
    return build_level("full", LEVEL_COLUMNS["full"], gold)


def person(gold: pd.DataFrame, row: int = 0, **changes: object) -> pd.DataFrame:
    complete = gold.dropna(subset=LEVEL_COLUMNS["full"])
    return complete.iloc[[row]][LEVEL_COLUMNS["full"]].assign(**changes)


def test_reference_is_the_weighted_average(gold: pd.DataFrame, bundle: dict) -> None:
    hazards = group_hazards(bundle["pipeline"], gold, bundle["columns"])
    for sex in ["female", "male"]:
        members = gold["sex"] == sex
        terms = np.column_stack([np.ones(members.sum()), age_terms(gold.loc[members, "age"].to_numpy(float))])
        for group, curves in bundle["group_reference"].items():
            gap = hazards.loc[members, group] - terms @ curves[sex]
            assert np.average(gap, weights=gold.loc[members, "weight_exam"]) == pytest.approx(0, abs=1e-6)


def test_groups_add_up_to_the_difference(gold: pd.DataFrame, bundle: dict) -> None:
    for row in range(5):
        for hidden in ([], ["glucose"], BLOOD_GROUPS["liver"]):
            data = person(gold, row, **dict.fromkeys(hidden, np.nan))
            total = sum(years for years in predict_groups(bundle, data).values() if years is not None)
            assert total == pytest.approx(predict_age(bundle, data)[0] - data["age"].iloc[0], abs=1e-6)


def test_years_are_the_hazard_over_the_average_at_the_own_rate(gold: pd.DataFrame, bundle: dict) -> None:
    data = person(gold)
    age, sex = float(data["age"].iloc[0]), data["sex"].iloc[0]
    hazard = log_cumulative_hazard(risk_at_horizon(bundle["pipeline"], data))[0]
    typical = read_hazard(np.array([age]), bundle["reference"], sex)[0]
    rate = (predict_age(bundle, data)[0] - age) / (hazard - typical)
    hazards = group_hazards(bundle["pipeline"], data, bundle["columns"]).iloc[0]
    years = predict_groups(bundle, data)
    for group, curves in bundle["group_reference"].items():
        average = curves[sex] @ [1, age - 50, (age - 50) ** 2]
        assert years[group] == pytest.approx((hazards[group] - average) * rate)


def test_group_without_data_has_no_years(gold: pd.DataFrame, bundle: dict) -> None:
    years = predict_groups(bundle, person(gold, glucose=np.nan, creatinine=np.nan))
    assert years["sugar"] is None
    assert years["kidney"] is not None  # urea and uric acid are known
    assert years[OTHER] is not None


def test_level_decides_the_groups() -> None:
    assert "smoking" not in model_groups(LEVEL_COLUMNS["routine"])
    assert model_groups(LEVEL_COLUMNS["routine"])["liver"] == ["ast", "alt"]
    assert OTHER not in model_groups(LEVEL_COLUMNS["full"])


def test_only_the_group_that_changes_adds_hazard(gold: pd.DataFrame, bundle: dict) -> None:
    before = group_hazards(bundle["pipeline"], person(gold, glucose=80), bundle["columns"]).iloc[0]
    after = group_hazards(bundle["pipeline"], person(gold, glucose=95), bundle["columns"]).iloc[0]
    assert after["sugar"] != pytest.approx(before["sugar"])
    assert after.drop("sugar").to_dict() == pytest.approx(before.drop("sugar").to_dict(), abs=1e-6)


def test_years_per_hazard(bundle: dict) -> None:
    reference = bundle["reference"]
    low, high = read_hazard(np.array([49.5, 50.5]), reference, "female")
    assert years_per_hazard(6, 0.5, 50, "female", reference) == pytest.approx(12)
    assert years_per_hazard(0, 0, 50, "female", reference) == pytest.approx(1 / (high - low))
