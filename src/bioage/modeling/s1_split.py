"""ML Pipeline: Step 1 - Splitting Gold.

- Split: 80/20, stratified by cycle and death.
- Cross-validation: 5 folds inside train.
"""

# Imports
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split

from bioage.config.study import CV_FOLDS, SPLIT_SEED, TEST_SIZE


def split_data(gold: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, list[tuple[np.ndarray, np.ndarray]]]:
    """Gold → train, test and the cross-validation folds of train.

    Args:
        gold: Gold table.

    Returns:
        Train, test and the folds.
    """
    train, test = train_test_split(gold, test_size=TEST_SIZE, stratify=strata(gold), random_state=SPLIT_SEED)
    return train, test, cv_folds(train)


def cv_folds(train: pd.DataFrame, seed: int = SPLIT_SEED) -> list[tuple[np.ndarray, np.ndarray]]:
    """Folds of train, stratified by cycle and death.

    Args:
        train: Train part of Gold.
        seed: Seed of the shuffle.

    Returns:
        One (fit positions, validation positions) pair per fold.
    """
    splitter = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=seed)
    return list(splitter.split(train, strata(train)))


def strata(data: pd.DataFrame) -> pd.Series:
    """Stratum of each person: cycle and death, e.g. '1999_2000_1'.

    Args:
        data: People with their cycle and outcome.

    Returns:
        Stratum label of each person.
    """
    return data["cycle"].astype(str) + "_" + data["death"].astype(int).astype(str)
