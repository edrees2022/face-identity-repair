# Candidate-A / Paper A — Released Numerical Data Artifacts

This directory contains the privacy-screened, immutable numerical inputs required for Tier 1 analysis replay. All biometric feature vectors (e.g. 512-dimensional facial embeddings) and private personal identifiers have been excluded.

## Data Inventory

| File | Format | Description | Primary Usage |
| --- | --- | --- | --- |
| `study2_master_paired_input.csv` | CSV (357 rows) | Case- and seed-level realizations for Action A1 and Action A2 | Tier 1a Full LMM & Bootstrap Replay |
| `study1_inference_summary.json` | JSON | Frozen fitted REML estimates, SEs, and CIs for Study 1 | Tier 1b Frozen Output Verification |
| `study1_joint_summary.json` | JSON | Descriptive quadrant counts and correlations for Study 1 | Verification of Table S4 & Figure S3 |
| `study2_joint_summary.json` | JSON | Descriptive quadrant counts and correlations for Study 2 | Verification of Table S9 & Figure S5 |
| `validation_summary.json` | JSON | Integrated summary of Validation Axes V1, V2, and V3 | Verification of Table S10 & Figure 3 |
| `cohort_n119_manifest.json` | JSON | Specification of the 119 accepted two-person scenes and roles | Denominator verification |

## `study2_master_paired_input.csv` Schema
- `case_id`: Anonymized baseline case identifier (`conf_case_001` to `conf_case_119`).
- `seed`: POST generation sampling seed (`1101`, `2202`, `3303`).
- `target_role`: Spatial role of the targeted identity (`person_1` or `person_2`).
- `protected_role`: Spatial role of the co-present protected identity (`person_1` or `person_2`).
- `paired_measurable`: Boolean flag indicating if both A1 and A2 yielded valid, tracked faces ($N=287$).
- `A1_Delta_ID_j`, `A2_Delta_ID_j`: Continuous identity cosine similarity transition for protected person under A1 and A2.
- `A1_Delta_ID_k`, `A2_Delta_ID_k`: Continuous identity cosine similarity transition for target person under A1 and A2.
- `D_j`, `D_k`: Paired between-action contrast: $D = \Delta\text{ID}(\text{A2}) - \Delta\text{ID}(\text{A1})$.
