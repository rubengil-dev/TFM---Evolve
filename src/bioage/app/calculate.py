"""Person → result: picks the model and calculates the biological age."""

# Imports
import numpy as np
import pandas as pd

from bioage.app.predict import predict_age
from bioage.app.schemas import Person, Result
from bioage.app.validation import check_age


def calculate(person: Person, bundles: dict[str, dict]) -> Result:
    """Biological age of a person, with the model their data allow.

    Args:
        person: Data of the person.
        bundles: Bundle of each level.

    Returns:
        Result to show.

    Raises:
        AppError: If the app does not calculate for that age.
    """
    check_age(person.age)
    bundle = bundles[choose_level(person)]
    bio_age = predict_age(bundle, model_row(person, bundle["columns"]))[0]
    return Result(
        age=person.age,
        bio_age=round(float(bio_age), 1),
        blood={},  # not calculated yet
        habits=None if person.habits is None else {},
    )


def choose_level(person: Person) -> str:
    """Level whose model is used (Extras not used yet).

    Args:
        person: Data of the person.

    Returns:
        Name of the level.
    """
    return "routine" if person.habits is None else "questionnaire"


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
        "age": person.age,
        "sex": person.sex,
        "bmi": person.weight / (person.height / 100) ** 2,
        **({} if person.habits is None else person.habits.model_dump()),
    }
    return pd.DataFrame([{column: known.get(column, np.nan) for column in columns}])
