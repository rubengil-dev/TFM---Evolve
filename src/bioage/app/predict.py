"""Predicts 10-year risk with a saved model and turns it into biological age and years of each group."""

# Imports
import joblib
import numpy as np
import pandas as pd

from bioage.config.paths import TRAINED_MODELS
from bioage.modeling.s4_biological_age import biological_age, risk_at_horizon
from bioage.modeling.s6_group_years import group_years
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
    return biological_age(predict_risk(bundle, data), data["sex"], bundle["reference"])


def predict_risk(bundle: dict, data: pd.DataFrame) -> np.ndarray:
    """People → 10-year risk with the model of a level.

    Args:
        bundle: Bundle of the level.
        data: People with the columns of the level.

    Returns:
        Risk of each person.
    """
    return risk_at_horizon(bundle["pipeline"], data)


def predict_groups(bundle: dict, person: pd.DataFrame) -> dict[str, float | None]:
    """One person → years each group adds or takes away, with the model of a level.

    Args:
        bundle: Bundle of the level.
        person: One row with the columns of the level.

    Returns:
        Group → years; None = no data of that group.
    """
    return group_years(bundle["pipeline"], person, bundle["columns"], bundle["reference"], bundle["group_reference"])


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
