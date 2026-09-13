"""EP001-C paired closed-loop routing experiment.

The runner implements the frozen EP001-C protocol.  It has separate
discovery and confirmation entry points; the latter requires a frozen cost
grid and never fits a coefficient.  P3 is deliberately a receding local
reference-coupled valuation, not a rollout or continuation-value oracle.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np

import analyze_ep001b2 as b2
import run_ep001a as a
import run_ep001b2_discovery as b2_discovery
from validation import transported_risk_matrices


PREREGISTRATION_COMMIT = "505047084bcc331f5eb1159e5cb3eeeacddf04ba"
PREREGISTRATION_SHA256 = "9d5af0f7652bd36e3c05c96a247a3e989df32fa1fb9534ca1900f91c3e1c1d1b"
B2_DISCOVERY_SHA256 = "9e64ee92e45b3925f2babfe847d1d3d04ec6388ea1537d8a6c37f6e3105757a8"
PRIMARY_CONFIGS = tuple(range(76))
DISCOVERY_SEEDS = tuple(range(20))
CONFIRMATION_SEEDS = tuple(range(20, 50))
GAMMAS = (0.5, 0.9, 1.0)
HORIZON = 10
ROUNDS = 2000
DELAY = 5
W_STAR = np.array([1.0, -0.5])
POLICIES = ("P0", "P1", "P2", "P3")
PAIR_NAMES = ("P0_P1", "P0_P2", "P0_P3", "P1_P2", "P1_P3", "P2_P3")
TEMPORAL_SEGMENTS = ((0, 666), (666, 1333), (1333, 2000))
MASTER_SEED = 20260917


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def named_rng(*coordinates: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence((MASTER_SEED, *coordinates)))


def _fourth_moments(config: dict) -> np.ndarray:
    q = config["q"]
    return a.fourth_moments(str(config["distribution"]), q if q is not None else None)


def load_configuration_grid(manifest_path: Path) -> dict[int, dict]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    configurations = manifest.get("configurations", [])
    if [item.get("config_id") for item in configurations] != list(range(80)):
        raise ValueError("unexpected frozen EP001-A configuration grid")
    result = {int(item["config_id"]): item for item in configurations}
    if set(PRIMARY_CONFIGS) - set(result):
        raise ValueError("missing EP001-C primary configuration")
    return result


def load_frozen_b2_calibrations(path: Path) -> dict[float, b2.Calibration]:
    _, calibrations = b2_discovery.load_frozen_discovery_artifact(path, B2_DISCOVERY_SHA256)
    if set(calibrations) != set(GAMMAS) or any(
        calibration.configs != PRIMARY_CONFIGS for calibration in calibrations.values()
    ):
        raise ValueError("frozen B2 calibration grid mismatch")
    return calibrations


def exogenous_stream(config: dict, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate the entire policy-common stream without inspecting its future in routing."""
    if seed not in (*DISCOVERY_SEEDS, *CONFIRMATION_SEEDS):
        raise ValueError("seed outside fixed EP001-C split")
    distribution_index = int(config["distribution_index"])
    eta_index = int(config["eta_index"])
    noise_index = int(config["noise_index"])
    input_rng = named_rng(0, distribution_index, eta_index, noise_index, seed)
    inputs = a.sample_inputs(input_rng, ROUNDS, str(config["distribution"]), config["q"])
    target_noise = named_rng(1, distribution_index, eta_index, noise_index, seed).normal(
        scale=float(config["target_noise_std"]), size=ROUNDS
    )
    teacher_standard_noise = named_rng(2, int(config["config_id"]), seed).normal(size=ROUNDS)
    return inputs, target_noise, teacher_standard_noise


def local_values(
    theta: np.ndarray,
    x: np.ndarray,
    *,
    teacher_variance: float,
    eta_teacher: float,
    gamma: float,
    risk_matrices: list[np.ndarray],
    scalar_c: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return P0/P1/P2/P3 valuations at states shaped [..., 2]."""
    error = theta - W_STAR
    alpha = np.einsum("...i,i->...", error, x)
    delta_now = alpha**2 - teacher_variance
    x_ke = np.einsum("i,kij,...j->...k", x, np.stack(risk_matrices[:HORIZON]), error)
    x_kx = np.einsum("i,kij,j->k", x, np.stack(risk_matrices[:HORIZON]), x)
    deltas = (
        2.0 * eta_teacher * alpha[..., None] * x_ke
        - eta_teacher**2 * (alpha[..., None] ** 2 + teacher_variance) * x_kx
    )
    powers = gamma ** np.arange(HORIZON)
    delta_static = float(powers.sum()) * deltas[..., 0]
    delta_ref = np.einsum("...k,k->...", deltas, powers)
    return (
        delta_now,
        delta_now + gamma * delta_static,
        delta_now + gamma * scalar_c * delta_static,
        delta_now + gamma * delta_ref,
    )


def policy_actions(
    theta: np.ndarray,
    x: np.ndarray,
    costs: np.ndarray,
    *, teacher_variance: float, eta_teacher: float, gamma: float,
    risk_matrices: list[np.ndarray], scalar_c: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply the four frozen strict decision rules without future information."""
    theta = np.asarray(theta, dtype=float)
    costs = np.asarray(costs, dtype=float)
    if theta.ndim != 3 or theta.shape[0] != len(POLICIES) or theta.shape[2] != 2:
        raise ValueError("theta must be [policy, cost, parameter]")
    if costs.shape != (theta.shape[1],):
        raise ValueError("costs must align with theta cost axis")
    valuation_by_rule = local_values(
        theta, x, teacher_variance=teacher_variance, eta_teacher=eta_teacher,
        gamma=gamma, risk_matrices=risk_matrices, scalar_c=scalar_c,
    )
    values = np.stack(
        [valuation_by_rule[policy_index][policy_index] for policy_index in range(len(POLICIES))]
    )
    return values > costs[None, :], values


def temporal_segment(t_zero_based: int) -> int:
    for index, (start, stop) in enumerate(TEMPORAL_SEGMENTS):
        if start <= t_zero_based < stop:
            return index
    raise ValueError("round outside frozen temporal thirds")


def feedback_due_index(round_index: int) -> int | None:
    """Zero-based source round whose reliable feedback is revealed after this response."""
    due = round_index - DELAY
    return due if due >= 0 else None


def pseudo_update(theta: np.ndarray, x: np.ndarray, d_response: float, eta_teacher: float) -> np.ndarray:
    """The query-side update uses exactly the operational D response."""
    return np.asarray(theta, dtype=float) + eta_teacher * x * (d_response - np.asarray(theta) @ x)


def simulate_one(
    config: dict,
    seed: int,
    costs: np.ndarray,
    calibrations: dict[float, b2.Calibration],
) -> dict[str, np.ndarray]:
    """Simulate all gamma/cost/policy cells for one paired exogenous trajectory."""
    costs = np.asarray(costs, dtype=float)
    if costs.ndim != 1 or not costs.size or np.any(costs < 0) or not np.isfinite(costs).all():
        raise ValueError("cost grid must be finite, nonnegative, and nonempty")
    if seed not in (*DISCOVERY_SEEDS, *CONFIRMATION_SEEDS):
        raise ValueError("seed split violation")
    inputs, target_noise, teacher_noise = exogenous_stream(config, seed)
    eta = float(config["eta"])
    eta_teacher = float(config["eta_teacher"])
    teacher_variance = float(config["teacher_variance"])
    risk_matrices = transported_risk_matrices(_fourth_moments(config), eta, HORIZON)
    g_count, p_count, c_count = len(GAMMAS), len(POLICIES), len(costs)
    theta = np.zeros((g_count, p_count, c_count, 2), dtype=float)
    objective = np.zeros((g_count, c_count, p_count), dtype=float)
    prediction = np.zeros_like(objective)
    query_cost = np.zeros_like(objective)
    queries = np.zeros_like(objective)
    segment_objective = np.zeros((3, g_count, c_count, p_count), dtype=float)
    segment_prediction = np.zeros_like(segment_objective)
    segment_query_cost = np.zeros_like(segment_objective)
    segment_queries = np.zeros_like(segment_objective)
    disagreements = np.zeros((3, g_count, c_count, len(PAIR_NAMES)), dtype=float)
    first_divergence = np.full((g_count, c_count, len(PAIR_NAMES)), -1, dtype=np.int16)
    state_divergence_sum = np.zeros((g_count, c_count, len(PAIR_NAMES)), dtype=float)
    pair_indices = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))

    for round_index, x in enumerate(inputs):
        y = float(W_STAR @ x + target_noise[round_index])
        d_response = float(W_STAR @ x + np.sqrt(teacher_variance) * teacher_noise[round_index])
        discount = np.asarray(GAMMAS, dtype=float) ** round_index
        segment = temporal_segment(round_index)
        for gamma_index, gamma in enumerate(GAMMAS):
            c_scalar = calibrations[gamma].config_o[int(config["config_id"])].c
            action, _ = policy_actions(
                theta[gamma_index], x, costs, teacher_variance=teacher_variance,
                eta_teacher=eta_teacher, gamma=gamma, risk_matrices=risk_matrices,
                scalar_c=c_scalar,
            )
            pred = np.einsum("pci,i->pc", theta[gamma_index], x)
            squared_loss = np.where(action, (d_response - y) ** 2, (pred - y) ** 2)
            query_component = action * costs[None, :]
            weighted_prediction = discount[gamma_index] * squared_loss.T
            weighted_query = discount[gamma_index] * query_component.T
            prediction[gamma_index] += weighted_prediction
            query_cost[gamma_index] += weighted_query
            objective[gamma_index] += weighted_prediction + weighted_query
            queries[gamma_index] += action.T
            segment_prediction[segment, gamma_index] += weighted_prediction
            segment_query_cost[segment, gamma_index] += weighted_query
            segment_objective[segment, gamma_index] += weighted_prediction + weighted_query
            segment_queries[segment, gamma_index] += action.T
            for pair_index, (left, right) in enumerate(pair_indices):
                different = action[left] != action[right]
                disagreements[segment, gamma_index, :, pair_index] += different
                unseen = (first_divergence[gamma_index, :, pair_index] < 0) & different
                first_divergence[gamma_index, unseen, pair_index] = round_index + 1
            pseudo = eta_teacher * x[None, None, :] * (d_response - pred)[..., None]
            theta[gamma_index] += action[..., None] * pseudo
            due = feedback_due_index(round_index)
            if due is not None:
                x_due = inputs[due]
                y_due = float(W_STAR @ x_due + target_noise[due])
                feedback_prediction = np.einsum("pci,i->pc", theta[gamma_index], x_due)
                theta[gamma_index] += eta * x_due[None, None, :] * (
                    y_due - feedback_prediction
                )[..., None]
            for pair_index, (left, right) in enumerate(pair_indices):
                state_divergence_sum[gamma_index, :, pair_index] += np.linalg.norm(
                    theta[gamma_index, left] - theta[gamma_index, right], axis=1
                )

    final_risk = np.sum((theta - W_STAR) ** 2, axis=-1).transpose(0, 2, 1)
    final_divergence = np.empty((g_count, c_count, len(PAIR_NAMES)), dtype=float)
    for pair_index, (left, right) in enumerate(pair_indices):
        final_divergence[:, :, pair_index] = np.linalg.norm(
            theta[:, left] - theta[:, right], axis=-1
        )
    return {
        "objective": objective,
        "prediction_loss": prediction,
        "query_cost": query_cost,
        "queries": queries,
        "final_risk": final_risk,
        "segment_objective": segment_objective,
        "segment_prediction_loss": segment_prediction,
        "segment_query_cost": segment_query_cost,
        "segment_queries": segment_queries,
        "disagreements": disagreements,
        "first_divergence": first_divergence,
        "mean_state_divergence": state_divergence_sum / ROUNDS,
        "final_state_divergence": final_divergence,
    }


def discovery_cost_candidates(configs: dict[int, dict], calibrations: dict[float, b2.Calibration]) -> np.ndarray:
    """Discovery-only reference valuations along the no-query feedback trajectory.

    This implements the predeclared cost-grid rule: use the positive pooled
    P0/P1/P2/P3 valuation quantiles (10,25,50,75,90,99) plus zero and a
    discovery-maximum high-cost endpoint.  It never uses confirmation data.
    """
    values: list[np.ndarray] = []
    for config_id in PRIMARY_CONFIGS:
        config = configs[config_id]
        eta = float(config["eta"])
        eta_teacher = float(config["eta_teacher"])
        teacher_variance = float(config["teacher_variance"])
        risk_matrices = transported_risk_matrices(_fourth_moments(config), eta, HORIZON)
        for seed in DISCOVERY_SEEDS:
            inputs, noise, _ = exogenous_stream(config, seed)
            theta = np.zeros(2, dtype=float)
            for round_index, x in enumerate(inputs):
                for gamma in GAMMAS:
                    scalar = calibrations[gamma].config_o[config_id].c
                    values.append(np.stack(local_values(
                        theta, x, teacher_variance=teacher_variance, eta_teacher=eta_teacher,
                        gamma=gamma, risk_matrices=risk_matrices, scalar_c=scalar,
                    )))
                due = round_index - DELAY
                if due >= 0:
                    x_due = inputs[due]
                    y_due = float(W_STAR @ x_due + noise[due])
                    theta += eta * x_due * (y_due - theta @ x_due)
    positive = np.concatenate(values).reshape(-1)
    positive = positive[np.isfinite(positive) & (positive > 0)]
    if not positive.size:
        raise RuntimeError("discovery has no positive valuation for a cost grid")
    quantile_values = np.quantile(positive, (0.10, 0.25, 0.50, 0.75, 0.90, 0.99))
    return np.unique(np.r_[0.0, quantile_values, positive.max() * 1.01])


def write_cost_grid(output_dir: Path, costs: np.ndarray) -> Path:
    output_dir.mkdir(parents=True, exist_ok=False)
    artifact = {
        "schema": "ep001c.discovery-cost-grid",
        "schema_version": 1,
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "preregistration_sha256": PREREGISTRATION_SHA256,
        "split": "discovery",
        "seeds": list(DISCOVERY_SEEDS),
        "configs": list(PRIMARY_CONFIGS),
        "selection_rule": "positive pooled no-query reference-trajectory P0/P1/P2/P3 valuation quantiles 10,25,50,75,90,99; include 0 and 1.01 times discovery maximum",
        "costs": [float(value) for value in costs],
        "rounds": ROUNDS,
        "H": HORIZON,
        "gammas": list(GAMMAS),
    }
    path = output_dir / "cost_grid.json"
    path.write_bytes(json_bytes(artifact))
    return path


def load_cost_grid(path: Path) -> np.ndarray:
    artifact = json.loads(path.read_text(encoding="utf-8"))
    if (
        artifact.get("schema") != "ep001c.discovery-cost-grid"
        or artifact.get("preregistration_sha256") != PREREGISTRATION_SHA256
        or artifact.get("split") != "discovery"
        or artifact.get("seeds") != list(DISCOVERY_SEEDS)
        or artifact.get("configs") != list(PRIMARY_CONFIGS)
        or artifact.get("rounds") != ROUNDS
        or artifact.get("H") != HORIZON
        or artifact.get("gammas") != list(GAMMAS)
    ):
        raise ValueError("cost grid does not satisfy frozen EP001-C gate")
    costs = np.asarray(artifact["costs"], dtype=float)
    if not np.all(np.diff(costs) > 0) or costs[0] != 0 or np.any(costs < 0):
        raise ValueError("invalid frozen cost grid")
    return costs


def run_split(
    *, configs: dict[int, dict], calibrations: dict[float, b2.Calibration], costs: np.ndarray,
    seeds: tuple[int, ...], split: str, output_dir: Path, cost_grid_path: Path,
) -> dict:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite EP001-C {split} output")
    if split == "discovery" and seeds != DISCOVERY_SEEDS:
        raise ValueError("discovery must use only seeds 0--19")
    if split == "confirmation" and seeds != CONFIRMATION_SEEDS:
        raise ValueError("confirmation must use only seeds 20--49")
    n_config, n_seed, n_gamma, n_cost, n_policy = (
        len(PRIMARY_CONFIGS), len(seeds), len(GAMMAS), len(costs), len(POLICIES)
    )
    shapes = {
        "objective": (n_config, n_seed, n_gamma, n_cost, n_policy),
        "prediction_loss": (n_config, n_seed, n_gamma, n_cost, n_policy),
        "query_cost": (n_config, n_seed, n_gamma, n_cost, n_policy),
        "queries": (n_config, n_seed, n_gamma, n_cost, n_policy),
        "final_risk": (n_config, n_seed, n_gamma, n_cost, n_policy),
        "segment_objective": (n_config, n_seed, 3, n_gamma, n_cost, n_policy),
        "segment_prediction_loss": (n_config, n_seed, 3, n_gamma, n_cost, n_policy),
        "segment_query_cost": (n_config, n_seed, 3, n_gamma, n_cost, n_policy),
        "segment_queries": (n_config, n_seed, 3, n_gamma, n_cost, n_policy),
        "disagreements": (n_config, n_seed, 3, n_gamma, n_cost, len(PAIR_NAMES)),
        "first_divergence": (n_config, n_seed, n_gamma, n_cost, len(PAIR_NAMES)),
        "mean_state_divergence": (n_config, n_seed, n_gamma, n_cost, len(PAIR_NAMES)),
        "final_state_divergence": (n_config, n_seed, n_gamma, n_cost, len(PAIR_NAMES)),
    }
    storage = {name: np.empty(shape, dtype=np.int16 if name == "first_divergence" else float)
               for name, shape in shapes.items()}
    for c_index, config_id in enumerate(PRIMARY_CONFIGS):
        for s_index, seed in enumerate(seeds):
            result = simulate_one(configs[config_id], seed, costs, calibrations)
            for name in storage:
                storage[name][c_index, s_index] = result[name]
    output_dir.mkdir(parents=True, exist_ok=False)
    metrics_path = output_dir / f"{split}_trajectory_metrics.npz"
    np.savez_compressed(
        metrics_path,
        **storage,
        config_id=np.asarray(PRIMARY_CONFIGS, dtype=np.int16),
        seed=np.asarray(seeds, dtype=np.int16),
        gamma=np.asarray(GAMMAS),
        cost=np.asarray(costs),
        policy=np.asarray(POLICIES),
        pair=np.asarray(PAIR_NAMES),
        temporal_segments=np.asarray(TEMPORAL_SEGMENTS, dtype=np.int16),
    )
    manifest = {
        "schema": "ep001c.trajectory-output",
        "schema_version": 1,
        "split": split,
        "seeds": list(seeds),
        "configs": list(PRIMARY_CONFIGS),
        "rounds": ROUNDS,
        "delay": DELAY,
        "H": HORIZON,
        "gammas": list(GAMMAS),
        "cost_grid_path": str(cost_grid_path),
        "cost_grid_sha256": sha256_file(cost_grid_path),
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "preregistration_sha256": PREREGISTRATION_SHA256,
        "b2_discovery_sha256": B2_DISCOVERY_SHA256,
        "policies": list(POLICIES),
        "pairing": "all policies share inputs, target noise, teacher noise, and delayed-feedback schedule within config/seed",
        "p2_coefficients_refitted": False,
        "p3_future_information_used": False,
        "metrics_file": metrics_path.name,
        "metrics_sha256": sha256_file(metrics_path),
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
    }
    manifest_path = output_dir / f"{split}_manifest.json"
    manifest_path.write_bytes(json_bytes(manifest))
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    grid = subparsers.add_parser("select-cost-grid")
    grid.add_argument("--ep001a-manifest", type=Path, required=True)
    grid.add_argument("--b2-calibration", type=Path, required=True)
    grid.add_argument("--output-dir", type=Path, required=True)
    simulation = subparsers.add_parser("run-split")
    simulation.add_argument("--split", choices=("discovery", "confirmation"), required=True)
    simulation.add_argument("--ep001a-manifest", type=Path, required=True)
    simulation.add_argument("--b2-calibration", type=Path, required=True)
    simulation.add_argument("--cost-grid", type=Path, required=True)
    simulation.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    configs = load_configuration_grid(args.ep001a_manifest)
    calibrations = load_frozen_b2_calibrations(args.b2_calibration)
    if args.command == "select-cost-grid":
        costs = discovery_cost_candidates(configs, calibrations)
        path = write_cost_grid(args.output_dir, costs)
        print(json.dumps({"cost_grid": str(path), "sha256": sha256_file(path), "costs": costs.tolist()}))
        return
    costs = load_cost_grid(args.cost_grid)
    seeds = DISCOVERY_SEEDS if args.split == "discovery" else CONFIRMATION_SEEDS
    result = run_split(
        configs=configs, calibrations=calibrations, costs=costs, seeds=seeds,
        split=args.split, output_dir=args.output_dir, cost_grid_path=args.cost_grid,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
