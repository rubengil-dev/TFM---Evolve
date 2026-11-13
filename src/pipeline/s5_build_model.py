"""
Model step of the pipeline, the final model of each level (1 to 4), the one the app uses:
    - Fitted on all of Gold, train and test (the test was already used once, in the final evaluation)
    - Preprocessing and algorithm of the level (LEVEL_COLUMNS, LEVEL_MODELS)
    - Biological age reference fitted on the model's own risk
    - Saved to models/<level>.joblib with its columns, what it was trained on and library versions
"""

# Imports
import hashlib
import subprocess

import joblib
import pandas as pd

from src.config.model_sets import LEVEL_COLUMNS, LEVEL_MODELS
from src.config.paths import GOLD_TABLE, ROOT, TRAINED_MODELS
from src.models.predict import library_versions, risk_at_horizon
from src.models.s3_algorithms import build_pipeline, survival_target
from src.models.s4_biological_age import fit_reference
from src.models.s5_evaluation import c_index


def run():
    """Model step, called from main."""
    gold = pd.read_parquet(GOLD_TABLE)
    TRAINED_MODELS.mkdir(exist_ok=True)
    for level, columns in LEVEL_COLUMNS.items():
        bundle = build_level(level, columns, gold)
        path = TRAINED_MODELS / f"{level}.joblib"
        joblib.dump(bundle, path)
        print_summary(bundle, path)


def build_level(level, columns, data):
    """Fitted pipeline, biological age reference and what is needed to use and trace them, all from data."""
    pipeline = build_pipeline(LEVEL_MODELS[level], columns).fit(data, survival_target(data))
    risk = risk_at_horizon(pipeline, data)
    return {
        "level": level,
        "columns": columns,
        "pipeline": pipeline,
        "reference": fit_reference(risk, data),
        "c_index_fit": c_index(risk, data, data),
        "trained_on": {
            "people": len(data),
            "deaths": int(data["death"].sum()),
            "data_fingerprint": data_fingerprint(data),
            "code": code_version(),
        },
        "versions": library_versions(),
    }


def data_fingerprint(data):
    """Short hash of the rows and columns of data: same data → same fingerprint."""
    rows = pd.util.hash_pandas_object(data, index=False).to_numpy().tobytes()
    columns = ",".join(data.columns).encode()
    return hashlib.sha256(columns + rows).hexdigest()[:16]


def code_version():
    """Git commit of the code, with '-dirty' if src/ has uncommitted changes."""
    commit = git("rev-parse", "--short", "HEAD")
    changed = git("status", "--porcelain", "--", "src")
    return commit + ("-dirty" if changed else "")


def git(*arguments):
    """Output of a git command run at the project root."""
    return subprocess.run(["git", *arguments], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def print_summary(bundle, path):
    """Variables, people, training C-index, code and file of a level."""
    trained_on = bundle["trained_on"]
    print(
        f"{bundle['level']}: {len(bundle['columns'])} variables | {trained_on['people']} people, {trained_on['deaths']} deaths"
        f" | C-index in training data {bundle['c_index_fit']:.4f} | code {trained_on['code']} | {path.name}"
    )
