"""Smoke tests — verify the package installs and imports cleanly."""

from __future__ import annotations

from typer.testing import CliRunner

import apex_core
from apex_core.cli import app


def test_version_exposed() -> None:
    assert apex_core.__version__ == "0.1.0"


def test_package_importable() -> None:
    assert hasattr(apex_core, "__version__")


def test_cli_version_command() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "apex-core 0.1.0" in result.stdout
