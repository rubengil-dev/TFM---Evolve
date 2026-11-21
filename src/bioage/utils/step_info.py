"""What each pipeline step leaves: the saved data layer and the printed summary.

- Save a data layer
- Summary of Silver raw (per cycle), of Silver clean and Gold (per variable) and of a model
"""

# Imports
from pathlib import Path

import pandas as pd


def save_layer(table: pd.DataFrame, path: Path) -> None:
    """Data layer → parquet, creating its folder if needed.

    Args:
        table: Data layer.
        path: File to save it to.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_parquet(path, index=False)


def print_raw_summary(raw: pd.DataFrame, path: Path) -> None:
    """Print persons and deaths per cycle, then the totals.

    Args:
        raw: Silver raw table, still with NHANES names.
        path: File it was saved to.
    """
    summary = raw.groupby("cycle").agg(persons=("SEQN", "size"), deaths=("MORTSTAT", "sum")).astype(int)
    print(summary.to_string())
    print(f"\n{len(raw)} persons, {int(raw['MORTSTAT'].sum())} deaths, {raw.shape[1]} columns, saved to {path.name}")


def print_layer_summary(table: pd.DataFrame, path: Path) -> None:
    """Print persons, deaths, columns and % with value per variable.

    Args:
        table: Data layer just saved.
        path: File it was saved to.
    """
    print(f"{len(table)} persons, {int(table['death'].sum())} deaths, {table.shape[1]} columns, saved to {path.name}\n")
    coverage = (table.notna().mean() * 100).round(0).astype(int)
    print(coverage.to_string())


def print_model_summary(bundle: dict, path: Path) -> None:
    """Print the variables, people, training C-index, code and file of a level.

    Args:
        bundle: Saved bundle of the level.
        path: File it was saved to.
    """
    trained_on = bundle["trained_on"]
    print(
        f"{bundle['level']}: {len(bundle['columns'])} variables"
        f" | {trained_on['people']} people, {trained_on['deaths']} deaths"
        f" | C-index in training data {bundle['c_index_fit']:.4f} | code {trained_on['code']} | {path.name}"
    )
