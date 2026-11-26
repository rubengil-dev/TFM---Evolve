"""Tests: App - Checks before calculating.

- Every lab variable: both limits of its range accepted, just outside refused
- BMI: weights and heights valid on their own but impossible together are refused
- Enough data: up to 5 Routine values missing in the quick mode, 8 in the full one
- Order: the age first, so each person is told the right reason
"""

# Imports
from typing import get_args

import pytest

from bioage.app.read_pdf import EXAMPLE_READING
from bioage.app.schemas import AppError, Person
from bioage.app.validation import check_bmi, check_enough, check_lab_values, check_person
from bioage.config.model_levels import LabVariable
from bioage.config.plausible_ranges import PLAUSIBLE_RANGES

ROUTINE_LAB = list(EXAMPLE_READING.lab_values)
PERSON = {"lab_values": EXAMPLE_READING.lab_values, "sex": "male", "age": 45, "weight": 80, "height": 175}


@pytest.mark.parametrize("variable", get_args(LabVariable))
def test_limits_of_a_lab_value_are_accepted(variable: str) -> None:
    for limit in PLAUSIBLE_RANGES[variable][2]:
        check_lab_values({variable: limit})


@pytest.mark.parametrize("variable", get_args(LabVariable))
def test_lab_value_outside_its_range_is_refused(variable: str) -> None:
    low, high = PLAUSIBLE_RANGES[variable][2]
    for value in (low - 0.001, high + 0.001):
        with pytest.raises(AppError, match="^impossible$"):
            check_lab_values({variable: value})


def test_one_impossible_value_among_good_ones_is_refused() -> None:
    with pytest.raises(AppError, match="^impossible$"):
        check_lab_values({"glucose": 98, "potassium": 9.8, "hdl": 50})


def test_nothing_to_check_is_accepted() -> None:
    check_lab_values({})


@pytest.mark.parametrize(("weight", "height"), [(300, 120), (30, 220), (39, 181)])
def test_impossible_bmi_is_refused(weight: float, height: float) -> None:
    with pytest.raises(AppError, match="^impossible_bmi$"):
        check_bmi(weight, height)


@pytest.mark.parametrize(("weight", "height"), [(48, 200), (225, 150), (80, 175)])
def test_possible_bmi_is_accepted(weight: float, height: float) -> None:
    check_bmi(weight, height)


@pytest.mark.parametrize(
    ("changes", "code"),
    [
        ({"age": 12, "lab_values": {"potassium": 9.8}, "weight": 300, "height": 120}, "too_young"),
        ({"lab_values": {"potassium": 9.8}, "weight": 300, "height": 120}, "impossible"),
        ({"weight": 300, "height": 120}, "impossible_bmi"),
    ],
)
def test_first_reason_is_told(changes: dict, code: str) -> None:
    with pytest.raises(AppError, match=f"^{code}$"):
        check_person(Person(**{**PERSON, **changes}))


def test_possible_person_is_accepted() -> None:
    check_person(Person(**PERSON))


@pytest.mark.parametrize(
    ("missing", "mode", "fine"), [(5, "quick", True), (6, "quick", False), (8, "full", True), (9, "full", False)]
)
def test_enough_data_for_the_mode(missing: int, mode: str, fine: bool) -> None:
    known = set(ROUTINE_LAB[missing:]) | {"ggt", "ldh"}
    if fine:
        check_enough(known, mode)
    else:
        with pytest.raises(AppError, match="too_few"):
            check_enough(known, mode)


def test_person_with_too_few_values_is_refused() -> None:
    with pytest.raises(AppError, match="too_few"):
        check_person(Person(**{**PERSON, "lab_values": {"glucose": 98}}))
