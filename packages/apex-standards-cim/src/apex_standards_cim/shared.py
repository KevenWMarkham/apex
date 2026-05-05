"""CIM shared primitives — MRID, DateTimeInterval, UnitSymbol."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

MRID = Annotated[
    str,
    StringConstraints(pattern=r"^[0-9a-fA-F\-_\.:a-zA-Z0-9]{1,128}$", min_length=1),
]
"""CIM Master Resource Identifier — typically UUID but permissive per IEC 61970-301."""


class UnitSymbol(StrEnum):
    """Subset of IEC 61970-301 unit symbols used by ER reference deployments."""

    NONE = "none"
    W = "W"                 # watt
    VAR = "VAr"             # volt-ampere reactive
    VA = "VA"               # volt-ampere
    V = "V"                 # volt
    A = "A"                 # ampere
    OHM = "ohm"
    HZ = "Hz"
    DEG_C = "degC"
    K = "K"                 # kelvin
    KW = "kW"
    KWH = "kWh"
    MW = "MW"
    MWH = "MWh"
    GW = "GW"
    GWH = "GWh"
    M3 = "m3"
    KG = "kg"
    PCT = "percent"


class DateTimeInterval(BaseModel):
    """CIM DateTimeInterval — a start/end pair."""

    model_config = ConfigDict(extra="forbid")
    start: datetime
    end: datetime | None = None
