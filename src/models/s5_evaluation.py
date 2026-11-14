"""
Step 5, evaluation at 10 years, out of training:
    - evaluate_level: summary of every model of a level
    - compare_risks: whether one model really beats another
    - bootstrap_c_indexes, confidence_interval: C-index of several models with its interval
    - calibration_in_years: calibration gap told in years of biological age
    - plot_calibration: predicted against observed risk
    - tune_model: best settings of a model
"""

# Imports
import time

import matplotlib.pyplot as plt
import numpy as np
import optuna
import pandas as pd
from scipy.optimize import brentq
from sksurv.metrics import concordance_index_ipcw
from sksurv.nonparametric import kaplan_meier_estimator

from src.config.study import (
    BOOTSTRAP_SAMPLES,
    CALIBRATION_GROUPS,
    HORIZON_MONTHS,
    SPLIT_SEED,
    TUNING_SPACES,
    TUNING_TRIALS,
)
from src.models.predict import risk_at_horizon
from src.models.s3_algorithms import MODELS, build_pipeline, survival_target
from src.models.s4_biological_age import reference_risk
from src.utils.features import age_groups

YEARS_SEARCHED = 50  # largest shift tried when telling a calibration gap in years


def evaluate_level(columns, train, folds, models=MODELS, settings=None):
    """
    Every model of a level, cross-validated:
        - settings: tuned values of each model, if any
        - summary: one row per model
        - details: each model's risk, groups and calibration
    """
    settings = settings or {}
    details = {name: cross_validate(name, columns, train, folds, settings.get(name)) for name in models}
    summary = pd.DataFrame({name: summarize(detail) for name, detail in details.items()}).T
    return summary.round(4), details


def cross_validate(name, columns, train, folds, settings=None):
    """One model over the folds → out-of-fold risk and metrics."""
    risk = pd.Series(index=train.index, dtype=float)
    rows = []
    for fit_rows, validation_rows in folds:
        fit, validation = train.iloc[fit_rows], train.iloc[validation_rows]
        start = time.time()
        pipeline = build_pipeline(name, columns, settings).fit(fit, survival_target(fit))
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
    values = bootstrap_c_indexes({"new": risk_new, "old": risk_old}, data, samples)
    return confidence_interval(values["new"] - values["old"]).rename(columns={"value": "difference"})


def bootstrap_c_indexes(risks, data, samples=BOOTSTRAP_SAMPLES):
    """
    C-index of several models on the same resampled people:
        - risks: model name → risk of each person in data
        - One row per sample; columns (model, 'c_index' / 'c_index_same_age')
        - Differences between columns give the interval of an improvement
    """
    rng = np.random.default_rng(SPLIT_SEED)
    rows = []
    for _ in range(samples):
        picked = rng.integers(0, len(data), len(data))
        sample = data.iloc[picked].reset_index(drop=True)
        groups = age_groups(sample)
        row = {}
        for name, risk in risks.items():
            resampled = pd.Series(np.asarray(risk)[picked])
            row[(name, "c_index")] = c_index(resampled, sample, data)
            row[(name, "c_index_same_age")] = same_age_c_index(c_index_by_group(resampled, sample, groups, data))
        rows.append(row)
    table = pd.DataFrame(rows)
    table.columns = pd.MultiIndex.from_tuples(table.columns)
    return table


def confidence_interval(values):
    """Mean and 95% interval of each column of bootstrap values."""
    return pd.DataFrame({
        "value": values.mean(),
        "low": values.quantile(0.025),
        "high": values.quantile(0.975),
    }).round(4)


def calibration_in_years(risk, age, data, reference):
    """
    Calibration table with each gap told in years:
        - age: biological age of each person from this risk
        - years: shift of the group's biological ages that makes its predicted risk match the observed one
        - years above 0 = biological age underestimated
    """
    table = calibration_table(risk, data)
    groups = pd.qcut(risk, CALIBRATION_GROUPS, labels=False, duplicates="drop")
    table["age"] = pd.Series(np.asarray(age), index=data.index).groupby(groups).mean()
    table["years"] = [
        years_to_observed(np.asarray(age)[np.asarray(groups == group)], data.loc[groups == group, "sex"], observed, reference)
        for group, observed in table["observed"].items()
    ]
    return table


def years_to_observed(ages, sex, observed, reference):
    """Years to add to every age so that the mean typical risk equals the observed risk; NaN if out of reach."""
    gap = lambda years: reference_risk(ages + years, sex, reference).mean() - observed
    if gap(-YEARS_SEARCHED) * gap(YEARS_SEARCHED) > 0:
        return np.nan
    return brentq(gap, -YEARS_SEARCHED, YEARS_SEARCHED)


def tune_model(name, columns, train, folds, trials=TUNING_TRIALS):
    """Settings with the best same-age C-index, searched with Optuna."""
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=SPLIT_SEED))
    study.optimize(lambda trial: same_age_score(name, columns, train, folds, suggest_settings(trial, name)), n_trials=trials)
    return suggest_settings(optuna.trial.FixedTrial(study.best_params), name)


def suggest_settings(trial, name):
    """One set of settings from the search space of a model."""
    suggest = {
        "int": trial.suggest_int,
        "float": trial.suggest_float,
        "log": lambda key, low, high: trial.suggest_float(key, low, high, log=True),
        "log_list": lambda key, low, high: [trial.suggest_float(key, low, high, log=True)],
    }
    return {key: suggest[kind](key, low, high) for key, (kind, low, high) in TUNING_SPACES[name].items()}


def same_age_score(name, columns, train, folds, settings):
    """Same-age C-index of some settings, on people left out of each fit."""
    return same_age_c_index(cross_validate(name, columns, train, folds, settings)["by_age"])


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
