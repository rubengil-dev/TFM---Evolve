"""Limits, error codes, result groups and margin of the app.

- Ages the app calculates for
- PDF: largest size and how to recognize it
- Error codes
- Groups of variables shown in the result: blood test and habits
- Data needed: most values that can be missing, fewest Extras to use their model
- Margin ±: base error and error for what is missing
"""

# Imports
from typing import Literal

# Ages the app calculates for
MIN_AGE = 16
MAX_AGE = 90

# PDF
MAX_PDF_MB = 10
PDF_MARK = b"%PDF-"
PDF_MARK_WITHIN = 1024  # bytes

# Errors the user is told about
ErrorCode = Literal["unreadable", "too_few", "impossible", "impossible_bmi", "too_young", "too_old"]

# Groups of the result
BLOOD_GROUPS = {
    "minerals":   ["vitamin_d", "sodium", "potassium", "chloride", "phosphorus"],
    "sugar":      ["glucose"],
    "red_cells":  ["hemoglobin", "erythrocytes", "mchc"],
    "defences":   ["neutrophils", "lymphocytes", "monocytes"],
    "liver":      ["ast", "alt", "ggt", "alkaline_phosphatase", "albumin"],
    "kidney":     ["creatinine", "urea", "uric_acid", "urine_acr"],
    "weight":     ["bmi"],
    "other":      ["hdl", "ldh"],
}

HABIT_GROUPS = {
    "smoking":    ["smoking"],
    "exercise":   ["physical_activity"],
    "sitting":    ["sedentary_hours"],
    "sleep":      ["sleep_hours"],
}

# Group that also takes what the rest do not explain, so all add up to biological age - age
OTHER = "other"

# Data needed (notebooks/missing_values.ipynb)
# Most Routine lab values that can be missing: 9 of 10 people move up to 7 years
MAX_MISSING = {"quick": 5, "full": 8}
# Fewest Extras that make their model better: level without them → level with them
MIN_EXTRAS = {"routine": ("extras", 3), "questionnaire": ("full", 4)}

# Margin ± = √(base² + Routine values missing² + Extras missing²), in years
# Base (notebooks/margin.ipynb): calibration in years; risk below the median → low risk
# level              low risk below   low risk   rest
BASE_MARGIN = {
    "routine":       (0.0366,         5.24,      1.30),
    "extras":        (0.0331,         5.75,      1.36),
    "questionnaire": (0.0344,         5.32,      1.63),
    "full":          (0.0317,         4.98,      1.88),
}
# Routine values missing → median years the age moves (notebooks/missing_values.ipynb), 0 to 15
MISSING_MARGIN = {
    "quick": [0, 0.85, 1.43, 1.85, 2.18, 2.45, 2.69, 2.91, 3.06, 3.20, 3.31, 3.41, 3.47, 3.51, 3.55, 3.57],
    "full":  [0, 0.66, 1.14, 1.50, 1.78, 2.01, 2.21, 2.37, 2.51, 2.63, 2.73, 2.83, 2.88, 2.93, 2.97, 2.99],
}
# Extras known → median years the age moves against knowing the 8, in the levels that use them
EXTRAS_MARGIN = {
    "extras": [3.48, 3.17, 2.87, 2.55, 2.20, 1.84, 1.40, 0.84, 0],
    "full":   [3.04, 2.78, 2.53, 2.24, 1.95, 1.63, 1.25, 0.72, 0],
}
