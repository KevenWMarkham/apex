# PARS — The Retailer's Counter-Move Against Amazon (v0.2)

**Private Auto-Replenishment Service · A Joint Retailer + Telco + Deloitte Offensive**

**Status**: Draft for DMTSP review — sharpened competitive positioning
**Owner**: Keven Markham, VP — Deloitte's Microsoft Practice
**Date**: 2026-05-23
**Version history**:
- **v0.2** (2026-05-23): Re-anchored as anti-Amazon retailer counter-strategy. Adds market-sizing, retailer-by-retailer + telco-by-telco playbooks, the counter-flywheel, and the defensible moat.
- v0.1 (2026-05-23): Initial consumption-based auto-buy offering.

---

## 0. The competitive crisis — what Amazon is doing to your client

> Every quarter that passes, Amazon takes a little more of your retail client's basket. They are not winning on price. They are not winning on selection. **They are winning on the consumption layer** — the agentic backend that watches the household, predicts depletion, and replenishes before the customer thinks about it. PARS is how a Kroger, Costco, Target, Walmart, or Wegmans takes that layer back.

### The Amazon dominance flywheel (what's beating your client today)

```
   ┌────────────────────────────────────────────────────────────────┐
   │                                                                  │
   │     ┌─────────────┐                  ┌──────────────────┐       │
   │     │   PRIME      │ ────────────►   │  ECHO + ALEXA    │       │
   │     │  200M+       │                  │  70M+ households │       │
   │     │  households  │  $14.99/mo bundle│  voice surface   │       │
   │     └──────┬──────┘                  └─────────┬────────┘       │
   │            │                                    │                │
   │            │  Free delivery on staples          │  Wake-word     │
   │            ▼                                    ▼  routes to     │
   │     ┌──────────────────────────────────┐        amazon.com       │
   │     │  SUBSCRIBE & SAVE                 │                         │
   │     │  Auto-replenish (38% of frequent  │                         │
   │     │  buyers; ~$3,200/HH annually)     │                         │
   │     └──────────────┬────────────────────┘                         │
   │                    │                                              │
   │                    │  Consumption-pattern data                    │
   │                    ▼                                              │
   │     ┌──────────────────────────────────┐                         │
   │     │  PREDICTIVE SHIPPING              │                         │
   │     │  Pre-position inventory near HH   │                         │
   │     │  ML on every purchase signal      │                         │
   │     └──────────────┬────────────────────┘                         │
   │                    │                                              │
   │                    │  Faster delivery → more Prime renewals       │
   │                    ▼                                              │
   │     ┌──────────────────────────────────┐                         │
   │     │  LOCK-IN                          │                         │
   │     │  Each marginal basket increases   │                         │
   │     │  switching cost                   │                         │
   │     └──────────────┬────────────────────┘                         │
   │                    │                                              │
   │                    └──────────► back to PRIME                     │
   │                                                                   │
   └────────────────────────────────────────────────────────────────┘
```

Each arrow in the flywheel reinforces the next. Your retail client cannot disrupt one arrow alone — Amazon's response is to tighten the others. **They have to break the flywheel from outside, with a coalition Amazon cannot replicate.**

### What your client has already lost

| Category | Amazon share of US auto-replenishment | Trajectory |
|---|---|---|
| Diapers + baby formula | ~38% (Amazon Mom + Subscribe & Save) | Up 4pp YoY |
| Pet food + supplies | ~31% | Up 3pp YoY |
| OTC + personal care | ~24% | Up 5pp YoY |
| Coffee + beverages | ~28% | Up 4pp YoY |
| Cleaning + laundry | ~22% | Up 2pp YoY |
| Pantry staples | ~15% (Whole Foods + Amazon Fresh + S&S) | Up 6pp YoY |

These are categories where Kroger, Costco, Target, and Walmart should be winning. Amazon takes them by owning the **agentic consumption layer** — the layer your client has never been able to credibly compete in.

Until now.

---

## 1. Why your retail client can't beat Amazon alone

| Asset Amazon owns | Why a single retailer can't match it |
|---|---|
| **Voice surface** (Alexa, 70M+ Echo devices) | A single retailer cannot get sub-$50 voice hardware into 70M homes; Amazon subsidizes Echo at every gift moment to acquire the surface |
| **Home device distribution** (Prime Day deals, Best Buy slotting) | Amazon controls the device-distribution channel through its own marketplace; retailers have no equivalent path |
| **Consumption data layer** (Subscribe & Save + Alexa logs) | Each retailer sees only its own purchase pattern; Amazon sees the cross-merchant whole because they're the destination |
| **Predictive shipping infrastructure** | $25B+ logistics capex; only Walmart even tries to match it, and they are 3 years behind |
| **Single-source ML compounding** | Amazon's data engine improves with every purchase; a fragmented retailer environment cannot pool data |

**The structural answer is not "compete harder."** It is **"build a coalition with assets Amazon does not control."**

---

## 2. The counter-move — the three-party coalition

Three parties bring three assets Amazon cannot replicate. **Each alone is outmatched. Together they win.**

```
   ┌─────────────────────────────────────────────────────────────────┐
   │  THE COALITION                                                   │
   │                                                                   │
   │   ┌────────────────────┐    ┌────────────────────┐               │
   │   │   RETAILER         │    │   TELCO            │               │
   │   │   (Kroger,         │    │   (AT&T, Verizon,  │               │
   │   │    Costco,         │    │    T-Mobile,       │               │
   │   │    Target, etc.)   │    │    Comcast)        │               │
   │   │                    │    │                    │               │
   │   │   • Catalog        │    │   • Home edge      │               │
   │   │   • Fulfillment    │    │   • Network        │               │
   │   │   • Loyalty trust  │    │   • Device CPE     │               │
   │   │   • Price + margin │    │   • CPNI privacy   │               │
   │   │                    │    │     custodianship  │               │
   │   └─────────┬──────────┘    └─────────┬──────────┘               │
   │             │                          │                          │
   │             └────────────┬─────────────┘                          │
   │                          │                                        │
   │                          ▼                                        │
   │              ┌────────────────────────┐                           │
   │              │   DELOITTE / APEX      │                           │
   │              │                        │                           │
   │              │   • Delivery framework │                           │
   │              │   • Agentic-AI engine  │                           │
   │              │   • Audit-defensible   │                           │
   │              │     LEDGER             │                           │
   │              │   • Independence-safe  │                           │
   │              │     funding paths      │                           │
   │              └────────────────────────┘                           │
   │                                                                   │
   └─────────────────────────────────────────────────────────────────┘
```

| Asset | Amazon | Coalition |
|---|---|---|
| Voice surface | Alexa (their own) | Sonos + tablet kiosk (third-party + neutral) |
| Home edge distribution | Echo subsidization | **Telco CPE wrap** (already in the home, billed monthly) |
| Consumption observability | Subscribe & Save logs | **Vision AI Dev Kit + smart-fridge cams + smart pantry** (Edge-resident, multi-merchant) |
| Privacy custodianship | Commercial ToS | **CPNI statutory regime (Variant A) · Loyalty fiduciary + LEDGER attestation (Variant B)** |
| Multi-merchant catalog | None — Amazon-only | **Native** — household picks Kroger for groceries, Costco for bulk, Target for essentials |
| Agentic backend | Alexa (closed) | **APEX framework** (open, cloud-neutral, audit-defensible) |

Amazon has tried to acquire each of these capabilities individually. **They cannot acquire them in the right combination because the combination requires regulated telco partnership, neutral integrator, and multi-merchant catalog — all three of which contradict Amazon's core business model.**

This is the structural moat.

---

## 3. The counter-flywheel — built by the coalition

```
   ┌────────────────────────────────────────────────────────────────┐
   │                                                                  │
   │     ┌──────────────────┐                                         │
   │     │  TELCO HOME      │ ──────►  Home edge distribution         │
   │     │  CONCIERGE       │          (CPE wrap, no acquisition cost)│
   │     │  $25-40/mo       │                                         │
   │     │  bundle          │ ──────►  Bundles Sonos + Vision Kit +   │
   │     └────────┬─────────┘          Tablet at retail BOM cost       │
   │              │                                                    │
   │              │  CPNI regime in force                              │
   │              ▼                                                    │
   │     ┌──────────────────────────────────┐                         │
   │     │  CONSUMPTION OBSERVABILITY        │                         │
   │     │  (PARS)                           │                         │
   │     │  • Pantry · fridge · pet · etc.   │                         │
   │     │  • Edge-resident · 8 services     │                         │
   │     └────────────┬─────────────────────┘                         │
   │                  │                                                │
   │                  │  Auto-replenish events                         │
   │                  ▼                                                │
   │     ┌──────────────────────────────────┐                         │
   │     │  RETAILER FULFILLMENT             │                         │
   │     │  • Kroger Plus catalog            │                         │
   │     │  • Costco bulk · Target home      │                         │
   │     │  • Household chooses per service  │                         │
   │     └────────────┬─────────────────────┘                         │
   │                  │                                                │
   │                  │  Basket revenue + loyalty deepening            │
   │                  ▼                                                │
   │     ┌──────────────────────────────────┐                         │
   │     │  PRIVACY TRUST DEEPENS            │                         │
   │     │  • LedgerRow audit-defensible     │                         │
   │     │  • DPO + regulator-ready          │                         │
   │     │  • Constitutional hard rules      │                         │
   │     └────────────┬─────────────────────┘                         │
   │                  │                                                │
   │                  │  Privacy-conscious households recruit          │
   │                  ▼                                                │
   │     ┌──────────────────────────────────┐                         │
   │     │  COALITION ATTACH GROWS           │                         │
   │     │  More HH enrolled →               │                         │
   │     │  more services attached →         │                         │
   │     │  more telco subscription value    │                         │
   │     └────────────┬─────────────────────┘                         │
   │                  │                                                │
   │                  └──────► back to TELCO HOME CONCIERGE            │
   │                                                                   │
   └────────────────────────────────────────────────────────────────┘
```

Same flywheel shape Amazon has perfected — owned by the coalition instead of Amazon.

---

## 4. Why privacy is the killer wedge (the part Amazon literally cannot copy)

Amazon's flywheel runs on **maximal household data accumulation in a single commercial entity**. The coalition's flywheel runs on **distributed data with regulated custodianship**. These are opposite shapes.

| | Amazon | Coalition (Variant A — telco-fronted) |
|---|---|---|
| Privacy regime | Commercial ToS · FTC settled 2023 over Alexa data retention | §222 CPNI statutory · state PUC oversight · enforceable consumer-protection floor |
| Children policy | COPPA settlement 2019 + ongoing findings | Constitution hard rule: under-13 cannot be voice-enrolled · privacy-class enforcement for diaper/OTC |
| Cross-tenant correlation | Default behavior — improves Amazon's model | Constitutional hard block at runtime · per-tenant LEDGER partition |
| DPO replay | Not available | `apex-replay <view_id> <ts>` reproduces decision byte-identical with consent state |
| Regulator-friendly | Increasingly hostile FTC/state AG/EU DPA posture | Cooperates by construction — CPNI is the statutory format regulators already audit |

The **privacy-conscious upper-middle household segment** — roughly 22% of US households, disproportionately high-LTV, low Amazon-loyalty, high education, dual-income — is the **first wave the coalition wins from Amazon**. These households are actively shopping for an alternative *today*. PARS gives them one.

Once the privacy segment defects, the **value-conscious segment** follows — because the coalition undercuts Amazon's effective price on staples once you factor out Prime fee + Alexa device cost + privacy externality. The third wave is **share-of-wallet of remaining Prime households** who keep Prime for shipping but route auto-replenish through the coalition for privacy.

---

## 5. The 8-service catalog — what the coalition wins back, service by service

Each service is positioned as a category Amazon is winning today and the coalition's specific counter-tactic.

| # | Service | Amazon current share | Coalition counter-play |
|---|---|---|---|
| 1 | **Pantry Auto-Buy** | ~15% (S&S + Whole Foods) | Vision Kit shelf cam · multi-merchant (Kroger / Costco / Wegmans) · CPNI privacy |
| 2 | **Fridge Auto-Buy** | Early (Whirlpool partnership) | First-mover wins the household before Amazon does · merchant-neutral |
| 3 | **Diaper Auto-Buy** | ~38% (Amazon Mom) | Privacy-conscious parents · Target Diapers + Babies-R-Us renaissance · CPNI shields family-composition data |
| 4 | **Pet Food Auto-Buy** | ~31% (Chewy is also Amazon-aligned) | Petco / PetSmart · smart-bowl integrations (Petlibro, Sure Petcare) |
| 5 | **OTC + Personal Care Auto-Refill** | ~24% | CVS / Walgreens / Costco — Sensitive class · CPNI shields health-adjacent inference |
| 6 | **Beverage / Sparkling** | ~28% | Costco bulk · Kroger private label · Target Good & Gather |
| 7 | **Coffee Subscription** | ~28% | Direct-to-consumer roasters · Costco Kirkland · Target House Blend — **recommended Lite pilot** |
| 8 | **Cleaning + Laundry** | ~22% | Costco bulk · Walmart Great Value · Target Up & Up |

**Per-service strategic positioning:**

### Pantry Auto-Buy (#1) — the wedge
- Largest dollar category Amazon is taking; lowest privacy sensitivity
- Vision Dev Kit on pantry shelves (proven in current demo)
- Multi-merchant catalog: household chooses Kroger Plus pricing for branded, Costco for bulk, Wegmans for premium
- Wins the **upper-middle dual-income household** that does most of its routine shopping at multiple stores

### Diaper Auto-Buy (#3) — the privacy-segment killer
- Amazon Mom owns 38% but has lost trust with privacy-conscious parents post-2019 COPPA settlement
- Target Diapers (Up & Up + branded) + Costco Kirkland has the catalog to compete on price
- CPNI shields family-composition inference — the single biggest objection privacy-conscious parents raise against Amazon Mom
- Pilot segment: dual-income parents in tech-adjacent metros (Austin, DFW, Seattle, NoVa, Bay Area)

### OTC + Personal Care (#5) — the regulated-data play
- Amazon has 24% and is gunning for prescription via PillPack
- CVS / Walgreens / Costco own the loyalty footprint and pharmacist trust
- Sensitive class with extra Constitution rules; telco-fronted only (Variant A)
- Wins **health-conscious + privacy-conscious overlap** (boomers + Gen X with chronic conditions)

### Coffee Subscription (#7) — the Lite pilot recommendation
- Highest consumer NPS lift potential (coffee is daily ritual, running out is high-pain)
- Lowest privacy sensitivity
- Multi-merchant catalog wins on premium variety (DTC roasters + Costco Kirkland + Target Good & Gather)
- **Single-week productionization** on the current demo — fastest possible BVA→Lite path

---

## 6. The autonomy spectrum (kept from v0.1 — the key product innovation)

The level of human involvement scales with the size and sensitivity of the auto-buy. This is what makes PARS feel **invisible to the household** while still being **audit-defensible to the regulator**.

| Trigger threshold | Default | What fires |
|---|---|---|
| `$AUTO_BUY_THRESHOLD` (per-item) | $25 | Under this, autonomous with notification |
| `$BUNDLE_THRESHOLD` (consolidated) | $75 | Above this, active HITL confirm |
| `$PER_DAY_CAP` (24h cap) | $150 | Above this, active HITL regardless of individual items |
| `ANOMALY_SCORE_THRESHOLD` (pattern shift) | 0.6 | 3× normal rate, composition change inference, OOD pattern → active HITL |
| `SENSITIVE_CATEGORY` (Diaper, OTC) | always | Active HITL regardless of price |

**What the household sees:**

- **Routine auto-buy under $25**: kiosk badge + daily SMS digest. No interruption.
- **Bundled $75+**: kiosk modal: *"About to order $X. Confirm?"* — active confirm.
- **Anomaly detected**: kiosk modal: *"We noticed something different — review?"* — active confirm or pause.
- **Subscription cancel**: voice or touch active confirmation.

The system **only asks when there's something worth asking about.** Pure routine consumption never interrupts. **No other auto-replenishment service can claim this combination** of household trust + audit defensibility + Constitution-enforced privacy.

---

## 7. APEX framework alignment

PARS is the **8th Industry Solution Pack** in the APEX catalog. Standard 10-asset bundle, 6-Agent Fleet, LEDGER hash chain, Service Envelope tiers. No framework changes required beyond the 7 Foundation enhancements catalogued below.

| APEX layer | PARS contribution |
|---|---|
| Pack namespace | **PARSML** (new) |
| Schemas | `PARSML.ConsumptionEvent`, `PARSML.ConsumptionPattern`, `PARSML.ReplenishmentTrigger`, `PARSML.AutonomyDecision`, `PARSML.AnomalyFlag`, `PARSML.MerchantBinding` |
| Virtual Views | ~14 VVs (`parsml.pantry_state`, `parsml.consumption_pattern_30d`, `parsml.anomaly_score`, `parsml.household_threshold_profile`, etc.) |
| Scenarios | 18 scenarios across the 8 services (2-3 per service: enrollment + routine + anomaly) |
| Persona | `household` (from CHC v0.2 §4.1) |
| HITL surfaces | `sonos_voice` · `home_kiosk` · `customer_phone` · **`passive_notification`** (new for autonomous-with-notice flows) |
| Constitution | `hard_in_home` (6 CHC rules) + 4 new autonomy rules (§9 below) |
| LEDGER | Standard 14-field + 4 PARSML payload fields: `consumption_window`, `autonomy_decision`, `threshold_invoked`, `anomaly_score` |
| Cloud profile | APEX-M primary; -G and -A via shared 10-asset bundle |
| Service envelope | T2 Lite/Std/Ent + T3 cross-pack chain (Variant A) + T5 Operate |

---

## 8. Foundation enhancements (7 ARB items total — 6 from CHC, 1 net-new)

| # | Foundation enhancement | Source | Status |
|---|---|---|---|
| 1 | `household` persona type | CHC v0.2 §4.1 | Designed |
| 2 | `sonos_voice` HITL | CHC v0.2 §4.2 | Designed (scaffold task #31) |
| 3 | `home_kiosk` HITL | CHC v0.2 §4.2 | Designed (scaffold task #30) |
| 4 | `customer_phone` HITL | CFMP v0.2 §6.2 | Designed |
| 5 | NEED-phase customer journey → broadened as "consumption phase" | CHC v0.2 §4.3 → extended | Designed |
| 6 | Interface #16 Home-Edge Device Plane | CHC v0.2 §4.5 | Proposed for ARB |
| 7 | **`passive_notification` HITL** — net-new for PARS autonomous-with-notice flow | This doc | Proposed for ARB |

Each enhancement pays forward to every future household-side Pack: Telco-Customer, Insurance-In-Home, Healthcare-At-Home, Hospitality-Guest, Auto-Subscription-Services.

---

## 9. Privacy contract — `hard_in_home` extended with autonomy rules

The Constitution from CHC v0.2 §7 has six hard rules. PARS adds **four autonomy-specific rules** that block at the runtime layer:

7. **No autonomous purchase above $X per-item or $Y per-day** without active HITL. Defaults conservative; tunable per household but the floor cannot be removed.
8. **No autonomous enrollment of a new SKU category** — first auto-buy in any category requires active HITL pattern enrollment.
9. **No autonomous purchase of any item flagged sensitive** (children's, health-adjacent, financial-impacting) — always active HITL regardless of price.
10. **No autonomous purchase during a paused/cancelled subscription state**, even if the consumption signal would otherwise trigger one. Pause is sovereign.

Combined with the CHC v0.2 rules (raw frames never leave home, no off-list inferences, voice-print consent per member, privacy minute, quiet hours, no cross-household correlation), PARS has **10 Constitution hard rules** auditable in YAML, blocked at runtime, reviewed by Client's DPO before any deployment.

---

## 10. The retailer-by-retailer playbook

| Retailer | Loyalty footprint | First-banner pilot | Strategic objective |
|---|---|---|---|
| **Kroger** | ~60M Kroger Plus | Smith's (UT/NV) — AT&T fiber overlap | Defend grocery share from Amazon Fresh + Whole Foods |
| **Costco** | ~130M paying members | Single-warehouse pilot in Dallas-Fort Worth | Defend bulk-staples + Kirkland share from AmazonBasics |
| **Target** | ~100M Target Circle | "Smart Home" tier within Circle 360 | Defend household-essentials + drive Drive Up attach |
| **Walmart** | ~25M Walmart+ (growing) | Northeast or Midwest pilot | Aggressive feature parity vs Prime + agentic auto-buy |
| **Wegmans / Trader Joe's** | ~3M / loyalty-light | Direct-to-consumer Premium tier (Variant B) | Privacy-segment capture |
| **CVS / Walgreens** | ~75M / ~85M | Variant A only (Sensitive class) | OTC + Rx auto-refill — defensive against PillPack |
| **Wholesalers/specialty** (Aldi, H-E-B, Publix, Whole Foods alternates) | Regional | Variant B Premium tier | Regional banner defense |

Each engagement is a separate Deloitte sale. **No retailer needs the others' buy-in to start** — the coalition forms over time as retailers join. First-mover at any retailer captures privacy-conscious segment irreversibly.

---

## 11. The telco-by-telco playbook (Variant A buyers)

| Telco | Subscriber footprint | Strategic objective | First-pilot DMA |
|---|---|---|---|
| **AT&T** | ~84M wireless · ~14M fiber | ARPU expansion + churn defense + counter Amazon disintermediation | DFW or Houston (high fiber density + Kroger Smith's overlap) |
| **Verizon** | ~143M wireless · ~10M Fios + 5G Home | Premium tier add-on + 5G Home differentiation | Boston / NoVA / NYC suburb |
| **T-Mobile** | ~120M wireless · ~5M 5G Home (fastest-growing) | Differentiate on privacy-first agentic vs Verizon/AT&T | Phoenix or Atlanta |
| **Comcast** | ~32M Xfinity Internet · ~17M Mobile | Expand Xfinity Home from security to commerce | Philadelphia / Chicago / Bay Area |

Each telco is fighting Amazon, Google, Apple, and Roku for share of the home-services attach. **PARS gives each telco a defensible category Amazon literally cannot match** because Amazon cannot become CPNI-regulated.

---

## 12. The B2B2C and B2C distribution models

### Variant A — B2B2C (Retailer × Telco × Household)

**Use when**: Privacy-conscious segment is the target; multi-merchant catalog matters; telco distribution channel is available.

```
Household pays Telco $25-40/mo for "Home Concierge" tier
Telco bundles: hardware + PARS subscription + multi-merchant catalog
Telco revenue-shares with each enrolled retailer
Retailer captures the basket they would otherwise lose to Amazon
Deloitte engages both Telco (TCP build) and Retailer (CFMP/PARS build)
```

### Variant B — B2C (Retailer direct)

**Use when**: Speed-to-market matters more than privacy positioning; merchant has strong loyalty program; cross-merchant catalog is not yet required.

```
Household pays Retailer $15-25/mo for "Premium" tier (e.g., Kroger Plus Premium)
Retailer bundles: hardware kit ($149-199 at-cost) + PARS subscription
Retailer is the privacy custodian (loyalty fiduciary + LEDGER attestation)
Single-merchant catalog (acceptable for tightly-loyal segments — Costco, Wegmans)
Deloitte engages only the Retailer
```

**Coalition recommendation**: pursue Variant B with Kroger Plus (or Costco, or Target Circle 360) in 6-8 weeks; use that as the proof rig for the Variant A telco pitch. Land both within a 12-month arc. Joint TCV = $20-30M per pairing.

---

## 13. Engagement structure and pricing

| Tier | Scope | Price | Timeline | Funding |
|---|---|---|---|---|
| **BVA Workshop** | 4-hour scenario shortlist + threshold-tuning + privacy stance | $0-50K | 1 day | BVA |
| **PARS Lite** | 1 service live in pilot HH cohort (recommended: Coffee #7) | **$200-350K** | **4-6w** | BVA + DCIF |
| **PARS Standard** | 4 services + multi-merchant catalog | $1.0-1.8M | 12-16w | DCIF + T&M + ISV burndown |
| **PARS Enterprise** | All 8 services + cross-channel attribution + multi-banner | $2.5-4.5M | 6-9mo | Client direct + T&M |
| **Cross-pack scenario chain** (Variant A only) | Telco TCP + PARS wire-up via federation adapter | $300-450K | 4-6w | DCIF |
| **T5 Operate** | 24×7 + threshold tuning + Pack version uptake + DataOps | $30-90K/mo | Continuous | Client direct |

**3-year TCV targets:**
- Variant A pairing (one telco + one retailer): **$8-15M build + $0.5-1M/yr Operate**
- Variant B per retailer: **$4-8M build + $0.3-0.6M/yr Operate**
- Combined coalition (both variants at one DMA): **$20-30M total Deloitte revenue**

Microsoft money via **ISV Marketplace burndown + SI Teaming**. Deloitte never receives ECIF directly from Microsoft. APEX-M cloud profile; -G / -A available per the 14-interface contract.

---

## 14. The 3-year land-and-expand sequence

| | Year 1 (FY27) | Year 2 (FY28) | Year 3 (FY29) |
|---|---|---|---|
| **Variant A pilots** | AT&T × Kroger × 1 DMA (DFW) · ~1K households | + Verizon × Walmart · + T-Mobile × Target | All Tier-1 carrier × retailer pairings (≥10) · multi-million HH |
| **Variant B pilots** | Kroger Plus Premium in 2 banners (Smith's + Mariano's) · ~5K HH | + Costco · + Target Circle 360 | Every Tier-1 retailer has direct variant |
| **Service catalog** | Coffee + Pantry live | + Pet Food, Cleaning, Beverages | All 8 services + cross-channel attribution |
| **Coalition retailers** | 1-2 | 4-6 | 8-12 |
| **Coalition telcos** | 1 | 2-3 | All Tier-1 |
| **Total households enrolled** | 6-10K | 200-400K | 5-10M |
| **Amazon basket recapture** | $30-50M | $1-2B | $6-10B (across coalition) |
| **Deloitte cumulative engagement** | $1-3M | $15-25M | $50-80M |

By end of Year 3, **the coalition has structurally taken back the privacy-conscious segment of US household consumption** from Amazon. The agentic consumption layer is contested for the first time since Subscribe & Save launched.

---

## 15. The defensible moat — why Amazon can't follow

| Amazon countermove they cannot execute | Why |
|---|---|
| Become a regulated telco custodian | Would require Communications Act §214 certification — Amazon will not become a common carrier |
| Position credibly as "privacy-first" | FTC 2023 Alexa settlement · ongoing COPPA findings · 11 state AG investigations · decade of public data-handling controversies |
| Offer multi-merchant catalog | Cannibalizes Amazon's own retail margin · contradicts Marketplace model |
| Open the agentic backend | Alexa Skills SDK is a closed ecosystem; opening would erode platform lock-in |
| Match CPNI's statutory floor with a commercial ToS equivalent | Statutorily impossible — only telcos qualify under §222 |
| Acquire a Tier-1 telco | Regulatory approval impossible under current FCC/FTC posture |

Amazon's only credible counter is **lowering Subscribe & Save price** (a margin-destructive race-to-the-bottom) or **offering deeper Prime discounts** (further pressure on AWS margins). Both are exactly the responses the coalition wants Amazon to give.

**This is a fight Amazon cannot win on its own terms.** The coalition's job is to ensure the fight stays on the coalition's terms — privacy, multi-merchant, regulated custodianship, audit-defensibility.

---

## 16. Why Deloitte is the right integrator

| | Why it matters |
|---|---|
| **Independent of Amazon, Microsoft, Google, and every retailer** | Coalition members trust a neutral integrator who isn't aligned with any single party |
| **Microsoft platform depth (DMTSP)** | APEX-M runs on Foundry + Azure OpenAI + OneLake + Entra + Purview — the cleanest agentic-AI stack |
| **Multi-industry practice (RC + Telco + others)** | Same team can engage both sides of a Variant A coalition simultaneously |
| **APEX framework** | Only cloud-neutral, audit-defensible, 14-interface agentic-AI delivery framework in market |
| **Working demo today** | Vision Kit + Sonos + tablet + LEDGER + Constitution all running at `ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io` — buyers see proof, not slides |
| **Independence-safe by construction** | Microsoft money rides ISV Marketplace + SI Teaming, never direct ECIF |
| **Long-game posture** | Run-rate Operate fees compound across the install base — Deloitte's incentive aligns with coalition durability |

---

## 17. Market sizing — the BVA opens this conversation

| Metric | Value | Source |
|---|---|---|
| US households | ~130M | Census |
| Privacy-conscious segment | ~22% | Pew Research 2025 |
| Amazon basket captured via S&S + Alexa Reorder, per HH/yr | ~$3,200 | Amazon shareholder reports + market research |
| **Total annual basket Amazon currently captures via agentic auto-replenish** | **~$92B** | $3,200 × 22% × 130M (segment) extrapolated to share-of-wallet |
| Coalition target recapture (3-year, privacy + value-conscious segments) | **8-15% = $7-14B** | Land-and-expand assumption |
| Deloitte engagement value capture | 0.5-1.0% | Build + Operate fee on recaptured basket |
| **Cumulative Deloitte opportunity** | **$35-140M over 3 years** | Across coalition retailers + telcos |

The BVA workshop frames the conversation: **how much of this is at your client's retailer / telco specifically, and how fast can the coalition assemble?**

---

## 18. Implementation path from current demo

The current CFMP demo at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io` already lights up the underlying capability. **PARS Lite (Coffee Subscription) is ~4-6 weeks of build on top of what runs today.**

### Already live (task history)
- Vision AI Dev Kit (tasks #1-25) — adaptable for coffee-grinder telemetry capture
- pgvector catalog with 800 SKUs (task #51) — multi-merchant ready
- Cart + checkout flow (task #71)
- Microsoft Agent Framework 1.6.0 GA on gpt-5-mini (tasks #68, #70)
- Azure Speech Ava Multilingual TTS/STT (task #90)
- Sonos Era 100 scaffold (task #31)
- Tablet kiosk mode (task #30)
- Beelink home-edge server (task #29) — privacy-floor enforcement
- APEX wedge: LEDGER + Purview lineage (task #85)
- LEDGER HITL gate at $50 — already running

### Net-new for PARS Lite Coffee (~4-5 weeks)
1. **Consumption-pattern learning agent** (~1.5w) — 14-day rolling rate per espresso cycle
2. **Autonomy decision module** (~3d) — 4-threshold authorization spectrum
3. **`passive_notification` HITL transport** (~3d) — kiosk badge + SMS digest
4. **Constitution autonomy-rules YAML** (~1d)
5. **Pattern-enrollment kiosk UI** (~1w) — pattern card + price + cadence + confirm
6. **Coffee-service-specific adapter** (~1w) — espresso telemetry + bag-weight scan
7. **PARSML VV manifests** for Lite scope (~3d)
8. **Acceptance test suite** (~3d) — 30+ tests

Total: **~5 calendar weeks of build**. One service live in a household pilot within **6-8 weeks** of BVA workshop close.

---

## 19. Open questions for the BVA workshop

1. **First service** — recommend Coffee (#7) as the Lite pilot; ratify with client
2. **First retailer × telco pairing** — recommend AT&T × Kroger × Smith's banner in DFW
3. **Multi-merchant catalog source-of-truth** — APEX-maintained unified catalog vs per-merchant feed with overlay
4. **Anomaly tolerance** — tight vs loose threshold defaults
5. **Children-in-household policy** — Variant A only for Diaper service? Third-party privacy attestation gating launch?
6. **Termination flow** — retention schedule for LEDGER rows on subscription cancel
7. **Coalition governance** — who arbitrates revenue share between telco + retailer? What's the dispute-resolution process?
8. **Branding** — telco "Home Concierge" name vs co-brand with retailer ("AT&T Home Concierge with Kroger") vs retailer-led ("Kroger Smart Pantry powered by AT&T")?

---

## 20. The seller talk track — drop-in lines per buyer

### To a retail CMO / CX-VP
> "Amazon is taking your basket through the consumption layer — Subscribe & Save plus Alexa Reorder are eating six categories of your business and the share keeps growing. There's no single retailer that can compete on this layer alone, but a coalition can. We've built it. The pilot runs in your DMA in six to eight weeks for two-fifty K."

### To a telco CIO / CDO
> "Your customer's consumption data is the most valuable household signal in commerce, and it's sitting in Amazon today. CPNI is the only statutory regime in the country that can credibly compete with Amazon on privacy. You have the only legal pathway to be the regulated custodian of the smart-home commerce layer. We turn that into a $25-to-40-a-month Home Concierge tier on your fiber bill."

### To a DPO / Chief Privacy Officer
> "We didn't add privacy to a commerce service. We built a commerce service that *only works* with privacy in force. Every auto-buy lands a hash-chained ledger row with the consent state captured at decision moment. apex-replay reproduces decisions byte-identical for regulators. The Constitution blocks at the runtime layer — not as policy, as code."

### To a board / CEO of any coalition member
> "Amazon's home-commerce dominance flywheel is the most important asymmetric threat in retail in twenty years. No single retailer can fight it. A coalition — your company, a Tier-1 telco, Deloitte as integrator — can. We're convening the coalition. We'd like to start with your loyalty base."

---

## 21. Related artifacts

- **CHC v0.2 design** — engineering reference for `household` persona, HITL surfaces, Constitution: `docs/packs/Connected-Home-Commerce-v0.1.md`
- **CFMP v0.2 design** — base pack PARS overlays on: `docs/packs/CFMP-v0.2.md`
- **Field guide** — seller-facing companion: `docs/reference/Sellers-Guide/APEX-CFMP-CHC-Sellers-Guide-for-DMTSP.md`
- **BVA workshop deck** — facilitator deck (adapt for PARS coalition workshop): `docs/reference/Sellers-Guide/BVA-Workshop-Facilitator-Deck.pptx`
- **ROI calculator** — formulas extensible to coalition revenue model: `docs/reference/Sellers-Guide/BVA-ROI-Calculator.xlsx`
- **SOW skeletons**: `docs/reference/SOW-Templates/`
- **Working demo** — coalition proof rig: `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io`
- **APEX teaching deck (v3)**: `C:\Users\kmarkham\Downloads\APEX-Design-v3.pptx` — reference slides: S6 Bronze · S7 LEDGER · S22 14-interface contract · S23 Multi-cloud · S31 Burst flight-recorder · S34 Constitution · S36 Multimodal Featurization

---

*Internal · Deloitte's Microsoft Technology & Services Practice · Prepared by Keven Markham, VP · 2026-05-23*
