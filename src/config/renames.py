"""
Variable names:
    - RENAMES: NHANES aliases between cycles (Bronze → Silver raw)
    - CLEAN_NAMES: NHANES names → readable names (Silver raw → Silver clean)
"""

# Aliases between cycles
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

# Readable names
CLEAN_NAMES = {
    # Identification and outcome
    "SEQN":         "seqn",
    "MORTSTAT":     "death",              # 0 alive, 1 deceased
    "PERMTH_EXM":   "follow_up_months",   # from exam
    "UCOD_LEADING": "death_cause",        # NCHS leading cause recode

    # Survey design
    "SDMVPSU":      "psu",
    "SDMVSTRA":     "strata",

    # Demographics
    "RIDAGEYR":     "age",                # years

    # Blood count
    "LBXWBCSI":     "leukocytes",         # 10^3/uL
    "LBXRBCSI":     "erythrocytes",       # 10^6/uL
    "LBXHGB":       "hemoglobin",         # g/dL
    "LBXHCT":       "hematocrit",         # %
    "LBXMCVSI":     "mcv",                # fL
    "LBXMCHSI":     "mch",                # pg
    "LBXMC":        "mchc",               # g/dL
    "LBXRDW":       "rdw",                # %
    "LBXPLTSI":     "platelets",          # 10^3/uL
    "LBXMPSI":      "mpv",                # fL
    "LBXNEPCT":     "neutrophils_pct",    # %
    "LBXLYPCT":     "lymphocytes_pct",    # %
    "LBXMOPCT":     "monocytes_pct",      # %
    "LBXEOPCT":     "eosinophils_pct",    # %
    "LBXBAPCT":     "basophils_pct",      # %
    "LBDNENO":      "neutrophils",        # 10^3/uL
    "LBDLYMNO":     "lymphocytes",        # 10^3/uL
    "LBDMONO":      "monocytes",          # 10^3/uL
    "LBDEONO":      "eosinophils",        # 10^3/uL
    "LBDBANO":      "basophils",          # 10^3/uL

    # Biochemistry
    "LBXSGL":       "glucose",            # mg/dL
    "LBXSCR":       "creatinine",         # mg/dL
    "LBXSUA":       "uric_acid",          # mg/dL
    "LBDHDD":       "hdl",                # mg/dL
    "LBXSASSI":     "ast",                # U/L
    "LBXSATSI":     "alt",                # U/L
    "LBXSGTSI":     "ggt",                # U/L
    "LBXSAPSI":     "alkaline_phosphatase",  # U/L
    "LBXSTB":       "bilirubin",          # mg/dL
    "LBXSNASI":     "sodium",             # mmol/L
    "LBXSKSI":      "potassium",          # mmol/L
    "LBXSCLSI":     "chloride",           # mmol/L
    "LBXSCA":       "calcium",            # mg/dL
    "LBXSPH":       "phosphorus",         # mg/dL
    "LBXSTP":       "total_protein",      # g/dL
    "LBXSAL":       "albumin",            # g/dL
    "LBXSIR":       "iron",               # ug/dL
    "LBXSLDSI":     "ldh",                # U/L
    "LBXSCK":       "cpk",                # U/L
    "LBXGH":        "hba1c",              # %
    "LBXVIDMS":     "vitamin_d",          # nmol/L
    "LBXIN":        "insulin",            # uU/mL, fasting subsample

    # Measures
    "BMXWT":        "weight",             # kg
    "BMXHT":        "height",             # cm
    "BMXBMI":       "bmi",                # kg/m2
    "BMXWAIST":     "waist",              # cm
}
