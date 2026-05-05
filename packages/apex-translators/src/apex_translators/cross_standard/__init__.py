"""Cross-standard translators — Sprint 24 (BL.P.161-165).

Each translator takes content expressed in one standard and renders the
equivalent in another. Where the two standards share full information
density, translation is bidirectional and round-trips. Where one standard
is a strict superset, the lossy direction is documented in
``LOSSY_CASES.md`` per Sprint 24 exit criterion.

Translators shipped:

- :func:`hl7v2_to_fhir` — HL7 v2.x ADT / ORU → FHIR R4 Bundle (Task 24.2)
- :func:`cda_to_fhir` — HL7 CDA / C-CDA → FHIR R4 Bundle (Task 24.3)
- :func:`cim_to_iso15926`, :func:`iso15926_to_cim` — power-grid ↔ process
  asset class translation (Task 24.4)
- :func:`j1939_to_aemp`, :func:`aemp_to_j1939` — telematics CAN-frame ↔
  AEMP 2.0 cross-OEM fleet event translation (Task 24.5)

Note: GS1 ↔ Schema.org Product translation (Task 24.1) lives in
``apex-scml/translators`` per its original Sprint 3 home.
"""

from apex_translators.cross_standard.cim_iso15926 import (
    CIM_ISO_EQUIPMENT_MAP,
    cim_to_iso15926,
    iso15926_to_cim,
)
from apex_translators.cross_standard.fhir_r4 import (
    cda_to_fhir,
    hl7v2_to_fhir,
)
from apex_translators.cross_standard.j1939_aemp import (
    AEMP_EVENT_TYPES,
    J1939_PGN_MAP,
    aemp_to_j1939,
    j1939_to_aemp,
)

__all__ = [
    "AEMP_EVENT_TYPES",
    "CIM_ISO_EQUIPMENT_MAP",
    "J1939_PGN_MAP",
    "aemp_to_j1939",
    "cda_to_fhir",
    "cim_to_iso15926",
    "hl7v2_to_fhir",
    "iso15926_to_cim",
    "j1939_to_aemp",
]
