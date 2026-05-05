"""Tests for ``apex_core.validators.fleet.validate_fleet``."""

from __future__ import annotations

from pathlib import Path

from apex_core.validators import validate_fleet

FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_single_tenant_valid() -> None:
    report = validate_fleet([FIXTURES / "tenant_acme_grocery.yaml"])
    assert report.valid
    assert len(report.tenant_reports) == 1
    assert report.cross_tenant_errors == []


def test_duplicate_tenant_name_detected(tmp_path: Path) -> None:
    src = (FIXTURES / "tenant_acme_grocery.yaml").read_text(encoding="utf-8")
    a = tmp_path / "t1.yaml"
    b = tmp_path / "t2.yaml"
    a.write_text(src, encoding="utf-8")
    b.write_text(src, encoding="utf-8")  # same name -> duplicate
    report = validate_fleet([a, b])
    assert not report.valid
    assert any("Duplicate tenant name" in e for e in report.cross_tenant_errors)
