"""
Week 2 Exercise - Scatter plot of credit_score vs. interest_rate, colored by
loan_status, for the wildcat loans dataset.

Loads the cleaned loan CSV into a pandas DataFrame, builds a scatter plot
with credit_score on the x-axis and interest_rate on the y-axis, colors
each point by loan_status (Current, Paid Off, Delinquent, Default), and
saves the chart to outputs/scatter_credit_rate.png.

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
# so `python scripts/eda_scatter_credit_rate.py` works from any location.
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = PROJECT_ROOT / "02_Data" / "Raw" / "wildcat_loans_clean.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "scatter_credit_rate.png"

STATUS_ORDER = ["Current", "Paid Off", "Delinquent", "Default"]

# Colors (light-mode chart palette) - matches eda_box_interest_by_status.py
# so loan_status colors stay consistent across charts.
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

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

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
    fig.savefig(OUTPUT_PATH, facecolor=SURFACE)
    plt.close(fig)

    print(f"Loaded: {DATA_PATH}")
    print(f"Scatter plot saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
