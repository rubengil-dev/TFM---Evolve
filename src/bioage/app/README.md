# app/
What the app runs:

- `api.py`: Web server; receives the requests and hands them to the rest.
- `schemas.py`: What enters and leaves each endpoint, and its error.
- `read_pdf.py`: Reads a blood test in PDF.
- `calculate.py`: Picks the model and calculates the result.
- `validation.py`: Checks before calculating.
- `predict.py`: Loads a saved model and computes the biological age.
- `utils.py`: Functions shared within the app.
- `logs.py`: One line of JSON per request, with nothing of the user.

Run it with `uv run uvicorn bioage.app.api:app --reload`; the endpoints can be tried at http://127.0.0.1:8000/docs.
