"""
Data pipeline:
    Bronze → Silver → Gold.
"""

# Imports
from src.pipeline import download_bronze, build_raw_silver


def main():
    download_bronze.run()
    build_raw_silver.run()


if __name__ == "__main__":
    main()
