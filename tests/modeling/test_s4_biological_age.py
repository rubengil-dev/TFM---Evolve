"""Tests: Models - Step 4, biological age, on made-up values.

- The typical person of each age gets that same age back, inside and outside the study ages
- More risk → older; reference that does not grow with age → error
- Survey weights move the reference
- Men and women in one call each read their own curve; the curve ends exactly at the last study age
- Risk read at the 10-year horizon; risks of exactly 0 or 1 still give a finite age
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.config.study import AGE_MAX, AGE_MIN, HORIZON_MONTHS
from bioage.modeling.s4_biological_age import (
    biological_age,
    fit_reference,
    log_cumulative_hazard,
    reference_risk,
    risk_at_horizon,
)


def made_up_risk(slope: float = 0.09) -> tuple[pd.Series, pd.DataFrame]:
    """Risk that grows with age, higher for men, for 2000 made-up people."""
    rng = np.random.default_rng(0)
    data = pd.DataFrame(
        {"age": rng.uniform(18, 80, 2000), "sex": rng.choice(["female", "male"], 2000), "weight_exam": 1.0}
    )
    hazard = -6 + slope * (data["age"] - 18) + 0.4 * (data["sex"] == "male") + rng.normal(0, 0.3, 2000)
    return 1 - np.exp(-np.exp(hazard)), data


def test_risk_and_hazard_are_inverse() -> None:
    risk = np.array([0.001, 0.1, 0.5, 0.9])
    assert 1 - np.exp(-np.exp(log_cumulative_hazard(risk))) == pytest.approx(risk)


@pytest.mark.parametrize("sex", ["female", "male"])
def test_typical_person_gets_own_age(sex: str) -> None:
    reference = fit_reference(*made_up_risk())
    ages = np.array([10, 18, 30, 50, 79, 90])
    sexes = np.full(len(ages), sex)
    assert biological_age(reference_risk(ages, sexes, reference), sexes, reference) == pytest.approx(ages, abs=1e-6)


def test_more_risk_means_older() -> None:
    reference = fit_reference(*made_up_risk())
    risks = np.array([0.01, 0.05, 0.2, 0.5])
    female = biological_age(risks, ["female"] * 4, reference)
    male = biological_age(risks, ["male"] * 4, reference)
    assert np.all(np.diff(female) > 0) and np.all(male < female)


def test_reference_must_grow_with_age() -> None:
    with pytest.raises(ValueError):
        fit_reference(*made_up_risk(slope=-0.09))


def test_weights_move_the_reference() -> None:
    risk, data = made_up_risk()
    unweighted = fit_reference(risk, data)
    above_typical = risk > reference_risk(data["age"], data["sex"], unweighted)
    weighted = fit_reference(risk, data.assign(weight_exam=np.where(above_typical, 10.0, 1.0)))
    assert np.all(weighted["female"] > unweighted["female"]) and np.all(weighted["male"] > unweighted["male"])


def test_mixed_sexes_read_their_own_curve() -> None:
    reference = fit_reference(*made_up_risk())
    ages, sexes = np.array([40, 40, 60, 60]), np.array(["female", "male", "male", "female"])
    assert biological_age(reference_risk(ages, sexes, reference), sexes, reference) == pytest.approx(ages, abs=1e-6)


def test_curve_covers_the_study_ages_exactly() -> None:
    ages = fit_reference(*made_up_risk())["ages"]
    assert (ages[0], ages[-1]) == (AGE_MIN, AGE_MAX)


class FixedCurves:
    """Stand-in for a fitted pipeline: survival exp(-rate × months) for each person."""

    def __init__(self, rates: list[float]) -> None:
        self.rates = rates

    def predict_survival_function(self, data: pd.DataFrame) -> list:
        return [lambda months, rate=rate: np.exp(-rate * months) for rate in self.rates]


def test_risk_read_at_the_horizon() -> None:
    risk = risk_at_horizon(FixedCurves([0.001, 0.01]), pd.DataFrame(index=[0, 1]))
    expected = [1 - np.exp(-0.001 * HORIZON_MONTHS), 1 - np.exp(-0.01 * HORIZON_MONTHS)]
    assert risk.tolist() == pytest.approx(expected)


def test_risk_of_zero_or_one_gives_a_finite_age() -> None:
    reference = fit_reference(*made_up_risk())
    assert np.isfinite(biological_age(np.array([0.0, 1.0]), ["female", "male"], reference)).all()
