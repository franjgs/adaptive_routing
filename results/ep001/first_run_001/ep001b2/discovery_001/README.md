# EP001-B2 discovery calibration artifact provenance

`discovery_calibration.json` is the deterministic, discovery-only calibration
payload frozen for EP001-B2. It is intentionally excluded from ordinary Git
because GitHub rejects individual Git objects above 100 MiB. This README is
small, versioned provenance for the locally generated artifact; the JSON may
remain beside it as an ignored generated file.

| field | value |
|---|---|
| Original filename | `discovery_calibration.json` |
| Original filesystem size | 211,192,800 bytes (about 201.41 MiB) |
| SHA-256 | `9e64ee92e45b3925f2babfe847d1d3d04ec6388ea1537d8a6c37f6e3105757a8` |
| Original ordinary-Git blob | `c433b5be6500955ebc405c68a6ab7b479ad05f3b` |
| Artifact role | Frozen EP001-B2 discovery-only M1/M2 scalar calibrations and exact minimizer metadata |
| Generator | `code/ep001/run_ep001b2_discovery.py` |
| Frozen preregistration | `09404c92970a909b8263b11e334cb7b29ce7289a` |
| Frozen implementation | `9ea32d07fac4d4b3663d7e9287be787dd3c43de0` |
| Original unpublished freeze | `1d8267430a1e1bacd7dd95284f9137e44455b79d` |
| Rewritten equivalent freeze | `9c3d1449a8d19105fa9c270ecf5cd8871816939e` |
| Discovery seeds | 0--19 only |
| Primary configurations | 0--75 |
| Excluded motivating configurations | 76--79 |
| Population | Finite `Delta_now` and `Delta_0,...,Delta_9`; no `eligible`, `rho_rev`, or reversal filter |
| Horizon / gamma grid | `H=10`; gamma in `{0.5, 0.9, 1.0}` |

The artifact was externalized only after GitHub rejected the unpublished local
history for its size. The source, scientific protocol, numerical contents, and
SHA-256 were not changed. Its hash is also recorded in
`discovery_calibration_report.md`, the EP001-B2 confirmation manifest and
metrics, and the frozen confirmation loaders.

## Reproduction

With the preserved EP001-A archive available locally, generate into a fresh
directory (the runner intentionally refuses to overwrite frozen output):

```sh
PYTHONDONTWRITEBYTECODE=1 python code/ep001/run_ep001b2_discovery.py \
  --raw results/ep001/first_run_001/raw_ep001a.npz \
  --output-dir /tmp/ep001b2_discovery_reproduction
shasum -a 256 /tmp/ep001b2_discovery_reproduction/discovery_calibration.json
```

The displayed digest must equal the SHA-256 in this table. The original
artifact is reproducible from the frozen generator, the preserved raw archive,
the fixed seeds/configurations above, and the stated frozen commits; no
confirmation records are read by the discovery runner.
