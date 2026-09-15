"""
Week 2 Exercise - Initial EDA inspection of the wildcat loans dataset.

Loads the cleaned loan CSV into a pandas DataFrame and prints:
  1. The shape of the DataFrame (rows, columns)
  2. Every column name with its data type
  3. The count of missing (null) values for every column

Run from anywhere inside the project - the data path is resolved relative
to this script's own location, so it doesn't depend on your current
working directory.
"""

from pathlib import Path

import pandas as pd

# Resolve the data file relative to this script, not the current working
# directory, so `python scripts/eda_inspect.py` works from any location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print(f"Loaded: {DATA_PATH}")
    print()

    print("=== Shape (rows, columns) ===")
    print(df.shape)
    print()

    print("=== Column names and data types ===")
    print(df.dtypes)
    print()

    print("=== Missing values per column ===")
    print(df.isnull().sum())


if __name__ == "__main__":
    main()
