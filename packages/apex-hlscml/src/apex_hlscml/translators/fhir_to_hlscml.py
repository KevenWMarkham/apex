"""FHIR → HLSCML translators (Pattern D — Pattern C materialised).

Every ``_token`` field is tokenised at the boundary; cleartext never lands in
the returned HLSCML instance.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from apex_standards_fhir import FhirObservation, FhirPatient

from apex_hlscml.entities import Observation, ObservationStatus, Patient
from apex_hlscml.translators._tokenize import tokenize


def _envelope(
    *,
    entity_id: str,
    source_system: str,
    event_ts: datetime | None = None,
    source_system_ts: datetime | None = None,
    event_id: UUID | None = None,
) -> dict[str, Any]:
    """Produce a default canonical-envelope kwargs dict."""
    now = datetime.now(UTC)
    return {
        "event_id": event_id or uuid4(),
        "event_ts": event_ts or now,
        "entity_id": entity_id,
        "source_system": source_system,
        "source_system_ts": source_system_ts or now,
    }


def _first_usual_identifier(fhir: FhirPatient) -> tuple[str | None, str | None]:
    """Return the ``(value, system)`` of the 'usual' identifier, or the first."""
    for ident in fhir.identifier:
        if ident.use == "usual" and ident.value:
            return ident.value, ident.system
    for ident in fhir.identifier:
        if ident.value:
            return ident.value, ident.system
    return None, None


def _first_official_name(fhir: FhirPatient) -> tuple[str | None, str | None]:
    """Return ``(family, given_first)`` from the 'official' HumanName, or the first."""
    for name in fhir.name:
        if name.use == "official":
            return name.family, (name.given[0] if name.given else None)
    if fhir.name:
        first = fhir.name[0]
        return first.family, (first.given[0] if first.given else None)
    return None, None


def _first_telecom(fhir: FhirPatient, system: str) -> str | None:
    for t in fhir.telecom:
        if t.system == system and t.value:
            return t.value
    return None


def _first_address_text(fhir: FhirPatient) -> str | None:
    """Return the best-available free-text address."""
    for addr in fhir.address:
        if addr.text:
            return addr.text
        parts = [*addr.line, addr.city, addr.state, addr.postal_code, addr.country]
        joined = " ".join(p for p in parts if p)
        if joined.strip():
            return joined
    return None


def patient_from_fhir(
    fhir: FhirPatient,
    *,
    source_system: str = "fhir",
    scd2_row_hash: str = "na",
) -> Patient:
    """Translate a FHIR R4 Patient resource into an APEX HLSCML Patient.

    All direct identifiers are tokenised at the boundary.
    """
    mrn_value, mrn_system = _first_usual_identifier(fhir)
    family, given = _first_official_name(fhir)
    now = datetime.now(UTC)

    return Patient(
        # Canonical envelope
        **_envelope(entity_id=f"patient:{fhir.id}", source_system=source_system),
        # SCD2
        scd2_valid_from=now,
        scd2_is_current=True,
        row_hash=scd2_row_hash,
        # FHIR-carried (tokenised)
        fhir_id=fhir.id or "",
        mrn_token=tokenize(mrn_value),
        mrn_system=mrn_system,
        name_family_token=tokenize(family),
        name_given_token=tokenize(given),
        gender=fhir.gender,
        birth_date=fhir.birth_date,
        deceased=fhir.deceased_boolean,
        address_token=tokenize(_first_address_text(fhir)),
        phone_token=tokenize(_first_telecom(fhir, "phone")),
        email_token=tokenize(_first_telecom(fhir, "email")),
        source_fhir_version="R4",
    )  # type: ignore[arg-type]


def observation_from_fhir(
    fhir: FhirObservation,
    *,
    patient_key: str,
    encounter_key: str | None = None,
    source_system: str = "fhir",
) -> Observation:
    """Translate a FHIR R4 Observation into an APEX HLSCML Observation."""
    loinc_code: str | None = None
    code_display = fhir.code.text or ""
    for coding in fhir.code.coding:
        if coding.system == "http://loinc.org" and coding.code:
            loinc_code = coding.code
            if not code_display and coding.display:
                code_display = coding.display
            break

    vq = fhir.value_quantity
    value_numeric: Decimal | None = None
    value_unit: str | None = None
    if vq is not None and vq.value is not None:
        value_numeric = Decimal(str(vq.value))
        value_unit = vq.unit

    value_code: str | None = None
    if fhir.value_codeable_concept:
        for coding in fhir.value_codeable_concept.coding:
            if coding.code:
                value_code = coding.code
                break

    return Observation(
        **_envelope(
            entity_id=f"observation:{fhir.id}",
            source_system=source_system,
            event_ts=fhir.effective_date_time,
        ),
        fhir_id=fhir.id or "",
        status=ObservationStatus(fhir.status),
        loinc_code=loinc_code,
        code_display=code_display,
        patient_key=patient_key,
        encounter_key=encounter_key,
        effective_ts=fhir.effective_date_time or datetime.now(UTC),
        value_numeric=value_numeric,
        value_unit=value_unit,
        value_code=value_code,
        value_string=fhir.value_string,
    )  # type: ignore[arg-type]
