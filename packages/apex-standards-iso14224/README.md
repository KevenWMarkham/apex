# apex-standards-iso14224

**Pattern-B** mirror for ISO 14224:2016 — Petroleum, petrochemical and natural-gas industries: collection and exchange of reliability and maintenance data for equipment.

**Shared by:** `apex-axlecml`, `apex-iceml`.

## Scope

- **Equipment taxonomy** — top-level equipment classes (pump, compressor, valve, motor, heat-exchanger, etc.)
- **Failure modes** — controlled vocabulary of failure modes
- **Reliability record** — canonical per-event shape (equipment, failure mode, downtime, cause, repair)

## What defers

- Full ISO 14224 Annex A taxonomy (thousands of leaf nodes) — tenant-specific.
- Confidence intervals / statistical aggregates — computed by agents in later sprints.

Design anchor: `Sprint-3-Practice-Schemas-Plan.md` §4.8.
