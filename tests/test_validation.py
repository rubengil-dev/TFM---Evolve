"""
Gold validation on a made-up Gold:
    - A valid Gold passes every check but size
    - Each check catches the error it is for
"""

# Imports
import pytest

from src.utils import validation


def test_valid_gold_passes_every_check_but_size(made_up_gold):
    """No error or warning on valid data; too few people for check_size."""
    checks = [
        validation.check_structure, validation.check_coverage, validation.check_required, validation.check_outcome,
        validation.check_population, validation.check_categories, validation.check_ranges, validation.check_consistency,
    ]
    assert {check.__name__: check(made_up_gold) for check in checks} == {check.__name__: [] for check in checks}
    assert validation.check_size(made_up_gold)


def test_failed_validation_stops_gold(made_up_gold, capsys):
    """Any error → ValueError, so Gold is not saved."""
    with pytest.raises(ValueError):
        validation.validate_gold(made_up_gold)


def test_structure_catches_missing_extra_and_wrong_type(made_up_gold):
    """Missing column, unexpected column and a number stored as text."""
    gold = made_up_gold.drop(columns="hdl").assign(extra=1, glucose=made_up_gold["glucose"].astype(str))
    assert sorted(validation.check_structure(gold)) == [
        "glucose: should be numeric", "missing column: hdl", "unexpected column: extra",
    ]


def test_categories_catch_unknown_answer(made_up_gold):
    """An answer outside CATEGORICAL_LEVELS."""
    made_up_gold.loc[0, "smoking"] = "sometimes"
    assert validation.check_categories(made_up_gold) == ["smoking: unknown answers ['sometimes']"]


def test_ranges_catch_impossible_value(made_up_gold):
    """A value outside PLAUSIBLE_RANGES limits."""
    made_up_gold.loc[0, "glucose"] = 900
    assert validation.check_ranges(made_up_gold) == ["glucose: 1 values outside 30-600"]


def test_required_catches_missing_value_and_repeated_person(made_up_gold):
    """Missing sex and a repeated seqn."""
    made_up_gold.loc[0, "sex"] = None
    made_up_gold.loc[1, "seqn"] = made_up_gold.loc[2, "seqn"]
    assert validation.check_required(made_up_gold) == ["sex: 1 missing", "seqn: 1 repeated"]


def test_outcome_and_population_catch_impossible_values(made_up_gold):
    """death other than 0 / 1, follow-up of 0 and age above AGE_MAX."""
    made_up_gold.loc[0, "death"] = 2
    made_up_gold.loc[1, "follow_up_months"] = 0
    made_up_gold.loc[2, "age"] = 85
    assert validation.check_outcome(made_up_gold) == ["death: values other than 0 / 1", "follow_up_months: 1 values outside 0.1-252"]
    assert validation.check_population(made_up_gold) == ["age: 1 values outside 18-79"]


def test_consistency_warns_of_pairs_out_of_order(made_up_gold):
    """HDL not below total cholesterol → warning, not error."""
    made_up_gold.loc[0, ["hdl", "total_cholesterol"]] = [150, 140]
    assert validation.check_consistency(made_up_gold) == ["hdl not below total_cholesterol: 1 persons"]
