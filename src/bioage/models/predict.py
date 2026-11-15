"""Prediction with a saved model, what the app uses (no training libraries).

- Saved model of a level, checked against the installed library versions
- People → 10-year risk → biological age
"""

# Imports
from importlib.metadata import version
from platform import python_version_tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from bioage.config.paths import TRAINED_MODELS
from bioage.config.study import HORIZON_MONTHS
from bioage.models.s4_biological_age import biological_age

LIBRARIES = [
    "numpy",
    "pandas",
    "scipy",
    "scikit-learn",
    "scikit-survival",
    "joblib",
]  # the ones a saved model depends on


def load_bundle(level: str) -> dict:
    """Saved model of a level; fails if it was saved with other library versions.

    Args:
        level: Name of the level.

    Returns:
        Bundle of the level.
    """
    bundle = joblib.load(TRAINED_MODELS / f"{level}.joblib")
    check_versions(bundle["versions"])
    return bundle


def predict_age(bundle: dict, data: pd.DataFrame) -> np.ndarray:
    """People → biological age with the model of a level.

    Args:
        bundle: Bundle of the level.
        data: People with the columns of the level.

    Returns:
        Biological age of each person.
    """
    risk = risk_at_horizon(bundle["pipeline"], data)
    return biological_age(risk, data["sex"], bundle["reference"])


def check_versions(saved: dict[str, str]) -> None:
    """Fail listing every library whose installed version differs from the saved one.

    Args:
        saved: Versions the model was saved with.

    Raises:
        RuntimeError: If any version differs.
    """
    installed = library_versions()
    different = [
        f"{name} {saved[name]} saved, {installed.get(name)} installed"
        for name in saved
        if saved[name] != installed.get(name)
    ]
    if different:
        raise RuntimeError("Model saved with other library versions: " + "; ".join(different))


def library_versions() -> dict[str, str]:
    """Python (major.minor) and the version of each library in LIBRARIES.

    Returns:
        Name → version.
    """
    return {"python": ".".join(python_version_tuple()[:2]), **{name: version(name) for name in LIBRARIES}}


def risk_at_horizon(pipeline: Pipeline, data: pd.DataFrame) -> np.ndarray:
    """Probability of dying within the horizon, for each person.

    Args:
        pipeline: Fitted preprocessing and model.
        data: People with the columns of the model.

    Returns:
        Risk of each person.
    """
    curves = pipeline.predict_survival_function(data)
    return 1 - np.array([curve(HORIZON_MONTHS) for curve in curves])
