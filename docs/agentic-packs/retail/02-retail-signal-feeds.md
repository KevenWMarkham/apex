# 02 — Retail Signal Feeds

> Data feeds that the Walmart Retail Channel consumes from across the household, the partner retailer ecosystem, and shared catalog services.

## 1. In-household signals (already in Home pack)

- Smart-fridge / pantry sensors → inventory state (overlap with HOM-01)
- Trash barcode scanners → disposal-driven reorder signals
- HVAC consumables (filter status) → home-improvement reorder triggers
- HOM-03 eldercare signals → triggers for pharmacy + OTC purchases
- HOM-07 vehicle signals → triggers for auto-care
- Smart speakers / phones → voice intents ("we're out of ...")

## 2. Partner-retailer signals (new in this Channel)

| Source | Feed type | Classification |
|---|---|---|
| Walmart purchase history | `bronze.tmt_rtl.walmart_orders` | pii |
| Walmart Health prescription history | `bronze.tmt_rtl.walmart_rx` | phi |
| Walmart+ membership status | `bronze.tmt_rtl.walmart_plus_membership` | pii |
| Walmart Auto Care (TLE) appointment / service history | `bronze.tmt_rtl.walmart_tle` | pii |
| Walmart Connect ad-engagement | `bronze.tmt_rtl.walmart_connect` | pii |
| Target purchase history | `bronze.tmt_rtl.target_orders` | pii |
| Target Circle loyalty | `bronze.tmt_rtl.target_circle` | pii |
| Costco membership + purchase | `bronze.tmt_rtl.costco_purchases` | pii |
| Sam's Club membership + purchase | `bronze.tmt_rtl.sams_club` | pii |
| Best Buy purchases + protection plans | `bronze.tmt_rtl.bestbuy` | pii |
| Home Depot purchases + Pro account | `bronze.tmt_rtl.homedepot` | pii |
| Kroger purchases (overlaps HOM-01 grocery) | `bronze.tmt_rtl.kroger` | pii |

## 3. Public / shared catalog signals

| Source | Use |
|---|---|
| UPC / GTIN product catalog | Cross-retailer product normalization |
| CPSC recall feeds | Product safety alerts |
| FDA OTC + drug catalog | Pharmacy safety alerts |
| USDA grocery nutrition data | Dietary cross-reference |

## 4. Cross-Channel signal exchange

The Walmart Retail Channel **reads from** and **writes to**:

| Channel | Read | Write |
|---|---|---|
| Home | Pantry state, eldercare context, vehicle service-due | Grocery + OTC orders that affect inventory |
| Travel | Trip-mode state | None (skipped during trips) |
| Mobility (Toyota) | Vehicle telematics | TLE coordinated with Toyota dealer service preference |
| CPG / Beverage | Adult-beverage preferences | Age-gated product orders routed via BEV Channel |

Cross-Channel signal exchange happens via the orchestrator (HOM-99); the Walmart Channel does not read Home Bronze directly.

## 5. Consent scopes consumed

The Walmart Channel requires (and exposes individually-revocable scopes for):

- `purchases` — retail purchase history (always required)
- `purchases.pharmacy` — prescription history (RTL-02 only; PHI-classified)
- `vehicle` — for RTL-03 auto care
- `loyalty` — for Walmart+, Costco, Target Circle, Sam's Club account access

A customer who revokes `purchases.pharmacy` keeps RTL-01, RTL-03, RTL-04 functional but pauses RTL-02. The marketplace's granular consent design tolerates partial activation.
