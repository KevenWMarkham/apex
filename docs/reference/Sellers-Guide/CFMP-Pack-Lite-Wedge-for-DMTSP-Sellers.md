# CFMP Pack Lite — Vision AI Dev Kit Wedge

**The quickest wedge for a CMO / CX-VP conversation in DMTSP.**
Sold as Deloitte agentic-AI delivery services (not a product) under APEX-M Service Envelope Tier-2 Lite.

| | |
|---|---|
| **Pack** | CFMP — Customer Focused Merchandise Pack (the 7th Industry Pack) |
| **Sub-tier** | Pack Lite (Tier-2A per Architecture v5 §11.4) |
| **Buyer** | CMO · CX-VP · Loyalty Director — *not* the Ops VP that buys RC |
| **Price band** | **$150K–$250K** fixed fee (CFMP v0.2 §8) |
| **Timeline** | **4–6 weeks** |
| **Funding** | **BVA + DCIF** primary; ISV Marketplace burndown secondary (APEX-Design-v3 §S21) |
| **Persona type** | `customer` (loyalty-ID-bound, consent-gated) — extends APEX's persona model |
| **HITL surface** | `customer_phone` (signed-link push via Azure Notification Hubs) |
| **Proof asset** | **Working demo** at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io` |

---

## 60-second pitch

> "You're selling shelf-edge AI on Foundry today. Deloitte's CFMP turns that into a billable, audit-defensible, repeatable engagement: customer-journey scenarios on the cameras you already own, with a 14-field WORM ledger that proves to your DPO every nudge was consent-gated. We ship three scenarios live in 4–6 weeks for $150–250K under a BVA, then grow scenario-by-scenario."

**Why CFMP-Lite is the strongest opening at a Microsoft retail account right now:**

1. **The proof rig already exists.** Vision AI Dev Kit + portal + agent + LEDGER + Azure Maps wayfinding is running on `gpt-5-mini` today. No "imagine if…" demo. The seller can show it on a phone.
2. **CMO/CX-VP buy faster than Ops VP.** Customer-funded BVAs (trip conversion, basket size, NPS, loyalty churn) are easier to land than ops-cost BVAs.
3. **Foundation enhancements that ship with CFMP unlock the next four packs** (Banking-Customer, Telco-Customer, Hospitality-Guest, Healthcare-Patient). The buyer gets the wedge; Deloitte gets the platform leverage.
4. **Independence-safe by design.** APEX-M routes Microsoft funding via ISV Marketplace + SI Teaming — never direct ECIF to Deloitte.

---

## What ships in Pack Lite — three live scenarios

CFMP v0.2 §3 sub-tier rule: Lite ships 3 / Standard 10 / Enterprise all 18. Lite uses scenarios that are **already proven on the working demo**, so the engineering risk is in *productization*, not *invention*.

| # | Scenario ID | Customer journey phase | KPI target | Status on demo today |
|---|---|---|---|---|
| 1 | `rc-sampling-table-engagement` | CHOOSE | +50% promo ROI clarity | ✅ Live on Vision AI Dev Kit |
| 2 | `rc-cart-dwell-abandonment-rescue` | BUY | +12% physical cart-abandon recovery | ✅ Live (Proactive Associate) |
| 3 | `cfmp-wayfinding-walk-to-product` | SELECT | Time-to-find −60% · basket +8% | ✅ Live on local-fallback storemap |

**Engineering gap to Lite (CFMP v0.2 §8):**

1. Wayfinding production path — provision Azure Maps Creator per tenant, upload retailer Drawing Package, populate `CFMP.StoreMap` manifest (1w dev + 2w Creator dataset capture)
2. Azure Maps Web SDK indoor view in portal — render Tileset + route polyline (3 days)
3. BVA worksheet with three scenarios + wayfinding (1w)
4. Sample SOW template — Lite skeleton (2d)
5. Lite acceptance test suite — ~80 tests (1w)

Total: **~4 weeks dev + 2 weeks elapsed for retailer CAD capture = 4–6w**.

---

## Where Vision AI Dev Kit plugs into the APEX framework

This is the framework-anchored architecture story. Reference APEX-Design-v3.pptx slide-by-slide:

```
   Vision AI Dev Kit (Altek QCS605, edge)
        │
        │  raw frames + on-device classifier output (SNPE)
        │  + barcode/UPC + person-detected events
        ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  S6 · Bronze layer (replay source of truth)                  │  ← media stays here
   │  OneLake raw landing — per-frame blobs + event JSON         │
   └──────────────────────────────────────────────────────────────┘
        │
        ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  S36 · Featurization Layer (v4 extension)                    │
   │  • Emits canonical events  (CXML.CartDwellEvent,             │
   │    CXML.SamplingEngagement, MERML.ShelfState, ...)           │
   │  • Emits embeddings (768-d vectors on Silver)                │
   │  • Agents call fetch_media(raw_ref) for multimodal LLM       │
   │    inspection at decision time only                          │
   └──────────────────────────────────────────────────────────────┘
        │
        ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  S8/S9 · Virtual Views (sensing-to-resolution plane)         │
   │  • cxml.cart_dwell_event   (band: dwell > 90s = warn)       │
   │  • cxml.sampling_engagement (band: pickup_rate < 8% = warn) │
   │  • cfmp.storemap_view  (route source)                        │
   │  • merml.osa_by_aisle  (band: gap > 4ft = critical)         │
   └──────────────────────────────────────────────────────────────┘
        │
        ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  S11 · 6-Agent Fleet                                         │
   │  Assess → Classify → Quantify → APPROVE (HITL) → Act → Evidence │
   │  Customer-side HITL = customer_phone (consent prompt)        │
   │  Operator-side HITL = Teams Adaptive Card to associate       │
   └──────────────────────────────────────────────────────────────┘
        │
        ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  S7 · LEDGER (14-field WORM hash chain)                      │
   │  Every customer-facing action lands a row with:              │
   │  • customer_id_tkn      (consent-token hashed)              │
   │  • consent_hash         (proves opt-in at decision moment)  │
   │  • payload_hash + row_hash + prev_hash                       │
   │  • reasoning_trace_id   (model · prompt · steps · outputs)  │
   │  Auditor + DPO query is one apex-replay call away.           │
   └──────────────────────────────────────────────────────────────┘
```

**Special v4-extension touch-points to call out in the BVA:**

- **S31 Burst flight-recorder** — when a shelf-gap or sampling-table threshold trips, pre-buffer + during + tail frames are captured around the decision moment. Audit-ready for "show me the evidence behind that nudge."
- **S33 Agent Intelligence Layer — Memory + Calibration** — multi-visit customers benefit from precedent memory; uncertainty calibration prevents over-confident nudges.
- **S34 Constitution** — CFMP ships a customer-facing constitution: no nudge to under-18 inferences, no nudge during a clear "looking at private item" frame, no nudge if consent flag is withdrawn.
- **S36 Multimodal sources** — raw video stays in Bronze; agents `fetch_media(raw_ref)` only when a decision needs a multimodal-LLM look. Pays off bandwidth and DLP at once.
- **S37 Archival + Custody Chain** — for chains operating in CCPA/GDPR jurisdictions, the LEDGER's `media_refs` + `legal_hold` fields are exactly what the DPO is asking for.

---

## The 10-asset bundle — what's done, what's left for Lite

| # | Asset | Status for Lite |
|---|---|---|
| 1 | **VV manifests** | 6 written; 3 needed for Lite (`cxml.cart_dwell_event`, `cxml.sampling_engagement`, `cfmp.storemap_view`) ✅ |
| 2 | **Scenario manifests** | 3 of 3 Lite scenarios drafted ✅ |
| 3 | **Source adapters** | Vision AI Dev Kit MQTT + POS + Loyalty CRM + Beacon vendor — Vision adapter ✅, others scaffold |
| 4 | **Adaptive Cards** | Phone JSON + Teams operator JSON — both rendered in demo ✅ |
| 5 | **Persona map** | New `customer` persona type wired ✅; store_associate operator persona scaffold |
| 6 | **Demo data** | 800-product pgvector catalog + synthetic store + 50 simulated shoppers ✅ |
| 7 | **BVA worksheet** | Pack-level KPI rollup (CFMP v0.2 §9) — needs Excel pass (1w) |
| 8 | **Sample SOW** | Lite skeleton — 2 days to land (CFMP v0.2 §8) |
| 9 | **Acceptance tests** | 80+ tests targeted — currently ~30 live in CI |
| 10 | **Runbook + training** | Field install guide for beacons + storemap capture; store-team training deck — drafted, needs polish |

Eight of ten assets are already real. The two unfinished assets (BVA worksheet, Lite SOW) are exactly what a BVA workshop produces. **The Lite engagement IS the finishing-of-the-bundle.**

---

## Funding paths the LCSP can sequence

Per APEX-Design-v3 S21 + CFMP v0.2 §11:

| Path | When to use | Independence stance |
|---|---|---|
| **BVA (client-funded)** | Lite entry — 4 hour workshop produces shortlist + ROI worksheet | Clean — Deloitte fee from client |
| **DCIF (Deloitte co-invest)** | When Lite is the proving ground for a known FY-bound Standard | Clean — Deloitte commits its own balance sheet |
| **ISV Marketplace burndown** | Microsoft co-funds via the retailer's Marketplace commitment | Clean — money flows Microsoft → Marketplace → Deloitte |
| **SI Teaming POC** | Microsoft wants a co-pursuit but Deloitte's audit relationship blocks direct ECIF | Clean — non-competing SI receives ECIF, Deloitte delivers under SI sub |
| **Client direct + T&M** | Custom-build asks beyond the Lite scope (T4) | Clean — Deloitte on Deloitte paper |
| ❌ Direct ECIF to Deloitte | Never | Forbidden — SEC audit-independence rule |

---

## Growth path — Lite → Standard → Enterprise

| Tier | Scope | Price | Timeline | Funding |
|---|---|---|---|---|
| **Lite** (T2A) | 3 scenarios live + BVA + Lite SOW | $150–250K | 4–6w | BVA + DCIF |
| **Standard** (T2B) | +7 scenarios (OSA · shelf-gap · end-cap ROI · queue prediction · loyalty churn · complaint triage · in-store ad impact) | $750K–$1.5M | 12–16w | DCIF + T&M + ISV burndown |
| **Enterprise** (T2C) | All 18 scenarios + multi-store rollout + Operate-readiness + Fuse-with-MFG (cold-chain) and AXLE (dealer/parts) | $1.5–3.5M | 6–9mo | Client direct + T&M extensions |
| **Operate** (T5) | 24×7 monitor + threshold tuning + pack version uptake + DataOps for upstream | $/mo subscription | Continuous | Client direct |

**Additive by design.** No scenario re-platforms when the client moves up a sub-tier (CFMP v0.2 §3 + APEX-Design-v3 S20).

---

## One-line answers for the seller

| Buyer question | Seller answer |
|---|---|
| "Is this a product?" | "No. CFMP is a scoped Deloitte agentic-AI delivery engagement on the APEX framework, sold per industry under the standard Service Envelope tiers." |
| "Why now?" | "Because the proof rig is running on a laptop today. You're not buying a vision — you're funding the productization of three working scenarios into your stores." |
| "What about my DPO?" | "Every customer-facing action lands a LedgerRow with the consent token at decision moment, hashed into the chain. apex-replay reproduces the decision byte-identical. Your DPO gets cryptographic evidence, not a screenshot." |
| "What if we move off Azure later?" | "Same 10-asset bundle runs on APEX-G and APEX-A. The Maps interface (proposed #15) abstracts Azure Maps Creator behind a profile-swappable contract. No re-platform, just a config flip." |
| "How do I expand this?" | "Same wedge, more scenarios. Lite → Standard adds 7 more in 12–16 weeks. Standard → Enterprise lights up all 18. Each step is additive — no rework." |
| "How does this connect to your audit relationship with Microsoft?" | "Microsoft money flows via ISV Marketplace or SI Teaming, never direct ECIF to Deloitte. We've packaged the funding paths so the LCSP can sequence them in one slide." |

---

## Related artifacts

- **Working demo**: `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io` (CFMP v0.2)
- **CFMP design**: `C:\Stage\Clients\Industries\APEX\docs\packs\CFMP-v0.2.md`
- **Scenario chains (18)**: `C:\Stage\Clients\Industries\APEX\docs\packs\CFMP-Scenario-Chains-v0.1.xlsx`
- **DMTSP walkthrough deck**: `C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Walkthrough-Deck-for-DMTSP-Sellers-v5.pptx`
- **APEX teaching deck (parent)**: `C:\Users\kmarkham\Downloads\APEX-Design-v3.pptx` — slides referenced: S6 (Bronze), S7 (LEDGER), S8/S9 (VV + manifest), S11 (6-agent fleet), S20 (sub-tiers), S21 (funding), S31 (burst flight-recorder), S33 (Agent Intelligence), S34 (Constitution), S36 (Featurization Layer), S37 (Archival)
- **Architecture v5**: `C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Architecture-v5.docx` — §6 Cloud Profile, §9.6 RC Pack sibling, §10 Scenario Chains, §11 Service Envelopes, §17 Agent Intelligence

---

*Internal · Deloitte Microsoft Technology & Services Practice · Prepared by Keven Markham, VP · 2026-05-23*
