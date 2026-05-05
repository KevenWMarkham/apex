"""apex-adapters Typer subcommands — attached to the root ``apex`` CLI."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from apex_adapters.catalog import (
    ADAPTER_REGISTRY,
    list_shipped_manifests,
    load_all_shipped_manifests,
    load_shipped_manifest,
)
from apex_adapters.framework import (
    list_adapters,
    load_adapter_spec,
    register_adapter,
)


adapters_app = typer.Typer(
    name="adapters",
    help="APEX SOR adapter framework — list / inspect / smoke-test / validate.",
    no_args_is_help=True,
)


@adapters_app.command("list")
def list_cmd() -> None:
    """List every shipped reference manifest with its track + Sprint subtask."""
    manifests = list_shipped_manifests()
    typer.echo(f"Shipped reference manifests: {len(manifests)}")
    typer.echo("")
    typer.echo(f"{'Name':30} {'Track':12} {'Subtask':10}")
    typer.echo("-" * 56)
    for name in manifests:
        meta = ADAPTER_REGISTRY.get(name, {})
        track = meta.get("track", "?")
        subtask = meta.get("subtask", "?")
        typer.echo(f"{name:30} {track:12} {subtask:10}")


@adapters_app.command("inspect")
def inspect_cmd(
    adapter_name: str = typer.Argument(..., help="Manifest name (e.g., 'epic-clarity')."),
) -> None:
    """Print a summary of one shipped manifest."""
    spec = load_shipped_manifest(adapter_name)
    typer.echo(f"name:               {spec.name}")
    typer.echo(f"sor:                {spec.sor_name} ({spec.sor_vendor})")
    typer.echo(f"practice:           {spec.practice}")
    typer.echo(f"connection_method:  {spec.connection_method.value}")
    typer.echo(f"schedule:           {spec.schedule}")
    typer.echo(f"bronze_workspace:   {spec.bronze_workspace}")
    typer.echo(f"schema_mappings:    {len(spec.schema_mappings)}")
    typer.echo(f"total_fields:       {spec.total_fields()}")
    typer.echo(f"runbook contact:    {spec.runbook.primary_contact}")
    typer.echo(f"sla_recovery_min:   {spec.runbook.sla_recovery_minutes}")
    typer.echo(f"failure modes:      {len(spec.runbook.failure_modes)}")
    if spec.standards:
        typer.echo(f"standards:          {', '.join(spec.standards)}")


@adapters_app.command("validate-all")
def validate_all_cmd() -> None:
    """Load every shipped manifest and confirm it parses cleanly.

    CI gate for Sprint 15. Exits non-zero if any manifest fails to load.
    """
    manifests = list_shipped_manifests()
    failures: list[tuple[str, str]] = []
    for name in manifests:
        try:
            load_shipped_manifest(name)
        except Exception as exc:  # noqa: BLE001
            failures.append((name, f"{type(exc).__name__}: {exc}"))
    if failures:
        typer.echo(f"FAIL: {len(failures)} manifest(s) failed to load:")
        for name, err in failures:
            typer.echo(f"  {name}  {err}")
        raise typer.Exit(code=1)
    typer.echo(f"OK: {len(manifests)} manifests loaded cleanly.")


@adapters_app.command("smoke-test")
def smoke_test_cmd(
    adapter_name: str = typer.Argument(..., help="Registered adapter name."),
    manifest: Path | None = typer.Option(
        None, "--manifest",
        help="Override the shipped manifest with an external YAML.",
    ),
    golden: Path | None = typer.Option(
        None, "--golden",
        help="Optional golden-dataset JSON for fixture replay.",
    ),
    limit: int = typer.Option(100, "--limit", help="Max rows per mapping."),
) -> None:
    """Run an adapter's smoke test.

    Requires the adapter class is registered (currently: epic-clarity,
    sap-s4hana). Other shipped manifests can be inspected but not
    executed without a registered implementation.
    """
    if manifest is not None:
        spec = load_adapter_spec(manifest)
    else:
        spec = load_shipped_manifest(adapter_name)

    cls = None
    if adapter_name in list_adapters():
        cls = list_adapters_to_class(adapter_name)
    if cls is None:
        typer.echo(
            f"No adapter implementation registered for {adapter_name!r}. "
            f"Registered: {list_adapters()}. Manifest validation only:"
        )
        typer.echo(f"  Spec loads OK: {spec.name} ({spec.total_fields()} fields)")
        return

    instance = cls(spec)
    result = instance.smoke_test(golden_dataset=golden, limit=limit)
    typer.echo(
        f"smoke-test {adapter_name}: "
        f"rows_read={result.rows_read} "
        f"rows_written={result.rows_written} "
        f"fields={result.fields_mapped}"
    )
    if result.errors:
        for e in result.errors:
            typer.echo(f"  ERROR: {e}")
        raise typer.Exit(code=1)


def list_adapters_to_class(name: str):
    """Return the registered adapter class for ``name`` (or None)."""
    from apex_adapters.framework import get_adapter

    try:
        return get_adapter(name)
    except KeyError:
        return None
