# 05 — Services Catalog (`TMT-TEL-BEV-01..04`)

| Service | Description | Headline KPI |
|---|---|---|
| `TMT-TEL-BEV-01` Replenishment | Age-verified adult-beverage replenishment with state-shipping compliance | Compliant-order rate; cellar-replenishment lead time |
| `TMT-TEL-BEV-02` Allocation Alerts | BTAC / Pappy / Eagle Rare 17 / Stagg drop alerts with reserved holds | Allocation hit-rate; customer conversion |
| `TMT-TEL-BEV-03` Cocktail Concierge | Recipes + ingredient orchestration across BEV + Retail Channels | Recipes completed; cross-Channel basket attach |
| `TMT-TEL-BEV-04` Tasting Events | Distillery tours, tasting events, allocation-line VIP access | Event attendance + repeat booking |

## Anchor + bench partners

| Service | Anchor | Bench |
|---|---|---|
| BEV-01 | Sazerac standard (Buffalo Trace, Blanton's, Sazerac Rye, Weller) | Diageo, Pernod Ricard, Brown-Forman, Constellation |
| BEV-02 | Sazerac allocation (BTAC, Pappy, Eagle Rare 17, Stagg) | Bench OEMs' allocated lines (Diageo Special Releases, Glenmorangie Private Edition, Old Forester Birthday Bourbon) |
| BEV-03 | Sazerac cocktail library | Diffords Guide, Liquor.com, Punch (recipe content licensing) |
| BEV-04 | Sazerac House (the visitor experience in New Orleans) + Buffalo Trace Distillery tours | Diageo Master Distiller experiences, Jameson Distillery, Glenlivet Distillery |

## Pricing

| Bundle | Channels | Monthly |
|---|---|---|
| Beverage — Concierge (recipes only, no allocation) | BEV-03 | $2.99 |
| Beverage — Full | BEV-01..04 | $4.99 |
| Family Bundle + Beverage | Home Family + Beverage full | $23.99 |

## Archetype mapping

| Service | Archetype | Oversight | HITL gates |
|---|---|---|---|
| BEV-01 | `F3-predictive-trigger-workflow-aware` | HITL | Any order requires age-verification check; state-eligibility check |
| BEV-02 | `F2-event-cluster-pattern-match` | HITL | Reserved holds always HITL-confirmed before customer commits |
| BEV-03 | `F2-event-cluster-pattern-match` | HOTL | Cross-Channel ingredient routing |
| BEV-04 | `F2-event-cluster-pattern-match` | HITL | Booking fees > $100 / seat |

## Action-commerce take rates

| Service | Take rate |
|---|---|
| BEV-01 | 5–10% of order (higher than other Channels — narrower volume, premium-product mix) |
| BEV-02 | 3–7% (Sazerac-mediated; lower take, but higher AOV) |
| BEV-03 | Mostly indirect (drives BEV-01 and Retail Channel basket) |
| BEV-04 | 10–15% of booking + per-seat distillery referral fee |
