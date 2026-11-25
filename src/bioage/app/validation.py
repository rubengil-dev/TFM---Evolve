"""Checks before calculating.

- Age
- Impossible values
- Lacking so many values
"""

# Imports
from bioage.app.schemas import AppError
from bioage.config.app import MAX_AGE, MIN_AGE


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
