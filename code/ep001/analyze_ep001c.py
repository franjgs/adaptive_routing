"""Summarize frozen EP001-C trajectory outputs without fitting any model."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

import analyze_ep001b2 as b2
import run_ep001c as c


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def jsonable(value):
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return jsonable(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    return value


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(jsonable(value), sort_keys=True, indent=2, allow_nan=False) + "\n")


def load_split(trajectory_path: Path, manifest_path: Path, expected_split: str) -> tuple[dict, dict]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        manifest.get("schema") != "ep001c.trajectory-output"
        or manifest.get("split") != expected_split
        or manifest.get("preregistration_sha256") != c.PREREGISTRATION_SHA256
        or manifest.get("rounds") != c.ROUNDS
        or manifest.get("H") != c.HORIZON
        or manifest.get("gammas") != list(c.GAMMAS)
        or manifest.get("configs") != list(c.PRIMARY_CONFIGS)
        or manifest.get("metrics_sha256") != sha256_file(trajectory_path)
        or manifest.get("p2_coefficients_refitted") is not False
        or manifest.get("p3_future_information_used") is not False
    ):
        raise ValueError("EP001-C trajectory output fails its frozen manifest gate")
    with np.load(trajectory_path, allow_pickle=False) as archive:
        raw = {key: archive[key] for key in archive.files}
    expected_seeds = c.DISCOVERY_SEEDS if expected_split == "discovery" else c.CONFIRMATION_SEEDS
    if not (
        np.array_equal(raw["config_id"], np.asarray(c.PRIMARY_CONFIGS))
        and np.array_equal(raw["seed"], np.asarray(expected_seeds))
        and np.array_equal(raw["gamma"], np.asarray(c.GAMMAS))
        and np.array_equal(raw["policy"], np.asarray(c.POLICIES))
        and np.array_equal(raw["pair"], np.asarray(c.PAIR_NAMES))
        and np.array_equal(raw["temporal_segments"], np.asarray(c.TEMPORAL_SEGMENTS))
    ):
        raise ValueError("trajectory output structure violates fixed split/configuration protocol")
    if not all(np.isfinite(raw[name]).all() for name in (
        "objective", "prediction_loss", "query_cost", "queries", "final_risk",
        "segment_objective", "segment_prediction_loss", "segment_query_cost", "segment_queries",
        "disagreements", "mean_state_divergence", "final_state_divergence",
    )):
        raise FloatingPointError("nonfinite EP001-C metric")
    return raw, manifest


def _pairs(values: np.ndarray) -> dict:
    return {
        "P0_minus_P1": float(values[0] - values[1]),
        "P0_minus_P2": float(values[0] - values[2]),
        "P0_minus_P3": float(values[0] - values[3]),
        "P1_minus_P2": float(values[1] - values[2]),
        "P1_minus_P3": float(values[1] - values[3]),
        "P2_minus_P3": float(values[2] - values[3]),
    }


def _interval(values: np.ndarray) -> list[float]:
    return np.quantile(np.asarray(values, dtype=float), (.025, .975), method="linear").tolist()


def point_rows(raw: dict) -> list[dict]:
    rows = []
    for gamma_index, gamma in enumerate(c.GAMMAS):
        for cost_index, cost in enumerate(raw["cost"]):
            def grid(name):
                return raw[name][:, :, gamma_index, cost_index].mean(axis=(0, 1))
            objective = grid("objective")
            prediction = grid("prediction_loss")
            query_cost = grid("query_cost")
            queries = grid("queries") / c.ROUNDS
            risk = grid("final_risk")
            segments = []
            for segment_index, (start, stop) in enumerate(c.TEMPORAL_SEGMENTS):
                length = stop - start
                segment_objective = raw["segment_objective"][:, :, segment_index, gamma_index, cost_index].mean(axis=(0, 1))
                segment_prediction = raw["segment_prediction_loss"][:, :, segment_index, gamma_index, cost_index].mean(axis=(0, 1))
                segment_query = raw["segment_query_cost"][:, :, segment_index, gamma_index, cost_index].mean(axis=(0, 1))
                segment_rate = raw["segment_queries"][:, :, segment_index, gamma_index, cost_index].mean(axis=(0, 1)) / length
                disagreement = raw["disagreements"][:, :, segment_index, gamma_index, cost_index].mean(axis=(0, 1)) / length
                segments.append({
                    "rounds": [start + 1, stop], "objective": segment_objective,
                    "prediction_loss": segment_prediction, "query_cost": segment_query,
                    "query_rate": segment_rate, "disagreement_rate": disagreement,
                })
            first = raw["first_divergence"][:, :, gamma_index, cost_index]
            first_summary = []
            for pair_index in range(len(c.PAIR_NAMES)):
                observed = first[..., pair_index]
                valid = observed[observed >= 0]
                first_summary.append({
                    "fraction_diverged": float(valid.size / observed.size),
                    "median_first_divergence": None if not valid.size else float(np.median(valid)),
                })
            rows.append({
                "gamma": gamma, "cost": float(cost), "objective": objective,
                "objective_pair_differences": _pairs(objective),
                "prediction_loss": prediction, "query_cost": query_cost, "query_rate": queries,
                "final_risk": risk, "temporal_segments": segments,
                "first_divergence": first_summary,
                "mean_state_divergence": raw["mean_state_divergence"][:, :, gamma_index, cost_index].mean(axis=(0, 1)),
                "final_state_divergence": raw["final_state_divergence"][:, :, gamma_index, cost_index].mean(axis=(0, 1)),
            })
    return rows


def bootstrap_rows(raw: dict, replicates: int = 10_000) -> list[dict]:
    if raw["seed"].size != len(c.CONFIRMATION_SEEDS):
        raise ValueError("paired confirmation bootstrap requires seeds 20--49")
    counts = b2.bootstrap_multiplicities(replicates)
    output = []
    for gamma_index, gamma in enumerate(c.GAMMAS):
        for cost_index, cost in enumerate(raw["cost"]):
            table = raw["objective"][:, :, gamma_index, cost_index]
            draws = b2.bootstrap_aggregate(table, counts)["grid"]
            differences = np.column_stack((
                draws[:, 0] - draws[:, 1], draws[:, 0] - draws[:, 2], draws[:, 0] - draws[:, 3],
                draws[:, 1] - draws[:, 2], draws[:, 1] - draws[:, 3], draws[:, 2] - draws[:, 3],
            ))
            output.append({
                "gamma": gamma, "cost": float(cost), "replicates": replicates,
                "objective_policy_ci": {name: _interval(draws[:, index]) for index, name in enumerate(c.POLICIES)},
                "objective_pair_difference_ci": {name: _interval(differences[:, index]) for index, name in enumerate((
                    "P0_minus_P1", "P0_minus_P2", "P0_minus_P3", "P1_minus_P2", "P1_minus_P3", "P2_minus_P3",
                ))},
            })
    return output


def configuration_rows(raw: dict) -> list[dict]:
    rows = []
    for config_index, config_id in enumerate(raw["config_id"]):
        for gamma_index, gamma in enumerate(c.GAMMAS):
            for cost_index, cost in enumerate(raw["cost"]):
                objective = raw["objective"][config_index, :, gamma_index, cost_index].mean(axis=0)
                rows.append({
                    "config_id": int(config_id), "gamma": gamma, "cost": float(cost),
                    "objective": objective, "objective_pair_differences": _pairs(objective),
                })
    return rows


def report_text(summary: dict, split: str) -> str:
    lines = [f"# EP001-C {split} report", "", "Absolute objective values precede paired differences.", ""]
    for row in summary["grid"]:
        objective = row["objective"]
        diff = row["objective_pair_differences"]
        lines.extend([
            f"## gamma={row['gamma']}, C_D={row['cost']:.12g}", "",
            "| policy | J | prediction loss | query cost | query rate | final risk |",
            "|---|---:|---:|---:|---:|---:|",
        ])
        for index, policy in enumerate(c.POLICIES):
            lines.append(
                f"| {policy} | {objective[index]:.9g} | {row['prediction_loss'][index]:.9g} | "
                f"{row['query_cost'][index]:.9g} | {row['query_rate'][index]:.9g} | {row['final_risk'][index]:.9g} |"
            )
        lines.extend(["", f"Paired objective differences (positive favors first policy): `{diff}`", ""])
    lines.extend([
        "## Boundary", "", "This report contains measured outcomes only. It does not classify the C1--C5 logic or make an applied claim.", "",
    ])
    return "\n".join(lines)


def run(trajectory_path: Path, manifest_path: Path, split: str, output_dir: Path) -> dict:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError("refusing to overwrite EP001-C analysis output")
    raw, manifest = load_split(trajectory_path, manifest_path, split)
    summary = {
        "schema": "ep001c.summary", "schema_version": 1, "split": split,
        "trajectory_manifest_sha256": sha256_file(manifest_path),
        "trajectory_metrics_sha256": sha256_file(trajectory_path),
        "preregistration_commit": c.PREREGISTRATION_COMMIT,
        "preregistration_sha256": c.PREREGISTRATION_SHA256,
        "rounds": c.ROUNDS, "H": c.HORIZON, "gammas": list(c.GAMMAS),
        "costs": raw["cost"], "configs": raw["config_id"], "seeds": raw["seed"],
        "policies": list(c.POLICIES), "pairs": list(c.PAIR_NAMES),
        "temporal_segments": [[start + 1, stop] for start, stop in c.TEMPORAL_SEGMENTS],
        "grid": point_rows(raw), "configuration": configuration_rows(raw),
        "p2_coefficients_refitted": False, "p3_future_information_used": False,
    }
    if split == "confirmation":
        summary["bootstrap"] = bootstrap_rows(raw)
    output_dir.mkdir(parents=True, exist_ok=False)
    json_path = output_dir / f"{split}_summary.json"
    write_json(json_path, summary)
    report_path = output_dir / f"{split}_report.md"
    report_path.write_text(report_text(summary, split), encoding="utf-8")
    result = {"summary": json_path.name, "report": report_path.name,
              "summary_sha256": sha256_file(json_path), "report_sha256": sha256_file(report_path)}
    (output_dir / "analysis_manifest.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trajectory", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--split", choices=("discovery", "confirmation"), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.trajectory, args.manifest, args.split, args.output_dir), sort_keys=True))


if __name__ == "__main__":
    main()
