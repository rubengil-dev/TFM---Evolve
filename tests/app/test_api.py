"""Tests: App - Web server, with the saved models.

- /api/read: needs the mode, which decides how many values can be missing; a PDF gives the fields the front expects
- /api/read: not a PDF, an empty file or one too large → unreadable
- /api/correct: only its contract, until it is built
- /api/calculate: same age as the model called directly, with the level of each mode; the answers change it
- One person does not affect the next; every level is loaded
- Result: every group of the front, habits only in the full mode
- Too young or too old, impossible values or BMI → its code; data from the browser that cannot be right → refused
- Nothing of the user in the errors, not even when the code fails
- Contract: habits and their categories are the ones of the model
"""

# Imports
import json
from collections.abc import Iterator
from typing import get_args

import pytest
from fastapi.testclient import TestClient

from bioage.app import api, read_pdf
from bioage.app.api import app
from bioage.app.calculate import model_row
from bioage.app.predict import load_bundle, predict_age
from bioage.app.read_pdf import EXAMPLE_READING
from bioage.app.schemas import Habits, Person
from bioage.config.app import BLOOD_GROUPS, HABIT_GROUPS, MAX_AGE, MAX_PDF_MB, MIN_AGE
from bioage.config.model_levels import LEVEL_COLUMNS, QUESTIONNAIRE, LabVariable

PDF = b"%PDF-1.7\nmade up"
ODD = {"variable": "potassium", "text": "4,5", "unit": "mmol/L", "factor": 1}
HABITS = {"smoking": "former", "physical_activity": "moderate", "sedentary_hours": 7, "sleep_hours": 7}
PERSON = {"lab_values": EXAMPLE_READING.lab_values, "age": 45, "sex": "male", "weight": 80, "height": 175}


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    with TestClient(app) as running:
        yield running


def bio_age(client: TestClient, **changes: object) -> float:
    answer = client.post("/api/calculate", json={**PERSON, **changes})
    assert answer.status_code == 200, answer.text
    return answer.json()["bio_age"]


def test_health_answers(client: TestClient) -> None:
    assert client.get("/api/health").json() == {"status": "ok"}


def test_read_gives_the_fields_of_the_front(client: TestClient) -> None:
    answer = client.post("/api/read?mode=full", content=PDF)
    assert answer.status_code == 200
    assert set(answer.json()) == {"lab_values", "age", "sex", "odd"}


@pytest.mark.parametrize("path", ["/api/read", "/api/read?mode=slow"])
def test_read_needs_a_known_mode(client: TestClient, path: str) -> None:
    answer = client.post(path, content=PDF)
    assert answer.status_code == 422 and answer.json()["invalid"]


def test_read_uses_the_mode(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    kept = dict(list(EXAMPLE_READING.lab_values.items())[6:])
    monkeypatch.setattr(read_pdf, "EXAMPLE_READING", EXAMPLE_READING.model_copy(update={"lab_values": kept}))
    assert client.post("/api/read?mode=quick", content=PDF).json() == {"error": "too_few"}
    assert client.post("/api/read?mode=full", content=PDF).status_code == 200


@pytest.mark.parametrize(
    "body", [b"", b"plain text", b"%PDF-" + b"0" * MAX_PDF_MB * 1024**2], ids=["empty", "text", "large"]
)
def test_read_refuses_what_is_not_a_pdf(client: TestClient, body: bytes) -> None:
    answer = client.post("/api/read?mode=full", content=body)
    assert (answer.status_code, answer.json()) == (422, {"error": "unreadable"})


def test_correct_is_not_built_yet(client: TestClient) -> None:
    assert client.post("/api/correct", json=[ODD]).status_code == 501


@pytest.mark.parametrize("change", [{"variable": "glucosa"}, {"text": None}, {"unknown": 1}])
def test_correct_refuses_what_is_not_an_odd_value(client: TestClient, change: dict) -> None:
    answer = client.post("/api/correct", json=[{**ODD, **change}])
    assert answer.status_code == 422 and answer.json()["invalid"]


@pytest.mark.parametrize(("habits", "level"), [(None, "routine"), (HABITS, "questionnaire")])
def test_calculate_matches_the_model_of_each_mode(client: TestClient, habits: dict | None, level: str) -> None:
    person = Person(**PERSON, habits=habits)
    expected = predict_age(load_bundle(level), model_row(person, LEVEL_COLUMNS[level]))[0]
    assert bio_age(client, habits=habits) == pytest.approx(expected, abs=0.05)


def test_result_has_habits_only_in_the_full_mode(client: TestClient) -> None:
    assert client.post("/api/calculate", json=PERSON).json()["habits"] is None
    assert client.post("/api/calculate", json={**PERSON, "habits": HABITS}).json()["habits"] is not None


def test_answers_change_the_age(client: TestClient) -> None:
    assert bio_age(client, weight=130) > bio_age(client)
    assert bio_age(client, habits={**HABITS, "smoking": "current"}) > bio_age(client, habits=HABITS)


def test_values_change_the_age(client: TestClient) -> None:
    assert bio_age(client, lab_values={**EXAMPLE_READING.lab_values, "glucose": 250}) > bio_age(client)


def test_missing_values_still_give_an_age(client: TestClient) -> None:
    some = dict(list(EXAMPLE_READING.lab_values.items())[5:])
    assert 18 < bio_age(client, lab_values=some) < 79


def test_one_person_does_not_affect_the_next(client: TestClient) -> None:
    before = bio_age(client)
    bio_age(client, age=80, sex="female", lab_values={**EXAMPLE_READING.lab_values, "glucose": 250}, habits=HABITS)
    assert bio_age(client) == before


def test_every_level_is_loaded(client: TestClient) -> None:
    assert set(app.state.bundles) == set(LEVEL_COLUMNS)


@pytest.mark.parametrize(("age", "code"), [(MIN_AGE - 1, "too_young"), (MAX_AGE + 1, "too_old")])
def test_age_out_of_limits_gives_its_code(client: TestClient, age: int, code: str) -> None:
    answer = client.post("/api/calculate", json={**PERSON, "age": age})
    assert (answer.status_code, answer.json()) == (422, {"error": code})


@pytest.mark.parametrize(
    ("changes", "code"),
    [
        ({"lab_values": {"potassium": 9.8}}, "impossible"),
        ({"weight": 300, "height": 120}, "impossible_bmi"),
    ],
)
def test_impossible_data_give_their_code(client: TestClient, changes: dict, code: str) -> None:
    answer = client.post("/api/calculate", json={**PERSON, **changes})
    assert (answer.status_code, answer.json()) == (422, {"error": code})


def test_result_has_every_group(client: TestClient) -> None:
    result = client.post("/api/calculate", json={**PERSON, "habits": HABITS}).json()
    assert list(result["blood"]) == list(BLOOD_GROUPS)
    assert list(result["habits"]) == list(HABIT_GROUPS)
    assert all(isinstance(years, float) for years in result["habits"].values())


@pytest.mark.parametrize("age", [MIN_AGE, MAX_AGE])
def test_age_limits_are_accepted(client: TestClient, age: int) -> None:
    assert client.post("/api/calculate", json={**PERSON, "age": age}).status_code == 200


@pytest.mark.parametrize(("age", "code"), [(MIN_AGE - 1, "too_young"), (MAX_AGE + 1, "too_old")])
def test_age_of_the_pdf_is_checked(client: TestClient, monkeypatch: pytest.MonkeyPatch, age: int, code: str) -> None:
    monkeypatch.setattr(read_pdf, "EXAMPLE_READING", EXAMPLE_READING.model_copy(update={"age": age}))
    assert client.post("/api/read?mode=full", content=PDF).json() == {"error": code}


@pytest.mark.parametrize(
    "changes",
    [
        {"sex": "other"},
        {"age": 45.5},
        {"weight": 5},
        {"height": 400},
        {"lab_values": {"glucosa": 98}},
        {"lab_values": {"glucose": "high"}},
        {"lab_values": {"age": 20}},
        {"habits": {**HABITS, "smoking": "sometimes"}},
        {"habits": {"smoking": "never"}},
        {"unknown": 1},
    ],
)
def test_impossible_data_from_the_browser_is_refused(client: TestClient, changes: dict) -> None:
    answer = client.post("/api/calculate", json={**PERSON, **changes})
    assert answer.status_code == 422 and answer.json()["invalid"]


def test_refused_values_are_not_repeated(client: TestClient) -> None:
    answer = client.post("/api/calculate", json={**PERSON, "lab_values": {"glucose": "my secret"}})
    assert "glucose" in answer.text and "my secret" not in answer.text


def test_broken_json_is_refused(client: TestClient) -> None:
    answer = client.post("/api/calculate", content='{"secret": ', headers={"Content-Type": "application/json"})
    assert answer.status_code == 422 and "secret" not in answer.text


def test_code_failure_tells_nothing_of_the_user(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(*_: object) -> None:
        raise ValueError("my secret")

    monkeypatch.setattr(api, "calculate", fail)
    answer = TestClient(app, raise_server_exceptions=False).post("/api/calculate", json=PERSON)
    assert answer.status_code == 500 and "my secret" not in answer.text


@pytest.mark.parametrize("number", [float("nan"), float("inf")])
def test_numbers_that_are_not_finite_are_refused(client: TestClient, number: float) -> None:
    body = json.dumps({**PERSON, "lab_values": {"glucose": number}})
    answer = client.post("/api/calculate", content=body, headers={"Content-Type": "application/json"})
    assert answer.status_code == 422 and "finite" in answer.text


def test_contract_covers_every_model_variable() -> None:
    assert set(Habits.model_fields) == set(QUESTIONNAIRE)
    assert {"age", "sex", "bmi", *get_args(LabVariable), *Habits.model_fields} == set(LEVEL_COLUMNS["full"])
