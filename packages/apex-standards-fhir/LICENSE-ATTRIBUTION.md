# apex-standards-fhir — Third-Party Content Attribution

This package mirrors structural definitions from HL7 FHIR.

## HL7 FHIR

- **Authority:** Health Level Seven International (HL7)
- **URL:** https://www.hl7.org/fhir/
- **License:** Creative Commons CC0 1.0 Universal (Public Domain Dedication)
- **Redistribution:** Structural definitions may be freely redistributed with attribution.

This package ships **Pydantic models whose structure mirrors a subset of FHIR R4 resources**. It does **not** ship FHIR ValueSets, CodeSystems, or terminology content.

## Terminologies referenced but not redistributed

The following terminologies are referenced by FHIR resources in this package via regex-validated identifier fields. Their vocabulary content is **not** included.

| Terminology | Authority | License | Consumer note |
|-------------|-----------|---------|---------------|
| LOINC | Regenstrief Institute | Free with registration | Tenants BYO terminology service |
| SNOMED CT | SNOMED International | Member-country fee | Tenants BYO; tied to national licence |
| RxNorm | NLM | Public domain | Tenants may embed locally |
| ICD-10-CM | CDC/NCHS | Public domain (US) | — |
| NDC | FDA | Public domain | — |
| CPT | AMA | Commercial licence | Tenants BYO |
| HCPCS Level II | CMS | Public domain | — |
