# 08 — Consumer Business Case

> _Draft — the case made to a household, not to a Telco CFO. Frames the willingness-to-pay arithmetic and the trust-asymmetry argument that makes the Telco offer rationally preferable to a Big Tech equivalent._

## 1. Why the household says yes

Consumers do not buy "agentic platforms". They buy three things they recognize:

1. **Time back** — the grocery trip that didn't happen, the bill that got lower without them thinking about it, the maintenance call that didn't escalate to a repair.
2. **Peace of mind** — Mom is OK, the leak didn't flood the basement, the EV is charged before tomorrow's commute.
3. **Money saved** — verifiable, on the same bill they already pay.

The pack monetizes by **packaging all three into the existing Telco invoice**, removing the cognitive overhead of yet another monthly subscription, yet another app, yet another login.

## 2. The willingness-to-pay (WTP) anchor — grocery

The grocery wedge is the most universally usable proof point. Replenishment-driven grocery agentic orchestration creates:

| Saving | Per household per week |
|---|---|
| Time on planning + list-making | 20–40 minutes |
| Time on the shopping trip itself (when consolidated to delivery) | 30–60 minutes |
| Avoided "ran-out-of-X mid-recipe" trips | 0.5–1.5 trips |
| Reduced food waste (expiry-aware reordering) | $5–12 |

A household that values its own time at even $15 / hr is willing to pay **$30–60 / mo** in principle. The actual bundled price of $9.99 (Essential) → $19.99 (Family) lives well inside the comfort envelope.

## 3. The arithmetic across services

A "Family" subscriber at $19.99 / mo who actively uses Grocery + Energy + Maintenance + Security typically captures, by service:

| Service | Tangible monthly value to the household |
|---|---|
| HOM-01 grocery | $30–60 (time) + $5–12 (waste) |
| HOM-02 energy | $8–18 (utility bill reduction) |
| HOM-04 maintenance | $5–15 amortized (avoided repair escalation) + warranty optimization |
| HOM-05 security | $3–8 insurance-premium discount passed through |
| **Aggregate** | **$50–110 / mo of recognizable value vs. $19.99 / mo paid** |

The pack's pricing is deliberately positioned at **~20–30% of captured household value** — high enough to fund the platform, low enough that the value-per-dollar story is overwhelming and the cancel motion is irrational.

## 4. The trust-asymmetry argument

Standalone IoT subscriptions churn at 30%+ per year because customers cannot answer two questions:

1. *Who actually sees this data?*
2. *What happens if the vendor's business changes?*

The Telco's structural answer:

| Question | The Telco answer |
|---|---|
| Who sees the data? | Your data lives in your vault. You hold the encryption key. The Telco operates the vault but cannot read it. |
| What happens if the Telco changes the business? | Your vault is portable by construction. You can export and switch the orchestrator while keeping all of your history. See [`09-portability-open-home.md`](./09-portability-open-home.md). |
| Why isn't this a Big Tech monopoly play? | Big Tech monetizes by reading your data. The Telco's business model is the subscription on your bill and the partnership rev-share on transactions. The incentives don't pull in the same direction. |

This argument is **stronger when delivered by a regulated utility** than by any other player. Telcos already operate under privacy regulation that Big Tech does not. The pack converts a regulatory liability into a brand asset.

## 5. The eldercare-as-loss-leader argument

The single most powerful consumer-acquisition mechanic in the pack is:

> _"`TMT-TEL-HOM-03` is free for your aging parent because their Medicare Advantage plan pays for it. The platform that monitors Mom is the same platform that orders your groceries."_

A consumer who would never sign up for a $30 / mo IoT subscription will sign up for a free service for their parent — and once the family is on the platform, the cross-attach to Family-bundle services is the **highest-conversion motion the pack offers**.

This is also where the Telco wins **against the cable / broadband incumbents** in the same market. Without the eldercare wedge, the Telco's offer is "$20 for some smart-home agents." With it, the offer is "your parent's safety net, paid for by Medicare, and the rest of your household's automation for the cost of a Netflix subscription."

## 6. Adoption funnel — illustrative

| Stage | Conversion rate envelope | Notes |
|---|---|---|
| Eligible Telco home-internet subscribers | 100% (denominator) | — |
| Aware of Home Agentic offering | 60–80% | Bill-insert + in-app prompts + retail-channel pull |
| Triggered into onboarding flow | 25–40% | Eldercare wedge is the dominant trigger |
| Active subscriber at 90 days | 70–85% of triggered | Stickiness driven by orchestrator value, not single-agent value |
| Cross-attached to a second sub-agent | 50–65% | Bundle pricing favours this strongly |
| Outcome-share enrolled (HOM-03 / HOM-06) | 10–18% | Constrained by MA / payer eligibility, not by demand |

Numbers are envelopes for sizing the conversation, not committed forecasts. Even at the **low end** they materially exceed standalone-IoT industry benchmarks because the Telco starts from an active billing relationship, not from cold acquisition.

## 7. What kills the consumer case if we're not careful

- **One bad voice / chat UX** — if the orchestrator interaction feels worse than the existing Alexa / Google Assistant, no amount of data sophistication recovers it. Voice UX has to be **at parity day one**.
- **One privacy headline** — a "Telco read my fridge" headline kills the pack. The vault-first design must be **auditable by the customer**, not just claimed.
- **One bundle that fails** — entertainment concierge (HOM-08) is the lowest-stakes service; if it doesn't work, customers extrapolate. Either build it right or de-scope it from the launch.
- **A pricing structure that becomes opaque on the bill** — Telco bills already get criticized for opacity. Sub-agent line items must be **explicitly readable and individually cancellable**, or churn will follow.
