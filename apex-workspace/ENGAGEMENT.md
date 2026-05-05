---
file: ENGAGEMENT.md
version: 0.2.0
scope: engagement
class: Internal
required: true
immutable_during_run: true
inherits_from:
  - APEX-CORE.md
  - CHARTER.md
authors:
  - Deloitte DMTSP — Consumer Industry
purpose: >
  Engagement-specific collaborator list, escalation rota, contractual
  windows, and named thresholds. Inherits constitutional rules from
  APEX-CORE and Practice rules from CHARTER; never restates them.
---

# ENGAGEMENT — Tenant Configuration

> Anchor template for Wave-1 reference deployments. Each engagement
> ships its own ENGAGEMENT.md derived from this template with concrete
> client identifiers, collaborator list, and contractual windows.

## §1 — Engagement identity

- **Engagement code:** `apex-{tenant}-{practice}-wave1`
- **Practice:** RC (anchor; per-engagement override)
- **Reference deployment:** `big-box-store` (anchor; per-engagement override)
- **Wave:** 1 (Envision & Land)
- **Contract type:** fixed-fee (per Sellers Guide §2.6)

## §2 — Collaborators (escalation rota)

| Role | Named contact | Escalation latency | Bands they receive |
|------|---------------|--------------------|--------------------|
| Engagement lead | (per-engagement) | 15 min | §3 ask-first + §4 escalate |
| Engagement controller | (per-engagement) | 30 min | budget breaches |
| Engagement counsel | (per-engagement) | 30 min | Independence near-misses |
| Engagement security lead | (per-engagement) | 15 min | manifest hash mismatches |
| APEX SRE on-call | (rota) | 5 min | Redis unreachable, missed HEARTBEAT |
| Tenant DPO | (per-engagement) | 30 min | PII / PCI exposure |
| Data engineering lead | (per-engagement) | 30 min | source drift > 5% |

## §3 — Contractual windows

- **Standard HITL deadline:** 60 minutes (CHARTER default)
- **Close-acceleration window:** day 1–8 of every month, HITL deadline
  compressed to 15 minutes
- **Black-out windows:** none default; per-engagement override applies

## §4 — Named thresholds

Default Wave-1 thresholds. Per-engagement OPERATOR.md overrides.

| Threshold | Default | Cited by |
|-----------|---------|----------|
| Refund / credit auto-cap | $1000 | AGENTS §3 |
| Inventory reservation auto-cap | 100 units / $5000 retail | AGENTS §3 |
| Source-drift escalation | 5% delta vs. SOR at temporal cut | AGENTS §4 |
| Anomaly variance escalation | 5% vs. trailing 7-day mean | HEARTBEAT routine 3 |
| Budget breach during close | absolute (no soft cap) | AGENTS §4 |

## §5 — Cross-references

- `APEX-CORE.md` §6 — HITL is non-negotiable
- `CHARTER.md` §4 — HITL gate registry per Practice
- `OPERATOR.md` §2 — operator-specific override of §4 thresholds
- `HEARTBEAT.md` — periodic-routine schedule
- `AGENTS.md` §6 — operating rules per HEARTBEAT routine

End of ENGAGEMENT.md.
