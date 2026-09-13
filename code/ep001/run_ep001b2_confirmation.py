"""Locked EP001-B2 confirmation analysis using frozen discovery coefficients."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
import sys
import zipfile

import numpy as np

import analyze_ep001b2 as b2
import run_ep001b2_discovery as discovery


DISCOVERY_FREEZE_COMMIT = "1d8267430a1e1bacd7dd95284f9137e44455b79d"
DISCOVERY_SHA256 = "9e64ee92e45b3925f2babfe847d1d3d04ec6388ea1537d8a6c37f6e3105757a8"
CONFIRMATION_SEEDS = tuple(range(20, 50))
PRIMARY_CONFIGS = tuple(range(76))
EXPOSED_CONFIGS = tuple(range(76, 80))
FUNCTIONAL_MODELS = ("M0", "M1F", "M2F")
OPERATIONAL_MODELS = ("M0", "M1O", "M2O")


def confirmation_ranges(configs: tuple[int, ...]) -> list[tuple[int, int]]:
    if not configs or any(c < 0 or c >= discovery.TOTAL_CONFIGS for c in configs):
        raise ValueError("invalid confirmation configurations")
    rows_per_config = discovery.TOTAL_SEEDS * discovery.ROWS_PER_SEED
    ranges = []
    for config_id in configs:
        start = config_id * rows_per_config + 20 * discovery.ROWS_PER_SEED
        ranges.append((start, start + 30 * discovery.ROWS_PER_SEED))
    return ranges


def load_confirmation_only(
    raw_path: Path, configs: tuple[int, ...]
) -> tuple[dict[str, np.ndarray], dict]:
    """Decode only confirmation rows for an explicit primary/exposed block."""
    if configs not in (PRIMARY_CONFIGS, EXPOSED_CONFIGS):
        raise ValueError("confirmation block must be primary or pre-exposed")
    manifest_path = raw_path.with_name("run_manifest.json")
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    expected_rows = discovery.TOTAL_CONFIGS * discovery.TOTAL_SEEDS * discovery.ROWS_PER_SEED
    if (
        manifest.get("master_seed") != 20260913
        or manifest.get("row_count") != expected_rows
        or manifest.get("raw_file") != raw_path.name
        or [x.get("config_id") for x in manifest.get("configurations", [])]
        != list(range(80))
    ):
        raise ValueError("unexpected EP001-A source manifest")
    ranges = confirmation_ranges(configs)
    with zipfile.ZipFile(raw_path, "r") as archive:
        raw = {
            name: discovery.read_selected_member(archive, name, ranges, expected_rows)
            for name in discovery.REQUIRED_MEMBERS
        }
    expected_count = len(configs) * len(CONFIRMATION_SEEDS) * discovery.ROWS_PER_SEED
    expected_config = np.repeat(configs, len(CONFIRMATION_SEEDS) * discovery.ROWS_PER_SEED)
    expected_seed = np.tile(
        np.repeat(CONFIRMATION_SEEDS, discovery.ROWS_PER_SEED), len(configs)
    )
    expected_checkpoint = np.tile(
        np.repeat(b2.CHECKPOINTS, 64), len(configs) * len(CONFIRMATION_SEEDS)
    )
    expected_query = np.tile(np.arange(64), expected_count // 64)
    if not (
        all(value.shape[0] == expected_count for value in raw.values())
        and np.array_equal(raw["config_id"], expected_config)
        and np.array_equal(raw["seed"], expected_seed)
        and np.array_equal(raw["split"], np.ones(expected_count, dtype=raw["split"].dtype))
        and np.array_equal(raw["checkpoint"], expected_checkpoint)
        and np.array_equal(raw["query_id"], expected_query)
    ):
        raise ValueError("confirmation source structure differs from frozen design")
    finite = np.isfinite(raw["delta_now"]) & np.isfinite(raw["deltas"][:, :10]).all(1)
    by_config = []
    for config_id in configs:
        selected = raw["config_id"] == config_id
        by_config.append(
            {
                "config_id": config_id,
                "candidate_cases": int(selected.sum()),
                "finite_cases": int((selected & finite).sum()),
                "excluded_nonfinite_cases": int((selected & ~finite).sum()),
                "seeds_with_finite_cases": int(np.unique(raw["seed"][selected & finite]).size),
            }
        )
    audit = {
        "candidate_cases": expected_count,
        "finite_cases": int(finite.sum()),
        "excluded_nonfinite_cases": int((~finite).sum()),
        "by_configuration": by_config,
        "run_manifest_sha256": discovery.sha256_bytes(manifest_bytes),
        "raw_archive_filename": raw_path.name,
        "raw_archive_bytes": raw_path.stat().st_size,
        "eligible_used": False,
        "rho_rev_used": False,
        "reversal_filter_used": False,
    }
    filtered = {key: value[finite] for key, value in raw.items()}
    if np.any(filtered["seed"] < 20) or np.any(filtered["split"] != 1):
        raise AssertionError("discovery record entered confirmation arrays")
    return filtered, audit


def jsonable(value):
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return [jsonable(item) for item in value.tolist()]
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, float) and not np.isfinite(value):
        raise ValueError("nonfinite JSON result")
    return value


def json_bytes(value) -> bytes:
    return (json.dumps(jsonable(value), sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def interval(values) -> dict:
    return b2.percentile_interval([float(x) for x in np.asarray(values)])


def reduction_array(numerator, denominator) -> np.ndarray:
    numerator = np.asarray(numerator, dtype=np.longdouble)
    denominator = np.asarray(denominator, dtype=np.longdouble)
    result = np.full(numerator.shape, np.nan, dtype=float)
    positive = denominator > 0
    result[positive] = (1 - numerator[positive] / denominator[positive]).astype(float)
    return result


def comparison_intervals(draws: np.ndarray) -> dict:
    m0, m1, m2 = (draws[..., index] for index in range(3))
    values = {
        "R1": reduction_array(m1, m0),
        "R2": reduction_array(m2, m0),
        "G_2_1": reduction_array(m2, m1),
        "difference_1_0": m1 - m0,
        "difference_2_0": m2 - m0,
        "difference_2_1": m2 - m1,
    }
    result = {}
    for name, data in values.items():
        flat = np.asarray(data)
        seq = [None if not np.isfinite(x) else float(x) for x in flat]
        result[name] = b2.percentile_interval(seq)
    return result


def bootstrap_summary(draws: dict, model_names: tuple[str, ...]) -> dict:
    grid = draws["grid"]
    configuration = draws["configuration"]
    return {
        "grid": {
            "losses": {name: interval(grid[:, i]) for i, name in enumerate(model_names)},
            "comparisons": comparison_intervals(grid),
        },
        "configuration": [
            {
                "config_id": config_id,
                "losses": {
                    name: interval(configuration[:, config_id, i])
                    for i, name in enumerate(model_names)
                },
                "comparisons": comparison_intervals(configuration[:, config_id, :]),
            }
            for config_id in PRIMARY_CONFIGS
        ],
    }


def diagnostic_intervals(result: dict) -> dict:
    output = {}
    for scope, data in result.items():
        if scope == "grid":
            output[scope] = {
                name: b2.percentile_interval(list(values))
                for name, values in data.items()
            }
        else:
            output[scope] = [
                {
                    "config_id": config_id,
                    **{
                        name: b2.percentile_interval(list(values[:, config_id]))
                        for name, values in data.items()
                    },
                }
                for config_id in PRIMARY_CONFIGS
            ]
    return output


def coefficient_summary(calibration: b2.Calibration) -> dict:
    def summarize(fits):
        values = np.asarray([fit.c for fit in fits])
        return {
            "values": values.tolist(),
            "P25_P50_P75_P90": b2.quantiles(values, np.ones(len(values))),
            "minimum": float(values.min()),
            "maximum": float(values.max()),
            "in_0_1": int(np.sum((values >= 0) & (values <= 1))),
        }
    return {
        "functional_M1": calibration.global_f.c,
        "functional_M2": summarize(calibration.config_f),
        "operational_M1": calibration.global_o.c,
        "operational_M2": summarize(calibration.config_o),
        "functional_OLS_M1": calibration.global_ols.c,
        "functional_OLS_M2": summarize(calibration.config_ols),
        "functional_constrained_M1": calibration.global_f_01.c,
        "functional_constrained_M2": summarize(calibration.config_f_01),
        "operational_constrained_M1": calibration.global_o_01.c,
        "operational_constrained_M2": summarize(calibration.config_o_01),
    }


def configuration_summaries(
    raw: dict[str, np.ndarray], values: dict, predictions: dict, gamma: float
) -> tuple[list[dict], list[dict]]:
    functional = []
    operational = []
    for config_id in np.unique(raw["config_id"]):
        mask = raw["config_id"] == config_id
        weights = b2.hierarchical_weights(raw["config_id"][mask], raw["seed"][mask], (config_id,))
        f = {
            name: b2.functional_summary(values["delta_adapt"][mask], predictions[name][mask], weights)
            for name in ("M0", "M1F", "M2F", "M1OLS", "M2OLS", "M1F01", "M2F01")
            if name in predictions
        }
        o = {
            name: b2.operational_summary(
                raw["delta_now"][mask], values["delta_static"][mask],
                values["delta_adapt"][mask], predictions[name][mask], gamma, weights
            )
            for name in ("M0", "M1O", "M2O", "M1O01", "M2O01")
            if name in predictions
        }
        functional.append(
            {
                "config_id": int(config_id),
                "models": f,
                "comparisons": b2.comparisons(*(f[name]["loss"] for name in FUNCTIONAL_MODELS))
                if all(name in f for name in FUNCTIONAL_MODELS) else None,
            }
        )
        operational.append(
            {
                "config_id": int(config_id),
                "models": o,
                "comparisons": b2.comparisons(*(o[name]["loss"] for name in OPERATIONAL_MODELS))
                if all(name in o for name in OPERATIONAL_MODELS) else None,
            }
        )
    return functional, operational


def analyze_primary_gamma(
    raw: dict[str, np.ndarray], calibration: b2.Calibration, counts: np.ndarray
) -> tuple[dict, dict, dict[str, np.ndarray], dict[str, np.ndarray]]:
    gamma = calibration.gamma
    weights = b2.hierarchical_weights(raw["config_id"], raw["seed"], PRIMARY_CONFIGS)
    values = b2.derived(raw["delta_now"], raw["deltas"], gamma)
    predictions = b2.predictions(calibration, values["delta_static"], raw["config_id"])
    functional_names = ("M0", "M1F", "M2F", "M1OLS", "M2OLS", "M1F01", "M2F01")
    operational_names = ("M0", "M1O", "M2O", "M1O01", "M2O01")
    functional_grid = {
        name: b2.functional_summary(values["delta_adapt"], predictions[name], weights)
        for name in functional_names
    }
    operational_grid = {
        name: b2.operational_summary(
            raw["delta_now"], values["delta_static"], values["delta_adapt"],
            predictions[name], gamma, weights
        )
        for name in operational_names
    }
    functional_config, operational_config = configuration_summaries(
        raw, values, predictions, gamma
    )

    functional_losses = np.column_stack(
        [abs(values["delta_adapt"] - predictions[name]) for name in FUNCTIONAL_MODELS]
    )
    target = values["c_transport"]
    baseline = values["c_static"]
    operational_thresholds = {
        name: np.asarray(raw["delta_now"]) + gamma * predictions[name]
        for name in OPERATIONAL_MODELS
    }
    operational_losses = np.column_stack(
        [b2.feasible_width(operational_thresholds[name], target) for name in OPERATIONAL_MODELS]
    )
    packed = np.column_stack((functional_losses, operational_losses))
    trajectory = b2.trajectory_table(packed, raw["config_id"], raw["seed"])
    functional_draws = b2.bootstrap_aggregate(trajectory[..., :3], counts)
    operational_draws = b2.bootstrap_aggregate(trajectory[..., 3:6], counts)
    bootstrap = {
        "functional": bootstrap_summary(functional_draws, FUNCTIONAL_MODELS),
        "operational": bootstrap_summary(operational_draws, OPERATIONAL_MODELS),
        "diagnostics": {},
    }
    for name in OPERATIONAL_MODELS:
        result = b2.bootstrap_diagnostics(
            b2.feasible_width(operational_thresholds[name], target), target, baseline,
            operational_thresholds[name], raw["config_id"], raw["seed"], counts
        )
        bootstrap["diagnostics"][name] = diagnostic_intervals(result)

    curves = {}
    for name in OPERATIONAL_MODELS:
        curve = b2.disagreement_curve(operational_thresholds[name], target, weights)
        curves[f"gamma_{gamma}_{name}_costs"] = np.asarray(curve["costs"], dtype=float)
        curves[f"gamma_{gamma}_{name}_disagreement"] = np.asarray(
            curve["disagreement"], dtype=float
        )
        curves[f"gamma_{gamma}_{name}_integral"] = np.asarray(curve["integral"])

    point = {
        "gamma": gamma,
        "coefficients": coefficient_summary(calibration),
        "functional": {
            "absolute_losses_before_ratios": {
                name: functional_grid[name]["loss"] for name in FUNCTIONAL_MODELS
            },
            "comparisons": b2.comparisons(
                *(functional_grid[name]["loss"] for name in FUNCTIONAL_MODELS)
            ),
            "models": functional_grid,
            "configuration": functional_config,
        },
        "operational": {
            "absolute_losses_before_ratios": {
                name: operational_grid[name]["loss"] for name in OPERATIONAL_MODELS
            },
            "comparisons": b2.comparisons(
                *(operational_grid[name]["loss"] for name in OPERATIONAL_MODELS)
            ),
            "models": operational_grid,
            "configuration": operational_config,
        },
    }
    trajectory_arrays = {
        f"gamma_{gamma}_functional_losses": np.asarray(trajectory[..., :3], dtype=float),
        f"gamma_{gamma}_operational_losses": np.asarray(trajectory[..., 3:6], dtype=float),
    }
    return point, bootstrap, curves, trajectory_arrays


def analyze_exposed_gamma(raw: dict[str, np.ndarray], calibration: b2.Calibration) -> dict:
    """Non-holdout M0/global-M1 evaluation; no exposed M2 coefficient is fitted."""
    gamma = calibration.gamma
    weights = b2.hierarchical_weights(raw["config_id"], raw["seed"], EXPOSED_CONFIGS)
    values = b2.derived(raw["delta_now"], raw["deltas"], gamma)
    predictions = {
        "M0": values["delta_static"],
        "M1F": calibration.global_f.c * values["delta_static"],
        "M1O": calibration.global_o.c * values["delta_static"],
        "M1OLS": calibration.global_ols.c * values["delta_static"],
        "M1F01": calibration.global_f_01.c * values["delta_static"],
        "M1O01": calibration.global_o_01.c * values["delta_static"],
    }
    functional = {
        name: b2.functional_summary(values["delta_adapt"], predictions[name], weights)
        for name in ("M0", "M1F", "M1OLS", "M1F01")
    }
    operational = {
        name: b2.operational_summary(
            raw["delta_now"], values["delta_static"], values["delta_adapt"],
            predictions[name], gamma, weights
        )
        for name in ("M0", "M1O", "M1O01")
    }
    functional_config, operational_config = configuration_summaries(
        raw, values, predictions, gamma
    )
    return {
        "gamma": gamma,
        "status": "PRE-EXPOSED_NON-HOLDOUT",
        "M2_evaluated": False,
        "M2_reason": "No frozen configs 76-79 M2 coefficient; confirmation task forbids refitting.",
        "functional": {"models": functional, "configuration": functional_config},
        "operational": {"models": operational, "configuration": operational_config},
    }


def report_text(metrics: dict, bootstrap: dict, exposed: dict) -> str:
    lines = [
        "# EP001-B2 locked confirmation report",
        "",
        "This report evaluates frozen discovery coefficients on confirmation seeds 20--49. "
        "Absolute losses precede relative reductions. No coefficient was refitted.",
        "",
        f"Primary cases: {metrics['structure']['finite_cases']} finite of "
        f"{metrics['structure']['candidate_cases']} candidates; "
        f"{metrics['structure']['excluded_nonfinite_cases']} excluded.",
        "",
        "## Primary grid results",
        "",
    ]
    for row, boot in zip(metrics["gammas"], bootstrap["gammas"]):
        f = row["functional"]
        o = row["operational"]
        lines.extend(
            [
                f"### gamma = {row['gamma']}",
                "",
                "Functional absolute LAD losses:",
                "",
                "| model | loss | 95% bootstrap interval |",
                "|---|---:|---:|",
            ]
        )
        for name in FUNCTIONAL_MODELS:
            ci = boot["functional"]["grid"]["losses"][name]["interval"]
            lines.append(f"| {name} | {f['models'][name]['loss']:.9g} | {ci} |")
        lines.extend(
            [
                "",
                f"Functional reductions: `{f['comparisons']}`",
                "",
                "Feasible-cost absolute disagreement losses:",
                "",
                "| model | loss | 95% bootstrap interval | active loss | active mass | induced loss | induced-positive |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for name in OPERATIONAL_MODELS:
            summary = o["models"][name]
            ci = boot["operational"]["grid"]["losses"][name]["interval"]
            lines.append(
                f"| {name} | {summary['loss']:.9g} | {ci} | "
                f"{summary['active_loss']:.9g} | {summary['active_mass']:.9g} | "
                f"{summary['induced_loss']:.9g} | {summary['induced_positive']:.9g} |"
            )
        lines.extend(
            [
                "",
                f"Operational reductions: `{o['comparisons']}`",
                "",
                "Active-region W+ quantiles (P50/P90/P99):",
                "",
                *[f"- {name}: {o['models'][name]['active_quantiles']}" for name in OPERATIONAL_MODELS],
                "",
            ]
        )
    lines.extend(
        [
            "## Pre-exposed block",
            "",
            "Configs 76--79 are reported separately as PRE-EXPOSED / NON-HOLDOUT. "
            "Only M0 and frozen primary-global M1 coefficients are evaluated. M2 is omitted "
            "because no exposed M2 coefficient was frozen and refitting is forbidden.",
            "",
            "## Interpretation boundary",
            "",
            "Use the preregistered A/B/C/D logic with absolute scale, bootstrap uncertainty, "
            "active/induced diagnostics, and configuration/trajectory heterogeneity. These "
            "synthetic fixed-grid results do not establish applied routing usefulness or "
            "performance under divergent policies.",
            "",
        ]
    )
    return "\n".join(lines)


def write_bytes(path: Path, payload: bytes) -> None:
    path.write_bytes(payload)


def run(raw_path: Path, calibration_path: Path, output_dir: Path) -> dict:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite locked confirmation output: {output_dir}")
    artifact, calibrations = discovery.load_frozen_discovery_artifact(
        calibration_path, DISCOVERY_SHA256
    )
    if any(calibrations[g].configs != PRIMARY_CONFIGS for g in b2.GAMMAS):
        raise ValueError("frozen discovery calibration grid mismatch")
    raw, audit = load_confirmation_only(raw_path, PRIMARY_CONFIGS)
    counts = b2.bootstrap_multiplicities(10_000)
    if counts.shape != (10_000, 76, 30):
        raise AssertionError("wrong frozen bootstrap replicate count")

    metadata = {
        "schema": "ep001b2.locked-confirmation",
        "schema_version": 1,
        "source_preregistration_commit": discovery.PREREGISTRATION_COMMIT,
        "source_implementation_commit": discovery.IMPLEMENTATION_COMMIT,
        "source_discovery_freeze_commit": DISCOVERY_FREEZE_COMMIT,
        "discovery_calibration_sha256": DISCOVERY_SHA256,
        "confirmation_seeds": list(CONFIRMATION_SEEDS),
        "primary_configs": list(PRIMARY_CONFIGS),
        "excluded_preexposed_configs": list(EXPOSED_CONFIGS),
        "H": 10,
        "gammas": list(b2.GAMMAS),
        "bootstrap_replicates": 10_000,
        "bootstrap_rng": "default_rng(SeedSequence([20260915, group_id]))",
        "scalars_refitted": False,
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "source": audit,
    }
    point_rows, bootstrap_rows, curves, trajectories = [], [], {}, {}
    for gamma in b2.GAMMAS:
        point, boot, gamma_curves, gamma_trajectories = analyze_primary_gamma(
            raw, calibrations[gamma], counts
        )
        point_rows.append(point)
        bootstrap_rows.append({"gamma": gamma, **boot})
        curves.update(gamma_curves)
        trajectories.update(gamma_trajectories)
    trajectories.update(
        config_id=np.asarray(PRIMARY_CONFIGS), seed=np.asarray(CONFIRMATION_SEEDS),
        functional_models=np.asarray(FUNCTIONAL_MODELS), operational_models=np.asarray(OPERATIONAL_MODELS)
    )
    primary_metrics = {"metadata": metadata, "structure": audit, "gammas": point_rows}
    bootstrap = {"metadata": metadata, "gammas": bootstrap_rows}

    output_dir.mkdir(parents=True, exist_ok=False)
    metrics_path = output_dir / "primary_metrics.json"
    bootstrap_path = output_dir / "primary_bootstrap.json"
    curves_path = output_dir / "primary_disagreement_curves.npz"
    trajectory_path = output_dir / "primary_trajectory_metrics.npz"
    write_bytes(metrics_path, json_bytes(primary_metrics))
    write_bytes(bootstrap_path, json_bytes(bootstrap))
    np.savez_compressed(curves_path, **curves)
    np.savez_compressed(trajectory_path, **trajectories)

    # Only after primary output exists, decode and evaluate the non-holdout block.
    exposed_raw, exposed_audit = load_confirmation_only(raw_path, EXPOSED_CONFIGS)
    exposed = {
        "metadata": {**metadata, "status": "PRE-EXPOSED_NON-HOLDOUT"},
        "structure": exposed_audit,
        "gammas": [analyze_exposed_gamma(exposed_raw, calibrations[g]) for g in b2.GAMMAS],
    }
    exposed_path = output_dir / "preexposed_nonholdout_metrics.json"
    write_bytes(exposed_path, json_bytes(exposed))
    report_path = output_dir / "confirmation_report.md"
    report_path.write_text(report_text(primary_metrics, bootstrap, exposed), encoding="utf-8")

    result_files = [metrics_path, bootstrap_path, curves_path, trajectory_path, exposed_path, report_path]
    manifest = {
        "schema": "ep001b2.confirmation-output-manifest",
        "schema_version": 1,
        "metadata": metadata,
        "files": [
            {"path": path.name, "sha256": discovery.sha256_file(path), "bytes": path.stat().st_size}
            for path in result_files
        ],
    }
    manifest_path = output_dir / "confirmation_manifest.json"
    write_bytes(manifest_path, json_bytes(manifest))
    return {
        "output_dir": str(output_dir),
        "manifest": str(manifest_path),
        "files": [str(path) for path in result_files],
        "primary_candidate_cases": audit["candidate_cases"],
        "primary_finite_cases": audit["finite_cases"],
        "bootstrap_replicates": 10_000,
        "scalars_refitted": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--calibration", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    json.dump(run(args.raw, args.calibration, args.output_dir), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
