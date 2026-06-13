# Review 0002: pass

Allows auto-continue: True

## Reasons

- Required outputs are present: research/sto_trl/results/0002_result.json, research/sto_trl/results/0002_summary.md, and populated artifacts under research/sto_trl/artifacts/0002.
- Result JSON validates against schemas/result.schema.json with artifact existence checks.
- The script implements exact discounted-reachability DP for evaluation and uses constructed offline trajectories for training; the training methods inspected use empirical trajectory counts or returns, not true transition probabilities or DP labels.
- The comparison is fair for this diagnostic: mc_supervised, trl_raw, trl_log, and mc_plus_trl_log are run on the same per-scenario offline datasets with the same gamma and fixed update count.
- The experiment includes the deterministic chain guard plus both safe-optimal and risk-optimal risky-shortcut settings across matched, lucky_biased, lucky_only, unlucky_biased, and no_risky_success regimes.
- Raw metrics are not limited to prose or aggregates: metrics.csv and raw_metrics.json include per-scenario, per-method value errors, Q calibration, policy regret, risky action selection, learned/exact Q values, and coverage diagnostics.
- The interpretation is appropriately bounded: it reports raw TRL support-driven overestimation and explicitly notes that MC/log calibration is coverage-dependent and can become overoptimistic or conservative.

## Required fixes


## Risk flags

- The Q overestimation and underestimation maxima are computed across all goals, not only the eval goal, so those headline error fields can reflect non-eval goals such as trap; eval-goal learned/exact Q columns mitigate this.
- commands_run records setup, execution, and validation commands but not the manual edits that transformed the copied 0001 script into the 0002 harness.
- git status only showed an untracked reviewer packet, but without committed baselines this review cannot fully prove no prior artifacts were modified.
