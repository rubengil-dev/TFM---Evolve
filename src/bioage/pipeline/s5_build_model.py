"""Building model from gold data layer.

- Fitted on all of Gold.
- 4 model levels, based on what the app needs.
- Biological age reference and average of each group, fitted on the model's own risk
- Margin ± and data needed, from the blocks of train (modeling/s7_margin.py)
- Saved to models/<level>.joblib with its columns, what it was trained on and library versions
"""

# Imports
import logging

import joblib
import pandas as pd

from bioage.config.model_levels import LEVEL_COLUMNS, LEVEL_MODELS
from bioage.config.paths import GOLD_TABLE, TRAINED_MODELS
from bioage.modeling.s3_algorithms import build_pipeline, survival_target
from bioage.modeling.s4_biological_age import fit_reference, risk_at_horizon
from bioage.modeling.s5_evaluation import c_index
from bioage.modeling.s6_group_years import fit_group_reference
from bioage.modeling.s7_margin import fit_margins
from bioage.utils.provenance import code_version, data_fingerprint, library_versions
from bioage.utils.step_info import print_model_summary

logger = logging.getLogger(__name__)


def run() -> None:
    """Model step, called from main."""
    gold = pd.read_parquet(GOLD_TABLE)
    TRAINED_MODELS.mkdir(exist_ok=True)
    logger.info("Margin: measuring on the blocks of train...")
    margins = fit_margins(gold)
    for level, columns in LEVEL_COLUMNS.items():
        logger.info("%s: training...", level)
        bundle = {**build_level(level, columns, gold), "margin": margins[level]}
        path = TRAINED_MODELS / f"{level}.joblib"
        joblib.dump(bundle, path)
        print_model_summary(bundle, path)


def build_level(level: str, columns: list[str], data: pd.DataFrame) -> dict:
    """Fitted pipeline, its references and what is needed to use and trace them, all from data.

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
        "group_reference": fit_group_reference(pipeline, data, columns),
        "c_index_fit": c_index(risk, data, data),
        "trained_on": {
            "people": len(data),
            "deaths": int(data["death"].sum()),
            "data_fingerprint": data_fingerprint(data),
            "code": code_version(),
        },
        "versions": library_versions(),
    }
