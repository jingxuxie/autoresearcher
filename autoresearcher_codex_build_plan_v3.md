# Autoresearcher Build Plan v3: Local Codex Role-Resume First, Optional ChatGPT-5.5-Pro Supervisor Later

## Purpose

Build a practical autoresearcher orchestration loop that can rapidly evaluate research ideas using small-scale experiments.

The first implementation must use **only local Codex CLI sessions**:

```text
Codex supervisor session  -> decides next experiment and writes plan
Codex executor session    -> implements/runs the experiment and writes result
Codex reviewer session    -> audits whether the result supports the claim
Python orchestrator       -> controls loop state, timeout, schemas, git commits, and push
```

After the Codex-only loop works, add an optional **ChatGPT-5.5-Pro supervision backend** every 2-3 iterations using `codex-chatgpt-control`.

The goal is not to build a fancy multi-agent framework. The goal is to build a reliable research loop that avoids wasting compute on vague, infinite, or self-congratulatory agent activity.

---

## Important design decisions

### 1. Use role-resume for local Codex

Use three separate resumed Codex sessions:

```text
supervisor session
executor session
reviewer session
```

Do **not** use one shared session for all roles. A single shared session risks role contamination: the executor may become too optimistic, the supervisor may inherit implementation details, and the reviewer may be less independent.

Role-resume gives us:

```text
- continuity inside each role
- less repeated context
- clearer separation of responsibilities
- easier debugging
```

The repo files remain the source of truth. Resume is helpful memory, not authoritative memory.

### 2. Still build compact context packets

Even with Codex resume, build compact context packets for each role. These packets should be automatically generated from repo files, so the user does not need to maintain context manually.

Why this is necessary:

```text
- resumed sessions can drift
- old hidden context can become stale
- repo files are auditable
- the same packet can be used for ChatGPT-5.5-Pro review later
- fresh-mode fallback becomes possible
```

Context packet does **not** need to be huge. It should include:

```text
- charter.md
- state.json
- latest plan
- latest result.json
- latest summary.md
- latest review.json
- last 2-3 decisions/results/reviews
- current requested action
```

### 3. Use ChatGPT-5.5-Pro only as optional escalation

Phase 2 should add ChatGPT-5.5-Pro supervision every 2-3 iterations, but the default loop must remain Codex-only.

Use ChatGPT Pro review for:

```text
- project start / initial research plan review
- every 2 or 3 completed iterations
- pivot decisions
- stop decisions
- ambiguous reviewer verdicts
- before expensive runs
- before declaring an idea promising
```

Do not depend on ChatGPT web for every iteration.

### 4. The orchestrator commits and pushes, not the agents

Agents should write outputs, but the Python orchestrator validates them first.

Only after validation should the orchestrator run:

```bash
git add ...
git commit -m "..."
git push
```

This gives GitHub history while avoiding accidental commits of broken, unrelated, or dangerous files.

### 5. Hard timeout for executor

Each executor run must have a hard wall-clock timeout, default:

```text
30 minutes
```

If the executor exceeds the timeout:

```text
- kill the entire process tree
- write a timeout result JSON
- commit the timeout result
- pause or return to supervisor depending on config
```

Research prototyping should be small-scale. Long-running experiments are usually a sign that the plan is not suitable for the autoresearcher loop.

### 6. Use GPT-5.5 + xhigh reasoning for Codex roles

Default local Codex config:

```text
model: gpt-5.5
model_reasoning_effort: xhigh
```

If the installed Codex model catalog does not expose `gpt-5.5` or does not support `xhigh`, fail clearly with an actionable message.

Do not silently fall back to a weaker model unless the user explicitly configures fallback behavior.

---

## Phase 1: Build Codex-only autoresearcher loop

### Target command

The user should be able to run:

```bash
python scripts/autoresearcher.py run --project project_001 --max-iters 1
```

or:

```bash
python scripts/autoresearcher.py run --project project_001 --max-iters 5
```

The loop should stop automatically on:

```text
- timeout
- missing/invalid result
- reviewer fail
- pivot proposal
- stop proposal
- needs_human
- max iterations
- no-progress limit
```

---

## Required repository structure

Create this structure:

```text
.
├── AGENTS.md
├── autoresearcher.yaml
├── prompts/
│   ├── supervisor.md
│   ├── executor.md
│   ├── reviewer.md
│   └── chatgpt_pro_supervisor.md
├── schemas/
│   ├── decision.schema.json
│   ├── result.schema.json
│   ├── review.schema.json
│   └── pro_decision.schema.json
├── scripts/
│   ├── autoresearcher.py
│   ├── build_context.py
│   ├── validate_artifacts.py
│   └── kill_process_tree.py
├── research/
│   └── project_001/
│       ├── charter.md
│       ├── state.json
│       ├── plans/
│       ├── results/
│       ├── reviews/
│       ├── decisions/
│       ├── packets/
│       └── artifacts/
└── .gitignore
```

Add to `.gitignore`:

```gitignore
.autoresearcher/
__pycache__/
*.pyc
.env
```

Use `.autoresearcher/local_state.json` for local role session IDs and other non-committed runtime details.

Do **not** commit Codex auth files or local ChatGPT bridge state.

---

## `autoresearcher.yaml`

Create:

```yaml
project_default: project_001

codex:
  model: gpt-5.5
  reasoning_effort: xhigh
  resume_mode: role-resume
  fail_if_model_unavailable: true

roles:
  supervisor:
    sandbox: read-only
    output_schema: schemas/decision.schema.json
    timeout_minutes: 15

  executor:
    sandbox: workspace-write
    output_schema: null
    timeout_minutes: 30

  reviewer:
    sandbox: read-only
    output_schema: schemas/review.schema.json
    timeout_minutes: 15

loop:
  max_iterations: 12
  max_no_progress_rounds: 3
  require_human_for_pivot: true
  require_human_for_expensive_run: true
  require_human_for_publishable_claim: true
  stop_on_missing_result: true
  stop_on_invalid_schema: true
  stop_on_timeout: true

git:
  enabled: true
  commit: true
  push: false
  remote: origin
  branch: null

chatgpt_pro:
  enabled: false
  backend: codex-chatgpt-control
  cadence_iterations: 3
  allow_cadence_2_or_3: true
  thread_url: null
  existing_tab: true
  require_visible_session: true
  require_user_approved_prompt: true
  require_model: GPT-5.5 Pro
  require_thinking: Heavy
  fail_if_unavailable: true
  max_retries: 0
```

Notes:

```text
- Phase 1 must work with chatgpt_pro.enabled=false.
- Phase 2 adds chatgpt_pro.enabled=true support.
- Push defaults to false for safety; user can enable it.
```

---

## Local state file

Create `.autoresearcher/local_state.json` automatically:

```json
{
  "projects": {
    "project_001": {
      "codex_sessions": {
        "supervisor": {
          "session_id": null,
          "last_used_at": null
        },
        "executor": {
          "session_id": null,
          "last_used_at": null
        },
        "reviewer": {
          "session_id": null,
          "last_used_at": null
        }
      },
      "chatgpt_pro": {
        "thread_url": null,
        "last_review_iteration": 0
      }
    }
  }
}
```

This file is local and should not be committed.

---

## Project state file

Create `research/project_001/state.json`:

```json
{
  "iteration": 0,
  "status": "active",
  "last_decision": "start",
  "primary_metric": null,
  "best_primary_metric": null,
  "no_progress_rounds": 0,
  "human_review_required": false,
  "last_pro_review_iteration": 0,
  "notes": []
}
```

This file **should** be committed because it is part of the research ledger.

---

## `AGENTS.md`

Create:

```markdown
# AGENTS.md

This repository is controlled by an autoresearcher loop.

Hard rules for all Codex sessions:

1. Do not change the research goal unless the task explicitly asks for a pivot proposal.
2. Do not delete previous experiment plans, results, reviews, decisions, or artifacts.
3. Every experiment must be small-scale and suitable for fast validation.
4. The executor must finish within the configured timeout, normally 30 minutes.
5. Every experiment must produce:
   - `research/<project>/results/NNNN_result.json`
   - `research/<project>/results/NNNN_summary.md`
   - artifacts under `research/<project>/artifacts/NNNN/` when applicable
6. Every result must include exact commands run.
7. Negative results are valuable. Do not hide failures.
8. Do not claim success unless the predeclared success criteria are satisfied.
9. Do not install large dependencies, download large datasets, or run expensive training without explicit human approval.
10. Prefer small, decisive experiments over broad exploration.
11. For numerical claims, save raw metrics, not just prose.
12. Do not edit `scripts/autoresearcher.py`, schemas, or this file unless explicitly instructed.
```

---

## Supervisor role

### Purpose

Before each experiment, the supervisor decides:

```text
continue | pivot | stop | needs_human
```

If continuing, it proposes exactly one small experiment.

### Sandbox

Use:

```bash
--sandbox read-only
```

The supervisor does not directly write code or mutate experiment artifacts. It returns structured JSON. The orchestrator then writes `decision.json`, `decision.md`, and `plan.md`.

### Prompt file: `prompts/supervisor.md`

```markdown
You are SUPERVISOR_CODEX in an automated research loop.

You are deciding what experiment should be run next.

You may inspect the repository, but you must not edit files or run long experiments.

Be skeptical:
- Reward evidence, not activity.
- Use the project charter and result JSON as the source of truth.
- Treat executor summaries as claims to verify, not facts.
- Prefer one small decisive experiment over vague exploration.
- If latest result JSON is missing, invalid, incomplete, or unsupported by artifacts, choose needs_human.
- If the latest result does not test the main hypothesis, choose needs_human or stop.
- If proposing a next experiment, make it small enough to complete within 30 minutes.

Decision policy:
- continue: evidence suggests progress or there is a high-information cheap next test.
- pivot: current evidence weakens the original idea but reveals a nearby testable idea.
- stop: repeated negative, invalid, unreproducible, or low-value results.
- needs_human: ambiguous interpretation, expensive compute, subjective taste, missing artifacts, or risky pivot.

Return JSON only matching `schemas/decision.schema.json`.
```

---

## Executor role

### Purpose

The executor implements and runs one experiment from the plan.

### Sandbox

Use:

```bash
--sandbox workspace-write
```

### Hard timeout

The orchestrator must enforce the executor timeout externally.

Default:

```text
30 minutes
```

The executor prompt should mention the timeout, but the timeout must be enforced by Python, not by prompt compliance.

### Prompt file: `prompts/executor.md`

```markdown
You are EXECUTOR_CODEX in an automated research loop.

Follow the supplied experiment plan exactly.

Rules:
- Implement the smallest code change needed to test the hypothesis.
- Run the baseline under comparable conditions when applicable.
- Run only small-scale experiments suitable for quick validation.
- Do not run anything expected to exceed the configured timeout.
- Save exact commands run.
- Save raw metrics.
- Save artifacts.
- Write a machine-readable result JSON matching `schemas/result.schema.json`.
- Write a human-readable summary Markdown.
- Do not delete previous results.
- Do not change the research goal.
- If the plan is impossible, write a failed result JSON explaining why.

Required paths:
- `research/<project>/results/NNNN_result.json`
- `research/<project>/results/NNNN_summary.md`
- `research/<project>/artifacts/NNNN/`
```

---

## Reviewer role

### Purpose

After execution, the reviewer audits whether the result supports the executor's interpretation.

The reviewer answers:

```text
pass | weak_pass | fail | needs_human
```

The reviewer should catch:

```text
- missing artifacts
- unfair baseline comparison
- cherry-picked metrics
- failure to satisfy success criteria
- data leakage
- broken benchmark
- invalid or missing commands
- optimistic interpretation
```

### Sandbox

Use:

```bash
--sandbox read-only
```

### Prompt file: `prompts/reviewer.md`

```markdown
You are REVIEWER_CODEX in an automated research loop.

You audit the latest experiment.

You may inspect files and artifacts, but you must not edit files.

Check:
- Did the executor actually produce the required files?
- Are baseline and proposed method compared fairly?
- Are success criteria satisfied?
- Are failure criteria triggered?
- Are metrics cherry-picked?
- Are artifacts present and relevant?
- Is the interpretation too optimistic?
- Is there any data leakage, seed issue, broken benchmark, or invalid comparison?
- Should the supervisor be allowed to continue automatically?

Return JSON only matching `schemas/review.schema.json`.
```

---

## Schemas

### `schemas/decision.schema.json`

```json
{
  "type": "object",
  "properties": {
    "decision": {
      "type": "string",
      "enum": ["continue", "pivot", "stop", "needs_human"]
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    },
    "progress_score": {
      "type": "integer",
      "minimum": 0,
      "maximum": 10
    },
    "rationale": {
      "type": "string"
    },
    "evidence": {
      "type": "array",
      "items": { "type": "string" }
    },
    "risks": {
      "type": "array",
      "items": { "type": "string" }
    },
    "next_experiment": {
      "type": ["object", "null"],
      "properties": {
        "experiment_id": { "type": "string" },
        "objective": { "type": "string" },
        "hypothesis": { "type": "string" },
        "success_criteria": {
          "type": "array",
          "items": { "type": "string" }
        },
        "failure_criteria": {
          "type": "array",
          "items": { "type": "string" }
        },
        "tasks_for_codex": {
          "type": "array",
          "items": { "type": "string" }
        },
        "required_outputs": {
          "type": "array",
          "items": { "type": "string" }
        },
        "estimated_runtime_minutes": {
          "type": "integer",
          "minimum": 1,
          "maximum": 30
        }
      },
      "required": [
        "experiment_id",
        "objective",
        "hypothesis",
        "success_criteria",
        "failure_criteria",
        "tasks_for_codex",
        "required_outputs",
        "estimated_runtime_minutes"
      ],
      "additionalProperties": false
    }
  },
  "required": [
    "decision",
    "confidence",
    "progress_score",
    "rationale",
    "evidence",
    "risks",
    "next_experiment"
  ],
  "additionalProperties": false
}
```

### `schemas/result.schema.json`

```json
{
  "type": "object",
  "properties": {
    "experiment_id": { "type": "string" },
    "status": {
      "type": "string",
      "enum": ["completed", "failed", "blocked", "timeout"]
    },
    "claim_tested": { "type": "string" },
    "commands_run": {
      "type": "array",
      "items": { "type": "string" }
    },
    "metrics": {
      "type": "object",
      "additionalProperties": true
    },
    "baseline_metrics": {
      "type": "object",
      "additionalProperties": true
    },
    "artifacts": {
      "type": "array",
      "items": { "type": "string" }
    },
    "interpretation": { "type": "string" },
    "known_failures": {
      "type": "array",
      "items": { "type": "string" }
    },
    "next_questions": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": [
    "experiment_id",
    "status",
    "claim_tested",
    "commands_run",
    "metrics",
    "baseline_metrics",
    "artifacts",
    "interpretation",
    "known_failures",
    "next_questions"
  ],
  "additionalProperties": false
}
```

### `schemas/review.schema.json`

```json
{
  "type": "object",
  "properties": {
    "experiment_id": { "type": "string" },
    "verdict": {
      "type": "string",
      "enum": ["pass", "weak_pass", "fail", "needs_human"]
    },
    "allows_auto_continue": {
      "type": "boolean"
    },
    "reasons": {
      "type": "array",
      "items": { "type": "string" }
    },
    "evidence_checked": {
      "type": "array",
      "items": { "type": "string" }
    },
    "required_fixes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "risk_flags": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": [
    "experiment_id",
    "verdict",
    "allows_auto_continue",
    "reasons",
    "evidence_checked",
    "required_fixes",
    "risk_flags"
  ],
  "additionalProperties": false
}
```

---

## Codex runner implementation

Implement a Python class:

```python
class CodexRunner:
    def run_role(
        self,
        project: str,
        role: str,
        prompt: str,
        output_path: Path,
        schema_path: Path | None,
        sandbox: str,
        timeout_minutes: int,
        resume: bool = True,
    ) -> CodexRunResult:
        ...
```

### Required behavior

For the first run of a role:

```bash
codex exec \
  --cd <repo_root> \
  --json \
  --model gpt-5.5 \
  -c model_reasoning_effort=xhigh \
  --sandbox <sandbox> \
  --output-last-message <output_path> \
  [--output-schema <schema_path>] \
  -
```

Prompt is passed through stdin.

Parse JSONL stdout. On `thread.started`, capture `thread_id` and store it in `.autoresearcher/local_state.json`.

For subsequent runs of that role:

```bash
codex exec resume <SESSION_ID> \
  --cd <repo_root> \
  --json \
  --model gpt-5.5 \
  -c model_reasoning_effort=xhigh \
  --sandbox <sandbox> \
  --output-last-message <output_path> \
  [--output-schema <schema_path>] \
  -
```

If this exact CLI ordering does not work with the installed Codex version, inspect `codex exec --help` and implement the equivalent valid command.

Required fields in `CodexRunResult`:

```python
@dataclass
class CodexRunResult:
    role: str
    session_id: str | None
    output_path: Path
    jsonl_log_path: Path
    return_code: int
    timed_out: bool
    stdout_tail: str
    stderr_tail: str
```

### Important

Do not use:

```bash
--dangerously-bypass-approvals-and-sandbox
```

Do not use:

```bash
--sandbox danger-full-access
```

unless the user explicitly enables this in config and the orchestrator prints a warning.

---

## Timeout implementation

Use Python process groups so child experiment processes are killed too.

Implementation requirements:

```text
- start subprocess in a new process group/session
- on timeout, terminate process group
- after grace period, kill process group
- write timeout result JSON if executor timed out
```

Pseudocode:

```python
proc = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    start_new_session=True,
)

try:
    stdout, stderr = proc.communicate(input=prompt, timeout=timeout_seconds)
except subprocess.TimeoutExpired:
    os.killpg(proc.pid, signal.SIGTERM)
    try:
        stdout, stderr = proc.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        stdout, stderr = proc.communicate()
    timed_out = True
```

If executor timeout occurs, write:

```json
{
  "experiment_id": "NNNN",
  "status": "timeout",
  "claim_tested": "Executor timed out before completing the experiment.",
  "commands_run": [],
  "metrics": {},
  "baseline_metrics": {},
  "artifacts": [],
  "interpretation": "The executor exceeded the configured timeout. Treat this as a failed or blocked small-scale experiment.",
  "known_failures": ["Executor timeout"],
  "next_questions": ["Can the experiment be reduced to a smaller validation?"]
}
```

---

## Context builder

Implement:

```bash
python scripts/build_context.py --project project_001 --role supervisor
python scripts/build_context.py --project project_001 --role executor --plan research/project_001/plans/0001_plan.md
python scripts/build_context.py --project project_001 --role reviewer
python scripts/build_context.py --project project_001 --role chatgpt_pro
```

The context builder should output Markdown.

### Supervisor context should include

```text
- project charter
- current state
- latest result JSON
- latest summary
- latest review
- last 2-3 decisions
- stop/pivot/continue rules
```

### Executor context should include

```text
- current experiment plan
- result schema
- required output paths
- timeout warning
- relevant existing code pointers if known
```

### Reviewer context should include

```text
- latest plan
- latest result JSON
- latest summary
- artifact paths
- success/failure criteria
```

### ChatGPT Pro context should include

```text
- compact project charter
- current state
- last 2-3 iterations
- latest result and review
- explicit question: continue/pivot/stop/needs_human?
- required output JSON schema
```

---

## Plan generation

When supervisor returns `decision=continue`, orchestrator writes:

```text
research/<project>/decisions/NNNN_decision.json
research/<project>/decisions/NNNN_decision.md
research/<project>/plans/NNNN_plan.json
research/<project>/plans/NNNN_plan.md
```

The plan Markdown should be executor-ready:

```markdown
# Experiment NNNN

## Objective

...

## Hypothesis

...

## Success criteria

- ...

## Failure criteria

- ...

## Estimated runtime

<= 30 minutes

## Tasks for Codex

- ...

## Required outputs

- `research/<project>/results/NNNN_result.json`
- `research/<project>/results/NNNN_summary.md`
- `research/<project>/artifacts/NNNN/`
```

---

## Orchestrator loop

Implement command:

```bash
python scripts/autoresearcher.py run --project project_001 --max-iters 5
```

Loop:

```text
1. Load config and project state.
2. Check model availability with `codex debug models`.
3. Stop if project status is not active.
4. Stop if human_review_required is true.
5. Stop if max_iterations reached.
6. Decide whether to use local Codex supervisor or ChatGPT Pro supervisor.
7. Build supervisor context.
8. Run supervisor.
9. Validate decision JSON.
10. If decision is pivot/stop/needs_human, write/commit/push and pause.
11. If decision is continue, write plan.
12. Run executor with 30-minute hard timeout.
13. Validate result JSON and artifact paths.
14. Run reviewer.
15. Validate review JSON.
16. Update state.
17. Commit and optionally push.
18. Repeat until max-iters or stop condition.
```

---

## State update policy

Increment `iteration` only after executor produces a valid result or timeout result.

Update `no_progress_rounds` using simple deterministic logic where possible.

Initial deterministic rule:

```text
If reviewer verdict is pass or weak_pass and supervisor progress_score >= 5:
    no_progress_rounds = 0
else:
    no_progress_rounds += 1
```

Later, add project-specific metric comparison.

Stop if:

```text
no_progress_rounds >= max_no_progress_rounds
```

---

## Git policy

After each valid stage, commit:

```text
supervisor decision committed after decision validation
plan committed after plan generation
executor result committed after result validation or timeout result creation
review committed after review validation
state committed after state update
```

Suggested messages:

```bash
autoresearcher(project_001): decision 0001
autoresearcher(project_001): plan 0001
autoresearcher(project_001): result 0001
autoresearcher(project_001): review 0001
autoresearcher(project_001): state after 0001
```

Push only if `git.push=true`.

If push fails, do not retry forever. Save blocker:

```text
research/<project>/decisions/NNNN_git_push_blocker.md
```

---

## Phase 2: Add ChatGPT-5.5-Pro supervisor backend

### Tool

Use:

```text
https://github.com/adamallcock/codex-chatgpt-control
```

Only use it for visible, user-directed ChatGPT web consultation.

### Key behavior

It should send a prompt to an existing visible ChatGPT thread when `chatgpt_pro.thread_url` is configured.

Use thread URL mode:

```javascript
await chatgpt.askInThread({
  thread: { type: "url", url: "<chatgpt conversation url>" },
  existingTab: true,
  prompt: packet,
  wait: true,
  read: { format: "markdown" }
});
```

### Answer to the user's context question

Yes, this can continue the same ChatGPT thread by URL, so it is similar to "resume" at the ChatGPT web-thread level.

However, still generate and send a compact `PRO_REVIEW_PACKET.md` each time.

Reason:

```text
- ChatGPT thread memory is not a reliable database.
- The visible thread can drift or contain stale assumptions.
- Context windows can truncate old details.
- The model may not inspect the repo unless the relevant facts are included.
- The repo packet makes the review reproducible and auditable.
```

The context builder should be automatic, so this is not inconvenient for the user.

### Pro cadence

Trigger Pro review when:

```text
- chatgpt_pro.enabled = true
- completed_iterations_since_last_pro_review >= chatgpt_pro.cadence_iterations
```

Default:

```text
cadence_iterations: 3
```

Allow user to set:

```text
cadence_iterations: 2
```

Also trigger Pro review immediately when:

```text
- supervisor proposes pivot
- supervisor proposes stop
- reviewer verdict is fail or needs_human
- latest result is ambiguous
- expensive run requested
- before the project is marked promising
```

### Pro packet path

Write:

```text
research/<project>/packets/NNNN_PRO_REVIEW_PACKET.md
```

### Pro decision output paths

Write:

```text
research/<project>/decisions/NNNN_pro_raw.md
research/<project>/decisions/NNNN_pro_decision.json
research/<project>/decisions/NNNN_pro_decision.md
```

### Pro supervisor prompt

Create `prompts/chatgpt_pro_supervisor.md`:

```markdown
You are the external high-stakes research supervisor for this autoresearcher project.

Your job:
1. Decide whether the project is making real progress.
2. Choose exactly one: continue, pivot, stop, needs_human.
3. Be skeptical. Reward evidence, not activity.
4. Prefer small decisive experiments.
5. Do not propose expensive runs unless clearly justified.
6. If continuing, propose exactly one next experiment that should complete within 30 minutes.
7. If the evidence is ambiguous, choose needs_human.

Return:
1. A concise Markdown rationale.
2. A fenced JSON block matching the required schema.

Do not rely only on previous thread memory. Use the packet below as the source of truth.
```

### Pro blocker behavior

If ChatGPT bridge fails due to any of the following:

```text
- browser_bridge_unavailable
- login_required
- captcha
- rate_limit
- permission
- selector_drift
- upload_failed
- model_unavailable
- thread_unavailable
- user_approval_required
```

then:

```text
- do not blindly retry
- save blocker JSON/Markdown
- commit blocker
- set human_review_required=true
- stop loop
```

### Pro model selection

Try to require:

```text
model: GPT-5.5 Pro
thinking: Heavy
```

If the UI or bridge cannot guarantee model/thinking selection, save a warning in the raw Pro decision metadata.

Do not silently accept a different model unless config says:

```yaml
chatgpt_pro:
  allow_model_fallback: true
```

Default:

```yaml
allow_model_fallback: false
```

---

## Phase 2 implementation plan

Do not implement Phase 2 until Phase 1 tests pass.

Add:

```text
scripts/chatgpt_pro_bridge.py
scripts/build_pro_packet.py
```

or implement them as subcommands:

```bash
python scripts/autoresearcher.py build-pro-packet --project project_001
python scripts/autoresearcher.py pro-review --project project_001
```

### Expected user flow for first Pro test

1. User opens ChatGPT in Chrome.
2. User opens or creates a GPT-5.5-Pro thread.
3. User copies the thread URL into `autoresearcher.yaml`:

```yaml
chatgpt_pro:
  enabled: true
  thread_url: "https://chatgpt.com/c/..."
  cadence_iterations: 3
```

4. User runs:

```bash
python scripts/autoresearcher.py pro-smoke --project project_001
```

5. System sends a tiny safe prompt:

```text
Reply with JSON: {"ok": true, "purpose": "autoresearcher smoke test"}
```

6. System saves response and reports success/failure.

Only after smoke test passes should the loop use Pro supervision.

---

## Tests

Implement tests with mocked Codex calls first.

Use:

```bash
python -m unittest discover tests
```

or `pytest` if the repo already uses it.

Required tests:

```text
1. Context builder includes charter, state, latest result, latest review.
2. CodexRunner fresh run parses `thread.started` session ID from JSONL.
3. CodexRunner role-resume uses stored role session ID.
4. Supervisor decision JSON validates.
5. Plan Markdown is generated correctly.
6. Executor timeout writes timeout result JSON.
7. Timeout kills child process.
8. Reviewer fail sets human_review_required=true.
9. Missing result sets human_review_required=true.
10. Git commit is skipped gracefully when there are no changes.
11. Pro cadence triggers every 3 iterations by default.
12. Pro cadence can be configured to 2.
13. Pro bridge blocker pauses loop and writes blocker.
14. Phase 1 runs with chatgpt_pro.enabled=false and no Pro dependencies installed.
```

---

## Smoke tests

### Smoke test 1: null project

Create a toy project where no improvement should be possible.

Expected:

```text
- executor runs a tiny experiment
- reviewer catches no real progress
- loop stops or asks human within 1-3 iterations
```

### Smoke test 2: positive-control project

Create a toy project with a known bug or easy improvement.

Expected:

```text
- executor fixes/evaluates it
- metrics improve
- reviewer passes
- supervisor proposes validation, not random exploration
```

### Smoke test 3: timeout project

Create an experiment plan that sleeps for longer than the timeout.

Expected:

```text
- executor process is killed
- timeout result JSON is written
- state is updated
- loop stops
```

---

## CLI commands to implement

```bash
python scripts/autoresearcher.py init --project project_001
python scripts/autoresearcher.py run --project project_001 --max-iters 1
python scripts/autoresearcher.py run --project project_001 --max-iters 5
python scripts/autoresearcher.py build-context --project project_001 --role supervisor
python scripts/autoresearcher.py reset-role-session --project project_001 --role supervisor
python scripts/autoresearcher.py reset-role-session --project project_001 --role executor
python scripts/autoresearcher.py reset-role-session --project project_001 --role reviewer
python scripts/autoresearcher.py status --project project_001
python scripts/autoresearcher.py pro-smoke --project project_001
python scripts/autoresearcher.py build-pro-packet --project project_001
```

---

## Acceptance criteria for Phase 1

Phase 1 is done when:

```text
- `init` creates repo structure and default files.
- `run --max-iters 1` successfully executes supervisor -> executor -> reviewer.
- Role session IDs are captured and reused.
- Executor timeout is enforced.
- Invalid/missing results stop the loop.
- JSON schemas are validated.
- Git commits are created after validated steps.
- The loop can run 3 iterations on a toy project without manual intervention.
- A timeout toy project is stopped cleanly.
- The system works with `chatgpt_pro.enabled=false`.
```

---

## Acceptance criteria for Phase 2

Phase 2 is done when:

```text
- `pro-smoke` can send a visible prompt to an existing ChatGPT thread.
- It can reuse the configured thread URL.
- It saves raw Pro response.
- It extracts a decision JSON block.
- It validates Pro decision JSON.
- It triggers Pro review every 2 or 3 iterations according to config.
- It triggers Pro review on pivot/stop/ambiguous decisions.
- It writes blockers and pauses on bridge/login/captcha/rate-limit/permission errors.
- Codex-only mode still works if Pro bridge is disabled or not installed.
```

---

## Recommended build order for Codex

Implement in this order:

```text
1. Repo structure + config loader.
2. Context builder.
3. JSON schema validation.
4. CodexRunner fresh mode.
5. CodexRunner role-resume mode.
6. Supervisor decision -> plan writer.
7. Executor runner with 30-minute timeout.
8. Timeout result writer.
9. Reviewer runner.
10. State updater.
11. Git commit/push wrapper.
12. Phase 1 tests and toy smoke projects.
13. ChatGPT Pro packet builder.
14. ChatGPT Pro smoke test.
15. ChatGPT Pro supervisor backend.
16. Pro cadence and escalation logic.
17. Phase 2 tests.
```

Do not start Phase 2 until Phase 1 is reliable.

---

## Final implementation principle

The model can suggest and execute experiments, but the deterministic orchestrator must control:

```text
- loop state
- role separation
- timeout
- schema validation
- artifact checks
- git commits
- stopping rules
- Pro escalation cadence
```

This is what prevents the autoresearcher from becoming an expensive loop that only produces plausible summaries.
