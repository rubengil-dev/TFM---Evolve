"""
Building Gold from Silver clean: creates the table the model consumes, one row per person.
    1. Derived features (utils/features.py)
    2. Columns: identification, outcome, candidate predictors (config/column_roles.py) and derived features
    3. Follow-up of 0 months → FOLLOW_UP_MIN
    4. Save into data/03_gold/gold.parquet
"""

# Imports
import pandas as pd

from src.config.column_roles import ID_COLUMNS, OUTCOME_COLUMNS, SILVER_PREDICTORS
from src.config.paths import GOLD, GOLD_TABLE, SILVER_CLEAN
from src.config.study import FOLLOW_UP_MIN
from src.utils.features import derived_features


def run():
    """
    Gold step, called from main.
    """
    clean = pd.read_parquet(SILVER_CLEAN)
    gold = pd.concat([
        clean[ID_COLUMNS + OUTCOME_COLUMNS + SILVER_PREDICTORS],
        derived_features(clean),
    ], axis=1)
    gold = fix_zero_follow_up(gold)

    save(gold)
    print_summary(gold)


def fix_zero_follow_up(gold):
    """
    Follow-up of 0 months → FOLLOW_UP_MIN.
    """
    gold["follow_up_months"] = gold["follow_up_months"].clip(lower=FOLLOW_UP_MIN)
    return gold


def save(gold):
    """
    Gold → parquet.
    """
    GOLD.mkdir(parents=True, exist_ok=True)
    gold.to_parquet(GOLD_TABLE, index=False)


def print_summary(gold):
    """
    Persons, deaths, columns and % with value per variable.
    """
    print(f"{len(gold)} persons, {int(gold['death'].sum())} deaths, {gold.shape[1]} columns, saved to {GOLD_TABLE.name}\n")
    coverage = (gold.notna().mean() * 100).round(0).astype(int)
    print(coverage.to_string())
