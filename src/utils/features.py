"""
Builds derived features from lab values and measures:
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

from src.config.study import AGE_GROUP_EDGES


def derived_features(data):
    """
    Every derived feature from Silver clean columns:
        - Any input missing → output missing
    """
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


def egfr_ckd_epi_2021(creatinine, age, sex):
    """
    Glomerular filtration rate (mL/min/1.73 m2), CKD-EPI 2021 without race:
        - 142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^-1.200 × 0.9938^age × 1.012 (female)
        - Sex missing (not male or female) → missing
    """
    female = sex == "female"
    kappa = np.where(female, 0.7, 0.9)
    alpha = np.where(female, -0.241, -0.302)
    ratio = creatinine / kappa
    egfr = 142 * np.minimum(ratio, 1) ** alpha * np.maximum(ratio, 1) ** -1.200 * 0.9938 ** age
    return (egfr * np.where(female, 1.012, 1)).where(sex.isin(["male", "female"]))


def age_groups(data):
    """Age group of each person, e.g. '30-39'; missing outside the study ages."""
    edges = AGE_GROUP_EDGES
    labels = [f"{low}-{high - 1}" for low, high in zip(edges[:-1], edges[1:])]
    return pd.cut(data["age"], bins=edges, right=False, labels=labels)
