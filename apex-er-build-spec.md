# APEX · Energy & Resources Edition (APEX-ER)
## Edition Build Specification

**Spec version:** 1.0
**Parent spec:** `apex-core-build-spec.md` — **REQUIRED READING BEFORE THIS DOCUMENT**
**Edition code:** ER
**Edition accent token:** `--er-accent: #ea580c` (ember-burnished — industrial heat, horizon light)
**Status:** Planned build
**Sub-variants:** `ER-OG` (Oil & Gas), `ER-PU` (Power & Utilities), `ER-MN` (Mining & Metals)

---

## Part 0 — Inheritance Declaration

This spec inherits from APEX Core v1.2 unchanged.

**Manifest:** `apex-er/data/schemas.manifest.json` — conforms to the Core v1.2 schema-manifest contract (to be populated).

**Inheritance map:**

| Core Part | Inherited |
|---|---|
| 0 | Compliance & language constraints (immutable) |
| 3 | Forces of Change framing |
| 4 | AI Journey Eras (unchanged) |
| 5 | CMM stages (unchanged; edition adds signals) |
| 6 | Reference architecture |
| 7 | Schema naming, medallion, envelope |
| 8 | ORCH + MCP + HITL taxonomy |
| 9 | Design system (extended with `--er-accent`) |
| 10 | Reusable widgets |
| 12 | Wave deployment model |
| 13 | Solution Stack shape |

**ER-specific compliance additions:**

1. **Safety-critical posture.** Any agent whose decision could affect human safety, environmental integrity, or infrastructure integrity operates under **validated-workflow constraints** with full audit trails. "Safety-critical" is a binary attribute on every agent spec — true or false; if true, deployment requires formal HAZOP-style review.
2. **Operational technology (OT) isolation.** Agents interact with OT/SCADA systems through **read-only surfaces** by default. Write-back capabilities require explicit edition-level approval and are never enabled in demo / reference implementations.
3. **Environmental reporting accuracy.** Demo data for emissions, water, or regulatory filings must be clearly synthetic. ER operates in a regulatory space where fabricated numbers could be misread as real claims.
4. **Critical infrastructure classification.** Agent design must respect that the underlying assets are often classified as critical national infrastructure — discussion of vulnerability patterns, even in hypotheticals, is out of scope.

---

## Part 1 — Edition Positioning

### 1.1 What APEX-ER is

APEX-ER is the APEX instantiation tuned to **energy and resources enterprises** — integrated oil and gas operators, independents and services companies, regulated and deregulated utilities (electric, gas, water), renewable developers and independent power producers, and mining and metals companies.

### 1.2 Primary audiences

**Oil & Gas (ER-OG):** Chief Operating Officers, Chief Technology Officers, Upstream / Midstream / Downstream VPs, HSE leadership, Digital Transformation Officers.

**Power & Utilities (ER-PU):** Chief Operating Officers, Grid Operations leaders, Chief Customer Officers, Regulatory Affairs leaders, VPs of Distribution and Generation.

**Mining & Metals (ER-MN):** Chief Operating Officers, VPs of Operations, Heads of Mine Planning, Chief Sustainability Officers, Safety leaders.

### 1.3 Operating zone

APEX-ER delivers Era 4 (Agentic) outcomes in physical asset operations, commercial optimization, and sustainability reporting. Like HLS, ER operates at a **higher HITL rate** than consumer-facing editions — safety-critical and environment-critical decisions always route through qualified humans.

### 1.4 Why ER demands its own edition

ER differs structurally from other APEX editions in five ways:

1. **Physical-asset-heavy operations** — the scoreboard is asset availability, throughput, and integrity, not transactions or subscribers
2. **OT/IT convergence is the dominant data fabric challenge** — historians, SCADA, PLCs, control systems, industrial IoT at a scale no other industry operates
3. **Commodity economics** — price is exogenous; operational excellence is the lever
4. **Safety, environment, and community-license-to-operate** are first-order operational concerns, not CSR overlays
5. **The energy transition is a simultaneous operating and strategic challenge** — running hydrocarbons while building renewables, or managing the distribution network through a demand-shape transformation

### 1.5 Three sub-variants, one edition

Oil & Gas, Power & Utilities, and Mining & Metals share the physical-asset spine, the OT/IT convergence pattern, the safety-and-environment posture, and the commodity-economics framing. They differ in their product/flow and regulatory specifics. One edition, three sub-variants.

---

## Part 2 — Forces of Change (Energy & Resources)

| id | force | signal | implication |
|---|---|---|---|
| FOC-01 | Energy Transition & Decarbonization | Hydrocarbon demand plateauing in key markets; renewables cost curve; carbon pricing expansion; scope-3 accountability | Agents must reason over transition economics, not only current operating models |
| FOC-02 | Aging Infrastructure & Workforce | Pipeline, grid, and asset vintage profiles; retirement-wave workforce exits; knowledge-capture urgency | Predictive-maintenance and knowledge-retrieval agents become workforce-continuity tools |
| FOC-03 | Grid Complexity & Bidirectional Flow | DER penetration; EV load growth; prosumer dynamics; demand response scaling | Grid-operations agents must handle orders-of-magnitude more control points than legacy tools |
| FOC-04 | Extreme Weather & Climate Resilience | Wildfire liability (utilities); hurricane impact (upstream and coastal infrastructure); drought (mining water rights) | Weather-aware operational agents become safety and liability management, not optimization |
| FOC-05 | Commodity Price Volatility | Geopolitical shock cycles; OPEC+ dynamics; critical-minerals concentration | Commercial and trading agents must operate at intra-hour decisioning with risk guardrails |
| FOC-06 | OT/IT Convergence & Cyber | Targeted attacks on OT; ICS-specific threat surface; regulatory frameworks (CIP, NIS2) | Identity, access, and anomaly-detection agents are safety features in ER |
| FOC-07 | Sustainability & ESG Reporting Mandates | CSRD, SEC climate disclosure, mandatory scope-3 reporting, TCFD, biodiversity frameworks | Reporting agents move from annual to continuous; auditability is first-class |
| FOC-08 | Community & License-to-Operate | Indigenous consultation; local regulatory resistance; social media velocity; ESG investor scrutiny | Stakeholder-engagement agents operate across jurisdictions and cultures |
| FOC-09 | Capital Allocation Discipline | Shareholder return pressure; project scrutiny; brownfield vs. greenfield trade-offs | Investment and opportunity agents must produce defensible economics quickly |
| FOC-10 | Digital Twins & Industrial AI Maturity | Proliferation of high-fidelity twins; physics-informed ML; edge compute in operations | Agentic decisioning connects to twin-based simulation, not just historical data |

**File:** `apex-er/data/forces-of-change.json`

---

## Part 3 — CMM Signal Extensions for ER

| stage | er signals |
|---|---|
| CMM-1 Foundations | ERP + CMMS + historians exist; reporting is largely manual; OT data siloed |
| CMM-2 Connected | Real-time historian-to-data-lake pipelines; predictive maintenance models piloted; integrated planning systems online |
| CMM-3 Intelligent | Copilots for operators / planners / engineers; digital twin integrated with live data in key assets |
| CMM-4 Agentic | Autonomous production optimization within guardrails; autonomous grid balancing for bounded scenarios; sustainability reporting automated end-to-end |
| CMM-5 Adaptive | Continuous-learning fleet operations; cross-asset optimization; fleet-level learnings applied to new greenfield developments without human porting |

**File:** `apex-er/data/cmm-signals.json`

---

## Part 4 — Canonical Schemas (Energy & Resources)

| schema | domain | scope | sub_variants | target_entity_count |
|---|---|---|---|---|
| **ASTML** | Asset & Operations | Asset hierarchy, performance telemetry, reliability events, work orders, integrity events | ALL | ~45 |
| **PRODML** | Production & Flow | Production / generation events, throughput, losses, routing decisions (oil/gas flow, grid power flow, ore movement) | ALL | ~35 |
| **CMRML** | Commercial & Markets | Trading positions, hedges, contracts, settlement, load forecasts | ALL | ~30 |
| **SEHML** | Safety, Environment & HSE | HSE events, incidents, near-misses, environmental telemetry, permit-to-work, isolation records | ALL | ~30 |
| **SUSML** | Sustainability & ESG | Emissions (scope 1/2/3), water, waste, biodiversity, community engagement, reporting artifacts | ALL | ~25 |

All five schemas shared across sub-variants, with sub-variant-specific entities within each.

### 4.1 Dimensional anchors

**Shared:**
`DIM_ASSET`, `DIM_FACILITY`, `DIM_EQUIPMENT`, `DIM_OPERATOR`, `DIM_SHIFT`, `DIM_UNIT_OF_MEASURE`, `DIM_REGULATOR`, `DIM_COMMODITY`, `DIM_CURRENCY`, `DIM_DATE`, `DIM_TIME`.

**Oil & Gas:** `DIM_WELL`, `DIM_FIELD`, `DIM_BASIN`, `DIM_PIPELINE_SEGMENT`, `DIM_REFINERY_UNIT`.
**Power & Utilities:** `DIM_SUBSTATION`, `DIM_FEEDER`, `DIM_METER`, `DIM_GENERATING_UNIT`, `DIM_TERRITORY`.
**Mining & Metals:** `DIM_MINE`, `DIM_PIT`, `DIM_STOPE`, `DIM_HAUL_ROUTE`, `DIM_PROCESSING_UNIT`.

### 4.2 ER controlled vocabulary for event envelope

- `business_step`: `producing`, `transporting`, `processing`, `distributing`, `maintaining`, `inspecting`, `permitting`, `isolating`, `reporting`, `trading`, `settling`, `remediating`
- `disposition`: `operating`, `degraded`, `isolated`, `offline`, `tripped`, `remediated`, `pending_maintenance`, `abnormal`, `reported`, `settled`

### 4.3 Key entities (summary)

**ASTML:** `ASSET`, `EQUIPMENT`, `CONDITION_TELEMETRY`, `RELIABILITY_EVENT`, `WORK_ORDER`, `MAINTENANCE_EVENT`, `INSPECTION_EVENT`, `INTEGRITY_EVENT`, `ANOMALY`, plus ~36 more.

**PRODML:** `PRODUCTION_EVENT`, `GENERATION_EVENT` (PU), `EXTRACTION_EVENT` (MN), `THROUGHPUT_RECORD`, `LOSS_EVENT`, `FLOW_ROUTING_DECISION`, `DISPATCH_ORDER` (PU), `HAUL_CYCLE` (MN), plus ~27 more.

**CMRML:** `TRADE`, `POSITION`, `HEDGE`, `CONTRACT`, `NOMINATION` (OG pipeline), `SCHEDULE` (PU), `SETTLEMENT_EVENT`, `LOAD_FORECAST` (PU), plus ~22 more.

**SEHML:** `HSE_EVENT`, `NEAR_MISS`, `INCIDENT`, `ENV_TELEMETRY`, `EMISSION_EVENT`, `PERMIT_TO_WORK`, `ISOLATION_RECORD`, `LOCKOUT_TAGOUT`, plus ~22 more.

**SUSML:** `EMISSION_RECORD` (scope 1/2/3), `WATER_USAGE`, `WASTE_EVENT`, `BIODIVERSITY_OBSERVATION`, `COMMUNITY_ENGAGEMENT`, `DISCLOSURE_ARTIFACT`, plus ~19 more.

---

## Part 5 — Domain Architectures (32 Agents)

Four domains. 32 agents.

### 5.1 Asset Operations Domain (12 agents)

**Primary schema:** ASTML. **Consumed schemas:** PRODML, SEHML.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| AST-A01 | Predictive Maintenance Agent | multi-signal fusion, failure-mode classifier, lead-time estimator | ORCH-07 |
| AST-A02 | Condition Monitoring Agent | vibration/thermal/acoustic trend, anomaly scorer, severity classifier | ORCH-07 |
| AST-A03 | Work Order Optimizer | priority scorer, resource matcher, window scheduler | ORCH-07 |
| AST-A04 | Integrity Management Agent | corrosion / erosion / fatigue model, inspection-planner, deferral risk scorer | (platform) |
| AST-A05 | Reliability Root-Cause Agent | failure-mode-effect analyzer, precedent retriever, CAPA drafter | ORCH-08 |
| AST-A06 | Spare Parts Agent | consumption-pattern learner, stocking-level optimizer | (platform) |
| AST-A07 | Turnaround Planner | scope-aggregator, critical-path analyzer, risk scorer | (platform) |
| AST-A08 | Operator Rounds Copilot | route optimizer, observation prompter, anomaly-intake | ORCH-01 |
| AST-A09 | Asset Digital Twin Bridge | live-to-twin state sync, scenario comparator | (platform) |
| AST-A10 | Mobile Worker Dispatch | skill-match router, travel-time optimizer | ORCH-07 |
| AST-A11 | Inspection Evidence Agent | image/data classifier, compliance-evidence packager | ORCH-09 |
| AST-A12 | Isolation & LOTO Agent | permit-validator, conflict detector, isolation-state tracker | (platform) |

### 5.2 Production / Grid / Mine Operations Domain (8 agents)

**Primary schema:** PRODML. **Consumed schemas:** ASTML, CMRML.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| PRD-A01 | Production Optimization Agent | setpoint recommender, constraint-aware optimizer, opportunity detector | ORCH-02 |
| PRD-A02 | Flow Routing Agent (OG) | pipeline-balance optimizer, nomination-conflict resolver | ORCH-02 |
| PRD-A03 | Grid Dispatch Agent (PU) | reserve-margin monitor, contingency-dispatch recommender | ORCH-02 |
| PRD-A04 | Haul & Material Flow Agent (MN) | cycle-time optimizer, dispatch coordinator | ORCH-02 |
| PRD-A05 | Loss Accounting Agent | gain/loss reconciler, anomaly flagger, attribution composer | (platform) |
| PRD-A06 | Demand Response / Load-Shape Agent (PU) | portfolio-optimizer, customer-level incentive router | ORCH-10 |
| PRD-A07 | Storage Management Agent | tankage / battery / inventory optimizer, schedule integrator | (platform) |
| PRD-A08 | Outage Coordinator | planned-vs-forced harmonizer, customer-impact communicator | ORCH-05 |

### 5.3 Safety, Environment & HSE Domain (6 agents)

**Primary schema:** SEHML. **Consumed schemas:** ASTML, PRODML.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| HSE-A01 | HSE Event Intake Agent | multi-source classifier (report, sensor, video), severity scorer, stakeholder router | ORCH-08 |
| HSE-A02 | Near-Miss Pattern Agent | cross-asset / cross-site pattern detector, precursor-signal analyzer | ORCH-08 |
| HSE-A03 | Environmental Telemetry Agent | limit-monitor, excursion classifier, regulatory-report primer | ORCH-08 |
| HSE-A04 | Permit & Isolation Agent | validity checker, conflict detector, SIMOPs coordinator | (platform) |
| HSE-A05 | Incident Investigation Agent | evidence-timeline assembler, root-cause-candidate generator | ORCH-08 |
| HSE-A06 | Safety Copilot | procedure-retriever, context-aware reminder, HITL-gate orchestrator | (experience) |

### 5.4 Commercial, Sustainability & Reporting Domain (6 agents)

**Primary schemas:** CMRML, SUSML.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| CMS-A01 | Trading Desk Copilot | position-context, scenario analyzer, P&L attribution | ORCH-06 |
| CMS-A02 | Hedge Optimization Agent | exposure-aggregator, strategy simulator, guardrail enforcer | ORCH-06 |
| CMS-A03 | Settlement Reconciliation Agent | multi-counterparty matcher, discrepancy flagger | (platform) |
| CMS-A04 | Emissions Reporting Agent | scope 1/2/3 aggregator, uncertainty quantifier, auditor-ready evidencer | ORCH-09 |
| CMS-A05 | ESG Disclosure Agent | framework-mapper (CSRD/SEC/TCFD), assurance-ready packager | ORCH-09 |
| CMS-A06 | Community Engagement Agent | stakeholder-sentiment monitor, inquiry router, commitment tracker | ORCH-12 |

---

## Part 6 — Orchestrations (ER)

| orch_id | name | domain | sub_variant | agents | trigger | primary_gold_view | cycle_time_slo |
|---|---|---|---|---|---|---|---|
| ORCH-01 | Operator Rounds / Shift Start | AST | ALL | AST-A08 | Shift start / rounds event | GV_ASSET_ROUND | Rounds-driven |
| ORCH-02 | Production / Dispatch Optimization | PRD | ALL | PRD-A01, PRD-A02, PRD-A03, PRD-A04 | Optimization cycle OR constraint change | GV_PRODUCTION_OPTIM | < 15 min decision cycle |
| ORCH-03 | (Reserved slot) | — | — | — | — | — | — |
| ORCH-04 | Asset Health & Throughput | AST/PRD | ALL | AST-A01, AST-A02 | Condition anomaly / throughput deviation | GV_ASSET_HEALTH | < 5 min to alert |
| ORCH-05 | Outage & Disruption Response | PRD/AST | ALL | PRD-A08, AST-A10 | Unplanned outage / grid event / pipeline break | GV_OUTAGE_IMPACT | < 10 min to scope |
| ORCH-06 | Trading & Commercial Decisioning | CMS | ALL | CMS-A01, CMS-A02 | Market event / position drift | GV_COMMERCIAL_POSITION | Intra-hour |
| ORCH-07 | Maintenance & Work Execution | AST | ALL | AST-A01, AST-A03, AST-A10 | Maintenance trigger / work request | GV_WORK_PIPELINE | < 15 min to dispatch |
| ORCH-08 | Safety & HSE Event | HSE | ALL | HSE-A01, HSE-A02, HSE-A05, AST-A05 | HSE event / near-miss / environmental limit | GV_HSE_CASES | < 5 min to hold/isolate |
| ORCH-09 | Regulatory Reporting & Disclosure | CMS/HSE | ALL | AST-A11, CMS-A04, CMS-A05 | Reporting trigger / submission milestone | GV_DISCLOSURE_PIPELINE | Cycle-driven |
| ORCH-10 | Demand / Load Sensing | PRD | PU | PRD-A06 | Continuous signal fusion | GV_LOAD_SIGNAL | 15-min cadence |
| ORCH-11 | (Reserved slot) | — | — | — | — | — | — |
| ORCH-12 | Stakeholder & Community | CMS | ALL | CMS-A06 | Inquiry / event trigger | GV_STAKEHOLDER_QUEUE | Event-driven |

Note: ORCH-03 and ORCH-11 reserved for future ER expansion.

**File:** `apex-er/data/orchestrations.json`

---

## Part 7 — MCP Tool Catalog (ER)

### 7.1 ER domain codes

| code | scope |
|---|---|
| `mcp.asset.*` | Asset-scoped operations |
| `mcp.equipment.*` | Equipment-scoped operations |
| `mcp.facility.*` | Facility-scoped operations |
| `mcp.well.*` | Well-scoped (OG) |
| `mcp.pipeline.*` | Pipeline / gathering (OG) |
| `mcp.refinery.*` | Refinery operations (OG) |
| `mcp.grid.*` | Grid operations (PU) |
| `mcp.substation.*` | Substation scope (PU) |
| `mcp.generation.*` | Generation unit (PU) |
| `mcp.meter.*` | Meter / AMI (PU) |
| `mcp.mine.*` | Mine-scoped (MN) |
| `mcp.haul.*` | Haul / material flow (MN) |
| `mcp.process.*` | Process unit operations |
| `mcp.work.*` | Work order / maintenance operations |
| `mcp.hse.*` | HSE operations |
| `mcp.permit.*` | Permit-to-work / isolation operations |
| `mcp.emissions.*` | Emissions reporting operations |
| `mcp.trade.*` | Trading operations |
| `mcp.settlement.*` | Settlement operations |

### 7.2 Catalog target

Initial catalog: ~65 tools reflecting the breadth of physical-asset operations.

**File:** `apex-er/data/tools.json`

---

## Part 8 — ISV Ecosystem (ER)

| category | isv_examples | microsoft_integration |
|---|---|---|
| ERP — Asset-Intensive | SAP S/4HANA, Oracle Fusion Cloud | API / Fabric |
| EAM / CMMS | IBM Maximo, Hexagon EAM, GE APM | API |
| Historian / Operations Data | AVEVA PI System, GE Proficy, Wonderware | API / ADX |
| SCADA / DCS | Schneider, ABB, Emerson, Siemens, Honeywell | Azure IoT |
| Upstream (OG) | AspenTech, IHS Markit / S&P, Halliburton Landmark | API |
| Refining / Petrochem | AspenTech, Honeywell UOP, KBC | API |
| Power / Utilities | Oracle Utilities, Itron, Landis+Gyr, Schneider Grid | API |
| Mining Planning & Fleet Mgmt | Komatsu Modular, Caterpillar MineStar, Hexagon MinePlan, Dassault GEOVIA | API |
| Trading & Risk | Openlink, ION Triple Point, Allegro (ION) | API |
| HSE | Intelex, Enablon (Wolters Kluwer), Sphera | API |
| ESG / Sustainability | Sphera, Workiva, Greenstone, Watershed | Fabric |
| Digital Twin | Siemens NX / Teamcenter, Bentley iTwin, Dassault 3DEXPERIENCE | API |
| OT Security | Claroty, Nozomi, Dragos | Native / API |
| Geospatial | ESRI ArcGIS, Hexagon Luciad | API |

**File:** `apex-er/data/isv-ecosystem.json`

---

## Part 9 — Wave Content (ER)

| wave | name | scope | duration | entry | exit | economic_case |
|---|---|---|---|---|---|---|
| W1 | Foundation | L1–L4 stand-up; ASTML + SEHML Silver/Gold; first 3–5 agents (PdM, rounds copilot, HSE intake); pilot in 1–3 assets/sites | 6–9 mo | CMM-1 or CMM-2 | CMM-3 readiness | Maintenance-cost reduction + HSE cycle-time + rounds productivity — validated-workflow evidence |
| W2 | Expansion | PRODML + CMRML canonical; first full domain ORCH stack; 10–15 agents | 9–12 mo | CMM-3 | Early CMM-4 | Production uplift + unplanned-downtime reduction + emissions accuracy |
| W3 | Platform | Cross-domain ORCHs; full 32-agent fleet; enterprise rollout | 12–18 mo | CMM-4 entry | CMM-4 full | Enterprise asset optimization; commercial-operational integration |
| W4 | Adaptive | Continuous learning; fleet self-optimization within OT-safety envelope | Ongoing | CMM-4 | CMM-5 | Compounding returns across asset fleet |

ER waves run long (like HLS) because validation and OT change-control discipline gate production deployments.

**File:** `apex-er/data/waves.json`

---

## Part 10 — Reference Implementations (ER)

| ref_impl | scope | sub_variant | status | spec |
|---|---|---|---|---|
| **Offshore Platform Charlie Day-in-OIM-Seat** | Offshore oil & gas platform, single operational day, 8 events across AST/PRD/HSE | OG | Planned | TBD |
| **Control Center Gamma Day-in-Ops** | Utility distribution control center, 8 grid/customer events | PU | Planned | TBD |
| **Mine Site Delta Day-in-Ops** | Open-pit mine, 8 operational events | MN | Planned | TBD |

**File:** `apex-er/data/ref-implementations.json`

### 10.1 Three sub-variant reference implementations

Like TMT, ER benefits from one reference implementation per sub-variant because the operational spines diverge enough that a single demo cannot represent the edition. Unlike TMT, ER ref-impls carry heavier safety-and-validation framing in their content.

---

## Part 11 — Solution Stack (ER)

~60 rows.

**File:** `apex-er/data/solution-stack.json`

---

## Part 12 — File Structure (ER)

```
apex-er/
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
    ├── /platform-charlie/
    ├── /control-center-gamma/
    └── /mine-site-delta/
```

---

## Part 13 — Build Sequence

Six phases. Three-way sub-variant selector in masthead (OG / PU / MN).

---

## Part 14 — Acceptance Criteria

1. ☐ `apex-er/` folder
2. ☐ README, code ER, sub-variants
3. ☐ 10 Forces of Change
4. ☐ Eras / CMM referenced unchanged
5. ☐ 5 schemas (ASTML, PRODML, CMRML, SEHML, SUSML)
6. ☐ Envelope inherited with ER vocabulary
7. ☐ 12 ORCHs (ORCH-03 and ORCH-11 reserved)
8. ☐ MCP catalog with ER domain codes
9. ☐ `--er-accent` added
10. ☐ Core widgets consumed
11. ☐ Compliance lint passes (both Core and ER additions)
12. ☐ Solution Stack ≥60 rows
13. ☐ Three reference implementations planned

---

## Part 15 — ER-Specific Design Considerations

### 15.1 Voice

- **OG:** Platform-OIM / control-room operator tempo — drilled procedures, clipped radio protocol, deep respect for asset integrity and crew
- **PU:** Grid-operator tempo — minute-to-minute vigilance, N-1 contingency awareness, public-safety consciousness
- **MN:** Mine-site-supervisor tempo — shift-scoped planning, haul-cycle discipline, safety-above-tonnage culture

### 15.2 Safety framing in reference implementations

Every ER ref-impl should lead its summary with **safety and environmental integrity outcomes** alongside operational and financial metrics. "Zero safety incidents, X% emissions reduction, Y% unplanned downtime avoided, $Z production uplift" — in that order.

### 15.3 OT discipline is visible in the framework

The framework site should make it visually clear which agents operate in read-only OT-adjacent roles vs. write-enabled roles (almost none, by design). This is a credibility signal to ER SteerCos who carry cyber-and-safety accountability.

### 15.4 Energy transition as a framing layer

Unlike retail or hospitality, ER has a **strategic fork**: legacy operations and transition operations run simultaneously. The framework should surface this through explicit "transition readiness" tagging on relevant agents — which ones accelerate decarbonization, which ones optimize current operations, which ones do both.

---

## Part 16 — Handoff Notes to Claude Code

**OT / IT convergence is the distinguishing technical story.** The framework site must treat L1 (Edge & Source) as more detailed than in RC or TH — historians, SCADA, DCS, industrial IoT are first-class, not line items. Give this layer visual space.

**Safety-critical tagging.** Every agent in `agents.json` carries a `safety_critical: true | false` attribute. The Solution Stack Chart filters and the agent tabs expose this visibly. Agents tagged `safety_critical: true` render with a distinct badge.

**Three-way sub-variant complexity.** Same as TMT — tag everything `sub_variant: "OG" | "PU" | "MN" | "ALL"` and filter.

**Validation footprint shown.** Like HLS, ER carries a validation footprint. Expose it in the framework site — don't hide it in footnotes.

---

**End of APEX-ER specification · v1.0**

*Parent:* `apex-core-build-spec.md` v1.0
