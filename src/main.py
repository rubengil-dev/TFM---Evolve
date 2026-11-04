"""
Pipeline:
    - Bronze → Silver raw → Silver clean → Gold → model
"""

# Imports
from src.pipeline import (
    s1_download_bronze,
    s2_build_raw_silver,
    s3_build_clean_silver,
    s4_build_gold,
    s5_build_model,
)


def main():
    """Run every pipeline step in order."""
    s1_download_bronze.run()
    s2_build_raw_silver.run()
    s3_build_clean_silver.run()
    s4_build_gold.run()
    s5_build_model.run()


if __name__ == "__main__":
    main()
