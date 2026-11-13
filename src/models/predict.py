"""
Prediction with a saved model, what the app uses (no training libraries):
    - Saved model of a level, checked against the installed library versions
    - People → 10-year risk → biological age
"""

# Imports
from importlib.metadata import version
from platform import python_version_tuple

import joblib
import numpy as np

from src.config.paths import TRAINED_MODELS
from src.config.study import HORIZON_MONTHS
from src.models.s4_biological_age import biological_age

LIBRARIES = ["numpy", "pandas", "scipy", "scikit-learn", "scikit-survival", "joblib"]  # the ones a saved model depends on


def load_bundle(level):
    """Saved model of a level; fails if it was saved with other library versions."""
    bundle = joblib.load(TRAINED_MODELS / f"{level}.joblib")
    check_versions(bundle["versions"])
    return bundle


def predict_age(bundle, data):
    """People → biological age with the model of a level."""
    risk = risk_at_horizon(bundle["pipeline"], data)
    return biological_age(risk, data["sex"], bundle["reference"])


def check_versions(saved):
    """Error listing every library whose installed version differs from the saved one."""
    installed = library_versions()
    different = [f"{name} {saved[name]} saved, {installed.get(name)} installed" for name in saved if saved[name] != installed.get(name)]
    if different:
        raise RuntimeError("Model saved with other library versions: " + "; ".join(different))


def library_versions():
    """Python (major.minor) and the version of each library in LIBRARIES."""
    return {"python": ".".join(python_version_tuple()[:2]), **{name: version(name) for name in LIBRARIES}}


def risk_at_horizon(pipeline, data):
    """Probability of dying within the horizon, for each person."""
    curves = pipeline.predict_survival_function(data)
    return 1 - np.array([curve(HORIZON_MONTHS) for curve in curves])
