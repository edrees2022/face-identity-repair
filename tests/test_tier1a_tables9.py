import pytest
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_table_s9_recalculation():
    p = ROOT / "data/study2_master_paired_input.csv"
    assert p.exists()
    df = pd.read_csv(p)
    df_a2 = df[df["A2_identity_measurable"] == True].copy()
    
    assert len(df_a2) == 319
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
    
    assert abs(mean_j - (-0.070549)) <= 1e-5
    assert abs(mean_k - (-0.080126)) <= 1e-5
    assert abs(r_val - 0.826727) <= 1e-5
    assert abs(rho_val - 0.461802) <= 1e-5
    assert q1 == 46 and q2 == 91 and q3 == 114 and q4 == 68
