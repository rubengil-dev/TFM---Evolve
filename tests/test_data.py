"""
Local data, skipped without data/ (not in git):
    - Same test people as in the final evaluation (the split follows row order, so a new Gold can move people)
    - Saved models trained on the current Gold
"""

# Imports
import hashlib

import pandas as pd
import pytest

from src.config.model_sets import LEVEL_COLUMNS
from src.config.paths import GOLD_TABLE
from src.models.predict import load_bundle
from src.models.s1_split import split_train_test
from src.utils.provenance import data_fingerprint

# Test people of the final evaluation (notebooks/final_evaluation.ipynb)
TEST_PEOPLE = 9699
TEST_DEATHS = 1086
TEST_FINGERPRINT = "3db7cb485c350b61"  # sorted seqn of the test people

pytestmark = pytest.mark.skipif(not GOLD_TABLE.exists(), reason="needs data/, not in git")


@pytest.fixture(scope="module")
def gold():
    """Gold table, read once for every test of the file."""
    return pd.read_parquet(GOLD_TABLE)


def test_same_test_people(gold):
    """The split still gives the test people of the final evaluation."""
    _, test = split_train_test(gold)
    assert (len(test), int(test["death"].sum())) == (TEST_PEOPLE, TEST_DEATHS)
    assert seqn_fingerprint(test) == TEST_FINGERPRINT


@pytest.mark.parametrize("level", LEVEL_COLUMNS)
def test_models_trained_on_current_gold(gold, level):
    """Each saved model was trained on exactly the Gold on disk."""
    assert load_bundle(level)["trained_on"]["data_fingerprint"] == data_fingerprint(gold)


def seqn_fingerprint(data):
    """Short hash of the sorted seqn of data."""
    return hashlib.sha256(",".join(map(str, sorted(data["seqn"]))).encode()).hexdigest()[:16]
