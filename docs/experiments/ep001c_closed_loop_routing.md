EP001-C — Closed-loop routing with transported adaptation value

Status: preregistration draft
Scope: synthetic closed-loop experiment extending EP001-A/B/B2
Purpose: test whether explicitly valuing the future learning consequence of consulting the expensive predictor improves sequential routing performance once different routing policies are allowed to generate different learner trajectories.

## Pre-execution amendment history

The original preregistration was frozen in commit `157765a249aab85e55a3e0984ba96d54710f5650` with SHA-256 `8340ee815f2862f8b6d5bdc2d841e4c11b789a9cb1d6a8dbbb1e9bc3da0e44b8`.

Before any EP001-C implementation, discovery, confirmation, scalar fitting, or inspection of an EP001-C result, an omission was identified: the trajectory length \(T\) was referenced but not specified. This amendment fixes \(T=2000\) sequential operational rounds per trajectory. It is a protocol-completeness correction, not a result-driven modification. The choice is consistent with the numerical scale already used in EP001, but EP001-A does not scientifically determine \(T\).

⸻

1. Motivation

EP001-A, EP001-B and EP001-B2 studied the future effect of an expensive-model query under a controlled counterfactual coupling.

The established setting contains:

* a cheap adaptive predictor (F_\theta);
* an expensive predictor (D);
* a routing decision between (F_\theta) and (D);
* an immediate operational consequence of consulting (D);
* a pseudo-update of (F_\theta) using the same response returned by (D);
* reliable target feedback (Y) arriving later, independently of routing;
* subsequent learning of (F_\theta).

The previous experiments established:

1. the effect of the query-induced update can be transported through subsequent learning and need not preserve its initial sign;
2. natural sign reversals exist but failed the preregistered EP001-A confirmation criterion and are therefore not the empirical centerpiece;
3. ignoring transport can generate a non-negligible valuation error;
4. in EP001-B2, transported adaptation value was not well represented by one universal scalar across configurations, but was extremely well approximated by a configuration-specific scalar within each frozen configuration.

However, EP001-B and EP001-B2 evaluated routing-threshold discrepancies on common frozen trajectories. They did not test whether those differences lead to better sequential decisions when each routing policy generates its own learner trajectory.

EP001-C addresses that missing question.

⸻

2. Primary research question

Does explicitly valuing the transported future learning effect of an expensive-model query improve the sequential operational objective relative to routing based only on its immediate value?

Equivalently:

[
\boxed{
\text{Does future-aware routing outperform myopic routing
once routing decisions change the future learner state?}
}
]

The experiment is deliberately restricted to the existing synthetic EP001 setting.

It does not introduce concept drift, new application domains, new model classes, or new forms of delayed feedback.

⸻

3. Secondary research questions

EP001-C will also determine:

1. whether the static approximation used in EP001-B provides useful closed-loop routing decisions;
2. whether the configuration-specific scalar compression identified in EP001-B2 remains operationally useful once trajectories diverge;
3. how much closed-loop improvement is obtained from exact knowledge of the reference-coupled transported adaptation quantity defined by EP001;
4. whether the practical approximation captures a substantial fraction of that closed-loop improvement;
5. whether differences arise through:
    * lower prediction loss,
    * fewer expensive-model consultations,
    * or a different balance between both;
6. whether early routing differences amplify, disappear, or remain small as the learner trajectories diverge.

⸻

4. Non-goals

EP001-C does not attempt to establish:

* universal scalar reducibility of transported value;
* a general theory of optimal routing;
* concept-drift adaptation;
* deployment under non-stationarity;
* practical estimation of the scalar transport factor from real data;
* performance on a real application;
* superiority over state-of-the-art cloud–edge, learning-to-defer, active-learning, or forecasting systems.

Those questions remain outside this experiment.

⸻

5. Environment

Retain the same basic synthetic linear environment used in EP001-A/B/B2.

The environment is stationary while the cheap learner adapts. Routing demand may therefore decrease as the learner approaches the stationary target. If routing activity and policy differences become concentrated in the initial learning transient, EP001-C must be interpreted as evidence about transient adaptive routing in the stationary EP001 environment. It must not be interpreted as evidence about persistent routing demand in continuously changing or nonstationary environments.

5.1 Target process

[
Y_t = {w^\star}^{\top}X_t+\epsilon_t.
]

5.2 Cheap adaptive predictor

[
F_{\theta_t}(x)=\theta_t^\top x.
]

Define

[
e_t=\theta_t-w^\star.
]

5.3 Expensive predictor

[
D(x)=(w^\star+b)^\top x+\nu.
]

The expensive predictor is imperfect.

Conditional assumptions remain those already used in the frozen EP001 formulation, including

[
\mathbb E[\nu\mid x]=0,
\qquad
\mathbb E[\nu^2\mid x]=\sigma_D^2.
]

5.4 Query-induced pseudo-update

If (D) is consulted at time (t), its returned response may update (F) according to the same pseudo-supervised update used in the existing EP001 formulation.

For the linear SGD case,

[
\theta_t^+

\theta_t
+
\eta_D X_t
\left[
D(X_t)-\theta_t^\top X_t
\right].
]

5.5 Reliable delayed feedback

The reliable target (Y_t) arrives after the fixed delay (\tau), independently of the routing action.

Maintain the existing timing convention:

feedback associated with time (t) is revealed only after the operational decision and response at time (t+\tau), and can first affect prediction at time (t+\tau+1).

When reliable feedback arrives, the corresponding update of (F) follows the same rule already used in the EP001 environment.

⸻

6. Sequential routing protocol

At each time (t):

1. observe (X_t);
2. compute the information available to the routing policy;
3. select
    [
    A_t\in{F,D};
    ]
4. if (A_t=F), output
    [
    \hat Y_t=F_{\theta_t}(X_t);
    ]
5. if (A_t=D), output
    [
    \hat Y_t=D(X_t),
    ]
    incur query cost (C_D), and apply the query-induced pseudo-update to (F);
6. after the operational response, reveal any reliable feedback whose delay expires at that time;
7. update (F) from the newly available reliable feedback;
8. proceed to (t+1).

Each routing policy maintains its own learner state.

Therefore, after the first routing disagreement,

[
\theta_t^{\pi_1}\neq\theta_t^{\pi_2}
]

is allowed and expected.

No attempt will be made to recouple policy trajectories after they diverge.

⸻

7. Objective

The operational objective for policy (\pi) is

[
J^\pi

\mathbb E_\pi
\left[
\sum_{t=1}^{T}
\gamma^{t-1}
\left(
\ell(\hat Y_t,Y_t)
+
C_D,\mathbf 1{A_t=D}
\right)
\right].
]

Squared prediction loss will be used unless the existing EP001 implementation requires another already-frozen convention.

The same objective must be used for every compared routing policy.

Lower (J^\pi) is better.

For interpretability, report prediction loss and query cost separately in addition to their sum.

⸻

8. Routing policies

The primary comparison contains four policies.

8.1 P0 — Myopic router

The myopic router values only the immediate operational effect of consulting (D).

Using the existing notation,

[
\Delta_{\mathrm{now},t}.
]

It queries when

[
\Delta_{\mathrm{now},t}>C_D.
]

This is the primary baseline.

⸻

8.2 P1 — Static future-aware router

This policy uses the static approximation studied in EP001-B.

For horizon (H),

[
B_H

\sum_{k=0}^{H-1}\gamma^k
]

and

[
\Delta_{\mathrm{static},t}

B_H\Delta_{0,t}.
]

Its query valuation is

[
V_t^{\mathrm{static}}

\Delta_{\mathrm{now},t}
+
\gamma\Delta_{\mathrm{static},t}.
]

It queries when

[
V_t^{\mathrm{static}}>C_D.
]

This policy represents future-aware routing that ignores transported attenuation or distortion.

⸻

8.3 P2 — Scalar transported router

This policy uses the configuration-specific scalar compression identified in EP001-B2.

P2 is deliberately privileged by configuration-specific calibration. Its purpose is to test whether the strong within-configuration scalar compression observed in EP001-B2 survives closed-loop execution.

P2 is not a deployment-ready policy. This experiment does not establish that the relevant coefficient is known or estimable online in a real system. If P2 performs well, the supported conclusion is limited to the finding that the frozen configuration-specific scalar compression preserves useful routing information under closed-loop execution in the tested synthetic configurations. It does not imply that a real router would know the configuration ID, that (c) is a universal persistence factor, or that (c) can be estimated online.

For each frozen configuration and discount factor,

[
\widehat{\Delta}_{\mathrm{adapt},t}

c_{\gamma,j},
\Delta_{\mathrm{static},t},
]

where (c_{\gamma,j}) is fixed before evaluation.

Its query valuation is

[
V_t^{\mathrm{scalar}}

\Delta_{\mathrm{now},t}
+
\gamma
\widehat{\Delta}_{\mathrm{adapt},t}.
]

It queries when

[
V_t^{\mathrm{scalar}}>C_D.
]

The coefficient used by this router must not be fitted on its own evaluation trajectory.

The source of (c_{\gamma,j}) must be frozen before confirmation evaluation.

The preferred primary version is the configuration-specific coefficient justified by EP001-B2.

A global scalar may be retained as a secondary sensitivity analysis but is not a separate primary policy.

⸻

### 8.4 P3 — Exact reference-coupled transport router

This policy uses the transported adaptation quantity defined by the existing EP001 theory, evaluated exactly for its common-subsequent-update reference counterfactual.

For the current learner state and current query candidate,

\[
\Delta_{\mathrm{adapt},t}^{\mathrm{ref}}
=
\sum_{k=0}^{H-1}
\gamma^k
\Delta_{k,t},
\]

where each \(\Delta_{k,t}\) is computed using the exact transport operator \(K_k\) under the same common-subsequent-update coupling used in the theoretical development and in EP001-B/B2.

Its query valuation is

\[
V_t^{\mathrm{ref}}
=
\Delta_{\mathrm{now},t}
+
\gamma
\Delta_{\mathrm{adapt},t}^{\mathrm{ref}}.
\]

It queries when

\[
V_t^{\mathrm{ref}}>C_D.
\]

At each actual state visited by P3, the policy recomputes this exact reference-coupled transported quantity for the current query candidate. The word “exact” refers to exact evaluation of the EP001 reference-coupled counterfactual, not exact evaluation of the future closed-loop effect.

It is **not** an oracle for the full closed-loop routing problem.

In particular,

\[
\Delta_{\mathrm{adapt},t}^{\mathrm{ref}}
\]

does not generally equal the Bellman or policy-dependent continuation-value difference

\[
Q^\pi(s_t,D)-Q^\pi(s_t,F),
\]

because after the current decision the two closed-loop trajectories may make different future routing decisions and therefore receive different future query-induced pseudo-updates.

P3 is included to answer a narrower and directly relevant question:

> if the exact reference-coupled transported value developed in EP001 were available at every decision point, would using it as a routing surrogate improve the actual closed-loop trajectory?

The actual P3 trajectory is not constrained to follow the reference coupling. Future routing decisions may differ, learner states may diverge, and future query-induced pseudo-updates may therefore differ. Thus P3 is a receding, local, reference-coupled routing surrogate. It is mathematically exact for the reference counterfactual used to define \(\Delta_k\), but it is not exact for the closed-loop continuation value generated by P3 itself.

This makes P3 the natural reference for evaluating P1 and P2 without claiming that it is the globally optimal future-aware routing policy.

⸻

## 9. Reference-coupled transport information restriction

P3 may use:

- the current learner state;
- the current input \(X_t\);
- the known synthetic data-generating distribution;
- the frozen EP001 model parameters;
- the exact reference-coupled transport operators \(K_k\) required to compute the EP001 transported quantity.

P3 must not inspect:

- future realized inputs \(X_{t+1:t+H}\);
- future realized targets;
- future target noise;
- future expensive-model noise;
- future routing decisions;
- future realized learner trajectories.

Thus P3 computes an **expected reference-coupled transported effect**, not a realized future effect.

The quantity is exact only under the common-subsequent-update reference coupling used to define \(\Delta_k\).

Once EP001-C runs in closed loop, policies are allowed to diverge and subsequent query-induced updates need not remain common. Therefore P3 must not be described as:

- a full closed-loop oracle;
- an optimal router;
- a Bellman-optimal policy;
- an upper bound on achievable closed-loop performance.

A true full closed-loop oracle would require evaluating the policy-dependent continuation value associated with each present action, including the effects of future routing decisions on future learner states. That is a different problem and is outside EP001-C.

No Monte Carlo rollout oracle, dynamic-programming oracle, or other full continuation-value method will be introduced in EP001-C.

⸻

10. Closed-loop coupling across policies

For fair comparison, policies evaluated under the same experimental replicate should share the same exogenous random stream wherever possible:

* initial learner state;
* (X_t);
* target noise (\epsilon_t);
* expensive-model noise (\nu_t);
* delayed-feedback schedule.

Routing decisions and learner updates are policy-specific.

Thus:

[
X_t^{P0}=X_t^{P1}=X_t^{P2}=X_t^{P3}
]

within a paired replicate, while

[
\theta_t^{P0},
\theta_t^{P1},
\theta_t^{P2},
\theta_t^{P3}
]

may diverge.

This paired exogenous stream is required to reduce comparison variance without artificially forcing learner trajectories to remain equal.

⸻

11. Experimental configurations

EP001-C should remain anchored to the frozen EP001 parameter family.

No new configuration family should be introduced solely to obtain stronger routing differences.

The initial experiment should use configurations already characterized in EP001-A/B/B2.

Configuration selection must be fixed before evaluating the confirmation split.

If a smaller subset is required for computational reasons, its selection rule must be defined from information available before confirmation evaluation and must not depend on EP001-C confirmation outcomes.

⸻

12. Horizon and discounting

Use the previously studied horizon

[
H=10
]

unless implementation analysis identifies a genuine incompatibility with the closed-loop protocol.

Primary discount factors remain

[
\gamma\in{0.5,0.9,1.0}.
]

The same (H) and (\gamma) must be used consistently by P1, P2 and P3.

The sequential operational trajectory length is fixed at

\[
T=2000.
\]

Every policy is evaluated for exactly 2000 sequential operational rounds per trajectory. This is a fixed EP001-C design parameter, not a discovery-tuned parameter.

⸻

13. Query-cost sweep

A single (C_D) is insufficient because routing policies can agree trivially when queries are almost free or prohibitively expensive.

Therefore evaluate a preregistered grid of non-negative costs:

[
C_D\ge 0.
]

The cost grid must cover:

1. a low-cost region where most policies query frequently;
2. an intermediate region where routing decisions differ;
3. a high-cost region where queries become rare.

The numerical grid must be selected from discovery data or from previously frozen EP001 scale information, never from confirmation outcomes.

Primary conclusions must not depend on one hand-selected query cost.

⸻

14. Discovery and confirmation

Maintain strict separation between discovery and confirmation.

The existing seed split should be reused wherever technically compatible:

* discovery: seeds (0)–(19);
* confirmation: seeds (20)–(49).

Discovery may be used only to:

* debug implementation;
* select a fixed cost grid;
* verify that the experiment covers non-trivial query regimes;
* freeze any coefficient required by P2 if the existing B2 coefficient cannot be reused directly;
* define numerical tolerances and plotting ranges.

Discovery must not be used to redefine the scientific success criterion after observing policy performance.

Once the confirmation protocol is frozen, no retuning or rerunning of confirmation seeds is allowed.

⸻

15. Primary outcomes

15.1 Total operational objective

For each policy:

[
J^\pi(C_D,\gamma).
]

Primary paired comparisons:

[
J^{P0}-J^{P1},
\qquad
J^{P0}-J^{P2},
\qquad
J^{P0}-J^{P3}.
]

Positive values indicate improvement over the myopic router.

⸻

### 15.2 Reference-transport closed-loop gain

Define

\[
G_{\mathrm{ref}}
=
J^{P0}-J^{P3}.
\]

This measures the closed-loop improvement obtained by routing with the exact **reference-coupled EP001 transported value** rather than with immediate value alone.

It does not measure the maximum gain attainable by an optimal future-aware router.

If \(G_{\mathrm{ref}}\) is negligible, the transported quantity developed in EP001 has little additional operational value over myopic routing in the tested regime.

This does not rule out benefits from a more general policy-dependent continuation-value formulation.

⸻

### 15.3 Fraction of reference-transport gain captured by scalar compression

When

\[
G_{\mathrm{ref}}>0,
\]

define descriptively

\[
Q_{\mathrm{scalar}}
=
\frac{J^{P0}-J^{P2}}
     {J^{P0}-J^{P3}}.
\]

This measures how much of the closed-loop gain obtained using exact reference-coupled transport is reproduced by the scalar approximation.

The ratio is secondary and must never be interpreted without the absolute numerator and denominator.

It is not a fraction of globally attainable or optimal future-aware routing gain.

No arbitrary threshold for a “sufficient fraction captured” is preregistered.

⸻

16. Secondary outcomes

For each policy and cost:

* cumulative prediction loss;
* cumulative query cost;
* number and fraction of queries;
* time-resolved cumulative objective;
* routing-disagreement rate relative to P0;
* routing-disagreement rate between P2 and P3;
* learner excess risk over time;
* final learner excess risk;
* distribution of consecutive query runs;
* distribution of intervals between queries.

Report the following fixed temporal segments: early \(t=1,\ldots,666\), middle \(t=667,\ldots,1333\), and late \(t=1334,\ldots,2000\). Their lengths are respectively 666, 667, and 667 rounds. For each segment, report query rate, objective/loss contribution, and policy disagreement. These are diagnostics only and do not replace the primary whole-trajectory objective.

⸻

17. Trajectory divergence diagnostics

Because EP001-C specifically tests closed-loop effects, trajectory divergence is itself informative.

For paired policies (\pi_a,\pi_b), record:

[
|\theta_t^{\pi_a}-\theta_t^{\pi_b}|
]

over time.

Also record the first time at which their routing decisions differ:

[
t_{\mathrm{div}}

\min{t:A_t^{\pi_a}\neq A_t^{\pi_b}}.
]

These diagnostics are descriptive.

They are intended to determine whether operational differences arise from persistent learner-state divergence or merely isolated routing decisions.

⸻

18. Statistical unit and weighting

The independent experimental unit remains the seed/trajectory within configuration.

Pooled individual time steps are not independent statistical units.

Primary aggregation should preserve the same principle used in EP001-B2:

1. equal weight to each configuration;
2. equal weight to each independent trajectory within configuration.

Time steps within a trajectory contribute to its sequential objective but are not treated as independent replicates.

⸻

19. Uncertainty estimation

Use paired resampling at the trajectory level because all policies within a replicate share the same exogenous random stream.

Bootstrap or another resampling method may be used, but it must:

* preserve policy pairing;
* preserve configuration structure;
* preserve complete sequential trajectories;
* never resample individual time steps as independent observations.

If the existing EP001 convention of 10,000 bootstrap replicates is computationally practical, retain it.

Freeze the resampling procedure before confirmation.

⸻

20. Primary falsification logic

EP001-C is not designed to force a positive conclusion.

Interpretation will follow the hierarchy below.

### Case C1 — Exact reference-coupled transport is operationally useful and scalar compression preserves that value

P3 improves meaningfully over P0 across a non-trivial range of query costs, and P2 reproduces a substantial part of that absolute improvement.

Interpretation:

> the EP001 reference-coupled transported quantity has closed-loop operational value in the tested synthetic regime, and the frozen configuration-specific scalar compression identified in EP001-B2 retains useful decision information after policy trajectories are allowed to diverge.

This would provide a strong justification for testing the mechanism in a natural applied setting.

⸻

### Case C2 — Exact reference-coupled transport is useful, but scalar compression is insufficient in closed loop

P3 improves meaningfully over P0, but P2 provides substantially smaller, inconsistent, or negligible improvement.

Interpretation:

> the exact EP001 reference-coupled transported value contains operationally useful information, but the B2 scalar approximation does not preserve enough of that information once routing policies generate different learner trajectories.

This would motivate investigating a better approximation.

It would not automatically justify restoring the full state-dependent \(K_k\) machinery as a deployable method.

⸻

### Case C3 — Static future valuation is already sufficient

P1 performs approximately as well as P2 and P3 over the operationally relevant query-cost range.

Interpretation:

> the reference-coupled transport correction provides little additional operational value beyond the simpler static future-learning approximation in the tested regime.

This would substantially weaken the case for making the EP001 transport machinery or its scalar compression a central practical contribution.

The broader idea that queries should be valued partly for their future learning effect could still remain valid.

⸻

### Case C4 — Exact reference-coupled transport adds little or no closed-loop value over myopic routing

P3 does not produce a meaningful absolute improvement over P0 across the operationally relevant query-cost range.

Interpretation:

> the EP001 reference-coupled transported adaptation effect characterized by EP001-A/B/B2 does not translate into substantial closed-loop routing benefit in the tested stationary regime.

This would be a strong negative result for the operational relevance of the EP001 reference-coupled transport quantity in the tested stationary regime.

However, it must **not** be interpreted as showing that future learning value is generally irrelevant to routing.

EP001-C does not evaluate the full policy-dependent continuation value

\[
Q^\pi(s_t,D)-Q^\pi(s_t,F),
\]

and therefore cannot falsify more general future-aware routing formulations.

### Case C5 — Reference-coupled transport is actively harmful in closed loop

This case applies when P3 produces systematically worse closed-loop objective than P0 across a non-trivial region of the preregistered query-cost domain, especially if P3 is also worse than P1.

Using the convention that lower (J^\pi) is better, this corresponds to:

\[
J^{P3} > J^{P0}
\]

systematically over a non-trivial cost region.

Interpretation:

> the reference-coupled transported value is not merely operationally unnecessary; repeatedly using it as a closed-loop routing surrogate can systematically degrade performance in the tested regime.

If P3 is also worse than P1, this is evidence that the reference-coupled transport correction can be less useful than the simpler static future-value approximation once policy trajectories diverge.

This would be a strong negative result for using the EP001 reference-coupled transport quantity as a practical routing rule.

It would not invalidate the mathematical derivation of (K_k) for its stated common-update counterfactual.

It would also not establish that future learning value in general is harmful or irrelevant.

⸻

21. No arbitrary success threshold

EP001-C will not preregister an arbitrary percentage improvement required for publication-level success.

The primary report must give absolute quantities first:

* total objective difference;
* prediction-loss difference;
* query-cost difference;
* query-rate difference;
* uncertainty intervals.

Relative percentages may be reported only after the corresponding absolute scale.

Claims of practical importance must be based on the magnitude and consistency of the observed effect, not only statistical detectability.

⸻

22. Required implementation validation before execution

Before any real discovery or confirmation run:

1. unit-test delayed-feedback timing;
2. unit-test query-induced pseudo-updates;
3. verify identical exogenous streams across paired policies;
4. verify policy-specific learner states diverge correctly;
5. verify (C_D=0) and very large (C_D) boundary behavior;
6. verify P0 reproduces the intended myopic rule;
7. verify P1 implements the exact EP001-B static valuation;
8. verify P2 uses only frozen coefficients;
9. verify P3 does not access realized future information;
10. test objective decomposition:
    [
    J =
    J_{\mathrm{prediction}}
    +
    J_{\mathrm{query}};
    ]
11. test reproducibility from fixed seeds;
12. verify discovery and confirmation seed isolation.

No confirmation run may be executed before these checks pass.

⸻

23. Reporting requirements

The final EP001-C report must include, for every (\gamma):

1. absolute (J^\pi) for all policies;
2. paired improvement relative to P0;
3. prediction-loss component;
4. query-cost component;
5. query rate;
6. cost-dependent performance curves;
7. P0/P1/P2/P3 comparisons over the full preregistered cost grid;
8. reference-transport closed-loop gain;
9. scalar fraction of reference-transport gain where interpretable;
10. trajectory-divergence diagnostics;
11. per-configuration results;
12. per-seed dispersion;
13. discovery and confirmation reported separately.

A result must not be summarized only by averaging over costs if policy behavior differs materially across the cost range.

⸻

24. Relationship to previous EP001 results

EP001-C does not invalidate or redefine EP001-A/B/B2.

The sequence is:

* EP001-A: can transported adaptation change sign naturally?
* EP001-B: does transport alter operational query valuation on frozen trajectories?
* EP001-B2: can transported value be compressed to a simple scalar approximation?
* EP001-C: does using transported future value improve actual closed-loop routing?

Thus EP001-C is the operational closure of the existing line rather than a new research direction.

⸻

25. Decision after EP001-C

Only after confirmation results are frozen should the project decide whether to proceed to a natural applied testbed.

Proceeding to an application is justified only if EP001-C shows that future-aware routing has enough closed-loop operational value to merit testing outside the synthetic environment.

The applied novelty audit remains relevant for selecting that later testbed, but does not determine EP001-C.

Concept drift, complementary adaptation timescales, dynamic role redistribution, and model replacement/regeneration remain possible later generalizations and are explicitly outside EP001-C.
