"""Step 2, preprocessing pipeline, fitted only on train and reused by the app.

- Clip extremes → fill gaps → log, scale and encode → squared terms
"""

# Imports
from typing import Self

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from bioage.config.study import CATEGORICAL_LEVELS, CLIP_QUANTILES, LOG_VARIABLES, SQUARED_VARIABLES
from bioage.utils.features import age_groups


def build_preprocessor(columns: list[str]) -> Pipeline:
    """Unfitted pipeline for a list of Gold columns (age and sex among them).

    Args:
        columns: Gold columns the model uses.

    Returns:
        Preprocessing pipeline, not fitted yet.
    """
    categorical = [column for column in columns if column in CATEGORICAL_LEVELS]
    numeric = [column for column in columns if column not in CATEGORICAL_LEVELS]

    numeric_steps = Pipeline(
        [
            ("log", FunctionTransformer(log_skewed, feature_names_out="one-to-one")),
            ("scale", StandardScaler()),
        ]
    )
    encoder = OneHotEncoder(
        categories=[CATEGORICAL_LEVELS[column] for column in categorical],
        drop="first",
        sparse_output=False,
    )
    features = ColumnTransformer(
        [("numeric", numeric_steps, numeric), ("categorical", encoder, categorical)],
        verbose_feature_names_out=False,
    ).set_output(transform="pandas")

    return Pipeline(
        [
            ("clip", QuantileClipper(numeric)),
            ("fill_gaps", GroupImputer(columns)),
            ("features", features),
            ("squares", FunctionTransformer(add_squares)),
        ]
    )


class QuantileClipper(BaseEstimator, TransformerMixin):
    """Limits numeric columns to the quantiles of their observed values in train."""

    def __init__(self, columns: list[str]) -> None:
        """Keep the columns to clip.

        Args:
            columns: Numeric columns.
        """
        self.columns = columns

    def fit(self, data: pd.DataFrame, y: object = None) -> Self:
        """Learn the limits of each column from train.

        Args:
            data: Train people.
            y: Ignored, kept for the scikit-learn interface.

        Returns:
            The fitted transformer.
        """
        self.limits_ = data[self.columns].quantile(list(CLIP_QUANTILES))
        return self

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clip each column to its limits.

        Args:
            data: People to transform.

        Returns:
            The data with the columns clipped.
        """
        low, high = self.limits_.iloc[0], self.limits_.iloc[1]
        return data.assign(**{column: data[column].clip(low[column], high[column]) for column in self.columns})


class GroupImputer(BaseEstimator, TransformerMixin):
    """Fills gaps with the value of the person's sex and age group in train.

    - Median for numeric columns, most frequent answer for categorical ones
    - Overall value for groups without data
    """

    def __init__(self, columns: list[str]) -> None:
        """Keep the columns to fill.

        Args:
            columns: Columns of the model.
        """
        self.columns = columns

    def fit(self, data: pd.DataFrame, y: object = None) -> Self:
        """Learn the fill value of each column, per group and overall.

        Args:
            data: Train people.
            y: Ignored, kept for the scikit-learn interface.

        Returns:
            The fitted transformer.
        """
        keys = group_keys(data)
        self.by_group_ = {
            column: data[column].groupby(keys).agg(lambda values, column=column: fill_value(values, column))
            for column in self.columns
        }
        self.overall_ = {column: fill_value(data[column], column) for column in self.columns}
        return self

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Fill the gaps of each column.

        Args:
            data: People to transform.

        Returns:
            The columns of the model, without gaps.
        """
        keys = group_keys(data)
        filled = data[self.columns].copy()
        for column in self.columns:
            values = keys.map(self.by_group_[column]).fillna(self.overall_[column])
            filled[column] = filled[column].where(filled[column].notna(), values)
        return consistent_alcohol(filled)


def group_keys(data: pd.DataFrame) -> pd.Series:
    """Imputation group of each person: sex and age group, e.g. 'female|30-39'.

    Args:
        data: People with their age and sex.

    Returns:
        Group label of each person.
    """
    return data["sex"].astype(str) + "|" + age_groups(data).astype(str)


def fill_value(values: pd.Series, column: str) -> float | str:
    """Median of a numeric column or most frequent answer of a categorical one; missing if empty.

    Args:
        values: Observed values of the column.
        column: Name of the column.

    Returns:
        The value that fills its gaps.
    """
    if column not in CATEGORICAL_LEVELS:
        return values.median()
    modes = values.mode()
    return modes.iloc[0] if len(modes) else np.nan


def consistent_alcohol(filled: pd.DataFrame) -> pd.DataFrame:
    """No drinks per day for people who never drink.

    Args:
        filled: Columns already filled.

    Returns:
        The same table with consistent alcohol answers.
    """
    if {"alcohol_frequency", "alcohol_drinks"} <= set(filled.columns):
        filled.loc[filled["alcohol_frequency"] == "never", "alcohol_drinks"] = 0.0
    return filled


def log_skewed(numeric: pd.DataFrame) -> pd.DataFrame:
    """log1p of the skewed variables present in the data.

    Args:
        numeric: Numeric columns.

    Returns:
        The same columns, the skewed ones in logarithm.
    """
    return numeric.assign(**{column: np.log1p(numeric[column]) for column in LOG_VARIABLES if column in numeric})


def add_squares(features: pd.DataFrame) -> pd.DataFrame:
    """Squares of the scaled U-shaped variables present in the data.

    Args:
        features: Scaled features.

    Returns:
        The features plus one squared column per U-shaped variable.
    """
    return features.assign(
        **{f"{column}_squared": features[column] ** 2 for column in SQUARED_VARIABLES if column in features}
    )
