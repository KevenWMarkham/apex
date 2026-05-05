"""AXLECML ProductionEvent entity — ISA-95 + ISA-88 shape."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class ProductionEventType(StrEnum):
    BATCH_START = "batch_start"
    BATCH_END = "batch_end"
    PHASE_TRANSITION = "phase_transition"
    SETUP_START = "setup_start"
    SETUP_END = "setup_end"
    CHANGEOVER = "changeover"
    SCRAP = "scrap"
    REWORK = "rework"
    UNIT_COMPLETE = "unit_complete"
    OEE_SNAPSHOT = "oee_snapshot"


class ProductionEvent(CanonicalEntity):
    """A discrete event on the plant floor."""

    event_type: ProductionEventType
    equipment_key: str = Field(..., description="FK → AXLECML Equipment.entity_id.")
    work_center_key: str | None = Field(
        None, description="FK → AXLECML WorkCenter.entity_id."
    )
    batch_id: str | None = None
    phase_id: str | None = Field(None, description="ISA-88 phase name.")
    operator_id: str | None = None
    product_id: str | None = None
    occurred_at: datetime
    quantity: Decimal | None = None
    unit_of_measure: str | None = None
    notes: str = ""
