# apex-standards-cdisc

**Pattern-B** mirror for CDISC Operational Data Model (ODM) + Study Data Tabulation Model (SDTM) subsets.

**Consumed by:** `apex-hlscml` (StudyML entities).

## Scope (Sprint 3 Phase 1)

### ODM

- `CdiscStudy` — study-level metadata
- `CdiscSubject` — trial participant
- `CdiscFormData` — captured form at one visit

### SDTM skeletons

- `SdtmDemographics` (DM domain) — one row per subject
- `SdtmAdverseEvent` (AE domain) — safety events
- `SdtmLabResult` (LB domain) — lab measurements

## What defers

- Define-XML metadata
- ADaM analysis-ready datasets
- Full SDTMIG 3.x controlled terminology

Design anchor: `Sprint-3-Practice-Schemas-Plan.md` §4.6.
