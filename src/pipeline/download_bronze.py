"""
Download, unchanged, raw source files to "data/01_bronze/<cycle>/" if they are not already on disk.

- NHANES 1999-2018: participants data (.xpt) + codebook (.htm/.pdf) per dataset and cycle
- NCHS (follow-up to 2019): linked mortality, one .dat per cycle
- manifest.csv: file, URL, size and download date
"""

# Imports
import csv
from datetime import datetime

from src.config.paths import BRONZE, BRONZE_MANIFEST
from src.config.sources import CYCLES, DATASETS, PDF_DOCS, NHANES_URL, MORTALITY_FILE, MORTALITY_URL
from src.utils.data_download import download
from src.utils.nhanes import cycle_label


def run():
    """Bronze step, called from main."""
    BRONZE.mkdir(parents=True, exist_ok=True)
    jobs = build_jobs()
    failed = download_all(jobs)
    write_manifest(jobs)
    print_summary(jobs, failed)


def build_jobs():
    """List of files to download: dataset, cycle, url, dest."""
    jobs = []

    # NHANES: data + codebook
    for dataset, names in DATASETS.items():
        for year, name in zip(CYCLES, names):
            if name is None:
                continue
            doc_ext = "pdf" if name in PDF_DOCS else "htm"
            for ext in ("xpt", doc_ext):
                jobs.append({
                    "dataset": dataset,
                    "cycle": cycle_label(year),
                    "url": NHANES_URL.format(year=year, name=name, ext=ext),
                    "dest": BRONZE / cycle_label(year) / f"{name}.{ext}",
                })

    # Mortality
    for year in CYCLES:
        jobs.append({
            "dataset": "MORT",
            "cycle": cycle_label(year),
            "url": MORTALITY_URL.format(cycle=cycle_label(year)),
            "dest": BRONZE / cycle_label(year) / MORTALITY_FILE.format(cycle=cycle_label(year)),
        })

    return jobs


def download_all(jobs):
    """Download files not yet on disk. Returns the ones that failed."""
    failed = []
    for i, job in enumerate(jobs, 1):
        if job["dest"].exists():
            continue
        print(f"[{i}/{len(jobs)}] {job['dest'].relative_to(BRONZE).as_posix()}", flush=True)
        try:
            download(job["url"], job["dest"])
        except RuntimeError as error:
            print(f"    FAILED: {error}", flush=True)
            failed.append(job)
    return failed


def write_manifest(jobs):
    """One row per file on disk. Download date = file modification date."""
    with open(BRONZE_MANIFEST, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["dataset", "cycle", "path", "url", "bytes", "downloaded_at"])
        for job in jobs:
            dest = job["dest"]
            if not dest.exists():
                continue
            stat = dest.stat()
            writer.writerow([
                job["dataset"],
                job["cycle"],
                dest.relative_to(BRONZE).as_posix(),
                job["url"],
                stat.st_size,
                datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            ])


def print_summary(jobs, failed):
    """Files on disk, total size and failed URLs."""
    on_disk = [job for job in jobs if job["dest"].exists()]
    total_mb = sum(job["dest"].stat().st_size for job in on_disk) / 1e6
    print(f"\n{len(on_disk)}/{len(jobs)} files in bronze ({total_mb:.1f} MB)")
    if failed:
        print(f"{len(failed)} failed, re-run to retry:")
        for job in failed:
            print(f"  - {job['url']}")
