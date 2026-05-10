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


def test_bundle_has_four_schema_families() -> None:
    bundle = rc_bundle()
    assert set(bundle.schema_families) == {"scml", "merml", "cxml", "proml"}


def test_scml_entities_present() -> None:
    bundle = rc_bundle()
    # Sprint 30.3 added Inventory.
    assert set(bundle.entities["scml"]) == {
        "SKU", "Inventory", "Location", "Lot", "Shipment", "Supplier", "Item",
    }


def test_merml_entities_present() -> None:
    bundle = rc_bundle()
    # Sprint 30.3 added Elasticity + Competitor.
    assert set(bundle.entities["merml"]) == {
        "Category", "Price", "Promotion", "Markdown", "Elasticity", "Competitor",
    }


def test_cxml_entities_present() -> None:
    bundle = rc_bundle()
    assert set(bundle.entities["cxml"]) == {
        "Customer", "Loyalty", "Interaction", "Order",
    }


def test_proml_entities_listed() -> None:
    """Sprint 30.4 — PROML entities are listed by name only (no hard dep)."""
    bundle = rc_bundle()
    assert set(bundle.entities["proml"]) == {"Pricing", "DiscountRule"}


def test_crmml_aliases_resolve_to_cxml() -> None:
    """Sprint 30.5 — CRMML.* aliases must resolve to canonical CXML entities."""
    from apex_cxml import Customer as CxmlCustomer, Loyalty as CxmlLoyalty
    from apex_rc.crmml import CRMML_ALIASES, Customer, Loyalty

    # Re-exports are the same class, not a copy.
    assert Customer is CxmlCustomer
    assert Loyalty is CxmlLoyalty

    # Alias map covers the three RC build-status calls out + Order.
    assert set(CRMML_ALIASES) == {
        "CRMML.Customer", "CRMML.Loyalty", "CRMML.Interaction", "CRMML.Order",
    }
    assert CRMML_ALIASES["CRMML.Customer"] is CxmlCustomer


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
