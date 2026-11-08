"""
Step 4, biological age, the same for every algorithm:
    - 10-year mortality risk → age at which the typical person of the same sex has that risk
    - Typical person: the median of what the same model gives to people of each age and sex
"""

# Imports
import numpy as np
from sklearn.linear_model import QuantileRegressor

from src.config.study import AGE_MAX, AGE_MIN

AGE_STEP = 0.01  # years, resolution of the reference curve


def fit_reference(risk, data):
    """
    Typical person of each sex, from the model's risk in train:
        - Risk → log of the cumulative hazard, which grows almost in a straight line with age
        - Median curve of second degree per sex, over the study ages
    """
    hazard = log_cumulative_hazard(risk)
    ages = np.arange(AGE_MIN, AGE_MAX + AGE_STEP, AGE_STEP)
    reference = {"ages": ages}
    for sex in ["female", "male"]:
        members = np.asarray(data["sex"] == sex)
        curve = QuantileRegressor(quantile=0.5, alpha=0, solver="highs")
        curve.fit(age_terms(np.asarray(data["age"], dtype=float)[members]), hazard[members])
        reference[sex] = curve.predict(age_terms(ages))
        if np.any(np.diff(reference[sex]) <= 0):
            raise ValueError(f"Reference curve of {sex} does not always grow with age")
    return reference


def biological_age(risk, sex, reference):
    """
    Risk at the horizon → age at which the typical person of the same sex has it:
        - Inside the study ages: read from the curve
        - Outside: the curve goes on in a straight line, so extreme risks give ages below 18 or above 79
    """
    hazard = log_cumulative_hazard(risk)
    is_male = np.asarray(sex) == "male"
    return np.where(is_male, read_age(hazard, reference, "male"), read_age(hazard, reference, "female"))


def reference_risk(age, sex, reference):
    """Risk at the horizon of the typical person of that age and sex."""
    age = np.asarray(age, dtype=float)
    is_male = np.asarray(sex) == "male"
    hazard = np.where(is_male, read_hazard(age, reference, "male"), read_hazard(age, reference, "female"))
    return 1 - np.exp(-np.exp(hazard))


def log_cumulative_hazard(risk):
    """Risk at the horizon → log(-log(1 - risk))."""
    risk = np.clip(np.asarray(risk, dtype=float), 1e-12, 1 - 1e-12)
    return np.log(-np.log(1 - risk))


def age_terms(age):
    """Age and age squared, centred at 50 to keep the numbers small."""
    centred = age - 50
    return np.column_stack([centred, centred ** 2])


def read_age(hazard, reference, sex):
    """Hazard → age on the curve of one sex, straight beyond its ends."""
    ages, curve = reference["ages"], reference[sex]
    low_slope, high_slope = end_slopes(ages, curve)
    inside = np.interp(hazard, curve, ages)
    below = ages[0] + (hazard - curve[0]) / low_slope
    above = ages[-1] + (hazard - curve[-1]) / high_slope
    return np.select([hazard < curve[0], hazard > curve[-1]], [below, above], inside)


def read_hazard(age, reference, sex):
    """Age → hazard on the curve of one sex, straight beyond its ends."""
    ages, curve = reference["ages"], reference[sex]
    low_slope, high_slope = end_slopes(ages, curve)
    inside = np.interp(age, ages, curve)
    below = curve[0] + (age - ages[0]) * low_slope
    above = curve[-1] + (age - ages[-1]) * high_slope
    return np.select([age < ages[0], age > ages[-1]], [below, above], inside)


def end_slopes(ages, curve):
    """Slope of the curve at its youngest and oldest ages."""
    return (curve[1] - curve[0]) / (ages[1] - ages[0]), (curve[-1] - curve[-2]) / (ages[-1] - ages[-2])
