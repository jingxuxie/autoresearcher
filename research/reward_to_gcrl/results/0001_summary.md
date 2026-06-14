# Experiment 0001 Summary

## Setup

This diagnostic isolates the immediate terminal-mass estimator in the one-state augmented model. Rewards are pre-normalized as `r_bar in [0, 1]`; the sampled model uses `P(g_plus | s,a) = (1 - gamma) * r_bar`, and the deterministic soft target uses the same expected mass directly.

Samples per sweep point: `1000000`. Seed: `20260614`. Bootstrap is set to zero so the only variance source is the sampled terminal event.

## Commands Run

```bash
mkdir -p research/reward_to_gcrl/artifacts/0001 research/reward_to_gcrl/results
conda run -n autoresearcher_reward_to_gcrl python research/reward_to_gcrl/artifacts/0001/run_terminal_variance_diagnostic.py --samples 1000000 --seed 20260614
conda run -n autoresearcher_reward_to_gcrl python -m jsonschema -i research/reward_to_gcrl/results/0001_result.json schemas/result.schema.json
conda run -n autoresearcher_reward_to_gcrl python scripts/validate_artifacts.py --repo-root . --json research/reward_to_gcrl/results/0001_result.json --schema schemas/result.schema.json --check-result-artifacts
```

## Raw Metrics

| gamma | r_bar | sampled mean | soft mean | sampled var | soft var | g_plus / 10000 | expected / 10000 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.900 | 0.01 | 0.00096100 | 0.00100000 | 0.00096008 | 0.0 | 9.6100 | 10.0000 |
| 0.900 | 0.10 | 0.01019400 | 0.01000000 | 0.01009008 | 0.0 | 101.9400 | 100.0000 |
| 0.900 | 0.50 | 0.04987600 | 0.05000000 | 0.04738838 | 0.0 | 498.7600 | 500.0000 |
| 0.900 | 1.00 | 0.10050200 | 0.10000000 | 0.09040135 | 0.0 | 1005.0200 | 1000.0000 |
| 0.950 | 0.01 | 0.00047900 | 0.00050000 | 0.00047877 | 0.0 | 4.7900 | 5.0000 |
| 0.950 | 0.10 | 0.00508600 | 0.00500000 | 0.00506013 | 0.0 | 50.8600 | 50.0000 |
| 0.950 | 0.50 | 0.02521700 | 0.02500000 | 0.02458110 | 0.0 | 252.1700 | 250.0000 |
| 0.950 | 1.00 | 0.05002500 | 0.05000000 | 0.04752250 | 0.0 | 500.2500 | 500.0000 |
| 0.990 | 0.01 | 0.00010900 | 0.00010000 | 0.00010899 | 0.0 | 1.0900 | 1.0000 |
| 0.990 | 0.10 | 0.00099700 | 0.00100000 | 0.00099601 | 0.0 | 9.9700 | 10.0000 |
| 0.990 | 0.50 | 0.00502600 | 0.00500000 | 0.00500074 | 0.0 | 50.2600 | 50.0000 |
| 0.990 | 1.00 | 0.00978000 | 0.01000000 | 0.00968435 | 0.0 | 97.8000 | 100.0000 |
| 0.995 | 0.01 | 0.00004800 | 0.00005000 | 0.00004800 | 0.0 | 0.4800 | 0.5000 |
| 0.995 | 0.10 | 0.00047900 | 0.00050000 | 0.00047877 | 0.0 | 4.7900 | 5.0000 |
| 0.995 | 0.50 | 0.00254900 | 0.00250000 | 0.00254250 | 0.0 | 25.4900 | 25.0000 |
| 0.995 | 1.00 | 0.00501000 | 0.00500000 | 0.00498490 | 0.0 | 50.1000 | 50.0000 |

The rarest analytic event rate occurs at `gamma=0.995` and `r_bar=0.01`: `0.5000` expected `g_plus` events per 10000 transitions.

## Finite-MDP Equivalence

The same script solves a tiny 3-state, 2-action finite MDP twice: once with normalized rewards as `Q_norm_star`, and once with soft terminal mass rewards `(1 - gamma) * r_bar` as `F_gplus_star`. The check reports `max_abs(F_gplus_star / (1 - gamma) - Q_norm_star)`.

| gamma | max abs error | tolerance | q iterations | f iterations |
|---:|---:|---:|---:|---:|
| 0.900 | 7.615e-11 | 1.0e-06 | 264 | 242 |
| 0.950 | 3.476e-10 | 1.0e-06 | 540 | 482 |
| 0.990 | 9.708e-09 | 1.0e-06 | 2751 | 2293 |
| 0.995 | 3.948e-08 | 1.0e-06 | 5514 | 4457 |

## Outcome

Status: `completed`.

All sampled means were within the predeclared Monte Carlo tolerance rule `6 * sqrt(p * (1 - p) / samples)`, where `p=(1-gamma)*r_bar`. The soft target variance was exactly zero in every setting. The finite-MDP scaled soft successor check passed at tolerance `1.0e-06`. The sampled estimator therefore matches the soft target mean in this sanity check, but keeps Bernoulli target variance and exposes rare `g_plus` events as `gamma` approaches 1.

## Artifacts

- `research/reward_to_gcrl/artifacts/0001/run_terminal_variance_diagnostic.py`
- `research/reward_to_gcrl/artifacts/0001/raw_metrics.json`
- `research/reward_to_gcrl/artifacts/0001/metrics.csv`
- `research/reward_to_gcrl/artifacts/0001/metadata.json`
- `research/reward_to_gcrl/artifacts/0001/finite_mdp_equivalence.json`

## Negative Findings

No success criterion failed in this isolated diagnostic. This does not yet test bootstrapped fitted updates, partial-coverage data, or larger tabular environments; those remain separate follow-up checks.
