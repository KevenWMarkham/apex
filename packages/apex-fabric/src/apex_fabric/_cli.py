"""apex-fabric Typer subcommands (attached to the root ``apex`` CLI).

Subcommands:

    apex fabric validate-name <name>
    apex fabric canonical-name <practice> <environment> <role> [--suffix S]
    apex fabric describe-blueprint <blueprint>

The REST-call subcommands (create-workspace, create-shortcut) require an
authenticated session and are intentionally omitted from the top-level
CLI surface — production callers use the Python API directly so token
provisioning and error handling stay explicit. Tests cover the API
client directly (see ``tests/test_workspaces.py``,
``tests/test_shortcuts.py``).
"""

from __future__ import annotations

from pathlib import Path

import typer

from apex_fabric.workspaces import (
    ENVIRONMENTS,
    PRACTICES,
    ROLES,
    canonical_workspace_name,
    parse_workspace_name,
    validate_workspace_name,
)


fabric_app = typer.Typer(
    name="fabric",
    help="APEX Fabric integration — workspace naming, capacity blueprints, OneLake shortcuts.",
    no_args_is_help=True,
)


@fabric_app.command("validate-name")
def validate_name_cmd(name: str = typer.Argument(...)) -> None:
    """Validate a workspace name against the APEX canonical pattern.

    Exits 0 if valid, 1 otherwise. Prints parsed components on success.
    """
    if not validate_workspace_name(name):
        typer.echo(f"FAIL: {name} does not match canonical pattern.")
        typer.echo(
            "Expected: apex-{practice}-{environment}-{role}[-{suffix}]"
        )
        typer.echo(f"  Practices:    {', '.join(PRACTICES)}")
        typer.echo(f"  Environments: {', '.join(ENVIRONMENTS)}")
        typer.echo(f"  Roles:        {', '.join(ROLES)}")
        raise typer.Exit(code=1)
    parts = parse_workspace_name(name)
    typer.echo(f"OK: {name}")
    for k in ("practice", "environment", "role", "suffix"):
        typer.echo(f"  {k:14}{parts[k] or '(none)'}")


@fabric_app.command("canonical-name")
def canonical_name_cmd(
    practice: str = typer.Argument(..., help=f"One of {', '.join(PRACTICES)}."),
    environment: str = typer.Argument(..., help=f"One of {', '.join(ENVIRONMENTS)}."),
    role: str = typer.Argument(..., help=f"One of {', '.join(ROLES)}."),
    suffix: str = typer.Option(None, "--suffix", help="Optional suffix [a-z0-9]+."),
) -> None:
    """Generate the canonical workspace name for the given parts."""
    typer.echo(canonical_workspace_name(practice, environment, role, suffix))


@fabric_app.command("describe-blueprint")
def describe_blueprint_cmd(
    blueprint: str = typer.Argument(
        ...,
        help="One of: single-capacity-tenant, dev-prod-split, per-workload-isolation.",
    ),
) -> None:
    """Print a brief description of a Terraform blueprint."""
    descriptions = {
        "single-capacity-tenant": (
            "Single F-SKU capacity hosting all medallion roles (Bronze, Silver, "
            "Gold, Governance, Runtime). Right for Wave 1 pilots and small-to-"
            "mid Wave 2 engagements. Smallest viable: F16."
        ),
        "dev-prod-split": (
            "Two capacities — one F16/F32 for dev/test, one F64+ for production. "
            "Right for Wave 2 engagements where dev iterations should not contend "
            "with production workloads. Cost-attribution tags separate the two."
        ),
        "per-workload-isolation": (
            "Multiple production capacities, each scoped to a workload class "
            "(e.g., F128 for warehouse, F64 for real-time, F64 for governance). "
            "Right for Wave 3 enterprise scale, particularly when compliance "
            "boundaries require workload isolation. Minimum total: F256."
        ),
    }
    if blueprint not in descriptions:
        typer.echo(f"Unknown blueprint: {blueprint!r}")
        typer.echo(f"Available: {', '.join(descriptions.keys())}")
        raise typer.Exit(code=1)

    typer.echo(f"Blueprint: {blueprint}\n")
    typer.echo(descriptions[blueprint])
    typer.echo(f"\nTerraform: infra/terraform/blueprints/{blueprint}/")
