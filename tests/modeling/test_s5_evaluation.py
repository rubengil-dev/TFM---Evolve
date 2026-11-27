"""Tests: Models - Step 5, evaluation, on made-up people.

- C-index: right order → near 1, reversed → near 0; only deaths up to the horizon count;
  same-age C-index weighted by deaths
- Observed risk at the horizon: share of deaths, allowing for people followed less
- Calibration gap above 0 = risk underestimated; a known shift in years recovered
- Bootstrap: two equal risks differ by 0; a clearly better one differs above 0; same seed → same result;
  95% interval from the 2.5 and 97.5 percentiles
- Cross-validation: each person's risk comes from the model of the fold that left them out
- Weighted median: equal weights → the plain median; a heavy person pulls it; missing values skipped; per group
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.config.model_levels import ROUTINE
from bioage.modeling import s5_evaluation as evaluation
from bioage.modeling.s1_split import cv_folds
from bioage.modeling.s3_algorithms import build_pipeline, survival_target
from bioage.modeling.s4_biological_age import fit_reference, reference_risk, risk_at_horizon

pytestmark = pytest.mark.filterwarnings("ignore:The least populated class:UserWarning")


def people_dying_in_order(n: int = 300) -> pd.DataFrame:
    """People who die one after another, a third followed to the end without dying."""
    rng = np.random.default_rng(0)
    months = rng.permutation(np.arange(1, n + 1) * 100 / n)
    death = (rng.uniform(size=n) > 1 / 3).astype(int)
    return pd.DataFrame({"follow_up_months": np.where(death == 1, months, 150), "death": death})


def test_c_index_right_and_reversed_order() -> None:
    people = people_dying_in_order()
    earlier_is_riskier = -people["follow_up_months"]
    assert evaluation.c_index(earlier_is_riskier, people, people) > 0.99
    assert evaluation.c_index(-earlier_is_riskier, people, people) < 0.01


def test_c_index_counts_only_deaths_up_to_the_horizon() -> None:
    months = np.arange(1, 201, dtype=float)
    people = pd.DataFrame({"follow_up_months": months, "death": 1})
    right_until_120 = pd.Series(np.where(months <= 120, -months, -1000 + months))  # wrong order after 120
    assert evaluation.c_index(right_until_120, people, people) == pytest.approx(1)


def test_same_age_c_index_weighted_by_deaths() -> None:
    by_age = pd.DataFrame({"c_index": [0.6, 0.8], "deaths": [10, 30]})
    assert evaluation.same_age_c_index(by_age) == pytest.approx(0.75)


def test_observed_risk_allows_for_shorter_follow_up() -> None:
    # 10 people: 3 die before 120 months, 6 followed past it alive, 1 left at 60 months alive
    people = pd.DataFrame(
        {"follow_up_months": [10, 50, 100, 150, 150, 150, 150, 150, 150, 60], "death": [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]}
    )
    survival = (9 / 10) * (8 / 9) * (6 / 7)  # Kaplan-Meier: the person left at 60 is out from then on
    assert evaluation.observed_risk(people) == pytest.approx(1 - survival)


def test_calibration_gap_above_zero_means_underestimated() -> None:
    people = people_dying_in_order(400)
    risk = pd.Series(np.where(np.arange(400) < 200, 0.05, 0.95))
    table = evaluation.calibration_table(risk, people)
    observed = evaluation.observed_risk(people.iloc[:200]), evaluation.observed_risk(people.iloc[200:])
    assert table["gap"].tolist() == pytest.approx([observed[0] - 0.05, observed[1] - 0.95])
    assert table["gap"].iloc[0] > 0 > table["gap"].iloc[1]


def test_years_to_observed_recovers_a_known_shift() -> None:
    rng = np.random.default_rng(0)
    data = pd.DataFrame({"age": rng.uniform(18, 80, 2000), "sex": rng.choice(["female", "male"], 2000)})
    hazard = -6 + 0.09 * (data["age"] - 18) + rng.normal(0, 0.3, 2000)
    reference = fit_reference(1 - np.exp(-np.exp(hazard)), data.assign(weight_exam=1.0))
    ages, sex = np.full(50, 50.0), pd.Series(["female"] * 25 + ["male"] * 25)
    observed = reference_risk(ages + 5, sex, reference).mean()
    assert evaluation.years_to_observed(ages, sex, observed, reference) == pytest.approx(5, abs=0.01)


def test_bootstrap_difference_zero_for_equal_risks_and_above_zero_for_better() -> None:
    people = people_dying_in_order().assign(age=50)
    perfect, noise = -people["follow_up_months"], pd.Series(np.random.default_rng(1).uniform(size=len(people)))
    same = evaluation.compare_risks(perfect, perfect, people, samples=20)
    better = evaluation.compare_risks(perfect, noise, people, samples=20)
    assert (same[["difference", "low", "high"]] == 0).all().all()
    assert (better["low"] > 0).all()


def test_each_risk_comes_from_the_fold_that_left_the_person_out(made_up_gold: pd.DataFrame) -> None:
    train = made_up_gold.sample(frac=1, random_state=0)  # shuffled index, as after the real split
    folds = cv_folds(train)
    risk = evaluation.cross_validate("cox", ROUTINE, train, folds)["risk"]
    fit_rows, validation_rows = folds[0]
    fit, validation = train.iloc[fit_rows], train.iloc[validation_rows]
    pipeline = build_pipeline("cox", ROUTINE).fit(fit, survival_target(fit))
    assert risk.notna().all()
    assert risk.loc[validation.index].tolist() == pytest.approx(risk_at_horizon(pipeline, validation).tolist())


def test_bootstrap_same_seed_same_result() -> None:
    people = people_dying_in_order().assign(age=50)
    risks = {"model": -people["follow_up_months"] + np.random.default_rng(2).normal(0, 30, len(people))}
    first = evaluation.bootstrap_c_indexes(risks, people, samples=5)
    pd.testing.assert_frame_equal(first, evaluation.bootstrap_c_indexes(risks, people, samples=5))


def test_confidence_interval_percentiles() -> None:
    interval = evaluation.confidence_interval(pd.DataFrame({"x": np.arange(1001, dtype=float)})).loc["x"]
    assert interval.tolist() == pytest.approx([500, 25, 975])


def test_weighted_median_equal_weights_is_the_median() -> None:
    values = pd.Series([5.0, 1.0, 3.0, 9.0, 7.0])
    assert evaluation.weighted_median(values, pd.Series(np.ones(5))) == 5


def test_weighted_median_follows_the_heavy_person() -> None:
    values = pd.Series([1.0, 2.0, 3.0, 10.0])
    assert evaluation.weighted_median(values, pd.Series([1.0, 1.0, 1.0, 5.0])) == 10


def test_weighted_median_skips_missing_values() -> None:
    values = pd.Series([np.nan, 1.0, 2.0, 3.0])
    assert evaluation.weighted_median(values, pd.Series([100.0, 1.0, 1.0, 1.0])) == 2


def test_weighted_medians_per_group() -> None:
    gaps = pd.DataFrame({"level": [1.0, 2.0, 3.0, 10.0, 20.0, 30.0]})
    weights = pd.Series([1.0, 1.0, 5.0, 5.0, 1.0, 1.0])
    groups = pd.Series(["a", "a", "a", "b", "b", "b"])
    medians = evaluation.weighted_medians(gaps, weights, groups)
    assert medians.loc["a", "level"] == 3
    assert medians.loc["b", "level"] == 10
    assert evaluation.weighted_medians(gaps, weights)["level"] == 3
