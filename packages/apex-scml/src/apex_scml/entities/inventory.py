"""SCML Inventory entity — point-in-time on-hand position per SKU × Location.

Sprint 30 item 30.3. Read by RC-E2E-03's Pricing Agent + Demand Checker
through the ``g_inventory_position_current`` Gold mart, and by RC-E2E-05
On-Shelf Availability for shelf-gap detection.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity, ScdType2Fields


class InventorySnapshotKind(StrEnum):
    """How the inventory row was captured."""

    PERPETUAL = "PERPETUAL"          # System-of-record perpetual count
    PHYSICAL = "PHYSICAL"            # Physical count override
    CYCLE_COUNT = "CYCLE_COUNT"      # Cycle-count adjustment
    RECEIPT = "RECEIPT"              # Inbound receipt event
    SHIPMENT = "SHIPMENT"            # Outbound / transfer event


class Inventory(CanonicalEntity, ScdType2Fields):
    """On-hand inventory position for a SKU × Location at a point in time.

    SCD2 history is required because the Pricing Agent's elasticity model and
    the Markdown Agent's stock-days-remaining calculation both look back at
    the inventory state at the time a candidate decision was made.
    """

    sku_key: str = Field(..., description="FK → SCML SKU.")
    location_key: str = Field(..., description="FK → SCML Location.")
    lot_key: str | None = Field(
        None, description="FK → SCML Lot. Null when lot tracking is disabled for this SKU."
    )
    snapshot_kind: InventorySnapshotKind
    snapshot_at: datetime = Field(..., description="When the position was observed.")
    on_hand_qty: Decimal = Field(..., description="Sellable on-hand quantity.")
    reserved_qty: Decimal = Field(
        Decimal("0"), description="Reserved for outstanding orders / transfers."
    )
    in_transit_qty: Decimal = Field(
        Decimal("0"), description="On the inbound network but not yet received."
    )
    avg_daily_demand: Decimal | None = Field(
        None, description="Trailing 14-day average daily demand. Feeds stock_days_remaining."
    )
    last_received_at: datetime | None = None
    last_sold_at: datetime | None = None
