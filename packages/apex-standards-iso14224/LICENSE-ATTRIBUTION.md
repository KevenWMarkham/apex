# apex-standards-iso14224 — Third-Party Content Attribution

This package mirrors **taxonomy structure** from ISO 14224. It does **not**
redistribute ISO standard text.

## ISO 14224 — Reliability Data Collection for Petroleum, Petrochemical and Natural Gas Industries

- **Authority:** International Organization for Standardization (ISO)
- **URL:** https://www.iso.org/standard/64076.html
- **Pinned version:** 2016
- **License:** Restricted — ISO publishes under commercial licence
- **Pattern:** B (data model mirror — taxonomy mirror only) per `Industry-Standards-Incorporation-Plan.md` §3
- **Redistribution:** **Standard text is NOT redistributed.** Class names and taxonomy hierarchy positions are reflected in Pydantic models / enumerations for interoperability. The full ISO document must be obtained directly from ISO or an authorized national-body distributor.

## What this package ships

- Pydantic models named after ISO 14224 entity classes
  (`Equipment`, `FailureMode`, `MaintenanceItem`, `RootCauseCategory`)
- Equipment-class hierarchy enumerations
- Failure-mode taxonomy enumerations
- Validators for ISO 14224 codified field formats

## What this package does NOT ship

- Full ISO 14224 standard text
- Verbatim clause definitions or annex content
- Diagrams reproduced from the standard
- Full failure-mode mapping tables (these must be obtained from ISO)

## Tenant responsibility

Tenants in the upstream oil & gas / mining / heavy-industrial space deploying
APEX with ISO 14224 conformance attestation must:

1. Hold their own ISO 14224 licence
2. Provide their own complete failure-mode mapping content where the
   engagement requires it

## Restricted content guardrail

CI scans this package for known ISO 14224 document fingerprints (verbatim
clause text, full taxonomy table dumps) and fails on detection.
