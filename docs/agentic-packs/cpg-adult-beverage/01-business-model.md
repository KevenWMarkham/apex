# 01 — Business Model

> Sazerac anchors a CPG / adult-beverage Channel where the wedge is **allocation drops** (Buffalo Trace Antique Collection, Pappy Van Winkle, Eagle Rare 17, George T. Stagg, William Larue Weller). The Channel is age-gated, state-shipping-compliant, and tightly integrated with the household vault. Lower attach rate than Home or Retail, but materially higher ARPU per engaged subscriber.

## 1. Why Sazerac as anchor

Sazerac Company owns or distributes:

- **Buffalo Trace Antique Collection** (the BTAC — George T. Stagg, William Larue Weller, Sazerac Rye 18, Eagle Rare 17, Thomas H. Handy)
- **Pappy Van Winkle** (Van Winkle Lot B, Old Rip 10/12, Pappy 15/20/23)
- **Eagle Rare** (regular bourbon line + 17-year-old in BTAC)
- **Blanton's, Weller, Stagg Jr, Sazerac Rye**
- 100+ regional / heritage brands across spirits

What makes Sazerac the natural anchor:

- Sazerac controls the most coveted allocation calendar in the US bourbon market
- The allocation system today is **opaque to consumers** — bottles arrive at retailers, sell within hours, customers have no warning
- A Channel that surfaces allocation drops with reserved-hold mechanics adds enormous value
- Sazerac benefits by reducing scalper-flipper activity and routing scarce product to engaged enthusiasts

## 2. The allocation-alert wedge

```
3-bottle drop of Eagle Rare 17 (2024 BTAC) lands at Pearson's Wine in Washington DC.
Sazerac's distributor releases the SKU to Pearson's at 9:14 AM.

Sazerac House Channel orchestrator:
  1. Sees allocation drop within 60 seconds via partner-side webhook
  2. Filters: Pearson's is in customer's market AND customer has Eagle Rare 17 on watchlist
     AND customer has age-verification in vault AND customer has Reserved-Hold preference
  3. Submits reserved-hold request to Pearson's (Sazerac-mediated)
  4. Pearson's confirms 1-bottle hold valid until 7 PM
  5. Pushes notification to customer: "Eagle Rare 17 reserved for you at Pearson's
     until 7 PM. $129 MSRP. Tap to confirm. Already age-verified. Pickup only."
  6. Customer confirms in 2 minutes
  7. Customer picks up at 6:15 PM
```

Today this experience does not exist anywhere — customers either (a) get lucky walking into a retailer at the right moment, (b) flip on secondary market at 3–10x markup, (c) miss the bottle entirely. The Channel **creates a new market structure** for allocation distribution.

## 3. The everyday hook — cocktail concierge

Allocation is the wedge; cocktail concierge is the everyday hook. The Channel:

- Suggests a cocktail recipe for tonight (based on weather, day-of-week, household preferences)
- Cross-references the household's spirits cabinet (vault-tracked) against the recipe
- Identifies missing ingredients (mixers, citrus, bitters, garnish)
- Routes missing ingredients to the appropriate channel:
  - Adult beverage ingredients → BEV Channel (age-gated)
  - Mixers, citrus, garnish → Retail Channel (Walmart) or Home Channel grocery

The recipe + ingredient orchestration is the daily-utility surface. The allocation alerts are the **memorable moment**.

## 4. Three revenue layers

| Layer | Beverage-specific motion |
|---|---|
| Consumer subscription | $4.99 / mo Channel subscription |
| Action commerce | 5–10% of bottle value on Sazerac-routed orders + retailer-attribution fees + tasting-event booking fees |
| Outcome / risk-share | Limited; primary "outcome" is allocation-distribution efficiency, value to Sazerac |

## 5. Per-household envelope (for engaged subscribers)

| Source | Annual / engaged HH |
|---|---|
| Subscription ($4.99 × 12) | $60 |
| BEV-01 replenishment commerce (4–8 orders × $80 × 7%) | $25–50 |
| BEV-02 allocation alerts (1–3 successful drops × $250 × 5%) | $15–40 |
| BEV-03 cocktail concierge ingredient flow | $10–20 |
| BEV-04 tasting events + distillery tours | $30–80 |
| **Blended GP / engaged HH / yr** | **$140–250** |

Per-HH-ARPU is moderate; what matters is the **collector segment** (~3% of households drives 30%+ of revenue) — these subscribers contribute $400–1,000 / yr each.

## 6. Compliance considerations

Adult-beverage commerce is the **most regulated** of all the marketplace's verticals:

| Concern | Requirement |
|---|---|
| Age verification | Verified at every BEV order; ID-document tokenised in vault (handoff from existing `travel_document` infrastructure) |
| State-by-state shipping | DTC allowed in ~45 states for wine; ~13 states for spirits; 3-tier states require licensed retailer fulfillment |
| Dry counties | Geo-block at order-validation; no orders to dry zip codes |
| Federal labelling | TTB compliance for any cross-state delivery |
| Distillery direct-to-consumer | State-by-state legal review; some allow, some don't |
| Tied-house laws | Tasting-event referral fees must comply |

Compliance footprint is non-trivial. The pack delegates state-by-state legal review to specialist counsel; the Channel architecture supports the resulting rules but does not encode them as static logic — they live in a rules engine the Channel queries at every transaction.

## 7. Why other players can't credibly run this

| Alternative | Disqualifier |
|---|---|
| ReserveBar | Single-retailer aggregator; doesn't have allocation-feed primacy; doesn't have age-verification scale |
| Drizly (Uber) | Last-mile delivery only; allocation drops are inherently pickup-or-licensed-shipper |
| Total Wine direct | Single-retailer-only; can't recommend BevMo or Binny's |
| Mash & Grape | Whiskey-only marketplace; great brand but no Telco-grade compliance footprint |
| BTAC scalper marketplaces | Unauthorized; Sazerac actively combats these |

Only the Telco can offer Sazerac a **legitimate** distribution channel for allocation that's better than the current opaque "walk-in luck" model.
