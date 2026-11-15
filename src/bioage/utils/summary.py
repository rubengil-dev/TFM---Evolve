"""
Summary printed after saving a data layer.
"""


def print_layer_summary(table, path):
    """Persons, deaths, columns and % with value per variable."""
    print(f"{len(table)} persons, {int(table['death'].sum())} deaths, {table.shape[1]} columns, saved to {path.name}\n")
    coverage = (table.notna().mean() * 100).round(0).astype(int)
    print(coverage.to_string())
