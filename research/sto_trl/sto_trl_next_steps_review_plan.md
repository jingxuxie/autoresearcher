# Stochastic TRL: Results Review and Next-Step Plan

**Date:** 2026-06-13  
**Repo reviewed:** `jingxuxie/autoresearcher`, especially `research/sto_trl/`  
**Scope reviewed:** charter, progress summary, results/reviews for iterations 0002–0007, 0008 stop decision, metrics artifacts, and the 0007 generic-uncertainty script/artifacts.

---

## 1. Bottom line

The current results are **promising for the problem diagnosis**, but **not yet promising for the originally proposed stochastic successor-distance TRL method**.

The evidence says:

1. **Raw deterministic-style TRL really does have a stochastic overoptimism failure mode.** This is a valid and useful finding.
2. **Log-space TRL is a useful baseline** for long-horizon recovery under matched or adequate coverage.
3. **The explicit successor-distance + TRL-log variant is not distinct from TRL-log** on the current tabular diagnostics.
4. **The hand-shaped conservative penalty can fix one lucky-only stress case**, but it is too tailored to count as a general method.
5. **The generic count/Dirichlet-style uncertainty penalty reduced some Q overestimation but failed the policy-level stress test**, so it should not be treated as a solved stochastic extension.

My recommendation: **continue, but pivot the project**. Do not scale to OGBench, AntMaze, or neural networks yet. The next phase should test a more principled formulation around **transition-level uncertainty / posterior transition models / identifiability**, while keeping log-TRL as the horizon-propagation component.

A concise reframing:

> Can transition-level stochastic uncertainty plus log-space transitive propagation produce calibrated long-horizon goal reachability under finite offline stochastic coverage?

This is a better question than:

> Can successor-distance regularization improve TRL-log?

The latter is currently weakly supported or negatively supported.

---

## 2. Evidence review

### 2.1 Experiment setup quality

The setup is appropriate for early screening:

- It starts with tabular experiments, as the charter requires.
- It uses exact DP ground truth for discounted reachability.
- It includes deterministic chain sanity checks.
- It includes stochastic risky shortcut MDPs with safe-optimal and risk-optimal regimes.
- It reports value MSE, calibration, overestimation, regret, risky-action selection, and coverage diagnostics.
- Later iterations validate result artifacts and compare methods on controlled matched datasets.

This means the current negative results should be taken seriously. They are not just artifacts of a sloppy first experiment.

### 2.2 What is genuinely positive

| Finding | Evidence | Meaning |
|---|---|---|
| Raw TRL is support-driven under stochastic shortcuts | In 0002, raw TRL recovered the chain but selected risky whenever a lucky risky transition was observed; in safe-optimal matched `2/6`, it chose risky with regret `0.504` and learned risky Q `0.900` vs exact `0.225`. | This confirms a real stochastic failure mode worth studying. |
| Log-TRL recovers long-horizon values under censoring | In 0003, chain held-out MSE dropped from MC-only `0.391705823230` to `0.0` for TRL-log and MC+TRL-log. | Log-space transitive propagation is useful and should remain a core baseline. |
| Log-TRL fixes matched stochastic shortcut cases | In 0002/0003, TRL-log chose the exact optimal action in matched regimes. | The basic empirical-frequency/log-backup story works when coverage is representative. |
| The tabular harness is reproducible and well-instrumented | Results contain commands, raw metrics, summaries, transition/value tables, and reviews. | This is a useful benchmark harness to keep extending. |

### 2.3 What is negative or weak

| Finding | Evidence | Meaning |
|---|---|---|
| Successor-distance + TRL-log did not show distinct value | In 0005, improving lambdas matched TRL-log within `1e-10`; `any_positive_successor_evidence=false`. | Do not continue the current successor-distance formulation without a new theoretical or algorithmic distinction. |
| One-sided conservative penalty is hand-shaped | In 0006, the penalty is `alpha * gamma / sqrt(count)` only for direct-goal single-branch shortcut actions at multi-action states. | It is useful as a diagnostic, not a general algorithm. |
| Generic count-based uncertainty is not enough | In 0007, the best generic variant reduced safe-optimal lucky-only Q overestimation but still chose risky and kept policy regret `0.504`, unchanged from TRL-log. | It reduces a scalar error but does not fix the decision. |
| Risk-optimal no-success remains unresolved | If the true risky action is optimal but the offline dataset has zero risky successes, empirical methods choose safe. | This is an identifiability/prior problem, not just a TRL backup problem. |
| Scaling now would be premature | The 0008 decision correctly says OGBench/neural work would be premature because the tabular stochastic-calibration story is weak. | Do not spend compute until the assumptions are clarified. |

---

## 3. My answer: should you continue?

### Continue if the project is reframed

The project is worth continuing **if the next phase explicitly studies one of these two questions**:

1. **Transition-level uncertainty + TRL:**  
   Can a posterior or confidence-set transition model correct stochastic branch bias while log-TRL handles long-horizon composition?

2. **Identifiability boundaries for stochastic offline TRL:**  
   Which stochastic failures are impossible from offline data alone, and what priors or coverage assumptions are needed?

### Do not continue the original formulation unchanged

I would not continue with more variants of:

- successor-distance + TRL-log with only a lambda sweep,
- ad hoc count penalties,
- direct-goal shortcut-specific rules,
- generic scalar uncertainty penalties applied at goal-value level.

The next version needs a principled assumption: posterior transition uncertainty, confidence sets, conservative/off-policy lower bounds, or an explicit prior over risky branches.

---

## 4. Key conceptual pivot

The current experiments reveal three different issues that should no longer be conflated:

### A. Long-horizon propagation

TRL-log helps here. It composes short-horizon observed transitions into long-horizon reachability. This is the positive result from 0003.

### B. Aleatoric stochasticity

When stochastic outcomes are sampled representatively, empirical frequencies and TRL-log can recover the right value.

### C. Epistemic uncertainty / finite offline coverage

This is the unresolved part. Lucky-only and no-success regimes are about finite-data uncertainty, not merely stochastic dynamics.

A good next method should operate at the **transition-model uncertainty level**, not by adding a generic penalty directly to `Q(s,a,g)` after the fact.

---

## 5. Immediate next-step plan

The next phase should be short, CPU-friendly, and tabular. I would run the following milestones in order.

---

# Milestone 0 — Freeze current evidence and tighten success criteria

**Goal:** Avoid another undirected automatic sweep.

Create a short file:

```text
research/sto_trl/progress/human_pivot_0008.md
```

Include:

- raw TRL failure is established,
- log-TRL baseline is useful,
- successor-distance lambda version is negative,
- generic count penalty is insufficient,
- next experiments require a principled transition-uncertainty assumption.

Revise success criteria for future experiments:

A future method is positive only if it satisfies all of:

1. Preserves deterministic chain held-out MSE near zero.
2. Preserves matched safe-optimal and matched risk-optimal action choices.
3. Improves safe-optimal lucky-only policy regret versus TRL-log.
4. Does not simply avoid risky everywhere.
5. Beats or matches a simple empirical-transition-model DP baseline.
6. Shows a specific benefit from the transitive/log-TRL component, not just from uncertainty alone.

**Exit condition:** A new checklist exists before writing more algorithm code.

---

# Milestone 1 — Identifiability and coverage grid

**Proposed iteration:** `0008_identifiability_grid`  
**Priority:** Highest  
**Runtime target:** seconds to minutes

## Question

Which failures are actually solvable from offline data, and which require priors?

## Why this matters

The `risk_optimal_no_success_stress` case cannot be solved by empirical data alone if the dataset contains zero risky successes but the true risky success probability is high. A method can choose risky there only if it has an explicit optimistic prior, model assumption, or external knowledge.

Before adding algorithms, map the impossible/ambiguous regimes.

## MDP family

Use the same risky shortcut structure, but sweep:

```python
true_p_risky_success = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90]
safe_path_length = [2, 3, 4, 5]
risky_episode_count = [1, 2, 4, 8, 16, 32]
observed_success_count = 0..n
```

Compute:

```python
Q_star_risky = gamma * true_p_risky_success
Q_star_safe = gamma ** safe_path_length
```

For each `(true_p, safe_len, n, k_success)` compare:

- empirical mean risky value: `gamma * k / n`,
- Beta posterior mean with several priors,
- lower confidence bound / posterior quantile,
- upper confidence bound / optimistic posterior quantile,
- TRL-log value,
- raw TRL value.

## Required outputs

Save:

```text
research/sto_trl/artifacts/0008/identifiability_grid.csv
research/sto_trl/artifacts/0008/regret_heatmaps.json
research/sto_trl/artifacts/0008/impossibility_cases.json
research/sto_trl/results/0008_result.json
research/sto_trl/results/0008_summary.md
```

## Metrics

For each method:

- policy regret,
- chosen action,
- risky Q calibration,
- safe Q calibration,
- false-risky rate when safe is optimal,
- false-safe rate when risky is optimal,
- calibration across `(n, k)` bins.

## Pass/fail interpretation

This is not an algorithm win/loss experiment. It is a map of what is identifiable.

Expected outcome:

- Conservative lower bounds fix safe-optimal lucky-only but fail risk-optimal no-success.
- Optimistic priors fix risk-optimal no-success but can fail safe-optimal lucky-only.
- No single prior-free method can solve both extremes.

If this expected outcome appears, the project should explicitly state an assumption before continuing.

---

# Milestone 2 — Transition-level posterior baseline

**Proposed iteration:** `0009_transition_posterior_baseline`  
**Priority:** Highest  
**Runtime target:** minutes

## Question

Does transition-level Bayesian or confidence-set uncertainty solve the branch issue better than goal-level penalties?

## Why this differs from 0007

0007 applied a generic penalty to value/goal-level estimates. The next experiment should model uncertainty in:

```text
P(s' | s, a)
```

This is more principled because the stochasticity lives in transition outcomes, not directly in every goal-conditioned value.

## Methods to implement

### 1. Empirical model DP

Estimate transition probabilities from counts:

```python
P_hat[s, a, s_next] = count(s, a, s_next) / count(s, a)
```

Then run exact value iteration on `P_hat`.

This is an important baseline. If a proposed TRL method cannot beat empirical-model DP in tabular settings, its contribution must come from function approximation or long-horizon composition, not tabular stochastic estimation.

### 2. Bayesian posterior mean DP

Use a Dirichlet posterior:

```python
P_sample_or_mean[s, a] ~ Dirichlet(counts[s, a, :] + alpha_prior[s, a, :])
```

Evaluate posterior mean values.

### 3. Posterior quantile DP

Sample `M` transition models from the posterior:

```python
for m in range(M):
    P_m ~ Dirichlet(counts + prior)
    V_m = value_iteration(P_m)
Q_lcb = quantile(Q_m, tau=0.10)
Q_mean = mean(Q_m)
Q_ucb = quantile(Q_m, tau=0.90)
```

Test `tau ∈ [0.05, 0.10, 0.25, 0.50, 0.75, 0.90]`.

### 4. Robust confidence-set DP

For small tabular MDPs, implement a conservative confidence-set approximation:

```python
Q_robust(s,a,g) = gamma * min_{P in confidence_set(s,a)} E_P[V(next,g)]
```

Start with a simple L1 confidence radius, or approximate via posterior samples and quantiles.

## Baselines

Compare against:

- MC supervised,
- raw TRL,
- TRL-log,
- MC+TRL-log,
- successor_distance_best_0005,
- one_sided_conservative_0006,
- generic_0007 best method,
- empirical-model DP,
- posterior mean DP,
- posterior quantile DP.

## Pass criteria

A transition-level method is promising only if it:

1. Fixes or materially reduces safe-optimal lucky-only policy regret.
2. Does not fail risk-optimal matched cases.
3. Has a clear, predeclared behavior on risk-optimal no-success: either conservative by design or optimistic by prior.
4. Beats generic 0007 on policy regret, not only on Q-overestimation.
5. Explains every win by transition uncertainty, not by direct-goal shortcut rules.

## Expected decision after this milestone

If posterior/robust transition baselines solve the tabular cases, then the research question becomes:

> How do we combine transition uncertainty with TRL-log so we retain long-horizon composition under function approximation?

If they do not solve the cases, stop the stochastic-calibrated TRL branch and write the negative result.

---

# Milestone 3 — Add transitive propagation to posterior transition models

**Proposed iteration:** `0010_posterior_log_trl`  
**Priority:** High, but only after Milestone 2

## Question

Does log-TRL add anything beyond posterior model estimation?

## Design

For each posterior transition sample `P_m`, compute or learn short-horizon labels, then apply log-space transitive backups:

```python
log_U(s, a, g) <- max_or_softmax_w [log_U(s, a, w) + log_V(w, g)]
```

Compare:

1. posterior model DP only,
2. posterior model + MC labels only,
3. posterior model + TRL-log,
4. posterior model + TRL-log with conservative quantile action selection.

## Critical ablation

You need to show the transitive component matters.

Measure:

```text
posterior_log_trl - posterior_model_dp
```

on long-horizon heldout value MSE and regret.

If posterior model DP already solves everything and TRL-log adds nothing in tabular experiments, that is okay. It means the next research claim must be about function approximation and long-horizon credit assignment, not tabular stochastic inference.

## Pass criteria

Continue only if posterior + TRL-log improves at least one of:

- held-out long-horizon value MSE,
- sample efficiency at small `n`,
- calibration under censored long-horizon labels,
- stability under finite update steps,

without increasing policy regret in matched stochastic cases.

---

# Milestone 4 — Randomized MDP generalization suite

**Proposed iteration:** `0011_randomized_tabular_suite`  
**Priority:** High  
**Runtime target:** minutes

## Question

Does the method generalize beyond the five hand-authored scenarios?

## Why this matters

The current positive 0006 result is too tied to a direct-goal shortcut. The next method must survive randomized stress tests.

## MDP families

Create 100–500 tiny MDPs across these families:

### Family A: Branch-chain MDPs

- one safe path,
- one risky shortcut,
- random safe length,
- random risky success probability,
- optional trap/recovery path.

### Family B: Stochastic safe route

- safe path also has small slip/failure probability,
- tests whether method avoids over-conservatism toward all stochastic actions.

### Family C: Multi-branch stochastic maze

- 2–4 actions at start,
- multiple stochastic branches,
- no direct-goal shortcut in many cases.

### Family D: Stochastic teleporter

- action may teleport to one of several states,
- goal may require composition after teleport,
- closer to the future OGBench/PointMaze teleporter motivation.

## Dataset regimes

For each MDP, generate offline datasets under:

- matched coverage,
- lucky-biased coverage,
- unlucky-biased coverage,
- missing-success coverage,
- missing-failure coverage,
- behavior-policy skew.

## Metrics

Aggregate over random seeds:

- median regret,
- 90th percentile regret,
- risky false-positive rate,
- risky false-negative rate,
- calibration error,
- overestimation error,
- underestimation error,
- long-horizon heldout MSE,
- fraction of MDPs where method beats TRL-log,
- fraction where method is worse than empirical-model DP.

## Pass criteria

A method is promising only if:

- it improves median regret versus TRL-log,
- it improves worst-decile regret or at least does not worsen it,
- it does not rely on direct-goal shortcut detection,
- it beats empirical-model DP in long-horizon/censored settings or has a clear reason why not,
- wins persist over randomized MDPs, not only one handcrafted scenario.

---

# Milestone 5 — One-hot neural tabular approximation

**Proposed iteration:** `0012_onehot_mlp`  
**Priority:** Medium  
**Only run after:** Milestones 2–4 show a principled positive result.

## Question

Does the method still work when values are represented by a small neural network instead of exact tables?

## Setup

Use the same randomized tabular MDPs, but replace table values with a tiny MLP:

```text
input: one-hot(s), one-hot(a), one-hot(g)
output: log_U or U
```

Run 5–10 seeds.

Compare:

- TRL-log table,
- TRL-log MLP,
- posterior/robust method table,
- posterior/robust method MLP.

## Metrics

- MSE to exact DP,
- regret,
- overestimation,
- training stability,
- sensitivity to target-network lag,
- sensitivity to expectile/softmax temperature.

## Pass criteria

The method should preserve the tabular direction under function approximation. If it collapses here, do not move to continuous control.

---

# Milestone 6 — Tiny stochastic gridworld / point maze

**Proposed iteration:** `0013_tiny_grid_or_pointmaze`  
**Priority:** Medium-low  
**Only run after:** One-hot MLP succeeds.

## Question

Does the method survive a spatial environment with stochastic transitions?

## Start with a hand-coded gridworld

Avoid OGBench first. Use a tiny gridworld:

- 7x7 or 11x11 grid,
- slip probability sweep `[0.0, 0.05, 0.10, 0.20]`,
- stochastic teleporter cells,
- safe long route vs risky shortcut,
- exact DP still available.

## Baselines

- empirical model DP,
- posterior model DP,
- TRL-log,
- posterior + TRL-log,
- conservative/posterior quantile action selection.

## Pass criteria

Only move to OGBench if the method improves regret/calibration on the gridworld and remains stable with MLP value approximation.

---

# Milestone 7 — OGBench/PointMaze teleport only after gates pass

**Proposed iteration:** `0014_ogbench_pointmaze_teleport`  
**Priority:** Low for now

Do not run this yet.

Run only if:

1. transition/posterior method passes randomized tabular tests,
2. one-hot MLP works,
3. tiny stochastic gridworld works,
4. the algorithm has a clear ablation showing what TRL-log contributes beyond model uncertainty.

Start with the smallest OGBench PointMaze teleport task and a tiny number of seeds. Do not start with AntMaze or HumanoidMaze.

---

## 6. Specific algorithmic directions to test

### Direction A — Keep log-TRL as a baseline, not the full method

TRL-log is clearly useful for horizon composition. Keep it in every experiment.

But do not claim that log-TRL alone solves stochastic offline RL. It fails lucky-only and no-success coverage regimes.

### Direction B — Transition-posterior TRL

Most promising next direction.

Core idea:

```python
# Estimate transition uncertainty
posterior_P[s,a] = Dirichlet(counts[s,a] + prior)

# Sample transition models
for m in range(M):
    P_m = sample(posterior_P)
    U_m = log_trl_or_value_iteration(P_m)

# Use posterior mean or quantile for learning/action selection
U_mean = mean(U_m)
U_lcb = quantile(U_m, tau)
U_ucb = quantile(U_m, 1 - tau)
```

This separates:

- transition uncertainty,
- value propagation,
- policy risk preference.

### Direction C — Robust TRL lower bound

Conservative version:

```python
Q_target(s,a,g) = gamma * min_{P in C(s,a)} E_P[V(next,g)]
```

Then apply log-transitive propagation using robust targets.

This should fix lucky-only overoptimism but will be conservative unless paired with a prior or exploration assumption.

### Direction D — Bayesian risk-sensitive family

Instead of trying to find one universal method, report a family:

- pessimistic quantile for safety-critical offline RL,
- posterior mean for calibrated prediction,
- optimistic quantile for exploration/planning settings.

This may be a cleaner paper story than pretending one setting solves all regimes.

---

## 7. What not to do next

Do **not**:

- run another generic alpha/lambda sweep without a new assumption,
- move directly to OGBench,
- run AntMaze/HumanoidMaze,
- claim successor-distance evidence from the current 0005 results,
- tune another hand-shaped direct-goal penalty,
- optimize only held-out MSE while ignoring policy regret,
- treat no-success risk-optimal cases as solvable without priors.

---

## 8. Recommended experiment order

Run these in order:

1. `0008_identifiability_grid`
2. `0009_transition_posterior_baseline`
3. `0010_posterior_log_trl`
4. `0011_randomized_tabular_suite`
5. `0012_onehot_mlp`
6. `0013_tiny_grid_or_pointmaze`
7. `0014_ogbench_pointmaze_teleport`

Stop after any milestone that fails its gate.

---

## 9. Proposed decision gates

### Gate A — After Milestone 1

If the identifiability grid confirms that no prior-free method can solve both lucky-only and no-success regimes, explicitly choose one of:

- conservative offline RL objective,
- Bayesian prior objective,
- calibrated prediction objective,
- exploration/optimistic planning objective.

Do not mix these objectives in one metric.

### Gate B — After Milestone 2

If transition-posterior baselines solve the tabular branch problem, continue.

If not, stop or write a negative result.

### Gate C — After Milestone 3

If posterior + TRL-log does not beat posterior-only baselines on any long-horizon/censored metric, the contribution is not TRL-specific. Pivot to uncertainty modeling or stop.

### Gate D — After Milestone 4

If the method only works on the hand-authored risky shortcut MDP and not randomized MDPs, do not scale.

### Gate E — After Milestone 5

If the method fails under one-hot MLP approximation, do not run OGBench.

---

## 10. Concrete result table template for future summaries

Each future result summary should include this table:

| Scenario group | Method | Regret median | Regret p90 | Calibration | Overest. | Underest. | False risky | False safe | Long-horizon MSE | Beats TRL-log? | Beats empirical DP? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| matched | | | | | | | | | | |
| lucky-biased | | | | | | | | | | |
| lucky-only | | | | | | | | | | |
| unlucky-biased | | | | | | | | | | |
| no-success | | | | | | | | | | |
| randomized all | | | | | | | | | | |

Also include:

```text
- exact commands run
- raw metrics file path
- coverage diagnostics file path
- transition counts summary
- predeclared pass/fail status
- known limitations
```

---

## 11. Code hygiene recommendations

The reviews repeatedly mention unrelated protected-file modifications. For the next phase:

1. Put new experiments only under:

```text
research/sto_trl/artifacts/0008/
research/sto_trl/results/
research/sto_trl/reviews/
research/sto_trl/decisions/
```

2. Avoid editing:

```text
scripts/autoresearcher.py
schemas/
project control files
```

3. Factor shared tabular code into one local experiment utility only if allowed by the project rules. Otherwise copy code per artifact and record all commands.

4. Every run should save:

```text
raw_metrics.json
metrics.csv
transition_tables.json
value_tables.json
coverage_diagnostics.json
```

5. Every algorithm result should be comparable on identical offline datasets.

---

## 12. Suggested next experiment prompt

Use this as the next human-authored experiment request:

> Implement `0008_identifiability_grid`. Do not introduce a new stochastic TRL algorithm yet. Sweep true risky success probability, safe path length, risky sample count, and observed success count. Compare empirical, TRL-log, raw TRL, Beta posterior mean, posterior lower quantile, and posterior upper quantile. Produce regret/calibration heatmaps and explicitly mark cases that are not identifiable without a prior. Save raw metrics, CSV, and summary. The purpose is to decide what assumption the next stochastic TRL variant is allowed to make.

---

## 13. Final recommendation

Continue the research, but with a narrowed claim:

> **Promising:** stochastic TRL as a study of finite-coverage stochastic branch uncertainty plus log-space long-horizon propagation.

> **Not currently promising:** successor-distance TRL as implemented in 0004/0005, or generic count penalties as implemented in 0007.

The next publishable path is likely not “we added stochastic successor distances to TRL.” It is more likely:

> “We identify stochastic overoptimism and identifiability failures in transitive offline GCRL, then show that transition-level posterior/robust uncertainty can be combined with log-space transitive propagation to preserve long-horizon generalization without support-driven optimism.”

That is a stronger and cleaner project direction.
