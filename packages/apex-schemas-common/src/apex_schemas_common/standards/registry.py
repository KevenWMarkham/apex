"""StandardSpec + ``STANDARDS`` registry.

The registry is intentionally seed-populated with standards in active use by
Sprint 2–3 Practices. Remaining standards are added incrementally as Practices
adopt them.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict

from apex_core.types import Practice


class StandardType(StrEnum):
    """Five-type taxonomy (Industry-Standards-Incorporation-Plan §3)."""

    IDENTIFIER = "identifier"
    TERMINOLOGY = "terminology"
    DATA_MODEL = "data_model"
    MESSAGE_FORMAT = "message_format"
    PROTOCOL = "protocol"


class StandardSpec(BaseModel):
    """Catalog entry describing a single industry standard."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str
    name: str
    authority: str
    authority_url: str
    type: StandardType
    current_version: str
    apex_pinned_version: str
    license: Literal["open", "royalty_free", "restricted", "redistribution_ok"]
    redistribution_ok: bool
    pattern: Literal["A", "B", "C", "D", "A+D", "B+C", "B+D"]
    supporting_package: str | None = None
    practices: list[Practice]
    notes: str = ""


# --- Registry seed -------------------------------------------------------------

STANDARDS: dict[str, StandardSpec] = {
    # ------- RC Practice (Sprint 2) ---------------------------------------
    "gs1-gtin": StandardSpec(
        id="gs1-gtin", name="GS1 GTIN", authority="GS1",
        authority_url="https://www.gs1.org/standards/id-keys/gtin",
        type=StandardType.IDENTIFIER, current_version="BMS-1.34",
        apex_pinned_version="BMS-1.34", license="royalty_free",
        redistribution_ok=True, pattern="A", practices=[Practice.RC],
    ),
    "gs1-sscc": StandardSpec(
        id="gs1-sscc", name="GS1 SSCC", authority="GS1",
        authority_url="https://www.gs1.org/standards/id-keys/sscc",
        type=StandardType.IDENTIFIER, current_version="BMS-1.34",
        apex_pinned_version="BMS-1.34", license="royalty_free",
        redistribution_ok=True, pattern="A", practices=[Practice.RC],
    ),
    "gs1-gln": StandardSpec(
        id="gs1-gln", name="GS1 GLN", authority="GS1",
        authority_url="https://www.gs1.org/standards/id-keys/gln",
        type=StandardType.IDENTIFIER, current_version="BMS-1.34",
        apex_pinned_version="BMS-1.34", license="royalty_free",
        redistribution_ok=True, pattern="A", practices=[Practice.RC],
    ),
    "epcis": StandardSpec(
        id="epcis", name="EPCIS", authority="GS1",
        authority_url="https://www.gs1.org/standards/epcis",
        type=StandardType.MESSAGE_FORMAT, current_version="2.0",
        apex_pinned_version="2.0", license="royalty_free",
        redistribution_ok=True, pattern="D", practices=[Practice.RC],
    ),
    "schema-org": StandardSpec(
        id="schema-org", name="Schema.org", authority="Schema.org",
        authority_url="https://schema.org/",
        type=StandardType.DATA_MODEL, current_version="25.0",
        apex_pinned_version="25.0", license="open",
        redistribution_ok=True, pattern="D", practices=[Practice.RC],
    ),
    # ------- HLS Practice (Sprint 3) --------------------------------------
    "hl7-fhir": StandardSpec(
        id="hl7-fhir", name="HL7 FHIR", authority="HL7",
        authority_url="https://www.hl7.org/fhir/",
        type=StandardType.DATA_MODEL, current_version="R5",
        apex_pinned_version="R4", license="royalty_free",
        redistribution_ok=True, pattern="B",
        supporting_package="apex-standards-fhir",
        practices=[Practice.HLS],
    ),
    "loinc": StandardSpec(
        id="loinc", name="LOINC", authority="Regenstrief Institute",
        authority_url="https://loinc.org/",
        type=StandardType.TERMINOLOGY, current_version="2.77",
        apex_pinned_version="2.77", license="restricted",
        redistribution_ok=False, pattern="A", practices=[Practice.HLS],
        notes="Regex + external lookup; vocabulary content not redistributed.",
    ),
    "icd-10-cm": StandardSpec(
        id="icd-10-cm", name="ICD-10-CM", authority="CDC/NCHS",
        authority_url="https://www.cdc.gov/nchs/icd/icd10cm.htm",
        type=StandardType.IDENTIFIER, current_version="2026-Q1",
        apex_pinned_version="2026-Q1", license="open",
        redistribution_ok=True, pattern="A", practices=[Practice.HLS],
    ),
    "ndc": StandardSpec(
        id="ndc", name="National Drug Code", authority="FDA",
        authority_url="https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory",
        type=StandardType.IDENTIFIER, current_version="2026",
        apex_pinned_version="2026", license="open",
        redistribution_ok=True, pattern="A", practices=[Practice.HLS],
    ),
    "snomed-ct": StandardSpec(
        id="snomed-ct", name="SNOMED CT", authority="SNOMED International",
        authority_url="https://www.snomed.org/",
        type=StandardType.TERMINOLOGY, current_version="2026-01",
        apex_pinned_version="2026-01", license="restricted",
        redistribution_ok=False, pattern="A", practices=[Practice.HLS],
        notes="Licensed terminology; tenant provides terminology service.",
    ),
    "cpt": StandardSpec(
        id="cpt", name="CPT", authority="AMA",
        authority_url="https://www.ama-assn.org/practice-management/cpt",
        type=StandardType.IDENTIFIER, current_version="2026",
        apex_pinned_version="2026", license="restricted",
        redistribution_ok=False, pattern="A", practices=[Practice.HLS],
        notes="AMA-licensed; regex binding only.",
    ),
    "hcpcs": StandardSpec(
        id="hcpcs", name="HCPCS", authority="CMS",
        authority_url="https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system",
        type=StandardType.IDENTIFIER, current_version="2026",
        apex_pinned_version="2026", license="open",
        redistribution_ok=True, pattern="A", practices=[Practice.HLS],
    ),
    "rxnorm": StandardSpec(
        id="rxnorm", name="RxNorm", authority="NLM",
        authority_url="https://www.nlm.nih.gov/research/umls/rxnorm/",
        type=StandardType.TERMINOLOGY, current_version="2026-01",
        apex_pinned_version="2026-01", license="open",
        redistribution_ok=True, pattern="A", practices=[Practice.HLS],
    ),
    # ------- ER / AXLE / ICE shared ---------------------------------------
    "isa-95": StandardSpec(
        id="isa-95", name="ISA-95", authority="ISA",
        authority_url="https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95",
        type=StandardType.DATA_MODEL, current_version="2018",
        apex_pinned_version="2018", license="royalty_free",
        redistribution_ok=True, pattern="B",
        supporting_package="apex-standards-isa95",
        practices=[Practice.ER, Practice.AXLE, Practice.ICE],
    ),
    "sae-j1939": StandardSpec(
        id="sae-j1939", name="SAE J1939", authority="SAE International",
        authority_url="https://www.sae.org/standards/development/standards-committee-content/sae-j1939",
        type=StandardType.IDENTIFIER, current_version="2025",
        apex_pinned_version="2025", license="restricted",
        redistribution_ok=False, pattern="A",
        practices=[Practice.AXLE, Practice.ICE],
    ),
    # ------- TMT / TH / additional (seed — expand per Practice rollout) ----
    "tm-forum-sid": StandardSpec(
        id="tm-forum-sid", name="TM Forum SID", authority="TM Forum",
        authority_url="https://www.tmforum.org/oda/information-systems/",
        type=StandardType.DATA_MODEL, current_version="22.5",
        apex_pinned_version="22.5", license="open",
        redistribution_ok=True, pattern="B",
        supporting_package="apex-standards-sid",
        practices=[Practice.TMT],
    ),
    "iata-ndc": StandardSpec(
        id="iata-ndc", name="IATA NDC", authority="IATA",
        authority_url="https://www.iata.org/en/programs/airline-distribution/ndc/",
        type=StandardType.DATA_MODEL, current_version="2024.2",
        apex_pinned_version="2024.2", license="royalty_free",
        redistribution_ok=True, pattern="B+C", practices=[Practice.TH],
    ),
    "eidr": StandardSpec(
        id="eidr", name="EIDR Content ID", authority="EIDR",
        authority_url="https://www.eidr.org/",
        type=StandardType.IDENTIFIER, current_version="2.1",
        apex_pinned_version="2.1", license="open",
        redistribution_ok=True, pattern="A", practices=[Practice.TMT],
    ),
    # ------- Sprint 3 Phase 1 additions ------------------------------------
    "iso-14224": StandardSpec(
        id="iso-14224", name="ISO 14224", authority="ISO",
        authority_url="https://www.iso.org/standard/64076.html",
        type=StandardType.DATA_MODEL, current_version="2016",
        apex_pinned_version="2016", license="restricted",
        redistribution_ok=False, pattern="B",
        supporting_package="apex-standards-iso14224",
        practices=[Practice.AXLE, Practice.ICE],
        notes="ISO publishes under commercial licence; APEX mirrors taxonomy only.",
    ),
    "cim-iec-61970": StandardSpec(
        id="cim-iec-61970", name="IEC 61970 CIM (Power System)", authority="IEC",
        authority_url="https://webstore.iec.ch/publication/61167",
        type=StandardType.DATA_MODEL, current_version="2021",
        apex_pinned_version="2021", license="restricted",
        redistribution_ok=False, pattern="B",
        supporting_package="apex-standards-cim",
        practices=[Practice.ER],
    ),
    "cim-iec-61968": StandardSpec(
        id="cim-iec-61968", name="IEC 61968 CIM (Utility Operations)", authority="IEC",
        authority_url="https://webstore.iec.ch/publication/6197",
        type=StandardType.DATA_MODEL, current_version="2020",
        apex_pinned_version="2020", license="restricted",
        redistribution_ok=False, pattern="B",
        supporting_package="apex-standards-cim",
        practices=[Practice.ER],
    ),
    "opentravel": StandardSpec(
        id="opentravel", name="OpenTravel Alliance (OTA)", authority="OpenTravel Alliance",
        authority_url="https://opentravel.org/",
        type=StandardType.DATA_MODEL, current_version="2025A",
        apex_pinned_version="2025A", license="open",
        redistribution_ok=True, pattern="B",
        supporting_package="apex-standards-opentravel",
        practices=[Practice.TH],
    ),
    "cdisc-odm": StandardSpec(
        id="cdisc-odm", name="CDISC ODM", authority="CDISC",
        authority_url="https://www.cdisc.org/standards/data-exchange/odm",
        type=StandardType.DATA_MODEL, current_version="2.0",
        apex_pinned_version="2.0", license="open",
        redistribution_ok=True, pattern="B",
        supporting_package="apex-standards-cdisc",
        practices=[Practice.HLS],
    ),
    "cdisc-sdtm": StandardSpec(
        id="cdisc-sdtm", name="CDISC SDTM", authority="CDISC",
        authority_url="https://www.cdisc.org/standards/foundational/sdtm",
        type=StandardType.DATA_MODEL, current_version="2.0",
        apex_pinned_version="2.0", license="open",
        redistribution_ok=True, pattern="B",
        supporting_package="apex-standards-cdisc",
        practices=[Practice.HLS],
    ),
    # ------- Sprint 22 Task 22.6 — Master-data-quality binding ----------
    "iso-8000": StandardSpec(
        id="iso-8000", name="ISO 8000 Data Quality", authority="ISO",
        authority_url="https://www.iso.org/standard/50798.html",
        type=StandardType.DATA_MODEL, current_version="8000-61:2016",
        apex_pinned_version="8000-61:2016", license="restricted",
        redistribution_ok=False, pattern="B",
        supporting_package=None,
        practices=[
            Practice.RC, Practice.HLS, Practice.ER, Practice.AXLE,
            Practice.TMT, Practice.TH, Practice.ICE,
        ],
        notes=(
            "Master-data-quality dimensions (completeness, consistency, accuracy, "
            "currency, provenance, conformance) bound at the CanonicalEnvelope "
            "level via DataQualityMetadata. Standard text NOT redistributed; "
            "APEX implements the dimension semantics in code only."
        ),
    ),
}


def lookup(standard_id: str) -> StandardSpec:
    """Return the :class:`StandardSpec` registered under ``standard_id``.

    Raises:
        KeyError: If no such standard is registered.
    """
    try:
        return STANDARDS[standard_id]
    except KeyError as exc:
        raise KeyError(
            f"Unknown standard {standard_id!r}. "
            f"Known: {sorted(STANDARDS)}"
        ) from exc


def list_standards(practice: Practice | None = None) -> list[StandardSpec]:
    """List registered standards, optionally filtered to one Practice."""
    if practice is None:
        return sorted(STANDARDS.values(), key=lambda s: s.id)
    return sorted(
        (s for s in STANDARDS.values() if practice in s.practices),
        key=lambda s: s.id,
    )
