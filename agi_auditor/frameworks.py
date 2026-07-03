"""Framework rubric loader.

A framework is a citable readiness rubric: a list of criteria, each with a `bar`
(the threshold a company must publicly meet) and a `source` URL.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_FRAMEWORK_DIR = Path(__file__).parent / "frameworks"

# id -> filename
_REGISTRY = {
    "anthropic-rsp": "anthropic_rsp.json",
    "deepmind-fsf": "deepmind_fsf.json",
    "openai-5-levels": "openai_5_levels.json",
    "openai-preparedness": "openai_preparedness.json",
}


def list_frameworks() -> list[str]:
    return sorted(_REGISTRY.keys())


def load_framework(framework_id: str) -> dict[str, Any]:
    if framework_id not in _REGISTRY:
        raise ValueError(
            f"Unknown framework '{framework_id}'. Available: {', '.join(list_frameworks())}"
        )
    path = _FRAMEWORK_DIR / _REGISTRY[framework_id]
    with open(path, "r", encoding="utf-8") as f:
        fw = json.load(f)
    _validate(fw)
    return fw


def _validate(fw: dict[str, Any]) -> None:
    for key in ("id", "name", "sources", "scale", "criteria"):
        if key not in fw:
            raise ValueError(f"Framework missing required key: {key}")
    if not fw["criteria"]:
        raise ValueError("Framework has no criteria")
    for c in fw["criteria"]:
        for key in ("id", "name", "bar", "source"):
            if key not in c:
                raise ValueError(f"Criterion missing required key '{key}': {c}")
