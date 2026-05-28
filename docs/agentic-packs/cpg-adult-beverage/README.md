# Sazerac House — Channel 5 of the Agentic Marketplace

> Sazerac-anchored CPG / adult-beverage Channel. The wedge event: **Buffalo Trace allocation alert** — when a small-volume release lands at a specific retailer in the customer's market, the Channel surfaces a reserved-bottle hold with one-tap purchase and age-verified pickup. The Channel also runs everyday adult-beverage replenishment, cocktail concierge with ingredient orchestration, and tasting-event / distillery-tour bookings. Age-gated commerce + state-by-state shipping rules are the non-trivial compliance footprint.

**Parent Edition:** `TMT` + `RC` (CPG sits under Retail & Consumer)
**Channel category:** CPG / Adult Beverage
**New service-code family:** `TMT-TEL-BEV-01..04`
**Companion build-spec amendment:** [`docs/build-specs/apex-tmt-agentic-beverage-amendment.md`](../../build-specs/apex-tmt-agentic-beverage-amendment.md)
**Status:** Draft
**Anchor partner:** Sazerac Company (Buffalo Trace, Pappy Van Winkle, Eagle Rare, Blanton's, Sazerac Rye, Weller, Stagg, Van Winkle family)
**Bench:** Diageo (Johnnie Walker, Crown Royal, Bulleit), Pernod Ricard (Jameson, Glenlivet, Absolut), Brown-Forman (Woodford, Jack Daniel's, Old Forester), Constellation Brands (Casa Noble, High West, Bulleit's sister High Note)

## Pack contents

| # | Document | Purpose |
|---|---|---|
| 01 | [Business model](./01-business-model.md) | Sazerac as anchor; allocation-economics as wedge |
| 02 | [Adult-beverage signals](./02-beverage-signals.md) | Allocation feeds, age-verification, state-shipping-rules, retailer inventory |
| 03 | [ERD & Postgres extensions](./03-erd-and-postgres.md) | `beverage_order`, `allocation_alert`, `age_verification`, `tasting_event` |
| 04 | [Medallion (Bronze / Silver / Gold)](./04-medallion-bronze-silver-gold.md) | Sazerac, Diageo, Pernod, Brown-Forman Bronze landings |
| 05 | [Services catalog](./05-services-catalog.md) | `TMT-TEL-BEV-01..04` |
| 06 | [Partnership map](./06-partnership-map.md) | Sazerac anchor + Diageo, Pernod Ricard, Brown-Forman, Constellation bench |
| 07 | [Business value model](./07-business-value-model.md) | Lower attach but higher per-engaged-HH ARPU |
| 08 | [Consumer business case](./08-consumer-business-case.md) | Allocation wedge; cocktail concierge as everyday hook |
| 09 | [Portability / open-home](./09-portability-open-home.md) | Cellar inventory, allocation history, age-verification portability |
| 10 | [Ecosystem differentiators](./10-beverage-differentiators.md) | Why Telco wins this against ReserveBar, Drizly, retailer-direct |

## Service codes

| Service | Scenario | YAML | Description |
|---|---|---|---|
| `TMT-TEL-BEV-01` | `TMT-CX-46-sazerac-replenishment` | `tmt/36-sazerac-replenishment.yaml` | Age-verified adult-beverage replenishment with state-shipping compliance |
| `TMT-TEL-BEV-02` | `TMT-CX-47-sazerac-allocation-alerts` | `tmt/37-allocation-alerts.yaml` | Buffalo Trace / Pappy / Eagle Rare allocation alerts with reserved holds |
| `TMT-TEL-BEV-03` | `TMT-CX-48-sazerac-cocktail-concierge` | `tmt/38-cocktail-concierge.yaml` | Recipes + ingredient orchestration across retailers |
| `TMT-TEL-BEV-04` | `TMT-CX-49-sazerac-tasting-events` | `tmt/39-tasting-events.yaml` | Distillery tours, tasting events, allocation-line VIP access |

## Three things that make this Channel work

1. **Allocation economics.** Buffalo Trace's Antique Collection, Pappy Van Winkle, Eagle Rare 17, Stagg Jr — small-volume releases that sell out within hours of landing on shelves. Customers will pay for a structured alert + reserved-hold mechanism. **Sazerac wins by being the source of truth for its own allocation calendar.**
2. **Age verification is the compliance hard part.** Every other agentic-commerce flow assumes the customer is who they say they are; adult beverage requires affirmative age verification at point of sale + delivery + (in 3-tier states) at the licensed retailer. The pack treats this as a first-class concern.
3. **Lower attach rate is fine.** Only ~12–18% of households will subscribe — but engaged subscribers have **3–5x higher ARPU** than baseline retail customers, especially in the bourbon / allocation collector segment. The Channel is a high-value-per-subscriber bet, not a high-attach bet.
