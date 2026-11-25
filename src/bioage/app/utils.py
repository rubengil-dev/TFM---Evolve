"""Functions shared within the app."""

# Imports
from fastapi import Request

from bioage.app.schemas import AppError
from bioage.config.app import MAX_PDF_MB


async def body_in_memory(request: Request) -> bytes:
    """Body of a request, kept in memory (a file form is written to disk above 1 MB).

    Args:
        request: The request.

    Returns:
        Its body.

    Raises:
        AppError: If it is larger than the largest PDF accepted.
    """
    body = bytearray()
    async for chunk in request.stream():
        body += chunk
        if len(body) > MAX_PDF_MB * 1024**2:
            raise AppError("unreadable")
    return bytes(body)
