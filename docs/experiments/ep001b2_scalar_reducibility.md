# EP001-B2 — Scalar reducibility of transported adaptation value

Status: formal preregistration draft; execution is not authorized by this document.
No B2 scalar has been fitted and no B2 confirmation reducibility result has
been inspected in preparing this draft. EP001-A and EP001-B are closed.
EP001-A's first-run verdict remains exactly:

> FAILS TO SUPPORT THE PHENOMENON IN THE TESTED REGIME.

## Scientific purpose and two questions

EP001-B found valuation displacement in the previously selected configuration
79's eligible confirmation subset. The high correlation and apparently
concentrated relative displacement between static and transported adaptation
motivated an adversarial explanation:

- **Scalar Reducibility Hypothesis (SRH):** transported adaptation may be
  represented approximately by a state-independent scalar,
  `Delta_adapt ≈ c Delta_static`.
- **Global Scalar Contraction Hypothesis (GSCH):** the stronger global special
  case has one scalar with `0 <= c <= 1`.

The mathematical target is the existing theory's transported adaptation
functional, not an external ground truth. B2 gives simple scalar competitors
a strong opportunity to explain it and separates two questions:

**Q1 — Functional scalar reducibility.** Can a discovery-calibrated scalar
approximate the functional out of sample across states and queries?

**Q2 — Operational scalar reducibility.** Can a scalar reproduce the target's
routing threshold over feasible costs `C_D >= 0`, even if functional errors
remain? Each scalar receives calibration specifically optimized for this
operational question.

A small operational residual does not prove functional reducibility. A
functional residual does not establish operational relevance if it produces
no disagreement at feasible costs. No correlation will be used as evidence
of routing equivalence.

## Frozen data, population and timing

The only data source is
`results/ep001/first_run_001/raw_ep001a.npz`, with its preserved
`run_manifest.json` as configuration metadata. No new trajectories, query
inputs, distributions, learning rates, noises or horizons are permitted.

The primary population includes every stored row for which `Delta_now` and
`Delta_0,...,Delta_9` are finite. Do not require `rho_rev`, `k_flip`, or
`Delta_10` to be finite. In particular, intentional missing reversal
diagnostics must not exclude rows. Report finite-case exclusions and their
configuration/trajectory counts, if any; derived overflow is an implementation
problem to resolve, not a reason for silently changing the population.

The old EP001-A condition

\[
\mathrm{eligible}\iff
\Delta_0>10^{-6}(1+\|e_t\|^2)
\]

was designed for reversal of an initially beneficial update. It excludes
approximately 47% of stored routing cases and is not a primary B2 filter.

Use `H=10` and separately report every `gamma in {0.5,0.9,1.0}`:

\[
B_H(\gamma)=\sum_{k=0}^{9}\gamma^k,\qquad
\Delta_{\mathrm{static}}=B_H(\gamma)\Delta_0,\qquad
\Delta_{\mathrm{adapt}}=\sum_{k=0}^{9}\gamma^k\Delta_k.
\]

The stored `Delta_10` does not enter these sums. The outer gamma in routing
thresholds below is retained exactly as in the frozen theory. Here `B_H`
uses EP001-B's discount origin; the paper's isolated-horizon `B_H` starts at
power one and equals `gamma B_H` in this document's notation.

These are common-coupled evaluation stages counted by subsequent updates.
They are not automatically elapsed operational rounds or the reliable-feedback
delay. The response-time interpretation requires the schedule stated in
`paper/primary/sections/theoretical_analysis.tex` under “Accumulated adaptation
and the two clocks.” B2 retains the existing surrogate and does not insert
pending reliable feedback into its i.i.d. transport functional.

## Exposure, fixed grid and holdout

The primary fixed grid is **configurations 0–75**, comprising 76 configurations
in 19 independently keyed base-trajectory groups. Configurations are a fixed
design, not a random sample of possible environments.

Each quartet `0–3, 4–7, ..., 76–79` shares base trajectories and evaluation
queries for a displayed seed; the RNG key omits pseudo-step and teacher
variance. Configuration 79's confirmation observations motivated SRH.
Consequently the **entire quartet 76–79 is previously exposed** and excluded
from all primary calibration and confirmation estimates. It may be described
only in a separate motivating-block analysis.

Discovery uses seeds **0–19**; confirmation uses **20–49**. Every scalar is
learned exclusively from discovery. Primary M1 uses only discovery configs
0–75; primary M2 uses discovery from its individual primary configuration.
All gammas' coefficients, fitting diagnostics and model identities must be
recorded and frozen before any confirmation reducibility calculation.

The audited complete primary grid contains 486,400 discovery and 729,600
confirmation case records (320 per configuration/seed), but only 380 and
570 distinct base trajectories respectively. Four teacher configurations
reuse each base trajectory. Previously available M0 audit summaries do not
constitute unobserved data; the holdout protection concerns the newly posed
scalar-reducibility diagnostics.

## Models and hierarchical weights

For each gamma, with no intercept:

| Model | Approximation | Scalar scope |
|---|---|---|
| M0 | `Delta_hat = Delta_static` | Fixed coefficient 1 |
| M1 | `Delta_hat = c_gamma^G Delta_static` | One coefficient across the entire primary grid |
| M2 | `Delta_hat = c_gamma,j^C Delta_static` | One coefficient per configuration, constant across all its trajectories, checkpoints, states and queries |

M2 is deliberately an oracle-calibrated compressibility competitor, not
necessarily a deployable router. Primary coefficients range over all real
numbers. No M3 or flexible regressor is included.

For any case loss `l_ijs`, define

\[
L_{js}=\frac1{n_{js}}\sum_i l_{ijs},\qquad
L_j=\frac1{S_j}\sum_s L_{js},\qquad
L_{\mathrm{grid}}=\frac1{76}\sum_{j=0}^{75}L_j.
\]

Thus cases have weight `1/(76 S_j n_js)` in the grid objective. Within a
configuration, M2 uses `1/(S_j n_js)`. Retain this definition even when all
counts are equal. All losses, empirical residual distributions and reporting
of scale use these weights; do not let larger selected samples dominate.
If an analysis subset leaves a trajectory empty, its conditional case loss
is undefined: report it and average over nonempty trajectories, explicitly
labeling the resulting coverage. The audit found none in the primary or old
eligible populations. An empty primary configuration prevents a complete
fixed-grid estimate and must be reported, not silently dropped.

## Q1: functional calibration and endpoints

Primary discovery calibration is weighted least absolute deviations (LAD):

\[
F(c)=\mathbb E_w\left|\Delta_{\mathrm{adapt}}
                  -c\Delta_{\mathrm{static}}\right|.
\]

Fit global `c_gamma^G,F` for M1 and configuration-specific `c_gamma,j^C,F`
for M2 with the weights above. Freeze coefficients and evaluate on
confirmation:

\[
F_A=\mathbb E_w|\Delta_{\mathrm{adapt}}-\widehat\Delta_A|,
\quad A\in\{M0,M1^F,M2^F\}.
\]

Report absolute losses together with

\[
RF1=1-F_{M1^F}/F_{M0},\qquad
RF2=1-F_{M2^F}/F_{M0},\qquad
GF_{2|1}=1-F_{M2^F}/F_{M1^F}.
\]

Report grid and configuration estimates, per-trajectory losses, and
hierarchically weighted signed/absolute residual quantiles (P25, P50, P75,
P90). These quantiles are descriptive endpoints, not equivalence margins.
Also report fitted coefficients and weighted RMSE. If reporting R-squared,
use `1 - E_w residual^2 / E_w (Delta_adapt - E_w Delta_adapt)^2`, leaving it
undefined for zero target variance. No correlation-based conclusion is allowed.

## Q2: operational calibration and endpoints

For the transport target and any approximation A:

\[
C_T^*=\Delta_{\mathrm{now}}+\gamma\Delta_{\mathrm{adapt}},\qquad
C_A^*=\Delta_{\mathrm{now}}+\gamma\widehat\Delta_A.
\]

The operational domain is `C_D >= 0`; `C_D` already denotes incremental
consultation cost. Query when `C_D < C_A*`, with a no-query tie convention.
Ties affect isolated curve endpoints, not integrated widths. Define

\[
W_A^+=|\max(C_A^*,0)-\max(C_T^*,0)|,\qquad
L_A^+=\mathbb E_w W_A^+.
\]

This all-case loss remains the primary Q2 estimand. When both thresholds
are nonpositive, the zero contribution correctly represents agreement at
every feasible cost; it is not statistical dilution.

Give Q2 its own discovery-optimized scalars:

\[
c_O\in\arg\min_{c\in\mathbb R}
\mathbb E_w\left|\max(\Delta_{\mathrm{now}}+
                 \gamma c\Delta_{\mathrm{static}},0)
                   -\max(C_T^*,0)\right|.
\]

M1^O uses one global scalar and M2^O one scalar per configuration, with the
same hierarchical weights. They are distinct from Q1's functional LAD fits;
do not substitute a Q1 coefficient and call it operationally optimized.

Freeze these coefficients and report primary confirmation endpoints

\[
L_{M0}^+,\ L_{M1^O}^+,\ L_{M2^O}^+,
\quad R1^+=1-L_{M1^O}^+/L_{M0}^+,
\quad R2^+=1-L_{M2^O}^+/L_{M0}^+,
\quad G_{2|1}^+=1-L_{M2^O}^+/L_{M1^O}^+.
\]

Report grid, configuration and trajectory losses and paired absolute loss
differences, preserving absolute units. Full-domain threshold width
`|C_A* - C_T*|` is a secondary mathematical comparator only.

The absolute losses `L_M0+`, `L_M1O+`, and `L_M2O+`, with their 95% confidence
intervals, are mandatory primary outputs and must appear before relative
ratios. If `L_M0+` is already very small in absolute cost units, a large
relative reduction must not be described as a large operational effect.

Define the hierarchically weighted disagreement curve

\[
D_A(C)=\mathbb E_w\mathbf1\{\mathbf1(C<C_A^*)
                                  \ne\mathbf1(C<C_T^*)\},\quad C\geq0.
\]

Then `L_A+ = integral_0^infinity D_A(C) dC`. This is **integrated feasible-cost
disagreement width**, not an expected disagreement probability: no cost
distribution has been specified.

Report all three curves for every gamma at grid level and by configuration.
Use the observed range from zero through the largest nonnegative target or
approximation threshold in the relevant set; beyond it disagreement is zero.
Construct the step curves from the union of clipped threshold endpoints and
integrate interval by interval. Any plotting decimation must retain the exact
curve for integration. Check numerical area against the directly computed
`L_A+` using relative tolerance `1e-10` and absolute tolerance `1e-12`.
These are arithmetic checks, not scientific relevance thresholds. Report and
resolve numerical failures before interpreting model performance.

### Fixed active-region secondary diagnostic

For each gamma define, using only the transport target and M0,

\[
S_{\mathrm{active}}^0
=\{i:\max(C_{T,i}^*,C_{M0,i}^*)>0\}.
\]

Membership is fixed identically for M0, M1^O and M2^O; no fitted-model
threshold enters the subset definition. On confirmation report, for all
three models,

\[
L_{A,\mathrm{active}}^+
=\mathbb E_w[W_A^+\mid S_{\mathrm{active}}^0],
\]

and the conditional hierarchically weighted distribution of `W_A+`, including
P50, P90 and P99 on exactly that subset. These describe disagreement among
cases where the target or original static baseline admits some positive
feasible consultation-cost region. They do not replace the all-case loss.

To make the conditional notation exact, first assign the existing all-case
hierarchical weights `w_ijs=1/(76 S_j n_js)`, then condition that measure:
`E_w[W | S] = E_w[W 1_S] / E_w[1_S]`. Use the same restricted weights for
the empirical conditional distribution, defining each quantile as its inverse
CDF (smallest value attaining the requested cumulative mass). Report the
weighted subset mass as well. Do not redefine S or its weights for each
model. This conditional diagnostic is distinct from the separately specified
old-eligible continuity analysis's within-trajectory renormalization.

### Scalar-induced positive regions outside the active set

Let `N^0` be the complement of `S_active^0` in the primary population:
`C_T* <= 0 and C_M0* <= 0`. A scalar model may nevertheless produce
`C_A* > 0` there, creating a spurious feasible consultation region. For
`A in {M1O,M2O}`, report the secondary confirmation quantities

\[
L_{A,\mathrm{induced}}^+
=\mathbb E_w[W_A^+\mathbf1_{N^0}],\qquad
p_{A,\mathrm{induced}}
=\frac{\mathbb E_w[\mathbf1_{\{C_A^*>0\}}\mathbf1_{N^0}]}
       {\mathbb E_w[\mathbf1_{N^0}]}.
\]

The induced loss is an unconditional contribution in the original weights;
the second quantity is a conditional weighted proportion of cases. Report
both at grid and configuration level. They prevent good active-region
performance from hiding false-positive consultation regions elsewhere.
If either conditioning set has zero weighted mass, its conditional loss,
quantiles or proportion are undefined and must be labeled as such, not zero.
The unconditional induced loss is zero when its set is empty.

## Fitting conventions and sensitivities

Calibration must reach a global minimum of each one-dimensional discovery
objective, not a selected local solution or a coefficient grid whose bounds
are adjusted after seeing confirmation. The operational objective need not
be globally convex. Use the following deterministic global procedure for
its finite-sample piecewise-linear objective. For each discovery case write
`a=Delta_now`, `b=gamma Delta_static`, `t=max(C_T*,0)`. If `b != 0`, collect
the breakpoints `-a/b` and `(t-a)/b`; cases with `b=0` contribute constant
loss. Sort and deduplicate the breakpoints, combine weighted slope changes,
and sweep them to evaluate the aggregate objective at every breakpoint and
its slope on every intervening region and both unbounded tails. Identify
the global minimum and its entire minimizing set, including flat intervals,
rays and isolated points. For the [0,1] sensitivity also include domain
endpoints and restrict the regions to that domain. Do not rely on an arbitrary
local optimizer, its plateau representative, or a bounded coefficient grid.
Retain the method, minimum, minimizing regions and selected coefficient.
A fit that cannot be verified must not be interpreted as evidence against
scalar reducibility.

For functional LAD and functional OLS fits, retain the existing convention:
for multiple minimizing coefficients, select the minimizer nearest to 1;
if a tie remains, select the smaller coefficient. If the objective is
constant in c (including all static inputs zero), choose 1 and report lack
of identification.

For operational fits, freeze the corresponding primary discovery functional
LAD scalar `c_F` first (global for M1, configuration-specific for M2, always
at the same gamma). Among **all global operational minimizers**, apply this
lexicographic rule:

1. Minimize `|c-c_F|`.
2. If tied, minimize `|c|`.
3. If still tied, choose the numerically smallest c.

For flat intervals or rays consider the nearest point to `c_F`, not merely
their endpoints. If the operational objective is constant over R, choose
`c_F` and report lack of operational identification. The constrained
operational sensitivity uses the same frozen primary `c_F` as reference,
selecting only among minimizers in [0,1]. This gives the scalar approximation
a favorable and stable choice among operationally equivalent discovery fits.

Do not introduce a scientific epsilon to define plateaus. Only documented
machine-precision/implementation tolerances for numerically identical
objective values and slope arithmetic may be used; their exact rules must
be recorded before confirmation inspection. Do not add an intercept or bound
unconstrained primary fits to [0,1].

Preregister two secondary sensitivities, fitted on discovery and frozen
alongside primary coefficients: (i) functional weighted OLS instead of LAD;
(ii) coefficients restricted to [0,1] for both functional and operational
objectives, labeled GSCH-specific. Constrained operational fits must minimize
their constrained objective, not simply clip an unconstrained coefficient.
These sensitivities cannot replace primary results. A configuration-specific
constrained success alone does not establish a *global* contraction.

For all comparative estimands, a zero denominator yields an undefined ratio;
report the absolute losses and paired difference instead. Do not add an
epsilon, discard the case, truncate negative improvement, or assign a perfect
score to 0/0. Report small positive denominators alongside ratios so large
relative values cannot substitute for absolute evidence.

## Confirmation uncertainty

Use **10,000 bootstrap replicates** and pointwise **95% percentile intervals**
(2.5th and 97.5th percentiles, linear quantile interpolation). Fix the bootstrap
RNG before execution: NumPy `default_rng(SeedSequence([20260915, group_id]))`
with `group_id=0,...,18`. This is inference resampling of frozen records, not
generation of new SGD trajectories.

In each replicate, each base group independently samples 30 confirmation seed
indices with replacement from 20–49. Use that same sampled list simultaneously
for all four teacher configurations in the group, retaining every query and
checkpoint of each sampled trajectory. Do not bootstrap query cases, resample
the four configurations independently, or impose one shared seed sample across
all 19 groups. Configurations remain fixed, not bootstrap sampling units.

Use the same replicate indices for all models, both questions, all gammas
and paired comparisons. Do **not** refit scalars in these replicates. The
intervals quantify confirmation-performance variation conditional on the
discovery-calibrated coefficients, not discovery-fit uncertainty.

Recompute hierarchical aggregate losses inside each replicate and form RF/R/G
ratios from these aggregates, never from an average of per-seed ratios. Report
95% intervals for losses, paired differences and comparative estimands at grid
and configuration level. If a ratio has undefined replicates, report their
number and do not label a finite-replicate-only interval an unconditional
95% interval; retain the valid absolute-loss intervals. Curve bands, if shown,
are pointwise from these same replicates, not simultaneous confidence bands.

Use these same paired replicates for secondary active-region and induced-region
diagnostics. Retain each sampled record's original target/M0 subset membership;
recompute hierarchical weights and conditional numerators/denominators in the
resampled population. Do not refit models or select a new model-specific set.
Report undefined conditional replicates using the same explicit-coverage
convention as other zero-denominator ratios.

All intervals are descriptive uncertainty summaries; no binary equivalence
test or familywise claim follows from their multiplicity across the fixed grid.

## Interpretation registered before confirmation

Report magnitudes, uncertainty, per-configuration patterns, seed dispersion,
and dependence on gamma. No preferred gamma will be selected. No 5%, 10%,
20%, P90 or other equivalence margin is introduced. Expressions such as
“nearly all,” “little,” and “negligible” below are qualitative interpretations
to be supported by full numerical results, not hidden numerical cutoffs.
Mixed or imprecise findings remain unresolved rather than forced into a case.

A large `R1+`, `R2+` or `G_2|1+` alone is not evidence of a practically large
operational discrepancy or improvement. Interpret every relative reduction
alongside the absolute losses and their confidence intervals, active-region
losses, induced-region diagnostics, and observed feasible-threshold/width
scales. No distribution over consultation cost is assumed: neither these
losses nor reductions are expected routing-error probabilities. The induced
positive-threshold proportion is a probability over weighted cases conditional
on `N^0`, not over consultation costs.

Good scalar performance on the active region alone cannot establish general
operational redundancy. Within the frozen synthetic fixed grid and B2 surrogate
threshold formulation, successful compression across the full population and
its diagnostics would remove the current empirical justification for proceeding
to EP001-C centered on the exact transport operator. This conclusion does not
extend to divergent policies, external applications or real-world cost distributions.

**Case A — Global scalar suffices.** If functional M1^F and operational M1^O
each remove nearly all their respective baseline discrepancies and M2 adds
little consistently across the fixed grid, strong global scalar reducibility
is supported within this grid. The separately calibrated objectives must
still be identified: success of two different coefficients does not establish
that a single common coefficient achieves both. If the relevant global
coefficients also lie in [0,1], contraction is additionally compatible with
the findings. This triggers STOP/REFRAME before EP001-C, not automatic advance.

**Case B — Functional non-scalarity but operational reducibility.** If
functional residuals persist but operationally optimized M1^O or M2^O makes
feasible-cost disagreement negligible relative to M0 across the grid, remaining
mathematical complexity is largely irrelevant to this routing comparison.
This does not justify EP001-C centered on the exact transport operator.

**Case C — Regime-dependent scalar transport.** If M1 is materially worse than
M2 but M2 removes nearly all discrepancy, the explanation is regime-dependent,
approximately scalar transport; describe it as scalar decay only when the
coefficient values support contraction rather than amplification or sign change.
Do not proceed automatically to EP001-C. Whether known configuration variables
predict c is a possible later question, outside B2 and not implemented here.

**Case D — Residual non-scalar operational information.** If even oracle-favored,
configuration-specific, operationally calibrated M2^O leaves reproducible
feasible-cost disagreement across multiple configurations and seeds, assess
its absolute scale and uncertainty. Such residual routing-relevant structure
would justify *designing* EP001-C. Nonzero numerical residual alone is
insufficient. Do not call it “state dependence” without characterization:
state, query x, checkpoint or another microscopic variable may be involved.

## Secondary continuity and exposed block

Only after primary definitions and discovery fits have been frozen, report
the old eligible subset as a secondary continuity analysis. Evaluate the same
primary-fitted coefficients on that subset, renormalizing the hierarchical
weights within its trajectories; do not recalibrate to rescue an endpoint.
Its conclusions cannot change the primary interpretation.

Configurations 76–79 always remain a separate previously exposed/motivating
block, including eligible analyses. If reported, apply frozen primary global
coefficients and fit any block-specific M2 coefficients on its discovery seeds
only, labeling all block results non-confirmatory for the motivating hypothesis.
Never include this block in primary grid means or confidence intervals.

## Pre-execution audit and compatibility notes

The prior read-only audit established the following without scalar fitting:

- Old eligibility includes 53.0158% of discovery and 53.0324% of confirmation
  stored cases over the original 80-configuration grid.
- Negative routing thresholds are common in the all-case population.
- Restricting M0 disagreement to `C_D >= 0` reduced mean width by less than
  1% in every audited split/gamma/population grid aggregate. Those audit
  aggregates used all 80 configurations; they are not B2 primary estimates.
- Feasible-domain width is nevertheless required because it matches the
  nonnegative incremental cost in the problem formulation.
- Configs 76–79 share base trajectories and queries; config79 motivated SRH,
  so the entire quartet is excluded from primary confirmation.
- No M1/M2 fits or SRH reducibility diagnostics for configs 0–75 were inspected
  during the audit or preparation of this preregistration. The exposure record
  includes previously generated EP001-A/B outputs and permitted M0 audit
  summaries; it does not claim these data had never been computed or analyzed.

The implementation is authoritative about shared trajectories. The older
EP001-A plan's blanket independent-stream wording conflicts with its later
reuse provision and the runner's shared-quartet implementation. B2 uses the
actual dependence structure. Existing EP001-B summaries condition on eligibility
and cannot serve as primary B2 estimates. Its trajectory column
`median_delta_c` stores median `E_transport` rather than gamma times that
quantity; future B2 calculation must derive thresholds from raw values rather
than inherit that mislabeled column. No existing code is changed by this draft.

Sources: `code/ep001/validation.py` (`reversal_metrics`),
`code/ep001/run_ep001a.py` (`rng_for`, `append_rows`, `run`),
`code/ep001/analyze_ep001b.py` (`transport_values`, `analyze`),
`docs/experiments/ep001_natural_transport.md`,
`docs/experiments/ep001b_operational_relevance.md`, and Decisions 009–010 in
`docs/research_log.md`, `docs/theory/primary_notes.md` and the frozen paper.

## Claim boundaries and execution gate

B2 studies compressibility of a mathematical transport functional. It does
not validate that functional against external real-world ground truth, prove
operational superiority of an exact transport router, study divergent policy
trajectories, or establish prevalence in applications. The 76 primary
configurations form a fixed synthetic grid, with families designed to include
anisotropic transport behavior. Conclusions are conditional on that grid,
its natural SGD trajectories, the oracle quantities and the common-coupled
surrogate assumptions.

Actual cumulative routing consequences under divergent policies would require
EP001-C if B2 warrants designing it. This preregistration provides no authority
to execute B2 or C. Later authorized execution must preserve the source raw
data, record source and preregistration hashes, freeze discovery coefficients
before evaluating confirmation, and preserve the first analysis outputs.
Numerical/implementation failures are recorded and corrected transparently;
the population, models and interpretation rules are not tuned to the results.
