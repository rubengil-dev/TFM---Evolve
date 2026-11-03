"""
Gold validation before saving:
    - Blocking (error → Gold not saved): structure, size, coverage, required columns, outcome,
      population, answers and plausible ranges
    - Warning only: consistency between variables
"""

# Imports
import pandas as pd

from src.config.column_roles import DERIVED_FEATURES, ID_COLUMNS, OUTCOME_COLUMNS, SILVER_PREDICTORS
from src.config.plausible_ranges import PLAUSIBLE_RANGES
from src.config.sources import CYCLES
from src.config.study import AGE_MAX, AGE_MIN, FOLLOW_UP_MIN
from src.config.validation_rules import (
    BMI_TOLERANCE, CATEGORIES, LOWER_THAN, MAX_FOLLOW_UP, MIN_COVERAGE, MIN_COVERAGE_PARTIAL, MIN_DEATHS,
    MIN_PERSONS, MIN_PERSONS_PER_CYCLE, PARTIAL_COVERAGE, REQUIRED,
)
from src.utils.nhanes import cycle_label


def validate_gold(gold):
    """Every check on Gold: errors → ValueError, warnings → printed."""
    errors = check_structure(gold)
    if not errors:
        errors = (
            check_size(gold) + check_coverage(gold) + check_required(gold) + check_outcome(gold)
            + check_population(gold) + check_categories(gold) + check_ranges(gold)
        )
    warnings = [] if errors else check_consistency(gold)
    print_report(errors, warnings)
    if errors:
        raise ValueError(f"Gold validation failed with {len(errors)} errors, Gold not saved")


def check_structure(gold):
    """Exactly the expected columns; text columns as text, the rest as numbers."""
    expected = ID_COLUMNS + OUTCOME_COLUMNS + SILVER_PREDICTORS + DERIVED_FEATURES
    errors = [f"missing column: {column}" for column in expected if column not in gold]
    errors += [f"unexpected column: {column}" for column in gold if column not in expected]
    text = ["cycle"] + list(CATEGORIES)
    for column in gold.columns.intersection(expected):
        is_number = pd.api.types.is_numeric_dtype(gold[column])
        if is_number == (column in text):
            errors.append(f"{column}: should be {'text' if column in text else 'numeric'}")
    return errors


def check_size(gold):
    """At least MIN_PERSONS persons, MIN_PERSONS_PER_CYCLE in each cycle and MIN_DEATHS deaths."""
    errors = []
    if len(gold) < MIN_PERSONS:
        errors.append(f"{len(gold)} persons, minimum {MIN_PERSONS}")
    per_cycle = gold["cycle"].value_counts()
    for cycle in [cycle_label(year) for year in CYCLES]:
        persons = per_cycle.get(cycle, 0)
        if persons < MIN_PERSONS_PER_CYCLE:
            errors.append(f"cycle {cycle}: {persons} persons, minimum {MIN_PERSONS_PER_CYCLE}")
    deaths = int(gold["death"].sum())
    if deaths < MIN_DEATHS:
        errors.append(f"{deaths} deaths, minimum {MIN_DEATHS}")
    return errors


def check_coverage(gold):
    """% with value ≥ MIN_COVERAGE (MIN_COVERAGE_PARTIAL for PARTIAL_COVERAGE)."""
    coverage = gold.notna().mean() * 100
    errors = []
    for column, percent in coverage.items():
        minimum = MIN_COVERAGE_PARTIAL if column in PARTIAL_COVERAGE else MIN_COVERAGE
        if percent < minimum:
            errors.append(f"{column}: {percent:.0f}% with value, minimum {minimum}%")
    return errors


def check_required(gold):
    """No missing values in REQUIRED; one row per person."""
    errors = [f"{column}: {n} missing" for column, n in gold[REQUIRED].isna().sum().items() if n]
    if gold["seqn"].duplicated().any():
        errors.append(f"seqn: {gold['seqn'].duplicated().sum()} repeated")
    return errors


def check_outcome(gold):
    """death only 0 / 1; follow-up between FOLLOW_UP_MIN and MAX_FOLLOW_UP; survey weight > 0."""
    errors = []
    if not gold["death"].isin([0, 1]).all():
        errors.append("death: values other than 0 / 1")
    errors += out_of_bounds(gold, "follow_up_months", FOLLOW_UP_MIN, MAX_FOLLOW_UP)
    if (gold["weight_exam"] <= 0).any():
        errors.append(f"weight_exam: {(gold['weight_exam'] <= 0).sum()} not above 0")
    return errors


def check_population(gold):
    """Age between AGE_MIN and AGE_MAX; cycle one of CYCLES."""
    errors = out_of_bounds(gold, "age", AGE_MIN, AGE_MAX)
    unknown = ~gold["cycle"].isin([cycle_label(year) for year in CYCLES])
    if unknown.any():
        errors.append(f"cycle: {unknown.sum()} unknown")
    return errors


def check_categories(gold):
    """Text answers only from CATEGORIES (or missing)."""
    errors = []
    for column, allowed in CATEGORIES.items():
        unknown = gold[column].dropna()
        unknown = unknown[~unknown.isin(allowed)].unique()
        if len(unknown):
            errors.append(f"{column}: unknown answers {list(unknown)}")
    return errors


def check_ranges(gold):
    """Every value inside the PLAUSIBLE_RANGES limits (Silver clean blanks the rest)."""
    errors = []
    for variable, (_, _, (low, high), _) in PLAUSIBLE_RANGES.items():
        errors += out_of_bounds(gold, variable, low, high)
    return errors


def check_consistency(gold):
    """Each LOWER_THAN pair in order; bmi matching weight / height² (± BMI_TOLERANCE)."""
    warnings = []
    for lower, higher in LOWER_THAN:
        wrong = (gold[lower] >= gold[higher]).sum()
        if wrong:
            warnings.append(f"{lower} not below {higher}: {wrong} persons")
    bmi = gold["weight"] / (gold["height"] / 100) ** 2
    wrong = ((bmi - gold["bmi"]).abs() > BMI_TOLERANCE).sum()
    if wrong:
        warnings.append(f"bmi not matching weight / height^2: {wrong} persons")
    return warnings


def out_of_bounds(gold, column, low, high):
    """Error line if any value of column is outside [low, high] (missing values ignored)."""
    outside = gold[column].notna() & ~gold[column].between(low, high)
    return [f"{column}: {outside.sum()} values outside {low}-{high}"] if outside.any() else []


def print_report(errors, warnings):
    """Errors and warnings, or OK."""
    print("Gold validation:")
    for line in errors:
        print(f"    ERROR   {line}")
    for line in warnings:
        print(f"    WARNING {line}")
    if not errors and not warnings:
        print("    OK")
    print()
