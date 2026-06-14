"""Build compact deterministic metric ledgers from autoresearcher results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


INTERESTING_TOKENS = (
    "best",
    "calibration",
    "exact",
    "improvement",
    "mse",
    "overestimation",
    "overoptimism",
    "positive",
    "regret",
    "risk",
    "risky",
    "success",
    "unsolved",
)


def project_dir(repo_root: Path, project: str) -> Path:
    return repo_root / "research" / project


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def iteration_from_name(path: Path) -> Optional[str]:
    head = path.name.split("_", 1)[0]
    if len(head) == 4 and head.isdigit():
        return head
    return None


def is_interesting_key(key: str) -> bool:
    lowered = key.lower()
    return any(token in lowered for token in INTERESTING_TOKENS)


def iter_interesting_scalars(value: Any, prefix: str = "") -> Iterable[Tuple[str, Any]]:
    if isinstance(value, (int, float, bool)) or value is None:
        if prefix and is_interesting_key(prefix):
            yield prefix, value
        return
    if isinstance(value, str):
        if prefix and is_interesting_key(prefix) and len(value) <= 160:
            yield prefix, value
        return
    if isinstance(value, list):
        for index, item in enumerate(value[:20]):
            child_prefix = f"{prefix}.{index}" if prefix else str(index)
            yield from iter_interesting_scalars(item, child_prefix)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            yield from iter_interesting_scalars(item, child_prefix)


def compact_text_list(items: Any, limit: int = 4) -> List[str]:
    if not isinstance(items, list):
        return []
    output: List[str] = []
    for item in items[:limit]:
        if not isinstance(item, str):
            continue
        text = " ".join(item.split())
        if len(text) > 220:
            text = text[:220].rstrip() + "..."
        output.append(text)
    return output


def infer_signals(result: Dict[str, Any], review: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    positives: List[str] = []
    negatives: List[str] = []

    for item in compact_text_list(result.get("decision_relevant_findings", [])):
        target = negatives if any(token in item.lower() for token in ("fail", "risk", "not ", "unsolved", "negative")) else positives
        target.append(item)

    interpretation = result.get("interpretation")
    if isinstance(interpretation, str) and interpretation:
        positives.append(" ".join(interpretation.split())[:260])

    for item in compact_text_list(result.get("known_failures", [])):
        negatives.append(item)
    for item in compact_text_list(review.get("risk_flags", [])):
        negatives.append(item)
    for item in compact_text_list(review.get("required_fixes", [])):
        negatives.append(item)

    return positives[:5], negatives[:5]


def build_metric_ledger(repo_root: Path, project: str) -> Dict[str, Any]:
    root = project_dir(repo_root, project)
    rows: List[Dict[str, Any]] = []
    for result_path in sorted((root / "results").glob("*_result.json")):
        iteration = iteration_from_name(result_path)
        if not iteration:
            continue
        result = load_json(result_path)
        if not isinstance(result, dict):
            continue
        review = load_json(root / "reviews" / f"{iteration}_review.json")
        if not isinstance(review, dict):
            review = {}
        decision = load_json(root / "decisions" / f"{iteration}_decision.json")
        if not isinstance(decision, dict):
            decision = {}

        metrics: Dict[str, Any] = {}
        for key, value in iter_interesting_scalars({"metrics": result.get("metrics", {}), "baseline_metrics": result.get("baseline_metrics", {})}):
            if len(metrics) >= 12:
                break
            metrics[key] = value

        positives, negatives = infer_signals(result, review)
        rows.append(
            {
                "iteration": iteration,
                "status": result.get("status"),
                "claim_tested": result.get("claim_tested"),
                "review_verdict": review.get("verdict"),
                "allows_auto_continue": review.get("allows_auto_continue"),
                "decision": decision.get("decision"),
                "important_metrics": metrics,
                "positive_signals": positives,
                "negative_signals": negatives,
            }
        )

    return {"project": project, "iterations": rows}


def ledger_markdown(ledger: Dict[str, Any]) -> str:
    lines = [
        f"# Metric Ledger: {ledger.get('project')}",
        "",
        "| Iteration | Status | Review | Decision | Key metrics |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in ledger.get("iterations", []):
        metrics = row.get("important_metrics", {})
        if isinstance(metrics, dict) and metrics:
            metric_bits = [f"`{key}`={value}" for key, value in list(metrics.items())[:5]]
            metric_text = "<br>".join(metric_bits)
        else:
            metric_text = "_None extracted_"
        lines.append(
            "| {iteration} | {status} | {review} | {decision} | {metrics} |".format(
                iteration=row.get("iteration"),
                status=row.get("status"),
                review=row.get("review_verdict"),
                decision=row.get("decision"),
                metrics=metric_text,
            )
        )

    lines.extend(["", "## Positive Signals", ""])
    for row in ledger.get("iterations", []):
        for signal in row.get("positive_signals", [])[:3]:
            lines.append(f"- `{row.get('iteration')}`: {signal}")
    lines.extend(["", "## Negative Signals", ""])
    for row in ledger.get("iterations", []):
        for signal in row.get("negative_signals", [])[:3]:
            lines.append(f"- `{row.get('iteration')}`: {signal}")
    return "\n".join(lines).rstrip() + "\n"


def write_metric_ledger(repo_root: Path, project: str) -> Tuple[Path, Path]:
    root = project_dir(repo_root, project) / "progress"
    root.mkdir(parents=True, exist_ok=True)
    ledger = build_metric_ledger(repo_root, project)
    json_path = root / "metric_ledger.json"
    md_path = root / "metric_ledger.md"
    json_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
    md_path.write_text(ledger_markdown(ledger))
    return json_path, md_path


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Write an autoresearcher metric ledger.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--project", required=True)
    args = parser.parse_args()
    json_path, md_path = write_metric_ledger(args.repo_root.resolve(), args.project)
    print(json_path)
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
