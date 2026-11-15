"""
CDC correction equations for laboratory method changes:
    - One row per equation, applied to the cycles between the first and the last start year
    - Rows of the same variable and cycle chain in order: each one takes the previous result
    - Equation: slope * x + intercept + square * x², written on its scale (x = value, log10 or √value)
    - Original values: (low, high) of the uncorrected value the row applies to, both included (None = no limit)
    - Minimum: lowest corrected value allowed (None = no minimum)
"""

CORRECTIONS = [
    # variable    cycles        scale     slope    intercept  square  original values  minimum

    # Serum creatinine standardization (CDC: "highly recommended")
    ("LBXSCR",    (1999, 1999), "linear", 1.013,    0.147,    0,      None,            None),
    ("LBXSCR",    (2005, 2005), "linear", 0.978,   -0.016,    0,      None,            None),

    # 2017-2018 biochemistry: Roche Cobas 6000 → Beckman DxC 660i scale (bridging study, backward equations)
    ("LBXSAL",    (2017, 2017), "linear", 1.044,    0.01128,  0,      None,            None),
    ("LBXSAPSI",  (2017, 2017), "log10",  1.001,   -0.04294,  0,      None,            None),
    ("LBXSASSI",  (2017, 2017), "linear", 1.018,    3.762,    0,      None,            None),
    ("LBXSATSI",  (2017, 2017), "linear", 1.013,    2.688,    0,      None,            None),
    ("LBXSBU",    (2017, 2017), "linear", 1.001,    0.4488,   0,      None,            None),
    ("LBXSCH",    (2017, 2017), "linear", 1.046,   -2.203,    0,      None,            None),
    ("LBXSCK",    (2017, 2017), "linear", 0.9360,   1.059,    0,      None,            None),
    ("LBXSCR",    (2017, 2017), "linear", 1.051,   -0.06945,  0,      None,            None),
    ("LBXSGTSI",  (2017, 2017), "linear", 0.8042,   2.363,    0,      None,            None),
    ("LBXSIR",    (2017, 2017), "linear", 0.9776,  -4.494,    0,      None,            None),
    ("LBXSLDSI",  (2017, 2017), "linear", 0.8568,   2.062,    0,      None,            None),
    ("LBXSTR",    (2017, 2017), "linear", 0.9655,  -7.020,    0,      None,            None),
    ("LBXSUA",    (2017, 2017), "linear", 0.9323,   0.2326,   0,      None,            None),

    # 2017-2018 hs-CRP (mg/L): Cobas 6000 → DxC 660i scale up to 20; not below 0.08, the DxC value under its detection limit
    ("LBXHSCRP",  (2017, 2017), "linear", 1.150,   -0.3397,   0,      (None, 20),      0.08),

    # Insulin (uU/mL): 5 assays chained to the 2013-2018 Tosoh AIA scale (forward equations)
    ("LBXIN",     (1999, 2001), "linear", 1.0027,  -2.2934,   0,      None,            None),  # Pharmacia → Tosoh (2003-2004)
    ("LBXIN",     (1999, 2003), "linear", 0.9501,   1.4890,   0,      None,            None),  # Tosoh → Mercodia (2005-2010)
    ("LBXIN",     (1999, 2009), "linear", 0.8868,  -0.0744,   0.0011, None,            None),  # Mercodia → Roche (2011-2012)
    ("LBXIN",     (1999, 2011), "log10",  1.024,   -0.0802,   0,      None,            None),  # Roche → Tosoh AIA (2013-2018)

    # Urine creatinine (mg/dL, whole numbers) before 2007 → 2007 onwards scale, piecewise
    ("URXUCR",    (1999, 2005), "sqrt",   1.02,    -0.36,     0,      (None, 74),      None),
    ("URXUCR",    (1999, 2005), "sqrt",   1.05,    -0.74,     0,      (75, 249),       None),
    ("URXUCR",    (1999, 2005), "sqrt",   1.01,    -0.10,     0,      (250, None),     None),
]
