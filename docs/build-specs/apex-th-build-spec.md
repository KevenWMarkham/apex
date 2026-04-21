# APEX · Travel & Hospitality Edition (APEX-TH)
## Edition Build Specification

**Spec version:** 1.0
**Parent spec:** `apex-core-build-spec.md` — **REQUIRED READING BEFORE THIS DOCUMENT**
**Edition code:** TH
**Edition accent token:** `--th-accent: #2a9d8f` (teal-jade — travel horizon)
**Status:** Active build
**Sibling edition:** APEX-RC (Retail & Consumer) — reference for structural patterns

---

## Part 0 — Inheritance Declaration

This spec inherits from APEX Core v1.2. Every convention, template, design token, widget contract, and compliance constraint defined in Core applies here unchanged.

**Manifest:** `apex-th/data/schemas.manifest.json` — conforms to the Core v1.2 schema-manifest contract (to be populated).

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
| Core Part 9 | Design system (extended with `--th-accent`) |
| Core Part 10 | Reusable render widgets |
| Core Part 12 | Wave deployment model |
| Core Part 13 | Solution Stack shape |

**Edition additions start at Part 1 of this document.**

---

## Part 1 — Edition Positioning

### 1.1 What APEX-TH is

APEX-TH is the APEX instantiation tuned to the operational vocabulary, regulatory environment, and commercial maturity curve of **travel and hospitality enterprises** — lodging (full-service, limited-service, luxury, extended-stay, resorts), airlines, cruise lines, car rental, online travel agencies, destination management, and integrated travel platforms.

### 1.2 Primary audiences

- Hotel chief operating officers, chief commercial officers, chief digital officers
- Airline chief commercial / chief customer officers, revenue management heads
- Cruise and integrated resort operators
- Loyalty program executives and distribution strategy leaders
- DMTSP engagement teams pursuing T&H clients

### 1.3 Operating zone

APEX-TH delivers **Era 4 (Agentic)** outcomes while remaining architecturally ready for Era 5 (Adaptive). A client entering at CMM-2 (Connected) can progress to CMM-4 (Agentic) on APEX-TH's deployment rails over Waves 1–3.

### 1.4 Why T&H demands its own edition

T&H operations differ from retail in four structural ways that justify edition-specific treatment:

1. **Perishable inventory with no backroom** — a room-night, a seat-mile, a cabin-voyage cannot be restocked; unsold inventory is a permanent revenue loss
2. **Identity follows the guest across properties and channels** — loyalty is central to the P&L, not peripheral
3. **Operations run 24/7 with no close** — there is no "end of day" reset for a 350-room hotel or a hub airport
4. **Disruption recovery is core to the product** — weather, mechanical, overbooking, geopolitical events are not exceptions; they are a daily operating mode

These properties reshape every domain below.

---

## Part 2 — Forces of Change (Travel & Hospitality)

Eight T&H-specific forces. Conforms to Core Part 3 template.

| id | force | signal | implication |
|---|---|---|---|
| FOC-01 | RevPAR & Rate Compression | Supply growth outpacing demand in key markets; short-term rental competition; corporate travel budget scrutiny | Revenue management agents must operate at intra-day cadence with guardrails |
| FOC-02 | Agentic Travel Distribution | Consumer AI agents planning and booking travel; OTAs embedding agentic search; traditional direct channel erosion | Properties and carriers must expose machine-bookable and machine-negotiable inventory or lose discovery |
| FOC-03 | Loyalty as Platform | Points/miles as cross-industry currency; co-brand credit card economics dominant; guest lifetime value the scoreboard | Loyalty state must be the integration spine, not a downstream CRM concern |
| FOC-04 | Labor Scarcity & Wage Inflation | Housekeeping and F&B labor shortages persistent; service ratios under pressure; turnover doubled pre-pandemic rates | Agents must augment associate capacity, not add to associate load |
| FOC-05 | Disruption-as-Operating-Mode | Weather volatility; ATC/infrastructure constraints; geopolitical visa disruption; single-event cascade failures | Disruption recovery orchestration is a W1 priority, not a W3 aspiration |
| FOC-06 | Sustainability & ESG Pressure | Carbon reporting mandates; SAF adoption curves; water and energy accountability at property level | Agents reason over sustainability KPIs as first-class, not post-hoc |
| FOC-07 | Data Fabric Consolidation | Cloud-native PMS/CRS/RMS on Fabric; legacy monolith exit; real-time guest profile unification | OneLake / Fabric as unified T&H fabric unlocks cross-property agent deployment |
| FOC-08 | Experience Personalization at Scale | Guest expectation of in-stay / in-flight personalization; generative concierge emergence; zero-tolerance for service inconsistency | Agentic personalization layers over every guest touchpoint, with HITL for high-value interventions |

**File:** `apex-th/data/forces-of-change.json`

---

## Part 3 — CMM Signal Extensions for Travel & Hospitality

T&H-specific observable signals per CMM stage. Additive to Core Part 5.

| stage | t&h signals |
|---|---|
| CMM-1 Foundations | Rate decisions made in spreadsheets; guest complaints the primary OSAT signal; overbooking visible only at check-in or gate |
| CMM-2 Connected | RMS in production; unified guest profile emerging across properties; disruption recovery still manual and agent-desk-driven |
| CMM-3 Intelligent | Property management copilots deployed; dynamic rate optimization with human approval; generative content in distribution |
| CMM-4 Agentic | Upsell/upgrade fully autonomous; overbooking optimization self-manages; disruption rebooking runs without agent-desk queues for >60% of affected guests |
| CMM-5 Adaptive | Observed RevPAR improves without explicit model retraining; guest personalization adapts continuously; cross-property orchestration emerges without human integration |

**File:** `apex-th/data/cmm-signals.json`

---

## Part 4 — Canonical Schemas (Travel & Hospitality)

Four schemas. Conforms to Core Part 7 naming and template.

| schema | domain | scope | target_entity_count |
|---|---|---|---|
| **RESML** | Reservations & Inventory | Bookings, room/seat inventory, rate plans, availability, holds, cancellations, overbooking state | ~35 |
| **GXML** | Guest Experience | Guest profile, stay/trip lifecycle, service requests, incidents, loyalty state, personalization signals, on-property / in-flight events | ~40 |
| **REVML** | Revenue Management | Rate optimization, demand forecasts, channel mix, ancillary revenue, compression events, yield decisions | ~30 |
| **OPSML** | Operations | Housekeeping, maintenance, F&B operations, staffing, property systems, cold chain for F&B, sustainability telemetry | ~30 |

### 4.1 Dimensional anchors (TH-specific)

`DIM_PROPERTY`, `DIM_ROOM_TYPE`, `DIM_RATE_PLAN`, `DIM_CHANNEL`, `DIM_GUEST`, `DIM_LOYALTY_TIER`, `DIM_EMPLOYEE`, `DIM_SERVICE_CATEGORY`, `DIM_ROUTE` (for air/cruise/rail), `DIM_DATE`, `DIM_TIME`.

For **airline-specialized** deployments: add `DIM_FLIGHT`, `DIM_EQUIPMENT`, `DIM_AIRPORT`.
For **cruise-specialized** deployments: add `DIM_SAILING`, `DIM_CABIN_CATEGORY`, `DIM_ITINERARY`.

### 4.2 T&H-specific controlled vocabulary for event envelope

For Core Part 7.4 envelope, TH uses these controlled vocabularies:

- `business_step`: `searching`, `booking`, `confirming`, `arriving`, `checking_in`, `checking_out`, `servicing`, `billing`, `cancelling`, `rebooking`, `departing`, `remediating`
- `disposition`: `held`, `confirmed`, `in_stay`, `in_transit`, `completed`, `cancelled`, `no_show`, `disrupted`, `compensated`, `closed`

### 4.3 Key schema entities (summary)

**RESML (Reservations & Inventory):**
`BOOKING`, `RESERVATION_HOLD`, `INVENTORY_POSITION`, `RATE_PLAN`, `CHANNEL_INVENTORY_ALLOCATION`, `OVERBOOKING_STATE`, `CANCELLATION_EVENT`, `NO_SHOW_EVENT`, `WAITLIST_POSITION`, `GROUP_BLOCK`, `PACE_CURVE`, plus ~24 more.

**GXML (Guest Experience):**
`GUEST_PROFILE`, `STAY`, `TRIP_SEGMENT`, `CHECK_IN_EVENT`, `CHECK_OUT_EVENT`, `SERVICE_REQUEST`, `INCIDENT`, `LOYALTY_STATE`, `POINTS_TRANSACTION`, `PERSONALIZATION_SIGNAL`, `GUEST_SENTIMENT_EVENT`, `AMENITY_CONSUMPTION`, plus ~28 more.

**REVML (Revenue Management):**
`DEMAND_FORECAST`, `RATE_RECOMMENDATION`, `COMPRESSION_EVENT`, `YIELD_DECISION`, `CHANNEL_MIX_STATE`, `ANCILLARY_OPPORTUNITY`, `UPSELL_OFFER`, `UPGRADE_OFFER`, `ATTRIBUTION_EVENT`, plus ~21 more.

**OPSML (Operations):**
`HOUSEKEEPING_TASK`, `ROOM_STATUS`, `MAINTENANCE_TICKET`, `FB_SERVICE_EVENT`, `COLD_CHAIN_TELEMETRY`, `STAFFING_SCHEDULE`, `PROPERTY_SYSTEM_EVENT`, `ENERGY_TELEMETRY`, `WATER_TELEMETRY`, `SUSTAINABILITY_METRIC`, plus ~20 more.

Full registry in `apex-th/data/schemas.json`.

---

## Part 5 — Domain Architectures (30 Agents)

Four domains. 30 total agents. Decomposition philosophy applied throughout.

### 5.1 Revenue Management Domain (10 agents)

**Primary schema:** REVML. **Consumed schemas:** RESML, GXML.
**Decision cadence:** Minute–hour for rate decisions; daily for planning; demand-driven for compression events.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| REV-A01 | Dynamic Rate Agent | elasticity learner, competitive signal, guardrail enforcer | ORCH-02 |
| REV-A02 | Demand Forecaster | base + trend + event decomposition, uncertainty band | ORCH-10 |
| REV-A03 | Compression Detector | pace-vs-forecast comparator, cross-property signal | ORCH-02 |
| REV-A04 | Overbooking Optimizer | no-show predictor, displacement cost modeler | ORCH-03 |
| REV-A05 | Channel Mix Agent | cost-of-channel scorer, allocation rebalancer | ORCH-02 |
| REV-A06 | Upsell Ranker | guest-profile scorer, margin optimizer, inventory-aware allocator | ORCH-06 |
| REV-A07 | Upgrade Offer Agent | availability watcher, offer pricer, accept-probability scorer | ORCH-06 |
| REV-A08 | Ancillary Revenue Agent | bundle composer, journey-timing scorer | ORCH-11 |
| REV-A09 | Group Block Optimizer | washout predictor, displacement analyzer | (platform) |
| REV-A10 | Rate Parity Monitor | channel scanner, breach detector, remediation drafter | (platform) |

### 5.2 Guest Experience Domain (8 agents)

**Primary schema:** GXML. **Consumed schemas:** RESML, REVML.
**Decision cadence:** Second for service requests; minute–hour for incidents; stay-lifecycle for personalization.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| GXP-A01 | Service Request Handler | intent classifier, routing resolver, SLA monitor | ORCH-06 |
| GXP-A02 | Guest Incident Agent | tier classifier, stakeholder router, remediation composer | ORCH-08 |
| GXP-A03 | Personalization Agent | preference resolver, next-best-action ranker, brand-voice checker | ORCH-12 |
| GXP-A04 | Loyalty State Agent | tier progression tracker, benefit activation, status challenge handler | ORCH-12 |
| GXP-A05 | Check-In/Check-Out Agent | preference pre-stage, room-ready coordinator, mobile-key issuer | ORCH-01 |
| GXP-A06 | Sentiment Signal Agent | review / chat / voice sentiment fusion, real-time risk scorer | ORCH-08 |
| GXP-A07 | Recovery Agent | incident-to-remedy matcher, points/offer composer, guardrail enforcer | ORCH-08 |
| GXP-A08 | Concierge Copilot | knowledge retrieval, reservation-aware recommender, service-integrated | (experience) |

### 5.3 Operations Domain (8 agents)

**Primary schema:** OPSML. **Consumed schemas:** GXML, RESML.
**Decision cadence:** Second for system integrity; minute for dispatch; day for scheduling.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| OPS-A01 | Housekeeping Router | room-ready sequencer, priority scorer (VIP, early arrival), staff-load balancer | ORCH-04 |
| OPS-A02 | Room Status Reconciler | PMS-vs-sensor-vs-mobile fusion, discrepancy resolver | ORCH-04 |
| OPS-A03 | Maintenance Dispatcher | severity classifier, skill-match router, SLA monitor | ORCH-07 |
| OPS-A04 | F&B Cold Chain Monitor | threshold watcher, excursion classifier, disposition recommender | ORCH-03 (F&B sub-variant) |
| OPS-A05 | Staffing Forecaster | occupancy-driven demand, skill-mix optimizer, compliance checker | (platform) |
| OPS-A06 | Energy & Water Agent | telemetry monitor, anomaly detector, sustainability KPI reporter | ORCH-09 |
| OPS-A07 | Property System Integrity Agent | HVAC / access-control / network health, cascade-prevention | ORCH-07 |
| OPS-A08 | Lost-and-Found Agent | item intake, guest matcher, shipment coordinator | (experience) |

### 5.4 Distribution & Disruption Domain (4 agents)

**Primary schema:** RESML. **Consumed schemas:** GXML, REVML.
**Decision cadence:** Second for disruption events; minute for rebooking; continuous for distribution health.

| agent_id | name | decomposition_note | primary_orch |
|---|---|---|---|
| DIS-A01 | Disruption Recovery Agent | cascade modeler, rebooking optimizer, compensation policy enforcer | ORCH-05 |
| DIS-A02 | Rebooking Agent | alternative finder, guest-preference-aware ranker, one-tap confirm gateway | ORCH-05 |
| DIS-A03 | Compensation Agent | policy mapper, offer composer, precedent tracker | ORCH-05 |
| DIS-A04 | Distribution Health Agent | channel latency monitor, content-parity checker, booking-engine health | (platform) |

---

## Part 6 — Orchestrations (ORCH-01 through ORCH-12)

Conforms to Core Part 8.2. T&H-native ORCHs occupy the same numbering slots as RC — slots are positional, not semantic (per Core Part 8.1).

| orch_id | name | domain | agents | trigger | primary_gold_view | cycle_time_slo |
|---|---|---|---|---|---|---|
| ORCH-01 | Arrival & Check-In | GXP | GXP-A05, OPS-A02 | Inbound guest arrival signal (OTA confirm, mobile app, desk intake) | GV_PROPERTY_ARRIVAL_FLOW | < 90 sec to key |
| ORCH-02 | Dynamic Rate & Channel | REV | REV-A01, REV-A03, REV-A05 | Pace/competitor signal change | GV_PROPERTY_RATE_STATE | < 15 min to channels |
| ORCH-03 | Cold Chain Integrity (F&B) | OPS | OPS-A04 | Threshold breach on F&B sensor | GV_PROPERTY_COLD_CHAIN | < 5 min to brief |
| ORCH-04 | Room Readiness | OPS | OPS-A01, OPS-A02 | Check-out event OR inspection completion | GV_PROPERTY_ROOM_PIPELINE | < 40 min avg turnaround |
| ORCH-05 | Disruption Recovery | DIS | DIS-A01, DIS-A02, DIS-A03 | Disruption event (weather, mechanical, overbooking, force majeure) | GV_TRIP_DISRUPTION_IMPACT | < 10 min to rebooking options |
| ORCH-06 | Service & Upsell | GXP/REV | GXP-A01, REV-A06, REV-A07 | Guest service request OR journey-stage trigger | GV_GUEST_SERVICE_QUEUE | < 60 sec to routing |
| ORCH-07 | Maintenance & Systems | OPS | OPS-A03, OPS-A07 | Maintenance ticket OR system anomaly | GV_PROPERTY_MAINTENANCE | < 5 min dispatch |
| ORCH-08 | Guest Incident | GXP | GXP-A02, GXP-A06, GXP-A07 | Guest complaint, negative review, service failure signal | GV_GUEST_INCIDENT_CASES | < 10 min to case file |
| ORCH-09 | Sustainability Operations | OPS | OPS-A06 | Telemetry anomaly OR reporting cycle | GV_PROPERTY_SUSTAINABILITY | Daily + event-driven |
| ORCH-10 | Demand Sensing | REV | REV-A02 | Continuous signal fusion | GV_CHAIN_DEMAND | 15-min cadence |
| ORCH-11 | Ancillary & Campaign Activation | REV | REV-A08 | Journey-stage trigger OR campaign intake | GV_GUEST_AUDIENCE | Minutes to channel |
| ORCH-12 | Guest Lifecycle & Loyalty | GXP | GXP-A03, GXP-A04 | Event-driven state change | GV_GUEST_LIFECYCLE | Continuous |

**File:** `apex-th/data/orchestrations.json`

### 6.1 ORCH-RC vs ORCH-TH slot comparison

For reference — illustrates how slots are positional:

| slot | APEX-RC | APEX-TH |
|---|---|---|
| ORCH-01 | Inbound Receiving | Arrival & Check-In |
| ORCH-02 | Price Integrity | Dynamic Rate & Channel |
| ORCH-03 | Cold Chain Integrity | Cold Chain Integrity (F&B) |
| ORCH-04 | OSA Triage | Room Readiness |
| ORCH-05 | Recall Impact | Disruption Recovery |
| ORCH-06 | Omnichannel Fulfillment | Service & Upsell |
| ORCH-07 | Shrink Signal | Maintenance & Systems |
| ORCH-08 | Customer Incident | Guest Incident |
| ORCH-09 | Assortment Optimization | Sustainability Operations |
| ORCH-10 | Demand Sensing | Demand Sensing |
| ORCH-11 | Campaign Activation | Ancillary & Campaign Activation |
| ORCH-12 | Customer Lifecycle | Guest Lifecycle & Loyalty |

---

## Part 7 — MCP Tool Catalog (Travel & Hospitality)

Conforms to Core Part 8.4 naming.

### 7.1 T&H domain codes

| code | scope |
|---|---|
| `mcp.property.*` | Property-scoped operations (hotel, resort, terminal) |
| `mcp.chain.*` | Brand-scoped (multi-property) operations |
| `mcp.guest.*` | Guest-scoped operations |
| `mcp.booking.*` | Reservation / booking operations |
| `mcp.rate.*` | Rate and yield operations |
| `mcp.channel.*` | Distribution channel operations |
| `mcp.loyalty.*` | Loyalty program operations |
| `mcp.housekeeping.*` | Housekeeping operations |
| `mcp.maintenance.*` | Maintenance operations |
| `mcp.disruption.*` | Disruption recovery operations |
| `mcp.fnb.*` | Food and beverage operations |
| `mcp.sustainability.*` | Energy, water, sustainability operations |
| `mcp.flight.*` | Airline-specific (flight ops, irregular ops) |
| `mcp.sailing.*` | Cruise-specific (voyage ops, onboard) |

### 7.2 Catalog target

Initial catalog: ~60 tools. Seed catalog for Wave 1 (Property 201 reference implementation): ~28 tools.

**File:** `apex-th/data/tools.json`

---

## Part 8 — ISV Ecosystem (Travel & Hospitality)

Reference catalog — clients select per existing estate.

| category | isv_examples | microsoft_integration |
|---|---|---|
| Property Management Systems | Oracle Opera (hospitality), Mews, Cloudbeds, Infor HMS, Stayntouch | API / Fabric |
| Central Reservation Systems | Sabre SynXis, Amadeus HotSOS / iHotelier, Derbysoft | API |
| Revenue Management | IDeaS (SAS), Duetto, Atomize, Pace Revenue | API / Fabric |
| Airline GDS / PSS | Sabre, Amadeus Altéa, Travelport | API |
| Customer Data / CDP | D365 Customer Insights, Amperity, Tealium | Native / Fabric |
| Loyalty Platforms | Salesforce Loyalty, Comarch, Marigold | API |
| Guest Messaging | Kipsu, Medallia, Akia, Zingle (Medallia) | API |
| Housekeeping / Ops | HotSOS, Quore, Alice, Flexkeeping | API |
| Airline Operations | Sabre MOVEMENT, Amadeus Altéa Departure Control | API |
| IoT / Property Systems | Honeywell Forge, Schneider EcoStruxure, Siemens Desigo | Azure IoT Hub |
| Energy / Sustainability | Enel X, Verdantix, Measurabl | Fabric integration |
| Distribution Health | Triptease, OTA Insight (now Lighthouse) | API |

**File:** `apex-th/data/isv-ecosystem.json`

---

## Part 9 — Wave Content (Travel & Hospitality)

Conforms to Core Part 12.2 contract.

| wave | name | scope | duration | entry | exit | economic_case |
|---|---|---|---|---|---|---|
| W1 | Foundation | L1–L4 stand-up; RESML + OPSML Silver/Gold; first 3–5 agents (rate, room readiness, service routing); pilot at 1–3 properties | 4–6 mo | CMM-1 or CMM-2 | CMM-3 readiness | Room readiness cycle time + ancillary revenue uplift + service SLA improvement — 90-day payback signal |
| W2 | Expansion | GXML + REVML canonical; first full REV ORCH stack; 10–15 agents; 25–50 properties | 6–9 mo | CMM-3 | Early CMM-4 | RevPAR uplift + disruption recovery cost reduction + labor productivity |
| W3 | Platform | Cross-domain ORCHs; full 30-agent fleet; brand-wide rollout | 9–12 mo | CMM-4 entry | CMM-4 full | Enterprise disruption handling; GM/GuestX productivity flip; loyalty P&L visibility |
| W4 | Adaptive | Continuous-learning harnesses; fleet self-optimization; cross-property planning | Ongoing | CMM-4 | CMM-5 | Compounding returns as fleet improves itself |

**File:** `apex-th/data/waves.json`

---

## Part 10 — Reference Implementations (TH)

| ref_impl | scope | status | spec |
|---|---|---|---|
| **Property 201 Day-in-the-GM-Seat** | Single full-service hotel, single day, 8 events across REV/GXP/OPS/DIS, ORCH-01 through ORCH-08 | **To be built** | `apex-th-property-201-build-spec.md` (stub) |
| RefImpl-02 Disruption Cascade | Regional weather event cascading across a brand; multi-property rebooking coordination | Reserved | TBD |
| RefImpl-03 Compression Week | Citywide compression event; yield optimization across brand's properties | Reserved | TBD |
| RefImpl-04 Loyalty Journey | Cross-property loyalty journey from booking through stay through post-stay | Reserved | TBD |

**File:** `apex-th/data/ref-implementations.json`

### 10.1 Property 201 as T&H analog to Store 100

Property 201 (working name) should mirror Store 100's narrative structure:
- Single location, single shift (General Manager's day, 6 AM – 10 PM compressed)
- 8 events spanning the four domains (REV, GXP, OPS, DIS)
- Mix of HITL / ACK_ONLY / ZERO_TOUCH / ESCALATION gates
- Cinematic editorial HTML, dark + light themes
- Schema Lit Up / Agent Response / Decision / Outcome blocks per event

**Suggested event spine for Property 201:**
1. 6:15 AM — Overnight F&B cold chain excursion (ORCH-03)
2. 7:40 AM — Compression event detected for the weekend; rate surge opportunity (ORCH-02)
3. 9:22 AM — Housekeeping pipeline bottleneck; early-arrival VIP at risk (ORCH-04)
4. 10:45 AM — HVAC cascade failure on tower 3 floors 12–18 (ORCH-07)
5. 12:10 PM — Regional airport disruption; inbound guests rebooking flights, some arriving late (ORCH-05)
6. 1:35 PM — Upsell offer autonomous flow for a loyalty Platinum arrival (ORCH-06, ZERO_TOUCH)
7. 3:14 PM — Guest incident at the pool, food-safety allegation (ORCH-08)
8. 4:50 PM — Sustainability anomaly: water consumption spike pattern-matched to a systemic leak (ORCH-09)

---

## Part 11 — Solution Stack (TH)

Conforms to Core Part 13 column contract. ~50 rows.

**Row distribution:**
- 7 rows — L1–L2 infrastructure (PMS, CRS, RMS, Event Hubs, Fabric, OneLake, IoT Hub)
- 4 rows — L3–L4 schema registries (RESML, GXML, REVML, OPSML)
- 4 rows — Gold view categories (property ops, guest, revenue, sustainability)
- 30 rows — Agent fleet (one per TH agent)
- 12 rows — ORCH definitions
- (balance) — L7 experiences and ISV bindings

**File:** `apex-th/data/solution-stack.json`

---

## Part 12 — File Structure (TH)

```
apex-th/
├── README.md                               # This spec
├── CHANGELOG.md                            # TH version history
├── index.html                              # TH framework site
├── /data/
│   ├── forces-of-change.json               # Part 2
│   ├── cmm-signals.json                    # Part 3
│   ├── schemas.json                        # Part 4
│   ├── agents.json                         # Part 5 (30 agents)
│   ├── orchestrations.json                 # Part 6 (12 ORCHs)
│   ├── tools.json                          # Part 7 MCP catalog
│   ├── isv-ecosystem.json                  # Part 8
│   ├── waves.json                          # Part 9
│   ├── ref-implementations.json            # Part 10
│   └── solution-stack.json                 # Part 11
└── /ref-impl/
    └── /property-201/                      # To be built
        ├── index.html
        └── /data/
```

---

## Part 13 — Build Sequence

Six phases. Consumes Core widgets and design system. Mirrors APEX-RC Phase structure for consistency across editions.

### Phase 1 — TH framework skeleton
**Deliverable:** `index.html` rendering Parts 1–6 and 9 as static content.
**Imports from Core:** design tokens, typography, components CSS; theme.js, navigation.js.
**Extends:** adds `--th-accent: #2a9d8f` to its local stylesheet.
**Acceptance:** Parts 1–6 and 9 render; theme toggle works; AA contrast both themes; masthead wordmark uses `--th-accent`.

### Phase 2 — Domain architecture
**Deliverable:** Part 5 (four domain tabs: REV / GXP / OPS / DIS) interactive.
**Imports from Core:** `/js/domain-tabs.js`.
**Acceptance:** Four domain tabs cross-fade; agent rows hover-expand to show sub-agents.

### Phase 3 — ORCH + MCP + Gold views
**Deliverable:** Parts 6, 7 interactive.
**Imports from Core:** `/js/orch-expander.js`.
**Acceptance:** 12 ORCH rows click-to-expand; tool catalog filterable by domain code; slot-comparison table (Part 6.1) rendered.

### Phase 4 — Solution Stack Chart
**Deliverable:** Part 11 interactive with ≥50 rows.
**Imports from Core:** `/js/solution-stack.js`.
**Acceptance:** Filter by layer/domain/wave/CMM; sortable; row-click detail panel.

### Phase 5 — Wave Timeline + ISV Ecosystem
**Deliverable:** Parts 8, 9 interactive.
**Imports from Core:** `/js/wave-timeline.js`.
**Acceptance:** Hover-reveal of wave exit criteria; ISV catalog filterable.

### Phase 6 — Reference Implementations hub
**Deliverable:** Part 10 with Property 201 stub card visible.
**Acceptance:** Card grid for ref-impls; Property 201 card is a "Coming Wave 1" stub; RefImpl-02/03/04 as "Reserved" cards.

---

## Part 14 — Acceptance Criteria

Per Core Part 11, TH is Core-conformant when:

1. ☐ Folder exists as `apex-th/` parallel to `apex-core/` and `apex-rc/`
2. ☐ README declares code TH, version, Core spec version referenced
3. ☐ 8 Forces of Change defined (Part 2 above)
4. ☐ Eras and CMM referenced unchanged; CMM signals added (Part 3)
5. ☐ 4 schemas defined (RESML, GXML, REVML, OPSML)
6. ☐ Event envelope inherited unchanged with TH controlled vocabulary
7. ☐ 12 ORCHs defined with contracts (Part 6)
8. ☐ MCP tool catalog with T&H domain codes (Part 7)
9. ☐ Design system inherited; `--th-accent` added
10. ☐ Core widgets consumed, not reimplemented
11. ☐ Part 0 compliance passes lint
12. ☐ Solution Stack has ≥50 rows per Core Part 13 contract
13. ☐ At least one reference implementation planned (Property 201 stub)

---

## Part 15 — T&H-Specific Design Considerations

### 15.1 Visual atmosphere

The T&H edition leans into a slightly warmer visual tone than RC to evoke hospitality rather than retail efficiency:

- Masthead hero image treatment: subtle horizon gradient (teal-jade to warm gold) evoking travel horizons
- Event cards in reference implementations lean into cinematic imagery references (no actual photography — SVG and gradient treatments only)
- Typography unchanged (Fraunces / Instrument Sans / JetBrains Mono per Core)

### 15.2 Narrative voice for T&H reference implementations

Where RC's Store 100 voice is "operational calm under pressure" (Marisol the store manager), TH's Property 201 voice should be "seasoned hospitality leadership" — more gracious, less tactical. The agents serve a General Manager who is responsible for guest experience as a brand asset, not only for operational KPIs.

### 15.3 Status language in T&H

T&H uses different operational vocabulary that should show up in copy:

- **"Disruption"** not "exception" for weather / mechanical / irregular events
- **"Recovery"** not "remediation" for making a guest whole
- **"Arrival"** and **"departure"** not "inbound" and "outbound"
- **"Property"** / **"house"** / **"hotel"** not "store" or "location"
- **"Guest"** not "customer" (except in loyalty P&L conversations where "member" is used)
- **"Stay"** / **"trip"** / **"sailing"** as the unit of lifecycle, not "order" or "basket"

---

## Part 16 — Handoff Notes to Claude Code

**Read Core first.** Every convention, template, and widget contract lives in `apex-core-build-spec.md`. Do not begin this build without it.

**Study APEX-RC as a sibling reference.** The RC spec (`apex-rc-build-spec-v2.md`) shows how an edition inherits from Core. TH follows the same inheritance pattern but with T&H-native content.

**The vocabulary discipline in Part 15.3 is not cosmetic.** It's a brand-positioning constraint. A T&H client reading APEX-TH copy should feel the framework was built for their industry, not retrofitted from retail. Every "store" that accidentally survives translation into "property" breaks that trust.

**Property 201 is T&H's Store 100.** When it's time to build the first T&H reference implementation, mirror Store 100's cinematic editorial structure and production values. The event spine sketched in Part 10.1 is a starting point, not a requirement — refine with subject-matter review before committing to the build.

**Airline and cruise are sub-variants, not separate editions.** Keep them inside APEX-TH with specialized dimensional anchors (Part 4.1) and domain-specific MCP tool prefixes (`mcp.flight.*`, `mcp.sailing.*`). Only split to a new edition if the core vocabulary truly diverges (which it doesn't for lodging + airline + cruise).

**TH's ORCH-05 (Disruption Recovery) is likely the single most differentiated orchestration in APEX.** It deserves the most detailed contract documentation. Retail has no direct analog; RC's ORCH-05 (Recall Impact) is the closest structural sibling but the operational tempo and guest-facing nature are fundamentally different. Invest accordingly in the Property 201 reference implementation's treatment of Event 5 (regional airport disruption).

---

**End of APEX-TH specification · v1.0**

*Parent spec:*
- *`apex-core-build-spec.md` v1.0*

*Sibling edition:*
- *`apex-rc-build-spec-v2.md` — Retail & Consumer edition*

*Child reference implementation (planned):*
- *`apex-th-property-201-build-spec.md` — to be built*
