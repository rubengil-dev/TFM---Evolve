"""Prediction with a saved model, what the app uses (no training libraries).

- Saved model of a level, checked against the installed library versions
- People → 10-year risk → biological age
"""

# Imports
import joblib
import numpy as np
import pandas as pd

from bioage.config.paths import TRAINED_MODELS
from bioage.models.s4_biological_age import biological_age, risk_at_horizon
from bioage.utils.provenance import library_versions


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
