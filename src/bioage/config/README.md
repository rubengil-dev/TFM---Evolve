# config/
Files within this folder contain internal configuration.

- `paths.py`            : Internal project paths.
- `sources.py`          : Data download paths and config.
- `study.py`            : Project design parameters.
- `model_levels.py`     : Variables for each model and discarded ones.
- `nhanes_codes.py`     : NHANES answering codes.
- `gold_columns.py`     : Role of each Gold column.
- `renames.py`          : Clear and standard name definition.
- `corrections.py`      : Corrections for NHANES measurement method changes.
- `validation_rules.py` : Gold data validation thresholds.
- `plausible_ranges.py` : Removes data artifacts (not illness data).

Hand-aligned tables: ruff does not format this folder, keep the columns aligned when editing.
