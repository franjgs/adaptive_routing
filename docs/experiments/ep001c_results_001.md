# EP001-C confirmation_001 — closed-loop result record

## Frozen protocol and artifacts

This is the first EP001-C confirmation execution under the amended frozen
preregistration:

- original preregistration: `157765a249aab85e55a3e0984ba96d54710f5650`;
- transparent pre-execution amendment fixing (T=2000):
  `505047084bcc331f5eb1159e5cb3eeeacddf04ba`;
- amended preregistration SHA-256:
  `9d5af0f7652bd36e3c05c96a247a3e989df32fa1fb9534ca1900f91c3e1c1d1b`;
- initial implementation: `5124e0aa9cf6ceae0ce8e140dbfa992299270365`;
- discovery freeze: `bddbffecd6b8b1d99847a4e346609c9c8643acc2`.

The confirmation population is all 76 primary configurations (0--75) and
seeds 20--49. Every policy within a configuration/seed shares inputs, target
noise, expensive-model noise, and the delayed-feedback schedule. Routing and
learner updates then diverge endogenously. P2 uses the frozen B2
configuration-specific operational coefficient; no coefficient was refit.
P3 uses only the current state/input and the EP001 reference-coupled
transport operator; it uses no realized future information.

The frozen discovery cost grid is

`0`, `0.006953200541309065`, `0.028917347074465062`,
`0.13315811517182036`, `0.524901723139824`, `1.538266022681499`,
`6.171916457008025`, and `22.53586305796004`.

All 24 gamma/cost cells and every primary endpoint are retained in the
versioned machine-readable confirmation summary:
`results/ep001/first_run_001/ep001c/confirmation_001/analysis/confirmation_summary.json`
(SHA-256 `ac556899f4af8a385d86d70d6eee6991e3a9f199383c3ca13d0bc92aebc17244`).
It includes absolute (J), loss/query components, query rates, final risk,
all six paired policy contrasts, temporal thirds, first-divergence and
state-divergence diagnostics, per-configuration outcomes, and 10,000 paired
trajectory-bootstrap intervals. The associated trajectory archive has
SHA-256 `d860b138a14783e8838b800f2851cd4ffedee7e54a8774c81bd81eda1f83e95d`.

## Empirical result

Lower (J) is better. The table reports the primary P0--P3 comparison as
(J^{P0}-J^{P3}); positive values favor P3. Brackets are its paired 95%
bootstrap interval across complete trajectories, preserving B2's shared
quartet dependence.

| (gamma) | (C_D) | (J^{P0}-J^{P3}) | 95% interval |
|---:|---:|---:|---:|
| 0.5 | 0 | -0.000244 | [-0.000866, 0.000127] |
| 0.5 | 0.0069532 | -0.0000976 | [-0.000274, 0.0000411] |
| 0.5 | 0.0289173 | -0.0000678 | [-0.000266, 0.000111] |
| 0.5 | 0.133158 | -0.000190 | [-0.000584, 0.000121] |
| 0.5 | 0.524902 | 0.000283 | [-0.000653, 0.001372] |
| 0.5 | 1.53827 | -0.00109 | [-0.002082, -0.000201] |
| 0.5 | 6.17192 | 0.00398 | [0.000779, 0.008657] |
| 0.5 | 22.5359 | -0.00000408 | [-0.0000122, 0] |
| 0.9 | 0 | -0.000532 | [-0.001517, 0.000362] |
| 0.9 | 0.0069532 | -0.00123 | [-0.002245, -0.000341] |
| 0.9 | 0.0289173 | -0.00242 | [-0.003514, -0.001342] |
| 0.9 | 0.133158 | -0.00648 | [-0.008213, -0.004764] |
| 0.9 | 0.524902 | -0.01245 | [-0.016387, -0.008419] |
| 0.9 | 1.53827 | 0.01381 | [0.005602, 0.022190] |
| 0.9 | 6.17192 | 0.15373 | [0.122521, 0.187115] |
| 0.9 | 22.5359 | 0.000529 | [0, 0.001568] |
| 1.0 | 0 | 0.01133 | [0.006950, 0.015738] |
| 1.0 | 0.0069532 | 0.01484 | [0.010514, 0.019159] |
| 1.0 | 0.0289173 | 0.02115 | [0.016692, 0.025686] |
| 1.0 | 0.133158 | 0.06740 | [0.059435, 0.075774] |
| 1.0 | 0.524902 | 0.25703 | [0.235884, 0.278888] |
| 1.0 | 1.53827 | 0.81641 | [0.757222, 0.877373] |
| 1.0 | 6.17192 | 1.87841 | [1.685657, 2.072647] |
| 1.0 | 22.5359 | 0.02230 | [0, 0.055100] |

P2 closely reproduces P3 in this frozen grid: the largest absolute grid-level
(J^{P2}-J^{P3}) difference is (1.33\times10^{-5}),
(4.65\times10^{-5}), and (2.50\times10^{-4}) for gamma 0.5, 0.9 and
1.0 respectively. This is a closed-loop observation about the frozen
configuration-specific compression, not evidence that its coefficient is
available or estimable in a deployed system.

P1 is not uniformly sufficient. At gamma 1.0, P3 improves over P1 across
low/intermediate costs; for example (J^{P1}-J^{P3}=0.02338) at
(C_D=0.524902), with interval [0.017283, 0.029665]. At gamma 1.0 and
(C_D=6.17192), however, P1 is better:
(J^{P1}-J^{P3}=-0.11508), interval [-0.153363, -0.077733]. At gamma 0.5,
P1/P2/P3 differences are small and mixed on this scale.

## Temporal result

The stationary/transient limitation is active in this run. Query activity and
routing disagreement are concentrated in the early third (rounds 1--666).
For example, at gamma 1.0 and (C_D=0.524902), P0/P3 early query rates are
0.01096/0.01392 and their early disagreement rate is 0.00299; middle and
late query and disagreement rates are zero at that cost. This pattern recurs
over most nontrivial costs: the summary retains the complete thirds table.

Accordingly, this experiment is evidence only about **transient adaptive
routing in the stationary EP001 environment**. It is not evidence about
persistent routing demand under continuously changing environments.

## Preregistered interpretation

The overall verdict is **AMBIGUOUS**, rather than a forced favorable case.

- **C1-type evidence:** at gamma 1.0, P3 improves over P0 over the low through
  intermediate grid and P2 reproduces that absolute improvement closely.
- **C5-type evidence:** at gamma 0.9, P3 is systematically worse than P0 at
  costs 0.0069532, 0.0289173, 0.133158, and 0.524902, whose paired intervals
  are wholly negative. P3 is usually slightly better than P1 in that region,
  but both future-valuing policies are worse than P0. Repeated use of the
  reference-coupled surrogate can therefore be harmful in this tested
  closed-loop regime.
- **C3/C4-type evidence in restricted regimes:** gamma 0.5 is mostly
  null/mixed with no stable P3 advantage, while high costs produce nearly no
  queries and hence mechanically small policy differences.

The result does not invalidate the derivation of (K_k): it remains exact for
the stated common-subsequent-update reference counterfactual. It does weaken
the claim that repeated use of that local surrogate is a robust central
practical routing rule. It also does not establish that future learning value
in general is irrelevant, because EP001-C does not evaluate a
policy-dependent continuation value.

## Project consequence

Retain the immediate and static future-learning baselines, the exact
reference-coupled derivation as a diagnostic/local quantity, and the B2
observation that a configuration-specific scalar can compress that quantity.
Demote exact state-dependent transport and scalar transport as universal or
primary practical routing mechanisms. Do not advance EP001 transport as the
empirical centerpiece without a concrete problem in which the relevant
discount/time-scale is justified and the closed-loop surrogate is re-tested.

No concept drift, application experiment, rollout oracle, dynamic-programming
method, or new theoretical development was introduced here.
