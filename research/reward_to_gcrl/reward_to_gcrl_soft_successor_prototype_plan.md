# Prototype Plan: Soft Successor-Measure for Reward-to-GCRL

**Project goal:** Prototype a low-variance alternative to the blog post's sampled MDP-to-GCMDP conversion. The immediate goal is not to build a full paper-ready benchmark suite, but to answer a smaller question quickly:

> Can we preserve the reward-to-goal equivalence while avoiding the sparse, high-variance terminal sampling that made the blog conversion hard to learn?

This plan assumes you will **not reimplement every baseline from the blog**. Use the blog's reported baselines as an initial reference point. Your prototype should focus on one new method: **soft successor-measure reward-to-goal learning**.

Reference blog: <https://iclr-blogposts.github.io/2026/blog/2026/mdp-to-gcmdp/>

---

## 1. Core idea

### 1.1 The blog conversion, in one line

For normalized reward \(\bar r(s,a) \in [0,1]\), the blog constructs an augmented MDP with success and failure absorbing states:

\[
P_{\text{aug}}(s' \in S \mid s,a)=\gamma P(s'\mid s,a),
\]

\[
P_{\text{aug}}(g_+\mid s,a)=(1-\gamma)\bar r(s,a),
\]

\[
P_{\text{aug}}(g_-\mid s,a)=(1-\gamma)(1-\bar r(s,a)).
\]

Then maximizing the probability of reaching \(g_+\) is equivalent to maximizing normalized discounted return.

The problem is algorithmic, not mathematical: when \(\gamma=0.99\), even \(\bar r=1\) gives only a 1% immediate success-transition probability. Dense reward becomes rare terminal events.

---

## 2. Soft successor-measure version

Instead of **sampling** the augmented terminal transition, train against its **expected probability mass**.

Define a goal-conditioned quantity:

\[
M_\theta(s,a,g) \approx \text{optimal discounted mass of reaching/visiting goal } g
\]

with goal set

\[
\mathcal G = S \cup \{g_+\}.
\]

For the artificial reward-success goal \(g_+\), use the soft Bellman target:

\[
y(s,a,g_+) = (1-\gamma)\bar r(s,a) + \gamma \max_{a'} M_{\bar\theta}(s',a',g_+).
\]

This is the key trick. You do **not** sample whether the agent transitioned to \(g_+\). You directly use the expected mass \((1-\gamma)\bar r(s,a)\).

For real state-goals \(g \in S\), use an auxiliary successor-measure target:

\[
y(s,a,g) = (1-\gamma)\mathbf{1}[s'=g] + \gamma \max_{a'}M_{\bar\theta}(s',a',g).
\]

The policy for the original reward task is:

\[
\pi(s)=\arg\max_a M_\theta(s,a,g_+).
\]

Important sanity check:

\[
M^*(s,a,g_+)=(1-\gamma)Q^*_{\bar r}(s,a),
\]

so the \(g_+\) head is exactly a normalized reward Q-function when trained with the soft target. This means:

- In tabular settings, terminal-only soft successor learning should behave like Q-learning.
- Any research gain must come from better representation learning, auxiliary real-state goals, lower target variance, better offline generalization, or better long-horizon compositionality.
- If terminal-only soft successor learning does **not** match Q-learning in tabular CliffWalking, the implementation is wrong.

---

## 3. Why this is worth testing

The blog's sampled augmented GCMDP has two practical failure modes:

1. Reward becomes stochastic transition mass, increasing target variance.
2. Dense reward supervision is delayed into rare success/failure absorbing states, making the problem sparse.

The soft successor-measure prototype directly tests whether those are the main blockers.

The method keeps the conceptual reward-as-goal framing but restores dense supervision:

| Component | Blog sampled conversion | Soft successor-measure conversion |
|---|---|---|
| Reward signal | Sampled terminal event | Expected terminal mass |
| Immediate \(g_+\) target | \(\mathbf{1}[s_{\text{aug}}'=g_+]\) | \((1-\gamma)\bar r(s,a)\) |
| Variance from terminal sampling | High | Removed |
| Real achieved goals | Not useful by default | Added as auxiliary goals |
| Policy extraction | Reach \(g_+\) | Maximize \(M(s,a,g_+)\) |

---

## 4. Minimal implementation path

### 4.1 Start with discrete environments

Use environments where every failure is inspectable:

1. **CliffWalking**
   - Use Gymnasium `CliffWalking-v0` or the blog's 48-state variant if available.
   - Primary sanity environment.
   - The terminal-only soft method should solve it about as easily as ordinary Q-learning.

2. **RiverSwim**
   - Implement a small custom chain with 6, 10, and 20 states.
   - Useful for exploration and long-horizon reward propagation.

3. **Tiny FourRooms**
   - Optional after the first two.
   - Useful for testing whether auxiliary real-state goals learn meaningful reachability structure.

Do not start with MuJoCo, AntMaze, or image observations. You first need to establish that the operator and diagnostics behave correctly.

---

## 5. Code organization

Suggested small repo layout:

```text
reward_to_goal_ssm/
  envs.py                 # CliffWalking wrapper, RiverSwim, tiny FourRooms
  replay.py               # simple replay buffer with trajectory IDs
  ssm_tabular.py           # tabular soft successor-measure learner
  ssm_nn.py                # neural / factorized learner
  train_online.py          # epsilon-greedy online training
  train_offline.py         # fitted Q-style offline training
  diagnostics.py           # variance, Bellman error, g+ event counts, plots
  configs/
    cliff_tabular.yaml
    river_tabular.yaml
    cliff_nn_aux.yaml
```

---

## 6. Prototype v0: tabular terminal-only soft learner

This is the first thing to implement. It is intentionally simple.

### 6.1 Data structures

For \(n_S\) states and \(n_A\) actions:

```python
M_plus = np.zeros((n_states, n_actions))
```

This is just the \(g_+\) slice of \(M(s,a,g)\).

### 6.2 Update

For one transition \((s,a,r,s',done)\):

```python
r_bar = normalize_reward(r)  # must be in [0, 1]
bootstrap = 0.0 if done else np.max(M_plus[s_next])
target = (1.0 - gamma) * r_bar + gamma * bootstrap
M_plus[s, a] += lr * (target - M_plus[s, a])
```

Policy:

```python
a = np.argmax(M_plus[s])
```

This should be equivalent to Q-learning up to the scaling factor \((1-\gamma)\).

### 6.3 First validation

Run on CliffWalking with known reward normalization.

Expected outcome:

- Learns the same policy as Q-learning.
- \(M_+(s,a)/(1-\gamma)\) matches the ordinary normalized-reward Q-table.
- If it fails, debug reward normalization, terminal masking, and indexing before moving on.

---

## 7. Prototype v1: tabular vector successor-measure learner

Now add real state-goals.

### 7.1 Data structures

```python
g_plus = n_states
n_goals = n_states + 1
M = np.zeros((n_states, n_actions, n_goals))
```

Goal IDs:

- `0 ... n_states-1`: real state goals.
- `n_states`: artificial reward-success goal \(g_+\).

### 7.2 Vector update over all goals

For transition \((s,a,r,s',done)\):

```python
immediate = np.zeros(n_goals)

# Real-state successor-measure mass.
immediate[s_next] += (1.0 - gamma)

# Reward-success soft terminal mass.
immediate[g_plus] += (1.0 - gamma) * r_bar

if done:
    target = immediate
else:
    target = immediate + gamma * np.max(M[s_next], axis=0)

M[s, a, :] += lr * (target - M[s, a, :])
```

Reward-task policy:

```python
a = np.argmax(M[s, :, g_plus])
```

Goal-reaching auxiliary policy for a real goal \(g\):

```python
a = np.argmax(M[s, :, g])
```

### 7.3 What this version tests

This tabular vector version does **not** yet test representation learning, because every goal has its own table entry. It tests:

- Whether the \(g_+\) slice still solves the reward task.
- Whether real-state goals learn sensible reachability maps.
- Whether your Bellman targets are numerically stable.
- Whether diagnostics are correct.

Expected outcome:

- \(g_+\) policy matches terminal-only soft learner.
- Real-state goals produce intuitive shortest-path-ish behavior in grids.
- No major improvement over terminal-only in tabular mode; that is fine.

---

## 8. Prototype v2: low-capacity factorized successor-measure learner

This is the first version that can show a research signal.

The point is to force sharing across goals so that real-state auxiliary goals can help the reward-success goal.

### 8.1 Simple factorized model

Use a low-rank model:

\[
M_\theta(s,a,g) = \sigma(u_\theta(s,a)^\top v_\theta(g)),
\]

or without sigmoid if using unclipped MSE:

\[
M_\theta(s,a,g) = u_\theta(s,a)^\top v_\theta(g).
\]

For discrete environments:

```python
state_emb = Embedding(n_states, d)
action_emb = Embedding(n_actions, d)
goal_emb = Embedding(n_goals, d)

u = MLP(concat(state_emb[s], action_emb[a]))
v = goal_emb[g]
m = dot(u, v)
```

Start with `d = 8` or `d = 16`. Low capacity is useful because it makes transfer and interference visible.

### 8.2 Loss

For minibatch transitions and sampled goals:

```python
loss = mean((M_theta(s, a, g) - stopgrad(target(s, a, r, s_next, g))) ** 2)
```

Target:

```python
if g == g_plus:
    immediate = (1 - gamma) * r_bar
else:
    immediate = (1 - gamma) * int(s_next == g)

bootstrap = 0.0 if done else max_a_target M_target(s_next, a, g)
target = immediate + gamma * bootstrap
```

Use a target network or Polyak-averaged copy for stability.

### 8.3 Goal sampling

For each transition, sample a small set of goals:

```text
Always include: g_plus
Include: s_next
Include: 1-4 future states from the same trajectory, if available
Include: 8-32 random state goals as negatives / coverage goals
```

For the first neural prototype, use all goals if the state space is tiny. For larger grids, sampled goals are enough.

### 8.4 Loss weighting

Use separate weights:

\[
L = L_{g_+} + \lambda_{\text{state}} L_{S}.
\]

Start with:

```text
lambda_state in {0.0, 0.1, 0.3, 1.0, 3.0}
```

The key comparison is:

```text
lambda_state = 0.0    # terminal-only soft reward-to-goal
lambda_state > 0.0    # soft reward-to-goal + real-state auxiliary goals
```

---

## 9. Small-scale experiments and milestones

### Milestone 0: variance sanity check

**Goal:** Show the blog's sampled terminal event has much higher target variance than the soft target.

Create a synthetic one-state MDP with fixed \(\bar r\) and no dynamics complexity.

For sampled conversion:

\[
B \sim \text{Bernoulli}((1-\gamma)\bar r).
\]

For soft conversion:

\[
B_{\text{soft}} = (1-\gamma)\bar r.
\]

Sweep:

```text
gamma in {0.90, 0.95, 0.99, 0.995}
r_bar in {0.01, 0.1, 0.5, 1.0}
```

Log:

```text
empirical mean of target
empirical variance of target
number of observed g+ events per 10k transitions
```

Expected result:

- Means match.
- Soft target variance is zero for terminal sampling noise.
- Sampled target has very few \(g_+\) events when \(\gamma\) is high.

This is not a full RL result, but it validates the core diagnosis.

---

### Milestone 1: tabular CliffWalking equivalence

**Goal:** Confirm terminal-only soft successor learning is equivalent to normalized Q-learning.

Run:

```text
Environment: CliffWalking
Methods:
  A. ordinary Q-learning on normalized reward
  B. terminal-only soft successor learner, M(s,a,g+)
Seeds: 10
Metrics:
  average return
  success rate
  max |M_plus/(1-gamma) - Q|
  policy disagreement rate
```

Expected result:

- Methods A and B learn nearly identical policies.
- The scaled values agree up to learning noise.

Failure diagnosis:

| Symptom | Likely bug |
|---|---|
| \(M_+\) learns too slowly | accidentally using reward \(r\) instead of \((1-\gamma)r\), or bad learning rate |
| Wrong policy | reward normalization inverted or terminal mask wrong |
| Values explode | bootstrap after terminal states not masked |
| Good values but bad evaluation | policy extracting wrong goal slice |

---

### Milestone 2: sampled augmented vs soft terminal update

**Goal:** Demonstrate that soft terminal updates are better than sampled augmented updates under the same data budget.

You only need to implement one stripped-down sampled baseline, not all blog baselines.

For each original transition \((s,a,r,s')\):

Sample augmented next state:

```python
u = np.random.rand()
p_success = (1 - gamma) * r_bar
p_failure = (1 - gamma) * (1 - r_bar)

if u < p_success:
    s_aug_next = g_plus
elif u < p_success + p_failure:
    s_aug_next = g_minus
else:
    s_aug_next = s_next
```

Then train a goal-conditioned Q for reaching \(g_+\) on the sampled transition.

Compare against the soft target:

```python
target_soft = (1 - gamma) * r_bar + gamma * max_a M_plus[s_next, a]
```

Metrics:

```text
sample efficiency
success rate
TD target variance
number of success transitions observed
Bellman error to dynamic-programming solution, if available
```

Expected result:

- Soft update should be much more stable in short-horizon/dense-reward cases.
- Sampled augmented update should become worse as \(\gamma \to 1\).

This directly tests the hypothesis that the blog's negative result is partly an estimator problem.

---

### Milestone 3: real-state auxiliary goals in tabular mode

**Goal:** Verify auxiliary state-goals learn real reachability, but do not expect a major reward improvement yet.

Run tabular vector SSM:

```text
Goals: S union {g+}
Environment: CliffWalking or tiny FourRooms
Policy for reward task: argmax_a M(s,a,g+)
Policy for goal task: argmax_a M(s,a,g)
```

Diagnostics:

```text
For random state-goals, visualize greedy arrows toward g.
Plot M(s,a,g) heatmaps.
Check whether nearer states have higher successor mass.
Check whether cliff states are avoided for useful goals.
```

Expected result:

- Real-state goal slices should look like reasonable reachability maps.
- Reward-task performance should remain close to terminal-only soft.

If adding state-goals hurts \(g_+\) in tabular mode, the update is coupling goals accidentally; tabular slices should be independent unless you intentionally share parameters.

---

### Milestone 4: low-capacity function approximation

**Goal:** Test the first real research hypothesis: auxiliary real-state goals improve the learned representation for the reward-success goal.

Run factorized or small neural SSM on CliffWalking and RiverSwim.

Compare:

```text
A. terminal-only soft: goals = {g+}
B. combined soft SSM: goals = S union {g+}, lambda_state > 0
```

Use deliberately limited settings:

```text
embedding dimension: 4, 8, 16
replay size: 1k, 5k, 10k transitions
online interactions: small budgets first
reward sparsity: dense CliffWalking, sparse right-end RiverSwim
```

Metrics:

```text
reward-task return / success
steps to solve
Bellman error on g+
state-goal reachability accuracy
policy disagreement with tabular oracle
sensitivity to lambda_state
```

Promising signal:

- Combined goals reduce sample count to reach the same reward-task performance.
- Combined goals improve generalization from smaller datasets.
- Combined goals make the learned state representation more spatially meaningful.

Negative signal:

- Combined goals consistently slow down or destabilize \(g_+\).
- Improvements disappear when capacity increases.
- State-goal loss dominates and causes negative transfer.

If negative, try smaller \(\lambda_{\text{state}}\), future-state-only goals, or a separate auxiliary encoder with partial sharing.

---

### Milestone 5: offline fitted learning

**Goal:** Test whether soft successor-measure learning helps when data is fixed and reward information is limited.

Collect datasets:

```text
D_random: random policy
D_mixed: mixture of random, partial expert, and exploratory policies
D_near_opt: near-optimal policy
```

Train offline by repeated Bellman regression:

```text
for gradient_step in range(num_steps):
    batch = sample(D)
    sample goals
    compute soft successor targets
    update M_theta
```

Evaluate the greedy \(g_+\) policy online in the real environment.

Compare:

```text
A. terminal-only soft
B. combined soft SSM
C. optional: ordinary fitted Q-learning sanity baseline
```

Important caveat:

If the dataset has no support for a necessary transition, no method should solve the task. Track state-action coverage so you do not misdiagnose a support problem as an algorithm problem.

Promising signal:

- Combined soft SSM works better on mixed datasets than terminal-only soft.
- State-goal auxiliary training helps stitch paths in FourRooms or RiverSwim-like settings.

---

## 10. Diagnostics to implement from day one

### 10.1 Reward-success target variance

Track:

```text
Var[y(g+)] in each batch
mean y(g+)
percent nonzero immediate g+ labels
```

For soft SSM, the immediate \(g_+\) label is nonzero whenever \(\bar r>0\). For sampled augmentation, it is nonzero only when a sampled success transition occurs.

---

### 10.2 Bellman residual by goal type

Track separately:

```text
Bellman MSE for g+
Bellman MSE for real state-goals
Bellman MSE for achieved goals vs random goals
```

This tells you whether auxiliary goals are actually being learned or just adding noise.

---

### 10.3 Policy/value equivalence check

For tabular environments, compute dynamic-programming solutions when possible.

Check:

\[
\max_{s,a}\left|\frac{M(s,a,g_+)}{1-\gamma}-Q^*(s,a)\right|.
\]

Also check:

```text
policy disagreement rate = mean_s[argmax_a M(s,a,g+) != argmax_a Q*(s,a)]
```

---

### 10.4 Auxiliary transfer vs interference

For neural/factorized models, track performance as a function of \(\lambda_{\text{state}}\):

```text
lambda_state = 0.0, 0.1, 0.3, 1.0, 3.0
```

Interpretation:

| Pattern | Interpretation |
|---|---|
| Small \(\lambda\) helps, large hurts | useful auxiliary signal but negative transfer at high weight |
| All \(\lambda>0\) hurts | auxiliary goal formulation or sharing architecture is bad |
| Only helps in low-data regime | representation/curriculum benefit, worth pursuing |
| Helps even in tabular | likely bug, because tabular goals should be independent |

---

## 11. Concrete experiment grid

Start with this grid. Do not expand until these are understood.

### Experiment A: CliffWalking sanity

```text
Env: CliffWalking
Gamma: 0.95, 0.99
Methods:
  Q-learning sanity
  terminal-only soft SSM
  vector tabular SSM
Seeds: 10
Budget: small enough to see learning curves clearly
Decision: terminal-only soft must match Q-learning
```

### Experiment B: sampled vs soft estimator

```text
Env: CliffWalking
Gamma: 0.95, 0.99, 0.995
Methods:
  sampled augmented g+ learner
  terminal-only soft SSM
Metrics:
  return
  TD target variance
  g+ event count
Decision: soft should dominate in target variance and usually in learning speed
```

### Experiment C: auxiliary representation test

```text
Env: CliffWalking, RiverSwim-10
Methods:
  neural terminal-only soft SSM
  neural combined soft SSM
Architecture:
  low-rank dot-product model, d in {4, 8, 16}
Lambda_state:
  {0.0, 0.1, 0.3, 1.0}
Decision: combined goals should help at least one low-data or low-capacity setting
```

### Experiment D: offline mixed dataset

```text
Env: tiny FourRooms or RiverSwim-10
Datasets:
  random
  mixed
  partial expert
Methods:
  terminal-only soft SSM
  combined soft SSM
Optional sanity:
  fitted Q-learning
Decision: combined goals should help most on mixed datasets with reusable paths
```

---

## 12. Minimal pseudocode for neural SSM

```python
for step in range(num_updates):
    batch = replay.sample(batch_size)
    s, a, r, s_next, done = batch
    r_bar = normalize_reward(r)

    goals = sample_goals(
        include_g_plus=True,
        achieved=s_next,
        future_states=batch.future_states_optional,
        random_states=True,
        num_random=16,
    )

    pred = M_theta(s, a, goals)

    with torch.no_grad():
        # Max over actions for each sampled goal.
        next_values = []
        for a2 in actions:
            next_values.append(M_target(s_next, a2, goals))
        bootstrap = torch.stack(next_values, dim=0).max(dim=0).values
        bootstrap = bootstrap * (1.0 - done.float())

        immediate = torch.zeros_like(pred)
        immediate[goals == g_plus] = (1.0 - gamma) * r_bar
        immediate[goals != g_plus] = (1.0 - gamma) * (s_next[:, None] == goals).float()

        target = immediate + gamma * bootstrap

    loss_plus = mse(pred[goals == g_plus], target[goals == g_plus])
    loss_state = mse(pred[goals != g_plus], target[goals != g_plus])
    loss = loss_plus + lambda_state * loss_state

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    update_target_network()
```

Implementation note: the indexing in the pseudocode is schematic. In actual PyTorch, it is often easier to flatten all `(transition, goal)` pairs into one batch.

---

## 13. Reward normalization

The blog normalizes rewards into \([0,1]\). Do this explicitly and avoid running min/max normalization during early experiments.

Use known environment bounds:

```python
def normalize_reward(r, r_min, r_max):
    return np.clip((r - r_min) / (r_max - r_min), 0.0, 1.0)
```

Examples:

```text
CliffWalking:
  r_min = -100
  r_max = 0 or chosen max shaped reward

RiverSwim:
  r_min = 0
  r_max = 1
```

Be careful: changing reward normalization changes the policy if the transformation is not positive affine or if terminal handling changes. Keep it fixed across methods.

---

## 14. What would count as evidence that the idea is promising?

Minimum promising evidence:

1. Soft terminal \(g_+\) learning matches Q-learning in tabular environments.
2. Soft terminal learning has much lower target variance than sampled augmented learning.
3. Auxiliary real-state goals improve reward-task learning in at least one low-data, low-capacity, or offline setting.

Strong evidence:

1. Combined soft SSM beats terminal-only soft SSM on RiverSwim or FourRooms under matched data.
2. The improvement is robust to 5-10 seeds.
3. Diagnostics show state-goal learning improves reachability representations rather than merely regularizing values.
4. The method does not collapse when \(\gamma\) is high.

Weak or negative evidence:

1. Terminal-only soft works, but auxiliary goals never help.
2. Gains only appear from tuning but vanish across seeds.
3. The method is indistinguishable from ordinary Q-learning except for extra compute.

That negative result would still be informative: it would suggest the useful research direction is not the soft conversion alone, but either better goal-conditioned architectures, stochastic quasimetric structure, or offline stitching.

---

## 15. Likely failure modes and fixes

| Failure mode | Diagnosis | First fix |
|---|---|---|
| Soft \(g_+\) does not match Q-learning | Bug in scaling, terminal mask, or reward normalization | Compare against tabular Q after every update |
| Auxiliary goals hurt reward learning | Negative transfer | Lower \(\lambda_{\text{state}}\), use separate final head, or stop-gradient through shared encoder for auxiliary loss |
| Real-state goals learn nothing | Goal sampling too sparse or labels too imbalanced | Always include `s_next`; add future achieved states; oversample nearby goals |
| Neural model unstable | Bootstrapping instability | Add target network, Huber loss, smaller LR, clipped outputs |
| RiverSwim not solved | Exploration/support problem | Track state-action coverage; add epsilon schedule; do not blame SSM if right-end states are never seen |
| No improvement over Q-learning | Expected in tabular setting | Move to low-data, low-capacity, offline, or compositional environments |

---

## 16. Suggested first implementation order

1. Implement `normalize_reward` and tabular `M_plus` update.
2. Run CliffWalking sanity and compare against ordinary Q-learning.
3. Implement sampled augmented transition only for the \(g_+\) baseline.
4. Plot sampled-vs-soft target variance.
5. Implement vector tabular `M[s,a,g]` with real-state goals.
6. Visualize real-state goal policies.
7. Implement factorized neural `M_theta(s,a,g)`.
8. Run terminal-only vs combined-goal comparisons.
9. Add offline fitted training.
10. Decide whether to scale, pivot, or write a negative-result note.

---

## 17. One-sentence research framing

A good framing for this project is:

> The exact MDP-to-GCMDP conversion is sample-inefficient because it samples reward as rare terminal events; we propose a soft successor-measure estimator that preserves the reward-as-goal Bellman operator while using real-state goal prediction as auxiliary structure for representation learning.

---

## 18. Best first result to aim for

Aim for a figure with three panels:

1. **Target variance:** sampled augmented target vs soft target as \(\gamma\) increases.
2. **CliffWalking learning:** Q-learning, sampled augmented, terminal-only soft SSM.
3. **Auxiliary goal benefit:** terminal-only soft SSM vs combined soft SSM under low-capacity neural approximation or limited offline data.

If panel 1 is strong, panel 2 shows the estimator matters, and panel 3 shows auxiliary goals help at least somewhere, the idea is worth scaling.

