"""ML Pipeline: Step 3 - Building the model(s).

Tested models:
- Cox (& its elastic net variant).
- Random survival forest.
- Gradient boosting.

SPOILER: Cox won in all 4 model levels.
"""

# Imports
from typing import Any, Self

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sksurv.ensemble import RandomSurvivalForest
from sksurv.linear_model import CoxnetSurvivalAnalysis, CoxPHSurvivalAnalysis
from sksurv.linear_model.coxph import BreslowEstimator
from sksurv.util import Surv
from xgboost import XGBRegressor

from bioage.config.study import MODEL_PARAMS
from bioage.modeling.s2_preprocessing import build_preprocessor


class GradientBoostingCox(XGBRegressor):
    """XGBoost with the outcome format and the survival curves of the other models."""

    def fit(self, X: pd.DataFrame, y: np.ndarray, **kwargs: Any) -> Self:
        """Survival outcome → XGBoost label, then the baseline risk over time.

        - Label: months of follow-up, negative if the person did not die

        Args:
            X: Preprocessed features.
            y: Survival outcome, with its event and time fields.
            **kwargs: Passed on to XGBoost.

        Returns:
            The fitted model.
        """
        super().fit(X, y["time"] * (2 * y["event"] - 1), **kwargs)
        self.baseline_ = BreslowEstimator().fit(self.log_hazard(X), y["event"], y["time"])
        return self

    def predict_survival_function(self, X: pd.DataFrame) -> np.ndarray:
        """Survival curve of each person.

        Args:
            X: Preprocessed features.

        Returns:
            One step function per person.
        """
        return self.baseline_.get_survival_function(self.log_hazard(X))

    def log_hazard(self, X: pd.DataFrame) -> np.ndarray:
        """Raw score of the model.

        Args:
            X: Preprocessed features.

        Returns:
            Score of each person.
        """
        return self.predict(X, output_margin=True)


# fmt: off
MODELS = {
    "cox":                CoxPHSurvivalAnalysis,
    "elastic_net":        CoxnetSurvivalAnalysis,
    "random_forest":      RandomSurvivalForest,
    "gradient_boosting":  GradientBoostingCox,
}
# fmt: on


def build_pipeline(name: str, columns: list[str], settings: dict | None = None) -> Pipeline:
    """Unfitted preprocessing and model for an algorithm and a list of Gold columns.

    Args:
        name: Algorithm key in MODELS.
        columns: Gold columns the model uses.
        settings: Values that replace the fixed ones of MODEL_PARAMS.

    Returns:
        Pipeline, not fitted yet.
    """
    return Pipeline(
        [
            ("preprocessing", build_preprocessor(columns)),
            ("model", MODELS[name](**{**MODEL_PARAMS[name], **(settings or {})})),
        ]
    )


def survival_target(data: pd.DataFrame) -> np.ndarray:
    """Outcome in the format of the models: death and months of follow-up.

    Args:
        data: People with their outcome columns.

    Returns:
        Structured array with the event and time fields.
    """
    return Surv.from_arrays(event=data["death"] == 1, time=data["follow_up_months"])
