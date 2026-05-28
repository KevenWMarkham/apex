# 05 — Services Catalog (`TMT-TEL-AUT-01..08`)

> Eight sub-agents covering the full vehicle ownership lifecycle. Each independently subscribable on the Telco bill; each 1:1 maps to a scenario folder and agent YAML.

## Service codes

| Code | Scenario folder | Agent YAML | Description | Headline KPI |
|---|---|---|---|---|
| `TMT-TEL-AUT-01` | `TMT-CX-50-vehicle-discovery` | `tmt/40-vehicle-discovery.yaml` | Vehicle research, shortlisting, comparison across KBB / Autotrader / Edmunds / CarGurus / OEM inventory | Time-to-shortlist; Shortlist quality (post-purchase regret rate) |
| `TMT-TEL-AUT-02` | `TMT-CX-51-vehicle-purchase` | `tmt/41-vehicle-purchase.yaml` | Purchase orchestration — AutoNation, dealer-direct, CarMax, Carvana | Walk-out time; out-the-door price vs market |
| `TMT-TEL-AUT-03` | `TMT-CX-52-auto-financing` | `tmt/42-auto-financing.yaml` | Pre-approval shopping + financing execution across lenders | Best-APR delta; pre-approval acceptance rate |
| `TMT-TEL-AUT-04` | `TMT-CX-53-auto-insurance` | `tmt/43-auto-insurance.yaml` | Quote, bind, manage policies — Progressive anchor + State Farm / Geico / Allstate / Root / USAA | Annual premium savings; UBI participation rate |
| `TMT-TEL-AUT-05` | `TMT-CX-54-aftermarket-accessories` | `tmt/44-aftermarket.yaml` | Parts + accessories — AutoZone, Advance, O'Reilly, NAPA, RockAuto | Order accuracy; cross-retailer price savings |
| `TMT-TEL-AUT-06` | `TMT-CX-55-charging-fueling` | `tmt/45-charging-fueling.yaml` | Multi-network charging + fuel-price optimization | Annual fuel/charging cost reduction |
| `TMT-TEL-AUT-07` | `TMT-CX-56-fleet-management` | `tmt/46-fleet-management.yaml` | Multi-vehicle households + small-business fleets, IRS-grade mileage log | Tax-deduction $ captured |
| `TMT-TEL-AUT-08` | `TMT-CX-57-resale-endoflife` | `tmt/47-resale-endoflife.yaml` | Trade-in vs private vs CarMax vs Carvana vs donate; orchestrates the choice | Resale-value delta vs trade-in only |

## Anchor + bench partners by service

| Service | Anchor(s) | Bench |
|---|---|---|
| AUT-01 | Cox Automotive (KBB, Autotrader) | Edmunds, CarGurus, TrueCar, Consumer Reports |
| AUT-02 | AutoNation | Lithia, Penske, Group 1, Sonic; CarMax, Carvana for used |
| AUT-03 | Capital One Auto Navigator | Ally, Chase Auto, USAA, AutoNation Finance, credit unions |
| AUT-04 | Progressive (UBI anchor) | State Farm, Geico, Allstate, Liberty Mutual, Root, Lemonade, USAA |
| AUT-05 | AutoZone | Advance Auto, O'Reilly, NAPA, RockAuto, Amazon Auto |
| AUT-06 | Shell + ChargePoint | Chevron, BP, ExxonMobil, Costco Gas, EVgo, Electrify America, Tesla Supercharger, GasBuddy |
| AUT-07 | Element Fleet (B2B handoff) | Wheels Donlen, MileIQ, Everlance |
| AUT-08 | CarMax (Instant Cash Offer) + AutoNation (trade-in) | Carvana, KBB ICO, Peddle, donate via charity partners |

## Archetype mapping

| Service | Archetype | Oversight | Notable HITL gates |
|---|---|---|---|
| AUT-01 | `F2-event-cluster-pattern-match` | HOTL | Read-only; no writes; recommendations only |
| AUT-02 | `F4-orchestrator-with-subagents` | HITL | Out-the-door price > $5K above shortlist median; trade-in delta > $2K |
| AUT-03 | `F3-predictive-trigger-workflow-aware` | HITL | All credit pulls require explicit authorization; final-financing-decision HITL |
| AUT-04 | `F3-predictive-trigger-workflow-aware` | HITL | Policy bind requires HITL; UBI enrolment opt-in mandatory |
| AUT-05 | `F2-event-cluster-pattern-match` | HOTL | Parts orders > $200 require approval |
| AUT-06 | `F2-event-cluster-pattern-match` | HOTL | Charging-network roaming; no write-side beyond session-initiation |
| AUT-07 | `F1-continuous-monitor-hitl-alert` | HOTL | Tax-deduction submissions require HITL |
| AUT-08 | `F3-predictive-trigger-workflow-aware` | HITL | Resale-channel commitment requires HITL; accepted offer requires HITL |

## Subscription bundles

| Bundle | Channels | Monthly |
|---|---|---|
| Automobile — Lifecycle Core | AUT-01..04 (research → purchase → finance → insurance) | $9.99 |
| Automobile — Full | AUT-01..08 | $11.99 |
| Mobility + Automobile (Toyota household) | mobility-auto/MOB-01..04 + AUT-01..08 | $18.99 |
| Family Bundle + Automobile | Home Family + AUT full | $29.99 |

## Action-commerce take rates

| Service | Take rate envelope |
|---|---|
| AUT-01 | Referral fees from KBB / Autotrader / Edmunds (CPC + CPA model) |
| AUT-02 | 0.5–2% of purchase price (modest %, but $250–950 / vehicle is meaningful) |
| AUT-03 | 0.5–1.5% of financed amount as origination-attribution + servicing-share |
| AUT-04 | 8–15% of first-year insurance commission + UBI premium-savings share |
| AUT-05 | 5–10% on aftermarket-parts purchases |
| AUT-06 | Per-gallon / per-kWh micro-fee share |
| AUT-07 | Subscription-led; minimal action commerce |
| AUT-08 | $100–300 per resale-event attribution fee |

## Cross-references

- Pack README: [`./README.md`](./README.md)
- Business model: [`./01-business-model.md`](./01-business-model.md)
- Partnership map: [`./06-partnership-map.md`](./06-partnership-map.md)
- Build-spec amendment: [`../../build-specs/apex-tmt-agentic-automobile-amendment.md`](../../build-specs/apex-tmt-agentic-automobile-amendment.md)
