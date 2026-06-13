#!/usr/bin/env python3
"""Validate autoresearcher JSON artifacts and declared artifact paths."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class ValidationError(Exception):
    """Raised when an artifact does not satisfy deterministic checks."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise ValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {path}: {exc}") from exc


def _type_matches(value: Any, expected: Any) -> bool:
    if isinstance(expected, list):
        return any(_type_matches(value, item) for item in expected)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _validate_fallback(instance: Any, schema: Dict[str, Any], path: str = "$") -> None:
    expected_type = schema.get("type")
    if expected_type is not None and not _type_matches(instance, expected_type):
        raise ValidationError(f"{path}: expected type {expected_type}, got {type(instance).__name__}")

    if "enum" in schema and instance not in schema["enum"]:
        raise ValidationError(f"{path}: expected one of {schema['enum']}, got {instance!r}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise ValidationError(f"{path}: expected >= {schema['minimum']}, got {instance}")
        if "maximum" in schema and instance > schema["maximum"]:
            raise ValidationError(f"{path}: expected <= {schema['maximum']}, got {instance}")

    if isinstance(instance, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                raise ValidationError(f"{path}: missing required key {key!r}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = sorted(set(instance) - set(properties))
            if extra:
                raise ValidationError(f"{path}: unexpected keys {extra}")

        for key, value in instance.items():
            subschema = properties.get(key)
            if subschema:
                _validate_fallback(value, subschema, f"{path}.{key}")

    if isinstance(instance, list) and "items" in schema:
        for idx, item in enumerate(instance):
            _validate_fallback(item, schema["items"], f"{path}[{idx}]")


def validate_json_schema(instance_path: Path, schema_path: Path) -> None:
    instance = load_json(instance_path)
    schema = load_json(schema_path)
    try:
        import jsonschema  # type: ignore

        jsonschema.Draft7Validator.check_schema(schema)
        validator = jsonschema.Draft7Validator(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))
        if errors:
            first = errors[0]
            location = "$" + "".join(f".{part}" if isinstance(part, str) else f"[{part}]" for part in first.path)
            raise ValidationError(f"{instance_path}: {location}: {first.message}")
    except ImportError:
        _validate_fallback(instance, schema)


def validate_result_artifact_paths(repo_root: Path, result_path: Path) -> None:
    result = load_json(result_path)
    artifacts = result.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise ValidationError(f"{result_path}: artifacts must be an array")
    for raw in artifacts:
        if not isinstance(raw, str):
            raise ValidationError(f"{result_path}: artifact path must be a string: {raw!r}")
        artifact_path = (repo_root / raw).resolve() if not Path(raw).is_absolute() else Path(raw).resolve()
        try:
            artifact_path.relative_to(repo_root.resolve())
        except ValueError as exc:
            raise ValidationError(f"{result_path}: artifact escapes repo root: {raw}") from exc
        if not artifact_path.exists():
            raise ValidationError(f"{result_path}: missing declared artifact: {raw}")


def validate_required_result_files(repo_root: Path, project: str, iteration: int) -> None:
    iter_id = f"{iteration:04d}"
    result_path = repo_root / "research" / project / "results" / f"{iter_id}_result.json"
    summary_path = repo_root / "research" / project / "results" / f"{iter_id}_summary.md"
    artifact_dir = repo_root / "research" / project / "artifacts" / iter_id
    missing = [path for path in (result_path, summary_path, artifact_dir) if not path.exists()]
    if missing:
        raise ValidationError("missing required result files: " + ", ".join(str(path) for path in missing))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate autoresearcher artifacts.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--json", type=Path, required=True, help="JSON artifact to validate")
    parser.add_argument("--schema", type=Path, required=True, help="JSON schema path")
    parser.add_argument("--check-result-artifacts", action="store_true")
    args = parser.parse_args()

    try:
        validate_json_schema(args.json, args.schema)
        if args.check_result_artifacts:
            validate_result_artifact_paths(args.repo_root.resolve(), args.json)
    except ValidationError as exc:
        print(f"validation failed: {exc}")
        return 1
    print("validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

