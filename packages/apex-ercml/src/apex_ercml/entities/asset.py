"""ERCML Asset entity — Pattern C over CIM Asset (IEC 61968-4)."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity, ScdType2Fields


class AssetLifecycleState(StrEnum):
    PLANNED = "planned"
    IN_SERVICE = "in_service"
    OUT_OF_SERVICE = "out_of_service"
    RETIRED = "retired"
    SCRAPPED = "scrapped"


class Asset(CanonicalEntity, ScdType2Fields):
    """A physical or logical asset on the utility network."""

    cim_mrid: str = Field(..., description="CIM Master Resource Identifier.")
    name: str
    asset_type: str | None = Field(
        None, description="e.g. 'PowerTransformer', 'Conductor', 'SwitchDisconnector'."
    )
    location_key: str | None = None
    in_service_date: datetime | None = None
    lifecycle_state: AssetLifecycleState = AssetLifecycleState.IN_SERVICE
    manufacturer: str | None = None
    model: str | None = None
    rated_voltage_kv: float | None = Field(None, ge=0.0)
