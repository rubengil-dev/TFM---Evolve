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
