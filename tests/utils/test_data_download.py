"""File hash and signature checks of the downloads."""

# Imports
import hashlib
from pathlib import Path

from bioage.utils.data_download import file_sha256, is_valid


def test_hash_matches_sha256_of_content(tmp_path: Path) -> None:
    path = tmp_path / "file.dat"
    content = b"x" * 3_000_000  # more than one block
    path.write_bytes(content)
    assert file_sha256(path) == hashlib.sha256(content).hexdigest()


def test_html_error_page_is_not_valid_data() -> None:
    assert not is_valid(Path("DEMO.xpt"), b"<!DOCTYPE html>")
    assert not is_valid(Path("NHANES_1999_2000_MORT_2019_PUBLIC.dat"), b"  <html>")
    assert is_valid(Path("DEMO.xpt"), b"HEADER RECORD*******")
