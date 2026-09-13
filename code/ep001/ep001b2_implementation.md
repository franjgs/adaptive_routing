# EP001-B2 implementation notes

Specification: `docs/experiments/ep001b2_scalar_reducibility.md`, frozen in
commit `09404c92970a909b8263b11e334cb7b29ce7289a`. This implementation is a
library of analysis primitives, not an enabled real-data execution command.
Running the module exits with an explanatory message. Tests use synthetic
fixtures only and never open the preserved experiment. No scientific results
are produced as part of implementation validation.

## Data and workflow

`load_raw`/`validate_structure` require the frozen wide NPZ schema: 80 configs,
50 seeds, five checkpoints (5,20,100,500,2000), 64 queries per checkpoint,
aligned ID vectors and an N-by-11 `deltas` array. They check unique complete
configuration/seed/checkpoint/query keys, split membership, and all manifest
distribution/learning-rate/noise settings. `finite_population` selects configs
0–75 or explicitly exposed 76–79 and checks only `delta_now` and columns
0–9. Eligibility and missing reversal diagnostics do not affect primary
membership. Exclusion reports identify counts per configuration/trajectory.

`derived` uses H=10 and gamma=0.5,0.9,1 separately. With x=Delta_static and
y=Delta_adapt, x=(sum gamma^k) Delta_0, y=sum gamma^k Delta_k for k=0,...,9.
Target threshold is Delta_now+gamma*y. M0 is Delta_now+gamma*x. The outer
gamma is retained for signed threshold differences, including their medians.
All required inputs must be finite; overflow is an error rather than a filter.

`calibrate_discovery` rejects confirmation or exposed records, fits M1 globally
and M2 by configuration, and returns immutable `Calibration`/`ScalarFit`
records. Functional LAD and operational fits are distinct. OLS and [0,1]
sensitivities are also included. `expected_configs` defaults to the complete
primary grid; reduced primary sets support synthetic testing. It cannot
authorize exposed configs. For later authorized use, freeze every gamma's
calibration and record source/preregistration hashes before confirmation.
No automatic loader-to-fit-to-confirmation pipeline is provided in this task.

`predictions`, `evaluate_fixed`, `functional_summary`, `operational_summary`
and `disagreement_curve` consume fixed coefficients and never fit models.
Use the full grid by default, then the same frozen predictions for configuration
and trajectory reports. For old-eligible continuity, subset frozen predictions
and recompute hierarchical weights; report missing trajectories explicitly.
Primary APIs reject the exposed block; optional motivating-block calibration
is not automatically run or pooled with primary inference.

## Functional optimization

For nonzero x, w|y-cx| = w|x| |y/x-c|. Thus a weighted median of y/x with
mass w|x| globally minimizes the through-origin LAD objective. An exact half
mass boundary gives the entire interval between adjacent ordered ratios.
Rows with x=0 contribute w|y| to the attained loss and cannot identify c.
Choose the minimizer nearest 1. Restricting a convex LAD objective to [0,1]
projects its minimizing interval onto that domain. All-zero x selects 1.
OLS uses sum(w*x*y)/sum(w*x*x), selecting 1 if the denominator is zero.

## Global operational optimization

Write a=Delta_now, b=gamma*x and t=max(C_T*,0). Each term is
w|max(a+bc,0)-t|. For b!=0 its possible breakpoints are -a/b (activation)
and (t-a)/b (target match). As c increases, the slope jump at activation is
-w|b| and at target match is +2w|b|, regardless of the sign of b. When t=0
the events coincide and combine to +w|b|. Terms with b=0 are constant.
The initial left slope is -sum_{b<0} w|b|; the right tail slope is
sum_{b>0} w|b|. Negative-left/positive-right slopes increase loss toward
the corresponding infinite tail; zero slopes permit minimizing rays.

`operational_fit` sorts and combines events, evaluates the first objective
directly, integrates slopes through all events, and examines all breakpoint
values, flat intervals, and flat tails. It retains disconnected minimizing
components and merges touching components. No local optimizer or guessed
search range is used. For the constrained sensitivity, add 0 and 1 as
zero-jump events and search only the restricted domain; do not clip an
unconstrained operational solution.

Project frozen c_F onto each minimizing component, then compare candidates
lexicographically by (|c-c_F|, |c|, c). This also handles isolated minima,
plateaus and a constant objective. The returned fit records its coefficient,
attained objective, minimizing regions, algorithm and comparison tolerance.
A direct reevaluation of the chosen optimum must agree with the sweep.

Numerical comparison rules, fixed before any real fit: calculations use
NumPy longdouble, whose precision is platform dependent. Let eps be
`np.finfo(np.longdouble).eps`. LAD cumulative half-mass comparisons use
`64*eps*n*total_mass`. Operational slope comparisons use
`64*eps*m*sum(abs(jumps))`, with m the event count (including domain endpoints).
Objective comparisons use `64*eps*m*(abs(first_objective)+sum(abs(increments)))`.
The direct-check allowance additionally includes `64*eps*abs(actual_objective)`.
There is no absolute unit-scale epsilon, coefficient rounding grid or scientific
equivalence margin. Flat tails use exact coefficient-sign tests. Nonfinite
breakpoints or a failed direct/sweep check raise errors. Platform precision
and per-fit tolerances must be retained in later execution metadata.

## Weights, summaries and undefined quantities

`hierarchical_weights` gives equal mass to configs, then seeds within config,
then cases within seed. `conditional_mean` and `quantiles` restrict those
original weights and normalize only by the subset mass. Weighted quantiles
use the inverse empirical CDF (smallest value attaining the requested mass).
The original target/M0 active set is shared by all model summaries. Induced
loss is unconditional weighted width outside that set; induced positive
proportion is conditional on that complement. Empty conditional sets return
None; the unconditional empty-set contribution is zero.

`reduction` returns None for any zero baseline loss, including 0/0; it keeps
negative reductions when the approximation is worse. No epsilon, clipping or
infinite ratio is introduced. `comparisons` returns absolute paired differences
alongside R1/R2/G; callers label these RF1/RF2/GF for functional losses and
R1+/R2+/G+ for feasible operational losses. R-squared is None for zero weighted
target variance. Absolute loss outputs precede ratio interpretation.

`disagreement_curve` emits the union of clipped threshold endpoints with the
right-continuous weighted step height at each endpoint. Query iff C<threshold;
equality means no query. Interval widths times heights give its exact
piecewise-constant integral, checked against mean W+ with the frozen
rtol=1e-10, atol=1e-12. These checks are not relevance thresholds.

## Bootstrap

`bootstrap_multiplicities` defaults to 10,000 replicates and returns shape
(replicates,76,30). Each group uses
default_rng(SeedSequence([20260915,group_id])); its 30 resampled seed indices
are reused across its four configs. Different groups draw independently.
Reusing the same count array pairs every gamma, objective and model.

`trajectory_table` first averages fixed case losses/numerators within each
confirmation trajectory. `bootstrap_aggregate` applies multiplicities and
averages seeds then configs, returning both configuration and grid replicates.
No coefficient or fitting function enters this API. `bootstrap_comparisons`
forms ratios from replicate aggregate model losses and uses 95% percentile
intervals with NumPy linear interpolation. `percentile_interval` explicitly
reports undefined replicates and withholds an unconditional interval when any
are undefined; NaN/inf is rejected in favor of explicit None.

`bootstrap_diagnostics` aggregates the original active/inactive indicators,
width numerators and masses with those same counts. `bootstrap_case_weights`
provides repeated-case mass for conditional quantiles and optional curve bands;
subset membership and predictions stay fixed. For secondary subsets with
empty trajectories, report coverage and undefined conditionals rather than
silently counting an empty conditional as zero. Confidence intervals are
conditional on discovery-fitted coefficients; no refitting or configuration
resampling occurs inside confirmation replicates.

## Validation command

`python3 -B -m unittest discover -s code/ep001 -p 'test_*.py' -v`

Synthetic tests cover algebra, weighted LAD versus brute force, operational
global minima versus independent breakpoint and dense-grid oracles, plateaus,
disconnected minima, both infinite tails, constraints, unequal sampling weights,
conditional measures, induced regions, curve integration, bootstrap pairing,
fixed-fit evaluation, zero denominators, schema integrity and primary exclusions.
No real B2 scientific result is needed by any test.
