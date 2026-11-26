"""Person → result: picks the model and calculates the biological age, its margin and the years of each group."""

# Imports
import math

import numpy as np
import pandas as pd

from bioage.app.predict import predict_age, predict_groups, predict_risk
from bioage.app.schemas import Person, Result
from bioage.app.utils import bmi, extras_known, max_missing, routine_missing
from bioage.app.validation import check_person
from bioage.config.app import BLOOD_GROUPS, EXTRAS_LEVELS, HABIT_GROUPS, MODE_LEVELS
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
    check_person(person, max_missing(bundles, person.mode))
    bundle = bundles[choose_level(person, bundles)]
    row = model_row(person, bundle["columns"])
    years = predict_groups(bundle, row)
    return Result(  # age and margin unrounded: the front rounds them once, to whole years
        age=person.age,
        bio_age=float(predict_age(bundle, row)[0] + person.age - study_age(person.age)),
        margin=float(margin(person, bundle, predict_risk(bundle, row)[0])),
        blood={group: one_decimal(years.get(group)) for group in BLOOD_GROUPS},
        habits=None if person.habits is None else {group: one_decimal(years[group]) for group in HABIT_GROUPS},
    )


def choose_level(person: Person, bundles: dict[str, dict]) -> str:
    """Level whose model is used: with Extras if there are enough of them to make it better.

    Args:
        person: Data of the person.
        bundles: Bundle of each level.

    Returns:
        Name of the level.
    """
    level = MODE_LEVELS[person.mode]
    with_extras = EXTRAS_LEVELS[level]
    is_enough = extras_known(set(person.lab_values)) >= bundles[with_extras]["margin"]["min_extras"]
    return with_extras if is_enough else level


def margin(person: Person, bundle: dict, risk: float) -> float:
    """Margin ± of the biological age: base error and error for what is missing, from the bundle of the level.

    Args:
        person: Data of the person.
        bundle: Bundle of the level used.
        risk: 10-year risk of the person.

    Returns:
        Years.
    """
    parts = bundle["margin"]
    base = np.interp(risk, parts["base"]["risk"], parts["base"]["years"])  # straight lines between tenths
    known = set(person.lab_values)
    missing = parts["routine_missing"][routine_missing(known)]
    extras = parts["extras_known"][extras_known(known)] if "extras_known" in parts else 0
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
