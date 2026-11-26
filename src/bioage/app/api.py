"""Web server of the app: receives the requests and hands them to the code that does the work.

Endpoints:
- POST /api/read?mode=quick|full: PDF → Reading
- POST /api/correct: list of OddValue → Correction (TODO)
- POST /api/calculate: Person → Result
- GET /api/health: the server is running

Errors:
- AppError: Give its code.
- DataError: Give the field that doesn't match the schema.

Logs: one line of JSON per request, with nothing of the user (see logs.py).

NOTE: Nothing is stored; between requests, the browser keeps the values.
"""

# Imports
import time
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from bioage.app.calculate import calculate, choose_level
from bioage.app.logs import note, setup_logs, write_line
from bioage.app.predict import load_bundle
from bioage.app.read_pdf import read_pdf
from bioage.app.schemas import AppError, Correction, Mode, OddValue, Person, Reading, Result
from bioage.app.utils import body_in_memory, extras_known, max_missing, routine_missing
from bioage.config.model_levels import LEVEL_COLUMNS


@asynccontextmanager
async def load_models(app: FastAPI) -> AsyncIterator[None]:
    """Load the models and set the logs once, when the server starts.

    Args:
        app: The web server.

    Yields:
        Nothing: the server runs meanwhile.
    """
    setup_logs()
    app.state.bundles = {level: load_bundle(level) for level in LEVEL_COLUMNS}
    yield


app = FastAPI(title="BioAge", lifespan=load_models)


@app.middleware("http")
async def log_requests(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Write one line per request of the API, also when the code fails; the health check is left out.

    Args:
        request: The request.
        call_next: What answers it.

    Returns:
        The answer.
    """
    if not request.url.path.startswith("/api/") or request.url.path == "/api/health":
        return await call_next(request)
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        note(request, error="crash")
        write_line(request, 500, started)
        raise
    write_line(request, response.status_code, started)
    return response


@app.post("/api/read")
async def post_read(request: Request, mode: Mode) -> Reading:
    """PDF (raw body) → what was read from it.

    Args:
        request: Request with the PDF as its body.
        mode: Mode the user chose.

    Returns:
        What was read.
    """
    note(request, mode=mode)
    most = max_missing(request.app.state.bundles, mode)
    reading = await run_in_threadpool(read_pdf, await body_in_memory(request), most)
    known = set(reading.lab_values) | {odd.variable for odd in reading.odd}
    note(request, missing=routine_missing(known), extras=extras_known(known))
    return reading


@app.post("/api/correct")
def post_correct(odd: list[OddValue]) -> Correction:
    """Values corrected by the user → in model units, or odd again if still impossible.

    TODO: With the parser, because it needs its table of units:
    1. Lab unit → model unit, with its factor
    2. Check the plausible range

    Args:
        odd: Odd values, with the text the user wrote.

    Returns:
        What was corrected and what is still odd.

    Raises:
        HTTPException: Always, until it is built.
    """
    raise HTTPException(status_code=501)


@app.post("/api/calculate")
def post_calculate(person: Person, request: Request) -> Result:
    """Data of a person → result.

    Args:
        person: Data of the person.
        request: The request, to reach the models.

    Returns:
        Result to show.
    """
    known = set(person.lab_values)
    level = choose_level(person, request.app.state.bundles)
    note(request, mode=person.mode, level=level, missing=routine_missing(known), extras=extras_known(known))
    return calculate(person, request.app.state.bundles)


@app.get("/api/health")
def get_health() -> dict[str, str]:
    """Tell that the server is running.

    Returns:
        Its status.
    """
    return {"status": "ok"}


@app.exception_handler(AppError)
def tell_error(request: Request, error: AppError) -> JSONResponse:
    """Error of the app → its code, for the front.

    Args:
        request: The request that failed.
        error: The error.

    Returns:
        Answer with the code.
    """
    note(request, error=error.code)
    return JSONResponse({"error": error.code}, status_code=422)


@app.exception_handler(RequestValidationError)
def tell_invalid_fields(request: Request, error: RequestValidationError) -> JSONResponse:
    """Data that does not match the schema → the fields at fault, without repeating their values.

    Args:
        request: The request that failed.
        error: The error.

    Returns:
        Answer with the fields.
    """
    note(request, error="invalid")
    fields = [{"field": list(detail["loc"]), "message": detail["msg"]} for detail in error.errors()]
    return JSONResponse({"invalid": fields}, status_code=422)
