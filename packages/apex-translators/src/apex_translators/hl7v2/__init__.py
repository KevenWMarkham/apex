"""HL7 v2.x parser + emitter — Sprint 23 Task 23.2 (BL.P.156).

Supports the named segment library (MSH, PID, PV1, OBX, OBR, ORC, RXE, AL1)
across v2.5.1 and v2.7 dialects. Includes MLLP framing helpers for wire-level
boundary detection and stripping.
"""

from apex_translators.hl7v2.parser import (
    HL7v2Delimiters,
    HL7v2Parser,
    SUPPORTED_SEGMENTS,
    parse_hl7v2,
    strip_mllp,
)
from apex_translators.hl7v2.emitter import HL7v2Emitter, emit_hl7v2, wrap_mllp

__all__ = [
    "HL7v2Delimiters",
    "HL7v2Emitter",
    "HL7v2Parser",
    "SUPPORTED_SEGMENTS",
    "emit_hl7v2",
    "parse_hl7v2",
    "strip_mllp",
    "wrap_mllp",
]
