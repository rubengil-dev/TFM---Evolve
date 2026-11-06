"""
Step 3, the four contenders of every level:
    - Cox
    - Cox elastic net
    - Random survival forest
    - Gradient boosting
"""

# Imports
from sklearn.pipeline import Pipeline
from sksurv.ensemble import RandomSurvivalForest
from sksurv.linear_model import CoxnetSurvivalAnalysis, CoxPHSurvivalAnalysis
from sksurv.linear_model.coxph import BreslowEstimator
from sksurv.util import Surv
from xgboost import XGBRegressor

from src.config.study import MODEL_PARAMS
from src.models.s2_preprocessing import build_preprocessor


class GradientBoostingCox(XGBRegressor):
    """XGBoost with the outcome format and the survival curves of the other models."""

    def fit(self, X, y, **kwargs):
        """
        Survival outcome → XGBoost label, then the baseline risk over time:
            - Label: months of follow-up, negative if the person did not die
        """
        super().fit(X, y["time"] * (2 * y["event"] - 1), **kwargs)
        self.baseline_ = BreslowEstimator().fit(self.log_hazard(X), y["event"], y["time"])
        return self

    def predict_survival_function(self, X):
        """Survival curve of each person."""
        return self.baseline_.get_survival_function(self.log_hazard(X))

    def log_hazard(self, X):
        """Raw score of the model."""
        return self.predict(X, output_margin=True)


MODELS = {
    "cox":                CoxPHSurvivalAnalysis,
    "elastic_net":        CoxnetSurvivalAnalysis,
    "random_forest":      RandomSurvivalForest,
    "gradient_boosting":  GradientBoostingCox,
}


def build_pipeline(name, columns, settings=None):
    """Unfitted preprocessing and model for an algorithm and a list of Gold columns; settings replace the fixed ones."""
    return Pipeline([
        ("preprocessing", build_preprocessor(columns)),
        ("model", MODELS[name](**{**MODEL_PARAMS[name], **(settings or {})})),
    ])


def survival_target(data):
    """Outcome in the format of the models: death and months of follow-up."""
    return Surv.from_arrays(event=data["death"] == 1, time=data["follow_up_months"])
