"""
NHANES questionnaire answer codes, from the codebooks.
"""

# Alcohol frequency
ALCOHOL_UNIT_DAYS = {1: 52, 2: 12, 3: 1}    # ALQ120U (until 2016): week, month, year
ALCOHOL_DAYS_2017 = {                       # ALQ121 (2017): drinking days per year
    0: 0,     # never in the last year
    1: 365,   # every day
    2: 260,   # nearly every day
    3: 182,   # 3-4 times a week
    4: 104,   # 2 times a week
    5: 52,    # once a week
    6: 30,    # 2-3 times a month
    7: 12,    # once a month
    8: 9,     # 7-11 times in the last year
    9: 4.5,   # 3-6 times in the last year
    10: 1.5,  # 1-2 times in the last year
}

# Refused / don't know in numeric answers (yes/no answers only use codes 1 and 2)
MISSING_CODES = {
    "ALQ120Q": [777, 999],
    "ALQ130":  [77, 99, 777, 999],
    "PAD680":  [7777, 9999],
    "DBD900":  [7777, 9999],
    "SLD010H": [77, 99],
}

# Fast food
MORE_THAN_21_MEALS = 5555  # DBD900 code, taken as 22

# Youth smoking (12-19 until 2012)
NEVER_WHOLE_CIGARETTE = 55  # SMD630 code
LIFETIME_100_PLUS = 8       # SMQ621 (2011-2012) code: 100 or more cigarettes in life; 1-7 fewer
