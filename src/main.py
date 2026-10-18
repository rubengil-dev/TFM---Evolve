"""
Data pipeline:
    Bronze → Silver → Gold.
"""

# Imports
from src.pipeline import download_bronze, build_raw_silver, build_clean_silver, build_gold


def main():
    download_bronze.run()
    build_raw_silver.run()
    build_clean_silver.run()
    build_gold.run()


if __name__ == "__main__":
    main()
