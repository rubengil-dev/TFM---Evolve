"""
Silver clean rules on made-up NHANES rows:
    - CDC corrections: cycles, chains, limits on the original value and minimum
    - Questionnaires → form answers: smoking (adult and youth), alcohol, physical activity
    - Blood pressure, survey weight and implausible values
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from src.config.corrections import CORRECTIONS
from src.pipeline import s3_build_clean_silver as silver
from src.utils.nhanes import cycle_label


def raw_rows(cycles, **columns):
    """Made-up Silver raw: one row per cycle start year, every corrected variable missing unless given."""
    raw = pd.DataFrame({"cycle": [cycle_label(year) for year in cycles]})
    for variable in dict.fromkeys(row[0] for row in CORRECTIONS):
        raw[variable] = np.nan
    return raw.assign(**{name: np.asarray(values, dtype=float) for name, values in columns.items()})


def test_creatinine_corrected_only_in_its_cycles():
    """1999 and 2005 have their own equation; 2001 stays as it is."""
    raw = silver.apply_corrections(raw_rows([1999, 2001, 2005], LBXSCR=[1.0, 1.0, 1.0]))
    assert raw["LBXSCR"].tolist() == pytest.approx([1.013 + 0.147, 1.0, 0.978 - 0.016])


def test_insulin_chains_every_assay_up_to_2013():
    """1999 goes through the 4 equations, 2009 through the last 2, 2013 through none."""
    raw = silver.apply_corrections(raw_rows([1999, 2009, 2013], LBXIN=[10.0, 10.0, 10.0]))
    tosoh = 1.0027 * 10 - 2.2934
    mercodia = 0.9501 * tosoh + 1.4890
    roche = lambda x: 0.8868 * x - 0.0744 + 0.0011 * x ** 2
    tosoh_aia = lambda x: 10 ** (1.024 * np.log10(x) - 0.0802)
    assert raw["LBXIN"].tolist() == pytest.approx([tosoh_aia(roche(mercodia)), tosoh_aia(roche(10)), 10])


def test_urine_creatinine_piece_chosen_by_original_value():
    """Each value gets only the equation of its own range, even after the previous one moved it."""
    raw = silver.apply_corrections(raw_rows([1999] * 3 + [2007], URXUCR=[74, 75, 250, 100]))
    expected = [(1.02 * np.sqrt(74) - 0.36) ** 2, (1.05 * np.sqrt(75) - 0.74) ** 2, (1.01 * np.sqrt(250) - 0.10) ** 2, 100]
    assert raw["URXUCR"].tolist() == pytest.approx(expected)


def test_hs_crp_corrected_up_to_20_and_not_below_minimum():
    """2017 hs-CRP: above 20 untouched, very low values → 0.08."""
    raw = silver.apply_corrections(raw_rows([2017] * 3, LBXHSCRP=[0.1, 10, 25]))
    assert raw["LBXHSCRP"].tolist() == pytest.approx([0.08, 1.150 * 10 - 0.3397, 25])


def test_adult_smoking_answers():
    """Fewer than 100 cigarettes → never; smokes every day or some days → current; not at all → former."""
    raw = youth_columns(4).assign(SMQ020=[2, 1, 1, 1], SMQ040=[np.nan, 1, 2, 3])
    assert silver.smoking(raw).tolist() == ["never", "current", "current", "former"]


def test_youth_smoking_answers():
    """
    18-19 year olds without adult answers:
        - 2011-2012: 100+ cigarettes and smoked this month → current, not this month → former, fewer → never
        - Until 2010: never tried or no whole cigarette → never; YOUTH_CURRENT_SMOKER_DAYS or more → current
    """
    raw = youth_columns(7).assign(
        SMQ621=[8, 8, 3, np.nan, np.nan, np.nan, np.nan],
        SMQ640=[5, 0, np.nan, np.nan, np.nan, np.nan, np.nan],
        SMQ620=[np.nan, np.nan, np.nan, 2, 1, 1, 1],
        SMD630=[np.nan, np.nan, np.nan, np.nan, 55, 14, 14],
        SMD641=[np.nan, np.nan, np.nan, np.nan, np.nan, 12, 3],
    )
    assert silver.smoking(raw).tolist() == ["current", "former", "never", "never", "never", "current", "never"]


def youth_columns(rows):
    """Every smoking question missing."""
    names = ["SMQ020", "SMQ040", "SMQ621", "SMQ640", "SMD641", "SMQ620", "SMD630"]
    return pd.DataFrame({name: [np.nan] * rows for name in names})


def test_alcohol_frequency_and_drinks():
    """
    Drinking days per year → answer; never → 0 drinks:
        - Until 2016: 1 a week → weekly, 5 a week → daily, 0 → never, lifetime abstainer → never
        - 2017: once a week (code 5) → weekly, 2-3 times a month (code 6) → less than weekly
    """
    raw = pd.DataFrame({
        "ALQ120Q": [1, 5, 0, np.nan, np.nan, np.nan],
        "ALQ120U": [1, 1, np.nan, np.nan, np.nan, np.nan],
        "ALQ121":  [np.nan, np.nan, np.nan, np.nan, 5, 6],
        "ALQ110":  [np.nan, np.nan, np.nan, 2, np.nan, np.nan],
        "ALQ111":  [np.nan] * 6,
        "ALQ130":  [2, 3, 4, np.nan, 1, 2],
    })
    frequency, drinks = silver.alcohol(raw)
    assert frequency.tolist() == ["weekly", "daily", "never", "never", "weekly", "less_than_weekly"]
    assert drinks.tolist() == [2, 3, 0, 0, 1, 2]


def test_physical_activity_answers():
    """Vigorous → intense, else moderate → moderate, no to both (or unable) → sedentary; until 2006 and from 2007."""
    raw = pd.DataFrame({
        "PAD200": [1, 2, 2, 3, np.nan, np.nan],
        "PAD320": [2, 1, 2, 3, np.nan, np.nan],
        "PAQ650": [np.nan, np.nan, np.nan, np.nan, 1, 2],
        "PAQ665": [np.nan, np.nan, np.nan, np.nan, 2, 2],
    })
    assert silver.physical_activity(raw).tolist() == ["intense", "moderate", "sedentary", "sedentary", "intense", "sedentary"]


def test_blood_pressure_mean_without_zero_diastolic():
    """Mean of the readings; diastolic 0 is not measurable and is left out."""
    raw = pd.DataFrame({
        "BPXSY1": [120], "BPXSY2": [130], "BPXSY3": [np.nan], "BPXSY4": [np.nan],
        "BPXDI1": [80], "BPXDI2": [0], "BPXDI3": [70], "BPXDI4": [np.nan],
    })
    pressure = silver.blood_pressure(raw)
    assert pressure.iloc[0].tolist() == [125, 75]


def test_survey_weight_for_the_combined_cycles():
    """1999-2002: 4-year weight × 2 / 10; later: 2-year weight / 10."""
    raw = raw_rows([1999, 2003], WTMEC4YR=[100, np.nan], WTMEC2YR=[np.nan, 300])
    assert silver.survey_weights(raw).tolist() == pytest.approx([20, 30])


def test_implausible_values_blanked(capsys):
    """Outside the PLAUSIBLE_RANGES limits → missing; limits themselves kept."""
    clean = pd.DataFrame({"glucose": [29, 30, 600, 601]})
    clean = clean.assign(**{variable: np.nan for variable in silver.PLAUSIBLE_RANGES if variable != "glucose"})
    assert silver.remove_implausible_values(clean)["glucose"].tolist() == pytest.approx([np.nan, 30, 600, np.nan], nan_ok=True)
