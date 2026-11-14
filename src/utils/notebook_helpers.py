"""
Helpers shared by the working notebooks of the model (lifelines, analysis only):
    - cox_weights: hazard ratio of each feature with its 95% interval
    - variable_of: Gold variable behind a feature
    - without: a list of columns minus some
"""

# Imports
import pandas as pd
from lifelines import CoxPHFitter

from src.models.s2_preprocessing import build_preprocessor


def cox_weights(columns, data, expected_signs=None):
    """
    Cox fitted on the preprocessed columns of data → one row per feature:
        - hazard_ratio, low, high, p; clear: interval excludes 1
        - With expected_signs (feature → 'above' / 'below'): variable, expected and contrary (clearly the other way)
    """
    features = build_preprocessor(columns).fit_transform(data)
    fitted = CoxPHFitter().fit(features.join(data[["follow_up_months", "death"]]), "follow_up_months", "death").summary
    weights = pd.DataFrame({
        "hazard_ratio": fitted["exp(coef)"],
        "low": fitted["exp(coef) lower 95%"],
        "high": fitted["exp(coef) upper 95%"],
        "p": fitted["p"],
    })
    weights["clear"] = (weights["low"] > 1) | (weights["high"] < 1)
    if expected_signs is not None:
        weights = add_signs(weights, columns, expected_signs)
    return weights


def add_signs(weights, columns, expected_signs):
    """Variable of each feature, its expected sign and whether the fit clearly goes the other way."""
    weights["variable"] = [variable_of(feature, columns) for feature in weights.index]
    weights["expected"] = pd.Series(expected_signs).reindex(weights.index)
    weights["contrary"] = (
        ((weights["expected"] == "above") & (weights["high"] < 1)) | ((weights["expected"] == "below") & (weights["low"] > 1))
    )
    return weights


def variable_of(feature, columns):
    """
    Gold variable behind a feature, the longest match:
        Example: 'smoking_current' → 'smoking'
    """
    return next(column for column in sorted(columns, key=len, reverse=True) if feature == column or feature.startswith(column + "_"))


def without(columns, removed):
    """columns in their order, minus those in removed."""
    return [column for column in columns if column not in removed]
