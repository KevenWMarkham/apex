# apex-axlecml

**APEX AXLECML** (Automotive / Industrial Manufacturing Canonical Markup Language) — Pattern C entities over ISA-95 + SAE J1939 + ISO 14224.

## Entities

- `Equipment` — production-floor asset (consumes ISA-95 `Isa95Equipment`)
- `WorkCenter` — production cell / line (consumes ISA-95 `Isa95WorkCenter`)
- `ProductionEvent` — batch start / end / transition (ISA-95 + ISA-88 shape)
- `QualityResult` — per-unit / per-batch quality measurement
- `Genealogy` — lot / serial traceability edges
- `BillOfMaterials` — product structure (STEP AP242-aligned — stub-level in Sprint 3)
- `J1939Signal` — vehicle-bus signal reference (consumes SAE J1939 SPN/PGN)
- `AxleReliabilityRecord` — failure / repair event (consumes ISO 14224)

## Translators

- `translators/isa95_to_axlecml.py` — ISA-95 Equipment hierarchy → AXLECML Equipment tree
- `translators/j1939_to_axlecml.py` — J1939 CAN frame → J1939Signal canonical record

## What defers

- Full STEP AP242 parser — BL.P later sprint
- OPC UA schema modelling — never (protocol adapter, Sprint 15)
- ISA-88 batch recipe model — stub in Sprint 3

Design anchor: `Sprint-3-Practice-Schemas-Plan.md` §3.3.
