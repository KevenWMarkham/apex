# Automobile — Channel 6 of the Agentic Marketplace

> The full vehicle ownership lifecycle as a single Channel. Discovery → purchase → financing → insurance → ownership → aftermarket → charging/fueling → resale, all orchestrated through the household vault. Where the existing `mobility-auto/` Channel focuses on Toyota-anchored connected-vehicle operations, this Channel focuses on the **transactional and commercial lifecycle** across all OEMs and the broader vehicle ecosystem. The wedge event: a customer researches a vehicle on Saturday morning; by Tuesday evening they're driving it home — every step (financing pre-approval, insurance binding, trade-in valuation, dealer negotiation, registration) orchestrated through the Telco rather than the customer's seven open browser tabs.

**Parent Editions:** `TMT` (Telco) + `AXLE` (Automotive & Manufacturing)
**Channel category:** Automobile (broader than Mobility)
**New service-code family:** `TMT-TEL-AUT-01..08`
**Companion build-spec amendment:** [`docs/build-specs/apex-tmt-agentic-automobile-amendment.md`](../../build-specs/apex-tmt-agentic-automobile-amendment.md)
**Marketplace meta-pack:** [`../_marketplace/`](../_marketplace/)
**Sibling Mobility Channel:** [`../mobility-auto/`](../mobility-auto/) — Toyota-anchored, connected-vehicle ops
**Status:** Draft

## Anchor partners — multi-anchor by design

| Anchor | Coverage |
|---|---|
| **AutoNation** | Largest US new + used dealer group; covers purchase, service, parts, finance, insurance — the closest thing to a single-anchor full-lifecycle partner |
| **Cox Automotive** (Kelley Blue Book, Autotrader, Dealer.com, Manheim, vAuto) | Data-side anchor — valuation, listings, dealer ops, wholesale auctions |
| **Progressive** | Insurance anchor; Snapshot UBI program is the most mature consumer-telematics UBI in the US |

## Bench partners

- **Dealer groups:** Lithia Motors, Group 1 Automotive, Penske Automotive Group, Sonic Automotive
- **Used-car retailers:** CarMax, Carvana, Vroom (when active), Peddle
- **OEMs:** Ford, GM, Tesla, Honda, Hyundai, Stellantis (handoffs to/from `mobility-auto/` for connected services)
- **Auto financing:** Capital One Auto Navigator, Ally Auto, Chase Auto, USAA, credit unions
- **Insurance carriers:** State Farm, Allstate, Geico, USAA, Liberty Mutual, Root, Lemonade Car
- **Aftermarket parts:** AutoZone, Advance Auto Parts, O'Reilly, NAPA, RockAuto
- **Charging networks:** ChargePoint, EVgo, Electrify America, Tesla Supercharger
- **Fuel networks:** Shell, Chevron, BP, ExxonMobil, Costco Gas, GasBuddy
- **Fleet:** Element Fleet, Wheels Donlen (B2B-leaning, but small-business households apply)
- **Title / registration / DMV automation:** Vitu, ALG, state-specific DMV partners

## Pack contents

| # | Document | Purpose |
|---|---|---|
| 01 | [Business model](./01-business-model.md) | Lifecycle-as-Channel; the multi-anchor model |
| 02 | [Automobile lifecycle state machine](./02-automobile-lifecycle.md) | Researching → Shopping → Purchasing → Owning → Selling state machine |
| 03 | [ERD & Postgres extensions](./03-erd-and-postgres.md) | `vehicle_listing`, `purchase_offer`, `financing_application`, `aftermarket_part_order`, `charging_session`, `fleet_vehicle`, `resale_listing` |
| 04 | [Medallion (Bronze / Silver / Gold)](./04-medallion-bronze-silver-gold.md) | AutoNation, KBB, Progressive Bronze landings |
| 05 | [Services catalog](./05-services-catalog.md) | `TMT-TEL-AUT-01..08` |
| 06 | [Partnership map](./06-partnership-map.md) | Multi-anchor partnership map |
| 07 | [Business value model](./07-business-value-model.md) | Per-service unit economics; lifetime value of a vehicle purchase |
| 08 | [Consumer business case](./08-consumer-business-case.md) | Purchase orchestration as wedge; lifecycle continuity |
| 09 | [Portability / open-home](./09-portability-open-home.md) | Vehicle ownership history, financing records, insurance policy data portability |
| 10 | [Ecosystem differentiators](./10-automobile-differentiators.md) | Why Telco wins this against OEM-direct, dealer apps, marketplace aggregators |

### Diagrams

- [`diagrams/mermaid-automobile-lifecycle.md`](./diagrams/mermaid-automobile-lifecycle.md) — full ownership-lifecycle state machine
- [`diagrams/flow-purchase-end-to-end.md`](./diagrams/flow-purchase-end-to-end.md) — Saturday-morning research → Tuesday-evening drive-home

## Service codes

| Service | Scenario | Agent YAML | Description |
|---|---|---|---|
| `TMT-TEL-AUT-01` | `TMT-CX-50-vehicle-discovery` | `tmt/40-vehicle-discovery.yaml` | Discovery, research, comparison via KBB + Autotrader + Edmunds + OEM inventory |
| `TMT-TEL-AUT-02` | `TMT-CX-51-vehicle-purchase` | `tmt/41-vehicle-purchase.yaml` | Purchase orchestration via AutoNation + dealer-direct + CarMax / Carvana |
| `TMT-TEL-AUT-03` | `TMT-CX-52-auto-financing` | `tmt/42-auto-financing.yaml` | Pre-approval shopping across Capital One Auto, Ally, Chase, AutoNation Finance, credit unions |
| `TMT-TEL-AUT-04` | `TMT-CX-53-auto-insurance` | `tmt/43-auto-insurance.yaml` | Quote, bind, manage policies across Progressive (anchor), State Farm, Geico, Allstate, Root, USAA |
| `TMT-TEL-AUT-05` | `TMT-CX-54-aftermarket-accessories` | `tmt/44-aftermarket.yaml` | AutoZone, Advance, O'Reilly, NAPA, RockAuto parts + accessories |
| `TMT-TEL-AUT-06` | `TMT-CX-55-charging-fueling` | `tmt/45-charging-fueling.yaml` | Multi-network charging + fuel-price optimization (Shell, Costco Gas, ChargePoint, EVgo) |
| `TMT-TEL-AUT-07` | `TMT-CX-56-fleet-management` | `tmt/46-fleet-management.yaml` | Multi-vehicle households + small-business fleets; mileage-log + tax-deduction tracking |
| `TMT-TEL-AUT-08` | `TMT-CX-57-resale-endoflife` | `tmt/47-resale-endoflife.yaml` | Trade-in vs private-sale vs CarMax vs Carvana vs donate; orchestrates the choice |

## Three things that make this Channel work

1. **The vehicle ownership lifecycle is fragmented across 15+ apps today.** Research lives in 4–6 sites. Purchase happens in dealer-direct apps. Financing requires bank-by-bank applications. Insurance requires carrier-by-carrier quotes. Aftermarket parts live in another set of apps. Charging stations in another. Resale in three more. The household has **no single source of truth** for their vehicle relationship. The Channel becomes that source of truth.
2. **The purchase moment is the highest-leverage event.** Average new-car transaction is $48K; used is $26K. The Channel's value at the purchase moment alone justifies the subscription. Every other lifecycle service (financing, insurance, ongoing ownership) compounds from that anchor.
3. **Insurance + financing are the high-LTV ongoing services.** $1,400–2,200 annual auto-insurance premium per vehicle × 1.8 vehicles per household; $4–8B+ in auto-finance origination per year per Telco subscriber base. Even 1% take rate on these layers materially shifts the Channel's economics.

## Relationship to other Channels

| Adjacent Channel | Boundary |
|---|---|
| `mobility-auto/` (Toyota Connected, MOB-01..04) | Toyota-specific connected-vehicle ongoing operations. The Automobile Channel handles the broader lifecycle; `mobility-auto/` is the OEM-mediated ongoing-ownership layer. When the customer owns a Toyota, both Channels coordinate. |
| `telco/` Home Channel HOM-07 (vehicle) | HOM-07 reads telematics for in-home orchestration. Automobile reads telematics for purchase / insurance / resale decisions. Same underlying data; different decisioning. |
| `retail/` Retail Channel RTL-03 (Walmart Auto Care) | RTL-03 handles independent-network service (TLE). Automobile handles OEM-dealer + parts purchases. |
| `travel-hospitality/` Travel Channel HOM-15 (ground mobility) | HOM-15 handles in-trip vehicle (rideshare, rental). Automobile handles owned-vehicle. |
