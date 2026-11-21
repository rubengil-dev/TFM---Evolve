# pipeline/
One file per pipeline step, in order:

- `s1_download_bronze`      : Download raw data.
- `s2_build_raw_silver`     : Merges data into 1 table.
- `s3_build_clean_silver`   : Standardizes & cleans data.
- `s4_build_gold`           : Prepares data for modeling.
- `s5_build_model`          : Builds the models.

Each one has a `run()` that `main.py` calls.
