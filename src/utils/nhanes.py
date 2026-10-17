"""
NHANES naming helpers.
"""

def cycle_label(year):
    """Cycle name creator: 1999 → '1999_2000'."""
    return f"{year}_{year + 1}"
