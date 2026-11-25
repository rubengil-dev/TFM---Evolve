"""Role of each Gold column.

- Identification and survey weight
- Outcome
- Candidate predictors, by type
- Derived features
"""

# Identification and survey weight (not model inputs)
ID_COLUMNS = ["seqn", "cycle", "weight_exam"]

# Outcome
OUTCOME_COLUMNS = ["follow_up_months", "death"]

# Predictors selected from Silver clean
DEMOGRAPHICS = ["age", "sex"]

BLOOD_COUNT = [
    "leukocytes", "erythrocytes", "hemoglobin", "hematocrit", "mcv", "mch", "mchc", "rdw",
    "platelets", "mpv", "neutrophils", "lymphocytes", "monocytes", "eosinophils", "basophils",
]

BIOCHEMISTRY = [
    "glucose", "urea", "creatinine", "uric_acid", "total_cholesterol", "hdl", "triglycerides",
    "ast", "alt", "ggt", "alkaline_phosphatase", "bilirubin", "sodium", "potassium",
    "hba1c", "calcium", "phosphorus", "total_protein", "albumin", "iron", "ldh", "cpk",
    "chloride", "crp", "vitamin_d", "urine_acr", "insulin",
]

MEASURES = ["weight", "height", "bmi", "waist", "systolic_bp", "diastolic_bp"]

HABITS = [
    "smoking", "alcohol_frequency", "alcohol_drinks", "physical_activity",
    "sedentary_hours", "fast_food_meals", "sleep_hours",
]

SELECTED_PREDICTORS = DEMOGRAPHICS + BLOOD_COUNT + BIOCHEMISTRY + MEASURES + HABITS

# Derived features (utils/features.py)
DERIVED_FEATURES = [
    "nlr", "plr", "sii", "non_hdl", "tg_hdl", "ast_alt", "globulin", "albumin_globulin",
    "urea_creatinine", "egfr", "homa_ir", "pulse_pressure",
]
