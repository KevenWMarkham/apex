# 05 — Services Catalog (`TMT-TEL-RTL-01..04`)

> Four sub-agents in the Walmart Retail Channel. Independently subscribable on the Telco bill; each maps to a scenario folder and agent YAML.

## Service codes

| Service code | Scenario folder | Agent YAML | Description | Headline KPI |
|---|---|---|---|---|
| `TMT-TEL-RTL-01` | `TMT-CX-38-walmart-merchandise` | `tmt/28-walmart-merchandise.yaml` | Multi-retailer general-merchandise + errand-chain orchestration | Errand-chain time saved per HH |
| `TMT-TEL-RTL-02` | `TMT-CX-39-walmart-pharmacy` | `tmt/29-walmart-pharmacy.yaml` | Pharmacy refills + Walmart Health + OTC reconciliation | Adherence rate; refill on-time rate |
| `TMT-TEL-RTL-03` | `TMT-CX-40-walmart-auto-care` | `tmt/30-walmart-auto-care.yaml` | TLE oil change, tire, battery; coordinated with Mobility Channel | Avoided unplanned service events |
| `TMT-TEL-RTL-04` | `TMT-CX-41-membership-optimizer` | `tmt/31-membership-optimizer.yaml` | Walmart+ / Costco / Sam's Club / Amazon Prime tier optimization | Net annual savings on memberships |

## Anchor + bench partners

| Service | Anchor | Bench |
|---|---|---|
| RTL-01 GM | Walmart | Target, Costco, Sam's Club, Best Buy, Home Depot, Lowes |
| RTL-02 Pharmacy | Walmart Pharmacy / Walmart Health | CVS, Walgreens (handoff to future Health Channel) |
| RTL-03 Auto Care | Walmart Auto Care (TLE) | Jiffy Lube, Firestone, dealer service (handoff to Mobility Channel) |
| RTL-04 Membership | Walmart+ | Costco, Sam's Club, Amazon Prime |

## Archetype mapping

| Service | Archetype | Oversight | HITL gates |
|---|---|---|---|
| RTL-01 | `F2-event-cluster-pattern-match` | HOTL | Chain total > $200 |
| RTL-02 | `F1-continuous-monitor-hitl-alert` | HITL | Any PHI-classified action; controlled-substance handling |
| RTL-03 | `F3-predictive-trigger-workflow-aware` | HOTL | Service cost estimate > $150 |
| RTL-04 | `F2-event-cluster-pattern-match` | HOTL | Membership cancellation or downgrade |

## Pricing

| Bundle | Channels included | Monthly price |
|---|---|---|
| Walmart Channel — basic | RTL-01 + RTL-04 | $4.99 |
| Walmart Channel — full | RTL-01..04 | $7.99 |
| Family Bundle + Walmart | Home Family + Walmart full | $25.99 |
| Marketplace Everything | All Channels | $49.99 (33% off à la carte) |

## Action-commerce take rates

| Service | Take rate envelope | Per-event $ |
|---|---|---|
| RTL-01 | 3–5% of order value | $2–6 per order |
| RTL-02 | $1–3 per refill + Walmart Health PMPM share | $1–3 |
| RTL-03 | 5–8% of service cost | $4–10 |
| RTL-04 | Member-attribution fee | $10–30 / yr |

See [`../telco/05-services-catalog.md`](../telco/05-services-catalog.md) for the canonical Home Channel sibling and [`06-partnership-map.md`](./06-partnership-map.md) for partner deal structures.
