"""Run the pre-specified EP001-A oracle experiment without routing policies."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

from validation import (
    reversal_metrics,
    sample_inputs,
    spike_fourth_moments,
    transported_risk_matrices,
)


MASTER_SEED = 20260913
DISCOVERY_SEEDS = tuple(range(20))
CONFIRMATION_SEEDS = tuple(range(20, 50))
CHECKPOINTS = (5, 20, 100, 500, 2000)
QUERY_COUNT = 64
HORIZON = 10
DELAY = 5
W_STAR = np.array([1.0, -0.5])
THETA_ZERO = np.zeros(2)
FUTURE_STEPS = (0.02, 0.05)
PSEUDO_STEPS = (0.02, 0.05)
TARGET_NOISE_STDS = (0.0, 0.1)
TEACHER_VARIANCES = (0.01, 0.05)
DISTRIBUTIONS = (
    ("gaussian", None, "gaussian"),
    ("gaussian_spike", 1.0 / 6.0, "spike_q_1_6"),
    ("gaussian_spike", 1.0 / 3.0, "spike_q_1_3"),
    ("gaussian_spike", 1.0 / 2.0, "spike_q_1_2"),
    ("gaussian_spike", 1.0, "spike_q_1"),
)


def rng_for(*coordinates: int) -> np.random.Generator:
    """Create a deterministic named random stream from fixed integer coordinates."""

    return np.random.default_rng(np.random.SeedSequence((MASTER_SEED, *coordinates)))


def fourth_moments(distribution: str, q: float | None) -> np.ndarray:
    if distribution == "gaussian":
        return np.array([3.0, 3.0])
    if distribution == "gaussian_spike" and q is not None:
        return spike_fourth_moments(q)
    raise ValueError("unknown distribution specification")


def split_for(seed: int) -> int:
    if seed in DISCOVERY_SEEDS:
        return 0
    if seed in CONFIRMATION_SEEDS:
        return 1
    raise ValueError("seed is outside the fixed EP001 split")


def delayed_sgd_checkpoints(
    *,
    distribution: str,
    q: float | None,
    eta: float,
    target_noise_std: float,
    seed: int,
    distribution_index: int,
    eta_index: int,
    noise_index: int,
) -> tuple[dict[int, tuple[np.ndarray, int]], np.ndarray]:
    """Generate the natural delayed-feedback trajectory and requested states.

    A checkpoint is recorded before its operational response.  Updates on a
    reliable target from round t are applied after the response at t + DELAY.
    """

    max_updates = max(CHECKPOINTS)
    total_rounds = DELAY + max_updates + 1
    trajectory_rng = rng_for(0, distribution_index, eta_index, noise_index, seed)
    inputs = sample_inputs(trajectory_rng, total_rounds, distribution, q)
    target_noise = trajectory_rng.normal(scale=target_noise_std, size=total_rounds)
    theta = THETA_ZERO.copy()
    applied_updates = 0
    checkpoints: dict[int, tuple[np.ndarray, int]] = {}
    for operational_round in range(1, total_rounds + 1):
        if applied_updates in CHECKPOINTS and applied_updates not in checkpoints:
            checkpoints[applied_updates] = (theta.copy(), operational_round)
        due_index = operational_round - DELAY - 1
        if due_index >= 0:
            x_due = inputs[due_index]
            y_due = float(W_STAR @ x_due + target_noise[due_index])
            theta += eta * x_due * (y_due - theta @ x_due)
            applied_updates += 1
    if set(checkpoints) != set(CHECKPOINTS):
        raise RuntimeError("delayed trajectory did not reach every checkpoint")
    return checkpoints, inputs


def vectorized_deltas(
    *,
    error: np.ndarray,
    query_inputs: np.ndarray,
    eta_teacher: float,
    teacher_variance: float,
    risk_matrices: list[np.ndarray],
) -> np.ndarray:
    """Evaluate Delta_0,...,Delta_H for all query inputs with b=0."""

    alpha = query_inputs @ error
    k_stack = np.stack(risk_matrices)
    x_ke = np.einsum("ni,kij,j->nk", query_inputs, k_stack, error)
    x_kx = np.einsum("ni,kij,nj->nk", query_inputs, k_stack, query_inputs)
    return (
        2.0 * eta_teacher * alpha[:, None] * x_ke
        - eta_teacher**2 * (alpha[:, None] ** 2 + teacher_variance) * x_kx
    )


def append_rows(
    storage: dict[str, list[np.ndarray]],
    *,
    config_id: int,
    seed: int,
    split: int,
    checkpoint: int,
    operational_round: int,
    error: np.ndarray,
    query_inputs: np.ndarray,
    eta_teacher: float,
    teacher_variance: float,
    risk_matrices: list[np.ndarray],
) -> None:
    deltas = vectorized_deltas(
        error=error,
        query_inputs=query_inputs,
        eta_teacher=eta_teacher,
        teacher_variance=teacher_variance,
        risk_matrices=risk_matrices,
    )
    risk = float(error @ error)
    tolerance = 1e-6 * (1.0 + risk)
    alpha = query_inputs @ error
    metrics = [reversal_metrics(row, tolerance) for row in deltas]
    n_rows = query_inputs.shape[0]
    storage["config_id"].append(np.full(n_rows, config_id, dtype=np.int16))
    storage["seed"].append(np.full(n_rows, seed, dtype=np.int16))
    storage["split"].append(np.full(n_rows, split, dtype=np.int8))
    storage["checkpoint"].append(np.full(n_rows, checkpoint, dtype=np.int16))
    storage["operational_round"].append(np.full(n_rows, operational_round, dtype=np.int16))
    storage["error_norm"].append(np.full(n_rows, np.linalg.norm(error), dtype=float))
    storage["risk"].append(np.full(n_rows, risk, dtype=float))
    storage["query_id"].append(np.arange(n_rows, dtype=np.int16))
    storage["query_input"].append(query_inputs)
    storage["delta_now"].append(alpha**2 - teacher_variance)
    storage["deltas"].append(deltas)
    storage["numerical_tolerance"].append(np.full(n_rows, tolerance, dtype=float))
    storage["eligible"].append(np.array([item.eligible for item in metrics], dtype=bool))
    storage["k_flip"].append(
        np.array([-1 if item.k_flip is None else item.k_flip for item in metrics], dtype=np.int8)
    )
    storage["rho_rev"].append(
        np.array(
            [np.nan if item.rho_rev is None else item.rho_rev for item in metrics],
            dtype=float,
        )
    )
    storage["robust_reversal"].append(
        np.array([item.robust_reversal for item in metrics], dtype=bool)
    )


def build_configurations() -> list[dict[str, object]]:
    configurations: list[dict[str, object]] = []
    config_id = 0
    for distribution_index, (distribution, q, label) in enumerate(DISTRIBUTIONS):
        for eta_index, eta in enumerate(FUTURE_STEPS):
            for noise_index, target_noise_std in enumerate(TARGET_NOISE_STDS):
                for eta_teacher in PSEUDO_STEPS:
                    for teacher_variance in TEACHER_VARIANCES:
                        configurations.append(
                            {
                                "config_id": config_id,
                                "distribution": distribution,
                                "q": q,
                                "label": label,
                                "distribution_index": distribution_index,
                                "eta": eta,
                                "eta_index": eta_index,
                                "eta_teacher": eta_teacher,
                                "target_noise_std": target_noise_std,
                                "noise_index": noise_index,
                                "teacher_variance": teacher_variance,
                                "is_isotropic_control": distribution == "gaussian"
                                or q == 1.0 / 3.0,
                            }
                        )
                        config_id += 1
    return configurations


def run(output_dir: Path) -> dict[str, object]:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite preserved first-run output: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    configurations = build_configurations()
    storage: dict[str, list[np.ndarray]] = {
        key: []
        for key in (
            "config_id",
            "seed",
            "split",
            "checkpoint",
            "operational_round",
            "error_norm",
            "risk",
            "query_id",
            "query_input",
            "delta_now",
            "deltas",
            "numerical_tolerance",
            "eligible",
            "k_flip",
            "rho_rev",
            "robust_reversal",
        )
    }
    start = time.perf_counter()
    base_cache: dict[tuple[int, int, int, int], tuple[dict[int, tuple[np.ndarray, int]], np.ndarray]] = {}
    for config in configurations:
        distribution_index = int(config["distribution_index"])
        eta_index = int(config["eta_index"])
        noise_index = int(config["noise_index"])
        distribution = str(config["distribution"])
        q = config["q"]
        eta = float(config["eta"])
        risk_matrices = transported_risk_matrices(
            fourth_moments(distribution, q if isinstance(q, float) else None),
            eta,
            HORIZON,
        )
        for seed in (*DISCOVERY_SEEDS, *CONFIRMATION_SEEDS):
            cache_key = (distribution_index, eta_index, noise_index, seed)
            if cache_key not in base_cache:
                base_cache[cache_key] = delayed_sgd_checkpoints(
                    distribution=distribution,
                    q=q if isinstance(q, float) else None,
                    eta=eta,
                    target_noise_std=float(config["target_noise_std"]),
                    seed=seed,
                    distribution_index=distribution_index,
                    eta_index=eta_index,
                    noise_index=noise_index,
                )
            checkpoints, _ = base_cache[cache_key]
            evaluation_rng = rng_for(1, distribution_index, eta_index, noise_index, seed)
            query_sets = {
                checkpoint: sample_inputs(
                    evaluation_rng,
                    QUERY_COUNT,
                    distribution,
                    q if isinstance(q, float) else None,
                )
                for checkpoint in CHECKPOINTS
            }
            for checkpoint, (theta, operational_round) in checkpoints.items():
                append_rows(
                    storage,
                    config_id=int(config["config_id"]),
                    seed=seed,
                    split=split_for(seed),
                    checkpoint=checkpoint,
                    operational_round=operational_round,
                    error=theta - W_STAR,
                    query_inputs=query_sets[checkpoint],
                    eta_teacher=float(config["eta_teacher"]),
                    teacher_variance=float(config["teacher_variance"]),
                    risk_matrices=risk_matrices,
                )
    raw = {key: np.concatenate(value) for key, value in storage.items()}
    raw_path = output_dir / "raw_ep001a.npz"
    np.savez_compressed(raw_path, **raw)
    control_ids = {
        int(config["config_id"])
        for config in configurations
        if bool(config["is_isotropic_control"])
    }
    control_mask = np.isin(raw["config_id"], list(control_ids)) & raw["eligible"]
    control_violation = bool(
        np.any(
            np.min(raw["deltas"][control_mask, 1:], axis=1)
            < -raw["numerical_tolerance"][control_mask]
        )
    ) if np.any(control_mask) else False
    report = {
        "plan": "EP001-A",
        "master_seed": MASTER_SEED,
        "runtime_seconds": time.perf_counter() - start,
        "raw_file": raw_path.name,
        "row_count": int(raw["seed"].size),
        "configurations": configurations,
        "validation": {
            "operator_control_scalar": True,
            "isotropic_control_expected_reversal_violation": control_violation,
            "interpretation_allowed": not control_violation,
            "note": "Monte Carlo/operator agreement is validated by the fixed unit tests.",
        },
    }
    (output_dir / "run_manifest.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/ep001/first_run_001"),
        help="empty directory in which raw first-run output will be preserved",
    )
    args = parser.parse_args()
    report = run(args.output)
    print(json.dumps(report["validation"], sort_keys=True))
    print(f"rows={report['row_count']} runtime_seconds={report['runtime_seconds']:.3f}")


if __name__ == "__main__":
    main()
