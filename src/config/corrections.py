"""
CDC correction equations for laboratory method changes:
    - corrected = slope * value + intercept
    - "log10" scale: log10(corrected) = slope * log10(value) + intercept
"""

CORRECTIONS = [
    # variable     cycle  slope    intercept  scale

    # Creatinine standardization (CDC: "highly recommended")
    ("LBXSCR",     1999,  1.013,    0.147,    "linear"),
    ("LBXSCR",     2005,  0.978,   -0.016,    "linear"),

    # 2017-2018: Roche Cobas 6000 → Beckman DxC 660i scale (CDC bridging study, backward equations)
    ("LBXSAL",     2017,  1.044,    0.01128,  "linear"),
    ("LBXSAPSI",   2017,  1.001,   -0.04294,  "log10"),
    ("LBXSASSI",   2017,  1.018,    3.762,    "linear"),
    ("LBXSATSI",   2017,  1.013,    2.688,    "linear"),
    ("LBXSBU",     2017,  1.001,    0.4488,   "linear"),
    ("LBXSCH",     2017,  1.046,   -2.203,    "linear"),
    ("LBXSCK",     2017,  0.9360,   1.059,    "linear"),
    ("LBXSCR",     2017,  1.051,   -0.06945,  "linear"),
    ("LBXSGTSI",   2017,  0.8042,   2.363,    "linear"),
    ("LBXSIR",     2017,  0.9776,  -4.494,    "linear"),
    ("LBXSLDSI",   2017,  0.8568,   2.062,    "linear"),
    ("LBXSTR",     2017,  0.9655,  -7.020,    "linear"),
    ("LBXSUA",     2017,  0.9323,   0.2326,   "linear"),
]
