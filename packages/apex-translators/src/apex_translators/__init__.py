"""APEX message-format translators — Sprint 23.

Bidirectional (parser + emitter) translators for enterprise message
formats so SORs speaking EDI X12, HL7 v2, EPCIS 2.0, OAGIS, and one-way
ingest from HL7 CDA and IATA PADIS integrate to APEX canonical Silver
without bespoke per-engagement parsing.

Public API:

- :class:`ParsedMessage` — format-neutral intermediate representation
- :func:`parse_x12`, :func:`emit_x12` — EDI X12 (Task 23.1)
- :func:`parse_hl7v2`, :func:`emit_hl7v2`, :func:`strip_mllp`, :func:`wrap_mllp` — HL7 v2 (Task 23.2)
- :func:`parse_cda` — HL7 CDA / C-CDA, one-way (Task 23.3)
- :func:`parse_epcis`, :func:`emit_epcis_json` — EPCIS 2.0 (Task 23.4)
- :func:`parse_oagis`, :func:`emit_oagis` — OAGIS BOD (Task 23.5)
- :func:`parse_padis` — IATA PADIS, one-way (Task 23.6)
"""

from __future__ import annotations

from apex_translators.base import (
    FORMAT_CDA,
    FORMAT_EDI_X12,
    FORMAT_EPCIS,
    FORMAT_HL7V2,
    FORMAT_OAGIS,
    FORMAT_PADIS,
    SUPPORTED_FORMATS,
    EmitError,
    Emitter,
    ParseError,
    ParsedMessage,
    Parser,
    Segment,
    TranslatorError,
)
from apex_translators.cda import parse_cda
from apex_translators.cross_standard import (
    AEMP_EVENT_TYPES,
    CIM_ISO_EQUIPMENT_MAP,
    J1939_PGN_MAP,
    aemp_to_j1939,
    cda_to_fhir,
    cim_to_iso15926,
    hl7v2_to_fhir,
    iso15926_to_cim,
    j1939_to_aemp,
)
from apex_translators.edi_x12 import emit_x12, parse_x12
from apex_translators.epcis import emit_epcis_json, parse_epcis
from apex_translators.hl7v2 import (
    emit_hl7v2,
    parse_hl7v2,
    strip_mllp,
    wrap_mllp,
)
from apex_translators.oagis import emit_oagis, parse_oagis
from apex_translators.padis import parse_padis

__all__ = [
    "AEMP_EVENT_TYPES",
    "CIM_ISO_EQUIPMENT_MAP",
    "EmitError",
    "Emitter",
    "FORMAT_CDA",
    "FORMAT_EDI_X12",
    "FORMAT_EPCIS",
    "FORMAT_HL7V2",
    "FORMAT_OAGIS",
    "FORMAT_PADIS",
    "J1939_PGN_MAP",
    "ParseError",
    "ParsedMessage",
    "Parser",
    "SUPPORTED_FORMATS",
    "Segment",
    "TranslatorError",
    "aemp_to_j1939",
    "cda_to_fhir",
    "cim_to_iso15926",
    "emit_epcis_json",
    "emit_hl7v2",
    "emit_oagis",
    "emit_x12",
    "hl7v2_to_fhir",
    "iso15926_to_cim",
    "j1939_to_aemp",
    "parse_cda",
    "parse_epcis",
    "parse_hl7v2",
    "parse_oagis",
    "parse_padis",
    "parse_x12",
    "strip_mllp",
    "wrap_mllp",
]

__version__ = "0.1.0"
