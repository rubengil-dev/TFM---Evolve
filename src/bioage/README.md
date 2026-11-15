# bioage/

The project package: from the NHANES download to the biological age of a person.

- `main.py`: the only entry point, runs every pipeline step in order (`uv run python -m bioage.main`).
- `config/`: paths, external sources and study tables. No logic.
- `pipeline/`: one file per step, numbered, each with its `run()`.
- `models/`: the steps of the model, plus `predict.py`, which is what the app uses.
- `utils/`: functions shared across the project, one file per topic.
