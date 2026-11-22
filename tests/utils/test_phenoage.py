"""Tests: Utils - PhenoAge, the external reference.

- Our shortcut from the score gives the same age as the paper's age curve on the risk
- Units: Gold units converted to the paper's by hand; CRP below the detection limit kept finite
- Highest scores: the risk rounds to 1, the age stays finite and keeps growing
- Its own 120-month horizon, apart from ours
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.config import phenoage as config
from bioage.config.phenoage import AGE_CURVE_FACTOR, AGE_CURVE_INTERCEPT, AGE_CURVE_SLOPE
from bioage.utils import phenoage as module
from bioage.utils.phenoage import phenoage, phenoage_inputs, phenoage_risk, phenoage_score

PERSON = pd.DataFrame(
    {
        "albumin": [4.2],  # g/dL
        "creatinine": [1.0],  # mg/dL
        "glucose": [90.08],  # mg/dL
        "crp": [10.0],  # mg/L
        "lymphocytes": [2.0],
        "leukocytes": [8.0],
        "mcv": [90.0],
        "rdw": [13.0],
        "alkaline_phosphatase": [70.0],
        "age": [50.0],
    }
)


def test_shortcut_equals_the_paper_age_curve() -> None:
    score = pd.Series([-12.0, -9.0, -6.0, -3.0])
    paper = AGE_CURVE_INTERCEPT + np.log(-AGE_CURVE_FACTOR * np.log(1 - phenoage_risk(score))) / AGE_CURVE_SLOPE
    assert phenoage(score).tolist() == pytest.approx(paper.tolist())


def test_units_converted_by_hand() -> None:
    inputs = phenoage_inputs(PERSON).iloc[0]
    assert inputs["albumin"] == pytest.approx(42)
    assert inputs["creatinine"] == pytest.approx(88.4)
    assert inputs["glucose"] == pytest.approx(5)
    assert inputs["log_crp"] == pytest.approx(np.log(1))
    assert inputs["lymphocyte_percent"] == pytest.approx(25)


def test_crp_below_detection_limit_finite() -> None:
    assert np.isfinite(phenoage_score(PERSON.assign(crp=0.0))).all()


def test_highest_scores_finite_and_growing() -> None:
    score = pd.Series([2.0, 3.0])
    assert (phenoage_risk(score) == 1).all()
    ages = phenoage(score)
    assert np.isfinite(ages).all() and ages.iloc[1] > ages.iloc[0]


def test_own_horizon_of_120_months() -> None:
    assert config.PHENOAGE_HORIZON_MONTHS == 120
    assert not hasattr(module, "HORIZON_MONTHS")  # ours never reaches the formula
