"""Tests: App - Functions shared within the app.

- Body of a request: the pieces joined in order, up to the largest size; one byte more → refused
"""

# Imports
import asyncio

import pytest
from fastapi import Request

from bioage.app.schemas import AppError
from bioage.app.utils import body_in_memory
from bioage.config.app import MAX_PDF_MB

LARGEST = MAX_PDF_MB * 1024**2


def made_up_request(pieces: list[bytes]) -> Request:
    messages = [{"type": "http.request", "body": piece, "more_body": True} for piece in pieces]
    messages.append({"type": "http.request", "body": b"", "more_body": False})

    async def receive() -> dict:
        return messages.pop(0)

    return Request({"type": "http"}, receive)


def test_pieces_are_joined_in_order() -> None:
    pieces = [b"%PDF-", b"a" * 70_000, b"end"]
    assert asyncio.run(body_in_memory(made_up_request(pieces))) == b"".join(pieces)


def test_largest_size_is_accepted() -> None:
    assert len(asyncio.run(body_in_memory(made_up_request([b"0" * LARGEST])))) == LARGEST


def test_one_byte_more_is_refused() -> None:
    with pytest.raises(AppError, match="unreadable"):
        asyncio.run(body_in_memory(made_up_request([b"0" * LARGEST, b"0"])))
