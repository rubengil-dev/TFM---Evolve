"""Tests: Models - Step 1, split, on a made-up Gold.

- Train and test: 80/20, nobody in both, nobody lost
- Folds: each person of train validated exactly once, never in the fit part of their own fold
- Strata: cycle and death
- Same seed → same split and folds; another seed → other folds (the comparison of tuned models)
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.config.study import COMPARISON_SEED, CV_FOLDS, TEST_SIZE
from bioage.models.s1_split import cv_folds, split_data, strata

# 600 made-up people over 10 cycles: some cycle-death strata are too small for 5 folds
pytestmark = pytest.mark.filterwarnings("ignore:The least populated class:UserWarning")


def test_train_and_test_split_everybody_once(made_up_gold: pd.DataFrame) -> None:
    train, test, _ = split_data(made_up_gold)
    assert len(test) == round(len(made_up_gold) * TEST_SIZE)
    assert set(train["seqn"]).isdisjoint(test["seqn"])
    assert set(train["seqn"]) | set(test["seqn"]) == set(made_up_gold["seqn"])


def test_each_person_validated_once_and_never_fitted_on(made_up_gold: pd.DataFrame) -> None:
    train, _, folds = split_data(made_up_gold)
    assert len(folds) == CV_FOLDS
    validated = np.concatenate([validation for _, validation in folds])
    assert sorted(validated) == list(range(len(train)))
    assert all(set(fit).isdisjoint(validation) for fit, validation in folds)


def test_strata_are_cycle_and_death() -> None:
    people = pd.DataFrame({"cycle": ["1999_2000", "2017_2018"], "death": [1.0, 0.0]})
    assert strata(people).tolist() == ["1999_2000_1", "2017_2018_0"]


def test_same_seed_same_split_another_seed_other_folds(made_up_gold: pd.DataFrame) -> None:
    train, test, folds = split_data(made_up_gold)
    again_train, again_test, again_folds = split_data(made_up_gold)
    assert train["seqn"].tolist() == again_train["seqn"].tolist()
    assert test["seqn"].tolist() == again_test["seqn"].tolist()
    assert all((a == b).all() for (_, a), (_, b) in zip(folds, again_folds, strict=True))
    other = cv_folds(train, seed=COMPARISON_SEED)
    assert any(set(a) != set(b) for (_, a), (_, b) in zip(folds, other, strict=True))
