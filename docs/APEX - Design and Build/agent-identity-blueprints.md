# Agent Identity Blueprints — APEX-M (Microsoft Entra Agent ID)

**Phase I.1 deliverable.** Design for the agent-identity layer of every APEX-M deployment.

**Status:** Authoritative design. Concrete tenant provisioning happens per-engagement.

**Reference:**
- [Microsoft Entra Agent ID](https://learn.microsoft.com/entra/agent-id/what-is-microsoft-entra-agent-id) — GA April 2026
- [Entra Agent ID identity platform for developers](https://learn.microsoft.com/entra/agent-id/identity-platform/what-is-agent-id-platform)
- [Agent blueprints](https://learn.microsoft.com/entra/agent-id/identity-platform/agent-blueprint)
- [Microsoft Cloud Security Benchmark v2 — Artificial Intelligence Security](https://learn.microsoft.com/security/benchmark/azure/mcsb-v2-artificial-intelligence-security)
- APEX-Core: [`AgentIdentityProvider` protocol](../../packages/apex-core/src/apex_core/protocols/agent_identity.py)
- APEX-M impl: [`apex_m.identity_entra`](../../apex-m/src/apex_m/identity_entra.py)

---

## 1. Why Entra Agent ID

Pre-April 2026, APEX-M agents used user-assigned managed identities (UAMI) directly. That worked for narrow scopes (one identity per agent role) but scaled badly:

- No native concept of an "agent identity" with parent/child relationships
- Conditional Access policies had to be authored per-UAMI
- Identity governance (lifecycle, access reviews, expiration) was bolt-on
- Agent-to-agent (A2A) authentication required custom OAuth dance
- M365 Copilot agent registration was disconnected from runtime identity

**Entra Agent ID** (GA April 2026) addresses every one of these gaps. Per Microsoft's overview:

> *"Microsoft Entra Agent ID is an identity and security framework that extends Microsoft Entra capabilities to AI agents… The Microsoft Entra Agent identity platform enables developers to create and manage agent identities, which are specialized identity constructs built for AI agents. Agent identity blueprints serve as templates for creating individual agent identities with parent-child relationships, enabling consistent security policies across large numbers of agents."*

APEX-M adopts Entra Agent ID as the **canonical** identity layer for agents in production deployments.

## 2. The blueprint hierarchy

Entra Agent ID's parent-child model maps naturally onto APEX's three-layer cake:

```
Layer 1 — APEX-M Tenant Root Blueprint
  ├─ apex-m-tenant-root                                        (parent)
  │   ├─ Conditional Access: tenant baseline (MFA on HITL)
  │   ├─ Identity Governance: 90-day access reviews
  │   └─ Lifecycle: revoke on tenant decommission
  │
  ├─ Layer 2 — Per-Service Blueprints (one per APEX service)
  │   ├─ apex-m-rc-e2e-03-blueprint                           (RC-E2E-03 = Pricing & Revenue)
  │   │   ├─ inherits: apex-m-tenant-root
  │   │   ├─ Adds CA: Tier-3 PII access requires compliant device
  │   │   ├─ Adds RBAC: Cosmos DB Reader on rc-canonical workspace
  │   │   └─ Adds RBAC: Storage Blob Data Reader on rc-canonical Silver
  │   ├─ apex-m-rc-e2e-04-blueprint                           (Loyalty Churn — Tier-3 PII)
  │   ├─ apex-m-rc-e2e-07-blueprint                           (Returns Fraud — Tier-3 PII)
  │   └─ … one per service code …
  │
  └─ Layer 3 — Per-Agent Identities (instantiated from blueprints)
      ├─ apex-m:rc-e2e-03:cold-chain-excursion-mid-shift:assess
      ├─ apex-m:rc-e2e-03:cold-chain-excursion-mid-shift:classify
      ├─ apex-m:rc-e2e-03:cold-chain-excursion-mid-shift:quantify
      ├─ apex-m:rc-e2e-03:cold-chain-excursion-mid-shift:decide
      ├─ apex-m:rc-e2e-03:cold-chain-excursion-mid-shift:act
      ├─ apex-m:rc-e2e-03:cold-chain-excursion-mid-shift:learn
      ├─ apex-m:rc-e2e-03:cold-chain-excursion-mid-shift:pricing  (The Pricer)
      └─ … 6–7 per scenario × 36 featured scenarios = ~250 identities …
```

Disabling a blueprint disables every identity beneath it in one operation — critical for incident response and tenant decommissioning.

## 3. Naming convention

Blueprint and identity ids are deterministic so the wizard, the audit row, and the Entra portal stay in sync:

| Layer | Pattern | Example |
|---|---|---|
| Tenant root | `apex-m-tenant-root` | `apex-m-tenant-root` |
| Service blueprint | `apex-m-{service-code-lowercase}-blueprint` | `apex-m-rc-e2e-03-blueprint` |
| Agent identity | `apex-m:{service-code}:{scenario-id}:{role}` | `apex-m:rc-e2e-03:rc-cold-chain-excursion-mid-shift:pricing` |

The wizard's render endpoint emits these ids. The audit row's `agent_id` field uses this exact format. Cross-references trace cleanly.

## 4. Per-blueprint policy

### 4.1 Tenant root (`apex-m-tenant-root`)

**Conditional Access (baseline):**
- HITL approver session must satisfy MFA + compliant device (per Defender for Endpoint)
- Block sign-in from unmanaged devices and risky IP ranges
- Sign-in frequency: 8 hours for HITL approvers, 24 hours for autonomous agents

**Identity Governance:**
- 90-day access review on the blueprint's role assignments
- Sponsor: tenant SRE (per [Pre-deployment Security Gate](Pre-deployment-Security-Gate.md))
- Auto-revoke on tenant decommission

**Lifecycle:**
- Created: by `apex-m/infra/bicep/platform/identity.bicep` at tenant provisioning
- Revoked: by `tools/decommission-tenant.py` (TBD)

### 4.2 Per-service blueprint policy

| Service code | Domain | Tier risk | Service-specific CA / RBAC additions |
|---|---|---|---|
| RC-E2E-03 | Pricing & Revenue | T2 | Cosmos DB Reader on rc-canonical · Storage Blob Data Reader on Silver |
| RC-E2E-04 | Customer Experience (Loyalty) | **T3 PII** | + Tier-3 PII unlock requires HITL approver MFA + step-up audit |
| RC-E2E-05 | On-Shelf Availability | T2 | Storage Blob Data Reader on shelf-gap Silver |
| RC-E2E-06 | Workforce Operations | T2 | + Workday connector read scope |
| RC-E2E-07 | Returns Fraud | **T3 PII** | + adaptive HITL threshold; auto-clear < 0.4 score, escalate > 0.7 |
| RC-E2E-08 | Marketing & Growth | T2 | + Adobe Experience Platform connector |
| RC-E2E-09 | Product Tracking (FSMA 204) | T2 + reg | + cross-Service consumer attestation (RC-E2E-03) |

For HLS / ER / AXLE / TH / TMT / ICE practices, equivalent blueprint matrices live in their respective build plan docs (TBD).

### 4.3 Per-agent identity policy

- All identities inherit parent blueprint CA + RBAC
- The `decide` and `act` roles add HITL gate binding (per [Pre-deployment Security Gate](Pre-deployment-Security-Gate.md))
- The Pricer role gets Redis Cache read/write scope for its episodic memory (Services Guide §25.8)

## 5. Cross-cloud federation slot

When a use case's `client_approved_architecture.identity.federation` references an adapter (e.g., `identity.okta`), Entra Agent ID acts as the *primary* with the adapter providing federation:

```
Operator (workforce in Okta)
        │
        ▼  (OIDC)
[ identity.okta adapter ]
        │
        ▼  (Workload Identity Federation)
[ Microsoft Entra ID ]
        │
        ▼  (Entra Agent ID OBO token exchange)
[ Agent identity: apex-m:rc-e2e-03:...:decide ]
        │
        ▼  (managed identity → resource access)
[ Cosmos DB · Fabric · Key Vault · Foundry Agent Service ]
```

The adapter satisfies APEX-Core's `AgentIdentityProvider` for the federation slot only; Entra Agent ID remains the runtime authority. Token issuance, rotation, and revocation are Microsoft's; the adapter only attests the operator's home-tenant identity.

## 6. Workload Identity Federation for the laptop substrate

Per Deployment Guide ch 2 (substrate-aware), the same agent image runs on Docker Desktop locally and Foundry on Azure in prod. Local substrate uses **Workload Identity Federation** instead of stored secrets:

- Laptop runs the agent container with a federated credential file (`AZURE_FEDERATED_TOKEN_FILE`)
- The federated identity is a child of `apex-m-{service-code}-blueprint` in Entra Agent ID
- Token exchange happens against Microsoft identity platform; no static credential lives on the laptop

This satisfies MCSB v2 AI-7 (no long-lived secrets in development environments).

## 7. Provisioning sequence

The wizard provisions identities in this order at platform deployment:

1. **Tenant root blueprint** — created by `apex-m/infra/bicep/platform/identity.bicep` via Microsoft Graph API call
2. **Service blueprints** — created per service code the operator selects in the wizard
3. **Per-agent identities** — instantiated from blueprints when the wizard runs `az deployment group create` for the agent fleet
4. **Federation credentials** — provisioned for non-Entra IdPs (Okta, Auth0, etc.) per the use case's `client_approved_architecture.identity.federation` block

Each step writes an audit row to Microsoft Purview Audit (system of record). The `apex-m.AuditLedger` impl appends a KPI-attribution overlay row.

## 8. Decommissioning

Tenant decommission revokes the tenant root blueprint, which cascades to every service blueprint and every per-agent identity. The Entra portal shows the full hierarchy as "Disabled — pending review" for 30 days, then hard-deletes per identity governance lifecycle policy.

This is testable: spin up a Lab tenant, create the blueprints, then run `tools/decommission-tenant.py` (TBD) and confirm 100% of identities transition to "Disabled" within the SLA.

## 9. Audit defensibility

Every API call by an APEX-M agent traces to:

1. **Agent identity** (deterministic id per §3) — the principal
2. **Blueprint** — the policy parent
3. **Operator principal** (via OBO) — for HITL-gated decisions
4. **Conditional Access result** — pass / blocked-by-policy / step-up-required
5. **Token issuance time + expiry** — short-lived (1h max for autonomous, 8h for HITL session)

All five fields land in the audit row's structured trace. Microsoft Purview Audit is system of record (per [Microsoft platform alignment delta §C.3](../plans/2026-05-09-microsoft-platform-alignment-delta.md#c-security--governance-must-integrate-with-defender-for-cloud--microsoft-purview)).

## 10. APEX-Core protocol mapping

The `AgentIdentityProvider` protocol's contract maps onto Entra Agent ID concepts as:

| Protocol method | Entra Agent ID concept | APEX-M impl module |
|---|---|---|
| `create_blueprint(blueprint)` | Microsoft Graph `POST /agentIdentities/blueprints` | `apex_m.identity_entra` |
| `provision_identity(blueprint_id, agent_id)` | Microsoft Graph `POST /agentIdentities/{blueprint_id}/instances` | same |
| `get_identity(agent_id)` | Microsoft Graph `GET /agentIdentities/{agent_id}` | same |
| `revoke_identity(agent_id, reason)` | Microsoft Graph `DELETE /agentIdentities/{agent_id}` (soft delete) | same |
| `acquire_obo_token(agent_id, operator_principal, target_resource)` | OAuth 2.0 OBO flow per [Microsoft identity platform](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-on-behalf-of-flow) | same |
| `list_blueprints()` | Microsoft Graph `GET /agentIdentities/blueprints?$filter=startswith(id,'apex-m-')` | same |

When APEX-G ships, an equivalent design doc covers `apex_g.identity_iam` against Cloud IAM service-account impersonation. APEX-A covers `apex_a.identity_iam_identity_center`.

## 11. Cross-references

- [Pre-deployment Security Gate](Pre-deployment-Security-Gate.md) — gates that must satisfy before agent identities provision
- [APEX-Core Independence Posture](../apex-core/Independence-Posture.md) — variant equality story
- [Microsoft platform alignment delta §A](../plans/2026-05-09-microsoft-platform-alignment-delta.md#a-identity-layer--must-adopt-entra-agent-id) — full delta detail
- [Roadmap.md BL.P.53](Roadmap.md) — managed-identity provisioning (now superseded by this design)
- [APEX-M Deployment Guide ch 8 — Identity, Scope & Visibility Lattice](../book/Professional-APEX-M-Deployment-Guide.html#ch-8) — implementation
