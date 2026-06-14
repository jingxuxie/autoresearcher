# Autoresearcher Phase 2 Improvement Plan

This is a Codex-ready build plan for improving the existing `jingxuxie/autoresearcher` repo after the Phase 1 local Codex loop worked on `research/sto_trl` but stopped after several iterations.

Primary goal: make the autoresearcher more autonomous **without** letting local Codex loops waste compute or overclaim. Add GPT-5.5-Pro supervision as a checkpoint backend every 2-3 iterations and whenever local Codex proposes `stop`, `pivot`, or `needs_human`.

Do **not** run more `sto_trl` research experiments while implementing this. Use `research/sto_trl` as a regression fixture for the orchestration logic.

---

## 1. Current diagnosis

The Phase 1 code is useful and already has several good pieces:

- `scripts/autoresearcher.py` implements a local Codex role loop.
- `autoresearcher.yaml` already has `gpt-5.5`, `xhigh`, `role-resume`, per-role sandboxes, timeouts, Git commit/push settings, and a `chatgpt_pro` config stub.
- The context builder already supports roles: `setup_env`, `supervisor`, `executor`, `reviewer`, `summarizer`, and `chatgpt_pro`.
- There are schemas for decision/result/review/pro-decision artifacts.
- The `sto_trl` run produced real evidence and stopped for research reasons, not simply because of an orchestrator crash.

But the system is not autonomous enough yet because:

1. **ChatGPT Pro is configured but not implemented.**
   - `chatgpt_pro.enabled` exists in config, but the backend is a stub.
   - When Pro review is due, the loop currently pauses with a message that Phase 2 is not implemented.

2. **Local Codex can make terminal decisions alone.**
   - A local supervisor `stop` currently sets the project status to `stopped`.
   - For research steering, local Codex should not be the final authority for `stop`, `pivot`, or ambiguous results once ChatGPT Pro is available.

3. **The original research plan is not always part of context.**
   - `research/sto_trl/charter.md` references `stochastic_trl_fast_prototype_plan.md`, but the context builder mostly uses the compact charter and recent artifacts.
   - The system needs a first-class way to include source documents and long project plans in compact packets.

4. **Progress tracking is mostly reviewer/supervisor judgment, not deterministic metrics.**
   - `state.json` has `primary_metric: null` and `best_primary_metric: null` for `sto_trl`.
   - The loop should maintain a metric ledger and stop/escalate based on deterministic signals where possible.

5. **No clean resume path after stop/pro review.**
   - Once `status` becomes `stopped`, the loop stops.
   - There should be a controlled `resume`, `ingest-pro-decision`, and `apply-pro-decision` path.


---

## 2. Desired architecture after this improvement

```text
Local Codex supervisor, role-resume
    ↓
local decision: continue / pivot / stop / needs_human
    ↓
checkpoint policy
    ↓
if routine continue:
    local Codex executor runs one small experiment
    local Codex reviewer audits result
    deterministic metrics ledger updates
    loop continues

if every 2-3 iterations OR local stop/pivot/needs_human OR timeout/ambiguous evidence:
    build PRO_REVIEW_PACKET.md
    send to same visible ChatGPT-5.5-Pro thread via codex-chatgpt-control when enabled
    otherwise pause with packet path for manual paste
    validate Pro decision
    apply Pro decision
```

The key principle:

```text
Codex = routine execution and local planning
ChatGPT-5.5-Pro = checkpoint supervisor / final authority on stop-pivot-continue gates
Repo files = source of truth
ChatGPT same thread = helpful memory, not the database
```

---

## 3. Same ChatGPT thread behavior

`codex-chatgpt-control` should be used in **same-thread mode** when configured.

Add config:

```yaml
chatgpt_pro:
  enabled: false
  backend: codex-chatgpt-control
  cadence_iterations: 3
  thread_url: null
  use_existing_thread: true
  existing_tab: true
  require_visible_session: true
  require_model: GPT-5.5 Pro
  require_thinking: Extended
  allow_model_fallback: false
  max_retries: 0
```

Behavior:

- If `thread_url` is set, send the review packet to that `https://chatgpt.com/c/<conversation-id>` thread.
- If `use_existing_thread=true`, prefer an already-open visible tab for that thread.
- If no thread URL is configured, create a new thread only if `allow_new_thread=true`; otherwise write a blocker.
- Save the thread URL in local state if the backend returns it.
- Still send a compact `PRO_REVIEW_PACKET.md` every checkpoint.

Important: same-thread ChatGPT history is useful, but do not rely on it as the only memory. The packet should include the latest objective evidence so the review is robust if the thread memory is stale, summarized, or too long.

---

## 4. New backend abstraction

Create `scripts/supervisor_backends.py`.

Implement:

```python
class SupervisorBackend:
    def decide(self, project: str, checkpoint_reason: str) -> SupervisorBackendResult:
        ...

class CodexSupervisorBackend(SupervisorBackend):
    ...

class ChatGPTProSupervisorBackend(SupervisorBackend):
    ...

class ManualProPacketBackend(SupervisorBackend):
    ...
```

Add dataclasses:

```python
@dataclass
class SupervisorBackendResult:
    status: str  # completed | blocked | failed
    decision_path: Path | None
    markdown_path: Path | None
    raw_response_path: Path | None
    blocker_path: Path | None
    reason: str | None
```

The orchestrator should not know browser details. It should call the backend and then validate produced files.

---

## 5. Checkpoint policy

Create `scripts/checkpoint_policy.py`.

Implement:

```python
def pro_checkpoint_due(state, config, local_decision=None, latest_review=None, latest_result=None) -> tuple[bool, str]:
    ...
```

Pro checkpoint should be due when:

- `chatgpt_pro.enabled=true` and completed iterations since last Pro review >= 2 or 3;
- local supervisor decision is `stop`;
- local supervisor decision is `pivot`;
- local supervisor decision is `needs_human`;
- executor timed out;
- reviewer verdict is `fail` or `needs_human`;
- reviewer verdict is `weak_pass` for 2 consecutive iterations;
- deterministic no-progress limit is reached or one round away;
- protected-file drift is detected;
- before moving from tabular to neural/OGBench/large compute;
- before making any strong “promising project” claim.

If `chatgpt_pro.enabled=false`, the same policy should build a packet and pause for manual Pro review instead of silently continuing.

---

## 6. Change local stop/pivot behavior

Modify `Orchestrator.run` so local Codex `stop`, `pivot`, or `needs_human` does not immediately finalize when Pro review is enabled or due.

Current bad behavior:

```text
local supervisor says stop
→ state.status = stopped
→ loop ends
```

New behavior:

```text
local supervisor says stop/pivot/needs_human
→ write local decision
→ build Pro packet
→ if chatgpt_pro.enabled: run ChatGPT Pro backend
→ else pause with packet path
→ apply Pro decision
```

Only allow final `stopped` status if:

- Pro agrees with stop, or
- Pro is disabled and human manually approves stop, or
- the project hits a hard safety budget that should not be overridden.

Add state fields:

```json
{
  "status": "active | paused | stopped | blocked",
  "pending_checkpoint": null,
  "pending_local_decision_path": null,
  "last_pro_review_iteration": 0,
  "last_pro_review_path": null,
  "pro_review_count": 0
}
```

---

## 7. Implement ChatGPT Pro packet builder v2

Improve `build_chatgpt_pro_context` in `scripts/build_context.py`.

The packet must include:

1. Explicit checkpoint reason.
2. Project charter.
3. Source documents, especially files referenced by the charter.
4. Current state.
5. Local supervisor's latest decision and rationale.
6. Last 2-3 plans.
7. Last 2-3 result summaries.
8. Last 2-3 review verdicts.
9. Deterministic metric ledger.
10. Known risks and blockers.
11. Exact requested output schema.
12. Instruction to decide: `continue`, `pivot`, `stop`, or `needs_human`.

Add source document discovery:

```python
def discover_source_docs(project_root: Path) -> list[Path]:
    patterns = [
        "*_prototype_plan.md",
        "*_plan.md",
        "project_goal.md",
        "research_goal.md",
        "brief.md",
        "background.md",
    ]
    ...
```

For `sto_trl`, the Pro packet should include or summarize:

```text
research/sto_trl/stochastic_trl_fast_prototype_plan.md
research/sto_trl/charter.md
research/sto_trl/progress/latest_summary.md
research/sto_trl/decisions/0008_decision.json
research/sto_trl/results/0007_result.json compact summary
research/sto_trl/reviews/0007_review.json
```

Keep the packet compact. Include full source document only if it is below a configurable character limit; otherwise include section headings and a generated compact summary.

Config:

```yaml
context:
  max_source_doc_chars: 12000
  max_result_chars: 8000
  recent_iterations_for_pro: 3
```

---

## 8. Add manual Pro fallback

Even after adding `codex-chatgpt-control`, keep a manual path.

Commands:

```bash
python scripts/autoresearcher.py build-pro-packet --project sto_trl --reason local_stop
python scripts/autoresearcher.py ingest-pro-response --project sto_trl --file /path/to/chatgpt_response.md
python scripts/autoresearcher.py apply-pro-decision --project sto_trl
python scripts/autoresearcher.py resume --project sto_trl --note "Pro approved continuing with narrowed pivot"
```

Manual response format:

```markdown
# ChatGPT Pro Decision

```json
{
  "decision": "continue",
  "confidence": 0.82,
  "rationale": "...",
  "evidence": ["..."],
  "risks": ["..."],
  "next_experiment": {
    "experiment_id": "0008",
    "objective": "...",
    "hypothesis": "...",
    "success_criteria": ["..."],
    "failure_criteria": ["..."],
    "tasks_for_codex": ["..."],
    "required_outputs": ["..."],
    "estimated_runtime_minutes": 30
  }
}
```
```

The ingest command should extract the fenced JSON block, validate it against `schemas/pro_decision.schema.json`, save it under `decisions/`, and write `plan.md` if `next_experiment` is present.

---

## 9. Implement `codex-chatgpt-control` backend

Add `scripts/chatgpt_pro_bridge.py`.

Use the Python package when available, but keep it optional. If dependencies are missing, write a structured blocker instead of crashing.

Expected behavior:

```bash
python scripts/autoresearcher.py pro-review --project sto_trl --reason cadence
```

Files written:

```text
research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md
research/sto_trl/decisions/0008_pro_raw_response.md
research/sto_trl/decisions/0008_pro_decision.json
research/sto_trl/decisions/0008_pro_decision.md
research/sto_trl/plans/0008_plan.json   # only if Pro decision has next_experiment
research/sto_trl/plans/0008_plan.md     # only if Pro decision has next_experiment
```

Blocker files:

```text
research/sto_trl/decisions/0008_pro_blocker.json
research/sto_trl/decisions/0008_pro_blocker.md
```

Blocker reasons:

```text
backend_dependency_missing
browser_bridge_unavailable
thread_url_missing
thread_unavailable
login_required
captcha
rate_limit
permission
selector_drift
model_unavailable
thinking_mode_unavailable
upload_failed
response_parse_failed
schema_validation_failed
```

Never blindly retry browser failures.

Pseudo-implementation:

```python
def run_chatgpt_pro_review(repo_root, project, config, packet_path, reason):
    try:
        from codex_chatgpt_control import Agent, BackendClient, Runner, StdioBackendTransport
    except ImportError:
        return write_blocker("backend_dependency_missing", ...)

    thread_url = config["chatgpt_pro"].get("thread_url") or local_state_thread_url(...)
    if not thread_url:
        return write_blocker("thread_url_missing", ...)

    backend = BackendClient(StdioBackendTransport(
        command=["npx", "--yes", "--package", "codex-chatgpt-control", "codex-chatgpt-control-backend"]
    ))
    runner = Runner(backend)
    try:
        result = runner.run_sync(
            Agent(name="chatgpt_pro_supervisor", instructions=read_prompt("chatgpt_pro_supervisor.md")),
            {
                "input": packet_path.read_text(),
                "thread": {"type": "url", "url": thread_url},
                "existingTab": True,
                "response": {"format": "markdown"},
            }
        )
    finally:
        backend.close()

    if result.status != "completed":
        return write_blocker(result.status or "pro_backend_failed", ...)

    save_raw_response(...)
    extract_fenced_json(...)
    validate_pro_decision(...)
    render_markdown(...)
    return completed_result
```

Adapt the exact key names to the installed SDK if needed. Add tests with a fake backend so CI does not require a real browser.

---

## 10. Update schemas

### 10.1 Update `decision.schema.json`

Add optional fields:

```json
{
  "checkpoint_recommended": { "type": "boolean" },
  "checkpoint_reason": { "type": ["string", "null"] },
  "terminal_decision_requires_pro": { "type": "boolean" }
}
```

Keep `decision` enum as-is if easier, or add:

```json
"pro_review"
```

If adding `pro_review`, update all code paths.

### 10.2 Strengthen `pro_decision.schema.json`

Make `next_experiment` schema match the regular decision schema. Currently it allows arbitrary properties; make it strict enough to produce executor-ready plans.

Required fields for `next_experiment`:

```text
experiment_id
objective
hypothesis
success_criteria
failure_criteria
tasks_for_codex
required_outputs
estimated_runtime_minutes
```

### 10.3 Strengthen `result.schema.json`

Add optional fields:

```json
{
  "runtime_seconds": { "type": ["number", "null"] },
  "resource_usage": { "type": "object" },
  "success_criteria_results": { "type": "array", "items": { "type": "string" } },
  "failure_criteria_results": { "type": "array", "items": { "type": "string" } },
  "metric_deltas": { "type": "object" },
  "decision_relevant_findings": { "type": "array", "items": { "type": "string" } }
}
```

Do not require these immediately for backward compatibility. Add them to prompts and new tests.

### 10.4 Strengthen `review.schema.json`

Add:

```json
{
  "evidence_quality": {
    "type": "string",
    "enum": ["strong", "medium", "weak", "invalid"]
  },
  "success_criteria_satisfied": { "type": "boolean" },
  "failure_criteria_triggered": { "type": "boolean" },
  "should_escalate_to_pro": { "type": "boolean" },
  "escalation_reason": { "type": ["string", "null"] }
}
```

---

## 11. Add deterministic metric ledger

Create `scripts/metrics_ledger.py`.

Output:

```text
research/<project>/progress/metric_ledger.json
research/<project>/progress/metric_ledger.md
```

The ledger should parse every `results/*_result.json` and summarize:

```json
{
  "iteration": "0007",
  "status": "completed",
  "claim_tested": "...",
  "review_verdict": "weak_pass",
  "allows_auto_continue": true,
  "important_metrics": {
    "safe_optimal_lucky_only.policy_regret": 0.504,
    "safe_optimal_lucky_only.q_overestimation": 0.625,
    "risk_optimal_matched.policy_regret": 0.0
  },
  "positive_signals": ["..."],
  "negative_signals": ["..."],
  "decision": "stop"
}
```

Initial generic extractor:

- recursively search metric dicts for scalar keys containing:
  - `regret`
  - `overestimation`
  - `mse`
  - `calibration`
  - `success`
  - `risky`
  - `positive`
  - `unsolved`
- include only compact scalar values in the ledger.

Add project-specific optional config:

```yaml
metrics:
  primary:
    - path: metrics.aggregate.best_positive_method
      direction: categorical
    - path: metrics.aggregate.generic_summaries.*.safe_optimal_lucky_policy_regret
      direction: minimize
    - path: metrics.aggregate.generic_summaries.*.risk_optimal_matched_policy_regret
      direction: minimize
  no_progress_metric_paths:
    - metrics.aggregate.any_positive_successor_evidence
```

Use ledger in Supervisor and Pro packets.

---

## 12. Add protected-file drift guard

Create `scripts/worktree_guard.py`.

Protected by default:

```text
scripts/autoresearcher.py
scripts/build_context.py
scripts/validate_artifacts.py
schemas/
prompts/
autoresearcher.yaml
AGENTS.md
```

During normal research execution, Executor may create/edit only:

```text
research/<project>/results/
research/<project>/artifacts/
research/<project>/packets/
research/<project>/setup_logs/
research/<project>/progress/
```

If the executor modifies protected files, pause unless:

```bash
--allow-orchestrator-edit
```

or config:

```yaml
safety:
  allow_executor_to_modify_orchestrator: false
```

Write drift report:

```text
research/<project>/decisions/NNNN_worktree_guard.json
research/<project>/decisions/NNNN_worktree_guard.md
```

---

## 13. Add resume and decision application commands

Commands:

```bash
python scripts/autoresearcher.py resume --project sto_trl --note "..."
python scripts/autoresearcher.py apply-pro-decision --project sto_trl
python scripts/autoresearcher.py stop --project sto_trl --note "..."
```

`resume` should:

- require a note;
- set `status=active`;
- set `human_review_required=false`;
- clear `pending_checkpoint`;
- commit state.

`apply-pro-decision` should:

- load latest valid `*_pro_decision.json`;
- if decision=`stop`, set `status=stopped`;
- if decision=`needs_human`, set `status=paused`;
- if decision=`continue` or `pivot` and `next_experiment` exists:
  - write/overwrite next `plan.json` and `plan.md`;
  - set `status=active`;
  - set `human_review_required=false`;
  - set `last_pro_review_iteration=state.iteration`;
  - continue to executor on next run.

---

## 14. Specific behavior for the current `sto_trl` stopped project

Use this as a regression test.

Current state:

```text
research/sto_trl/state.json says iteration=7, last_decision=stop, status=stopped.
research/sto_trl/decisions/0008_decision.json is the local Codex stop decision.
research/sto_trl/progress/latest_summary.md says the project should not be treated as solved and recommends a human choice among ending, reframing, keeping log-TRL only, or designing a principled uncertainty assumption.
```

After Phase 2 implementation, this command should work:

```bash
python scripts/autoresearcher.py build-pro-packet --project sto_trl --reason local_stop
```

It should create:

```text
research/sto_trl/pro_packets/0008_PRO_REVIEW_PACKET.md
```

The packet should ask GPT-5.5-Pro:

```text
Local Codex recommends stop. Do you agree?
Choose continue, pivot, stop, or needs_human.
If continue/pivot, propose exactly one small experiment under 30 minutes.
```

If ChatGPT Pro agrees with stop, `apply-pro-decision` should leave the project stopped.

If ChatGPT Pro recommends a pivot, it should produce a new plan for `0008` and resume the loop.

---

## 15. Tests to add

### 15.1 Unit tests

Add tests for:

```text
checkpoint due every 2 iterations
checkpoint due every 3 iterations
local stop triggers Pro escalation when enabled
local stop pauses with packet when Pro disabled
local pivot triggers Pro escalation
review weak_pass twice triggers escalation
result timeout triggers escalation
protected file drift triggers pause
metric ledger extracts scalar metrics
pro response fenced JSON parser works
pro decision schema validation fails on bad JSON
manual ingest saves decision and plan
resume clears paused state only with note
```

### 15.2 Fake ChatGPT Pro backend tests

Implement `FAKE_CHATGPT_PRO=1` or a fake backend class.

Fake outputs:

1. `continue` with next experiment.
2. `pivot` with next experiment.
3. `stop` with no next experiment.
4. `needs_human`.
5. blocker: `login_required`.
6. blocker: `browser_bridge_unavailable`.
7. malformed response.

### 15.3 Regression test for `sto_trl`

Create a test fixture copying enough of `research/sto_trl` to verify:

- stopped state can build Pro packet;
- `0008_decision.json` is included in packet;
- latest summary is included;
- source plan file is discovered;
- fake Pro `continue` writes `0008_plan.md` and resumes state;
- fake Pro `stop` keeps state stopped.

---

## 16. Implementation milestones

### Milestone A: Cleanup and tests around current Phase 1

- Factor backend logic out of `scripts/autoresearcher.py` where helpful.
- Add `checkpoint_policy.py`.
- Add `metrics_ledger.py`.
- Add `worktree_guard.py`.
- Keep all existing tests passing.

Acceptance:

```bash
pytest -q
python scripts/autoresearcher.py status --project sto_trl
```

### Milestone B: Pro packet and manual ingest

- Improve Pro packet builder.
- Add source doc discovery.
- Add `ingest-pro-response`.
- Add `apply-pro-decision`.
- Add `resume`.

Acceptance:

```bash
python scripts/autoresearcher.py build-pro-packet --project sto_trl --reason local_stop
python scripts/autoresearcher.py ingest-pro-response --project sto_trl --file tests/fixtures/fake_pro_continue.md
python scripts/autoresearcher.py apply-pro-decision --project sto_trl
```

### Milestone C: Automatic Pro checkpoint backend

- Implement `chatgpt_pro_bridge.py` using `codex-chatgpt-control` if available.
- Add fake backend tests.
- Add blocker handling.
- Do not require a real visible browser for tests.

Acceptance:

```bash
FAKE_CHATGPT_PRO=1 python scripts/autoresearcher.py pro-review --project sto_trl --reason local_stop
pytest -q tests/test_pro_bridge*.py
```

### Milestone D: Integrate Pro into main loop

- Modify local stop/pivot/needs_human paths to route through checkpoint policy.
- Add cadence reviews every 2-3 iterations.
- Apply Pro decisions to resume/stop/pivot.

Acceptance:

```bash
FAKE_CHATGPT_PRO=1 python scripts/autoresearcher.py run --project sto_trl --max-iters 1
```

Expected: if project is stopped and Pro fake says continue, it writes a plan and resumes; if Pro fake says stop, it confirms stopped.

### Milestone E: Real smoke test

Only after fake tests pass:

```bash
python scripts/autoresearcher.py pro-review --project sto_trl --reason local_stop
```

If no visible browser bridge is available, expected output is a structured blocker, not a crash.

---

## 17. ChatGPT Pro supervisor prompt

Create or update `prompts/chatgpt_pro_supervisor.md`:

```markdown
You are the GPT-5.5-Pro checkpoint supervisor for an automated research project.

You are consulted only at important gates: every 2-3 iterations, local stop/pivot/needs_human decisions, timeouts, ambiguous results, or before larger compute.

Your job:

1. Decide whether the project is making real progress toward the charter.
2. Choose exactly one: continue, pivot, stop, needs_human.
3. Be skeptical. Reward evidence, not activity.
4. Treat the repo packet as the source of truth. Same-thread context is helpful but not authoritative.
5. If continuing or pivoting, propose exactly one small experiment runnable within 30 minutes.
6. Do not approve OGBench, large neural training, large downloads, or expensive compute unless the packet proves tabular diagnostics justify it.
7. If local Codex recommended stop, explicitly say whether you agree or disagree and why.
8. If you disagree with local stop, provide a concrete next experiment with success/failure criteria.

Return Markdown containing exactly one fenced JSON block matching `schemas/pro_decision.schema.json`, followed by a concise explanation.
```

---

## 18. Do not overbuild

Do not build:

- web dashboard;
- database;
- GitHub Actions loop;
- hidden ChatGPT web automation;
- uncontrolled browser retries;
- autonomous large compute;
- automatic publication claims.

Keep the local loop boring, inspectable, and file-based.

---

## 19. Definition of done

The improvement is complete when:

1. Existing Phase 1 tests pass.
2. Pro packet includes charter, source docs, latest summary, local stop/pivot decision, result/review evidence, and metric ledger.
3. Local `stop`, `pivot`, and `needs_human` can trigger Pro checkpoint instead of immediately ending the project.
4. Pro checkpoint cadence works every 2-3 completed iterations.
5. Manual Pro ingest works without browser automation.
6. `codex-chatgpt-control` backend works when available or writes structured blockers when unavailable.
7. Same-thread ChatGPT mode uses configured `thread_url`.
8. Pro decisions are validated before being applied.
9. `resume` and `apply-pro-decision` commands work.
10. Protected-file drift is detected.
11. Metric ledger exists and is included in supervisor/Pro packets.
12. `sto_trl` stopped state can be handled by Pro checkpoint logic.

---

## 20. First instruction to Codex

Use this instruction to begin:

```markdown
Please improve the autoresearcher orchestration system using `autoresearcher_phase2_improvement_plan.md`.

Start with Milestone A and B only:

1. Add checkpoint policy, metric ledger, worktree guard, source-doc discovery, improved Pro packet builder, manual Pro response ingestion, apply-pro-decision, and resume.
2. Do not implement the live `codex-chatgpt-control` browser backend yet.
3. Add fake/manual tests and make `pytest -q` pass.
4. Use `research/sto_trl` as a regression fixture, but do not run new research experiments.
5. Stop after Milestone B and write a summary of changed files, tests run, and next steps for the live Pro backend.
```
