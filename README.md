# Biological age calculator

A free website that estimates biological age from a real blood test: the user uploads the PDF and, optionally, answers a short lifestyle questionnaire; only values the app could not read with confidence are shown for review.

It is not medical advice or a diagnosis.

## Who it is for and why
- For people in Spain without medical training, using it from home.
- No typing values by hand: the app reads them from the PDF.
- An understandable result: an age and an explanation, not a table of values.

## How it works
- **Data:** NHANES 1999-2018 (United States) with its linked mortality up to 2019. Adults aged 18 to 79.
- **Model:** there is no "true biological age" label, so a survival model (Cox) estimates the risk of dying within 10 years, and that risk is translated into the age at which a typical person of the same sex has the same risk, in the style of PhenoAge (Levine et al., 2018).
- **Four levels**, depending on what the user brings: basic blood test, extended blood test, basic plus questionnaire, or everything.
- **Privacy:** this is health data; the app processes everything in memory and stores nothing.

## Status
- Done: data, preparation and model.
- In progress: the app (PDF reading, review, questionnaire and result) and its deployment.

## How to install and run
It needs [uv](https://docs.astral.sh/uv/), which installs Python 3.11 and every dependency. From the repository root:

```bash
uv sync
uv run python -m bioage.main
uv run pytest
```

- `uv sync` creates `.venv` with the exact versions of `uv.lock`.
- `bioage.main` downloads NHANES (about 400 MB, resumable), builds the data layers and trains the models in `models/`.
- Tests that need `data/` are skipped if it does not exist; the rest run with what is in git.
- The project dependencies are only what the app needs to load a model and predict; the analysis and training libraries are in the `dev` group.

To check the code before committing, install the hooks once with `uv run pre-commit install`.

## Structure
```
TFM/
├── src/bioage/     # The package: pipeline, model steps, app, configuration and shared functions
├── frontend/       # The web interface (React); how to run it is in its README
├── models/         # One trained model per level, with its data fingerprint, code commit and versions
├── notebooks/      # Exploration, model comparison per level, biological age, PhenoAge and final evaluation
├── tests/          # Tests with pytest, mirroring src/; those of the app also run in GitHub Actions
├── docs/           # Deliverables of the master's programme
├── data/           # Bronze → Silver → Gold layers; not in git, rebuilt by the pipeline
└── private/        # Real blood tests in PDF to try the app; not in git
```

## Main limitations
- Reference population from the United States: it is assumed to be equivalent to the Spanish one.
- Some analytes change method between cycles with no official correction (for example RDW, which is left out of the model).
- Biological age is less precise in young people at low risk.

## License
[MIT](LICENSE).
