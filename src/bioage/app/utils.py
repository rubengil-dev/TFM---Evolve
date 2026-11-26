"""Functions shared within the app.

- `bmi`            : Body mass index.
- `body_in_memory` : Body of a request, without writing it to disk.
- `routine_missing`: Routine lab values missing.
- `extras_known`   : Extras known.
- `max_missing`    : Most Routine values that can be missing in a mode.
"""

# Imports
from fastapi import Request

from bioage.app.schemas import AppError, Mode
from bioage.config.app import MAX_PDF_MB, MODE_LEVELS
from bioage.config.model_levels import EXTRAS, ROUTINE_LAB


def bmi(weight: float, height: float) -> float:
    """Body mass index.

    Args:
        weight: Weight (kg).
        height: Height (cm).

    Returns:
        BMI (kg/m2).
    """
    return weight / (height / 100) ** 2


async def body_in_memory(request: Request) -> bytes:
    """Body of a request, kept in memory (a file form is written to disk above 1 MB).

    Args:
        request: The request.

    Returns:
        Its body.

    Raises:
        AppError: If it is larger than the largest PDF accepted.
    """
    body = bytearray()
    async for chunk in request.stream():
        body += chunk
        if len(body) > MAX_PDF_MB * 1024**2:
            raise AppError("unreadable")
    return bytes(body)


def routine_missing(variables: set[str]) -> int:
    """Routine lab values missing.

    Args:
        variables: Lab variables known.

    Returns:
        How many are missing.
    """
    return len(set(ROUTINE_LAB) - variables)


def extras_known(variables: set[str]) -> int:
    """Extras known.

    Args:
        variables: Lab variables known.

    Returns:
        How many there are.
    """
    return len(set(EXTRAS) & variables)


def max_missing(bundles: dict[str, dict], mode: Mode) -> int:
    """Most Routine values that can be missing in a mode, measured when its model was trained.

    Args:
        bundles: Bundle of each level.
        mode: Mode of the person.

    Returns:
        How many can be missing.
    """
    return len(bundles[MODE_LEVELS[mode]]["margin"]["routine_missing"]) - 1
