# data/

Data layers, rebuilt by the pipeline (`uv run python -m bioage.main`). Not in git, except this file.

- `01_bronze/`: NHANES and mortality files as downloaded from the CDC. One folder per cycle. Never edited.
- `02_silver/`: `silver_raw.parquet` (every cycle joined, one row per person) and `silver_clean.parquet` (study population, clean variables).
- `03_gold/`: `gold.parquet`, the only table the model and the app read.
