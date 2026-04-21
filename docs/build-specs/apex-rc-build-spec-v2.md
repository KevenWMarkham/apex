# APEX · Retail & Consumer Edition (APEX-RC)
## Edition Build Specification

**Spec version:** 2.0 (refactored to inherit from APEX Core v1.2)
**Manifest:** `apex-rc/data/schemas.manifest.json` — conforms to Core v1.2 schema-manifest contract.
**Parent spec:** `apex-core-build-spec.md` — **REQUIRED READING BEFORE THIS DOCUMENT**
**Edition code:** RC
**Edition accent token:** `--rc-accent: #d4a244` (gold)
**Status:** Active build

---

## Part 0 — Inheritance Declaration

This spec inherits from APEX Core v1.2. Every convention, template, design token, widget contract, and compliance constraint defined in Core applies here unchanged.

**Inheritance map:**

| Core Part | What this edition inherits |
|---|---|
| Core Part 0 | Compliance & language constraints (immutable) |
| Core Part 3 | Forces of Change framing convention (edition populates Part 2 below) |
| Core Part 4 | AI Journey Eras (unchanged, referenced) |
| Core Part 5 | CMM stages (unchanged, referenced; edition adds signals) |
| Core Part 6 | Reference architecture seven-layer model |
| Core Part 7 | Schema naming, medallion, entity template, event envelope |
| Core Part 8 | ORCH + MCP tool conventions, HITL gate taxonomy |
| Core Part 9 | Design system (extended with `--rc-accent`) |
| Core Part 10 | Reusable render widgets |
| Core Part 12 | Wave deployment model |
| Core Part 13 | Solution Stack shape |

**Edition additions start at Part 1 of this document.**

---

## Part 1 — Edition Positioning

### 1.1 What APEX-RC is

APEX-RC is the APEX instantiation tuned to the operational vocabulary, regulatory environment, and commercial maturity curve of **retail and consumer goods enterprises** — grocery, mass merchants, specialty retail, apparel, drug and convenience, and consumer packaged goods manufacturers.

### 1.2 Primary audiences

- Retail chief operating officers, chief supply chain officers, chief merchandising officers
- Consumer goods chief supply chain officers, chief commercial officers
- Store operations and asset protection leadership
- DMTSP engagement teams pursuing retail and CPG clients

### 1.3 Operating zone

APEX-RC delivers **Era 4 (Agentic)** outcomes while being architecturally ready for Era 5 (Adaptive). A client entering at CMM-2 (Connected) can progress to CMM-4 (Agentic) on APEX-RC's deployment rails over Waves 1–3.

---

## Part 2 — Forces of Change (Retail & Consumer)

Eight retail-specific forces. Conforms to Core Part 3 template.

| id | force | signal | implication |
|---|---|---|---|
| FOC-01 | Consumer Frugality & Value Migration | Trade-down across income bands; private-label share gains; channel-hopping for price | Pricing and assortment agents must operate at daily cadence, not quarterly |
| FOC-02 | Generative Commerce Emergence | AI-generated product content; conversational shopping agents on the consumer side; agentic shopping assistants | Retailers must match machine-legible and machine-conversational surfaces or lose discovery |
| FOC-03 | Channel Convergence & Store-as-Hub | BOPIS, SFS, curbside as permanent channels; store fulfillment share growing | Store-level agentic systems serve two masters: in-store shoppers and digital orders |
| FOC-04 | Margin Compression & Shrink Acceleration | Organized retail crime; self-checkout shrink; labor inflation; tariff-driven COGS volatility | Agentic loss prevention and dynamic pricing move from nice-to-have to mandatory |
| FOC-05 | Food Safety & Traceability Mandates | FSMA 204 (US); EU Digital Product Passports; state-level extended producer responsibility | Lot-level traceability and recall automation become regulatory floor |
| FOC-06 | Workforce Evolution | Frontline labor scarcity; associate role shifting to fulfillment operations; AI literacy gap | Agents must augment associate judgment, not demand new cognitive load |
| FOC-07 | Data Fabric Consolidation | Cloud-native retail stacks on Microsoft Fabric; legacy retail ERP exit | OneLake / Fabric as unified retail fabric unlocks agent deployment velocity |
| FOC-08 | Sustainability & Circularity | Reverse logistics investment; scope-3 reporting; circular supply chains | Agents reason over product lifecycle, not only first-sale economics |

**File:** `apex-rc/data/forces-of-change.json`

---

## Part 3 — CMM Signal Extensions for Retail & Consumer

Retail-specific observable signals per CMM stage. Additive to Core Part 5; does not replace it.

| stage | retail signals |
|---|---|
| CMM-1 Foundations | Spreadsheet-driven merchandising; stockouts detected by customer complaints; price changes executed weekly via manual ops |
| CMM-2 Connected | Real-time shelf-to-stock visibility; ML demand forecasting in production; merchants still manually route exception responses |
| CMM-3 Intelligent | Merchant copilots deployed; shelf CV in a subset of stores; pricing ML suggesting but humans approving at category level |
| CMM-4 Agentic | Store managers approve rather than triage; exception queues shift from "what happened" to "why it happened"; HITL rate <25% of detected events |
| CMM-5 Adaptive | Observed cycle times and loss rates improve without explicit retraining programs; assortment resets adapt to local velocity automatically |

**File:** `apex-rc/data/cmm-signals.json`

---

## Part 4 — Canonical Schemas (Retail & Consumer)

Four schemas. Conforms to Core Part 7 naming and template.

| schema | domain | scope | target_entity_count |
|---|---|---|---|
| MERML | Merchandising | Product, price, promotion, assortment, planogram, space, shelf, inventory position | ~40 |
| SCML | Supply Chain | Lots, shipments, receiving, cold chain, recalls, traceability, inbound/outbound logistics | ~35 |
| CXML | Customer Experience | Fulfillment orders, pick exceptions, substitutions, returns, incidents, loyalty, omnichannel signals | ~30 |
| MKTL | Marketing | Campaigns, audiences, creative assets, attribution, journey states, LTV, segment membership | ~25 |

### 4.1 Dimensional anchors (RC-specific)

`DIM_STORE`, `DIM_PRODUCT`, `DIM_LOT`, `DIM_EMPLOYEE`, `DIM_CUSTOMER`, `DIM_SUPPLIER`, `DIM_CATEGORY`, `DIM_LOCATION`, `DIM_DATE`, `DIM_TIME`.

### 4.2 Retail-specific controlled vocabulary for event envelope

For Core Part 7.4 envelope, RC uses these controlled vocabularies:

- `business_step`: `receiving`, `putaway`, `picking`, `stocking`, `counting`, `selling`, `returning`, `disposing`, `transferring`
- `disposition`: `in_progress`, `damaged`, `expired`, `recalled`, `active`, `reserved`, `sold`

### 4.3 Detailed schema entities

See `apex-rc/data/schemas.json` for full registry. Summary of key entities:

**MERML (Merchandising):**
`STORE_INVENTORY_POSITION`, `SHELF_FACING`, `OSA_EVENT`, `CYCLE_COUNT_VARIANCE`, `SHRINK_EVENT`, `PRICE_RECORD`, `PRICE_TAG_STATUS`, `PROMOTION_ACTIVATION`, `PLANOGRAM_ASSIGNMENT`, `PLANOGRAM_COMPLIANCE_EVENT`, `MARKDOWN_EVENT`, `WASTE_EVENT`, `LOT_EXPIRATION_STATE`, `POS_VOID`, plus ~25 more.

**SCML (Supply Chain):**
`ASN`, `STORE_RECEIVING_EVENT`, `RECEIVING_DISCREPANCY`, `DSD_INVOICE`, `COLD_CHAIN_TELEMETRY`, `TEMPERATURE_EXCURSION`, `RECALL_NOTICE`, `RECALL_DISPOSITION`, `LOT_TRACE`, `SHIPMENT_EVENT`, `CONTAINER_EVENT`, plus ~24 more.

**CXML (Customer Experience):**
`FULFILLMENT_ORDER`, `PICK_EXCEPTION`, `SUBSTITUTION_EVENT`, `RETURN_TRANSACTION`, `RETURN_DISPOSITION`, `RETURN_FRAUD_SIGNAL`, `CUSTOMER_INCIDENT`, `AGE_VERIFICATION_EVENT`, `CONTROLLED_SUBSTANCE_LEDGER`, `LOYALTY_STATE`, plus ~20 more.

**MKTL (Marketing):**
`CAMPAIGN`, `AUDIENCE`, `CREATIVE_ASSET`, `JOURNEY_STATE`, `ATTRIBUTION_EVENT`, `LTV_FORECAST`, `SEGMENT_MEMBERSHIP`, plus ~18 more.

---

## Part 5 — Domain Architectures (34 Agents)

Four domains. 34 total agents. Decomposition philosophy applied throughout (each agent has typed sub-agent contracts backtested in isolation before orchestrator connection).

### 5.1 Merchandising Domain (12 agents)

**Primary schema:** MERML. **Consumed schemas:** CXML, MKTL.
**Decision cadence:** Minute–hour operational; daily planning; weekly assortment.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| MER-A01 | Dynamic Pricing Agent | elasticity learner, competitive signal, margin guardrail | (platform) |
| MER-A02 | Assortment Optimizer | velocity analyzer, white-space detector, rationalization scorer | ORCH-09 |
| MER-A03 | Planogram Compliance Agent | shelf CV classifier, diff calculator, task router | (platform) |
| MER-A04 | ESL Gateway Monitor | push verifier, stale-tag detector, bridge-tag generator | ORCH-02 |
| MER-A05 | POS Mismatch Detector | price-ring comparator, customer refund stager | ORCH-02 |
| MER-A06 | Phantom OOS Detector | CV-POS-perpetual fusion, confidence scorer | ORCH-04 |
| MER-A07 | Pick List Optimizer | velocity ranker, walking-order solver | ORCH-04 |
| MER-A08 | Associate Router | zone tracker, task-match scorer, radio-status listener | ORCH-04 |
| MER-A09 | Void Pattern Detector | sigma anomaly, category isolator, employee-register correlator | ORCH-07 |
| MER-A10 | Variance Correlator | cycle-count matcher, return-receipt cross-checker | ORCH-07 |
| MER-A11 | Evidence Package Builder | timeline assembler, CCTV-frame referencer | ORCH-07 |
| MER-A12 | Markdown Cadence Agent | expiration tracker, disposition classifier | (platform) |

### 5.2 Supply Chain Domain (8 agents)

**Primary schema:** SCML. **Consumed schemas:** MERML.
**Decision cadence:** Second–minute for cold chain and recall; hour–day for planning.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| SCM-A01 | DSD Reconciliation Agent | portal-ASN matcher, line-level variance | ORCH-01 |
| SCM-A02 | Vendor Pattern Detector | 90d window scorer, recurrence classifier | ORCH-01 |
| SCM-A03 | Claim Assembly Agent | evidence attacher, dispute drafter | ORCH-01 |
| SCM-A04 | Cold Chain Telemetry Monitor | threshold watcher, excursion classifier | ORCH-03 |
| SCM-A05 | Disposition Classifier | sub-category risk scorer, save/destroy splitter | ORCH-03 |
| SCM-A06 | Write-Off Pre-Approver | loss-ledger stager, approval-route primer | ORCH-03 |
| SCM-A07 | FDA Feed Listener | recall parser, lot resolver | ORCH-05 |
| SCM-A08 | Lot Trace Resolver | upstream tracer, downstream tracer, customer identifier | ORCH-05 |

### 5.3 Customer Experience Domain (8 agents)

**Primary schema:** CXML. **Consumed schemas:** MERML, MKTL.
**Decision cadence:** Second for omnichannel; minute–hour for incidents; session-based for personalization.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| CXM-A01 | Pick Exception Handler | OOS classifier, alternative finder | ORCH-06 |
| CXM-A02 | Substitution Ranker | 14mo history scorer, rank composer | ORCH-06 |
| CXM-A03 | Customer Confirm Gateway | one-tap SMS, aging monitor | ORCH-06 |
| CXM-A04 | OCR Lot Extractor | image normalizer, code parser | ORCH-08 |
| CXM-A05 | Incident Pattern Detector | cross-store correlator, tier classifier | ORCH-08 |
| CXM-A06 | Stakeholder Router | QA/Legal/Comms parallel dispatcher | ORCH-08 |
| CXM-A07 | Returns Disposition Agent | disposition selector, RTV claim drafter | ORCH-12 |
| CXM-A08 | Lifecycle Signal Agent | churn predictor, winback opportunity scorer | ORCH-12 |

### 5.4 Marketing Domain (6 agents)

**Primary schema:** MKTL. **Consumed schemas:** CXML, MERML.
**Decision cadence:** Hour–day for activation; week for planning; campaign-lifecycle for optimization.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| MKT-A01 | Audience Builder | segment resolver, suppression filter | ORCH-11 |
| MKT-A02 | Creative Variant Generator | copy generator, image brief builder, brand guardrail checker | ORCH-11 |
| MKT-A03 | Campaign Orchestrator | channel sequencer, pacing controller | ORCH-11 |
| MKT-A04 | Attribution Agent | MTA model runner, incrementality tester | (platform) |
| MKT-A05 | LTV Forecaster | cohort modeler, intervention simulator | ORCH-12 |
| MKT-A06 | Journey State Agent | state transition classifier, next-best-action ranker | ORCH-12 |

---

## Part 6 — Orchestrations (ORCH-01 through ORCH-12)

Conforms to Core Part 8.2 contract template.

| orch_id | name | domain | agents | trigger | primary_gold_view | cycle_time_slo |
|---|---|---|---|---|---|---|
| ORCH-01 | Inbound Receiving | SCM | SCM-A01, SCM-A02, SCM-A03 | RFID portal event OR ASN arrival | GV_STORE_INBOUND_EXCEPTIONS | < 2 min at dock |
| ORCH-02 | Price Integrity | MERCH | MER-A04, MER-A05 | ESL sync anomaly OR POS-shelf divergence | GV_STORE_PRICE_INTEGRITY | < 10 min |
| ORCH-03 | Cold Chain Integrity | SCM | SCM-A04, SCM-A05, SCM-A06 | Threshold breach on telemetry stream | GV_STORE_COLD_CHAIN | < 5 min to brief |
| ORCH-04 | OSA Triage | MERCH | MER-A06, MER-A07, MER-A08 | Shelf CV + POS velocity fusion | GV_STORE_OSA_EXCEPTIONS | < 1 hr to restore |
| ORCH-05 | Recall Impact | SCM | SCM-A07, SCM-A08 | FDA / USDA / CPSC feed post | GV_STORE_RECALL_IMPACT | < 10 min to scope |
| ORCH-06 | Omnichannel Fulfillment | CXM | CXM-A01, CXM-A02, CXM-A03 | Pick exception from OMS | GV_STORE_OMNI_EXCEPTIONS | < 90 sec |
| ORCH-07 | Shrink Signal | MERCH | MER-A09, MER-A10, MER-A11 | 72hr rolling void-variance pattern | GV_STORE_SHRINK_SIGNAL | 72hr detect + <30 min package |
| ORCH-08 | Customer Incident | CXM | CXM-A04, CXM-A05, CXM-A06 | Service-desk incident intake | GV_STORE_SAFETY_CASES | < 10 min to case file |
| ORCH-09 | Assortment Optimization | MERCH | MER-A02 | Weekly planning cycle | GV_CATEGORY_ASSORTMENT | Weekly |
| ORCH-10 | Demand Sensing | SCM | (platform agents, shared) | Continuous signal fusion | GV_CHAIN_DEMAND | 15-min cadence |
| ORCH-11 | Campaign Activation | MKT | MKT-A01, MKT-A02, MKT-A03 | Brief intake OR trigger event | GV_CUSTOMER_AUDIENCE | Minutes to channel |
| ORCH-12 | Customer Lifecycle | CXM/MKT | CXM-A07, CXM-A08, MKT-A05, MKT-A06 | Event-driven state change | GV_CUSTOMER_LIFECYCLE | Continuous |

**File:** `apex-rc/data/orchestrations.json` — full contract per ORCH per Core Part 8.2.

---

## Part 7 — MCP Tool Catalog (Retail & Consumer)

Conforms to Core Part 8.4 naming and 8.5 contract.

### 7.1 RC domain codes

| code | scope |
|---|---|
| `mcp.store.*` | Store-scoped operations |
| `mcp.chain.*` | Chain-scoped (multi-store) operations |
| `mcp.vendor.*` | Vendor / supplier operations |
| `mcp.customer.*` | Customer-scoped operations |
| `mcp.product.*` | Product-scoped operations |
| `mcp.lot.*` | Lot-scoped traceability operations |
| `mcp.pos.*` | Point-of-sale operations |
| `mcp.omni.*` | Omnichannel fulfillment operations |
| `mcp.shrink.*` | Loss prevention operations |
| `mcp.ap.*` | Asset protection operations |
| `mcp.recall.*` | Recall-lifecycle operations |
| `mcp.campaign.*` | Marketing activation operations |

### 7.2 Catalog target

Initial catalog: ~60 tools. Seed catalog for Wave 1 (Store 100 reference implementation scope): 26 tools enumerated in `apex-rc/ref-impl/store-100/tools-seed.json`.

**File:** `apex-rc/data/tools.json`

---

## Part 8 — ISV Ecosystem (Retail & Consumer)

Reference catalog — clients select per existing estate.

| category | isv_examples | microsoft_integration |
|---|---|---|
| Retail ERP / Commerce | Dynamics 365 Commerce, D365 SCM | Native |
| POS / Store Tech | Diebold Nixdorf, NCR Voyix, Toshiba Global Commerce | Azure-integrated |
| Electronic Shelf Labels | SES-imagotag, Pricer, Hanshow | Azure IoT Hub |
| Shelf Computer Vision | Trigo, Focal Systems, Pensa | Azure AI + OneLake |
| RFID / Inventory | Sensormatic, Checkpoint Systems, Impinj | Azure IoT |
| Cold Chain / Telematics | Emerson, Sensitech, Controlant | Azure IoT + ADX |
| Transportation Visibility | project44, FourKites, Overhaul | API |
| Customer Data Platforms | D365 Customer Insights, Treasure Data, mParticle | Native / Fabric |
| Marketing Activation | Adobe Journey Optimizer, Braze, Iterable | Fabric + API |
| Loss Prevention | Everseen, Veesion, Corsight AI | Azure AI |
| Food Safety / Traceability | ReposiTrak, FoodLogiQ, TraceGains | Fabric integration |

**File:** `apex-rc/data/isv-ecosystem.json`

---

## Part 9 — Wave Content (Retail & Consumer)

Conforms to Core Part 12.2 contract.

| wave | name | scope | duration | entry | exit | economic_case |
|---|---|---|---|---|---|---|
| W1 | Foundation | L1–L4 stand-up; MERML Silver/Gold; first 3–5 agents; 1–3 pilot stores | 4–6 mo | CMM-1 or CMM-2 | CMM-3 readiness | OSA, pricing, receiving productivity — 90-day payback signal |
| W2 | Expansion | SCML + CXML canonical; first full MERCH ORCH stack; 10–15 agents; 25–50 stores | 6–9 mo | CMM-3 | Early CMM-4 | Shrink reduction + cold-chain loss avoidance + omnichannel cycle time |
| W3 | Platform | Cross-domain ORCHs; full 34-agent fleet; chain-wide rollout | 9–12 mo | CMM-4 entry | CMM-4 full | Enterprise exception handling; manager productivity flip |
| W4 | Adaptive | Continuous-learning harnesses; fleet self-optimization; cross-domain planning | Ongoing | CMM-4 | CMM-5 | Compounding returns as fleet improves itself |

**File:** `apex-rc/data/waves.json`

---

## Part 10 — Reference Implementations (RC)

| ref_impl | scope | status | spec |
|---|---|---|---|
| Store 100 Day-in-the-Shift | Single store, single shift, 8 events across MERCH/SCM/CXM, ORCH-01 through ORCH-08 | Built (v1) | `apex-rc-store-100-build-spec.md` |
| RefImpl-02 Recall Cascade | 14-store, multi-day recall execution | Reserved | TBD |
| RefImpl-03 Assortment Reset Week | Multi-agent weekly planning cycle | Reserved | TBD |
| RefImpl-04 Campaign-to-Conversion | MKT + CXM cross-domain loop | Reserved | TBD |

**File:** `apex-rc/data/ref-implementations.json`

---

## Part 11 — Solution Stack (RC)

Conforms to Core Part 13 column contract. ~50 rows.

**Row distribution:**
- 7 rows — L1–L2 infrastructure (POS, D365 Commerce, Event Hubs, Fabric, OneLake, ADX, Synapse Link)
- 4 rows — L3–L4 schema registries (MERML, SCML, CXML, MKTL)
- 4 rows — Gold view categories (store ops, chain analytics, customer, product)
- 34 rows — Agent fleet (one per RC agent)
- 12 rows — ORCH definitions
- (balance) — L7 experiences and ISV bindings

**File:** `apex-rc/data/solution-stack.json`

---

## Part 12 — File Structure (RC)

```
apex-rc/
├── README.md                               # This spec
├── CHANGELOG.md                            # RC version history
├── index.html                              # RC framework site
├── /data/
│   ├── forces-of-change.json               # Part 2
│   ├── cmm-signals.json                    # Part 3
│   ├── schemas.json                        # Part 4
│   ├── agents.json                         # Part 5 (34 agents)
│   ├── orchestrations.json                 # Part 6 (12 ORCHs)
│   ├── tools.json                          # Part 7 MCP catalog
│   ├── isv-ecosystem.json                  # Part 8
│   ├── waves.json                          # Part 9
│   ├── ref-implementations.json            # Part 10
│   └── solution-stack.json                 # Part 11
└── /ref-impl/
    └── /store-100/                         # Separate build from companion spec
        ├── index.html
        └── /data/
```

---

## Part 13 — Build Sequence

Six phases. Consumes Core widgets and design system.

### Phase 1 — RC framework skeleton
**Deliverable:** `index.html` rendering Parts 1–6 and 9 as static content.
**Imports from Core:** design tokens, typography, components CSS; theme.js, navigation.js.
**Extends:** adds `--rc-accent: #d4a244` to its local stylesheet.
**Acceptance:** Parts 1–6 and 9 render; theme toggle works; AA contrast both themes.

### Phase 2 — Domain architecture
**Deliverable:** Part 5 (four domain tabs) interactive.
**Imports from Core:** `/js/domain-tabs.js`.
**Acceptance:** MERCH/SCM/CXM/MKT tabs cross-fade; agent rows hover-expand.

### Phase 3 — ORCH + MCP + Gold views
**Deliverable:** Parts 6, 7 interactive.
**Imports from Core:** `/js/orch-expander.js`.
**Acceptance:** 12 ORCH rows click-to-expand; tool catalog filterable by domain code.

### Phase 4 — Solution Stack Chart
**Deliverable:** Part 11 interactive with ≥50 rows.
**Imports from Core:** `/js/solution-stack.js`.
**Acceptance:** Filter by layer/domain/wave/CMM; sortable; row-click detail panel.

### Phase 5 — Wave Timeline + ISV Ecosystem
**Deliverable:** Parts 8, 9 interactive.
**Imports from Core:** `/js/wave-timeline.js`.
**Acceptance:** Hover-reveal of wave exit criteria; ISV catalog filterable.

### Phase 6 — Reference Implementations hub
**Deliverable:** Part 10 with Store 100 live.
**Acceptance:** Card grid for ref-impls; Store 100 card links to `/ref-impl/store-100/index.html`.

---

## Part 14 — Acceptance Criteria

Per Core Part 11, RC is Core-conformant when:

1. ☑ Folder exists as `apex-rc/` parallel to `apex-core/`
2. ☑ README declares code RC, version, Core spec version referenced
3. ☑ 8 Forces of Change defined (Part 2 above)
4. ☑ Eras and CMM referenced unchanged; CMM signals added
5. ☑ 4 schemas defined (MERML, SCML, CXML, MKTL)
6. ☑ Event envelope inherited unchanged
7. ☑ 12 ORCHs defined with contracts (Part 6)
8. ☑ MCP tool catalog with domain codes (Part 7)
9. ☑ Design system inherited; `--rc-accent` added
10. ☑ Core widgets consumed, not reimplemented
11. ☑ Part 0 compliance passes lint
12. ☑ Solution Stack has ≥50 rows per Core Part 13 contract
13. ☑ At least one reference implementation (Store 100) under `/ref-impl/`

---

## Part 15 — Handoff Notes to Claude Code

**Read Core first.** Do not begin this build without reading `apex-core-build-spec.md`. Every convention, template, and widget contract lives there.

**Do not duplicate Core content.** If this spec seems to lack detail on a convention (e.g., HITL gate taxonomy, event envelope, wave contract), look in Core. Duplication is a sign the spec has drifted from the inheritance model.

**This spec replaces `apex-rc-framework-build-spec.md` v1.0.** Version 2.0 is the refactored, inheritance-aware spec. The v1.0 content has been split: cross-industry content moved to Core, RC-specific content stays here.

**Store 100 is unchanged.** The Store 100 reference implementation spec (`apex-rc-store-100-build-spec.md`) is still valid — it is a consumer of RC, and RC is now a consumer of Core. The chain runs: Core → RC → Store 100.

---

**End of APEX-RC specification · v2.0**

*Parent spec:*
- *`apex-core-build-spec.md` v1.0*

*Sibling edition:*
- *`apex-th-build-spec.md` — Travel & Hospitality edition*

*Child reference implementation:*
- *`apex-rc-store-100-build-spec.md`*
