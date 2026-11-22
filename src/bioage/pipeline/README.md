# pipeline/
One file per pipeline step, in order:

- `s1_download_bronze.py`      : Download raw data.
- `s2_build_raw_silver.py`     : Merges data into 1 table.
- `s3_build_clean_silver.py`   : Standardizes & cleans data.
- `s4_build_gold.py`           : Prepares data for modeling.
- `s5_build_model.py`          : Builds the models.

Each one has a `run()` that `main.py` calls.
