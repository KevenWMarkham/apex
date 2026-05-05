"""apex-scenarios Typer subcommands — attached to the root ``apex`` CLI.

Subcommands
-----------
- ``apex scenarios stats [--root .]``                  — coverage summary
- ``apex scenarios validate [--root .]``               — run all CI gates
- ``apex scenarios export-csv <out> [filters]``        — CSV export
- ``apex scenarios publish-catalog <out>``             — Appendix L master catalog
- ``apex scenarios bump <before.json> <after.json>``   — classify version bump
"""

from __future__ import annotations

from pathlib import Path

import typer

from apex_scenarios.exporters import csv_filename, write_csv
from apex_scenarios.foundation import (
    FOUNDATION_CLASSES,
    all_blocks as all_foundation_blocks,
    blocks_by_class as foundation_blocks_by_class,
    blocks_unblocking_scenario,
    effort_rollup,
    get_block as get_foundation_block,
    transitive_prerequisites,
)
from apex_scenarios.fusion import (
    all_meshes as all_fusion_meshes,
    get_mesh as get_fusion_mesh,
    mesh_by_w2_service_code,
    meshes_by_practice as fusion_meshes_by_practice,
    per_practice_counts as fusion_per_practice_counts,
)
from apex_scenarios.library import (
    DEFAULT_FEATURED_PATH,
    DEFAULT_LIBRARY_PATH,
    ScenarioIndex,
    load_featured_chains,
    load_scenario_library,
)
from apex_scenarios.publication import publish_master_catalog
from apex_scenarios.validators import (
    classify_library_bump,
    validate_agent_references,
    validate_kpis,
    validate_service_codes,
    validate_wave_data_presence,
)


scenarios_app = typer.Typer(
    name="scenarios",
    help="APEX Scenario Library tooling — validation, export, master catalog publication.",
    no_args_is_help=True,
)


def _index(root: Path) -> ScenarioIndex:
    library_path = root / DEFAULT_LIBRARY_PATH
    return ScenarioIndex(load_scenario_library(library_path))


@scenarios_app.command("stats")
def stats_cmd(
    root: Path = typer.Option(
        Path("."), "--root", help="Repository root containing docs/scenarios."
    ),
) -> None:
    """Show coverage and wave-completion statistics."""
    idx = _index(root)
    typer.echo(f"Total scenarios: {idx.total}")
    typer.echo("")
    typer.echo("Per-Practice counts:")
    for practice, count in idx.practice_counts().items():
        typer.echo(f"  {practice:6} {count}")
    typer.echo("")
    full = len(idx.with_full_wave_data())
    typer.echo(f"Wave-complete (W1+W2+W3 populated): {full}")
    typer.echo(f"Wave-incomplete:                    {idx.total - full}")


@scenarios_app.command("validate")
def validate_cmd(
    root: Path = typer.Option(Path("."), "--root"),
    fail_on_warnings: bool = typer.Option(
        False,
        "--fail-on-warnings",
        help="Treat warnings as errors (CI-strict mode).",
    ),
    skip_wave_check: bool = typer.Option(
        False,
        "--skip-wave-check",
        help="Skip Task 28.1.6 wave-data presence check (use during early sprint).",
    ),
) -> None:
    """Run every Sprint 28 governance validator and exit non-zero on errors."""
    idx = _index(root)
    chains = load_featured_chains(root / DEFAULT_FEATURED_PATH)

    reports = []
    if not skip_wave_check:
        reports.append(validate_wave_data_presence(idx.all))
    reports.append(validate_service_codes(idx.all))
    reports.append(validate_kpis(idx.all))
    reports.append(validate_agent_references(chains))

    any_errors = False
    any_warnings = False
    for r in reports:
        typer.echo(r.summary())
        for issue in r.issues:
            tag = issue.severity.upper()
            typer.echo(f"  [{tag}] {issue.code}  {issue.scope}")
            if issue.message:
                typer.echo(f"          {issue.message}")
        if r.errors:
            any_errors = True
        if r.warnings:
            any_warnings = True

    if any_errors or (fail_on_warnings and any_warnings):
        raise typer.Exit(code=1)


@scenarios_app.command("export-csv")
def export_csv_cmd(
    root: Path = typer.Option(Path("."), "--root"),
    practice: str | None = typer.Option(
        None,
        "--practice",
        "-p",
        help="Filter to one Practice (RC, HLS, ER, AXLE, TMT, TH, ICE).",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output path. If omitted, the canonical filename is used in CWD.",
    ),
) -> None:
    """Export the (optionally filtered) library as CSV."""
    idx = _index(root)
    rows = idx.by_practice(practice) if practice else idx.all

    if output is None:
        practices = [practice] if practice else None
        output = Path(csv_filename(practices=practices))

    written = write_csv(rows, output)
    typer.echo(f"Wrote {written} rows to {output}")


@scenarios_app.command("publish-catalog")
def publish_catalog_cmd(
    root: Path = typer.Option(Path("."), "--root"),
    output_dir: Path = typer.Argument(..., help="Output directory for Appendix L."),
) -> None:
    """Publish the Appendix L Scenario Library master catalog."""
    idx = _index(root)
    written = publish_master_catalog(idx, output_dir)
    typer.echo(f"Published {len(written)} files to {output_dir}:")
    for name, path in written.items():
        typer.echo(f"  {name:8} {path}")


@scenarios_app.command("bump")
def bump_cmd(
    before: Path = typer.Argument(..., exists=True, readable=True),
    after: Path = typer.Argument(..., exists=True, readable=True),
) -> None:
    """Classify the diff between two scenario-library JSONs."""
    before_scenarios = load_scenario_library(before)
    after_scenarios = load_scenario_library(after)
    result = classify_library_bump(before_scenarios, after_scenarios)
    typer.echo(f"Bump classification: {result.bump}")
    typer.echo(f"Rationale: {result.rationale}")
    if result.added:
        typer.echo(f"Added ({len(result.added)}):")
        for k in result.added[:20]:
            typer.echo(f"  + {k}")
        if len(result.added) > 20:
            typer.echo(f"  ... and {len(result.added) - 20} more")
    if result.removed:
        typer.echo(f"Removed ({len(result.removed)}):")
        for k in result.removed[:20]:
            typer.echo(f"  - {k}")


# ---------------------------------------------------------------------------
# Sprint 28 Task 28.2 — W1 Foundation catalog
# ---------------------------------------------------------------------------


@scenarios_app.command("foundation-list")
def foundation_list_cmd(
    cls: str | None = typer.Option(
        None, "--class", "-c",
        help=f"Filter to one class. Allowed: {', '.join(FOUNDATION_CLASSES)}.",
    ),
    unblocks: str | None = typer.Option(
        None, "--unblocks",
        help="Filter to blocks that unblock the named Wave-2 service code.",
    ),
) -> None:
    """List W1 Foundation building blocks (Sprint 28 Task 28.2)."""
    if unblocks is not None:
        blocks = blocks_unblocking_scenario(unblocks)
    elif cls is not None:
        blocks = foundation_blocks_by_class(cls)  # type: ignore[arg-type]
    else:
        blocks = all_foundation_blocks()
    typer.echo(f"Foundation blocks: {len(blocks)}")
    for b in blocks:
        typer.echo(
            f"  [{b.cls:6}] {b.name:34}  "
            f"{b.effort_story_points:>3} sp  "
            f"{b.effort_calendar_weeks:>4} wk"
        )


@scenarios_app.command("foundation-rollup")
def foundation_rollup_cmd(
    names: list[str] = typer.Argument(
        ..., help="Block names to roll up (whitespace-separated).",
    ),
) -> None:
    """SoW-quotable effort roll-up across selected W1 blocks (Sprint 28 §28.2.5)."""
    selection = []
    for name in names:
        b = get_foundation_block(name)
        if b is None:
            typer.echo(f"unknown block {name!r}", err=True)
            raise typer.Exit(code=1)
        selection.append(b)
    rollup = effort_rollup(selection)
    typer.echo(f"selected:                    {rollup.selected_count}")
    typer.echo(f"total story points:          {rollup.total_story_points}")
    typer.echo(f"total calendar weeks (seq):  {rollup.total_calendar_weeks}")
    typer.echo(f"parallelizable (wall clock): {rollup.parallelizable_calendar_weeks}")
    for cls, count in sorted(rollup.by_class.items()):
        typer.echo(f"  {cls:6} {count}")


@scenarios_app.command("foundation-prereqs")
def foundation_prereqs_cmd(
    name: str = typer.Argument(..., help="Block name."),
) -> None:
    """Show transitive prerequisites for a W1 block (topologically sorted)."""
    chain = transitive_prerequisites(name)
    typer.echo(f"transitive prerequisites for {name!r}:")
    for b in chain:
        marker = "*" if b.name == name else " "
        typer.echo(f"  {marker} [{b.cls:6}] {b.name}")


# ---------------------------------------------------------------------------
# Sprint 28 Task 28.3 — W3 Fusion catalog
# ---------------------------------------------------------------------------


@scenarios_app.command("fusion-list")
def fusion_list_cmd(
    practice: str | None = typer.Option(
        None, "--practice", "-p",
        help="Filter to one Practice (rc / hls / er / axle / tmt / th / ice).",
    ),
) -> None:
    """List W3 Fusion meshes (Sprint 28 Task 28.3)."""
    if practice is not None:
        meshes = fusion_meshes_by_practice(practice)
    else:
        meshes = all_fusion_meshes()
    typer.echo(f"Fusion meshes: {len(meshes)}")
    counts = fusion_per_practice_counts()
    for p in ("rc", "hls", "er", "axle", "tmt", "th", "ice"):
        typer.echo(f"  {p:6} {counts.get(p, 0)}")
    typer.echo("")
    for m in meshes:
        typer.echo(f"  [{m.practice:5}] {m.mesh_id:42}  {m.name}")


@scenarios_app.command("fusion-show")
def fusion_show_cmd(
    mesh_id: str = typer.Argument(..., help="Mesh id, e.g., mesh.rc.perishables-economics."),
) -> None:
    """Show one W3 Fusion mesh in detail."""
    m = get_fusion_mesh(mesh_id)
    if m is None:
        typer.echo(f"unknown mesh {mesh_id!r}", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"mesh_id:       {m.mesh_id}")
    typer.echo(f"practice:      {m.practice}")
    typer.echo(f"name:          {m.name}")
    typer.echo(f"description:   {m.description}")
    typer.echo(f"archetype:     {m.orchestration_archetype}")
    typer.echo(f"target tenant: {m.target_tenant_profile}")
    typer.echo(f"constituents ({len(m.constituent_w2_service_codes)}):")
    for sc in m.constituent_w2_service_codes:
        typer.echo(f"  - {sc}")
    typer.echo(f"composed outcomes ({len(m.composed_outcomes)}):")
    for outcome in m.composed_outcomes:
        typer.echo(f"  - {outcome}")


@scenarios_app.command("fusion-by-w2")
def fusion_by_w2_cmd(
    service_code: str = typer.Argument(..., help="Wave-2 service code, e.g., RC-E2E-04."),
) -> None:
    """Find W3 Fusion meshes that include the named Wave-2 scenario."""
    meshes = mesh_by_w2_service_code(service_code)
    if not meshes:
        typer.echo(f"No fusion meshes include {service_code!r}")
        return
    typer.echo(f"Meshes including {service_code!r}: {len(meshes)}")
    for m in meshes:
        typer.echo(f"  {m.mesh_id:42}  {m.name}")
