"""Variables of each model block, and the Gold predictors left out with their reason."""

# Level 0: baseline
BASELINE = ["age", "sex"]

# Level 1: routine Spanish blood test (+ age, sex & BMI)
ROUTINE = [
    "age", "sex", "bmi",
    "hemoglobin", "erythrocytes", "mchc",
    "neutrophils", "lymphocytes", "monocytes",
    "glucose", "creatinine", "urea", "uric_acid", "hdl", "ast", "alt",
    "sodium", "potassium",
]

# Level 2: added to Routine when the user brings them
EXTRAS = [
    "ggt", "alkaline_phosphatase", "albumin", "vitamin_d",
    "chloride", "phosphorus", "ldh", "urine_acr",
]

# Level 3: added to Routine in questionnaire mode
QUESTIONNAIRE = [
    "smoking", "physical_activity", "sedentary_hours", "sleep_hours",
]

# Level 4: Routine + Extras + Questionnaire

# Variables of each level
LEVEL_COLUMNS = {
    "routine":       ROUTINE,
    "extras":        ROUTINE + EXTRAS,
    "questionnaire": ROUTINE + QUESTIONNAIRE,
    "full":          ROUTINE + EXTRAS + QUESTIONNAIRE,
}

# Algorithm kept for each level
LEVEL_MODELS = {
    "routine":       "cox",
    "extras":        "cox",
    "questionnaire": "cox",
    "full":          "cox",
}

# Not used by any model (reason)
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
    "systolic_bp":       "rarely on the PDF or known by heart; removing it does not lower the C-index",
    "diastolic_bp":      "rarely on the PDF or known by heart; removing it does not lower the C-index",
    "egfr":              "follows from creatinine, age and sex",
    "insulin":           "47% coverage, unexplained jump in 2009, rarely requested",
    "homa_ir":           "47% coverage, built from insulin",
    "nlr":               "ratio of variables in Routine; not on the PDF",
    "plr":               "ratio of variables in Routine; not on the PDF",
    "sii":               "ratio of variables in Routine; not on the PDF",
    "tg_hdl":            "ratio of variables in the model; not on the PDF",
    "ast_alt":           "ratio of variables in Routine; not on the PDF",
    "urea_creatinine":   "ratio of variables in Routine; not on the PDF",
    "albumin_globulin":  "ratio of variables in Extras; not on the PDF",
    "cpk":               "only 4 cycles, 15% of deaths",
    "waist":             "the user does not know it",
    "platelets":         "no clear effect in Routine; removing it does not lower the C-index",
    "mpv":               "no clear effect in Routine; removing it does not lower the C-index",
    "eosinophils":       "no clear effect in Routine; removing it does not lower the C-index",
    "basophils":         "no clear effect in Routine; removing it does not lower the C-index",
    "total_cholesterol": "no clear effect in Routine; removing it does not lower the C-index",
    "calcium":           "no clear effect in Routine; removing it does not lower the C-index",
    "rdw":               "analyser-dependent: +1 point moves the biological age 2-3 years",
    "triglycerides":     "no clear effect in Extras; removing it does not lower the C-index",
    "crp":               "no clear effect in Extras; removing it does not lower the C-index",
    "bilirubin":         "no clear effect in Extras; removing it does not lower the C-index",
    "iron":              "no clear effect in Extras; removing it does not lower the C-index",
    "total_protein":     "no clear effect in Extras; removing it does not lower the C-index",
    "hba1c":             "no clear effect in Extras; removing it does not lower the C-index",
    "alcohol_frequency": "protective sign from reverse causation (sick quitters)",
    "alcohol_drinks":    "protective sign from reverse causation (sick quitters)",
    "fast_food_meals":   "no clear effect in Questionnaire; removing it does not lower the C-index",
}
