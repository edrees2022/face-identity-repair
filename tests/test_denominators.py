import pytest
import pandas as pd
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_cohort_denominators():
    p = ROOT / "data/study2_master_paired_input.csv"
    assert p.exists()
    df = pd.read_csv(p)
    
    assert len(df) == 357, "Total planned rows must be 357 (119 cases x 3 seeds)"
    assert df["case_id"].nunique() == 119, "Total cases must be 119"
    
    df_paired = df[df["paired_measurable"] == True]
    assert len(df_paired) == 287, "Paired rows must be 287"
    assert df_paired["case_id"].nunique() == 111, "Paired cases must be 111"
    
    # Seeds
    seed_counts = df_paired["seed"].value_counts().to_dict()
    assert seed_counts[1101] == 94
    assert seed_counts[2202] == 97
    assert seed_counts[3303] == 96

    # Verify safe cohort structural count if present
    safe_man = ROOT / "data/cohort_n119_safe_manifest.json"
    if safe_man.exists():
        with open(safe_man, "r") as f:
            sm = json.load(f)
        assert sm["confirmatory_n"] == 119
        assert len(sm["cases"]) == 119
