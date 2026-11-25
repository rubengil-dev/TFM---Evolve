"""Limits and error codes of the app.

- Ages the app calculates for
- PDF: largest size and how to recognize it
- Error codes
"""

# Imports
from typing import Literal

# Ages the app calculates for
MIN_AGE = 16
MAX_AGE = 90

# PDF
MAX_PDF_MB = 10
PDF_MARK = b"%PDF-"
PDF_MARK_WITHIN = 1024  # bytes

# Errors the user is told about
ErrorCode = Literal["unreadable", "too_few", "impossible", "too_young", "too_old"]
