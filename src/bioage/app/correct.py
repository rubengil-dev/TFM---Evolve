"""Values the user corrected → in model units, and those still impossible.

- `correct_values` : Each corrected value into lab_values if it is possible now, or back to odd.
- `lab_number`     : Text as a lab writes it ("4,5") → number.

NOTE: Until the parser exists, the unit comes with each value as its factor; then it will come from its table.
"""

# Imports
from bioage.app.schemas import Correction, OddValue
from bioage.app.validation import is_possible


def correct_values(odd: list[OddValue]) -> Correction:
    """Values the user corrected, each in model units if it is possible now, or odd again.

    Args:
        odd: Odd values, with the text the user wrote.

    Returns:
        What was corrected and what is still odd.
    """
    corrected = {value.variable: lab_number(value.text) * value.factor for value in odd}
    possible = {variable: value for variable, value in corrected.items() if is_possible(variable, value)}
    return Correction(lab_values=possible, odd=[value for value in odd if value.variable not in possible])


def lab_number(text: str) -> float:
    """Text as a lab writes it → number.

    Args:
        text: E.g. "4,5" or "4.5".

    Returns:
        The number.
    """
    return float(text.strip().replace(",", "."))
