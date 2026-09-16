# Wildcat Capital — Combined EDA Script

This document mirrors `combination_of_files.py`, which combines every standalone
exploratory data analysis (EDA) script in `03_Drafts/` into a single runnable
script, in pipeline order. It is a code reference, not a results/output report —
for the printed output and saved charts, run the `.py` file.

**Source scripts combined (11 total):**

1. `eda_inspect.py` — shape, dtypes, missing value counts
2. `eda_convert_dates.py` — convert `origination_date` to datetime
3. `eda_descriptive_stats.py` — descriptive statistics (numeric columns)
4. `eda_missingness_analysis.py` — missingness detail + comparison
5. `eda_categorical_frequencies.py` — category counts/percentages
6. `eda_groupby_loan_status.py` — summary stats by `loan_status`
7. `eda_correlation_matrix.py` — correlation matrix + top 3 pairs
8. `eda_hist_loan_amount.py` — histogram of `loan_amount` (chart)
9. `eda_box_interest_by_status.py` — box plot of `interest_rate` (chart)
10. `eda_scatter_credit_rate.py` — scatter plot, credit vs. rate (chart)
11. `eda_default_rate_by_purpose.py` — default rate by `loan_purpose`

`wildcat_loans_analysis.py` is intentionally excluded from this combination.

The CSV is loaded once and shared across all sections (each original script
loaded its own copy). Chart color constants duplicated across the three
plotting scripts (histogram, box plot, scatter plot) have been consolidated
into one shared palette below. Every section's logic and printed output is
otherwise unchanged from its original script.

---

## Imports and Shared Paths

```python
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
HIST_OUTPUT_PATH = OUTPUTS_DIR / "hist_loan_amount.png"
BOX_OUTPUT_PATH = OUTPUTS_DIR / "box_interest_by_status.png"
SCATTER_OUTPUT_PATH = OUTPUTS_DIR / "scatter_credit_rate.png"
```

## Shared Constants

```python
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

CATEGORICAL_COLUMNS = ["loan_purpose", "loan_status", "state"]
ID_COLUMNS = ["loan_id", "borrower_id"]
STATUS_ORDER = ["Current", "Paid Off", "Delinquent", "Default"]

SURFACE = "#fcfcfb"
BAR_FILL = "#2a78d6"        # categorical slot 1 - blue
MEAN_COLOR = "#eb6834"      # categorical slot 2 - orange
MEDIAN_COLOR = "#4a3aa7"    # categorical slot 7 - violet
PRIMARY_INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
MUTED_INK = "#898781"
GRIDLINE = "#e1e0d9"
AXIS_LINE = "#c3c2b7"
STATUS_COLORS = {
    "Current": "#2a78d6",     # blue
    "Paid Off": "#1baf7a",    # aqua
    "Delinquent": "#eda100",  # yellow
    "Default": "#e34948",     # red
}
```

---

## 1. Initial Inspection (`eda_inspect.py`)

```python
def section_01_inspect(df: pd.DataFrame) -> None:
    print("=== Shape (rows, columns) ===")
    print(df.shape)
    print()

    print("=== Column names and data types ===")
    print(df.dtypes)
    print()

    print("=== Missing values per column ===")
    print(df.isnull().sum())
    print()
```

## 2. Convert `origination_date` to Datetime (`eda_convert_dates.py`)

```python
def section_02_convert_dates(df: pd.DataFrame) -> None:
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
    print()
```

## 3. Descriptive Statistics (`eda_descriptive_stats.py`)

```python
def section_03_descriptive_stats(df: pd.DataFrame) -> None:
    numeric_df = df.select_dtypes(include="number")
    stats = numeric_df.describe().rename(index=STAT_LABELS)
    stats = stats.round(2)

    print("=== Descriptive statistics (numeric columns, rounded to 2 decimal places) ===")
    print(stats)
    print()
```

## 4. Missingness Analysis (`eda_missingness_analysis.py`)

```python
def compare_distribution(df: pd.DataFrame, missing_mask: pd.Series, column: str) -> pd.DataFrame:
    """Build a side-by-side % distribution table for `column`: full dataset
    vs. rows where credit_score is missing."""
    full_pct = df[column].value_counts(normalize=True, dropna=False) * 100
    missing_pct = df.loc[missing_mask, column].value_counts(normalize=True, dropna=False) * 100

    comparison = pd.DataFrame({
        "full_dataset_%": full_pct,
        "credit_score_missing_%": missing_pct,
    })
    comparison = comparison.fillna(0.0).sort_values("full_dataset_%", ascending=False)
    return comparison


def section_04_missingness_analysis(df: pd.DataFrame) -> None:
    with pd.option_context("display.float_format", lambda x: f"{x:.2f}"):
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
    print()
```

## 5. Categorical Frequencies (`eda_categorical_frequencies.py`)

```python
def frequency_table(df: pd.DataFrame, column: str) -> pd.DataFrame:
    counts = df[column].value_counts(sort=True)  # already most-to-least frequent
    percentages = (counts / len(df) * 100).round(1)
    table = pd.DataFrame({"count": counts, "percent": percentages})
    table.index.name = column
    return table


def section_05_categorical_frequencies(df: pd.DataFrame) -> None:
    for column in CATEGORICAL_COLUMNS:
        print(f"=== {column}: count and % of rows, most to least frequent ===")
        print(frequency_table(df, column))
        print()
```

## 6. Group-by Summary by `loan_status` (`eda_groupby_loan_status.py`)

```python
def section_06_groupby_loan_status(df: pd.DataFrame) -> None:
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
    print()
```

## 7. Correlation Matrix (`eda_correlation_matrix.py`)

```python
def top_correlations(corr: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """Return the n strongest correlations by absolute value, one row per
    unique pair (no self-correlations, no A-B/B-A duplicates)."""
    mask = pd.DataFrame(
        [[i < j for j in range(len(corr.columns))] for i in range(len(corr.columns))],
        index=corr.index, columns=corr.columns,
    )
    stacked = corr.where(mask).stack()
    stacked = stacked.rename("correlation").reset_index()
    stacked.columns = ["variable_1", "variable_2", "correlation"]
    stacked["abs_correlation"] = stacked["correlation"].abs()
    return stacked.sort_values("abs_correlation", ascending=False).head(n)


def section_07_correlation_matrix(df: pd.DataFrame) -> None:
    numeric_df = df.select_dtypes(include="number").drop(columns=ID_COLUMNS)
    corr = numeric_df.corr().round(2)

    print("=== Correlation matrix (numeric columns, excluding loan_id/borrower_id) ===")
    print(corr)
    print()

    full_corr = numeric_df.corr()
    top3 = top_correlations(full_corr, n=3)
    top3_display = top3.copy()
    top3_display["correlation"] = top3_display["correlation"].round(2)

    print("=== Three strongest correlations (by absolute value) ===")
    for _, row in top3_display.iterrows():
        print(f"{row['variable_1']} <-> {row['variable_2']}: {row['correlation']:+.2f}")
    print()
```

## 8. Histogram: `loan_amount` (`eda_hist_loan_amount.py`)

```python
def section_08_hist_loan_amount(df: pd.DataFrame) -> None:
    mean_val = df["loan_amount"].mean()
    median_val = df["loan_amount"].median()

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    ax.hist(
        df["loan_amount"],
        bins=30,
        color=BAR_FILL,
        edgecolor=SURFACE,
        linewidth=0.6,
        alpha=0.9,
        zorder=2,
    )

    ax.axvline(mean_val, color=MEAN_COLOR, linestyle="--", linewidth=2, zorder=3)
    ax.axvline(median_val, color=MEDIAN_COLOR, linestyle="--", linewidth=2, zorder=3)

    y_top = ax.get_ylim()[1]
    ax.text(
        mean_val, y_top * 0.97, f"  Mean: ${mean_val:,.2f}",
        color=MEAN_COLOR, fontsize=10, fontweight="bold",
        ha="left", va="top",
    )
    ax.text(
        median_val, y_top * 0.88, f"  Median: ${median_val:,.2f}",
        color=MEDIAN_COLOR, fontsize=10, fontweight="bold",
        ha="left", va="top",
    )

    ax.set_title(
        "Distribution of Loan Amounts — Wildcat Capital Portfolio",
        fontsize=14, fontweight="bold", color=PRIMARY_INK, pad=14,
    )
    ax.set_xlabel("Loan Amount ($)", fontsize=11, color=SECONDARY_INK)
    ax.set_ylabel("Number of Loans", fontsize=11, color=SECONDARY_INK)

    ax.xaxis.set_major_formatter(lambda x, pos: f"${x:,.0f}")
    ax.tick_params(colors=MUTED_INK, labelsize=9)

    ax.grid(axis="y", color=GRIDLINE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(AXIS_LINE)

    fig.tight_layout()
    fig.savefig(HIST_OUTPUT_PATH, facecolor=SURFACE)
    plt.close(fig)

    print(f"Mean loan_amount:   ${mean_val:,.2f}")
    print(f"Median loan_amount: ${median_val:,.2f}")
    print(f"Histogram saved to: {HIST_OUTPUT_PATH}")
    print()
```

## 9. Box Plot: `interest_rate` by `loan_status` (`eda_box_interest_by_status.py`)

```python
def section_09_box_interest_by_status(df: pd.DataFrame) -> None:
    # Build the data in the display order (Default at top -> Current at
    # bottom, since matplotlib's horizontal boxplot draws position 1 lowest).
    plot_order = list(reversed(STATUS_ORDER))
    data = [df.loc[df["loan_status"] == status, "interest_rate"] for status in plot_order]

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    box = ax.boxplot(
        data,
        vert=False,
        patch_artist=True,
        tick_labels=plot_order,
        widths=0.6,
        medianprops={"color": PRIMARY_INK, "linewidth": 2},
        whiskerprops={"color": AXIS_LINE, "linewidth": 1.2},
        capprops={"color": AXIS_LINE, "linewidth": 1.2},
        flierprops={
            "marker": "o", "markersize": 4,
            "markerfacecolor": MUTED_INK, "markeredgecolor": "none", "alpha": 0.6,
        },
        zorder=2,
    )

    for patch, status in zip(box["boxes"], plot_order):
        patch.set_facecolor(STATUS_COLORS[status])
        patch.set_edgecolor(SURFACE)
        patch.set_linewidth(1.2)
        patch.set_alpha(0.9)

    ax.set_title(
        "Interest Rate by Loan Status",
        fontsize=14, fontweight="bold", color=PRIMARY_INK, pad=14,
    )
    ax.set_xlabel("Interest Rate (%)", fontsize=11, color=SECONDARY_INK)
    ax.set_ylabel("Loan Status", fontsize=11, color=SECONDARY_INK)

    ax.xaxis.set_major_formatter(lambda x, pos: f"{x:.0f}%")
    ax.tick_params(colors=MUTED_INK, labelsize=10)

    ax.grid(axis="x", color=GRIDLINE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(AXIS_LINE)

    fig.tight_layout()
    fig.savefig(BOX_OUTPUT_PATH, facecolor=SURFACE)
    plt.close(fig)

    print("=== interest_rate summary by loan_status ===")
    print(df.groupby("loan_status")["interest_rate"].describe().loc[STATUS_ORDER].round(2))
    print()
    print(f"Box plot saved to: {BOX_OUTPUT_PATH}")
    print()
```

## 10. Scatter Plot: `credit_score` vs. `interest_rate` (`eda_scatter_credit_rate.py`)

```python
def section_10_scatter_credit_rate(df: pd.DataFrame) -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    # Plot Current first (largest group) so smaller, more critical groups
    # (Delinquent, Default) render on top and stay visible.
    plot_order = ["Current", "Paid Off", "Delinquent", "Default"]
    for status in plot_order:
        subset = df[df["loan_status"] == status]
        ax.scatter(
            subset["credit_score"],
            subset["interest_rate"],
            s=22,
            color=STATUS_COLORS[status],
            alpha=0.65,
            edgecolors="none",
            label=status,
            zorder=3,
        )

    ax.set_title(
        "Credit Score vs. Interest Rate by Loan Status",
        fontsize=14, fontweight="bold", color=PRIMARY_INK, pad=14,
    )
    ax.set_xlabel("Credit Score", fontsize=11, color=SECONDARY_INK)
    ax.set_ylabel("Interest Rate (%)", fontsize=11, color=SECONDARY_INK)

    ax.yaxis.set_major_formatter(lambda y, pos: f"{y:.0f}%")
    ax.tick_params(colors=MUTED_INK, labelsize=9)

    ax.grid(color=GRIDLINE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(AXIS_LINE)

    legend = ax.legend(
        title="Loan Status", loc="upper right", frameon=True,
        facecolor=SURFACE, edgecolor=AXIS_LINE, fontsize=9, title_fontsize=9,
    )
    legend.get_title().set_color(PRIMARY_INK)
    for text in legend.get_texts():
        text.set_color(SECONDARY_INK)

    fig.tight_layout()
    fig.savefig(SCATTER_OUTPUT_PATH, facecolor=SURFACE)
    plt.close(fig)

    print(f"Scatter plot saved to: {SCATTER_OUTPUT_PATH}")
    print()
```

## 11. Default Rate by `loan_purpose` (`eda_default_rate_by_purpose.py`)

```python
def section_11_default_rate_by_purpose(df: pd.DataFrame) -> None:
    # Work on a copy so this last section doesn't mutate the shared df.
    df = df.copy()
    df["is_default"] = df["loan_status"] == "Default"

    summary = df.groupby("loan_purpose").agg(
        count=("loan_purpose", "count"),
        default_count=("is_default", "sum"),
    )
    summary["default_percent"] = (summary["default_count"] / summary["count"] * 100).round(2)

    summary = summary.sort_values("default_percent", ascending=False)

    print("=== Default rate by loan_purpose (sorted by default %, descending) ===")
    print(summary)
    print()
```

## Entry Point

Runs all 11 sections in pipeline order against one shared load of the CSV,
and prints everything to the screen.

```python
def main() -> None:
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_rows", None)

    df = pd.read_csv(DATA_PATH)

    print("WILDCAT CAPITAL — COMBINED EDA ANALYSIS")
    print(f"Loaded: {DATA_PATH}")
    print()

    section_01_inspect(df)
    section_02_convert_dates(df)
    section_03_descriptive_stats(df)
    section_04_missingness_analysis(df)
    section_05_categorical_frequencies(df)
    section_06_groupby_loan_status(df)
    section_07_correlation_matrix(df)
    section_08_hist_loan_amount(df)
    section_09_box_interest_by_status(df)
    section_10_scatter_credit_rate(df)
    section_11_default_rate_by_purpose(df)

    print("############################################################")
    print("# DONE — all 11 sections complete")
    print("############################################################")


if __name__ == "__main__":
    main()
```
