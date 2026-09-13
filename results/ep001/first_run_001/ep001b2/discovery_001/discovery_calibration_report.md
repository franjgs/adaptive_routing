# EP001-B2 discovery calibration record

Discovery-only calibration under the frozen EP001-B2 preregistration. No confirmation performance endpoint or scientific interpretation is included.

- Artifact: `discovery_calibration.json`
- SHA-256: `9e64ee92e45b3925f2babfe847d1d3d04ec6388ea1537d8a6c37f6e3105757a8`
- Preregistration commit: `09404c92970a909b8263b11e334cb7b29ce7289a`
- Implementation commit: `9ea32d07fac4d4b3663d7e9287be787dd3c43de0`
- Seeds: 0--19 only
- Primary configurations: 0--75
- Excluded motivating configurations: 76--79
- Population: finite `Delta_now` and `Delta_0,...,Delta_9`; no eligibility or reversal filter
- Candidate / finite / excluded cases: 486400 / 486400 / 0
- Weighting: equal configuration, then equal trajectory, then equal case
- Primary coefficients per gamma/objective: one M1 and 76 M2
- Sensitivities frozen: functional OLS, functional LAD [0,1], operational [0,1]
- Confirmation seeds processed: no

## Primary global discovery coefficients

| gamma | functional M1 c_F^G | operational M1 c_O^G |
|---:|---:|---:|
| 0.5 | 0.96321493364720023 | 0.96321493364720023 |
| 0.9 | 0.87170266794622497 | 0.87170266794622508 |
| 1.0 | 0.8433199371302853 | 0.84331993713028552 |

All configuration-specific coefficients and exact minimizing-region metadata are in the artifact. Coefficient values are recorded without a scalar-reducibility interpretation.
