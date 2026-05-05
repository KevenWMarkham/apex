"""HL7 v2.x → FHIR R4 translator (stub).

Sprint 3 Phase 2 ships signatures + one fixture-level smoke translation.
Full parser lands in BL.P.156 in a later sprint.
"""

from __future__ import annotations

from apex_standards_fhir import FhirHumanName, FhirPatient


def adt_a01_to_fhir_patient_stub(adt_a01_message: str) -> FhirPatient:
    """Stub: parse the PID segment of an ADT^A01 HL7 v2 message.

    Sprint 3 implementation only honours enough of the PID segment to
    emit a :class:`FhirPatient` with ``id`` and ``name.family``. Everything
    else is ignored. Do not use in production.

    Args:
        adt_a01_message: Raw HL7 v2 message text (pipe-delimited).

    Returns:
        A FHIR Patient assembled from the PID segment.
    """
    pid_line = next(
        (line for line in adt_a01_message.splitlines() if line.startswith("PID|")),
        None,
    )
    if pid_line is None:
        return FhirPatient(resourceType="Patient")  # type: ignore[call-arg]

    fields = pid_line.split("|")
    # PID.3 Patient Identifier List
    patient_id = fields[3].split("^")[0] if len(fields) > 3 and fields[3] else None
    # PID.5 Patient Name — format: Family^Given
    name: FhirHumanName | None = None
    if len(fields) > 5 and fields[5]:
        parts = fields[5].split("^")
        family = parts[0] if parts else None
        given = [parts[1]] if len(parts) > 1 and parts[1] else []
        name = FhirHumanName(family=family, given=given)

    return FhirPatient(
        resourceType="Patient",  # type: ignore[call-arg]
        id=patient_id,
        name=[name] if name else [],
    )
