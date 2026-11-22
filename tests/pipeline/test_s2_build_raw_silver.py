"""Tests: Pipeline - Step 2, Silver raw.

- Joining a file: every DEMO person kept and nobody added; equal columns merged (numbers with rounding,
  text exactly), different ones kept apart
- More than one row per person in a file → error
- Population: ages 18 to 79 both included, only people eligible for mortality follow-up
- Alias renames: old name → common name; a rename onto an existing column → error
"""

# Imports
import pandas as pd
import pytest

from bioage.pipeline.s2_build_raw_silver import filter_population, merge_table, rename_aliases


def test_join_keeps_demo_people_and_merges_equal_columns() -> None:
    demo = pd.DataFrame({"SEQN": [1, 2, 3], "RIDAGEYR": [30, 40, 50], "WTMEC2YR": [100.0, None, 300.0]})
    lab = pd.DataFrame({"SEQN": [2, 3, 4], "WTMEC2YR": [200.0, 300.00001, 400.0], "LBXGLU": [90, 95, 99]})
    merged = merge_table(demo, lab, "GLU")
    assert merged["SEQN"].tolist() == [1, 2, 3]
    assert merged["WTMEC2YR"].tolist() == [100.0, 200.0, 300.0]
    assert merged["LBXGLU"].iloc[1:].tolist() == [90, 95] and pd.isna(merged["LBXGLU"].iloc[0])


def test_join_keeps_different_columns_apart() -> None:
    demo = pd.DataFrame({"SEQN": [1, 2], "LBXSCR": [0.8, 1.0]})
    lab = pd.DataFrame({"SEQN": [1, 2], "LBXSCR": [0.9, 1.2]})
    merged = merge_table(demo, lab, "BIOPRO")
    assert merged["LBXSCR"].tolist() == [0.8, 1.0]
    assert merged["LBXSCR_BIOPRO"].tolist() == [0.9, 1.2]


def test_join_compares_text_columns_exactly() -> None:
    demo = pd.DataFrame({"SEQN": [1, 2], "SDDSRVYR": ["A", "B"], "RIAGENDR": ["1", "2"]})
    other = pd.DataFrame({"SEQN": [1, 2], "SDDSRVYR": ["A", "B"], "RIAGENDR": ["1", "1"]})
    merged = merge_table(demo, other, "OTHER")
    assert "SDDSRVYR_OTHER" not in merged.columns
    assert merged["RIAGENDR_OTHER"].tolist() == ["1", "1"]


def test_join_rejects_repeated_person() -> None:
    with pytest.raises(ValueError, match="more than one row per SEQN"):
        merge_table(pd.DataFrame({"SEQN": [1]}), pd.DataFrame({"SEQN": [1, 1], "LBXGLU": [90, 91]}), "GLU")


def test_population_ages_included_and_only_eligible() -> None:
    table = pd.DataFrame({"RIDAGEYR": [17, 18, 79, 80, 50], "ELIGSTAT": [1, 1, 1, 1, 2]})
    assert filter_population(table)["RIDAGEYR"].tolist() == [18, 79]


def test_alias_renamed_and_collision_rejected() -> None:
    assert "LBDHDD" in rename_aliases(pd.DataFrame({"LBDHDL": [50]})).columns
    with pytest.raises(ValueError, match="Rename collision"):
        rename_aliases(pd.DataFrame({"LBDHDL": [50], "LBDHDD": [50]}))
