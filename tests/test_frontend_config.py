"""Tests: What the front repeats from the backend.

- Every number of frontend/src/config/limits.ts is the one of the config
- The front has a screen for every error code, and only one code of its own
- What travels has the same fields on both sides, and the front calls endpoints that exist
- The same groups in the result, in the same order
- The same modes on both sides
- A name for every lab variable; a question, with its categories, for every answer
"""

# Imports
import json
import re
from typing import get_args

import pytest
from pydantic import BaseModel

from bioage.app.api import app
from bioage.app.schemas import Habits, Mode, OddValue, Person, Reading, Result
from bioage.config.app import BLOOD_GROUPS, HABIT_GROUPS, MAX_AGE, MIN_AGE, ErrorCode
from bioage.config.model_levels import LabVariable
from bioage.config.paths import ROOT
from bioage.config.plausible_ranges import PLAUSIBLE_RANGES
from bioage.config.study import AGE_MAX, AGE_MIN, CATEGORICAL_LEVELS

FRONT = ROOT / "frontend" / "src"
RANGES = ["weight", "height", "bmi", "sedentary_hours", "sleep_hours"]


def front_text(name: str) -> str:
    return (FRONT / name).read_text(encoding="utf-8")


def test_front_limits_match_the_config() -> None:
    text = front_text("config/limits.ts")
    written = re.findall(r"^export const (\w+) = (.+)$", text, flags=re.MULTILINE)
    assert {name: json.loads(value) for name, value in written} == {
        "MIN_AGE": MIN_AGE,
        "MAX_AGE": MAX_AGE,
        "DATA_MIN_AGE": AGE_MIN,
        "DATA_MAX_AGE": AGE_MAX,
        **{name.upper(): list(PLAUSIBLE_RANGES[name][2]) for name in RANGES},
    }


def test_front_error_codes_match_the_config() -> None:
    text = front_text("config/errors.ts")
    line = re.search(r"^export type ErrorKind = (.+)$", text, flags=re.MULTILINE)
    assert line is not None
    assert set(re.findall(r"'(\w+)'", line[1])) == {*get_args(ErrorCode), "unavailable", "failed"}


@pytest.mark.parametrize("schema", [Reading, OddValue, Person, Result])
def test_front_types_have_the_fields_of_the_schemas(schema: type[BaseModel]) -> None:
    body = re.search(
        rf"^export type {schema.__name__} = \{{\n(.+?)^\}}", front_text("types.ts"), re.MULTILINE | re.DOTALL
    )
    assert body is not None
    assert set(re.findall(r"^  (\w+)\??:", body[1], flags=re.MULTILINE)) == set(schema.model_fields)


def test_front_sends_every_habit() -> None:
    sent = re.search(r"'full' \? \{ (.+?) \}", front_text("utils/person.ts"))
    assert sent is not None
    assert set(sent[1].split(", ")) == set(Habits.model_fields)


def test_front_calls_endpoints_that_exist() -> None:
    called = set(re.findall(r"['`](/api/\w+)", front_text("utils/api.ts")))
    assert called and called <= set(app.openapi()["paths"])


def test_front_names_every_lab_variable() -> None:
    names = re.findall(r"^  (\w+):", front_text("config/variables.ts"), flags=re.MULTILINE)
    assert set(names) == set(get_args(LabVariable))


def test_front_asks_every_answer_with_its_categories() -> None:
    questions = {}
    for question in front_text("config/questions.ts").split("    id: '")[1:]:
        questions[question.split("'")[0]] = set(re.findall(r"value: '(\w+)'", question))
    assert set(questions) == (set(Person.model_fields) | set(Habits.model_fields)) - {"lab_values", "habits"}
    for name, values in questions.items():
        assert values == set(CATEGORICAL_LEVELS.get(name, []))


def test_front_has_the_groups_of_the_result() -> None:
    blood, habits = (
        front_text("config/groups.ts").split("export const BLOOD_GROUPS")[1].split("export const HABIT_GROUPS")
    )
    assert re.findall(r"id: '(\w+)'", blood) == list(BLOOD_GROUPS)
    assert re.findall(r"id: '(\w+)'", habits) == list(HABIT_GROUPS)


def test_front_has_the_modes_of_the_backend() -> None:
    line = re.search(r"^export type Mode = (.+)$", front_text("types.ts"), flags=re.MULTILINE)
    assert line is not None
    assert set(re.findall(r"'(\w+)'", line[1])) == set(get_args(Mode))
