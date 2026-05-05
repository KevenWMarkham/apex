"""HLSCML → FHIR translators.

Detokenises ``_token`` fields only for authorised identities. The Sprint 3
placeholder unconditionally detokenises; the Sprint 5 runtime will gate on
the visibility lattice (see ``apex-identity`` Sprint 10).
"""

from __future__ import annotations

from apex_standards_fhir import (
    FhirAddress,
    FhirCodeableConcept,
    FhirCoding,
    FhirContactPoint,
    FhirHumanName,
    FhirIdentifier,
    FhirObservation,
    FhirPatient,
    FhirQuantity,
    FhirReference,
)

from apex_hlscml.entities import Observation, Patient
from apex_hlscml.translators._tokenize import detokenize


def patient_to_fhir(patient: Patient, *, detokenise: bool = True) -> FhirPatient:
    """Render an APEX HLSCML Patient as a FHIR R4 Patient.

    Args:
        patient: The APEX canonical Patient.
        detokenise: If ``False``, emit tokens as-is (raw-token export — useful
            for downstream systems that must not see cleartext). Default
            ``True`` recovers cleartext for authorised consumers.
    """
    transform = detokenize if detokenise else (lambda x: x)

    identifiers = []
    if patient.mrn_token:
        identifiers.append(
            FhirIdentifier(
                use="usual",
                system=patient.mrn_system,
                value=transform(patient.mrn_token),
            )
        )

    names = []
    family = transform(patient.name_family_token)
    given = transform(patient.name_given_token)
    if family or given:
        names.append(
            FhirHumanName(
                use="official",
                family=family,
                given=[given] if given else [],
            )
        )

    telecom = []
    phone = transform(patient.phone_token)
    if phone:
        telecom.append(FhirContactPoint(system="phone", value=phone))
    email = transform(patient.email_token)
    if email:
        telecom.append(FhirContactPoint(system="email", value=email))

    addresses = []
    addr = transform(patient.address_token)
    if addr:
        addresses.append(FhirAddress(text=addr))

    return FhirPatient(
        resourceType="Patient",  # type: ignore[call-arg]
        id=patient.fhir_id or None,
        identifier=identifiers,
        name=names,
        telecom=telecom,
        gender=patient.gender,
        birthDate=patient.birth_date,  # type: ignore[call-arg]
        deceasedBoolean=patient.deceased,  # type: ignore[call-arg]
        address=addresses,
    )


def observation_to_fhir(obs: Observation) -> FhirObservation:
    """Render an APEX HLSCML Observation as a FHIR R4 Observation."""
    code_coding = []
    if obs.loinc_code:
        code_coding.append(
            FhirCoding(
                system="http://loinc.org",
                code=obs.loinc_code,
                display=obs.code_display or None,
            )
        )
    code = FhirCodeableConcept(coding=code_coding, text=obs.code_display or None)

    value_quantity: FhirQuantity | None = None
    if obs.value_numeric is not None:
        value_quantity = FhirQuantity(
            value=float(obs.value_numeric),
            unit=obs.value_unit,
        )

    return FhirObservation(
        resourceType="Observation",  # type: ignore[call-arg]
        id=obs.fhir_id or None,
        status=obs.status.value,
        code=code,
        subject=FhirReference(reference=f"Patient/{obs.patient_key}"),
        encounter=(
            FhirReference(reference=f"Encounter/{obs.encounter_key}")
            if obs.encounter_key else None
        ),
        effectiveDateTime=obs.effective_ts,  # type: ignore[call-arg]
        valueQuantity=value_quantity,  # type: ignore[call-arg]
        valueString=obs.value_string,  # type: ignore[call-arg]
    )
