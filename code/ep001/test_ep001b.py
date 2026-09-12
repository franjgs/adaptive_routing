"""Unit tests for EP001-B algebra, independent of the preserved run."""

from __future__ import annotations

import unittest

import numpy as np

from analyze_ep001b import geometric_factor, transport_values


class EP001BTest(unittest.TestCase):
    def test_geometric_factor_and_gamma_one(self) -> None:
        self.assertAlmostEqual(geometric_factor(0.5, 10), 1.998046875)
        self.assertEqual(geometric_factor(1.0, 10), 10.0)

    def test_static_and_adapted_values(self) -> None:
        deltas = np.array([[2.0, 1.0, 0.5], [-1.0, -2.0, 3.0]])
        values = transport_values(deltas, np.array([4.0, 5.0]), 1.0)
        np.testing.assert_allclose(values["delta_static"], [4.0, -2.0])
        np.testing.assert_allclose(values["delta_adapt"], [3.0, -3.0])

    def test_delta_c_and_width_identities(self) -> None:
        deltas = np.array([[2.0, 1.0], [2.0, 3.0]])
        values = transport_values(deltas, np.array([0.0, 0.0]), 0.5)
        np.testing.assert_allclose(values["delta_c"], 0.5 * values["e_transport"])
        np.testing.assert_allclose(values["w_c"], np.abs(values["delta_c"]))

    def test_strictly_between_critical_costs_disagrees(self) -> None:
        deltas = np.array([[1.0, 0.0, 0.0], [1.0, 2.0, 2.0]])
        values = transport_values(deltas, np.array([1.0, 1.0]), 0.9)
        lo, hi = sorted((values["c_static"][1], values["c_transport"][1]))
        cost = (lo + hi) / 2.0
        self.assertNotEqual(np.sign(values["c_static"][1] - cost), np.sign(values["c_transport"][1] - cost))


if __name__ == "__main__":
    unittest.main()
