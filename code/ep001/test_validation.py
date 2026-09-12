"""Automated validation checks required before running EP001-A."""

from __future__ import annotations

import unittest

import numpy as np

from validation import (
    analytical_deltas,
    common_coupled_monte_carlo,
    evolve_sgd_state,
    reversal_metrics,
    sample_inputs,
    spike_fourth_moments,
    summarize_trajectory_reversals,
    transported_risk_matrices,
    weighted_fourth_matrix,
)


class EP001ValidationTest(unittest.TestCase):
    def test_reversal_timing_magnitude_and_robust_classification(self) -> None:
        robust = reversal_metrics(
            np.array([2.0, 0.4, -0.01, -0.3]),
            numerical_tolerance=0.05,
        )
        self.assertTrue(robust.eligible)
        self.assertEqual(robust.k_flip, 2)
        self.assertAlmostEqual(robust.rho_rev, 0.15)
        self.assertTrue(robust.robust_reversal)

        no_flip = reversal_metrics(
            np.array([2.0, 0.5, 0.2]),
            numerical_tolerance=0.05,
        )
        self.assertIsNone(no_flip.k_flip)
        self.assertLessEqual(no_flip.rho_rev, 0.0)
        self.assertFalse(no_flip.robust_reversal)

        numerical_only = reversal_metrics(
            np.array([2.0, -0.01]),
            numerical_tolerance=0.05,
        )
        self.assertEqual(numerical_only.k_flip, 1)
        self.assertAlmostEqual(numerical_only.rho_rev, 0.005)
        self.assertFalse(numerical_only.robust_reversal)

        ineligible = reversal_metrics(
            np.array([0.01, -1.0]),
            numerical_tolerance=0.05,
        )
        self.assertFalse(ineligible.eligible)
        self.assertIsNone(ineligible.k_flip)
        self.assertIsNone(ineligible.rho_rev)

    def test_trajectory_level_aggregation(self) -> None:
        summaries = summarize_trajectory_reversals(
            seeds=np.array([10, 10, 10, 11, 11, 12]),
            eligible=np.array([True, True, False, True, True, False]),
            robust_reversal=np.array([True, False, False, False, False, False]),
        )
        self.assertEqual([summary.seed for summary in summaries], [10, 11, 12])
        self.assertEqual(summaries[0].eligible_cases, 2)
        self.assertEqual(summaries[0].robust_reversal_cases, 1)
        self.assertAlmostEqual(summaries[0].robust_reversal_rate, 0.5)
        self.assertTrue(summaries[0].contains_robust_reversal)
        self.assertEqual(summaries[1].robust_reversal_rate, 0.0)
        self.assertFalse(summaries[1].contains_robust_reversal)
        self.assertIsNone(summaries[2].robust_reversal_rate)

    def test_parameterized_family_moments(self) -> None:
        for q in (1.0, 0.5, 1.0 / 3.0, 1.0 / 6.0):
            fourth = spike_fourth_moments(q)
            expected_h = np.diag([4.0, 1.0 + 1.0 / q])
            np.testing.assert_allclose(weighted_fourth_matrix(fourth), expected_h)

    def test_sampler_reproduces_second_and_weighted_fourth_moments(self) -> None:
        cases = (
            ("gaussian", None, np.array([3.0, 3.0])),
            ("gaussian_spike", 1.0 / 3.0, spike_fourth_moments(1.0 / 3.0)),
            ("gaussian_spike", 1.0, spike_fourth_moments(1.0)),
        )
        for case_index, (distribution, q, fourth) in enumerate(cases):
            x = sample_inputs(
                np.random.default_rng(161803 + case_index),
                400_000,
                distribution,
                q,
            )
            second_samples = np.einsum("ni,nj->nij", x, x)
            weighted_samples = np.einsum(
                "n,ni,nj->nij", np.einsum("ni,ni->n", x, x), x, x
            )
            expected = (np.eye(2), weighted_fourth_matrix(fourth))
            for samples, target in zip((second_samples, weighted_samples), expected):
                mean = samples.mean(axis=0)
                standard_error = samples.std(axis=0, ddof=1) / np.sqrt(samples.shape[0])
                tolerance = 5.0 * standard_error + 0.01
                self.assertTrue(np.all(np.abs(mean - target) <= tolerance))

    def test_sign_preserving_controls_keep_scalar_k(self) -> None:
        eta = 0.05
        for fourth in (np.array([3.0, 3.0]), spike_fourth_moments(1.0 / 3.0)):
            matrices = transported_risk_matrices(fourth, eta, horizon=10)
            for matrix in matrices:
                self.assertAlmostEqual(matrix[0, 0], matrix[1, 1])
                self.assertAlmostEqual(matrix[0, 1], 0.0)
            # This is a validation configuration; the state is produced by SGD below.
            rng = np.random.default_rng(31415)
            inputs = rng.normal(size=(40, 2))
            noise = rng.normal(scale=0.1, size=40)
            w_star = np.array([1.0, -0.5])
            theta = evolve_sgd_state(np.zeros(2), w_star, inputs, noise, eta)
            error = theta - w_star
            x = np.array([0.7, -1.1])
            deltas = analytical_deltas(error, x, np.zeros(2), 0.02, 0.05, matrices)
            nonzero = np.abs(deltas) > 1e-14
            self.assertTrue(np.all(np.sign(deltas[nonzero]) == np.sign(deltas[0])))

    def test_operator_matches_common_coupled_monte_carlo_at_natural_state(self) -> None:
        cases = (
            ("gaussian", None, np.array([3.0, 3.0])),
            # Decision 009 Gaussian--Rademacher sanity-check distribution.
            ("gaussian_spike", 1.0, spike_fourth_moments(1.0)),
        )
        for case_index, (distribution, q, fourth) in enumerate(cases):
            rng = np.random.default_rng(20260912 + case_index)
            eta = 0.05
            w_star = np.array([1.0, -0.5])
            training_x = sample_inputs(rng, 60, distribution, q)
            training_noise = rng.normal(scale=0.1, size=60)
            theta = evolve_sgd_state(
                np.zeros(2), w_star, training_x, training_noise, eta
            )
            error = theta - w_star  # Never manually constructed.
            query_input = sample_inputs(rng, 1, distribution, q)[0]
            matrices = transported_risk_matrices(fourth, eta, horizon=3)
            exact = analytical_deltas(
                error, query_input, np.zeros(2), 0.02, eta, matrices
            )
            estimate = common_coupled_monte_carlo(
                error=error,
                query_input=query_input,
                teacher_bias=np.zeros(2),
                teacher_variance=0.02,
                eta_teacher=eta,
                eta_future=eta,
                horizon=3,
                replications=200_000,
                rng=np.random.default_rng(271828 + case_index),
                distribution=distribution,
                q=q,
                target_noise_std=0.1,
            )
            tolerance = 5.0 * estimate.standard_error + 2e-5
            np.testing.assert_array_less(np.abs(estimate.mean - exact), tolerance)


if __name__ == "__main__":
    unittest.main()
