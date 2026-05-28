# 01 — Business Model

> The automobile ownership lifecycle — research, purchase, financing, insurance, ownership, aftermarket, charging, resale — is the single most fragmented high-value journey in the consumer's life. The Telco's Automobile Channel collapses 15+ disconnected experiences into one orchestrated flow on the existing Telco bill. AutoNation, Cox Automotive, and Progressive anchor; OEM-direct, used-car retailers, banks, and aftermarket parts brands fill the bench.

## 1. The fragmentation problem

A typical US household buying a vehicle today touches:

| Lifecycle stage | Apps / sites the customer uses today |
|---|---|
| Research | KBB, Edmunds, Autotrader, CarGurus, TrueCar, OEM-direct (Ford, GM, Toyota), Reddit r/cars |
| Compare | Side-by-side spreadsheets, screenshot collages, Consumer Reports |
| Inventory search | Dealer-direct sites, Autotrader, CarGurus, CarMax, Carvana |
| Trade-in valuation | KBB Instant Cash Offer, Carvana, CarMax, AutoNation, Vroom (defunct) |
| Pre-approved financing | Capital One Auto Navigator, Bank of America, Ally, dealer-direct |
| Dealer negotiation | In-person, email chains, possibly via TrueCar / CarsDirect |
| Insurance | Progressive site, State Farm site, Geico site, Allstate site, USAA, comparison sites (Compare.com, The Zebra) |
| Title / registration | State DMV site, dealer-handled, third-party services |
| Aftermarket parts | AutoZone, Advance Auto, O'Reilly, NAPA, RockAuto, Amazon, dealer parts |
| Charging / fueling | ChargePoint app, EVgo app, Electrify America app, Tesla app, Shell app, GasBuddy |
| Service (already in mobility-auto + retail) | OEM dealer apps, Walmart TLE, Jiffy Lube, independent shops |
| Resale | Carvana, CarMax, Vroom, Peddle, Craigslist, Facebook Marketplace |

**~15 apps for one journey.** Each app has its own login, its own data silo, its own incentives. The customer's mental map across them is held together by browser tabs and screenshots.

The Channel collapses this into a single household-vault-aware orchestrator. The vault holds the household's vehicle preferences, financial profile, insurance history, ownership records, and trade-in candidates; sub-agents talk to all the partners on behalf of the customer.

## 2. The wedge — Saturday-research-to-Tuesday-drive-home

```
Saturday 9 AM
  Household issues intent: "I think we need to replace the 2017 Highlander"

Sunday 11 AM
  AUT-01 Discovery agent surfaces:
   - 3 model candidates matching family size + budget + EV-preference
   - Side-by-side comparison via KBB + Edmunds + Consumer Reports
   - Trade-in offer on Highlander from CarMax / Carvana / AutoNation

Sunday evening
  Customer narrows to 2025 Toyota Grand Highlander HEV + 2025 Kia Telluride

Monday 9 AM
  AUT-03 Financing agent runs pre-approvals across:
   - Capital One Auto Navigator (rate quote, no-impact pull)
   - Ally Auto
   - USAA (customer is eligible)
   - Customer's credit union
  Returns 4 pre-approvals with rate sheets

Monday 11 AM
  AUT-04 Insurance agent runs quotes across:
   - Progressive (incl. Snapshot UBI discount based on household telematics)
   - State Farm
   - Geico
   - USAA
  Returns 4 quotes; presents tradeoffs

Monday 2 PM
  AUT-02 Purchase agent:
   - Identifies 3 AutoNation locations with target trim in stock
   - Initiates dealer-direct negotiation with target out-the-door price
   - Confirms trade-in value with chosen dealer
   - Reserves vehicle pending appointment

Tuesday 5 PM
  Customer arrives at AutoNation:
   - Vehicle waiting, pre-negotiated
   - Pre-approved financing already on file at dealer
   - Insurance binding ready to fire on signature
   - Trade-in valuation already confirmed
   - DMV paperwork pre-filled
  Walk-out time: ~45 min vs typical 3-5 hours.

Tuesday 7 PM
  Customer drives home.
  AUT-04 binds insurance via Progressive at signature.
  AUT-03 financing executes; first payment auto-scheduled.
  HOM-07 (vehicle, Home Channel) detects new vehicle, sets up telematics.
  MOB-01 (Toyota Connected) registers VIN and starts service-reminder lifecycle.
  AUT-06 charging-fueling agent surfaces home-charging-station options.
```

Total customer effort: ~6 hours of attention spread across 3 days, vs typical 20–40 hours and 6+ weeks. The Channel delivers a **10x improvement in the consumer's most disliked major purchase experience**.

## 3. Three revenue layers — applied to Automobile

| Layer | Automobile-specific motion |
|---|---|
| Consumer subscription | $11.99 / mo Channel subscription on Telco bill |
| Action commerce | 0.5–2% of vehicle purchase price; 3–8% of financing origination fees; 8–15% of insurance commissions; 5–10% on aftermarket parts |
| Outcome / risk-share | UBI insurance premium-reduction share; insurance loss-ratio improvement; financing default-rate improvement |

## 4. Per-household economic envelope

For a household that uses the Channel for one full purchase lifecycle + 12 months of ownership:

| Source | Per-purchase event | Annual recurring |
|---|---|---|
| AUT-01 Discovery / research | — | $5–15 (commerce from KBB / Autotrader referrals) |
| AUT-02 Purchase | $200–500 attribution (1% on $28K avg used / $48K new) | — |
| AUT-03 Financing | $150–400 financing-origination share | $5–15 (servicing fee share) |
| AUT-04 Insurance | $250–500 binding commission | $150–350 (12% of $1,400–2,200 annual premium × Telco share) |
| AUT-05 Aftermarket | — | $30–80 (parts + accessories action commerce) |
| AUT-06 Charging / fueling | — | $50–120 (route-cost-optimization fee share) |
| AUT-07 Fleet (when applicable) | — | $40–100 |
| AUT-08 Resale | $100–300 per resale event | — |
| Subscription ($11.99 × 12) | — | $144 |
| **GP / HH / yr (no purchase)** | | **$425–825** |
| **GP / HH / purchase event year** | | **$1,125–2,100** |

Vehicle purchases happen every 5–7 years per vehicle, every 3–4 years per household (1.8 vehicles, staggered). Steady-state blend per household per year: **$525–950**.

## 5. Telco-level upside

20M home-internet households × 15–25% attach rate × $525–950 blended = **$1.5–4.8B / yr in Telco GP**.

This is the third-highest Channel GP envelope in the marketplace after Home and Travel, despite being late in the rollout phase. The vehicle purchase moment is structurally that valuable.

## 6. Why the multi-anchor model

Unlike single-anchor Channels (Walmart-anchored Retail, Toyota-anchored Mobility), the Automobile Channel anchors on **three brands across the lifecycle** because no single player covers all of it:

| Anchor | Lifecycle stages owned |
|---|---|
| **AutoNation** | AUT-02 purchase, AUT-05 aftermarket (parts via dealer parts dept), AUT-08 resale (trade-in side) |
| **Cox Automotive** (KBB / Autotrader / Manheim / vAuto / Dealer.com) | AUT-01 discovery, AUT-08 valuation, dealer-side ops infrastructure |
| **Progressive** | AUT-04 insurance, Snapshot UBI, telematics-based outcome share |

The multi-anchor model parallels the Travel Channel (AA + Marriott + Expedia + Airbnb) — each anchor owns a slice; the orchestrator stitches them together.

## 7. What the Channel does not try to be

- **Not a new-car shopping marketplace** — TrueCar, KBB, Autotrader already do this; the Channel uses them as data + commerce partners
- **Not a dealer-direct app** — AutoNation, Lithia, Penske each have their own apps for ongoing service; the Channel covers cross-dealer / cross-OEM orchestration
- **Not a CarMax / Carvana replacement** — used-car retail is its own model; the Channel routes intent to them when they're the right answer
- **Not an insurance carrier** — Progressive remains Progressive; the Channel is the orchestration + UBI-mediation layer
- **Not a connected-vehicle ops platform** — that's `mobility-auto/` (Toyota); the Automobile Channel covers commerce + lifecycle
