# 07 — Business Value Model

> _Draft — synthesized from the partnership map and services catalog. Numbers are **illustrative envelopes** for sizing the conversation, not committed forecasts. Where a number is sourceable to an established benchmark it is footnoted; everything else should be challenged before quotation._

## 1. The three revenue layers, restated

| Layer | Payer | Pricing motion | Telco margin profile |
|---|---|---|---|
| **Consumer subscription** | Household, on the Telco bill | Bundled or à-la-carte sub-agents | 70–85% gross margin (mostly inference + integration cost) |
| **Action commerce** | Action partner (grocer, utility, OEM, service network) | % of basket / per-event fee | 90%+ gross margin (no inventory risk) |
| **Outcome / risk-share** | Sponsor (MA plan, P&C carrier, employer) | PMPM, per-incident, shared savings | 60–80% gross margin (delivery cost is real — clinician routing, escalation handling) |

The consumer subscription is the **wedge** — it secures the household and the consent grant. The action and outcome layers carry the actual P&L.

## 2. Per-service unit economics — illustrative

ARPU is per active subscriber per month. "Avg attach rate" is the share of all Telco home-internet subscribers expected to be on the service in steady state (year 3+). These are illustrative envelopes — not commitments.

| Service | Avg attach rate | Consumer ARPU | Action commerce | Outcome / risk-share | Blended ARPU |
|---|---|---|---|---|---|
| HOM-01 grocery | 35–45% | $5–7 | $4–8 / mo (5% on $100/wk basket) | — | **$10–15** |
| HOM-02 energy | 30–40% | $5–7 | $2–4 / mo (DR capacity share) | — | **$8–12** |
| HOM-03 eldercare | 5–10% | $0 (sponsored) | — | $50–80 PMPM | **$50–80** |
| HOM-04 maintenance | 25–35% | $4–6 | $2–4 / mo (service-call dispatch) | $1–2 (warranty co-sell) | **$8–13** |
| HOM-05 security | 15–25% | $5–9 | — | $2–4 (insurance discount share) | **$8–14** |
| HOM-06 wellness | 10–20% | $5–8 | $1–2 (telehealth escalation) | $10–25 PMPM (payer) | **$15–35** |
| HOM-07 vehicle | 20–30% | $4–6 | $1–3 (service / charging) | $1–2 (UBI share) | **$6–11** |
| HOM-08 entertainment | 40–55% | $3–5 | $1–3 (distribution rev-share) | — | **$4–8** |

## 3. Aggregate household uplift

Modelling a representative household at the **target adoption mix** described in [`01-business-model.md`](./01-business-model.md):

- 2.5 sub-agents on average (mix of attach-rate-weighted services above)
- At least one service routing meaningful action commerce
- One household member eligible for an outcome-share program (eldercare or wellness)

| Adoption cohort | Steady-state blended GP / mo | Annual GP per HH |
|---|---|---|
| **Light** (Essential bundle, no commerce flow) | $5–8 | $60–100 |
| **Typical** (Family bundle + grocery commerce) | $20–35 | $250–420 |
| **Outcome-share-attached** (Family bundle + eldercare PMPM) | $60–100 | $720–1,200 |

At Telco scale, the blend matters more than the headline number. A CSP with **20M home-internet households** that achieves a `40% light / 50% typical / 10% outcome-share` mix produces:

```
20M × [0.40·$80 + 0.50·$335 + 0.10·$960] = $7.9B / yr in incremental GP
```

This is **layered on top** of existing connectivity revenue. It does not require a single new physical asset — the router is already deployed.

## 4. Cost stack

| Cost line | Driver | Per-HH-per-mo envelope |
|---|---|---|
| Inference (LLM tokens) | Per agent-run, per action proposed | $0.20–0.80 |
| Vault storage + egress | Per-HH cloud storage of telemetry + embeddings | $0.10–0.40 |
| Integration / MCP partner fees | OAuth maintenance, partner API quotas | $0.05–0.30 |
| HITL / escalation handling | Outcome-share services only | $5–15 (loaded with clinician routing) |
| Customer-care load | Inversely correlated with maturity | $0.50–2.00 |

Light cohort costs sit around $1–2 / HH / mo; outcome-attached cohorts cost $10–20 / HH / mo. Both are **well below** the GP envelopes above.

## 5. The defensibility argument in P&L terms

The platform survives the obvious threats by structural choice, not by hope:

| Threat | Structural defence | P&L consequence |
|---|---|---|
| Big Tech bundles the same agents | Customer holds the vault key; data is portable by construction | Big Tech can't replicate the trust narrative without breaking their ad model |
| One partner (e.g., Kroger) blocks the integration | Multi-partner take-rate; orchestrator routes to the next best fulfilment | Partner concentration risk is bounded by archetype substitution |
| MA payer renegotiates the outcome rate | Multi-payer enrolment; non-payer-sponsored consumer tier still revenue-positive | Down-side floor = consumer subscription only |
| Regulatory move on consumer-data agents | Regulator already has a deep relationship with the Telco; the vault-first design is what they would have asked for | The regulator is a tailwind, not a headwind |

## 6. What still needs to be modelled

- **CAC offset.** Each new sub-agent reduces broadband / 5G churn — the platform's first job is to **reduce ARPU loss on the connectivity line**, not just add new ARPU.
- **Tenure curve.** Outcome-share programs (HOM-03, HOM-06) compound monthly; they should be modelled as a CLV not an ARPU.
- **Geographic mix.** US Medicare Advantage rates do not transfer to EU markets, where the eldercare wedge requires a different sponsor (national health system, private gap insurance).
- **Hyperscaler economics.** Vault storage + inference are sensitive to hyperscaler pricing trajectory; reserve capacity commitments shift the cost stack meaningfully.

> **Next step.** Build a one-page financial model with per-service P50 / P10 / P90 envelopes and run sensitivity against the three variables above (attach rate, partner take rate, outcome PMPM). The current numbers are envelope, not forecast.
