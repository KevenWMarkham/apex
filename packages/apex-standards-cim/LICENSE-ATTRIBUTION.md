# apex-standards-cim — Third-Party Content Attribution

This package mirrors **structural patterns** from IEC 61970 (Power System CIM)
and IEC 61968 (Utility Operations CIM). It does **not** redistribute the IEC
standard text.

## IEC 61970 — Common Information Model (Power System)

- **Authority:** International Electrotechnical Commission (IEC)
- **URL:** https://webstore.iec.ch/publication/61167
- **Pinned version:** 2021
- **License:** Restricted — IEC publishes under commercial licence
- **Pattern:** B (data model mirror — structural pattern only) per `Industry-Standards-Incorporation-Plan.md` §3
- **Redistribution:** **Standard text is NOT redistributed.** Class names, attribute names, and structural relationships are public-domain facts about the standard and are reflected in Pydantic models for interoperability. The full IEC document must be obtained directly from IEC.

## IEC 61968 — Common Information Model (Utility Operations)

- **Authority:** IEC
- **URL:** https://webstore.iec.ch/publication/6197
- **Pinned version:** 2020
- **License:** Restricted — commercial IEC licence
- **Pattern:** B
- **Redistribution:** Same posture as IEC 61970.

## What this package ships

- Pydantic models named after CIM classes (`Substation`, `Feeder`,
  `ConductingEquipment`, `Asset`, `Outage`, `Customer`, etc.) with field
  names mirroring CIM attributes
- RDF/XML namespace constants for CIM IRI generation
- IRI validators for CIM URIs

## What this package does NOT ship

- Full IEC 61970 / 61968 standard text
- Full CIM RDF/XML schemas (these must be obtained from IEC or via an
  authorized redistribution channel)
- Profile bundles (CGMES, MultiSpeak, etc.) — those require their own
  authority approval

## Tenant responsibility

Tenants deploying APEX in regulated electric-utility contexts must:

1. Hold their own IEC 61970 / 61968 licence(s) where the engagement requires
   reference to standard text
2. Provide their own CGMES / MultiSpeak profile artifacts where applicable
3. Audit their CIM IRI assignments against tenant-controlled namespaces

## Restricted content guardrail

CI scans this package for known IEC document fingerprints (clause numbers,
verbatim definitions) and fails the build if any verbatim standard text is
detected.
