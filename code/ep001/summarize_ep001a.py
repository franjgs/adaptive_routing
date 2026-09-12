"""Summarize preserved EP001-A raw output using seed-level confirmation inference."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from validation import summarize_trajectory_reversals


DISCOVERY_CODE = 0
CONFIRMATION_CODE = 1
BOOTSTRAP_REPLICATIONS = 10_000
BOOTSTRAP_SEED = 20260914


def configuration_rows(
    raw: np.lib.npyio.NpzFile, configurations: list[dict[str, object]], split: int
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for config in configurations:
        config_id = int(config["config_id"])
        mask = (raw["config_id"] == config_id) & (raw["split"] == split)
        eligible = raw["eligible"][mask]
        robust = raw["robust_reversal"][mask]
        seeds = raw["seed"][mask]
        seed_summaries = summarize_trajectory_reversals(seeds, eligible, robust)
        eligible_count = int(eligible.sum())
        robust_count = int(robust.sum())
        rows.append(
            {
                "config_id": config_id,
                "label": config["label"],
                "distribution": config["distribution"],
                "q": config["q"],
                "eta": config["eta"],
                "eta_teacher": config["eta_teacher"],
                "target_noise_std": config["target_noise_std"],
                "teacher_variance": config["teacher_variance"],
                "is_isotropic_control": config["is_isotropic_control"],
                "total_cases": int(mask.sum()),
                "eligible_cases": eligible_count,
                "robust_reversal_cases": robust_count,
                "pooled_robust_frequency_descriptive": (
                    robust_count / eligible_count if eligible_count else None
                ),
                "trajectories_with_robust_reversal": int(
                    sum(item.contains_robust_reversal for item in seed_summaries)
                ),
                "trajectory_count": len(seed_summaries),
            }
        )
    return rows


def choose_discovery_configuration(rows: list[dict[str, object]]) -> dict[str, object] | None:
    candidates = [
        row
        for row in rows
        if not bool(row["is_isotropic_control"]) and int(row["eligible_cases"]) > 0
    ]
    if not candidates:
        return None
    return sorted(
        candidates,
        key=lambda row: (
            -float(row["pooled_robust_frequency_descriptive"]),
            abs(float(row["q"]) - 1.0 / 3.0),
            float(row["eta"]),
            float(row["eta_teacher"]),
            float(row["target_noise_std"]),
            float(row["teacher_variance"]),
        ),
    )[0]


def percentile_interval(values: np.ndarray) -> list[float | None]:
    if values.size == 0:
        return [None, None]
    return [float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))]


def confirmation_detail(
    raw: np.lib.npyio.NpzFile, selected: dict[str, object] | None
) -> dict[str, object]:
    if selected is None:
        return {"selected_config_id": None, "status": "inconclusive_no_eligible_discovery_config"}
    config_id = int(selected["config_id"])
    mask = (raw["config_id"] == config_id) & (raw["split"] == CONFIRMATION_CODE)
    summaries = summarize_trajectory_reversals(
        raw["seed"][mask], raw["eligible"][mask], raw["robust_reversal"][mask]
    )
    eligible_rates = np.array(
        [item.robust_reversal_rate for item in summaries if item.robust_reversal_rate is not None],
        dtype=float,
    )
    robust_total = sum(item.robust_reversal_cases for item in summaries)
    eligible_total = sum(item.eligible_cases for item in summaries)
    has_reversal = np.array(
        [item.contains_robust_reversal for item in summaries], dtype=float
    )
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    bootstrap_occurrence = np.empty(BOOTSTRAP_REPLICATIONS)
    bootstrap_median_rate = np.empty(BOOTSTRAP_REPLICATIONS)
    for replication in range(BOOTSTRAP_REPLICATIONS):
        selected_indices = rng.integers(0, len(summaries), size=len(summaries))
        selected_summaries = [summaries[index] for index in selected_indices]
        bootstrap_occurrence[replication] = np.mean(
            [item.contains_robust_reversal for item in selected_summaries]
        )
        selected_rates = [
            item.robust_reversal_rate
            for item in selected_summaries
            if item.robust_reversal_rate is not None
        ]
        bootstrap_median_rate[replication] = (
            np.median(selected_rates) if selected_rates else np.nan
        )
    robust_mask = mask & raw["robust_reversal"]
    flip_values = raw["k_flip"][robust_mask]
    rho_values = raw["rho_rev"][mask & raw["eligible"]]
    contributions = [
        {
            "seed": item.seed,
            "eligible_cases": item.eligible_cases,
            "robust_reversal_cases": item.robust_reversal_cases,
            "r_s": item.robust_reversal_rate,
            "contains_robust_reversal": item.contains_robust_reversal,
            "robust_contribution_share": (
                item.robust_reversal_cases / robust_total if robust_total else 0.0
            ),
        }
        for item in summaries
    ]
    trajectories_with_robust = int(has_reversal.sum())
    criteria = {
        "minimum_eligible_cases": eligible_total >= 500,
        "minimum_robust_cases": robust_total >= 20,
        "minimum_independent_trajectories": trajectories_with_robust >= 5,
    }
    return {
        "selected_config_id": config_id,
        "selected_configuration": selected,
        "total_eligible_cases": eligible_total,
        "total_robust_reversals": robust_total,
        "pooled_robust_frequency_descriptive_only": (
            robust_total / eligible_total if eligible_total else None
        ),
        "trajectories_with_robust_reversal": trajectories_with_robust,
        "trajectory_fraction_with_robust_reversal": float(has_reversal.mean()),
        "r_s_median": float(np.median(eligible_rates)) if eligible_rates.size else None,
        "r_s_iqr": (
            [float(np.quantile(eligible_rates, 0.25)), float(np.quantile(eligible_rates, 0.75))]
            if eligible_rates.size
            else [None, None]
        ),
        "seed_bootstrap_95_ci": {
            "trajectory_occurrence_fraction": percentile_interval(bootstrap_occurrence),
            "median_r_s": percentile_interval(bootstrap_median_rate[np.isfinite(bootstrap_median_rate)]),
        },
        "per_seed": contributions,
        "k_flip_distribution_robust_cases": {
            str(int(value)): int((flip_values == value).sum())
            for value in np.unique(flip_values)
        },
        "rho_rev_eligible_cases": {
            "count": int(rho_values.size),
            "median": float(np.median(rho_values)) if rho_values.size else None,
            "iqr": (
                [float(np.quantile(rho_values, 0.25)), float(np.quantile(rho_values, 0.75))]
                if rho_values.size
                else [None, None]
            ),
        },
        "criteria": criteria,
        "pass": all(criteria.values()),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize(raw_path: Path, output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = raw_path.with_name("run_manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    raw = np.load(raw_path)
    discovery_rows = configuration_rows(raw, manifest["configurations"], DISCOVERY_CODE)
    confirmation_rows = configuration_rows(raw, manifest["configurations"], CONFIRMATION_CODE)
    selected = choose_discovery_configuration(discovery_rows)
    confirmation = confirmation_detail(raw, selected)
    invalid = bool(manifest["validation"]["isotropic_control_expected_reversal_violation"])
    if invalid:
        verdict = "INVALID"
    elif confirmation.get("status", "").startswith("inconclusive"):
        verdict = "INCONCLUSIVE"
    elif bool(confirmation["pass"]):
        verdict = "PASSES"
    else:
        verdict = "FAILS TO SUPPORT THE PHENOMENON IN THE TESTED REGIME"
    report = {
        "validation": manifest["validation"],
        "discovery": {"configuration_summary": discovery_rows, "selected_configuration": selected},
        "confirmation": {
            "configuration_summary": confirmation_rows,
            "selected_configuration_detail": confirmation,
        },
        "verdict": verdict,
    }
    write_csv(output_dir / "discovery_configuration_summary.csv", discovery_rows)
    write_csv(output_dir / "confirmation_configuration_summary.csv", confirmation_rows)
    if confirmation.get("per_seed"):
        write_csv(output_dir / "confirmation_per_seed.csv", confirmation["per_seed"])
    (output_dir / "ep001a_summary.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw",
        type=Path,
        default=Path("results/ep001/first_run_001/raw_ep001a.npz"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/ep001/first_run_001/summary"),
    )
    args = parser.parse_args()
    report = summarize(args.raw, args.output)
    print(report["verdict"])


if __name__ == "__main__":
    main()
