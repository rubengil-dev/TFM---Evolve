"""One line of JSON per request of the app, with nothing of the user.

- `setup_logs`    : Logger of the requests in JSON, and the access log of uvicorn off (it writes the IP).
- `note`          : Add fields to the line of a request, from the code that handles it.
- `write_line`    : Write the line of a finished request.
- `JsonFormatter` : A log record → one line of JSON.

NOTE: Only what helps to see why the app fails: endpoint, mode, level, result, error code, how many
Routine values are missing, how many Extras there are and time. Never values, age, sex, weight, height,
biological age, margin, variable names or IP.
"""

# Imports
import json
import logging
import sys
import time

from fastapi import Request

logger = logging.getLogger("bioage.requests")


def setup_logs() -> None:
    """Requests → JSON on the standard output, where the hosting shows it; uvicorn stops writing its own."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logging.getLogger("uvicorn.access").disabled = True


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
