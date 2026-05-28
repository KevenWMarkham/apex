# 07 — Marketplace Economics

> _Draft — synthesizes the per-Channel value models into a marketplace-level rollup. Numbers are envelopes for sizing; not committed forecasts._

## 1. Three revenue layers — marketplace rollup

| Layer | Telco GP / HH / mo (typical-engaged HH) | Notes |
|---|---|---|
| Consumer subscription (across all Channels) | $15–40 | Family bundle + 2–4 active vertical Channels |
| Action commerce (across all Channels) | $20–60 | Highest in travel + ground mobility + retail |
| Outcome / risk-share | $5–25 | Eldercare (HOM-03) + auto-insurance (MOB) + future Health Channel |
| **Blended GP / HH / mo** | **$40–125** | Steady-state at year 3+ |

## 2. Per-Channel contribution ranges (steady state)

| Channel | Attach rate | Blended ARPU / HH / mo | Marketplace contribution % |
|---|---|---|---|
| Home (HOM-01..08) | 40–55% | $20–40 | 35–40% |
| Travel | 25–40% | $10–25 | 15–20% |
| Retail (Walmart) | 30–45% | $8–18 | 12–15% |
| Mobility (Toyota) | 20–35% | $9–22 | 10–14% |
| CPG / Beverage (Sazerac) | 8–18% | $5–12 | 3–5% |
| Health (future) | 15–25% | $20–60 (PMPM-heavy) | 15–20% |
| Finance (future) | 20–30% | $8–18 | 7–10% |

## 3. Aggregate Telco-level upside

For a CSP with 20M home-internet subscribers, modelling at three cohort mixes:

| Mix | Steady-state Telco GP / yr (incremental) |
|---|---|
| Conservative (Home + Travel only) | $2.5B–4.5B |
| Base case (Home + Travel + Retail + Mobility) | $4.5B–7.5B |
| Full marketplace (incl. CPG, Health, Finance) | $7B–14B |

This is **incremental** to existing connectivity revenue. It does not require any new physical asset deployment beyond what the existing broadband / 5G build-out already provides.

## 4. CAC offset and churn protection

The marketplace's value to the Telco is not only the ARPU it generates directly — it is the **churn protection** it provides on the connectivity line:

| Cohort | Connectivity churn (annual) |
|---|---|
| No agentic subscription | 12–18% (industry baseline) |
| Home Channel only | 8–12% |
| Home + 1 vertical Channel | 5–8% |
| Home + 3+ Channels | 2–4% |

A 1% churn reduction on a 20M subscriber base is ~$180M / yr in saved CAC + retained connectivity revenue. The marketplace's churn-reduction effect alone is meaningful even before the direct ARPU is counted.

## 5. Cost stack (marketplace level)

| Cost line | Driver | Steady-state envelope |
|---|---|---|
| Inference (LLM tokens across all Channels) | Per agent run | $0.50–2.00 / HH / mo |
| Vault storage | Per HH per mo | $0.20–0.60 |
| Partner-API quota fees | Per booking / action | $0.30–1.50 |
| Customer-care load | Inverse-correlated with maturity | $1–4 / HH / mo |
| Channel-onboarding + maintenance | Amortized | $0.50–1.50 |
| Marketplace operations + compliance | Amortized | $0.20–0.70 |

Total marketplace COGS: **~$3–10 / HH / mo at engagement**, against $40–125 / HH / mo in blended GP. **Gross margin envelope: 75–92%.**

## 6. Comparison to the streaming bundle today

| Metric | Streaming bundle today | Agentic marketplace at steady state |
|---|---|---|
| Avg Telco take per included partner | $2–5 PMPM | $5–15 PMPM (incl. action commerce) |
| Channels per typical bundle | 4–7 | 4–7 |
| Telco GP / HH / mo from bundle | $10–25 | $40–125 |
| Marginal cost per added bundle subscriber | ~$0 | $3–10 |
| Customer-perceived value | High (entertainment) | Higher (everyday utility) |
| Churn protection on connectivity | Modest | Strong |

The agentic marketplace produces **3–5x the GP per HH** vs. the streaming bundle at steady state, with comparable gross margin profile and stronger churn-protection effect.

## 7. Phased P&L

| Year | Channels live | Households on marketplace | Blended GP / HH / mo | Annual GP |
|---|---|---|---|---|
| 1 | Home | 2M | $20–35 | ~$650M |
| 2 | Home + Travel | 5M | $30–55 | ~$2.5B |
| 3 | Home + Travel + Retail + Mobility | 10M | $40–80 | ~$7B |
| 4 | Above + CPG + initial Health | 14M | $55–105 | ~$13B |
| 5 | Full marketplace incl. Finance | 18M | $65–125 | ~$20B+ |

For context: this exceeds the entire current revenue of most Tier-1 streaming services. It is one of the **largest organic growth opportunities** available to a CSP this decade.

## 8. Sensitivity — what kills the model

| Risk | P&L impact |
|---|---|
| Channel attach rates 50% below envelope | -40% to GP; still ~$8B at year 5 |
| Action-commerce take rates 50% below envelope | -25% to GP |
| Lower bundle pricing power than modelled | -15–25% to subscription GP |
| Regulatory action on agentic commerce | High variance; could be zero or 3x cost |
| Big Tech competitive entry with subsidized pricing | -15% to attach; not -30% (trust asymmetry holds) |

Even at the **conservative joint envelope** (low attach × low take × low bundle pricing), the marketplace produces **$2–4B / yr GP at year 5** for a 20M-HH Telco. The downside is bounded; the upside is enormous.

> **Next step.** Build a full financial model with P10 / P50 / P90 per Channel and per cohort, validated against early bilateral conversations with anchor partners.
