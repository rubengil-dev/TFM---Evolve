"""Tests: App - Values the user corrected.

- Possible now → in model units, with the factor of its unit; still impossible → odd again, as written
- The lab writes decimals with a comma or a dot
- Both limits of the range are possible
"""

# Imports
import pytest

from bioage.app.correct import correct_values, lab_number
from bioage.app.schemas import OddValue
from bioage.config.plausible_ranges import PLAUSIBLE_RANGES


def odd(variable: str, text: str, factor: float = 1) -> OddValue:
    return OddValue(variable=variable, text=text, unit="x", factor=factor)


def test_possible_values_are_in_model_units_and_the_rest_stays_odd() -> None:
    still = odd("sodium", "1400")
    correction = correct_values([odd("potassium", "4,5"), odd("glucose", "5,5", factor=18), still])
    assert correction.lab_values == {"potassium": 4.5, "glucose": pytest.approx(99)}
    assert correction.odd == [still]


@pytest.mark.parametrize(("text", "number"), [("4,5", 4.5), ("4.5", 4.5), (" 12 ", 12.0)])
def test_lab_number_takes_comma_or_dot(text: str, number: float) -> None:
    assert lab_number(text) == number


def test_both_limits_are_possible() -> None:
    low, high = PLAUSIBLE_RANGES["glucose"][2]
    assert set(correct_values([odd("glucose", str(low)), odd("hdl", "1000")]).lab_values) == {"glucose"}
    assert correct_values([odd("glucose", str(high))]).odd == []
