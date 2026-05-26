# Connected Home Commerce (CHC) — Engagement Design v0.2

**Status**: Draft for DMTSP review — first cross-pack engagement design
**Owner**: Keven Markham, VP — Deloitte's Microsoft Practice (DMTSP)
**Date**: 2026-05-23
**Version history**:
- **v0.2** (2026-05-23): Added B2C variant — Kroger-direct go-to-market (§14-17). Same APEX engineering, single-client engagement, different commercial structure.
- v0.1 (2026-05-23): Initial B2B2C cross-pack design (AT&T × Kroger).

**Worked examples**:
- **Variant A — B2B2C**: AT&T (Telco buyer) × Kroger (Merchandiser partner) × Household (consumer) — *cross-pack engagement, two clients, primary+satellite cloud topology*
- **Variant B — B2C**: Kroger (direct-to-consumer) × Household — *single-pack engagement (CFMP-Home extension), one client, single-cloud topology*

**Key architectural point**: both variants run the **same APEX engineering** — same `household` persona, same `sonos_voice` / `home_kiosk` HITL surfaces, same NEED phase, same Constitution, same 6-Agent Fleet. Only the `identity_binding.source:` field in `personas.yaml` and the cloud topology change. **Switching variants is a manifest change, not a re-platform.** That's the framework's leverage.

---

## 0. Strategic thesis — replace Amazon Alexa for agentic commerce

The home-commerce voice-agent market is dominated by **Amazon Alexa** — ~70M US households have an Alexa-capable device, and every voice-driven purchase routes through Amazon's commerce engine by default. That's the problem CHC solves.

### The Alexa problem (for everyone who isn't Amazon)

| Stakeholder | Alexa's structural conflict |
|---|---|
| **Merchandiser** (Kroger, Walmart, Target, Wegmans) | Amazon is a direct competitor. Every "Alexa, order milk" routes basket to Amazon Fresh / Whole Foods by default. Merchandisers either pay Amazon for Skill placement or get disintermediated. |
| **Telco** (AT&T, Verizon, T-Mobile, Comcast) | Alexa rides their pipe and bypasses every customer-facing service they could otherwise offer. ARPU expansion blocked. |
| **Household** | Wake-word always listening, voice data trained against ad targeting, no contractual privacy floor, content moderation TOS one-sided. Privacy posture documented in repeated regulatory actions (FTC 2023 settlement, COPPA findings). |
| **Regulator** (state AGs, FTC, EU DPAs) | No statutory privacy custodian; Amazon's role is "commercial provider" with ToS-based recourse only. Children-data findings continuing. |

**There is no neutral, regulated, merchant-agnostic alternative in the home agentic-commerce category.** That's the white space CHC fills.

### Why a Telco-fronted home agent is the natural Alexa-replacement (Variant A)

Telcos have a structural advantage Amazon literally cannot replicate:

1. **Regulated privacy custodian by law.** US Communications Act §222 (CPNI) and state PUC rules already obligate carriers to handle customer communications data under a fiduciary-grade standard with statutory penalties. The privacy posture is not a marketing claim — it's a legal regime. Amazon has no equivalent.
2. **Not a merchant.** AT&T doesn't compete with Kroger for the basket. Verizon doesn't compete with Walmart. The voice surface stays neutral, and every merchandiser can plug in on equal terms.
3. **Already in the home.** Fiber CPE, 5G home internet, set-top boxes, Wi-Fi mesh — telcos have device-distribution rails that don't need new household acquisition cost.
4. **Defender for IoT + carrier-grade security.** Edge-device security is a telco core competency; Alexa devices are consumer-grade.
5. **Identity binding to a billed account.** The household is already a known, billed entity with statutory privacy rights. No fragile "Amazon account" attestation.

The pitch to AT&T, Verizon, T-Mobile, Comcast: **"You sell home internet. We add the regulated, privacy-first, merchant-neutral voice-commerce layer on top — and you keep the ARPU Amazon was taking."**

### Why a Merchant-direct home agent is the loyalty-deepening variant (Variant B)

For merchandisers without a telco partner ready to move (or where the merchandiser owns enough of the customer relationship to go direct):

1. **Loyalty-program leverage.** Kroger Plus has 60M+ members. The voice surface lives inside the loyalty program; the customer trusts Kroger because they already shop there.
2. **No Amazon cut.** Every basket routes to Kroger by default. The merchandiser captures 100% of the commerce, not the 30% Skill-mediated remainder.
3. **First-party data only.** No off-merchant data exchange; Kroger's existing data-broker posture extends to voice naturally.
4. **Faster than B2B2C.** One client to sign, not two.

The pitch to Kroger: **"Your Kroger Plus app already has 60M trusted households. Add a Smart-Pantry tier with in-home cameras + Sonos + tablet. Take the basket Alexa was sending to Amazon Fresh."**

### How APEX makes both variants real

The Alexa-replacement narrative is only credible if the *technical* answer is credible. APEX delivers four things Alexa structurally cannot:

| Capability | Alexa | APEX-CHC |
|---|---|---|
| Privacy custodian | Amazon (commercial ToS) | Telco (CPNI statutory — Variant A) or Merchandiser (loyalty fiduciary + LEDGER attestation — Variant B) |
| Audit trail | None disclosed | 14-field WORM LEDGER, cryptographic hash chain, apex-replay (S7) |
| Constitution / hard rules | Amazon-internal ToS | Per-pack `constitution.yaml` — auditable hard rules block at the runtime layer (S34) |
| Multi-merchant neutrality | Skill-mediated, fee-extracted | Each merchandiser has its own Pack, equal contract, no platform tax |
| In-home privacy mode | "Mute" button (advisory) | `hard_in_home` mode — raw frames never leave the house; embeddings only; constitution-blocked off-list inferences (§7) |
| Replay for DPO / regulator | Not available | `apex-replay <view_id> <ts>` reproduces decision byte-identical with consent state preserved |
| Cross-cloud portability | Locked to AWS | APEX-M / -G / -A — change `profile:` in manifest (S22) |

**The Alexa-replacement positioning is not a slogan. It's the structural difference between a commercial ad-platform and a regulated agentic-AI delivery framework.**

### Strategic sequencing (3-year)

| Year | Variant A — Telco-mediated | Variant B — Merchant-direct |
|---|---|---|
| Y1 (FY27) | AT&T × Kroger pilot in 1 DMA (DFW or Houston) — 1,000 households | Kroger Plus Premium pilot in 2 banners (Smith's + Mariano's) — 5,000 households |
| Y2 (FY28) | AT&T national rollout (~100K households) + Verizon × Walmart pilot | Kroger national + Walmart+ launch |
| Y3 (FY29) | All Tier-1 US carriers paired with all Tier-1 merchandisers (~10 pairings) — multi-million household scale | Every Tier-1 merchandiser has a direct variant; the in-store CFMP, in-home Variant B, and Variant-A federation share schemas |

By year 3, **APEX is the de-facto home-commerce agent framework**, and Alexa has competition for the first time in the category's history. Deloitte is the integrator on every major engagement.

---

## 1. The deal in one paragraph

AT&T sells a **Connected Home Commerce** subscription to households: in-home cameras, Sonos speakers, and a kitchen kiosk tablet detect consumption ("we're running low on milk"), suggest replenishment ("want me to add it to Wednesday's Kroger delivery?"), and auto-order against Kroger's catalog with a single voice or touch confirmation. AT&T owns the customer relationship, the home edge, and the network. Kroger owns the catalog, the price, and the fulfillment. Deloitte builds and operates the agentic-AI layer that stitches them together — sold as a **cross-pack APEX engagement** combining a new **Telco-Customer Pack (TCP)** with the existing **CFMP**, bound by a cross-pack scenario chain over the APEX framework.

The pitch to AT&T: ARPU expansion + churn reduction + new commerce revenue share, with Deloitte's CFMP demo already proving the merchandiser side runs today.

---

## 2. The three actors and what each gets

| Actor | What they own | What they get | Who they pay |
|---|---|---|---|
| **AT&T** (Telco) | Network · home edge devices · household identity · customer relationship | Subscription revenue ($25-40/mo · "Home Concierge" tier) · commerce revenue share with Kroger · 5G/fiber stickiness · churn reduction | Deloitte (build + operate) · Kroger (revenue share split) |
| **Kroger** (Merchandiser) | Catalog · pricing · fulfillment · loyalty program | Incremental basket from auto-replenishment (+8-15% household frequency) · ~zero cart-abandonment in this channel · loyalty deepening · POS data feedback loop | Deloitte (CFMP-side integration) · revenue share to AT&T |
| **Household** (Customer) | Their kitchen · their voice · their consent | Don't run out of staples · save 30+ min/week on shopping · privacy mode they actually control | AT&T (subscription) |

Deloitte sells **two engagements** that compose into one solution:
- **AT&T-side**: TCP Pack Standard ($1-2M, 12-16w) — sold to CIO/Chief Digital Officer of AT&T Mobility
- **Kroger-side**: CFMP Pack Standard ($750K-$1.5M, 12-16w) — sold to CMO/CX-VP of Kroger Digital
- **Cross-pack scenario chain bundle** ($250-400K, 4-6w) — the wire-up that makes the two halves actually talk

Total Deloitte engagement: **$2-4M Wave-1**, run-rate Operate (T5) thereafter.

---

## 3. Where this fits in APEX

Per APEX-Architecture-v5 §10 (Scenario Chains) and APEX-Design-v3 S18 (cross-pack composability), this is a **cross-pack scenario chain** with `imports:` spanning two Industry Solution Packs. Per S23 (Multi-Cloud Pattern), it's a **Primary + Satellite** topology — one LEDGER, one audit chain across two corporate clouds.

```
   ┌────────────────────────────────────────────────────────────────┐
   │  APEX FRAMEWORK (cloud-neutral Core: VV runtime · LEDGER ·     │
   │  6-Agent Fleet · MCP contracts · 14-interface profile spec)    │
   └────────────────────────────────────────────────────────────────┘
                │                                  │
                ▼                                  ▼
   ┌──────────────────────────────┐    ┌──────────────────────────────┐
   │  Telco-Customer Pack (TCP)   │    │  CFMP (Customer-Focused      │
   │  NEW — 8th industry pack     │    │  Merchandise Pack)           │
   │                              │    │                              │
   │  Buyer: Telco CIO/CDO        │    │  Buyer: Merchandiser CMO/CX  │
   │  Schemas: TCML + CXML        │    │  Schemas: MERML + CXML       │
   │  Persona: household          │    │  Persona: customer           │
   │  HITL: sonos_voice +         │    │  HITL: customer_phone +      │
   │        home_kiosk            │    │        customer_phone        │
   │                              │    │                              │
   │  Lives on APEX-M primary     │    │  Lives on APEX-A satellite   │
   │  (AT&T's Azure footprint)    │    │  (Kroger's AWS estate)       │
   └──────────────┬───────────────┘    └──────────────┬───────────────┘
                  │                                   │
                  └─────────── imports: ──────────────┘
                              cross-pack scenario chain
                              chc-replenishment-cycle
                              chc-need-detection
                              chc-pickup-coordination
                              chc-substitution-flow
                              chc-loyalty-fusion
```

**Cloud topology decision**: AT&T is Primary (LEDGER + agents + most of TCP runs on APEX-M); Kroger is Satellite (catalog + price + inventory queries served through Interface #12 federation adapter; no LEDGER on Kroger side). One unbroken hash chain across both corporate clouds.

**Why AT&T as Primary**: customer-identity binding, consent gating, and the home edge all live on AT&T's network. Kroger is a fulfillment partner whose data flows in via federated reads on demand.

---

## 4. The new bits APEX needs (Foundation enhancements)

These are not CHC-only costs — every one of them unlocks future Connected-Home plays (Verizon × Walmart, T-Mobile × Target, Comcast × Wegmans). ARB-flag-worthy.

### 4.1 New persona type: `household` (extends `customer` from CFMP v0.2 §6.1)

```yaml
- id: household
  identity_binding:
    source: telco_account_id           # AT&T account → household
    members:
      source: opt_in_voice_enrollment  # Sonos voice-print per resident
      consent_gate: per_member         # every adult must consent
  channel_priority:
    - sonos_voice
    - home_kiosk
    - customer_phone   # fallback when out-of-home
  privacy_floor: hard_in_home          # see §7
```

The household is a *first-class persona*, not a bag of customers. Decisions ("auto-order milk") are made by the household; nudges and HITL prompts route through whichever channel a household member is closest to.

### 4.2 New HITL surfaces (sibling to `customer_phone` from CFMP §6.2)

| Surface | Implementation (APEX-M) | When it fires |
|---|---|---|
| `sonos_voice` | Sonos Cloud API push → "Ava" voice prompt + voice-print intent capture | Ambient — household member is near a speaker |
| `home_kiosk` | Adaptive Card → kitchen tablet (BLE-paired to household account) | Visual decisions — substitutions, pickup-window selection |
| `customer_phone` | (existing — Azure Notification Hubs) | Out-of-home fallback |

All three land identical Adaptive Card JSON. The transport differs; the contract doesn't. Per APEX-Design-v3 S12 (Persona model), this is a profile-implementation detail — pack manifests reference `channel: household_default` and the cloud profile resolves.

### 4.3 New customer-journey phase: `NEED` (pre-CHOOSE)

CFMP v0.2 §2 defined the customer journey as CHOOSE → SELECT → BUY → SERVICES. CHC adds a **NEED** phase before CHOOSE — the household doesn't shop, the household *runs low*. The agentic detection of need is the trigger.

| Phase | Question | Pack capability | Primary device |
|---|---|---|---|
| **NEED** (NEW) | "What are we running out of?" | Pantry/fridge inventory inference · consumption pattern learning · staple replenishment scheduling | In-home cameras + Sonos + kiosk |
| CHOOSE | "What should we get?" | (CFMP existing) | Sonos + kiosk |
| SELECT | "Where & when?" | Pickup window vs delivery · substitution acceptance | Kiosk + phone |
| BUY | "Confirm?" | Voice/touch confirmation · consent re-affirm | Sonos + kiosk |
| SERVICES | "How did it go?" | Delivery feedback · substitution NPS · loyalty | Phone + kiosk |

### 4.4 New schemas

| Schema | Namespace | Purpose |
|---|---|---|
| `TCML.HouseholdProfile` | NEW namespace TCML | Telco-side household identity, member roster, channel preferences |
| `TCML.HomeDeviceInventory` | TCML | Cameras + speakers + kiosks paired to household |
| `TCML.ConsumptionEvent` | TCML | Per-product detected consumption (with privacy filter — see §7) |
| `TCML.ReplenishmentCart` | TCML | Pending auto-orders awaiting household confirmation |
| `CXML.VoicePrintConsent` (extend CXML) | shared | Per-member voice-print + consent + scope |

### 4.5 New interface (proposed #16): Home-Edge Device Plane

CFMP v0.2 §6.3 already proposed Interface #15 (Maps & Wayfinding). CHC proposes:

**Interface #16 — Home-Edge Device Plane** with cloud-profile implementations:

| Profile | Implementation |
|---|---|
| APEX-M | Azure IoT Hub + Device Provisioning Service + Azure Speech (Sonos via Cloud API bridge) + Defender for IoT |
| APEX-G | Cloud IoT (legacy migration to Pub/Sub) + Speech-to-Text + Sonos via same Cloud API |
| APEX-A | AWS IoT Core + Greengrass + Polly + Sonos via same Cloud API |

The agent code consumes the abstract interface; profile YAML wires the implementation. Sonos is cloud-neutral (it's a 3rd-party endpoint reached over the same Cloud API on every profile).

---

## 5. Reference architecture

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  HOUSEHOLD (AT&T home)                                              │
   │                                                                      │
   │   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐           │
   │   │ Vision AI    │   │ Sonos Era    │   │ Kitchen      │           │
   │   │ Dev Kit ×N   │   │ 100 ×N       │   │ Tablet       │           │
   │   │ (pantry,     │   │ (rooms)      │   │ (kiosk-mode) │           │
   │   │  fridge,     │   │              │   │              │           │
   │   │  countertop) │   │              │   │              │           │
   │   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘           │
   │          │                  │                  │                    │
   │          └──────────┬───────┴──────────┬───────┘                    │
   │                     │                  │                            │
   │                     ▼                  ▼                            │
   │         ┌────────────────────────────────────────┐                  │
   │         │  Beelink on-prem home edge server      │                  │
   │         │  (privacy-floor enforcement happens    │                  │
   │         │  HERE, before anything leaves house)   │                  │
   │         │  • Per-frame DLP scrub                 │                  │
   │         │  • Embeddings only · raw stays local   │                  │
   │         │  • Featurization (per S36)             │                  │
   │         └────────────────┬───────────────────────┘                  │
   └─────────────────────────│──────────────────────────────────────────┘
                             │  AT&T 5G / Fiber (Defender for IoT)
                             ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  APEX-M PRIMARY  (AT&T Azure tenant)                                │
   │                                                                      │
   │   ┌──────────────────────────────────────────────────────────────┐ │
   │   │  TCP — Telco-Customer Pack                                    │ │
   │   │  • TCML schemas · household persona · sonos_voice + kiosk HITL│ │
   │   │  • NEED-phase scenarios (consumption detection · replen sched)│ │
   │   │  • 6-Agent Fleet (Assess · Classify · Quantify · Approve ·   │ │
   │   │    Act · Evidence-Write) — same six                          │ │
   │   └──────────────────────────────────────────────────────────────┘ │
   │                                                                      │
   │   ┌──────────────────────────────────────────────────────────────┐ │
   │   │  LEDGER (14-field WORM hash chain) — single source of truth   │ │
   │   │  • Every consumption detect · every replen cart · every       │ │
   │   │    confirmation · every Kroger handoff lands a row            │ │
   │   │  • consent_hash per member captured at decision moment        │ │
   │   │  • cross-cloud reads ride Interface #12 federation adapter    │ │
   │   └──────────────────────────────────────────────────────────────┘ │
   └──────────────────────────────┬──────────────────────────────────────┘
                                  │
                                  │  signed-MCP federation (Interface #12)
                                  ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  APEX-A SATELLITE  (Kroger AWS tenant) — no LEDGER, data-plane only │
   │                                                                      │
   │   ┌──────────────────────────────────────────────────────────────┐ │
   │   │  CFMP — Customer Focused Merchandise Pack                     │ │
   │   │  • MERML catalog · price · planogram · inventory positions    │ │
   │   │  • Fulfillment APIs (delivery slots · BOPIS · substitution)   │ │
   │   │  • Loyalty (Kroger Plus) state — tokenized                    │ │
   │   │  • Returns surface them up via federated reads on demand      │ │
   │   └──────────────────────────────────────────────────────────────┘ │
   └─────────────────────────────────────────────────────────────────────┘
```

**One audit chain across two corporate clouds.** The hash chain stays intact because the LEDGER lives only on AT&T's APEX-M tenant; Kroger reads are federated but don't write rows. Per APEX-Design-v3 S23, this is the multi-cloud pattern operating exactly as designed.

---

## 6. Scenario shortlist (12 scenarios, NEED + bridge)

| # | Scenario ID | Phase | KPI | Pack | Devices |
|---|---|---|---|---|---|
| 1 | `chc-pantry-inventory-inference` | NEED | Staple-out events ≤1/wk | TCP | Camera + edge ML |
| 2 | `chc-consumption-pattern-learning` | NEED | Replen lead-time accuracy ±1 day | TCP | Camera + LEDGER history |
| 3 | `chc-low-stock-voice-prompt` | NEED→CHOOSE | Voice prompt → confirm conversion >70% | TCP | Sonos + kiosk |
| 4 | `chc-replenishment-cart-build` | CHOOSE | Auto-cart accept rate >60% | TCP + CFMP | Kiosk |
| 5 | `chc-substitution-acceptance` | SELECT | Sub-acceptance >55% (vs 35% baseline) | CFMP | Kiosk |
| 6 | `chc-pickup-window-optimization` | SELECT | Wasted-slot rate <5% | CFMP | Kiosk + phone |
| 7 | `chc-delivery-vs-pickup-routing` | SELECT | Right-channel choice +20pp | TCP + CFMP | Voice + kiosk |
| 8 | `chc-voice-confirmation-with-consent` | BUY | Consent-affirm friction <3s | TCP | Sonos |
| 9 | `chc-out-of-home-fallback` | BUY | Phone-fallback success >90% | TCP + CFMP | Phone |
| 10 | `chc-delivery-arrival-handoff` | SERVICES | Arrival-to-storage time ≤10min | TCP | Camera + voice |
| 11 | `chc-substitution-NPS-feedback` | SERVICES | NPS capture rate >80% | CFMP | Voice + kiosk |
| 12 | `chc-loyalty-fusion-attribution` ⭐ | SERVICES | Cross-channel loyalty attribution 100% | TCP + CFMP | LEDGER cross-cloud |

⭐ Featured cross-pack chain — the headline scenario in any pitch.

**Sub-tier mapping**:
- **Lite** = 3 scenarios (#1, #3, #4) — proves the cycle works
- **Standard** = 8 scenarios (#1-9, +12) — full NEED-to-BUY cycle
- **Enterprise** = all 12 — adds delivery handoff + NPS loop + cross-channel attribution

---

## 7. Privacy posture — "hard_in_home" mode

In-home cameras are an entirely different threat surface than shelf cameras. The privacy contract is the product's most important moat. Per APEX-Architecture-v5 §17 (Agent Intelligence — Constitution) and S34 (Constitution + Outcome Learning):

### 7.1 Hard rules (Constitution — block + escalate)

These rules live in `tcp/constitution.yaml` and cannot be overridden by any operator card or override path. Per S34, hard rules block the agent AND escalate.

1. **No raw frames leave the home** — only embeddings + canonical event JSON cross the AT&T NID. Raw frames stay on the Beelink for a configurable retention window (default 24h) then delete.
2. **No off-list inferences** — agents may only emit events for products on the household's pre-enrolled "this kitchen tracks these" list. Detecting a face, a guest, a private moment? Constitution-blocked: agent must return `inference_out_of_scope`, no LedgerRow with content.
3. **Per-member consent required** for voice-print enrollment. Children under 13 cannot be enrolled at all.
4. **"Privacy minute" voice command** — saying "Ava, privacy minute" pauses all cameras and Sonos mics for 60 minutes; the pause itself is logged but content during the pause is not captured.
5. **Quiet hours hard-floor** — no proactive voice prompts between 10pm and 7am local time, ever.
6. **No cross-household correlation** — even within a single AT&T tenant, household data is partitioned and the LEDGER's per-tenant filter is enforced at the query plane (per S25 Multi-tenancy).

### 7.2 LEDGER privacy fields (extend the 14-field row)

The standard LEDGER row gets three CHC-specific payload fields (in the `payload` hashed bag, so the row schema isn't versioned):

```
payload.consent_hash       sha256 of (member_id_tkn + scope + timestamp)
payload.privacy_mode       one of: standard · privacy_minute · quiet_hours
payload.raw_media_disposition  one of: discarded · home_retained_24h · home_retained_consent
```

Any DPO query reproduces decision-time consent state byte-identical via apex-replay (S13).

### 7.3 Customer-visible privacy controls (kiosk app)

- "Show me everything you've seen this week" — replays the canonical event stream
- "Forget X" — issues a tombstone row + Bronze purge for matching events
- "Pause [device]" — per-device pause with LEDGER row
- "Who's listening?" — list of voice-prints enrolled + consent date

The kiosk's privacy panel is mandatory in the Pack and ships as Asset #10 in the bundle.

---

## 8. Cross-pack scenario chain example: `chc-replenishment-cycle`

End-to-end, NEED-to-BUY, spanning TCP (AT&T) and CFMP (Kroger). This is the headline demo flow.

```yaml
scenario: chc-replenishment-cycle
name: Connected-home replenishment with cross-cloud handoff
namespace: TCML
industry_pack: tcp
services: [Agent_1, Agent_2, Agent_3, Agent_4, Agent_5, Agent_6]
personas: [household, sonos_voice, home_kiosk]

uses_views:
  - tcml.pantry_state                # TCP-side · APEX-M
  - tcml.consumption_pattern_7d      # TCP-side · APEX-M
  - tcml.household_channel_priority  # TCP-side · APEX-M

triggered_by:
  - view: tcml.pantry_state
    band: critical                   # any tracked staple at 0 detected qty

imports:                             # ← cross-pack ← per APEX-Design-v3 S18
  - pack: cfmp@1.x
    views:
      - merml.product_with_planogram_location
      - merml.delivery_slot_inventory
      - cxml.loyalty_state
    tools:
      - cfmp.add_to_cart
      - cfmp.reserve_delivery_slot
      - cfmp.confirm_order

steps:
  - { agent: Agent_1, action: assess_pantry_need, source: tcml.pantry_state }
  - { agent: Agent_2, action: classify_urgency_and_substitutions }
  - { agent: Agent_3, action: quantify_replen_qty, learn_from: tcml.consumption_pattern_7d }
  - { agent: Agent_4, action: build_household_card,
       transport: household_default,    # resolves to sonos_voice OR home_kiosk
       fallback: customer_phone }
  - { persona: household, decision: confirm_or_modify_cart }
  - { agent: Agent_5, action: dispatch_to_kroger,
       cross_pack_call: cfmp.confirm_order,
       federation_path: signed_mcp_via_interface_12 }
  - { agent: Agent_6, action: evidence_write,
       payload_extends: [consent_hash, privacy_mode, raw_media_disposition] }

sla:
  warn: 5_minutes
  critical: 30_minutes
```

Eight LedgerRows land in the AT&T-side chain during this flow. Kroger's side returns data but writes no rows; auditors trace the whole cycle from a single LEDGER. Per S23 + S7, the chain is unbroken.

---

## 9. Demo path — leveraging existing assets

The reason this engagement closes fast: **every device in the house is already scaffolded in the existing demo.**

| Device | Status in current demo |
|---|---|
| Vision AI Dev Kit (camera) | ✅ Working — task #1-25 series |
| Sonos Era 100 (speaker) | ✅ Scaffolded — task #31 |
| Tablet kiosk mode | ✅ Working — task #30 |
| Beelink on-prem edge server | ✅ Working — task #29 |
| Cloud orchestrator on Container Apps | ✅ Working — task #32 |
| Azure Speech (Ava Multilingual TTS) | ✅ Working — task #90 |
| pgvector catalog (800 products) | ✅ Working — task #51 |
| Cart + checkout flow | ✅ Working — task #71 |
| Proactive associate / cue agent | ✅ Working — task #72, #92 |
| Dietary prefs | ✅ Working — task #74 |
| CFMP pack design | ✅ v0.2 — task #75-84 |
| APEX wedge (LEDGER + Purview-shaped lineage) | ✅ Deployed — task #85 |
| Multi-provider toggle (gpt-5-mini default) | ✅ Working — task #69, #70 |

**What's net-new for CHC Lite (3-4 weeks of build):**
1. **NEED-phase agent tool**: pantry inventory inference from camera frames (Vision Dev Kit already does product detection; needs aggregation + state tracking)
2. **Sonos voice-prompt path**: Sonos Cloud API push + voice-print intent capture (Ava TTS already works; add Sonos endpoint + STT)
3. **TCML schemas + 3 VV manifests**: `tcml.pantry_state`, `tcml.consumption_pattern_7d`, `tcml.household_channel_priority`
4. **Constitution.yaml**: hard rules from §7.1 (1-2 days, declarative)
5. **Privacy panel on kiosk**: "show me everything" / "forget X" / "pause" UI (1 wk)
6. **Cross-pack federation adapter stub**: signed-MCP back to a mock Kroger surface (3 days)

The Sonos device just needs an IP set on the home network. The Beelink already runs the privacy-floor enforcement layer. The Vision Dev Kit already classifies products. **The novelty is the orchestration, not the devices.**

---

## 10. Commercial structure (independence-safe)

```
   ┌──────────┐      Subscription $25-40/mo
   │ HOUSEHOLD├──────────────────────────────┐
   └──────────┘                              │
                                             ▼
                                       ┌──────────┐
                                       │  AT&T    │
                                       └────┬─────┘
                                            │
                Revenue share              │ Commerce flow
                    ◄──────────────────────┤
                                            │
                                            ▼
                                       ┌──────────┐
                                       │ KROGER   │
                                       └──────────┘

   Deloitte engagement contracts:
   ┌───────────────────────────────────────────────────────┐
   │  AT&T pays Deloitte for TCP build + operate           │
   │  Kroger pays Deloitte for CFMP-side integration       │
   │  Both engagements ride APEX-M (independence: ISV      │
   │  Marketplace burndown + SI Teaming, never direct ECIF │
   │  from Microsoft per S21).                             │
   └───────────────────────────────────────────────────────┘
```

| Engagement | Buyer | Tier | Price band | Timeline | Funding |
|---|---|---|---|---|---|
| TCP Pack Lite | AT&T CIO/CDO | T2A | $200-300K | 4-6w | BVA + DCIF |
| CFMP Pack Lite (Kroger-side) | Kroger CMO/CX-VP | T2A | $150-250K | 4-6w | BVA + DCIF |
| Cross-pack scenario bundle | Joint (AT&T primary contract) | T3 | $250-400K | 4-6w | DCIF + ISV burndown |
| **Wave-1 total** | | | **$600K-$950K** | **6-8w concurrent** | |
| TCP Pack Standard | AT&T | T2B | $1.0-2.0M | 12-16w | DCIF + T&M |
| CFMP Pack Standard | Kroger | T2B | $750K-$1.5M | 12-16w | DCIF + T&M |
| **Wave-2 total** | | | **$1.75-3.5M** | **12-16w** | |
| TCP Operate | AT&T | T5 | $25-60K/mo | Continuous | Client direct |
| CFMP Operate | Kroger | T5 | $20-50K/mo | Continuous | Client direct |
| **Run-rate** | | | **$45-110K/mo** | | |

**3-year TCV target**: $8-15M across the two clients combined, with run-rate compounding from year 2.

---

## 11. Why this is the right second wedge after the CFMP demo

1. **The proof rig already exists in the home form-factor**, not just the store. Sonos + Vision Dev Kit + tablet on a Beelink IS the in-home demo today. We're not building a vision — we're packaging existing scaffolded assets.
2. **B2B2C is the architectural pattern of the next decade**. Telcos own the pipe; merchandisers own the catalog; APEX is the only framework that lets them compose without one absorbing the other.
3. **Cross-pack engagement is the framework's hardest demo**. Selling AT&T × Kroger end-to-end proves APEX scales beyond single-pack pilots — the strategic answer to "but is your framework actually general?"
4. **Foundation enhancements pay forward**. `household` persona, `sonos_voice`/`home_kiosk` HITL, NEED phase, Interface #16 — all reusable across Verizon × Walmart, T-Mobile × Target, Comcast × Wegmans, and into smart-home insurance plays, healthcare-at-home, etc.
5. **Independence-safe by construction**. AT&T isn't audited by Deloitte. Kroger isn't audited by Deloitte. Microsoft money rides ISV Marketplace + SI Teaming. The funding paths in S21 line up cleanly.

---

## 12. Open questions for the AT&T BVA workshop

1. **Whose camera firmware?** AT&T's existing home-security camera footprint (Digital Life heritage) vs net-new Vision-AI-class devices? Recommendation: net-new for replenishment-class cameras, integrate existing security cams for arrival-handoff scenarios only.
2. **Sonos vs Alexa vs Apple HomePod** as the voice surface primary? Recommendation: Sonos for Wave-1 (we have the scaffold and it's brand-neutral), Alexa/HomePod via plug-in adapter in Wave-2.
3. **Kroger Plus loyalty fusion** — does AT&T expose its account_id to Kroger, or stays double-blind via tokenized identity? Recommendation: tokenized always; the LEDGER's `consent_hash` is the join key.
4. **Edge device ownership** — AT&T-issued (better recurring revenue, harder unit economics) vs customer-purchased (lower ARPU, faster scale)? Recommendation: AT&T-issued under a 24-month subscription wrap, parallels their fiber CPE model.
5. **Which Kroger banner first?** Smith's? Fred Meyer? Mariano's? Recommendation: a single-banner pilot in a single DMA where AT&T fiber footprint + Kroger banner density coincide (Dallas-Fort Worth or Houston are the obvious candidates).

---

## 14. Variant B — B2C: Kroger direct-to-consumer

Same APEX engineering as Variant A, single-client engagement, single-cloud topology. Kroger sells "**Kroger Smart Pantry**" as a Kroger Plus Premium tier ($15-25/mo), with a hardware starter kit (Kroger-branded camera + Sonos integration + kitchen tablet) sold at near-cost ($149-199) or bundled into a 24-month subscription wrap.

### 14.1 Where this fits in APEX

This is **not a new pack** — it's a **`+home` overlay on CFMP** per the Pack Lifecycle / Overlay model (APEX-Design-v3 S24). Kroger's existing in-store CFMP scenarios (12 of the 18) keep running; the home overlay adds:

- The NEED-phase scenarios (1-3 from §6)
- The `household` persona variant with `kroger_loyalty_id` identity binding
- The `sonos_voice` + `home_kiosk` HITL surfaces
- The `hard_in_home` Constitution block

Per S24 overlay model, the home extension ships as `packs/cfmp/overlays/home/`; the base CFMP pack updates flow through without forking, and Kroger's home customizations stay reviewable.

```
   ┌────────────────────────────────────────────────────────────────────┐
   │  APEX-A PRIMARY  (Kroger AWS tenant)  — single-cloud topology      │
   │                                                                     │
   │   ┌─────────────────────────────────────────────────────────────┐ │
   │   │  CFMP base pack  (in-store scenarios — already deployed)    │ │
   │   │  + CFMP-home overlay  (NEED phase + home HITL + Constitution) │ │
   │   │                                                              │ │
   │   │  Schemas: MERML + CXML + CFMP.StoreMap (existing)           │ │
   │   │           + CXML.HouseholdProfile (new, lifted from TCML)   │ │
   │   │           + CXML.PantryState (new)                          │ │
   │   │           + CXML.ConsumptionEvent (new)                     │ │
   │   │                                                              │ │
   │   │  Persona: household  (identity_binding: kroger_loyalty_id)  │ │
   │   │  HITL: sonos_voice + home_kiosk + customer_phone            │ │
   │   │                                                              │ │
   │   │  LEDGER lives here — all rows on Kroger tenant               │ │
   │   └─────────────────────────────────────────────────────────────┘ │
   └────────────────────────────────────────────────────────────────────┘
```

No federation adapter needed (single cloud); no cross-pack `imports:`; LEDGER and audit chain stay on Kroger's APEX-A tenant.

### 14.2 What changes vs Variant A

| Dimension | Variant A — B2B2C | Variant B — B2C |
|---|---|---|
| **Buyer** | AT&T CIO/CDO + Kroger CMO/CX-VP (two enterprise sales) | Kroger CMO/CX-VP only (one) |
| **Customer subscription** | AT&T Home Concierge ($25-40/mo) | Kroger Plus Premium ($15-25/mo) |
| **Hardware delivery** | AT&T-issued CPE wrap, 24-month subscription | Kroger Plus Premium hardware kit ($149-199 at cost) or bundled |
| **Identity binding** | `telco_account_id` (AT&T billed account) | `kroger_loyalty_id` (Kroger Plus member) |
| **Privacy custodian** | AT&T — CPNI / §222 statutory regime | Kroger — CCPA / loyalty fiduciary + LEDGER attestation |
| **Pack structure** | TCP (new pack #8) + CFMP cross-pack `imports:` | CFMP base + `cfmp/overlays/home/` per S24 overlay model |
| **Cloud topology** | APEX-M primary + APEX-A satellite (cross-cloud per S23) | APEX-A primary only (single-cloud) |
| **LEDGER home** | AT&T tenant | Kroger tenant |
| **Independence** | Microsoft money via ISV / SI Teaming on AT&T side (audit-safe) | Microsoft money same path on Kroger side |
| **Network** | AT&T 5G/fiber w/ Defender for IoT | Consumer Wi-Fi (Kroger ships device with hardened firmware + Wi-Fi enrollment via Kroger Plus app) |
| **Voice prompts** | Same Sonos + Ava Multilingual TTS | Same (no change) |
| **Kiosk app** | AT&T Smart Home companion app | Kroger Plus app (extended w/ kiosk mode) |
| **Constitution.yaml** | `tcp/constitution.yaml` | `cfmp/overlays/home/constitution.yaml` (identical 6 hard rules) |
| **Speed to market** | Slower (two enterprise sales must align) | Faster (one client sale) |
| **Strategic value** | Foundation enhancements unlock all future Telco × Merch pairings | Foundation enhancements unlock all future Merch-direct home plays |

**Everything else is identical**: same 6-Agent Fleet, same NEED→CHOOSE→SELECT→BUY→SERVICES phases, same 12 scenarios, same `sonos_voice` / `home_kiosk` HITL surfaces, same privacy posture, same Constitution hard rules, same demo assets.

### 14.3 Scenario shortlist (B2C — same 12, mapped to Kroger's loyalty narrative)

The scenarios from §6 carry over unchanged. The KPI narrative shifts from "telco ARPU + churn" to "Kroger Plus deepening + basket frequency":

| Scenario | KPI re-targeted for Kroger | Loyalty-program tie-in |
|---|---|---|
| `chc-pantry-inventory-inference` | Staple-out events ≤1/wk | Kroger Plus Premium exclusive feature |
| `chc-consumption-pattern-learning` | Replen lead-time accuracy ±1 day | Personal "your kitchen knows you" narrative |
| `chc-low-stock-voice-prompt` | Voice → confirm >70% | "Ava, Kroger" wake-phrase routes to Kroger only |
| `chc-replenishment-cart-build` | Auto-cart accept rate >60% | Kroger Plus Premium price + member-exclusive promos auto-applied |
| `chc-substitution-acceptance` | Sub-acceptance >55% | Kroger-only catalog — no Amazon cross-sell |
| `chc-pickup-window-optimization` | Wasted-slot rate <5% | Kroger Delivery / Pickup native slots |
| `chc-delivery-vs-pickup-routing` | Right-channel +20pp | Kroger Plus delivery-free threshold optimization |
| `chc-voice-confirmation-with-consent` | Consent-affirm friction <3s | Voice-biometric per household member, Kroger-owned |
| `chc-out-of-home-fallback` | Phone-fallback >90% | Kroger Plus app push |
| `chc-delivery-arrival-handoff` | Arrival-to-storage ≤10min | Doorstep handoff via Kroger driver |
| `chc-substitution-NPS-feedback` | NPS capture >80% | Kroger Plus loyalty point bonus for feedback |
| `chc-loyalty-fusion-attribution` ⭐ | Cross-channel attribution 100% | In-store + in-home + online all in one LEDGER |

⭐ Featured chain for Variant B is **`chc-loyalty-fusion-attribution`** — proves Kroger sees every household interaction across every channel in one place, which is the single most powerful CMO-side narrative.

### 14.4 Commercial structure (Variant B — Kroger direct)

```
   ┌──────────┐    Subscription $15-25/mo + hardware kit $149-199
   │ HOUSEHOLD├────────────────────────────────────────────────────┐
   └──────────┘                                                    │
                                                                   ▼
                                                            ┌──────────┐
                                                            │  KROGER  │
                                                            │ (direct) │
                                                            └────┬─────┘
                                                                 │
                                                                 │ pays Deloitte
                                                                 ▼
                                                            ┌──────────┐
                                                            │ DELOITTE │
                                                            └──────────┘
```

| Engagement | Tier | Price band | Timeline | Funding |
|---|---|---|---|---|
| CFMP-home overlay Lite | T2A | $250-400K | 6-8w | BVA + DCIF |
| CFMP-home overlay Standard | T2B | $1.0-1.8M | 14-18w | DCIF + T&M + ISV burndown |
| CFMP-home overlay Enterprise | T2C | $2.0-3.5M | 8-10mo | Client direct + T&M |
| Cross-channel scenario chains (in-store + in-home fusion) | T3 | $250-400K | 4-6w | DCIF |
| CFMP-home Operate | T5 | $25-50K/mo | Continuous | Client direct |

**Wave-1 entry**: $250-400K Lite, single client, single cloud, no federation work needed. The fastest path to a live in-home demo at a real retailer.

**3-year Variant-B TCV per client**: $4-8M with Operate compounding.

### 14.5 Why Variant B closes even faster than Variant A

1. **One enterprise sale**, not two. The B2B2C model requires AT&T's CIO and Kroger's CMO to align on timeline, identity-binding, and revenue share — every additional buyer doubles the cycle time.
2. **Single cloud**. No Interface #12 federation adapter, no Primary+Satellite topology, no cross-cloud audit chain validation. Lower architectural risk.
3. **Kroger already runs the demo**. The 800-product pgvector catalog + CFMP wedge work is already on Kroger-shaped data. Lifting it into a home form factor is a 4-week port.
4. **No new persona type if we're loose about it**. The `customer` persona from CFMP v0.2 §6.1 can be extended in-place to a household via the loyalty-account model Kroger already runs (household-of-loyalty-account is a tested concept at Kroger).
5. **Loyalty-program leverage**. Kroger Plus has 60M+ members. A Premium tier launch can be marketed to existing trusted customers without paid acquisition.

### 14.6 Why Variant A still matters even if Variant B closes first

Even if Kroger goes direct, the Telco-mediated story is the **defensible Alexa-replacement** — strongest privacy posture, neutral merchant layer, statutory custodianship. Most large retailers will eventually want the telco-fronted version as the "premium privacy" tier of the same service. The two variants co-exist commercially.

A Kroger executive's likely view: "We'll launch B2C direct to capture the basket. We'll also partner with AT&T on a Variant-A pilot for the privacy-sensitive segment (households with children, high-net-worth, regulatory-exposed)."

---

## 15. The B2C Pack Lite wedge (parallel to the CFMP-Pack-Lite wedge)

Mirrors `CFMP-Pack-Lite-Wedge-for-DMTSP-Sellers.md` but home-extended:

| | |
|---|---|
| **Pack** | CFMP + `cfmp/overlays/home/` (overlay per S24) |
| **Sub-tier** | Pack Lite (T2A) |
| **Buyer** | Kroger CMO · CX-VP · Chief Digital Officer (Kroger Digital lead) |
| **Price band** | **$250-400K** fixed fee |
| **Timeline** | **6-8 weeks** |
| **Funding** | BVA + DCIF primary; ISV Marketplace burndown secondary |
| **Persona** | `household` w/ `kroger_loyalty_id` binding |
| **HITL** | `sonos_voice` + `home_kiosk` + `customer_phone` fallback |
| **Proof asset** | The same demo at `https://ca-visionkit-portal...` — now lifted into a kitchen form factor |

**Three scenarios live in Lite** (same as Variant A's Lite shortlist):
1. `chc-pantry-inventory-inference` (NEED)
2. `chc-low-stock-voice-prompt` (NEED→CHOOSE)
3. `chc-replenishment-cart-build` (CHOOSE, with Kroger catalog)

**Engineering gap for Lite**:
1. Lift pantry/fridge state inference from current demo (2 wks)
2. Sonos Cloud API + Ava TTS prompt path (3 days)
3. Kroger Plus app kiosk-mode UI extension (1 wk — collaborate with Kroger app team)
4. `cfmp/overlays/home/` overlay manifests (3 days, declarative)
5. `cfmp/overlays/home/constitution.yaml` — 6 hard rules from §7.1 (1 day)
6. Kiosk privacy panel ("show me everything you've seen this week" / "forget X" / "pause [device]") (1 wk)

Total: **~5 weeks dev + 2 weeks customer pilot in 5,000 households**.

---

## 16. Open questions for the Kroger BVA workshop (Variant B)

1. **Hardware ownership** — Kroger-issued sold at cost (better unit economics, slower adoption) vs Kroger-Plus-Premium-included (faster adoption, subsidized hardware cost in subscription)? Recommendation: hybrid — included with 24-month Premium commitment, $149 standalone.
2. **Where does the wake-phrase route?** "Ava" exclusive to Kroger (clear branding), or "Kroger" only (no Alexa-trademark collision risk)? Recommendation: dedicated wake-phrase `"Hey Kroger"` — clear, no Amazon overlap.
3. **Substitution defaults** — does the household pre-approve "any Kroger brand substitution in the same category," or does each substitution require voice/touch confirm? Recommendation: pre-approval with per-category granularity in kiosk settings; voice confirm only for first-time subs.
4. **Cross-channel attribution depth** — does Variant B share LEDGER rows with Kroger's in-store CFMP deployment, or stays in a separate LEDGER on the same tenant? Recommendation: same LEDGER (one tenant), namespace partitioned by view_id pattern; this enables the loyalty-fusion attribution scenario.
5. **Children-in-household policy** — Kroger has no statutory equivalent to telco CPNI; how do we earn the same trust? Recommendation: third-party privacy attestation (e.g., TrustArc or BBB OnLine) plus a publicly published `constitution.yaml` so the privacy contract is inspectable.
6. **Migration path to Variant A** — if AT&T later wants to wrap Kroger's home service, does the household keep their data? Recommendation: yes — LEDGER export per household via apex-replay, signed by Kroger, reattested by AT&T on import. The portability story is itself a privacy moat.

---

## 17. Why pursuing both variants in parallel is the right play

| | Variant A speed | Variant B speed | Joint speed |
|---|---|---|---|
| Wave-1 close to live demo | 14-18 weeks (two clients aligning) | 6-8 weeks (one client) | 6-8 weeks via Variant B |
| Foundation enhancements complete | After Variant A Wave-1 | After Variant B Wave-1 | After whichever closes first |
| 3-year TCV ceiling | $8-15M per pairing | $4-8M per merchandiser | $20-30M with both running |
| Alexa-replacement narrative strength | Strongest (CPNI + neutrality) | Medium (loyalty + LEDGER) | Strongest (both stories told together) |
| Net-new APEX foundation work | New pack (TCP) + Interface #16 + cross-pack chain | Overlay only + Interface #16 | All of it (paid for twice in dependencies, but mostly one-time across both) |

The foundation enhancements pay for themselves whichever variant closes first. The B2C variant lights up the demo at a real retailer fast, gives Variant A's eventual close a working reference, and the joint narrative (privacy-first telco-mediated PLUS loyalty-deepening merch-direct) is what makes APEX-CHC the **category leader against Alexa** rather than just another voice-commerce experiment.

**The recommendation**: pursue Variant B with Kroger NOW (4-6 weeks to live demo, $250-400K BVA), use it as the proof rig in the AT&T pitch, close Variant A in parallel over the next 6-12 months.

---

## 13. Related artifacts

- **Working demo** (CFMP side): `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io`
- **CFMP v0.2 design**: `C:\Stage\Clients\Industries\APEX\docs\packs\CFMP-v0.2.md`
- **CFMP Pack Lite wedge** (predecessor doc): `C:\Stage\Clients\Industries\APEX\docs\reference\CFMP-Pack-Lite-Wedge-for-DMTSP-Sellers.md`
- **APEX teaching deck**: `C:\Users\kmarkham\Downloads\APEX-Design-v3.pptx` — key slides for this engagement: S14 (10-asset bundle), S15 (pack roadmap — CHC adds TCP as #8), S18 (cross-pack scenario chains with `imports:`), S22 (interface contract — propose #16), S23 (Multi-Cloud Primary+Satellite), S31 (burst flight-recorder), S33 (Memory + Calibration), S34 (Constitution + Outcome Learning), S36 (Multimodal Featurization)
- **Architecture v5**: `C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Architecture-v5.docx` — §6 Cloud Profile Contract (propose Interface #16), §10 Scenario Chains (cross-pack imports), §11 Service Envelopes (Tier-3 cross-pack bundle), §17 Agent Intelligence (Constitution)

---

*Internal · Deloitte Microsoft Technology & Services Practice · Prepared by Keven Markham, VP · 2026-05-23*
