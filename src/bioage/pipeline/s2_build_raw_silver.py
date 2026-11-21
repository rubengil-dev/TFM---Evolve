"""Build silver raw data layer.

Every Bronze file in one table with one row per person.

Changes:
- Files of each cycle joined by SEQN on DEMO participants (mortality included, DXA averaged)
- Adults AGE_MIN-AGE_MAX eligible for mortality follow-up
- Variable alias standardization, so each variable has the same name in every cycle
- Cycles stacked and saved to data/02_silver/silver_raw.parquet
"""

# Imports
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from bioage.config.paths import BRONZE, SILVER_RAW
from bioage.config.renames import CYCLE_ALIASES
from bioage.config.sources import CYCLES, DATASETS, MORTALITY_FILE
from bioage.config.study import AGE_MAX, AGE_MIN
from bioage.utils.nhanes import cycle_label, dxa_average_imputations, read_mortality, read_xpt
from bioage.utils.step_info import print_raw_summary, save_layer

logger = logging.getLogger(__name__)


def run() -> None:
    """Silver raw step, called from main."""
    cycles = []
    for year in CYCLES:
        table = merge_cycle_files(year)
        table = filter_population(table)
        table = rename_aliases(table)
        cycles.append(table)

    raw = pd.concat(cycles, ignore_index=True)
    save_layer(raw, SILVER_RAW)
    print_raw_summary(raw, SILVER_RAW)


def merge_cycle_files(year: int) -> pd.DataFrame:
    """All files of a cycle → one table.

    - DEMO participants as base, every other file joined by SEQN
    - 'cycle' column added

    Args:
        year: Start year of the cycle.

    Returns:
        One row per participant of the cycle.
    """
    logger.info("%s...", cycle_label(year))
    folder = BRONZE / cycle_label(year)

    # NHANES files
    merged = read_dataset(folder, "DEMO", year)
    for dataset, names in DATASETS.items():
        if dataset != "DEMO" and names[CYCLES.index(year)] is not None:
            merged = merge_table(merged, read_dataset(folder, dataset, year), dataset)

    # Mortality
    mortality = read_mortality(folder / MORTALITY_FILE.format(cycle=cycle_label(year)))
    merged = merge_table(merged, mortality, "MORT")

    merged = merged.copy()  # defragment after many column updates
    merged.insert(1, "cycle", cycle_label(year))
    return merged


def read_dataset(folder: Path, dataset: str, year: int) -> pd.DataFrame:
    """One NHANES file of the cycle, DXA imputations averaged.

    Args:
        folder: Bronze folder of the cycle.
        dataset: Dataset key in DATASETS.
        year: Start year of the cycle.

    Returns:
        Table of the file.
    """
    name = DATASETS[dataset][CYCLES.index(year)]
    return dxa_average_imputations(read_xpt(folder / f"{name}.xpt"))


def merge_table(merged: pd.DataFrame, table: pd.DataFrame, dataset: str) -> pd.DataFrame:
    """Left join by SEQN.

    Columns already in merged:
    - Same values where both exist → missing values filled, column not repeated
    - Different values → kept as NAME_DATASET

    Args:
        merged: Table built so far.
        table: Table to join.
        dataset: Dataset key, used as suffix for the conflicting columns.

    Returns:
        The joined table.

    Raises:
        ValueError: If table has more than one row per SEQN.
    """
    merged = merged.set_index("SEQN")
    table = table.set_index("SEQN")
    if not table.index.is_unique:
        raise ValueError(f"{dataset}: more than one row per SEQN")

    for col in table.columns.intersection(merged.columns):
        new = table[col].reindex(merged.index)
        both = merged[col].notna() & new.notna()
        if same_values(merged.loc[both, col], new[both]):
            merged[col] = merged[col].fillna(new)
            table = table.drop(columns=col)
        else:
            table = table.rename(columns={col: f"{col}_{dataset}"})
            logger.info("    %s: %s differs from an earlier file, kept as %s_%s", dataset, col, col, dataset)

    return merged.join(table, how="left").reset_index()


def same_values(a: pd.Series, b: pd.Series) -> bool:
    """Equal values, allowing rounding differences in numbers (e.g. 14084.10 vs 14084.2).

    Args:
        a: Values of one table.
        b: Values of the other, for the same people.

    Returns:
        True if they can be taken as the same column.
    """
    if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):
        return np.allclose(a, b, rtol=1e-4)
    return a.equals(b)


def filter_population(table: pd.DataFrame) -> pd.DataFrame:
    """Adults AGE_MIN-AGE_MAX eligible for mortality follow-up.

    Args:
        table: Participants of a cycle.

    Returns:
        The rows of the study population.
    """
    adults = table["RIDAGEYR"].between(AGE_MIN, AGE_MAX)
    eligible = table["ELIGSTAT"] == 1
    logger.info(
        "    removed: %d outside %d-%d years, %d not eligible for mortality follow-up",
        (~adults).sum(),
        AGE_MIN,
        AGE_MAX,
        (adults & ~eligible).sum(),
    )
    return table[adults & eligible]


def rename_aliases(table: pd.DataFrame) -> pd.DataFrame:
    """Old names → common names (CYCLE_ALIASES).

    Args:
        table: Participants of a cycle.

    Returns:
        The table with the common names.

    Raises:
        ValueError: If a rename collides with an existing column.
    """
    table = table.rename(columns=CYCLE_ALIASES)
    repeated = table.columns[table.columns.duplicated()]
    if len(repeated):
        raise ValueError(f"Rename collision: {list(repeated)}")
    return table
