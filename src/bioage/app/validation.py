"""Checks before calculating.

- Age
- Impossible values
- Lacking so many values
"""

# Imports
from bioage.app.schemas import AppError, Person
from bioage.app.utils import bmi, routine_missing
from bioage.config.app import MAX_AGE, MIN_AGE
from bioage.config.plausible_ranges import PLAUSIBLE_RANGES


def check_person(person: Person, max_missing: int) -> None:
    """Every check of a person, before calculating.

    Args:
        person: Data of the person.
        max_missing: Most Routine values that can be missing in their mode.

    Raises:
        AppError: If no age can be calculated with those data.
    """
    check_age(person.age)
    check_lab_values(person.lab_values)
    check_enough(set(person.lab_values), max_missing)
    check_bmi(person.weight, person.height)


def check_age(age: int) -> None:
    """Refuse ages the app does not calculate for.

    Args:
        age: Age of the person.

    Raises:
        AppError: If the person is too young or too old.
    """
    if age < MIN_AGE:
        raise AppError("too_young")
    if age > MAX_AGE:
        raise AppError("too_old")


def check_lab_values(lab_values: dict[str, float]) -> None:
    """Refuse values outside their plausible range.

    Args:
        lab_values: Values of the blood test, in model units.

    Raises:
        AppError: If any value is impossible.
    """
    if not all(is_possible(variable, value) for variable, value in lab_values.items()):
        raise AppError("impossible")


def check_enough(variables: set[str], max_missing: int) -> None:
    """Refuse a blood test that lacks too many Routine values.

    Args:
        variables: Lab variables known.
        max_missing: Most that can be missing.

    Raises:
        AppError: If too many are missing.
    """
    if routine_missing(variables) > max_missing:
        raise AppError("too_few")


def check_bmi(weight: float, height: float) -> None:
    """Refuse a weight and a height that cannot go together.

    Args:
        weight: Weight (kg).
        height: Height (cm).

    Raises:
        AppError: If their BMI is impossible.
    """
    if not is_possible("bmi", bmi(weight, height)):
        raise AppError("impossible_bmi")


def is_possible(variable: str, value: float) -> bool:
    """Tell if a value is inside its plausible range, both limits included.

    Args:
        variable: Name of the variable.
        value: Value, in model units.

    Returns:
        Whether it is possible.
    """
    low, high = PLAUSIBLE_RANGES[variable][2]
    return low <= value <= high
