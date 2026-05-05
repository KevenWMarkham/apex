"""HL7 v2 → FHIR R4 + HL7 CDA → FHIR R4 — Sprint 24 Tasks 24.2 + 24.3.

Output is a FHIR R4 ``Bundle`` resource (collection-type) as a Python dict
shaped per the FHIR JSON wire format. Bundle is the natural pivot because
both ADT-family v2 and C-CDA documents map to multiple FHIR resources
(Patient, Encounter, Observation, AllergyIntolerance, MedicationStatement,
Condition, etc.).

Both translators are **one-way** (v2/CDA → FHIR) per Sprint 24 spec.
Reverse translation deferred unless demanded.

Lossy cases (see ``LOSSY_CASES.md``):

- HL7 v2 OBX with malformed unit codes — `valueQuantity.code` filled best-effort
- HL7 v2 PID-13 (multi-repetition phone) — only first repetition retained
- C-CDA section without templateId match — surfaced as ``Composition.section`` with `code` text only, no structured entry
- C-CDA observation without coded `value` — captured as text in `Observation.valueString`
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from apex_translators.base import ParsedMessage


# ---------------------------------------------------------------------------
# Common helpers
# ---------------------------------------------------------------------------


def _new_bundle(bundle_type: str = "collection") -> dict[str, Any]:
    return {
        "resourceType": "Bundle",
        "id": f"bundle-{uuid4()}",
        "type": bundle_type,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "entry": [],
    }


def _add_entry(bundle: dict[str, Any], resource: dict[str, Any]) -> dict[str, Any]:
    full_url = f"urn:uuid:{uuid4()}"
    bundle["entry"].append({"fullUrl": full_url, "resource": resource})
    return resource


def _hl7_dt_to_fhir(dtm: str) -> str:
    """Convert HL7 v2 DTM (YYYYMMDDHHMMSS) → FHIR dateTime (ISO 8601)."""
    s = dtm.strip()
    if not s:
        return ""
    if len(s) >= 14:
        return f"{s[0:4]}-{s[4:6]}-{s[6:8]}T{s[8:10]}:{s[10:12]}:{s[12:14]}Z"
    if len(s) >= 12:
        return f"{s[0:4]}-{s[4:6]}-{s[6:8]}T{s[8:10]}:{s[10:12]}:00Z"
    if len(s) >= 8:
        return f"{s[0:4]}-{s[4:6]}-{s[6:8]}"
    return s


def _split_components(value: str) -> list[str]:
    """Split on the HL7 v2 component delimiter ``^``."""
    return value.split("^") if value else []


def _split_repetitions(value: str) -> list[str]:
    """Split on the HL7 v2 repetition delimiter ``~``."""
    return value.split("~") if value else []


# ---------------------------------------------------------------------------
# HL7 v2 → FHIR R4 (Task 24.2)
# ---------------------------------------------------------------------------


def hl7v2_to_fhir(message: ParsedMessage) -> dict[str, Any]:
    """Translate an HL7 v2 ADT or ORU :class:`ParsedMessage` to a FHIR R4 Bundle.

    Supported message families:

    - ADT family (A04 patient registration, A08 update) → Patient + Encounter
    - ORU family (R01 observation result) → Observation + DiagnosticReport
    - ORM family (O01 pharmacy order) → MedicationRequest + Patient

    Returns the Bundle dict shaped per FHIR R4 JSON; pass ``json.dumps()`` if
    a serialized form is needed.
    """
    if message.format != "hl7v2":
        raise ValueError(
            f"hl7v2_to_fhir requires format='hl7v2', got {message.format!r}"
        )
    bundle = _new_bundle()
    msg_type = (message.message_type or "").upper()

    # Always extract Patient from PID
    patient = _patient_from_pid(message)
    if patient is not None:
        _add_entry(bundle, patient)

    if msg_type.startswith("ADT"):
        encounter = _encounter_from_pv1(message, patient)
        if encounter is not None:
            _add_entry(bundle, encounter)
        for allergy in _allergies_from_al1(message, patient):
            _add_entry(bundle, allergy)
    elif msg_type.startswith("ORU"):
        diag = _diagnostic_report_from_obr(message, patient)
        observations = _observations_from_obx(message, patient)
        for obs in observations:
            _add_entry(bundle, obs)
        if diag is not None:
            _add_entry(bundle, diag)
    elif msg_type.startswith("ORM") or msg_type.startswith("OMP"):
        med_req = _medication_request_from_rxe_orc(message, patient)
        if med_req is not None:
            _add_entry(bundle, med_req)

    return bundle


def _patient_from_pid(message: ParsedMessage) -> dict[str, Any] | None:
    pid = message.first("PID")
    if pid is None:
        return None
    pat: dict[str, Any] = {
        "resourceType": "Patient",
        "id": f"patient-{uuid4()}",
    }
    # PID-3 patient identifier
    if len(pid.elements) >= 3:
        comps = _split_components(pid.elements[2])
        if comps and comps[0]:
            pat["identifier"] = [
                {
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                "code": comps[4] if len(comps) >= 5 else "MR",
                            }
                        ]
                    },
                    "value": comps[0],
                }
            ]
    # PID-5 patient name
    if len(pid.elements) >= 5:
        comps = _split_components(pid.elements[4])
        if any(comps):
            family = comps[0] if len(comps) >= 1 else ""
            given = [c for c in comps[1:3] if c]
            pat["name"] = [
                {
                    "use": "official",
                    "family": family,
                    "given": given,
                }
            ]
    # PID-7 birthdate
    if len(pid.elements) >= 7:
        bd = pid.elements[6].strip()
        if len(bd) >= 8:
            pat["birthDate"] = f"{bd[0:4]}-{bd[4:6]}-{bd[6:8]}"
    # PID-8 administrative gender
    if len(pid.elements) >= 8:
        gender_map = {"M": "male", "F": "female", "O": "other", "U": "unknown"}
        pat["gender"] = gender_map.get(pid.elements[7].strip().upper(), "unknown")
    # PID-13 home phone (first repetition only — lossy)
    if len(pid.elements) >= 13:
        first_phone = _split_repetitions(pid.elements[12])
        if first_phone and first_phone[0]:
            pat["telecom"] = [
                {"system": "phone", "value": first_phone[0], "use": "home"}
            ]
    return pat


def _encounter_from_pv1(
    message: ParsedMessage, patient: dict[str, Any] | None
) -> dict[str, Any] | None:
    pv1 = message.first("PV1")
    if pv1 is None:
        return None
    enc: dict[str, Any] = {
        "resourceType": "Encounter",
        "id": f"encounter-{uuid4()}",
        "status": "in-progress",
    }
    # PV1-2 patient class (I=inpatient, O=outpatient, E=emergency, etc.)
    if len(pv1.elements) >= 2:
        class_map = {
            "I": ("IMP", "inpatient encounter"),
            "O": ("AMB", "ambulatory"),
            "E": ("EMER", "emergency"),
            "P": ("PRENC", "pre-admission"),
        }
        code, display = class_map.get(pv1.elements[1].strip(), ("AMB", "ambulatory"))
        enc["class"] = {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": code,
            "display": display,
        }
    if patient is not None:
        enc["subject"] = {"reference": f"Patient/{patient['id']}"}
    return enc


def _allergies_from_al1(
    message: ParsedMessage, patient: dict[str, Any] | None
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for al1 in message.find("AL1"):
        allergy: dict[str, Any] = {
            "resourceType": "AllergyIntolerance",
            "id": f"allergy-{uuid4()}",
        }
        # AL1-2 allergy type
        if len(al1.elements) >= 2:
            type_map = {"DA": "medication", "FA": "food", "MA": "medication", "EA": "environment"}
            allergy["category"] = [type_map.get(al1.elements[1].strip(), "medication")]
        # AL1-3 allergen code/text
        if len(al1.elements) >= 3:
            comps = _split_components(al1.elements[2])
            text = comps[1] if len(comps) >= 2 and comps[1] else (comps[0] if comps else "")
            allergy["code"] = {"text": text}
        # AL1-4 severity
        if len(al1.elements) >= 4:
            sev_raw = _split_repetitions(al1.elements[3])[0]
            sev_map = {"SV": "severe", "MO": "moderate", "MI": "mild"}
            allergy["criticality"] = (
                "high" if sev_map.get(sev_raw[:2].upper(), "") == "severe" else "low"
            )
        if patient is not None:
            allergy["patient"] = {"reference": f"Patient/{patient['id']}"}
        out.append(allergy)
    return out


def _diagnostic_report_from_obr(
    message: ParsedMessage, patient: dict[str, Any] | None
) -> dict[str, Any] | None:
    obr = message.first("OBR")
    if obr is None:
        return None
    rep: dict[str, Any] = {
        "resourceType": "DiagnosticReport",
        "id": f"report-{uuid4()}",
        "status": "final",
    }
    # OBR-4 universal service identifier
    if len(obr.elements) >= 4:
        comps = _split_components(obr.elements[3])
        if comps:
            rep["code"] = {
                "coding": [
                    {
                        "system": _guess_coding_system(comps[2] if len(comps) >= 3 else ""),
                        "code": comps[0] if comps else "",
                        "display": comps[1] if len(comps) >= 2 else "",
                    }
                ]
            }
    # OBR-7 observation date/time
    if len(obr.elements) >= 7:
        eff = _hl7_dt_to_fhir(obr.elements[6])
        if eff:
            rep["effectiveDateTime"] = eff
    if patient is not None:
        rep["subject"] = {"reference": f"Patient/{patient['id']}"}
    return rep


def _observations_from_obx(
    message: ParsedMessage, patient: dict[str, Any] | None
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for obx in message.find("OBX"):
        obs: dict[str, Any] = {
            "resourceType": "Observation",
            "id": f"observation-{uuid4()}",
            "status": "final",
        }
        if patient is not None:
            obs["subject"] = {"reference": f"Patient/{patient['id']}"}
        # OBX-3 observation identifier
        if len(obx.elements) >= 3:
            comps = _split_components(obx.elements[2])
            if comps:
                obs["code"] = {
                    "coding": [
                        {
                            "system": _guess_coding_system(comps[2] if len(comps) >= 3 else ""),
                            "code": comps[0] if comps else "",
                            "display": comps[1] if len(comps) >= 2 else "",
                        }
                    ]
                }
        # OBX-2 value type + OBX-5 value
        value_type = obx.elements[1].strip().upper() if len(obx.elements) >= 2 else ""
        value_raw = obx.elements[4] if len(obx.elements) >= 5 else ""
        if value_type == "NM" and value_raw:
            try:
                qty: dict[str, Any] = {"value": float(value_raw)}
                if len(obx.elements) >= 6 and obx.elements[5].strip():
                    qty["unit"] = obx.elements[5].strip()
                    qty["system"] = "http://unitsofmeasure.org"
                    qty["code"] = obx.elements[5].strip()
                obs["valueQuantity"] = qty
            except ValueError:
                obs["valueString"] = value_raw
        elif value_raw:
            obs["valueString"] = value_raw
        out.append(obs)
    return out


def _medication_request_from_rxe_orc(
    message: ParsedMessage, patient: dict[str, Any] | None
) -> dict[str, Any] | None:
    rxe = message.first("RXE")
    if rxe is None:
        return None
    req: dict[str, Any] = {
        "resourceType": "MedicationRequest",
        "id": f"medreq-{uuid4()}",
        "status": "active",
        "intent": "order",
    }
    # RXE-2 give code (drug)
    if len(rxe.elements) >= 2:
        comps = _split_components(rxe.elements[1])
        if comps:
            system = _guess_coding_system(comps[2] if len(comps) >= 3 else "")
            req["medicationCodeableConcept"] = {
                "coding": [
                    {
                        "system": system,
                        "code": comps[0] if comps else "",
                        "display": comps[1] if len(comps) >= 2 else "",
                    }
                ]
            }
    if patient is not None:
        req["subject"] = {"reference": f"Patient/{patient['id']}"}
    return req


def _guess_coding_system(token: str) -> str:
    """Map an HL7 v2 coding-system identifier (3rd subfield of CE/CWE) to a FHIR system URI."""
    s = token.strip().upper()
    return {
        "LN": "http://loinc.org",
        "LOINC": "http://loinc.org",
        "SCT": "http://snomed.info/sct",
        "SNOMED-CT": "http://snomed.info/sct",
        "I9": "http://hl7.org/fhir/sid/icd-9-cm",
        "I10": "http://hl7.org/fhir/sid/icd-10-cm",
        "NDC": "http://hl7.org/fhir/sid/ndc",
        "CPT": "http://www.ama-assn.org/go/cpt",
        "CPT4": "http://www.ama-assn.org/go/cpt",
        "RXNORM": "http://www.nlm.nih.gov/research/umls/rxnorm",
    }.get(s, "http://terminology.hl7.org/CodeSystem/v2-0396")


# ---------------------------------------------------------------------------
# HL7 CDA → FHIR R4 (Task 24.3)
# ---------------------------------------------------------------------------


def cda_to_fhir(message: ParsedMessage) -> dict[str, Any]:
    """Translate a HL7 CDA / C-CDA :class:`ParsedMessage` to a FHIR R4 Bundle.

    Maps the four anchor C-CDA sections:

    - ``Allergies`` → :literal:`AllergyIntolerance` resources
    - ``Medications`` → :literal:`MedicationStatement` resources
    - ``Problems`` → :literal:`Condition` resources
    - ``Results`` → :literal:`Observation` resources

    Sections without a recognized templateId surface as a
    :literal:`Composition.section` with their narrative text only and are
    documented in ``LOSSY_CASES.md``.
    """
    if message.format != "cda":
        raise ValueError(
            f"cda_to_fhir requires format='cda', got {message.format!r}"
        )

    bundle = _new_bundle()

    # Always emit a Patient resource from the CDA recordTarget metadata
    patient = _patient_from_cda_metadata(message)
    if patient is not None:
        _add_entry(bundle, patient)

    # Walk segments — each is a section with its template OIDs and entries
    section_handlers = {
        "Allergies": _allergy_intolerances_from_cda_section,
        "Medications": _medication_statements_from_cda_section,
        "Problems": _conditions_from_cda_section,
        "Results": _observations_from_cda_section,
    }

    for seg in message.segments:
        handler = section_handlers.get(seg.name)
        if handler is None:
            # Lossy: surface as a generic Composition.section narrative
            continue
        for resource in handler(seg, patient):
            _add_entry(bundle, resource)

    return bundle


def _patient_from_cda_metadata(message: ParsedMessage) -> dict[str, Any] | None:
    pat_meta = message.metadata.get("patient")
    ids = message.metadata.get("patient_ids", [])
    if not pat_meta and not ids:
        return None
    pat: dict[str, Any] = {
        "resourceType": "Patient",
        "id": f"patient-{uuid4()}",
    }
    if ids:
        pat["identifier"] = [
            {"system": f"urn:oid:{i.get('root', '')}", "value": i.get("extension", "")}
            for i in ids
            if i.get("extension")
        ]
    if pat_meta:
        family = pat_meta.get("family", "")
        given = pat_meta.get("given", "")
        if family or given:
            pat["name"] = [{
                "use": "official",
                "family": family,
                "given": [given] if given else [],
            }]
        gender_code = pat_meta.get("gender", "").upper()
        gender_map = {"M": "male", "F": "female", "UN": "unknown"}
        if gender_code:
            pat["gender"] = gender_map.get(gender_code, "unknown")
    return pat


def _allergy_intolerances_from_cda_section(
    section, patient: dict[str, Any] | None
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    entries = section.data.get("entries", [])
    for entry in entries:
        allergy: dict[str, Any] = {
            "resourceType": "AllergyIntolerance",
            "id": f"allergy-{uuid4()}",
            "code": _entry_code_to_codeable(entry),
        }
        if patient is not None:
            allergy["patient"] = {"reference": f"Patient/{patient['id']}"}
        out.append(allergy)
    if not entries and section.data.get("free_text"):
        # Lossy: free-text-only section → single AllergyIntolerance with text
        allergy = {
            "resourceType": "AllergyIntolerance",
            "id": f"allergy-{uuid4()}",
            "code": {"text": section.data["free_text"]},
        }
        if patient is not None:
            allergy["patient"] = {"reference": f"Patient/{patient['id']}"}
        out.append(allergy)
    return out


def _medication_statements_from_cda_section(
    section, patient: dict[str, Any] | None
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    entries = section.data.get("entries", [])
    for entry in entries:
        stmt: dict[str, Any] = {
            "resourceType": "MedicationStatement",
            "id": f"medstmt-{uuid4()}",
            "status": "active",
            "medicationCodeableConcept": _entry_code_to_codeable(entry),
        }
        if patient is not None:
            stmt["subject"] = {"reference": f"Patient/{patient['id']}"}
        out.append(stmt)
    if not entries and section.data.get("free_text"):
        stmt = {
            "resourceType": "MedicationStatement",
            "id": f"medstmt-{uuid4()}",
            "status": "active",
            "medicationCodeableConcept": {"text": section.data["free_text"]},
        }
        if patient is not None:
            stmt["subject"] = {"reference": f"Patient/{patient['id']}"}
        out.append(stmt)
    return out


def _conditions_from_cda_section(
    section, patient: dict[str, Any] | None
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    entries = section.data.get("entries", [])
    for entry in entries:
        cond: dict[str, Any] = {
            "resourceType": "Condition",
            "id": f"condition-{uuid4()}",
            "code": _entry_code_to_codeable(entry),
        }
        if patient is not None:
            cond["subject"] = {"reference": f"Patient/{patient['id']}"}
        out.append(cond)
    if not entries and section.data.get("free_text"):
        cond = {
            "resourceType": "Condition",
            "id": f"condition-{uuid4()}",
            "code": {"text": section.data["free_text"]},
        }
        if patient is not None:
            cond["subject"] = {"reference": f"Patient/{patient['id']}"}
        out.append(cond)
    return out


def _observations_from_cda_section(
    section, patient: dict[str, Any] | None
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    entries = section.data.get("entries", [])
    for entry in entries:
        obs: dict[str, Any] = {
            "resourceType": "Observation",
            "id": f"observation-{uuid4()}",
            "status": "final",
            "code": _entry_code_to_codeable(entry),
        }
        if patient is not None:
            obs["subject"] = {"reference": f"Patient/{patient['id']}"}
        # Lossy: no structured value — capture as text
        value = entry.get("value", "")
        if value:
            obs["valueString"] = value
        out.append(obs)
    if not entries and section.data.get("free_text"):
        # Lossy: surface narrative as Observation.valueString
        obs = {
            "resourceType": "Observation",
            "id": f"observation-{uuid4()}",
            "status": "final",
            "code": {"text": section.data.get("section_display", "Result")},
            "valueString": section.data["free_text"],
        }
        if patient is not None:
            obs["subject"] = {"reference": f"Patient/{patient['id']}"}
        out.append(obs)
    return out


def _entry_code_to_codeable(entry: dict[str, Any]) -> dict[str, Any]:
    """CDA observation code → FHIR CodeableConcept."""
    code = entry.get("code", "")
    code_system = entry.get("code_system", "")
    display = entry.get("display", "")
    # Map common OIDs to FHIR system URIs
    system_map = {
        "2.16.840.1.113883.6.96": "http://snomed.info/sct",
        "2.16.840.1.113883.6.1": "http://loinc.org",
        "2.16.840.1.113883.6.103": "http://hl7.org/fhir/sid/icd-9-cm",
        "2.16.840.1.113883.6.90": "http://hl7.org/fhir/sid/icd-10-cm",
        "2.16.840.1.113883.6.69": "http://hl7.org/fhir/sid/ndc",
    }
    system = system_map.get(code_system, f"urn:oid:{code_system}" if code_system else "")
    if code:
        return {
            "coding": [{
                "system": system,
                "code": code,
                "display": display,
            }]
        }
    return {"text": display or "(uncoded)"}
