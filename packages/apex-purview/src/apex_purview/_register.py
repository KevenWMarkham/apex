"""Batch Purview classification registration.

Discovers APEX canonical schema YAMLs across the repo, runs the emitter
against each, and writes the resulting Atlas v2 payloads to a target
directory. Non-zero exit on any emission error, which is what the CI
``register-classifications`` job consumes as a gate.

The module is invoked as:

    python -m apex_purview.register [ROOT] [--output DIR] [--strict]

or as a Typer subcommand under ``apex purview``:

    apex purview register-all [--root ROOT] [--output DIR] [--strict]
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import yaml

from apex_purview.classifications import (
    emit_classification_typedefs,
    emit_entity_classifications,
)


@dataclass
class RegistrationResult:
    """Outcome for one schema file."""

    path: Path
    ok: bool
    schema_name: str | None = None
    num_classifications: int = 0
    num_attachments: int = 0
    error: str | None = None


@dataclass
class RegistrationReport:
    """Aggregate outcome across every schema discovered."""

    results: list[RegistrationResult] = field(default_factory=list)

    @property
    def ok_count(self) -> int:
        return sum(1 for r in self.results if r.ok)

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results if not r.ok)

    @property
    def failed(self) -> list[RegistrationResult]:
        return [r for r in self.results if not r.ok]

    @property
    def exit_code(self) -> int:
        return 0 if self.fail_count == 0 else 1

    def summary(self) -> str:
        total = len(self.results)
        return (
            f"Purview classification registration: "
            f"{self.ok_count}/{total} schemas emitted, "
            f"{self.fail_count} failed."
        )


def discover_schemas(root: Path) -> list[Path]:
    """Return all schema YAMLs (``kind: schema``) under ``root``.

    Skips common noise directories (`.venv`, `node_modules`, `.git`,
    `__pycache__`). Files are included only if they parse as a mapping with
    ``kind: schema``.
    """
    skip_dirs = {
        ".venv",
        "node_modules",
        ".git",
        "__pycache__",
        "dist",
        "build",
        "fixtures",  # test-only schemas (including intentional negative cases)
    }
    candidates: list[Path] = []

    for path in root.rglob("*.yaml"):
        if any(part in skip_dirs for part in path.parts):
            continue
        try:
            with path.open("r", encoding="utf-8") as fh:
                doc = yaml.safe_load(fh)
        except Exception:
            continue
        if isinstance(doc, dict) and doc.get("kind") == "schema":
            candidates.append(path)

    for path in root.rglob("*.yml"):
        if any(part in skip_dirs for part in path.parts):
            continue
        try:
            with path.open("r", encoding="utf-8") as fh:
                doc = yaml.safe_load(fh)
        except Exception:
            continue
        if isinstance(doc, dict) and doc.get("kind") == "schema":
            candidates.append(path)

    return sorted(candidates)


def _emit_one(
    schema_path: Path,
    output_dir: Path | None,
) -> RegistrationResult:
    """Emit typedefs + attachments for a single schema. Never raises."""
    try:
        with schema_path.open("r", encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)

        if not isinstance(doc, dict):
            return RegistrationResult(
                path=schema_path,
                ok=False,
                error="Schema YAML does not parse to a mapping.",
            )

        schema_name = doc.get("name", "unknown")
        practice = doc.get("practice", "unknown")
        family = doc.get("family", schema_name)

        typedefs = emit_classification_typedefs(doc)
        attachments = emit_entity_classifications(doc)

        if output_dir is not None:
            rel = f"{practice}.{family}".lower()
            out_subdir = output_dir / rel
            out_subdir.mkdir(parents=True, exist_ok=True)
            (out_subdir / "classifications.json").write_text(
                json.dumps(typedefs, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            (out_subdir / "attachments.json").write_text(
                json.dumps(attachments, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

        return RegistrationResult(
            path=schema_path,
            ok=True,
            schema_name=schema_name,
            num_classifications=len(typedefs.get("classificationDefs", [])),
            num_attachments=len(attachments),
        )
    except Exception as exc:  # noqa: BLE001 — intentionally catch-all; recorded on result
        return RegistrationResult(
            path=schema_path,
            ok=False,
            error=f"{type(exc).__name__}: {exc}",
        )


def register_all(
    root: Path,
    output_dir: Path | None = None,
    schemas: Iterable[Path] | None = None,
) -> RegistrationReport:
    """Discover and emit Purview payloads for every schema under ``root``.

    Args:
        root: Repository root to scan.
        output_dir: Optional directory where per-schema payloads are written.
            If None, the emitter runs in validate-only mode (errors still
            surface but nothing is persisted).
        schemas: Optional explicit list of schema paths. When provided,
            ``root`` is not scanned.

    Returns:
        :class:`RegistrationReport` aggregating per-schema results.
    """
    if schemas is None:
        schemas = discover_schemas(root)

    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)

    report = RegistrationReport()
    for schema_path in schemas:
        report.results.append(_emit_one(schema_path, output_dir))
    return report


def print_report(report: RegistrationReport) -> None:
    """Print a human-readable summary of a registration run."""
    print(report.summary())
    for r in report.results:
        tag = "OK  " if r.ok else "FAIL"
        rel = r.path.name
        if r.ok:
            print(
                f"  {tag}  {rel}  classifications={r.num_classifications}  "
                f"attachments={r.num_attachments}"
            )
        else:
            print(f"  {tag}  {rel}")
            print(f"        {r.error}")


def main(argv: list[str] | None = None) -> int:
    """Script entry point used by ``python -m apex_purview.register``."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="apex-purview-register",
        description="Discover APEX schemas and emit Purview registration payloads.",
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        type=Path,
        help="Repository root to scan (default: current directory).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Directory for emitted payloads. Omit for validate-only mode.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Non-zero exit if zero schemas were discovered.",
    )
    args = parser.parse_args(argv)

    report = register_all(args.root, args.output)
    print_report(report)

    if args.strict and not report.results:
        print("FAIL: --strict is set and no schemas were discovered.", file=sys.stderr)
        return 2

    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())
