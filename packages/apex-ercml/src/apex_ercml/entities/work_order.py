"""ERCML WorkOrder entity — Pattern C over CIM WorkOrder (IEC 61968)."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class WorkOrderStatus(StrEnum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    CANCELLED = "cancelled"


class WorkOrder(CanonicalEntity):
    """A maintenance / inspection / construction work order."""

    cim_mrid: str | None = Field(None, description="CIM WorkOrder MRID when available.")
    work_order_number: str
    status: WorkOrderStatus = WorkOrderStatus.OPEN
    priority: int | None = Field(None, ge=1, le=5)
    created: datetime
    scheduled: datetime | None = None
    completed: datetime | None = None
    asset_key: str | None = Field(
        None, description="FK → ERCML Asset.entity_id (the asset worked on)."
    )
    assigned_to: str | None = Field(
        None, description="Crew / technician identifier."
    )
    description: str = ""
