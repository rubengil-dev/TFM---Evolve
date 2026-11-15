"""
Configuration consistency, without data:
    - Every Gold predictor used by a model or discarded with its reason
    - Model variables with what the app needs to check them
    - One algorithm and one saved model per level
    - App dependencies: the libraries of a saved model, each pinned to one version
"""

# Imports
import tomllib

from bioage.config.column_roles import DERIVED_FEATURES, SILVER_PREDICTORS
from bioage.config.model_sets import DISCARDED, LEVEL_COLUMNS, LEVEL_MODELS
from bioage.config.paths import ROOT, TRAINED_MODELS
from bioage.config.plausible_ranges import PLAUSIBLE_RANGES
from bioage.config.study import CATEGORICAL_LEVELS
from bioage.models.predict import LIBRARIES

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


def test_app_dependencies_are_the_model_libraries():
    """pyproject.toml pins, as app dependencies, exactly the libraries checked when loading a model."""
    assert set(app_dependencies()) == set(LIBRARIES)


def app_dependencies():
    """Library → pinned version of the project dependencies in pyproject.toml (the app ones)."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    return dict(dependency.split("==") for dependency in project["dependencies"])
