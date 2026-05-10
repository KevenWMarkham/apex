"""Validator for ``services/rc/_bronze/landing-config.yaml``.

Sprint 30 item 30.2. Loads the YAML, expands ``${...}`` placeholders to
deterministic mock values, and constructs a :class:`BronzeLandingConfig`
per source. Run with ``python services/rc/_bronze/validate.py`` — exits
non-zero on any failure.

The Sprint 30 deploy substitutes the real Fabric workspace + lakehouse
GUIDs from the Bicep deployment outputs at apply time; this validator
proves the schema shape stays consistent regardless of those values.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

from apex_medallion.bronze.config import BronzeLandingConfig

CONFIG_PATH = Path(__file__).resolve().parent / "landing-config.yaml"

_PLACEHOLDER_PATTERN = re.compile(r"\$\{([^}]+)\}")
_MOCK_VALUES: dict[str, str] = {
    "rc_canonical_workspace_id": "00000000-0000-0000-0000-000000000001",
    "rc_bronze_lakehouse_id":    "00000000-0000-0000-0000-000000000002",
}


def _expand(node: Any) -> Any:
    if isinstance(node, str):
        return _PLACEHOLDER_PATTERN.sub(lambda m: _MOCK_VALUES.get(m.group(1), m.group(0)), node)
    if isinstance(node, list):
        return [_expand(x) for x in node]
    if isinstance(node, dict):
        return {k: _expand(v) for k, v in node.items()}
    return node


def main() -> int:
    if not CONFIG_PATH.exists():
        print(f"ERROR: missing {CONFIG_PATH}", file=sys.stderr)
        return 2

    raw = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or "sources" not in raw:
        print("ERROR: top-level 'sources' key missing", file=sys.stderr)
        return 2

    expanded = _expand(raw)
    sources = expanded["sources"]
    print(f"Validating {len(sources)} RC Bronze source(s)...")

    errors = 0
    for source in sources:
        # Validator strips fields the BronzeLandingConfig doesn't know about
        # (extras like name / feeds_silver / feeds_eventhouse) before
        # constructing the model. These are surfaced by the wizard but not
        # part of the framework-level config object.
        framework_fields = {
            "source_system", "source_pattern", "source_connection_name",
            "workspace_id", "lakehouse_id", "target_table", "partition_columns",
            "practice", "classification", "retention", "deadletter_table",
            "max_retries", "retry_backoff_seconds", "pattern_detail",
        }
        kwargs = {k: v for k, v in source.items() if k in framework_fields}
        try:
            cfg = BronzeLandingConfig.model_validate(kwargs)
        except Exception as exc:
            print(f"  FAIL  {source.get('name', '?')}: {exc}", file=sys.stderr)
            errors += 1
            continue
        print(f"  OK    {source['name']:30s}  {cfg.source_pattern.value:18s}  -> {cfg.target_table}")

    if errors:
        print(f"\n{errors} source(s) failed validation.", file=sys.stderr)
        return 1
    print(f"\nAll {len(sources)} sources valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
