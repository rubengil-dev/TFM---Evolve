"""
Biological age and derived features, on made-up values:
    - The typical person of each age gets that same age back, inside and outside the study ages
    - More risk → older; reference that does not grow with age → error
    - eGFR and age groups
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from src.models.s4_biological_age import biological_age, fit_reference, log_cumulative_hazard, reference_risk
from src.utils.features import age_groups, egfr_ckd_epi_2021


def made_up_risk(slope=0.09):
    """Risk that grows with age, higher for men, for 2000 made-up people."""
    rng = np.random.default_rng(0)
    data = pd.DataFrame({"age": rng.uniform(18, 80, 2000), "sex": rng.choice(["female", "male"], 2000)})
    hazard = -6 + slope * (data["age"] - 18) + 0.4 * (data["sex"] == "male") + rng.normal(0, 0.3, 2000)
    return 1 - np.exp(-np.exp(hazard)), data


def test_risk_and_hazard_are_inverse():
    """log(-log(1 - risk)) undone by 1 - exp(-exp(hazard))."""
    risk = np.array([0.001, 0.1, 0.5, 0.9])
    assert 1 - np.exp(-np.exp(log_cumulative_hazard(risk))) == pytest.approx(risk)


@pytest.mark.parametrize("sex", ["female", "male"])
def test_typical_person_gets_own_age(sex):
    """Risk of the typical person of each age → that age, also beyond 18-79 where the curve goes straight."""
    reference = fit_reference(*made_up_risk())
    ages = np.array([10, 18, 30, 50, 79, 90])
    sexes = np.full(len(ages), sex)
    assert biological_age(reference_risk(ages, sexes, reference), sexes, reference) == pytest.approx(ages, abs=1e-6)


def test_more_risk_means_older():
    """Biological age grows with risk, and the same risk is younger for a man than for a woman."""
    reference = fit_reference(*made_up_risk())
    risks = np.array([0.01, 0.05, 0.2, 0.5])
    female = biological_age(risks, ["female"] * 4, reference)
    male = biological_age(risks, ["male"] * 4, reference)
    assert np.all(np.diff(female) > 0) and np.all(male < female)


def test_reference_must_grow_with_age():
    """Risk falling with age → no valid reference."""
    with pytest.raises(ValueError):
        fit_reference(*made_up_risk(slope=-0.09))


def test_egfr_ckd_epi_2021():
    """Known values: woman 40 years, 0.7 mg/dL → 112; man 60 years, 1.2 mg/dL → 69; sex missing → missing."""
    egfr = egfr_ckd_epi_2021(pd.Series([0.7, 1.2, 1.0]), pd.Series([40, 60, 50]), pd.Series(["female", "male", None]))
    assert egfr.tolist() == pytest.approx([112.0, 69.2, np.nan], abs=0.1, nan_ok=True)


def test_age_groups():
    """Lower bound included; outside the study ages → missing."""
    groups = age_groups(pd.DataFrame({"age": [18, 29.9, 30, 79, 80]}))
    assert groups.astype(object).tolist()[:4] == ["18-29", "18-29", "30-39", "70-79"]
    assert pd.isna(groups.iloc[4])
