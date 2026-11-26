"""Tests: App - One line of JSON per request, with nothing of the user.

- Calculate: mode, level, values missing and Extras, ok
- Read: the error code when it fails, the counts when it works
- Data that do not match the schema → error "invalid"; the code fails → "crash"
- Only these fields, and none of the values sent
- The health check is not written; uvicorn stops writing the IP
"""

# Imports
import json
import logging
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from bioage.app import api, read_pdf
from bioage.app.api import app
from bioage.app.logs import JsonFormatter, logger
from bioage.app.read_pdf import EXAMPLE_READING

PDF = b"%PDF-1.7\nmade up"
PERSON = {"lab_values": EXAMPLE_READING.lab_values, "age": 45, "sex": "male", "weight": 80, "height": 175}
FIELDS = {"time", "endpoint", "status", "error", "mode", "level", "missing", "extras", "ms"}


class Lines(logging.Handler):
    """Keeps the lines written, already formatted."""

    def __init__(self) -> None:
        super().__init__()
        self.setFormatter(JsonFormatter())
        self.lines: list[dict] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.lines.append(json.loads(self.format(record)))


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    with TestClient(app, raise_server_exceptions=False) as running:
        yield running


@pytest.fixture
def lines(client: TestClient) -> Iterator[list[dict]]:
    handler = Lines()
    logger.addHandler(handler)
    yield handler.lines
    logger.removeHandler(handler)


def test_calculate_writes_mode_level_and_counts(client: TestClient, lines: list[dict]) -> None:
    lab = {**dict(list(EXAMPLE_READING.lab_values.items())[2:]), "ggt": 30}
    client.post("/api/calculate", json={**PERSON, "lab_values": lab})
    [line] = lines
    assert line["endpoint"] == "calculate" and line["status"] == "ok" and line["error"] is None
    assert (line["mode"], line["level"], line["missing"], line["extras"]) == ("quick", "routine", 2, 1)
    assert isinstance(line["ms"], int)


def test_read_writes_the_error_or_the_counts(client: TestClient, lines: list[dict]) -> None:
    client.post("/api/read?mode=full", content=b"not a pdf")
    client.post("/api/read?mode=full", content=PDF)
    assert (lines[0]["status"], lines[0]["error"], lines[0]["mode"]) == ("error", "unreadable", "full")
    assert (lines[1]["status"], lines[1]["missing"], lines[1]["extras"]) == ("ok", 0, 0)


def test_too_few_values_are_written(client: TestClient, lines: list[dict], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(read_pdf, "EXAMPLE_READING", EXAMPLE_READING.model_copy(update={"lab_values": {}}))
    client.post("/api/read?mode=quick", content=PDF)
    assert lines[0]["error"] == "too_few"


def test_wrong_data_and_failures_are_written(
    client: TestClient, lines: list[dict], monkeypatch: pytest.MonkeyPatch
) -> None:
    client.post("/api/calculate", json={**PERSON, "weight": "heavy"})

    def fail(*_: object) -> None:
        raise RuntimeError

    monkeypatch.setattr(api, "calculate", fail)
    client.post("/api/calculate", json=PERSON)
    assert [line["error"] for line in lines] == ["invalid", "crash"]


def test_only_known_fields_and_nothing_sent(client: TestClient, lines: list[dict]) -> None:
    client.post("/api/calculate", json={**PERSON, "weight": 83.7, "height": 171.3})
    client.post("/api/read?mode=full", content=PDF)
    for line in lines:
        assert set(line) <= FIELDS
        assert not {"83.7", "171.3", "male", "glucose"} & set(json.dumps(line).replace('"', " ").split())


def test_health_is_not_written_and_uvicorn_keeps_no_ips(client: TestClient, lines: list[dict]) -> None:
    client.get("/api/health")
    assert lines == []
    assert logging.getLogger("uvicorn.access").disabled
