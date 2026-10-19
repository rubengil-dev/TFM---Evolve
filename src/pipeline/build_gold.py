"""
Gold step, the only table the model and the app read (one row per person):
    - Derived features (utils/features.py)
    - Columns: identification, outcome, candidate predictors (config/column_roles.py) and derived features
    - Follow-up of 0 months → FOLLOW_UP_MIN
    - Saved to data/03_gold/gold.parquet
"""

# Imports
import pandas as pd

from src.config.column_roles import ID_COLUMNS, OUTCOME_COLUMNS, SILVER_PREDICTORS
from src.config.paths import GOLD, GOLD_TABLE, SILVER_CLEAN
from src.config.study import FOLLOW_UP_MIN
from src.utils.features import derived_features
from src.utils.summary import print_layer_summary


def run():
    """Gold step, called from main."""
    clean = pd.read_parquet(SILVER_CLEAN)
    gold = pd.concat([
        clean[ID_COLUMNS + OUTCOME_COLUMNS + SILVER_PREDICTORS],
        derived_features(clean),
    ], axis=1)
    gold = fix_zero_follow_up(gold)

    save(gold)
    print_layer_summary(gold, GOLD_TABLE)


def fix_zero_follow_up(gold):
    """Follow-up of 0 months → FOLLOW_UP_MIN."""
    gold["follow_up_months"] = gold["follow_up_months"].clip(lower=FOLLOW_UP_MIN)
    return gold


def save(gold):
    """Gold → parquet."""
    GOLD.mkdir(parents=True, exist_ok=True)
    gold.to_parquet(GOLD_TABLE, index=False)
