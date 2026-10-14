#!/usr/bin/env python3
"""
scripts/replay_figures.py
Generates exploratory diagnostic plots from released numerical tables.
NOTE: These are standalone diagnostic plots, not the multi-panel composite LaTeX manuscript figures.
"""

import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "website/assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DATA_PATH = ROOT / "data/study2_master_paired_input.csv"

def main():
    print("Generating exploratory diagnostic data plots...")
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found.")
        return

    df = pd.read_csv(DATA_PATH)
    df_p = df[df["paired_measurable"] == True]

    # Diagnostic Plot: Study 2 Paired Contrasts Histogram
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    d_j = df_p["D_j"].values
    ax.hist(d_j, bins=25, color="#2b5c8f", alpha=0.8, edgecolor="white")
    ax.axvline(0.512918, color="#d95f02", linestyle="--", linewidth=2, label="Fitted Contrast (+0.513)")
    ax.axvline(0, color="gray", linestyle=":", linewidth=1)
    ax.set_xlabel("Protected Person Paired Contrast D_j = A2 - A1")
    ax.set_ylabel("Frequency (Pairs)")
    ax.set_title("Study 2: Protected Contrast Distribution (Diagnostic Plot, N=287)")
    ax.legend()
    plt.tight_layout()
    out_p = OUT_DIR / "fig_study2_paired_contrasts_diagnostic.png"
    plt.savefig(out_p)
    plt.close()
    print(f"Generated diagnostic plot: {out_p.name}")

if __name__ == "__main__":
    main()
