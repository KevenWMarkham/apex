# apex-standards-isa95 — Third-Party Content Attribution

This package mirrors structural definitions from ISA-95.

## ISA-95 — Enterprise / Control System Integration

- **Authority:** International Society of Automation (ISA) / IEC 62264
- **URL:** https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95
- **Pinned version:** 2018
- **License:** Royalty-free for implementations; standard text remains under ISA copyright
- **Pattern:** B (data model mirror) per `Industry-Standards-Incorporation-Plan.md` §3
- **Redistribution:** Class names, attribute names, and structural relationships are reflected in Pydantic models. **Standard text is NOT redistributed** — obtain the ISA-95 document directly from ISA.

## What this package ships

- Pydantic models named after ISA-95 / B2MML classes
  (`PersonnelClass`, `EquipmentClass`, `MaterialClass`, `ProductSegment`,
  `OperationsDefinition`, `OperationsRequest`, `OperationsResponse`, etc.)
- B2MML XML namespace constants
- Hierarchy-level enumerations (Enterprise, Site, Area, Work Center, Work Unit)

## What this package does NOT ship

- Full ISA-95 standard text or B2MML schema documents
- Verbatim clause text
- Diagrams reproduced from the standard

## Tenant responsibility

Tenants holding manufacturing-execution-system contracts that require ISA-95
conformance attestation must:

1. Hold their own ISA-95 licence (royalty-free for implementations; document
   text is licensed)
2. Provide their own B2MML XSD artifacts when XML-binding is required

## Restricted content guardrail

CI scans this package for known ISA-95 document fingerprints (clause
numbers, verbatim definitions) and fails the build on detection.
