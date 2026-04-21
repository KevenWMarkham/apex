# APEX · Industrial & Commercial Equipment Edition (APEX-ICE)
## Edition Build Specification

**Spec version:** 1.0
**Parent spec:** `apex-core-build-spec.md` — **REQUIRED READING BEFORE THIS DOCUMENT**
**Edition code:** ICE
**Edition accent token:** `--ice-accent: #0f766e` (deep teal-industrial — precision, engineered durability)
**Status:** Planned build
**Sub-variants:** Single edition (sub-variants may split in future: `ICE-HVY` Heavy Equipment, `ICE-AD` Aerospace & Defense, `ICE-AUT` Automotive)

---

## Part 0 — Inheritance Declaration

This spec inherits from APEX Core v1.2 unchanged.

**Manifest:** `apex-ice/data/schemas.manifest.json` — conforms to the Core v1.2 schema-manifest contract (to be populated).

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
| 9 | Design system (extended with `--ice-accent`) |
| 10 | Reusable widgets |
| 12 | Wave deployment model |
| 13 | Solution Stack shape |

**ICE-specific compliance additions:**

1. **Export controls** — any demo referencing defense, dual-use, or export-controlled products must avoid specific defense article references (ITAR/EAR classifications), specific weapon systems, specific export markets. Use deliberately generic product categories.
2. **Warranty & liability framing** — agent-generated recommendations touching product-liability-sensitive domains (diagnostics, failure analysis, service-bulletin triggers) operate under HITL gates with documented human sign-off.
3. **Product serialization & traceability** — synthetic identifiers only in demo data (serial patterns like `SN-DEMO-X001`).

---

## Part 1 — Edition Positioning

### 1.1 What APEX-ICE is

APEX-ICE is the APEX instantiation tuned to **industrial and commercial equipment manufacturers** — heavy equipment (construction, agriculture, mining equipment), aerospace & defense equipment, automotive OEMs and tier suppliers, commercial HVAC and building systems, industrial machinery, and capital equipment makers whose business combines engineered products with long service lifecycles.

### 1.2 Primary audiences

- Chief Operating Officers at OEMs and tier suppliers
- Chief Commercial Officers and Aftermarket / Service VPs
- Chief Product Officers / Chief Engineers
- Chief Digital Officers pursuing connected-product strategies
- Dealer and distributor network operations leaders

### 1.3 Operating zone

APEX-ICE delivers Era 4 (Agentic) outcomes across engineered-product lifecycle, connected-product telemetry, aftermarket service, and dealer/distributor operations. HITL rate is elevated in liability-sensitive contexts (diagnostics, field-service recommendations, product-bulletin triggers).

### 1.4 Why ICE demands its own edition

ICE differs from other APEX editions in four structural ways:

1. **The unit of economics is the product across its lifecycle** — new-machine sale, financing, service, parts, upgrades, trade-in, remanufacturing — aftermarket is often the dominant profit pool
2. **Connected products are the spine** — telemetry from the product in the field is the core data asset, enabling predictive service, usage-based offers, and product intelligence
3. **Dealer / distributor networks intermediate almost everything** — the OEM's customer experience is filtered through an independent network
4. **Configure-to-order and engineer-to-order manufacturing** — no two shipped machines are identical; the bill of materials, software configuration, and service history are product-unit-specific

### 1.5 Single edition for now

Unlike HLS, TMT, ER which have formal sub-variants from day one, ICE starts as a single edition. The reason: heavy equipment, aerospace & defense, automotive, and commercial HVAC share enough operational DNA that one edition serves them. If one sub-variant (most likely Aerospace & Defense, with its heavier regulatory and export-control posture) generates enough distinctive work, a future Core amendment may promote it to a sub-variant tag. Decision deferred.

---

## Part 2 — Forces of Change (Industrial & Commercial Equipment)

| id | force | signal | implication |
|---|---|---|---|
| FOC-01 | Aftermarket as Profit Engine | Service, parts, and subscriptions outpacing new-machine revenue in growth; OEMs competing on uptime, not specs | Service and parts agents become revenue agents, not cost agents |
| FOC-02 | Connected Product Ubiquity | Telematics in every machine; over-the-air software updates; fleet management as standard | Telemetry-driven agents operate on product-level data at massive scale |
| FOC-03 | Dealer Network Pressure | Consolidation; direct-to-customer disintermediation by OEMs; dealer economics squeezed | Dealer-enablement and channel-optimization agents move from optional to strategic |
| FOC-04 | Configuration Complexity | Engineered-to-order variance; software-defined product differentiation; variant explosion | Configuration and serviceability agents must reason over product-unit-specific context |
| FOC-05 | Supply Chain Resilience | Semi-shortage hangover; tier-N visibility demands; friendshoring / reshoring dynamics | Multi-tier supplier and inventory agents move from quarterly planning to continuous |
| FOC-06 | Sustainability & Circular Product Flows | Remanufacturing scaling; product-as-a-service offerings; Right-to-Repair legislation; carbon-aware manufacturing | Lifecycle and circularity agents become first-class domain |
| FOC-07 | Electrification & Autonomy | EV transition across vehicle / equipment categories; autonomy programs in commercial and construction | Product-data and service-network agents must adapt to new physics (batteries vs. combustion; software vs. mechanical failure modes) |
| FOC-08 | Labor Scarcity & Technician Skills Gap | Service technician shortage; legacy-technician retirement; apprenticeship crisis | Technician-augmentation agents become workforce continuity |
| FOC-09 | Regulatory Fragmentation | Emissions standards variance; A&D export controls; EV incentive complexity; medical-device-like scrutiny on safety systems | Compliance and regulatory agents navigate multi-jurisdictional rules |
| FOC-10 | Data Sovereignty Between OEM, Dealer, Customer | Who owns the machine data, who monetizes, who protects — unsettled across industries | Consent and data-governance agents are enterprise-strategic, not compliance-line-items |

**File:** `apex-ice/data/forces-of-change.json`

---

## Part 3 — CMM Signal Extensions for ICE

| stage | ice signals |
|---|---|
| CMM-1 Foundations | ERP + DMS (dealer management system) + PLM in place; telematics data siloed in OEM platform; service events reported retrospectively |
| CMM-2 Connected | Real-time telematics fabric; predictive maintenance piloted on selected fleets; parts-demand forecasting with ML |
| CMM-3 Intelligent | Service copilots for dealer technicians; warranty-claim automation; configuration assistants |
| CMM-4 Agentic | Autonomous warranty / service-bulletin triage; product-as-a-service billing agents; multi-tier supply chain agents handling exceptions |
| CMM-5 Adaptive | Continuous-learning service fleets; configuration optimization fed back to engineering; dealer-network performance self-improves |

**File:** `apex-ice/data/cmm-signals.json`

---

## Part 4 — Canonical Schemas (ICE)

| schema | domain | scope | target_entity_count |
|---|---|---|---|
| **PRDML** | Product & Engineering | BOM, configuration, variant, engineering change, release, software release | ~35 |
| **CPTML** | Connected Product Telemetry | Asset unit, telemetry, events, fault codes, diagnostic trouble codes (DTC), OTA state | ~40 |
| **AMSML** | Aftermarket Service | Service events, warranty claims, service bulletins, parts transactions, repair orders, technician events | ~40 |
| **SCML** | Supply Chain & Manufacturing | Supplier, multi-tier visibility, manufacturing orders, quality events, logistics events | ~35 |
| **CHNML** | Channel & Commerce | Dealer/distributor, configure-price-quote, order, delivery, financing, customer (end-user) | ~30 |

### 4.1 Dimensional anchors

`DIM_PRODUCT_FAMILY`, `DIM_PRODUCT_VARIANT`, `DIM_SERIAL_UNIT` (the individual machine), `DIM_CUSTOMER`, `DIM_DEALER`, `DIM_DEALER_LOCATION`, `DIM_SUPPLIER`, `DIM_PART`, `DIM_TECHNICIAN`, `DIM_SERVICE_BAY`, `DIM_MANUFACTURING_PLANT`, `DIM_GEOGRAPHY`, `DIM_DATE`, `DIM_TIME`.

### 4.2 ICE controlled vocabulary for event envelope

- `business_step`: `designing`, `configuring`, `ordering`, `manufacturing`, `shipping`, `delivering`, `commissioning`, `operating`, `servicing`, `repairing`, `upgrading`, `remanufacturing`, `retiring`, `claiming`, `billing`
- `disposition`: `in_design`, `in_production`, `shipped`, `in_service`, `under_warranty`, `out_of_warranty`, `service_pending`, `retired`, `remanufactured`

### 4.3 Key entities (summary)

**PRDML:** `PRODUCT_FAMILY`, `VARIANT`, `BOM`, `CONFIGURATION_SPEC`, `ENGINEERING_CHANGE`, `SOFTWARE_RELEASE`, `DESIGN_PARAMETER`, plus ~28 more.

**CPTML:** `SERIAL_UNIT`, `TELEMETRY_STREAM`, `OPERATING_EVENT`, `FAULT_CODE`, `DTC_EVENT`, `OTA_PUSH`, `OTA_STATE`, `UTILIZATION_RECORD`, `USAGE_CYCLE`, plus ~31 more.

**AMSML:** `SERVICE_EVENT`, `REPAIR_ORDER`, `WARRANTY_CLAIM`, `SERVICE_BULLETIN`, `PART_TRANSACTION`, `TECHNICIAN_EVENT`, `DIAGNOSTIC_SESSION`, `CAMPAIGN_EVENT` (recall/campaign), plus ~32 more.

**SCML:** `SUPPLIER`, `PURCHASE_ORDER`, `MANUFACTURING_ORDER`, `QUALITY_EVENT`, `LOGISTICS_EVENT`, `TIER_N_SIGNAL`, `COMPONENT_INVENTORY`, plus ~28 more.

**CHNML:** `DEALER`, `QUOTE`, `ORDER`, `DELIVERY`, `FINANCING_AGREEMENT`, `END_USER`, `CUSTOMER_INTERACTION`, plus ~23 more.

---

## Part 5 — Domain Architectures (32 Agents)

Four domains. 32 agents.

### 5.1 Connected Product & Engineering Domain (10 agents)

**Primary schemas:** PRDML, CPTML.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| CPR-A01 | Predictive Service Agent | failure-mode classifier from telemetry, lead-time estimator, service-window recommender | ORCH-07 |
| CPR-A02 | Fault Code Triage Agent | DTC-correlator, severity classifier, technician-action recommender | ORCH-07 |
| CPR-A03 | OTA Release Agent | rollout orchestrator, canary monitor, rollback detector | ORCH-07 |
| CPR-A04 | Product Intelligence Agent | in-field pattern detector, engineering-feedback composer | (platform) |
| CPR-A05 | Configuration Validation Agent | buildability checker, compatibility resolver, constraint verifier | ORCH-01 |
| CPR-A06 | Engineering Change Agent | change-impact analyzer, downstream-document updater, approval router | (platform) |
| CPR-A07 | Utilization Analytics Agent | usage-pattern learner, duty-cycle scorer, anomaly detector | (platform) |
| CPR-A08 | Safety Campaign Trigger Agent | field-data aggregator, campaign-threshold monitor, package builder | ORCH-05 |
| CPR-A09 | Digital Twin Bridge | as-designed / as-built / as-maintained sync | (platform) |
| CPR-A10 | Cybersecurity Agent (Connected Product) | anomaly detector on product comms, firmware integrity, threat response | ORCH-08 |

### 5.2 Aftermarket Service Domain (10 agents)

**Primary schema:** AMSML. **Consumed schemas:** CPTML, PRDML.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| AMS-A01 | Service Scheduling Agent | bay-availability matcher, technician-skill router, part-availability checker | ORCH-04 |
| AMS-A02 | Repair Order Copilot | diagnostic-question prompter, procedure retriever, labor-hours estimator | ORCH-06 |
| AMS-A03 | Warranty Claim Agent | eligibility resolver, evidence packager, fraud signal detector | ORCH-02 |
| AMS-A04 | Service Bulletin Agent | applicability resolver per serial unit, technician-notifier, compliance tracker | (platform) |
| AMS-A05 | Parts Demand Agent | forecasting, distribution optimizer, obsolescence manager | ORCH-10 |
| AMS-A06 | Technician Assist Agent | AR-instruction retriever, procedure-step prompter, expert-connect router | (experience) |
| AMS-A07 | Field Dispatch Agent | priority scorer, travel-time optimizer, truck-stock validator | ORCH-07 |
| AMS-A08 | Customer Service Interaction Agent | case-context builder, resolution-step retriever, escalation router | ORCH-06 |
| AMS-A09 | Remanufacturing Agent | core-return tracker, disassembly-decision recommender, upcycle-opportunity scorer | (platform) |
| AMS-A10 | Service Contract Agent | coverage resolver, billing-event generator, renewal opportunity scorer | ORCH-12 |

### 5.3 Manufacturing & Supply Chain Domain (6 agents)

**Primary schema:** SCML. **Consumed schemas:** PRDML, AMSML.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| MSC-A01 | Supplier Risk Agent | multi-tier signal aggregator, disruption predictor, alt-sourcing scorer | (platform) |
| MSC-A02 | Production Schedule Agent | capacity-constraint optimizer, change-order accommodator | ORCH-02 |
| MSC-A03 | Quality Event Agent | deviation classifier, containment-scope analyzer, root-cause candidate generator | ORCH-08 |
| MSC-A04 | Inventory Optimization Agent | multi-echelon optimizer, obsolescence detector | (platform) |
| MSC-A05 | Logistics Exception Agent | delay detector, rerouting optimizer, customer-impact communicator | ORCH-07 |
| MSC-A06 | Configuration-Aware Procurement Agent | variant-specific sourcing, supplier-capability matcher | (platform) |

### 5.4 Channel & Commerce Domain (6 agents)

**Primary schema:** CHNML. **Consumed schemas:** PRDML, AMSML.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| CHN-A01 | Quote-to-Order Copilot | configuration-guide, pricing-policy enforcer, financing-options retriever | ORCH-01 |
| CHN-A02 | Dealer Performance Agent | KPI aggregator, benchmark comparator, improvement-opportunity scorer | (platform) |
| CHN-A03 | Order Fulfillment Agent | delivery-date predictor, exception communicator, allocation optimizer | ORCH-07 |
| CHN-A04 | Lead Prioritization Agent | fit-score, stage-aware router, dealer-capacity-aware allocator | ORCH-11 |
| CHN-A05 | End-User Lifecycle Agent | usage-aware upsell, trade-in timing, renewal engagement | ORCH-12 |
| CHN-A06 | Dealer Inquiry Agent | policy retriever, precedent matcher, response composer | ORCH-06 |

---

## Part 6 — Orchestrations (ICE)

| orch_id | name | domain | agents | trigger | primary_gold_view | cycle_time_slo |
|---|---|---|---|---|---|---|
| ORCH-01 | Configure & Order | CHN/CPR | CHN-A01, CPR-A05 | Quote intake / order event | GV_ORDER_PIPELINE | < 15 min |
| ORCH-02 | Warranty & Pricing | AMS/MSC | AMS-A03, MSC-A02 | Claim filed / pricing-change event | GV_WARRANTY_QUEUE | < 10 min |
| ORCH-03 | (Reserved) | — | — | — | — | — |
| ORCH-04 | Service Scheduling & Throughput | AMS | AMS-A01 | Service request / bay availability | GV_SERVICE_SCHEDULE | < 30 min |
| ORCH-05 | Field Campaign / Recall | CPR | CPR-A08 | Campaign trigger (safety, performance) | GV_CAMPAIGN_IMPACT | < 1 hr to scoping |
| ORCH-06 | Service & Inquiry Routing | AMS/CHN | AMS-A02, AMS-A08, CHN-A06 | Service contact / dealer inquiry | GV_SUPPORT_QUEUE | < 90 sec |
| ORCH-07 | Service Pipeline Execution | AMS/CPR/MSC | CPR-A01, CPR-A02, CPR-A03, AMS-A07, MSC-A05 | Telemetry signal / dispatch event | GV_SERVICE_PIPELINE | < 15 min |
| ORCH-08 | Quality / Safety Event | MSC/CPR | MSC-A03, CPR-A10 | Quality event / cyber anomaly | GV_QUALITY_CASES | < 10 min |
| ORCH-09 | (Reserved) | — | — | — | — | — |
| ORCH-10 | Parts & Demand Sensing | AMS | AMS-A05 | Continuous signal fusion | GV_PARTS_DEMAND | 15-min cadence |
| ORCH-11 | Lead & Campaign Activation | CHN | CHN-A04 | Lead event / campaign intake | GV_LEAD_QUEUE | Minutes |
| ORCH-12 | Customer & Contract Lifecycle | AMS/CHN | AMS-A10, CHN-A05 | Lifecycle event / renewal trigger | GV_END_USER_LIFECYCLE | Continuous |

Note: ORCH-03 and ORCH-09 reserved for future ICE expansion.

**File:** `apex-ice/data/orchestrations.json`

---

## Part 7 — MCP Tool Catalog (ICE)

### 7.1 ICE domain codes

| code | scope |
|---|---|
| `mcp.serial.*` | Serial-unit-scoped operations (the individual machine) |
| `mcp.product.*` | Product family / variant operations |
| `mcp.telemetry.*` | Telemetry / fault-code operations |
| `mcp.ota.*` | Over-the-air release operations |
| `mcp.service.*` | Service event / repair order operations |
| `mcp.warranty.*` | Warranty claim operations |
| `mcp.bulletin.*` | Service bulletin / campaign operations |
| `mcp.parts.*` | Parts inventory / demand operations |
| `mcp.technician.*` | Technician operations |
| `mcp.dealer.*` | Dealer / distributor operations |
| `mcp.quote.*` | Quote-to-order operations |
| `mcp.order.*` | Order operations |
| `mcp.supplier.*` | Supplier / multi-tier operations |
| `mcp.quality.*` | Quality event operations |
| `mcp.customer.*` | End-user / customer operations |
| `mcp.contract.*` | Service contract / subscription operations |

### 7.2 Catalog target

Initial catalog: ~60 tools.

**File:** `apex-ice/data/tools.json`

---

## Part 8 — ISV Ecosystem (ICE)

| category | isv_examples | microsoft_integration |
|---|---|---|
| ERP — Mfg | SAP S/4HANA, Oracle Cloud ERP, Infor LN | API / Fabric |
| PLM | Siemens Teamcenter, PTC Windchill, Dassault ENOVIA | API |
| MES | Siemens Opcenter, Rockwell FactoryTalk, GE Plant Applications | API |
| CAD | Dassault CATIA / SOLIDWORKS, Siemens NX, PTC Creo | API |
| Connected Product / Telematics | PTC ThingWorx, Hitachi Lumada, Siemens Insights Hub (MindSphere) | Azure IoT / API |
| Field Service | D365 Field Service, ServiceMax (PTC), Salesforce Field Service | Native / API |
| Dealer Management Systems | CDK Global (automotive), e-Emphasys (heavy equipment), Reynolds & Reynolds | API |
| Warranty | Tavant, Syncron, PTC Servigistics (for parts) | API |
| Parts Planning | Syncron, PTC Servigistics, Baxter Planning | API |
| CPQ | Oracle CPQ, Salesforce CPQ, PROS, Tacton | API |
| Quality | Siemens Opcenter Quality, IQS, Sparta Systems | API |
| Simulation / Digital Twin | Ansys, Dassault SIMULIA, Siemens Simcenter | API |
| Aerospace-specific | Airbus Skywise, Boeing AnalytX, IFS (A&D) | API |
| Automotive-specific | Wejo, Otonomo, various OEM platforms | API |

**File:** `apex-ice/data/isv-ecosystem.json`

---

## Part 9 — Wave Content (ICE)

| wave | name | scope | duration | entry | exit | economic_case |
|---|---|---|---|---|---|---|
| W1 | Foundation | L1–L4 stand-up; CPTML + AMSML Silver/Gold; first 3–5 agents (predictive service, warranty, service scheduling); pilot on one product line / dealer network | 6–9 mo | CMM-1 or CMM-2 | CMM-3 readiness | Warranty-cost reduction + service throughput uplift — 90-day evidence signal |
| W2 | Expansion | PRDML + SCML canonical; first full domain ORCH stack; 10–15 agents | 9–12 mo | CMM-3 | Early CMM-4 | Uptime uplift + parts-inventory optimization + supplier-resilience signal |
| W3 | Platform | Cross-domain ORCHs; full 32-agent fleet; enterprise rollout across product lines | 12–18 mo | CMM-4 entry | CMM-4 full | Enterprise aftermarket-revenue uplift; dealer-network performance step-change |
| W4 | Adaptive | Continuous-learning fleets; engineering-feedback loops; remanufacturing-optimization agents | Ongoing | CMM-4 | CMM-5 | Compounding returns from field-to-engineering feedback |

**File:** `apex-ice/data/waves.json`

---

## Part 10 — Reference Implementations (ICE)

| ref_impl | scope | status | spec |
|---|---|---|---|
| **Dealer Site Bravo Day-in-the-Service-Manager-Seat** | Heavy equipment dealer, single service day, 8 events across AMS/CPR/MSC/CHN | Planned | TBD |
| RefImpl-02 Field Campaign Day | Safety campaign rollout across connected product fleet | Reserved | TBD |
| RefImpl-03 Supply Disruption Day | Multi-tier supplier disruption response | Reserved | TBD |
| RefImpl-04 Product-as-a-Service Launch | PaaS offering launch event sequence | Reserved | TBD |

**File:** `apex-ice/data/ref-implementations.json`

### 10.1 Dealer Site Bravo

The primary ICE reference implementation centers on a **dealer service manager** rather than a manufacturing plant manager or a product engineer. The reason: the dealer-network intersection is where OEM telemetry, dealer operations, service execution, warranty, parts, and end-customer experience collide. It's the highest-density operational context for demonstrating ICE's agentic fleet, and it's the operational persona that DMTSP pursuits most often engage.

---

## Part 11 — Solution Stack (ICE)

~55 rows.

**File:** `apex-ice/data/solution-stack.json`

---

## Part 12 — File Structure (ICE)

```
apex-ice/
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
    └── /dealer-site-bravo/
```

---

## Part 13 — Build Sequence

Six phases, mirroring RC/TH. No sub-variant toggle needed in v1.0.

---

## Part 14 — Acceptance Criteria

1. ☐ `apex-ice/` folder
2. ☐ README with ICE code, version, Core reference
3. ☐ 10 Forces of Change
4. ☐ Eras / CMM inherited unchanged
5. ☐ 5 schemas (PRDML, CPTML, AMSML, SCML, CHNML)
6. ☐ Envelope inherited with ICE vocabulary
7. ☐ 12 ORCHs (ORCH-03 and ORCH-09 reserved)
8. ☐ MCP catalog with ICE domain codes
9. ☐ `--ice-accent` added
10. ☐ Core widgets consumed
11. ☐ Compliance lint passes (Core + ICE additions)
12. ☐ Solution Stack ≥55 rows
13. ☐ At least one reference implementation planned (Dealer Site Bravo)

---

## Part 15 — ICE-Specific Design Considerations

### 15.1 Voice

Voice in ICE reference implementations should be **seasoned service / operations leadership** — service manager at a dealer, plant manager at a tier supplier, field-ops director at a fleet customer. Disciplined, pragmatic, customer-and-safety focused. Never tech-first; always work-first.

### 15.2 Serial unit as protagonist

The individual machine — identified by its serial number — is the protagonist of ICE demos. Every event threads through a specific serial unit (or a fleet of them), its history, its configuration, its operating context. This is different from RC (product SKU) or TH (booking/stay). The design should make serial-unit context feel first-class.

### 15.3 Dealer/channel surface

Because the dealer network intermediates so much of the OEM-customer relationship, the framework site should expose a clear narrative layer for **"who does what"** — OEM, dealer, end customer — across each orchestration. Agents operate at each layer, and the HITL gate varies depending on which party is the decision-maker.

### 15.4 Aftermarket-first framing

The framework should lead with **aftermarket service** as the primary value story — not new-machine sales. This inverts the instinctive manufacturing-industry narrative and aligns with where the actual profit pools sit in modern equipment OEMs.

---

## Part 16 — Handoff Notes to Claude Code

**Serial unit is a first-class entity.** Every agent, tool, and Gold view that touches a specific machine threads through `DIM_SERIAL_UNIT`. This is a fundamental design principle for ICE — don't genericize it to "product."

**Three-party design pattern.** Unlike single-party editions (RC, TH), ICE operationally involves OEM + Dealer + End Customer. Many agents surface decisions that belong to one of those three parties, not always the same one. The framework site should make this visible — labeled HITL gates per role.

**Aftermarket > new-machine narrative.** Lead with aftermarket in every narrative surface. A SteerCo at an OEM already knows they sell machines; the story that gets SteerCo attention is what APEX-ICE does to the service P&L.

**Sub-variant deferral.** ICE launches as single edition. If Aerospace & Defense, Automotive, or Heavy Equipment emerges as structurally distinct enough to need its own tag, amend Core to add the sub-variant — don't hack it into ICE silently.

---

**End of APEX-ICE specification · v1.0**

*Parent:* `apex-core-build-spec.md` v1.0
