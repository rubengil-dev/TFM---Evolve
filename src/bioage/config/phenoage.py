"""PhenoAge (Levine et al., 2018): the published formula constants and its units.

- Weights: one per input, in the units of the paper
- Units: Gold value × factor = value in the units of the paper
- Age curve: the NHANES III age at each risk, fitted with the paper's 10-year horizon
"""

# Inputs
PHENOAGE_VARIABLES = [
    "albumin",
    "creatinine",
    "glucose",
    "crp",
    "lymphocytes",
    "leukocytes",
    "mcv",
    "rdw",
    "alkaline_phosphatase",
]

# Units: Gold → paper
UNIT_FACTORS = {
    "albumin":    10,          # g/dL → g/L
    "creatinine": 88.4,        # mg/dL → µmol/L
    "glucose":    1 / 18.016,  # mg/dL → mmol/L
    "crp":        1 / 10,      # mg/L → mg/dL
}
CRP_MIN = 0.08  # mg/L, detection limit; avoids log(0)

# Weights of the score
PHENOAGE_WEIGHTS = {
    "albumin":               -0.0336,
    "creatinine":             0.0095,
    "glucose":                0.1953,
    "log_crp":                0.0954,
    "lymphocyte_percent":    -0.0120,
    "mcv":                    0.0268,
    "rdw":                    0.3306,
    "alkaline_phosphatase":   0.00188,
    "leukocytes":             0.0554,
    "age":                    0.0804,
}
PHENOAGE_INTERCEPT = -19.9067

# Risk: Gompertz over the paper's horizon (not ours: the age curve only holds at 120 months)
PHENOAGE_HORIZON_MONTHS = 120
GOMPERTZ_GAMMA = 0.0076927

# Age curve: age = intercept + log(-factor × log(1 - risk)) / slope
AGE_CURVE_INTERCEPT = 141.50225
AGE_CURVE_FACTOR = 0.00553
AGE_CURVE_SLOPE = 0.090165
