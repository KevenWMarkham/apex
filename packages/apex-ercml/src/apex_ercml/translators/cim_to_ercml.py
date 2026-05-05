"""CIM → ERCML translators (Pattern D)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from apex_standards_cim import (
    CimAsset,
    CimEnergyEvent,
    CimMeter,
    CimReading,
    CimWorkOrder,
)

from apex_ercml.entities import (
    Asset,
    AssetLifecycleState,
    GridEvent,
    GridEventType,
    Meter,
    MeterKind,
    MeterReading,
    ReadingQuality,
    WorkOrder,
    WorkOrderStatus,
)

_CIM_TO_MAP_EVENT_TYPE = {
    "outage": GridEventType.OUTAGE,
    "fault": GridEventType.FAULT,
    "voltage_sag": GridEventType.VOLTAGE_SAG,
    "voltage_swell": GridEventType.VOLTAGE_SWELL,
}


def _envelope(
    *, entity_id: str, source_system: str = "cim",
    event_ts: datetime | None = None,
    event_id: UUID | None = None,
) -> dict[str, Any]:
    now = datetime.now(UTC)
    return {
        "event_id": event_id or uuid4(),
        "event_ts": event_ts or now,
        "entity_id": entity_id,
        "source_system": source_system,
        "source_system_ts": now,
    }


def _scd2(valid_from: datetime | None = None) -> dict[str, Any]:
    return {
        "scd2_valid_from": valid_from or datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "cim-import",
    }


def meter_from_cim(cim: CimMeter, *, source_system: str = "cim") -> Meter:
    """Translate a CIM Meter into an APEX ERCML Meter."""
    return Meter(
        **_envelope(entity_id=f"meter:{cim.m_rid}", source_system=source_system),
        **_scd2(cim.install_date),
        cim_mrid=cim.m_rid,
        serial_number=cim.serial_number,
        kind=MeterKind(cim.kind.value),
        customer_key=cim.customer_mrid,
        location_key=cim.location_mrid,
        install_date=cim.install_date,
        remove_date=cim.remove_date,
    )  # type: ignore[arg-type]


def meter_reading_from_cim(
    cim: CimReading, *, meter_key: str, source_system: str = "cim",
) -> MeterReading:
    """Translate a CIM Reading into an APEX ERCML MeterReading."""
    quality = ReadingQuality.MEASURED
    if cim.quality_flag:
        try:
            quality = ReadingQuality(cim.quality_flag)
        except ValueError:
            quality = ReadingQuality.MEASURED
    return MeterReading(
        **_envelope(
            entity_id=f"reading:{cim.meter_mrid}:{cim.timestamp.isoformat()}",
            source_system=source_system,
            event_ts=cim.timestamp,
        ),
        meter_key=meter_key,
        timestamp=cim.timestamp,
        value=cim.value,
        unit=cim.unit.value,
        quality=quality,
    )  # type: ignore[arg-type]


def grid_event_from_cim(
    cim: CimEnergyEvent, *, source_system: str = "cim",
) -> GridEvent:
    """Translate a CIM EnergyEvent into an APEX ERCML GridEvent."""
    event_type = _CIM_TO_MAP_EVENT_TYPE.get(
        cim.event_type.lower(), GridEventType.OTHER
    )
    return GridEvent(
        **_envelope(
            entity_id=f"grid_event:{cim.m_rid}",
            source_system=source_system,
            event_ts=cim.occurred.start,
        ),
        cim_mrid=cim.m_rid,
        event_type=event_type,
        occurred_start=cim.occurred.start,
        occurred_end=cim.occurred.end,
        equipment_key=cim.equipment_mrid,
        severity=cim.severity,
        description=cim.description,
    )  # type: ignore[arg-type]


def asset_from_cim(cim: CimAsset, *, source_system: str = "cim") -> Asset:
    """Translate a CIM Asset into an APEX ERCML Asset."""
    state = AssetLifecycleState.IN_SERVICE
    if cim.lifecycle_state:
        try:
            state = AssetLifecycleState(cim.lifecycle_state.lower().replace(" ", "_"))
        except ValueError:
            state = AssetLifecycleState.IN_SERVICE
    return Asset(
        **_envelope(entity_id=f"asset:{cim.m_rid}", source_system=source_system),
        **_scd2(cim.in_service_date),
        cim_mrid=cim.m_rid,
        name=cim.name or cim.m_rid,
        asset_type=cim.asset_type,
        location_key=cim.location_mrid,
        in_service_date=cim.in_service_date,
        lifecycle_state=state,
    )  # type: ignore[arg-type]


def work_order_from_cim(
    cim: CimWorkOrder, *, source_system: str = "cim",
) -> WorkOrder:
    """Translate a CIM WorkOrder into an APEX ERCML WorkOrder."""
    status = WorkOrderStatus.OPEN
    try:
        status = WorkOrderStatus(cim.status.lower().replace(" ", "_"))
    except ValueError:
        status = WorkOrderStatus.OPEN
    return WorkOrder(
        **_envelope(
            entity_id=f"wo:{cim.m_rid}",
            source_system=source_system,
            event_ts=cim.created,
        ),
        cim_mrid=cim.m_rid,
        work_order_number=cim.work_order_number,
        status=status,
        priority=cim.priority,
        created=cim.created,
        scheduled=cim.scheduled,
        asset_key=cim.asset_mrid,
        description=cim.description,
    )  # type: ignore[arg-type]
