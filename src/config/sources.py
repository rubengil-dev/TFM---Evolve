"""
External data sources:
    - URLs and files to download per cycle
    - Mortality file layout
    - Download settings
"""

# NHANES cycles (start years)
CYCLES = [1999, 2001, 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017]

# URLs
NHANES_URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{year}/DataFiles/{name}.{ext}"
MORTALITY_FILE = "NHANES_{cycle}_MORT_2019_PUBLIC.dat"
MORTALITY_URL = "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/datalinkage/linked_mortality/" + MORTALITY_FILE

# Mortality file layout (fixed width, character positions from NCHS read-in program)
MORTALITY_COLUMNS = {
    "SEQN":         (1, 6),
    "ELIGSTAT":     (15, 15),  # 1 eligible, 2 under 18, 3 ineligible
    "MORTSTAT":     (16, 16),  # 0 alive, 1 deceased
    "UCOD_LEADING": (17, 19),  # underlying cause of death
    "DIABETES":     (20, 20),
    "HYPERTEN":     (21, 21),
    "PERMTH_INT":   (43, 45),  # months of follow-up from interview
    "PERMTH_EXM":   (46, 48),  # months of follow-up from exam
}

# NHANES file names per cycle (None: not measured)
DATASETS = {
    #          1999        2001        2003        2005        2007        2009        2011        2013        2015        2017

    # Demographics
    "DEMO":   ["DEMO",     "DEMO_B",   "DEMO_C",   "DEMO_D",   "DEMO_E",   "DEMO_F",   "DEMO_G",   "DEMO_H",   "DEMO_I",   "DEMO_J"],   # age, sex, ethnicity, survey weights

    # Examination
    "BMX":    ["BMX",      "BMX_B",    "BMX_C",    "BMX_D",    "BMX_E",    "BMX_F",    "BMX_G",    "BMX_H",    "BMX_I",    "BMX_J"],    # body measures
    "BPX":    ["BPX",      "BPX_B",    "BPX_C",    "BPX_D",    "BPX_E",    "BPX_F",    "BPX_G",    "BPX_H",    "BPX_I",    "BPX_J"],    # blood pressure
    "CVX":    ["CVX",      "CVX_B",    "CVX_C",    None,       None,       None,       None,       None,       None,       None],       # treadmill test, estimated VO2 max
    "DXX":    ["DXX",      "DXX_B",    "DXX_C",    "DXX_D",    None,       None,       "DXX_G",    "DXX_H",    "DXX_I",    "DXX_J"],    # DXA body composition

    # Laboratory
    "BIOPRO": ["LAB18",    "L40_B",    "L40_C",    "BIOPRO_D", "BIOPRO_E", "BIOPRO_F", "BIOPRO_G", "BIOPRO_H", "BIOPRO_I", "BIOPRO_J"], # biochemistry profile
    "CBC":    ["LAB25",    "L25_B",    "L25_C",    "CBC_D",    "CBC_E",    "CBC_F",    "CBC_G",    "CBC_H",    "CBC_I",    "CBC_J"],    # complete blood count
    "GHB":    ["LAB10",    "L10_B",    "L10_C",    "GHB_D",    "GHB_E",    "GHB_F",    "GHB_G",    "GHB_H",    "GHB_I",    "GHB_J"],    # HbA1c
    "GLU":    ["LAB10AM",  "L10AM_B",  "L10AM_C",  "GLU_D",    "GLU_E",    "GLU_F",    "GLU_G",    "GLU_H",    "GLU_I",    "GLU_J"],    # fasting glucose (+ insulin until 2012)
    "INS":    [None,       None,       None,       None,       None,       None,       None,       "INS_H",    "INS_I",    "INS_J"],    # fasting insulin
    "TCHOL":  ["LAB13",    "L13_B",    "L13_C",    "TCHOL_D",  "TCHOL_E",  "TCHOL_F",  "TCHOL_G",  "TCHOL_H",  "TCHOL_I",  "TCHOL_J"],  # total cholesterol (+ HDL until 2004)
    "HDL":    [None,       None,       None,       "HDL_D",    "HDL_E",    "HDL_F",    "HDL_G",    "HDL_H",    "HDL_I",    "HDL_J"],    # HDL cholesterol
    "TRIGLY": ["LAB13AM",  "L13AM_B",  "L13AM_C",  "TRIGLY_D", "TRIGLY_E", "TRIGLY_F", "TRIGLY_G", "TRIGLY_H", "TRIGLY_I", "TRIGLY_J"], # fasting triglycerides and LDL
    "CRP":    ["LAB11",    "L11_B",    "L11_C",    "CRP_D",    "CRP_E",    "CRP_F",    None,       None,       "HSCRP_I",  "HSCRP_J"],  # CRP (hs-CRP from 2015)
    "VID":    [None,       "VID_B",    "VID_C",    "VID_D",    "VID_E",    "VID_F",    "VID_G",    "VID_H",    "VID_I",    "VID_J"],    # vitamin D (2001-2006 converted to LC-MS/MS)
    "ALB_CR": ["LAB16",    "L16_B",    "L16_C",    "ALB_CR_D", "ALB_CR_E", "ALB_CR_F", "ALB_CR_G", "ALB_CR_H", "ALB_CR_I", "ALB_CR_J"], # urine albumin and creatinine
    "FASTQX": ["PH",       "PH_B",     "PH_C",     "FASTQX_D", "FASTQX_E", "FASTQX_F", "FASTQX_G", "FASTQX_H", "FASTQX_I", "FASTQX_J"], # fasting hours before blood draw

    # Questionnaire
    "SMQ":    ["SMQ",      "SMQ_B",    "SMQ_C",    "SMQ_D",    "SMQ_E",    "SMQ_F",    "SMQ_G",    "SMQ_H",    "SMQ_I",    "SMQ_J"],    # smoking
    "ALQ":    ["ALQ",      "ALQ_B",    "ALQ_C",    "ALQ_D",    "ALQ_E",    "ALQ_F",    "ALQ_G",    "ALQ_H",    "ALQ_I",    "ALQ_J"],    # alcohol
    "PAQ":    ["PAQ",      "PAQ_B",    "PAQ_C",    "PAQ_D",    "PAQ_E",    "PAQ_F",    "PAQ_G",    "PAQ_H",    "PAQ_I",    "PAQ_J"],    # physical activity and sedentary time (new format from 2007)
    "DBQ":    ["DBQ",      "DBQ_B",    "DBQ_C",    "DBQ_D",    "DBQ_E",    "DBQ_F",    "DBQ_G",    "DBQ_H",    "DBQ_I",    "DBQ_J"],    # diet behavior: self-rated diet, fast food
    "SLQ":    [None,       None,       None,       "SLQ_D",    "SLQ_E",    "SLQ_F",    "SLQ_G",    "SLQ_H",    "SLQ_I",    "SLQ_J"],    # sleep hours
}

# Codebooks published as .pdf instead of .htm
PDF_DOCS = {"DXX", "DXX_B", "DXX_C"}

# Download settings
RETRIES = 4
TIMEOUT = 120  # seconds
