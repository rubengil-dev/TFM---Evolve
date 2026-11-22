"""Helpers shared by the working notebooks of the model (analysis and display only).

- cox_weights: hazard ratio of each feature with its 95% interval
- variable_of: Gold variable behind a feature
- without: a list of columns minus some
- print_split_summary: people and deaths of train and test
- plot_calibration: predicted against observed risk
"""

# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from matplotlib.figure import Figure

from bioage.models.s2_preprocessing import build_preprocessor


def cox_weights(columns: list[str], data: pd.DataFrame, expected_signs: dict[str, str] | None = None) -> pd.DataFrame:
    """Cox fitted on the preprocessed columns of data → one row per feature.

    - hazard_ratio, low, high, p; clear: interval excludes 1
    - With expected_signs: variable, expected and contrary (clearly the other way)

    Args:
        columns: Gold columns the model uses.
        data: People to fit on, with the outcome columns.
        expected_signs: Feature → 'above' or 'below', the side of 1 its hazard ratio should fall on.

    Returns:
        Weights table, indexed by feature.
    """
    features = build_preprocessor(columns).fit_transform(data)
    fitted = CoxPHFitter().fit(features.join(data[["follow_up_months", "death"]]), "follow_up_months", "death").summary
    weights = pd.DataFrame(
        {
            "hazard_ratio": fitted["exp(coef)"],
            "low": fitted["exp(coef) lower 95%"],
            "high": fitted["exp(coef) upper 95%"],
            "p": fitted["p"],
        }
    )
    weights["clear"] = (weights["low"] > 1) | (weights["high"] < 1)
    if expected_signs is not None:
        weights = add_signs(weights, columns, expected_signs)
    return weights


def add_signs(weights: pd.DataFrame, columns: list[str], expected_signs: dict[str, str]) -> pd.DataFrame:
    """Variable of each feature, its expected sign and whether the fit clearly goes the other way.

    Args:
        weights: Weights table, indexed by feature.
        columns: Gold columns the model uses.
        expected_signs: Feature → 'above' or 'below'.

    Returns:
        The same table with the variable, expected and contrary columns.
    """
    weights["variable"] = [variable_of(feature, columns) for feature in weights.index]
    weights["expected"] = pd.Series(expected_signs).reindex(weights.index)
    weights["contrary"] = ((weights["expected"] == "above") & (weights["high"] < 1)) | (
        (weights["expected"] == "below") & (weights["low"] > 1)
    )
    return weights


def variable_of(feature: str, columns: list[str]) -> str:
    """Gold variable behind a feature, the longest match: 'smoking_current' → 'smoking'.

    Args:
        feature: Name of a preprocessed feature.
        columns: Gold columns the model uses.

    Returns:
        Name of the Gold variable.
    """
    return next(
        column
        for column in sorted(columns, key=len, reverse=True)
        if feature == column or feature.startswith(column + "_")
    )


def without(columns: list[str], removed: list[str]) -> list[str]:
    """Columns in their order, minus those in removed.

    Args:
        columns: Starting list.
        removed: Columns to leave out.

    Returns:
        The remaining columns.
    """
    return [column for column in columns if column not in removed]


def print_split_summary(train: pd.DataFrame, test: pd.DataFrame, folds: list[tuple[np.ndarray, np.ndarray]]) -> None:
    """Print the people and deaths per part and per cycle.

    Args:
        train: Train part of Gold.
        test: Test part of Gold.
        folds: Cross-validation folds of train.
    """
    parts = pd.concat([train.assign(part="train"), test.assign(part="test")])
    summary = parts.groupby(["cycle", "part"])["death"].agg(people="size", deaths="sum").unstack("part")
    print(summary.astype(int).to_string())
    print(f"train: {len(train)} people, {int(train['death'].sum())} deaths")
    print(f"test:  {len(test)} people, {int(test['death'].sum())} deaths")
    print(f"folds: {[len(validation) for _, validation in folds]} people in each validation part")


def plot_calibration(details: dict[str, dict]) -> Figure:
    """One panel per model: predicted against observed risk, diagonal = perfect.

    Args:
        details: Detail of each model, from evaluate_level.

    Returns:
        The figure.
    """
    figure, axes = plt.subplots(
        1, len(details), figsize=(3.2 * len(details), 3.4), sharex=True, sharey=True, squeeze=False
    )
    for axis, (name, detail) in zip(axes[0], details.items(), strict=True):
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
