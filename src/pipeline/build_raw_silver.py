"""
Silver raw step, every Bronze file in one table (one row per person, every variable, no cleaning):
    - Files of each cycle joined by SEQN on DEMO participants (mortality included, DXA averaged)
    - Adults AGE_MIN-AGE_MAX eligible for mortality follow-up
    - Variable aliases renamed so each variable has the same name in every cycle
    - Cycles stacked and saved to data/02_silver/silver_raw.parquet
"""

# Imports
import numpy as np
import pandas as pd

from src.config.paths import BRONZE, SILVER, SILVER_RAW
from src.config.renames import RENAMES
from src.config.sources import CYCLES, DATASETS, MORTALITY_FILE
from src.config.study import AGE_MIN, AGE_MAX
from src.utils.nhanes import cycle_label, dxa_average_imputations, read_mortality, read_xpt


def run():
    """Silver raw step, called from main."""
    cycles = []
    for year in CYCLES:
        table = merge_cycle_files(year)
        table = filter_population(table)
        table = rename_aliases(table)
        cycles.append(table)

    raw = pd.concat(cycles, ignore_index=True)
    save(raw)
    print_summary(raw)


def merge_cycle_files(year):
    """
    All files of a cycle → one table:
        - DEMO participants as base, every other file joined by SEQN
        - 'cycle' column added
    """
    print(f"{cycle_label(year)}...", flush=True)
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


def read_dataset(folder, dataset, year):
    """One NHANES file of the cycle, DXA imputations averaged."""
    name = DATASETS[dataset][CYCLES.index(year)]
    return dxa_average_imputations(read_xpt(folder / f"{name}.xpt"))


def merge_table(merged, table, dataset):
    """
    Left join by SEQN. Columns already in merged:
        - Same values where both exist → missing values filled, column not repeated
        - Different values → kept as NAME_DATASET
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

    return merged.join(table, how="left").reset_index()


def same_values(a, b):
    """Equal values, allowing rounding differences in numbers (e.g. 14084.10 vs 14084.2)."""
    if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):
        return np.allclose(a, b, rtol=1e-4)
    return a.equals(b)


def filter_population(table):
    """Adults AGE_MIN-AGE_MAX eligible for mortality follow-up."""
    adults = table["RIDAGEYR"].between(AGE_MIN, AGE_MAX)
    eligible = table["ELIGSTAT"] == 1
    return table[adults & eligible]


def rename_aliases(table):
    """Old names → common names (RENAMES). Fails if a rename collides with an existing column."""
    table = table.rename(columns=RENAMES)
    repeated = table.columns[table.columns.duplicated()]
    if len(repeated):
        raise ValueError(f"Rename collision: {list(repeated)}")
    return table


def save(raw):
    """Silver raw → parquet."""
    SILVER.mkdir(parents=True, exist_ok=True)
    raw.to_parquet(SILVER_RAW, index=False)


def print_summary(raw):
    """Persons, deaths and columns per cycle."""
    summary = raw.groupby("cycle").agg(persons=("SEQN", "size"), deaths=("MORTSTAT", "sum")).astype(int)
    print(summary.to_string())
    print(f"\n{len(raw)} persons, {int(raw['MORTSTAT'].sum())} deaths, {raw.shape[1]} columns, saved to {SILVER_RAW.name}")
