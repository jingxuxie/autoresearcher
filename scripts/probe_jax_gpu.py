#!/usr/bin/env python3
"""Probe JAX installation and GPU visibility."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether JAX can run a tiny computation on GPU.")
    parser.add_argument("--require-gpu", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result: Dict[str, Any] = {
        "ok": False,
        "jax_version": None,
        "default_backend": None,
        "devices": [],
        "gpu_devices": [],
        "tiny_compute": None,
        "error": None,
    }

    try:
        import jax
        import jax.numpy as jnp

        devices = jax.devices()
        gpu_devices = [device for device in devices if device.platform == "gpu"]
        result["jax_version"] = jax.__version__
        result["default_backend"] = jax.default_backend()
        result["devices"] = [str(device) for device in devices]
        result["gpu_devices"] = [str(device) for device in gpu_devices]

        target = gpu_devices[0] if gpu_devices else None
        if args.require_gpu and target is None:
            result["error"] = "JAX imported, but no GPU devices are visible."
            return write_result(args.output, result, 2)

        x = jnp.arange(8, dtype=jnp.float32)
        if target is not None:
            x = jax.device_put(x, target)
        y = jnp.sum(x * x)
        result["tiny_compute"] = float(y)
        result["ok"] = True
        return write_result(args.output, result, 0)
    except Exception as exc:  # pragma: no cover - depends on local GPU stack
        result["error"] = f"{type(exc).__name__}: {exc}"
        return write_result(args.output, result, 1)


def write_result(output: Path | None, result: Dict[str, Any], code: int) -> int:
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text)
    print(text, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
