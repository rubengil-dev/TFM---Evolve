"""Tests: App - From the data of a person to their result.

- Row for the model: its columns in its order, BMI and habits in their place
- Unknown values → gaps; values the model does not use → left out
- Result: real age, biological age unrounded (the front rounds it once), years with one decimal
- Impossible data are refused before calculating
- Ages out of the study: the difference of the nearest age, added to the real one
- Years: a value for every group, None only without data; they add up to the difference
- Worse habits and values → more years in their group
- Level: with Extras from the fewest their bundle says
- Margin: √(base² + what is missing²), with the base of the risk band, all from the bundle
- Saved models: every part of the margin, Routine missing up to the same count with and without Extras
"""

# Imports
import math

import pandas as pd
import pytest

from bioage.app.calculate import calculate, choose_level, margin, model_row, one_decimal, study_age
from bioage.app.predict import load_bundle, predict_age
from bioage.app.read_pdf import EXAMPLE_READING
from bioage.app.schemas import AppError, Person
from bioage.config.app import BLOOD_GROUPS, EXTRAS_LEVELS, HABIT_GROUPS
from bioage.config.model_levels import EXTRAS, LEVEL_COLUMNS

HABITS = {"smoking": "former", "physical_activity": "intense", "sedentary_hours": 9, "sleep_hours": 6.5}
BUNDLES = {level: load_bundle(level) for level in LEVEL_COLUMNS}
LAB = EXAMPLE_READING.lab_values
PERSON = {"lab_values": LAB, "sex": "female", "age": 52, "weight": 80, "height": 175}


def test_bmi_comes_from_weight_and_height() -> None:
    assert model_row(Person(**PERSON), ["bmi"])["bmi"][0] == pytest.approx(26.12, abs=0.01)


def test_row_has_the_columns_of_the_model_in_their_order() -> None:
    for columns in LEVEL_COLUMNS.values():
        assert list(model_row(Person(**PERSON), columns).columns) == columns


def test_row_keeps_every_value_in_its_place() -> None:
    row = model_row(Person(**PERSON, habits=HABITS), LEVEL_COLUMNS["full"]).iloc[0]
    expected = {"glucose": 98, "hdl": 48, "sex": "female", "age": 52, **HABITS}
    assert row[list(expected)].to_dict() == expected


def test_unknown_values_are_gaps() -> None:
    person = Person(**{**PERSON, "lab_values": {key: value for key, value in LAB.items() if key != "glucose"}})
    row = model_row(person, LEVEL_COLUMNS["full"]).iloc[0]
    known = {*person.lab_values, "sex", "age", "bmi"}
    assert {column for column in row.index if pd.notna(row[column])} == known


def test_values_the_model_does_not_use_are_left_out() -> None:
    person = Person(**{**PERSON, "lab_values": {**LAB, "ggt": 400}})
    assert "ggt" not in model_row(person, LEVEL_COLUMNS["routine"])


def test_result_has_the_real_age_and_the_unrounded_bio_age() -> None:
    result = calculate(Person(**PERSON), BUNDLES)
    exact = predict_age(BUNDLES["routine"], model_row(Person(**PERSON), LEVEL_COLUMNS["routine"]))[0]
    assert (result.age, result.bio_age) == (52, pytest.approx(float(exact), abs=1e-9))
    assert all(years is None or years == round(years, 1) for years in result.blood.values())


def test_impossible_data_are_refused_before_calculating() -> None:
    with pytest.raises(AppError, match="impossible_bmi"):
        only_margins = {level: {"margin": bundle["margin"]} for level, bundle in BUNDLES.items()}  # no models
        calculate(Person(**{**PERSON, "weight": 300, "height": 120}), only_margins)


@pytest.mark.parametrize(("age", "nearest"), [(16, 18), (17, 18), (18, 18), (45, 45), (79, 79), (80, 79), (90, 79)])
def test_study_age_is_the_nearest(age: int, nearest: int) -> None:
    assert study_age(age) == nearest


@pytest.mark.parametrize(("age", "nearest"), [(16, 18), (85, 79)])
@pytest.mark.parametrize("habits", [None, HABITS])
def test_difference_of_the_nearest_age_is_added_to_the_real_one(age: int, nearest: int, habits: dict | None) -> None:
    out = calculate(Person(**{**PERSON, "age": age}, habits=habits), BUNDLES)
    limit = calculate(Person(**{**PERSON, "age": nearest}, habits=habits), BUNDLES)
    assert out.bio_age - age == pytest.approx(limit.bio_age - nearest, abs=0.01)
    assert (out.age, out.blood, out.habits) == (age, limit.blood, limit.habits)


def test_row_has_the_nearest_age() -> None:
    assert model_row(Person(**{**PERSON, "age": 85}), ["age"])["age"][0] == 79


def test_every_group_is_in_the_result() -> None:
    result = calculate(Person(**PERSON, habits=HABITS), BUNDLES)
    assert list(result.blood) == list(BLOOD_GROUPS)
    assert list(result.habits) == list(HABIT_GROUPS)
    assert calculate(Person(**PERSON), BUNDLES).habits is None


def test_groups_without_data_are_none() -> None:
    lab = {key: value for key, value in LAB.items() if key not in BLOOD_GROUPS["red_cells"]}
    blood = calculate(Person(**{**PERSON, "lab_values": lab}), BUNDLES).blood
    assert {group for group, years in blood.items() if years is None} == {"red_cells"}


@pytest.mark.parametrize("habits", [None, HABITS])
def test_groups_add_up_to_the_difference(habits: dict | None) -> None:
    result = calculate(Person(**PERSON, habits=habits), BUNDLES)
    years = [*result.blood.values(), *(result.habits or {}).values()]
    rounding = 0.05 * (len(years) + 1)
    assert sum(value for value in years if value is not None) == pytest.approx(result.bio_age - 52, abs=rounding)


@pytest.mark.parametrize(
    ("group", "better", "worse"),
    [
        ("smoking", {"smoking": "never"}, {"smoking": "current"}),
        ("exercise", {"physical_activity": "intense"}, {"physical_activity": "sedentary"}),
        ("sitting", {"sedentary_hours": 4}, {"sedentary_hours": 14}),
        ("sleep", {"sleep_hours": 7.5}, {"sleep_hours": 12}),
    ],
)
def test_worse_habit_adds_years_to_its_group(group: str, better: dict, worse: dict) -> None:
    low, high = (
        calculate(Person(**PERSON, habits={**HABITS, **habits}), BUNDLES).habits[group] for habits in (better, worse)
    )
    assert low < high


def test_worse_value_adds_years_to_its_group() -> None:
    low, high = (
        calculate(Person(**{**PERSON, "lab_values": {**LAB, "glucose": glucose}}), BUNDLES).blood["sugar"]
        for glucose in (85, 250)
    )
    assert low < high


@pytest.mark.parametrize(("years", "shown"), [(None, None), (1.26, 1.3), (-0.04, 0.0), (-1.26, -1.3)])
def test_one_decimal(years: float | None, shown: float | None) -> None:
    assert one_decimal(years) == shown
    assert str(one_decimal(years)) != "-0.0"


@pytest.mark.parametrize(
    ("extras", "habits", "level"),
    [(2, None, "routine"), (3, None, "extras"), (3, HABITS, "questionnaire"), (4, HABITS, "full")],
)
def test_extras_are_used_from_their_minimum(extras: int, habits: dict | None, level: str) -> None:
    values = dict(list({"ggt": 30, "albumin": 4.3, "vitamin_d": 24, "ldh": 180}.items())[:extras])
    fewest = {"extras": {"margin": {"min_extras": 3}}, "full": {"margin": {"min_extras": 4}}}
    assert choose_level(Person(**{**PERSON, "lab_values": {**LAB, **values}}, habits=habits), fewest) == level


MARGIN = {"low_risk_below": 0.05, "low_risk": 4, "rest": 0.5, "routine_missing": [0, 1, 2, 3, 4, 5]}


@pytest.mark.parametrize(
    ("risk", "dropped", "expected"), [(0.01, 0, 4), (0.05, 0, 0.5), (0.2, 0, 0.5), (0.2, 3, math.sqrt(0.5**2 + 3**2))]
)
def test_margin_joins_base_and_what_is_missing(risk: float, dropped: int, expected: float) -> None:
    lab = dict(list(LAB.items())[dropped:])
    assert margin(Person(**{**PERSON, "lab_values": lab}), {"margin": MARGIN}, risk) == pytest.approx(expected)


def test_margin_adds_the_extras_missing() -> None:
    bundle = {"margin": {**MARGIN, "extras_known": [8, 7, 6, 5, 4, 3, 2, 1, 0]}}
    person = Person(**{**PERSON, "lab_values": {**LAB, "ggt": 30, "albumin": 4.3, "ldh": 180}})
    assert margin(person, bundle, 0.2) == pytest.approx(math.sqrt(0.5**2 + 5**2))


def test_saved_models_have_their_margin() -> None:
    for level, with_extras in EXTRAS_LEVELS.items():
        parts, extras = BUNDLES[level]["margin"], BUNDLES[with_extras]["margin"]
        assert parts["routine_missing"][0] == extras["routine_missing"][0] == 0
        assert len(parts["routine_missing"]) == len(extras["routine_missing"])
        assert len(extras["extras_known"]) == len(EXTRAS) + 1 and extras["extras_known"][-1] == 0
        assert 0 < extras["min_extras"] <= len(EXTRAS)
    assert all(0 < bundle["margin"]["low_risk_below"] < 1 for bundle in BUNDLES.values())


def test_result_has_a_margin() -> None:
    assert calculate(Person(**PERSON), BUNDLES).margin > 0
