# APEX Adapter Catalog

Adapters under `packages/apex-adapters/` integrate non-primary services into APEX-Core protocols. Use cases compose them per the client's approved cloud architecture.

## How adapters work

A use case declares which adapters fill which protocol slot:

```yaml
client_approved_architecture:
  data_lake:
    primary: { variant: APEX-M, target: fabric.onelake.rc-canonical }
    bronze_sources:
      - { source: pos, adapter: cloud.aws.rds, dataset: contoso-pos-prod }
      - { source: erp, adapter: cloud.azure.adls_gen2, dataset: sap-s4-mirror }
  identity:
    primary: { variant: APEX-M, source: entra-agent-id }
    federation: [ saas.okta ]
  siem_audit:
    primary: { variant: APEX-M, target: purview-audit }
    secondary: [ siem.splunk ]
```

The wizard validates each adapter reference resolves; render emits IaC for the chosen adapters alongside the primary variant's deployment.

## Catalog (priority adapters — Phase 0 stubs)

The 8 adapters below ship as protocol stubs in Phase 0. Concrete implementations build per-engagement when a client's CAB has approved the integration. Each adapter has a `sec_independence.md` recording Deloitte's Independence posture for that provider.

### Cloud · cross-cloud data + messaging

| Adapter | Satisfies | Use case | Status |
|---|---|---|---|
| `cloud.aws.s3` | DataLake (Bronze) | Bronze ingestion from client S3 buckets | Stub |
| `cloud.aws.rds` | DataLake (Mirroring source) | Mirror RDS POS / ERP into APEX-M Fabric | Stub |
| `cloud.gcp.bigquery` | DataLake (Silver/Gold) | Read BigQuery datasets as Silver source | Stub |
| `cloud.gcp.pubsub` | MessageBus | Cross-cloud event routing GCP → APEX-M Eventstream | Stub |

### SaaS · enterprise systems

| Adapter | Satisfies | Use case | Status |
|---|---|---|---|
| `saas.salesforce` | DataLake (CRM entities) | CRM as Silver source for RC-E2E-04 (Loyalty), HLS-* (Patient relationships) | Stub |
| `saas.snowflake` | DataLake (Gold consumer) | Snowflake-on-AWS Gold consumer for analytics-on-Snowflake clients | Stub |

### SIEM · parallel-write security

| Adapter | Satisfies | Use case | Status |
|---|---|---|---|
| `siem.splunk` | AuditLedger (secondary) + Observability | Client-mandated parallel-write to Splunk SIEM | Stub |

### Identity · federated IdP

| Adapter | Satisfies | Use case | Status |
|---|---|---|---|
| `identity.okta` | AgentIdentityProvider (federation slot) | Federated identity via Okta IdP for non-Entra workforces | Stub |

## Catalog (planned — beyond Phase 0)

Built per-engagement as client architectures demand them:

- **cloud**: `cloud.aws.eventbridge`, `cloud.aws.kms`, `cloud.aws.secrets_manager`, `cloud.gcp.gcs`, `cloud.gcp.kms`, `cloud.gcp.secret_manager`, `cloud.azure.adls_gen2`, `cloud.azure.event_grid`, `cloud.azure.storage`
- **saas**: `saas.databricks`, `saas.servicenow`, `saas.sap`, `saas.workday`, `saas.numerator`, `saas.adobe_experience_platform`
- **siem**: `siem.sumo_logic`, `siem.datadog`, `siem.qradar`, `siem.elastic`
- **identity**: `identity.auth0`, `identity.ping_identity`
- **collaboration**: `collaboration.slack`, `collaboration.zoom`, `collaboration.google_workspace`

## Adding a new adapter

1. Create directory: `packages/apex-adapters/src/apex_adapters/{category}/{provider}/`
2. Write `__init__.py` exporting the adapter class
3. Write `protocols.py` declaring which APEX-Core protocols this adapter satisfies
4. Write `client.py` wrapping the provider SDK
5. Write `iac/` with provider-native IaC snippets for adapter-side resources
6. Write `README.md` with capability summary
7. Write `sec_independence.md` with the Deloitte Independence statement for the provider
8. Smoke test: import the adapter; verify it satisfies the declared protocols
9. Add to `client_approved_architecture` schema validator's known-adapter list
10. Update this catalog

## Independence per adapter

Every adapter's `sec_independence.md` reads:

> *"This adapter integrates with the client's existing investment in **[Provider X]**. Deloitte does not resell, sublicense, or have an alliance posture with **[Provider X]**; the adapter exists to honor the client's approved cloud architecture per their Cloud Architecture Board (CAB)."*

The `apex-compliance-lint` package validates this statement appears verbatim in every `sec_independence.md` in the catalog.

## References

- [Independence Posture](Independence-Posture.md)
- [Protocols Reference](Protocols-Reference.md)
- [Variant Comparison](Variant-Comparison.md)
- Use-case schema: `services/_use-case.schema.md` (added in Phase 0.9)
