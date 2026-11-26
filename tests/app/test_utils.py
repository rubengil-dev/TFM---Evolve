"""Tests: App - Functions shared within the app.

- BMI from kilos and centimetres
- Routine values missing and Extras known, ignoring the rest
- Most missing in a mode: from the bundle of its level
- Body of a request: the pieces joined in order, up to the largest size; one byte more → refused
"""

# Imports
import asyncio

import pytest
from fastapi import Request

from bioage.app.schemas import AppError
from bioage.app.utils import bmi, body_in_memory, extras_known, max_missing, routine_missing
from bioage.config.app import MAX_PDF_MB

LARGEST = MAX_PDF_MB * 1024**2


def made_up_request(pieces: list[bytes]) -> Request:
    messages = [{"type": "http.request", "body": piece, "more_body": True} for piece in pieces]
    messages.append({"type": "http.request", "body": b"", "more_body": False})

    async def receive() -> dict:
        return messages.pop(0)

    return Request({"type": "http"}, receive)


def test_bmi_from_kilos_and_centimetres() -> None:
    assert bmi(80, 175) == pytest.approx(26.12, abs=0.01)


def test_pieces_are_joined_in_order() -> None:
    pieces = [b"%PDF-", b"a" * 70_000, b"end"]
    assert asyncio.run(body_in_memory(made_up_request(pieces))) == b"".join(pieces)


def test_largest_size_is_accepted() -> None:
    assert len(asyncio.run(body_in_memory(made_up_request([b"0" * LARGEST])))) == LARGEST


def test_one_byte_more_is_refused() -> None:
    with pytest.raises(AppError, match="unreadable"):
        asyncio.run(body_in_memory(made_up_request([b"0" * LARGEST, b"0"])))


def test_routine_missing_and_extras_known() -> None:
    assert routine_missing(set()) == 15
    assert routine_missing({"glucose", "hdl", "ggt", "bmi"}) == 13
    assert extras_known({"glucose", "ggt", "vitamin_d"}) == 2


def test_max_missing_comes_from_the_level_of_the_mode() -> None:
    bundles = {
        "routine": {"margin": {"routine_missing": [0, 1, 2]}},
        "questionnaire": {"margin": {"routine_missing": [0]}},
    }
    assert max_missing(bundles, "quick") == 2
    assert max_missing(bundles, "full") == 0
