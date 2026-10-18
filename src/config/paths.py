"""
Internal project paths.
"""

from pathlib import Path

# Root
ROOT = Path(__file__).resolve().parents[2]

# Data layers
DATA = ROOT / "data"
BRONZE = DATA / "01_bronze"
SILVER = DATA / "02_silver"
GOLD = DATA / "03_gold"

# Outputs
BRONZE_MANIFEST = BRONZE / "manifest.csv"
SILVER_RAW = SILVER / "silver_raw.parquet"
SILVER_CLEAN = SILVER / "silver_clean.parquet"
GOLD_TABLE = GOLD / "gold.parquet"
