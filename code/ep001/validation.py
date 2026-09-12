"""Independent checks for the EP001 transported-value experiment.

This module is intentionally small.  It supplies exact moment/operator
calculations for the two-dimensional controls and a common-coupled Monte
Carlo estimator.  It is not the EP001-A experiment runner.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]


@dataclass(frozen=True)
class DeltaEstimate:
    """Monte Carlo means and standard errors for Delta_0, ..., Delta_H."""

    mean: Array
    standard_error: Array


@dataclass(frozen=True)
class ReversalMetrics:
    """Pre-specified EP001 classification for one state/query case."""

    eligible: bool
    k_flip: int | None
    rho_rev: float | None
    robust_reversal: bool


@dataclass(frozen=True)
class TrajectoryReversalSummary:
    """Eligible and robust counts for one independent SGD trajectory."""

    seed: int
    eligible_cases: int
    robust_reversal_cases: int
    robust_reversal_rate: float | None
    contains_robust_reversal: bool


def reversal_metrics(
    deltas: Array,
    numerical_tolerance: float,
    robust_threshold: float = 0.1,
) -> ReversalMetrics:
    """Compute eligibility, first sign flip, and normalized reversal magnitude."""

    deltas = np.asarray(deltas, dtype=float)
    if deltas.ndim != 1 or deltas.size < 2:
        raise ValueError("deltas must contain Delta_0 and at least one later value")
    if numerical_tolerance < 0.0:
        raise ValueError("numerical_tolerance must be nonnegative")
    if robust_threshold < 0.0:
        raise ValueError("robust_threshold must be nonnegative")
    if not np.all(np.isfinite(deltas)):
        raise ValueError("deltas must be finite")
    eligible = bool(deltas[0] > numerical_tolerance)
    if not eligible:
        return ReversalMetrics(False, None, None, False)
    later = deltas[1:]
    negative_indices = np.flatnonzero(later < 0.0)
    k_flip = int(negative_indices[0] + 1) if negative_indices.size else None
    minimum = float(later.min())
    rho_rev = -minimum / float(deltas[0])
    robust = bool(minimum < -numerical_tolerance and rho_rev >= robust_threshold)
    return ReversalMetrics(True, k_flip, rho_rev, robust)


def summarize_trajectory_reversals(
    seeds: Array, eligible: Array, robust_reversal: Array
) -> list[TrajectoryReversalSummary]:
    """Aggregate query cases by seed, the confirmatory independent unit."""

    seeds = np.asarray(seeds)
    eligible = np.asarray(eligible, dtype=bool)
    robust_reversal = np.asarray(robust_reversal, dtype=bool)
    if seeds.ndim != 1 or eligible.shape != seeds.shape or robust_reversal.shape != seeds.shape:
        raise ValueError("seeds, eligible, and robust_reversal must be aligned vectors")
    if np.any(robust_reversal & ~eligible):
        raise ValueError("a robust reversal must be an eligible case")
    summaries: list[TrajectoryReversalSummary] = []
    for seed_value in np.unique(seeds):
        mask = seeds == seed_value
        eligible_count = int(eligible[mask].sum())
        robust_count = int(robust_reversal[mask].sum())
        rate = robust_count / eligible_count if eligible_count else None
        summaries.append(
            TrajectoryReversalSummary(
                seed=int(seed_value),
                eligible_cases=eligible_count,
                robust_reversal_cases=robust_count,
                robust_reversal_rate=rate,
                contains_robust_reversal=robust_count > 0,
            )
        )
    return summaries


def spike_fourth_moments(q: float) -> Array:
    """Return coordinate fourth moments for X=(G, Z_q).

    G is standard normal.  Z_q is zero with probability 1-q and equals
    either sign of q**(-1/2) with probability q/2 each.
    """

    if not 0.0 < q <= 1.0:
        raise ValueError("q must lie in (0, 1]")
    return np.array([3.0, 1.0 / q])


def weighted_fourth_matrix(fourth_moments: Array) -> Array:
    """Return H=E[||X||^2 XX^T] for independent symmetric unit-variance coordinates."""

    fourth_moments = np.asarray(fourth_moments, dtype=float)
    return np.diag(fourth_moments + fourth_moments.size - 1.0)


def sample_inputs(
    rng: np.random.Generator, size: int, distribution: str, q: float | None = None
) -> Array:
    """Sample either the 2-D Gaussian control or the Gaussian-spike family."""

    if distribution == "gaussian":
        return rng.normal(size=(size, 2))
    if distribution != "gaussian_spike" or q is None:
        raise ValueError("use distribution='gaussian' or provide q for 'gaussian_spike'")
    if not 0.0 < q <= 1.0:
        raise ValueError("q must lie in (0, 1]")
    g = rng.normal(size=size)
    active = rng.random(size) < q
    signs = rng.choice(np.array([-1.0, 1.0]), size=size)
    z = active * signs / np.sqrt(q)
    return np.column_stack((g, z))


def fourth_contraction(q_matrix: Array, fourth_moments: Array) -> Array:
    """Compute E[XX^T Q XX^T] for the supported independent-coordinate laws."""

    q_matrix = np.asarray(q_matrix, dtype=float)
    fourth_moments = np.asarray(fourth_moments, dtype=float)
    p = fourth_moments.size
    if q_matrix.shape != (p, p):
        raise ValueError("Q and fourth_moments have incompatible dimensions")
    result = 2.0 * q_matrix.copy()
    trace = float(np.trace(q_matrix))
    for i in range(p):
        result[i, i] = fourth_moments[i] * q_matrix[i, i] + trace - q_matrix[i, i]
    return result


def transported_risk_matrices(
    fourth_moments: Array, eta: float, horizon: int
) -> list[Array]:
    """Compute K_0,...,K_H for the implemented unit-variance input laws."""

    if horizon < 0:
        raise ValueError("horizon must be nonnegative")
    fourth_moments = np.asarray(fourth_moments, dtype=float)
    p = fourth_moments.size
    matrices = [np.eye(p)]
    for _ in range(horizon):
        previous = matrices[-1]
        contraction = fourth_contraction(previous, fourth_moments)
        matrices.append(previous - 2.0 * eta * previous + eta**2 * contraction)
    return matrices


def analytical_deltas(
    error: Array,
    query_input: Array,
    teacher_bias: Array,
    teacher_variance: float,
    eta_teacher: float,
    risk_matrices: list[Array],
) -> Array:
    """Evaluate the Decision 009 formula for Delta_0,...,Delta_H."""

    error = np.asarray(error, dtype=float)
    query_input = np.asarray(query_input, dtype=float)
    teacher_bias = np.asarray(teacher_bias, dtype=float)
    alpha = float(query_input @ error)
    beta = float(query_input @ teacher_bias)
    d = alpha - beta
    return np.array(
        [
            2.0 * eta_teacher * d * (query_input @ k_matrix @ error)
            - eta_teacher**2
            * (d**2 + teacher_variance)
            * (query_input @ k_matrix @ query_input)
            for k_matrix in risk_matrices
        ]
    )


def evolve_sgd_state(
    theta: Array,
    w_star: Array,
    inputs: Array,
    target_noise: Array,
    eta: float,
) -> Array:
    """Evolve theta by ordinary squared-loss SGD and return the resulting state."""

    state = np.asarray(theta, dtype=float).copy()
    w_star = np.asarray(w_star, dtype=float)
    for x, noise in zip(np.asarray(inputs, dtype=float), np.asarray(target_noise, dtype=float)):
        target = float(w_star @ x + noise)
        state += eta * x * (target - state @ x)
    return state


def common_coupled_monte_carlo(
    *,
    error: Array,
    query_input: Array,
    teacher_bias: Array,
    teacher_variance: float,
    eta_teacher: float,
    eta_future: float,
    horizon: int,
    replications: int,
    rng: np.random.Generator,
    distribution: str,
    q: float | None = None,
    target_noise_std: float = 0.0,
) -> DeltaEstimate:
    """Estimate transported values from independently replicated coupled branches."""

    error = np.asarray(error, dtype=float)
    query_input = np.asarray(query_input, dtype=float)
    teacher_bias = np.asarray(teacher_bias, dtype=float)
    alpha = float(query_input @ error)
    beta = float(query_input @ teacher_bias)
    teacher_noise = rng.normal(scale=np.sqrt(teacher_variance), size=replications)
    branch_f = np.broadcast_to(error, (replications, error.size)).copy()
    branch_d = branch_f + eta_teacher * (teacher_noise - (alpha - beta))[:, None] * query_input
    samples = np.empty((replications, horizon + 1), dtype=float)
    samples[:, 0] = (
        np.einsum("ij,ij->i", branch_f, branch_f)
        - np.einsum("ij,ij->i", branch_d, branch_d)
    )
    for step in range(1, horizon + 1):
        x = sample_inputs(rng, replications, distribution, q)
        noise = rng.normal(scale=target_noise_std, size=replications)
        # In error coordinates, a common ordinary-SGD update is
        # e <- e + eta*x*(epsilon - x^T e).
        branch_f += eta_future * x * (noise - np.einsum("ij,ij->i", x, branch_f))[:, None]
        branch_d += eta_future * x * (noise - np.einsum("ij,ij->i", x, branch_d))[:, None]
        samples[:, step] = (
            np.einsum("ij,ij->i", branch_f, branch_f)
            - np.einsum("ij,ij->i", branch_d, branch_d)
        )
    return DeltaEstimate(
        mean=samples.mean(axis=0),
        standard_error=samples.std(axis=0, ddof=1) / np.sqrt(replications),
    )
