"""Tests: Models - Step 3, algorithms, on a made-up Gold.

- Tuned settings replace the fixed ones and keep the rest (what Optuna tried was really tried)
- Survival outcome: death and months in the fields the models read
- Cox and XGBoost (with its own survival label): risk orders who dies first
"""

# Imports
import numpy as np
import pandas as pd
import pytest

from bioage.config.model_levels import ROUTINE
from bioage.config.study import MODEL_PARAMS
from bioage.modeling.s3_algorithms import build_pipeline, survival_target
from bioage.modeling.s4_biological_age import risk_at_horizon
from bioage.modeling.s5_evaluation import c_index


def test_tuned_settings_replace_the_fixed_ones() -> None:
    model = build_pipeline("gradient_boosting", ROUTINE, {"max_depth": 5}).named_steps["model"]
    assert model.max_depth == 5
    assert model.learning_rate == MODEL_PARAMS["gradient_boosting"]["learning_rate"]


def test_survival_target_fields() -> None:
    target = survival_target(pd.DataFrame({"death": [1, 0], "follow_up_months": [12.0, 150.0]}))
    assert target["event"].tolist() == [True, False] and target["time"].tolist() == [12.0, 150.0]


@pytest.mark.parametrize("name", ["cox", "gradient_boosting"])
def test_risk_orders_who_dies_first(made_up_gold: pd.DataFrame, name: str) -> None:
    rng = np.random.default_rng(1)
    gold = made_up_gold.assign(death=rng.binomial(1, ((made_up_gold["age"] - 10) / 80).clip(0, 1)))
    pipeline = build_pipeline(name, ROUTINE).fit(gold, survival_target(gold))
    assert c_index(risk_at_horizon(pipeline, gold), gold, gold) > 0.6
