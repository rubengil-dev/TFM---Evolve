"""Person → result: picks the model and calculates the biological age, its margin and the years of each group."""

# Imports
import math

import numpy as np
import pandas as pd

from bioage.app.predict import predict_age, predict_groups, predict_risk
from bioage.app.schemas import Person, Result
from bioage.app.utils import bmi, extras_known, routine_missing
from bioage.app.validation import check_person
from bioage.config.app import (
    BASE_MARGIN,
    BLOOD_GROUPS,
    EXTRAS_MARGIN,
    HABIT_GROUPS,
    MIN_EXTRAS,
    MISSING_MARGIN,
)
from bioage.config.study import AGE_MAX, AGE_MIN


def calculate(person: Person, bundles: dict[str, dict]) -> Result:
    """Biological age of a person, with the model their data allow.

    Args:
        person: Data of the person.
        bundles: Bundle of each level.

    Returns:
        Result to show.

    Raises:
        AppError: If no age can be calculated with those data.
    """
    check_person(person)
    level = choose_level(person)
    bundle = bundles[level]
    row = model_row(person, bundle["columns"])
    years = predict_groups(bundle, row)
    return Result(
        age=person.age,
        bio_age=one_decimal(predict_age(bundle, row)[0] + person.age - study_age(person.age)),
        margin=one_decimal(margin(person, level, predict_risk(bundle, row)[0])),
        blood={group: one_decimal(years.get(group)) for group in BLOOD_GROUPS},
        habits=None if person.habits is None else {group: one_decimal(years[group]) for group in HABIT_GROUPS},
    )


def choose_level(person: Person) -> str:
    """Level whose model is used: with Extras if there are enough of them.

    Args:
        person: Data of the person.

    Returns:
        Name of the level.
    """
    level = "routine" if person.habits is None else "questionnaire"
    with_extras, fewest = MIN_EXTRAS[level]
    return with_extras if extras_known(set(person.lab_values)) >= fewest else level


def margin(person: Person, level: str, risk: float) -> float:
    """Margin ± of the biological age: base error and error for what is missing.

    Args:
        person: Data of the person.
        level: Level of the model used.
        risk: 10-year risk of the person.

    Returns:
        Years.
    """
    low_risk_below, low_risk, rest = BASE_MARGIN[level]
    base = low_risk if risk < low_risk_below else rest
    known = set(person.lab_values)
    missing = MISSING_MARGIN[person.mode][routine_missing(known)]
    extras = EXTRAS_MARGIN[level][extras_known(known)] if level in EXTRAS_MARGIN else 0
    return math.sqrt(base**2 + missing**2 + extras**2)


def model_row(person: Person, columns: list[str]) -> pd.DataFrame:
    """Table of one person with the columns of a model; what is not known stays missing.

    Args:
        person: Data of the person.
        columns: Columns of the model.

    Returns:
        One row.
    """
    known = {
        **person.lab_values,
        "age": study_age(person.age),
        "sex": person.sex,
        "bmi": bmi(person.weight, person.height),
        **({} if person.habits is None else person.habits.model_dump()),
    }
    return pd.DataFrame([{column: known.get(column, np.nan) for column in columns}])


def study_age(age: int) -> int:
    """Nearest age of the study; the difference found for it is added to the real age.

    Args:
        age: Real age.

    Returns:
        The age, or the closest limit of the study.
    """
    return min(max(age, AGE_MIN), AGE_MAX)


def one_decimal(years: float | None) -> float | None:
    """Years with one decimal, never -0.0.

    Args:
        years: Years, or None if there are no data.

    Returns:
        The rounded years.
    """
    return None if years is None else round(float(years), 1) + 0.0
