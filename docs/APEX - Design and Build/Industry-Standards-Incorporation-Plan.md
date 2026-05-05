# APEX Industry-Standards Incorporation Plan

**Source:** `APEX_Design.md` §5.4 (consume / extend / translate), §15 (per-Practice standards alignment)
**Depends on:** Sprint 1 L1 contract (BL.P.01–P.07) ✅ complete
**Blocks:** Sprint 2 canonical schemas (BL.P.08–P.10), Sprint 3 per-Practice schemas (BL.P.11–P.19)
**Date:** 2026-04-19
**Purpose:** Define precisely *how* APEX canonical schemas consume, extend, translate, and stay aligned with the ~50 industry standards listed in `APEX_Design.md` §15 — so that Sprint 2 entity code ships against a clear standards pattern.

---

## 1. Why This Plan Is Its Own Document

`APEX_Design.md` §5.4 states the three-step pattern — **consume, extend, translate** — but does not prescribe:

- where standards live in the Python package tree,
- how identifiers/terminologies/data-models/message-formats/protocols differ in their incorporation mechanics,
- how to version-pin a standard and evolve APEX when the standard bumps,
- how to validate conformance at CI time,
- how to handle license-restricted terminologies (SNOMED CT, LOINC),
- how the standards inventory affects the Sprint 2–3 backlog.

Without this plan, two risks materialise:

1. **Drift.** Every schema package reinvents its own standards-binding convention.
2. **Scope creep.** Sprint 2 (SCML, MERML, CXML) quietly absorbs weeks of unbudgeted GS1 / EPCIS / Schema.org modelling work.

This document fixes both.

---

## 2. Principles

1. **Consume, don't recreate.** Where a standard is authoritative (GS1 GTIN structure, FHIR R4 Patient), APEX mirrors it field-for-field or references it by identifier — it does not invent a parallel model.
2. **Extend with governance, never fork.** APEX adds classification labels, tokenisation hooks, audit-row anchors, and SCD2 history. It does **not** rename or restructure standard fields.
3. **Translate bidirectionally.** Every `standard_a → standard_b` translator ships with its inverse, plus round-trip conformance tests. No one-way lossy conversions in the canonical layer.
4. **Pin standard versions.** Each standard has an explicit version (e.g., FHIR R4, GS1 BMS 1.34, ISA-95 Part 2:2018). Bumping a standard is its own PR with an impact analysis.
5. **License-respecting distribution.** Restricted terminologies (SNOMED CT, LOINC, ICD) are referenced, not redistributed. APEX ships the *binding layer* (regex / hook), not the vocabulary content.
6. **Conformance is a CI check, not a documentation claim.** Every entity that claims GS1 alignment has a test that fails if the entity drifts from GS1 shape.
7. **Standards are L1 citizens.** The standards registry lives in `apex-schemas-common` (Sprint 2 package), loaded into every Practice. Per-standard heavy code (FHIR, SID) ships as its own package.

---

## 3. Standards Taxonomy — Five Types

APEX's ~50 referenced standards split into five types. Each type has a distinct incorporation mechanic.

| Type | What it is | Examples | Incorporation |
|------|-----------|----------|---------------|
| **T1. Identifier** | A naming or coding scheme (usually structured strings) | GS1 GTIN/SSCC/GLN, LOINC codes, ICD-10 codes, NDC, ISBN, SAE J1939 PGN | Pattern A: regex-validated `Annotated[str, StandardRef(...)]` field |
| **T2. Terminology** | A controlled vocabulary, often hierarchical | SNOMED CT, RxNorm, SNOMED clinical terms, HCPCS | Pattern A + external lookup hook; content not redistributed |
| **T3. Data model** | A structural schema for entities | HL7 FHIR R4/R5, CIM (IEC 61970), TM Forum SID, ISA-95, OpenTravel OTA, STEP | Pattern B (mirror model) + Pattern C (consume + extend) |
| **T4. Message format** | A wire format or payload shape | HL7 v2, HL7 CDA, EDI X12, IATA PADIS, DICOM | Pattern D (translator package) — parse / emit / round-trip |
| **T5. Protocol** | A transport + payload combination | OPC UA, SAE J1939 (with CAN frames), IEC 61850, MEF 55/LSO | Pattern D — wrapped inside an SOR adapter, not a schema |

---

## 4. Four Incorporation Patterns

Each pattern maps to a concrete Python implementation. Sprint 2–3 entity code **must** use one of these four patterns for each standard it references.

### 4.1 Pattern A — Identifier Reference (T1, T2)

The attribute's *type* encodes the standard.

```python
# packages/apex-schemas-common/src/apex_schemas_common/standards/types.py

from dataclasses import dataclass
from typing import Annotated
from pydantic import StringConstraints

@dataclass(frozen=True, slots=True)
class StandardRef:
    """Marks an attribute as conforming to a named external standard."""
    standard: str          # e.g. "GS1"
    identifier: str        # e.g. "GTIN-14"
    version: str           # e.g. "BMS-1.34"
    authority_url: str     # e.g. "https://www.gs1.org/standards/id-keys/gtin"


# --- Reusable identifier types ----------------------------------------------

GTIN14 = Annotated[
    str,
    StringConstraints(pattern=r"^\d{14}$"),
    StandardRef("GS1", "GTIN-14", "BMS-1.34",
                "https://www.gs1.org/standards/id-keys/gtin"),
]

LoincCode = Annotated[
    str,
    StringConstraints(pattern=r"^\d{1,5}-\d$"),
    StandardRef("LOINC", "LOINC-Code", "2.77",
                "https://loinc.org/"),
]

Icd10Code = Annotated[
    str,
    StringConstraints(pattern=r"^[A-TV-Z][0-9][0-9AB](\.[0-9A-Z]{1,4})?$"),
    StandardRef("ICD-10-CM", "Icd10Code", "2026-Q1",
                "https://www.cdc.gov/nchs/icd/icd10cm.htm"),
]
```

**Use in entity:**

```python
class SKU(CanonicalEntity):
    gtin: GTIN14 | None = Field(None, description="Global Trade Item Number.")
```

**What Pattern A gives you automatically:**

- Runtime validation (regex enforced by Pydantic at entity-construction time).
- The `StandardRef` metadata is introspectable — DDL generators, Purview-payload builders, and conformance tests walk `get_type_hints(cls, include_extras=True)` and discover every standard binding.
- Drift detection: if someone changes the regex without bumping the registered version, CI fails.

---

### 4.2 Pattern B — Mirror Model (T3, high-authority)

Where a standard *is* the canonical shape (HL7 FHIR, CIM, SID), APEX ships a Pydantic mirror in `apex-standards-<name>` as its own package. APEX canonical entities then reference the mirror.

```python
# packages/apex-standards-fhir/src/apex_standards_fhir/r4/patient.py

class FhirHumanName(BaseModel):
    use: Literal["usual", "official", "temp", "nickname", "anonymous",
                 "old", "maiden"] | None = None
    text: str | None = None
    family: str | None = None
    given: list[str] = Field(default_factory=list)

class FhirPatientR4(BaseModel):
    resource_type: Literal["Patient"] = "Patient"
    id: str
    identifier: list[FhirIdentifier] = Field(default_factory=list)
    name: list[FhirHumanName] = Field(default_factory=list)
    birth_date: date | None = None
    # … relevant subset of FHIR R4 Patient
```

**Scope rule:** mirrors cover the subset of fields APEX canonical entities consume. A 100%-complete FHIR mirror is out of scope — we ship the subset that shows up in HLS agent catalogues.

---

### 4.3 Pattern C — Consume + Extend (T3 into canonical)

The APEX canonical entity constructs from the mirror and adds governance.

```python
# packages/apex-hlscml/src/apex_hlscml/entities/patient.py

from apex_schemas_common.entity import CanonicalEntity
from apex_standards_fhir.r4 import FhirPatientR4
from apex_core.types import Classification

class Patient(CanonicalEntity):
    """HLSCML canonical Patient — FHIR R4 + APEX governance."""
    # --- Carried from FHIR (subset) -----------------------------------------
    fhir_id: str
    mrn_token: Annotated[str, Classification.PHI]   # tokenised at Bronze→Silver
    name_family_token: Annotated[str, Classification.PHI]
    birth_date: date

    # --- APEX governance additions ------------------------------------------
    source_fhir_version: Literal["R4", "R5"] = "R4"
    consent_pointer: str | None = None   # reference into consent ledger

    @classmethod
    def from_fhir(cls, fhir: FhirPatientR4, *, envelope_fields: dict) -> "Patient":
        """Translate a FHIR R4 Patient resource into APEX canonical form."""
        ...
```

**Rule:** never rename a FHIR field to an APEX-flavoured name. If the APEX canonical must expose a different name, add it as an APEX-specific attribute alongside the preserved FHIR-named one.

---

### 4.4 Pattern D — Translator Bridge (T4, T5, cross-standard)

For message formats, protocols, and cross-standard conversions, ship **bidirectional** functions with round-trip tests.

```python
# packages/apex-scml/src/apex_scml/translators/gs1_to_schema_org.py

def gs1_gtin_to_schema_org_product(gtin: str) -> dict[str, object]:
    """GS1 GTIN-14 → Schema.org Product (gtin14 property)."""
    return {"@type": "Product", "gtin14": gtin}

def schema_org_product_to_gs1_gtin(product: dict[str, object]) -> str | None:
    """Extract GTIN from Schema.org Product (any of gtin, gtin8/12/13/14)."""
    for key in ("gtin14", "gtin13", "gtin12", "gtin8", "gtin"):
        value = product.get(key)
        if value is not None:
            return str(value)
    return None
```

**Round-trip test** (required):

```python
def test_gtin_round_trip():
    gtin = "09780201379624"  # example GTIN-14
    product = gs1_gtin_to_schema_org_product(gtin)
    assert schema_org_product_to_gs1_gtin(product) == gtin
```

---

## 5. Standards Registry — Where Bindings Live

### 5.1 Code layout

```
packages/
├── apex-schemas-common/
│   └── src/apex_schemas_common/
│       └── standards/
│           ├── __init__.py            registry API
│           ├── registry.py            StandardSpec + STANDARDS dict
│           ├── types.py               StandardRef, shared identifier types
│           ├── introspect.py          walk Pydantic fields → find StandardRefs
│           └── catalog.yaml           machine-readable catalog (Appendix source)
├── apex-standards-fhir/               (Pattern B mirrors for FHIR R4/R5)
├── apex-standards-cim/                (Pattern B mirrors for IEC 61970/61968)
├── apex-standards-sid/                (Pattern B mirrors for TM Forum SID)
├── apex-standards-isa95/              (Pattern B mirrors for ISA-95 hierarchy)
└── apex-standards-opentravel/         (Pattern B mirrors for OTA schemas)
```

**Only T3 standards get their own `apex-standards-*` package.** T1/T2/T4/T5 bindings live within the consuming Practice package (e.g., GS1 identifiers live in `apex-scml`, EDI translators live in `apex-scml/translators/`).

### 5.2 StandardSpec Pydantic model

```python
# apex_schemas_common/standards/registry.py

class StandardSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str                              # "gs1-gtin"
    name: str                            # "GS1 GTIN"
    authority: str                       # "GS1"
    authority_url: HttpUrl
    type: Literal["identifier", "terminology",
                   "data_model", "message_format", "protocol"]
    current_version: str
    apex_pinned_version: str
    license: Literal["open", "royalty_free", "restricted", "redistribution_ok"]
    redistribution_ok: bool
    pattern: Literal["A", "B", "C", "D"]
    supporting_package: str | None = None    # e.g. "apex-standards-fhir" for Pattern B
    practices: list[Practice]
    notes: str = ""


STANDARDS: dict[str, StandardSpec] = {
    "gs1-gtin": StandardSpec(
        id="gs1-gtin", name="GS1 GTIN", authority="GS1",
        authority_url="https://www.gs1.org/standards/id-keys/gtin",
        type="identifier", current_version="BMS-1.34",
        apex_pinned_version="BMS-1.34", license="royalty_free",
        redistribution_ok=True, pattern="A",
        practices=[Practice.RC],
    ),
    # … ~50 more entries
}
```

### 5.3 CLI surface

```
apex standards list
apex standards show gs1-gtin
apex standards audit packages/apex-scml          # find StandardRefs, verify all are registered
apex standards bump fhir-r4 --to R5 --dry-run    # impact analysis
```

---

## 6. Per-Standard Incorporation Matrix

Condensed from `APEX_Design.md` §15. Sprint-binding column indicates which Sprint introduces the binding.

### 6.1 RC Practice (Sprint 2)

| Standard | Type | Pattern | Use | Sprint |
|----------|------|---------|-----|--------|
| GS1 GTIN / SSCC / GLN | T1 | A | SCML SKU / Shipment / Location identifiers | 2 |
| EPCIS | T4 | D | Supply-chain event messages | 2 |
| GDSN | T4 | D | Product-data synchronisation | 3 |
| EDI X12 (850/856/810/820) | T4 | D | Order / shipment / invoice messages | 15 (adapters) |
| ARTS ODM | T3 | B+C | Retail transaction reference model | 3 |
| IFPS | T1 | A | Produce codes | 3 |
| ISO 8000 | T2 | A | Master data quality | 3 |
| Schema.org Product / Offer | T3 | D | Web / search interop | 2 |

### 6.2 HLS Practice (Sprint 3)

| Standard | Type | Pattern | Use | Sprint |
|----------|------|---------|-----|--------|
| HL7 FHIR R4/R5 | T3 | B+C | Core data model (`apex-standards-fhir`) | 3 |
| HL7 v2.x | T4 | D | Legacy message parser / emitter | 3 |
| HL7 CDA / C-CDA | T4 | D | Clinical document import | 3 |
| SNOMED CT | T2 | A | Clinical terms | 3 |
| LOINC | T2 | A | Lab / measurement codes | 3 |
| ICD-10 / ICD-11 | T1 | A | Diagnosis codes | 3 |
| CPT / HCPCS | T1 | A | Procedure codes | 3 |
| RxNorm | T2 | A | Drug codes | 3 |
| NDC | T1 | A | National drug codes | 3 |
| HIPAA X12 (837/835/270/271) | T4 | D | Claims / eligibility messages | 15 |
| NCPDP | T4 | D | Pharmacy messages | 15 |
| CDISC (ODM/SDTM/ADaM/Define-XML) | T3 | B | Clinical trial data | 3 |
| DICOM | T4 | D | Medical imaging | 15 |
| IHE profiles | T3 | B | Integration profiles | 3 |
| USCDI | T3 | B | US Core data for interop | 3 |
| IDMP | T3 | B | Drug product identification | 3 |

### 6.3 ER Practice (Sprint 3)

| Standard | Type | Pattern | Use | Sprint |
|----------|------|---------|-----|--------|
| CIM (IEC 61970/61968/62325) | T3 | B+C | Utility core model (`apex-standards-cim`) | 3 |
| ISO 15926 | T3 | B | Industrial process lifecycle | 3 |
| WITSML / PRODML | T4 | D | O&G data exchange | 3 |
| IEC 61850 | T5 | D | Substation automation | 15 |
| OPC UA | T5 | D | Industrial protocol (shared with AXLE, ICE) | 15 |
| ISA-95 | T3 | B | Manufacturing hierarchy (shared with AXLE) | 3 |
| NERC CIP | T2 | A | Critical infrastructure protection metadata | 3 |
| EPRI | T3 | B | Power-utility reference | 3 |

### 6.4 AXLE Practice (Sprint 3)

| Standard | Type | Pattern | Use | Sprint |
|----------|------|---------|-----|--------|
| ISA-95 / ISA-88 | T3 | B+C | Manufacturing hierarchy (`apex-standards-isa95`) | 3 |
| AutomationML | T3 | B | Plant engineering | 3 |
| OPC UA | T5 | D | Machine-floor protocol | 15 |
| STEP (AP242/203/214) | T3 | B | Product data | 3 |
| PLCS | T3 | B | Product lifecycle support | 3 |
| OAGIS | T4 | D | Open Applications Group Integration Specification | 3 |
| VDA / Odette | T4 | D | Automotive supply-chain messages | 15 |
| ANSI/ASC X12 | T4 | D | Supply-chain messages | 15 |
| MIMOSA CRIS | T3 | B | Condition monitoring | 3 |
| ISO 14224 | T3 | B | Reliability data (shared with ICE) | 3 |
| IATF 16949 | T3 | B | Quality metadata | 3 |
| SAE J1939 | T1+T5 | A+D | Vehicle network identifiers (shared with ICE) | 3 |
| ISO 11783 ISOBUS | T5 | D | Agricultural equipment protocol (shared with ICE) | 3 |

### 6.5 TMT Practice (Sprint 3)

| Standard | Type | Pattern | Use | Sprint |
|----------|------|---------|-----|--------|
| TM Forum SID | T3 | B+C | Information model (`apex-standards-sid`) | 3 |
| TM Forum ODA | T3 | B | Open Digital Architecture | 3 |
| TM Forum Open APIs | T4 | D | REST API specs | 3 |
| 3GPP | T3 | B | Telecom network | 3 |
| MEF 55/LSO | T3 | B | Network orchestration | 3 |
| DVB | T3 | B | Digital video broadcasting | 3 |
| EIDR | T1 | A | Entertainment identifier | 3 |
| SMPTE | T3 | B | Media engineering | 3 |
| IAB / AdCOM | T3 | B | Ad-tech taxonomy | 3 |
| ETSI | T3 | B | European telecoms | 3 |

### 6.6 TH Practice (Sprint 3)

| Standard | Type | Pattern | Use | Sprint |
|----------|------|---------|-----|--------|
| IATA NDC | T3 | B+C | New Distribution Capability | 3 |
| IATA PADIS | T4 | D | Passenger data messages | 3 |
| OpenTravel (OTA) | T3 | B | Travel-industry model (`apex-standards-opentravel`) | 3 |
| HTNG | T3 | B | Hospitality tech network | 3 |
| ONE Record | T3 | B | IATA cargo | 3 |
| TSA/APIS/PNR | T4 | D | Government screening messages | 15 |
| PCI DSS | T2 | A | Payment handling metadata (policy overlay) | 3 |
| IATA PSS | T4 | D | Passenger service system messages | 15 |
| GSF | T3 | B | Global sustainability framework | 3 |

### 6.7 ICE Practice (Sprint 3)

| Standard | Type | Pattern | Use | Sprint |
|----------|------|---------|-----|--------|
| SAE J1939 / J1708 | T1+T5 | A+D | Vehicle network | 3 |
| ISO 11783 ISOBUS | T5 | D | Agricultural equipment | 3 |
| OPC UA | T5 | D | Industrial protocol | 15 |
| AEMP 2.0 / ISO 15143-3 | T3 | B+D | Construction-equipment telematics | 3 |
| ISO 14224 | T3 | B | Reliability data | 3 |
| ESG / CDP | T3 | B | Sustainability reporting | 3 |

### 6.8 Shared standards (cross-Practice)

- **ISA-95** — ER, AXLE, ICE → one `apex-standards-isa95` package consumed by three Practices.
- **OPC UA** — ER, AXLE, ICE → adapter-level (Sprint 15).
- **ISO 14224** — AXLE, ICE → one package.
- **SAE J1939** — AXLE, ICE → one package.
- **HIPAA X12** — HLS → shared with RC's EDI X12 infrastructure (common parser core).

**Package consolidation rule:** if ≥2 Practices consume a T3 standard, it goes in its own `apex-standards-*` package. Single-Practice T3 standards may stay inside the consuming Practice package if mirror is <5 files.

---

## 7. Versioning Policy

### 7.1 Standard-version as APEX bump

When a standard version moves:

| Standard change | APEX bump on affected canonical entity |
|-----------------|----------------------------------------|
| Additive (new optional fields) | **MINOR** — ACK_ONLY gate per §9 |
| Breaking (field removal, type narrowing, renamed enum) | **MAJOR** — HITL gate |
| Clarification / documentation only | **PATCH** — ZERO_TOUCH |
| Terminology content update (new SNOMED release) | No schema bump; binding test refreshed |

### 7.2 Pinning and override

- Every `StandardSpec` has `apex_pinned_version` separate from `current_version`.
- CI `apex standards audit` fails if a used binding references an unpinned or mismatched version.
- Tenants may override pinned version via L4 tenant manifest for regulatory alignment (e.g., stay on FHIR R4 until US-Core forces R5).

### 7.3 Translation tables between standard versions

Where a standard releases a breaking version (FHIR R4 → R5, ISA-95:2005 → 2018), APEX ships a Pattern D translator module inside the Pattern B package:

```
apex-standards-fhir/src/apex_standards_fhir/
├── r4/
├── r5/
└── migrations/
    └── r4_to_r5.py
```

---

## 8. License & Redistribution Policy

| License class | Examples | APEX handling |
|---------------|----------|----------------|
| Open / public domain | ICD-10-CM, EPCIS | Redistribute freely in APEX packages |
| Royalty-free with attribution | GS1 GTIN structure, FHIR | Redistribute with LICENSE + attribution |
| Restricted (membership / fee required) | SNOMED CT, LOINC (commercial use), DICOM NEMA | **Do not redistribute vocabulary content.** Ship regex / binding layer only. Provide hook for customer-supplied terminology service |
| Vendor-proprietary (per-instance) | IATA PSS, some EDI dialects | Ship parser only if vendor's licence allows; otherwise adapter pattern delegates parsing to vendor-provided lib |

Every `apex-standards-*` package MUST include:

- `LICENSE-ATTRIBUTION.md` — list of third-party standards and their licences.
- No vocabulary content files unless explicitly `license: open` in `StandardSpec`.

---

## 9. Conformance Testing

Every canonical entity claiming alignment with a standard has automated conformance tests in its package:

- **Pattern A:** property-based tests generate valid / invalid identifiers; entity construction succeeds only on valid.
- **Pattern B:** round-trip a canonical reference payload from the standard authority (if open) through the mirror model.
- **Pattern C:** `from_<standard>` + `to_<standard>` round-trip (required).
- **Pattern D:** `<a>_to_<b>` + `<b>_to_<a>` round-trip on a fixture corpus.

CI job `conformance` runs alongside `test` in `.github/workflows/ci.yml`:

```yaml
  conformance:
    name: Standards conformance
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --all-packages
      - run: uv run apex standards audit packages
      - run: uv run pytest -m conformance
```

---

## 10. Per-Practice Rollout Order

Priorities driven by (a) Sprint dependencies, (b) complexity of the standard, (c) reference-deployment use cases.

| Order | Practice | Anchor standards | Why first / why later |
|-------|----------|------------------|------------------------|
| 1 | **RC** | GS1 (GTIN), Schema.org, EPCIS | Sprint 2 anchor; mostly identifier-type (Pattern A) — fastest to ship |
| 2 | **HLS** | FHIR R4, LOINC, ICD-10, SNOMED CT | Sprint 3; heaviest mirror package (`apex-standards-fhir`); clinical agent catalogue blocks on it |
| 3 | **ER** | CIM, ISA-95 | Sprint 3; CIM alone is a 4–6-week build |
| 4 | **AXLE** | ISA-95, ISA-88, OAGIS | Sprint 3; reuses ISA-95 from ER |
| 5 | **ICE** | SAE J1939, AEMP 2.0, ISO 14224 | Sprint 3; identifier-heavy, lean |
| 6 | **TMT** | TM Forum SID, MEF 55 | Sprint 3; SID is a large mirror but most agents use thin subset |
| 7 | **TH** | IATA NDC, OTA | Sprint 3; last because reference deployment (Airline IROP) is Sprint 18 |

---

## 11. New Backlog Items

These items extend `Roadmap.md` with standards-specific work. Insert after BL.P.19 (Cross-standard translators consolidation).

### 11.1 Standards Registry & Infrastructure

- [ ] **BL.P.134** — `apex-schemas-common.standards` module: `StandardSpec`, `StandardRef`, `STANDARDS` registry dict, `introspect` walker
- [ ] **BL.P.135** — `apex standards list|show|audit|bump` CLI subcommands
- [ ] **BL.P.136** — CI job: `conformance` lane in `.github/workflows/ci.yml`
- [ ] **BL.P.137** — `apex-schemas-common.standards.catalog.yaml` — machine-readable catalog (source for Appendix G-adjacent publication)
- [ ] **BL.P.138** — `LICENSE-ATTRIBUTION.md` template + generator per `apex-standards-*` package

### 11.2 Shared Pattern-B Standard Packages (Sprint 3)

- [ ] **BL.P.139** — `apex-standards-fhir` (R4 + R5 mirrors, R4→R5 migration)
- [ ] **BL.P.140** — `apex-standards-cim` (IEC 61970/61968/62325 mirrors)
- [ ] **BL.P.141** — `apex-standards-isa95` (Part 1–5 hierarchy, shared ER + AXLE + ICE)
- [ ] **BL.P.142** — `apex-standards-sid` (TM Forum SID domains)
- [ ] **BL.P.143** — `apex-standards-opentravel` (OTA schemas)
- [ ] **BL.P.144** — `apex-standards-cdisc` (ODM / SDTM / ADaM mirrors)
- [ ] **BL.P.145** — `apex-standards-iso14224` (reliability data)
- [ ] **BL.P.146** — `apex-standards-j1939` (SAE J1939 SPN / PGN registry)

### 11.3 Identifier-Type Bindings (T1 — Pattern A)

Bundled into their consuming Practice packages; tracked collectively:

- [ ] **BL.P.147** — RC identifiers: GS1 GTIN-8/12/13/14, SSCC, GLN, IFPS (in `apex-scml`, `apex-merml`)
- [ ] **BL.P.148** — HLS identifiers: ICD-10/11, CPT, HCPCS, NDC (in `apex-hlscml`)
- [ ] **BL.P.149** — ICE/AXLE identifiers: J1939 SPN/PGN, AEMP 2.0 fields (in `apex-ice`, `apex-axleml`)
- [ ] **BL.P.150** — TMT identifiers: EIDR (in `apex-telml`)

### 11.4 Terminology Bindings (T2 — Pattern A + external hook)

- [ ] **BL.P.151** — SNOMED CT binding + lookup hook interface
- [ ] **BL.P.152** — LOINC binding + lookup hook interface
- [ ] **BL.P.153** — RxNorm binding + lookup hook interface
- [ ] **BL.P.154** — ISO 8000 master-data-quality binding

### 11.5 Message-Format Translators (T4 — Pattern D)

- [ ] **BL.P.155** — EDI X12 parser/emitter (shared: 850/856/810/820 retail; 837/835/270/271 HLS)
- [ ] **BL.P.156** — HL7 v2.x parser/emitter
- [ ] **BL.P.157** — HL7 CDA / C-CDA parser
- [ ] **BL.P.158** — EPCIS event parser/emitter
- [ ] **BL.P.159** — OAGIS message parser/emitter
- [ ] **BL.P.160** — IATA PADIS parser

### 11.6 Cross-Standard Translators (T3 Pattern D)

- [ ] **BL.P.161** — GS1 ↔ Schema.org Product (round-trip)
- [ ] **BL.P.162** — HL7 v2 → FHIR R4 (one-way with conformance suite)
- [ ] **BL.P.163** — HL7 CDA → FHIR R4 (one-way)
- [ ] **BL.P.164** — CIM ↔ ISO 15926 (alignment where semantics permit)
- [ ] **BL.P.165** — SAE J1939 ↔ AEMP 2.0

### 11.7 Protocol Adapters (T5 — wrapped in SOR adapters, Sprint 15)

These stay in `packages/apex-adapters/` (Sprint 15), not schema packages:

- [ ] **BL.P.166** — OPC UA adapter core (shared: ER, AXLE, ICE)
- [ ] **BL.P.167** — IEC 61850 adapter core
- [ ] **BL.P.168** — SAE J1939 telematics transport wrapper

---

## 12. Impact on Sprint 2

The **revised Sprint 2 scope** now explicitly addresses standards:

### Original Task 2.1 (SCML) — revised subtasks

- [ ] 2.1.1 — Author entity YAMLs: SKU, Location, Lot, Shipment, Supplier, Item
- [ ] 2.1.2 — Classifications (trade-secret supplier cost, PII on supplier contact)
- [ ] 2.1.3 — **Apply Pattern A identifier bindings**: GS1 GTIN on SKU, SSCC on Shipment, GLN on Location (registered in `STANDARDS`)
- [ ] 2.1.4 — Generate Delta DDL via `ddl-driver`
- [ ] 2.1.5 — Generate Purview registration payload (including classification + `StandardRef` metadata)
- [ ] 2.1.6 — **Pattern D translator** `gs1_to_schema_org` with round-trip test
- [ ] 2.1.7 — **Pattern D translator** EPCIS event parser/emitter (stub with round-trip on one event type)
- [ ] 2.1.8 — Conformance test lane passes

Tasks 2.2 (MERML) and 2.3 (CXML) follow the same revised shape. Sprint 2 duration estimate grows from 3 weeks → **4 weeks** to absorb the standards work.

---

## 13. Open Questions

1. **Terminology-service hosting.** SNOMED CT is ~350k concepts. Do we expect tenants to bring their own terminology service (Snowstorm, TermServer), or do we ship a reference service? Default stance: tenants BYO, APEX ships the hook + a dev-only mock.
2. **Pinning transmission.** When APEX bumps `apex_pinned_version` for FHIR R4 → R5, tenants currently pinned at APEX `0.3.x` that don't upgrade — do they stay on R4 indefinitely, or is there a forced-upgrade policy driven by Appendix K (Independence / Compliance)?
3. **Licence review for production.** Before the first client ships, Deloitte Legal should sign off on the attribution + redistribution matrix in §8. Flagged as a gate before Sprint 18 reference deployments.
4. **Standards-bump cadence.** FHIR moves fast (R4 → R4B → R5 in ~4 years). ISA-95 has not moved since 2018. We propose quarterly registry audit, bumping only when consumers need it. Confirm cadence.
5. **Version-pin per tenant vs per APEX release?** Spec currently allows both; default is per-APEX-release to keep Fleet simple. Confirm.

---

## 14. Definition of Done (for this plan to close)

This plan closes when:

1. BL.P.134–P.137 (registry infra + CLI + CI lane) ship in Sprint 2.
2. All Sprint 2 entity code uses Pattern A bindings via `StandardRef` — no raw regex scattered in entity modules.
3. First `apex-standards-*` package (proof of concept — recommend `apex-standards-opentravel` for smallest footprint, or `apex-standards-fhir` if we want the biggest blocker resolved early) ships before Sprint 3 HLS work starts.
4. `apex standards audit` CI job is mandatory on every PR touching schemas.
5. `LICENSE-ATTRIBUTION.md` template + per-package license file in place.
6. Open questions §13 answered.
