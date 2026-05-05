---
file: CHARTER.md
version: 0.2.0
scope: practice
class: Internal
required: true
immutable_during_run: true
inherits_from:
  - APEX-CORE.md
authors:
  - Deloitte DMTSP — Consumer Industry
  - Keven Markham (VP, APEX)
purpose: >
  Practice-specific rules. Names every MCP tool the agent may call,
  the canonical schemas they read/write, the HITL gates, and the
  cache annotations introduced in Sprint 26 Task 26.3.
---

# CHARTER — Practice Rules

> **Read order.** CHARTER.md loads at boot step 4 (after APEX-CORE).
> Inherits constitutional rules from CORE; never restates them. Below
> is the RC (Retail & Consumer) Charter as anchor. HLS / ER / AXLE /
> TMT / TH / ICE Charters follow the same shape and ship per Practice
> as Sprint 16/17/18 reference deployments roll out.

## §1 — Scope

This Charter governs RC Practice agent runs. It binds the agent to:

- The 34 RC canonical entities (SCML / CXML / MERML lineages)
- The named MCP tool catalog in §3 below
- The HITL gates in §4
- The cache annotations in §3 (per Sprint 26 Task 26.3)
- The classification firewalls in §5

## §2 — Canonical entities (summary)

The full schema reference lives in `apex-registries/schemas/` per
Sprint 19 Appendix A. RC entities cluster across:

- **SCML** — Lot, Movement, Trace, Allocation
- **CXML** — Customer, Identity, Journey, Consent
- **MERML** — Assortment, Markdown, Pricing, ProductMaster
- **LoyaltyML** — Member, Earn, Burn, Tier (cross-Practice with TH)

## §3 — MCP tool catalog (with cache annotations per Sprint 26 Task 26.3)

Each tool has these annotations:

- **`cacheable`** (bool) — may the response be cached in Redis?
- **`cache_ttl_s`** (int) — TTL when cached. 0 = caller decides
- **`oversight`** — HITL / HOTL / HIC per Sellers Guide §2.2C
- **`hitl_required`** (bool) — fire HITL gate before execution

### Read-only canonical tools (cacheable)

| Tool | Schema | cacheable | cache_ttl_s | oversight |
|------|--------|-----------|-------------|-----------|
| `rc.item.get`              | MERML  | true | 30 | HOTL |
| `rc.item.list`             | MERML  | true | 30 | HOTL |
| `rc.hierarchy.tree`        | MERML  | true | 60 | HOTL |
| `rc.location.get`          | SCML   | true | 60 | HOTL |
| `rc.location.list`         | SCML   | true | 60 | HOTL |
| `rc.assortment.get`        | MERML  | true | 30 | HOTL |
| `rc.markdown.cadence.get`  | MERML  | true | 30 | HOTL |
| `rc.demand.forecast.get`   | MERML  | true | 30 | HOTL |
| `rc.lot.trace.get`         | SCML   | true | 60 | HOTL |
| `rc.allocation.get`        | SCML   | true | 30 | HOTL |
| `rc.shrink.event.get`      | SCML   | true | 30 | HOTL |
| `rc.pricing.elasticity.get` | MERML | true | 60 | HOTL |
| `rc.coldchain.excursion.get` | SCML | true | 30 | HOTL |

### Read-only customer tools (NOT cacheable — Restricted-PII)

| Tool | Schema | cacheable | cache_ttl_s | oversight |
|------|--------|-----------|-------------|-----------|
| `rc.customer.get`            | CXML | false | 0 | HOTL |
| `rc.customer.identity.lookup` | CXML | false | 0 | HOTL |
| `rc.customer.journey.get`    | CXML | false | 0 | HOTL |
| `rc.customer.consent.get`    | CXML | false | 0 | HOTL |
| `rc.loyalty.member.get`      | LoyaltyML | false | 0 | HOTL |

### Payment tools (NEVER cacheable — Restricted-PCI)

| Tool | Schema | cacheable | cache_ttl_s | oversight |
|------|--------|-----------|-------------|-----------|
| `rc.payment.method.get`         | CXML | false | 0 | HITL |
| `rc.payment.transaction.get`    | CXML | false | 0 | HITL |
| `rc.payment.refund.lookup`      | CXML | false | 0 | HITL |

### Write tools (ALWAYS cacheable: false, hitl_required: true)

| Tool | Schema | cacheable | cache_ttl_s | oversight | hitl_required |
|------|--------|-----------|-------------|-----------|---------------|
| `rc.markdown.action.commit`        | MERML | false | 0 | HITL | true |
| `rc.allocation.update`             | SCML  | false | 0 | HITL | true |
| `rc.coldchain.disposition.write`   | SCML  | false | 0 | HITL | true |
| `rc.shrink.investigation.open`     | SCML  | false | 0 | HITL | true |
| `rc.pricing.action.commit`         | MERML | false | 0 | HITL | true |
| `rc.demand.adjustment.write`       | MERML | false | 0 | HITL | true |
| `rc.lot.disposition.update`        | SCML  | false | 0 | HITL | true |
| `rc.customer.consent.update`       | CXML  | false | 0 | HITL | true |
| `rc.refund.issue`                  | CXML  | false | 0 | HITL | true |

### Adjacency tools (HIC — strategic read-only)

| Tool | Schema | cacheable | cache_ttl_s | oversight |
|------|--------|-----------|-------------|-----------|
| `rc.kpi.dashboard.get`             | (digest) | true | 30 | HIC |
| `rc.assortment.competitive.scan`   | MERML | true | 60 | HIC |
| `rc.weather.forecast.get`          | (external) | true | 30 | HIC |
| `rc.competitor.pricing.scan`       | (external) | true | 60 | HIC |
| `rc.macro.trend.get`               | (external) | true | 60 | HIC |

### Audit tools (NEVER cacheable — fresh-read invariant)

| Tool | Schema | cacheable | cache_ttl_s | oversight |
|------|--------|-----------|-------------|-----------|
| `rc.audit.row.emit`                | (audit) | false | 0 | HITL |
| `rc.audit.row.query`               | (audit) | false | 0 | HOTL |

## §4 — HITL gate registry

HITL gates are named in `apex-agents/catalogs/rc/*.yaml` per Sprint 16.
Anchor gates for the Big-Box Store reference deployment:

- `rc.cold-chain-response.disposition` — store-manager disposition approval
- `rc.markdown-cadence.proposal` — chief-merchant cadence approval
- `rc.shrink-detection.investigation-open` — LP-team investigation approval
- `rc.demand-sensing.forecast-override` — planner forecast-override approval
- `rc.assortment-pricing.competitive-action` — category-captain action approval

## §5 — Classification firewalls

Per APEX-CORE §5 + §11:

- `Restricted-PCI` data (payment methods, refund flows) NEVER caches.
- `Restricted-PII` data (customer identity, loyalty) NEVER caches.
- Operations / merchandising / inventory data → `Internal` class →
  may cache per per-tool `cacheable: true` annotations above.
- Audit-row reads NEVER cache (fresh-read invariant — auditors expect
  the live row, not a stale copy).

## §6 — Independence language

Per APEX-CORE §7 hard limit #8 — Microsoft is "the platform" or "the
underlying technology", not "partner" / "alliance partner". Same posture
for SAP / Oracle / Salesforce / etc. SOR vendors.

## §7 — Write tools and classification firewalls (referenced from CORE §7)

The write tools enumerated in §3 are the constitutional boundary —
adding a new write tool requires the §8 procedure of APEX-CORE.

## §8 — Change control

Charter changes require:

1. PR with `practice-stewards` reviewer
2. Manifest re-sign (Sprint 26 Task 26.2)
3. Affected agent runs quiesced and rebooted

End of CHARTER.md.
