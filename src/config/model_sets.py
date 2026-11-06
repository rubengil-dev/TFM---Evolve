"""
Variables of each model block, and the Gold predictors left out with their reason.
"""

# Level 0: baseline
BASELINE = ["age", "sex"]

# Level 1: routine Spanish blood test, plus age, sex and BMI (from weight and height)
BASE = [
    "age", "sex", "bmi",
    "hemoglobin", "erythrocytes", "mchc", "rdw",
    "neutrophils", "lymphocytes", "monocytes",
    "glucose", "creatinine", "urea", "uric_acid", "hdl", "ast", "alt",
    "sodium", "potassium",
]

# Level 2: added to Base when the user brings them
EXTRAS = [
    "triglycerides", "ggt", "alkaline_phosphatase", "bilirubin", "iron",
    "total_protein", "albumin", "hba1c", "crp", "vitamin_d",
    "chloride", "phosphorus", "ldh", "urine_acr",
    "systolic_bp", "diastolic_bp",
]

# Level 2: added to Base in questionnaire mode
QUESTIONNAIRE = [
    "smoking", "alcohol_frequency", "alcohol_drinks", "physical_activity",
    "sedentary_hours", "fast_food_meals", "sleep_hours",
]

# Algorithm kept for each level
LEVEL_MODELS = {
    "base":  "cox",
}

# Not used by any model: variable → reason
DISCARDED = {
    "weight":            "input of bmi",
    "height":            "input of bmi",
    "hematocrit":        "follows from hemoglobin / mchc",
    "mcv":               "follows from hematocrit / erythrocytes",
    "mch":               "follows from hemoglobin / erythrocytes",
    "leukocytes":        "sum of the five white cell types",
    "non_hdl":           "total_cholesterol - hdl",
    "globulin":          "total_protein - albumin",
    "pulse_pressure":    "systolic_bp - diastolic_bp",
    "egfr":              "follows from creatinine, age and sex",
    "insulin":           "47% coverage, unexplained jump in 2009, rarely requested",
    "homa_ir":           "47% coverage, built from insulin",
    "nlr":               "ratio of variables in Base; not on the PDF",
    "plr":               "ratio of variables in Base; not on the PDF",
    "sii":               "ratio of variables in Base; not on the PDF",
    "tg_hdl":            "ratio of variables in the model; not on the PDF",
    "ast_alt":           "ratio of variables in Base; not on the PDF",
    "urea_creatinine":   "ratio of variables in Base; not on the PDF",
    "albumin_globulin":  "ratio of variables in Extras; not on the PDF",
    "cpk":               "only 4 cycles, 15% of deaths",
    "waist":             "the user does not know it",
    "platelets":         "no clear effect in Base; removing it does not lower the C-index",
    "mpv":               "no clear effect in Base; removing it does not lower the C-index",
    "eosinophils":       "no clear effect in Base; removing it does not lower the C-index",
    "basophils":         "no clear effect in Base; removing it does not lower the C-index",
    "total_cholesterol": "no clear effect in Base; removing it does not lower the C-index",
    "calcium":           "no clear effect in Base; removing it does not lower the C-index",
}
