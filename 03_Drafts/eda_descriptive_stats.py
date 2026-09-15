"""
Week 2 Exercise - Descriptive statistics for the wildcat loans dataset.

Loads the cleaned loan CSV into a pandas DataFrame and prints descriptive
statistics (count, mean, standard deviation, min, 25th percentile, median,
75th percentile, max) for every numeric column. All values, including loan
amounts, are rounded to two decimal places for readability.

This is a standalone script - it loads its own copy of the data rather
than depending on the other eda_*.py scripts.

Run from anywhere inside the project - the data path is resolved relative
to this script's own location, so it doesn't depend on your current
working directory.
"""

from pathlib import Path

import pandas as pd

# Resolve the data file relative to this script, not the current working
# directory, so `python scripts/eda_descriptive_stats.py` works from any
# location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"

# Rename count/50% for clearer, more explicit labels than pandas' defaults.
STAT_LABELS = {
    "count": "count",
    "mean": "mean",
    "std": "std_dev",
    "min": "min",
    "25%": "25th_percentile",
    "50%": "median",
    "75%": "75th_percentile",
    "max": "max",
}


def main() -> None:
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

    df = pd.read_csv(DATA_PATH)

    print(f"Loaded: {DATA_PATH}")
    print()

    numeric_df = df.select_dtypes(include="number")

    stats = numeric_df.describe().rename(index=STAT_LABELS)
    stats = stats.round(2)

    print("=== Descriptive statistics (numeric columns, rounded to 2 decimal places) ===")
    print(stats)


if __name__ == "__main__":
    main()
