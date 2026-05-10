# Use Case Template — The Runnable Scenario Chain

**Audience:** Engagement leads, agent designers, anyone authoring a use case
**Purpose:** Define how a use case binds the 24-step scenario chain to specific agent roles, personas, KPI attribution paths, and a smoke-test fixture — so the use case is **executable end-to-end on the laptop substrate** and traceable for audit on cloud substrates.

**First iteration scope:** Retail & Consumer (RC) practice only. The 5 featured RC scenarios are the canonical worked examples; HLS / ER / AXLE / TH / TMT / ICE follow per the [Sprint Plan §58+](Sprint-Plan.md#sprints-57-second-client--hls-kickoff).

**Reference:**
- [Use case schema](../../services/_use-case.schema.md)
- [Deploy UX and Substrates](Deploy-UX-and-Substrates.md)
- [Services Guide §18](../book/Professional-APEX-M-Services-Guide.html#ch-18) — RC service profiles
- Working example: [`services/rc/RC-E2E-03/use-cases/_default/use-case.yaml`](../../services/rc/RC-E2E-03/use-cases/_default/use-case.yaml)

---

## 1. What "runnable" means

A use case is **runnable** when an engineer on Docker Desktop can:

1. `docker-compose up` from the wizard's rendered output
2. POST a synthetic event to a mock SOR endpoint (the `smoke_test.fixture` payload)
3. Watch the 24-step chain execute end-to-end through the agent fleet
4. Confirm: HITL gate fires at the right step for the right persona; audit row writes to mock Purview; KPI attribution paths land in the right Gold mart

The same chain runs unchanged on `dev` / `stage` / `prod` against real Foundry / Fabric / Purview. Substrate differs; chain semantics do not.

## 2. The five blocks of a runnable use case

```
use_case_id, service_code, primary_variant, substrate
        ▼
    [ identity blocks — see use-case.schema.md §1-3 ]
        ▼
    [ client_approved_architecture — adapter wiring ]
        ▼
    [ personas_active, kpis_targeted, hitl_thresholds, agent_overrides, foundry, deployment ]
        ▼
    [ chain_execution ]                ◄── NEW · the runnable specification
        ▼
    [ persona_kpi_attribution ]        ◄── NEW · who affects which KPI and how
        ▼
    [ smoke_test ]                     ◄── NEW · the runnable evidence
```

The first three blocks are **what to deploy**. The last three are **what should happen** when it runs — the executable specification.

## 3. The `chain_execution` block

Maps each of the 24 chain steps from `scenario.yaml` to the agent role(s) that execute it, what they read/write, what KPI they affect, and whether the step is a HITL decision point.

### Schema

```yaml
chain_execution:
  scenario_id: <must match scenario.yaml's scenario_id>

  steps:
    - step: <int 1..24>                    # matches chain_24[*].step
      key: <string>                        # matches chain_24[*].key (e.g., w1-sor)
      executed_by: <role | "platform">     # apex-agent role; "platform" = framework
      data_read: [<schema>.<entity>, ...]  # APEX-Core schemas read
      data_written: [<schema>.<entity>, ...]
      kpi_affected: <kpi-id | null>        # references services/_kpis.yaml
      decision_point: <bool>               # true = HITL gate fires here
      hitl_threshold_ref: <threshold-key>  # required if decision_point: true
      personas_involved: [<persona-id>, ...]  # who is on the gate
      mock_endpoint: <url-template>        # laptop substrate only — for fixtures
      notes: <free-text>
```

### Step → role mapping (APEX canonical)

The 24 steps follow the W1 (Foundation) → W2 (Pilot) → W3 (Scale & Fuse) layout. Default agent-role assignments per APEX three-layer cake:

| Step range | Layer | Default executor |
|---|---|---|
| 1–7 (Foundation: SOR, RTH, Bronze, Tokenizer, Silver, Canonical, Schemas) | Integration + Data Plane | `platform` (no agent involvement) |
| 8–9 (Trigger, Orchestrator) | Runtime Plane | `platform` (orchestrator) |
| 10–12 (Agent 1: Assess, Agent 2: Classify, Agent 3: Quantify) | Decision Plane | `assess`, `classify`, `quantify` |
| 13–14 (Agent 4: Decide, HITL Gate) | Decision Plane + Experience Plane | `decide` + persona |
| 15–16 (Agent 5: Act, Agent 6: Learn) | Decision Plane | `act`, `learn` |
| 17–18 (KPI rollup, Power BI surface) | Experience Plane · BI | `platform` |
| 19–22 (Scale, Fusion, Trust, Feedback) | W3 enterprise + Governance | `platform` (W3) |
| 23–24 (Executive KPI, Feedback loop) | Experience · Executive + Ledger · Feedback | `platform` |

When a service composes more than 6 agents (e.g., RC-E2E-03 adds **The Pricer**), the `executed_by` field shifts: The Pricer typically takes step 12 (Quantify) and feeds step 13 (Decide). Custom service-specific roles defined in `services/_extras.yaml` extend the mapping.

## 4. The `persona_kpi_attribution` block

Documents the cause-and-effect link between persona decisions and KPI movement. This is the **audit trail spec** for KPI attribution and the answer to "how did this persona move this number?"

### Schema

```yaml
persona_kpi_attribution:
  <persona-id>:
    - kpi: <kpi-id>                # references services/_kpis.yaml
      mechanism: <string>          # explanation of how this persona affects this KPI
      decision_steps: [<step-id>]  # steps where this persona acts
      direction: <"increase" | "decrease" | "either">
      magnitude_basis: <string>    # what drives the size of the effect
```

### Worked example (RC-E2E-03)

```yaml
persona_kpi_attribution:
  marisol-reyes-store-ops:                       # Store Operations Lead
    - kpi: shrink-cost-reduction-pct
      mechanism: |
        Approves or denies destroy/markdown decisions for cold-chain
        excursions. Faster + more accurate decisions = less perishable
        loss = lower shrink cost.
      decision_steps: [13, 14]                   # decide + HITL gate
      direction: decrease
      magnitude_basis: number of excursions × per-event margin protected
    - kpi: decision-loop-time-sec
      mechanism: Speed of HITL approval — current 12 min, target 90 sec
      decision_steps: [14]
      direction: decrease
      magnitude_basis: human review time

  daniel-chen-merch-director:                    # Merchandising Director
    - kpi: gm-pp-lift
      mechanism: |
        Reviews weekly markdown proposal in Power BI; approves The Pricer's
        per-SKU-per-store recommendations via Copilot chat. Better-optimized
        markdowns = higher realized gross margin.
      decision_steps: [14]                       # weekly batch HITL review
      direction: increase
      magnitude_basis: category-level price-elasticity gap closed
    - kpi: markdown-to-clear-pct
      mechanism: Category-level markdown cadence; faster clear = better velocity
      decision_steps: [14]
      direction: increase
      magnitude_basis: aged-stock days on hand reduced
```

This block answers **three audit questions** the engagement's commercial envelope depends on:

1. *"Who's accountable for moving the GM number?"* → `daniel-chen-merch-director`
2. *"Where in the chain does that happen?"* → step 14 (HITL approval)
3. *"How will we measure their effect?"* → magnitude_basis tells you what the Gold mart will compute

## 5. The `smoke_test` block

Names the fixture file the laptop substrate uses to drive the chain end-to-end, plus the assertions to run after. The wizard's `docker-compose up` flow can shell into this fixture for evidence the chain wires correctly.

### Schema

```yaml
smoke_test:
  fixture_path: <relative path from repo root>     # JSON or YAML
  trigger_event:
    type: <string>                                  # e.g., "cold-chain-excursion"
    inject_into: <step-id>                          # where to inject (typically step 1 or 8)
  expected_outcome:
    chain_completed: <bool>                         # all 24 steps fire
    hitl_triggered: <bool>                          # decide step ran the gate
    hitl_persona: <persona-id>                      # which persona was paged
    audit_row_written: <bool>                       # mock-purview received the row
    kpi_attribution:                                # KPI sanity checks
      <kpi-id>: <comparison-string>                  # e.g., ">= 1.0" or "in [-100, 0]"
  laptop_command: <bash command>                    # how to run the smoke test
```

### Worked example

```yaml
smoke_test:
  fixture_path: services/rc/RC-E2E-03/scenarios/rc-cold-chain-excursion-mid-shift/fixtures/excursion-event.json
  trigger_event:
    type: cold-chain-excursion
    inject_into: step:1                             # SOR · POS + Refrigeration Telemetry
  expected_outcome:
    chain_completed: true
    hitl_triggered: true
    hitl_persona: marisol-reyes-store-ops
    audit_row_written: true
    kpi_attribution:
      shrink-cost-reduction-pct: "<= 0"             # this scenario should reduce shrink
      decision-loop-time-sec: "< 120"               # HITL completes within 2 min
  laptop_command: |
    docker-compose up -d
    curl -X POST http://localhost:8810/inject \
      -H "Content-Type: application/json" \
      -d @services/rc/RC-E2E-03/scenarios/rc-cold-chain-excursion-mid-shift/fixtures/excursion-event.json
    # Watch the chain execute via the mocks; assert per expected_outcome
```

## 6. Adding a use case for a new client

Recipe per [`Pre-deployment-Security-Gate.md`](Pre-deployment-Security-Gate.md) item #12 (use case validates):

```bash
# 1. Clone the _default use case
cp -r services/rc/RC-E2E-03/use-cases/_default \
      services/rc/RC-E2E-03/use-cases/<client-slug>

# 2. Edit the new use case
#    - update use_case_id, client, client_segment, substrate
#    - populate client_approved_architecture per the client's CAB
#    - tune kpis_targeted to the engagement's commercial envelope
#    - tune hitl_thresholds per the client's Independence consultation
#    - update foundry.project_ref + image_tag for the client's Foundry project

# 3. The chain_execution block typically does NOT change client-by-client;
#    it captures scenario semantics, not tenant config. Override only when
#    a client adds custom roles or removes a step.

# 4. The persona_kpi_attribution block usually carries forward unchanged
#    unless the client substitutes alternative personas (e.g., a different
#    Store Operations Lead title).

# 5. The smoke_test block typically carries forward; add per-client fixtures
#    if the client wants tenant-specific synthetic data.

# 6. Run the wizard's validator
python tools/gen_services_tree.py     # validates persona/KPI refs

# 7. The new use case appears in the wizard at /api/catalog/use-cases?service=RC-E2E-03
```

## 7. The 5 featured RC scenarios — first-iteration coverage

For the first iteration (RC-only):

| Service | Scenario | Status |
|---|---|---|
| RC-E2E-03 | rc-cold-chain-excursion-mid-shift | **Worked example** — full chain_execution + smoke_test |
| RC-E2E-03 | rc-dynamic-markdown-optimization | Template stub — chain_execution TBD per engagement |
| RC-E2E-04 | rc-loyalty-churn-prediction-winback | Template stub |
| RC-E2E-05 | rc-on-shelf-availability-oos-reduction | Template stub |
| RC-E2E-07 | rc-returns-fraud-detection | Template stub |
| RC-E2E-09 | rc-perishable-waste-reduction | Template stub |

The four template stubs ship with `chain_execution` partially populated (step ranges + canonical role mappings) but with TODO markers on the per-step data flow + KPI attribution. Each engagement fills in the TODOs at use-case clone time using this template doc as the reference.

The two catalog-only RC services (RC-E2E-06, RC-E2E-08) gain runnable use cases only when an engagement promotes a scenario per the [RC-Build-Plan.md](RC-Build-Plan.md) Sprint 36 / Sprint 38 decision points.

## 8. How the wizard exercises the runnable use case

| Substrate | What runs | What the smoke_test asserts |
|---|---|---|
| **laptop** | `docker-compose up` brings agents + mocks online; operator POSTs the fixture; chain runs through mocks | All assertions in `expected_outcome` |
| **dev** | Bicep deploys agents to Lab Foundry; operator POSTs fixture to real Eventstream; chain runs end-to-end | Same assertions, against real services |
| **stage** | Same as dev, plus private networking; smoke test runs through pipelines as part of CI gate | Same assertions; KPI Gold marts populated |
| **prod** | Live client data; smoke_test fixture not used; engagement has its own fixtures + runbook | (n/a — production HITL is real, not smoke-tested) |

The fixture file itself is **substrate-agnostic** — same JSON drives the chain on every substrate. Only the routing changes.

## 9. Validation rules (wizard enforces)

The wizard's render endpoint validates a runnable use case has:

- ✅ Every `chain_execution.steps[*].step` is in `[1..24]` and unique
- ✅ Every `executed_by` is `"platform"` OR a role declared in `services/_extras.yaml` for the service code OR a default APEX-canonical role
- ✅ Every `data_read` and `data_written` references a known APEX-Core schema family (SCML, MERML, PROML, CRMML, etc.)
- ✅ Every `kpi_affected` resolves in `services/_kpis.yaml`
- ✅ Every `personas_involved[*]` resolves in `services/_personas.yaml`
- ✅ Every `decision_point: true` step has a `hitl_threshold_ref` AND at least one persona
- ✅ Every persona in `persona_kpi_attribution` is in `personas_active`
- ✅ Every KPI in `persona_kpi_attribution` is in `kpis_targeted`
- ✅ The `smoke_test.fixture_path` exists in the repo
- ✅ The `smoke_test.expected_outcome.hitl_persona` is in `personas_active`

Validation runs on `python tools/gen_services_tree.py` and on every `POST /api/deployments/render` call. Failure blocks render.

## 10. Cross-references

- [Use case schema (full)](../../services/_use-case.schema.md)
- [`services/rc/RC-E2E-03/use-cases/_default/use-case.yaml`](../../services/rc/RC-E2E-03/use-cases/_default/use-case.yaml) — fully worked example
- [`services/_personas.yaml`](../../services/_personas.yaml) — persona registry
- [`services/_kpis.yaml`](../../services/_kpis.yaml) — KPI registry
- [Deploy UX and Substrates](Deploy-UX-and-Substrates.md) — how the runnable use case lands per substrate
- [Pre-deployment Security Gate item #12](Pre-deployment-Security-Gate.md#per-deployment-gates-per-wave) — the use-case validator gate
