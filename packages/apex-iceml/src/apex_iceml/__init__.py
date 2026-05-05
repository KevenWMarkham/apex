"""APEX ICEML — Industrial & Commercial Equipment canonical entities."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields
from apex_standards_iso14224 import Iso14224EquipmentClass, Iso14224FailureMode


# --- Pattern-A identifier type ---------------------------------------------

Vin17 = Annotated[
    str,
    StringConstraints(pattern=r"^[A-HJ-NPR-Z0-9]{17}$"),
]
"""17-character Vehicle Identification Number (ISO 3779). No I, O, Q."""


# --- Entities --------------------------------------------------------------


class IceEquipmentKind(StrEnum):
    TRUCK = "truck"
    TRACTOR = "tractor"
    EXCAVATOR = "excavator"
    LOADER = "loader"
    DOZER = "dozer"
    HARVESTER = "harvester"
    SPRAYER = "sprayer"
    GENSET = "genset"
    OTHER = "other"


class IceEquipment(CanonicalEntity, ScdType2Fields):
    """A single industrial / commercial equipment unit."""

    aemp_equipment_id: str = Field(..., description="AEMP 2.0 Equipment Id.")
    vin17: Vin17 | None = Field(None, description="17-char VIN for on-road equipment.")
    serial_number: str
    kind: IceEquipmentKind = IceEquipmentKind.OTHER
    make: str | None = None
    model: str | None = None
    model_year: int | None = Field(None, ge=1900, le=2100)
    in_service_date: date | None = None
    customer_account_token: Annotated[str, Classification.PII] | None = None


class TelemetryQuality(StrEnum):
    RAW = "raw"
    DECODED = "decoded"
    DERIVED = "derived"


class TelemetryReading(CanonicalEntity):
    """A point-in-time telemetry snapshot (AEMP 2.0-aligned)."""

    equipment_key: str = Field(..., description="FK → IceEquipment.entity_id.")
    captured_at: datetime
    latitude: float | None = Field(None, ge=-90.0, le=90.0)
    longitude: float | None = Field(None, ge=-180.0, le=180.0)
    engine_hours: Decimal | None = None
    odometer_km: Decimal | None = None
    fuel_level_pct: Decimal | None = Field(None, ge=Decimal("0"), le=Decimal("100"))
    def_level_pct: Decimal | None = Field(None, ge=Decimal("0"), le=Decimal("100"))
    quality: TelemetryQuality = TelemetryQuality.DECODED
    j1939_signal_keys: list[str] = Field(
        default_factory=list,
        description="FKs to per-SPN signal rows backing this snapshot.",
    )


class ServiceEventSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ServiceEvent(CanonicalEntity):
    """A fault / warning / anomaly surfaced by equipment telemetry."""

    equipment_key: str = Field(..., description="FK → IceEquipment.entity_id.")
    occurred_at: datetime
    oem_fault_code: str | None = Field(
        None, description="OEM service / diagnostic trouble code."
    )
    j1939_spn: int | None = Field(None, ge=0)
    severity: ServiceEventSeverity = ServiceEventSeverity.INFO
    failure_mode: Iso14224FailureMode | None = None
    description: str = ""
    acknowledged: bool = False


class MaintenanceKind(StrEnum):
    SCHEDULED = "scheduled"
    UNPLANNED = "unplanned"
    PREDICTIVE = "predictive"
    RECALL = "recall"
    WARRANTY = "warranty"


class MaintenanceRecord(CanonicalEntity):
    """A maintenance event — scheduled or completed."""

    equipment_key: str = Field(..., description="FK → IceEquipment.entity_id.")
    kind: MaintenanceKind = MaintenanceKind.SCHEDULED
    scheduled_at: datetime | None = None
    completed_at: datetime | None = None
    work_description: str = ""
    parts_replaced: list[str] = Field(default_factory=list)
    labor_hours: Decimal | None = Field(None, ge=Decimal("0"))
    cost_usd: Decimal | None = Field(None, ge=Decimal("0"))
    service_event_key: str | None = Field(
        None, description="FK → ServiceEvent that triggered this maintenance."
    )
    equipment_class: Iso14224EquipmentClass | None = None


class FleetMember(CanonicalEntity):
    """Edge associating an IceEquipment to a fleet (AEMP 2.0)."""

    equipment_key: str
    fleet_id: str
    assigned_from: date | None = None
    assigned_to: date | None = None
    is_active: bool = True


# --- Translator ------------------------------------------------------------


class AempSnapshotInput(BaseModel):
    """Minimal AEMP 2.0 snapshot payload (placeholder shape for Sprint 3).

    The full AEMP 2.0 mirror lives in the ICE telematics adapter (Sprint 15).
    Sprint 3 ships this thin shape so ``iceml_from_aemp`` can round-trip
    a representative snapshot for testing.
    """

    model_config = ConfigDict(extra="forbid")

    equipment_id: str
    timestamp: datetime
    latitude: float | None = None
    longitude: float | None = None
    engine_hours: Decimal | None = None
    odometer_km: Decimal | None = None
    fuel_level_pct: Decimal | None = None


def _envelope(*, entity_id: str, event_ts: datetime, source_system: str = "aemp") -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": event_ts,
        "entity_id": entity_id,
        "source_system": source_system,
        "source_system_ts": datetime.now(UTC),
    }


def telemetry_reading_from_aemp(
    aemp: AempSnapshotInput,
    *,
    equipment_key: str,
    source_system: str = "aemp",
) -> TelemetryReading:
    """Translate an AEMP 2.0 snapshot into an APEX ICEML TelemetryReading."""
    return TelemetryReading(
        **_envelope(
            entity_id=f"telemetry:{aemp.equipment_id}:{aemp.timestamp.isoformat()}",
            event_ts=aemp.timestamp,
            source_system=source_system,
        ),
        equipment_key=equipment_key,
        captured_at=aemp.timestamp,
        latitude=aemp.latitude,
        longitude=aemp.longitude,
        engine_hours=aemp.engine_hours,
        odometer_km=aemp.odometer_km,
        fuel_level_pct=aemp.fuel_level_pct,
        quality=TelemetryQuality.DECODED,
    )  # type: ignore[arg-type]


__all__ = [
    "AempSnapshotInput",
    "FleetMember",
    "IceEquipment",
    "IceEquipmentKind",
    "MaintenanceKind",
    "MaintenanceRecord",
    "ServiceEvent",
    "ServiceEventSeverity",
    "TelemetryQuality",
    "TelemetryReading",
    "Vin17",
    "telemetry_reading_from_aemp",
]
