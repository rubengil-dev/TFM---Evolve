"""ML Pipeline: Step 5 - Model evaluation.

Evaluation:
1. Does the model order people correctly?
    - evaluate_level, cross_validate, metrics_row, c_index, c_index_by_group & same_age_c_index
2. Is the model accurate?
    - calibration_table, observed_risk, calibration_in_years & years_to_observed
3. Is every level actually better than a lower one?
    - compare_risks, bootstrap_c_indexes & confidence_interval

Tuning:
    - tune_model, suggest_settings & same_age_score
"""

# Imports
import time

import numpy as np
import optuna
import pandas as pd
from scipy.optimize import brentq
from sksurv.metrics import concordance_index_ipcw
from sksurv.nonparametric import kaplan_meier_estimator

from bioage.config.study import (
    BOOTSTRAP_SAMPLES,
    CALIBRATION_GROUPS,
    HORIZON_MONTHS,
    SPLIT_SEED,
    TUNING_SPACES,
    TUNING_TRIALS,
    YEARS_SEARCHED,
)
from bioage.models.s3_algorithms import MODELS, build_pipeline, survival_target
from bioage.models.s4_biological_age import reference_risk, risk_at_horizon
from bioage.utils.features import age_groups


def evaluate_level(
    columns: list[str],
    train: pd.DataFrame,
    folds: list[tuple[np.ndarray, np.ndarray]],
    models: dict[str, type] = MODELS,
    settings: dict[str, dict] | None = None,
) -> tuple[pd.DataFrame, dict[str, dict]]:
    """Every model of a level, cross-validated.

    Args:
        columns: Gold columns of the level.
        train: Train part of Gold.
        folds: Cross-validation folds of train.
        models: Algorithms to compare, name → class.
        settings: Tuned values of each model, if any.

    Returns:
        Summary with one row per model, and the detail of each one: risk, groups and calibration.
    """
    settings = settings or {}
    details = {name: cross_validate(name, columns, train, folds, settings.get(name)) for name in models}
    summary = pd.DataFrame({name: metrics_row(detail) for name, detail in details.items()}).T
    return summary.round(4), details


def cross_validate(
    name: str,
    columns: list[str],
    train: pd.DataFrame,
    folds: list[tuple[np.ndarray, np.ndarray]],
    settings: dict | None = None,
) -> dict:
    """One model over the folds → out-of-fold risk and metrics.

    Args:
        name: Algorithm key in MODELS.
        columns: Gold columns of the level.
        train: Train part of Gold.
        folds: Cross-validation folds of train.
        settings: Values that replace the fixed ones.

    Returns:
        Metrics per fold, out-of-fold risk, C-index by age and by sex, and calibration table.
    """
    risk = pd.Series(index=train.index, dtype=float)
    rows = []
    for fit_rows, validation_rows in folds:
        fit, validation = train.iloc[fit_rows], train.iloc[validation_rows]
        start = time.time()
        pipeline = build_pipeline(name, columns, settings).fit(fit, survival_target(fit))
        seconds = time.time() - start
        risk.loc[validation.index] = risk_at_horizon(pipeline, validation)
        rows.append(
            {
                "c_index": c_index(risk.loc[validation.index], validation, fit),
                "c_index_fit": c_index(risk_at_horizon(pipeline, fit), fit, fit),
                "seconds": seconds,
            }
        )
    return {
        "folds": pd.DataFrame(rows),
        "risk": risk,
        "by_age": c_index_by_group(risk, train, age_groups(train)),
        "by_sex": c_index_by_group(risk, train, train["sex"]),
        "calibration": calibration_table(risk, train),
    }


def c_index(risk: np.ndarray | pd.Series, data: pd.DataFrame, reference: pd.DataFrame) -> float:
    """C-index of Uno up to the horizon.

    Args:
        risk: Risk of each person in data.
        data: People to evaluate.
        reference: People that give the censoring distribution.

    Returns:
        The C-index.
    """
    return concordance_index_ipcw(
        survival_target(reference), survival_target(data), np.asarray(risk), tau=HORIZON_MONTHS
    )[0]


def c_index_by_group(
    risk: pd.Series, data: pd.DataFrame, groups: pd.Series, reference: pd.DataFrame | None = None
) -> pd.DataFrame:
    """C-index and deaths within the horizon of each group.

    Args:
        risk: Risk of each person in data.
        data: People to evaluate.
        groups: Group of each person.
        reference: People that give the censoring distribution; data if None.

    Returns:
        One row per group.
    """
    rows = {}
    for group, members in data.groupby(groups, observed=True):
        deaths = ((members["death"] == 1) & (members["follow_up_months"] <= HORIZON_MONTHS)).sum()
        rows[group] = {
            "c_index": c_index(risk.loc[members.index], members, data if reference is None else reference),
            "deaths": int(deaths),
        }
    return pd.DataFrame(rows).T


def same_age_c_index(by_age: pd.DataFrame) -> float:
    """C-index among people of the same age group, weighted by deaths.

    Args:
        by_age: C-index and deaths of each age group.

    Returns:
        The weighted C-index.
    """
    return np.average(by_age["c_index"], weights=by_age["deaths"])


def calibration_table(risk: pd.Series, data: pd.DataFrame) -> pd.DataFrame:
    """Predicted and observed risk of each risk group; gap above 0 = risk underestimated.

    Args:
        risk: Risk of each person in data.
        data: People to evaluate.

    Returns:
        One row per risk group.
    """
    groups = pd.qcut(risk, CALIBRATION_GROUPS, labels=False, duplicates="drop")
    table = pd.DataFrame(
        {
            "predicted": risk.groupby(groups).mean(),
            "observed": data.groupby(groups).apply(observed_risk, include_groups=False),
        }
    )
    table["gap"] = table["observed"] - table["predicted"]
    return table


def observed_risk(data: pd.DataFrame) -> float:
    """Share of people dead at the horizon, allowing for incomplete follow-up (Kaplan-Meier).

    Args:
        data: People of a group.

    Returns:
        Observed risk of the group.
    """
    times, survival = kaplan_meier_estimator(data["death"] == 1, data["follow_up_months"])
    return 1 - survival[np.searchsorted(times, HORIZON_MONTHS, side="right") - 1]


def metrics_row(detail: dict) -> dict[str, float]:
    """One row of the level summary.

    Args:
        detail: Detail of a model, from cross_validate.

    Returns:
        Metric → value.
    """
    folds, calibration = detail["folds"], detail["calibration"]
    # fmt: off
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
    # fmt: on


def compare_risks(
    risk_new: pd.Series, risk_old: pd.Series, data: pd.DataFrame, samples: int = BOOTSTRAP_SAMPLES
) -> pd.DataFrame:
    """Improvement of one risk over another, resampling the same people for both.

    - Difference in C-index, overall and within age group, with 95% interval
    - The improvement is real if the interval excludes 0

    Args:
        risk_new: Risk of the model that should improve.
        risk_old: Risk of the model it is compared with.
        data: People both risks belong to.
        samples: Number of bootstrap samples.

    Returns:
        Difference with its interval, one row per metric.
    """
    values = bootstrap_c_indexes({"new": risk_new, "old": risk_old}, data, samples)
    return confidence_interval(values["new"] - values["old"]).rename(columns={"value": "difference"})


def bootstrap_c_indexes(
    risks: dict[str, pd.Series], data: pd.DataFrame, samples: int = BOOTSTRAP_SAMPLES
) -> pd.DataFrame:
    """C-index of several models on the same resampled people.

    Differences between columns give the interval of an improvement.

    Args:
        risks: Model name → risk of each person in data.
        data: People the risks belong to.
        samples: Number of bootstrap samples.

    Returns:
        One row per sample; columns (model, 'c_index' / 'c_index_same_age').
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


def confidence_interval(values: pd.DataFrame) -> pd.DataFrame:
    """Mean and 95% interval of each column of bootstrap values.

    Args:
        values: One row per bootstrap sample.

    Returns:
        Value, low and high of each column.
    """
    return pd.DataFrame(
        {
            "value": values.mean(),
            "low": values.quantile(0.025),
            "high": values.quantile(0.975),
        }
    ).round(4)


def calibration_in_years(
    risk: pd.Series, age: np.ndarray, data: pd.DataFrame, reference: dict[str, np.ndarray]
) -> pd.DataFrame:
    """Calibration table with each gap told in years; years above 0 = biological age underestimated.

    Args:
        risk: Risk of each person in data.
        age: Biological age of each person from this risk.
        data: People to evaluate.
        reference: Reference curves of the level.

    Returns:
        Calibration table plus the mean age of each group and the years that make its
        predicted risk match the observed one.
    """
    table = calibration_table(risk, data)
    groups = pd.qcut(risk, CALIBRATION_GROUPS, labels=False, duplicates="drop")
    table["age"] = pd.Series(np.asarray(age), index=data.index).groupby(groups).mean()
    table["years"] = [
        years_to_observed(
            np.asarray(age)[np.asarray(groups == group)], data.loc[groups == group, "sex"], observed, reference
        )
        for group, observed in table["observed"].items()
    ]
    return table


def years_to_observed(ages: np.ndarray, sex: pd.Series, observed: float, reference: dict[str, np.ndarray]) -> float:
    """Years to add to every age so that the mean typical risk equals the observed risk.

    Args:
        ages: Biological ages of a group.
        sex: Sex of the same people.
        observed: Observed risk of the group.
        reference: Reference curves of the level.

    Returns:
        The shift in years; NaN if out of reach.
    """

    def gap(years: float) -> float:
        return reference_risk(ages + years, sex, reference).mean() - observed

    if gap(-YEARS_SEARCHED) * gap(YEARS_SEARCHED) > 0:
        return np.nan
    return brentq(gap, -YEARS_SEARCHED, YEARS_SEARCHED)


def tune_model(
    name: str,
    columns: list[str],
    train: pd.DataFrame,
    folds: list[tuple[np.ndarray, np.ndarray]],
    trials: int = TUNING_TRIALS,
) -> dict:
    """Settings with the best same-age C-index, searched with Optuna.

    Args:
        name: Algorithm key in MODELS.
        columns: Gold columns of the level.
        train: Train part of Gold.
        folds: Cross-validation folds of train.
        trials: Number of settings tried.

    Returns:
        The best settings.
    """
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=SPLIT_SEED))
    study.optimize(
        lambda trial: same_age_score(name, columns, train, folds, suggest_settings(trial, name)), n_trials=trials
    )
    return suggest_settings(optuna.trial.FixedTrial(study.best_params), name)


def suggest_settings(trial: optuna.trial.BaseTrial, name: str) -> dict:
    """One set of settings from the search space of a model.

    Args:
        trial: Optuna trial that proposes the values.
        name: Algorithm key in TUNING_SPACES.

    Returns:
        Setting → value.
    """
    suggest = {
        "int": trial.suggest_int,
        "float": trial.suggest_float,
        "log": lambda key, low, high: trial.suggest_float(key, low, high, log=True),
        "log_list": lambda key, low, high: [trial.suggest_float(key, low, high, log=True)],
    }
    return {key: suggest[kind](key, low, high) for key, (kind, low, high) in TUNING_SPACES[name].items()}


def same_age_score(
    name: str, columns: list[str], train: pd.DataFrame, folds: list[tuple[np.ndarray, np.ndarray]], settings: dict
) -> float:
    """Same-age C-index of some settings, on people left out of each fit.

    Args:
        name: Algorithm key in MODELS.
        columns: Gold columns of the level.
        train: Train part of Gold.
        folds: Cross-validation folds of train.
        settings: Values to try.

    Returns:
        The same-age C-index.
    """
    return same_age_c_index(cross_validate(name, columns, train, folds, settings)["by_age"])
