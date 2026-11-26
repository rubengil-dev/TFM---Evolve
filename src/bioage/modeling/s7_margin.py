"""ML Pipeline: Step 7 - Margin ± of the biological age and the data the app needs.

Each person of train is predicted by the model of the block that did not see them; the test is not used.

- `fit_margins`    : Margin and data needed of every level.
- `fit_blocks`     : One model per block of train, with its reference.
- `base_margin`    : Calibration in years with the blocks pooled, in two bands of risk.
- `hidden_table`   : How far the age moves with each number of values hidden.
- `most_missing`   : Most Routine values that can be missing.
- `fewest_extras`  : Fewest Extras that make their model better.
- `predict_blocks` : Risk and biological age, each person from the model that did not see them.
- `hide_random`    : Which values are hidden for each person.
- `same_age`       : C-index among people of the same age.

NOTE: Margin ± = √(base² + Routine values missing² + Extras missing²). Each part is saved per level in its bundle.
"""

# Imports
import logging

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from bioage.config.app import EXTRAS_LEVELS, MARGIN_REPEATS, MIN_GAIN, MOVE_SHARE, MOVE_YEARS
from bioage.config.model_levels import EXTRAS, LEVEL_COLUMNS, ROUTINE_LAB
from bioage.config.study import CALIBRATION_GROUPS, SPLIT_SEED
from bioage.modeling.s1_split import split_data
from bioage.modeling.s3_algorithms import build_pipeline, survival_target
from bioage.modeling.s4_biological_age import biological_age, fit_reference, risk_at_horizon
from bioage.modeling.s5_evaluation import c_index_by_group, calibration_in_years, same_age_c_index
from bioage.utils.features import age_groups

logger = logging.getLogger(__name__)

LOW_RISK_TENTHS = CALIBRATION_GROUPS // 2  # tenths of risk counted as low risk


def fit_margins(gold: pd.DataFrame) -> dict[str, dict]:
    """Margin and data needed of every level, from the blocks of train.

    Args:
        gold: Gold table.

    Returns:
        Level → low_risk_below, low_risk, rest, routine_missing and, with Extras, extras_known and min_extras.
    """
    train, _, folds = split_data(gold)
    blocks = {level: fit_blocks(train, folds, columns) for level, columns in LEVEL_COLUMNS.items()}
    margins = {level: base_margin(train, blocks[level]) for level in LEVEL_COLUMNS}
    logger.info("Margin: blocks fitted, base error measured")
    for level, with_extras in EXTRAS_LEVELS.items():
        people = train.dropna(subset=LEVEL_COLUMNS[level])
        routine = hidden_table(blocks[level], people, ROUTINE_LAB, range(len(ROUTINE_LAB) + 1))
        most = most_missing(routine)
        margins[level]["routine_missing"] = routine["median"].loc[:most].tolist()
        logger.info("Margin: %s, up to %d Routine values missing", level, most)

        people = train.dropna(subset=LEVEL_COLUMNS[with_extras])
        routine = hidden_table(blocks[with_extras], people, ROUTINE_LAB, range(most + 1))
        margins[with_extras]["routine_missing"] = routine["median"].tolist()
        extras = hidden_table(blocks[with_extras], people, EXTRAS, range(len(EXTRAS) + 1), blocks[level])
        margins[with_extras]["extras_known"] = extras["median"].drop(index=-1).iloc[::-1].tolist()
        margins[with_extras]["min_extras"] = fewest_extras(extras)
        logger.info("Margin: %s, from %d Extras", with_extras, margins[with_extras]["min_extras"])
    return margins


def fit_blocks(train: pd.DataFrame, folds: list[tuple[np.ndarray, np.ndarray]], columns: list[str]) -> list[tuple]:
    """One model per block, fitted on the other blocks, with its reference; the blocks run in parallel.

    Args:
        train: Train part of Gold.
        folds: (fit positions, validation positions) of each block.
        columns: Columns of the level.

    Returns:
        (people of the block, pipeline, reference) of each block.
    """

    def fit_block(fit_rows: np.ndarray, validation_rows: np.ndarray) -> tuple:
        fit = train.iloc[fit_rows]
        pipeline = build_pipeline("cox", columns).fit(fit, survival_target(fit))
        return train.index[validation_rows], pipeline, fit_reference(risk_at_horizon(pipeline, fit), fit)

    return Parallel(n_jobs=-1)(delayed(fit_block)(*fold) for fold in folds)


def base_margin(train: pd.DataFrame, blocks: list[tuple]) -> dict[str, float]:
    """Calibration in years with the blocks pooled: the mean of its size in the low and in the high tenths of risk.

    Args:
        train: Train part of Gold.
        blocks: Model of each block.

    Returns:
        Risk below which it is low, and the years of the low tenths and of the rest.
    """
    risk = predict_blocks(blocks, train)["risk"]
    reference = fit_reference(risk, train)
    age = biological_age(risk, train["sex"], reference)
    years = calibration_in_years(risk, age, train, reference)["years"].abs()
    return {
        "low_risk_below": float(risk.quantile(LOW_RISK_TENTHS / CALIBRATION_GROUPS)),
        "low_risk": float(years.iloc[:LOW_RISK_TENTHS].mean()),
        "rest": float(years.iloc[LOW_RISK_TENTHS:].mean()),
    }


def hidden_table(
    blocks: list[tuple], people: pd.DataFrame, columns: list[str], counts: range, without: list[tuple] | None = None
) -> pd.DataFrame:
    """How far the age moves from the one with every value, with each number of the columns hidden at random.

    Args:
        blocks: Model of each block.
        people: People with every value of the level.
        columns: Columns that can be hidden.
        counts: Numbers of columns hidden.
        without: Model of each block of the level without those columns; given, the C-index among people of the
            same age is added, with a row -1 for that level.

    Returns:
        Count hidden → median and MOVE_SHARE quantile (limit) of the years moved (and c_index),
        the mean of MARGIN_REPEATS draws.
    """
    target = predict_blocks(blocks, people)["age"]
    draws = [(count, repeat) for count in counts for repeat in range(MARGIN_REPEATS if 0 < count < len(columns) else 1)]
    hidden = [hide_random(people, columns, count, SPLIT_SEED + repeat) for count, repeat in draws]
    results = Parallel(n_jobs=-1)(delayed(predict_blocks)(blocks, people, mask) for mask in hidden)
    if without is not None:
        draws.append((-1, 0))
        results.append(predict_blocks(without, people))
    rows = []
    for (count, _), result in zip(draws, results, strict=True):
        moved = (result["age"] - target).abs()
        row = {"count": count, "median": moved.median(), "limit": moved.quantile(MOVE_SHARE)}
        if without is not None:
            row["c_index"] = same_age(result["risk"], people)
        rows.append(row)
    return pd.DataFrame(rows).groupby("count").mean().sort_index()


def most_missing(table: pd.DataFrame) -> int:
    """Most Routine values that can be missing: the age moves up to MOVE_YEARS for MOVE_SHARE of the people.

    Args:
        table: hidden_table of the Routine values.

    Returns:
        How many can be missing.
    """
    return int(table.index[table["limit"] <= MOVE_YEARS].max())


def fewest_extras(table: pd.DataFrame) -> int:
    """Fewest Extras known from which their model is always better than the one without them.

    Better: MIN_GAIN more of C-index among people of the same age and closer to the age with every Extra.

    Args:
        table: hidden_table of the Extras, with the row -1 of the level without them.

    Returns:
        Fewest Extras known.
    """
    without = table.loc[-1]
    hidden = table.drop(index=-1)
    is_better = (hidden["c_index"] - without["c_index"] >= MIN_GAIN) & (hidden["median"] < without["median"])
    better = pd.Series(is_better.to_numpy(), index=len(EXTRAS) - hidden.index).sort_index()  # by Extras known
    always = better[::-1].astype(int).cummin()[::-1].astype(bool)  # better there and with every one more known
    return int(always.index[always].min()) if always.any() else len(EXTRAS) + 1


def predict_blocks(blocks: list[tuple], data: pd.DataFrame, hidden: pd.DataFrame | None = None) -> pd.DataFrame:
    """Risk and biological age of each person, each from the model of the block that did not see them.

    Args:
        blocks: Model of each block.
        data: People to predict.
        hidden: Values to hide: True = missing.

    Returns:
        Risk and age of each person, in the order of data.
    """
    if hidden is not None:
        data = data.assign(**{column: data[column].mask(hidden[column]) for column in hidden})
    parts = []
    for people, pipeline, reference in blocks:
        members = data.loc[data.index.isin(people)]
        risk = risk_at_horizon(pipeline, members)
        age = biological_age(risk, members["sex"], reference)
        parts.append(pd.DataFrame({"risk": risk, "age": age}, index=members.index))
    return pd.concat(parts).loc[data.index]


def hide_random(data: pd.DataFrame, columns: list[str], count: int, seed: int) -> pd.DataFrame:
    """For each person, which of the columns are hidden: count of them, at random.

    Args:
        data: People.
        columns: Columns that can be hidden.
        count: How many are hidden for each person.
        seed: Seed of the draw.

    Returns:
        True = hidden.
    """
    order = np.random.default_rng(seed).random((len(data), len(columns))).argsort(axis=1).argsort(axis=1)
    return pd.DataFrame(order < count, index=data.index, columns=columns)


def same_age(risk: pd.Series, data: pd.DataFrame) -> float:
    """C-index among people of the same age group.

    Args:
        risk: Risk of each person.
        data: The same people.

    Returns:
        The C-index.
    """
    return same_age_c_index(c_index_by_group(risk, data, age_groups(data)))
