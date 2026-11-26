"""Tests: App - Reading of the PDF, until the parser exists.

- The mark of a PDF can be within the first bytes, not later
- A PDF without age is accepted: the front asks for it
- Too many values missing for the mode → too_few; values to correct count as there
"""

# Imports
import pytest

from bioage.app import read_pdf
from bioage.app.read_pdf import EXAMPLE_READING
from bioage.app.schemas import AppError, OddValue
from bioage.config.app import PDF_MARK, PDF_MARK_WITHIN


def test_mark_after_other_bytes_is_accepted() -> None:
    assert read_pdf.read_pdf(b" " * (PDF_MARK_WITHIN - len(PDF_MARK)) + PDF_MARK, "full") == EXAMPLE_READING


def test_mark_too_late_is_refused() -> None:
    with pytest.raises(AppError, match="unreadable"):
        read_pdf.read_pdf(b" " * PDF_MARK_WITHIN + PDF_MARK, "full")


def test_pdf_without_age_is_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(read_pdf, "EXAMPLE_READING", EXAMPLE_READING.model_copy(update={"age": None}))
    assert read_pdf.read_pdf(PDF_MARK, "full").age is None


@pytest.mark.parametrize(
    ("dropped", "mode", "fine"), [(5, "quick", True), (6, "quick", False), (8, "full", True), (9, "full", False)]
)
def test_too_many_values_missing_for_the_mode(
    monkeypatch: pytest.MonkeyPatch, dropped: int, mode: str, fine: bool
) -> None:
    kept = dict(list(EXAMPLE_READING.lab_values.items())[dropped:])
    monkeypatch.setattr(read_pdf, "EXAMPLE_READING", EXAMPLE_READING.model_copy(update={"lab_values": kept}))
    if fine:
        read_pdf.read_pdf(PDF_MARK, mode)
    else:
        with pytest.raises(AppError, match="too_few"):
            read_pdf.read_pdf(PDF_MARK, mode)


def test_values_to_correct_count_as_there(monkeypatch: pytest.MonkeyPatch) -> None:
    variables = list(EXAMPLE_READING.lab_values)
    odd = [OddValue(variable=variable, text="1", unit="x", factor=1) for variable in variables[:6]]
    kept = {variable: EXAMPLE_READING.lab_values[variable] for variable in variables[6:]}
    reading = EXAMPLE_READING.model_copy(update={"lab_values": kept, "odd": odd})
    monkeypatch.setattr(read_pdf, "EXAMPLE_READING", reading)
    read_pdf.read_pdf(PDF_MARK, "quick")
