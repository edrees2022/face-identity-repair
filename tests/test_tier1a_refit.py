import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.paired_lmm import fit_paired_lmm

def test_primary_paired_lmm_refit():
    p = ROOT / "data/study2_master_paired_input.csv"
    assert p.exists()
    df = pd.read_csv(p)
    df_p = df[df["paired_measurable"] == True]
    
    assert len(df_p) == 287
    assert df_p["case_id"].nunique() == 111
    
    cases = df_p["case_id"].values
    seeds = df_p["seed"].values
    y_j = df_p["D_j"].values
    y_k = df_p["D_k"].values
    
    fit_j = fit_paired_lmm(cases, y_j, seeds)
    fit_k = fit_paired_lmm(cases, y_k, seeds)
    
    assert abs(fit_j["theta_hat"] - 0.512918) <= 1e-5
    assert abs(fit_k["theta_hat"] - 0.158853) <= 1e-5
