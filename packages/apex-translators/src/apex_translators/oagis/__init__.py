"""OAGIS BOD parser + emitter — Sprint 23 Task 23.5 (BL.P.159).

OAGIS Business Object Documents (BODs) wrap a Verb (`Get`, `Process`,
`Sync`, `Acknowledge`, `Show`, `Confirm`, `Notify`, `Cancel`) and a Noun
(`Item`, `Carrier`, `ManufacturingFacility`, etc.) inside an
ApplicationArea + DataArea envelope. Used by AXLE supplier EDI + MES
integrations.
"""

from apex_translators.oagis.parser import (
    OAGIS_VERBS,
    OAGISParser,
    parse_oagis,
)
from apex_translators.oagis.emitter import OAGISEmitter, emit_oagis

__all__ = [
    "OAGIS_VERBS",
    "OAGISEmitter",
    "OAGISParser",
    "emit_oagis",
    "parse_oagis",
]
