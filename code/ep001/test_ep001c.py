"""Synthetic unit checks for the frozen EP001-C closed-loop protocol."""
from __future__ import annotations

import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np

import analyze_ep001b2 as b2
import run_ep001c as c
from validation import transported_risk_matrices


def synthetic_config(config_id: int = 0) -> dict:
    return {
        "config_id": config_id, "distribution": "gaussian", "q": None,
        "distribution_index": 0, "eta_index": 0, "noise_index": 0,
        "eta": 0.02, "eta_teacher": 0.05, "target_noise_std": 0.1,
        "teacher_variance": 0.01,
    }


def synthetic_calibrations() -> dict[float, b2.Calibration]:
    configs = tuple(range(76))
    fit = b2.ScalarFit(0.8, 0.0, ((0.8, 0.8),), "synthetic")
    fits = tuple(fit for _ in configs)
    return {
        gamma: b2.Calibration(gamma, configs, fit, fit, fits, fits, fit, fits, fit, fit, fits, fits)
        for gamma in c.GAMMAS
    }


class EP001CProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = synthetic_config()
        self.costs = np.array([0.0, 1000.0])
        self.calibrations = synthetic_calibrations()
        self.risk = transported_risk_matrices(np.array([3.0, 3.0]), 0.02, c.HORIZON)

    def test_temporal_thirds_are_exactly_frozen(self) -> None:
        self.assertEqual(c.TEMPORAL_SEGMENTS, ((0, 666), (666, 1333), (1333, 2000)))
        self.assertEqual([stop - start for start, stop in c.TEMPORAL_SEGMENTS], [666, 667, 667])
        self.assertEqual(c.temporal_segment(0), 0)
        self.assertEqual(c.temporal_segment(665), 0)
        self.assertEqual(c.temporal_segment(666), 1)
        self.assertEqual(c.temporal_segment(1332), 1)
        self.assertEqual(c.temporal_segment(1333), 2)
        self.assertEqual(c.temporal_segment(1999), 2)
        with self.assertRaises(ValueError):
            c.temporal_segment(2000)

    def test_delayed_feedback_timing(self) -> None:
        self.assertIsNone(c.feedback_due_index(0))
        self.assertIsNone(c.feedback_due_index(c.DELAY - 1))
        self.assertEqual(c.feedback_due_index(c.DELAY), 0)
        self.assertEqual(c.feedback_due_index(c.DELAY + 1), 1)

    def test_d_response_is_current_output_and_pseudo_supervision(self) -> None:
        theta = np.array([0.2, -0.4])
        x = np.array([1.0, 2.0])
        d_response = 1.7
        updated = c.pseudo_update(theta, x, d_response, 0.05)
        np.testing.assert_allclose(updated, theta + 0.05 * x * (d_response - theta @ x))

    def test_p0_p1_p2_p3_rules_and_strict_cost_inequality(self) -> None:
        theta = np.broadcast_to(np.array([0.4, -0.1]), (4, 2, 2)).copy()
        x = np.array([1.0, -0.5])
        actions, values = c.policy_actions(
            theta, x, np.array([0.0, 1e9]), teacher_variance=0.01,
            eta_teacher=0.05, gamma=0.9, risk_matrices=self.risk, scalar_c=0.8,
        )
        self.assertEqual(actions.shape, (4, 2))
        np.testing.assert_array_equal(actions[:, 0], values[:, 0] > 0.0)
        self.assertFalse(actions[:, 1].any())
        alpha = float((theta[0, 0] - c.W_STAR) @ x)
        self.assertAlmostEqual(values[0, 0], alpha**2 - 0.01)

    def test_p3_is_reference_coupled_and_not_future_dependent(self) -> None:
        theta = np.broadcast_to(np.array([0.3, 0.1]), (4, 1, 2)).copy()
        x = np.array([0.7, -1.2])
        first_actions, first_values = c.policy_actions(
            theta, x, np.array([0.1]), teacher_variance=0.05,
            eta_teacher=0.02, gamma=0.9, risk_matrices=self.risk, scalar_c=0.8,
        )
        # A different hypothetical future stream cannot enter this local function.
        second_actions, second_values = c.policy_actions(
            theta, x, np.array([0.1]), teacher_variance=0.05,
            eta_teacher=0.02, gamma=0.9, risk_matrices=self.risk, scalar_c=0.8,
        )
        np.testing.assert_array_equal(first_actions, second_actions)
        np.testing.assert_allclose(first_values, second_values)
        error = theta[3, 0] - c.W_STAR
        alpha = x @ error
        deltas = np.array([
            2 * .02 * alpha * (x @ k @ error) - .02**2 * (alpha**2 + .05) * (x @ k @ x)
            for k in self.risk[:10]
        ])
        self.assertAlmostEqual(first_values[3, 0], alpha**2 - .05 + .9 * (deltas @ (.9 ** np.arange(10))))

    def test_exogenous_stream_is_reproducible_and_routing_independent(self) -> None:
        first = c.exogenous_stream(self.config, 0)
        second = c.exogenous_stream(self.config, 0)
        for left, right in zip(first, second):
            np.testing.assert_array_equal(left, right)
        different = c.exogenous_stream(self.config, 1)
        self.assertFalse(np.array_equal(first[0], different[0]))

    def test_paired_simulation_objective_and_endogenous_divergence(self) -> None:
        # Short synthetic execution only; the production constant remains frozen at 2000.
        with patch.object(c, "ROUNDS", 8):
            result = c.simulate_one(self.config, 0, self.costs, self.calibrations)
        np.testing.assert_allclose(
            result["objective"], result["prediction_loss"] + result["query_cost"]
        )
        self.assertTrue(np.all(result["queries"] >= 0))
        self.assertTrue(np.all(result["queries"][:, 1] == 0))
        self.assertEqual(result["first_divergence"].shape[-1], len(c.PAIR_NAMES))

    def test_discovery_confirmation_isolation(self) -> None:
        with self.assertRaises(ValueError):
            c.run_split(
                configs={0: self.config}, calibrations=self.calibrations, costs=self.costs,
                seeds=c.CONFIRMATION_SEEDS, split="discovery", output_dir=Path("/tmp/never"),
                cost_grid_path=Path("/tmp/never-grid"),
            )

    def test_discovery_cost_grid_is_deterministic_and_nonnegative(self) -> None:
        configs = {index: synthetic_config(index) for index in range(76)}
        with patch.object(c, "ROUNDS", 8):
            first = c.discovery_cost_candidates(configs, self.calibrations)
            second = c.discovery_cost_candidates(configs, self.calibrations)
        np.testing.assert_array_equal(first, second)
        self.assertEqual(first[0], 0.0)
        self.assertTrue(np.all(np.diff(first) > 0))
        with self.assertRaises(ValueError):
            c.run_split(
                configs={0: self.config}, calibrations=self.calibrations, costs=self.costs,
                seeds=c.DISCOVERY_SEEDS, split="confirmation", output_dir=Path("/tmp/never"),
                cost_grid_path=Path("/tmp/never-grid"),
            )

    def test_preregistration_hash_is_frozen(self) -> None:
        path = Path(__file__).resolve().parents[2] / "docs/experiments/ep001c_closed_loop_routing.md"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), c.PREREGISTRATION_SHA256)


if __name__ == "__main__":
    unittest.main()
