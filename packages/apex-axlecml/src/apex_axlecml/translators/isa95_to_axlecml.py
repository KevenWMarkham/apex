"""ISA-95 → AXLECML translators."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from apex_standards_isa95 import Isa95Equipment

from apex_axlecml.entities import Equipment, EquipmentStatus


def _envelope(*, entity_id: str, source_system: str = "isa95") -> dict[str, Any]:
    now = datetime.now(UTC)
    return {
        "event_id": uuid4(),
        "event_ts": now,
        "entity_id": entity_id,
        "source_system": source_system,
        "source_system_ts": now,
    }


def _scd2() -> dict[str, Any]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "isa95-import",
    }


def equipment_from_isa95(
    isa95: Isa95Equipment,
    *,
    work_center_key: str | None = None,
    source_system: str = "isa95",
) -> Equipment:
    """Translate an ISA-95 Equipment into an APEX AXLECML Equipment."""
    return Equipment(
        **_envelope(entity_id=f"equipment:{isa95.id}", source_system=source_system),
        **_scd2(),
        isa95_id=isa95.id,
        name=isa95.name,
        equipment_class_id=isa95.equipment_class_id,
        work_unit_id=isa95.work_unit_id,
        work_center_key=work_center_key,
        serial_number=isa95.serial_number,
        status=EquipmentStatus.IN_SERVICE,
        capabilities=list(isa95.capabilities),
    )  # type: ignore[arg-type]
