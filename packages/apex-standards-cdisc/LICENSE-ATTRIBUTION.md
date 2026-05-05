# apex-standards-cdisc — Third-Party Content Attribution

This package mirrors structural definitions from CDISC ODM and SDTM.

## CDISC ODM (Operational Data Model)

- **Authority:** Clinical Data Interchange Standards Consortium (CDISC)
- **URL:** https://www.cdisc.org/standards/data-exchange/odm
- **Pinned version:** 2.0
- **License:** Open standard (CDISC public domain dedication for foundational standards)
- **Pattern:** B (data model mirror) per `Industry-Standards-Incorporation-Plan.md` §3
- **Redistribution:** Structural definitions may be freely redistributed with attribution.

## CDISC SDTM (Study Data Tabulation Model)

- **Authority:** CDISC
- **URL:** https://www.cdisc.org/standards/foundational/sdtm
- **Pinned version:** 2.0
- **License:** Open
- **Pattern:** B
- **Redistribution:** OK with attribution.

## What this package ships

This package ships **Pydantic models whose structure mirrors a subset of
CDISC ODM and SDTM domains** plus identifier validators for CDISC-canonical
field names (USUBJID, STUDYID, DOMAIN, VISIT, etc.). It does **not** ship
the full CDISC Controlled Terminology vocabulary.

## Terminologies referenced but not redistributed

| Terminology | Authority | License | Consumer note |
|-------------|-----------|---------|---------------|
| CDISC Controlled Terminology | NCI EVS | Open | Tenants pull current release from NCI EVS; APEX pins by version pointer |
| MedDRA | ICH | Restricted (subscription) | Tenants BYO MedDRA licence + content; APEX validates regex format only |
| WHODrug | UMC | Restricted (subscription) | Tenants BYO; APEX validates regex format only |
| ICD-10-CM | CDC/NCHS | Open | Cross-referenced; see `apex-standards-fhir/LICENSE-ATTRIBUTION.md` |

## Restricted content guardrail

This package contains **no MedDRA term content, no WHODrug term content, and
no full CDISC CT vocabulary tables.** All restricted-terminology bindings are
via regex-validated identifier types and tenant-supplied terminology services.
