"""
Cleaning silver raw to silver clean: Filtering population and variables, cleaning process and readable names.
    1. Population: allowing only population with exam done, not pregnant and with lab results
    2. CDC corrections for laboratory method changes
    3. Variables:
        - Kept as they are, renamed (CLEAN_NAMES)
        - Same test from two files → one column (cholesterol, CRP)
        - Spanish lab units (urea, urine albumin/creatinine ratio)
        - Triglycerides only with fasting ≥ FASTING_HOURS_MIN
        - Blood pressure: mean of readings
        - Questionnaires → form answers (skipped questions: never drinkers, never smokers)
        - Survey weights for the 10 cycles combined
    4. Save into data/02_silver/silver_clean.parquet
"""

# Imports
import numpy as np
import pandas as pd

from src.config.corrections import CORRECTIONS
from src.config.paths import SILVER_CLEAN, SILVER_RAW
from src.config.renames import CLEAN_NAMES
from src.config.sources import ALCOHOL_DAYS_2017, ALCOHOL_UNIT_DAYS, CYCLES, MISSING_CODES, MORE_THAN_21_MEALS
from src.config.study import ALCOHOL_FREQUENCY, FASTING_HOURS_MIN
from src.utils.nhanes import cycle_label


def run():
    """Silver clean step, called from main."""
    raw = pd.read_parquet(SILVER_RAW)
    raw = filter_population(raw)
    raw = apply_corrections(raw)
    raw = remove_missing_codes(raw)

    clean = pd.concat([
        kept_variables(raw),
        sex(raw),
        survey_weights(raw),
        lab_derived(raw),
        blood_pressure(raw),
        questionnaire(raw),
    ], axis=1)

    save(clean)
    print_summary(clean)


def filter_population(raw):
    """Exam done (RIDSTATR = 2), not pregnant (RIDEXPRG = 1) and at least one lab value (CLEAN_NAMES starting with LB)."""
    lab_columns = [name for name in CLEAN_NAMES if name.startswith("LB")]
    has_lab = raw[lab_columns].notna().any(axis=1)
    return raw[(raw["RIDSTATR"] == 2) & (raw["RIDEXPRG"] != 1) & has_lab].copy()


def apply_corrections(raw):
    """CDC equations (CORRECTIONS) applied to their cycle."""
    for variable, year, slope, intercept, scale in CORRECTIONS:
        rows = raw["cycle"] == cycle_label(year)
        value = raw.loc[rows, variable]
        if scale == "log10":
            raw.loc[rows, variable] = 10 ** (slope * np.log10(value) + intercept)
        else:
            raw.loc[rows, variable] = slope * value + intercept
    return raw


def remove_missing_codes(raw):
    """Refused / don't know codes in numeric answers (MISSING_CODES) → missing."""
    for variable, codes in MISSING_CODES.items():
        raw[variable] = raw[variable].mask(raw[variable].isin(codes))
    return raw


def kept_variables(raw):
    """Variables kept as they are, with readable names. 'cycle' after seqn."""
    kept = raw[list(CLEAN_NAMES)].rename(columns=CLEAN_NAMES)
    kept.insert(1, "cycle", raw["cycle"])
    return kept


def sex(raw):
    """male / female."""
    return raw["RIAGENDR"].map({1: "male", 2: "female"}).rename("sex")


def survey_weights(raw):
    """
    Weights for the cycles combined (CDC rule):
        - 1999-2002: 4-year weight × 2 / number of cycles
        - 2003-2018: 2-year weight × 1 / number of cycles
    """
    early = raw["cycle"].isin([cycle_label(1999), cycle_label(2001)])
    cycles = len(CYCLES)
    return pd.DataFrame({
        "weight_exam":    np.where(early, raw["WTMEC4YR"] * 2, raw["WTMEC2YR"]) / cycles,
        "weight_fasting": np.where(early, raw["WTSAF4YR"] * 2, raw["WTSAF2YR"]) / cycles,
    }, index=raw.index)


def lab_derived(raw):
    """
    Lab variables built from NHANES ones:
        - Total cholesterol: lipid file, biochemistry profile if missing
        - Urea = BUN × 2.14
        - CRP (mg/L): standard until 2010 (mg/dL × 10), high sensitivity from 2015
        - Triglycerides: lipid file, biochemistry profile if missing; only if fasting ≥ FASTING_HOURS_MIN
        - Urine albumin/creatinine ratio (mg/g)
    """
    fasting_hours = raw["PHAFSTHR"] + raw["PHAFSTMN"] / 60
    fasted = fasting_hours >= FASTING_HOURS_MIN
    return pd.DataFrame({
        "total_cholesterol": raw["LBXTC"].fillna(raw["LBXSCH"]),
        "urea":              raw["LBXSBU"] * 2.14,
        "crp":               (raw["LBXCRP"] * 10).fillna(raw["LBXHSCRP"]),
        "triglycerides":     raw["LBXTR"].fillna(raw["LBXSTR"]).where(fasted),
        "urine_acr":         raw["URXUMA"] / raw["URXUCR"] * 100,
        "fasting_hours":     fasting_hours,
    }, index=raw.index)


def blood_pressure(raw):
    """Mean of available readings (up to 4). Diastolic 0 (not measurable) → missing."""
    systolic = raw[["BPXSY1", "BPXSY2", "BPXSY3", "BPXSY4"]]
    diastolic = raw[["BPXDI1", "BPXDI2", "BPXDI3", "BPXDI4"]].replace(0, np.nan)
    return pd.DataFrame({
        "systolic_bp":  systolic.mean(axis=1),
        "diastolic_bp": diastolic.mean(axis=1),
    }, index=raw.index)


def questionnaire(raw):
    """Questionnaires → form answers."""
    frequency, drinks = alcohol(raw)
    return pd.DataFrame({
        "smoking":           smoking(raw),
        "alcohol_frequency": frequency,
        "alcohol_drinks":    drinks,
        "physical_activity": physical_activity(raw),
        "sedentary_hours":   raw["PAD680"] / 60,
        "fast_food_meals":   raw["DBD900"].replace(MORE_THAN_21_MEALS, 22),
        "sleep_hours":       raw["SLD012"].fillna(raw["SLD010H"]),
    }, index=raw.index)


def smoking(raw):
    """never (< 100 cigarettes in life) / former / current."""
    ever = raw["SMQ020"]
    now = raw["SMQ040"]
    answer = np.select([ever == 2, now.isin([1, 2]), now == 3], ["never", "current", "former"], default=None)
    return pd.Series(answer, index=raw.index)


def alcohol(raw):
    """
    Drinking frequency (ALCOHOL_FREQUENCY answers) and drinks per drinking day:
        - Until 2016: quantity × unit (ALQ120Q/U); lifetime abstainers (ALQ110 = 2) → never
        - 2017: ALQ121 answer; never had a drink (ALQ111 = 2) → never
        - Never → 0 drinks
    """
    quantity = raw["ALQ120Q"]
    days = (quantity * raw["ALQ120U"].map(ALCOHOL_UNIT_DAYS)).mask(quantity == 0, 0)
    days = days.fillna(raw["ALQ121"].map(ALCOHOL_DAYS_2017))
    never_drank = (raw["ALQ110"] == 2) | (raw["ALQ111"] == 2)
    days = days.mask(days.isna() & never_drank, 0)

    limits = list(ALCOHOL_FREQUENCY.values())
    bins = [-0.5] + [limit + 0.5 for limit in limits]
    frequency = pd.cut(days, bins=bins, labels=list(ALCOHOL_FREQUENCY)).astype(object)
    drinks = raw["ALQ130"].mask(frequency == "never", 0)
    return frequency, drinks


def physical_activity(raw):
    """
    sedentary / moderate / intense:
        - Until 2006: vigorous or moderate activity in the past 30 days (PAD200, PAD320)
        - From 2007: vigorous or moderate recreational activity (PAQ650, PAQ665)
        - "Unable to do activity" (3) → no
    """
    vigorous = raw["PAD200"].fillna(raw["PAQ650"])
    moderate = raw["PAD320"].fillna(raw["PAQ665"])
    answer = np.select(
        [vigorous == 1, moderate == 1, vigorous.isin([2, 3]) & moderate.isin([2, 3])],
        ["intense", "moderate", "sedentary"],
        default=None,
    )
    return pd.Series(answer, index=raw.index)


def save(clean):
    """Silver clean → parquet."""
    clean.to_parquet(SILVER_CLEAN, index=False)


def print_summary(clean):
    """Persons, deaths, columns and % with value per variable."""
    print(f"{len(clean)} persons, {int(clean['death'].sum())} deaths, {clean.shape[1]} columns, saved to {SILVER_CLEAN.name}\n")
    coverage = (clean.notna().mean() * 100).round(0).astype(int)
    print(coverage.to_string())
