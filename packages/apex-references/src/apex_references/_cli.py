"""apex-references Typer subcommands."""

from __future__ import annotations

import typer

from apex_references.framework import (
    catalogs_root,
    demo_scripts_root,
    get_reference,
    load_demo_script,
    scan_all_references,
    validate_references,
)


references_app = typer.Typer(
    name="references",
    help="APEX Reference Deployments — list / inspect / validate / demo turnkey Wave-1 blueprints.",
    no_args_is_help=True,
)


@references_app.command("stats")
def stats_cmd() -> None:
    """Show summary stats for the reference-deployment catalog."""
    entries = scan_all_references()
    typer.echo(f"Total reference deployments shipped: {len(entries)}")
    typer.echo(f"Catalog root: {catalogs_root()}")
    typer.echo(f"Demo scripts root: {demo_scripts_root()}")
    typer.echo("")
    by_practice: dict[str, int] = {}
    for entry in entries:
        by_practice[entry.spec.practice] = by_practice.get(entry.spec.practice, 0) + 1
    for p, n in sorted(by_practice.items()):
        typer.echo(f"  {p:6} {n}")


@references_app.command("list")
def list_cmd(
    practice: str | None = typer.Option(None, "--practice", "-p"),
) -> None:
    """List reference deployments (optionally filtered by Practice)."""
    entries = scan_all_references()
    for entry in entries:
        if practice is not None and entry.spec.practice != practice.lower():
            continue
        spec = entry.spec
        typer.echo(
            f"  {spec.name:18} [{spec.practice:5}] {spec.display_name}"
        )


@references_app.command("inspect")
def inspect_cmd(
    name: str = typer.Argument(..., help="Reference name (e.g., big-box-store)."),
) -> None:
    """Show full detail for one reference deployment."""
    spec = get_reference(name)
    if spec is None:
        typer.echo(f"Reference {name!r} not found", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"name:                  {spec.name}")
    typer.echo(f"display_name:          {spec.display_name}")
    typer.echo(f"practice:              {spec.practice}")
    typer.echo(f"sellers_guide_section: {spec.sellers_guide_section}")
    typer.echo("")
    typer.echo(f"description:")
    typer.echo(f"  {spec.description}")
    typer.echo("")
    typer.echo(f"sponsor_personas:")
    for p in spec.sponsor_personas:
        typer.echo(f"  - {p}")
    typer.echo("")
    typer.echo("triggering_scenarios:")
    for s in spec.triggering_scenarios:
        typer.echo(f"  - {s.name}  (sponsor: {s.sponsor_persona})")
    typer.echo("")
    arch = spec.architecture
    typer.echo("architecture:")
    typer.echo(f"  capacity_blueprint:  {arch.capacity_blueprint}")
    typer.echo(f"  fabric_sku:          {arch.fabric_sku}")
    typer.echo(f"  adapters:            {len(arch.adapters)}  ({', '.join(arch.adapters)})")
    typer.echo(f"  canonical_schemas:   {', '.join(arch.canonical_schemas)}")
    typer.echo(f"  foundry_model_pins:  {', '.join(arch.foundry_model_pins)}")
    typer.echo("")
    typer.echo(f"use_cases ({len(spec.use_cases)}):")
    for uc in spec.use_cases:
        agents_str = ", ".join(uc.agents) if uc.agents else "(none)"
        typer.echo(f"  - {uc.name}")
        typer.echo(f"      services: {', '.join(uc.service_codes)}")
        typer.echo(f"      agents:   {agents_str}")
    typer.echo("")
    typer.echo(f"kpi_targets ({len(spec.kpi_targets)}):")
    for k in spec.kpi_targets:
        typer.echo(f"  - {k.name} ({k.direction})")
        if k.wave2_target:
            typer.echo(f"      wave2: {k.wave2_target}")
        if k.wave3_target:
            typer.echo(f"      wave3: {k.wave3_target}")
    typer.echo("")
    ws = spec.wave1_scope
    typer.echo("wave1_scope:")
    typer.echo(
        f"  duration:  {ws.duration_weeks_low}-{ws.duration_weeks_high} weeks"
    )
    typer.echo(
        f"  fee band:  ${ws.fee_band_usd_low:,}-${ws.fee_band_usd_high:,}"
    )
    typer.echo(f"  deliverables: {len(ws.deliverables)}")
    typer.echo(f"  success_criteria: {len(ws.success_criteria)}")


@references_app.command("demo")
def demo_cmd(
    name: str = typer.Argument(..., help="Reference name (e.g., big-box-store)."),
) -> None:
    """Print the markdown demo script for a reference deployment."""
    md = load_demo_script(name)
    if not md:
        typer.echo(f"No demo script found for {name!r}", err=True)
        raise typer.Exit(code=1)
    typer.echo(md)


@references_app.command("validate")
def validate_cmd() -> None:
    """Validate every shipped reference deployment manifest."""
    # Cross-reference data — best-effort; validation passes if catalogs unreachable
    service_codes: set[str] | None = None
    agent_catalog: set[str] | None = None
    adapter_catalog: set[str] | None = None
    try:
        from apex_services import all_service_codes
        service_codes = all_service_codes()
    except Exception:
        pass
    try:
        from apex_agents import scan_all_catalogs as agents_scan
        agent_catalog = {
            entry.spec.name
            for entries in agents_scan().values()
            for entry in entries
        }
    except Exception:
        pass
    try:
        from apex_adapters.catalog import load_all_shipped_manifests
        adapter_catalog = set(load_all_shipped_manifests().keys())
    except Exception:
        pass

    report = validate_references(
        service_codes=service_codes,
        agent_catalog=agent_catalog,
        adapter_catalog=adapter_catalog,
    )
    typer.echo(f"References checked: {report.references_checked}")
    typer.echo(f"Issues:             {len(report.issues)}")
    typer.echo(f"Errors:             {len(report.errors)}")
    if report.issues:
        for i in report.issues:
            typer.echo(f"  [{i.severity}] {i.reference}/{i.code}: {i.message}")
    raise typer.Exit(code=report.exit_code)
