"""
Step 2, preprocessing pipeline, fitted only on train and reused by the app:
    - Clip extremes → fill gaps → log, scale and encode → squared terms
"""

# Imports
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from src.config.study import CATEGORICAL_LEVELS, CLIP_QUANTILES, LOG_VARIABLES, SQUARED_VARIABLES
from src.utils.features import age_groups


def build_preprocessor(columns):
    """Unfitted pipeline for a list of Gold columns (age and sex among them)."""
    categorical = [column for column in columns if column in CATEGORICAL_LEVELS]
    numeric = [column for column in columns if column not in CATEGORICAL_LEVELS]

    numeric_steps = Pipeline([
        ("log", FunctionTransformer(log_skewed, feature_names_out="one-to-one")),
        ("scale", StandardScaler()),
    ])
    encoder = OneHotEncoder(
        categories=[CATEGORICAL_LEVELS[column] for column in categorical],
        drop="first",
        sparse_output=False,
    )
    features = ColumnTransformer(
        [("numeric", numeric_steps, numeric), ("categorical", encoder, categorical)],
        verbose_feature_names_out=False,
    ).set_output(transform="pandas")

    return Pipeline([
        ("clip", QuantileClipper(numeric)),
        ("fill_gaps", GroupImputer(columns)),
        ("features", features),
        ("squares", FunctionTransformer(add_squares)),
    ])


class QuantileClipper(BaseEstimator, TransformerMixin):
    """Limits numeric columns to the quantiles of their observed values in train."""

    def __init__(self, columns):
        self.columns = columns

    def fit(self, data, y=None):
        self.limits_ = data[self.columns].quantile(list(CLIP_QUANTILES))
        return self

    def transform(self, data):
        low, high = self.limits_.iloc[0], self.limits_.iloc[1]
        return data.assign(**{column: data[column].clip(low[column], high[column]) for column in self.columns})


class GroupImputer(BaseEstimator, TransformerMixin):
    """
    Fills gaps with the value of the person's sex and age group in train:
        - Median for numeric columns, most frequent answer for categorical ones
        - Overall value for groups without data
    """

    def __init__(self, columns):
        self.columns = columns

    def fit(self, data, y=None):
        keys = group_keys(data)
        self.by_group_ = {column: data[column].groupby(keys).agg(fill_value) for column in self.columns}
        self.overall_ = {column: fill_value(data[column]) for column in self.columns}
        return self

    def transform(self, data):
        keys = group_keys(data)
        filled = data[self.columns].copy()
        for column in self.columns:
            values = keys.map(self.by_group_[column]).fillna(self.overall_[column])
            filled[column] = filled[column].where(filled[column].notna(), values)
        return consistent_alcohol(filled)


def group_keys(data):
    """Imputation group of each person: sex and age group, e.g. 'female|30-39'."""
    return data["sex"].astype(str) + "|" + age_groups(data).astype(str)


def fill_value(values):
    """Median of a numeric column or most frequent answer of a categorical one; missing if empty."""
    if values.name not in CATEGORICAL_LEVELS:
        return values.median()
    modes = values.mode()
    return modes.iloc[0] if len(modes) else np.nan


def consistent_alcohol(filled):
    """No drinks per day for people who never drink."""
    if {"alcohol_frequency", "alcohol_drinks"} <= set(filled.columns):
        filled.loc[filled["alcohol_frequency"] == "never", "alcohol_drinks"] = 0.0
    return filled


def log_skewed(numeric):
    """log1p of the skewed variables present in the data."""
    return numeric.assign(**{column: np.log1p(numeric[column]) for column in LOG_VARIABLES if column in numeric})


def add_squares(features):
    """Squares of the scaled U-shaped variables present in the data."""
    return features.assign(**{f"{column}_squared": features[column] ** 2 for column in SQUARED_VARIABLES if column in features})
