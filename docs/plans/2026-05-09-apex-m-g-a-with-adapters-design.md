# APEX-M / APEX-G / APEX-A + Client-Approved Adapter Variance — Design

**Date:** 2026-05-09
**Status:** Approved
**Authors:** Keven Markham · DMTSP, with Claude

## 1. The model

Three sibling products on a shared APEX-Core, plus a composed adapter pattern that handles per-client architecture variance.

```
                    ┌─────────────────────────────────┐
                    │       APEX-Core (provider-       │
                    │       neutral protocols + framework)
                    └─────────┬───────────────────────┘
                              │ implements
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ┌──────────┐         ┌──────────┐          ┌──────────┐
   │  APEX-M  │         │  APEX-G  │          │  APEX-A  │
   │ Microsoft│         │   GCP    │          │   AWS    │
   │ (FIRST)  │         │ (stub)   │          │ (stub)   │
   └─────┬────┘         └──────────┘          └──────────┘
         │
         │ composes
         ▼
   ┌─────────────────────────────────────────────────────┐
   │  apex-adapters (per client-approved architecture)   │
   │   cloud/aws · cloud/gcp · cloud/azure               │
   │   saas/{salesforce, snowflake, databricks, ...}     │
   │   siem/{splunk, sumo_logic, datadog, ...}           │
   │   identity/{okta, auth0, ping_identity}             │
   │   collaboration/{slack, zoom, google_workspace}     │
   └─────────────────────────────────────────────────────┘
                              │
                              │ bound by
                              ▼
   ┌─────────────────────────────────────────────────────┐
   │  use-case.yaml.client_approved_architecture         │
   │  (per-tenant: which adapters fill which protocol)   │
   └─────────────────────────────────────────────────────┘
```

## 2. Why this shape

- **SEC Independence**: APEX-M / G / A are sibling products on equal footing. Microsoft is **first shipped**, not preferred.
- **Audit defensibility**: real packages, real protocol contracts, real Independence statements per package. AWS and GCP variants exist as products even before they're built out.
- **Client-approved architecture variance**: clients have mixed cloud + SaaS investments. APEX-M deployed for a client running AWS RDS for POS + Splunk for SIEM + Okta for federation is a perfectly valid deployment via composed adapters — Deloitte isn't reselling AWS / Splunk / Okta, just integrating with the client's existing investments.
- **Books stay APEX-M**: the existing 6 books describe APEX-M and get renamed with `-M-` infix. APEX-G and APEX-A get their own book sets when those variants ship.

## 3. Repository structure

```
APEX/
  apex-core/                               # provider-neutral framework
    src/apex_core/
      protocols/                           # NEW — 10 protocols
        agent_runtime.py
        agent_identity.py
        secret_store.py
        audit_ledger.py
        data_lake.py
        embedding_service.py
        message_bus.py
        sensitivity_classifier.py
        observability.py
        threat_protection.py
    conventions/  data/  tools/            # existing
  apex-m/                                  # NEW — Microsoft
    src/apex_m/                            # protocol impls (Foundry, Entra, Fabric, Purview, Defender)
    infra/bicep/                           # MOVED from infra/bicep/ at root
    LICENSE-ATTRIBUTION.md
    pyproject.toml
    README.md
  apex-g/                                  # NEW — GCP stub
    src/apex_g/                            # NotImplementedError + Independence note
    infra/terraform-gcp/                   # placeholder
    LICENSE-ATTRIBUTION.md
    pyproject.toml
    README.md
  apex-a/                                  # NEW — AWS stub
    src/apex_a/
    infra/cloudformation/
    LICENSE-ATTRIBUTION.md
    pyproject.toml
    README.md
  apex-rc/  apex-fleet/  apex-workspace/   # existing — provider-neutral, stay
  packages/
    apex-adapters/                         # existing — extended:
      src/apex_adapters/
        cloud/aws/{s3,rds,eventbridge,kms,secrets_manager}/
        cloud/gcp/{bigquery,pubsub,gcs,kms,secret_manager}/
        cloud/azure/{adls_gen2,event_grid,storage}/
        saas/{salesforce,snowflake,databricks,servicenow,sap,workday}/
        siem/{splunk,sumo_logic,datadog,qradar}/
        identity/{okta,auth0,ping_identity}/
        collaboration/{slack,zoom,google_workspace}/
    ... existing packages stay ...
  services/                                # provider-neutral catalog (unchanged shape)
  apps/deploy-wizard/                      # provider-neutral wizard (extended)
  docs/
    book/
      Professional-APEX-M.html             # RENAMED
      Professional-APEX-M-Deployment-Guide.html
      Professional-APEX-M-Services-Guide.html
      Professional-APEX-M-Sellers-Guide.html
      Professional-APEX-M-Library.html
      Professional-APEX-M-Executive-Summary.html
    apex-core/                             # NEW — provider-neutral docs
      Protocols-Reference.md
      Independence-Posture.md
      Variant-Comparison.md
      Multi-Cloud-Port-Plan.md
      Adapter-Catalog.md
    APEX - Design and Build/               # existing
    plans/                                 # existing
```

## 4. The 10 APEX-Core protocols

Each is a Python `Protocol` (typing.Protocol) so duck-typed adapters and concrete impls both satisfy:

1. **`AgentRuntime`** — deploy / invoke / query / drain agent
2. **`AgentIdentityProvider`** — blueprint, OBO, Conditional Access binding
3. **`SecretStore`** — get / put / version
4. **`AuditLedger`** — append / query / sign / verify
5. **`DataLake`** — bronze/silver/gold paths, security policy, OneLake-compatible API
6. **`EmbeddingService`** — embed / similarity-search (for The Pricer, etc.)
7. **`MessageBus`** — publish / subscribe / activator-style trigger
8. **`SensitivityClassifier`** — APEX T1–T4 ↔ provider sensitivity-label mapping
9. **`Observability`** — trace / metric / alert
10. **`ThreatProtection`** — posture, prompt-shield, jailbreak, data-leak detection

## 5. Use-case schema extension

```yaml
use_case_id: contoso-rc-e2e-03-na-pilot
service_code: RC-E2E-03
primary_variant: APEX-M
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
    federation: [ saas.okta ]
  siem_audit:
    primary: { variant: APEX-M, target: purview-audit }
    secondary: [ siem.splunk ]
  crm:
    adapter: saas.salesforce
    org: contoso-prod
  hitl_channel:
    primary: { variant: APEX-M, target: teams }
    fallback: [ collaboration.slack ]
```

## 6. Adapter contract

Every adapter package contains:

```
apex-adapters/src/apex_adapters/<category>/<provider>/
  __init__.py            # exports the adapter class
  protocols.py           # which APEX-Core protocols this adapter satisfies
  client.py              # provider SDK calls (boto3 / google-cloud-* / etc.)
  iac/                   # CloudFormation / Terraform / Bicep snippets
  README.md              # what it does, what protocols it satisfies
  sec_independence.md    # Deloitte Independence posture for this provider
```

Independence text per adapter:
> *"This adapter integrates with the client's existing investment in [Provider X]. Deloitte does not resell, license, or have an alliance posture with [Provider X]; the adapter exists to honor the client's approved cloud architecture per their Cloud Architecture Board."*

## 7. Phase 0 execution sequence

1. **0.1** APEX-Core protocols (10 files)
2. **0.2** apex-m / apex-g / apex-a top-level workspaces
3. **0.3** Move `infra/bicep/` → `apex-m/infra/bicep/`; update wizard render paths
4. **0.4** apex-g + apex-a stubs (`NotImplementedError` + Independence note + port plan)
5. **0.5** Per-package LICENSE-ATTRIBUTION
6. **0.6** Rename 6 books with `-M-` infix + update titles
7. **0.7** APEX-Core docs (Protocols Reference / Independence Posture / Variant Comparison / Multi-Cloud Port Plan / Adapter Catalog)
8. **0.8** Adapter contract definition + base classes
9. **0.9** Use-case schema extension; generator updated
10. **0.10** 8 priority adapter stubs (`cloud.aws.s3`, `cloud.aws.rds`, `cloud.gcp.bigquery`, `cloud.gcp.pubsub`, `saas.salesforce`, `saas.snowflake`, `siem.splunk`, `identity.okta`)
11. **0.11** Wizard adapter-selection step
12. **0.12** APEX-M book chapter on composing client-approved adapters

## 8. Acceptance criteria

- [ ] `apex-core/`, `apex-m/`, `apex-g/`, `apex-a/` exist as top-level workspaces with `pyproject.toml`
- [ ] All 10 APEX-Core protocols defined with type hints
- [ ] APEX-G and APEX-A raise `NotImplementedError` with Independence note
- [ ] `infra/bicep/` lives at `apex-m/infra/bicep/`; wizard render emits paths that match
- [ ] 6 books renamed with `-M-` infix; old filenames symlinked or redirected; HTML titles updated
- [ ] 5 APEX-Core docs exist
- [ ] 8 adapter stubs scaffolded with protocol declarations + Independence notes
- [ ] Use-case YAML accepts `client_approved_architecture` block; validator checks adapter refs resolve
- [ ] Wizard surfaces adapter selection; render endpoint emits IaC for the chosen adapters
- [ ] APEX-M Deployment Guide gains the new chapter
- [ ] Wizard `/health`, `/api/catalog/tree`, `/api/deployments/render` still 200 with valid shapes
- [ ] All on `main`

## 9. References

- Phase I delta: [`2026-05-09-microsoft-platform-alignment-delta.md`](2026-05-09-microsoft-platform-alignment-delta.md)
- Foundry runtime design: [`2026-05-09-rc-design-docs-foundry-design.md`](2026-05-09-rc-design-docs-foundry-design.md)
- Implementation plan: [`2026-05-09-rc-design-docs-foundry-implementation.md`](2026-05-09-rc-design-docs-foundry-implementation.md) — Phase I and J implement against APEX-M after Phase 0 completes
