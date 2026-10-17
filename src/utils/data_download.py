"""
Helpers to download files: 
    - Retries
    - No half-written files
    - No error pages saved as data
"""

# Imports
import requests
import time

from src.config.sources import RETRIES, TIMEOUT


def is_valid(dest, head):
    """Check file signature (CDC can return an HTML error page with status 200)."""
    if dest.suffix == ".xpt":
        return head.startswith(b"HEADER RECORD")
    if dest.suffix == ".pdf":
        return head.startswith(b"%PDF")
    if dest.suffix == ".dat":
        return not head.lstrip().startswith(b"<")
    return True


def download(url, dest):
    """Download to a .part file, rename only when complete. Retries with growing wait."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")

    for attempt in range(1, RETRIES + 1):
        try:
            with requests.get(url, stream=True, timeout=TIMEOUT) as response:
                response.raise_for_status()
                with open(tmp, "wb") as f:
                    for chunk in response.iter_content(chunk_size=64 * 1024):
                        f.write(chunk)

            with open(tmp, "rb") as f:
                head = f.read(64)
            if not is_valid(dest, head):
                raise ValueError("unexpected file content")

            tmp.replace(dest)
            return

        except (requests.RequestException, ValueError) as error:
            tmp.unlink(missing_ok=True)
            if attempt == RETRIES:
                raise RuntimeError(f"{url}: {error}")
            time.sleep(2 ** attempt)  # 2, 4, 8 s
