"""Limits, error codes, result groups and margin of the app.

- Ages the app calculates for
- PDF: largest size and how to recognize it
- Error codes
- Groups of variables shown in the result: blood test and habits
- Level of each mode, with and without Extras
- Data needed and margin ±: criteria
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

# Level of each mode, and the one it goes to with enough Extras
MODE_LEVELS = {"quick": "routine", "full": "questionnaire"}
EXTRAS_LEVELS = {"routine": "extras", "questionnaire": "full"}

# Data needed and margin ±: criteria; modeling/s7_margin.py measures them when training and saves them in each bundle
MOVE_YEARS = 7        # most years the age can move for what is missing...
MOVE_SHARE = 0.9      # ...for this share of people
MIN_GAIN = 0.002      # C-index among people of the same age the Extras must add to use their model
MARGIN_REPEATS = 3    # random draws of what is hidden
