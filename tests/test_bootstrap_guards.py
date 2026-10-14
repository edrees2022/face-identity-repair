import pytest
import numpy as np
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.cluster_bootstrap import run_case_cluster_bootstrap

def test_negative_replicates_raises():
    with pytest.raises(ValueError, match="target_replicates must be > 0"):
        run_case_cluster_bootstrap([], "D_j", target_replicates=-5)

def test_empty_rows_raises():
    with pytest.raises(ValueError, match="No cases found"):
        run_case_cluster_bootstrap([], "D_j", target_replicates=10)

def test_missing_seeds_guard():
    # Only 2 seeds instead of 3
    fake_rows = [
        {"case_id": "c1", "seed": 1101, "D_j": 0.5},
        {"case_id": "c1", "seed": 2202, "D_j": 0.4},
        {"case_id": "c2", "seed": 1101, "D_j": 0.6},
        {"case_id": "c2", "seed": 2202, "D_j": 0.3},
    ]
    # Should trigger max attempts guard since seed 3303 is missing
    with pytest.raises(RuntimeError, match="Bootstrap aborted: exceeded maximum attempts"):
        run_case_cluster_bootstrap(fake_rows, "D_j", target_replicates=10)
