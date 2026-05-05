# Cross-Standard Translator — Lossy-Case Catalog

**Sprint 24 exit criterion:** "Each translator ships with a round-trip
conformance suite (lossy cases are documented explicitly)."

This document catalogs every information-loss path across the
cross-standard translators in `apex_translators.cross_standard`.
Round-trip tests in `tests/test_cross_standard.py` verify that
**lossless** cases survive `B(A(x)) == x`; **lossy** cases are excluded
from those round-trips and called out here.

## Common rule

If a translator drops or coerces a field, the loss is documented in this
file with: source field → target placement (or "dropped"), severity
(structural / cosmetic / unsafe), and a recommendation for the calling
ingestion pipeline.

---

## HL7 v2 → FHIR R4 (Task 24.2 / BL.P.162)

| Source | Target / Disposition | Severity |
|--------|---------------------|----------|
| `PID-13` repetitions 2..N (additional phone numbers) | first repetition only kept on `Patient.telecom`; rest dropped | cosmetic |
| `OBX-2` value-type ED, RP, AD (encapsulated/binary/address) | not yet supported — emitted as `Observation.valueString` if non-empty | structural |
| `OBX-5` numeric with malformed `OBX-6` units | `valueQuantity.code` set best-effort to raw unit string; UCUM compliance not validated | cosmetic |
| `MSH-21` profile identifier | not propagated to `Bundle.meta.profile` | structural |
| `EVN` segment | not yet mapped to `Encounter.statusHistory` | structural |
| `IN1` insurance segment | not yet mapped to `Coverage` | structural |
| `OBR-7` observation-period (single timestamp) | mapped to `effectiveDateTime`; range form (`OBR-7`/`OBR-8`) not yet captured | structural |
| Unknown `MSH-9` message type | only ADT/ORU/ORM family handled; other families emit Patient-only Bundle | structural |
| HL7 v2 escape sequences (`\\F\\`, `\\S\\`) | left as literal text; no unescape pass | cosmetic |

**Recommendation:** the v2-to-FHIR family is one-way per Sprint 24 spec.
For tenants needing reverse mapping, use the upstream FHIR servers'
`$message` operator instead of round-tripping through this translator.

## HL7 CDA → FHIR R4 (Task 24.3 / BL.P.163)

| Source | Target / Disposition | Severity |
|--------|---------------------|----------|
| Section without recognized `templateId` | dropped from output (no Composition.section emitted in v1) | structural |
| Observation without coded `value` | captured as `Observation.valueString` from entry text | cosmetic |
| Free-text-only section (no `<entry>` elements) | mapped to a single resource with `code.text` populated, no structured code | cosmetic |
| `effectiveTime` with low/high bounds | only point-in-time captured if present; range form not yet extracted | structural |
| Author / custodian / informant | dropped (Patient + section resources only in v1) | structural |
| Document-level metadata (`code`, `confidentialityCode`) | dropped | structural |

**Recommendation:** for CDAs requiring full provenance round-trip
fidelity, retain the original CDA XML alongside the FHIR Bundle and
reference it via `DocumentReference.attachment.contentType="text/xml"`.

## CIM ↔ ISO 15926 (Task 24.4 / BL.P.164)

| Source | Target / Disposition | Severity |
|--------|---------------------|----------|
| CIM equipment class outside `CIM_ISO_EQUIPMENT_MAP` | `KeyError` raised with extension guidance | structural — translator refuses |
| ISO 15926 RDL class outside `ISO_CIM_EQUIPMENT_MAP` | `KeyError` raised | structural — translator refuses |
| CIM RDF graph relationships (Substation → Bay → Equipment) | not propagated; only the asset itself is translated | structural |
| ISO 15926 lifecycle states (Possible / Actual) | not yet mapped | structural |
| `_cim_class` round-trip marker on properties | preserved across one round-trip; tenants relying on it for IRI generation should pin it | cosmetic |

**Recommendation:** this translator is for **per-asset** translation.
For full topology graphs, walk the CIM `RDFGraph` and translate each
asset individually, then rebuild the topology in ISO 15926 with the
named-asset object IDs.

## SAE J1939 ↔ AEMP 2.0 (Task 24.5 / BL.P.165)

| Source | Target / Disposition | Severity |
|--------|---------------------|----------|
| J1939 PGN outside `J1939_PGN_MAP` | `KeyError` raised | structural — translator refuses |
| AEMP event type outside `AEMP_PGN_MAP` | `KeyError` raised | structural — translator refuses |
| OEM-specific J1939 PGNs (>= 65500 ranges, vendor extensions) | not in the named cross-OEM set; tenants extend the map per OEM | structural |
| J1939 multi-PGN composite signals (e.g., position from two PGNs) | currently 1:1 PGN ↔ event only; composites need orchestration upstream | structural |
| AEMP `extras` fields (OEM-specific telematics extensions) | preserved on round-trip via `_source_pgn` / `_source_spn` markers; non-marker extras retained as-is | cosmetic |
| J1939 SPN range data (e.g., 0xFE = "not available") | passed through as-is to AEMP value; consumer must filter | unsafe |

**Recommendation:** keep `J1939_PGN_MAP` curated to the AEMP minimum-set
plus the named PGNs each fleet's OEMs emit. Don't use this translator
for diagnostic-trouble-code (DM1) decoding — that needs the
`apex-standards-j1939` SPN dictionary directly.

## Cross-cutting

- **Time zones.** All translators emit FHIR / AEMP timestamps in UTC.
  Source-format zone offsets are normalized into UTC before output.
- **Identifiers.** New `id` fields (Bundle, resource, etc.) are
  generated per call (UUID v4). Two calls with the same input produce
  different `id` values; round-trips compare structural content,
  not generated identifiers.
- **Coding-system OIDs.** Common OIDs are mapped to FHIR system URIs
  (LOINC, SNOMED, ICD-10, NDC). Unmapped OIDs round-trip as
  `urn:oid:<oid>` URIs.
