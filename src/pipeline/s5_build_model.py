"""
Model step of the pipeline, the final model of each level (1 to 4):
    - Gold → train (the test is kept for the final evaluation)
    - Preprocessing and algorithm of the level (LEVEL_COLUMNS, LEVEL_MODELS) fitted on train
    - Biological age reference fitted on the model's own risk in train
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
from src.models.s1_split import split_train_test
from src.models.s3_algorithms import build_pipeline, survival_target
from src.models.s4_biological_age import fit_reference
from src.models.s5_evaluation import c_index, risk_at_horizon


def run():
    """Model step, called from main."""
    train, _ = split_train_test(pd.read_parquet(GOLD_TABLE))
    TRAINED_MODELS.mkdir(exist_ok=True)
    for level, columns in LEVEL_COLUMNS.items():
        bundle = build_level(level, columns, train)
        path = TRAINED_MODELS / f"{level}.joblib"
        joblib.dump(bundle, path)
        print_summary(bundle, path)


def build_level(level, columns, train):
    """Fitted pipeline, biological age reference and what is needed to use them."""
    pipeline = build_pipeline(LEVEL_MODELS[level], columns).fit(train, survival_target(train))
    risk = risk_at_horizon(pipeline, train)
    return {
        "level": level,
        "columns": columns,
        "pipeline": pipeline,
        "reference": fit_reference(risk, train),
        "c_index_fit": c_index(risk, train, train),
        "trained_on": {"people": len(train), "deaths": int(train["death"].sum()), "date": date.today().isoformat()},
        "versions": {"scikit-learn": sklearn.__version__, "scikit-survival": sksurv.__version__},
    }


def print_summary(bundle, path):
    """Variables, training C-index and file of a level."""
    print(f"{bundle['level']}: {len(bundle['columns'])} variables | C-index in train {bundle['c_index_fit']:.4f} | {path.name}")
