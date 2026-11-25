# tests/
Tests with pytest, one `test_<file>.py` per source file, in the same folders as `src/bioage/`:

- `conftest.py`             : Builds a small made-up Gold shared by several tests.
- `test_import_graph.py`    : Import graph in `docs/` up to date, and import rules between folders.
- `test_frontend_config.py` : What the front repeats from the backend.
- `app/`                    : What the app runs, with the saved models, and its web server.
- `config/`                 : Configuration consistency, without data: one file for the whole folder.
- `modeling/`               : Model steps on made-up data.
- `pipeline/`               : Pipeline steps; some need `data/`.
- `utils/`                  : Shared functions.

Run them with `uv run pytest`. Tests that need `data/` are skipped if it does not exist.

NOTE: `app/reference_ages.json` holds the biological age of a few made-up people in each level. Rewrite it with `write_reference` (in `app/test_predict.py`) only after changing the model on purpose, and review the diff.
