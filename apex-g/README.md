# APEX-G — Google Cloud variant

The Google Cloud Platform implementation of APEX. Implements every
APEX-Core protocol against GCP services: Vertex AI, BigQuery,
Cloud Storage, Pub/Sub, Cloud DLP, Chronicle, Cloud IAM, Workspace.

**Status: Stub package.** Concrete implementations are scaffolded with
`NotImplementedError` and an Independence-compliant port plan. APEX-G
ships when a Deloitte client commissions a Google Cloud variant
deployment.

APEX-G is a **sibling product** to APEX-M and APEX-A — same APEX-Core
protocol contract, different cloud. See [Variant Comparison](../docs/apex-core/Variant-Comparison.md).

## Planned coverage

| APEX-Core protocol | Planned GCP service |
|---|---|
| AgentRuntime | Vertex AI Agent Builder + Agent Engine |
| AgentIdentityProvider | Cloud IAM + service account impersonation |
| SecretStore | Google Secret Manager |
| AuditLedger | Cloud Audit Logs + BigQuery overlay |
| DataLake | BigQuery + Cloud Storage + Dataform (Bronze/Silver/Gold) |
| EmbeddingService | Vertex AI text-embedding-005 + Vector Search |
| MessageBus | Pub/Sub + Eventarc |
| SensitivityClassifier | Sensitive Data Protection (Cloud DLP) |
| Observability | Cloud Logging + Cloud Monitoring + Cloud Trace |
| ThreatProtection | Vertex AI safety filters + Chronicle SecOps |

## Port plan

See [Multi-Cloud Port Plan](../docs/apex-core/Multi-Cloud-Port-Plan.md)
for the canonical sequence of work to ship APEX-G:

1. Concrete impls of the 10 protocols (`src/apex_g/`)
2. Terraform modules for GCP infrastructure (`infra/terraform-gcp/`)
3. APEX-G books (`docs/book/Professional-APEX-G-*.html`) — same shape
   as APEX-M's 6-book set
4. Wizard render adapter for `Microsoft.Resources/deployments` →
   `google_cloud_platform_deployment_manager` equivalent

## Independence

APEX-G integrates with the client's existing Google Cloud investment.
Deloitte does **not** resell, sublicense, or have an alliance posture
with Google. APEX-G exists as a sibling product so APEX is **not
Microsoft-dependent**; it is **multi-cloud-portable** by construction.

See [LICENSE-ATTRIBUTION.md](LICENSE-ATTRIBUTION.md).
