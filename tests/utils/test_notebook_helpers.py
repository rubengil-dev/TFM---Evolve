"""Tests: Utils - Notebook helpers (only the one with logic; the rest just shows data).

- Gold variable of a feature: the longest matching column, not the first one
"""

# Imports
from bioage.utils.notebook_helpers import variable_of


def test_variable_of_takes_the_longest_match() -> None:
    columns = ["alcohol", "alcohol_frequency", "smoking"]
    assert variable_of("alcohol_frequency_daily", columns) == "alcohol_frequency"
    assert variable_of("alcohol_drinks", columns) == "alcohol"
    assert variable_of("smoking", columns) == "smoking"
