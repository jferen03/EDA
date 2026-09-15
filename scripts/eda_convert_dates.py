"""
Week 2 Exercise - Convert origination_date to a proper datetime type.

Loads the cleaned loan CSV into a pandas DataFrame, checks whether the
origination_date column is stored as a datetime type, and if it's still
text (object), converts it. Prints the before and after types so the
change is visible.

This is a standalone companion to eda_inspect.py - it loads its own copy
of the data rather than depending on that script.

Run from anywhere inside the project - the data path is resolved relative
to this script's own location, so it doesn't depend on your current
working directory.
"""

from pathlib import Path

import pandas as pd

# Resolve the data file relative to this script, not the current working
# directory, so `python scripts/eda_convert_dates.py` works from any location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print(f"Loaded: {DATA_PATH}")
    print()

    print("=== origination_date type check ===")
    before_dtype = df["origination_date"].dtype
    print(f"Before: origination_date is stored as {before_dtype}")

    if pd.api.types.is_datetime64_any_dtype(df["origination_date"]):
        print("origination_date is already a datetime type - no conversion needed.")
    else:
        df["origination_date"] = pd.to_datetime(df["origination_date"])
        after_dtype = df["origination_date"].dtype
        print(f"After:  origination_date converted to {after_dtype}")
        print("Converted origination_date from text (object) to datetime.")


if __name__ == "__main__":
    main()
