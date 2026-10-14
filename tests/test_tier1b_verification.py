import pytest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_study1_estimates_verification():
    p = ROOT / "data/study1_inference_summary.json"
    assert p.exists()
    with open(p, "r") as f:
        s1 = json.load(f)
        
    j_res = s1["primary_outcome_j"]
    k_res = s1["secondary_outcome_k"]
    
    assert abs(j_res["theta_A1_j"]["point_estimate"] - (-0.567904)) <= 1e-6
    assert abs(j_res["theta_A0_j"]["point_estimate"] - (-0.010801)) <= 1e-6
    assert abs(j_res["theta_D_j_contrast"]["point_estimate"] - (-0.557103)) <= 1e-6
    assert abs(k_res["theta_A1_k"]["point_estimate"] - (-0.236904)) <= 1e-6
    assert abs(k_res["theta_A0_k"]["point_estimate"] - (-0.021632)) <= 1e-6
    assert abs(k_res["theta_D_k_contrast"]["point_estimate"] - (-0.215272)) <= 1e-6

def test_validation_estimates_verification():
    p = ROOT / "data/validation_summary.json"
    assert p.exists()
    with open(p, "r") as f:
        val = json.load(f)
        
    v1 = val["axis_results"]["V1_IDSIM"]
    v2 = val["axis_results"]["V2_HUMAN"]
    v3 = val["axis_results"]["V3_NUISANCE"]
    
    assert abs(v1["protected_estimate"] - 0.231351) <= 1e-6
    assert abs(v1["target_estimate"] - 0.072272) <= 1e-6
    assert abs(v2["protected_h_estimate"] - 0.986667) <= 1e-6
    assert abs(v2["target_h_estimate"] - 0.401948) <= 1e-6
    assert abs(v3["core_model_protected"] - 0.516443) <= 1e-6
    assert abs(v3["pose_model_protected"] - 0.516446) <= 1e-6
