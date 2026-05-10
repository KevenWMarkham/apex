# apex-proml

APEX **PROML** (Pricing & Revenue Markup Language) canonical entities for the RC Practice. Sprint 30.4.

Entities: `Pricing` · `DiscountRule`.

Read by RC-E2E-03's Pricing Agent (The Pricer) and the Markdown Agent. PROML
sits next to MERML — MERML carries the price *facts* (list, promo, markdown
events), PROML carries the *rules and policies* that govern what the agents
are allowed to recommend (floors, MAP, discount ladders).

Per ADR-005 sensitivity model, most PROML fields carry `TRADE_SECRET`
classification — the discount-rule cap percentages and price floors are the
RC team's most differentiating analytical assets for a tenant.
