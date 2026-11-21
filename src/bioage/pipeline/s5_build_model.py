"""Building model from gold data layer.

- Fitted on all of Gold.
- 4 model levels, based on what the app needs.
- Biological age reference fitted on the model's own risk
- Saved to models/<level>.joblib with its columns, what it was trained on and library versions
"""

# Imports
import joblib
import pandas as pd

from bioage.config.model_levels import LEVEL_COLUMNS, LEVEL_MODELS
from bioage.config.paths import GOLD_TABLE, TRAINED_MODELS
from bioage.models.s3_algorithms import build_pipeline, survival_target
from bioage.models.s4_biological_age import fit_reference, risk_at_horizon
from bioage.models.s5_evaluation import c_index
from bioage.utils.provenance import code_version, data_fingerprint, library_versions
from bioage.utils.step_info import print_model_summary


def run() -> None:
    """Model step, called from main."""
    gold = pd.read_parquet(GOLD_TABLE)
    TRAINED_MODELS.mkdir(exist_ok=True)
    for level, columns in LEVEL_COLUMNS.items():
        bundle = build_level(level, columns, gold)
        path = TRAINED_MODELS / f"{level}.joblib"
        joblib.dump(bundle, path)
        print_model_summary(bundle, path)


def build_level(level: str, columns: list[str], data: pd.DataFrame) -> dict:
    """Fitted pipeline, biological age reference and what is needed to use and trace them, all from data.

    Args:
        level: Name of the level.
        columns: Gold columns of the level.
        data: People to fit on.

    Returns:
        Bundle saved for the level.
    """
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
