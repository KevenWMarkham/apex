"""apex-services Typer subcommands."""

from __future__ import annotations

import typer

from apex_services.framework import (
    PRACTICE_CODES,
    Wave,
    catalogs_root,
    scan_all_catalogs,
    scan_practice_catalog,
    validate_service_catalogs,
)


services_app = typer.Typer(
    name="services",
    help="APEX Service Catalog — list / inspect / validate productized service manifests.",
    no_args_is_help=True,
)


@services_app.command("stats")
def stats_cmd() -> None:
    """Per-Practice service counts."""
    cats = scan_all_catalogs()
    total = sum(len(v) for v in cats.values())
    typer.echo(f"Total services shipped: {total}")
    typer.echo(f"Catalog root: {catalogs_root()}")
    typer.echo("")
    for practice in PRACTICE_CODES:
        typer.echo(f"  {practice:6} {len(cats[practice])}")


@services_app.command("list")
def list_cmd(
    practice: str | None = typer.Option(None, "--practice", "-p"),
    value_share: bool = typer.Option(
        False,
        "--value-share",
        help="Filter to value-share-eligible services only.",
    ),
) -> None:
    """List services."""
    if practice is not None:
        entries = scan_practice_catalog(practice)
        for entry in entries:
            if value_share and not entry.spec.has_value_share():
                continue
            vs = " [value-share]" if entry.spec.has_value_share() else ""
            typer.echo(f"  {entry.spec.service_code:30} {entry.spec.display_name}{vs}")
    else:
        cats = scan_all_catalogs()
        for p in PRACTICE_CODES:
            typer.echo(f"\n[{p.upper()}]")
            for entry in cats[p]:
                if value_share and not entry.spec.has_value_share():
                    continue
                vs = " [value-share]" if entry.spec.has_value_share() else ""
                typer.echo(f"  {entry.spec.service_code:30} {entry.spec.display_name}{vs}")


@services_app.command("inspect")
def inspect_cmd(
    service_code: str = typer.Argument(..., help="Service code (e.g., RC-E2E-03)."),
) -> None:
    """Show full detail for one service."""
    cats = scan_all_catalogs()
    for entries in cats.values():
        for entry in entries:
            if entry.spec.service_code.upper() == service_code.upper():
                spec = entry.spec
                typer.echo(f"service_code:        {spec.service_code}")
                typer.echo(f"display_name:        {spec.display_name}")
                typer.echo(f"practice:            {spec.practice}")
                typer.echo(f"primary_persona:     {spec.primary_persona().name if spec.primary_persona() else '(none)'}")
                typer.echo(f"commercial_model:    {spec.commercial_model.value}")
                typer.echo(f"value_share_elig:    {spec.value_share_eligible}")
                typer.echo(f"linked_agents:       {len(spec.linked_agents)}")
                typer.echo(f"linked_archetypes:   {len(spec.linked_archetypes)}")
                typer.echo(f"schemas_touched:     {spec.schemas_touched}")
                if spec.standards:
                    typer.echo(f"standards:           {', '.join(spec.standards)}")
                typer.echo("")
                typer.echo(f"brief:")
                typer.echo(f"  {spec.brief}")
                typer.echo("")
                typer.echo("KPIs:")
                for k in spec.kpis:
                    typer.echo(f"  - {k.name} ({k.direction})")
                    if k.wave2_target:
                        typer.echo(f"    wave2: {k.wave2_target}")
                typer.echo("")
                typer.echo("Wave envelopes:")
                for wave in (Wave.WAVE_1, Wave.WAVE_2, Wave.WAVE_3):
                    we = spec.wave_envelope(wave)
                    if we:
                        typer.echo(f"  {wave.value}  ${we.fee_band_low_usd:,}-${we.fee_band_high_usd:,}  ({we.duration})")
                return
    typer.echo(f"Service {service_code!r} not found.")
    raise typer.Exit(code=1)


@services_app.command("validate")
def validate_cmd() -> None:
    """Validate every shipped service manifest. CI gate."""
    # Try to cross-reference against the agent catalog
    try:
        from apex_agents.framework import scan_all_catalogs as agent_scan
        agents = set()
        for entries in agent_scan().values():
            for e in entries:
                agents.add(e.spec.name)
    except ImportError:
        agents = None

    report = validate_service_catalogs(agent_catalog=agents)
    typer.echo(f"Validated {report.services_checked} services.")
    if report.errors:
        typer.echo(f"\n{len(report.errors)} ERROR(S):")
        for issue in report.errors:
            typer.echo(f"  [{issue.code}] {issue.practice}/{issue.service_code}")
            if issue.message:
                typer.echo(f"    {issue.message}")
    warnings = [i for i in report.issues if i.severity == "warning"]
    if warnings:
        typer.echo(f"\n{len(warnings)} WARNING(S):")
        for issue in warnings:
            typer.echo(f"  [{issue.code}] {issue.practice}/{issue.service_code}")
            if issue.message:
                typer.echo(f"    {issue.message}")
    if report.ok:
        typer.echo("\nOK: every service manifest passes governance.")
    raise typer.Exit(code=report.exit_code)
