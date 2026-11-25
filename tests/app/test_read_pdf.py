"""Tests: App - Reading of the PDF, until the parser exists.

- The mark of a PDF can be within the first bytes, not later
- A PDF without age is accepted: the front asks for it
"""

# Imports
import pytest

from bioage.app import read_pdf
from bioage.app.read_pdf import EXAMPLE_READING
from bioage.app.schemas import AppError
from bioage.config.app import PDF_MARK, PDF_MARK_WITHIN


def test_mark_after_other_bytes_is_accepted() -> None:
    assert read_pdf.read_pdf(b" " * (PDF_MARK_WITHIN - len(PDF_MARK)) + PDF_MARK) == EXAMPLE_READING


def test_mark_too_late_is_refused() -> None:
    with pytest.raises(AppError, match="unreadable"):
        read_pdf.read_pdf(b" " * PDF_MARK_WITHIN + PDF_MARK)


def test_pdf_without_age_is_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(read_pdf, "EXAMPLE_READING", EXAMPLE_READING.model_copy(update={"age": None}))
    assert read_pdf.read_pdf(PDF_MARK).age is None
