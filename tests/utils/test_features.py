"""Tests: Utils - Derived features.

- eGFR (CKD-EPI 2021): both sides of the creatinine threshold, both sexes; missing sex → missing
- Age groups: each border in the upper group, missing outside the study ages
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.utils.features import age_groups, egfr_ckd_epi_2021


def test_egfr_ckd_epi_2021() -> None:
    creatinine = pd.Series([0.7, 1.2, 1.0, 0.5, 0.6])
    age = pd.Series([40, 60, 50, 40, 30])
    sex = pd.Series(["female", "male", None, "female", "male"])
    expected = [112.0, 69.3, np.nan, 121.5, 133.2]  # by hand from the published formula
    assert egfr_ckd_epi_2021(creatinine, age, sex).tolist() == pytest.approx(expected, abs=0.1, nan_ok=True)


def test_age_groups() -> None:
    groups = age_groups(pd.DataFrame({"age": [17, 18, 29.9, 30, 79, 80]}))
    assert groups.astype(object).tolist()[1:5] == ["18-29", "18-29", "30-39", "70-79"]
    assert pd.isna(groups.iloc[0]) and pd.isna(groups.iloc[5])
