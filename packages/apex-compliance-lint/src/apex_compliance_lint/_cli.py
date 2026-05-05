"""apex-compliance-lint CLI — Sprint 29 Task 29.9.4-5.

Standalone entry point (registered as console_script ``apex-compliance-lint``)
plus a Typer app subcommand integrable with the root ``apex`` CLI when
``apex-orchestrator`` is on the path.

Exit codes per Sprint 29 §29.9.5:

- 0 = clean (no errors)
- 1 = at least one violation at ERROR severity
- 2 = config error (unknown pack, malformed config, no files matched)
"""

from __future__ import annotations

import sys
from pathlib import Path

import typer

from apex_compliance_lint import (
    DEFAULT_PACKS,
    LintReport,
    Severity,
    default_registry,
    lint_paths,
)
from apex_compliance_lint.rules import (
    APEX_BRAND,
    APEX_TYPOGRAPHY,
    DELOITTE_MICROSOFT_INDEPENDENCE,
)


app = typer.Typer(
    name="apex-compliance-lint",
    help="APEX compliance linter — Independence-language + typography + brand rules.",
    no_args_is_help=True,
)


PACK_REGISTRY = {
    "deloitte_microsoft_independence": DELOITTE_MICROSOFT_INDEPENDENCE,
    "apex_typography": APEX_TYPOGRAPHY,
    "apex_brand": APEX_BRAND,
}


@app.callback(invoke_without_command=True)
def main(
    paths: list[Path] = typer.Argument(
        None, help="Files or directories to scan."
    ),
    pack: list[str] = typer.Option(
        None, "--pack", "-p",
        help=(
            "Rule pack id(s) to apply. Default: all three "
            "(deloitte_microsoft_independence, apex_typography, apex_brand). "
            "Pass --pack multiple times to compose."
        ),
    ),
    severity_floor: str = typer.Option(
        "warning", "--severity",
        help="Lowest severity to display (info / warning / error). Default warning.",
    ),
    quiet: bool = typer.Option(
        False, "--quiet", help="Suppress per-violation output; print summary only.",
    ),
    fail_on_warnings: bool = typer.Option(
        False, "--fail-on-warnings",
        help="Exit non-zero if any warnings are present (CI-strict mode).",
    ),
) -> None:
    """Run the compliance linter against one or more paths."""
    if not paths:
        typer.echo("error: no paths given", err=True)
        raise typer.Exit(code=2)

    # Resolve rule packs
    if pack:
        try:
            packs = [PACK_REGISTRY[p] for p in pack]
        except KeyError as exc:
            typer.echo(
                f"error: unknown rule pack {exc.args[0]!r}. "
                f"Known: {sorted(PACK_REGISTRY)}",
                err=True,
            )
            raise typer.Exit(code=2)
    else:
        packs = list(DEFAULT_PACKS)

    # Severity floor
    severity_order = {"info": 0, "warning": 1, "error": 2}
    if severity_floor.lower() not in severity_order:
        typer.echo(
            f"error: --severity must be info/warning/error, got {severity_floor!r}",
            err=True,
        )
        raise typer.Exit(code=2)
    floor = severity_order[severity_floor.lower()]

    # Expand directory inputs to file lists
    expanded: list[Path] = []
    registry = default_registry()
    valid_exts = set(registry.keys())
    for p in paths:
        if p.is_dir():
            for sub in p.rglob("*"):
                if sub.suffix.lower() in valid_exts:
                    expanded.append(sub)
        elif p.is_file():
            expanded.append(p)
        else:
            typer.echo(f"warn: skipping non-existent path {p}", err=True)

    if not expanded:
        typer.echo("error: no files matched after directory expansion", err=True)
        raise typer.Exit(code=2)

    report = lint_paths(expanded, adapter_registry=registry, packs=packs)

    # Render
    visible_violations = [
        v for v in report.violations
        if severity_order[v.severity.value] >= floor
    ]

    if not quiet:
        for v in visible_violations:
            tag = v.severity.value.upper()
            typer.echo(
                f"{v.file}:{v.line}:{v.column}: [{tag}] {v.rule_id}",
                err=(v.severity == Severity.ERROR),
            )
            typer.echo(f"  matched: {v.matched_text!r}")
            if v.guidance:
                typer.echo(f"  guidance: {v.guidance}")
            if v.approved_substitutes:
                typer.echo(
                    f"  approved substitutes: {', '.join(v.approved_substitutes)}"
                )

    typer.echo("")
    typer.echo(f"files scanned:    {report.files_scanned}")
    typer.echo(f"rules evaluated:  {report.rules_evaluated}")
    typer.echo(f"errors:           {len(report.errors)}")
    typer.echo(f"warnings:         {len(report.warnings)}")
    typer.echo(f"info:             {len(report.infos)}")

    if not report.ok:
        typer.echo("FAIL — Independence / brand / typography violations detected", err=True)
        raise typer.Exit(code=1)
    if fail_on_warnings and report.warnings:
        typer.echo("FAIL — warnings present and --fail-on-warnings was set", err=True)
        raise typer.Exit(code=1)
    typer.echo("OK — compliance lint clean")


if __name__ == "__main__":
    app()
