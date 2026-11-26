"""Tests: Models - Step 7, margin and data needed.

- What is hidden: count values per person, the same with the same seed
- Most Routine values missing: the largest count whose limit stays within MOVE_YEARS
- Fewest Extras: from there on always better than the model without them, in C-index and in age
- Base: by tenth of risk, with risk growing and years never growing
- On a made-up Gold: every level gets its parts and the same base, nothing hidden moves nothing, and the levels
  with Extras measure as many Routine values missing as their mode allows
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.config.app import EXTRAS_LEVELS, MIN_GAIN, MOVE_YEARS
from bioage.config.model_levels import EXTRAS, LEVEL_COLUMNS
from bioage.modeling import s7_margin
from bioage.modeling.s1_split import split_data
from bioage.modeling.s7_margin import (
    base_margin,
    fewest_extras,
    fit_blocks,
    fit_margins,
    hide_random,
    most_missing,
)


@pytest.fixture
def gold(made_up_gold: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(1)
    older_die_more = ((made_up_gold["age"] - 10) / 80).clip(0, 1)
    return made_up_gold.assign(death=rng.binomial(1, older_die_more))


def test_hide_random_hides_count_values_per_person(gold: pd.DataFrame) -> None:
    hidden = hide_random(gold, EXTRAS, 3, seed=1)
    assert (hidden.sum(axis=1) == 3).all()
    assert hidden.equals(hide_random(gold, EXTRAS, 3, seed=1))
    assert not hidden.equals(hide_random(gold, EXTRAS, 3, seed=2))


def test_most_missing_is_the_largest_count_within_the_years() -> None:
    limit = [0, 2, MOVE_YEARS, MOVE_YEARS + 1, MOVE_YEARS - 1, MOVE_YEARS + 2]
    table = pd.DataFrame({"median": 0.0, "limit": limit}, index=range(len(limit)))
    assert most_missing(table) == 4


def extras_table(gains: list[float], medians: list[float]) -> pd.DataFrame:
    """hidden_table of the Extras from the gain and median of each number known, 0 to 8."""
    without = {"median": 3.0, "c_index": 0.7}
    rows = {len(EXTRAS) - known: {"median": medians[known], "c_index": 0.7 + gains[known]} for known in range(9)}
    return pd.DataFrame({-1: without, **rows}).T


@pytest.mark.parametrize(
    ("gains", "medians", "fewest"),
    [
        ([0, 0.003, 0, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003], [2.0] * 9, 3),  # a dip at 2 known
        ([0.003] * 9, [4.0, 4.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0], 2),  # farther from the age with 0 and 1
        ([MIN_GAIN] * 9, [2.0] * 9, 0),  # the gain is enough when equal
        ([0.0] * 9, [2.0] * 9, 9),  # never better
    ],
)
def test_fewest_extras_from_always_better(gains: list[float], medians: list[float], fewest: int) -> None:
    assert fewest_extras(extras_table(gains, medians)) == fewest


def test_base_margin_never_grows_with_risk(gold: pd.DataFrame) -> None:
    train, _, folds = split_data(gold)
    base = base_margin(train, fit_blocks(train, folds, LEVEL_COLUMNS["routine"]))
    assert len(base["risk"]) == len(base["years"]) > 1
    assert np.all(np.diff(base["risk"]) > 0) and np.all(np.diff(base["years"]) <= 1e-12)
    assert min(base["years"]) >= 0


def test_margins_of_every_level(gold: pd.DataFrame, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(s7_margin, "MARGIN_REPEATS", 1)  # one draw is enough to check the structure
    margins = fit_margins(gold)
    assert set(margins) == set(LEVEL_COLUMNS)
    for level, with_extras in EXTRAS_LEVELS.items():
        assert margins[level]["routine_missing"][0] == 0
        assert len(margins[with_extras]["routine_missing"]) == len(margins[level]["routine_missing"])
        assert margins[with_extras]["routine_missing"][0] == 0
        assert len(margins[with_extras]["extras_known"]) == len(EXTRAS) + 1
        assert margins[with_extras]["extras_known"][-1] == 0
        assert 0 <= margins[with_extras]["min_extras"] <= len(EXTRAS) + 1
        assert "extras_known" not in margins[level]
    for parts in margins.values():
        assert parts["base"] == margins["routine"]["base"]
        assert all(np.isfinite(parts["routine_missing"]))
