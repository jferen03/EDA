"""
Week 2 Exercise - Correlation matrix for the wildcat loans dataset.

Loads the cleaned loan CSV into a pandas DataFrame, computes the
correlation matrix for all numeric columns (excluding the loan_id and
borrower_id identifier columns), prints it rounded to two decimal places,
and identifies the three strongest correlations (by absolute value,
positive or negative, excluding a variable's correlation with itself).

This is a standalone script - it loads its own copy of the data rather
than depending on the other eda_*.py scripts.

Run from anywhere inside the project - the data path is resolved relative
to this script's own location, so it doesn't depend on your current
working directory.
"""

from pathlib import Path

import pandas as pd

# Resolve the data file relative to this script, not the current working
# directory, so `python scripts/eda_correlation_matrix.py` works from any
# location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"

ID_COLUMNS = ["loan_id", "borrower_id"]


def top_correlations(corr: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """Return the n strongest correlations by absolute value, one row per
    unique pair (no self-correlations, no A-B/B-A duplicates)."""
    # Use the upper triangle (excluding the diagonal) to get each pair once.
    mask = pd.DataFrame(
        [[i < j for j in range(len(corr.columns))] for i in range(len(corr.columns))],
        index=corr.index, columns=corr.columns,
    )
    stacked = corr.where(mask).stack()
    stacked = stacked.rename("correlation").reset_index()
    stacked.columns = ["variable_1", "variable_2", "correlation"]
    stacked["abs_correlation"] = stacked["correlation"].abs()
    return stacked.sort_values("abs_correlation", ascending=False).head(n)


def main() -> None:
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

    df = pd.read_csv(DATA_PATH)

    print(f"Loaded: {DATA_PATH}")
    print()

    numeric_df = df.select_dtypes(include="number").drop(columns=ID_COLUMNS)
    corr = numeric_df.corr().round(2)

    print("=== Correlation matrix (numeric columns, excluding loan_id/borrower_id) ===")
    print(corr)
    print()

    # Use the un-rounded correlations to rank ties fairly, then display rounded.
    full_corr = numeric_df.corr()
    top3 = top_correlations(full_corr, n=3)
    top3_display = top3.copy()
    top3_display["correlation"] = top3_display["correlation"].round(2)

    print("=== Three strongest correlations (by absolute value) ===")
    for _, row in top3_display.iterrows():
        print(f"{row['variable_1']} <-> {row['variable_2']}: {row['correlation']:+.2f}")


if __name__ == "__main__":
    main()
