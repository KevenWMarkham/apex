"""APEX command-line interface.

Entry point for the ``apex`` CLI.

Subcommands:

- ``apex version`` — print the package version.
- ``apex validate <path>`` — validate one manifest or a Practice directory.
- ``apex classify-bump <old> <new>`` — classify the SemVer bump between two versions.
"""

from __future__ import annotations

from pathlib import Path

import typer

from apex_core._version import __version__
from apex_core.semver import SemVer, classify_bump
from apex_core.validators import validate_manifest, validate_practice

app = typer.Typer(
    name="apex",
    help="APEX — Agent-based Platform for EXecution. L1 contract tooling.",
    no_args_is_help=True,
)


# --- Optional subcommand groups (enabled if the package is installed) --------
try:  # pragma: no cover — trivial import probe
    from apex_schemas_common._cli import standards_app  # type: ignore[import-not-found]

    app.add_typer(standards_app, name="standards")
except ImportError:
    pass

try:  # pragma: no cover — trivial import probe
    from apex_purview._cli import purview_app  # type: ignore[import-not-found]

    app.add_typer(purview_app, name="purview")
except ImportError:
    pass

try:  # pragma: no cover — trivial import probe
    from apex_fabric._cli import fabric_app  # type: ignore[import-not-found]

    app.add_typer(fabric_app, name="fabric")
except ImportError:
    pass

try:  # pragma: no cover — trivial import probe
    from apex_scenarios._cli import scenarios_app  # type: ignore[import-not-found]

    app.add_typer(scenarios_app, name="scenarios")
except ImportError:
    pass

try:  # pragma: no cover — trivial import probe
    from apex_adapters._cli import adapters_app  # type: ignore[import-not-found]

    app.add_typer(adapters_app, name="adapters")
except ImportError:
    pass

try:  # pragma: no cover — trivial import probe
    from apex_agents._cli import agents_app  # type: ignore[import-not-found]

    app.add_typer(agents_app, name="agents")
except ImportError:
    pass

try:  # pragma: no cover — trivial import probe
    from apex_services._cli import services_app  # type: ignore[import-not-found]

    app.add_typer(services_app, name="services")
except ImportError:
    pass

try:  # pragma: no cover — trivial import probe
    from apex_references._cli import references_app  # type: ignore[import-not-found]

    app.add_typer(references_app, name="references")
except ImportError:
    pass

try:  # pragma: no cover — trivial import probe
    from apex_registries._cli import registries_app  # type: ignore[import-not-found]

    app.add_typer(registries_app, name="registries")
except ImportError:
    pass

try:  # pragma: no cover — trivial import probe
    from apex_translators._cli import translators_app  # type: ignore[import-not-found]

    app.add_typer(translators_app, name="translators")
except ImportError:
    pass

try:  # pragma: no cover — trivial import probe
    from apex_protocols._cli import protocols_app  # type: ignore[import-not-found]

    app.add_typer(protocols_app, name="protocols")
except ImportError:
    pass


@app.command()
def version() -> None:
    """Print the installed ``apex-core`` package version."""
    typer.echo(f"apex-core {__version__}")


@app.command()
def validate(
    path: Path = typer.Argument(..., exists=True, help="Manifest file or Practice directory."),
) -> None:
    """Validate a manifest YAML file or every manifest in a Practice directory.

    Exits with code 0 if everything validates, 1 otherwise.
    """
    if path.is_dir():
        report = validate_practice(path)
        typer.echo(report.summary())
        for r in report.failures:
            typer.echo(f"  {r.summary()}")
            for err in r.errors:
                typer.echo(f"    - {err}")
        raise typer.Exit(code=0 if report.valid else 1)

    single = validate_manifest(path)
    typer.echo(single.summary())
    if not single.valid:
        for err in single.errors:
            typer.echo(f"  - {err}")
        raise typer.Exit(code=1)


@app.command(name="classify-bump")
def classify_bump_cmd(
    previous: str = typer.Argument(..., help="Previous SemVer, e.g. 1.2.0"),
    current: str = typer.Argument(..., help="Current SemVer, e.g. 1.3.0"),
) -> None:
    """Classify the SemVer bump from ``previous`` to ``current``.

    Prints one of ``PATCH`` / ``MINOR`` / ``MAJOR`` and exits 0. On invalid
    input, prints the error to stderr and exits 1.
    """
    try:
        old = SemVer.parse(previous)
        new = SemVer.parse(current)
        bump = classify_bump(old, new)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(bump.value)


if __name__ == "__main__":
    app()
