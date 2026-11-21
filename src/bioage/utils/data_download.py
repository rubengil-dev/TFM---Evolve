"""Helpers to download files.

- Retries
- No half-written files
- No error pages saved as data
- SHA-256 of a file on disk
"""

# Imports
import hashlib
import logging
import time
from pathlib import Path

import requests

from bioage.config.sources import RETRIES, TIMEOUT

logger = logging.getLogger(__name__)


def download(url: str, dest: Path) -> None:
    """Download to a .part file and rename it only when complete, retrying with a growing wait.

    Args:
        url: Address of the file.
        dest: Path where the complete file is saved.

    Raises:
        RuntimeError: If the last retry also fails.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")

    for attempt in range(1, RETRIES + 1):
        try:
            with requests.get(url, stream=True, timeout=TIMEOUT) as response:
                response.raise_for_status()
                with tmp.open("wb") as f:
                    for chunk in response.iter_content(chunk_size=64 * 1024):
                        f.write(chunk)

            with tmp.open("rb") as f:
                head = f.read(64)
            if not is_valid(dest, head):
                raise ValueError("unexpected file content")

            tmp.replace(dest)
            return

        except (requests.RequestException, ValueError) as error:
            tmp.unlink(missing_ok=True)
            if attempt == RETRIES:
                raise RuntimeError(f"{url}: {error}") from error
            logger.warning("    retry %d/%d in %d s: %s", attempt + 1, RETRIES, 2**attempt, error)
            time.sleep(2**attempt)  # 2, 4, 8 s


def is_valid(dest: Path, head: bytes) -> bool:
    """Check the file signature (the CDC can return an HTML error page with status 200).

    Args:
        dest: Final path of the file; its suffix tells the expected format.
        head: First bytes of the downloaded file.

    Returns:
        True if the content matches the expected format.
    """
    if dest.suffix == ".xpt":
        return head.startswith(b"HEADER RECORD")
    if dest.suffix == ".pdf":
        return head.startswith(b"%PDF")
    if dest.suffix == ".dat":
        return not head.lstrip().startswith(b"<")
    return True


def file_sha256(path: Path) -> str:
    """SHA-256 of a file's content, read in blocks: same content → same hash.

    Args:
        path: File to hash.

    Returns:
        The 64-character hexadecimal hash.
    """
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
