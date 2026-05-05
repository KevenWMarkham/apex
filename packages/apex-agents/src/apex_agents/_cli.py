"""apex-agents Typer subcommands."""

from __future__ import annotations

import typer

from apex_agents.framework import (
    PRACTICE_CODES,
    catalogs_root,
    scan_all_catalogs,
    scan_practice_catalog,
    validate_catalogs,
)


agents_app = typer.Typer(
    name="agents",
    help="APEX Agent Catalog — list / inspect / validate Practice agent manifests.",
    no_args_is_help=True,
)


@agents_app.command("stats")
def stats_cmd() -> None:
    """Show per-Practice agent counts."""
    cats = scan_all_catalogs()
    total = sum(len(v) for v in cats.values())
    typer.echo(f"Total agents shipped: {total}")
    typer.echo(f"Catalog root: {catalogs_root()}")
    typer.echo("")
    typer.echo("Per-Practice counts:")
    for practice in PRACTICE_CODES:
        typer.echo(f"  {practice:6} {len(cats[practice])}")


@agents_app.command("list")
def list_cmd(
    practice: str | None = typer.Option(
        None, "--practice", "-p",
        help="Filter to one Practice (rc / hls / er / axle / tmt / th / ice).",
    ),
) -> None:
    """List agents in one Practice or every Practice."""
    if practice is not None:
        entries = scan_practice_catalog(practice)
        typer.echo(f"{practice.upper()}: {len(entries)} agent(s)")
        for entry in entries:
            typer.echo(
                f"  {entry.spec.name:60} "
                f"persona={entry.spec.persona[:25]:25} "
                f"tier={entry.spec.model_tier.value}"
            )
    else:
        cats = scan_all_catalogs()
        for p in PRACTICE_CODES:
            typer.echo(f"\n[{p.upper()}] {len(cats[p])} agent(s)")
            for entry in cats[p]:
                typer.echo(
                    f"  {entry.spec.name:60} "
                    f"persona={entry.spec.persona[:25]:25} "
                    f"tier={entry.spec.model_tier.value}"
                )


@agents_app.command("inspect")
def inspect_cmd(
    agent_name: str = typer.Argument(..., help="Agent name (e.g., 'apex.rc.agents.cold-chain-response')."),
) -> None:
    """Show full detail for one agent."""
    cats = scan_all_catalogs()
    for entries in cats.values():
        for entry in entries:
            if entry.spec.name == agent_name:
                spec = entry.spec
                typer.echo(f"name:                {spec.name}")
                typer.echo(f"version:             {spec.version}")
                typer.echo(f"practice:            {spec.practice}")
                typer.echo(f"persona:             {spec.persona}")
                typer.echo(f"service_codes:       {spec.service_codes}")
                typer.echo(f"model_tier:          {spec.model_tier.value}")
                typer.echo(f"model_pin:           {spec.model_pin}")
                typer.echo(f"oversight_modes:     {[m.value for m in spec.oversight_modes]}")
                typer.echo(f"tools:               {len(spec.tools)} ({len(spec.write_tools())} write)")
                typer.echo(f"hitl_gates:          {len(spec.hitl_gates)}")
                typer.echo(f"kpis:                {len(spec.kpis)}")
                if spec.archetype_id:
                    typer.echo(f"archetype_id:        {spec.archetype_id}")
                if spec.forbidden_classifications:
                    typer.echo(f"forbidden_classes:   {spec.forbidden_classifications}")
                typer.echo("")
                typer.echo(f"description:")
                typer.echo(f"  {spec.description}")
                return
    typer.echo(f"Agent {agent_name!r} not found.")
    raise typer.Exit(code=1)


@agents_app.command("validate")
def validate_cmd() -> None:
    """Validate every shipped catalog. CI gate. Exits non-zero on errors."""
    report = validate_catalogs()
    typer.echo(f"Validated {report.agents_checked} agents.")
    if report.errors:
        typer.echo(f"\n{len(report.errors)} ERROR(S):")
        for issue in report.errors:
            typer.echo(f"  [{issue.code}] {issue.practice}/{issue.agent_name}")
            if issue.message:
                typer.echo(f"    {issue.message}")
    warnings = [i for i in report.issues if i.severity == "warning"]
    if warnings:
        typer.echo(f"\n{len(warnings)} WARNING(S):")
        for issue in warnings:
            typer.echo(f"  [{issue.code}] {issue.practice}/{issue.agent_name}")
            if issue.message:
                typer.echo(f"    {issue.message}")
    if report.ok:
        typer.echo("\nOK: every agent manifest passes governance rules.")
    raise typer.Exit(code=report.exit_code)
