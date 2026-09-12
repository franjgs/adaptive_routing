# Experimental Plan 001 — Natural occurrence and operational relevance of transported adaptation value

Status: EP001-A design and validation utilities. EP001-B and EP001-C are design only. The core theory remains frozen after Decision 010; this plan does not add a theorem, modify the paper, or assert novelty.

## Scientific question and falsification target

The primary question is whether learner errors produced by an ordinary SGD trajectory, rather than selected algebraically, yield meaningful temporal sign reversal of the expected common-coupled adaptation value:

$$
\Delta_0>0
\quad\text{and}\quad
\Delta_k<0\quad\text{for some }k\in\{1,\ldots,H_{\max}\}.
$$

The experiment is oracle-based. It uses the known $w^*$, input law, $M$, weighted fourth-moment matrix $\mathsf H$, and exact transport operator. It does not estimate $e_t$ or an operational routing rule.

The hypotheses subjected to falsification are:

1. **EP001-H1, natural reversal:** within the pre-specified second-order-isotropic but weighted-fourth-moment-anisotropic family, naturally evolved SGD states and independently sampled query inputs produce robust expected reversals often enough and at sufficient magnitude to justify EP001-B.
2. **EP001-H2, transport matters beyond one update:** among eligible cases with $\Delta_0>0$, at least one later expected $\Delta_k$ contains information that is materially different from the sign and magnitude of $\Delta_0$. Sign reversal is the primary endpoint; magnitude deformation without reversal is descriptive.
3. **Validation hypothesis:** the operator value from Decision 009 agrees with an independently implemented common-coupled Monte Carlo estimate within Monte Carlo error.
4. **Negative-control prediction:** when $M=cI$ and $\mathsf H=\rho I$, expected values cannot reverse sign. Any reproducible expected reversal there is treated as a validation failure until a coding, estimation, or assumption mismatch is identified.

Failure to see the pre-specified frequency and magnitude of reversal counts against EP001-H1 in the tested regime. Individual pathwise negative gaps do not support it: the endpoint is the expected theoretical $\Delta_k$.

## Minimal data-generating model

Use dimension $p=2$ and

$$
Y=(w^*)^TX+\epsilon,\qquad
F_\theta(x)=\theta^Tx,\qquad
D(x)=(w^*+b)^Tx+\nu.
$$

EP001-A fixes $b=0$, $w^*=(1,-0.5)^T$, and initializes $\theta_0=0$. The initialization and $w^*$ are fixed before examining reversals. At every recorded state,

$$
e_t=\theta_t-w^*
$$

is read directly from the trajectory. The experiment must never replace it with a hand-selected vector, optimize it for reversal, or discard states because their geometry is unfavorable.

The base trajectory receives an i.i.d. stream of $(X_t,Y_t)$ and applies ordinary squared-loss SGD to reliable targets:

$$
\theta^+=\theta+\eta X(Y-\theta^TX).
$$

To retain the protocol timing, the default simulation uses a FIFO reliable-feedback delay $\tau=5$: the response-time state is recorded first, and feedback due from round $t-\tau$ is applied only after the response at $t$. Consequently, $Y_t$ can first affect the response at $t+\tau+1$. No teacher pseudo-update is applied to the base trajectory in EP001-A. The fixed delay changes the operational timestamp at which ordinary SGD updates occur; it does not authorize identifying response horizons with update counts. Every output row records both the operational round and the number of SGD updates already applied.

At a pre-specified checkpoint, sample query inputs independently from the same input law. Evaluate the counterfactual teacher pseudo-update and its future transport without mutating $\theta_t$, the feedback queue, the random-number stream used by the base trajectory, or later checkpoints. Future common-coupled validation uses fresh i.i.d. samples and counts $k$ subsequent SGD updates. It does not insert the query's delayed $Y_t$ into the Decision 009 i.i.d. operator formula.

## Control and anisotropy distributions

### Rotational sign-preserving control

Let $X\sim\mathcal N(0,I_2)$. Then

$$
M=\mathbb E[XX^T]=I_2,
\qquad
\mathsf H=\mathbb E[\|X\|^2XX^T]=4I_2.
$$

The second identity follows from $\mathbb E[X_i^4]=3$ and $\mathbb E[X_i^2X_j^2]=1$ for $i\ne j$. Decision 010 predicts sign preservation for all expected $\Delta_k$.

### Parameterized Gaussian–spike family

For $q\in(0,1]$, let

$$
X=(G,Z_q)^T,qquad G\sim\mathcal N(0,1),
$$

where $G$ and $Z_q$ are independent and

$$
Z_q=
\begin{cases}
+q^{-1/2},&\text{with probability }q/2,\\
-q^{-1/2},&\text{with probability }q/2,\\
0,&\text{with probability }1-q.
\end{cases}
$$

The distribution is centered and symmetric, with

$$
\mathbb E[Z_q^2]=1,qquad \mathbb E[Z_q^4]=q^{-1}.
$$

Independence and centering therefore give, for every $q$,

$$
M=I_2.
$$

For the weighted fourth moment, the off-diagonal terms vanish by symmetry, while

$$
\begin{aligned}
\mathsf H_{11}
&=\mathbb E[G^4]+\mathbb E[G^2Z_q^2]=3+1=4,\\
\mathsf H_{22}
&=\mathbb E[G^2Z_q^2]+\mathbb E[Z_q^4]=1+q^{-1}.
\end{aligned}
$$

Hence

$$
\boxed{M=I_2,\qquad
\mathsf H(q)=\operatorname{diag}(4,1+q^{-1}).}
$$

This gives a one-parameter change in weighted-fourth-moment anisotropy without changing the second moment. The value $q=1/3$ has $\mathsf H=4I_2$ and supplies a non-rotational sign-preserving control. The value $q=1$ makes $Z_q$ Rademacher and exactly recovers the Decision 009 input law, with $\mathsf H=\operatorname{diag}(4,2)$. It is retained as a sanity check rather than used as the only anisotropic case. Values below $1/3$ reverse which diagonal entry is larger and introduce increasingly rare, large second-coordinate observations; this makes numerical stability and effective sample size visible rather than hidden.

The experiment reports the anisotropy ratio

$$
a_{\mathsf H}(q)=
\frac{\max\{4,1+q^{-1}\}}{\min\{4,1+q^{-1}\}},
$$

only as a distribution descriptor. No new theoretical claim is attached to this scalar summary.

## EP001-A procedure

For each pre-specified configuration and seed:

1. Generate one base trajectory using only delayed reliable-target SGD. All configurations use independent named random streams for trajectory data, evaluation inputs, teacher noise, and Monte Carlo continuations.
2. At every checkpoint, record $\theta_t$, compute $e_t=\theta_t-w^*$, and retain the state regardless of whether it later yields an eligible query.
3. Draw 64 independent evaluation inputs $x$ from the configured law. These draws never update the base trajectory.
4. For each $(e_t,x)$, compute $alpha=x^Te_t$, $eta=x^Tb=0$, $d=\alpha$, and

   $$
   \Delta_{\mathrm{now}}=\alpha^2-\sigma_D^2.
   $$

5. Compute $K_0,\ldots,K_{H_{\max}}$ by the exact recursion $K_{k+1}=\mathcal T(K_k)$ using the known coordinate fourth moments, then compute

   $$
   \Delta_k=
   2\eta_Dd\,x^TK_ke
   -\eta_D^2(d^2+\sigma_D^2)x^TK_kx.
   $$

6. Record all values before classification. Label an eligible initial benefit, compute $k_{\mathrm{flip}}$ and $\rho_{\mathrm{rev}}$, and apply the pre-specified robust-reversal rule below. Do not select a horizon after inspecting a trajectory; report every $k=1,\ldots,H_{\max}$.
7. On a fixed validation subset chosen by seed/checkpoint indices before examining signs, independently simulate the two common-coupled branches and compare their Monte Carlo risk-gap means with every analytical $\Delta_k$.

For the supported independent symmetric unit-variance coordinate laws, the exact fourth-order contraction used by the utility is

$$
\begin{aligned}
[\mathbb E(XX^TQXX^T)]_{ii}
&=\mathbb E[X_i^4]Q_{ii}+\sum_{j\ne i}Q_{jj},\\
[\mathbb E(XX^TQXX^T)]_{ij}
&=2Q_{ij},\qquad i\ne j.
\end{aligned}
$$

This is an implementation formula for the chosen synthetic laws. EP001 does not extend it into a broader theoretical analysis.

## Independent common-coupled validation

For a retained natural state $e_t$, an evaluation input $x$, and each Monte Carlo replication:

1. Clone the error state into $e_0^F=e_t$ and

   $$
   e_0^D=e_t+\eta_Dx(\nu-d),
   \qquad \nu\sim(0,\sigma_D^2).
   $$

2. At each subsequent update draw one $(X_j,\epsilon_j)$ and apply it identically to both branches:

   $$
   e_j^a=e_{j-1}^a+eta X_j(\epsilon_j-X_j^Te_{j-1}^a),
   \qquad a\in\{F,D\}.
   $$

3. Store the individual realization

   $$
   R(e_j^F)-R(e_j^D)
   $$

   separately from its Monte Carlo mean. A pathwise sign is never called an expected reversal.
4. Compare the mean at each $k$ with the analytical $\Delta_k$. The automated smoke test accepts an absolute discrepancy no larger than five estimated standard errors plus $2\times10^{-5}$ for its fixed numerical case. Production validation also reports the difference, standard error, standardized discrepancy, replication count, and a confidence interval rather than only a pass/fail flag.

The current automated test obtains states after 60 ordinary SGD updates under both the Gaussian preserving control and the Decision 009 $q=1$ law. It checks $k=0,1,2,3$ with 200,000 coupled replications per case. This test validates implementation agreement; its selected states are not evidence about reversal frequency.

The sampler preflight uses 400,000 fixed-seed draws for the Gaussian control, the $q=1/3$ moment-isotropic control, and the $q=1$ Decision 009 case. Every entry of the empirical second-moment and weighted-fourth-moment matrices must lie within five estimated standard errors plus $0.01$ of its analytical value. The production runner applies the same check to every configured $q$ before generating trajectories.

## Measurements and output rows

The analytical table contains one row per seed, configuration, checkpoint, query input, and update count $k$. It records at least:

- distribution and $q$ when applicable;
- trajectory seed, operational round, and number of applied SGD updates;
- $\eta$, $\eta_D$, $\tau$, $\sigma_\epsilon$, and $\sigma_D^2$;
- query index, $k$, $\|e_t\|$, $\|x\|$, $\Delta_{\mathrm{now}}$, $\Delta_0$, and $\Delta_k$;
- sign of $\Delta_k$ relative to $\Delta_0$, robust-reversal indicator, and $|\Delta_k|$;
- $k_{\mathrm{flip}}$, stored as missing when no negative $\Delta_k$ occurs;
- $\rho_{\mathrm{rev}}=-\min_{k\geq1}\Delta_k/\Delta_0$ for eligible cases;
- $R(e_t)=e_t^TMe_t$ as the scale used by the numerical floor.

The validation table separately records analytical values, Monte Carlo means, Monte Carlo standard errors, confidence intervals, and standardized differences. A small fixed sample of individual pathwise gaps may be retained for diagnostics; it is not mixed into the analytical endpoint table.

The seed, hence the complete SGD trajectory, is the independent unit for confirmatory inference. Checkpoints and query inputs sharing a seed are repeated observations within that unit. For each confirmation seed $s$, aggregate

$$
r_s=
\frac{\#\{\text{eligible cases with a robust reversal in trajectory }s\}}
     {\#\{\text{eligible cases in trajectory }s\}},
$$

and record whether trajectory $s$ contains at least one robust reversal. If a trajectory has no eligible cases, store $r_s$ as missing and report that lack of coverage; its trajectory-level occurrence indicator is false. Across confirmation seeds, report the number and fraction containing a robust reversal, the median and interquartile range of $r_s$ among trajectories with eligible cases, and the eligible/robust counts for every seed. A pooled case-level reversal fraction may also be reported, but only descriptively.

## Minimal pre-specified grid

The first run uses:

| Component | Values |
| --- | --- |
| Input law | Gaussian control; Gaussian–spike $q\in\{1/6,1/3,1/2,1\}$ |
| $w^*$ | $(1,-0.5)^T$ |
| $\theta_0$ | $(0,0)^T$ |
| Reliable-feedback delay | $\tau=5$ rounds |
| SGD and future transport step $\eta$ | $0.02, 0.05$ |
| Initial pseudo-step $\eta_D$ | $0.02, 0.05$ independently crossed with $\eta$ |
| Target-noise standard deviation $\sigma_\epsilon$ | $0, 0.1$ |
| Teacher-noise variance $\sigma_D^2$ | $0.01, 0.05$ |
| Checkpoints, applied SGD updates | $5,20,100,500,2000$ |
| Evaluation inputs per checkpoint | 64 independent draws |
| Transport horizon | every $k=0,\ldots,10$ |
| Trajectory seeds | 50, fixed and split 20 discovery / 30 confirmation |

The $q=1/3$ family member and the Gaussian law are both negative controls. The former checks that sign preservation follows the moment condition rather than Gaussianity. The $q=1$ member is the Decision 009 sanity check. The remaining $q$ values prevent the study from resting on that single example. The grid is fixed before examining reversal results; adding values after inspection creates a new plan version and cannot rescue EP001-A retroactively.

The two $\eta_D$ values are constant steps, so some unbounded-input draws need not satisfy the conservative condition. Record $a_D=\eta_D\|x\|^2$ and stratify descriptively by $a_D\leq1$ without filtering the primary endpoint after seeing results. The primary eligibility condition is the actually computed $\Delta_0>0$ with numerical margin.

## Decision criteria for EP001-A

For each state/query pair define

$$
\delta_{\mathrm{num}}=10^{-6}\{1+R(e_t)\}.
$$

For every eligible pair, define the first strict sign reversal

$$
k_{\mathrm{flip}}
=\min\{k\in\{1,\ldots,10\}:\Delta_k<0\},
$$

and store it as missing when the set is empty. Also define

$$
\rho_{\mathrm{rev}}
=-\frac{\min_{1\leq k\leq10}\Delta_k}{\Delta_0}.
$$

Thus $\rho_{\mathrm{rev}}\leq0$ means that no negative transported value occurs within the horizon, while $\rho_{\mathrm{rev}}>0$ means that a sign reversal occurs; its size is normalized by the initially beneficial adaptation value. The pair is **eligible** when $\Delta_0>\delta_{\mathrm{num}}$. It has an **expected reversal** when $k_{\mathrm{flip}}$ exists. It has a **robust expected reversal** when

$$
\rho_{\mathrm{rev}}\geq0.1
\qquad\text{and}\qquad
\min_{1\leq k\leq10}\Delta_k<-\delta_{\mathrm{num}}.
$$

This is the existing 10% robust-reversal threshold rewritten in normalized notation, with the same numerical-scale safeguard. The strict $k_{\mathrm{flip}}$ records timing even for a tiny negative value, while the robust indicator prevents that value from becoming confirmatory evidence. All raw values remain available.

Validation is a gate. EP001-A is not interpreted until:

- the analytical/operator and coupled Monte Carlo checks pass on the fixed validation subset;
- neither sign-preserving control contains an analytical reversal beyond $\delta_{\mathrm{num}}$;
- moment checks reproduce $M$ and $\mathsf H$ within their pre-specified Monte Carlo intervals when sampled empirically;
- trajectories and outputs are finite, and any explosive run is reported rather than silently removed.

The 50-seed split is adopted because the workload remains small: base trajectories can be reused across $\eta_D$ and $\sigma_D^2$, leaving about two million two-dimensional SGD updates over the declared distribution, $\eta$, target-noise, and seed combinations. Analytical evaluation is closed-form/vectorizable, while the 200,000-replication Monte Carlo checks remain restricted to the selected validation cases and are not increased. The extra seeds therefore add independent trajectories at low expected runtime cost.

The first 20 seeds are discovery seeds. They identify at most one pre-specified anisotropic configuration by robust-reversal fraction; ties use the smaller $q$-distance from $1/3$, then the smaller steps. The choice is frozen before reading the 30 confirmation seeds.

EP001-A **supports proceeding to EP001-B** only if the selected configuration, on confirmation seeds alone:

- has at least 500 eligible state/query pairs;
- has at least 20 robust expected reversal cases overall;
- has robust reversals in at least 5 of the 30 independent confirmation trajectories; and
- reports every trajectory-level $r_s$, the median and IQR of the defined $r_s$ values, the fraction of trajectories containing a robust reversal, and the share of all robust cases contributed by each trajectory.

The requirement that five independent trajectories contain reversals prevents one or two favorable states from carrying the confirmatory result. The per-trajectory rates and contribution shares expose any remaining concentration without adding a new arbitrary cutoff. The preferred confirmatory interval is a nonparametric bootstrap that resamples the 30 seeds, never individual state/query cases, and recomputes the fraction of trajectories containing a reversal and the median $r_s$. Its confidence interval is reported but is not an additional pass threshold in EP001-A. A pooled Wilson interval over state/query cases is prohibited as primary confirmatory evidence; the pooled frequency is descriptive only.

It **fails to support the phenomenon in the tested regime** when validation passes but the discovery-selected configuration does not meet all confirmation criteria. Report the trajectory-level occurrence fraction, median and IQR of $r_s$, optional seed-bootstrap intervals, pooled descriptive frequency, magnitude distribution, and zero-event summaries; do not tune distributions, states, or thresholds to recover a positive result. It is **inconclusive** if validation fails, the negative control violates Decision 010, fewer than 500 confirmation cases are eligible, or numerical instability prevents faithful execution. An inconclusive run triggers diagnosis, not a scientific claim.

These criteria operationalize “meaningful frequency and magnitude” for the first cycle. They are design thresholds, not theoretical constants or claims about other regimes.

## EP001-B — planned only

If EP001-A passes, EP001-B will quantify operational relevance without yet allowing routing to alter the base trajectories. For the locked configuration and an independently generated evaluation set, plan to report:

- frequency and distribution of $k_{\mathrm{flip}}$ for expected sign reversals;
- distribution of $\rho_{\mathrm{rev}}$, alongside negative transported magnitude relative to $\Delta_{\mathrm{now}}$;
- magnitude relative to a declared grid of incremental consultation costs;
- fraction of states/query inputs where decisions based on current value plus single-update adaptation and current value plus accumulated transported adaptation differ;
- sensitivity to horizon and discount factor, declared before running EP001-B.

Consultation-cost values and success thresholds for EP001-B must be fixed in a separate plan after EP001-A. They are not selected from EP001-A outcomes to maximize apparent operational relevance.

## EP001-C — planned only

Only after EP001-A and EP001-B succeed may routing policies alter their trajectories. EP001-C will compare:

- myopic current-value routing;
- current value plus single-update adaptation;
- current value plus transported adaptation.

The planned outcomes are cumulative task loss, cumulative query cost, number of teacher calls, and cost/performance Pareto tradeoffs. EP001-C requires its own protocol for delayed feedback, policy estimation, common random numbers, and statistical comparison. None of those policies is implemented here.

## Minimal code and test architecture

Implemented now:

```text
code/ep001/
├── __init__.py
├── validation.py       # moments, exact K recursion, SGD state evolution, coupled MC
└── test_validation.py  # automated preflight checks
```

Proposed only when EP001-A is executed:

```text
code/ep001/
├── run_ep001_a.py       # immutable grid, named RNG streams, trajectory/checkpoint rows
└── summarize_ep001_a.py # validation gate, seed-level aggregation/bootstrap, report
```

The runner should write a machine-readable configuration manifest, analytical rows including $k_{\mathrm{flip}}$ and $\rho_{\mathrm{rev}}$, validation rows, and a summary under a generated-results directory. It should not contain routing policies. The summary code should aggregate by seed before confirmatory inference, optionally bootstrap whole seeds, compute the pre-specified decision criteria from raw rows, and refuse to label a run successful when validation has failed.

Run the current automated validation with:

```bash
python3 -m unittest discover -s code/ep001 -p 'test_*.py' -v
```

The utilities use NumPy already available in the environment; this plan does not install or declare new dependencies.

## Known ambiguities and boundaries

- **Input support versus geometric existence:** Decision 010 can construct an $x\in\mathbb R^2$ but need not place it in the support of every anisotropic law. EP001 samples $x$ from the law and directly tests this gap.
- **Natural state depends on the state generator:** “Naturally evolved” here means delayed reliable-target SGD from fixed initialization under the declared synthetic stream. It does not mean stationary, typical across every optimizer, or induced by an active router.
- **Two clocks:** $\Delta_k$ is indexed by common future SGD updates. The delayed protocol is indexed by operational rounds. EP001 records both and does not silently identify them.
- **Oracle versus practical routing:** exact $e_t$, $M$, $\mathsf H$, and $K_k$ are used only because the experiment is synthetic. Estimating them is out of scope unless the oracle experiment succeeds.
- **Expected versus realized effects:** a negative individual coupled realization is ordinary Monte Carlo variation. Expected reversal is determined by the operator value after the independent estimator validates it.
- **Full continuation value:** common-coupled population-risk transport does not include action-dependent future routing, responses, or costs. EP001-B may assess whether the surrogate is operationally material; EP001-C is the first phase where routing changes trajectories.
- **Rare spikes:** small $q$ creates rare large inputs. Runs must report finite-sample coverage of nonzero $Z_q$ events and instability. Neither clipping nor silent run deletion is permitted without a revised plan.
