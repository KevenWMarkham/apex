# Use Case YAML Schema

A use case is the per-tenant variance layer that binds a Service to a specific client deployment. Same Service + same Agents → different personas, different KPI envelope, different cloud variant, different adapter composition.

**File location:** `services/{industry}/{SERVICE-CODE}/use-cases/{slug}/use-case.yaml`
**Companion:** `services/{industry}/{SERVICE-CODE}/use-cases/{slug}/DESIGN.md` — narrative explaining how this use case extends the default
**Default per service:** `use-cases/_default/use-case.yaml` — canonical envelope from the Services Guide; clones for client-specific variants

## Top-level fields

| Field | Type | Required | Description |
|---|---|---|---|
| `use_case_id` | string | yes | Globally unique slug, e.g., `contoso-rc-e2e-03-na-pilot` |
| `service_code` | string | yes | Must match the parent directory's service code (e.g., `RC-E2E-03`) |
| `primary_variant` | enum | yes | `APEX-M` · `APEX-G` · `APEX-A` |
| `client` | string | optional | Client slug; omit for `_default` |
| `client_segment` | string | optional | Brief descriptor (e.g., "Big-Box Grocery · 250 stores · NA pilot") |
| `substrate` | enum | yes | `lab` · `dev` · `stage` · `prod` |
| `client_approved_architecture` | object | yes | See §Adapter binding below |
| `personas_active` | list | yes | List of persona ids from `services/_personas.yaml` |
| `kpis_targeted` | list | yes | List of `{id, target}` entries; ids resolve in `services/_kpis.yaml` |
| `hitl_thresholds` | object | optional | Per-decision thresholds (markdown_pct_above, refund_usd_above, etc.) |
| `agent_overrides` | object | optional | Per-role overrides (model, prompts, redis cache config) |
| `foundry` | object | optional (APEX-M only) | Foundry-specific block: project ref, hosted agent image tag |
| `deployment` | object | optional | wave + blueprint + parameters file path |

## Adapter binding — `client_approved_architecture`

Per-protocol slot assignments. Each slot has a `primary` (the variant's native service) and optional `secondary` / `federation` / `fallback` (adapters that satisfy the same protocol). The wizard validates every adapter reference resolves against `packages/apex-adapters/src/apex_adapters/protocol_adapters/`.

### Schema

```yaml
client_approved_architecture:
  data_lake:
    primary:
      variant: APEX-M
      target: fabric.onelake.<workspace>
    bronze_sources:
      - source: <name>
        adapter: <category.provider>     # e.g., cloud.aws.rds
        dataset: <provider-specific id>
        # Adapter MUST satisfy DataLake per its protocols.py
  identity:
    primary:
      variant: APEX-M
      source: entra-agent-id
    federation:
      - identity.okta
      # Adapters MUST satisfy AgentIdentityProvider
  siem_audit:
    primary:
      variant: APEX-M
      target: purview-audit
    secondary:
      - siem.splunk
      # Adapters MUST satisfy AuditLedger (with is_primary=False) + Observability
  crm:
    adapter: saas.salesforce
    org: <provider-specific id>
  hitl_channel:
    primary:
      variant: APEX-M
      target: teams
    fallback:
      - collaboration.slack
  message_bus:
    primary:
      variant: APEX-M
      target: eventstream
    cross_cloud:
      - cloud.gcp.pubsub
```

### Validation rules

The generator (`tools/gen_services_tree.py`) and the wizard's render endpoint validate:

1. Every `adapter:` reference resolves to a directory under `packages/apex-adapters/src/apex_adapters/protocol_adapters/{adapter}/`
2. Each adapter's `SATISFIES` list must include the protocol the slot expects (e.g., `data_lake.bronze_sources[*].adapter` adapters must satisfy `DataLake`)
3. `primary.variant` must be one of `APEX-M` / `APEX-G` / `APEX-A`
4. Variant-specific slots (`foundry` block) are only valid for APEX-M; raise on use with `APEX-G` or `APEX-A`
5. `personas_active` ids resolve in `services/_personas.yaml`
6. `kpis_targeted[*].id` resolves in `services/_kpis.yaml`

## Worked example — `contoso-rc-e2e-03-na-pilot`

```yaml
use_case_id: contoso-rc-e2e-03-na-pilot
service_code: RC-E2E-03
primary_variant: APEX-M
client: contoso
client_segment: Big-Box Grocery · 250 stores · NA pilot
substrate: lab

client_approved_architecture:
  data_lake:
    primary: { variant: APEX-M, target: fabric.onelake.rc-canonical }
    bronze_sources:
      - { source: pos, adapter: cloud.aws.rds, dataset: contoso-pos-prod }
      - { source: erp, adapter: cloud.azure.adls_gen2, dataset: sap-s4-mirror }
      - { source: refrigeration, adapter: cloud.azure.iot_hub, hub: contoso-iot }
      - { source: competitor_pricing, adapter: saas.numerator, account: contoso-num }
  identity:
    primary: { variant: APEX-M, source: entra-agent-id }
    federation: [ identity.okta ]
  siem_audit:
    primary: { variant: APEX-M, target: purview-audit }
    secondary: [ siem.splunk ]
  crm:
    adapter: saas.salesforce
    org: contoso-prod
  hitl_channel:
    primary: { variant: APEX-M, target: teams }
    fallback: [ collaboration.slack ]

personas_active:
  - id: marisol-reyes-store-ops
  - id: daniel-chen-merch-director

kpis_targeted:
  - { id: gm-pp-lift, target: 3.2 }
  - { id: doh-reduction-pct, target: -28 }
  - { id: markdown-to-clear-pct, target: 41 }

hitl_thresholds:
  markdown_pct_above: 30
  destroy_decision: any
  refund_usd_above: 500

agent_overrides:
  pricing:
    model: gpt-4o-2024-11-20
    redis_episodic_memory: true
    learning_loop_window_days: 90

foundry:
  project_ref: foundry-rc-e2e-03-contoso
  hosted_agent_image_tag: rc-e2e-03/v1.2.0
  workflow_def: workflows/excursion-triage.yaml

deployment:
  wave: w2
  blueprint: apex-m/infra/bicep/blueprints/w2-pilot.bicep
  parameters_path: apps/deploy-wizard/parameters/contoso-rc-e2e-03-w2.json
```

## How a client adds a use case

1. Copy `services/{ind}/{code}/use-cases/_default/` to `services/{ind}/{code}/use-cases/{client-slug}/`
2. Fill in `client`, `client_segment`, `client_approved_architecture` per the client's CAB approval
3. Adjust `personas_active`, `kpis_targeted`, `hitl_thresholds` per the engagement
4. Re-run `python tools/gen_services_tree.py` — generator validates all refs
5. Wizard's `/api/catalog/use-cases?service={code}` surfaces the new use case

## Runnable use case blocks

A "runnable" use case adds three blocks beyond the configuration above: `chain_execution`, `persona_kpi_attribution`, and `smoke_test`. Together they make the use case **executable end-to-end** on the laptop substrate and traceable for audit on cloud substrates.

Full template + worked example: [Use-Case-Template-Runnable-Chain.md](../docs/APEX%20-%20Design%20and%20Build/Use-Case-Template-Runnable-Chain.md).

### `chain_execution`

Maps each of the 24 chain steps from `scenario.yaml` to an agent role + data flow + KPI affected + HITL behavior. Schema:

```yaml
chain_execution:
  scenario_id: <must match scenario.yaml>
  steps:
    - step: <int 1..24>
      key: <chain key, e.g., w2-decide>
      executed_by: <agent role | "platform">
      data_read: [<schema>.<entity>, ...]
      data_written: [<schema>.<entity>, ...]
      kpi_affected: <kpi-id | null>
      decision_point: <bool>
      hitl_threshold_ref: <key into hitl_thresholds>
      personas_involved: [<persona-id>, ...]
      mock_endpoint: <url-template>     # laptop substrate fixture binding
      notes: <free text>
```

### `persona_kpi_attribution`

Documents the cause-and-effect link between persona decisions and KPI movement. The audit-trail spec for KPI attribution. Schema:

```yaml
persona_kpi_attribution:
  <persona-id>:
    - kpi: <kpi-id>
      mechanism: <string>
      decision_steps: [<step-id>]
      direction: <"increase" | "decrease" | "either">
      magnitude_basis: <string>
```

### `smoke_test`

Names the fixture the laptop substrate uses to drive the chain end-to-end + assertions to run after. Schema:

```yaml
smoke_test:
  fixture_path: <relative path from repo root>
  trigger_event:
    type: <event kind>
    inject_into: step:<int>
  expected_outcome:
    chain_completed: <bool>
    hitl_triggered: <bool>
    hitl_persona: <persona-id>
    audit_row_written: <bool>
    kpi_attribution:
      <kpi-id>: <comparison string>     # e.g., "<= 0", ">= 1.0", "< 120"
  laptop_command: |
    # operator-runnable bash; wizard exposes this via the Deploy page
```

## Validation rules

The wizard's render endpoint and the generator's `tools/gen_services_tree.py` validate every use case has:

- ✅ Every `chain_execution.steps[*].step` is in `[1..24]` and unique
- ✅ Every `executed_by` is `"platform"` OR a known agent role
- ✅ Every `data_read` and `data_written` references a known APEX-Core schema family
- ✅ Every `kpi_affected` resolves in `services/_kpis.yaml`
- ✅ Every `personas_involved[*]` resolves in `services/_personas.yaml`
- ✅ Every `decision_point: true` step has `hitl_threshold_ref` AND ≥1 persona
- ✅ Every persona in `persona_kpi_attribution` is in `personas_active`
- ✅ Every KPI in `persona_kpi_attribution` is in `kpis_targeted`
- ✅ The `smoke_test.fixture_path` exists in the repo
- ✅ The `smoke_test.expected_outcome.hitl_persona` is in `personas_active`

## See also

- [Use Case Template — Runnable Chain](../docs/APEX%20-%20Design%20and%20Build/Use-Case-Template-Runnable-Chain.md) — the template + worked example
- [APEX-Core Adapter Catalog](../docs/apex-core/Adapter-Catalog.md) — full inventory of available adapters
- [APEX-Core Independence Posture](../docs/apex-core/Independence-Posture.md) — variant equality, language standards
- [APEX-Core Protocols Reference](../docs/apex-core/Protocols-Reference.md) — what each adapter slot expects
- [services/_personas.yaml](_personas.yaml) — persona registry
- [services/_kpis.yaml](_kpis.yaml) — KPI registry
