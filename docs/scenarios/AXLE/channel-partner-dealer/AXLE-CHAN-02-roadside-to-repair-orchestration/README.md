# Roadside-to-repair orchestration — connected commercial-vehicle fleet

**Practice:** AXLE — Automotive & Manufacturing
**Domain:** channel-partner-dealer
**Scenario index:** 02 of 5 featured
**Service code:** `AXLE-CHAN-02`
**Headline KPI:** ↓ -38% truck dwell time (event → wheels-rolling)
**Source narrative:** worked-example chain authored 2026-05-26 for connected-fleet OEM dealer-network engagement; cites DTNA / Detroit Connect telemetry as the real-world referent for the connected-vehicle integration plane.

## Scenario

A Class-8 tractor throws a fault code on a long-haul corridor. Engine derates. The driver pulls onto the shoulder or, if lucky, into a dealer lounge. Today: the driver calls dispatch, dispatch calls the dealer, the dealer triages by phone, the truck is towed in cold, the bay opens it up, parts are wrong, the wrong dealer was picked, the load is late, the ELD clock burns. Mean event-to-wheels-rolling time is 11.4 hours. Two hours of that is mechanic work. The other 9 are coordination loss across six actor lanes that don't share a system of record.

The actor lanes (canonical for this scenario):

| Lane | Actor / surface |
|---|---|
| Driver | In the cab, on the shoulder, or in the dealer lounge |
| Fleet Dispatcher | Back at HQ, juggling loads + ELD hours |
| Service Writer | At the dealer, scheduling the bay |
| Mechanic | At the bay, doing the work |
| DTNA Field Ops (OEM) | Watching the connected-fleet telemetry |
| Parts | Dealer + regional + OEM central — pre-positioning inventory |
| The Agent Fleet | The orchestration layer making it all compose |

## Solution

A six-agent fleet, orchestrated on Microsoft-native infrastructure, that converts the breakdown event into a synchronized work plan across all six human lanes — and proves out the eight-phase chain (P1 Event → P8 Release + Learn) in ≤90 minutes wheels-to-wheels for the addressable 70% of fault classes.

| Agent | Role |
|---|---|
| **Diagnostic** | Reads Detroit Connect telemetry, composes prognosis + confidence; resolves fault code to candidate root-causes |
| **Dispatch** | Selects best dealer by capacity × parts coverage × geo × ELD-hours; reroutes load |
| **Service-Writer Brief** | Pre-stages the work order; books the bay; gives the writer a one-screen brief |
| **Parts Pre-Position** | Stages dealer + regional + OEM-central inventory; triggers transfer if needed |
| **Bay-Assist** | Walks junior mechanics through the procedure; HITL on torque/release; captures evidence |
| **Audit + Learn** | Seals the audit row to Purview; routes the resolved case back into the prognosis model |

Each agent is bounded, has a single OneLake schema family it owns, and writes its decisions to a single Bronze→Silver→Gold ledger. The orchestrator is platform-managed (Foundry); no agent calls another directly.

## Use Case

Connected commercial-vehicle OEM pilot: 1 corridor (I-80 Reno → Salt Lake City), 1 OEM region, 14 dealer locations, ~3,800 connected Class-8 tractors under a single fleet customer. Reads `AXLEML.Equipment`, `AXLEML.Telemetry`, `AXLEML.WorkOrder`, `AXLEML.PartsInventory`, `AXLEML.DealerCapacity`, `AXLEML.DriverHOS`. Writes work-order pre-stage, parts-transfer requests, audit rows. Wave 2 pilot scope; Wave 3 expands to 6 corridors and full OEM region rollout.

## Service

`AXLE-CHAN-02` — Connected-fleet roadside-to-repair orchestration. Sits adjacent to `AXLE-CHAN-01` (dealer-inventory visibility) and consumes its Gold mart for the dealer-selection step. W2 at corridor pilot; W3 at OEM-region scale; W3-fusion with `AXLE-ASSET-09` (MTBF forecasting) feeds the Diagnostic agent's prognosis confidence interval.

## Personas

**Primary**

- **Cassie Whitford · Fleet Dispatcher (operator) · synthetic.** Lives in the dispatch console. Approves dealer reroute + load-replanning decisions at the P4 HITL gate. Today owns 80% of the coordination loss; the agent fleet collapses that to a single approval click + an exception queue.

**Secondaries**

- **Mike Tobler · Service Writer (dealer) · synthetic.** Receives the pre-staged work order and parts manifest; confirms the bay slot. P5 HITL gate.
- **Jorge Almeida · Mechanic, Tier-2 (dealer bay) · synthetic.** Executes the repair with Bay-Assist; HITL on torque-spec confirmation and final release.
- **Ana DTNA · OEM Field Ops · synthetic.** Sees the corridor-level telemetry roll-up; intervenes only on prognosis-confidence outliers.
- **Driver (informational lane).** Sees status via the cab telematics surface; not a decision-maker in the chain.

All persona identifiers are synthetic per APEX-Core Part 0.

## KPIs

- **Truck dwell time (event → wheels-rolling):** target ↓ 38% (11.4 hr → 7.0 hr corridor-wide); ↓ 70% for the addressable 70% of fault classes (target ≤90 min)
- **First-time fix rate:** target ↑ 18pp (parts-correct on first bay visit)
- **Dispatch decision-loop time:** target ≤ 90 sec (Cassie's approval at P4 HITL gate)
- **Audit-row completeness:** 100% of repair events sealed to Purview within 5 min of P8

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

- **W1 Foundation.** Detroit Connect → Event Hubs ingest; OneLake Bronze landing; AXLEML.Equipment + AXLEML.Telemetry canonical schemas; Entra ID + Purview baselined; dealer-capacity SOR adapter built.
- **W2 Pilot.** Six-agent fleet stood up in Foundry against the corridor pilot; Cassie + Mike on the HITL gates; Power BI dispatch console live; smoke-test fixture green.
- **W3 Scale & Fuse.** OEM-region rollout; fusion with `AXLE-ASSET-09` MTBF; cross-corridor learning feedback loop closed; executive dwell-KPI rollup on the OEM CX dashboard.

---

## The runnable chain — Azure substrate

This block binds the 8 narrative phases (P1–P8) to the canonical APEX 24-step runnable chain per [Use-Case Template — The Runnable Scenario Chain](../../../APEX%20-%20Design%20and%20Build/Use-Case-Template-Runnable-Chain.md). Same fixture drives the chain on laptop / dev / stage / prod; only the substrate routing differs.

### Phase → chain-step mapping

| Phase | When | Chain steps | Azure surface |
|---|---|---|---|
| P1 · Event | T=0 | step 1 (SOR) | Detroit Connect telemetry + ELD; fault code emitted to OEM cloud |
| P2 · Telemetry | T+30s | steps 1–7 (SOR → Canonical → Schemas) | Event Hubs → Fabric Eventstream → OneLake Bronze → Silver (AXLEML.Telemetry) |
| P3 · Diagnosis | T+2 min | steps 8–12 (Trigger → Orchestrator → Assess / Classify / Quantify) | Foundry agents: Diagnostic composes prognosis; Bay-Assist preloads procedure candidates |
| P4 · Dispatch | T+5 min | steps 13–14 (Decide + HITL gate) | Foundry Dispatch agent + Power BI / Teams adaptive card; **HITL: Cassie Whitford** |
| P5 · Pre-position | T+15 min | step 15 (Act) + step 11 re-run (Parts Classify) | Foundry Parts Pre-Position agent → Inventory API + transfer requests; **HITL: Mike Tobler** |
| P6 · Arrive | T+30–90 min | step 15 (Act continued) | Truck/tow arrives; bay opens with pre-staged WO + parts |
| P7 · Repair | T+2–4 hr | step 15 (Act) + step 14 (HITL) + step 16 (Learn) | Foundry Bay-Assist; **HITL: Jorge Almeida** on torque + release |
| P8 · Release + learn | T+complete | steps 17–18 (KPI rollup, Power BI) + steps 19–24 (Scale / Fusion / Trust / Feedback / Executive / Ledger) | Power BI dispatch + OEM exec dashboard; Purview audit seal; resolved case feeds prognosis model retrain |

### chain_execution (YAML)

```yaml
chain_execution:
  scenario_id: AXLE-CHAN-02

  steps:
    - step: 1
      key: w1-sor
      executed_by: platform
      data_read: [AXLEML.Equipment, AXLEML.Telemetry, AXLEML.DriverHOS]
      data_written: [AXLEML.Telemetry]
      kpi_affected: null
      decision_point: false
      mock_endpoint: http://localhost:8810/inject
      notes: Detroit Connect fault code + ELD HOS land in Event Hubs

    - step: 7
      key: w1-canonical
      executed_by: platform
      data_read: [AXLEML.Telemetry]
      data_written: [AXLEML.Telemetry.silver]
      kpi_affected: null
      decision_point: false
      notes: Bronze → Silver canonicalization in Fabric

    - step: 8
      key: w2-trigger
      executed_by: platform
      data_read: [AXLEML.Telemetry.silver]
      data_written: [AXLEML.Trigger]
      kpi_affected: null
      decision_point: false
      notes: Fabric RTI rule fires when fault code + severity crosses threshold

    - step: 10
      key: w2-assess
      executed_by: diagnostic
      data_read: [AXLEML.Telemetry.silver, AXLEML.Equipment, AXLEML.MaintenanceHistory]
      data_written: [AXLEML.Prognosis]
      kpi_affected: dwell-time-reduction-pct
      decision_point: false
      notes: Diagnostic agent composes prognosis + confidence

    - step: 11
      key: w2-classify
      executed_by: dispatch
      data_read: [AXLEML.Prognosis, AXLEML.DealerCapacity, AXLEML.PartsInventory, AXLEML.DriverHOS]
      data_written: [AXLEML.DealerCandidate]
      kpi_affected: dwell-time-reduction-pct
      decision_point: false
      notes: Rank dealers by capacity × parts × geo × HOS

    - step: 12
      key: w2-quantify
      executed_by: parts-preposition
      data_read: [AXLEML.DealerCandidate, AXLEML.PartsInventory]
      data_written: [AXLEML.PartsPlan]
      kpi_affected: first-time-fix-rate-pp
      decision_point: false
      notes: Compute parts staging plan (dealer + regional + OEM-central)

    - step: 13
      key: w2-decide
      executed_by: dispatch
      data_read: [AXLEML.DealerCandidate, AXLEML.PartsPlan]
      data_written: [AXLEML.DispatchProposal]
      kpi_affected: dispatch-decision-loop-time-sec
      decision_point: false
      notes: Compose the dispatch proposal for HITL

    - step: 14
      key: w2-hitl
      executed_by: dispatch
      data_read: [AXLEML.DispatchProposal]
      data_written: [AXLEML.DispatchDecision, AXLEML.AuditEvent]
      kpi_affected: dispatch-decision-loop-time-sec
      decision_point: true
      hitl_threshold_ref: dispatch-confidence-band
      personas_involved: [cassie-whitford-fleet-dispatcher]
      notes: Cassie approves dealer + reroute in Teams adaptive card / Power BI

    - step: 15
      key: w2-act
      executed_by: service-writer-brief
      data_read: [AXLEML.DispatchDecision, AXLEML.PartsPlan]
      data_written: [AXLEML.WorkOrder, AXLEML.PartsTransferRequest]
      kpi_affected: first-time-fix-rate-pp
      decision_point: true
      hitl_threshold_ref: service-writer-bay-slot
      personas_involved: [mike-tobler-service-writer]
      notes: Pre-stage WO + transfer parts; Mike confirms bay slot

    - step: 15
      key: w2-act-repair
      executed_by: bay-assist
      data_read: [AXLEML.WorkOrder, AXLEML.RepairProcedure]
      data_written: [AXLEML.RepairEvent, AXLEML.AuditEvent]
      kpi_affected: first-time-fix-rate-pp
      decision_point: true
      hitl_threshold_ref: torque-and-release
      personas_involved: [jorge-almeida-mechanic]
      notes: Bay-Assist walks the repair; Jorge confirms torque + release

    - step: 16
      key: w2-learn
      executed_by: audit-learn
      data_read: [AXLEML.RepairEvent, AXLEML.Prognosis]
      data_written: [AXLEML.LearningSignal]
      kpi_affected: null
      decision_point: false
      notes: Compare prognosis to actual; emit retrain signal

    - step: 17
      key: w2-kpi
      executed_by: platform
      data_read: [AXLEML.RepairEvent, AXLEML.AuditEvent]
      data_written: [AXLEML.KpiRollup.gold]
      kpi_affected: dwell-time-reduction-pct
      decision_point: false
      notes: Gold KPI mart in Fabric for Power BI

    - step: 18
      key: w2-bi
      executed_by: platform
      data_read: [AXLEML.KpiRollup.gold]
      data_written: []
      kpi_affected: null
      decision_point: false
      notes: Power BI dispatch console + OEM exec dashboard

    - step: 22
      key: w3-feedback
      executed_by: platform
      data_read: [AXLEML.LearningSignal]
      data_written: [AXLEML.ModelRetrainQueue]
      kpi_affected: null
      decision_point: false
      notes: Resolved cases feed Diagnostic agent retrain in Foundry
```

### persona_kpi_attribution (YAML)

```yaml
persona_kpi_attribution:
  cassie-whitford-fleet-dispatcher:
    - kpi: dwell-time-reduction-pct
      mechanism: |
        Approves dealer-reroute + load-replan decisions at P4. Today the
        same call takes ~22 min of phone tag across dispatch + dealer +
        driver; the HITL gate collapses it to a single Teams approval
        with the proposal pre-composed.
      decision_steps: [14]
      direction: decrease
      magnitude_basis: coordination minutes saved per event × events per corridor
    - kpi: dispatch-decision-loop-time-sec
      mechanism: Speed of HITL approval — current 22 min, target ≤ 90 sec
      decision_steps: [14]
      direction: decrease
      magnitude_basis: time-from-proposal-to-decision

  mike-tobler-service-writer:
    - kpi: first-time-fix-rate-pp
      mechanism: |
        Confirms bay slot + parts-staging plan at P5. Catching a parts
        gap before the truck arrives is what makes the repair single-visit.
      decision_steps: [15]
      direction: increase
      magnitude_basis: parts-correct-on-first-bay-visit rate

  jorge-almeida-mechanic:
    - kpi: first-time-fix-rate-pp
      mechanism: |
        Executes the repair with Bay-Assist; HITL on torque + release
        prevents the rework that kills first-time-fix.
      decision_steps: [15]
      direction: increase
      magnitude_basis: rework events avoided per 100 repairs
```

### smoke_test (YAML)

```yaml
smoke_test:
  fixture_path: docs/scenarios/AXLE/channel-partner-dealer/AXLE-CHAN-02-roadside-to-repair-orchestration/tests/fault-event.json
  trigger_event:
    type: detroit-connect-fault-code
    inject_into: step:1
  expected_outcome:
    chain_completed: true
    hitl_triggered: true
    hitl_persona: cassie-whitford-fleet-dispatcher
    audit_row_written: true
    kpi_attribution:
      dwell-time-reduction-pct: "<= 0"
      dispatch-decision-loop-time-sec: "< 120"
      first-time-fix-rate-pp: ">= 0"
  laptop_command: |
    docker-compose up -d
    curl -X POST http://localhost:8810/inject \
      -H "Content-Type: application/json" \
      -d @docs/scenarios/AXLE/channel-partner-dealer/AXLE-CHAN-02-roadside-to-repair-orchestration/tests/fault-event.json
```

---

## Azure substrate wiring (W2 pilot)

| APEX plane | Azure service | Purpose in this scenario |
|---|---|---|
| Integration | **Event Hubs** + **Fabric Eventstream** | Ingest Detroit Connect fault codes + ELD HOS |
| Data — Bronze/Silver/Gold | **Microsoft Fabric (OneLake)** | Medallion landing for telemetry, work-order, parts, capacity |
| Real-time trigger | **Fabric Real-Time Intelligence (RTI)** | Threshold rule that fires the orchestrator |
| Orchestration + Agents | **Azure AI Foundry** (agents project) | Diagnostic / Dispatch / Service-Writer-Brief / Parts-Preposition / Bay-Assist / Audit-Learn |
| HITL surface | **Copilot Studio** + **Teams adaptive cards** + **Power BI** | Cassie / Mike / Jorge approval gates |
| BI + KPI rollup | **Power BI** in Fabric | Dispatch console, OEM exec dwell dashboard |
| Identity | **Microsoft Entra ID** | Per-persona role; dealer-scoped data access |
| Secrets | **Azure Key Vault** | Detroit Connect API key, dealer SOR creds |
| Audit | **Microsoft Purview** | Per-event audit row at steps 14 / 15 / 16 |
| Compute (UI surfaces) | **Azure App Service** | Dispatch console host — created with `--https-only true` per subscription policy |
| Deploy | **Bicep** + **az CLI** | W2 pilot infra-as-code |

All services deploy Microsoft-native; no third-party platform sits on the critical path.

---

## Open questions for the engagement to close

These are the deltas a real engagement converts from template to client-specific use case (see [Use-Case-Template-Runnable-Chain.md §6](../../../APEX%20-%20Design%20and%20Build/Use-Case-Template-Runnable-Chain.md)):

1. **HITL thresholds.** What confidence band on the Diagnostic prognosis lets Dispatch auto-decide vs. page Cassie? (`dispatch-confidence-band` threshold key.)
2. **Dealer scoring weights.** How is capacity × parts × geo × HOS weighted in the dealer-rank model? Engagement-specific.
3. **Parts transfer SLA.** What is the regional-warehouse transfer SLA that makes P5 viable? Drives the W2 corridor selection.
4. **OEM/fleet data-sharing posture.** Which AXLEML.Telemetry fields can the OEM share to the fleet's tenant, and at what latency? Sets the Bronze partition design.
5. **Foundry project topology.** One project per OEM region, or one per dealer-network? Drives `foundry.project_ref` in the use case YAML.

## Artifacts to land in this folder

- `APEX-roadside-to-repair-build-guide.md` — step-by-step Azure build (W1 plumbing → W2 agent stand-up → W3 fusion)
- `APEX-roadside-to-repair-walkthrough.docx` — narrative walkthrough for sellers
- `tests/fault-event.json` — smoke-test fixture (synthetic fault code + ELD payload)
- `manifests/` — Foundry agent manifests, Fabric workspace manifest, Bicep parameter set
- `artifacts/` — actor-lane diagram, phase-timeline diagram, dispatch-console mockup

## Cross-references

- Practice overview: [../README.md](../README.md)
- Sibling scenario (consumed Gold mart): [../AXLE-CHAN-01-dealer-inventory-visibility/README.md](../AXLE-CHAN-01-dealer-inventory-visibility/README.md)
- W3 fusion candidate: [../../asset-maintenance/AXLE-ASSET-09-mean-time-between-failure-forecasting/README.md](../../asset-maintenance/AXLE-ASSET-09-mean-time-between-failure-forecasting/README.md)
- Compact catalog row: [../_browse-catalog.md](../_browse-catalog.md)
- Runnable chain template: [../../../APEX - Design and Build/Use-Case-Template-Runnable-Chain.md](../../../APEX%20-%20Design%20and%20Build/Use-Case-Template-Runnable-Chain.md)
- APEX Design: [../../../APEX - Design and Build/APEX_Design.md](../../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
