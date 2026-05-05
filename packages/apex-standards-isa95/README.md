# apex-standards-isa95

**Pattern-B** mirror for ISA-95 (ANSI/ISA-95.00.01 through 95.00.05, 2018 edition).

**Shared by:** `apex-ercml`, `apex-axlecml`, `apex-iceml`.

## Scope (Sprint 3 Phase 1)

- **Hierarchy** — Enterprise → Site → Area → WorkCenter → WorkUnit
- **Personnel** — PersonnelClass + Person
- **Equipment** — EquipmentClass + Equipment + capabilities
- **Material** — MaterialClass + Material + type (raw / WIP / finished)
- **Hierarchy validator** — `validate_hierarchy()` checks parent/child FK integrity across a set of entities

## What defers

- ISA-88 batch model (stub reference only)
- Full B2MML XML round-trip
- SP95 operations-management scheduling objects

Design anchor: `Sprint-3-Practice-Schemas-Plan.md` §4.3.
