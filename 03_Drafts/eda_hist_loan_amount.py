"""
Week 2 Exercise - Histogram of loan_amount for the wildcat loans dataset.

Loads the cleaned loan CSV into a pandas DataFrame, builds a 30-bin
histogram of loan_amount, marks the mean and median with labeled vertical
lines, and saves the chart to outputs/hist_loan_amount.png.

This is a standalone script - it loads its own copy of the data rather
than depending on the other eda_*.py scripts.

Run from anywhere inside the project - all paths are resolved relative to
this script's own location, so it doesn't depend on your current working
directory.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Resolve paths relative to this script, not the current working directory,
# so `python scripts/eda_hist_loan_amount.py` works from any location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "hist_loan_amount.png"

# Colors (light-mode chart palette)
SURFACE = "#fcfcfb"
BAR_FILL = "#2a78d6"        # categorical slot 1 - blue
MEAN_COLOR = "#eb6834"      # categorical slot 2 - orange
MEDIAN_COLOR = "#4a3aa7"    # categorical slot 7 - violet
PRIMARY_INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
MUTED_INK = "#898781"
GRIDLINE = "#e1e0d9"
AXIS_LINE = "#c3c2b7"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    mean_val = df["loan_amount"].mean()
    median_val = df["loan_amount"].median()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

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
    fig.savefig(OUTPUT_PATH, facecolor=SURFACE)
    plt.close(fig)

    print(f"Loaded: {DATA_PATH}")
    print(f"Mean loan_amount:   ${mean_val:,.2f}")
    print(f"Median loan_amount: ${median_val:,.2f}")
    print(f"Histogram saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
