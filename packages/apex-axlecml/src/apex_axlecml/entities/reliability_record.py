"""AXLECML AxleReliabilityRecord — Pattern C over ISO 14224."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from apex_schemas_common import CanonicalEntity
from apex_standards_iso14224 import (
    Iso14224EquipmentClass,
    Iso14224EquipmentSubclass,
    Iso14224FailureMechanism,
    Iso14224FailureMode,
)


class AxleReliabilityRecord(CanonicalEntity):
    """Reliability / maintenance event on an AXLE Equipment."""

    equipment_key: str = Field(..., description="FK → AXLECML Equipment.entity_id.")
    equipment_class: Iso14224EquipmentClass
    equipment_subclass: Iso14224EquipmentSubclass | None = None
    failure_mode: Iso14224FailureMode | None = None
    failure_mechanism: Iso14224FailureMechanism | None = None
    detected_at: datetime | None = None
    repair_started_at: datetime | None = None
    repair_completed_at: datetime | None = None
    downtime_hours: float | None = Field(None, ge=0.0)
    production_impact_units: int | None = Field(None, ge=0)
    cause_description: str = ""
    corrective_action: str = ""
    is_critical: bool = False
