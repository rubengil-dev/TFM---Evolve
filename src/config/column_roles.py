"""
Role of each Gold column: identification, outcome or candidate predictor.
"""

# Identification and survey weight (not model inputs)
ID_COLUMNS = ["seqn", "cycle", "weight_exam"]

# Outcome
OUTCOME_COLUMNS = ["follow_up_months", "death"]

# Candidate predictors from Silver clean
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

QUESTIONNAIRE = [
    "smoking", "alcohol_frequency", "alcohol_drinks", "physical_activity",
    "sedentary_hours", "fast_food_meals", "sleep_hours",
]

SILVER_PREDICTORS = DEMOGRAPHICS + BLOOD_COUNT + BIOCHEMISTRY + MEASURES + QUESTIONNAIRE
