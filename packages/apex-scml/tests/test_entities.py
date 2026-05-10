"""Tests for SCML entities."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from apex_schemas_common import generate_delta_ddl
from apex_schemas_common.standards import audit_model
from apex_scml import SKU, Inventory, Item, Location, Lot, Shipment, Supplier
from apex_scml.entities import (
    InventorySnapshotKind,
    LocationType,
    SkuStatus,
    SupplierTier,
)


def _envelope() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "test_entity",
        "source_system": "sap-retail",
        "source_system_ts": datetime.now(UTC),
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "deadbeef",
    }


def test_sku_minimal_construction() -> None:
    sku = SKU(
        sku_natural="sku_0001",
        sku_status=SkuStatus.ACTIVE,
        category_key="cat_dairy",
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert sku.sku_natural == "sku_0001"
    assert sku.sku_status is SkuStatus.ACTIVE


def test_sku_with_valid_gtin() -> None:
    sku = SKU(
        sku_natural="sku_0001",
        gtin="09780201379624",
        sku_status=SkuStatus.ACTIVE,
        category_key="cat_dairy",
        unit_retail=Decimal("4.99"),
        case_pack=12,
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert sku.gtin == "09780201379624"


def test_sku_invalid_gtin_rejected() -> None:
    with pytest.raises(ValidationError):
        SKU(
            sku_natural="sku_0001",
            gtin="abc",  # fails GTIN14 regex
            sku_status=SkuStatus.ACTIVE,
            category_key="cat_dairy",
            **_envelope(),
            **_scd2(),
        )  # type: ignore[arg-type]


def test_location_with_gln() -> None:
    loc = Location(
        location_natural="store-100",
        gln="0012345678905",
        location_type=LocationType.STORE,
        name="Store 100",
        region="US-WEST",
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert loc.gln == "0012345678905"
    assert loc.location_type is LocationType.STORE


def test_lot_with_dates() -> None:
    lot = Lot(
        lot_number="LOT-2026-001",
        sku_key="sku_0001",
        manufacture_date=date(2026, 3, 1),
        expiration_date=date(2027, 3, 1),
        **_envelope(),
    )  # type: ignore[arg-type]
    assert lot.manufacture_date == date(2026, 3, 1)


def test_shipment_with_sscc() -> None:
    ship = Shipment(
        shipment_natural="SHIP-1",
        sscc="001234567890123459",
        origin_key="dc-1",
        destination_key="store-100",
        ship_datetime=datetime.now(UTC),
        **_envelope(),
    )  # type: ignore[arg-type]
    assert ship.sscc == "001234567890123459"


def test_supplier_tier_defaults_primary() -> None:
    sup = Supplier(
        supplier_natural="sup-42",
        supplier_name="ACME Co.",
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert sup.tier is SupplierTier.PRIMARY


def test_item_minimal() -> None:
    item = Item(
        item_natural="item-brand-x",
        brand="BrandX",
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert item.brand == "BrandX"


def test_inventory_minimal_construction() -> None:
    inv = Inventory(
        sku_key="sku_0001",
        location_key="store-100",
        snapshot_kind=InventorySnapshotKind.PERPETUAL,
        snapshot_at=datetime.now(UTC),
        on_hand_qty=Decimal("42"),
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert inv.on_hand_qty == Decimal("42")
    assert inv.reserved_qty == Decimal("0")  # default
    assert inv.snapshot_kind is InventorySnapshotKind.PERPETUAL


def test_inventory_with_all_quantities() -> None:
    inv = Inventory(
        sku_key="sku_0001",
        location_key="dc-east",
        lot_key="LOT-2026-001",
        snapshot_kind=InventorySnapshotKind.RECEIPT,
        snapshot_at=datetime.now(UTC),
        on_hand_qty=Decimal("120"),
        reserved_qty=Decimal("12"),
        in_transit_qty=Decimal("48"),
        avg_daily_demand=Decimal("8.5"),
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert inv.in_transit_qty == Decimal("48")
    assert inv.avg_daily_demand == Decimal("8.5")
    assert inv.lot_key == "LOT-2026-001"


def test_sku_ddl_generation() -> None:
    ddl = generate_delta_ddl(SKU, database="silver_scml", partition_by=["sku_status"])
    assert "CREATE TABLE silver_scml.sku" in ddl
    assert "gtin" in ddl
    assert "PARTITIONED BY (sku_status)" in ddl


@pytest.mark.conformance
def test_standards_audit_all_registered() -> None:
    """Every StandardRef in SCML entities must resolve in the STANDARDS registry."""
    for entity_cls in (SKU, Location, Shipment):
        entries = audit_model(entity_cls)
        assert entries, f"Expected at least one StandardRef on {entity_cls.__name__}"
        for entry in entries:
            assert entry.registered, (
                f"{entity_cls.__name__}.{entry.field}: "
                f"unregistered standard {entry.ref.standard_id}"
            )
            assert entry.version_matches, (
                f"{entity_cls.__name__}.{entry.field}: "
                f"version drift {entry.ref.version}"
            )
