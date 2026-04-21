# APEX · Health Care & Life Sciences Edition (APEX-HLS)
## Edition Build Specification

**Spec version:** 1.0
**Parent spec:** `apex-core-build-spec.md` — **REQUIRED READING BEFORE THIS DOCUMENT**
**Edition code:** HLS
**Edition accent token:** `--hls-accent: #0891b2` (cyan-clinical — clarity, trust, precision)
**Status:** Planned build
**Sub-variants:** `HLS-PRV` (Provider & Payer), `HLS-LS` (Life Sciences)

---

## Part 0 — Inheritance Declaration

This spec inherits from APEX Core v1.2. Every convention, template, design token, widget contract, and compliance constraint defined in Core applies here unchanged.

**Manifest:** `apex-hls/data/schemas.manifest.json` — conforms to the Core v1.2 schema-manifest contract (to be populated).

**Inheritance map:**

| Core Part | What this edition inherits |
|---|---|
| Core Part 0 | Compliance & language constraints (immutable) |
| Core Part 3 | Forces of Change framing convention |
| Core Part 4 | AI Journey Eras (unchanged, referenced) |
| Core Part 5 | CMM stages (unchanged, referenced; edition adds signals) |
| Core Part 6 | Reference architecture seven-layer model |
| Core Part 7 | Schema naming, medallion, entity template, event envelope |
| Core Part 8 | ORCH + MCP tool conventions, HITL gate taxonomy |
| Core Part 9 | Design system (extended with `--hls-accent`) |
| Core Part 10 | Reusable render widgets |
| Core Part 12 | Wave deployment model |
| Core Part 13 | Solution Stack shape |

**Edition-specific additional compliance (HLS-only):**

Beyond Core Part 0, HLS adds these non-negotiable constraints:

1. **Protected Health Information (PHI)** must never appear in seed data, demo content, or illustrative examples. Use synthetic identifiers (e.g., `pat-X001`, `mrn-test-091`) that are visibly non-real.
2. **Clinical decision support language** must never suggest that an agent diagnoses, prescribes, or otherwise substitutes for a licensed clinician. Agents *surface*, *correlate*, *recommend for clinician review* — they do not *decide*.
3. **GxP validation posture** is assumed throughout. Any agent touching a GxP-regulated workflow (clinical trial, manufacturing, pharmacovigilance) operates under validated-workflow constraints with full audit trails.
4. **21 CFR Part 11 electronic-record integrity** requirements apply to every event the edition's agents emit in GxP contexts.
5. **Serialization under DSCSA** (US) and **FMD** (EU) for life sciences supply chain is a regulatory floor, not a feature.

---

## Part 1 — Edition Positioning

### 1.1 What APEX-HLS is

APEX-HLS is the APEX instantiation tuned to the operational vocabulary, regulatory environment, and commercial maturity curve of **health care and life sciences enterprises** — integrated delivery networks, academic medical centers, health plans, pharma and biotech manufacturers, medical device makers, contract research and manufacturing organizations, and specialty clinical services.

### 1.2 Primary audiences

**Provider & Payer sub-variant (HLS-PRV):**
- Chief Medical Officers, Chief Nursing Officers, Chief Medical Information Officers
- Chief Operating Officers at IDNs / health systems
- Chief Medical / Pharmacy officers at health plans
- Revenue cycle, population health, quality / HEDIS leaders

**Life Sciences sub-variant (HLS-LS):**
- Chief Medical Affairs Officers, Chief Commercial Officers at pharma and device manufacturers
- Chief Scientific / R&D Officers, Chief Manufacturing Officers
- Global Regulatory Affairs, Pharmacovigilance, Quality Assurance leadership
- Chief Patient Officers (emerging role)

Across both sub-variants: Chief Compliance Officers, General Counsel, Chief Data / Digital Officers.

### 1.3 Operating zone

APEX-HLS delivers **Era 4 (Agentic)** outcomes within validated-workflow constraints. The HITL gate rate in HLS is higher than in RC or TH — clinical and GxP decisions require human sign-off even when the agent fully understands the decision. That's not a limitation; that's the regulatory floor.

### 1.4 Why HLS demands its own edition

HLS differs from other APEX editions in five structural ways:

1. **Regulatory validation is the operating constraint, not a compliance overlay** — every production workflow must be validated, documented, and auditable end-to-end
2. **Multiple concurrent regulatory frameworks** — HIPAA + GxP + FDA/EMA + state-level + payer-specific + trial-sponsor-specific layered simultaneously
3. **Clinical judgment is not substitutable** — agents augment clinicians; they never act as clinicians
4. **Data grains span populations, patients, episodes, visits, orders, administrations, and specimens** — far finer than retail's SKU/transaction or T&H's stay/booking
5. **Outcomes are measured in lives, not dollars** — the ROI model must speak in quality measures, adverse-event avoidance, and time-to-therapy alongside financial metrics

### 1.5 Two sub-variants, one edition

Provider/Payer and Life Sciences share the same regulatory DNA, the same data-fabric patterns, and the same validation posture. They differ in their operational spine (care delivery vs. product development and supply). Rather than split into separate editions, APEX-HLS declares two sub-variants that share the schema grammar and design system while providing their own agent fleets and orchestrations.

---

## Part 2 — Forces of Change (Health Care & Life Sciences)

Ten HLS-specific forces. Conforms to Core Part 3 template.

| id | force | signal | implication |
|---|---|---|---|
| FOC-01 | Clinical Workforce Burnout | Physician and nursing attrition; documentation burden cited as primary driver; ambient capture adoption accelerating | Agents must reduce cognitive and documentation load, never add to it |
| FOC-02 | Value-Based Care Acceleration | CMS model proliferation; risk-bearing arrangements expanding; quality measures as reimbursement drivers | Population-health and risk-adjustment agents move from analytics to operations |
| FOC-03 | Precision & Personalized Medicine | Genomics, biomarkers, companion diagnostics in mainstream oncology and rare disease; cell and gene therapy scale-up | Patient-level decisioning agents must operate on multi-modal data (clinical + omics + imaging + RWE) |
| FOC-04 | Real-World Evidence as Regulatory Input | FDA RWE framework; EMA adaptive pathways; payer evidence requirements for access | RWE pipelines become first-class, not retrospective analytics |
| FOC-05 | Clinical Trial Modernization | Decentralized and hybrid trial models; digital endpoints; trial-matching platforms | Patient-recruitment and protocol-execution agents deploy into active trial operations |
| FOC-06 | Supply Chain Resilience & Drug Shortages | Active ingredient sourcing concentration; generic market fragility; cold chain for biologics and cell therapies | Manufacturing and distribution agents must reason over resilience and continuity of supply |
| FOC-07 | Payer-Provider-Life-Sciences Convergence | Vertical integration (payvider, pharmacy); risk-sharing with pharma; outcomes-based contracting | Cross-stakeholder agentic workflows replace fragmented bilateral processes |
| FOC-08 | AI Regulatory Framework Emergence | FDA AI/ML guidance evolving; EU AI Act high-risk classifications; HHS rule-making on algorithmic accountability | Validation, explainability, bias monitoring are mandatory, not aspirational |
| FOC-09 | Patient-Generated Health Data at Scale | Wearables, remote monitoring, patient-reported outcomes entering clinical record | Data-ingestion and signal-filtering agents must triage patient-sourced data without overwhelming clinicians |
| FOC-10 | Cyber & Privacy Threat Escalation | Ransomware in hospital systems; biopharma IP exfiltration attempts; medical device vulnerability disclosures | Identity, access, and data-minimization agents are patient-safety features |

**File:** `apex-hls/data/forces-of-change.json`

---

## Part 3 — CMM Signal Extensions for Health Care & Life Sciences

HLS-specific observable signals per CMM stage.

| stage | hls signals |
|---|---|
| CMM-1 Foundations | EHR / ERP in place; departmental reporting; compliance via manual attestation; no real-time patient flow visibility |
| CMM-2 Connected | FHIR-based integration emerging; data warehouse with clinical + claims + operational; ML models in population health or adverse-event signals |
| CMM-3 Intelligent | Validated copilots for documentation, coding, and clinical summarization; predictive models integrated into clinician workflow with surfaced recommendations |
| CMM-4 Agentic | Agents autonomously resolve administrative exceptions (prior-auth status, order status, scheduling conflicts); clinician-facing recommendations paired with validated HITL gates; GxP workflows partially autonomous within validated boundaries |
| CMM-5 Adaptive | Agent fleet continuously retrained on real-world outcomes within validated drift-monitoring boundaries; quality measure performance improves without explicit intervention |

**File:** `apex-hls/data/cmm-signals.json`

---

## Part 4 — Canonical Schemas (Health Care & Life Sciences)

Five schemas — one more than RC/TH because HLS has both care delivery and product lifecycle to represent. Conforms to Core Part 7.

| schema | domain | scope | sub_variant | target_entity_count |
|---|---|---|---|---|
| **CLNML** | Clinical | Patient, encounter, order, medication, observation, diagnosis, allergy, problem, care plan — FHIR-compatible | PRV | ~50 |
| **RCML** | Revenue Cycle | Claims, authorizations, eligibility, remits, denials, appeals, coding, collections | PRV | ~30 |
| **LSML** | Life Sciences | Clinical trial, subject, protocol, investigational product, lot, adverse event, regulatory submission | LS | ~40 |
| **SCML** | Supply Chain | Serialized product, lot, shipment, cold chain, recall, pedigree (DSCSA) | Both | ~30 |
| **OPSML** | Operations & Quality | Facility, equipment, calibration, CAPA, quality event, training record | Both | ~25 |

### 4.1 Dimensional anchors (HLS-specific)

**Provider/Payer shared:**
`DIM_PATIENT` (tokenized MRN), `DIM_PROVIDER`, `DIM_FACILITY`, `DIM_DEPARTMENT`, `DIM_PAYER`, `DIM_PLAN`, `DIM_ENCOUNTER_TYPE`, `DIM_DIAGNOSIS_CODE` (ICD-10), `DIM_PROCEDURE_CODE` (CPT/HCPCS), `DIM_MEDICATION` (RxNorm), `DIM_DATE`, `DIM_TIME`.

**Life Sciences:**
`DIM_COMPOUND`, `DIM_INDICATION`, `DIM_TRIAL`, `DIM_SITE`, `DIM_SUBJECT` (tokenized), `DIM_LOT` (GS1 SGTIN), `DIM_HCP`, `DIM_PRODUCT`, `DIM_REGULATORY_AUTHORITY`.

### 4.2 HLS-specific controlled vocabulary for event envelope

For Core Part 7.4 envelope, HLS uses these controlled vocabularies:

- `business_step`: `ordering`, `scheduling`, `admitting`, `observing`, `medicating`, `administering`, `documenting`, `coding`, `billing`, `authorizing`, `adjudicating`, `dispensing`, `reporting`, `auditing`, `consenting`
- `disposition`: `pending`, `active`, `resolved`, `completed`, `canceled`, `on_hold`, `in_error`, `denied`, `authorized`, `reported`

### 4.3 Key schema entities (summary)

**CLNML (Clinical, FHIR-aligned where possible):**
`PATIENT`, `ENCOUNTER`, `OBSERVATION`, `MEDICATION_ORDER`, `MEDICATION_ADMINISTRATION`, `CONDITION`, `ALLERGY_INTOLERANCE`, `PROCEDURE`, `CARE_PLAN`, `CARE_TEAM`, `SPECIMEN`, `DIAGNOSTIC_REPORT`, `IMMUNIZATION`, `DEVICE`, `CLINICAL_NOTE`, `PATIENT_FLOW_EVENT`, plus ~34 more.

**RCML (Revenue Cycle):**
`CLAIM`, `CLAIM_LINE`, `AUTHORIZATION_REQUEST`, `ELIGIBILITY_EVENT`, `REMITTANCE`, `DENIAL_EVENT`, `APPEAL`, `CODING_EVENT`, `CHARGE_CAPTURE`, `PAYMENT_POSTING`, plus ~20 more.

**LSML (Life Sciences):**
`PROTOCOL`, `TRIAL`, `SUBJECT`, `SITE`, `VISIT`, `INVESTIGATIONAL_PRODUCT`, `ADVERSE_EVENT`, `SERIOUS_ADVERSE_EVENT`, `PROTOCOL_DEVIATION`, `REGULATORY_SUBMISSION`, `SAFETY_SIGNAL`, `PHARMACOVIGILANCE_CASE`, plus ~28 more.

**SCML (Supply Chain):**
`SERIALIZED_PRODUCT`, `LOT`, `TRANSACTION_HISTORY` (DSCSA T3), `COLD_CHAIN_TELEMETRY`, `TEMPERATURE_EXCURSION`, `RECALL_NOTICE`, `RECALL_DISPOSITION`, `SHIPMENT`, `PEDIGREE_EVENT`, plus ~21 more.

**OPSML (Operations & Quality):**
`FACILITY`, `EQUIPMENT`, `CALIBRATION_EVENT`, `CAPA`, `QUALITY_EVENT`, `DEVIATION`, `CHANGE_CONTROL`, `TRAINING_RECORD`, `VALIDATION_RECORD`, plus ~16 more.

---

## Part 5 — Domain Architectures (34 Agents)

Four domains. 34 total agents across the two sub-variants.

### 5.1 Clinical Operations Domain (PRV · 10 agents)

**Primary schema:** CLNML. **Consumed schemas:** RCML, SCML.
**Decision cadence:** Second for alerts; minute–hour for patient flow; shift-scoped for staffing.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| CLN-A01 | Clinical Documentation Copilot | ambient capture transcriber, problem-list suggester, note-structure validator | ORCH-01 |
| CLN-A02 | Patient Flow Agent | bed-placement optimizer, discharge-barrier detector, throughput predictor | ORCH-04 |
| CLN-A03 | Early Deterioration Signal | vitals-trend analyzer, sepsis-risk scorer, escalation notifier | ORCH-08 |
| CLN-A04 | Medication Reconciliation Agent | source-list harmonizer, interaction flagger, omission detector | ORCH-02 |
| CLN-A05 | Care Gap Agent | quality-measure resolver, outreach prioritizer, scheduling coordinator | ORCH-12 |
| CLN-A06 | Clinical Decision Surfacer | guideline retriever, patient-specific contextualizer, evidence-grade tagger | (experience) |
| CLN-A07 | Specimen Tracking Agent | chain-of-custody monitor, result-return predictor, lost-sample detector | ORCH-07 |
| CLN-A08 | Imaging Workflow Agent | protocol matcher, priority router, result-acknowledgment tracker | ORCH-07 |
| CLN-A09 | Consult Routing Agent | specialty matcher, availability resolver, referral-completion tracker | ORCH-06 |
| CLN-A10 | Order Status Agent | pending-order triage, bottleneck identifier, clinician nudger | (platform) |

### 5.2 Revenue Cycle Domain (PRV · 8 agents)

**Primary schema:** RCML. **Consumed schemas:** CLNML.
**Decision cadence:** Minute–hour for denials; claim-lifecycle for authorization; cycle-scoped for collections.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| RCM-A01 | Prior Authorization Agent | payer-rule retriever, evidence packager, submission drafter | ORCH-02 |
| RCM-A02 | Eligibility Verification Agent | coverage resolver, benefit-detail extractor, discrepancy flagger | ORCH-02 |
| RCM-A03 | Coding Assist Agent | note-to-code suggester, CDI-query drafter, audit-risk scorer | ORCH-01 |
| RCM-A04 | Denial Management Agent | denial-pattern classifier, appeal-drafter, root-cause tagger | ORCH-08 |
| RCM-A05 | Charge Capture Agent | missing-charge detector, documentation-evidence linker | (platform) |
| RCM-A06 | Underpayment Detector | contract-expected vs remit comparator, variance ranker | ORCH-08 |
| RCM-A07 | Patient Financial Agent | estimate generator, financial-assistance matcher, payment-plan proposer | ORCH-12 |
| RCM-A08 | Authorization Status Agent | submission-to-decision tracker, aged-auth escalator | (platform) |

### 5.3 Life Sciences R&D / Clinical Operations Domain (LS · 8 agents)

**Primary schema:** LSML. **Consumed schemas:** CLNML (real-world), SCML.
**Decision cadence:** Trial-milestone for protocol; adverse-event for safety; submission-scoped for regulatory.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| LSR-A01 | Trial Matching Agent | inclusion-criteria resolver, patient-profile scorer, site-capability matcher | ORCH-05 |
| LSR-A02 | Protocol Deviation Detector | expected-vs-actual comparator, materiality classifier, reporting-route selector | ORCH-08 |
| LSR-A03 | Adverse Event Intake Agent | source classifier (site, PV hotline, literature, social), coding assister (MedDRA), case builder | ORCH-08 |
| LSR-A04 | Safety Signal Agent | disproportionality analyzer, temporal-pattern detector, evidence-package builder | ORCH-08 |
| LSR-A05 | Regulatory Submission Agent | module assembler, precedent retriever, formatting validator | ORCH-09 |
| LSR-A06 | Medical Affairs Inquiry Agent | HCP-question classifier, response retriever (approved content), routing resolver | ORCH-06 |
| LSR-A07 | Real-World Evidence Agent | cohort definer, endpoint computer, comparator constructor | ORCH-10 |
| LSR-A08 | Trial Supply Agent | enrollment-pace monitor, depot-inventory matcher, shipment scheduler | ORCH-11 |

### 5.4 Manufacturing, Supply & Quality Domain (Both · 8 agents)

**Primary schema:** SCML, OPSML. **Consumed schemas:** LSML.
**Decision cadence:** Second for cold chain; minute for batch events; day for quality review.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| MSQ-A01 | Cold Chain Monitor | threshold watcher, excursion classifier, product-disposition recommender | ORCH-03 |
| MSQ-A02 | Serialization Verifier | SGTIN-check, aggregation validator, pedigree-builder | (platform) |
| MSQ-A03 | Recall Impact Agent | lot-trace resolver, distribution-reach calculator, notification-stager | ORCH-05 |
| MSQ-A04 | CAPA Lifecycle Agent | trend detector, investigation-drafter, effectiveness-checker | ORCH-08 |
| MSQ-A05 | Deviation Triage Agent | deviation-classifier, root-cause candidate generator, risk-scorer | ORCH-08 |
| MSQ-A06 | Batch Release Agent | spec-compliance checker, document-completeness validator, QA-sign-off stager | ORCH-07 |
| MSQ-A07 | Equipment Integrity Agent | calibration-due tracker, performance-trend analyzer, maintenance-scheduler | ORCH-07 |
| MSQ-A08 | Training Compliance Agent | curriculum-gap detector, expiry notifier, role-change reassigner | (platform) |

---

## Part 6 — Orchestrations (ORCH-01 through ORCH-12)

Conforms to Core Part 8.2. Slot positions align with RC/TH per Core Part 8.1.

| orch_id | name | domain | sub_variant | agents | trigger | primary_gold_view | cycle_time_slo |
|---|---|---|---|---|---|---|---|
| ORCH-01 | Documentation & Coding | CLN/RCM | PRV | CLN-A01, RCM-A03 | Encounter documentation event | GV_ENCOUNTER_DOCUMENTATION | < 2 min turnaround on suggestions |
| ORCH-02 | Authorization & Eligibility | RCM | PRV | RCM-A01, RCM-A02, CLN-A04 | Order placed requiring auth | GV_PATIENT_ACCESS | < 10 min to submission |
| ORCH-03 | Cold Chain Integrity | MSQ | Both | MSQ-A01 | Telemetry threshold breach | GV_LOT_COLD_CHAIN | < 5 min to disposition brief |
| ORCH-04 | Patient Flow & Throughput | CLN | PRV | CLN-A02 | Admission / transfer / discharge event | GV_FACILITY_FLOW | < 15 min to bed assignment |
| ORCH-05 | Trial Matching / Recall Impact | LSR/MSQ | Both | LSR-A01, MSQ-A03 | Eligible patient encounter OR recall notice | GV_TRIAL_CANDIDATE / GV_RECALL_IMPACT | < 10 min |
| ORCH-06 | Consult & Inquiry Routing | CLN/LSR | Both | CLN-A09, LSR-A06 | Consult request OR medical inquiry | GV_REFERRAL_QUEUE / GV_MEDICAL_INQUIRY | < 2 min to routing |
| ORCH-07 | Clinical Specimen & Imaging / Batch | CLN/MSQ | Both | CLN-A07, CLN-A08, MSQ-A06, MSQ-A07 | Specimen collected / image acquired / batch ready | GV_SPECIMEN_TRACK / GV_BATCH_RELEASE | < 20 min documentation lag |
| ORCH-08 | Safety Event & Denial Triage | CLN/RCM/LSR/MSQ | Both | CLN-A03, RCM-A04, LSR-A02, LSR-A03, LSR-A04, MSQ-A04, MSQ-A05 | Clinical deterioration / denial receipt / AE report / deviation / quality event | GV_SAFETY_CASES / GV_DENIAL_QUEUE | < 10 min case assembly |
| ORCH-09 | Regulatory Submission | LSR | LS | LSR-A05 | Submission milestone trigger | GV_SUBMISSION_PIPELINE | Milestone-driven |
| ORCH-10 | Demand & Evidence Sensing | LSR | LS | LSR-A07 | Continuous RWE signal fusion | GV_RWE_COHORTS | Continuous |
| ORCH-11 | Trial Supply & Distribution | LSR | LS | LSR-A08 | Enrollment / depot signal | GV_TRIAL_SUPPLY | Daily + event-driven |
| ORCH-12 | Care Gap & Patient Engagement | CLN/RCM | PRV | CLN-A05, RCM-A07 | Gap detected / financial event | GV_CARE_GAP_QUEUE / GV_PATIENT_FINANCIAL | Event-driven |

**File:** `apex-hls/data/orchestrations.json`

---

## Part 7 — MCP Tool Catalog (Health Care & Life Sciences)

Conforms to Core Part 8.4 naming.

### 7.1 HLS domain codes

| code | scope |
|---|---|
| `mcp.patient.*` | Patient-scoped operations (PRV) |
| `mcp.encounter.*` | Encounter-scoped operations (PRV) |
| `mcp.facility.*` | Facility-scoped operations |
| `mcp.provider.*` | Provider / clinician operations |
| `mcp.order.*` | Clinical order operations |
| `mcp.claim.*` | Claims / revenue cycle operations |
| `mcp.auth.*` | Authorization / eligibility operations |
| `mcp.trial.*` | Clinical trial operations (LS) |
| `mcp.subject.*` | Trial subject operations (LS) |
| `mcp.pv.*` | Pharmacovigilance operations (LS) |
| `mcp.regulatory.*` | Regulatory submission operations (LS) |
| `mcp.lot.*` | Lot-scoped (serialization, DSCSA) operations |
| `mcp.capa.*` | CAPA / quality operations |
| `mcp.recall.*` | Recall-lifecycle operations |

### 7.2 Catalog target

Initial catalog: ~65 tools (more than RC/TH due to dual sub-variant coverage).

**File:** `apex-hls/data/tools.json`

---

## Part 8 — ISV Ecosystem (Health Care & Life Sciences)

| category | isv_examples | microsoft_integration |
|---|---|---|
| EHR — Acute | Epic, Oracle Health (Cerner), Meditech Expanse | API / FHIR |
| EHR — Ambulatory | Epic, athenahealth, eClinicalWorks | API / FHIR |
| Health Data Platforms | Azure Health Data Services, Innovaccer, Datavant | Native / Fabric |
| Revenue Cycle | Epic Tapestry, Oracle Health RCM, R1, Waystar | API |
| Payer Core | HealthEdge, TriZetto, Change Healthcare | API |
| Clinical Trial — EDC | Veeva Vault CDMS, Medidata Rave, Oracle Clinical | API |
| Clinical Trial — CTMS | Veeva Vault CTMS, Oracle Siebel CTMS | API |
| Pharmacovigilance | Oracle Argus, Veeva Vault Safety, ArisGlobal | API |
| Regulatory | Veeva Vault RIM, Parexel LIQUENT, Ennov | API |
| Quality Management | Veeva Vault QMS, MasterControl, TrackWise | API |
| Supply Chain — LS | SAP IBP, Kinaxis, o9 | API |
| Serialization | TraceLink, rfxcel (Antares Vision), Systech | API |
| Cold Chain | Controlant, Sensitech, Berlinger | Azure IoT + ADX |
| Real-World Evidence | Flatiron, ConcertAI, Aetion, TriNetX | API / Fabric |
| Imaging | Epic Radiant, Philips IntelliSpace, Change Healthcare | API / DICOM |

**File:** `apex-hls/data/isv-ecosystem.json`

---

## Part 9 — Wave Content (Health Care & Life Sciences)

| wave | name | scope | duration | entry | exit | economic_case |
|---|---|---|---|---|---|---|
| W1 | Foundation | L1–L4 stand-up; CLNML or LSML Silver/Gold for one sub-variant; first 3–5 agents (documentation copilot, prior auth, cold chain, or AE intake); pilot at 1–3 facilities or sites | 6–9 mo | CMM-1 or CMM-2 | CMM-3 readiness | Documentation-time reduction + prior-auth turnaround + AE processing cycle time — validated-workflow evidence |
| W2 | Expansion | RCML + OPSML canonical; first full domain ORCH stack; 10–15 agents; pilot expands to regional rollout | 9–12 mo | CMM-3 | Early CMM-4 | Denial rate reduction + throughput improvement + quality-measure lift |
| W3 | Platform | Cross-domain ORCHs; full 34-agent fleet; enterprise rollout | 12–18 mo | CMM-4 entry | CMM-4 full | Enterprise exception handling; clinician productivity flip; regulatory-submission cycle-time compression |
| W4 | Adaptive | Continuous-learning within validated drift-monitoring; fleet self-optimization; cross-domain planning | Ongoing | CMM-4 | CMM-5 | Compounding returns within regulatory-validated envelope |

HLS wave durations run longer than RC/TH because validation cycles gate every production agent deployment.

**File:** `apex-hls/data/waves.json`

---

## Part 10 — Reference Implementations (HLS)

| ref_impl | scope | sub_variant | status | spec |
|---|---|---|---|---|
| **Memorial 4-West Day-in-the-Unit** | Med-surg nursing unit, single shift, 8 events across CLN/RCM | PRV | To be built | TBD |
| **Trial ATLAS-3 Day-in-Operations** | Phase III oncology trial, single day, 8 events across LSR/MSQ | LS | To be built | TBD |
| RefImpl-03 Recall Cascade | Biologic lot recall across 200 distribution nodes | Both | Reserved | TBD |
| RefImpl-04 Prior-Auth Storm | Payer policy change triggering reauth wave | PRV | Reserved | TBD |

**File:** `apex-hls/data/ref-implementations.json`

### 10.1 Two reference implementations, not one

Unlike RC and TH which each have one primary reference implementation (Store 100, Property 201), HLS has two because the sub-variants are different enough that neither alone represents the edition. Both should be built on the same pattern — cinematic editorial HTML, 8 events, mix of HITL / ACK_ONLY / ZERO_TOUCH / ESCALATION gates.

---

## Part 11 — Solution Stack (HLS)

Conforms to Core Part 13 column contract. ~60 rows (larger than RC/TH due to dual sub-variant coverage).

**File:** `apex-hls/data/solution-stack.json`

---

## Part 12 — File Structure (HLS)

```
apex-hls/
├── README.md                               # This spec
├── CHANGELOG.md
├── index.html                              # HLS framework site with sub-variant toggle
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
    ├── /memorial-4-west/                   # PRV reference impl
    └── /trial-atlas-3/                     # LS reference impl
```

---

## Part 13 — Build Sequence

Six phases, mirroring RC/TH. Distinctive HLS consideration: **sub-variant toggle in the framework site**.

### Phase 1 — HLS framework skeleton with sub-variant toggle
**Deliverable:** `index.html` rendering Parts 1–4 and 9 with PRV / LS sub-variant switcher in the masthead.
**Acceptance:** Toggle instantly recomposes content that differs by sub-variant; shared content (Forces of Change, CMM, schemas) is visible in both; sub-variant selection persists via localStorage.

Remaining phases mirror the APEX-RC build sequence.

---

## Part 14 — Acceptance Criteria

Per Core Part 11, HLS is Core-conformant when:

1. ☐ Folder exists as `apex-hls/` parallel to `apex-core/`
2. ☐ README declares code HLS, version, Core spec version, sub-variants (PRV, LS)
3. ☐ 10 Forces of Change defined
4. ☐ Eras and CMM referenced unchanged; CMM signals added
5. ☐ 5 schemas defined (CLNML, RCML, LSML, SCML, OPSML)
6. ☐ Event envelope inherited unchanged with HLS controlled vocabulary
7. ☐ 12 ORCHs defined with sub-variant tagging where relevant
8. ☐ MCP tool catalog with HLS domain codes
9. ☐ Design system inherited; `--hls-accent` added
10. ☐ Core widgets consumed, not reimplemented
11. ☐ Part 0 (both Core and HLS-specific extensions) passes lint
12. ☐ Solution Stack has ≥60 rows
13. ☐ Two reference implementations planned (Memorial 4-West, Trial ATLAS-3)

---

## Part 15 — HLS-Specific Design Considerations

### 15.1 Clinical voice

Voice in HLS-PRV reference implementations should be **seasoned clinical leadership** — charge nurse, nocturnist, hospitalist. Calm under pressure, precise in language, protective of their teams and patients. Never casual about clinical judgment; always respectful of the work.

Voice in HLS-LS reference implementations should be **trial operations / medical affairs leadership** — project managers, medical science liaisons, QA leads. Disciplined in documentation, obsessive about protocol fidelity, thoughtful about risk.

### 15.2 HITL posture is elevated

Every clinical decision is an HITL gate. Every GxP-regulated decision is an HITL gate. Agents prepare decision-ready briefs; clinicians and qualified personnel decide. The demo should make clear that **the human touch in HLS is not a limitation — it's the product**. Agents reduce documentation and cognitive load so clinicians can spend more time on the decisions that require them.

### 15.3 Validation footprint

Every production agent in HLS carries a validation footprint: requirements, risk assessment, test evidence, change-control linkage. The framework site should include a visible "Validation Readiness" column or badge on the Solution Stack Chart — not hidden in a footnote.

---

## Part 16 — Handoff Notes to Claude Code

**Read Core first.** Do not begin without `apex-core-build-spec.md`.

**Study RC and TH as sibling references.** The RC spec shows the inheritance pattern; the TH spec shows how industry vocabulary reshapes Forces/schemas/ORCHs. HLS extends both patterns with sub-variant toggling.

**Two sub-variants are real in this edition.** The framework site must render PRV and LS as switchable views — not as two separate sites. This means `agents.json` tags each agent with `sub_variant: "PRV" | "LS" | "BOTH"` and the widgets filter accordingly.

**Regulatory language discipline.** Clinical decision support is always *decision support*, never *decision-making*. The lint tool (Core Phase 4) should flag any agent description that suggests autonomous clinical or GxP action without an HITL gate.

**The two reference implementations (Memorial 4-West and Trial ATLAS-3) are the credibility test.** SteerCo audiences in HLS are highly skilled clinicians and regulators. Get the vocabulary, the operational tempo, and the validation footprint right or the framework loses credibility. Subject-matter review is mandatory before either reference impl is published.

---

**End of APEX-HLS specification · v1.0**

*Parent spec:* `apex-core-build-spec.md` v1.0
*Sibling editions:* APEX-RC, APEX-TH
