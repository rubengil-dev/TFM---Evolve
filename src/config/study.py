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
