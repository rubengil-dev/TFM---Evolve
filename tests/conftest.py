"""Shared test data, without data/.

- made_up_gold: small Gold with every column, valid values and a few gaps
- Without the training libraries (CI): the tests of training code are not collected
"""

# Imports
from importlib.util import find_spec

import numpy as np
import pandas as pd
import pytest

from bioage.config.gold_columns import DERIVED_FEATURES, ID_COLUMNS, OUTCOME_COLUMNS, SELECTED_PREDICTORS
from bioage.config.plausible_ranges import PLAUSIBLE_RANGES
from bioage.config.sources import CYCLES
from bioage.config.study import CATEGORICAL_LEVELS
from bioage.config.validation_rules import REQUIRED
from bioage.utils.features import derived_features
from bioage.utils.nhanes import cycle_label

TRAINING_LIBRARIES = ["lifelines", "matplotlib", "optuna", "requests", "xgboost"]
TRAINING_TESTS = [
    "models/test_s3_algorithms.py",
    "models/test_s5_evaluation.py",
    "pipeline/test_s1_download_bronze.py",
    "pipeline/test_s5_build_model.py",
    "utils/test_data_download.py",
    "utils/test_notebook_helpers.py",
]
collect_ignore = [] if all(find_spec(name) for name in TRAINING_LIBRARIES) else TRAINING_TESTS

PEOPLE = 600
GAPS = 0.03  # share of missing values in each optional column
OWN_VALUES = {"age", "weight", "height", "bmi", "waist", "sedentary_hours", "fast_food_meals", "alcohol_drinks"}


@pytest.fixture
def made_up_gold() -> pd.DataFrame:
    """Gold of PEOPLE made-up people that passes every check but size."""
    rng = np.random.default_rng(0)
    # fmt: off
    gold = pd.DataFrame({
        "seqn":              np.arange(1, PEOPLE + 1),
        "cycle":             rng.choice([cycle_label(year) for year in CYCLES], PEOPLE),
        "weight_exam":       rng.uniform(1000, 50000, PEOPLE),
        "follow_up_months":  rng.uniform(1, 240, PEOPLE).round(),
        "death":             rng.binomial(1, 0.15, PEOPLE),
        "age":               rng.integers(18, 80, PEOPLE),
        "sex":               rng.choice(CATEGORICAL_LEVELS["sex"], PEOPLE),
        "weight":            rng.uniform(50, 100, PEOPLE),
        "height":            rng.uniform(150, 190, PEOPLE),
        "waist":             rng.uniform(70, 110, PEOPLE),
        "sedentary_hours":   rng.integers(1, 13, PEOPLE),
        "fast_food_meals":   rng.integers(0, 6, PEOPLE),
    })
    # fmt: on
    gold["bmi"] = gold["weight"] / (gold["height"] / 100) ** 2
    for variable, (_, normal, _, _) in PLAUSIBLE_RANGES.items():
        if variable in SELECTED_PREDICTORS and variable not in OWN_VALUES:
            gold[variable] = rng.uniform(*normal, PEOPLE)
    for variable, answers in CATEGORICAL_LEVELS.items():
        if variable != "sex":
            gold[variable] = rng.choice(answers, PEOPLE).astype(object)
    gold["alcohol_drinks"] = np.where(gold["alcohol_frequency"] == "never", 0.0, rng.integers(1, 5, PEOPLE))
    gold = with_gaps(gold, rng)
    gold = pd.concat([gold, derived_features(gold)], axis=1)
    return gold[ID_COLUMNS + OUTCOME_COLUMNS + SELECTED_PREDICTORS + DERIVED_FEATURES]


def with_gaps(gold: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """GAPS of each optional column → missing."""
    for column in gold.columns.difference(REQUIRED):
        gold[column] = gold[column].mask(rng.random(len(gold)) < GAPS)
    return gold
