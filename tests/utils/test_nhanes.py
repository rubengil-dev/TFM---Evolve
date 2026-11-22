"""Tests: Utils - NHANES readers.

- Mortality file: each field read from its character positions, '.' as missing, Windows line ends,
  5- and 6-digit SEQN
- Cycle names from the start year
"""

# Imports
from pathlib import Path

import pandas as pd

from bioage.utils.nhanes import cycle_label, read_mortality

# Made-up people in the NCHS fixed-width layout: eligible and dead, under 18 (no follow-up), and alive
# as in the later files (6-digit SEQN, months aligned left, line cut after the last value)
MORTALITY_LINES = [
    "12345" + " " * 9 + "1100601" + " " * 21 + "120118",
    "12346" + " " * 9 + "2.   .." + " " * 21 + ".  .  ",
    "102345" + " " * 8 + "10   .." + " " * 21 + "27 26",
]


def test_mortality_fields_from_their_positions(tmp_path: Path) -> None:
    path = tmp_path / "NHANES_1999_2000_MORT_2019_PUBLIC.dat"
    path.write_bytes("\r\n".join(MORTALITY_LINES).encode() + b"\r\n")
    mortality = read_mortality(path)
    dead, child, alive = mortality.iloc[0], mortality.iloc[1], mortality.iloc[2]
    assert mortality["SEQN"].tolist() == [12345, 12346, 102345]
    assert (dead["ELIGSTAT"], dead["MORTSTAT"], dead["UCOD_LEADING"]) == (1, 1, 6)
    assert (dead["DIABETES"], dead["HYPERTEN"]) == (0, 1)
    assert (dead["PERMTH_INT"], dead["PERMTH_EXM"]) == (120, 118)
    assert child["ELIGSTAT"] == 2
    assert child[["MORTSTAT", "PERMTH_INT", "PERMTH_EXM"]].isna().all()
    assert (alive["MORTSTAT"], alive["PERMTH_INT"], alive["PERMTH_EXM"]) == (0, 27, 26)
    assert pd.api.types.is_integer_dtype(mortality["SEQN"])


def test_cycle_label() -> None:
    assert cycle_label(1999) == "1999_2000"
    assert cycle_label(2017) == "2017_2018"
