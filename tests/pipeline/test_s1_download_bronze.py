"""Bronze manifest: the first download date survives while the file stays the same."""

# Imports
import os
from pathlib import Path

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
