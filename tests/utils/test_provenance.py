"""Tests: Utils - Provenance of the saved models.

- Data fingerprint: same data → same fingerprint; one value, one column name or the row order changed → another
- Saved library versions: exactly the app dependencies in pyproject.toml, plus Python
- App dependencies pinned to one version (a dependency without == fails to read)
"""

# Imports
import tomllib

import pandas as pd

from bioage.config.paths import ROOT
from bioage.utils.provenance import data_fingerprint, library_versions


def test_fingerprint_follows_the_data(made_up_gold: pd.DataFrame) -> None:
    fingerprint = data_fingerprint(made_up_gold)
    changed_value = made_up_gold.copy()
    changed_value.loc[0, "glucose"] += 1
    assert data_fingerprint(made_up_gold.copy()) == fingerprint
    assert data_fingerprint(changed_value) != fingerprint
    assert data_fingerprint(made_up_gold.rename(columns={"glucose": "glucosa"})) != fingerprint
    assert data_fingerprint(made_up_gold.iloc[::-1]) != fingerprint


def test_saved_versions_cover_every_app_dependency() -> None:
    assert set(library_versions()) == {"python", *app_dependencies()}


def app_dependencies() -> dict[str, str]:
    """Library → pinned version of the project dependencies in pyproject.toml (the app ones)."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    return dict(dependency.split("==") for dependency in project["dependencies"])
