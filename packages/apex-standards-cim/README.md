# apex-standards-cim

**Pattern-B** mirror for IEC 61970 (Power System) + IEC 61968 (Utility Operations) CIM.

**Consumed by:** `apex-ercml`.

## Scope (Sprint 3 Phase 1)

- `shared/` — MRID, DateTimeInterval, UnitSymbol (shared primitives)
- `iec_61970/` — core power-system classes (Asset, Equipment, EnergyEvent)
- `iec_61968/` — utility-operations subset (Meter, Reading, WorkOrder, Customer reference)

## What defers

- IEC 62325 market model (no ER agent in Sprint 3 consumes it)
- Full IEC 61970-301 class hierarchy (only the classes ER agents actually consume ship in Sprint 3)

Licence: IEC publishes CIM under commercial licence. APEX ships **structural mirrors only** (class shapes), not IEC text or diagrams.

Design anchor: `Sprint-3-Practice-Schemas-Plan.md` §4.2.
