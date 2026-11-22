"""Tests: Pipeline - Step 5, final models.

- Each level built on a made-up Gold: the app reads its bundle, the typical person gets their own age back,
  and the bundle records the people, deaths and fingerprint it was trained on
- With data/ only (skipped without it, not in git):
    - Same test people as in the final evaluation (the split follows row order, so a new Gold can move people)
    - Saved models trained on the current Gold
"""

# Imports
import hashlib

import numpy as np
import pandas as pd
import pytest

from bioage.app.predict import load_bundle, predict_age
from bioage.config.model_levels import LEVEL_COLUMNS
from bioage.config.paths import GOLD_TABLE
from bioage.models.s1_split import split_data
from bioage.pipeline.s5_build_model import build_level
from bioage.utils.provenance import data_fingerprint

# Test people of the final evaluation (notebooks/final_evaluation.ipynb)
TEST_PEOPLE = 9699
TEST_DEATHS = 1086
TEST_FINGERPRINT = "3db7cb485c350b61"  # sorted seqn of the test people

needs_data = pytest.mark.skipif(not GOLD_TABLE.exists(), reason="needs data/, not in git")


@pytest.mark.parametrize("level", LEVEL_COLUMNS)
def test_built_level_gives_the_typical_person_their_own_age(made_up_gold: pd.DataFrame, level: str) -> None:
    rng = np.random.default_rng(1)
    older_die_more = ((made_up_gold["age"] - 10) / 80).clip(0, 1)
    gold = made_up_gold.assign(death=rng.binomial(1, older_die_more))
    bundle = build_level(level, LEVEL_COLUMNS[level], gold)
    assert bundle["trained_on"]["people"] == len(gold)
    assert bundle["trained_on"]["deaths"] == gold["death"].sum()
    assert bundle["trained_on"]["data_fingerprint"] == data_fingerprint(gold)
    assert bundle["c_index_fit"] > 0.6  # age alone orders who dies first
    years_older = pd.Series(predict_age(bundle, gold), index=gold.index) - gold["age"]
    assert years_older.groupby(gold["sex"]).median().abs().max() < 1


@pytest.fixture(scope="module")
def gold() -> pd.DataFrame:
    """Gold table, read once for every test of the file."""
    return pd.read_parquet(GOLD_TABLE)


@needs_data
def test_same_test_people(gold: pd.DataFrame) -> None:
    _, test, _ = split_data(gold)
    assert (len(test), int(test["death"].sum())) == (TEST_PEOPLE, TEST_DEATHS)
    assert seqn_fingerprint(test) == TEST_FINGERPRINT


@needs_data
@pytest.mark.parametrize("level", LEVEL_COLUMNS)
def test_models_trained_on_current_gold(gold: pd.DataFrame, level: str) -> None:
    assert load_bundle(level)["trained_on"]["data_fingerprint"] == data_fingerprint(gold)


def seqn_fingerprint(data: pd.DataFrame) -> str:
    """Short hash of the sorted seqn of data."""
    return hashlib.sha256(",".join(map(str, sorted(data["seqn"]))).encode()).hexdigest()[:16]
