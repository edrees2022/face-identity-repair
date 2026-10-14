"""
src/core/paired_lmm.py
Curated, authoritative linear mixed-effects model solver for paired contrasts:
D ~ Seed + (1 | Case) via profile REML over tau = sigma_u^2 / sigma_e^2.
"""

from typing import Any, Dict, List, Tuple
import numpy as np
import scipy.optimize as opt

def fit_paired_lmm(
    case_ids: List[str],
    y: np.ndarray,
    seeds: np.ndarray,
    tol_singular: float = 1e-6,
) -> Dict[str, Any]:
    """
    Fits D ~ Seed + (1 | Case) via REML profile likelihood over tau = sigma_u^2 / sigma_e^2.
    Seeds: array of 1101, 2202, 3303.
    """
    seed_levels = [1101, 2202, 3303]
    p = len(seed_levels)
    seed_to_col = {s: i for i, s in enumerate(seed_levels)}

    # Group data by case
    case_groups: Dict[str, List[int]] = {}
    for i, cid in enumerate(case_ids):
        case_groups.setdefault(cid, []).append(i)

    c_list = sorted(case_groups.keys())
    case_data = []
    for cid in c_list:
        idx = case_groups[cid]
        n_c = len(idx)
        y_c = y[idx]
        X_c = np.zeros((n_c, p), dtype=np.float64)
        for row_i, data_i in enumerate(idx):
            X_c[row_i, seed_to_col[seeds[data_i]]] = 1.0
        case_data.append({"cid": cid, "n_c": n_c, "y_c": y_c, "X_c": X_c})

    N = len(y)

    def eval_reml(tau: float) -> Tuple[float, np.ndarray, float, float]:
        W = np.zeros((p, p), dtype=np.float64)
        b_vec = np.zeros(p, dtype=np.float64)
        sum_log_det_unit = 0.0

        for cd in case_data:
            n_c = cd["n_c"]
            X_c = cd["X_c"]
            y_c = cd["y_c"]

            factor = tau / (1.0 + n_c * tau) if (1.0 + n_c * tau) > 0 else 0.0
            sum_log_det_unit += np.log(max(1.0 + n_c * tau, 1e-15))

            col_sums_X = np.sum(X_c, axis=0)
            X_t_V_X = X_c.T @ X_c - factor * np.outer(col_sums_X, col_sums_X)
            W += X_t_V_X

            sum_y = np.sum(y_c)
            X_t_V_y = X_c.T @ y_c - factor * col_sums_X * sum_y
            b_vec += X_t_V_y

        try:
            L_W = np.linalg.cholesky(W)
            log_det_W = 2.0 * np.sum(np.log(np.diag(L_W)))
            u = np.linalg.solve(L_W, b_vec)
            beta = np.linalg.solve(L_W.T, u)
        except np.linalg.LinAlgError:
            beta = np.linalg.pinv(W) @ b_vec
            sign, log_det_W = np.linalg.slogdet(W)
            if sign <= 0:
                log_det_W = 1e12

        q_unit = 0.0
        for cd in case_data:
            n_c = cd["n_c"]
            X_c = cd["X_c"]
            y_c = cd["y_c"]
            r_c = y_c - X_c @ beta
            sum_r = np.sum(r_c)
            factor = tau / (1.0 + n_c * tau) if (1.0 + n_c * tau) > 0 else 0.0
            q_unit += np.sum(r_c ** 2) - factor * (sum_r ** 2)

        sig_e_sq = max(q_unit / (N - p), 1e-12)
        reml_crit = (N - p) * np.log(sig_e_sq) + sum_log_det_unit + log_det_W
        return reml_crit, beta, sig_e_sq, tau * sig_e_sq

    crit_0, beta_0, sig_e_0, sig_u_0 = eval_reml(0.0)

    def obj(log_tau: float) -> float:
        tau = np.exp(log_tau)
        crit, _, _, _ = eval_reml(tau)
        return float(crit)

    res = opt.minimize_scalar(obj, bounds=(-15.0, 10.0), method="bounded")
    best_tau = float(np.exp(res.x)) if res.success else 0.0
    crit_opt, beta_opt, sig_e_opt, sig_u_opt = eval_reml(best_tau)

    if best_tau * sig_e_opt <= tol_singular or crit_0 <= crit_opt:
        selected_branch = "BRANCH_B"
        beta_final = beta_0
        sig_u_sq = 0.0
        sig_e_sq = sig_e_0
    else:
        selected_branch = "BRANCH_A"
        beta_final = beta_opt
        sig_u_sq = sig_u_opt
        sig_e_sq = sig_e_opt

    mu_1101 = float(beta_final[0])
    mu_2202 = float(beta_final[1])
    mu_3303 = float(beta_final[2])
    theta_hat = float((mu_1101 + mu_2202 + mu_3303) / 3.0)

    return {
        "selected_branch": selected_branch,
        "mu_1101": mu_1101,
        "mu_2202": mu_2202,
        "mu_3303": mu_3303,
        "theta_hat": theta_hat,
        "sigma_u_sq": sig_u_sq,
        "sigma_e_sq": sig_e_sq,
        "tau": best_tau
    }

def fit_ols_cell_means(seeds: np.ndarray, y: np.ndarray) -> Tuple[float, float, float, float]:
    mu_1101 = float(np.mean(y[seeds == 1101]))
    mu_2202 = float(np.mean(y[seeds == 2202]))
    mu_3303 = float(np.mean(y[seeds == 3303]))
    theta_hat = float((mu_1101 + mu_2202 + mu_3303) / 3.0)
    return mu_1101, mu_2202, mu_3303, theta_hat
