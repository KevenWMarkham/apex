# 07 — Business Value Model

> _Draft — synthesized from the services catalog and partnership map. Refines the per-service unit economics in [`01-business-model.md`](./01-business-model.md) §4 and rolls them up against the Home Agentic baseline._

## 1. The three revenue layers, applied to Travel

| Layer | Travel-specific motion | Notes |
|---|---|---|
| Consumer subscription | Trip Add-On at $7.99 / mo; Travel Premium $14.99 / mo; Family Travel $19.99 / mo | Stacks on Home bundle; pricing positioned at ~20–30% of captured value |
| Action commerce | 1–15% of booking value depending on segment | Ground mobility highest (5–15%); flight lowest (1–3%) |
| Outcome / risk-share | Travel insurance + IROPS-economics with airlines | $20–80 per disruption avoided |

## 2. Per-service ARPU envelopes (illustrative)

Same shape as `../telco/07-business-value-model.md`. Attach rate = share of all Telco home-internet subscribers expected to be on the service at steady state.

| Service | Avg attach rate | Consumer ARPU | Action commerce | Outcome / risk-share | Blended ARPU |
|---|---|---|---|---|---|
| HOM-11 flight | 25–40% | $2–4 | $5–10 (avg 2 trips/qtr × 2% take on $400 fare) | $1–2 (IROPS share) | **$8–16** |
| HOM-12 hotel | 25–40% | $2–4 | $5–12 (avg 1 stay/qtr × 6% on $600) | — | **$7–16** |
| HOM-13 OTA | 35–50% | $1–3 | $1–3 | — | **$2–6** |
| HOM-14 STR | 10–20% | $1–3 | $2–5 | — | **$3–8** |
| HOM-15 ground | 30–45% | $1–3 | $2–6 | — | **$3–9** |
| HOM-16 experience | 15–30% | $1–2 | $1–3 | — | **$2–5** |
| HOM-10 orchestrator | included free | — | — | — | — |
| HOM-17 reunification | included with Trip Add-On | — | — | — | — |

## 3. Aggregate annual GP uplift per household

Layering travel on top of the Home Agentic baselines:

| Adoption cohort | Home GP / yr (baseline) | + Travel GP / yr | **Total GP / yr** |
|---|---|---|---|
| Light (no travel attach) | $60–100 | $0 | $60–100 |
| Typical-home + Trip Add-On | $250–420 | $150–300 | $400–720 |
| Family-bundle + Travel Premium | $720–1,200 | $400–700 | $1,120–1,900 |

For a CSP with 20M home-internet households assuming a `35% / 50% / 15%` cohort mix, the travel layer alone adds **~$2.1–3.6B / yr in incremental GP** on top of the Home Agentic baseline.

## 4. Cost-stack additions specific to travel

| Cost line | Driver | Per-HH-per-mo envelope |
|---|---|---|
| Partner-API fees (airlines, OTAs, STRs) | Per-search / per-booking quota | $0.10–0.50 |
| IROPS-recovery handle (HITL escalation) | Per disruption event | $1–5 amortized monthly |
| Travel-document tokenization + KMS | Per-traveler-per-mo | $0.05–0.15 |
| Currency / FX handling | International trips | $0.10–0.30 |

## 5. Open questions for the financial model

- **Airline rebook-attribution rates.** The actual $-per-rebook varies wildly by carrier and by route; needs partner-by-partner negotiation.
- **Hotel direct-vs-OTA mix economics.** Direct take rate is 2–3x OTA take rate, but direct coverage is ~70% of room-nights. The mix matters enormously to the P&L.
- **Travel insurance D-archetype methodology.** Outcome attribution is contested with insurers; needs a control-cohort design.
- **International expansion.** The pack's loyalty / payments / partner-API assumptions are US-centric. EU and APAC require separate models.

> **Next step.** Add a travel-specific tab to the financial model from [`../telco/07-business-value-model.md`](../telco/07-business-value-model.md) §6 with sensitivity on the three open questions above.
