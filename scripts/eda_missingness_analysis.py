"""
Week 2 Exercise - Missingness analysis for the wildcat loans dataset.

Loads the cleaned loan CSV into a pandas DataFrame and:
  1. Prints the count and percentage of missing values for every column.
  2. For rows where credit_score is missing, compares the distribution of
     loan_status and loan_purpose against the same distributions across
     the full dataset - to help judge whether the missingness looks
     random or concentrated in a particular group.

This is a standalone script - it loads its own copy of the data rather
than depending on the other eda_*.py scripts.

Run from anywhere inside the project - the data path is resolved relative
to this script's own location, so it doesn't depend on your current
working directory.
"""

from pathlib import Path

import pandas as pd

# Resolve the data file relative to this script, not the current working
# directory, so `python scripts/eda_missingness_analysis.py` works from
# any location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"

pd.set_option("display.float_format", lambda x: f"{x:.2f}")


def compare_distribution(df: pd.DataFrame, missing_mask: pd.Series, column: str) -> pd.DataFrame:
    """Build a side-by-side % distribution table for `column`: full dataset
    vs. rows where credit_score is missing."""
    full_pct = df[column].value_counts(normalize=True, dropna=False) * 100
    missing_pct = df.loc[missing_mask, column].value_counts(normalize=True, dropna=False) * 100

    comparison = pd.DataFrame({
        "full_dataset_%": full_pct,
        "credit_score_missing_%": missing_pct,
    })
    # Rows that only appear in one side become NaN in the other - treat as 0%.
    comparison = comparison.fillna(0.0).sort_values("full_dataset_%", ascending=False)
    return comparison


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print(f"Loaded: {DATA_PATH}")
    print()

    print("=== Missing values per column (count and %) ===")
    missing_count = df.isnull().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)
    missing_summary = pd.DataFrame({
        "missing_count": missing_count,
        "missing_%": missing_pct,
    })
    print(missing_summary)
    print()

    missing_mask = df["credit_score"].isnull()
    n_missing = missing_mask.sum()
    print(f"=== credit_score missing: {n_missing} rows ({n_missing / len(df) * 100:.2f}% of dataset) ===")
    print()

    print("--- loan_status distribution: full dataset vs. credit_score-missing rows ---")
    print(compare_distribution(df, missing_mask, "loan_status"))
    print()

    print("--- loan_purpose distribution: full dataset vs. credit_score-missing rows ---")
    print(compare_distribution(df, missing_mask, "loan_purpose"))


if __name__ == "__main__":
    main()
