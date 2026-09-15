"""
Week 2 Exercise - Box plot of interest_rate by loan_status for the wildcat
loans dataset.

Loads the cleaned loan CSV into a pandas DataFrame, builds a horizontal box
plot comparing the distribution of interest_rate across the four
loan_status categories (Current, Paid Off, Delinquent, Default), and saves
the chart to outputs/box_interest_by_status.png.

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
# so `python scripts/eda_box_interest_by_status.py` works from any location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "box_interest_by_status.png"

STATUS_ORDER = ["Current", "Paid Off", "Delinquent", "Default"]

# Colors (light-mode chart palette, one categorical hue per category)
SURFACE = "#fcfcfb"
STATUS_COLORS = {
    "Current": "#2a78d6",     # blue
    "Paid Off": "#1baf7a",    # aqua
    "Delinquent": "#eda100",  # yellow
    "Default": "#e34948",     # red
}
PRIMARY_INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
MUTED_INK = "#898781"
GRIDLINE = "#e1e0d9"
AXIS_LINE = "#c3c2b7"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    # Build the data in the display order (Default at top -> Current at
    # bottom, since matplotlib's horizontal boxplot draws position 1 lowest).
    plot_order = list(reversed(STATUS_ORDER))
    data = [df.loc[df["loan_status"] == status, "interest_rate"] for status in plot_order]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

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
    fig.savefig(OUTPUT_PATH, facecolor=SURFACE)
    plt.close(fig)

    print(f"Loaded: {DATA_PATH}")
    print()
    print("=== interest_rate summary by loan_status ===")
    print(df.groupby("loan_status")["interest_rate"].describe().loc[STATUS_ORDER].round(2))
    print()
    print(f"Box plot saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
