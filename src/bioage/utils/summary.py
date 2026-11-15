"""Summary printed after saving a data layer."""

# Imports
from pathlib import Path

import pandas as pd


def print_layer_summary(table: pd.DataFrame, path: Path) -> None:
    """Print persons, deaths, columns and % with value per variable.

    Args:
        table: Data layer just saved.
        path: File it was saved to.
    """
    print(f"{len(table)} persons, {int(table['death'].sum())} deaths, {table.shape[1]} columns, saved to {path.name}\n")
    coverage = (table.notna().mean() * 100).round(0).astype(int)
    print(coverage.to_string())
