"""Tests: Utils - Gold validation, on a made-up Gold.

- A valid Gold passes every check but size; a failed check stops Gold
- Each check catches the error it is for: missing cycle and too few deaths, low coverage (stricter outside the partial
  columns), unknown cycle, BMI not matching weight and height, and the rest
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.config.validation_rules import MIN_COVERAGE, MIN_DEATHS, MIN_PERSONS_PER_CYCLE
from bioage.utils import validation


def test_valid_gold_passes_every_check_but_size(made_up_gold: pd.DataFrame) -> None:
    checks = [
        validation.check_structure,
        validation.check_coverage,
        validation.check_required,
        validation.check_outcome,
        validation.check_population,
        validation.check_categories,
        validation.check_ranges,
        validation.check_finite,
        validation.check_consistency,
    ]
    assert {check.__name__: check(made_up_gold) for check in checks} == {check.__name__: [] for check in checks}
    assert validation.check_size(made_up_gold)


def test_failed_validation_stops_gold(made_up_gold: pd.DataFrame) -> None:
    with pytest.raises(ValueError):
        validation.validate_gold(made_up_gold)


def test_size_catches_missing_cycle_and_too_few_deaths(made_up_gold: pd.DataFrame) -> None:
    gold = made_up_gold[made_up_gold["cycle"] != "2009_2010"].assign(death=0)  # as if mortality never joined
    errors = validation.check_size(gold)
    assert f"cycle 2009_2010: 0 persons, minimum {MIN_PERSONS_PER_CYCLE}" in errors
    assert f"0 deaths, minimum {MIN_DEATHS}" in errors


def test_coverage_catches_column_mostly_empty(made_up_gold: pd.DataFrame) -> None:
    half = made_up_gold.index[: len(made_up_gold) // 2]
    made_up_gold.loc[half, ["glucose", "vitamin_d"]] = np.nan
    errors = validation.check_coverage(made_up_gold)  # vitamin_d is partial: about half is enough
    assert len(errors) == 1 and errors[0].startswith("glucose:") and errors[0].endswith(f"minimum {MIN_COVERAGE}%")


def test_structure_catches_missing_extra_and_wrong_type(made_up_gold: pd.DataFrame) -> None:
    gold = made_up_gold.drop(columns="hdl").assign(extra=1, glucose=made_up_gold["glucose"].astype(str))
    assert sorted(validation.check_structure(gold)) == [
        "glucose: should be numeric",
        "missing column: hdl",
        "unexpected column: extra",
    ]


def test_categories_catch_unknown_answer(made_up_gold: pd.DataFrame) -> None:
    made_up_gold.loc[0, "smoking"] = "sometimes"
    assert validation.check_categories(made_up_gold) == ["smoking: unknown answers ['sometimes']"]


def test_ranges_catch_impossible_value(made_up_gold: pd.DataFrame) -> None:
    made_up_gold.loc[0, "glucose"] = 900
    assert validation.check_ranges(made_up_gold) == ["glucose: 1 values outside 30-600"]


def test_required_catches_missing_value_and_repeated_person(made_up_gold: pd.DataFrame) -> None:
    made_up_gold.loc[0, "sex"] = None
    made_up_gold.loc[1, "seqn"] = made_up_gold.loc[2, "seqn"]
    assert validation.check_required(made_up_gold) == ["sex: 1 missing", "seqn: 1 repeated"]


def test_outcome_and_population_catch_impossible_values(made_up_gold: pd.DataFrame) -> None:
    made_up_gold.loc[0, "death"] = 2
    made_up_gold.loc[1, "follow_up_months"] = 0
    made_up_gold.loc[2, "age"] = 85
    assert validation.check_outcome(made_up_gold) == [
        "death: values other than 0 / 1",
        "follow_up_months: 1 values outside 0.1-252",
    ]
    assert validation.check_population(made_up_gold) == ["age: 1 values outside 18-79"]


def test_population_catches_unknown_cycle(made_up_gold: pd.DataFrame) -> None:
    made_up_gold.loc[0, "cycle"] = "2019_2020"
    assert validation.check_population(made_up_gold) == ["cycle: 1 unknown"]


def test_required_catches_survey_weight_not_above_zero(made_up_gold: pd.DataFrame) -> None:
    made_up_gold.loc[0, "weight_exam"] = 0
    assert validation.check_required(made_up_gold) == ["weight_exam: 1 not above 0"]


def test_finite_catches_division_by_zero(made_up_gold: pd.DataFrame) -> None:
    made_up_gold.loc[0, "albumin_globulin"] = np.inf  # what albumin / 0 gives
    made_up_gold.loc[1, "urine_acr"] = -np.inf
    assert sorted(validation.check_finite(made_up_gold)) == [
        "albumin_globulin: 1 infinite values",
        "urine_acr: 1 infinite values",
    ]


def test_consistency_warns_of_pairs_out_of_order(made_up_gold: pd.DataFrame) -> None:
    made_up_gold.loc[0, ["hdl", "total_cholesterol"]] = [150, 140]
    assert validation.check_consistency(made_up_gold) == ["hdl not below total_cholesterol: 1 persons"]


def test_consistency_warns_of_bmi_not_matching_weight_and_height(made_up_gold: pd.DataFrame) -> None:
    made_up_gold.loc[0, ["weight", "height", "bmi"]] = [80, 180, 30]  # 80 / 1.8² = 24.7
    assert validation.check_consistency(made_up_gold) == ["bmi not matching weight / height^2: 1 persons"]
