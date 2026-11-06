"""
Study design parameters.
"""

# Population
AGE_MIN = 18  # mortality follow-up only for adults
AGE_MAX = 79  # NHANES top-codes age: 80 means 80 or older (85 before 2007)

# Fasting
FASTING_HOURS_MIN = 8  # triglycerides only kept if fasting at least this long

# Form answers
ALCOHOL_FREQUENCY = {      # answer → maximum drinking days per year
    "never":            0,
    "less_than_weekly": 51,
    "weekly":           259,
    "daily":            366,
}

# Youth smoking
YOUTH_CURRENT_SMOKER_DAYS = 10  # days smoked of the past 30 to count an 18-19 year old as current smoker (until 2010)

# Follow-up
FOLLOW_UP_MIN = 0.1  # months; parametric survival models need time > 0

# Split
TEST_SIZE = 0.2
CV_FOLDS = 5
SPLIT_SEED = 42

# Model settings: fixed, first estimate
MODEL_PARAMS = {
    "cox":                {"ties": "efron"},
    "elastic_net":        {"l1_ratio": 0.5, "alphas": [0.001], "fit_baseline_model": True},
    "random_forest":      {"n_estimators": 100, "min_samples_leaf": 15, "max_features": "sqrt", "n_jobs": -1, "random_state": SPLIT_SEED},
    "gradient_boosting":  {"objective": "survival:cox", "n_estimators": 200, "learning_rate": 0.05, "max_depth": 3, "subsample": 0.8, "n_jobs": -1, "random_state": SPLIT_SEED},
}

# Evaluation
HORIZON_MONTHS = 120
CALIBRATION_GROUPS = 10
BOOTSTRAP_SAMPLES = 200

# Tuning: settings searched, as (kind, lowest, highest)
TUNING_TRIALS = 50
TUNING_SPACES = {
    "gradient_boosting": {
        "n_estimators":      ("int", 100, 800),
        "learning_rate":     ("log", 0.01, 0.2),
        "max_depth":         ("int", 2, 6),
        "min_child_weight":  ("int", 1, 50),
        "subsample":         ("float", 0.5, 1.0),
        "colsample_bytree":  ("float", 0.5, 1.0),
        "reg_lambda":        ("log", 0.001, 10.0),
    },
    "elastic_net": {
        "alphas":            ("log_list", 0.0001, 0.05),
        "l1_ratio":          ("float", 0.01, 1.0),
    },
}

# Comparison of tuned models: folds other than those used for tuning
COMPARISON_SEED = 7

# Preprocessing: imputation groups
AGE_GROUP_EDGES = [18, 30, 40, 50, 60, 70, 80]  # lower bound included

# Preprocessing: extremes
CLIP_QUANTILES = (0.001, 0.999)

# Preprocessing: skewness above 2 in train
LOG_VARIABLES = [
    "rdw", "neutrophils", "lymphocytes", "monocytes", "eosinophils", "basophils",
    "glucose", "creatinine", "urea", "ast", "alt",
    "triglycerides", "ggt", "alkaline_phosphatase", "bilirubin", "hba1c", "crp", "ldh", "urine_acr",
    "alcohol_drinks", "fast_food_meals",
]

# Preprocessing: U-shaped relationships
SQUARED_VARIABLES = ["bmi", "sleep_hours"]

# Preprocessing: categories of each variable; the first one is the reference and gets no column
CATEGORICAL_LEVELS = {
    "sex":                ["female", "male"],
    "smoking":            ["never", "former", "current"],
    "alcohol_frequency":  ["never", "less_than_weekly", "weekly", "daily"],
    "physical_activity":  ["sedentary", "moderate", "intense"],
}
