# Adaptive Routing — Project Handover

Last updated: 2026-09-14
Repository HEAD represented: `a36f3930aba027d26a2b79ca082d1a7a5375aea8`
Handover version: 2.2

## 0. Purpose and evidence hierarchy

This is a navigation and state-reconstruction document. It is **not** primary
scientific evidence and must not override a frozen artifact.

When sources disagree, use this hierarchy, report the discrepancy, and retain
the higher-level source as authoritative:

1. frozen machine-readable result artifacts and manifests;
2. frozen preregistrations and experiment-specific result reports;
3. experiment, theory, and literature documentation tied to those artifacts;
4. `docs/research_log.md`;
5. this `docs/HANDOVER.md`;
6. conversational memory or chat summaries.

Known historical-document caveats:

- `README.md` still says that no experiments have run and that `code/` is
  empty. That is stale and contradicted by the EP001 artifacts below.
- The immutable B2/C preregistration files retain pre-execution wording such
  as “draft” or “execution not authorized.” Read them as frozen protocols;
  confirmation manifests and reports establish execution.
- The paper contains the frozen theory/protocol, but its experiment/conclusion
  sections are placeholders and are not a source of current empirical status.

## 1. Instructions for a new session

Before proposing theory, experiments, applications, or code:

1. Read this file completely.
2. Identify the current decision point in Section 10.
3. Read only the primary sources cited for that decision and task.
4. Preserve negative, null, ambiguous, and harmful findings as evidence.
5. Label statements as **theorem**, **empirical result**, **interpretation**,
   **hypothesis**, or **open question**.
6. Do not revive a demoted direction without a concrete problem and new
   evidence.
7. Follow **problem first**: introduce mathematics only when a selected
   scientific problem requires it.

## 2. Current research problem

At a decision time, a cheap adaptive predictor \(F\) and an expensive,
potentially more capable predictor \(D\) are available. Routing to \(D\) can
replace \(F\)'s current response, incur consultation cost, and supply
imperfect supervision to \(F\). Reliable task feedback \(Y\) may arrive later
independently of routing. The objective is task loss plus consultation cost.

**Current scientific question.**

> Is the narrow intersection of adaptive-supervision acquisition and adaptive
> model routing already satisfactorily solved, or is there a practically
> computable and observable approximation to the policy-dependent
> continuation-value advantage of consulting (D) that remains methodologically
> and empirically open?

The broader fact that a query can have immediate operational value and alter
future learning is now treated as a standard sequential-decision structure, not
as a new principle. This does not presuppose that the EP001 reference-coupled
transport operator is a practical solution.

## 3. Current scientific thesis

### General structural novelty hypothesis — rejected/reducible

Decision 011 concludes that the coexistence of immediate operational value and
future learning consequences is representable by standard sequential decision
theory with an appropriately augmented state. It is not, by itself, a new
decision-theoretic structure or a defensible primary novelty claim.

### Algorithmic hypothesis — provisionally partially occupied

The first narrow audit finds that reinforcement-learning-based active learning
already treats supervision acquisition as a sequential action-value problem,
while EER and local model/output-change surrogates already approximate future
learning consequences and learning-to-defer/model routing cover the current
operational decision. This blocks any claim that Bellman/RL approximation of
future supervision value is new in general.

**Provisional status: B — PARTIALLY OCCUPIED / ALGORITHMIC GAP NOT YET
ESTABLISHED.** A possible remaining issue is whether existing methods provide a
computable, observable, and methodologically adequate approximation to the
true policy-dependent continuation advantage for the particular protocol where
the costly output both replaces the current response and pseudo-updates an
adaptive cheap predictor. This is a hypothesis under focused audit, not a
novelty claim.

### Not established / not claimed

- Exact state-dependent transport \(K_k\) is not claimed deployable, necessary,
  or universally beneficial.
- A scalar transport coefficient is not claimed universal, persistent,
  observable online, or available to a real router.
- EP001 does not validate a real cloud--edge, energy/load, LLM, or
  concept-drift router.
- EP001 does not solve a full policy-dependent continuation/Q-value problem.
- No universal factorization such as “learnability \(\times\) future relevance”
  is established or assumed.
- The presence of RL/Q-learning active-learning predecessors does not, by
  itself, establish that this narrow operational intersection is solved; their
  conceptual coverage, information requirements, methodology, and experiments
  must be audited.

## 4. Established mathematical results

Primary sources: [technical notes](theory/primary_notes.md),
`paper/primary/sections/problem_formulation.tex`, and
`paper/primary/sections/theoretical_analysis.tex`.

### T1 — delayed-feedback protocol — established formulation

The router acts before the final response. Choosing \(D\) uses its same
realized output both operationally and as immediate pseudo-supervision for
\(F\). Reliable \(Y_t\) arrives after a fixed routing-independent delay and
may subsequently update/correct \(F\).

**Scope.** This is a model/protocol, not proof of a sufficient state, optimal
routing, or novelty. A teacher query does not purchase ground truth.

### T2 — immediate and single-update values — theorem

In the stated squared-loss linear model, under documented conditional moment
assumptions,
\[
\Delta_{\mathrm{now}}=\alpha^2-\beta^2-\sigma_D^2
\]
is the immediate expected task-loss gain, and
\[
\Delta_R=2\eta_D(\alpha-\beta)x^TMe-
\eta_D^2\big[(\alpha-\beta)^2+\sigma_D^2\big]x^TMx
\]
is the exact population-risk gain from one query-induced pseudo-update.

**Scope.** \(\Delta_R\) is not total sequential value, an implementation of
a router, or a full continuation-value difference.

### T3 — compatibility/conflict geometry — theorem

Under \(M=cI\) and conservative query updates
\(0<\eta_D\lVert x\rVert^2\le1\), \(\Delta_{\mathrm{now}}>0\) implies
\(\Delta_R>0\). For positive-definite \(M\not\propto I\), there exist
algebraic state/input configurations with \(\Delta_{\mathrm{now}}>0\) and
\(\Delta_R<0\), even for arbitrarily small positive query steps.

**Scope.** The anisotropic claim is existence, not frequency of naturally
reached states or support-restricted inputs.

### T4 — common-coupled transport — theorem

With common subsequent samples, targets, and updates in F/D counterfactual
branches, \(h_k=P_kh_0\). With \(K_k=\mathbb E[P_k^TMP_k]\),
\[
\Delta_k=2\eta_Dd\,x^TK_ke-
\eta_D^2(d^2+\sigma_D^2)x^TK_kx,
\qquad
\Delta_{\mathrm{adapt}}^{(H)}=\sum_{k=0}^{H-1}\gamma^k\Delta_k.
\]

**Scope.** Target cancellation concerns the branch difference under common
coupling. When routing diverges, this quantity is generally not
\(Q^\pi(s_t,D)-Q^\pi(s_t,F)\).

### T5 — fourth-order sign structure — theorem

Under \(M=cI\), \(p\ge2\), and finite fourth moment, let
\(\mathsf H=\mathbb E[\lVert X\rVert^2XX^T]\). If
\(\mathsf H=\rho I\), then \(K_k=c\lambda^kI\), with
\(\lambda\ge(p-1)/p>0\), and the sign of \(\Delta_k\) persists for finite
\(k\). If \(\mathsf H\not\propto I\), there exists a conservative initially
beneficial configuration with \(\Delta_{\mathrm{now}}>0\), \(\Delta_0>0\),
and \(\Delta_1<0\). Rotational invariance is sufficient for the first case.

**Scope.** This is neither new SGD theory nor evidence that reversal is common.
The notes retain two qualified implications rather than an unqualified
operational iff.

### Theory status

The linear-quadratic core was frozen after Decision 010. Corrections or
clarifications remain possible; new theory requires a problem-driven need.
Full adaptive continuation values, stationary-SGD theory, nonlinear learners,
and arbitrary pending-feedback processes are open, not accepted prerequisites.
Decision 011 does not add a theorem: it judges the *general* future-learning
formulation reducible to standard sequential decision theory.

## 5. Frozen experimental evidence

All EP001 experiments use one frozen synthetic linear environment. They do not
establish applied utility.

### EP001-A — natural occurrence of reference-coupled sign reversal

**Question.** Do naturally evolved SGD states exhibit robust expected
\(\Delta_0>0\) and later \(\Delta_k<0\) reversals?

**Primary result.** The isotropic negative control and independent
operator/common-coupled Monte Carlo validation passed. In discovery-selected
anisotropic `spike_q_1` (config 79), confirmation found 18 robust reversals in
3,950 eligible cases across 11/30 trajectories, below the preregistered
minimum of 20 cases.

**Formal verdict.** `FAILS TO SUPPORT THE PHENOMENON IN THE TESTED REGIME`.

**Scientific consequence.** Natural temporal sign reversal is not the
empirical centerpiece.

**Does establish.** The pre-registered measurement/controls worked and rare
labelled cases occurred in this sample.

**Does not establish.** Meaningful natural prevalence, frequency under SGD, or
operational benefit/harm from reversal-aware routing.

**Authority.** `results/ep001/first_run_001/summary/ep001a_summary.json` and
`raw_ep001a.npz`; protocol [EP001-A](experiments/ep001_natural_transport.md);
run/implementation freeze `74d754c`.

### EP001-B — scale of transported versus static value

**Question.** On preserved EP001-A states, does transporting the local update
change finite-horizon valuation beyond static repetition of \(\Delta_0\)?

**Primary result.** In the pre-specified selected config-79 eligible subset,
the static approximation generally overvalued consultation. The correction was
small on the observed scale at \(\gamma=0.5\), but material in scale at
\(\gamma=0.9\) and \(1.0\). At \(\gamma=1\), median \(W_C\) was 33.87% of
\(|\Delta_{\rm now}|\) and 16.93% of \(|C_{\rm static}^*|\), not generally
an artefact of near-zero denominators.

**Formal verdict.** No binary pass/fail was preregistered; the recorded
conclusion is **scale-dependent: small under short discounting, material under
moderate/undiscounted transport**.

**Scientific consequence.** Threshold displacement justified the adversarial
compression test, not a claim of policy benefit.

**Does establish.** The common-coupled transport surrogate can materially move
the synthetic threshold in that subset.

**Does not establish.** Closed-loop improvement, a full continuation value, or
a practical cost distribution.

**Authority.** [EP001-B record](experiments/ep001b_operational_relevance.md)
and `results/ep001/first_run_001/ep001b/ep001b_report.json`; freeze `b08aa63`.

### EP001-B2 — scalar reducibility adversarial test

**Question.** Can the reference transported functional and feasible-cost
threshold be compressed by a state-independent scalar?

**Protocol.** Primary data were all finite EP001-A cases; configs 0--75;
discovery seeds 0--19; confirmation seeds 20--49; and equal configuration,
trajectory, then case weighting. Configs 76--79 were pre-exposed/excluded.
M0 was static, M1 global scalar, and M2 configuration-specific scalar. M2 was
a deliberately oracle-calibrated compression competitor, not deployable.

**Primary result.** Global M1 removed about 70--73% of functional and
feasible-cost discrepancy. Configuration-specific M2 removed about
99.5--99.6% for all three gammas. At \(\gamma=1\), functional LAD loss was
0.03613 (M0), 0.00967 (M1), and 0.000145 (M2); feasible disagreement loss was
0.03592, 0.00960, and 0.000142. Confirmation used 10,000
dependence-preserving bootstrap replicates and did not refit scalars.

**Formal verdict.** Preregistered **Case C**: regime/configuration-dependent,
approximately scalar transport decay.

**Scientific consequence.** Exact state-dependent transport was demoted as the
synthetic empirical centerpiece; scalar evidence is configuration-specific and
privileged by calibration.

**Does establish.** Strong within-configuration scalar compressibility in this
fixed synthetic grid.

**Does not establish.** A universal/global scalar, online estimation, real
deployment, or closed-loop benefit.

**Authority.** [B2 preregistration](experiments/ep001b2_scalar_reducibility.md),
`confirmation_manifest.json`, `primary_metrics.json`, and
`primary_bootstrap.json` in `results/ep001/first_run_001/ep001b2/confirmation_001/`;
preregistration `09404c9`, implementation `9ea32d0`, confirmation freeze
`4ed070f`.

### EP001-C — closed-loop closure experiment

**Question.** When policies generate their own learner trajectories, does
progressively adding future-learning value improve
\(J=J_{\rm prediction}+J_{\rm query}\)?

**Protocol.** The amended frozen preregistration fixes \(T=2000\),
\(H=10\), \(\gamma\in\{0.5,0.9,1\}\), configs 0--75, confirmation seeds
20--49, paired exogenous streams, and 10,000 trajectory-level bootstrap
replicates. P0 uses immediate value; P1 static future value; P2 frozen
configuration-specific B2 operational coefficients; P3 exact
**reference-coupled** local transport. P3 sees no future realized
inputs/noises/targets/actions and is not a continuation-value oracle.

**Primary result and formal verdict.** **AMBIGUOUS**; it must not be reduced to
either “P3 failed” or “P3 succeeded.”

- \(\gamma=1\) has clear **C1-type positive evidence** over substantial
  low/intermediate cost regions: P3 improves P0 and P2 reproduces it closely.
  At \(C_D=0.524902\), \(J^{P0}-J^{P3}=0.25703\), 95% interval
  [0.235884, 0.278888].
- \(\gamma=0.9\) has **C5-type harmful regions**: P3 is systematically worse
  than P0 at several low/intermediate costs. At \(C_D=0.524902\),
  \(J^{P0}-J^{P3}=-0.01245\), [−0.016387, −0.008419]. P3 is often slightly
  better than P1 there, but both future-valuing policies are worse than P0.
- \(\gamma=0.5\) is largely small/null/mixed; high costs mechanically
  suppress queries and policy differences.
- P2 reproduces P3 extremely closely: its largest grid-level
  \(J^{P2}-J^{P3}\) gap is \(1.33\times10^{-5}\), \(4.65\times10^{-5}\),
  and \(2.50\times10^{-4}\) at gamma 0.5, 0.9, and 1.0. This reflects
  privileged frozen per-configuration calibration.
- P1 is not uniformly sufficient: at gamma 1, P3 beats P1 by 0.02338 at
  \(C_D=0.524902\), while P1 beats P3 by 0.11508 at \(C_D=6.17192\).
- Activity and routing disagreement are predominantly transient, concentrated
  in early rounds 1--666; later thirds are mostly inactive in this stationary
  environment.

**Scientific consequence.** \(K_k\) remains mathematically valid for its
reference-coupled counterfactual, but repeatedly using that local surrogate is
not a robust universal practical rule. It can help, harm, or be negligible.

**Does establish.** The stated P0--P3 behavior on the frozen grid, including
positive and harmful regions, P2/P3 proximity, and transient concentration.

**Does not establish.** Full-continuation optimality, a real deployment,
persistent demand under nonstationarity, or general irrelevance of future
learning value.

**Authority.** [EP001-C result record](experiments/ep001c_results_001.md),
`analysis/confirmation_summary.json`,
`trajectories/confirmation_manifest.json`, and `analysis/analysis_manifest.json`
in `results/ep001/first_run_001/ep001c/confirmation_001/`.
Preregistration SHA-256:
`9d5af0f7652bd36e3c05c96a247a3e989df32fa1fb9534ca1900f91c3e1c1d1b`;
amendment `0a80989`, discovery freeze `e38596d`, confirmation freeze
`d810dea`, final result documentation `a5ddd2a`.

### Literature/theory audit — sequential-decision reducibility — 2026-09-14

**Question examined.** Does the general structure “consulting (D) can
improve the current response and update (F), whose learning may be useful in
future contexts” define a new decision-theoretic object?

**KNOWN RESULT / formal correspondence.** With an application-appropriate
state (S_t) containing the learner state, current context, pending delayed
feedback, and any required future-context/dynamics information, the actions
are (F) and (D). Under (D), an operational response (Z_t) replaces
(F)'s current response, incurs consultation cost, and can enter the state
transition as imperfect pseudo-supervision; delayed reliable (Y_t) enters
later as exogenous information. The exact comparison is Bellman:

\[
Q_t(s,F)-Q_t(s,D)
= \text{immediate cost/loss difference}
+ \gamma\,\text{continuation-value difference}.
\]

The continuation value already accounts for update benefit or harm, future
context distribution and reuse, future routing and query cost, diverging
trajectories, delayed feedback, and nonstationarity when these are represented
in the state/model. Sharing (Z_t) between immediate response and update, or
allowing (D) to be imperfect, changes the cost and transition kernel; it does
not obstruct the formulation.

**Decisive conceptual test.** If two current queries (a,b) have the same
immediate loss/cost and learning capacity but the learned information will be
reused with different future frequency or relevance, a correctly specified
continuation value already prefers the action that leads to greater future
utility. This does not reveal a separate structure.

**Relation to prior frameworks.** Expected Error Reduction and
decision-theoretic Value of Information already value future predictive use of
acquired supervision; sequential Bayesian optimal experimental design,
MDP/POMDP/Bayes-adaptive formulations, and dual control supply general
sequential representations. The audit does not assert that one prior article
reproduces every implementation detail of this project.

**VERDICT: A — REDUCIBLE.** The general future-learning-value formulation is
not a surviving theoretical novelty hypothesis. In particular, do not posit a
universal “learnability \(\times\) future relevance” factorization.

**OPEN QUESTION.** The only direction meriting further audit is whether a
computable, observable, and sufficiently accurate approximation to the true
policy-dependent continuation-value advantage is novel and useful for adaptive
supervision acquisition/model routing in high-dimensional systems. This is an
algorithmic/computational question, not an established gap.

**Constraint.** EP001 remains closed. Do not start EP001-D or rehabilitate
(K_k) as a main direction. Recover (K_k) only if a concrete application or
new approximation problem specifically requires it.

### Literature audit checkpoint — algorithmic continuation-value approaches — 2026-09-14

**Question examined.** After the general Bellman reduction, is approximating
the future value of acquiring supervision by Bellman/RL itself a defensible
algorithmic novelty claim?

**KNOWN RESULT.** Reinforcement-learning-based active learning formulates
supervision acquisition as a sequential decision and approximates an action
value for querying, including with Q-learning/DQN-style methods. EER and
model-change/output-change surrogates (including EMOC-type families) also
provide computable, more local proxies for the future effect of acquiring
supervision. Learning-to-defer and model routing cover operational selection
between predictors or experts. Therefore, “use Bellman/RL because a queried
label changes a learner that will be used later” is not an available novelty
claim.

The names Fang, Li and Cohn, *Learning how to Active Learn: A Deep
Reinforcement Learning Approach*; Woodward and Finn, *Active One-shot
Learning*; and later RL-based active-learning work are **candidates pending
bibliographic and methodological verification** in the repository. They are
not yet primary local evidence for a claim about their exact protocol or
results.

**HYPOTHESIS.** The narrower intersection may remain insufficiently solved:
at each round an expensive, fallible (D) supplies the operational response
and the same output is immediate pseudo-supervision for (F), while delayed
reliable (Y_t) arrives exogenously and the induced update can alter later
routing. It is not established that this conjunction is novel, nor that no
existing method estimates an adequate continuation advantage for it.

**Audit rule.** Existence of prior work is not equivalent to the problem being
satisfactorily solved. Each dangerous antecedent must be assessed separately
for (1) conceptual coverage, (2) methodological adequacy of the estimated
quantity and information available at decision time, (3) experimental
validity, and (4) effective result relative to strong, equally tuned baselines
and computational cost. Deficiencies must be named specifically (for example,
privileged/oracle information, leakage, weak baseline, unequal tuning,
inadequate uncertainty, or unsupported mechanistic interpretation), never
called ``tricked'' without evidence.

**PROVISIONAL STATUS: B — PARTIALLY OCCUPIED / ALGORITHMIC GAP NOT YET
ESTABLISHED.** The next action is the focused audit, not mathematics or an
experiment. Do not start EP001-D or rehabilitate (K_k) unless a concrete
algorithmic or application need survives that audit.

## 6. Demoted or rejected directions

### General future-learning value as a new decision principle — rejected

**Why.** Decision 011 reduces the general formulation to a standard augmented
state and Bellman/VoI continuation-value comparison.

**Required to revisit.** A precise formal limitation showing that standard
sequential decision frameworks cannot represent a specified operational
protocol; none has been identified.

### Natural temporal sign reversal as empirical centerpiece — demoted

**Why.** EP001-A failed its preregistered confirmation criterion.

**Required to revisit.** New problem-driven, preregistered evidence that
natural states/inputs make reversal frequent or materially consequential; not
another tuned EP001 sweep.

### Exact state-dependent \(K_k\) as primary deployable router — demoted

**Why.** B2 showed strong configuration-specific compression and C showed that
reference-coupled P3 can help or harm rather than give stable benefit.

**Required to revisit.** A concrete application where the additional operator
information is observable/estimable and beats strong baselines in closed loop.

### Universal/global scalar transport — rejected in the frozen grid

**Why.** M1 is materially worse than configuration-specific M2.

**Required to revisit.** A separately preregistered, application-grounded
invariance claim with out-of-sample evidence.

### P2/configuration-specific scalar as deployment recipe — rejected

**Why.** Configuration ID and its frozen coefficient are privileged oracle
information; no online estimator exists here.

**Required to revisit.** An observable estimation protocol and evaluation
against baselines without the same privilege.

### Further EP001-D synthetic transport work — not next

**Why.** The synthetic line is closed and contains positive, null, and harmful
outcomes.

**Required to revisit.** A specific applied problem whose measurement/control
need cannot be met without a narrow synthetic validation. Do not tune gamma,
cost, horizon, family, or policy to rescue a result.

## 7. Current novelty position

Detailed sources: [primary novelty review](literature/primary_novelty_review.md),
[literature inventory](literature/consolidation_inventory.md), and
[applied audit](literature/applied_novelty_audit.md).

### Closest occupied prior-work families

- active learning/value-of-information and expected-error-reduction;
- decision-theoretic selective supervision;
- online selective sampling with noisy/multiple teachers;
- dual-use expert intervention and online teacher-to-student adaptation;
- cloud--edge hard-sample routing, cloud assistance, and distillation.

The strongest documented threats include Roy--McCallum, Kapoor--Horvitz--Basu,
Sogawa, Sekhari et al., Hanneke--Yang, Dekel et al., ThriftyDAgger, TRACER,
and, in cloud--edge forecasting, CE-CoLSM and SCECS. Shoggoth and L2D-SLDS
are protocol/comparator boundaries. Consult the audits for exact verified
claims; this handover adds no literature result.

### Claims already unavailable

Do not claim novelty for future learning value alone, fallible teacher queries,
selective querying, mistake/query trade-offs, dual present/adaptation use of a
query, cloud--edge collaboration, hard-sample routing, cloud-to-edge
retraining/distillation, reduced calls through adaptation, or the generic
Bellman comparison between immediate and future learning effects.

### Remaining candidate — open algorithmic question only

The previous candidate that explicitly pricing the future learning consequence
of the same queried supervision was itself a new decision principle is
superseded by Decision 011. The additional audit checkpoint finds general
RL/Bellman supervision acquisition and local future-learning surrogates already
occupied. The remaining question is only whether existing methods adequately
cover the specified adaptive-routing/pseudo-supervision protocol. Neither
novelty nor practical value is established; the required audit is narrower,
algorithmic, and adversarial.

## 8. Current application status

### Selected application

**None.** No repository evidence records an application selection or an
applied experimental protocol.

### Candidate application: cloud--edge traffic forecasting

Cloud--edge traffic forecasting is the strongest documented candidate.
Energy/load forecasting has not been separately selected or protocolized in
the repository; at most, it is an unassessed candidate within the broader
forecasting family, not a validated method.

**Why interesting.** This family can offer exogenous delayed ground truth (the
future target occurs whether or not a query was made), sequential operation,
meaningful consultation/latency cost, and natural transients or regime changes
that may sustain or alter routing demand.

**Unresolved before selection.** No observable estimator of immediate relative
advantage or future learning value has been established; neither have the F/D
pair, precise temporal/feedback/update protocol, legitimate pseudo-supervision
use, or deployable scalar correction. Natural nonstationarity motivates an
application; EP001 has not solved it.

CE-CoLSM is the anchor novelty threat. A study must show more than
confidence-triggered cloud querying plus later distillation; the query
valuation approximation, not architecture, is at most a candidate algorithmic
gap and has not survived the required focused audit.

### Broader direction — hypothesis, not architecture

The project must not collapse into cloud--edge routing. A working hypothesis
concerns complementary fast/shallow and slow/deep models, role redistribution,
and, under strong regime change, possible replacement/regeneration rather than
transfer from obsolete models. Separate intra-regime routing/adaptation from
inter-regime detection/retraining/replacement. No formal model, experiment, or
result has established this direction.

### Secondary Bayesian routing line — priority unresolved

`docs/research_log.md` Decision 001 also records **Bayesian Cost-Aware Routing
under Changing Operating Conditions** as a secondary line. The current history
contains neither a later frozen protocol/result for it nor an explicit decision
to retire it. Treat it as dormant rather than an active next step until Fran
decides its priority; do not infer support for it from the EP001 evidence.

## 9. Current interpretation

**Empirical result.** In the frozen synthetic setting, transport can materially
change local reference-coupled valuation (B), and is strongly compressible by a
configuration-specific scalar (B2). In closed loop, the reference-coupled
surrogate is not consistently beneficial (C).

**Interpretation.** Retain exact/scalar EP001 transport as diagnostic/model
components, not as a robust practical contribution. Decision 011 further
rejects treating generic future-learning valuation as a new theoretical
principle: it belongs inside a correctly specified continuation value.

**OPEN QUESTION.** It remains unknown whether the narrow intersection has a
methodologically adequate practical solution. A forecasting-like application
may expose an observable computational problem, but neither an application nor
a novel or winning routing representation exists.

## 10. Current scientific decision point

EP001 is closed. The immediate decision is whether the focused literature
audit leaves any credible **algorithmic/computational novelty gate** after
RL-based active learning, EER/EMOC-type surrogates, learning-to-defer, online
teacher querying, adaptive distillation, selective prediction with feedback,
and model routing are examined at the protocol level. A concrete application
is relevant only if it has routing-independent delayed ground truth where
needed, genuine consultation cost, observable decision-time signals, and a
clear distinction from strong baselines.

This requires a focused bibliographic audit before a problem formulation or
implementation. If no candidate meets that bar, stop or substantially reframe
the applied line. The frozen evidence does not justify another synthetic
transport extension as a substitute for this decision.

## 11. NEXT / NOT NEXT

### NEXT

1. Conduct the fixed four-level audit (conceptual coverage, methodological
   adequacy, experimental validity, effective result) of practical/observable
   continuation-value approximations in adaptive supervision acquisition and
   model routing.
2. Only if that audit leaves a candidate, assess an application protocol and
   data availability; separate observable facts from hypotheses.
3. Only then decide whether a new problem-level specification or preregistered
   empirical study is warranted and what minimal representation it requires.

### NOT NEXT

- No EP001-D merely to explore synthetic transport mathematics.
- No new \(K_k\) derivation without an application-driven need.
- No claim that “immediate value + future learning value” is a new
  decision-theoretic structure.
- No claim that Bellman/RL estimation of future supervision value is new in
  general.
- No universal “learnability \(\times\) future relevance” factorization.
- No claim that concept drift has been solved.
- No claim that energy/load/traffic forecasting has validated the method.
- No assumption that B2/P2 configuration-specific coefficients are available
  to a real router.
- No rebranding of P3 as an oracle, optimal policy, or full continuation value.

## 12. Where to reconstruct the full scientific history

- `docs/research_log.md`: chronological decisions, supersessions, freezes, and
  repository-maintenance provenance, including Decisions 011--012 and their
  reducibility/algorithmic-audit boundaries.
- `docs/theory/primary_notes.md`: full derivations, assumptions,
  counterexample, theorems, and limits of Decisions 007--010.
- `docs/literature/primary_novelty_review.md` and
  `docs/literature/consolidation_inventory.md`: targeted audit and local
  evidence provenance.
- `docs/literature/applied_novelty_audit.md`: candidate-domain audit; a working
  note, not an application-selection decision.
- `docs/experiments/ep001_natural_transport.md`,
  `ep001b_operational_relevance.md`, `ep001b2_scalar_reducibility.md`, and
  `ep001c_closed_loop_routing.md`: frozen protocols/definitions.
- `docs/experiments/ep001c_discovery_001.md` and
  `ep001c_results_001.md`: C discovery/result records tied to artifacts.
- `results/ep001/first_run_001/`: primary raw data, manifests, machine-readable
  metrics, bootstrap outputs, and checksums.
- `paper/primary/sections/problem_formulation.tex` and
  `theoretical_analysis.tex`: paper-facing theory/protocol only.

## 13. Reproducibility and frozen artifacts

| Item | Primary authority | Freeze/status |
|---|---|---|
| Theory Decisions 007--010 | `docs/theory/primary_notes.md` | Frozen after `fd5c956` |
| General formulation audit | `docs/research_log.md`, Decision 011 | Reducible; 2026-09-14 |
| Narrow algorithmic audit | `docs/research_log.md`, Decision 012 | Provisional B; 2026-09-14 |
| EP001-A | `summary/ep001a_summary.json`, `raw_ep001a.npz` | Closed; `74d754c` |
| EP001-B | `ep001b/ep001b_report.json` | Closed; `b08aa63` |
| B2 protocol | `docs/experiments/ep001b2_scalar_reducibility.md` | Frozen; `09404c9` |
| B2 confirmation | confirmation manifest, metrics, bootstrap | Closed; `4ed070f` |
| C amended protocol | C preregistration, SHA in Section 5 | Immutable; `0a80989` |
| C discovery | `ep001c/discovery_001/` manifests/reports | Frozen; `e38596d` |
| C confirmation | `ep001c/confirmation_001/` manifests/summary | Closed; `d810dea`, `a5ddd2a` |

The B2 discovery calibration JSON is reproducible but excluded from ordinary
Git because its original size was 211,192,800 bytes. Its SHA-256 is
`9e64ee92e45b3925f2babfe847d1d3d04ec6388ea1537d8a6c37f6e3105757a8`; full
provenance/reproduction instructions are in
`results/ep001/first_run_001/ep001b2/discovery_001/README.md`.

## 14. Known mistakes and lessons

- **EP001-C omitted \(T\) originally.** Detected before implementation,
  discovery, or results; a transparent amendment fixed \(T=2000\), retaining
  the original preregistration in history.
- **P3 could be overstated as an oracle.** The frozen C protocol corrects this:
  it is exact only for its reference-coupled counterfactual, not for its own
  closed-loop continuation value.
- **Two interrupted C discovery attempts produced no artifact/result.** Tested
  mechanical optimizations (operator caching and seed vectorization) preceded
  the completed discovery run; no endpoint, parameter, or policy changed.
- **Interpretation lesson.** High correlation, threshold displacement, or
  scalar compression does not prove closed-loop usefulness. C retained C1-like
  and C5-like regions rather than selecting a favorable summary.
- **Conceptual lesson.** Immediate operational value plus a future learning
  consequence does not by itself create a new decision theory; a sufficient
  sequential state and its continuation value already contain both. Do not
  assume a product factorization of learning effect and future reuse.
- **Audit lesson.** Prior work can invalidate priority without showing that a
  problem is satisfactorily solved. Record the exact objective, approximation,
  decision-time information, computational cost, protocol, and evidence before
  treating any close method as either equivalent or inadequate.
- **Inference-unit lesson.** Cases/checkpoints/time steps sharing an SGD
  trajectory are not independent; confirmation preserves full trajectories and
  shared quartet dependence.
- **Repository lesson.** The oversized B2 discovery JSON required an
  unpublished-history rewrite before push; hash/provenance were retained. This
  was maintenance, not a scientific rerun/amendment.

## 15. Collaboration protocol

**Fran** is the scientific owner and makes final scientific decisions.

**ChatGPT** is a critical scientific collaborator: challenge hypotheses,
distinguish theorem/result/interpretation/hypothesis, and reconstruct state
from repository evidence at new-chat startup.

**Codex** handles implementation, tests, execution, artifact generation,
repository maintenance, and reproducibility. It preserves frozen protocols and
reports unfavorable results.

**Adversarial expert** is an independent red-team reviewer. Its input is
valuable but non-authoritative until checked against theory and primary
evidence.

## 16. New-chat bootstrap protocol

A new session must:

1. read this handover completely;
2. identify the current decision point;
3. inspect the cited primary sources for that decision;
4. report its reconstructed state before proposing work; and
5. explicitly identify any inconsistency.

Copy/paste prompt:

```text
We are continuing adaptive_routing. Read docs/HANDOVER.md completely first.
Use its evidence hierarchy and inspect the cited primary sources for the
current decision before proposing work. Reconstruct the state explicitly,
distinguishing theorem, empirical result, interpretation, hypothesis, and open
question. EP001 is closed: do not revive demoted directions or reinterpret its
AMBIGUOUS/null/harmful evidence as positive without an application-driven
reason.
```

## 17. Handover maintenance protocol

Review/update this file whenever an experiment is preregistered, discovery is
frozen, confirmation is frozen, a formal verdict changes, a major theoretical
result is established/demoted, a novelty audit materially changes, an
application is selected/rejected, or scientific direction changes.

Do not update it for routine code changes without scientific-state impact.
Every update must state the repository HEAD it represents and preserve the
evidence hierarchy above.
