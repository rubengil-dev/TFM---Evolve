"""Reads a blood test in PDF.

NOTE: Until the parser exists, every PDF gives the same made-up person (EXAMPLE_READING).
"""

# Imports
from bioage.app.schemas import AppError, Mode, Reading
from bioage.app.validation import check_age, check_enough
from bioage.config.app import PDF_MARK, PDF_MARK_WITHIN

# Sex missing on purpose: the front has to ask for it
# fmt: off
EXAMPLE_READING = Reading(
    lab_values={
        "hemoglobin":    15.0,
        "erythrocytes":  5.0,
        "mchc":          34.0,
        "neutrophils":   4.0,
        "lymphocytes":   2.0,
        "monocytes":     0.5,
        "glucose":       98,
        "creatinine":    1.0,
        "urea":          35,
        "uric_acid":     6.0,
        "hdl":           48,
        "ast":           24,
        "alt":           28,
        "sodium":        140,
        "potassium":     4.3,
    },
    age=45,
    sex=None,
    odd=[],
)
# fmt: on


def read_pdf(pdf: bytes, mode: Mode) -> Reading:
    """PDF → values of the blood test, and age and sex if it has them.

    Args:
        pdf: Content of the file.
        mode: Mode the user chose, which decides how many values can be missing.

    Returns:
        What was read.

    Raises:
        AppError: If it is not a PDF, lacks too many values, or the app does not calculate for that age.
    """
    if PDF_MARK not in pdf[:PDF_MARK_WITHIN]:
        raise AppError("unreadable")
    reading = EXAMPLE_READING
    if reading.age is not None:
        check_age(reading.age)
    check_enough(set(reading.lab_values) | {odd.variable for odd in reading.odd}, mode)
    return reading
