"""
Plausible range of each numeric variable, in Gold units:
    - Catches data and unit errors, not outliers: limits far beyond the normal range
    - Outside the limits → impossible in a living adult or a measurement artifact
    - Silver clean blanks values outside; Gold validation checks none is left; the app can reuse it on the review screen
    - Outlier clipping is part of the model preprocessing, not this table
"""

PLAUSIBLE_RANGES = {
    # variable               unit          normal          limits         why outside the limits is an error

    # Blood count
    "leukocytes":           ("10^3/uL",    (4, 11),        (0.1, 1000),   "leukemias reach a few hundred"),
    "erythrocytes":         ("10^6/uL",    (4, 6),         (1, 10),       "polycythemia stays below 10"),
    "hemoglobin":           ("g/dL",       (12, 17),       (2, 26),       "below 2 not compatible with life"),
    "hematocrit":           ("%",          (36, 50),       (6, 80),       "same limits as hemoglobin"),
    "mcv":                  ("fL",         (80, 100),      (50, 150),     "severe thalassemia stays above 50"),
    "mch":                  ("pg",         (27, 33),       (12, 50),      "tied to mcv: above 50 is a counting error"),
    "mchc":                 ("g/dL",       (32, 36),       (20, 45),      "physical limit of hemoglobin in a red cell"),
    "rdw":                  ("%",          (11.5, 14.5),   (8, 40),       "analyzer range"),
    "platelets":            ("10^3/uL",    (150, 400),     (1, 3000),     "thrombocythemia rarely exceeds 2000"),
    "mpv":                  ("fL",         (7, 11),        (4, 20),       "analyzer range"),
    "neutrophils":          ("10^3/uL",    (2, 7.5),       (0, 300),      "part of leukocytes"),
    "lymphocytes":          ("10^3/uL",    (1, 4),         (0, 1000),     "chronic lymphocytic leukemia reaches hundreds"),
    "monocytes":            ("10^3/uL",    (0.2, 1),       (0, 100),      "part of leukocytes"),
    "eosinophils":          ("10^3/uL",    (0, 0.5),       (0, 100),      "part of leukocytes"),
    "basophils":            ("10^3/uL",    (0, 0.2),       (0, 50),       "part of leukocytes"),

    # Biochemistry
    "glucose":              ("mg/dL",      (70, 100),      (10, 3000),    "hyperosmolar coma stays below 3000"),
    "urea":                 ("mg/dL",      (15, 50),       (2, 500),      "end-stage kidney failure stays below 500"),
    "creatinine":           ("mg/dL",      (0.6, 1.3),     (0.1, 30),     "end-stage kidney failure stays below 30"),
    "uric_acid":            ("mg/dL",      (3, 7),         (0.1, 25),     "tumor lysis stays below 25"),
    "total_cholesterol":    ("mg/dL",      (125, 200),     (40, 2000),    "familial hypercholesterolemia and cholestasis stay below 2000"),
    "hdl":                  ("mg/dL",      (40, 90),       (2, 250),      "below total cholesterol"),
    "triglycerides":        ("mg/dL",      (40, 150),      (10, 20000),   "chylomicronemia reaches about 10000"),
    "ast":                  ("U/L",        (5, 40),        (2, 30000),    "acute liver failure reaches tens of thousands"),
    "alt":                  ("U/L",        (5, 40),        (2, 30000),    "acute liver failure reaches tens of thousands"),
    "ggt":                  ("U/L",        (8, 60),        (2, 10000),    "cholestasis stays in the thousands"),
    "alkaline_phosphatase": ("U/L",        (40, 130),      (5, 5000),     "bone and biliary disease stay in the thousands"),
    "bilirubin":            ("mg/dL",      (0.2, 1.2),     (0, 60),       "severe jaundice stays below 60"),
    "sodium":               ("mmol/L",     (135, 145),     (90, 200),     "outside: coma and death"),
    "potassium":            ("mmol/L",     (3.5, 5.1),     (1, 10),       "outside: cardiac arrest"),
    "hba1c":                ("%",          (4, 5.7),       (3, 20),       "below 3: hemolysis or hemoglobin variant, not glycemia"),
    "calcium":              ("mg/dL",      (8.5, 10.5),    (4, 20),       "outside: cardiac arrest"),
    "phosphorus":           ("mg/dL",      (2.5, 4.5),     (0.5, 20),     "outside: not compatible with life"),
    "total_protein":        ("g/dL",       (6, 8.3),       (2, 15),       "myeloma stays below 15"),
    "albumin":              ("g/dL",       (3.5, 5),       (0.5, 7),      "below total protein"),
    "iron":                 ("ug/dL",      (60, 170),      (1, 1500),     "iron poisoning stays below 1500"),
    "ldh":                  ("U/L",        (120, 250),     (30, 20000),   "in every cell: below 30 is not a real value"),
    "cpk":                  ("U/L",        (30, 200),      (5, 500000),   "rhabdomyolysis reaches hundreds of thousands"),
    "chloride":             ("mmol/L",     (98, 107),      (60, 150),     "same limits as sodium"),
    "crp":                  ("mg/L",       (0, 5),         (0, 1000),     "septic shock stays below 1000"),
    "vitamin_d":            ("ng/mL",      (30, 100),      (1, 1000),     "intoxication stays below 1000"),
    "urine_acr":            ("mg/g",       (0, 30),        (0, 50000),    "nephrotic syndrome stays below 50000"),
    "insulin":              ("uU/mL",      (2, 25),        (0.1, 3000),   "insulinoma stays below 3000"),

    # Measures
    "weight":               ("kg",         None,           (25, 650),     "beyond the lightest and heaviest adults recorded"),
    "height":               ("cm",         None,           (55, 275),     "beyond the shortest and tallest adults recorded"),
    "bmi":                  ("kg/m2",      (18.5, 25),     (8, 200),      "follows from weight and height"),
    "waist":                ("cm",         None,           (40, 250),     "follows from weight and height"),
    "systolic_bp":          ("mmHg",       (90, 120),      (50, 350),     "outside: shock or a measurement error"),
    "diastolic_bp":         ("mmHg",       (60, 80),       (20, 250),     "below 20: manual reading heard down to zero, an artifact"),

    # Questionnaire
    "alcohol_drinks":       ("drinks/day", (0, 2),         (0, 50),       "drinks per drinking day: above 50 is not a credible answer"),
    "sedentary_hours":      ("h/day",      None,           (0, 24),       "a day has 24 hours"),
    "fast_food_meals":      ("meals/week", None,           (0, 22),       "22 = more than 21 (NHANES code)"),
    "sleep_hours":          ("h/day",      (7, 9),         (0, 24),       "a day has 24 hours"),
}
