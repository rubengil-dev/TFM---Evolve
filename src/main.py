"""
Data pipeline:
    Bronze → Silver → Gold.
"""

# Imports
from src.pipeline import download_bronze


def main():
    download_bronze.run()


if __name__ == "__main__":
    main()
