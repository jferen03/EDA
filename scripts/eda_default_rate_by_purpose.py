"""
Week 2 Exercise - Default rate by loan_purpose for the wildcat loans dataset.

Loads the cleaned loan CSV into a pandas DataFrame, groups by loan_purpose,
and for each purpose computes:
  - count of loans
  - number of loans with loan_status == "Default"
  - percentage of loans with loan_status == "Default"

Results are sorted by default percentage, descending.

This is a standalone script - it loads its own copy of the data rather
than depending on the other eda_*.py scripts.

Run from anywhere inside the project - the data path is resolved relative
to this script's own location, so it doesn't depend on your current
working directory.
"""

from pathlib import Path

import pandas as pd

# Resolve the data file relative to this script, not the current working
# directory, so `python scripts/eda_default_rate_by_purpose.py` works from
# any location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main() -> None:
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

    df = pd.read_csv(DATA_PATH)

    print(f"Loaded: {DATA_PATH}")
    print()

    df["is_default"] = df["loan_status"] == "Default"

    summary = df.groupby("loan_purpose").agg(
        count=("loan_purpose", "count"),
        default_count=("is_default", "sum"),
    )
    summary["default_percent"] = (summary["default_count"] / summary["count"] * 100).round(2)

    summary = summary.sort_values("default_percent", ascending=False)

    print("=== Default rate by loan_purpose (sorted by default %, descending) ===")
    print(summary)


if __name__ == "__main__":
    main()
