"""
Step 1, split of Gold:
    - Random 80/20, stratified by cycle and death
    - 5 cross-validation folds inside train
"""

# Imports
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split

from src.config.study import CV_FOLDS, SPLIT_SEED, TEST_SIZE


def split_data(gold):
    """Gold → train, test and the cross-validation folds of train."""
    train, test = split_train_test(gold)
    folds = cv_folds(train)
    print_summary(train, test, folds)
    return train, test, folds


def split_train_test(gold):
    """Train and test, stratified by cycle and death."""
    return train_test_split(gold, test_size=TEST_SIZE, stratify=strata(gold), random_state=SPLIT_SEED)


def cv_folds(train, seed=SPLIT_SEED):
    """
    Folds of train, stratified by cycle and death:
        - List of (fit positions, validation positions)
    """
    splitter = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=seed)
    return list(splitter.split(train, strata(train)))


def strata(data):
    """Stratum of each person: cycle and death, e.g. '1999_2000_1'."""
    return data["cycle"].astype(str) + "_" + data["death"].astype(int).astype(str)


def print_summary(train, test, folds):
    """People and deaths per part and per cycle."""
    parts = pd.concat([train.assign(part="train"), test.assign(part="test")])
    summary = parts.groupby(["cycle", "part"])["death"].agg(people="size", deaths="sum").unstack("part")
    print(summary.astype(int).to_string())
    print(f"train: {len(train)} people, {int(train['death'].sum())} deaths")
    print(f"test:  {len(test)} people, {int(test['death'].sum())} deaths")
    print(f"folds: {[len(validation) for _, validation in folds]} people in each validation part")
