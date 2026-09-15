"""
Week 2 Exercise - Group-by summary of the wildcat loans dataset by loan_status.

Loads the cleaned loan CSV into a pandas DataFrame, groups by loan_status,
and for each status computes:
  - count of loans
  - mean loan_amount (rounded to 2 decimal places)
  - mean interest_rate (rounded to 4 decimal places)
  - mean credit_score (rounded to 1 decimal place, nulls excluded)
  - mean debt_to_income_ratio (rounded to 4 decimal places)

Results are sorted by count, descending.

This is a standalone script - it loads its own copy of the data rather
than depending on the other eda_*.py scripts.

Run from anywhere inside the project - the data path is resolved relative
to this script's own location, so it doesn't depend on your current
working directory.
"""

from pathlib import Path

import pandas as pd

# Resolve the data file relative to this script, not the current working
# directory, so `python scripts/eda_groupby_loan_status.py` works from any
# location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main() -> None:
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

    df = pd.read_csv(DATA_PATH)

    print(f"Loaded: {DATA_PATH}")
    print()

    # groupby().mean() skips NaN by default, so credit_score's mean already
    # excludes the missing values.
    summary = df.groupby("loan_status").agg(
        count=("loan_status", "count"),
        mean_loan_amount=("loan_amount", "mean"),
        mean_interest_rate=("interest_rate", "mean"),
        mean_credit_score=("credit_score", "mean"),
        mean_debt_to_income_ratio=("debt_to_income_ratio", "mean"),
    )

    summary["mean_loan_amount"] = summary["mean_loan_amount"].round(2)
    summary["mean_interest_rate"] = summary["mean_interest_rate"].round(4)
    summary["mean_credit_score"] = summary["mean_credit_score"].round(1)
    summary["mean_debt_to_income_ratio"] = summary["mean_debt_to_income_ratio"].round(4)

    summary = summary.sort_values("count", ascending=False)

    print("=== loan_status summary (sorted by count, descending) ===")
    print(summary)


if __name__ == "__main__":
    main()
