"""PhenoAge (Levine et al., 2018), the external reference of the model.

- Fixed formula from NHANES III, nothing to train (constants in config/phenoage.py)
- Our Spanish lab units → the units of the paper before applying it
"""

# Imports
import numpy as np
import pandas as pd

from bioage.config.phenoage import (
    AGE_CURVE_FACTOR,
    AGE_CURVE_INTERCEPT,
    AGE_CURVE_SLOPE,
    CRP_MIN,
    GOMPERTZ_GAMMA,
    PHENOAGE_HORIZON_MONTHS,
    PHENOAGE_INTERCEPT,
    PHENOAGE_WEIGHTS,
    UNIT_FACTORS,
)


def phenoage_score(data: pd.DataFrame) -> pd.Series:
    """Risk score; orders people like the risk, which rounds to 1 for the highest scores.

    Args:
        data: People with PHENOAGE_VARIABLES and age, in Gold units.

    Returns:
        Score of each person.
    """
    return PHENOAGE_INTERCEPT + phenoage_inputs(data).mul(PHENOAGE_WEIGHTS).sum(axis=1)


def phenoage_risk(score: pd.Series) -> pd.Series:
    """Score → probability of dying within the paper's horizon.

    Args:
        score: PhenoAge risk score.

    Returns:
        Risk of each person.
    """
    return 1 - np.exp(-np.exp(score) * gompertz_months())


def phenoage(score: pd.Series) -> pd.Series:
    """Score → age at which the NHANES III population has that risk.

    Same as the age curve on phenoage_risk(score), computed from the score so a risk rounded to 1 stays finite.

    Args:
        score: PhenoAge risk score.

    Returns:
        PhenoAge of each person, in years.
    """
    log_hazard = score + np.log(gompertz_months())
    return AGE_CURVE_INTERCEPT + (np.log(AGE_CURVE_FACTOR) + log_hazard) / AGE_CURVE_SLOPE


def phenoage_inputs(data: pd.DataFrame) -> pd.DataFrame:
    """Our units → the units of the paper.

    Args:
        data: People with PHENOAGE_VARIABLES and age, in Gold units.

    Returns:
        One column per PhenoAge weight.
    """
    return pd.DataFrame(
        {
            "albumin": data["albumin"] * UNIT_FACTORS["albumin"],
            "creatinine": data["creatinine"] * UNIT_FACTORS["creatinine"],
            "glucose": data["glucose"] * UNIT_FACTORS["glucose"],
            "log_crp": np.log(data["crp"].clip(lower=CRP_MIN) * UNIT_FACTORS["crp"]),
            "lymphocyte_percent": data["lymphocytes"] / data["leukocytes"] * 100,
            "mcv": data["mcv"],
            "rdw": data["rdw"],
            "alkaline_phosphatase": data["alkaline_phosphatase"],
            "leukocytes": data["leukocytes"],
            "age": data["age"],
        }
    )


def gompertz_months() -> float:
    """Gompertz cumulative hazard factor over the paper's horizon.

    Returns:
        (exp(horizon × gamma) - 1) / gamma.
    """
    return (np.exp(PHENOAGE_HORIZON_MONTHS * GOMPERTZ_GAMMA) - 1) / GOMPERTZ_GAMMA
