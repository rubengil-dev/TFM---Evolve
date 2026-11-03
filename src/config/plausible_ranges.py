"""
Plausible range of each numeric variable, in Gold units:
    - Context: an adult who walks in for a scheduled test (NHANES exam, app user at home)
    - Outside the limits → vital emergency or measurement artifact, not a real everyday value
    - Extreme values from a known disease (diabetes, dialysis, iron deficiency…) stay inside
    - Silver clean blanks values outside; Gold validation checks none is left
    - App: a value outside → no biological age, warning to see a doctor right away
    - Outlier clipping is part of the model preprocessing, not this table
"""

PLAUSIBLE_RANGES = {
    # variable               unit          normal          limits         why outside the limits is an emergency or an artifact

    # Blood count
    "leukocytes":           ("10^3/uL",    (4, 11),        (1, 500),      "below 1: severe neutropenia; chronic leukemias stay below 500"),
    "erythrocytes":         ("10^6/uL",    (4, 6),         (1.5, 10),     "same limits as hemoglobin; thalassemia trait reaches 8"),
    "hemoglobin":           ("g/dL",       (12, 17),       (5, 22),       "below 5: transfusion emergency; above 22: hyperviscosity"),
    "hematocrit":           ("%",          (36, 50),       (15, 65),      "same limits as hemoglobin"),
    "mcv":                  ("fL",         (80, 100),      (50, 130),     "severe thalassemia and B12 deficiency stay inside"),
    "mch":                  ("pg",         (27, 33),       (10, 45),      "tied to mcv: above 45 is an analyzer artifact"),
    "mchc":                 ("g/dL",       (32, 36),       (25, 40),      "above 40: artifact (lipemia, cold agglutinins, hemolysis)"),
    "rdw":                  ("%",          (11.5, 14.5),   (8, 40),       "analyzer range"),
    "platelets":            ("10^3/uL",    (150, 400),     (10, 1500),    "below 10: bleeding emergency; above 1500: thrombosis emergency"),
    "mpv":                  ("fL",         (7, 11),        (4, 20),       "analyzer range"),
    "neutrophils":          ("10^3/uL",    (2, 7.5),       (0.1, 100),    "below 0.1: agranulocytosis, an emergency"),
    "lymphocytes":          ("10^3/uL",    (1, 4),         (0.1, 500),    "chronic lymphocytic leukemia stays below 500"),
    "monocytes":            ("10^3/uL",    (0.2, 1),       (0, 30),       "part of leukocytes"),
    "eosinophils":          ("10^3/uL",    (0, 0.5),       (0, 30),       "part of leukocytes"),
    "basophils":            ("10^3/uL",    (0, 0.2),       (0, 10),       "part of leukocytes"),

    # Biochemistry
    "glucose":              ("mg/dL",      (70, 100),      (30, 600),     "below 30: severe hypoglycemia; above 600: hyperosmolar state"),
    "urea":                 ("mg/dL",      (15, 50),       (2, 300),      "dialysis patients stay below 300"),
    "creatinine":           ("mg/dL",      (0.6, 1.3),     (0.2, 20),     "below 0.2: not a real value; dialysis patients stay below 20"),
    "uric_acid":            ("mg/dL",      (3, 7),         (0.1, 18),     "gout stays below 18"),
    "total_cholesterol":    ("mg/dL",      (125, 200),     (40, 1000),    "familial hypercholesterolemia stays below 1000"),
    "hdl":                  ("mg/dL",      (40, 90),       (2, 250),      "below total cholesterol; genetic high HDL stays below 250"),
    "triglycerides":        ("mg/dL",      (40, 150),      (10, 5000),    "above 5000: pancreatitis risk, an emergency"),
    "ast":                  ("U/L",        (5, 40),        (2, 1000),     "above 1000: acute hepatitis, an emergency"),
    "alt":                  ("U/L",        (5, 40),        (2, 1000),     "above 1000: acute hepatitis, an emergency"),
    "ggt":                  ("U/L",        (8, 60),        (2, 5000),     "alcohol and cholestasis stay below 5000"),
    "alkaline_phosphatase": ("U/L",        (40, 130),      (5, 1500),     "bone and biliary disease stay below 1500"),
    "bilirubin":            ("mg/dL",      (0.2, 1.2),     (0, 15),       "above 15: severe jaundice, an emergency"),
    "sodium":               ("mmol/L",     (135, 145),     (100, 160),    "below 100 or above 160: seizures and coma"),
    "potassium":            ("mmol/L",     (3.5, 5.1),     (2.5, 6.5),    "outside: arrhythmia; high values are often a hemolyzed sample"),
    "hba1c":                ("%",          (4, 5.7),       (3.5, 18),     "below 3.5: hemolysis or hemoglobin variant; above 18: analyzer limit"),
    "calcium":              ("mg/dL",      (8.5, 10.5),    (6, 14),       "below 6: tetany; above 14: hypercalcemic crisis"),
    "phosphorus":           ("mg/dL",      (2.5, 4.5),     (0.5, 15),     "dialysis patients stay below 15"),
    "total_protein":        ("g/dL",       (6, 8.3),       (4, 12),       "myeloma stays below 12; below 4: severe protein loss"),
    "albumin":              ("g/dL",       (3.5, 5),       (1.5, 6),      "below 1.5: severe protein loss, edema"),
    "iron":                 ("ug/dL",      (60, 170),      (1, 500),      "iron deficiency stays inside; above 500: iron poisoning"),
    "ldh":                  ("U/L",        (120, 250),     (30, 2000),    "in every cell: below 30 is not a real value; above 2000: hemolysis or tissue damage"),
    "cpk":                  ("U/L",        (30, 200),      (5, 10000),    "above 10000: rhabdomyolysis, an emergency"),
    "chloride":             ("mmol/L",     (98, 107),      (80, 125),     "follows sodium"),
    "crp":                  ("mg/L",       (0, 5),         (0, 300),      "above 300: sepsis level"),
    "vitamin_d":            ("ng/mL",      (30, 100),      (1, 150),      "above 150: intoxication"),
    "urine_acr":            ("mg/g",       (0, 30),        (0, 50000),    "nephrotic syndrome stays below 50000"),
    "insulin":              ("uU/mL",      (2, 25),        (0.1, 3000),   "insulin-treated diabetes and insulinoma stay below 3000"),

    # Measures
    "weight":               ("kg",         None,           (30, 300),     "outside: hard to walk in for a test"),
    "height":               ("cm",         None,           (120, 220),    "adult dwarfism and gigantism stay inside"),
    "bmi":                  ("kg/m2",      (18.5, 25),     (12, 100),     "below 12: starvation; follows from weight and height"),
    "waist":                ("cm",         None,           (50, 200),     "follows from weight and height"),
    "systolic_bp":          ("mmHg",       (90, 120),      (70, 250),     "below 70: shock; above 250: hypertensive emergency"),
    "diastolic_bp":         ("mmHg",       (60, 80),       (30, 150),     "below 30: manual reading heard down to zero, an artifact; above 150: emergency"),

    # Questionnaire
    "alcohol_drinks":       ("drinks/day", (0, 2),         (0, 30),       "drinks per drinking day: above 30 is not a credible answer"),
    "sedentary_hours":      ("h/day",      None,           (0, 24),       "a day has 24 hours"),
    "fast_food_meals":      ("meals/week", None,           (0, 22),       "22 = more than 21 (NHANES code)"),
    "sleep_hours":          ("h/day",      (7, 9),         (2, 16),       "usual sleep outside 2-16 hours is not a credible answer"),
}
