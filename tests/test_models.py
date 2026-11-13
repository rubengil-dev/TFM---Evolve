"""
Saved models, as the app uses them:
    - Same biological age as the reference for a few made-up people (REFERENCE_AGES)
    - Prediction without the training libraries
    - After a deliberate retrain or preprocessing change: write_reference() and review the diff
"""

# Imports
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.config.model_sets import LEVEL_COLUMNS
from src.config.paths import ROOT
from src.models.predict import load_bundle, predict_age

REFERENCE_AGES = Path(__file__).parent / "reference_ages.json"
TOLERANCE = 0.01  # years

# Made-up people: every column of the full model; missing values on purpose
PEOPLE = pd.DataFrame({
    # variable               healthy_young  typical_middle  unhealthy_old  partial_data   age_sex_only   older_than_79
    "age":                   [25,           45,             70,            60,            50,            85],
    "sex":                   ["female",     "male",         "male",        "female",      "female",      "male"],
    "bmi":                   [22.0,         27.5,           33.0,          26.0,          np.nan,        25.0],
    "hemoglobin":            [13.5,         15.0,           12.5,          13.0,          np.nan,        14.0],
    "erythrocytes":          [4.5,          5.0,            4.1,           4.4,           np.nan,        4.6],
    "mchc":                  [33.5,         34.0,           33.0,          33.5,          np.nan,        33.5],
    "neutrophils":           [3.2,          4.0,            6.5,           3.8,           np.nan,        4.2],
    "lymphocytes":           [2.2,          2.0,            1.3,           2.1,           np.nan,        1.8],
    "monocytes":             [0.45,         0.5,            0.8,           0.5,           np.nan,        0.6],
    "glucose":               [85,           98,             160,           102,           np.nan,        105],
    "creatinine":            [0.75,         1.0,            1.6,           0.8,           np.nan,        1.2],
    "urea":                  [28,           35,             60,            32,            np.nan,        45],
    "uric_acid":             [4.2,          6.0,            7.8,           5.0,           np.nan,        6.2],
    "hdl":                   [65,           48,             35,            58,            np.nan,        50],
    "ast":                   [18,           24,             35,            22,            np.nan,        25],
    "alt":                   [15,           28,             30,            20,            np.nan,        18],
    "sodium":                [140,          140,            137,           141,           np.nan,        139],
    "potassium":             [4.2,          4.3,            4.9,           4.4,           np.nan,        4.5],
    "ggt":                   [14,           30,             90,            22,            np.nan,        28],
    "alkaline_phosphatase":  [60,           75,             120,           np.nan,        np.nan,        85],
    "albumin":               [4.5,          4.3,            3.6,           np.nan,        np.nan,        4.0],
    "vitamin_d":             [32,           24,             14,            np.nan,        np.nan,        22],
    "chloride":              [103,          102,            100,           np.nan,        np.nan,        102],
    "phosphorus":            [3.6,          3.3,            3.9,           np.nan,        np.nan,        3.4],
    "ldh":                   [160,          180,            240,           np.nan,        np.nan,        200],
    "urine_acr":             [6,            10,             150,           np.nan,        np.nan,        25],
    "systolic_bp":           [110,          125,            155,           130,           np.nan,        140],
    "diastolic_bp":          [70,           80,             88,            82,            np.nan,        78],
    "smoking":               ["never",      "former",       "current",     np.nan,        np.nan,        "former"],
    "physical_activity":     ["intense",    "moderate",     "sedentary",   np.nan,        np.nan,        "moderate"],
    "sedentary_hours":       [5,            7,              11,            np.nan,        np.nan,        8],
    "sleep_hours":           [8,            7,              5,             np.nan,        np.nan,        7],
}, index=["healthy_young", "typical_middle", "unhealthy_old", "partial_data", "age_sex_only", "older_than_79"])


@pytest.mark.parametrize("level", LEVEL_COLUMNS)
def test_ages_match_reference(level):
    """Biological age of each made-up person within TOLERANCE of the reference."""
    expected = json.loads(REFERENCE_AGES.read_text())[level]
    ages = pd.Series(predict_age(load_bundle(level), PEOPLE), index=PEOPLE.index)
    assert np.isfinite(ages).all()
    assert ages.to_dict() == pytest.approx(expected, abs=TOLERANCE)


def test_prediction_without_training_libraries():
    """Loading a model and predicting does not import xgboost, optuna or matplotlib."""
    code = (
        "import sys; from src.models.predict import load_bundle; load_bundle('full'); "
        "print([name for name in ('xgboost', 'optuna', 'matplotlib') if name in sys.modules])"
    )
    result = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, check=True)
    assert result.stdout.strip() == "[]"


def write_reference():
    """Current biological age of each made-up person and level → REFERENCE_AGES."""
    reference = {
        level: {person: round(float(age), 4) for person, age in zip(PEOPLE.index, predict_age(load_bundle(level), PEOPLE))}
        for level in LEVEL_COLUMNS
    }
    REFERENCE_AGES.write_text(json.dumps(reference, indent=4) + "\n", newline="\n")
