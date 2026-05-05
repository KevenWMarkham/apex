"""HL7 CDA / Consolidated CDA parser — Sprint 23 Task 23.3.

CDA is XML-based. We use the stdlib ``xml.etree.ElementTree`` parser with
XML-bomb guards (`xml.etree.ElementTree` is safe against billion-laughs by
default in Python 3.8+; we add explicit size limits per CSWE).

Section template OIDs we extract per Consolidated CDA:

- 2.16.840.1.113883.10.20.22.2.6.1   — Allergies
- 2.16.840.1.113883.10.20.22.2.1.1   — Medications
- 2.16.840.1.113883.10.20.22.2.5.1   — Problem List
- 2.16.840.1.113883.10.20.22.2.3.1   — Results

The parser walks the structuredBody → component → section tree and emits
one :class:`Segment` per recognized section, with the section's text body
(observations, ordinals, codes) populated into ``data``.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any

from apex_translators.base import (
    FORMAT_CDA,
    ParseError,
    ParsedMessage,
    Segment,
)


# CDA namespace (HL7 v3)
NS_CDA = "urn:hl7-org:v3"


# Recognized C-CDA section template root OIDs
SECTION_TEMPLATES: dict[str, str] = {
    "2.16.840.1.113883.10.20.22.2.6.1": "Allergies",
    "2.16.840.1.113883.10.20.22.2.6":   "Allergies",
    "2.16.840.1.113883.10.20.22.2.1.1": "Medications",
    "2.16.840.1.113883.10.20.22.2.1":   "Medications",
    "2.16.840.1.113883.10.20.22.2.5.1": "Problems",
    "2.16.840.1.113883.10.20.22.2.5":   "Problems",
    "2.16.840.1.113883.10.20.22.2.3.1": "Results",
    "2.16.840.1.113883.10.20.22.2.3":   "Results",
    "2.16.840.1.113883.10.20.22.2.7.1": "Procedures",
    "2.16.840.1.113883.10.20.22.2.4.1": "Vital Signs",
    "2.16.840.1.113883.10.20.22.2.17":  "Social History",
    "2.16.840.1.113883.10.20.22.2.22.1": "Encounters",
}


# Maximum payload size guard (10 MB) — defensive
MAX_PAYLOAD_BYTES = 10 * 1024 * 1024


@dataclass
class CDAParser:
    """C-CDA section extractor."""

    def parse(self, raw: str) -> ParsedMessage:
        if not raw:
            raise ParseError("CDA payload is empty")
        if len(raw.encode("utf-8")) > MAX_PAYLOAD_BYTES:
            raise ParseError(
                f"CDA payload exceeds {MAX_PAYLOAD_BYTES} bytes — refusing to parse"
            )

        try:
            root = ET.fromstring(raw)
        except ET.ParseError as exc:
            raise ParseError(f"CDA XML parse error: {exc}") from exc

        # Strip namespace from tag for predictable matching
        if not root.tag.endswith("ClinicalDocument"):
            raise ParseError(
                f"CDA root element should be ClinicalDocument, got {root.tag!r}"
            )

        msg = ParsedMessage(format=FORMAT_CDA, raw=raw)

        # Header — patient + author + custodian
        type_id = root.find(f"{{{NS_CDA}}}typeId")
        if type_id is not None:
            msg.message_type = type_id.get("extension", "")

        # Patient demographics → store in metadata
        record_target = root.find(f"{{{NS_CDA}}}recordTarget")
        if record_target is not None:
            patient_role = record_target.find(f"{{{NS_CDA}}}patientRole")
            if patient_role is not None:
                ids = patient_role.findall(f"{{{NS_CDA}}}id")
                msg.metadata["patient_ids"] = [
                    {"root": i.get("root", ""), "extension": i.get("extension", "")}
                    for i in ids
                ]
                patient = patient_role.find(f"{{{NS_CDA}}}patient")
                if patient is not None:
                    given_el = patient.find(f"{{{NS_CDA}}}name/{{{NS_CDA}}}given")
                    family_el = patient.find(f"{{{NS_CDA}}}name/{{{NS_CDA}}}family")
                    gender_el = patient.find(f"{{{NS_CDA}}}administrativeGenderCode")
                    msg.metadata["patient"] = {
                        "given": given_el.text if given_el is not None else "",
                        "family": family_el.text if family_el is not None else "",
                        "gender": gender_el.get("code", "") if gender_el is not None else "",
                    }

        # effectiveTime as sent_at
        eff_time = root.find(f"{{{NS_CDA}}}effectiveTime")
        if eff_time is not None and eff_time.get("value"):
            msg.metadata["effective_time"] = eff_time.get("value", "")

        # Walk structuredBody / component / section
        body = root.find(
            f"{{{NS_CDA}}}component/{{{NS_CDA}}}structuredBody"
        )
        if body is None:
            return msg

        for component in body.findall(f"{{{NS_CDA}}}component"):
            section = component.find(f"{{{NS_CDA}}}section")
            if section is None:
                continue

            template_oids = [
                t.get("root", "")
                for t in section.findall(f"{{{NS_CDA}}}templateId")
            ]
            section_name = "Unknown"
            for oid in template_oids:
                if oid in SECTION_TEMPLATES:
                    section_name = SECTION_TEMPLATES[oid]
                    break

            # Extract codes + free-text body
            code_el = section.find(f"{{{NS_CDA}}}code")
            code = (
                code_el.get("code", "") if code_el is not None else ""
            )
            display = (
                code_el.get("displayName", "") if code_el is not None else ""
            )

            text_el = section.find(f"{{{NS_CDA}}}text")
            free_text = (
                "".join(text_el.itertext()).strip() if text_el is not None else ""
            )

            # Pull entries — each <entry> represents a structured observation
            entries: list[dict[str, Any]] = []
            for entry in section.findall(f"{{{NS_CDA}}}entry"):
                obs = entry.find(f".//{{{NS_CDA}}}observation")
                if obs is None:
                    continue
                obs_code = obs.find(f"{{{NS_CDA}}}code")
                obs_value = obs.find(f"{{{NS_CDA}}}value")
                entries.append({
                    "code": obs_code.get("code", "") if obs_code is not None else "",
                    "code_system": obs_code.get("codeSystem", "") if obs_code is not None else "",
                    "display": obs_code.get("displayName", "") if obs_code is not None else "",
                    "value": obs_value.get("displayName") or obs_value.get("value") or ""
                        if obs_value is not None else "",
                })

            msg.segments.append(
                Segment(
                    name=section_name,
                    data={
                        "section_code": code,
                        "section_display": display,
                        "template_oids": template_oids,
                        "free_text": free_text,
                        "entries": entries,
                    },
                )
            )

        return msg


def parse_cda(raw: str) -> ParsedMessage:
    """Convenience: parse a C-CDA document."""
    return CDAParser().parse(raw)
