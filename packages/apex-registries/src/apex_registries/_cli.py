"""apex-registries Typer subcommands."""

from __future__ import annotations

import typer

from apex_registries.framework import (
    REGISTRY_DIRS,
    list_discovery,
    list_playbooks,
    list_preclearance,
    load_playbook,
    package_root,
    scan_all_registries,
    scan_registry,
    total_entries,
    validate_registries,
)


registries_app = typer.Typer(
    name="registries",
    help="APEX Master Registries — list / inspect / validate KPI / Persona / MCP-tool / Schema / Archetype / Product / Partner / Competitive / Exercise + Wave playbooks + discovery + pre-clearance artifacts.",
    no_args_is_help=True,
)


@registries_app.command("stats")
def stats_cmd() -> None:
    """Show per-registry counts."""
    totals = total_entries()
    grand = sum(totals.values())
    typer.echo(f"Total registry entries shipped: {grand}")
    typer.echo(f"Package root: {package_root()}")
    typer.echo("")
    for name, count in totals.items():
        typer.echo(f"  {name:14} {count}")
    typer.echo("")
    typer.echo(f"Wave playbooks:        {len(list_playbooks())}")
    typer.echo(f"Discovery prompts:     {len(list_discovery())}")
    typer.echo(f"Pre-clearance docs:    {len(list_preclearance())}")


@registries_app.command("list")
def list_cmd(
    registry: str = typer.Argument(
        ..., help="Registry name (kpis, personas, mcp_tools, schemas, archetypes, products, partners, competitive, exercises)."
    ),
    practice: str | None = typer.Option(None, "--practice", "-p"),
    family: str | None = typer.Option(None, "--family", "-f", help="Family filter (archetypes/products/partners only)."),
) -> None:
    """List entries in one registry, optionally filtered."""
    if registry not in REGISTRY_DIRS:
        typer.echo(f"Unknown registry {registry!r}. Available: {list(REGISTRY_DIRS)}", err=True)
        raise typer.Exit(code=1)
    entries = scan_registry(registry)
    for entry in entries:
        spec = entry.spec
        if practice and getattr(spec, "practice", None) and spec.practice != practice.lower():
            continue
        if practice and getattr(spec, "practices", None):
            if practice.lower() not in spec.practices:
                continue
        if family and getattr(spec, "family", None) and spec.family != family.lower():
            continue
        if family and getattr(spec, "category", None) and spec.category != family.lower():
            continue
        # Resolve a sensible label
        label_keys = ("name", "display_name", "schema_code", "tool_id", "competitor")
        label = next((getattr(spec, k) for k in label_keys if getattr(spec, k, None)), entry.path.stem)
        id_keys = ("kpi_id", "persona_id", "tool_id", "schema_code", "archetype_id", "product_id", "partner_id", "entry_id", "exercise_id")
        ident = next((getattr(spec, k) for k in id_keys if getattr(spec, k, None)), entry.path.stem)
        typer.echo(f"  {ident:50} {label}")


@registries_app.command("inspect")
def inspect_cmd(
    registry: str = typer.Argument(...),
    ident: str = typer.Argument(..., help="Entry id (kpi_id, persona_id, tool_id, etc.)."),
) -> None:
    """Show full detail for one entry."""
    if registry not in REGISTRY_DIRS:
        typer.echo(f"Unknown registry {registry!r}", err=True)
        raise typer.Exit(code=1)
    entries = scan_registry(registry)
    id_keys = ("kpi_id", "persona_id", "tool_id", "schema_code", "archetype_id", "product_id", "partner_id", "entry_id", "exercise_id")
    for entry in entries:
        for k in id_keys:
            if getattr(entry.spec, k, None) == ident:
                import yaml
                typer.echo(yaml.safe_dump(entry.spec.model_dump(), sort_keys=False, default_flow_style=False, allow_unicode=True))
                return
    typer.echo(f"Entry {ident!r} not found in {registry!r}", err=True)
    raise typer.Exit(code=1)


@registries_app.command("playbook")
def playbook_cmd(
    practice: str = typer.Argument(..., help="Practice code (rc, hls, er, axle, tmt, th, ice)."),
) -> None:
    """Print the markdown Wave playbook for a Practice."""
    md = load_playbook(practice.lower())
    if not md:
        typer.echo(f"No playbook found for practice {practice!r}", err=True)
        raise typer.Exit(code=1)
    typer.echo(md)


@registries_app.command("discovery")
def discovery_cmd(
    practice: str = typer.Argument(..., help="Practice code."),
) -> None:
    """Print discovery prompts for a Practice."""
    from apex_registries.framework import discovery_root

    p = discovery_root() / f"{practice.lower()}.md"
    if not p.exists():
        typer.echo(f"No discovery prompts for practice {practice!r}", err=True)
        raise typer.Exit(code=1)
    typer.echo(p.read_text(encoding="utf-8"))


@registries_app.command("preclearance")
def preclearance_cmd(
    kind: str = typer.Argument(..., help="Pre-clearance kind: technical, legal, compliance."),
) -> None:
    """Print the named pre-clearance checklist."""
    from apex_registries.framework import preclearance_root

    p = preclearance_root() / f"{kind.lower()}-checklist.md"
    if not p.exists():
        typer.echo(f"No pre-clearance checklist for {kind!r}", err=True)
        raise typer.Exit(code=1)
    typer.echo(p.read_text(encoding="utf-8"))


@registries_app.command("validate")
def validate_cmd() -> None:
    """Validate every registry + cross-reference Sprint 16/17 catalogs."""
    a_kpi: set[str] | None = None
    s_kpi: set[str] | None = None
    a_per: set[str] | None = None
    s_per: set[str] | None = None
    a_tool: set[str] | None = None
    try:
        from apex_agents import scan_all_catalogs as agents_scan
        a_kpi = set()
        a_per = set()
        a_tool = set()
        for entries in agents_scan().values():
            for entry in entries:
                a_per.add(entry.spec.persona)
                for k in entry.spec.kpis:
                    a_kpi.add(k.name)
                for t in entry.spec.tools:
                    a_tool.add(t.tool_id)
    except Exception:
        pass
    try:
        from apex_services import scan_all_catalogs as services_scan
        s_kpi = set()
        s_per = set()
        for entries in services_scan().values():
            for entry in entries:
                for k in entry.spec.kpis:
                    s_kpi.add(k.name)
                for p in entry.spec.personas:
                    s_per.add(p.name)
    except Exception:
        pass
    report = validate_registries(
        agents_kpi_names=a_kpi,
        services_kpi_names=s_kpi,
        agents_persona_names=a_per,
        services_persona_names=s_per,
        agents_tool_ids=a_tool,
    )
    typer.echo(f"Entries checked: {report.entries_checked}")
    typer.echo(f"Issues:          {len(report.issues)}")
    typer.echo(f"Errors:          {len(report.errors)}")
    warnings = [i for i in report.issues if i.severity == "warning"]
    typer.echo(f"Warnings:        {len(warnings)}")
    for e in report.errors[:20]:
        typer.echo(f"  [{e.severity}] {e.registry}/{e.entry}: {e.code}: {e.message}")
    raise typer.Exit(code=report.exit_code)
