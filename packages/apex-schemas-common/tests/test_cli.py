"""Tests for the `apex standards` CLI subcommand group."""

from __future__ import annotations

from typer.testing import CliRunner

from apex_core.cli import app

runner = CliRunner()


class TestStandardsList:
    def test_list_all(self) -> None:
        result = runner.invoke(app, ["standards", "list"])
        assert result.exit_code == 0
        assert "gs1-gtin" in result.stdout
        assert "hl7-fhir" in result.stdout

    def test_list_filter_by_practice_rc(self) -> None:
        result = runner.invoke(app, ["standards", "list", "--practice", "rc"])
        assert result.exit_code == 0
        assert "gs1-gtin" in result.stdout
        assert "hl7-fhir" not in result.stdout

    def test_list_filter_by_practice_hls(self) -> None:
        result = runner.invoke(app, ["standards", "list", "-p", "hls"])
        assert result.exit_code == 0
        assert "hl7-fhir" in result.stdout
        assert "gs1-gtin" not in result.stdout

    def test_list_invalid_practice(self) -> None:
        result = runner.invoke(app, ["standards", "list", "--practice", "not-real"])
        assert result.exit_code == 1
        assert "unknown practice" in result.stderr or "unknown practice" in result.output


class TestStandardsShow:
    def test_show_known(self) -> None:
        result = runner.invoke(app, ["standards", "show", "gs1-gtin"])
        assert result.exit_code == 0
        assert "GS1 GTIN" in result.stdout
        assert "pattern:" in result.stdout
        assert "rc" in result.stdout

    def test_show_unknown_fails(self) -> None:
        result = runner.invoke(app, ["standards", "show", "not-a-real-standard"])
        assert result.exit_code == 1


class TestStandardsAudit:
    def test_audit_clean_passes(self) -> None:
        # With just the core standards packages installed, every registered
        # binding on every apex_* model should validate.
        result = runner.invoke(app, ["standards", "audit"])
        assert result.exit_code == 0
        assert "OK" in result.stdout


class TestStandardsBump:
    def test_bump_dry_run_prints_impact(self) -> None:
        result = runner.invoke(
            app, ["standards", "bump", "gs1-gtin", "--to", "BMS-1.35"]
        )
        assert result.exit_code == 0
        assert "BMS-1.35" in result.stdout
        assert "dry-run" in result.stdout.lower()

    def test_bump_unknown_fails(self) -> None:
        result = runner.invoke(
            app, ["standards", "bump", "not-a-real-standard", "--to", "2.0"]
        )
        assert result.exit_code == 1

    def test_bump_apply_not_implemented(self) -> None:
        result = runner.invoke(
            app,
            ["standards", "bump", "gs1-gtin", "--to", "BMS-1.35", "--apply"],
        )
        assert result.exit_code == 2
