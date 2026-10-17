"""
NHANES variable aliases:
    - Same measure and unit, different name depending on the cycle
    - Old name → name used in most cycles
    - Questionnaires not included: a new code usually means a new question
"""

RENAMES = {
    # Biochemistry (2001-2002)
    "LBDSAPSI": "LBXSAPSI",  # alkaline phosphatase (U/L)
    "LBDSCR":   "LBXSCR",    # creatinine (mg/dL)
    "LBDSLDSI": "LBXSLDSI",  # LDH (U/L)
    "LBDSPH":   "LBXSPH",    # phosphorus (mg/dL)
    "LBDSTB":   "LBXSTB",    # total bilirubin (mg/dL)

    # Glucose and insulin (1999-2002)
    "LBXGLUSI": "LBDGLUSI",  # fasting glucose (mmol/L)
    "LBXINSI":  "LBDINSI",   # insulin (pmol/L)

    # HDL (1999-2004)
    "LBDHDL":   "LBDHDD",    # HDL (mg/dL), 1999-2002
    "LBDHDLSI": "LBDHDDSI",  # HDL (mmol/L), 1999-2002
    "LBXHDD":   "LBDHDD",    # HDL (mg/dL), 2003-2004

    # Vitamin D (2001-2006, converted by CDC to LC-MS/MS)
    "LBDVIDMS": "LBXVIDMS",  # 25-OH vitamin D (nmol/L)

    # Urine (1999-2004)
    "URXUCRSI": "URXCRS",    # urine creatinine (umol/L)
    "URXUMASI": "URXUMS",    # urine albumin (mg/L)

    # Bone alkaline phosphatase (2001-2002)
    "LBDBAP":   "LBXBAP",    # ug/L
}
