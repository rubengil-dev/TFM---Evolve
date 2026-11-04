"""
Step 5, evaluation at 10 years, out of training:
    - evaluate_level: summary of every model of a level
    - compare_risks: whether one model really beats another
    - plot_calibration: predicted against observed risk
"""

# Imports
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sksurv.metrics import concordance_index_ipcw
from sksurv.nonparametric import kaplan_meier_estimator

from src.config.study import BOOTSTRAP_SAMPLES, CALIBRATION_GROUPS, HORIZON_MONTHS, SPLIT_SEED
from src.models.s3_algorithms import MODELS, build_pipeline, survival_target
from src.utils.features import age_groups


def evaluate_level(columns, train, folds, models=MODELS):
    """
    Every model of a level, cross-validated:
        - summary: one row per model
        - details: each model's risk, groups and calibration
    """
    details = {name: cross_validate(name, columns, train, folds) for name in models}
    summary = pd.DataFrame({name: summarize(detail) for name, detail in details.items()}).T
    return summary.round(4), details


def cross_validate(name, columns, train, folds):
    """One model over the folds → out-of-fold risk and metrics."""
    risk = pd.Series(index=train.index, dtype=float)
    rows = []
    for fit_rows, validation_rows in folds:
        fit, validation = train.iloc[fit_rows], train.iloc[validation_rows]
        start = time.time()
        pipeline = build_pipeline(name, columns).fit(fit, survival_target(fit))
        seconds = time.time() - start
        risk.loc[validation.index] = risk_at_horizon(pipeline, validation)
        rows.append({
            "c_index": c_index(risk.loc[validation.index], validation, fit),
            "c_index_fit": c_index(risk_at_horizon(pipeline, fit), fit, fit),
            "seconds": seconds,
        })
    return {
        "folds": pd.DataFrame(rows),
        "risk": risk,
        "by_age": c_index_by_group(risk, train, age_groups(train)),
        "by_sex": c_index_by_group(risk, train, train["sex"]),
        "calibration": calibration_table(risk, train),
    }


def risk_at_horizon(pipeline, data):
    """Probability of dying within the horizon, for each person."""
    curves = pipeline.predict_survival_function(data)
    return 1 - np.array([curve(HORIZON_MONTHS) for curve in curves])


def c_index(risk, data, reference):
    """C-index of Uno up to the horizon; reference: data for the censoring distribution."""
    return concordance_index_ipcw(
        survival_target(reference), survival_target(data), np.asarray(risk), tau=HORIZON_MONTHS
    )[0]


def c_index_by_group(risk, data, groups, reference=None):
    """C-index and deaths within the horizon of each group."""
    rows = {}
    for group, members in data.groupby(groups, observed=True):
        deaths = ((members["death"] == 1) & (members["follow_up_months"] <= HORIZON_MONTHS)).sum()
        rows[group] = {
            "c_index": c_index(risk.loc[members.index], members, data if reference is None else reference),
            "deaths": int(deaths),
        }
    return pd.DataFrame(rows).T


def same_age_c_index(by_age):
    """C-index among people of the same age group, weighted by deaths."""
    return np.average(by_age["c_index"], weights=by_age["deaths"])


def calibration_table(risk, data):
    """Predicted and observed risk of each risk group; gap above 0 = risk underestimated."""
    groups = pd.qcut(risk, CALIBRATION_GROUPS, labels=False, duplicates="drop")
    table = pd.DataFrame({
        "predicted": risk.groupby(groups).mean(),
        "observed": data.groupby(groups).apply(observed_risk, include_groups=False),
    })
    table["gap"] = table["observed"] - table["predicted"]
    return table


def observed_risk(data):
    """Share of people dead at the horizon, allowing for incomplete follow-up (Kaplan-Meier)."""
    times, survival = kaplan_meier_estimator(data["death"] == 1, data["follow_up_months"])
    return 1 - survival[np.searchsorted(times, HORIZON_MONTHS, side="right") - 1]


def summarize(detail):
    """One row of the level summary."""
    folds, calibration = detail["folds"], detail["calibration"]
    return {
        "c_index":             folds["c_index"].mean(),
        "c_index_std":         folds["c_index"].std(),
        "c_index_fit":         folds["c_index_fit"].mean(),
        "c_index_same_age":    same_age_c_index(detail["by_age"]),
        "c_index_female":      detail["by_sex"].loc["female", "c_index"],
        "c_index_male":        detail["by_sex"].loc["male", "c_index"],
        "calibration_gap":     calibration["gap"].abs().mean(),
        "worst_underestimate": calibration["gap"].max(),
        "seconds_per_fit":     folds["seconds"].mean(),
    }


def compare_risks(risk_new, risk_old, data, samples=BOOTSTRAP_SAMPLES):
    """
    Improvement of one risk over another, resampling the same people for both:
        - Difference in C-index, overall and within age group, with 95% interval
        - The improvement is real if the interval excludes 0
    """
    rng = np.random.default_rng(SPLIT_SEED)
    differences = []
    for _ in range(samples):
        rows = rng.integers(0, len(data), len(data))
        sample = data.iloc[rows].reset_index(drop=True)
        new, old = pd.Series(risk_new.to_numpy()[rows]), pd.Series(risk_old.to_numpy()[rows])
        groups = age_groups(sample)
        differences.append({
            "c_index": c_index(new, sample, data) - c_index(old, sample, data),
            "c_index_same_age": (
                same_age_c_index(c_index_by_group(new, sample, groups, data))
                - same_age_c_index(c_index_by_group(old, sample, groups, data))
            ),
        })
    differences = pd.DataFrame(differences)
    return pd.DataFrame({
        "difference": differences.mean(),
        "low": differences.quantile(0.025),
        "high": differences.quantile(0.975),
    }).round(4)


def plot_calibration(details):
    """One panel per model: predicted against observed risk, diagonal = perfect."""
    figure, axes = plt.subplots(1, len(details), figsize=(3.2 * len(details), 3.4), sharex=True, sharey=True, squeeze=False)
    for axis, (name, detail) in zip(axes[0], details.items()):
        table = detail["calibration"]
        limit = max(table["predicted"].max(), table["observed"].max()) * 1.05
        axis.plot([0, limit], [0, limit], color="#b0b0b0", linewidth=1)
        axis.plot(table["predicted"], table["observed"], color="#2a78d6", linewidth=2, marker="o", markersize=5)
        axis.set_title(name, fontsize=11)
        axis.set_xlabel("Predicted risk")
        axis.spines[["top", "right"]].set_visible(False)
    axes[0][0].set_ylabel("Observed risk")
    figure.tight_layout()
    return figure
