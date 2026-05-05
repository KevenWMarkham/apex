"""ISO 14224 canonical reliability-event record."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from apex_standards_iso14224.failure_modes import (
    Iso14224FailureMechanism,
    Iso14224FailureMode,
)
from apex_standards_iso14224.taxonomy import (
    Iso14224EquipmentClass,
    Iso14224EquipmentSubclass,
)


class ReliabilityRecord(BaseModel):
    """Canonical reliability / maintenance event for a single equipment."""

    model_config = ConfigDict(extra="forbid")

    equipment_id: str = Field(..., description="FK → consuming Practice's Equipment canonical entity.")
    equipment_class: Iso14224EquipmentClass
    equipment_subclass: Iso14224EquipmentSubclass | None = None

    failure_mode: Iso14224FailureMode | None = None
    failure_mechanism: Iso14224FailureMechanism | None = None

    detected_at: datetime | None = Field(
        None, description="When the failure / event was first detected."
    )
    repair_started_at: datetime | None = None
    repair_completed_at: datetime | None = None
    downtime_hours: float | None = Field(None, ge=0.0)

    cause_description: str = ""
    corrective_action: str = ""
    cost_usd: float | None = Field(None, ge=0.0)
    is_critical: bool = False
