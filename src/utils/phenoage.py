"""
PhenoAge (Levine et al., 2018), the external reference of the model:
    - Fixed formula from NHANES III, nothing to train
    - Our Spanish lab units → the units of the paper before applying it
"""

# Imports
import numpy as np
import pandas as pd

from src.config.study import HORIZON_MONTHS

PHENOAGE_VARIABLES = ["albumin", "creatinine", "glucose", "crp", "lymphocytes", "leukocytes", "mcv", "rdw", "alkaline_phosphatase"]

PHENOAGE_WEIGHTS = {
    "albumin":              -0.0336,
    "creatinine":            0.0095,
    "glucose":               0.1953,
    "log_crp":               0.0954,
    "lymphocyte_percent":   -0.0120,
    "mcv":                   0.0268,
    "rdw":                   0.3306,
    "alkaline_phosphatase":  0.00188,
    "leukocytes":            0.0554,
    "age":                   0.0804,
}
PHENOAGE_INTERCEPT = -19.9067
GOMPERTZ_GAMMA = 0.0076927


def phenoage_score(data):
    """Risk score; orders people like the risk, without rounding it to 1."""
    return PHENOAGE_INTERCEPT + phenoage_inputs(data).mul(PHENOAGE_WEIGHTS).sum(axis=1)


def phenoage_risk(score):
    """Score → probability of dying within the horizon."""
    return 1 - np.exp(-np.exp(score) * (np.exp(HORIZON_MONTHS * GOMPERTZ_GAMMA) - 1) / GOMPERTZ_GAMMA)


def phenoage(score):
    """
    Score → age at which the NHANES III population has that risk:
        Same as 141.50225 + log(-0.00553 * log(1 - risk)) / 0.090165, without rounding the risk to 1
    """
    log_hazard = score + np.log((np.exp(HORIZON_MONTHS * GOMPERTZ_GAMMA) - 1) / GOMPERTZ_GAMMA)
    return 141.50225 + (np.log(0.00553) + log_hazard) / 0.090165


def phenoage_inputs(data):
    """Our units → the units of the paper (albumin g/L, creatinine µmol/L, glucose mmol/L, log CRP mg/dL, lymphocyte %)."""
    return pd.DataFrame({
        "albumin": data["albumin"] * 10,
        "creatinine": data["creatinine"] * 88.4,
        "glucose": data["glucose"] / 18.016,
        "log_crp": np.log(data["crp"].clip(lower=0.08) / 10),
        "lymphocyte_percent": data["lymphocytes"] / data["leukocytes"] * 100,
        "mcv": data["mcv"],
        "rdw": data["rdw"],
        "alkaline_phosphatase": data["alkaline_phosphatase"],
        "leukocytes": data["leukocytes"],
        "age": data["age"],
    })
