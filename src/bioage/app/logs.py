"""One line of JSON per request of the app, with nothing of the user.

- `setup_logs`    : Logger of the requests in JSON; uvicorn stops writing the IP and the message of a crash.
- `note`          : Add fields to the line of a request, from the code that handles it.
- `write_line`    : Write the line of a finished request.
- `crash_place`   : Kind of error and file:line of a crash, without its message.
- `JsonFormatter` : A log record → one line of JSON.
- `NoMessage`     : A crash written by uvicorn → only its kind and place.

NOTE: Only what helps to see why the app fails: endpoint, mode, level, model, result, error code, where it
crashed, how many Routine values are missing, how many Extras there are and time. Never values, age, sex,
weight, height, biological age, margin, variable names, IP or the message of an error (it can carry values).
"""

# Imports
import json
import logging
import sys
import time
import traceback
from pathlib import Path

from fastapi import Request

logger = logging.getLogger("bioage.requests")


def setup_logs() -> None:
    """Requests → JSON on the standard output, where the hosting shows it; uvicorn writes no IP nor messages."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logging.getLogger("uvicorn.access").disabled = True
    uvicorn_errors = logging.getLogger("uvicorn.error")
    if not any(isinstance(kept, NoMessage) for kept in uvicorn_errors.filters):
        uvicorn_errors.addFilter(NoMessage())


def note(request: Request, **fields: object) -> None:
    """Add fields to the line of a request.

    Args:
        request: The request.
        **fields: Name → value.
    """
    request.state.log = {**getattr(request.state, "log", {}), **fields}


def write_line(request: Request, status_code: int, started: float) -> None:
    """Write the line of a finished request.

    Args:
        request: The request.
        status_code: HTTP status of the answer.
        started: When it began (time.perf_counter).
    """
    fields = {
        "endpoint": request.url.path.removeprefix("/api/"),
        "status": "ok" if status_code < 400 else "error",
        "error": None,
        **getattr(request.state, "log", {}),
        "ms": round((time.perf_counter() - started) * 1000),
    }
    logger.info("request", extra={"fields": fields})


def crash_place(error: BaseException) -> str:
    """Kind of error and where it happened, without its message.

    Args:
        error: The error.

    Returns:
        E.g. "ValueError at calculate.py:42".
    """
    frames = traceback.extract_tb(error.__traceback__)
    place = f" at {Path(frames[-1].filename).name}:{frames[-1].lineno}" if frames else ""
    return type(error).__name__ + place


class JsonFormatter(logging.Formatter):
    """A log record → one line of JSON, with its time and its fields."""

    def format(self, record: logging.LogRecord) -> str:
        """Turn a record into one line of JSON.

        Args:
            record: The record, with its fields in `fields`.

        Returns:
            The line.
        """
        return json.dumps({"time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"), **getattr(record, "fields", {})})


class NoMessage(logging.Filter):
    """A crash that uvicorn writes → only its kind and place: its message and traceback can carry values."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Strip the details of a crash during a request; other records pass as they are.

        Args:
            record: A record of uvicorn.

        Returns:
            Always True: the record is kept.
        """
        is_crash = str(record.msg).startswith("Exception in ASGI application")  # not, e.g., failing to start
        if is_crash and record.exc_info and record.exc_info[1] is not None:
            record.msg = "Exception in ASGI application: " + crash_place(record.exc_info[1])
            record.args = ()
            record.exc_info = None
            record.exc_text = None
        return True
