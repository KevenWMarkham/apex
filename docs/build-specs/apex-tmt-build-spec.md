# APEX · Technology, Media & Telecom Edition (APEX-TMT)
## Edition Build Specification

**Spec version:** 1.0
**Parent spec:** `apex-core-build-spec.md` — **REQUIRED READING BEFORE THIS DOCUMENT**
**Edition code:** TMT
**Edition accent token:** `--tmt-accent: #8b5cf6` (violet-signal — bandwidth, connection, modernity)
**Status:** Planned build
**Sub-variants:** `TMT-TEL` (Telecom), `TMT-MED` (Media & Entertainment), `TMT-TEC` (Technology)

---

## Part 0 — Inheritance Declaration

This spec inherits from APEX Core v1.2 unchanged. Every Core convention, template, and constraint applies.

**Manifest:** `apex-tmt/data/schemas.manifest.json` — conforms to the Core v1.2 schema-manifest contract (to be populated).

**Inheritance map:**

| Core Part | Inherited |
|---|---|
| 0 | Compliance & language constraints (immutable) |
| 3 | Forces of Change framing convention |
| 4 | AI Journey Eras (unchanged) |
| 5 | CMM stages (unchanged; edition adds signals) |
| 6 | Reference architecture |
| 7 | Schema naming, medallion, entity template, event envelope |
| 8 | ORCH + MCP + HITL taxonomy |
| 9 | Design system (extended with `--tmt-accent`) |
| 10 | Reusable render widgets |
| 12 | Wave deployment model |
| 13 | Solution Stack shape |

**TMT-specific compliance additions:**

1. **Content rights** — any demo referencing media content must use clearly fictional titles, assets, and rights-holders.
2. **Network identity** — any subscriber or device identifier in demos must be synthetic (e.g., `sub-test-0091`, `imsi-demo-X`).
3. **Developer data** — any API/telemetry identifier must be synthetic.

---

## Part 1 — Edition Positioning

### 1.1 What APEX-TMT is

APEX-TMT is the APEX instantiation tuned to **technology, media & entertainment, and telecommunications enterprises** — communication service providers (wireless, wireline, cable, satellite), media companies (streaming, studios, publishers, broadcasters), and technology companies (SaaS, enterprise software, semiconductors, consumer hardware, platform businesses).

### 1.2 Primary audiences

**Telecom (TMT-TEL):** Chief Customer Officers, Network/Technology Officers, Chief Revenue Officers, Chief Digital Officers of CSPs.

**Media (TMT-MED):** Chief Content Officers, Chief Product Officers (streaming platforms), Heads of Distribution, Chief Revenue / Ad-Sales Officers, Chief Audience / Insights Officers.

**Technology (TMT-TEC):** Chief Product Officers, Chief Customer Officers (at platform / SaaS companies), Heads of Customer Success, Chief Developer Relations Officers, Chief Revenue Officers.

### 1.3 Operating zone

APEX-TMT delivers Era 4 (Agentic) outcomes in customer lifecycle, content / network operations, and product telemetry workflows. TMT has a **lower HITL gate rate** than HLS because most operational decisions do not carry clinical or regulatory consequence — though billing disputes, content rights enforcement, and network emergency response retain HITL gates.

### 1.4 Why TMT demands its own edition

TMT differs from other APEX editions in four structural ways:

1. **Subscription / usage-based economics dominate** — the revenue machine is a subscriber / consumer / developer lifecycle, not a product sale
2. **Delivery pipelines are the operational spine** — content supply chain (media), network operations (telecom), product telemetry (tech) — they rhyme structurally
3. **Customer LTV and churn are the scoreboard** — more than transaction margin
4. **Distribution and partner ecosystems are the surface** — the enterprise serves through channels (app stores, operators, aggregators, MVNOs, resellers)

### 1.5 Three sub-variants, one edition

Telecom, Media, and Technology share subscription economics, lifecycle cadence, and content/service delivery patterns. Their differences are in the **spine entity** — network for telecom, content catalog for media, product/platform for tech — but the agents, orchestrations, and customer lifecycle schemas share structure.

---

## Part 2 — Forces of Change (Technology, Media & Telecom)

| id | force | signal | implication |
|---|---|---|---|
| FOC-01 | Subscriber Fatigue & Churn Compounding | Streaming cord-cutting among cord-cutters; telecom number-portability friction; SaaS consolidation pressure | Retention and personalization agents must operate at intra-session cadence |
| FOC-02 | AI-Native Consumer Expectation | Consumers expect conversational / agentic interfaces; traditional IVR and chat satisfaction collapsing | Customer agents must match or exceed consumer-grade AI on any customer-facing surface |
| FOC-03 | Content / Spectrum / Compute as Scarce Capital | Content arms race margin pressure; 5G monetization challenge; GPU/compute constraint for AI | Yield and allocation agents become central, not peripheral |
| FOC-04 | Creator & Developer Economy | UGC, creator economics, developer-as-customer, platform API surfaces — the "long tail" as real revenue | Creator/developer lifecycle becomes a first-class agentic domain |
| FOC-05 | Privacy / Regulatory Fragmentation | GDPR, CCPA, state-level US laws, DSA/DMA in EU, children's privacy enforcement | Consent, data-minimization, and explainability agents are table stakes |
| FOC-06 | Network / Cloud Convergence | Telco network functions virtualized on cloud; edge compute emergence; 5G core as software | Network operations adopts cloud-native patterns — agents deploy natively |
| FOC-07 | Generative Content Economics | Generative AI redefining content creation cost curves; rights and provenance under pressure; search engine disruption | Content workflows must support attribution, provenance, and rights-aware agents |
| FOC-08 | Ad / Distribution Platform Concentration | Walled gardens dominant; attribution fragmented; retail media emergent | Activation agents must operate across fragmented and consented channels |
| FOC-09 | Fraud & Abuse Sophistication | SIM swap; streaming/ad fraud; account takeover; bot ecosystems | Trust & safety agents operate at machine speed against machine-speed adversaries |
| FOC-10 | Platform Interoperability Pressure | Device-to-device messaging interop, streaming interop, enterprise integration via MCP-style catalogs | Agents expect interoperable APIs/catalogs, not bespoke integrations |

**File:** `apex-tmt/data/forces-of-change.json`

---

## Part 3 — CMM Signal Extensions for TMT

| stage | tmt signals |
|---|---|
| CMM-1 Foundations | Billing and CRM in place; subscriber / customer / developer reporting; churn detected retrospectively |
| CMM-2 Connected | Real-time event fabric (usage, network, content, product telemetry); ML for churn and next-best-action in production |
| CMM-3 Intelligent | Copilots for care, sales, creator-support; generative content and conversational surfaces live in production |
| CMM-4 Agentic | Agents resolve tier-1 / tier-2 issues autonomously; personalization runs without human intervention; network / content / product pipeline exceptions handled by agent fleet with HITL for edge cases |
| CMM-5 Adaptive | Observed LTV and churn improve without explicit retraining; cross-channel orchestration emerges |

**File:** `apex-tmt/data/cmm-signals.json`

---

## Part 4 — Canonical Schemas (TMT)

Four schemas. The three sub-variants share two schemas (CLTML, COMML) and specialize in a third (NETML for Telecom, CNTML for Media, PRDML for Technology).

| schema | domain | scope | sub_variants | target_entity_count |
|---|---|---|---|---|
| **CLTML** | Customer Lifecycle | Subscriber/customer/developer identity, journey states, subscription, billing, churn, LTV | ALL | ~40 |
| **COMML** | Commerce & Monetization | Offers, pricing, plans, promotions, upgrades/downgrades, cross-sell, ad/monetization events | ALL | ~30 |
| **NETML** | Network Operations | Cell sites, core network elements, service assurance, incident, performance telemetry, field dispatch | TEL | ~35 |
| **CNTML** | Content Operations | Catalog, metadata, rights, encoding/distribution, scheduling, measurement | MED | ~35 |
| **PRDML** | Product Telemetry | Product usage, feature adoption, API calls, SLA events, release state, developer activity | TEC | ~35 |

Each client deployment typically uses CLTML + COMML + one of the spine schemas (NETML / CNTML / PRDML), though integrated TMT enterprises may use multiple spines.

### 4.1 Dimensional anchors (TMT)

**Shared across all sub-variants:**
`DIM_CUSTOMER` (tokenized), `DIM_ACCOUNT`, `DIM_SUBSCRIPTION`, `DIM_PLAN`, `DIM_CHANNEL`, `DIM_DEVICE`, `DIM_GEOGRAPHY`, `DIM_DATE`, `DIM_TIME`.

**Telecom:**
`DIM_CELL_SITE`, `DIM_NETWORK_ELEMENT`, `DIM_SERVICE`, `DIM_SIM`.

**Media:**
`DIM_TITLE`, `DIM_TALENT`, `DIM_RIGHTS_WINDOW`, `DIM_PLATFORM` (distribution endpoint).

**Technology:**
`DIM_PRODUCT`, `DIM_FEATURE`, `DIM_TENANT`, `DIM_DEVELOPER`, `DIM_RELEASE`.

### 4.2 TMT controlled vocabulary for event envelope

- `business_step`: `browsing`, `enrolling`, `subscribing`, `consuming`, `renewing`, `upgrading`, `downgrading`, `cancelling`, `resolving`, `billing`, `collecting`, `reporting`
- `disposition`: `prospective`, `active`, `suspended`, `in_grace`, `churned`, `resolved`, `escalated`

### 4.3 Key entities (summary)

**CLTML:** `SUBSCRIBER`, `ACCOUNT`, `SUBSCRIPTION`, `JOURNEY_STATE`, `LIFECYCLE_EVENT`, `CHURN_SIGNAL`, `LTV_FORECAST`, `SUPPORT_INTERACTION`, `CONSENT_RECORD`, plus ~31 more.

**COMML:** `OFFER`, `PROMOTION`, `UPGRADE_EVENT`, `BILL_LINE`, `PAYMENT_EVENT`, `DUNNING_EVENT`, `AD_IMPRESSION`, `AD_EVENT`, `ATTRIBUTION_EVENT`, plus ~21 more.

**NETML:** `NETWORK_INCIDENT`, `CELL_PERFORMANCE`, `SERVICE_TICKET`, `FIELD_DISPATCH`, `PROVISIONING_EVENT`, `ACTIVATION_EVENT`, `ROAMING_EVENT`, `SIM_EVENT`, plus ~27 more.

**CNTML:** `CONTENT_ASSET`, `METADATA_RECORD`, `RIGHTS_GRANT`, `RIGHTS_WINDOW`, `ENCODING_JOB`, `DISTRIBUTION_EVENT`, `MEASUREMENT_EVENT`, `AD_POD`, plus ~27 more.

**PRDML:** `USAGE_EVENT`, `FEATURE_INVOCATION`, `API_CALL`, `SLA_EVENT`, `TENANT_HEALTH`, `RELEASE`, `DEPLOYMENT_EVENT`, `DEV_ACTIVITY`, plus ~27 more.

---

## Part 5 — Domain Architectures (30 Agents)

Four domains. 30 agents distributed across sub-variants.

### 5.1 Customer & Lifecycle Domain (ALL · 10 agents)

**Primary schema:** CLTML. **Consumed schemas:** COMML, spine schemas.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| CLC-A01 | Churn Risk Agent | multi-signal aggregator, intervention-window predictor, segment-aware scorer | ORCH-12 |
| CLC-A02 | Retention Offer Agent | offer-eligibility resolver, NBA ranker, margin guardrail | ORCH-12 |
| CLC-A03 | Onboarding Agent | activation-path optimizer, friction-point detector, next-step nudger | ORCH-01 |
| CLC-A04 | Support Copilot | case-context builder, resolution-step retriever, KB-article matcher | ORCH-06 |
| CLC-A05 | Escalation Agent | sentiment tracker, priority classifier, stakeholder router | ORCH-08 |
| CLC-A06 | Billing Dispute Agent | usage-correlator, policy-interpreter, refund-stager | ORCH-02 |
| CLC-A07 | Upgrade / Cross-sell Agent | fit-scorer, timing optimizer, inventory-aware allocator | ORCH-06 |
| CLC-A08 | Consent Orchestrator | preference resolver, applicability checker, audit-trail builder | (platform) |
| CLC-A09 | Community / Creator Support Agent | tier-appropriate routing, moderation assist, dispute resolution drafter | ORCH-06 |
| CLC-A10 | LTV Forecaster | cohort modeler, intervention simulator | ORCH-12 |

### 5.2 Network / Content / Product Operations Domain (10 agents across sub-variants)

**Telecom (NETML) — 4 agents:**

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| NET-A01 | Network Incident Agent | alarm-fusion, root-cause candidate generator, impact-scoper | ORCH-07 |
| NET-A02 | Field Dispatch Agent | skill-match router, SLA monitor, parts-inventory coordinator | ORCH-07 |
| NET-A03 | Service Assurance Agent | KPI trend analyzer, degradation predictor, customer-impact correlator | ORCH-04 |
| NET-A04 | Activation & Provisioning Agent | order-to-activation orchestrator, exception triage | ORCH-01 |

**Media (CNTML) — 3 agents:**

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| CNT-A01 | Content Supply Chain Agent | ingest-to-publish pipeline, rights-window enforcer, encoding-exception handler | ORCH-07 |
| CNT-A02 | Metadata Enrichment Agent | auto-tagger, taxonomy harmonizer, rights-metadata compiler | ORCH-07 |
| CNT-A03 | Rights & Clearance Agent | rights-window resolver, violation detector, clearance-request drafter | (platform) |

**Technology (PRDML) — 3 agents:**

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| PRD-A01 | Tenant Health Agent | usage-trend analyzer, SLA-breach predictor, intervention recommender | ORCH-04 |
| PRD-A02 | Release & Rollout Agent | canary-progression monitor, rollback signal, feature-flag orchestrator | ORCH-07 |
| PRD-A03 | Developer Experience Agent | API friction detector, docs gap analyzer, migration-guide surfacer | ORCH-06 |

### 5.3 Monetization & Commerce Domain (ALL · 6 agents)

**Primary schema:** COMML. **Consumed schemas:** CLTML.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| MON-A01 | Pricing / Packaging Agent | elasticity learner, competitive signal, margin guardrail | ORCH-02 |
| MON-A02 | Offer Personalization Agent | segment-aware composer, suppression filter | ORCH-02 |
| MON-A03 | Ad Yield Agent | inventory optimizer, bid-shading signal, brand-safety enforcer | ORCH-11 |
| MON-A04 | Campaign Orchestrator | channel sequencer, pacing controller, attribution-aware budget reallocator | ORCH-11 |
| MON-A05 | Creative Variant Generator | copy/imagery composer, brand guardrail checker, rights validator | ORCH-11 |
| MON-A06 | Revenue Assurance Agent | billing-event reconciliator, leakage detector, dispute-aggregator | (platform) |

### 5.4 Trust, Safety & Assurance Domain (ALL · 4 agents)

**Primary schemas:** spine + CLTML.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| TRS-A01 | Fraud Detection Agent | pattern anomaly, velocity signal, risk-band classifier | ORCH-08 |
| TRS-A02 | Account Takeover Agent | behavioral anomaly, device-fingerprint comparator, step-up orchestrator | ORCH-08 |
| TRS-A03 | Content Moderation Agent | policy-applicability classifier, context-aware reviewer, HITL escalator | ORCH-08 |
| TRS-A04 | Regulatory Compliance Agent | reporting-requirement tracker, audit-trail builder, policy-change propagator | ORCH-09 |

---

## Part 6 — Orchestrations (TMT)

| orch_id | name | domain | sub_variant | agents | trigger | primary_gold_view | cycle_time_slo |
|---|---|---|---|---|---|---|---|
| ORCH-01 | Onboarding & Activation | CLC/NET/PRD | ALL | CLC-A03, NET-A04 | New subscriber/customer/tenant | GV_CUSTOMER_ONBOARDING | < 15 min to productive |
| ORCH-02 | Pricing & Offer Activation | MON | ALL | MON-A01, MON-A02, CLC-A06 | Pricing change OR offer trigger | GV_CUSTOMER_OFFERS | < 10 min channel sync |
| ORCH-03 | (Reserved slot) | — | — | — | — | — | — |
| ORCH-04 | Service Health / Tenant Health | NET/PRD | TEL/TEC | NET-A03, PRD-A01 | Health anomaly signal | GV_SERVICE_HEALTH | < 5 min to alert |
| ORCH-05 | Disruption Response | NET/CNT/PRD | ALL | NET-A01, NET-A02, CNT-A01, PRD-A02 | Outage / pipeline break / release incident | GV_INCIDENT_IMPACT | < 10 min to scope |
| ORCH-06 | Support & Resolution | CLC/PRD | ALL | CLC-A04, CLC-A07, CLC-A09, PRD-A03 | Support contact / developer request | GV_SUPPORT_QUEUE | < 90 sec to routing |
| ORCH-07 | Pipeline / Incident Management | NET/CNT/PRD | ALL | NET-A01, NET-A02, CNT-A01, CNT-A02, PRD-A02 | Pipeline event OR incident | GV_OPS_PIPELINE | < 15 min to action |
| ORCH-08 | Trust & Safety / Escalation | TRS/CLC | ALL | TRS-A01, TRS-A02, TRS-A03, CLC-A05 | Fraud signal / policy violation / escalation | GV_TRUST_CASES | < 5 min to hold |
| ORCH-09 | Regulatory & Reporting | TRS | ALL | TRS-A04 | Reporting trigger | GV_COMPLIANCE_QUEUE | Cycle-driven |
| ORCH-10 | Demand / Audience / Tenant Sensing | MON/CLC | ALL | (shared agents) | Continuous signal fusion | GV_AUDIENCE | 15-min cadence |
| ORCH-11 | Campaign & Yield Activation | MON | ALL | MON-A03, MON-A04, MON-A05 | Campaign trigger | GV_ACTIVATION | Minutes to channel |
| ORCH-12 | Lifecycle & Retention | CLC | ALL | CLC-A01, CLC-A02, CLC-A10 | Event-driven state change | GV_CUSTOMER_LIFECYCLE | Continuous |

Note: ORCH-03 is unused in TMT (no cold-chain analog); slot reserved for future TMT expansion.

**File:** `apex-tmt/data/orchestrations.json`

---

## Part 7 — MCP Tool Catalog (TMT)

### 7.1 TMT domain codes

| code | scope |
|---|---|
| `mcp.subscriber.*` | Subscriber / customer operations |
| `mcp.account.*` | Account operations |
| `mcp.subscription.*` | Subscription lifecycle operations |
| `mcp.offer.*` | Offer & promotion operations |
| `mcp.billing.*` | Billing & dispute operations |
| `mcp.support.*` | Support ticket / case operations |
| `mcp.network.*` | Network operations (TEL) |
| `mcp.cell.*` | Cell-site scoped (TEL) |
| `mcp.field.*` | Field service (TEL) |
| `mcp.content.*` | Content catalog & pipeline (MED) |
| `mcp.rights.*` | Rights & clearance (MED) |
| `mcp.distribution.*` | Distribution & measurement (MED) |
| `mcp.product.*` | Product & tenant operations (TEC) |
| `mcp.release.*` | Release & deployment (TEC) |
| `mcp.developer.*` | Developer experience (TEC) |
| `mcp.ad.*` | Ad & monetization operations |
| `mcp.fraud.*` | Fraud / trust operations |
| `mcp.consent.*` | Consent & preference operations |

### 7.2 Catalog target

Initial catalog: ~60 tools.

**File:** `apex-tmt/data/tools.json`

---

## Part 8 — ISV Ecosystem (TMT)

| category | isv_examples | microsoft_integration |
|---|---|---|
| CRM / Customer | D365 CRM, Salesforce, HubSpot | Native / API |
| CDP | D365 Customer Insights, Adobe RT CDP, Treasure Data | Native / Fabric |
| Billing / Monetization | Amdocs, Oracle BRM, Zuora, Stripe Billing | API |
| OSS / BSS (Telco) | Amdocs, Netcracker, Huawei (BSS) | API |
| Network Management | Nokia NSP, Ericsson OSS, Cisco Crosswork | API |
| Field Service | D365 Field Service, Salesforce Field Service | Native / API |
| Content MAM | Iconik, Wasabi, Dalet, Avid MediaCentral | API |
| Distribution / CDN | Azure CDN, Akamai, Cloudflare, Fastly | Native / API |
| Ad Tech | Google Ad Manager, FreeWheel, Magnite | API |
| Product Analytics | Amplitude, Mixpanel, Heap, Pendo | API |
| Developer Platform | GitHub, Azure DevOps, Stripe Workbench, Twilio | Native / API |
| Fraud / Trust | Sift, Forter, Arkose Labs | API |

**File:** `apex-tmt/data/isv-ecosystem.json`

---

## Part 9 — Wave Content (TMT)

| wave | name | scope | duration | entry | exit | economic_case |
|---|---|---|---|---|---|---|
| W1 | Foundation | L1–L4 stand-up; CLTML + one spine schema; first 3–5 agents (support copilot, churn risk, one spine agent); pilot in one segment | 4–6 mo | CMM-1 or CMM-2 | CMM-3 readiness | Support deflection + churn-risk intervention lift — 90-day signal |
| W2 | Expansion | COMML + full spine canonical; first full domain ORCH stack; 10–15 agents | 6–9 mo | CMM-3 | Early CMM-4 | LTV uplift + incident MTTR reduction + campaign ROI improvement |
| W3 | Platform | Cross-domain ORCHs; full 30-agent fleet; enterprise rollout | 9–12 mo | CMM-4 entry | CMM-4 full | Enterprise lifecycle automation; agent-to-agent interop |
| W4 | Adaptive | Continuous learning; fleet self-optimization | Ongoing | CMM-4 | CMM-5 | Compounding returns |

**File:** `apex-tmt/data/waves.json`

---

## Part 10 — Reference Implementations (TMT)

| ref_impl | scope | sub_variant | status | spec |
|---|---|---|---|---|
| Carrier NOC Day-in-the-Console | Tier-1 CSP NOC shift, 8 network/customer events | TEL | Planned | TBD |
| Streaming Platform Operations Day | Streaming service ops, 8 content/audience events | MED | Planned | TBD |
| SaaS Tenant Success Day | Platform customer success team, 8 tenant events | TEC | Planned | TBD |

**File:** `apex-tmt/data/ref-implementations.json`

### 10.1 Three lightweight ref-impls

Rather than one deep reference implementation per sub-variant, TMT may benefit from three lighter-weight ref-impls that share structure. Decision: start with one (Carrier NOC), validate the pattern, then clone to the other two.

---

## Part 11 — Solution Stack (TMT)

Conforms to Core Part 13. ~55 rows reflecting three-spine coverage.

**File:** `apex-tmt/data/solution-stack.json`

---

## Part 12 — File Structure (TMT)

```
apex-tmt/
├── README.md
├── CHANGELOG.md
├── index.html
├── /data/
│   ├── forces-of-change.json
│   ├── cmm-signals.json
│   ├── schemas.json
│   ├── agents.json
│   ├── orchestrations.json
│   ├── tools.json
│   ├── isv-ecosystem.json
│   ├── waves.json
│   ├── ref-implementations.json
│   └── solution-stack.json
└── /ref-impl/
    ├── /carrier-noc/
    ├── /streaming-ops/
    └── /saas-success/
```

---

## Part 13 — Build Sequence

Six phases, mirroring RC/TH. TMT adds a **three-way sub-variant selector** in the framework site masthead (TEL / MED / TEC).

---

## Part 14 — Acceptance Criteria

1. ☐ `apex-tmt/` folder parallel to `apex-core/`
2. ☐ README declares TMT code, version, Core spec, sub-variants
3. ☐ 10 Forces of Change
4. ☐ Eras and CMM unchanged; signals added
5. ☐ 5 schemas (CLTML, COMML, NETML, CNTML, PRDML)
6. ☐ Envelope inherited unchanged with TMT vocab
7. ☐ 12 ORCHs (ORCH-03 reserved)
8. ☐ MCP catalog with TMT domain codes
9. ☐ Design system with `--tmt-accent`
10. ☐ Core widgets consumed
11. ☐ Compliance lint passes
12. ☐ Solution Stack ≥55 rows
13. ☐ Three reference implementations planned

---

## Part 15 — TMT-Specific Design Considerations

### 15.1 Voice

- **TEL:** NOC-ops tempo — precise, minute-to-minute, incident-oriented
- **MED:** Creative-ops tempo — editorial, audience-aware, brand-sensitive
- **TEC:** Platform-ops tempo — customer-success driven, SLA-conscious, developer-empathetic

### 15.2 Speed and subscription economics as narrative spine

Every TMT reference implementation should lead with **a lifecycle event** — a signup, a churn signal, an outage, a content launch, a feature rollout — because that's what TMT runs on. The framing should never be "transaction volume" or "inventory position"; it's always "subscriber moment" or "customer moment."

### 15.3 The TEC sub-variant warning

Technology (TEC) sits closer to industrial/B2B patterns than to Telecom or Media in some respects (enterprise sales motion, B2B customer success, long-tail developer engagement). If TEC pursuits drive enough work, consider promoting TEC to its own edition (APEX-TEC) in a future Core amendment. For now, TEC remains in TMT with the understanding that it's the highest-divergence sub-variant.

---

## Part 16 — Handoff Notes to Claude Code

**Three-way sub-variant complexity.** TMT is the most sub-variant-complex edition in APEX. Every content decision must be tagged `sub_variant: "TEL" | "MED" | "TEC" | "ALL"`. The framework site filters on this tag; get the tagging right or the UX collapses.

**Spine schemas are where specialization happens.** CLTML and COMML are shared; NETML/CNTML/PRDML each carry their sub-variant's operational spine. Don't force all three into one schema — they diverge enough that joining would produce meaningless hybrid entities.

**Rights and privacy compliance.** TMT demos must be scrupulous about fictional content titles, synthetic subscriber IDs, and consent-posture language. The lint tool should flag any non-synthetic-looking identifiers in demo data.

---

**End of APEX-TMT specification · v1.0**

*Parent:* `apex-core-build-spec.md` v1.0
