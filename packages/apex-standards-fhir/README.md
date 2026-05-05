# apex-standards-fhir

**Pattern-B** mirror package for HL7 FHIR R4/R5.

Scope (Sprint 3 Phase 1):

- **R4 resources:** Patient, Encounter, Observation, DiagnosticReport, MedicationRequest, Practitioner, Claim
- **Shared primitives:** Identifier, HumanName, ContactPoint, Address, Period, Reference, Coding, CodeableConcept, Quantity
- **R5:** skeleton module only — consumed by nothing in Sprint 3
- **Migration:** `migrations/r4_to_r5.py` stub
- **Terminology service:** `terminology/mock.py` dev-only in-memory mock; tenants swap for a real terminology server (Snowstorm, TermServer, etc.)

Design anchor: `docs/APEX - Design and Build/Sprint-3-Practice-Schemas-Plan.md` §3.1, §4.1.

## FHIR compatibility

- Field names are snake_case (Python convention) with FHIR camelCase aliases.
- Models accept construction by either naming via `populate_by_name=True`.
- JSON dump with `by_alias=True` emits FHIR-conformant JSON.
- Fields not in scope are silently tolerated (`extra="ignore"`) so real FHIR payloads don't fail to parse.

## Scope discipline

**Every new FHIR field requires a PR tied to a consuming APEX agent or service.** Additions for "completeness" are rejected. See Sprint 3 Plan §9 (risks).

## License attribution

HL7 FHIR content is royalty-free with attribution. See `LICENSE-ATTRIBUTION.md`.
