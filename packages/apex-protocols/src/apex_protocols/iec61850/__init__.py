"""IEC 61850 adapter core — Sprint 25 Task 25.2 (BL.P.167).

SCD (Substation Configuration Description) file parser, MMS client
interface, GOOSE / SV awareness (metadata only — raw frames stay in OT
domain per Sprint 25 §25.2.3).
"""

from apex_protocols.iec61850.client import IEC61850StubClient
from apex_protocols.iec61850.scd import (
    GOOSEControlBlock,
    IED,
    LogicalDevice,
    LogicalNode,
    SVControlBlock,
    SCDDocument,
    parse_scd,
)

__all__ = [
    "GOOSEControlBlock",
    "IEC61850StubClient",
    "IED",
    "LogicalDevice",
    "LogicalNode",
    "SVControlBlock",
    "SCDDocument",
    "parse_scd",
]
