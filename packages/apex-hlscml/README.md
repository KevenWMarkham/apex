# apex-hlscml

**APEX HLSCML** (Healthcare & Life Sciences Canonical Markup Language) — Pattern C canonical entities over FHIR R4 + CDISC ODM/SDTM.

## Entities

**FHIR-aligned (clinical):**
- `Patient` — tokenised MRN, name, address, phone, email
- `Practitioner` — tokenised NPI + name
- `Encounter` — visit / admission
- `Observation` — lab result / vital sign (LOINC-coded)
- `DiagnosticReport` — clinical findings report
- `MedicationRequest` — prescription / order (RxNorm + NDC)
- `ClaimHeader` / `ClaimLine` — billing (CPT + HCPCS)

**CDISC-aligned (clinical trials):**
- `Study` — trial-level metadata
- `StudyEnrollment` — trial participant
- `AdverseEvent` — safety event (MedDRA)

## Classifications

**Heavy PHI surface.** Every direct identifier uses the `_token` suffix and `Classification.PHI`. Silver never holds cleartext; tokens only. Tokenisation happens at the Bronze→Silver boundary (Sprint 5 ships the runtime; Sprint 3 uses a placeholder function).

## Translators

- `translators/fhir_to_hlscml.py` — FHIR → HLSCML (tokenises on ingest)
- `translators/hlscml_to_fhir.py` — HLSCML → FHIR (detokenises for authorised identities only)
- `translators/hl7v2_to_fhir.py` — stub (full parser: BL.P.156)
- `translators/cda_to_fhir.py` — stub (full parser: BL.P.157)
