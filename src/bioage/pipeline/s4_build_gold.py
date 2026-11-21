"""Build gold data layer.

This is the only table the model and the app read (one row per person).

Changes:
- Derived features (utils/features.py)
- Columns: identification, outcome, selected predictors (config/gold_columns.py) and derived features
- Follow-up of 0 months → FOLLOW_UP_MIN
- Validation (utils/validation.py): any error → not saved
- Saved to data/03_gold/gold.parquet
"""

# Imports
import pandas as pd

from bioage.config.gold_columns import ID_COLUMNS, OUTCOME_COLUMNS, SELECTED_PREDICTORS
from bioage.config.paths import GOLD, GOLD_TABLE, SILVER_CLEAN
from bioage.config.study import FOLLOW_UP_MIN
from bioage.utils.features import derived_features
from bioage.utils.summary import print_layer_summary
from bioage.utils.validation import validate_gold


def run() -> None:
    """Gold step, called from main."""
    clean = pd.read_parquet(SILVER_CLEAN)
    gold = pd.concat(
        [
            clean[ID_COLUMNS + OUTCOME_COLUMNS + SELECTED_PREDICTORS],
            derived_features(clean),
        ],
        axis=1,
    )
    gold = fix_zero_follow_up(gold)
    validate_gold(gold)

    save(gold)
    print_layer_summary(gold, GOLD_TABLE)


def fix_zero_follow_up(gold: pd.DataFrame) -> pd.DataFrame:
    """Follow-up of 0 months → FOLLOW_UP_MIN.

    Args:
        gold: Gold table.

    Returns:
        The same table with the follow-up fixed.
    """
    gold["follow_up_months"] = gold["follow_up_months"].clip(lower=FOLLOW_UP_MIN)
    return gold


def save(gold: pd.DataFrame) -> None:
    """Gold → parquet.

    Args:
        gold: Gold table.
    """
    GOLD.mkdir(parents=True, exist_ok=True)
    gold.to_parquet(GOLD_TABLE, index=False)
