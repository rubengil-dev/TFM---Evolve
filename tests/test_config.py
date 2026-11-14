"""
Configuration consistency, without data:
    - Every Gold predictor used by a model or discarded with its reason
    - Model variables with what the app needs to check them
    - One algorithm and one saved model per level
    - App requirements: the libraries of a saved model, at the versions of the analysis
"""

# Imports
from src.config.column_roles import DERIVED_FEATURES, SILVER_PREDICTORS
from src.config.model_sets import DISCARDED, LEVEL_COLUMNS, LEVEL_MODELS
from src.config.paths import ROOT, TRAINED_MODELS
from src.config.plausible_ranges import PLAUSIBLE_RANGES
from src.config.study import CATEGORICAL_LEVELS
from src.models.predict import LIBRARIES

GOLD_PREDICTORS = SILVER_PREDICTORS + DERIVED_FEATURES
MODEL_VARIABLES = set().union(*LEVEL_COLUMNS.values())


def test_model_variables_in_gold():
    """Every model variable is a Gold predictor."""
    assert MODEL_VARIABLES - set(GOLD_PREDICTORS) == set()


def test_every_gold_predictor_used_or_discarded():
    """No Gold predictor forgotten: each one is in a model or in DISCARDED."""
    assert set(GOLD_PREDICTORS) - MODEL_VARIABLES - set(DISCARDED) == set()


def test_no_variable_used_and_discarded():
    """A variable is either in a model or discarded, never both."""
    assert MODEL_VARIABLES & set(DISCARDED) == set()


def test_numeric_model_variables_have_plausible_range():
    """The app can check every numeric value it receives (age has its own limits)."""
    numeric = MODEL_VARIABLES - set(CATEGORICAL_LEVELS) - {"age"}
    assert numeric - set(PLAUSIBLE_RANGES) == set()


def test_every_level_has_algorithm_and_saved_model():
    """Same levels in LEVEL_COLUMNS and LEVEL_MODELS, each with its file in models/."""
    assert set(LEVEL_COLUMNS) == set(LEVEL_MODELS)
    assert all((TRAINED_MODELS / f"{level}.joblib").exists() for level in LEVEL_COLUMNS)


def test_app_requirements_are_the_model_libraries():
    """requirements.txt pins exactly the libraries checked when loading a model."""
    assert set(pinned("requirements.txt")) == set(LIBRARIES)


def test_app_and_analysis_requirements_match():
    """Each app library at the same version as in requirements-dev.txt."""
    analysis = pinned("requirements-dev.txt")
    assert {name: analysis.get(name) for name in pinned("requirements.txt")} == pinned("requirements.txt")


def pinned(file):
    """Library → version of a requirements file, comments left out."""
    lines = (ROOT / file).read_text().splitlines()
    return dict(line.split("==") for line in lines if line and not line.startswith("#"))
