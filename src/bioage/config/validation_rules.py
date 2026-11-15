"""
Gold validation thresholds (plausible ranges in config/plausible_ranges.py, answers in config/study.py).
"""

# Size
MIN_PERSONS = 45000            # one lost cycle drops 4000-5600 persons
MIN_PERSONS_PER_CYCLE = 4000
MIN_DEATHS = 5000              # survival models learn from deaths, not rows

# Follow-up
MAX_FOLLOW_UP = 252  # months; from 1999 to the end of 2019

# Coverage (% of persons with a value)
MIN_COVERAGE = 90
MIN_COVERAGE_PARTIAL = 35
PARTIAL_COVERAGE = [  # measured on part of the sample by design (subsample, fasting, some cycles)
    "cpk", "insulin", "homa_ir", "fast_food_meals", "triglycerides", "tg_hdl", "sedentary_hours",
    "sleep_hours", "crp", "alcohol_frequency", "alcohol_drinks", "vitamin_d",
]

# Required values (text answers may be missing, except sex)
REQUIRED = ["seqn", "cycle", "weight_exam", "follow_up_months", "death", "age", "sex"]

# Consistency between variables
LOWER_THAN = [  # (lower, higher)
    ("hdl", "total_cholesterol"),
    ("albumin", "total_protein"),
    ("diastolic_bp", "systolic_bp"),
]
BMI_TOLERANCE = 1  # kg/m2 between bmi and weight / height²
