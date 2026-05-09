# Microsoft Platform Alignment — Delta Review

**Date:** 2026-05-09
**Scope:** All 6 APEX books + service catalog + Bicep modules cross-checked against current Microsoft documentation (May 2026). Identifies concrete changes to make BEFORE deploying to Microsoft Platform (Azure / M365 / Power Platform / Security / Governance).

**Companion docs:**
- [`2026-05-09-rc-design-docs-foundry-design.md`](2026-05-09-rc-design-docs-foundry-design.md) — Path C runtime architecture
- [`2026-05-09-rc-design-docs-foundry-implementation.md`](2026-05-09-rc-design-docs-foundry-implementation.md) — implementation plan (will be extended below)

---

## TL;DR — what changed in Microsoft's platform since the books were written

| Area | Status | Impact on APEX |
|---|---|---|
| **Microsoft Entra Agent ID** | **GA April 2026** | Replaces ad-hoc managed-identity-only model for agents. Mandatory for production. |
| **Foundry Standard Setup with Private Networking** | GA | APEX production must use BYO VNet, delegated subnet, private endpoints. Bicep needs rewrite. |
| **Foundry BYO Storage + AI Search + Cosmos DB** | Required for Standard Setup | APEX must provision these at Layer 1, not let Foundry auto-provision. |
| **OneLake Security (user identity mode)** | GA | Replaces SQL `GRANT/REVOKE` on tables. RLS/CLS/object-level live in OneLake. |
| **OneLake primary-workspace pattern** | GA best practice | Centralize ownership in primary workspace; downstream consumes via shortcuts. APEX's per-service workspaces need a hub. |
| **Fabric workspace identity** | GA Jan 2026 | Default replaces SP-with-secret for workspace → ADLS Gen2 access. |
| **Workspace-level IP Firewall** | Preview Jan 2026 | Add to Layer 1 hardening. |
| **Defender for Cloud AI security posture (DSPM for AI)** | GA | Mandatory pre-prod — discovers AI BOM, runs attack-path analysis. |
| **Defender for AI services threat protection** | GA | Prompt shields, jailbreak detection, data leakage. Required by MCSB. |
| **Microsoft Purview for Foundry/M365 agents** | GA | Sensitivity-label propagation through RAG, DLP, audit log integration. APEX classification must align. |
| **AI Model Security scanning** | Preview | Pre-prod model scan for embedded malware/secrets. |
| **Custom engine agents for M365 Copilot** | GA May 2025 | Foundry-hosted agents publishable to M365 Copilot + Teams channels via M365 Agents Toolkit. |
| **Real-Time Intelligence MCP servers (Activator + Eventhouse)** | Preview Mar 2026 | Microsoft-hosted MCP — APEX can stop building custom MCP for these. |
| **Eventhouse SLM embeddings (`ai_embeddings`)** | Preview Jan 2026 | The Pricer's similarity search no longer needs external endpoint. |
| **Eventstream Activator destination** | GA Nov 2025 | Natural HITL trigger target. |
| **Eventstream DeltaFlow CDC** | Preview Mar 2026 | Flattens Debezium JSON for Bronze. Replaces custom CDC parsing. |
| **PostgreSQL flex server mirroring to Fabric** | GA Nov 2025 | New SOR option for tenants on PG. |
| **Fabric SQL Database (with Copilot)** | GA Nov 2025 | Alternative to Azure SQL for the LEDGER. |
| **Synapse Data Explorer → Eventhouse migration** | GA tooling | Any reference to "Synapse Data Explorer" is stale. |
| **Dataverse MCP servers + Python SDK** | GA Nov 2025 | New cross-service knowledge surface for org-context. |
| **Power Platform 2026 wave 1** | April–Sep 2026 | Multi-agent orchestration, deeper Foundry integration, Power Automate AI agent self-healing. |

---

## A. Identity layer — must adopt Entra Agent ID

**Current books:** Deployment Guide ch 1 + 8 reference user-assigned managed identities only (`mi-apex-merch-mcp` etc.). No agent-identity governance, no conditional access for agents, no agent-identity blueprints.

**Required changes:**

- [ ] **A.1** Adopt **Microsoft Entra Agent ID** as the canonical identity for every Foundry hosted agent in APEX. Replace text in Deployment Guide §8 and Professional APEX §13.
- [ ] **A.2** Define an **agent identity blueprint** per APEX service (e.g., `apex-rc-e2e-03-agent-blueprint`). Each scenario's 6 agents inherit conditional access, RBAC, and governance from the blueprint. Cite [Agent identity platform](https://learn.microsoft.com/entra/agent-id/identity-platform/what-is-agent-id-platform).
- [ ] **A.3** Add a **Conditional Access** chapter to Deployment Guide — agents accessing Tier-3/4 PII data must satisfy CA policies (compliant device, network range, MFA on HITL approver session).
- [ ] **A.4** Document **Workload Identity Federation** for the laptop-substrate Z-tier — agent on Docker Desktop authenticates via WIF instead of stored secret. Cite [Workload identity federation concepts](https://learn.microsoft.com/entra/workload-id/workload-identity-federation).
- [ ] **A.5** Update Bicep `infra/bicep/platform/identity.bicep` to provision Entra Agent ID parent identity in addition to UAMIs. Use the [Entra SDK for Agent ID](https://learn.microsoft.com/entra/msidweb/agent-id-sdk/scenarios/managed-identity).
- [ ] **A.6** Add to RC build plan as Sprint 30.A — enable Entra Agent ID at tenant; provision blueprints; CA policies.

## B. Data tier (Fabric) — must adopt OneLake Security + primary-workspace pattern + workspace identity

**Current books:** Services Guide ch 1 (Bronze→Silver→Gold) and ch 4–5 use per-service workspaces (`rc-e2e-03`, `hls-e2e-04`). Authentication described as "SP-with-secret" or "managed identity." No mention of user identity mode, OneLake security roles, or primary-workspace pattern.

**Required changes:**

- [ ] **B.1** Adopt the **primary-workspace pattern** ([best practice](https://learn.microsoft.com/fabric/onelake/security/best-practices-secure-data-in-onelake)). Each practice gets a primary workspace owning the canonical Silver entities (e.g., `rc-canonical` owns `SCML.*`, `MERML.*`, `PROML.*`, `CRMML.*`). Per-service workspaces (`rc-e2e-03`, etc.) consume via OneLake shortcuts. **Update Services Guide §1.2 + new §1.5.** Update Professional APEX ch 8.
- [ ] **B.2** Mandate **OneLake user identity mode** for SQL analytics endpoints serving HITL approvers. RLS/CLS/object-level live in OneLake; SQL `GRANT/REVOKE` ignored on tables. Cite [User identity mode](https://learn.microsoft.com/fabric/onelake/security/sql-analytics-endpoint-onelake-security#user-identity-mode-in-onelake-security). **Update Services Guide ch 1.3 (Silver contract) + Deployment Guide §13 Security Architecture.**
- [ ] **B.3** Adopt **Fabric workspace identity** GA. Replace any "service principal with secret" pattern in Services Guide §4.4 (`sor-connections.yaml`) with workspace-identity + trusted workspace access for ADLS Gen2.
- [ ] **B.4** Document the **1:1 identity mapping** rule for cross-workspace shortcuts in Services Guide §1.5: "If producer role references `Group A`, then `Group A` itself must have Fabric Read on consumer — not just a member."
- [ ] **B.5** Replace any "Synapse Data Explorer" reference with **Eventhouse**. Grep across all books and update.
- [ ] **B.6** Add **DeltaFlow CDC transformation** to Services Guide ch 5 (Real-Time Hub) — replaces custom Debezium JSON parsing for Bronze CDC.
- [ ] **B.7** Add **Eventstream Activator destination** as the canonical HITL trigger pattern in Deployment Guide ch 9 (HITL gates) and Services Guide ch 5.
- [ ] **B.8** Add **Eventhouse SLM embeddings** (`ai_embeddings`) as the recommended substrate for The Pricer's episodic-memory similarity search in Services Guide §25.8 (replaces external embedding endpoint).
- [ ] **B.9** Add **Real-Time Intelligence MCP servers** (Activator + Eventhouse remote MCP) to Deployment Guide ch 10 — APEX agents reuse these instead of bespoke MCP for the same surface.
- [ ] **B.10** Document **Workspace-level IP Firewall** (Preview) as Layer 1 hardening in Deployment Guide §13.
- [ ] **B.11** Add **PostgreSQL flex server mirroring** as a supported SOR pattern in Services Guide ch 4.
- [ ] **B.12** Document **Fabric SQL Database** as an alternative to Azure SQL for the LEDGER store in Deployment Guide ch 11 — comes with Copilot GA, may simplify the audit-row schema work.

## C. Security & Governance — must integrate with Defender for Cloud + Microsoft Purview

**Current books:** Deployment Guide ch 13 talks about classification tiers (T1–T4 PII/PHI) in APEX-specific terms. No reference to Microsoft Purview sensitivity labels, no Defender for Cloud integration, no DSPM for AI, no AI Content Safety prompt shields.

**Required changes:**

- [ ] **C.1** Map APEX classification tiers (T1–T4) to **Microsoft Purview sensitivity labels** ([Information Protection overview](https://learn.microsoft.com/graph/security-information-protection-overview)). Define the bidirectional mapping in Deployment Guide ch 13 + Services Guide §7.3. APEX classifications **must** flow as Purview sensitivity labels for the inheritance chain to work through Foundry RAG.
- [ ] **C.2** Adopt **Microsoft Purview DLP** for AI interactions — agent-to-human, human-to-agent, agent-to-tools, agent-to-agent flows. Update Deployment Guide ch 13 to reference [Purview DLP for AI](https://learn.microsoft.com/purview/ai-microsoft-purview).
- [ ] **C.3** Stop building parallel audit infrastructure. Use **Microsoft Purview Audit + DSPM for AI Activity Explorer** as the canonical capture; APEX's audit-row store is a *secondary* trace for KPI attribution. Deployment Guide ch 11 needs a major update.
- [ ] **C.4** Mandate **Defender for Cloud CSPM with AI security posture** as Sprint 30 prerequisite. APEX's AI BOM must surface in DSPM.
- [ ] **C.5** Mandate **Defender for AI services threat protection** for every Foundry project — prompt shields, jailbreak detection, credential theft detection. Required by [MCSB v2 Artificial Intelligence Security](https://learn.microsoft.com/security/benchmark/azure/mcsb-v2-artificial-intelligence-security).
- [ ] **C.6** Add **AI Model Security scanning** (Preview) to the pre-prod gate — every custom agent image scanned in CI/CD pipeline. Cite [AI model security](https://learn.microsoft.com/azure/defender-for-cloud/ai-model-security).
- [ ] **C.7** Add **Customer Managed Keys (CMK)** support to Layer 1 Bicep — required for Standard Setup with private networking.
- [ ] **C.8** New chapter in Deployment Guide: **Pre-deployment Security Gate** — checklist of MCSB controls, Purview labels enabled, Defender for Cloud + Defender for AI enabled, Entra Agent ID provisioned, CA policies in place, Customer Lockbox configured, AI Model Security scan green.
- [ ] **C.9** Update RC build plan with Sprint 30.S security-hardening items (B + C).

## D. Foundry runtime — must adopt Standard Setup with Private Networking

**Current books:** Deployment Guide ch 1 (recently approved Path C) describes Foundry generally but not the Standard Setup with Private Networking specifics. Bicep references AVM module but doesn't pin to standard-setup-with-private-networking pattern.

**Required changes:**

- [ ] **D.1** Specify **Standard Setup with Private Networking** as the APEX production substrate (S+ tier). Cite [Set up private networking for Foundry Agent Service](https://learn.microsoft.com/azure/foundry/agents/how-to/virtual-networks). **Bring Your Own**: Storage Account + Azure AI Search + Cosmos DB + virtual network with delegated `Microsoft.App/environments` subnet (/27 minimum).
- [ ] **D.2** Update Layer 1 Bicep to provision **all four BYO resources** before Foundry account creation. Network injection **must** be configured at Foundry account creation — cannot be added later.
- [ ] **D.3** Document the **ACR public-reachability constraint** — hosted-agent images require ACR over public endpoint at this time. Add to Deployment Guide §10 with a "watch this space" note for when private ACR support lands.
- [ ] **D.4** Provision the four required private DNS zones: `privatelink.cognitiveservices.azure.com`, `privatelink.openai.azure.com`, `privatelink.services.ai.azure.com`, plus AI Search / Cosmos DB / Storage zones. Add to `infra/bicep/platform/` as a `dns.bicep` module.
- [ ] **D.5** Adopt the **Customer Managed Keys** pattern for Storage Account and Cognitive Account (Foundry) when client compliance posture requires it.
- [ ] **D.6** Pin the AVM version (`br/public:avm/ptn/ai-ml/ai-foundry:<X.Y.Z>`) in `infra/bicep/platform/foundry.bicep`. Document upgrade policy.
- [ ] **D.7** Add to RC build plan: Sprint 30.D Foundry Standard Setup provisioning.

## E. M365 + Power Platform integration — surface APEX agents where users already work

**Current books:** Deployment Guide does not mention M365 Copilot publishing, Copilot Studio integration, Teams channel publishing, or Dataverse. This is a missed strategic opportunity — APEX agents that need conversational entry should surface in M365 Copilot.

**Required changes:**

- [ ] **E.1** Add a new chapter **"Surfacing APEX in Microsoft 365"** to Deployment Guide (proposed ch 11.5). Documents the [Custom engine agents for M365 Copilot](https://learn.microsoft.com/microsoft-365/copilot/extensibility/overview-custom-engine-agent) path. Foundry hosted agent → M365 Agents Toolkit packaging → publish to M365 Copilot + Teams.
- [ ] **E.2** Define publishing policy per RC service — e.g., RC-E2E-04 Loyalty Churn surfaced as Copilot Studio agent for marketers; RC-E2E-03 Pricing surfaced as M365 Copilot custom engine agent for the merchandising director.
- [ ] **E.3** Document **Microsoft Commercial Marketplace** path for agents Deloitte wants to ship across multiple tenants. Cite [Make your multitenant agent available](https://learn.microsoft.com/en-us/microsoft-copilot-studio/multi-tenant-make-agent-available-teams-microsoft-365-copilot).
- [ ] **E.4** Add **Dataverse** as an organizational-context data source for agents needing M365 entity lookups. Cite [Dataverse MCP server + Python SDK](https://learn.microsoft.com/power-platform/release-plan/2026wave1/data-platform/).
- [ ] **E.5** Add **Power Automate** as an alternative orchestration substrate for the wizard's "non-agent" workflow steps (e.g., approval routing, ticket creation). Cite Power Automate 2026 wave 1.
- [ ] **E.6** Update Sellers Guide to call out the M365 Copilot surface as part of every service envelope where applicable.

## F. Cross-cutting terminology fixes

Grep + replace across all 6 books:

- [ ] **F.1** "Azure AD" / "AAD" → **Microsoft Entra ID**
- [ ] **F.2** "Azure AI Studio" → **Microsoft Foundry**
- [ ] **F.3** "Real-Time Analytics" → **Real-Time Intelligence**
- [ ] **F.4** "Synapse Data Explorer" → **Eventhouse** (with note that the migration tooling is GA)
- [ ] **F.5** "Defender for X" branding (when meaning the unified portal) → **Defender XDR portal**
- [ ] **F.6** Confirm all `Microsoft.App/containerApps` references in service-Bicep examples are correct for **MCP servers** but NOT for agents (agents = Foundry hosted)

## G. Things APEX shouldn't build (already in Microsoft platform)

The most important lesson from this review: APEX is over-building in places where Microsoft has shipped GA capability since the books were written. Stop and reuse:

| APEX was building | Microsoft already provides | Action |
|---|---|---|
| Custom audit-row schema with HMAC signing | Microsoft Purview Audit + DSPM for AI Activity Explorer | Make Purview the system of record; APEX audit row is a KPI-attribution overlay only |
| Custom MCP server for Eventhouse queries | Real-Time Intelligence remote MCP (Eventhouse + Activator) | Adopt Microsoft-hosted MCP; deprecate `eventhouse-mcp` if planned |
| Custom embedding service for The Pricer's similarity memory | Eventhouse SLM `ai_embeddings` plugin | Switch to in-Eventhouse embeddings |
| Custom Bronze CDC parser for Debezium | Eventstream DeltaFlow transformation | Use DeltaFlow |
| Custom HITL alert trigger | Eventstream Activator destination | Use Activator |
| Custom agent identity governance | Microsoft Entra Agent ID + ID Governance | Use Entra Agent ID blueprints |
| Custom agent threat detection | Defender for AI services + Defender for Cloud | Enable Defender plans |
| Custom CDC for PostgreSQL SOR | Fabric Mirroring for Azure DB for PostgreSQL Flex | Use Mirroring |

## H. Things to validate (open questions)

- [ ] **H.1** Does the Foundry hosted-agent ACR public-reachability constraint conflict with Deloitte client tenants requiring no-public-egress? If yes, design a workaround (Container Apps fallback for those tenants until private ACR support lands).
- [ ] **H.2** APEX's "tenant manifest" per Deployment Guide §3 — is this still needed if Entra Agent ID provides the agent-identity registry? Consider folding APEX manifest into Entra Agent ID blueprints.
- [ ] **H.3** APEX's audit-row schema (14 fields per BL.P.77) — needs cross-walk against Purview Audit schema. Likely overlap; reconcile.
- [ ] **H.4** Does Foundry Agent Service's standard region list cover every Deloitte client tenant region we'll target? Validate against client commercial envelopes.
- [ ] **H.5** APEX's classification tier model (T1–T4) — cross-walk with Purview's standard sensitivity-label taxonomy (Public / Internal / Confidential / Highly Confidential / Strictly Confidential). Likely 1:1 but confirm.

---

## Recommended sprint additions to RC build plan

| Sprint | Items |
|---|---|
| **Sprint 30.A** (Identity) | A.1 Entra Agent ID enable · A.2 blueprints · A.3 CA policies · A.5 Bicep update |
| **Sprint 30.B** (Data tier hardening) | B.1 primary-workspace pattern · B.2 OneLake user identity mode · B.3 workspace identity · B.10 IP firewall |
| **Sprint 30.C** (Security/Governance) | C.1–C.7 sensitivity labels, DLP, Purview Audit, Defender CSPM + AI, AI Model Scan, CMK |
| **Sprint 30.D** (Foundry Standard Setup) | D.1–D.6 BYO resources, private networking, DNS, AVM pinning |
| **Sprint 30.E** (Surface in M365 — optional, post-pilot) | E.1–E.5 M365 publishing path, Dataverse, Power Automate |
| **Sprint 30.F** (Terminology grep) | F.1–F.6 across all 6 books |
| **Sprint 30.S** (Pre-deployment Security Gate) | C.8 — gate every wave on the checklist |

These weave into the existing Phase A through Phase H of the implementation plan. Phase G (book updates) gets significantly heavier — the books need real surgery, not just a Layer 3 paragraph swap.

---

## References (Microsoft Learn)

**Identity:** [What is Microsoft Entra Agent ID?](https://learn.microsoft.com/entra/agent-id/what-is-microsoft-entra-agent-id) · [Entra Agent ID releases April 2026](https://learn.microsoft.com/entra/fundamentals/whats-new#april-2026) · [Workload identity federation](https://learn.microsoft.com/entra/workload-id/workload-identity-federation) · [Microsoft agent identity platform for developers](https://learn.microsoft.com/entra/agent-id/identity-platform/what-is-agent-id-platform)

**Data tier (Fabric):** [What's new in Microsoft Fabric](https://learn.microsoft.com/fabric/fundamentals/whats-new) · [OneLake security best practices](https://learn.microsoft.com/fabric/onelake/security/best-practices-secure-data-in-onelake) · [OneLake security for SQL analytics endpoints](https://learn.microsoft.com/fabric/onelake/security/sql-analytics-endpoint-onelake-security) · [Workspace identity](https://learn.microsoft.com/fabric/security/workspace-identity) · [Fabric end-to-end security scenario](https://learn.microsoft.com/fabric/security/security-scenario) · [Build AI agents for Real-Time Intelligence](https://learn.microsoft.com/fabric/real-time-intelligence/ai-agents-eventhouse) · [Eventhouse SLM embeddings](https://learn.microsoft.com/en-us/kusto/functions-library/slm-embeddings-fl) · [DeltaFlow CDC](https://learn.microsoft.com/fabric/real-time-intelligence/event-streams/delta-flow-output-transformation)

**Security/Governance:** [Defender for Cloud overview](https://learn.microsoft.com/azure/defender-for-cloud/defender-for-cloud-introduction) · [AI threat protection](https://learn.microsoft.com/azure/defender-for-cloud/ai-threat-protection) · [AI security posture management](https://learn.microsoft.com/azure/defender-for-cloud/ai-security-posture) · [AI model security](https://learn.microsoft.com/azure/defender-for-cloud/ai-model-security) · [Purview for Foundry](https://learn.microsoft.com/purview/ai-azure-foundry) · [Purview for M365 Copilot](https://learn.microsoft.com/purview/ai-m365-copilot) · [Purview for Copilot Studio](https://learn.microsoft.com/purview/ai-copilot-studio) · [Purview for Agent 365](https://learn.microsoft.com/purview/ai-agent-365) · [Purview Information Protection](https://learn.microsoft.com/graph/security-information-protection-overview) · [Azure AI security best practices](https://learn.microsoft.com/azure/security/fundamentals/ai-security-best-practices) · [MCSB v2 AI Security](https://learn.microsoft.com/security/benchmark/azure/mcsb-v2-artificial-intelligence-security)

**Foundry:** [Foundry Agent Service overview](https://learn.microsoft.com/azure/foundry/agents/overview) · [Standard Setup with Private Networking](https://learn.microsoft.com/azure/foundry/agents/how-to/virtual-networks) · [Foundry Agent Service environment setup](https://learn.microsoft.com/azure/foundry/agents/environment-setup) · [Foundry Hosted Agents (Agent Framework)](https://learn.microsoft.com/agent-framework/hosting/foundry-hosted-agent) · [AVM `ai-foundry` Bicep module](https://github.com/Azure/bicep-registry-modules/tree/main/avm/ptn/ai-ml/ai-foundry)

**M365 + Power Platform:** [Custom engine agents for M365 Copilot](https://learn.microsoft.com/microsoft-365/copilot/extensibility/overview-custom-engine-agent) · [Publish agents for M365 Copilot](https://learn.microsoft.com/microsoft-365/copilot/extensibility/publish) · [Power Platform 2026 wave 1](https://learn.microsoft.com/power-platform/release-plan/2026wave1/) · [Dataverse MCP + Python SDK 2026](https://learn.microsoft.com/power-platform/release-plan/2026wave1/data-platform/)
