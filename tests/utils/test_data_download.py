"""Tests: Utils - Download helpers.

- SHA-256 of a file read in blocks: same as hashing it whole
- HTML error page (sent by the CDC with status 200) or empty file not taken as data
- Download: an error page leaves no file behind; a failed attempt is retried and the good one saved whole
"""

# Imports
import hashlib
from pathlib import Path

import pytest
import requests

from bioage.utils import data_download
from bioage.utils.data_download import download, file_sha256, is_valid

XPT = b"HEADER RECORD*******" + b"x" * 200_000  # more than one chunk of the download
ERROR_PAGE = b"<!DOCTYPE html><html>Service unavailable</html>"


class FakeResponse:
    """Response of requests.get with a fixed content and status 200."""

    def __init__(self, content: bytes) -> None:
        self.content = content

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        pass

    def raise_for_status(self) -> None:
        pass

    def iter_content(self, chunk_size: int) -> list[bytes]:
        return [self.content[i : i + chunk_size] for i in range(0, len(self.content), chunk_size)]


def fake_server(monkeypatch: pytest.MonkeyPatch, answers: list) -> None:
    """requests.get gives each answer in turn (content, or an error to raise); no waits between retries."""
    answers = iter(answers)

    def get(url: str, **kwargs: object) -> FakeResponse:
        answer = next(answers)
        if isinstance(answer, Exception):
            raise answer
        return FakeResponse(answer)

    monkeypatch.setattr(data_download.requests, "get", get)
    monkeypatch.setattr(data_download.time, "sleep", lambda seconds: None)


def test_hash_matches_sha256_of_content(tmp_path: Path) -> None:
    path = tmp_path / "file.dat"
    content = b"x" * 3_000_000  # more than one block
    path.write_bytes(content)
    assert file_sha256(path) == hashlib.sha256(content).hexdigest()


def test_html_error_page_is_not_valid_data() -> None:
    assert not is_valid(Path("DEMO.xpt"), b"<!DOCTYPE html>")
    assert not is_valid(Path("NHANES_1999_2000_MORT_2019_PUBLIC.dat"), b"  <html>")
    assert not is_valid(Path("NHANES_1999_2000_MORT_2019_PUBLIC.dat"), b"")
    assert not is_valid(Path("DEMO.pdf"), b"<!DOCTYPE html>")
    assert is_valid(Path("DEMO.xpt"), b"HEADER RECORD*******")
    assert is_valid(Path("DEMO.pdf"), b"%PDF-1.7")


def test_error_page_leaves_no_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake_server(monkeypatch, [ERROR_PAGE] * data_download.RETRIES)
    dest = tmp_path / "DEMO.xpt"
    with pytest.raises(RuntimeError, match="unexpected file content"):
        download("https://cdc.gov/DEMO.xpt", dest)
    assert list(tmp_path.iterdir()) == []


def test_failed_attempt_retried_and_file_saved_whole(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake_server(monkeypatch, [requests.ConnectionError("connection reset"), XPT])
    dest = tmp_path / "DEMO.xpt"
    download("https://cdc.gov/DEMO.xpt", dest)
    assert dest.read_bytes() == XPT
    assert list(tmp_path.iterdir()) == [dest]
