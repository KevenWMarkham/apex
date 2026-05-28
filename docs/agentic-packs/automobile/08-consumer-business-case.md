# 08 — Consumer Business Case (Automobile Channel)

> _Draft — purchase orchestration as wedge; insurance savings as everyday hook; lifetime-relationship as moat._

## 1. Wedge — purchase orchestration

The vehicle-purchase experience is universally disliked. Industry research (CDK Global, Cox Automotive) consistently finds:

| Friction point | Average impact |
|---|---|
| Time spent researching | 12–25 hours |
| Time at dealership | 3–5 hours per visit × 2–3 visits |
| Stress level (self-reported, 1-10) | 7.8 |
| Trust in dealer process | 28% positive |
| Post-purchase regret (financing terms, vehicle choice) | 30–40% |

The Channel collapses purchase into a 3-day, 6-hour orchestrated flow. Per the wedge example in `01-business-model.md`:

- Research narrowed Saturday morning to Sunday evening (vault-assisted)
- Financing pre-approval Monday morning (no-impact credit pulls)
- Insurance quotes Monday morning (binding ready)
- Purchase Tuesday evening (45-min walk-out time)

**Captured value per purchase event:** 15–25 hours saved + reduced stress + better financing terms ($1,000–4,000 lifetime APR savings) + better insurance terms ($300–900/yr savings). Easily $3,000–8,000 in tangible value per purchase event.

Against an $11.99 / mo subscription ($144/yr), the purchase-event return is overwhelming.

## 2. Everyday hook — insurance + fueling savings

Between purchase events (steady-state ownership), the Channel earns its keep through:

| Service | Per-household-per-year value |
|---|---|
| AUT-04 insurance — annual re-shop signal + UBI optimization | $200–600 |
| AUT-06 fueling — price-by-station routing + payment-card optimization | $80–200 |
| AUT-05 aftermarket — cross-retailer parts price-comparison | $40–150 |
| AUT-07 fleet — IRS-grade mileage log (for the ~30% of HH with self-employed driver) | $500–2,000 in tax deductions |
| **Steady-state value** | **$320–950 / yr** (or $820–2,950 with fleet) |

Against $144/yr subscription, the steady-state value is also overwhelming.

## 3. Insurance + UBI mechanic

Progressive Snapshot offers up to 30% discount based on driving behaviour. The Channel:

- Reads household telematics from connected vehicles (HOM-07, MOB-01)
- Pre-computes projected UBI discount before binding
- Pre-shops with carriers that have UBI programs (Progressive, State Farm Drive Safe, Geico DriveEasy, Allstate Drivewise)
- Surfaces the best combined (base rate + UBI discount) offer

Customer typically saves $200–800 / yr on auto insurance vs unmanaged-renewal baseline. The Channel takes a share of the savings; customer keeps the rest.

## 4. Adoption funnel

| Stage | Envelope |
|---|---|
| Home Channel subscribers | 100% |
| Owns at least one vehicle | 92% |
| Aware of Automobile Channel | 60–75% |
| Triggered to trial (often via insurance-renewal signal) | 18–28% |
| Active at 90 days | 78–85% |
| Cross-attach to mobility-auto/ Channel (for Toyota households) | 55–70% |

## 5. The cross-Channel cross-sell

- Home subscribers → Travel + Retail + Mobility/Auto + Automobile = household-level orchestrator across all four
- Automobile-only subscribers → strong upsell to Home (because vehicle is one of household's biggest economic items, and HOM-07/HOM-02 home-charging coordination is a natural extension)
- Insurance-driven Automobile attach (AUT-04 anchor) → strong upsell to Home Family Bundle for HOM-05 security insurance discount coordination

The Automobile Channel sits at a particularly rich cross-sell intersection.

## 6. What kills the consumer case

- **One bad purchase experience.** A vehicle the customer regrets, or financing terms the customer feels misled by — kills trust irreparably. AUT-02 + AUT-03 require **extraordinarily** careful HITL design.
- **Insurance binding error.** Wrong coverage, wrong vehicle ID, wrong dates — exposes customer to uninsured-driver liability. Compliance footprint is non-negotiable.
- **Credit-pull surprise.** Customer expected soft pulls; got hard pulls; credit score drops. Consent UX must be airtight.
- **Dealer-side coordination breakdown.** Customer arrives at AutoNation; pre-negotiated price not honored. Channel must terminate partnership relationships with non-compliant dealers.
