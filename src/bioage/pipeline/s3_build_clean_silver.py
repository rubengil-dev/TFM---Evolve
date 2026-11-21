"""Build silver clean data layer.

Filters the study population and cleans the variables.

Changes:
- Population: exam done, not pregnant and at least one lab value.
- Variables:
  - Readable names (renames.py).
  - Converting to Spanish lab units: urea, urine albumin/creatinine ratio & vit-D.
  - Merging tests that come from two files: cholesterol, triglycerides & CRP.
  - Removing triglycerides if fasting < FASTING_HOURS_MIN.
  - Averaging blood pressure.
  - Questionnaires → form answers (skipped questions: never drinkers, never smokers)
  - Exam survey weight for the 10 cycles combined
- Values:
  - CDC corrections for NHANES laboratory method changes (corrections.py).
  - Removing values outside PLAUSIBLE_RANGES.
"""

# Imports
import numpy as np
import pandas as pd

from bioage.config.corrections import CORRECTIONS
from bioage.config.nhanes_codes import (
    ALCOHOL_DAYS_2017,
    ALCOHOL_UNIT_DAYS,
    LIFETIME_100_CIGARETTES,
    MISSING_CODES,
    MORE_THAN_21_MEALS,
    NEVER_WHOLE_CIGARETTE,
)
from bioage.config.paths import SILVER_CLEAN, SILVER_RAW
from bioage.config.plausible_ranges import PLAUSIBLE_RANGES
from bioage.config.renames import CLEAN_NAMES
from bioage.config.sources import CYCLES
from bioage.config.study import ALCOHOL_FREQUENCY, FASTING_HOURS_MIN, YOUTH_CURRENT_SMOKER_DAYS
from bioage.utils.nhanes import cycle_label
from bioage.utils.summary import print_layer_summary


def run() -> None:
    """Silver clean step, called from main."""
    raw = pd.read_parquet(SILVER_RAW)
    raw = filter_population(raw)
    raw = apply_corrections(raw)
    raw = remove_missing_codes(raw)

    clean = pd.concat(
        [
            kept_variables(raw),
            sex(raw),
            survey_weights(raw),
            lab_derived(raw),
            blood_pressure(raw),
            questionnaire(raw),
        ],
        axis=1,
    )
    clean = vitamin_d_to_ng_ml(clean)
    clean = remove_implausible_values(clean)

    save(clean)
    print_layer_summary(clean, SILVER_CLEAN)


def filter_population(raw: pd.DataFrame) -> pd.DataFrame:
    """Exam done, not pregnant and at least one lab value.

    Means:
        - RIDSTATR = 2
        - RIDEXPRG ≠ 1
        - CLEAN_NAMES column starting with LB

    Args:
        raw: Silver raw table.

    Returns:
        The rows of the study population.
    """
    lab_columns = [name for name in CLEAN_NAMES if name.startswith("LB")]
    has_lab = raw[lab_columns].notna().any(axis=1)
    return raw[(raw["RIDSTATR"] == 2) & (raw["RIDEXPRG"] != 1) & has_lab].copy()


def apply_corrections(raw: pd.DataFrame) -> pd.DataFrame:
    """CDC equations (CORRECTIONS) applied in order.

    - Same variable and cycle: each equation takes the previous result
    - Limits of each row checked on the original value

    Args:
        raw: Silver raw table.

    Returns:
        The same table with the corrected values.
    """
    original = raw[list(dict.fromkeys(row[0] for row in CORRECTIONS))].copy()
    for variable, cycles, scale, slope, intercept, square, limits, minimum in CORRECTIONS:
        rows = in_cycles(raw["cycle"], cycles) & within(original[variable], limits)
        raw.loc[rows, variable] = corrected(raw.loc[rows, variable], scale, slope, intercept, square, minimum)
    return raw


def in_cycles(cycle: pd.Series, cycles: tuple[int, int]) -> pd.Series:
    """Rows whose cycle starts between the first and the last year of cycles.

    Args:
        cycle: Cycle name of each row.
        cycles: First and last start year, both included.

    Returns:
        True for the rows inside.
    """
    first, last = cycles
    return cycle.isin([cycle_label(year) for year in CYCLES if first <= year <= last])


def within(values: pd.Series, limits: tuple[float | None, float | None] | None) -> pd.Series:
    """Values between low and high, both included.

    Args:
        values: Original values of the variable.
        limits: Low and high (None = no limit on that side); None → every row.

    Returns:
        True for the rows inside.
    """
    if limits is None:
        return pd.Series(True, index=values.index)
    low, high = limits
    return values.between(-np.inf if low is None else low, np.inf if high is None else high)


def corrected(
    value: pd.Series, scale: str, slope: float, intercept: float, square: float, minimum: float | None
) -> pd.Series:
    """One CDC equation on its scale, back to the original units and not below minimum.

    Args:
        value: Values to correct.
        scale: Scale the equation is written on: 'linear', 'log10' or 'sqrt'.
        slope: Coefficient of x.
        intercept: Constant term.
        square: Coefficient of x².
        minimum: Lowest corrected value allowed, or None.

    Returns:
        Corrected values.
    """
    x = to_scale(value, scale)
    result = from_scale(slope * x + intercept + square * x**2, scale)
    return result if minimum is None else result.clip(lower=minimum)


def to_scale(value: pd.Series, scale: str) -> pd.Series:
    """Original units → scale of the equation (linear, log10 or sqrt).

    Args:
        value: Values in the original units.
        scale: Scale of the equation.

    Returns:
        Values on that scale.
    """
    if scale == "log10":
        return np.log10(value)
    if scale == "sqrt":
        return np.sqrt(value)
    return value


def from_scale(value: pd.Series, scale: str) -> pd.Series:
    """Scale of the equation → original units.

    Args:
        value: Values on the scale of the equation.
        scale: Scale of the equation.

    Returns:
        Values in the original units.
    """
    if scale == "log10":
        return 10**value
    if scale == "sqrt":
        return value**2
    return value


def remove_missing_codes(raw: pd.DataFrame) -> pd.DataFrame:
    """Refused / don't know codes in numeric answers (MISSING_CODES) → missing.

    Args:
        raw: Silver raw table.

    Returns:
        The same table without those codes.
    """
    for variable, codes in MISSING_CODES.items():
        raw[variable] = raw[variable].mask(raw[variable].isin(codes))
    return raw


def kept_variables(raw: pd.DataFrame) -> pd.DataFrame:
    """Variables kept as they are, with readable names; 'cycle' after seqn.

    Args:
        raw: Silver raw table.

    Returns:
        The renamed columns.
    """
    kept = raw[list(CLEAN_NAMES)].rename(columns=CLEAN_NAMES)
    kept.insert(1, "cycle", raw["cycle"])
    return kept


def sex(raw: pd.DataFrame) -> pd.Series:
    """Male / female.

    Args:
        raw: Silver raw table.

    Returns:
        Sex of each person.
    """
    return raw["RIAGENDR"].map({1: "male", 2: "female"}).rename("sex")


def survey_weights(raw: pd.DataFrame) -> pd.Series:
    """Exam weight for the cycles combined (CDC rule).

    - 1999-2002: 4-year weight × 2 / number of cycles
    - 2003-2018: 2-year weight × 1 / number of cycles

    Args:
        raw: Silver raw table.

    Returns:
        Weight of each person.
    """
    early = raw["cycle"].isin([cycle_label(1999), cycle_label(2001)])
    weight = np.where(early, raw["WTMEC4YR"] * 2, raw["WTMEC2YR"]) / len(CYCLES)
    return pd.Series(weight, index=raw.index, name="weight_exam")


def lab_derived(raw: pd.DataFrame) -> pd.DataFrame:
    """Units conversion and variables built from NHANES ones.

    - Total cholesterol: lipid file, biochemistry profile if missing
    - Urea = BUN × 2.14
    - CRP (mg/L): standard until 2010 (mg/dL × 10), high sensitivity from 2015
    - Triglycerides: lipid file, biochemistry profile if missing; only if fasting ≥ FASTING_HOURS_MIN
    - Urine albumin/creatinine ratio (mg/g)

    Args:
        raw: Silver raw table.

    Returns:
        One column per variable.
    """
    fasting_hours = raw["PHAFSTHR"] + raw["PHAFSTMN"] / 60
    fasted = fasting_hours >= FASTING_HOURS_MIN
    # fmt: off
    return pd.DataFrame({
        "total_cholesterol": raw["LBXTC"].fillna(raw["LBXSCH"]),
        "urea":              raw["LBXSBU"] * 2.14,
        "crp":               (raw["LBXCRP"] * 10).fillna(raw["LBXHSCRP"]),
        "triglycerides":     raw["LBXTR"].fillna(raw["LBXSTR"]).where(fasted),
        "urine_acr":         raw["URXUMA"] / raw["URXUCR"] * 100,
    }, index=raw.index)
    # fmt: on


def blood_pressure(raw: pd.DataFrame) -> pd.DataFrame:
    """Mean of the available readings (up to 4); diastolic 0 (not measurable) → missing.

    Args:
        raw: Silver raw table.

    Returns:
        Systolic and diastolic pressure.
    """
    systolic = raw[["BPXSY1", "BPXSY2", "BPXSY3", "BPXSY4"]]
    diastolic = raw[["BPXDI1", "BPXDI2", "BPXDI3", "BPXDI4"]].replace(0, np.nan)  # 0 = manual measurement artifact

    return pd.DataFrame(
        {
            "systolic_bp": systolic.mean(axis=1),
            "diastolic_bp": diastolic.mean(axis=1),
        },
        index=raw.index,
    )


def questionnaire(raw: pd.DataFrame) -> pd.DataFrame:
    """Questionnaires → form answers.

    Args:
        raw: Silver raw table.

    Returns:
        One column per habit question.
    """
    frequency, drinks = alcohol(raw)
    # fmt: off
    return pd.DataFrame({
        "smoking"           :smoking(raw),
        "alcohol_frequency" :frequency,
        "alcohol_drinks"    :drinks,
        "physical_activity" :physical_activity(raw),
        "sedentary_hours"   :raw["PAD680"] / 60,
        "fast_food_meals"   :raw["DBD900"].replace(MORE_THAN_21_MEALS, 22),
        "sleep_hours"       :raw["SLD012"].fillna(raw["SLD010H"]),
    }, index=raw.index)
    # fmt: on


def smoking(raw: pd.DataFrame) -> pd.Series:
    """Never (< 100 cigarettes in life) / former / current.

    - Adult questions (SMQ020, SMQ040)
    - Youth questions for 18-19 year olds until 2012 (youth_smoking)

    Args:
        raw: Silver raw table.

    Returns:
        Answer of each person.
    """
    ever = raw["SMQ020"]
    now = raw["SMQ040"]
    answer = np.select([ever == 2, now.isin([1, 2]), now == 3], ["never", "current", "former"], default=None)
    return pd.Series(answer, index=raw.index).fillna(youth_smoking(raw))


def youth_smoking(raw: pd.DataFrame) -> pd.Series:
    """Youth questions → adult answers.

    - 2011-2012: cigarettes in life (SMQ621); 100 or more → current if smoked in the past 30 days, else former
    - Until 2010: never tried (SMQ620) or never a whole cigarette (SMD630) → never;
      smoked on ≥ YOUTH_CURRENT_SMOKER_DAYS of the past 30 (SMQ640, SMD641) → current; fewer → never

    Args:
        raw: Silver raw table.

    Returns:
        Answer of each person who got the youth questions; missing for the rest.
    """
    lifetime = raw["SMQ621"]
    days = raw["SMQ640"].fillna(raw["SMD641"])
    days = days.where(days.between(0, 30))
    youth = lifetime.notna() | raw["SMQ620"].notna()
    answer = np.select(
        [
            lifetime.between(1, LIFETIME_100_CIGARETTES - 1),
            (lifetime == LIFETIME_100_CIGARETTES) & (days >= 1),
            (lifetime == LIFETIME_100_CIGARETTES) & (days == 0),
            raw["SMQ620"] == 2,
            raw["SMD630"] == NEVER_WHOLE_CIGARETTE,
            days >= YOUTH_CURRENT_SMOKER_DAYS,
            days < YOUTH_CURRENT_SMOKER_DAYS,
        ],
        ["never", "current", "former", "never", "never", "current", "never"],
        default=None,
    )
    return pd.Series(answer, index=raw.index).where(youth)


def alcohol(raw: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Drinking frequency (ALCOHOL_FREQUENCY answers) and drinks per drinking day.

    - Until 2016: quantity × unit (ALQ120Q/U); lifetime abstainers (ALQ110 = 2) → never
    - 2017: ALQ121 answer; never had a drink (ALQ111 = 2) → never
    - Never → 0 drinks

    Args:
        raw: Silver raw table.

    Returns:
        Frequency and drinks of each person.
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


def physical_activity(raw: pd.DataFrame) -> pd.Series:
    """Sedentary / moderate / intense.

    - Until 2006: vigorous or moderate activity in the past 30 days (PAD200, PAD320)
    - From 2007: vigorous or moderate recreational activity (PAQ650, PAQ665)
    - "Unable to do activity" (3) → no

    Args:
        raw: Silver raw table.

    Returns:
        Answer of each person.
    """
    vigorous = raw["PAD200"].fillna(raw["PAQ650"])
    moderate = raw["PAD320"].fillna(raw["PAQ665"])
    answer = np.select(
        [vigorous == 1, moderate == 1, vigorous.isin([2, 3]) & moderate.isin([2, 3])],
        ["intense", "moderate", "sedentary"],
        default=None,
    )
    return pd.Series(answer, index=raw.index)


def vitamin_d_to_ng_ml(clean: pd.DataFrame) -> pd.DataFrame:
    """Vitamin D: nmol/L → ng/mL (÷ 2.5).

    Args:
        clean: Silver clean table.

    Returns:
        The same table with vitamin D in ng/mL.
    """
    clean["vitamin_d"] = clean["vitamin_d"] / 2.5
    return clean


def remove_implausible_values(clean: pd.DataFrame) -> pd.DataFrame:
    """Values outside the PLAUSIBLE_RANGES limits → missing, printing a count per variable.

    Args:
        clean: Silver clean table.

    Returns:
        The same table without the implausible values.
    """
    print("Implausible values set to missing:")
    for variable, (_, _, (low, high), _) in PLAUSIBLE_RANGES.items():
        implausible = clean[variable].notna() & ~clean[variable].between(low, high)
        if implausible.any():
            print(f"    {variable}: {implausible.sum()}")
        clean[variable] = clean[variable].mask(implausible)
    print()
    return clean


def save(clean: pd.DataFrame) -> None:
    """Silver clean → parquet.

    Args:
        clean: Silver clean table.
    """
    clean.to_parquet(SILVER_CLEAN, index=False)
