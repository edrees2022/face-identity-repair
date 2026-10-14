#!/usr/bin/env python3
"""
scripts/run_tier1b_frozen_verification.py
Executes Track R1-T1b: Frozen-Output Verification on Study 1, Joint Tables, and Validation.
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

S1_PATH = ROOT / "data/study1_inference_summary.json"
S1_JOINT_PATH = ROOT / "data/study1_joint_summary.json"
VAL_PATH = ROOT / "data/validation_summary.json"

def main():
    print("=================================================================")
    print("  TRACK R1-T1b: FROZEN-OUTPUT VERIFICATION (STUDY 1 & VALIDATION)")
    print("=================================================================")

    # 1. Verify Study 1 Primary Estimates (Table 2)
    with open(S1_PATH, "r") as f:
        s1 = json.load(f)

    j_res = s1["primary_outcome_j"]
    theta_a1_j = j_res["theta_A1_j"]["point_estimate"]
    theta_a0_j = j_res["theta_A0_j"]["point_estimate"]
    theta_d_j  = j_res["theta_D_j_contrast"]["point_estimate"]

    k_res = s1["secondary_outcome_k"]
    theta_a1_k = k_res["theta_A1_k"]["point_estimate"]
    theta_a0_k = k_res["theta_A0_k"]["point_estimate"]
    theta_d_k  = k_res["theta_D_k_contrast"]["point_estimate"]

    print("[1/3] Study 1 Table 2 Estimates & Table S2 Variance Components")
    print(f"  Protected A1:       {theta_a1_j:.6f} (Expected: -0.567904)")
    print(f"  Protected A0:       {theta_a0_j:.6f} (Expected: -0.010801)")
    print(f"  Protected Contrast: {theta_d_j:.6f}  (Expected: -0.557103)")
    print(f"  Target A1:          {theta_a1_k:.6f} (Expected: -0.236904)")
    print(f"  Target A0:          {theta_a0_k:.6f} (Expected: -0.021632)")
    print(f"  Target Contrast:    {theta_d_k:.6f}  (Expected: -0.215272)")

    assert abs(theta_a1_j - (-0.567904)) <= 1e-6
    assert abs(theta_d_j - (-0.557103)) <= 1e-6
    assert abs(theta_d_k - (-0.215272)) <= 1e-6

    vc = j_res["variance_components"]
    print(f"  tau_A0_sq: {vc['tau_A0_sq']:.6f}, tau_A1_sq: {vc['tau_A1_sq']:.6f}, cov: {vc['cov_A0_A1']:.6f}")
    assert abs(vc["tau_A0_sq"] - 0.008743) <= 1e-5
    assert abs(vc["tau_A1_sq"] - 0.028059) <= 1e-5
    assert abs(vc["cov_A0_A1"] - 0.011380) <= 1e-5

    # 2. Verify Study 1 Table S4: Joint Quadrants & Correlation
    with open(S1_JOINT_PATH, "r") as f:
        s1_j = json.load(f)
    
    a1_res = s1_j["results_by_action"]["A1"]
    a0_res = s1_j["results_by_action"]["A0"]
    print("\n[2/3] Study 1 Table S4: Joint Quadrants & Correlations")
    print(f"  Action A1 (N={a1_res['evaluable_N']}): Q1={a1_res['quadrants']['Q1_k_pos_j_neg']['count']}, Q3={a1_res['quadrants']['Q3_k_nonpos_j_neg']['count']}, r={a1_res['correlations']['pearson_r']:.4f}")
    print(f"  Action A0 (N={a0_res['evaluable_N']}): Q1={a0_res['quadrants']['Q1_k_pos_j_neg']['count']}, Q2={a0_res['quadrants']['Q2_k_pos_j_nonneg']['count']}, Q3={a0_res['quadrants']['Q3_k_nonpos_j_neg']['count']}, Q4={a0_res['quadrants']['Q4_k_nonpos_j_nonneg']['count']}, r={a0_res['correlations']['pearson_r']:.4f}")

    assert a1_res["evaluable_N"] == 304
    assert a1_res["quadrants"]["Q1_k_pos_j_neg"]["count"] == 29
    assert a1_res["quadrants"]["Q3_k_nonpos_j_neg"]["count"] == 275
    assert abs(a1_res["correlations"]["pearson_r"] - 0.09064) <= 1e-4

    assert a0_res["evaluable_N"] == 293
    assert a0_res["quadrants"]["Q1_k_pos_j_neg"]["count"] == 45
    assert a0_res["quadrants"]["Q2_k_pos_j_nonneg"]["count"] == 77
    assert a0_res["quadrants"]["Q3_k_nonpos_j_neg"]["count"] == 118
    assert a0_res["quadrants"]["Q4_k_nonpos_j_nonneg"]["count"] == 53
    assert abs(a0_res["correlations"]["pearson_r"] - 0.491008) <= 1e-4

    # 3. Verify Validation Tri-Axis (Table S10, Table S11, Figure 3)
    with open(VAL_PATH, "r") as f:
        val = json.load(f)

    v1 = val["axis_results"]["V1_IDSIM"]
    v2 = val["axis_results"]["V2_HUMAN"]
    v3 = val["axis_results"]["V3_NUISANCE"]

    print("\n[3/3] Validation Tri-Axis Estimates (Table S10, Table S11)")
    print(f"  V1 ID-Sim Protected:   {v1['protected_estimate']:.6f} (Expected: 0.231351)")
    print(f"  V1 ID-Sim Target:      {v1['target_estimate']:.6f} (Expected: 0.072272)")
    print(f"  V2 Human H Protected:  {v2['protected_h_estimate']:.6f} (Expected: 0.986667)")
    print(f"  V2 Human H Target:     {v2['target_h_estimate']:.6f} (Expected: 0.401948)")
    print(f"  V3 Nuisance Core Prot: {v3['core_model_protected']:.6f} (Expected: 0.516443)")
    print(f"  V3 Nuisance Pose Prot: {v3['pose_model_protected']:.6f} (Expected: 0.516446)")

    assert abs(v1['protected_estimate'] - 0.231351) <= 1e-6
    assert abs(v2['protected_h_estimate'] - 0.986667) <= 1e-6
    assert abs(v3['core_model_protected'] - 0.516443) <= 1e-6

    print("\n=================================================================")
    print("  TRACK R1-T1b EXECUTION RESULT: PASS (EXACT NUMERICAL MATCH)")
    print("=================================================================")

if __name__ == "__main__":
    main()
