# APEX-Core Protocols Reference

The 10 provider-neutral protocols every APEX variant (APEX-M / APEX-G / APEX-A) and every adapter must satisfy. Defined in [`packages/apex-core/src/apex_core/protocols/`](../../packages/apex-core/src/apex_core/protocols/).

## Index

| # | Protocol | Module | What it represents |
|---|---|---|---|
| 1 | `AgentRuntime` | `agent_runtime.py` | Where agents execute |
| 2 | `AgentIdentityProvider` | `agent_identity.py` | Agent identity, blueprints, OBO, CA |
| 3 | `SecretStore` | `secret_store.py` | Secrets, keys, certs with rotation |
| 4 | `AuditLedger` | `audit_ledger.py` | Append-only decision history |
| 5 | `DataLake` | `data_lake.py` | Bronze/Silver/Gold storage |
| 6 | `EmbeddingService` | `embedding_service.py` | Vectors + similarity search |
| 7 | `MessageBus` | `message_bus.py` | Pub/sub + activator triggers |
| 8 | `SensitivityClassifier` | `sensitivity_classifier.py` | T1–T4 ↔ provider labels |
| 9 | `Observability` | `observability.py` | Traces, metrics, alerts |
| 10 | `ThreatProtection` | `threat_protection.py` | Prompt-shield, jailbreak, DLP for AI |

## Variant mapping

| Protocol | APEX-M | APEX-G (planned) | APEX-A (planned) |
|---|---|---|---|
| AgentRuntime | Foundry Agent Service (Hosted Agents) | Vertex AI Agent Builder + Agent Engine | Bedrock Agents + AgentCore |
| AgentIdentityProvider | Microsoft Entra Agent ID (GA Apr 2026) | Cloud IAM + service-account impersonation | IAM Identity Center + STS AssumeRole |
| SecretStore | Azure Key Vault Premium HSM | Google Secret Manager | AWS Secrets Manager + KMS |
| AuditLedger | Microsoft Purview Audit (primary) + Fabric SQL ledger overlay | Cloud Audit Logs + BigQuery overlay | CloudTrail + DynamoDB overlay |
| DataLake | Microsoft Fabric (OneLake / Lakehouse / Eventhouse / Mirroring / Direct Lake) | BigQuery + Cloud Storage + Dataform | Lake Formation + S3 + Glue |
| EmbeddingService | Eventhouse SLM `ai_embeddings` plugin + Azure OpenAI | Vertex AI text-embedding-005 + Vector Search | Bedrock Titan Embeddings + OpenSearch Vector |
| MessageBus | Fabric Eventstream + Activator + Service Bus + Event Grid | Pub/Sub + Eventarc | EventBridge + SNS/SQS |
| SensitivityClassifier | Microsoft Purview Information Protection | Sensitive Data Protection (Cloud DLP) | Macie + Comprehend |
| Observability | Azure Monitor + App Insights + Log Analytics | Cloud Logging + Cloud Monitoring + Cloud Trace | CloudWatch + X-Ray + Application Signals |
| ThreatProtection | Defender for Cloud (CSPM, AI security posture) + Defender for AI services + Azure AI Content Safety | Vertex AI safety filters + Chronicle SecOps | Bedrock Guardrails + GuardDuty + Security Hub |

## Adapter mapping

Adapters under `packages/apex-adapters/` may satisfy one or more protocols, integrating non-primary services without changing the variant:

| Adapter (sample) | Satisfies | Used for |
|---|---|---|
| `cloud.aws.s3` | DataLake | Bronze ingestion from AWS S3 to APEX-M Fabric |
| `cloud.aws.rds` | DataLake | Mirroring source for client RDS POS data |
| `cloud.gcp.bigquery` | DataLake | Silver source from BigQuery for analytics-on-GCP clients |
| `cloud.gcp.pubsub` | MessageBus | Cross-cloud event routing |
| `saas.salesforce` | DataLake (CRM entities) | Salesforce CRM as silver source |
| `saas.snowflake` | DataLake (Gold consumer) | Snowflake-on-AWS Gold consumer for analytics |
| `siem.splunk` | AuditLedger (parallel-write) + Observability | Client-mandated Splunk SIEM |
| `identity.okta` | AgentIdentityProvider (federation slot) | Federated identity via Okta IdP |

## Using a protocol

Every protocol is a `runtime_checkable` `typing.Protocol`. Concrete impls satisfy by duck typing:

```python
from apex_core.protocols import AgentRuntime, AgentInvocation

def deploy_agent_fleet(runtime: AgentRuntime, scenarios: list[str]) -> None:
    """This function works against APEX-M, APEX-G, APEX-A, or a hybrid
    composition — the protocol is the only contract."""
    for sid in scenarios:
        runtime.deploy_agent(blueprint_id=f"apex-rc-{sid}", agent_definition={...})

# Wire APEX-M:
from apex_m.runtime_foundry import AgentRuntimeFoundry  # concrete impl
deploy_agent_fleet(AgentRuntimeFoundry(...), scenarios=[...])

# Same code wires APEX-G when shipped:
from apex_g.runtime_vertex import AgentRuntimeVertex
deploy_agent_fleet(AgentRuntimeVertex(...), scenarios=[...])
```

## Versioning

Protocol surface is **stable** within a major version. Field additions are minor. Breaking changes require a major bump and a documented migration. Per BL.P.185 (scenario versioning discipline) extended to protocols.

## Implementation status

| Variant | Status |
|---|---|
| APEX-M | Concrete impls in progress; Phase I delivers them per [Microsoft platform alignment delta](../plans/2026-05-09-microsoft-platform-alignment-delta.md) |
| APEX-G | Stub — `NotImplementedError` with port-plan reference |
| APEX-A | Stub — `NotImplementedError` with port-plan reference |
