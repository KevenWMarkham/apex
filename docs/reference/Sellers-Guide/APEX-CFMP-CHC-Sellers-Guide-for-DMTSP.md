# APEX · CFMP · CHC — Sellers Guide for DMTSP

**A field reference for taking the agentic-commerce conversation into the client meeting.**
Read cover-to-cover once. Reference any section live in 30 seconds.

| | |
|---|---|
| **Audience** | DMTSP sellers, LCSPs, engagement leads taking CFMP or CHC into a client conversation |
| **Scope** | APEX as the framework · CFMP (in-store, customer-side) · CHC (in-home, two variants) · Alexa-replacement positioning |
| **Date** | 2026-05-23 |
| **Owner** | Keven Markham, VP — Deloitte's Microsoft Practice |

---

## 1. Master frame — what you're selling

### You ARE selling:
**A scoped Deloitte agentic-AI delivery engagement on the APEX framework, sold per industry under standard Service Envelope tiers.** The buyer pays Deloitte for engineering + ongoing operate; the framework itself is the IP that makes the engagement repeatable, auditable, and sellable.

### You are NOT selling:
- **A product** — APEX is a delivery framework. CFMP is a scoped engagement. CHC is a cross-pack engagement.
- **A Microsoft co-sell** — Deloitte sells; Microsoft money rides ISV Marketplace / SI Teaming. Never direct ECIF to Deloitte.
- **A platform license** — there is no license SKU. Clients buy delivery services that include the framework, manifests, and Operate run-rate.
- **A custom build** — first-time clients buy the catalog Pack with their overlay, not a bespoke greenfield build.

### The one-sentence positioning
> "Deloitte delivers your in-store and in-home agentic-commerce capability as a scoped engagement on APEX — our cloud-neutral delivery framework that ships the canonical playbook, the 14-field WORM ledger, the privacy constitution, and the operate run-rate. Microsoft Foundry, Azure OpenAI, and Azure Maps run underneath. The agent that talks to your customer is delivered by Deloitte."

---

## 2. The five pitches

Each pitch is a deeper layer of the same story. Use the shortest version that earns you the next conversation.

### 2.1 The 30-second pitch (elevator, single-person hallway, LinkedIn DM)

> "Amazon Alexa routes 70 million American households' grocery baskets straight to Amazon Fresh by default — bypassing every other merchandiser. We've built the regulated, privacy-first alternative on Microsoft's stack: cameras, speakers, and a kitchen tablet that detect what you're running out of and auto-order from your preferred retailer — not Amazon's. It's running on a laptop today. Have you got 15 minutes to see it?"

### 2.2 The 60-second pitch (intro on a discovery call)

> "Deloitte has built an agentic-commerce delivery framework called APEX. We've shipped a working merchandise demo on Microsoft Foundry — eight hundred SKUs in a vector catalog, voice-driven shopping with Azure Speech, a fourteen-field cryptographic audit trail on every nudge, and a customer journey from 'what should I buy' through pickup and substitution. We've extended it into the home: cameras and Sonos in the kitchen, a tablet kiosk on the counter, and a privacy regime tougher than Alexa by construction. We sell it as a scoped engagement to your team — first a BVA workshop, then a four-to-six-week Pack Lite live with three scenarios in your stores, then a path to your loyalty base across the whole journey. The demo runs in a browser. Want me to share my screen?"

### 2.3 The 5-minute pitch (slot opened up in a meeting, no demo yet)

Cover these five beats in order — about a minute each:

1. **The problem**: Alexa-mediated commerce. 70M households, every basket routes to Amazon by default. Merchandisers either pay Amazon to be a Skill or get disintermediated. Telcos own the pipe and watch the ARPU bypass them.
2. **The thesis**: A regulated, privacy-first alternative exists when the agent is delivered by an integrator (Deloitte) on a delivery framework (APEX), with a custodian who isn't a merchant (telco) or a fiduciary loyalty-program (Kroger Plus, Walmart+).
3. **The technical answer**: APEX is cloud-neutral; runs on Foundry today, also on Vertex, also on Bedrock. Industry Solution Packs are 10-asset bundles. Every customer-facing action lands a hash-chained LedgerRow with the consent state at decision moment. Auditors and DPOs query in seconds.
4. **The proof**: working demo on Microsoft Foundry with gpt-5-mini agents, Azure Speech, Azure Maps Creator wayfinding, 800-product pgvector catalog, Vision AI Dev Kit cameras feeding the Bronze layer through the Featurization Layer. Running today.
5. **The ask**: a 4-hour BVA workshop with your CMO/CX team to shortlist 3-5 scenarios for a Pack Lite engagement. $100K-$400K depending on scope. Funded as BVA + DCIF. Microsoft money rides ISV Marketplace separately.

End with: "What's the right next conversation? Is it your CMO, your DPO, or your cloud architect?"

### 2.4 The 15-minute pitch (the demo)

See §6 Demo Script. Open the portal, narrate seven chapters, end on the architecture page. The demo IS the pitch from minute 5 onward.

### 2.5 The 45-minute briefing (CMO + CDO + CIO in the room)

Use the v5 DMTSP deck (`APEX-Walkthrough-Deck-for-DMTSP-Sellers-v5.pptx`). 15 slides; pace it about three minutes per. Demo opens at slide 8 and runs for 10 minutes. Land §11 commercial sequencing as your close.

---

## 3. Talk tracks by buyer persona

Same framework, different language. Lead with the buyer's pain, not your framework.

### 3.1 The Chief Marketing Officer / VP-CX (Merchandiser side)

**Their pain**: trip conversion is flat, basket size is plateauing, NPS is exposed to substitutions and out-of-stocks, Amazon Fresh is taking share they can't see.

**Your line**:
> "You're funding loyalty programs to deepen households you already know. We add the agentic layer that detects when a household is running out, suggests replenishment in their voice, and routes the basket to YOU — not Alexa. Every nudge is consent-gated, logged, and provable to your DPO. Three scenarios live in 4-6 weeks for $150-250K under a BVA."

**What they'll ask**: "Trip conversion lift?" "Basket-size lift?" "What about my DPO?" "Where's the ROI?"

**Your answer pattern**: cite CFMP v0.2 §9 Pack-Level KPIs (trip conversion +14%, basket size +8%, NPS +9pt, loyalty churn -22%). Cite the working demo. Don't invent numbers — anchor every claim to the demo or the published design.

### 3.2 The Chief Information Officer / CDO (Telco side)

**Their pain**: ARPU growth is hard, churn is steady at 1.2-1.5% monthly, the 5G consumer narrative needs services to ride on, every voice query in the home routes to Amazon and bypasses them.

**Your line**:
> "Your customers' baskets are routing through Alexa to Amazon today. CPNI says you have a statutory privacy custodianship over communications data that Amazon literally cannot match. We add the home-commerce agentic layer to your fiber/5G subscription as 'Home Concierge' — $25-40/mo per household, revenue share with the merchandiser, and your CPNI obligation becomes a competitive advantage. The proof rig runs in our lab today."

**What they'll ask**: "What about my Defender for IoT footprint?" "What's the CPNI burden vs benefit?" "What does this do to my fiber retention?"

**Your answer pattern**: cite CHC v0.2 §0 Alexa-replacement table. Cite Interface #16 proposed in §4.5 — your home-edge plane is the proposed APEX framework interface that runs Azure IoT Hub natively on APEX-M. Cite the 3-year sequencing in §0.

### 3.3 The Chief Digital Officer / Head of Loyalty (either side)

**Their pain**: loyalty program is mature but engagement is plateauing. The next vector is making the program *useful in the moment*, not just at the register.

**Your line**:
> "Your loyalty database is the most valuable thing you own. We turn it into an active relationship — the agent knows the household, learns the cadence, and shows up when they need you. Voice + camera + tablet. Same Kroger Plus identity, same trust, but now your loyalty program runs in the kitchen, not just at checkout."

### 3.4 The Chief Privacy Officer / Data Protection Officer

**Their pain**: every new commerce surface is a privacy headache; in-home cameras 100x. They're already nervous about Alexa precedent (FTC 2023 settlement, COPPA). They need a story they can defend to regulators, board, and customers.

**Your line**:
> "We didn't bolt privacy on. The framework's runtime is the privacy contract. Every customer-facing action lands a hash-chained ledger row with the consent state at decision moment. Constitutional hard rules block off-list inferences at the runtime layer — not as policy, as code. Raw frames never leave the household. The DPO query 'show me how this decision was made' returns cryptographic proof in seconds via apex-replay. Want to see it?"

This is the buyer who closes deals. Spend extra time here.

**What they'll ask**: "How do you handle children?" "What about a privacy-minute?" "Who's the custodian?" "What about a subpoena?" "GDPR data-subject access request?"

**Your answer pattern**: open CHC v0.2 §7 "hard_in_home mode" and walk the six Constitution hard rules. Show the LEDGER schema with `consent_hash`, `privacy_mode`, `raw_media_disposition`. Show apex-replay reproducing a decision byte-identical.

### 3.5 The Chief Information Security Officer

**Their pain**: edge devices are exposure; cloud connectivity is exposure; agentic systems making decisions are exposure. They want compartmentalization, attestation, and a clear breach-domain story.

**Your line**:
> "The home edge runs a Beelink mini-server doing on-prem privacy enforcement before anything leaves the house. Defender for IoT on the network. Sonos and Vision Dev Kit are managed via Azure IoT Hub with Device Provisioning Service. Tenant-isolated by construction; cross-tenant correlation is constitutionally blocked. Apex-replay gives you forensic evidence on every decision. Your incident response gets a 14-field row, not a vendor support ticket."

### 3.6 The IT Architect / Cloud Lead

**Their pain**: another framework. They've heard "platform" pitches before. They want to know how it composes with what they already run.

**Your line**:
> "APEX has fourteen cloud-profile interfaces. Storage, identity, LLM, observability, lineage — your existing investments slot in. CFMP runs on whichever cloud profile you choose; in your case that's Microsoft. No lift-and-shift. The pack manifests touch only the abstract interface — moving you to a different cloud profile later is a config change, not a re-platform."

### 3.7 Procurement / Sourcing

**Their pain**: scope, change orders, lock-in.

**Your line**:
> "Three fixed sub-tiers per Pack: Lite, Standard, Enterprise — additive only. No client ever re-platforms moving up. BVA-funded workshop earns the Lite SOW; Lite SOW earns Standard. Independence-safe funding paths are pre-mapped: BVA, DCIF, ISV Marketplace burndown, SI Teaming, T&M, client direct. We don't take ECIF directly from Microsoft."

---

## 4. Discovery playbook — qualifying questions

You need three pieces of information before you can credibly propose anything: **who buys**, **what budget vehicle**, and **what scenario hurts most today**. Ask in this order:

### 4.1 Opening discovery (first 15 minutes of any meeting)

1. "Who in your organization owns the customer in-the-moment relationship? Marketing? CX? Digital?"
2. "What's the current state of your loyalty engagement metric? Where's it stuck?"
3. "How much of your basket is routing through voice channels today? Amazon, Google, Siri?"
4. "If we put a working demo on your laptop and walked your CMO through a 15-minute scenario, what would they care most about: trip conversion, basket size, NPS, or churn?"
5. "Is there budget for innovation pilots, or does everything route through capital planning?"

### 4.2 Qualifying questions (whether to invest in this pursuit)

| Signal | Strong | Weak |
|---|---|---|
| Buyer engagement | CMO + CDO both want a follow-up | Only IT wants the meeting |
| Privacy posture | Has a CPO, asks DPO-grade questions | "We'll worry about privacy later" |
| Cloud posture | Mature Azure footprint already | Predominantly on-prem or AWS-only |
| Loyalty maturity | 50M+ identified members, mobile app | Anonymous-mostly, no loyalty data |
| Vision posture | Has explored agentic AI but hasn't committed | "We're still on rule-based chatbots" |
| Procurement | Has a BVA budget envelope or DCIF appetite | All spend goes through full procurement |

3 strongs of 6 = pursue. 4+ = lead pursuit. 2 or below = qualify out or pivot to a different opener.

### 4.3 Sizing questions (before proposing pricing)

- "What's the right banner / business unit / region for a pilot?"
- "What does success look like in 90 days?"
- "Do you fund pilots from operating budget or innovation budget?"
- "Is there an existing Microsoft ELA or ISV commitment we should know about?"

### 4.4 Red-flag questions (qualify out)

- "Can you just give us the framework code and we'll run it ourselves?" → **No.** APEX is delivered, not licensed. Politely explain.
- "Can Microsoft fund this directly?" → **No.** Independence rule. Microsoft money via ISV Marketplace + SI Teaming only.
- "What's the lowest-priced way to get started?" → They're shopping commodity. Re-anchor on the BVA workshop value, not price.
- "Can you have something live next week?" → Set expectations. 4-week Lite minimum. Faster = irresponsible.

---

## 5. Whiteboard moves

Five framings you should be able to draw on a wall in under 60 seconds. Each lands a different beat of the story.

### 5.1 The Alexa-replacement contrast

```
   ALEXA  (Amazon)              vs               APEX  (Deloitte / framework)
   ─────────────────────                          ─────────────────────────
   Commercial provider                            Telco (CPNI) or Merch (LEDGER)
   ToS-based recourse                             Statutory privacy regime
   Skill-mediated commerce (Amazon cut)           Pack-mediated, no platform tax
   "Mute" button (advisory)                       hard_in_home mode (enforced)
   Single cloud (AWS)                             Cloud-neutral (M/G/A)
   No audit trail disclosed                       14-field WORM hash chain
```

Draw on the wall when the buyer says "isn't this just Alexa with a Deloitte logo?"

### 5.2 The 5-layer APEX pancake

```
   ┌─────────────────────────────────────────────────┐
   │  SCENARIO CHAINS    (named business outcomes)   │
   ├─────────────────────────────────────────────────┤
   │  VIRTUAL VIEWS      (sensing-to-resolution)     │
   ├─────────────────────────────────────────────────┤
   │  6-AGENT FLEET      (Assess→Class→...→Evidence) │
   ├─────────────────────────────────────────────────┤
   │  LEDGER             (14-field WORM hash chain)  │
   ├─────────────────────────────────────────────────┤
   │  CLOUD PROFILE      (Microsoft / Google / AWS)  │
   └─────────────────────────────────────────────────┘
```

Use this when the buyer asks "what IS APEX." Each layer is a manifest, not code. Same six agents in every Pack. Same LEDGER on every cloud profile.

### 5.3 The customer journey spine (CFMP + CHC)

```
   NEED  →  CHOOSE  →  SELECT  →  BUY  →  SERVICES
   home    home      in-store     in-store  cross
   only    + store   + home       + home    channel
```

Use this to explain how the same Pack scales from in-store (CFMP base) to in-home (CHC overlay) to cross-channel attribution.

### 5.4 The two-variant comparison

```
                 VARIANT A (B2B2C)         VARIANT B (B2C)
                 AT&T × Kroger             Kroger direct
                 ────────────              ────────────
   Buyer         CIO + CMO                 CMO
   Privacy       CPNI statutory            LEDGER + loyalty fiduciary
   Cloud         M primary + A satellite   A primary only
   Pack          TCP + CFMP cross-pack     CFMP + home overlay
   Wave-1        $600-950K, 6-8w           $250-400K, 6-8w
   Speed         Slower (2 clients)        Faster (1 client)
   Alexa-kill    Strongest                 Medium
```

Use this when the buyer wants to know whether to go alone or partner with a telco.

### 5.5 The service envelope ladder

```
   T5  OPERATE      $/month subscription   (run-rate)
   T4  CUSTOM       T&M, sprints           (bespoke)
   T3  SCENARIO     $150-400K, 4-8w        (one outcome)
   T2  PACK LITE    $100K-3.5M, 4w-9mo    (Lite/Std/Ent)
   T1  FOUNDATION   $400-700K, 6-10w       (sold once)
```

Use this when the buyer says "how do I sequence this across two fiscal years?"

---

## 6. Demo script — chapter by chapter

The demo runs at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io`. Total time: 15 minutes from "let me share my screen" to "what questions do you have?"

### Chapter 1 (2 min) — "This is your shopper, holding a phone, in your store today."

Open the portal. Show the camera feed with live person + product detection. Drop your barcode-product on the table. Watch the agent identify, look up, and respond with a card.

**Narration**: "What you're seeing is a customer's phone view. The shelf cameras detect them, our agent identifies what they're holding, and answers in their voice. Eight hundred SKUs in your catalog. Three agents running concurrently."

### Chapter 2 (2 min) — "Now watch what happens when they linger."

Stand near the cart for 90 seconds. The Proactive Associate fires a cue.

**Narration**: "This is what we call the cart-dwell-abandonment-rescue scenario. The agent saw the customer stopped, didn't pick up, and proactively offered a nudge. In a real store, this drives a 12% recovery rate on physical cart abandons that today are just lost revenue."

### Chapter 3 (2 min) — "Wayfinding through your store."

Ask "where's the cheese?" in the chat box.

**Narration**: "The agent just routed through Azure Maps Creator — Microsoft's indoor maps platform. Real CAD floor plan from a retailer, real wayfinding REST API, real route returned. Customer phone sees zone, aisle, distance. This is the SELECT phase of the customer journey."

### Chapter 4 (2 min) — "Add it to the cart. Watch what happens at $50."

Add steaks. Show the cart hitting $59.96. Open the Architecture page → LEDGER tail.

**Narration**: "Every cart action over $50 trips the HITL consent gate. A LedgerRow lands with `hitl_status: PENDING`. The customer's phone gets a consent prompt. Below the threshold, no prompt — but the row still lands. Every cart action, every nudge, every dietary filter, every checkout — all in the chain. Your DPO queries this; auditors query this. apex-replay reproduces byte-identical."

### Chapter 5 (2 min) — "Now imagine this in the kitchen."

Open the architecture page → Dependency Tree. Click into the CHC v0.2 section.

**Narration**: "Same engineering. Same agents. Same LEDGER. The Vision Dev Kit moves from the store ceiling to the pantry. Sonos picks up the voice. Tablet becomes the kiosk. The customer journey gets a new phase — NEED — before CHOOSE. The agent learns the household's cadence. Auto-orders replenishment with one voice confirmation."

### Chapter 6 (2 min) — "Here's the privacy contract."

Open the CHC §7 Constitution section in the docs.

**Narration**: "Six hard rules. Raw frames never leave the home. Off-list inferences blocked at the runtime layer. Per-member voice-print consent. 'Privacy minute' voice command. Hard quiet-hours floor. No cross-household correlation. These rules live in YAML, audited and reviewed by your DPO before deployment. They block at runtime — not as policy, as code."

### Chapter 7 (3 min) — "Here's how this becomes an engagement."

Open the Service Envelope diagram. Walk T1 Foundation → T2 Pack Lite → T2 Standard → T5 Operate. Quote prices. Show the funding paths.

**Narration**: "Three sub-tiers per Pack, additive only. Pack Lite is the BVA-funded entry — $150-400K depending on whether we go in-store, in-home, or both. Standard is the production push. Enterprise rolls it across your full footprint. Operate is the subscription that compounds. Microsoft money rides ISV Marketplace, never direct ECIF. We can sequence a 3-year story across your fiscal calendar."

End with: "What part would you like to dig into?"

---

## 7. Objection handbook — top 15 with handlers

### O1. "Isn't this just Alexa with a Deloitte logo?"
> "Alexa is a commercial provider with ToS-based recourse. We're delivering a regulated framework with statutory privacy custodianship — either via the telco's CPNI obligation or the merchandiser's loyalty fiduciary. Amazon doesn't compete with itself; we deliver an agent for YOU. Different category."

### O2. "We already have an Alexa Skill. Why this?"
> "Your Skill routes 30% commission to Amazon and competes against Amazon Fresh by default. Our agent runs on your stack, in your loyalty program, with no platform tax. You capture 100% of the basket and own the customer relationship."

### O3. "What's the framework lock-in?"
> "None. APEX runs on Microsoft, Google, or AWS — same Pack manifests, profile-specific implementations. Industry Solution Packs are 10-asset bundles delivered to you. The manifests are yours. The runtime is open architecture. Independent of Deloitte, the framework still works."

### O4. "Microsoft does this with Foundry directly."
> "Foundry is the agent runtime — and an excellent one. We use it as the LLM and orchestration substrate. APEX is the engagement layer above Foundry: methodology, canonical schemas, the LEDGER, industry packs, service envelopes. Foundry runs the runtime. We deliver the engagement."

### O5. "What about ChatGPT? OpenAI is doing this."
> "OpenAI is a model provider. We use their models — gpt-5-mini is the current default in the demo. The model is one of 14 cloud-profile interfaces. APEX is what wraps the model into a billable, audit-defensible, repeatable delivery."

### O6. "We don't want our customers' voice data going to OpenAI."
> "The Constitution and the 14-interface contract mean the model is a config swap. You can run on Azure OpenAI (Microsoft-tenanted), on Anthropic (Microsoft Foundry route), or on a model you self-host. The agents don't care. The customer-voice path can be Microsoft-only with no third-party retention."

### O7. "How long until we get to production?"
> "BVA workshop is 4 hours. Pack Lite is 4-6 weeks, live with three scenarios. Standard is 12-16 weeks. We can be live in three of your stores or 5,000 households within 90 days of BVA close."

### O8. "What's the actual ROI?"
> "Anchor on CFMP v0.2 §9: trip conversion +14%, basket size +8% units/trip, NPS +9pt, loyalty churn -22%, cart-abandon recovery +12%. These are pack-level KPIs your BVA workshop produces with your CFO's input. We don't promise lift in the SOW; we promise the engineering that proves it on your data."

### O9. "What about my children/family privacy?"
> "Children under 13 cannot be voice-enrolled. Constitutional hard rules block off-list inferences. Privacy-minute voice command pauses cameras and mics. Quiet-hours hard floor is enforced. Every household member individually consents to voice-print. We publish the constitution.yaml so it's inspectable. Third-party privacy attestation in production rollout."

### O10. "This sounds expensive."
> "It IS the right size of investment for the problem. BVA workshop is your filtration step — your CMO/CX team picks the three scenarios with the biggest internal champion and the cleanest ROI. The $150-400K Pack Lite then converts the workshop into a live engagement. You can stop after Lite, or you can continue. Most don't stop."

### O11. "What if we want to switch off Azure later?"
> "The Pack manifests touch only the 14-interface abstract contract. The cloud profile is a deployment YAML setting. Same Pack runs on Vertex, Bedrock, or wherever. Re-platforming a Pack is a config change, not a code migration. You don't get locked into Microsoft via this engagement."

### O12. "Deloitte is Microsoft's auditor. Aren't we breaking independence rules?"
> "We've engineered the funding paths to be independence-safe by construction. Microsoft money to us routes via ISV Marketplace burndown or SI Teaming with a non-competing SI. Deloitte never receives ECIF directly from Microsoft. SOWs reference Microsoft as 'cloud profile' or 'platform' — never 'partner' or 'alliance.' Our legal has cleared the pattern; we have language discipline."

### O13. "We don't have the data to do this."
> "The Pack ships with synthetic demo data, source adapters for common SOR systems (Oracle RMS, SAP IS-Retail, Manhattan, etc.), and a 60+ acceptance-test suite that proves Pack health in CI. We're delivering capability, not asking you to be data-perfect first."

### O14. "Sounds like a big change-management lift."
> "Pack Lite intentionally lands ONE scenario in production. Your CX team owns the persona definition and the SLA — we deliver the engineering. Sub-tier additivity means no rework when you scale up. We have a runbook + training asset in the 10-asset bundle that covers the operate hand-off."

### O15. "What if our scenarios don't fit your Pack?"
> "First — they usually do, because the Pack scenarios are derived from the canonical industry playbook. Second — if they don't, that's the T4 Custom Build tier: T&M sprints producing new VVs and scenarios that become permanent client-overlay assets. Your overlays survive Pack updates per the lifecycle model."

---

## 8. Commercial framing — pricing & sequencing

### 8.1 The price ladder (memorize)

| Tier | What it includes | Price | Timeline | Funding |
|---|---|---|---|---|
| BVA Workshop | 4-hour discovery + scenario shortlist + ROI worksheet | $0-50K (sometimes Deloitte-absorbed) | 1 day | Client or DCIF |
| T1 Foundation | One-time per tenant: VV runtime, LEDGER, MCP, Entra/Purview wiring | $400-700K | 6-10w | BVA + DCIF |
| **CFMP Pack Lite** | 3 scenarios live on client data | **$150-250K** | **4-6w** | **BVA + DCIF** |
| **CHC Pack Lite (B2C)** | CFMP + home overlay, 3 NEED scenarios live | **$250-400K** | **6-8w** | **BVA + DCIF** |
| CFMP Pack Standard | 1 sub-domain + 3-5 scenarios in production | $500K-$1.5M | 12-16w | DCIF + T&M + ISV burndown |
| CFMP Pack Enterprise | Full catalog + all scenarios + Operate-ready | $1.5-3.5M | 6-9mo | Client direct |
| Cross-pack scenario chain (Variant A) | TCP + CFMP wire-up | $250-400K | 4-6w | DCIF |
| T5 Operate | 24×7 monitor + tuning + Pack version uptake | $20-110K/mo | Continuous | Client direct |

### 8.2 The three opening sizes (memorize too)

- **Smallest credible**: BVA workshop ($0-50K) → CFMP Pack Lite ($150-250K). 5 weeks total.
- **Standard opener**: BVA → CFMP Pack Lite + CHC Pack Lite combined ($400-650K). 8 weeks. Includes home demo at one household.
- **Strategic opener**: BVA → CFMP Pack Standard ($750K-$1.5M). 14 weeks. Lands the Pack into production at one banner.

### 8.3 Funding-path matrix (from APEX-Design-v3 §S21)

| Vehicle | T1 Foundation | T2 Lite | T2 Std | T3 | T4 | T5 |
|---|---|---|---|---|---|---|
| BVA (client-funded) | ✓ | ✓ | | | | |
| DCIF (Deloitte co-invest) | ✓ | ✓ | ✓ | | | |
| ISV Marketplace burndown | | ✓ | ✓ | ✓ | | |
| SI Teaming POC | | | ✓ | ✓ | | |
| Client direct | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| T&M | | | ✓ | ✓ | ✓ | |

### 8.4 The 3-year arc one-liner

> "Year one: BVA + Pack Lite. Year two: Pack Standard + Operate hand-off. Year three: Enterprise rollout + cross-pack scenarios. Per-banner annual TCV ranges $1.5-4M; Operate compounds from year two."

---

## 9. Independence language discipline

This protects the firm. **Memorize the words to use and the words to never use.**

### NEVER say
- "Microsoft partner" / "Microsoft alliance" / "We partner with Microsoft"
- "Joint Microsoft commercial" / "Microsoft commits funding"
- "Microsoft pays Deloitte" / "Microsoft co-funds us"
- "ECIF" in client conversation (it's an internal Microsoft mechanism, not a client-visible term)
- "Microsoft GTM"

### Always say (the legal-safe equivalents)
- "Deloitte's Microsoft practice" / "DMTSP"
- "Microsoft technology" / "Microsoft platform" / "Cloud profile: Microsoft"
- "Microsoft incentive routes via Marketplace" (if technical context requires)
- "Independent of Microsoft" (when referring to Deloitte's role)
- "Microsoft-funded burndown via ISV Marketplace" (only with procurement in the room)

### The independence sentence (always available)
> "Deloitte is Microsoft's auditor. SEC rules forbid us receiving ECIF directly from Microsoft. We've engineered the funding paths around that constraint — Microsoft money flows via ISV Marketplace burndown or SI Teaming, never directly to Deloitte. Our language discipline reflects the rule."

### If pressed for more detail
> "We have a non-competing SI we team with for Microsoft-funded POCs. That SI receives ECIF; Deloitte delivers under sub. Our Architecture Council and legal have cleared the pattern. We can walk procurement through it if helpful."

---

## 10. The close — BVA workshop ask

Every client conversation should end with one of three asks. Pick the one that fits the temperature.

### 10.1 The standard close (warm meeting)
> "I'd like to set up a 4-hour BVA workshop with your CMO/CX team and our delivery lead. We'll come with the demo on a laptop, shortlist 3-5 scenarios with your team, and produce a Pack Lite SOW skeleton in the same session. Can your team commit half a day in the next two weeks?"

### 10.2 The technical close (architect in the room)
> "I'd like to arrange a one-day deep-dive with your cloud architects. We'll bring the framework documentation, walk the 14 interfaces against your existing investments, and produce a Pack Lite implementation plan. Open to that?"

### 10.3 The exec close (CMO/CIO in the room, time pressure)
> "If I send you the 15-page Pack Lite proposal Monday morning, can you commit to a BVA workshop in your team's calendar within two weeks?"

### What "yes" sounds like
- "Send the proposal." (warm)
- "Have your team contact mine." (warm but delegated)
- "Let me run this past my CFO." (warm but slow)
- "We're already evaluating something similar." (cold — try to learn what)
- "We'll get back to you." (lukewarm — follow-up in 5 days)

### What "no" sounds like
- "It's not the right time." (acknowledge, ask when IS the right time)
- "We've got it covered internally." (probe — what does internally look like)
- "Send me a one-pager." (it's a polite stall; send it but expect silence)

### Always follow up
Send the next-step email within 24 hours. Reference one specific thing they said. Attach the working-demo URL. Propose two concrete dates.

---

## 11. Email kit

### 11.1 Cold outreach (LinkedIn DM or referred email)

> Subject: 15 minutes — what we built on Foundry
>
> [Name],
>
> Deloitte's Microsoft practice has built a working agentic-commerce demo on Foundry — voice-driven shopping, in-store wayfinding via Azure Maps, a 14-field cryptographic ledger on every customer-facing decision. It runs in a browser on my laptop.
>
> We've extended it into the home: cameras, Sonos, a kitchen tablet, a privacy regime designed to be tougher than Alexa by construction.
>
> I'd love 15 minutes to share my screen. Are you open to that next week?
>
> — [Your name]

### 11.2 Follow-up after first meeting

> Subject: Recap + next step from yesterday
>
> [Name],
>
> Thanks for the time yesterday. Three things that stood out:
> 1. [Specific point they made about their priority]
> 2. [Specific question they asked, with your answer or commitment to follow up]
> 3. [Specific objection they raised, acknowledged]
>
> Two next steps I'd propose:
> - A 4-hour BVA workshop with your CMO/CX team — I have [DATE A] and [DATE B] open.
> - A technical deep-dive with [name of architect they mentioned] — same dates work.
>
> Demo lives here: [URL]
> Architecture overview: [link to your v5 deck export or the architecture page]
>
> Which next step makes sense?
>
> — [Your name]

### 11.3 Pre-meeting prep email (warming an exec audience)

> Subject: Tomorrow's meeting — 5-minute prep
>
> [Name],
>
> For tomorrow's discussion, three artifacts that will frame the conversation:
> - The 60-second thesis: [paste your 60-second pitch from §2.2]
> - The working demo: [URL] — open it before the call if you can; I'll narrate live
> - Pricing one-pager: [attach the §8.1 table]
>
> Five things I'd like to learn from your team:
> 1. Who owns the in-the-moment customer relationship?
> 2. What's your current voice-commerce posture?
> 3. What's the loyalty engagement metric that's stuck?
> 4. Is innovation funded from OpEx or CapEx?
> 5. Has your DPO weighed in on agentic AI yet?
>
> See you at [TIME].
>
> — [Your name]

---

## 12. Pre-meeting checklist (15-minute pre-call ritual)

Before any client conversation:

- [ ] Open the demo portal in a browser tab. Confirm it loads. Confirm camera feed is live.
- [ ] Open the architecture page in a second tab.
- [ ] Open CFMP-v0.2.md and CHC v0.2 in a third tab (for any deep-dive question).
- [ ] Have the v5 DMTSP deck in a fourth tab as a fallback if the demo glitches.
- [ ] Know the buyer's three biggest internal initiatives (Google their last 3 earnings calls or investor decks).
- [ ] Know the buyer's stated cloud posture (Azure-heavy? AWS? Hybrid? Their CIO's last public talk.).
- [ ] Have the §8.1 price ladder memorized.
- [ ] Have the 60-second pitch memorized.
- [ ] Have the §10 close ready in three flavors.
- [ ] Phone on silent.

---

## 13. Quick-reference card (print this)

**The 60-second pitch**: APEX framework. CFMP in-store, CHC in-home. Working demo on Foundry. 4-week Pack Lite for $150-400K under a BVA. Alexa-replacement positioning. Microsoft money via ISV Marketplace.

**The five pitches**: 30s / 60s / 5min / 15min (demo) / 45min (deck)

**The five whiteboard moves**: Alexa contrast / APEX pancake / Customer journey spine / Two-variant comparison / Service envelope ladder

**Key buyer questions to answer in this order**: Who owns the customer? Cloud posture? Voice-commerce today? Loyalty maturity? Privacy maturity? Budget vehicle?

**The standard close**: BVA workshop in 2 weeks, 4 hours, with their CMO/CX team.

**The price anchors**: $150-250K CFMP Lite · $250-400K CHC Lite · $750K-1.5M Standard · $25-110K/mo Operate.

**The two language rules**: "Deloitte's Microsoft practice" not "Microsoft partner." "Microsoft money rides ISV Marketplace" not "Microsoft funds us."

**The proof anchor**: the demo URL. If they can see it, they buy it.

---

## 14. Related artifacts (for the seller's reference)

- **The working demo**: `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io`
- **APEX teaching deck**: `C:\Users\kmarkham\Downloads\APEX-Design-v3.pptx` (41 slides — share when buyer wants the framework overview)
- **DMTSP walkthrough deck**: `C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Walkthrough-Deck-for-DMTSP-Sellers-v5.pptx` (15 slides — your primary seller deck)
- **CFMP v0.2 design**: `C:\Stage\Clients\Industries\APEX\docs\packs\CFMP-v0.2.md`
- **CFMP Pack Lite wedge**: `C:\Stage\Clients\Industries\APEX\docs\reference\CFMP-Pack-Lite-Wedge-for-DMTSP-Sellers.md`
- **CHC v0.2 design** (Connected Home Commerce, both variants + Alexa-replacement thesis): `C:\Stage\Clients\Industries\APEX\docs\packs\Connected-Home-Commerce-v0.1.md`
- **Architecture v5**: `C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Architecture-v5.docx` (25 chapters — share when buyer wants the engineering depth)
- **Sellers Guide volume of the book**: `C:\Stage\Clients\Industries\APEX\docs\book\Professional-APEX-M-Sellers-Guide.html` (the full reference; this doc is the field abstract)

---

## 15. Live market evidence — the consumer BOM (snapshot May 2026)

When the buyer says "this sounds futuristic," show them the BOM. **Every device in the CHC design ships on Amazon Prime for tomorrow-delivery, today.** The capability we're delivering is just orchestration — not new device categories, not new supply chain, not new consumer trust signals.

### 15.1 The household starter kit (real Amazon listings)

| Role | Device | Live signal | Price | Delivery |
|---|---|---|---|---|
| Edge ML + camera | **NVIDIA Jetson Orin Nano Developer Kit** | 1K+ bought past month · 371 ratings · 4.5★ | **$249** | Overnight |
| | + Waveshare aluminum alloy case w/ camera | 100+ bought past month · 142 ratings · 4★ | **$24** | Tomorrow |
| Smart speaker (voice) | **Sonos Era 100 — White (Alexa-Enabled)** | 500+ bought past month · 2,566 ratings · 4.5★ · `-14% deal` | **$189** (was $219) | Tomorrow |
| Kitchen kiosk (touch) | **WXUNJA Android 16 Tablet** 11" · Octa-Core · 28GB RAM · 128GB ROM · 1TB expand · Widevine L1 | 1K+ bought past month · 1,078 ratings · 4★ | **$110** | Overnight 7-11 AM |
| **Per-household starter kit total** | | | **~$572** | All Prime |

These are not specialty SKUs. These are mass-market consumer hardware with 1K+/month velocity at well-trusted price points. The total is less than a single iPhone.

### 15.2 Architecture mapping (BOM → CHC roles)

| BOM device | CHC role per CHC v0.2 §5 | What runs on it |
|---|---|---|
| Jetson Orin Nano + camera case | Vision Dev Kit equivalent — pantry / fridge / countertop edge | On-device classifier (TensorRT), frame embedding, person-detection, barcode capture |
| Sonos Era 100 | `sonos_voice` HITL surface | Audio output via Azure Speech "Ava Multilingual" TTS, optional STT via Sonos Voice Control or routed to tablet mic |
| Android 11" tablet | `home_kiosk` HITL surface | Kroger Plus app in kiosk mode (Variant B) or AT&T Smart Home app (Variant A) — Adaptive Cards, privacy panel, manual confirm |

The demo currently runs on Altek QCS605 (Snapdragon SoC, SNPE inference). **Jetson Orin Nano is a hardware swap, not an architectural change.** Interface #16 (proposed Home-Edge Device Plane per CHC v0.2 §4.5) abstracts the inference toolchain; same Pack manifests run on either silicon.

### 15.3 The "Alexa-Enabled Sonos" twist — it's a feature, not a bug

Worth pausing on: the Era 100 ships labeled "Alexa-Enabled." For an Alexa-replacement pitch, that reads ironic. It's actually the **strongest possible adoption story**:

> "The customer doesn't have to buy new hardware. They already own the Alexa device. We just route its agentic backend through APEX instead of Amazon."

The Era 100 supports three voice paths:

| Path | What it routes through | Best fit |
|---|---|---|
| 1. Amazon Alexa | Amazon Skill / Echo backend | What we're replacing |
| 2. Sonos Voice Control | Sonos's own non-Alexa voice surface | **Variant B preferred** |
| 3. No-wake-word audio-only | Pure Sonos Cloud API (TTS playback); wake-word lives on tablet/camera mic | **Variant A preferred** |

**In Variant A** (Telco-fronted): Sonos becomes pure audio output. Wake-word and STT live on the AT&T-managed tablet or Beelink home-edge node. Alexa fully removed.

**In Variant B** (Kroger-direct): Either path 2 (Sonos's own voice) or path 3 (Kroger Plus app on tablet hosts `"Hey Kroger"` wake-word). Sonos remains pure audio output.

**In both variants the customer's existing Sonos investment carries forward.** The decommissioning of Alexa is a software-and-account change, not a hardware change. This dramatically reduces adoption friction and is a privacy-story strength: the customer is "moving their agent backend off Amazon" rather than "buying new hardware and starting over."

### 15.4 Commercial implications per variant (BOM vs subsidized price)

The retail BOM ($572) sets the upper bound on what the customer would pay assembling this themselves. Each variant beats it decisively:

**Variant A — AT&T Home Concierge**
- Hardware bundled into 24-month subscription wrap
- AT&T's negotiated bulk pricing brings BOM to ~$350-400 effective
- Subscription ($25-40/mo) amortizes hardware + service + margin
- **Customer's incremental cost: $0 upfront, ~$30/mo**

**Variant B — Kroger Smart Pantry (Kroger Plus Premium)**
- Sold at-cost: starter kit $149-199
- OR: $0 hardware with 24-month Kroger Plus Premium commitment ($15-25/mo)
- Reference point in pitch: **"$572 to assemble it themselves from Amazon — or $0-199 with Kroger Plus Premium"**

Both variants undercut the retail-DIY price by 65-100% while also providing the orchestration, privacy regime, ongoing updates, and merchant integration the consumer cannot self-assemble.

### 15.5 Talk track for the meeting

When the client asks "is this real today?":

> "It's not just real — it's already in your customers' homes. Every device on the BOM ships on Amazon Prime overnight. The household starter kit totals five hundred and seventy-two dollars. What we deliver is the orchestration — the agent that turns three pieces of consumer hardware into a private, audit-trailed, merchant-aligned home concierge. Your customer is one app-store update away from leaving Alexa. We're delivering the alternative they're already shopping for."

This is your **"this is the present, not the future"** anchor. Use it:
- At the close of the demo (after §6 Chapter 5 "Now imagine this in the kitchen")
- Right before pricing in §8
- As the rebuttal to objection O7 "How long until production?"

### 15.6 What this evidence sharpens

Three updates to the rest of the seller motion now that real-market BOM is on the table:

1. **The CHC v0.2 §9 demo path is now even shorter.** Jetson Orin Nano + Sonos Era 100 + Android tablet = the lab can stand up an in-home rig identical to the customer-facing rig **in days, not weeks**. No specialty hardware procurement, no enterprise lead-time.
2. **Variant B pricing has new credibility.** Kroger Plus Premium hardware-at-cost ($149-199) is now provably **65-75% below the customer's DIY retail BOM** ($572) — a tangible subsidy story for the BVA worksheet.
3. **The Alexa-replacement positioning gains a "no new hardware" wedge.** Customer keeps their existing Sonos; only the agentic backend changes. This is the **softest possible adoption ramp**, and a privacy-story strength (the customer is moving their agent off Amazon, not starting from scratch).

### 15.7 BOM lifecycle for the SOW (Operate tier)

For the T5 Operate tier SOW, the BOM has three lifecycle dimensions worth costing:

| Lifecycle event | Cadence | Variant A impact | Variant B impact |
|---|---|---|---|
| Hardware refresh | 36-48mo | AT&T CPE swap-out program | Kroger Plus hardware-upgrade benefit |
| Firmware updates | Quarterly (security + capability) | Defender for IoT–managed push | Kroger Plus app + IoT Hub push |
| Battery / consumables | None — all line-powered | N/A | N/A |
| Add-device per household | Optional (more rooms = more cameras) | Per-device subscription line | Kroger Plus Premium add-on |

The point for the seller: **this is durable hardware** (no battery replacement, no consumables). Operate-tier economics are clean.

---

## 16. Related artifacts

- **The working demo**: `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io`
- **APEX teaching deck**: `C:\Users\kmarkham\Downloads\APEX-Design-v3.pptx` (41 slides — share when buyer wants the framework overview)
- **DMTSP walkthrough deck**: `C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Walkthrough-Deck-for-DMTSP-Sellers-v5.pptx` (15 slides — your primary seller deck)
- **CFMP v0.2 design**: `C:\Stage\Clients\Industries\APEX\docs\packs\CFMP-v0.2.md`
- **CFMP Pack Lite wedge**: `C:\Stage\Clients\Industries\APEX\docs\reference\CFMP-Pack-Lite-Wedge-for-DMTSP-Sellers.md`
- **CHC v0.2 design** (Connected Home Commerce, both variants + Alexa-replacement thesis): `C:\Stage\Clients\Industries\APEX\docs\packs\Connected-Home-Commerce-v0.1.md`
- **Architecture v5**: `C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Architecture-v5.docx` (25 chapters)
- **Sellers Guide volume of the book**: `C:\Stage\Clients\Industries\APEX\docs\book\Professional-APEX-M-Sellers-Guide.html`

---

*Internal · Deloitte Microsoft Technology & Services Practice · Prepared by Keven Markham, VP · 2026-05-23*
