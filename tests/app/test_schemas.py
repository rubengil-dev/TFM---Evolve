"""Tests: App - What each schema accepts.

- Ranges: both limits accepted, anything outside refused
- Unknown fields refused in everything the browser sends
- Nothing missing or empty, except what is optional
- Every lab variable accepted
- Every error code raised is in the list
- Result: only known groups; a habit always has its years
"""

# Imports
import re
from typing import get_args

import pytest
from pydantic import BaseModel, ValidationError

from bioage.app.schemas import Habits, OddValue, Person, Reading, Result
from bioage.config.app import ErrorCode
from bioage.config.model_levels import LabVariable
from bioage.config.paths import ROOT
from bioage.config.plausible_ranges import PLAUSIBLE_RANGES

HABITS = {"smoking": "former", "physical_activity": "moderate", "sedentary_hours": 7, "sleep_hours": 7}
PERSON = {"lab_values": {"glucose": 98}, "sex": "male", "age": 45, "weight": 80, "height": 175}
ODD = {"variable": "potassium", "text": "45", "unit": "mmol/L", "factor": 1}
READING = {"lab_values": {"glucose": 98}, "sex": None, "age": None, "odd": []}
SENT = [(Person, PERSON), (Habits, HABITS), (OddValue, ODD)]
RANGES = [
    (Person, PERSON, "weight"),
    (Person, PERSON, "height"),
    (Habits, HABITS, "sedentary_hours"),
    (Habits, HABITS, "sleep_hours"),
]


@pytest.mark.parametrize(("schema", "data", "field"), RANGES)
def test_limits_of_a_range_are_accepted(schema: type[BaseModel], data: dict, field: str) -> None:
    for limit in PLAUSIBLE_RANGES[field][2]:
        assert getattr(schema(**{**data, field: limit}), field) == limit


@pytest.mark.parametrize(("schema", "data", "field"), RANGES)
def test_outside_a_range_is_refused(schema: type[BaseModel], data: dict, field: str) -> None:
    low, high = PLAUSIBLE_RANGES[field][2]
    for value in (low - 0.1, high + 0.1):
        with pytest.raises(ValidationError):
            schema(**{**data, field: value})


@pytest.mark.parametrize(("schema", "data"), SENT)
def test_unknown_fields_are_refused(schema: type[BaseModel], data: dict) -> None:
    with pytest.raises(ValidationError, match="Extra inputs"):
        schema(**data, unknown=1)


@pytest.mark.parametrize(
    ("schema", "data", "field"), [(schema, data, field) for schema, data in SENT for field in data]
)
def test_fields_cannot_be_missing_or_empty(schema: type[BaseModel], data: dict, field: str) -> None:
    with pytest.raises(ValidationError):
        schema(**{name: value for name, value in data.items() if name != field})
    with pytest.raises(ValidationError):
        schema(**{**data, field: None})


@pytest.mark.parametrize("field", READING)
def test_reading_says_everything(field: str) -> None:
    with pytest.raises(ValidationError):
        Reading(**{name: value for name, value in READING.items() if name != field})


def test_habits_are_optional() -> None:
    assert Person(**PERSON).habits is None
    assert Person(**PERSON, habits=HABITS).habits == Habits(**HABITS)


def test_every_lab_variable_is_accepted() -> None:
    values = dict.fromkeys(get_args(LabVariable), 1.0)
    assert Person(**{**PERSON, "lab_values": values}).lab_values == values


def test_error_codes_raised_are_in_the_list() -> None:
    files = (ROOT / "src" / "bioage" / "app").glob("*.py")
    raised = {code for file in files for code in re.findall(r'AppError\("(\w+)"\)', file.read_text(encoding="utf-8"))}
    assert raised and raised <= set(get_args(ErrorCode))


@pytest.mark.parametrize(
    "changes",
    [{"blood": {"heart": 1.0}}, {"habits": {"alcohol": 1.0}}, {"habits": {"smoking": None}}],
)
def test_result_refuses_unknown_groups_and_habits_without_years(changes: dict) -> None:
    with pytest.raises(ValidationError):
        Result(**{"age": 45, "bio_age": 44.0, "blood": {"sugar": None}, **changes})
