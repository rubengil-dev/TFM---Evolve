"""Tests: App - From the data of a person to their result.

- Row for the model: its columns in its order, BMI and habits in their place
- Unknown values → gaps; values the model does not use → left out
- Result: real age, biological age with one decimal
"""

# Imports
import pandas as pd
import pytest

from bioage.app.calculate import calculate, model_row
from bioage.app.predict import load_bundle, predict_age
from bioage.app.schemas import Person
from bioage.config.model_levels import LEVEL_COLUMNS

HABITS = {"smoking": "former", "physical_activity": "intense", "sedentary_hours": 9, "sleep_hours": 6.5}
PERSON = {"lab_values": {"glucose": 98, "hdl": 48}, "sex": "female", "age": 52, "weight": 80, "height": 175}


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
    row = model_row(Person(**PERSON), LEVEL_COLUMNS["full"]).iloc[0]
    known = {*PERSON["lab_values"], "sex", "age", "bmi"}
    assert {column for column in row.index if pd.notna(row[column])} == known


def test_values_the_model_does_not_use_are_left_out() -> None:
    person = Person(**{**PERSON, "lab_values": {"glucose": 98, "ggt": 400}})
    assert "ggt" not in model_row(person, LEVEL_COLUMNS["routine"])


def test_result_has_the_real_age_and_one_decimal() -> None:
    bundles = {"routine": load_bundle("routine")}
    result = calculate(Person(**PERSON), bundles)
    exact = predict_age(bundles["routine"], model_row(Person(**PERSON), LEVEL_COLUMNS["routine"]))[0]
    assert (result.age, result.bio_age) == (52, round(float(exact), 1))
