"""
Model step of the pipeline, the final model of each level (1 to 4), the one the app uses:
    - Fitted on all of Gold, train and test (the test was already used once, in the final evaluation)
    - Preprocessing and algorithm of the level (LEVEL_COLUMNS, LEVEL_MODELS)
    - Biological age reference fitted on the model's own risk
    - Saved to models/<level>.joblib with its columns and library versions
"""

# Imports
from datetime import date

import joblib
import pandas as pd
import sklearn
import sksurv

from src.config.model_sets import LEVEL_COLUMNS, LEVEL_MODELS
from src.config.paths import GOLD_TABLE, TRAINED_MODELS
from src.models.s3_algorithms import build_pipeline, survival_target
from src.models.s4_biological_age import fit_reference
from src.models.s5_evaluation import c_index, risk_at_horizon


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
    """Fitted pipeline, biological age reference and what is needed to use them, all from data."""
    pipeline = build_pipeline(LEVEL_MODELS[level], columns).fit(data, survival_target(data))
    risk = risk_at_horizon(pipeline, data)
    return {
        "level": level,
        "columns": columns,
        "pipeline": pipeline,
        "reference": fit_reference(risk, data),
        "c_index_fit": c_index(risk, data, data),
        "trained_on": {"people": len(data), "deaths": int(data["death"].sum()), "date": date.today().isoformat()},
        "versions": {"scikit-learn": sklearn.__version__, "scikit-survival": sksurv.__version__},
    }


def print_summary(bundle, path):
    """Variables, people, training C-index and file of a level."""
    trained_on = bundle["trained_on"]
    print(
        f"{bundle['level']}: {len(bundle['columns'])} variables | {trained_on['people']} people, {trained_on['deaths']} deaths"
        f" | C-index in training data {bundle['c_index_fit']:.4f} | {path.name}"
    )
