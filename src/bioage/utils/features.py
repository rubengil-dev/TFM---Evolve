"""Builds derived features from lab values and measures.

- Inflammation: NLR, PLR, SII
- Lipids: non-HDL cholesterol, TG/HDL
- Liver and proteins: AST/ALT, globulin, albumin/globulin
- Kidney: urea/creatinine, eGFR (CKD-EPI 2021)
- Glucose: HOMA-IR
- Blood pressure: pulse pressure
- Age groups, for the preprocessing and the evaluation
"""

# Imports
import numpy as np
import pandas as pd

from bioage.config.study import AGE_GROUP_EDGES


def derived_features(data: pd.DataFrame) -> pd.DataFrame:
    """Every derived feature from Silver clean columns.

    - Any input missing → output missing

    Args:
        data: Table with the Silver clean columns.

    Returns:
        One column per derived feature, same rows as data.
    """
    # fmt: off
    return pd.DataFrame({
        "nlr":               data["neutrophils"] / data["lymphocytes"],
        "plr":               data["platelets"] / data["lymphocytes"],
        "sii":               data["platelets"] * data["neutrophils"] / data["lymphocytes"],
        "non_hdl":           data["total_cholesterol"] - data["hdl"],
        "tg_hdl":            data["triglycerides"] / data["hdl"],
        "ast_alt":           data["ast"] / data["alt"],
        "globulin":          data["total_protein"] - data["albumin"],
        "albumin_globulin":  data["albumin"] / (data["total_protein"] - data["albumin"]),
        "urea_creatinine":   data["urea"] / data["creatinine"],
        "egfr":              egfr_ckd_epi_2021(data["creatinine"], data["age"], data["sex"]),
        "homa_ir":           data["glucose"] * data["insulin"] / 405,
        "pulse_pressure":    data["systolic_bp"] - data["diastolic_bp"],
    }, index=data.index)
    # fmt: on


def egfr_ckd_epi_2021(creatinine: pd.Series, age: pd.Series, sex: pd.Series) -> pd.Series:
    """Glomerular filtration rate (mL/min/1.73 m2), CKD-EPI 2021 without race.

    - 142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^-1.200 × 0.9938^age × 1.012 (female)
    - Sex missing (not male or female) → missing

    Args:
        creatinine: Serum creatinine, in mg/dL.
        age: Age, in years.
        sex: 'male' or 'female'.

    Returns:
        Filtration rate of each person.
    """
    female = sex == "female"
    kappa = np.where(female, 0.7, 0.9)
    alpha = np.where(female, -0.241, -0.302)
    ratio = creatinine / kappa
    egfr = 142 * np.minimum(ratio, 1) ** alpha * np.maximum(ratio, 1) ** -1.200 * 0.9938**age
    return (egfr * np.where(female, 1.012, 1)).where(sex.isin(["male", "female"]))


def age_groups(data: pd.DataFrame) -> pd.Series:
    """Age group of each person, e.g. '30-39'; missing outside the study ages.

    Args:
        data: Table with the age column.

    Returns:
        Group label of each person.
    """
    edges = AGE_GROUP_EDGES
    labels = [f"{low}-{high - 1}" for low, high in zip(edges[:-1], edges[1:], strict=True)]
    return pd.cut(data["age"], bins=edges, right=False, labels=labels)
