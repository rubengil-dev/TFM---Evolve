"""Build bronze data layer.

Download unchanged files (only those not on disk yet).

Files downloaded:
- NHANES 1999-2018: participant data (.xpt) and codebook (.htm/.pdf) per dataset and cycle
- NCHS linked mortality (follow-up to 2019): one .dat per cycle
- Saved to data/01_bronze/<cycle>/ with their original names
- manifest.csv: file, URL, SHA-256 and first download date
"""

# Imports
import csv
import logging
from datetime import datetime
from pathlib import Path

from bioage.config.paths import BRONZE, BRONZE_MANIFEST
from bioage.config.sources import CYCLES, DATASETS, MORTALITY_FILE, MORTALITY_URL, NHANES_URL, PDF_DOCS
from bioage.utils.data_download import download, file_sha256
from bioage.utils.nhanes import cycle_label

logger = logging.getLogger(__name__)


def run() -> None:
    """Bronze step, called from main."""
    BRONZE.mkdir(parents=True, exist_ok=True)
    jobs = build_jobs()
    failed = download_all(jobs)
    write_manifest(jobs)
    print_summary(jobs, failed)


def build_jobs() -> list[dict]:
    """List of files to download.

    Returns:
        One job per file: dataset, cycle, url and dest.
    """
    jobs = []

    # NHANES: data + codebook
    for dataset, names in DATASETS.items():
        for year, name in zip(CYCLES, names, strict=True):
            if name is None:
                continue
            doc_ext = "pdf" if name in PDF_DOCS else "htm"
            for ext in ("xpt", doc_ext):
                jobs.append(
                    {
                        "dataset": dataset,
                        "cycle": cycle_label(year),
                        "url": NHANES_URL.format(year=year, name=name, ext=ext),
                        "dest": BRONZE / cycle_label(year) / f"{name}.{ext}",
                    }
                )

    # Mortality
    for year in CYCLES:
        jobs.append(
            {
                "dataset": "MORT",
                "cycle": cycle_label(year),
                "url": MORTALITY_URL.format(cycle=cycle_label(year)),
                "dest": BRONZE / cycle_label(year) / MORTALITY_FILE.format(cycle=cycle_label(year)),
            }
        )

    return jobs


def download_all(jobs: list[dict]) -> list[dict]:
    """Download the files not yet on disk.

    Args:
        jobs: Files to download.

    Returns:
        The jobs that failed.
    """
    failed = []
    for i, job in enumerate(jobs, 1):
        if job["dest"].exists():
            continue
        logger.info("[%d/%d] %s", i, len(jobs), job["dest"].relative_to(BRONZE).as_posix())
        try:
            download(job["url"], job["dest"])
        except RuntimeError as error:
            logger.error("    FAILED: %s", error)
            failed.append(job)
    return failed


def write_manifest(jobs: list[dict]) -> None:
    """Write one row per file on disk, with its SHA-256 and the date it was first downloaded.

    Args:
        jobs: Files of the Bronze layer.
    """
    previous = read_manifest()
    rows = []
    for job in jobs:
        dest = job["dest"]
        if not dest.exists():
            continue
        path = dest.relative_to(BRONZE).as_posix()
        sha256 = file_sha256(dest)
        rows.append(
            {
                "dataset": job["dataset"],
                "cycle": job["cycle"],
                "path": path,
                "url": job["url"],
                "sha256": sha256,
                "downloaded_at": download_date(previous.get(path), sha256, dest),
            }
        )
    with BRONZE_MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["dataset", "cycle", "path", "url", "sha256", "downloaded_at"])
        writer.writeheader()
        writer.writerows(rows)


def read_manifest() -> dict[str, dict]:
    """Rows of the current manifest by path; empty if there is none yet.

    Returns:
        Path → row.
    """
    if not BRONZE_MANIFEST.exists():
        return {}
    with BRONZE_MANIFEST.open(newline="", encoding="utf-8") as f:
        return {row["path"]: row for row in csv.DictReader(f)}


def download_date(previous: dict | None, sha256: str, dest: Path) -> str:
    """Date the file was first downloaded.

    - Same file as in the previous manifest → its date, even if the file was copied since
    - Previous manifest without SHA-256 (older format) → its date
    - New or changed file → its modification date, the moment it was just downloaded

    Args:
        previous: Row of the file in the previous manifest, or None.
        sha256: Hash of the file now.
        dest: Path of the file.

    Returns:
        Date as YYYY-MM-DD HH:MM.
    """
    if previous and previous.get("sha256", sha256) == sha256:
        return previous["downloaded_at"]
    return datetime.fromtimestamp(dest.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


def print_summary(jobs: list[dict], failed: list[dict]) -> None:
    """Print the files on disk, the total size and the failed URLs.

    Args:
        jobs: Files of the Bronze layer.
        failed: Jobs that could not be downloaded.
    """
    on_disk = [job for job in jobs if job["dest"].exists()]
    total_mb = sum(job["dest"].stat().st_size for job in on_disk) / 1e6
    print(f"\n{len(on_disk)}/{len(jobs)} files in bronze ({total_mb:.1f} MB)")
    if failed:
        print(f"{len(failed)} failed, re-run to retry:")
        for job in failed:
            print(f"  - {job['url']}")
