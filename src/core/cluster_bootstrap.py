"""
src/core/cluster_bootstrap.py
Authoritative case-cluster percentile bootstrap implementation with dynamic branch selection,
infinite-retry guards, and input validation.
"""

from typing import Any, Dict, List
import numpy as np
from src.core.paired_lmm import fit_paired_lmm, fit_ols_cell_means

def run_case_cluster_bootstrap(
    paired_rows: List[Dict[str, Any]],
    outcome_col: str,
    selected_branch: str = "BRANCH_A",
    target_replicates: int = 5000,
    seed: int = 20260921,
) -> Dict[str, Any]:
    if target_replicates <= 0:
        raise ValueError(f"target_replicates must be > 0, got {target_replicates}")

    cases_dict: Dict[str, List[Dict[str, Any]]] = {}
    for r in paired_rows:
        cid = r["case_id"]
        cases_dict.setdefault(cid, []).append(r)

    case_keys = sorted(cases_dict.keys())
    n_cases = len(case_keys)
    if n_cases == 0:
        raise ValueError("No cases found in input data")

    rng = np.random.default_rng(seed)
    replicates: List[float] = []
    attempted = 0
    failed = 0
    fail_reasons: Dict[str, int] = {}
    max_attempts = max(target_replicates * 5, 2000)

    while len(replicates) < target_replicates:
        attempted += 1
        if attempted > max_attempts:
            raise RuntimeError(
                f"Bootstrap aborted: exceeded maximum attempts ({max_attempts}) with only "
                f"{len(replicates)} successful replicates. Fail reasons: {fail_reasons}"
            )

        sampled_cids = rng.choice(case_keys, size=n_cases, replace=True)

        boot_y: List[float] = []
        boot_seeds: List[int] = []
        boot_cids: List[str] = []

        for b_idx, cid in enumerate(sampled_cids):
            cluster_id = f"bcase_{b_idx}_{cid}"
            for row in cases_dict[cid]:
                boot_y.append(row[outcome_col])
                boot_seeds.append(row["seed"])
                boot_cids.append(cluster_id)

        arr_y = np.array(boot_y, dtype=np.float64)
        arr_seeds = np.array(boot_seeds, dtype=int)

        if len(set(arr_seeds)) < 3:
            failed += 1
            fail_reasons["SEED_MISSING"] = fail_reasons.get("SEED_MISSING", 0) + 1
            continue

        try:
            if selected_branch == "BRANCH_A":
                res = fit_paired_lmm(boot_cids, arr_y, arr_seeds)
                theta_b = res["theta_hat"]
            else:
                _, _, _, theta_b = fit_ols_cell_means(arr_seeds, arr_y)

            if np.isnan(theta_b) or np.isinf(theta_b):
                failed += 1
                fail_reasons["NON_FINITE"] = fail_reasons.get("NON_FINITE", 0) + 1
                continue

            replicates.append(theta_b)
        except Exception as ex:
            failed += 1
            fail_reasons[f"EX_{type(ex).__name__}"] = fail_reasons.get(f"EX_{type(ex).__name__}", 0) + 1

    arr_reps = np.array(replicates, dtype=np.float64)
    q025 = float(np.percentile(arr_reps, 2.5))
    q975 = float(np.percentile(arr_reps, 97.5))
    boot_se = float(np.std(arr_reps, ddof=1))
    boot_mean = float(np.mean(arr_reps))

    return {
        "target_replicates": target_replicates,
        "bootstrap_attempted": attempted,
        "bootstrap_successful": len(replicates),
        "bootstrap_failed": failed,
        "failure_reason_counts": fail_reasons,
        "bootstrap_mean": round(boot_mean, 6),
        "bootstrap_se": round(boot_se, 6),
        "ci_95": [round(q025, 6), round(q975, 6)],
    }
