"""Tests: Pipeline - Step 1, Bronze manifest.

- Same file (same SHA-256) → keeps its first download date, even after a copy
- Older manifest without SHA-256 → keeps its date
- New or changed file → its modification date; a changed one also warns
- A failed download stops the step
"""

# Imports
import logging
import os
from pathlib import Path

import pytest

from bioage.pipeline import s1_download_bronze
from bioage.pipeline.s1_download_bronze import download_date

OLD_DATE = "2026-10-17 16:42"


def make_file(tmp_path: Path) -> Path:
    path = tmp_path / "DEMO.xpt"
    path.write_bytes(b"HEADER RECORD")
    os.utime(path, (1_800_000_000, 1_800_000_000))  # a later modification, as after a copy
    return path


def test_same_file_keeps_first_download_date(tmp_path: Path) -> None:
    path = make_file(tmp_path)
    assert download_date({"sha256": "abc", "downloaded_at": OLD_DATE}, "abc", path) == OLD_DATE


def test_changed_file_gets_its_modification_date(tmp_path: Path) -> None:
    path = make_file(tmp_path)
    assert download_date({"sha256": "abc", "downloaded_at": OLD_DATE}, "xyz", path) != OLD_DATE


def test_older_manifest_without_hash_keeps_its_date(tmp_path: Path) -> None:
    path = make_file(tmp_path)
    assert download_date({"downloaded_at": OLD_DATE}, "abc", path) == OLD_DATE


def test_new_file_gets_its_modification_date(tmp_path: Path) -> None:
    path = make_file(tmp_path)
    assert download_date(None, "abc", path) != OLD_DATE


def test_changed_file_warns(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    path = make_file(tmp_path)
    with caplog.at_level(logging.WARNING):
        download_date({"sha256": "abc", "downloaded_at": OLD_DATE}, "xyz", path)
    assert "DEMO.xpt changed" in caplog.text


def test_same_file_does_not_warn(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    path = make_file(tmp_path)
    with caplog.at_level(logging.WARNING):
        download_date({"sha256": "abc", "downloaded_at": OLD_DATE}, "abc", path)
    assert caplog.text == ""


def test_failed_download_stops_bronze(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    job = {"dataset": "DEMO", "cycle": "1999_2000", "url": "https://cdc.gov/DEMO.xpt", "dest": tmp_path / "DEMO.xpt"}
    monkeypatch.setattr(s1_download_bronze, "BRONZE", tmp_path)
    monkeypatch.setattr(s1_download_bronze, "build_jobs", lambda: [job])
    monkeypatch.setattr(s1_download_bronze, "download_all", lambda jobs: jobs)
    monkeypatch.setattr(s1_download_bronze, "write_manifest", lambda jobs: None)
    monkeypatch.setattr(s1_download_bronze, "print_summary", lambda jobs, failed: None)
    with pytest.raises(RuntimeError, match="1 files not downloaded"):
        s1_download_bronze.run()
