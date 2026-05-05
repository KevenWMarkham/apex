# APEX — Third-Party Content Attribution

This document is the workspace-level attribution manifest for the APEX
monorepo. The APEX framework is **proprietary — Deloitte Internal**. APEX
incorporates structural patterns and identifier formats from third-party
industry standards. Per-package attribution files (`LICENSE-ATTRIBUTION.md`
inside each `apex-standards-*` package) carry the binding-level detail.

## Industry standards referenced by APEX

| Standard | Authority | Pattern (IS-Plan §3) | License | Redistribution? | Per-package file |
|----------|-----------|----------------------|---------|-----------------|------------------|
| GS1 GTIN / SSCC / GLN | GS1 | A (regex identifier) | Royalty-free | OK | (binding via `apex-schemas-common.standards`) |
| EPCIS 2.0 | GS1 | D (message format) | Royalty-free | OK | (binding via `apex-schemas-common.standards`) |
| Schema.org | Schema.org consortium | D | Open | OK | (binding via `apex-schemas-common.standards`) |
| HL7 FHIR R4 | HL7 International | B (data model mirror) | Royalty-free / CC0 | OK | `apex-standards-fhir/LICENSE-ATTRIBUTION.md` |
| LOINC | Regenstrief Institute | A | Restricted (free with registration) | **No vocabulary redistribution** | `apex-standards-fhir/LICENSE-ATTRIBUTION.md` |
| SNOMED CT | SNOMED International | A | Restricted (member-country fee) | **No vocabulary redistribution** | `apex-standards-fhir/LICENSE-ATTRIBUTION.md` |
| ICD-10-CM | CDC/NCHS | A | Open (US public domain) | OK | `apex-standards-fhir/LICENSE-ATTRIBUTION.md` |
| NDC | FDA | A | Open (US public domain) | OK | `apex-standards-fhir/LICENSE-ATTRIBUTION.md` |
| CPT | AMA | A | Restricted (commercial licence) | **No vocabulary redistribution** | `apex-standards-fhir/LICENSE-ATTRIBUTION.md` |
| HCPCS Level II | CMS | A | Open | OK | `apex-standards-fhir/LICENSE-ATTRIBUTION.md` |
| RxNorm | NLM | A | Open | OK | `apex-standards-fhir/LICENSE-ATTRIBUTION.md` |
| ISA-95 | ISA | B (data model mirror) | Royalty-free | OK | `apex-standards-isa95/LICENSE-ATTRIBUTION.md` |
| ISO 14224 | ISO | B | Restricted (commercial licence) | **Taxonomy mirror only — no redistribution of standard text** | `apex-standards-iso14224/LICENSE-ATTRIBUTION.md` |
| IEC 61970 / 61968 (CIM) | IEC | B | Restricted (commercial licence) | **Structural pattern only — no redistribution of standard text** | `apex-standards-cim/LICENSE-ATTRIBUTION.md` |
| SAE J1939 | SAE International | A | Restricted (commercial licence) | **Identifier format only — no redistribution** | `apex-standards-j1939/LICENSE-ATTRIBUTION.md` |
| TM Forum SID | TM Forum | B | Open (member benefit) | OK | `apex-standards-sid/LICENSE-ATTRIBUTION.md` |
| OpenTravel (OTA) | OpenTravel Alliance | B | Open | OK | `apex-standards-opentravel/LICENSE-ATTRIBUTION.md` |
| IATA NDC | IATA | B+C | Royalty-free | OK | (binding via `apex-schemas-common.standards`) |
| EIDR Content ID | EIDR | A | Open | OK | (binding via `apex-schemas-common.standards`) |
| CDISC ODM / SDTM | CDISC | B | Open | OK | `apex-standards-cdisc/LICENSE-ATTRIBUTION.md` |

The catalog at
`packages/apex-schemas-common/src/apex_schemas_common/standards/catalog.yaml`
is the machine-readable source of this table; CI fails on drift between
that catalog and the in-memory `STANDARDS` registry.

## Restricted-terminology guardrail

APEX **never redistributes** any of the following content sources:

- LOINC concept tables, mappings, or display text
- SNOMED CT concept tables, mappings, descriptions, or relationships
- ICD-10 / ICD-11 tabular text or code descriptions
- CPT code descriptors or modifier text
- ISO standard documents (full text)
- IEC standard documents (full text)
- SAE J1939 SPN/PGN data dictionaries (full text)

APEX binds to these via **regex-validated identifier types** plus a
tenant-supplied terminology service (FHIR `$lookup` / `$translate` / etc.).
The CI pipeline scans every package source tree for known restricted
content patterns and fails the build if any is present (see
`tools/check_restricted_terminology.py`).

## Open-source licensing of APEX framework code

The framework Python packages (apex-core, apex-agents, apex-services, etc.)
are **proprietary — Deloitte Internal**. They depend on permissively-licensed
open-source libraries (Pydantic, Typer, PyYAML, pytest, Hatchling). No AGPL
or copyleft dependencies are present.

## Updating this document

Run `apex standards sync-catalog` to regenerate the machine-readable catalog;
update this attribution manifest whenever a new `apex-standards-*` package is
added or a standard's redistribution status changes.

Cross-reference: `Industry-Standards-Incorporation-Plan.md` §4 (binding
patterns) and §6 (licensing posture).
