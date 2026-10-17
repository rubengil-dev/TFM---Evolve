"""
NHANES helpers:
    - Cycle names
    - File readers (.xpt, mortality .dat)
    - DXA multiple imputation
"""

# Imports
import pandas as pd

from src.config.sources import MORTALITY_COLUMNS


def cycle_label(year):
    """
    Cycle name creator: 1999 → '1999_2000'.
    """
    return f"{year}_{year + 1}"


def read_xpt(path):
    """
    SAS transport file → DataFrame:
        - SEQN as integer
        - SAS zero artifact (5.4e-79) → 0
    """
    table = pd.read_sas(path, format="xport", encoding="latin-1")
    numeric = table.select_dtypes("number").columns
    table[numeric] = table[numeric].mask(table[numeric].abs() < 1e-70, 0)
    table["SEQN"] = table["SEQN"].astype(int)
    return table.copy()  # defragment


def read_mortality(path):
    """
    Fixed-width mortality file → DataFrame:
        - Columns and positions from MORTALITY_COLUMNS
        - '.' → missing
    """
    colspecs = [(start - 1, end) for start, end in MORTALITY_COLUMNS.values()]
    return pd.read_fwf(path, colspecs=colspecs, names=list(MORTALITY_COLUMNS), na_values=".")


def dxa_average_imputations(table):
    """
    DXA 1999-2006: 5 imputed rows per person → 1 row (mean).
    """
    if "_MULT_" not in table.columns:
        return table
    return table.drop(columns="_MULT_").groupby("SEQN", as_index=False).mean(numeric_only=True)
