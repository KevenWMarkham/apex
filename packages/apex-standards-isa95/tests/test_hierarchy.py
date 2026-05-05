"""Tests for the ISA-95 hierarchy and validator."""

from __future__ import annotations

import pytest

from apex_standards_isa95 import (
    Isa95Area,
    Isa95Enterprise,
    Isa95Site,
    Isa95WorkCenter,
    Isa95WorkUnit,
    validate_hierarchy,
)

pytestmark = pytest.mark.conformance


def _sample_tree() -> dict[str, list]:
    enterprise = Isa95Enterprise(id="ent1", name="Acme Corp")
    site = Isa95Site(id="site1", name="Plant 1", enterprise_id="ent1", location="Detroit")
    area = Isa95Area(id="area1", name="Assembly", site_id="site1")
    wc = Isa95WorkCenter(id="wc1", name="Line A", area_id="area1")
    unit = Isa95WorkUnit(id="u1", name="Station 1", work_center_id="wc1")
    return {
        "enterprises": [enterprise],
        "sites": [site],
        "areas": [area],
        "work_centers": [wc],
        "work_units": [unit],
    }


def test_valid_hierarchy_passes() -> None:
    tree = _sample_tree()
    result = validate_hierarchy(**tree)
    assert result.ok
    assert result.errors == []


def test_missing_enterprise_detected() -> None:
    tree = _sample_tree()
    tree["enterprises"] = []  # remove
    result = validate_hierarchy(**tree)
    assert not result.ok
    assert any("enterprise" in e.lower() for e in result.errors)


def test_orphan_work_unit() -> None:
    tree = _sample_tree()
    tree["work_centers"] = []
    result = validate_hierarchy(**tree)
    assert not result.ok
    assert any("work center" in e.lower() for e in result.errors)


def test_multiple_sites_with_cross_references() -> None:
    ent = Isa95Enterprise(id="e1", name="Acme")
    sites = [
        Isa95Site(id="s1", name="Plant 1", enterprise_id="e1"),
        Isa95Site(id="s2", name="Plant 2", enterprise_id="e1"),
    ]
    # s3 references non-existent enterprise
    sites.append(Isa95Site(id="s3", name="Ghost", enterprise_id="e-missing"))
    result = validate_hierarchy(enterprises=[ent], sites=sites)
    assert not result.ok
    assert len(result.errors) == 1
    assert "s3" in result.errors[0]
