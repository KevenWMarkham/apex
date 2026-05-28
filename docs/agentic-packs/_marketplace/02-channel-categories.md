# 02 — Channel Categories

> The seven channel categories that anchor the marketplace at launch. Each is **structurally orthogonal** to the others — no two categories compete for the same household intent. Each can scale independently. Each has clear partner anchors and clear consumer wedge events.

## Category 1 — Home (`TMT-TEL-HOM-01..08`, `HOM-99`)

**What the channel does:** Orchestrates in-home services — grocery, energy, eldercare, maintenance, security, wellness, vehicle, entertainment.
**Pack:** [`../telco/`](../telco/)
**Anchor partners:** Samsung Family Hub, LG ThinQ, Nest, Ring, Dexcom, Whirlpool, ChargePoint
**Wedge event:** Automated grocery replenishment driven by smart fridge + pantry signals
**Avg attach rate (steady state):** 35–60% of home-internet subscribers
**Blended ARPU:** $20–40 PMPM (incl. action commerce)

## Category 2 — Travel & Hospitality (`TMT-TEL-HOM-10..17`)

**What the channel does:** Trip-mode orchestration — flight, hotel, OTA, vacation rental, ground mobility, local experience, return reunification.
**Pack:** [`../travel-hospitality/`](../travel-hospitality/)
**Anchor partners:** American Airlines (AAdvantage), Marriott (Bonvoy), Expedia, Airbnb, Hertz, Uber, OpenTable, Viator
**Wedge event:** IROPS flight rebook with cross-carrier optimization
**Avg attach rate:** 25–50%
**Blended ARPU:** $10–25 PMPM

## Category 3 — Retail (`TMT-TEL-RTL-01..04`)

**What the channel does:** Cross-store everyday retail orchestration beyond grocery — general merchandise, pharmacy, optical, auto care, membership tier optimization.
**Pack:** [`../retail/`](../retail/)
**Anchor partner:** Walmart (with bench: Target, Costco, Kroger, Best Buy, Home Depot)
**Wedge event:** Pharmacy-pickup-while-running-errands coordination (Walmart Health prescription ready + Costco grocery + Home Depot return all chained)
**Avg attach rate:** 30–45%
**Blended ARPU:** $8–18 PMPM

## Category 4 — Mobility / Auto (`TMT-TEL-MOB-01..04`)

**What the channel does:** Multi-OEM connected-vehicle orchestration — telematics, dealer-network service, next-vehicle decisioning, OEM financing & insurance.
**Pack:** [`../mobility-auto/`](../mobility-auto/)
**Anchor partner:** Toyota (Toyota Connected Services + Toyota Financial + Toyota Insurance)
**Bench:** Ford (Sync 4 / Lincoln Way), GM (OnStar / Ultium), Tesla, Honda, Hyundai
**Wedge event:** Recall + service-bulletin reconciliation across the household's vehicle fleet
**Avg attach rate:** 20–35%
**Blended ARPU:** $9–22 PMPM

## Category 5 — CPG / Adult Beverage (`TMT-TEL-BEV-01..04`)

**What the channel does:** Adult-beverage replenishment with age-gated commerce, allocation alerts (Buffalo Trace, Pappy Van Winkle, allocated single malts), cocktail recipes that compose ingredient orchestration, tasting events / distillery tour bookings.
**Pack:** [`../cpg-adult-beverage/`](../cpg-adult-beverage/)
**Anchor partner:** Sazerac (Buffalo Trace, Pappy Van Winkle, Eagle Rare, Blanton's, Sazerac Rye)
**Bench:** Diageo, Pernod Ricard, Brown-Forman, Constellation Brands
**Wedge event:** Buffalo Trace allocation drop alert with reserved-bottle hold at the customer's preferred retailer
**Avg attach rate:** 8–18%
**Blended ARPU:** $5–12 PMPM (lower attach, higher ARPU on engaged subscribers)

## Category 6 — Health & Pharmacy (future)

**What the channel will do:** Prescription orchestration, telehealth scheduling, chronic-condition program enrolment, pharmacy reconciliation, lab-results management.
**Pack:** _Not yet authored_
**Anchor partner candidates:** CVS (Caremark + MinuteClinic), Walgreens, UnitedHealth Optum, Walmart Health
**Note:** Has overlap with `HOM-03 eldercare` and `HOM-06 wellness`; the Channel will need a clear scope boundary.

## Category 7 — Finance & Insurance (future)

**What the channel will do:** Multi-bank account orchestration, bill negotiation, insurance shop / renew, sub-account budgeting per household member.
**Pack:** _Not yet authored_
**Anchor partner candidates:** Chase, Bank of America, Amex (cards + travel), Capital One, State Farm, Progressive, Allstate, Plaid (rails)
**Note:** PCI / GLBA compliance footprint significantly extends the trust framework; this category should ship after the other five are stable.

## Channel-category design principles

1. **Orthogonality.** No two categories should compete for the same intent. Grocery is Home; food-delivery-during-travel is Travel; pantry-restock-on-return is Home; reserved-bottle-pickup is CPG. The orchestrator's job becomes trivial when the categories are clean.
2. **Anchor-partner-led.** Every category launches with one flagship partner anchor — the named partner (Samsung, AA, Walmart, Toyota, Sazerac) — and a bench that fills in over Phase 3+ of rollout.
3. **Wedge-event-led.** Every category has one **memorable consumer moment** that justifies the subscription at first-use. The marketplace cannot launch a category without an articulated wedge.
4. **Independent attach economics.** Every category's adoption thesis stands alone. We don't model cross-category attach as a precondition; we model it as upside.
5. **Bounded compliance footprint.** Categories with deep compliance baggage (Health, Finance) should not be in the launch wave. Categories with light footprint (Home, Travel, Retail, Mobility, CPG) should lead.

## Adding a new category

The marketplace welcomes new categories. To add one:

1. Identify the **anchor partner** willing to be flagship
2. Identify the **wedge event** that justifies subscription at first use
3. Author a 10-section pack following the [`_template/`](../_template/) structure
4. Reserve a service-code family (`TMT-TEL-<XXX>-*` where `<XXX>` is the 3-letter category code)
5. Submit the pack for marketplace registration via [`05-channel-catalog.md`](./05-channel-catalog.md)
6. Have the anchor partner implement `apex.tmt.mcp.partner.v1`

No core platform change is required. The marketplace is **additive by construction**.
