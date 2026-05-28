# Toyota Connected — Channel 4 of the Agentic Marketplace

> Toyota-anchored mobility Channel. Extends connected-vehicle telemetry (already in `HOM-07`) into the full Toyota ecosystem — Toyota Connected Services, dealer-network service scheduling, next-vehicle decisioning, Toyota Financial Services, Toyota Insurance — and across the multi-OEM household. The wedge event is **household-fleet recall reconciliation**: cross-references every recall feed (NHTSA, OEM-direct) against every vehicle the household owns, schedules the service, attaches loaner-car or rideshare coverage, surfaces it as a single coordinated action.

**Parent Edition:** `TMT` + `AXLE` (Automotive & Manufacturing)
**Channel category:** Mobility
**New service-code family:** `TMT-TEL-MOB-01..04`
**Companion build-spec amendment:** [`docs/build-specs/apex-tmt-agentic-mobility-amendment.md`](../../build-specs/apex-tmt-agentic-mobility-amendment.md)
**Status:** Draft
**Anchor partner:** Toyota Motor North America (Toyota Connected, Toyota Financial Services, Toyota Insurance Management Solutions)
**Bench:** Ford (SYNC 4 / Lincoln Way), GM (OnStar / Ultium / SuperCruise), Tesla, Honda, Hyundai, Stellantis (Uconnect)

## Pack contents

| # | Document | Purpose |
|---|---|---|
| 01 | [Business model](./01-business-model.md) | Toyota as anchor; multi-OEM household coverage |
| 02 | [Vehicle signal feeds](./02-vehicle-signal-feeds.md) | Telematics, recall, service, charging signals |
| 03 | [ERD & Postgres extensions](./03-erd-and-postgres.md) | New entities: `vehicle`, `vehicle_recall`, `dealer_appointment`, `auto_loan_lease`, `auto_policy` |
| 04 | [Medallion (Bronze / Silver / Gold)](./04-medallion-bronze-silver-gold.md) | OEM Bronze landings + recall feeds + service network |
| 05 | [Services catalog](./05-services-catalog.md) | `TMT-TEL-MOB-01..04` |
| 06 | [Partnership map](./06-partnership-map.md) | Toyota anchor + Ford, GM, Tesla, Honda, Hyundai bench |
| 07 | [Business value model](./07-business-value-model.md) | Per-service unit economics |
| 08 | [Consumer business case](./08-consumer-business-case.md) | Recall-reconciliation wedge; next-vehicle decisioning |
| 09 | [Portability / open-home](./09-portability-open-home.md) | Vehicle data, loan / lease, insurance portability |
| 10 | [Ecosystem differentiators](./10-mobility-differentiators.md) | Why Telco wins this against OEM-direct apps |

## Service codes

| Service | Scenario | YAML | Description |
|---|---|---|---|
| `TMT-TEL-MOB-01` | `TMT-CX-42-toyota-connected-plus` | `tmt/32-toyota-connected.yaml` | Connected vehicle telematics extension to Toyota Connected Services |
| `TMT-TEL-MOB-02` | `TMT-CX-43-toyota-dealer-network` | `tmt/33-toyota-dealer.yaml` | Dealer service appointment scheduling, recall coordination, software updates |
| `TMT-TEL-MOB-03` | `TMT-CX-44-toyota-next-vehicle` | `tmt/34-toyota-next-vehicle.yaml` | Next-vehicle decisioning, trade-in valuation, configurator |
| `TMT-TEL-MOB-04` | `TMT-CX-45-toyota-finance-insurance` | `tmt/35-toyota-finance.yaml` | Toyota Financial Services (lease, loan, refi) + Toyota Insurance |

## Three things that make this Channel work

1. **Households are multi-OEM by default.** The average US household has 1.8 vehicles, often different brands. Toyota wins as Channel anchor *because* it accepts that the Channel will route to Ford / GM / Tesla services when those are the right answer for a non-Toyota vehicle.
2. **Recall reconciliation is universally valuable.** Every vehicle has a non-zero chance of recall annually; coordinating across the household's full fleet is something no single OEM app does.
3. **Toyota Financial Services + Toyota Insurance gives the Channel a deep D-archetype layer.** Lease-end orchestration, refi opportunities, telematics-based insurance — these are the high-LTV moments in mobility, and Toyota has the captive infrastructure for both.
