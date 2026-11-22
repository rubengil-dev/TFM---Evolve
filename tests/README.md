# tests/
Tests with pytest, one `test_<file>.py` per source file, in the same folders as `src/bioage/`:

- `conftest.py` : Builds a small made-up Gold shared by several tests.
- `app/`        : Saved models, as the app uses them.
- `config/`     : Configuration consistency, without data: one file for the whole folder.
- `models/`     : Model steps on made-up data.
- `pipeline/`   : Pipeline steps; some need `data/`.
- `utils/`      : Shared functions.

Run them with `uv run pytest`. Tests that need `data/` are skipped if it does not exist.

NOTE: `app/reference_ages.json` holds the biological age of a few made-up people in each level. Rewrite it with `write_reference` (in `app/test_predict.py`) only after changing the model on purpose, and review the diff.
