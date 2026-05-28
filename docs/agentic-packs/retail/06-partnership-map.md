# 06 — Strategic Partnership Map (Retail Channel)

> Walmart-anchored partnership map using the canonical five archetypes. Bench partners cover the routing diversity the orchestrator needs.

## 1. Walmart — the anchor

**Why Walmart and not Amazon, Target, or Costco?**

- **Scale:** ~10,500 stores, ~90% population coverage within 10 miles
- **Vertical breadth:** Grocery + GM + Pharmacy + Health + Auto Care + Tax Services + Money Services — one anchor covers the most surface
- **Membership infrastructure already in place:** Walmart+ (~25M US members), Sam's Club, paid acquisition machinery
- **Retail-media (Walmart Connect) revenue model already aligns with sponsored-placement disclosure**
- **B2B muscle:** Walmart already partners aggressively (with Microsoft, Adobe, Salesforce, etc.) — culturally prepared to be a Channel partner

| Walmart-side benefit | Telco-side benefit |
|---|---|
| Default-routing in the orchestrator's retail logic | $7.99 / mo Channel subscription per HH |
| Lower-CAC Walmart+ enrolment via Telco bill bundling | Per-order 3–5% take rate |
| Verified-intent baskets with cross-channel context | Walmart Health PMPM share |
| Walmart Connect surface inside the orchestrator (with disclosure) | TLE per-service-call commerce |
| Pharmacy-refill volume from the eldercare wedge | Net new revenue layer |

**Archetype mix:** B (Action-Out) + C (Distribution / Bundle) + limited A (Data-In)

## 2. Bench partners

### Target

| Aspect | Detail |
|---|---|
| Archetype | B + C |
| Why bench: | Walmart's most direct competitor at scale; can't be anchor, but customers shop both; Target Circle loyalty + Drive Up + Same Day fulfillment are differentiated |
| Take rate | 3–5% of basket |
| Strategic note | Target's higher-AOV / higher-margin general merchandise complements Walmart's broader-but-thinner mix |

### Costco

| Aspect | Detail |
|---|---|
| Archetype | C (membership distribution) + B (action commerce on Costco delivery) |
| Why bench: | Membership wholesale model; complements Walmart on bulk staples; passionate customer base |
| Take rate | Limited per-order (Costco's margins are thin); higher value in membership-attribution |
| Strategic note | Costco Gold Star + Executive tiers are the membership-optimization anchor for RTL-04 |

### Sam's Club

| Aspect | Detail |
|---|---|
| Archetype | C (Walmart-owned) + B |
| Why bench: | Walmart-owned wholesale club; natural extension of the Walmart anchor relationship |
| Take rate | Inherits Walmart partnership terms |

### Best Buy

| Aspect | Detail |
|---|---|
| Archetype | B + D (Geek Squad protection plan as D-archetype outcome share) |
| Why bench: | Electronics-only specialty retailer; complements general merchandise with high-AOV electronics |
| Take rate | 3–5% on consumer electronics; protection-plan-attach margin sharing |

### Home Depot

| Aspect | Detail |
|---|---|
| Archetype | B + A (Pro account telemetry → home maintenance signal back to HOM-04) |
| Why bench: | Home improvement specialty; very high errand-chain inclusion (light fixtures, paint, hardware, lumber) |
| Take rate | 3–6% on consumer purchases; higher on contractor / Pro tier |

### Lowes

| Aspect | Detail |
|---|---|
| Archetype | B |
| Why bench: | Home Depot's direct counterpart; some markets favour one over the other |

### Kroger (handoff to HOM-01)

| Aspect | Detail |
|---|---|
| Archetype | Already in Home Channel HOM-01 grocery |
| Why bench: | Grocery overlaps; Walmart's grocery share competes; the orchestrator routes by household preference and proximity |

## 3. Pharmacy partnerships (RTL-02)

| Partner | Archetype | Notes |
|---|---|---|
| **Walmart Pharmacy / Walmart Health** | Anchor — B + D | Pharmacy refill volume; Walmart Health PMPM for chronic conditions |
| CVS | Bench — B (handoff to Health Channel) | Caremark + MinuteClinic create scope conflict with future Health Channel; deferred |
| Walgreens | Bench — B (handoff to Health Channel) | Same |
| Hero (med dispenser) | A | Adherence telemetry; already in HOM-03 eldercare |
| MedMinder | A | Same |

## 4. Auto-care partnerships (RTL-03)

| Partner | Archetype | Notes |
|---|---|---|
| **Walmart Auto Care (TLE)** | Anchor — B | National coverage at supercenter network |
| Jiffy Lube | Bench — B | Higher-density coverage in some markets |
| Firestone | Bench — B | Tire + service combined |
| Pep Boys | Bench — B | |
| Dealer service (Toyota, Ford, GM) | Handoff to Mobility Channel | OEM-owned service network; Mobility Channel sub-agents own these |

## 5. Membership partnerships (RTL-04)

| Partner | Archetype | Strategic note |
|---|---|---|
| Walmart+ | Anchor — C | Walmart-owned; co-bundled with Telco bill |
| Costco | Bench — C | Highest payback ratio for typical households |
| Sam's Club | Bench — C | Walmart-owned bench |
| Amazon Prime | Bench — C | Competes with Walmart+; included for portfolio completeness |

## 6. Cross-Channel coordination

The Retail Channel coordinates with other Channels via the orchestrator:

| Adjacent Channel | Coordination shape |
|---|---|
| Home (HOM-01 grocery) | Walmart grocery overlaps; orchestrator routes by household preference + price |
| Home (HOM-03 eldercare) | Pharmacy refill due → eldercare-aware notification |
| Home (HOM-04 maintenance) | Home Depot purchase logged → maintenance project context |
| Travel | Trip-mode pauses non-urgent retail orchestration |
| Mobility (Toyota) | TLE / dealer-service routing decided by orchestrator based on warranty + cost |
| CPG / Beverage | Adult-beverage purchases routed via BEV Channel for age-gating |

## 7. Phasing

| Phase | Quarter | Partner additions |
|---|---|---|
| Phase 0 | Q1–Q2 (Year 2) | Walmart anchor MCP integration; Walmart+ co-bundle |
| Phase 1 | Q3 (Year 2) | Target, Costco onboarded; multi-retailer routing live |
| Phase 2 | Q4 (Year 2) | Best Buy, Home Depot, Lowes onboarded |
| Phase 3 | Year 3 | Long-tail (CVS, Walgreens) when Health Channel launches |
