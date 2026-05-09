# APEX-A — AWS variant

The Amazon Web Services implementation of APEX. Implements every
APEX-Core protocol against AWS services: Bedrock, Lake Formation, S3,
EventBridge, Macie, IAM, GuardDuty, Workspaces.

**Status: Stub package.** Concrete implementations are scaffolded with
`NotImplementedError` and an Independence-compliant port plan. APEX-A
ships when a Deloitte client commissions an AWS variant deployment.

APEX-A is a **sibling product** to APEX-M and APEX-G — same APEX-Core
protocol contract, different cloud. See [Variant Comparison](../docs/apex-core/Variant-Comparison.md).

## Planned coverage

| APEX-Core protocol | Planned AWS service |
|---|---|
| AgentRuntime | AWS Bedrock Agents + AgentCore |
| AgentIdentityProvider | AWS IAM Identity Center + STS AssumeRole + IAM Roles Anywhere |
| SecretStore | AWS Secrets Manager + KMS |
| AuditLedger | AWS CloudTrail + DynamoDB overlay |
| DataLake | AWS Lake Formation + S3 + Glue (Bronze/Silver/Gold) |
| EmbeddingService | Bedrock Titan Embeddings + OpenSearch Vector |
| MessageBus | EventBridge + SNS/SQS |
| SensitivityClassifier | AWS Macie + Comprehend custom classifications |
| Observability | CloudWatch + X-Ray + Application Signals |
| ThreatProtection | Bedrock Guardrails + GuardDuty + Security Hub |

## Port plan

See [Multi-Cloud Port Plan](../docs/apex-core/Multi-Cloud-Port-Plan.md)
for the canonical sequence to ship APEX-A:

1. Concrete impls of the 10 protocols (`src/apex_a/`)
2. CloudFormation modules for AWS infrastructure (`infra/cloudformation/`)
3. APEX-A books (`docs/book/Professional-APEX-A-*.html`) — same shape
   as APEX-M's 6-book set
4. Wizard render adapter for `Microsoft.Resources/deployments` →
   `aws_cloudformation_stack` equivalent

## Independence

APEX-A integrates with the client's existing AWS investment. Deloitte
does **not** resell, sublicense, or have an alliance posture with AWS.
APEX-A exists as a sibling product so APEX is **not Microsoft-dependent**;
it is **multi-cloud-portable** by construction.

See [LICENSE-ATTRIBUTION.md](LICENSE-ATTRIBUTION.md).
