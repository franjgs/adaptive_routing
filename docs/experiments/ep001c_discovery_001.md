# EP001-C discovery_001 freeze record

This record freezes the EP001-C discovery phase before confirmation. It uses
only seeds 0--19 and primary configurations 0--75 under the amended
preregistration (`505047084bcc331f5eb1159e5cb3eeeacddf04ba`; SHA-256
`9d5af0f7652bd36e3c05c96a247a3e989df32fa1fb9534ca1900f91c3e1c1d1b`).
No confirmation seed was opened or processed in this phase.

## Fixed discovery outputs

The discovery-only cost grid is:

`0`, `0.006953200541309065`, `0.028917347074465062`,
`0.13315811517182036`, `0.524901723139824`, `1.538266022681499`,
`6.171916457008025`, and `22.53586305796004`.

It was selected exactly by the preregistered discovery rule recorded in
`cost_grid.json`: positive pooled P0/P1/P2/P3 valuations on no-query
reference trajectories, at the 10th, 25th, 50th, 75th, 90th and 99th
percentiles, augmented by zero and 1.01 times the discovery maximum. It is
now frozen for confirmation; it was not selected from confirmation outcomes.

| Artifact | SHA-256 |
|---|---|
| `cost_grid.json` | `d28adde01af5c8abdc7dd9125cae11e5b7576487d8eb4885c14964888f1eee16` |
| `trajectories/discovery_trajectory_metrics.npz` | `afa3852a40b1b725937730d59fe7ca7e36e15d585584769f07eb709e5d7230dd` |
| `trajectories/discovery_manifest.json` | `3f276865cff494d946c877e2888d3d4942921ed7162628f8c96e5b8136799c37` |
| `analysis/discovery_summary.json` | `1cf2138814b7766d73d69d64e50087a9a25ad8ce5edab283883e004bf7ed9f48` |
| `analysis/discovery_report.md` | `696590c153745c827f3ede1343137adccf7a494e2a9f3108850a367210328f71` |

The machine-readable outputs retain every fixed-grid policy/cost/gamma result,
including unfavorable, null and ambiguous discovery comparisons. Discovery is
not used for the EP001-C scientific verdict.

## Implementation incident before the completed run

Two incomplete discovery attempts produced no output artifact and no
scientific result. The first rebuilt the fixed (K_k) stack at every round;
the second iterated seeds one by one and was prohibitively slow. They were
interrupted before artifact creation. The resulting mechanical corrections
cached the unchanged (K_k) stack and vectorized independent seeds while
preserving one stored trajectory per seed and the same paired exogenous stream
for all policies. The corrections are recorded in commits `ece21bd` and
`3c0c70d`, with synthetic equivalence tests.

No policy, parameter, horizon, cost-grid selection rule, coefficient, or
scientific endpoint changed as a consequence of those interruptions.
