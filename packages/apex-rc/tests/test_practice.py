"""Tests for the RC Practice bundle."""

from __future__ import annotations

from pathlib import Path

from apex_core.types import Practice
from apex_core.validators import validate_manifest
from apex_rc import rc_bundle
from apex_schemas_common.standards import STANDARDS


def test_bundle_identifies_rc_practice() -> None:
    bundle = rc_bundle()
    assert bundle.practice is Practice.RC
    assert bundle.name == "rc"


def test_bundle_has_three_schema_families() -> None:
    bundle = rc_bundle()
    assert set(bundle.schema_families) == {"scml", "merml", "cxml"}


def test_scml_entities_present() -> None:
    bundle = rc_bundle()
    assert set(bundle.entities["scml"]) == {
        "SKU", "Location", "Lot", "Shipment", "Supplier", "Item",
    }


def test_merml_entities_present() -> None:
    bundle = rc_bundle()
    assert set(bundle.entities["merml"]) == {
        "Category", "Price", "Promotion", "Markdown",
    }


def test_cxml_entities_present() -> None:
    bundle = rc_bundle()
    assert set(bundle.entities["cxml"]) == {
        "Customer", "Loyalty", "Interaction", "Order",
    }


def test_bundle_standards_registered() -> None:
    bundle = rc_bundle()
    for standard_id in bundle.standards:
        assert standard_id in STANDARDS, f"Unregistered: {standard_id}"


def test_bundle_is_frozen() -> None:
    bundle = rc_bundle()
    import pytest
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        bundle.name = "something-else"  # type: ignore[misc]


def test_declarative_yaml_manifest_validates() -> None:
    """The data/schemas.manifest.yaml parses as a valid SchemaManifest."""
    manifest_path = (
        Path(__file__).parent.parent
        / "src" / "apex_rc" / "data" / "schemas.manifest.yaml"
    )
    report = validate_manifest(manifest_path)
    assert report.valid, f"Errors: {report.errors}"
    assert report.kind == "schema"
    assert report.manifest is not None
