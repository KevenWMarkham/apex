# apex-adapters

APEX SOR-adapter framework + 15 reference adapters. Sprint 15
(BL.P.95–P.109).

## Scope

| Subtask | Adapter | Track | Connection method |
|---|---|---|---|
| 15.1.1 | epic-clarity | HLS | ODBC |
| 15.1.2 | hl7-fhir | HLS | Eventstream |
| 15.2.1 | sap-s4hana | ERP | Mirrored DB (CDC) |
| 15.2.2 | oracle-ebs-fusion | ERP | Mirrored DB (CDC) |
| 15.3.1 | salesforce | CRM | Dataflow Gen2 |
| 15.3.2 | workday-hcm | HCM | Dataflow Gen2 |
| 15.3.3 | servicenow | ITSM | Dataflow Gen2 |
| 15.3.4 | salesforce-marketing-cloud | MarTech | Dataflow Gen2 |
| 15.4.1 | manhattan-wms | Supply | Data Pipeline |
| 15.4.2 | sap-ariba-coupa | Supply | Dataflow Gen2 |
| 15.5.1 | osi-pi | Historian | Eventstream |
| 15.5.2 | ge-proficy | Historian | Eventstream |
| 15.6.1 | as400-db2 | Legacy | ODBC |
| 15.6.2 | analytics-platforms | Analytics | Dataflow Gen2 |
| 15.6.3 | snowflake-databricks | Interop | Data Pipeline |

## Framework

Every adapter has the same shape:

1. **YAML manifest** — declares SOR, connection method, schema mapping,
   schedule, runbook (failure modes + escalation).
2. **Python implementation** — subclass of `Adapter` with `probe`,
   `discover`, `ingest`, and `smoke_test`.
3. **Terraform reference workspace** — provisions Bronze capacity + RG;
   uses Sprint 14 `fabric_capacity` module + `apex-fabric` Python
   wrapper for workspace creation.
4. **Runbook (markdown)** — operations document with failure modes,
   escalation, retry policy.

Two reference implementations ship in this package — `epic-clarity` and
`sap-s4hana` — illustrating ODBC and Mirrored-DB patterns. The remaining
13 ship as YAML manifests with documented integration patterns; Wave-1
engagements implement the Python class against the same framework.

## Quick Start

```bash
# Install:
pip install -e packages/apex-core packages/apex-adapters

# List shipped manifests:
apex adapters list

# Inspect one manifest:
apex adapters inspect epic-clarity

# Validate every shipped manifest parses cleanly (CI gate):
apex adapters validate-all

# Run a smoke test (requires registered adapter implementation):
apex adapters smoke-test epic-clarity --golden tests/fixtures/golden-epic.json
```

## Provisioning a Bronze workspace for an adapter

```bash
# Terraform:
cd infra/terraform/blueprints/adapter-workspace
terraform init
terraform apply -var practice=rc -var adapter_name=sap-s4hana \
  -var capacity_admins='["apex-rc-admins@deloitte.com"]' \
  -var cost_center=RC-ENG-001

# Then create the canonical-named Bronze workspace via apex-fabric:
python -c "
from apex_fabric import WorkspaceSpec, WorkspaceClient
spec = WorkspaceSpec(practice='rc', environment='prod', role='bronze', capacity_id='<from-tf-output>')
client = WorkspaceClient(token_provider=...)
client.ensure_workspace(spec)
"
```

## Cross-reference

- Sellers Guide §5.2 — medallion Bronze landing patterns
- Sellers Guide §6.13 — file-first context architecture
- Sellers Guide §9.11.3 / §10.10.3 / §11.10.3 / §12.10.3 / §13.13.3 / §14.9.3 / §15.9.3 — Practice-specific SOR tables
- APEX Orchestrator Sprint 4 (Bronze landing templates) — connection-method primitives
- APEX Orchestrator Sprint 14 — Fabric capacity + workspace provisioning
- APEX Orchestrator Sprint 15 — this work
