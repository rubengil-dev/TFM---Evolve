# tests/

Tests with pytest, mirroring `src/bioage/`: `test_<file>.py` in the folder of the file it tests. `conftest.py` builds a small made-up Gold shared by several of them.

Run them with `uv run pytest`. Tests that need `data/` are skipped if it does not exist.

`app/reference_ages.json` holds the biological age of a few made-up people in each level. Rewrite it with `write_reference` (in `app/test_predict.py`) only after changing the model on purpose, and review the diff.
