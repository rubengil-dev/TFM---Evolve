"""Silver clean rules on made-up NHANES rows.

- CDC corrections: cycles, chains, limits on the original value and minimum
- Questionnaires → form answers: smoking (adult and youth), alcohol, physical activity
- Blood pressure, survey weight and implausible values
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.config.corrections import CORRECTIONS
from bioage.pipeline import s3_build_clean_silver as silver
from bioage.utils.nhanes import cycle_label


def raw_rows(cycles: list[int], **columns: list[float]) -> pd.DataFrame:
    """Made-up Silver raw: one row per cycle start year, every corrected variable missing unless given."""
    raw = pd.DataFrame({"cycle": [cycle_label(year) for year in cycles]})
    for variable in dict.fromkeys(row[0] for row in CORRECTIONS):
        raw[variable] = np.nan
    return raw.assign(**{name: np.asarray(values, dtype=float) for name, values in columns.items()})


def test_creatinine_corrected_only_in_its_cycles() -> None:
    raw = silver.apply_corrections(raw_rows([1999, 2001, 2005], LBXSCR=[1.0, 1.0, 1.0]))
    assert raw["LBXSCR"].tolist() == pytest.approx([1.013 + 0.147, 1.0, 0.978 - 0.016])


def test_insulin_chains_every_assay_up_to_2013() -> None:
    raw = silver.apply_corrections(raw_rows([1999, 2009, 2013], LBXIN=[10.0, 10.0, 10.0]))
    tosoh = 1.0027 * 10 - 2.2934
    mercodia = 0.9501 * tosoh + 1.4890

    def roche(x: float) -> float:
        return 0.8868 * x - 0.0744 + 0.0011 * x**2

    def tosoh_aia(x: float) -> float:
        return 10 ** (1.024 * np.log10(x) - 0.0802)

    assert raw["LBXIN"].tolist() == pytest.approx([tosoh_aia(roche(mercodia)), tosoh_aia(roche(10)), 10])


def test_urine_creatinine_piece_chosen_by_original_value() -> None:
    raw = silver.apply_corrections(raw_rows([1999] * 3 + [2007], URXUCR=[74, 75, 250, 100]))
    expected = [
        (1.02 * np.sqrt(74) - 0.36) ** 2,
        (1.05 * np.sqrt(75) - 0.74) ** 2,
        (1.01 * np.sqrt(250) - 0.10) ** 2,
        100,
    ]
    assert raw["URXUCR"].tolist() == pytest.approx(expected)


def test_hs_crp_corrected_up_to_20_and_not_below_minimum() -> None:
    raw = silver.apply_corrections(raw_rows([2017] * 3, LBXHSCRP=[0.1, 10, 25]))
    assert raw["LBXHSCRP"].tolist() == pytest.approx([0.08, 1.150 * 10 - 0.3397, 25])


def test_adult_smoking_answers() -> None:
    raw = youth_columns(4).assign(SMQ020=[2, 1, 1, 1], SMQ040=[np.nan, 1, 2, 3])
    assert silver.smoking(raw).tolist() == ["never", "current", "current", "former"]


def test_youth_smoking_answers() -> None:
    raw = youth_columns(7).assign(
        SMQ621=[8, 8, 3, np.nan, np.nan, np.nan, np.nan],
        SMQ640=[5, 0, np.nan, np.nan, np.nan, np.nan, np.nan],
        SMQ620=[np.nan, np.nan, np.nan, 2, 1, 1, 1],
        SMD630=[np.nan, np.nan, np.nan, np.nan, 55, 14, 14],
        SMD641=[np.nan, np.nan, np.nan, np.nan, np.nan, 12, 3],
    )
    assert silver.smoking(raw).tolist() == ["current", "former", "never", "never", "never", "current", "never"]


def youth_columns(rows: int) -> pd.DataFrame:
    """Every smoking question missing."""
    names = ["SMQ020", "SMQ040", "SMQ621", "SMQ640", "SMD641", "SMQ620", "SMD630"]
    return pd.DataFrame({name: [np.nan] * rows for name in names})


def test_alcohol_frequency_and_drinks() -> None:
    # fmt: off
    raw = pd.DataFrame({
        "ALQ120Q": [1, 5, 0, np.nan, np.nan, np.nan],
        "ALQ120U": [1, 1, np.nan, np.nan, np.nan, np.nan],
        "ALQ121":  [np.nan, np.nan, np.nan, np.nan, 5, 6],
        "ALQ110":  [np.nan, np.nan, np.nan, 2, np.nan, np.nan],
        "ALQ111":  [np.nan] * 6,
        "ALQ130":  [2, 3, 4, np.nan, 1, 2],
    })
    # fmt: on
    frequency, drinks = silver.alcohol(raw)
    assert frequency.tolist() == ["weekly", "daily", "never", "never", "weekly", "less_than_weekly"]
    assert drinks.tolist() == [2, 3, 0, 0, 1, 2]


def test_physical_activity_answers() -> None:
    raw = pd.DataFrame(
        {
            "PAD200": [1, 2, 2, 3, np.nan, np.nan],
            "PAD320": [2, 1, 2, 3, np.nan, np.nan],
            "PAQ650": [np.nan, np.nan, np.nan, np.nan, 1, 2],
            "PAQ665": [np.nan, np.nan, np.nan, np.nan, 2, 2],
        }
    )
    assert silver.physical_activity(raw).tolist() == [
        "intense",
        "moderate",
        "sedentary",
        "sedentary",
        "intense",
        "sedentary",
    ]


def test_blood_pressure_mean_without_zero_diastolic() -> None:
    # fmt: off
    raw = pd.DataFrame({
        "BPXSY1": [120], "BPXSY2": [130], "BPXSY3": [np.nan], "BPXSY4": [np.nan],
        "BPXDI1": [80], "BPXDI2": [0], "BPXDI3": [70], "BPXDI4": [np.nan],
    })
    # fmt: on
    pressure = silver.blood_pressure(raw)
    assert pressure.iloc[0].tolist() == [125, 75]


def test_survey_weight_for_the_combined_cycles() -> None:
    raw = raw_rows([1999, 2003], WTMEC4YR=[100, np.nan], WTMEC2YR=[np.nan, 300])
    assert silver.survey_weights(raw).tolist() == pytest.approx([20, 30])


def test_implausible_values_blanked(capsys: pytest.CaptureFixture[str]) -> None:
    clean = pd.DataFrame({"glucose": [29, 30, 600, 601]})
    clean = clean.assign(**{variable: np.nan for variable in silver.PLAUSIBLE_RANGES if variable != "glucose"})
    assert silver.remove_implausible_values(clean)["glucose"].tolist() == pytest.approx(
        [np.nan, 30, 600, np.nan], nan_ok=True
    )


def test_vitamin_d_in_spanish_units() -> None:
    raw = pd.DataFrame(
        {
            "PHAFSTHR": [10], "PHAFSTMN": [0], "LBXTC": [200], "LBXSCH": [np.nan], "LBXSBU": [14],
            "LBXCRP": [0.1], "LBXHSCRP": [np.nan], "LBXTR": [100], "LBXSTR": [np.nan],
            "URXUMA": [10], "URXUCR": [100], "LBXVIDMS": [75.0],
        }
    )  # fmt: skip
    assert silver.lab_derived(raw)["vitamin_d"].iloc[0] == pytest.approx(30.0)
