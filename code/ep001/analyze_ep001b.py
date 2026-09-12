"""Postprocess the preserved EP001-A first-run output for EP001-B."""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import numpy as np

GAMMAS = (0.5, 0.9, 1.0)
RELATIVE_EPSILON = 1e-12
DISCOVERY_CODE = 0
CONFIRMATION_CODE = 1


def geometric_factor(gamma: float, horizon: int) -> float:
    return float(sum(gamma**k for k in range(horizon)))


def transport_values(deltas: np.ndarray, delta_now: np.ndarray, gamma: float) -> dict[str, np.ndarray]:
    """Compute all EP001-B values row-wise; deltas has columns k=0,...,H."""
    horizon = deltas.shape[1] - 1
    b_h = geometric_factor(gamma, horizon)
    static = b_h * deltas[:, 0]
    weights = gamma ** np.arange(horizon)
    adapt = deltas[:, :horizon] @ weights
    error = adapt - static
    delta_c = gamma * error
    return {
        "delta_static": static,
        "delta_adapt": adapt,
        "e_transport": error,
        "abs_e_transport": np.abs(error),
        "e_rel": np.abs(error) / (np.abs(static) + RELATIVE_EPSILON),
        "c_myopic": delta_now,
        "c_static": delta_now + gamma * static,
        "c_transport": delta_now + gamma * adapt,
        "delta_c": delta_c,
        "w_c": np.abs(delta_c),
    }


def quantiles(values: np.ndarray) -> dict[str, float | int | None]:
    values = values[np.isfinite(values)]
    if not values.size:
        return {"count": 0, "median": None, "q25": None, "q75": None, "mean": None}
    return {
        "count": int(values.size),
        "median": float(np.median(values)),
        "q25": float(np.quantile(values, 0.25)),
        "q75": float(np.quantile(values, 0.75)),
        "mean": float(np.mean(values)),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def analyze(raw_path: Path, output_dir: Path) -> dict[str, object]:
    start = time.perf_counter()
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(raw_path.with_name("run_manifest.json").read_text(encoding="utf-8"))
    raw = np.load(raw_path)
    deltas = raw["deltas"]
    horizon = deltas.shape[1] - 1
    if horizon != 10:
        raise ValueError(f"EP001-B requires the preserved H=10 horizon, got H={horizon}")

    derived: dict[str, np.ndarray] = {}
    config_rows: list[dict[str, object]] = []
    trajectory_rows: list[dict[str, object]] = []
    checkpoint_rows: list[dict[str, object]] = []
    config_by_id = {int(c["config_id"]): c for c in manifest["configurations"]}

    for gamma in GAMMAS:
        values = transport_values(deltas, raw["delta_now"], gamma)
        for key, array in values.items():
            derived[f"{key}_g{str(gamma).replace('.', '')}"] = array
        for split, split_name in ((DISCOVERY_CODE, "discovery"), (CONFIRMATION_CODE, "confirmation")):
            split_mask = raw["split"] == split
            for config_id, config in config_by_id.items():
                mask = split_mask & (raw["config_id"] == config_id)
                eligible = mask & raw["eligible"]
                if not np.any(mask):
                    continue
                e = values["e_transport"][eligible]
                w = values["w_c"][eligible]
                dc = values["delta_c"][eligible]
                tol = raw["numerical_tolerance"][eligible]
                seeds = raw["seed"][mask]
                seed_values = raw["seed"][eligible]
                seed_rows = []
                for seed in np.unique(seeds):
                    sm = seed_values == seed
                    sw = w[sm]
                    se = e[sm]
                    st = tol[sm]
                    seed_rows.append((int(seed), sw, se, st))
                    trajectory_rows.append({
                        "split": split_name, "gamma": gamma, "config_id": config_id,
                        "distribution": config["distribution"], "q": config["q"],
                        "eta": config["eta"], "eta_teacher": config["eta_teacher"],
                        "target_noise_std": config["target_noise_std"], "teacher_variance": config["teacher_variance"],
                        "seed": int(seed), "eligible_cases": int(sm.sum()),
                        "median_w_c": float(np.median(sw)) if sw.size else None,
                        "mean_w_c": float(np.mean(sw)) if sw.size else None,
                        "sum_w_c": float(sw.sum()),
                        "median_delta_c": float(np.median(se)) if se.size else None,
                        "any_non_negligible_transport": bool(np.any(np.abs(se) > st)) if se.size else False,
                    })
                abs_w = np.abs(w)
                top_share = 0.0
                if abs_w.sum() > 0:
                    seed_totals = [float(np.abs(item[1]).sum()) for item in seed_rows]
                    top_share = max(seed_totals) / float(abs_w.sum())
                config_rows.append({
                    "split": split_name, "gamma": gamma, "config_id": config_id,
                    "distribution": config["distribution"], "label": config["label"], "q": config["q"],
                    "eta": config["eta"], "eta_teacher": config["eta_teacher"],
                    "target_noise_std": config["target_noise_std"], "teacher_variance": config["teacher_variance"],
                    "is_isotropic_control": config["is_isotropic_control"],
                    "eligible_cases": int(eligible.sum()),
                    "delta_static": quantiles(values["delta_static"][eligible]),
                    "delta_adapt": quantiles(values["delta_adapt"][eligible]),
                    "e_transport": quantiles(e),
                    "abs_e_transport": quantiles(np.abs(e)),
                    "w_c": quantiles(w),
                    "delta_c_positive_cases": int((dc > 0)[...].sum()),
                    "delta_c_negative_cases": int((dc < 0)[...].sum()),
                    "non_negligible_transport_cases": int((np.abs(e) > tol).sum()),
                    "trajectories_with_non_negligible_transport": int(sum(np.any(np.abs(item[2]) > item[3]) for item in seed_rows)),
                    "trajectory_count": len(seed_rows),
                    "top_seed_abs_w_c_share": top_share,
                })
            # Checkpoint relationship for all configurations, retaining compact aggregates.
            for config_id, config in config_by_id.items():
                for checkpoint in np.unique(raw["checkpoint"]):
                    mask = (raw["split"] == split) & (raw["config_id"] == config_id) & (raw["checkpoint"] == checkpoint) & raw["eligible"]
                    if np.any(mask):
                        checkpoint_rows.append({
                            "split": split_name, "gamma": gamma, "config_id": config_id,
                            "checkpoint": int(checkpoint), "eligible_cases": int(mask.sum()),
                            "median_error_norm": float(np.median(raw["error_norm"][mask])),
                            "median_abs_e_transport": float(np.median(values["abs_e_transport"][mask])),
                            "median_w_c": float(np.median(values["w_c"][mask])),
                        })

    derived_path = output_dir / "ep001b_case_values.npz"
    np.savez_compressed(derived_path, **derived)
    write_csv(output_dir / "ep001b_configuration_summary.csv", [
        {k: (json.dumps(v, sort_keys=True) if isinstance(v, dict) else v) for k, v in row.items()}
        for row in config_rows
    ])
    write_csv(output_dir / "ep001b_trajectory_summary.csv", trajectory_rows)
    write_csv(output_dir / "ep001b_checkpoint_summary.csv", checkpoint_rows)
    report = {
        "plan": "EP001-B", "source_raw": str(raw_path), "horizon": horizon,
        "gammas": list(GAMMAS), "relative_epsilon": RELATIVE_EPSILON,
        "timing_convention": "Delta_adapt=sum_{k=0}^{H-1} gamma^k Delta_k; routing value uses outer gamma.",
        "configuration_summary_rows": len(config_rows), "trajectory_summary_rows": len(trajectory_rows),
        "runtime_seconds": time.perf_counter() - start,
        "files": {"case_values": derived_path.name, "configuration_summary": "ep001b_configuration_summary.csv", "trajectory_summary": "ep001b_trajectory_summary.csv", "checkpoint_summary": "ep001b_checkpoint_summary.csv"},
    }
    (output_dir / "ep001b_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, default=Path("results/ep001/first_run_001/raw_ep001a.npz"))
    parser.add_argument("--output", type=Path, default=Path("results/ep001/first_run_001/ep001b"))
    args = parser.parse_args()
    report = analyze(args.raw, args.output)
    print(json.dumps({"runtime_seconds": report["runtime_seconds"], "configuration_summary_rows": report["configuration_summary_rows"]}, sort_keys=True))


if __name__ == "__main__":
    main()
