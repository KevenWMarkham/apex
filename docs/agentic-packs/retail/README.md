# Walmart Retail — Channel 3 of the Agentic Marketplace

> Walmart-anchored everyday-retail Channel for the Telco's agentic marketplace. Extends grocery orchestration (already in `HOM-01`) into the rest of the Walmart everyday-life surface: general merchandise, pharmacy + health, auto care (TLE), and membership-tier optimization across Walmart+, Sam's Club, Costco. The wedge event is **errand chaining** — Walmart Pharmacy prescription ready + Costco grocery list + Home Depot return + Walmart Auto Care oil change, all sequenced into a single optimized route on the customer's preferred Saturday morning.

**Parent Edition:** `TMT` (Telco) + `RC` (Retail & Consumer)
**Channel category:** Retail
**New service-code family:** `TMT-TEL-RTL-01..04`
**Companion build-spec amendment:** [`docs/build-specs/apex-tmt-agentic-retail-amendment.md`](../../build-specs/apex-tmt-agentic-retail-amendment.md)
**Marketplace meta-pack:** [`../_marketplace/`](../_marketplace/)
**Status:** Draft
**Primary author:** tmt-practice-lead@deloitte.com / rc-practice-lead@deloitte.com

## The thesis in one paragraph

The Telco's Walmart Channel is not a Walmart-direct app. It is **Walmart-as-a-Channel inside the Telco marketplace**, alongside Marriott, American Airlines, Toyota, Sazerac. The Channel orchestrates the household's everyday-retail behaviour — what to buy, where to buy it (Walmart / Target / Costco / Sam's Club), when to pick it up, how to chain errands across stores — and lets Walmart pay for the privilege of being the default. The wedge isn't a new shopping app; the wedge is **eliminating the 4–6 errand-related tasks a household sequences per weekend**, replaced with a single orchestrator that drafts the chain and executes it.

## Pack contents

| # | Document | Purpose |
|---|---|---|
| 01 | [Business model](./01-business-model.md) | Walmart as anchor; retail Channel economics |
| 02 | [Retail signal feeds](./02-retail-signal-feeds.md) | Purchase history, pharmacy refills, loyalty signals, store-locator + inventory feeds |
| 03 | [ERD & Postgres extensions](./03-erd-and-postgres.md) | New entities: `retail_order`, `prescription`, `auto_service_appointment`, `membership_tier` |
| 04 | [Medallion (Bronze / Silver / Gold)](./04-medallion-bronze-silver-gold.md) | Walmart, Target, Costco, Best Buy, Home Depot Bronze landings; retail Silver + Gold |
| 05 | [Services catalog](./05-services-catalog.md) | `TMT-TEL-RTL-01..04` services |
| 06 | [Partnership map](./06-partnership-map.md) | Walmart anchor + Target, Costco, Best Buy, Home Depot bench |
| 07 | [Business value model](./07-business-value-model.md) | Per-service unit economics; Walmart Channel P&L envelope |
| 08 | [Consumer business case](./08-consumer-business-case.md) | Errand-chaining as wedge; pharmacy-as-eldercare-extension |
| 09 | [Portability / open-home](./09-portability-open-home.md) | Walmart-side vault data, loyalty exports, multi-retailer portability |
| 10 | [Ecosystem differentiators](./10-retail-differentiators.md) | Why the Telco wins this against Amazon, Walmart-direct, Instacart |

## Anchor service mapping

| Service code | Scenario | Agent YAML | Description |
|---|---|---|---|
| `TMT-TEL-RTL-01` | `TMT-CX-38-walmart-merchandise` | `tmt/28-walmart-merchandise.yaml` | General merchandise + cross-store inventory orchestration |
| `TMT-TEL-RTL-02` | `TMT-CX-39-walmart-pharmacy` | `tmt/29-walmart-pharmacy.yaml` | Pharmacy refills, Walmart Health, OTC reconciliation |
| `TMT-TEL-RTL-03` | `TMT-CX-40-walmart-auto-care` | `tmt/30-walmart-auto-care.yaml` | TLE oil change, tire service, battery service |
| `TMT-TEL-RTL-04` | `TMT-CX-41-membership-optimizer` | `tmt/31-membership-optimizer.yaml` | Walmart+, Sam's Club, Costco tier optimization |

## Three things that make this Channel work

1. **Walmart's scale gives the Channel reach from day one.** ~90% of US population lives within 10 miles of a Walmart store. The Channel can launch nationally without store-density gaps.
2. **Errand-chaining is multi-retailer by design.** Walmart is the anchor, but customers also shop Target, Costco, Best Buy, Home Depot. The Channel routes intents to the optimal retailer; Walmart wins by being the default, not by being the only option.
3. **Pharmacy connects to eldercare.** A Walmart Health prescription ready signal flows into HOM-03 (eldercare) and HOM-06 (wellness). The Retail Channel is not an isolated silo — it shares context with the Home Channel.
