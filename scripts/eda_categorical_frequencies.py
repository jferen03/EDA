"""
Week 2 Exercise - Categorical column frequencies for the wildcat loans dataset.

Loads the cleaned loan CSV into a pandas DataFrame and, for each categorical
column (loan_purpose, loan_status, state), prints the count and percentage
of rows belonging to each unique value, sorted from most to least frequent.
Percentages are shown to one decimal place.

This is a standalone script - it loads its own copy of the data rather
than depending on the other eda_*.py scripts.

Run from anywhere inside the project - the data path is resolved relative
to this script's own location, so it doesn't depend on your current
working directory.
"""

from pathlib import Path

import pandas as pd

# Resolve the data file relative to this script, not the current working
# directory, so `python scripts/eda_categorical_frequencies.py` works from
# any location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"

CATEGORICAL_COLUMNS = ["loan_purpose", "loan_status", "state"]


def frequency_table(df: pd.DataFrame, column: str) -> pd.DataFrame:
    counts = df[column].value_counts(sort=True)  # already most-to-least frequent
    percentages = (counts / len(df) * 100).round(1)
    table = pd.DataFrame({"count": counts, "percent": percentages})
    table.index.name = column
    return table


def main() -> None:
    pd.set_option("display.max_rows", None)

    df = pd.read_csv(DATA_PATH)

    print(f"Loaded: {DATA_PATH}")
    print()

    for column in CATEGORICAL_COLUMNS:
        print(f"=== {column}: count and % of rows, most to least frequent ===")
        print(frequency_table(df, column))
        print()


if __name__ == "__main__":
    main()
