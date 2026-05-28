# 01 — Business Model

> Walmart's existing retail muscle gets a new distribution channel; the Telco gets a high-attach Channel with deep action commerce flow; the household gets errand-chain orchestration that no single-retailer app can deliver. Mutually beneficial in a way that closed retail apps structurally cannot replicate.

## 1. What Walmart already does well — and what it can't

Walmart is the world's largest retailer by revenue. They already have:

- ~10,500 stores across 24 countries
- Walmart+ membership (~25M US members)
- Walmart Health clinics + Pharmacy
- Walmart Auto Care Centers (Tire, Lube, Express — TLE)
- Sam's Club (membership wholesale)
- Walmart Connect (advertising network)
- Walmart Fulfillment Services (3rd-party logistics)

What Walmart **cannot** structurally do alone:

| Limitation | Why |
|---|---|
| Route customers to Target / Costco when Walmart doesn't have the SKU | Brand-conflicted |
| Orchestrate errand chains across competitors | Walmart-app-only |
| Read in-home pantry signals from Samsung / LG / Whirlpool | No vault relationship |
| Read eldercare signals from wearables / sleep trackers | No PHI infrastructure |
| Bundle with airline + hotel + auto on one monthly bill | No consumer billing relationship |

The Telco delivers each of these. Walmart joins as a Channel and gets distribution it cannot build alone.

## 2. The Walmart Retail Channel value exchange

```
              TO WALMART                          TO TELCO
   - Higher-AOV verified-intent orders     - Per-order rev-share (3–5%)
   - Lower CAC on Walmart+ memberships     - Walmart Health PMPM share
   - Pharmacy refill volume                - TLE service-call commerce
   - TLE service-call volume               - Member-tier optimization fee
   - Vault-side household signal           - Subscription on Telco bill ($7.99 / mo)
```

Walmart pays the Telco roughly the same way Hulu pays the Telco today for bundled streaming distribution — per included subscriber per month — **plus** action commerce. The combined economics are several multiples of Walmart's existing CAC on Walmart-app-direct customers.

## 3. The errand-chaining wedge

The headline use case:

```
Saturday morning, 9:30 AM. Household intent: "we need to do the weekend errands"

The Walmart Retail Channel orchestrator:
  1. Reads pantry signals from HOM-01 → grocery list to Walmart Pickup
  2. Reads HOM-03 (eldercare) → Mom's blood pressure med ready at Walmart Pharmacy
  3. Reads HOM-07 (vehicle) → oil change overdue, TLE has 11 AM slot at same store
  4. Reads household calendar → kid's birthday Tuesday, no gift yet (Target run needed)
  5. Reads previous-week purchases → Costco run for paper goods every 3 weeks, due now
  6. Reads home repair backlog (HOM-04) → light fixture for kitchen (Home Depot)

Drafts a single chained route:
  9:45 AM → Costco (paper goods, ~25 min)
  10:30 AM → Walmart Supercenter (grocery + pharmacy + TLE) — 60 min
  11:30 AM → Target (kid gift) — 15 min
  11:55 AM → Home Depot (light fixture) — 10 min
  12:15 PM → home

Total customer time: 2.5 hrs vs. typical 3.5–4.5 hrs unplanned
Customer pays: Walmart bill + Costco bill + Target bill + Home Depot bill
                (split correctly across the cards-on-file the customer chose)
Telco earns: 3–5% take-rate across $200–400 in chained spend
```

This is the **value moment** the Walmart Channel delivers. It cannot be delivered by Walmart-direct, by Target-direct, by Costco-direct, or by Amazon. It requires the **multi-retailer orchestration layer** the Telco uniquely operates.

## 4. Why Walmart says yes despite multi-retailer routing

Walmart is the anchor, but the Channel will route to Target / Costco / Best Buy / Home Depot when those retailers fit better. This is a feature, not a bug, for Walmart:

| Benefit | Why |
|---|---|
| Walmart is the **default retailer** in the orchestrator's routing logic — chosen unless explicitly displaced | Capture share of intent that customers would otherwise route to competitors |
| Walmart Health pharmacy refills get routed to Walmart automatically because the household connected their account | Higher repeat-fill rate than direct-app baseline |
| Walmart+ memberships get co-bundled with the Telco bill, lowering Walmart+ CAC | Member acquisition at a fraction of Walmart's current paid-acquisition cost |
| Walmart Connect (Walmart's ad network) gets a high-intent context surface | Customer-vault-aware sponsored placements (with disclosure) |

Walmart trades **exclusivity it never actually had** (customers always shopped multi-retailer) for **structured priority** (default-routing) and **acquisition-cost reduction** (lower CAC on memberships). The trade is favourable.

## 5. Three revenue layers, applied to Retail

| Layer | Walmart Channel motion |
|---|---|
| Consumer subscription | $7.99 / mo Channel subscription on Telco bill |
| Action commerce | 3–5% of basket (groceries via HOM-01 already coded, GM via RTL-01 new) + per-prescription fee (RTL-02) + per-service-call share (RTL-03) |
| Outcome / risk-share | Limited — Walmart Health PMPM for chronic conditions (overlap with future Health Channel) |

## 6. Per-household economic envelope

Family-bundle subscriber adding the Walmart Channel ($7.99 / mo):

| Service | Annual transaction volume per HH | Telco take-rate envelope | Annual contribution |
|---|---|---|---|
| RTL-01 GM | 30–50 orders × $60 avg | 3–4% | $55–100 |
| RTL-02 Pharmacy | 8–24 refills × $15 avg | $1–2 per refill + Walmart Health PMPM | $20–60 |
| RTL-03 Auto Care | 2–4 TLE visits × $80 avg | 5–8% | $10–25 |
| RTL-04 Membership | Walmart+ + Sam's tier optimization | Member-attribution fee | $10–20 |
| **Subscription + commerce** | | | **$95–205 / yr per Walmart-Channel HH** |

At 30–45% attach rate on a 20M-HH base, the Walmart Channel produces **~$600M–1.8B / yr in Telco GP**.

## 7. What the Channel does not try to be

- **Not Walmart-direct.** Walmart's own app is excellent for Walmart-only orders. The Channel adds the multi-retailer + cross-Channel orchestration layer.
- **Not Instacart.** Instacart is a delivery-shopper marketplace; the Channel is an intent-orchestration marketplace. Different layer of the stack; can coexist with Instacart as fulfilment partner.
- **Not Amazon-displacement.** Amazon is a different retailer category (long-tail, fast-delivery, marketplace). The Channel doesn't try to win Amazon's surface; it wins the **everyday-physical-retail** surface where Amazon is weaker.
