# EP001-B — Operational relevance of transported adaptation value

## Pre-analysis record

EP001-B is a postprocessing study of the preserved EP001-A first run. It
does not generate trajectories or alter the EP001-A verdict
(`FAILS TO SUPPORT THE PHENOMENON IN THE TESTED REGIME`). The source is
`results/ep001/first_run_001/raw_ep001a.npz`; discovery and confirmation are
kept separate, with confirmation as the primary evidential split.

The frozen timing convention is unambiguous: for each stored row and each
`gamma` in `{0.5, 0.9, 1.0}`,

\[
B_H=\sum_{k=0}^{H-1}\gamma^k,\quad
\Delta_{static}^{(H)}=B_H\Delta_0,\quad
\Delta_{adapt}^{(H)}=\sum_{k=0}^{H-1}\gamma^k\Delta_k.
\]

The routing quantities use the additional outer factor specified in the
paper: `C_myopic*=Delta_now`, `C_static*=Delta_now + gamma Delta_static`,
and `C_transport*=Delta_now + gamma Delta_adapt`. Therefore
`Delta_C*=gamma E_transport` and `W_C=|Delta_C*|`. The relative diagnostic
uses only `epsilon=1e-12`; it is not interpreted without absolute scales.

The postprocessor writes exact per-case derived arrays and compact
configuration, trajectory, and checkpoint summaries. “Non-negligible” in the
trajectory diagnostic means `|E_transport|` exceeds the row's existing
EP001 numerical tolerance; no new scientific threshold is introduced.

## Observed results

The discovery-selected configuration was the pre-existing `spike_q_1`
configuration (`eta=0.05`, `eta_D=0.05`, target-noise standard deviation
`0.1`, teacher variance `0.05`). Selection used discovery only and was not
changed after inspecting confirmation.

For confirmation (3,950 eligible cases), the distributions below are
median [Q1, Q3] (means are retained in the machine-readable CSV):

The independently verified absolute immediate-gain reference scale has
P25/P50/P75/P90 = 0.0391838 / 0.0867269 / 0.471230 / 1.34801.

| gamma | Delta_static | Delta_adapt | E_transport | W_C |
|---|---:|---:|---:|---:|
| 0.5 | 0.02557 [0.00451, 0.09753] | 0.02339 [0.00415, 0.08925] | -0.00213 [-0.00818, -0.00037] | 0.00107 [0.00019, 0.00409] |
| 0.9 | 0.08335 [0.01472, 0.31792] | 0.06113 [0.01080, 0.23125] | -0.02257 [-0.08666, -0.00393] | 0.02031 [0.00354, 0.07800] |
| 1.0 | 0.12797 [0.02260, 0.48811] | 0.08701 [0.01530, 0.32881] | -0.04172 [-0.16023, -0.00726] | 0.04172 [0.00726, 0.16023] |

The full pre-specified scale comparison (P25/P50/P75/P90) is:

| gamma | W_C | W_C / |Delta_now| | W_C / |C_static*| | W_C / |gamma Delta_static| |
|---|---|---|---|---|
| 0.5 | 0.000185667 / 0.00106727 / 0.00409067 / 0.0106511 | 0.00663209 / 0.00866076 / 0.0115202 / 0.0226737 | 0.00634396 / 0.00787805 / 0.0104451 / 0.0199276 | 0.0818339 / 0.0837547 / 0.0855741 / 0.0890461 |
| 0.9 | 0.00353973 / 0.0203137 / 0.0779952 / 0.202887 | 0.126498 / 0.164895 / 0.219139 / 0.431340 | 0.0924293 / 0.104118 / 0.131800 / 0.234143 | 0.266431 / 0.271803 / 0.276898 / 0.286579 |
| 1.0 | 0.00726432 / 0.0417226 / 0.160226 / 0.416718 | 0.259594 / 0.338707 / 0.450034 / 0.885668 | 0.154149 / 0.169340 / 0.208366 / 0.355634 | 0.321012 / 0.327275 / 0.333216 / 0.344503 |

Near-zero denominator checks were verified directly: `|Delta_now| < 1e-4`
occurs in 0.0253% of cases; `|C_static*| < 1e-4` occurs in 0.0506%,
0.0506%, and 0.1266% for gamma 0.5, 0.9, and 1.0. The ratios are therefore
not generally driven by a large population of near-zero denominators,
although tail ratios can still be amplified by individual small values.

Most confirmation `Delta_C*` cases were negative in the selected
configuration (3,931/3,950, 3,932/3,950, and 3,932/3,950 respectively were
negative for gamma 0.5, 0.9, and 1.0; the remainder were positive). Thus the
static approximation generally overvalues consultation, with a small
positive subset where it undervalues it. The corresponding static/adapted
correlations were 0.999999, 0.999992, and 0.999987. These high correlations
do not imply equivalent threshold values: the median `W_C` grows with gamma.

The median correction relative to the static adaptation component is 8.38%,
27.18%, and 32.73% for gamma 0.5, 0.9, and 1.0. For gamma=1, median `W_C`
is 33.87% of `|Delta_now|` and 16.93% of `|C_static*|`. Absolute values
remain the primary scale evidence.

Effects were not concentrated in one trajectory: the largest single-seed
share of total absolute `W_C` was about 6.1% in confirmation. Checkpoint
summaries retain median `||e_t||`, absolute transport error, and `W_C` for
every configuration and gamma. The complete per-seed and per-configuration
records are the authoritative source for dispersion and concentration.

The 18 robust EP001-A reversals remain a labeled subgroup in the raw data,
but EP001-B is not conditioned on them. The reported transport differences
use all eligible naturally evolved states; reversal cases are descriptive
only and are not the main sample.

## Interpretation and scope

In this fixed oracle regime, transport differences are systematic in sign and
increase with the declared discount factor, while static and transported
values remain highly correlated. The scale comparisons support a
discount-dependent conclusion: the transport correction is small on the
observed routing scale for gamma=0.5, but operationally material in scale for
gamma=0.9 and gamma=1.0. The resulting classification is
**scale-dependent: small under short discounting, material under moderate and
undiscounted transport**. This is not a claim of practical routing benefit.

Transport effects are systematic and small under short discounting
(gamma=0.5), but become material relative to both the immediate operational
gain and the total static routing threshold for gamma=0.9 and gamma=1.0.
Operational benefit remains unresolved because EP001-B does not execute
divergent routing policies.

EP001-B does not simulate divergent routing policies. The interval of costs
between `C_static*` and `C_transport*` is the algebraic disagreement width;
actual policy comparison remains EP001-C. No conclusion about full
continuation values follows from this common-coupled surrogate.

## Artifacts and reproducibility

The run was performed once with:

```text
python3 code/ep001/analyze_ep001b.py
```

Outputs are under `results/ep001/first_run_001/ep001b/`:

- `ep001b_case_values.npz` (per-case values for all three gammas);
- `ep001b_configuration_summary.csv`;
- `ep001b_trajectory_summary.csv`;
- `ep001b_checkpoint_summary.csv`;
- `ep001b_report.json`.

The frozen EP001-A raw file was not modified. No EP001-C implementation or
new theory is authorized by this analysis.
