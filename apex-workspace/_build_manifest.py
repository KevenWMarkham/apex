"""Build apex-workspace/manifest.json from the live file family.

Sprint 26 Task 26.2 — bumps manifest_version 0.1.0 → 0.2.0, expands
boot_sequence from 8 to 10 steps, registers HEARTBEAT.md + AGENTS.md.

Run:
    py apex-workspace/_build_manifest.py

This is intentionally idempotent — re-running re-computes per-file
SHA-256 hashes from disk and re-writes the manifest. The Ed25519
signature step requires the engagement security lead's key; this
builder writes a placeholder ``signature_pending`` field.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


WORKSPACE_DIR = Path(__file__).parent

# Boot sequence — 10 steps per Sprint 26 Task 26.2.2
BOOT_SEQUENCE = [
    {"step": 1,  "action": "verify_manifest_signature",
     "description": "Ed25519 signature on manifest.json"},
    {"step": 2,  "action": "bind_workspace_scope",
     "description": "Entra scope match: read_scope must include caller"},
    {"step": 3,  "action": "load_apex_core",
     "file": "APEX-CORE.md", "description": "Constitutional rules"},
    {"step": 4,  "action": "load_charter",
     "file": "CHARTER.md", "description": "Practice rules + MCP catalog"},
    {"step": 5,  "action": "load_engagement",
     "file": "ENGAGEMENT.md", "description": "Tenant collaborators + windows"},
    {"step": 6,  "action": "load_operator",
     "file": "OPERATOR.md", "description": "Per-operator thresholds"},
    {"step": 7,  "action": "load_heartbeat",
     "file": "HEARTBEAT.md", "description": "Periodic autonomy routines (Sprint 26)"},
    {"step": 8,  "action": "load_agents",
     "file": "AGENTS.md", "description": "Operating rules — four bands (Sprint 26)"},
    {"step": 9,  "action": "load_memory",
     "files": ["memory/MEMORY.md"],
     "description": "Curated long-term memory + recent per-day files"},
    {"step": 10, "action": "open_status_channel",
     "description": "Trigger source tag + audit-row stream open"},
]

# Per-file registry — class + scopes + inheritance + immutability
FILES = {
    "APEX-CORE.md": dict(
        version="0.2.0", file_class="Internal",
        read_scope="apex-all-agents",
        modify_scope="apex-framework-stewards",
        inherits_from=[],
        required=True, immutable_during_run=True,
    ),
    "CHARTER.md": dict(
        version="0.2.0", file_class="Internal",
        read_scope="apex-rc-agents",
        modify_scope="apex-rc-practice-stewards",
        inherits_from=["APEX-CORE.md"],
        required=True, immutable_during_run=True,
    ),
    "ENGAGEMENT.md": dict(
        version="0.2.0", file_class="Internal",
        read_scope="apex-engagement-agents",
        modify_scope="apex-engagement-leads",
        inherits_from=["APEX-CORE.md", "CHARTER.md"],
        required=True, immutable_during_run=True,
    ),
    "OPERATOR.md": dict(
        version="0.2.0", file_class="Internal",
        read_scope="apex-engagement-agents",
        modify_scope="apex-engagement-leads",
        inherits_from=["APEX-CORE.md", "CHARTER.md", "ENGAGEMENT.md"],
        required=True, immutable_during_run=True,
    ),
    "HEARTBEAT.md": dict(
        version="0.1.0", file_class="Internal",
        read_scope="apex-engagement-agents",
        modify_scope="apex-engagement-leads",
        inherits_from=["APEX-CORE.md", "CHARTER.md", "ENGAGEMENT.md"],
        required=True, immutable_during_run=True,
    ),
    "AGENTS.md": dict(
        version="0.1.0", file_class="Internal",
        read_scope="apex-engagement-agents",
        modify_scope="apex-engagement-leads",
        inherits_from=["APEX-CORE.md", "CHARTER.md", "ENGAGEMENT.md"],
        required=True, immutable_during_run=True,
    ),
}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build() -> dict:
    files: dict[str, dict] = {}
    for fname, attrs in FILES.items():
        target = WORKSPACE_DIR / fname
        if not target.exists():
            raise FileNotFoundError(
                f"required workspace file missing: {target}. "
                "All Sprint 26 Task 26.1 files must exist before manifest build."
            )
        files[fname] = {
            **attrs,
            "sha256": sha256_of(target),
            "size_bytes": target.stat().st_size,
        }

    return {
        "manifest_version": "0.2.0",
        "schema_version": "apex.workspace.manifest/v0.2",
        "built_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "boot_sequence_steps": len(BOOT_SEQUENCE),
        "boot_sequence": BOOT_SEQUENCE,
        "files": files,
        "memory": {
            "directory": "memory/",
            "primary_file": "memory/MEMORY.md",
            "per_day_pattern": "memory/YYYY-MM-DD.md",
            "class": "Internal",
            "operator_curated": True,
        },
        "signature": {
            "algorithm": "Ed25519",
            "public_key_kid": "engagement-security-lead",
            "value": "signature_pending",
            "comment": (
                "Replace with engagement-security-lead's Ed25519 signature "
                "before deploying to a tenant. Sprint 26 Task 26.2.4."
            ),
        },
    }


def main() -> int:
    manifest = build()
    out = WORKSPACE_DIR / "manifest.json"
    out.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    print(f"manifest_version: {manifest['manifest_version']}")
    print(f"boot_sequence_steps: {manifest['boot_sequence_steps']}")
    print(f"files: {len(manifest['files'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
