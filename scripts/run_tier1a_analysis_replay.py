#!/usr/bin/env python3
"""
scripts/run_tier1a_analysis_replay.py
Executes Track R1-T1a: Genuine CPU Analysis Replay on Study 2 Paired Data.
Fits LMM, executes case-cluster bootstrap, and recalculates Table S9 descriptive statistics.
"""

import sys
import argparse
import json
import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.paired_lmm import fit_paired_lmm
from src.core.cluster_bootstrap import run_case_cluster_bootstrap

DATA_PATH = ROOT / "data/study2_master_paired_input.csv"

def main():
    parser = argparse.ArgumentParser(description="Candidate-A Track R1-T1a Analysis Replay")
    parser.add_argument("--reps", type=int, default=1000, help="Number of bootstrap replicates (default: 1000; use 5000 for full paper parity)")
    args = parser.parse_args()

    print("=================================================================")
    print("  TRACK R1-T1a: STUDY 2 FULL CPU ANALYSIS REPLAY (GENUINE REFIT)")
    print("=================================================================")

    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found.")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    total_planned = len(df)
    assert total_planned == 357, f"Expected 357 total planned rows, got {total_planned}"

    # 1. Table S5: Availability Accounting
    print("\n[1/5] Recomputing Table S5: Study 2 Availability Accounting...")
    df_paired = df[df["paired_measurable"] == True].copy()
    n_pairs = len(df_paired)
    n_cases = df_paired["case_id"].nunique()
    
    n_a1_only = len(df[(df["A1_identity_measurable"] == True) & (df["A2_identity_measurable"] == False)])
    n_a2_only = len(df[(df["A1_identity_measurable"] == False) & (df["A2_identity_measurable"] == True)])
    n_neither = len(df[(df["A1_identity_measurable"] == False) & (df["A2_identity_measurable"] == False)])
    total_a1 = len(df[df["A1_identity_measurable"] == True])
    total_a2 = len(df[df["A2_identity_measurable"] == True])

    print(f"  Total planned:       {total_planned}")
    print(f"  Paired measurable:   {n_pairs} ({n_pairs/total_planned*100:.2f}%) across {n_cases} cases")
    print(f"  A1-only measurable:  {n_a1_only}")
    print(f"  A2-only measurable:  {n_a2_only}")
    print(f"  Neither measurable:  {n_neither}")
    print(f"  Total A1 measurable: {total_a1} ({total_a1/total_planned*100:.2f}%)")
    print(f"  Total A2 measurable: {total_a2} ({total_a2/total_planned*100:.2f}%)")

    assert n_pairs == 287 and n_cases == 111
    assert n_a1_only == 17 and n_a2_only == 32 and n_neither == 21
    assert total_a1 == 304 and total_a2 == 319

    cases = df_paired["case_id"].values
    seeds = df_paired["seed"].values
    y_j = df_paired["D_j"].values
    y_k = df_paired["D_k"].values
    paired_records = df_paired.to_dict(orient="records")

    # 2. Primary Protected Estimand
    print(f"\n[2/5] Fitting Primary Protected Contrast D_j (Bootstrap reps: {args.reps})...")
    fit_j = fit_paired_lmm(cases, y_j, seeds)
    branch_j = fit_j["selected_branch"]
    print(f"  Fitted Branch: {branch_j} (tau = {fit_j['tau']:.6f}, sig_u_sq = {fit_j['sigma_u_sq']:.6f}, sig_e_sq = {fit_j['sigma_e_sq']:.6f})")
    boot_j = run_case_cluster_bootstrap(paired_records, "D_j", selected_branch=branch_j, target_replicates=args.reps, seed=20260921)
    
    print(f"  Fitted theta_hat_j: {fit_j['theta_hat']:.6f} (Paper: +0.512918)")
    print(f"  95% Bootstrap CI:   [{boot_j['ci_95'][0]:.6f}, {boot_j['ci_95'][1]:.6f}] (Paper: [+0.471434, +0.550259])")
    print(f"  Bootstrap SE:       {boot_j['bootstrap_se']:.6f} (Paper: 0.020057)")

    # 3. Key Secondary Target Estimand
    print(f"\n[3/5] Fitting Key Secondary Target Contrast D_k (Bootstrap reps: {args.reps})...")
    fit_k = fit_paired_lmm(cases, y_k, seeds)
    branch_k = fit_k["selected_branch"]
    print(f"  Fitted Branch: {branch_k} (tau = {fit_k['tau']:.6f}, sig_u_sq = {fit_k['sigma_u_sq']:.6f}, sig_e_sq = {fit_k['sigma_e_sq']:.6f})")
    boot_k = run_case_cluster_bootstrap(paired_records, "D_k", selected_branch=branch_k, target_replicates=args.reps, seed=20260921)
    
    print(f"  Fitted theta_hat_k: {fit_k['theta_hat']:.6f} (Paper: +0.158853)")
    print(f"  95% Bootstrap CI:   [{boot_k['ci_95'][0]:.6f}, {boot_k['ci_95'][1]:.6f}] (Paper: [+0.118903, +0.197523])")
    print(f"  Bootstrap SE:       {boot_k['bootstrap_se']:.6f} (Paper: 0.020346)")

    # 4. Sensitivity: Complete 3-Seed Cases & Seed Strata
    print("\n[4/5] Sensitivity: Complete 3-Seed Cases & Seed Strata...")
    case_counts = df_paired["case_id"].value_counts()
    complete_cases = case_counts[case_counts == 3].index
    df_complete = df_paired[df_paired["case_id"].isin(complete_cases)].copy()
    n_comp_cases = len(complete_cases)
    n_comp_rows = len(df_complete)
    print(f"  Complete 3-seed cases: {n_comp_cases} (rows: {n_comp_rows}) (Expected: 74 cases, 222 rows)")
    assert n_comp_cases == 74 and n_comp_rows == 222

    fit_comp_j = fit_paired_lmm(df_complete["case_id"].values, df_complete["D_j"].values, df_complete["seed"].values)
    fit_comp_k = fit_paired_lmm(df_complete["case_id"].values, df_complete["D_k"].values, df_complete["seed"].values)
    print(f"  Complete Protected theta: {fit_comp_j['theta_hat']:.6f} (Paper: +0.526683)")
    print(f"  Complete Target theta:    {fit_comp_k['theta_hat']:.6f} (Paper: +0.169166)")

    for s in [1101, 2202, 3303]:
        df_s = df_paired[df_paired["seed"] == s]
        print(f"  Seed {s} (N={len(df_s)}): Protected={df_s['D_j'].mean():.6f}, Target={df_s['D_k'].mean():.6f}")

    # 5. Table S9: Recalculating A2 Descriptive Statistics & Quadrants
    print("\n[5/5] Recomputing Table S9: A2 Descriptive Statistics & Quadrants (N=319)...")
    df_a2 = df[df["A2_identity_measurable"] == True].copy()
    assert len(df_a2) == 319, f"Expected 319 measurable A2, got {len(df_a2)}"

    vals_j = df_a2["A2_Delta_ID_j"].values
    vals_k = df_a2["A2_Delta_ID_k"].values
    mean_j = float(np.mean(vals_j))
    mean_k = float(np.mean(vals_k))
    r_val, _ = stats.pearsonr(vals_j, vals_k)
    rho_val, _ = stats.spearmanr(vals_j, vals_k)

    q1 = int(np.sum((vals_k > 0) & (vals_j < 0)))
    q2 = int(np.sum((vals_k > 0) & (vals_j >= 0)))
    q3 = int(np.sum((vals_k <= 0) & (vals_j < 0)))
    q4 = int(np.sum((vals_k <= 0) & (vals_j >= 0)))

    print(f"  Protected Mean: {mean_j:.6f} (Paper: -0.070549)")
    print(f"  Target Mean:    {mean_k:.6f} (Paper: -0.080126)")
    print(f"  Pearson r:      {r_val:.6f} (Paper: 0.826727)")
    print(f"  Spearman rho:   {rho_val:.6f} (Paper: 0.461802)")
    print(f"  Quadrants:      Q1={q1} (14.42%), Q2={q2} (28.53%), Q3={q3} (35.74%), Q4={q4} (21.32%)")

    assert abs(mean_j - (-0.070549)) <= 1e-5
    assert abs(mean_k - (-0.080126)) <= 1e-5
    assert abs(r_val - 0.826727) <= 1e-5
    assert q1 == 46 and q2 == 91 and q3 == 114 and q4 == 68

    # Tolerance Assertions
    tol = 1e-5
    assert abs(fit_j['theta_hat'] - 0.512918) <= tol
    assert abs(fit_k['theta_hat'] - 0.158853) <= tol
    assert abs(fit_comp_j['theta_hat'] - 0.526683) <= tol
    assert abs(fit_comp_k['theta_hat'] - 0.169166) <= tol

    # Bootstrap CI stochastic bounds check
    assert 0.45 <= boot_j['ci_95'][0] <= 0.49
    assert 0.53 <= boot_j['ci_95'][1] <= 0.57
    assert 0.10 <= boot_k['ci_95'][0] <= 0.14
    assert 0.18 <= boot_k['ci_95'][1] <= 0.22

    print("\n=================================================================")
    print("  TRACK R1-T1a EXECUTION RESULT: PASS (TOLERANCE <= 1e-5)")
    print("=================================================================")

if __name__ == "__main__":
    main()
