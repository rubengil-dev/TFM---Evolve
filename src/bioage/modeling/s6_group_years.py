"""ML Pipeline: Step 6 - Years each group of variables adds or takes away.

Years of a group = (points its Cox weights give the person - the average at their age and sex) x years per point.

- `fit_group_reference` : Average points of each group by age and sex, when the model is trained.
- `group_years`         : Years of each group for one person.
- `years_per_hazard`    : Years one point is worth for a person.
- `group_hazards`       : Points of each group: the person against themselves with fixed values in it.
- `model_groups`        : Groups of a level.

NOTE: Points = log hazard. What no group explains goes to OTHER, so all of them add up to biological age - age.
"""

# Imports
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

from bioage.config.app import BLOOD_GROUPS, HABIT_GROUPS, OTHER
from bioage.modeling.s4_biological_age import (
    age_terms,
    log_cumulative_hazard,
    read_age,
    read_hazard,
    risk_at_horizon,
)

SMALL_HAZARD = 0.01  # below it, the rate is the slope of the curve


def fit_group_reference(pipeline: Pipeline, data: pd.DataFrame, columns: list[str]) -> dict[str, dict]:
    """Average log hazard each group adds, by age and sex.

    Args:
        pipeline: Fitted preprocessing and model.
        data: People it was fitted on, with their survey weight.
        columns: Columns of the model.

    Returns:
        Group → sex → curve: value at 50 years and its two age terms.
    """
    hazards = group_hazards(pipeline, data, columns)
    reference = {group: {} for group in hazards}
    for sex in ["female", "male"]:
        members = np.asarray(data["sex"] == sex)
        terms = age_terms(np.asarray(data["age"], dtype=float)[members])
        weights = np.asarray(data["weight_exam"], dtype=float)[members]
        for group in hazards:
            curve = LinearRegression().fit(terms, hazards.loc[members, group], sample_weight=weights)
            reference[group][sex] = np.array([curve.intercept_, *curve.coef_])
    return reference


def group_years(
    pipeline: Pipeline,
    person: pd.DataFrame,
    columns: list[str],
    reference: dict[str, np.ndarray],
    group_reference: dict[str, dict],
) -> dict[str, float | None]:
    """Years each group adds (+) or takes away (-) from one person; None = no data of that group.

    Args:
        pipeline: Fitted preprocessing and model.
        person: One row with the columns of the model.
        columns: Columns of the model.
        reference: Reference curves of the level.
        group_reference: Average hazard of each group, from fit_group_reference.

    Returns:
        Group → years, with OTHER.
    """
    age, sex = float(person["age"].iloc[0]), person["sex"].iloc[0]
    hazard = log_cumulative_hazard(risk_at_horizon(pipeline, person))
    difference = read_age(hazard, reference, sex)[0] - age
    rate = years_per_hazard(
        difference, hazard[0] - read_hazard(np.array([age]), reference, sex)[0], age, sex, reference
    )

    hazards = group_hazards(pipeline, person, columns).iloc[0]
    terms = np.array([1, *age_terms(np.array([age]))[0]])
    years = {}
    for group, members in model_groups(columns).items():
        is_known = person[members].notna().any(axis=None)
        years[group] = (hazards[group] - group_reference[group][sex] @ terms) * rate if is_known else None
    return {**years, OTHER: difference - sum(value for value in years.values() if value is not None)}


def years_per_hazard(difference: float, hazard: float, age: float, sex: str, reference: dict[str, np.ndarray]) -> float:
    """Years one unit of log hazard is worth for a person.

    Args:
        difference: Biological age - age.
        hazard: Log hazard of the person - the one of the typical person.
        age: Age of the person.
        sex: Sex of the person.
        reference: Reference curves of the level.

    Returns:
        Years per unit.
    """
    if abs(hazard) > SMALL_HAZARD:
        return difference / hazard
    low, high = read_hazard(np.array([age - 0.5, age + 0.5]), reference, sex)
    return 1 / (high - low)


def group_hazards(pipeline: Pipeline, data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Log hazard each group adds, against the overall fill values of its variables.

    Args:
        pipeline: Fitted preprocessing and Cox model.
        data: People with the columns of the model.
        columns: Columns of the model.

    Returns:
        One column per group.
    """
    fixed = pipeline.named_steps["preprocessing"].named_steps["fill_gaps"].overall_
    groups = model_groups(columns)
    versions = [data[columns].assign(**{column: fixed[column] for column in members}) for members in groups.values()]
    # All at once: predicting is slow to start
    total, *replaced = np.split(pipeline.predict(pd.concat([data[columns], *versions])), len(versions) + 1)
    return pd.DataFrame({group: total - rest for group, rest in zip(groups, replaced, strict=True)}, index=data.index)


def model_groups(columns: list[str]) -> dict[str, list[str]]:
    """Groups with the variables a model uses; OTHER left out.

    Args:
        columns: Columns of the model.

    Returns:
        Group → its columns.
    """
    groups = {
        group: [column for column in members if column in columns]
        for group, members in {**BLOOD_GROUPS, **HABIT_GROUPS}.items()
    }
    return {group: members for group, members in groups.items() if members and group != OTHER}
