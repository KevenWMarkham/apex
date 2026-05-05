"""`apex standards` subcommand group.

Hooked into the `apex` CLI by a conditional import in ``apex_core.cli``;
decoupled so ``apex-core`` has no hard dependency on ``apex-schemas-common``.

Subcommands: ``list`` · ``show`` · ``audit`` · ``bump``.
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

import typer
from pydantic import BaseModel

from apex_core.types import Practice
from apex_schemas_common.standards import (
    STANDARDS,
    audit_model,
    list_standards,
    lookup,
)
from apex_schemas_common.standards.catalog import (
    catalog_path,
    check_catalog_drift,
    write_catalog,
)

standards_app = typer.Typer(
    name="standards",
    help="APEX industry-standards registry + audit commands.",
    no_args_is_help=True,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _import_all_apex_packages() -> None:
    """Import every installed ``apex_*`` package and walk its submodules.

    Forces Pydantic model classes to be registered as subclasses of ``BaseModel``
    so subsequent ``BaseModel.__subclasses__()`` traversal sees them.
    """
    seen: set[str] = set()
    for mod_info in pkgutil.iter_modules():
        if not mod_info.name.startswith("apex_") or mod_info.name in seen:
            continue
        seen.add(mod_info.name)
        try:
            pkg = importlib.import_module(mod_info.name)
        except ImportError:
            continue
        if hasattr(pkg, "__path__"):
            for submod in pkgutil.walk_packages(
                pkg.__path__, prefix=pkg.__name__ + "."
            ):
                try:
                    importlib.import_module(submod.name)
                except ImportError:
                    pass


def _collect_subclasses(root: type[BaseModel]) -> set[type[BaseModel]]:
    """Depth-first collection of every subclass of ``root``."""
    subs: set[type[BaseModel]] = set()
    for sub in root.__subclasses__():
        subs.add(sub)
        subs.update(_collect_subclasses(sub))
    return subs


def _apex_pydantic_models() -> list[type[BaseModel]]:
    """Return every Pydantic model defined in an ``apex_*`` module."""
    _import_all_apex_packages()
    models = _collect_subclasses(BaseModel)
    return sorted(
        (m for m in models if m.__module__.startswith("apex_")),
        key=lambda m: f"{m.__module__}.{m.__name__}",
    )


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


@standards_app.command("list")
def list_cmd(
    practice: str | None = typer.Option(
        None,
        "--practice",
        "-p",
        help="Filter to a Practice (rc, hls, er, axle, tmt, th, ice).",
    ),
) -> None:
    """List registered standards, optionally filtered to one Practice."""
    filter_practice: Practice | None = None
    if practice is not None:
        try:
            filter_practice = Practice(practice.lower())
        except ValueError as exc:
            valid = ", ".join(p.value for p in Practice)
            typer.echo(
                f"error: unknown practice {practice!r}. Valid: {valid}", err=True
            )
            raise typer.Exit(code=1) from exc

    specs = list_standards(filter_practice)
    if not specs:
        typer.echo("(no standards registered)")
        return

    typer.echo(f"{'ID':<22} {'NAME':<26} {'TYPE':<16} {'PATTERN':<7} VERSION")
    typer.echo("-" * 85)
    for spec in specs:
        typer.echo(
            f"{spec.id:<22} {spec.name:<26} {spec.type.value:<16} "
            f"{spec.pattern:<7} {spec.apex_pinned_version}"
        )


@standards_app.command("show")
def show_cmd(standard_id: str = typer.Argument(..., help="Registry id, e.g. gs1-gtin.")) -> None:
    """Print full metadata for a single registered standard."""
    try:
        spec = lookup(standard_id)
    except KeyError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"id:                 {spec.id}")
    typer.echo(f"name:               {spec.name}")
    typer.echo(f"authority:          {spec.authority}")
    typer.echo(f"authority_url:      {spec.authority_url}")
    typer.echo(f"type:               {spec.type.value}")
    typer.echo(f"current_version:    {spec.current_version}")
    typer.echo(f"apex_pinned:        {spec.apex_pinned_version}")
    typer.echo(f"license:            {spec.license}")
    typer.echo(f"redistribution_ok:  {spec.redistribution_ok}")
    typer.echo(f"pattern:            {spec.pattern}")
    if spec.supporting_package:
        typer.echo(f"supporting_package: {spec.supporting_package}")
    typer.echo(f"practices:          {', '.join(p.value for p in spec.practices)}")
    if spec.notes:
        typer.echo(f"notes:              {spec.notes}")


@standards_app.command("audit")
def audit_cmd(
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Exit 1 even on version-mismatches (not just unregistered).",
    ),
) -> None:
    """Audit every Pydantic model in installed ``apex_*`` packages.

    Walks all canonical entity classes and verifies every ``StandardRef`` they
    carry is registered in the ``STANDARDS`` registry and its version pin
    matches the registry entry.

    Exits with code 1 if any ``StandardRef`` is unregistered. With ``--strict``,
    also exits 1 on any version mismatch.
    """
    models = _apex_pydantic_models()
    total_models = len(models)
    issues: list[str] = []
    models_with_refs = 0

    for model_cls in models:
        entries = audit_model(model_cls)
        if not entries:
            continue
        models_with_refs += 1
        for entry in entries:
            qualified = f"{model_cls.__module__}.{model_cls.__name__}.{entry.field}"
            if not entry.registered:
                issues.append(
                    f"[unregistered] {qualified} -> {entry.ref.standard_id!r} "
                    f"(identifier={entry.ref.identifier})"
                )
            elif not entry.version_matches:
                spec = STANDARDS[entry.ref.standard_id]
                kind = "version-drift"
                msg = (
                    f"[{kind}] {qualified} -> {entry.ref.standard_id} "
                    f"pins {entry.ref.version}, registry pins {spec.apex_pinned_version}"
                )
                issues.append(msg)

    typer.echo(f"audited {total_models} models ({models_with_refs} with standards bindings)")
    if not issues:
        typer.echo("OK - all bindings registered, all versions match")
        return

    for issue in issues:
        typer.echo(issue, err=True)

    has_unregistered = any("[unregistered]" in i for i in issues)
    has_drift = any("[version-drift]" in i for i in issues)
    if has_unregistered or (strict and has_drift):
        typer.echo(f"FAIL - {len(issues)} issue(s)", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"WARN - {len(issues)} version-drift(s); rerun with --strict to fail the build")


@standards_app.command("bump")
def bump_cmd(
    standard_id: str = typer.Argument(..., help="Registry id."),
    to_version: str = typer.Option(..., "--to", help="Target version string."),
    dry_run: bool = typer.Option(
        True,
        "--dry-run/--apply",
        help="Show impact only (default) vs. attempt to apply (not yet supported).",
    ),
) -> None:
    """Impact analysis for bumping a registered standard to a new version."""
    try:
        spec = lookup(standard_id)
    except KeyError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"{spec.id}: {spec.apex_pinned_version} -> {to_version}")
    typer.echo(f"pattern:            {spec.pattern}")
    typer.echo(f"practices affected: {', '.join(p.value for p in spec.practices)}")
    if spec.supporting_package:
        typer.echo(f"supporting package: {spec.supporting_package}")

    # Find every model field that references this standard_id
    models = _apex_pydantic_models()
    hits: list[str] = []
    for model_cls in models:
        for entry in audit_model(model_cls):
            if entry.ref.standard_id == standard_id:
                hits.append(
                    f"  {model_cls.__module__}.{model_cls.__name__}.{entry.field} "
                    f"(currently pinned to {entry.ref.version})"
                )
    typer.echo(f"\nfields referencing this standard: {len(hits)}")
    for hit in hits:
        typer.echo(hit)

    typer.echo("\nimpact class (version-string math only):")
    typer.echo(
        "  APEX bump policy: additive -> MINOR -> ACK_ONLY; breaking -> MAJOR -> HITL"
    )

    if not dry_run:
        typer.echo(
            "\nerror: --apply is not yet implemented. Edit registry.py directly "
            "and open a PR.",
            err=True,
        )
        raise typer.Exit(code=2)
    typer.echo("\n(dry-run) No changes applied.")


# ---------------------------------------------------------------------------
# Sprint 20 Task 20.4 — catalog.yaml round-trip + drift check
# ---------------------------------------------------------------------------


@standards_app.command("sync-catalog")
def sync_catalog_cmd(
    check: bool = typer.Option(
        False,
        "--check",
        help="Don't write — just exit 1 if catalog.yaml is stale relative to STANDARDS.",
    ),
) -> None:
    """Write standards/catalog.yaml from the in-memory STANDARDS registry.

    With ``--check``, only verify the catalog is in sync (CI-friendly).
    """
    if check:
        report = check_catalog_drift()
        typer.echo(f"standards in code:     {report.standards_in_code}")
        typer.echo(f"standards in catalog:  {report.standards_in_catalog}")
        typer.echo(f"issues:                {len(report.issues)}")
        if report.errors:
            for issue in report.errors:
                typer.echo(
                    f"  [{issue.severity}] {issue.standard_id}: [{issue.code}] {issue.message}",
                    err=True,
                )
            typer.echo("FAIL — run `apex standards sync-catalog` to regenerate", err=True)
            raise typer.Exit(code=1)
        typer.echo("OK — catalog.yaml is in sync with STANDARDS")
        return

    target = write_catalog()
    typer.echo(f"wrote {target}")
    typer.echo(f"standards: {len(STANDARDS)}")


@standards_app.command("validate-catalog")
def validate_catalog_cmd() -> None:
    """Validate catalog.yaml structurally and check drift.

    Fails on any of:

    - File missing or unparseable
    - Field mismatch between catalog and code
    - Extra catalog rows with no code registration
    - Missing catalog rows for code registrations
    """
    target = catalog_path()
    if not target.exists():
        typer.echo(f"FAIL — catalog file does not exist: {target}", err=True)
        raise typer.Exit(code=1)

    report = check_catalog_drift()
    typer.echo(f"catalog file:          {target}")
    typer.echo(f"standards in code:     {report.standards_in_code}")
    typer.echo(f"standards in catalog:  {report.standards_in_catalog}")
    typer.echo(f"issues:                {len(report.issues)}")
    if report.errors:
        for issue in report.errors:
            typer.echo(
                f"  [{issue.severity}] {issue.standard_id}: [{issue.code}] {issue.message}",
                err=True,
            )
        typer.echo(f"FAIL — {len(report.errors)} catalog issue(s)", err=True)
        raise typer.Exit(code=1)
    typer.echo("OK — catalog and code are consistent")
