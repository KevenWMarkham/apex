---
file: OPERATOR.md
version: 0.2.0
scope: operator
class: Internal
required: true
immutable_during_run: true
inherits_from:
  - APEX-CORE.md
  - CHARTER.md
  - ENGAGEMENT.md
authors:
  - Deloitte DMTSP — Consumer Industry
purpose: >
  The human at the keyboard. Per-operator threshold overrides, working
  hours, primary collaborators. Loaded at boot step 5 (after ENGAGEMENT,
  before HEARTBEAT). Constitutional rules + Practice rules + engagement
  rules all inherit downward; OPERATOR may only LOOSEN write thresholds
  via explicit override.
---

# OPERATOR — Per-User Configuration

> Anchor template for Wave-1 reference deployments. Each operator ships
> their own OPERATOR.md derived from this template.

## §1 — Operator identity

- **Operator UPN:** `(per-operator)`
- **Display name:** `(per-operator)`
- **Engagement code:** inherits from ENGAGEMENT.md
- **Role:** `category-captain` / `store-manager` / `analyst` / etc.
- **Working hours / time zone:** `(per-operator)`

## §2 — Threshold overrides (downward only — never tighter than ENGAGEMENT)

Per APEX-CORE §7 hard limits, the operator can only relax thresholds
within the bands ENGAGEMENT permits. The operator can never raise a
threshold above ENGAGEMENT's named cap.

| Threshold | Default (ENGAGEMENT) | Operator override (per-operator) |
|-----------|---------------------|----------------------------------|
| Refund auto-cap | $1000 | `(<= $1000)` |
| Inventory reservation cap | 100 units / $5000 | `(<= ENGAGEMENT cap)` |
| HITL deadline | 60 min (15 min during close) | `(>= ENGAGEMENT deadline)` |

## §3 — Primary collaborators (operator-specific subset)

Operator's most-frequent escalation targets — a subset of ENGAGEMENT §2.

## §4 — Working preferences

- **Surfaces:** Teams card / Copilot Studio / mobile per-operator
- **Notification batching:** per-operator
- **Memory cadence:** end-of-shift (default) / end-of-day / per-decision

## §5 — Cross-references

- `ENGAGEMENT.md` §4 — engagement-level thresholds (the upper bound)
- `AGENTS.md` §3 — operator threshold cited by ask-first band
- `memory/MEMORY.md` — operator's curated memory surface

End of OPERATOR.md.
