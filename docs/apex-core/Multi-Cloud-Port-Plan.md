# Multi-Cloud Port Plan — APEX-G and APEX-A

How sibling variants ship after APEX-M. Both follow the same template; differences are noted per variant.

## Trigger

A Deloitte client commissions a non-Microsoft variant deployment as their **primary substrate**. Examples:

- Client's CAB has approved Google Cloud as the primary cloud → port APEX-G
- Client is AWS-native with no M365 footprint → port APEX-A

(For *mixed* clients where Microsoft is primary but other clouds appear as secondary, the **adapter pattern** under [`packages/apex-adapters/`](../../packages/apex-adapters/) handles that without a full variant port. See [Independence Posture §Client-Approved Architecture Variance](Independence-Posture.md#client-approved-architecture-variance).)

## Port template (applies to both APEX-G and APEX-A)

The port is **bounded** because the protocol contract is fixed. Each port is a discrete project.

### Sprint G/A.1 — Concrete protocol implementations
Implement all 10 APEX-Core protocols against the variant's services. Estimated 4–6 sprints depending on team familiarity:

- `runtime_*.py` — agent runtime (Vertex Agent Builder / Bedrock Agents)
- `identity_*.py` — agent identity provider (Cloud IAM impersonation / IAM Identity Center)
- `secret_store_*.py` — Secret Manager / Secrets Manager
- `audit_*.py` — Cloud Audit Logs / CloudTrail (primary) + overlay
- `data_lake_*.py` — BigQuery / Lake Formation
- `embedding_*.py` — Vertex Vector Search / OpenSearch Vector
- `message_bus_*.py` — Pub/Sub / EventBridge
- `classifier_*.py` — Cloud DLP / Macie
- `observability_*.py` — Cloud Logging / CloudWatch
- `threat_*.py` — Vertex safety + Chronicle / Bedrock Guardrails + GuardDuty

### Sprint G/A.2 — IaC modules
Provider-native IaC for Layer 1 platform + Layer 2 service modules + 3-wave blueprints:

- **APEX-G**: Terraform — modules for Vertex AI hub/project, Cloud IAM, BigQuery datasets, Pub/Sub topics, Secret Manager
- **APEX-A**: CloudFormation — stacks for Bedrock agents, IAM Identity Center, Lake Formation, EventBridge, Secrets Manager

### Sprint G/A.3 — Variant book set
Six books with the same shape as APEX-M:

- `Professional-APEX-G.html` (or `-A.html`)
- `Professional-APEX-G-Deployment-Guide.html`
- `Professional-APEX-G-Services-Guide.html`
- `Professional-APEX-G-Sellers-Guide.html`
- `Professional-APEX-G-Library.html`
- `Professional-APEX-G-Executive-Summary.html`

Book content is largely a clone of the APEX-M book set with terminology + IaC + service-name swaps. Independence-language linter applies identically.

### Sprint G/A.4 — Wizard render adapter
Extend `apps/deploy-wizard/api/src/apex_wizard/deployments.py` render endpoint:

```python
RENDERERS = {
    "APEX-M": MicrosoftBicepRenderer,         # exists
    "APEX-G": GoogleCloudTerraformRenderer,   # adds in port
    "APEX-A": AwsCloudFormationRenderer,      # adds in port
}
```

Wizard's existing Cloud Variant selector flips the chosen variant from "Future · Independence Stub" to functional.

### Sprint G/A.5 — Pre-deployment Security Gate equivalent
APEX-M's Security Gate ([Pre-deployment Security Gate](../APEX%20-%20Design%20and%20Build/Pre-deployment-Security-Gate.md)) maps to:

- **APEX-G**: Security Command Center posture + Cloud DLP enabled + Cloud KMS CMK + Vertex AI safety filters configured + IAM Identity Federation
- **APEX-A**: Security Hub posture + Macie classifications enabled + KMS CMK + Bedrock Guardrails configured + IAM Identity Center

### Sprint G/A.6 — Per-service catalog port
Each service code that ships in the variant gets:

- `services/{ind}/{code}/iac/{terraform-gcp|cloudformation}/main.{tf|yaml}`
- `services/{ind}/{code}/use-cases/_default/use-case.yaml` regenerated with `primary_variant: APEX-G` (or `APEX-A`)

The provider-neutral parts (`service.yaml`, `scenario.yaml`, persona/KPI registries, generator) **do not change**.

## Variant-specific port notes

### APEX-G (Google Cloud)

**Strengths to leverage**:
- Vertex AI Vector Search has a clean separation of vector-store and model-host that maps well to APEX-Core protocols
- Workspace as an organizational-context source rivals M365 for some client segments
- Looker as the BI layer integrates naturally with BigQuery Gold marts

**Open questions**:
- Vertex Agent Builder's evolution (Agent Engine GA timeline) — the runtime story is moving fast
- Workspace Marketplace publishing for agents (parallel to M365 Copilot custom engine agents)
- Pricing model for Vertex AI Agent Engine vs flat-rate Foundry Hosted Agents

**Estimated effort**: 8–10 sprints from kickoff to first client deploy.

### APEX-A (AWS)

**Strengths to leverage**:
- Bedrock Agents has the clearest "agent + tools + actions" model out of the gate
- Lake Formation governance is mature for the client's existing data lake patterns
- Bedrock Guardrails has parity-or-better feature set vs Defender for AI

**Open questions**:
- AgentCore vs Bedrock Agents long-term positioning (similar to Foundry Hosted vs prompt-agent on APEX-M)
- IAM Identity Center maturity for agent-identity governance vs Microsoft Entra Agent ID
- M365 Copilot equivalent — Q in QuickSight is narrower; AppSync/Step Functions for custom UX

**Estimated effort**: 8–10 sprints from kickoff to first client deploy.

## Independence checkpoints during a port

Each sprint of a port reviews:

- [ ] No new "alliance" / "partner" / "preferred" language in commits
- [ ] LICENSE-ATTRIBUTION updated as concrete SDK dependencies are pinned
- [ ] APEX-M, APEX-G, APEX-A book set remains structurally identical
- [ ] No code shared at runtime between variants beyond `apex-core` (single exception: shared `apex-adapters` packages where the *client's* architecture board has approved a non-primary integration)
- [ ] Wizard's Cloud Variant selector updated; new variant moves from "Future · Independence Stub" to functional in the same release

## Out of scope for the port

- **Repackaging APEX-M's Foundry-specific details into APEX-G/A books**: each variant book is written natively for that variant; no cross-pollination of cloud-specific examples.
- **Cross-variant orchestration at runtime**: a single use case picks ONE primary variant. Adapters compose secondary services into that primary variant. Splitting agents across variants is not supported.
- **Single-codebase agents that run on all three runtimes**: the agent definition lives in the variant; portability is at the *protocol* level, not the *agent* level.

## Sequencing recommendation

Microsoft is staffed deepest. Port APEX-G next (Vertex AI Agent Builder is the closest functional parallel to Foundry Hosted Agents). Port APEX-A third (Bedrock Agents has unique IAM and Guardrails patterns that need fresh design).

Alternative: port both in parallel by separate teams — protocol contract isolates the work cleanly.
