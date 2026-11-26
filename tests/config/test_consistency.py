"""Tests: Config - Consistency between config files, without data.

- Every Gold predictor used by a model or discarded with its reason; nothing discarded outside Gold
- Model variables with what the app needs to check them
- Plausible ranges in order (low below high, normal inside the limits) and only for Gold variables
- Log and squared terms only for model variables
- One algorithm and one saved model per level
- Result groups: every model variable but age and sex in one, habits = questionnaire
"""

# Imports
from bioage.config.app import BLOOD_GROUPS, HABIT_GROUPS, OTHER
from bioage.config.gold_columns import DERIVED_FEATURES, ID_COLUMNS, OUTCOME_COLUMNS, SELECTED_PREDICTORS
from bioage.config.model_levels import DISCARDED, LEVEL_COLUMNS, LEVEL_MODELS, QUESTIONNAIRE
from bioage.config.paths import TRAINED_MODELS
from bioage.config.plausible_ranges import PLAUSIBLE_RANGES
from bioage.config.study import CATEGORICAL_LEVELS, LOG_VARIABLES, SQUARED_VARIABLES

GOLD_PREDICTORS = SELECTED_PREDICTORS + DERIVED_FEATURES
MODEL_VARIABLES = set().union(*LEVEL_COLUMNS.values())


def test_model_variables_in_gold() -> None:
    assert MODEL_VARIABLES - set(GOLD_PREDICTORS) == set()


def test_every_gold_predictor_used_or_discarded() -> None:
    assert set(GOLD_PREDICTORS) - MODEL_VARIABLES - set(DISCARDED) == set()


def test_no_variable_used_and_discarded() -> None:
    assert MODEL_VARIABLES & set(DISCARDED) == set()


def test_discarded_variables_in_gold() -> None:
    assert set(DISCARDED) - set(GOLD_PREDICTORS) == set()


def test_numeric_model_variables_have_plausible_range() -> None:
    numeric = MODEL_VARIABLES - set(CATEGORICAL_LEVELS) - {"age"}
    assert numeric - set(PLAUSIBLE_RANGES) == set()


def test_plausible_ranges_in_order() -> None:
    for variable, (_, normal, limits, _) in PLAUSIBLE_RANGES.items():
        low, high = limits
        assert low < high, variable
        if normal is not None:
            assert low <= normal[0] <= normal[1] <= high, variable


def test_plausible_ranges_only_for_gold_columns() -> None:
    assert set(PLAUSIBLE_RANGES) - set(ID_COLUMNS + OUTCOME_COLUMNS + GOLD_PREDICTORS) == set()


def test_log_and_squared_only_for_model_variables() -> None:
    assert set(LOG_VARIABLES + SQUARED_VARIABLES) - MODEL_VARIABLES == set()


def test_every_level_has_algorithm_and_saved_model() -> None:
    assert set(LEVEL_COLUMNS) == set(LEVEL_MODELS)
    assert all((TRAINED_MODELS / f"{level}.joblib").exists() for level in LEVEL_COLUMNS)


def test_every_variable_is_in_one_group() -> None:
    grouped = [column for members in [*BLOOD_GROUPS.values(), *HABIT_GROUPS.values()] for column in members]
    assert sorted(grouped) == sorted(set(LEVEL_COLUMNS["full"]) - {"age", "sex"})


def test_habit_groups_are_the_questionnaire() -> None:
    assert [column for members in HABIT_GROUPS.values() for column in members] == QUESTIONNAIRE


def test_other_is_a_blood_group() -> None:
    assert OTHER in BLOOD_GROUPS
