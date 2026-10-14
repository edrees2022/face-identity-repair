# Candidate-A / Paper A — Reproducibility Entrypoints & Expected Outputs

**Protocol Authority:** `Candidate_A_CONCISE_v1_1`  
**Execution Environment:** Python >= 3.9, Linux/macOS/Windows x86_64  

---

## 1. Reproducibility Classification

This release organizes reproducibility artifacts into three distinct tiers:
- **Tier 1a (Genuine CPU Analysis Replay):** Refits the primary paired linear mixed-effects model ($D \sim 	ext{Seed} + (1|	ext{Case})$), executes case-cluster percentile bootstrap, and recalculates Table S9 descriptive statistics directly from row-level observations.
- **Tier 1b (Frozen Summary Verification):** Verifies published estimates for Study 1 and Validation axes against immutable summary JSON outputs.
- **Tier 2 (Full Pipeline Reference):** Documented runbook for GPU generation and feature extraction. Staged as a reference guide only; **not executable** within this CPU package.

---

## 2. Step-by-Step Execution Guide

### Step 1: Verify Staged Numerical Artifacts
Checks SHA256 cryptographic equality for all 6 data files:
```bash
python scripts/verify_data_integrity.py
```
Expected Output:
```text
=== CANDIDATE-A RELEASE DATA INTEGRITY AUDIT ===
PASS: cohort_n119_manifest.json matches expected hash (762206cd732d...).
PASS: study1_inference_summary.json matches expected hash (8b16f23b8ed9...).
PASS: study1_joint_summary.json matches expected hash (88fb502afae6...).
PASS: study2_joint_summary.json matches expected hash (dd2b9a48a9a4...).
PASS: study2_master_paired_input.csv matches expected hash (373c9f1d0600...).
PASS: validation_summary.json matches expected hash (b40fc4e074c2...).
ALL DATA ARTIFACTS VERIFIED SUCCESSFULLY (PASS).
```

### Step 2: Run Tier 1a Analysis Replay
Refits primary LMM and bootstrap on 287 paired rows:
```bash
python scripts/run_tier1a_analysis_replay.py --reps 1000
```
Expected Values:
- Primary Protected Contrast ($\hat{	heta}_j$): `+0.512918` (tolerance $\le 10^{-5}$)
- Primary Target Contrast ($\hat{	heta}_k$): `+0.158853` (tolerance $\le 10^{-5}$)
- Complete 3-Seed Cases ($N=74$): `+0.526683` / `+0.169166`
- Table S9 Descriptive Stats: Mean `j = -0.070549`, `k = -0.080126`, Pearson `r = 0.826727`, Q1=46, Q2=91, Q3=114, Q4=68.

### Step 3: Run Tier 1b Frozen Summary Verification
Verifies Study 1 and Validation metrics:
```bash
python scripts/run_tier1b_frozen_verification.py
```
Expected Values:
- Study 1 Protected Contrast: `-0.557103`
- Study 1 Target Contrast: `-0.215272`
- Validation Axis V1 (ID-Sim): `+0.231351` / `+0.072272`
- Validation Axis V2 (Human H): `+0.986667` / `+0.401948`
- Validation Axis V3 (Nuisance Core): `+0.516443`
- Validation Axis V3 (Nuisance Pose): `+0.516446`

### Step 4: Run Automated Test Suite
```bash
pytest -q -p no:cacheprovider tests/
```
Expected Output: All tests pass.
