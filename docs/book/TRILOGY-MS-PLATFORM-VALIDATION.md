# Trilogy Microsoft-Platform Validation Report

> **Status (2026-05-11): ALL D1–D9 + A1–A6 + A7–A9 APPLIED.**
> The original D1–D9 + A1–A6 recommendations have been landed in
> `Professional-APEX-M-Services-Guide.html` and `Professional-APEX-M-Deployment-Guide.html`.
> The May 2026 Fabric IQ pass adds A7–A9 — landed as new closing appendices in all three
> Trilogy volumes plus a currency banner on the Library landing.
> This report is preserved as the audit trail of what was changed and why.

## 2026-05-11 update · Fabric IQ adoption pass

**Method:** Re-grounded against current Microsoft Learn via `microsoft_docs_fetch` against
`learn.microsoft.com/fabric/iq/overview`, `.../data-science/concept-data-agent`,
`.../real-time-intelligence/operations-agent`, and `.../iq/ontology/overview`.

**Added recommendations (now applied):**

- **A7 — Fabric IQ workload as a first-class architectural option.** Microsoft shipped the
  workload bundling Ontology · Plan · Graph · Data Agent · Operations Agent · Power BI
  semantic models. Services Guide Appendix O (new) documents 14 architectural edits;
  Sellers Guide Appendix AB (new) handles positioning; Library landing carries a currency
  banner. Status pin: workload preview; Data Agent GA.
- **A8 — Fabric Data Agent (GA) as MCP-equivalent for read paths.** The Data Agent dispatches
  NL2SQL / NL2DAX / NL2KQL / Microsoft Graph / NL2Ontology natively. Hard constraints
  surfaced: 5 sources/agent · 25-row × 25-column response cap · English only · region
  affinity · LLM not user-configurable. MCP catalog bifurcates into Read (Fabric Data Agent
  path) vs. Action (custom MCP servers stay).
- **A9 — Operations Agent as a new orchestration archetype.** Configuration shape
  (goals · instructions · data · actions → playbook); creator-identity action execution
  model; Activator + Power Automate flow wiring; Teams app required. Deployment Guide
  Appendix M (new) documents the substrate-side mechanics including F-SKU floor and the
  new **PSG-16** candidate (Workspace Outbound Boundary).

**Design doc:** `docs/plans/2026-05-11-trilogy-fabric-iq-adoption-design.md`

**Author:** Keven Markham, Vice President, Deloitte Microsoft Technology & Services Practice (DMTSP)
**Scope:** Cross-check load-bearing Microsoft-platform claims in the APEX Trilogy (Services Guide, Deployment Guide, Sellers Guide) against current Microsoft Learn documentation.
**Method:** 10 targeted `microsoft_docs_search` passes against Microsoft Agent Framework, Foundry Agent Service, Microsoft Entra Agent ID, Microsoft Fabric, Microsoft Purview (DSPM for AI), Microsoft Sentinel/Defender for AI, `Microsoft.Fabric/capacities` Bicep, Azure AI Content Safety, Azure Logic Apps Hybrid, and Microsoft Notation/AKV image signing.
**Audience:** Deloitte authors and reviewers editing the trilogy. Not for client release.
**Date:** 2026-05-10

---

## 1. How to read this report

The trilogy is **largely correct** on Microsoft platform architecture. The big-picture story (Agent Framework patterns, Foundry hosted agents, Microsoft Entra Agent ID, Fabric capacity hierarchy, Content Safety primitives, Notation+AKV signing) matches current Microsoft Learn.

What needs attention is **version pinning, role names, hosting fabric, and a handful of new features that have shipped or moved out of preview** since the earlier drafts. None of these are conceptual rewrites — they are surgical edits.

I have grouped findings as:

- **Validations** — the trilogy matches current Microsoft guidance; leave as-is.
- **Deviations** — the trilogy says something that no longer matches Microsoft Learn; specific edit recommended.
- **Recommended additions** — features Microsoft has shipped that strengthen the trilogy's story and should be considered for inclusion.

---

## 2. Validations (no changes needed)

| # | Claim in trilogy | Microsoft source | Status |
|---|---|---|---|
| V1 | Agent Framework supports five workflow patterns: **Sequential, Concurrent, Handoff, Group Chat, Magentic** | Microsoft Learn — Agent Framework workflows | Confirmed |
| V2 | Microsoft Fabric uses a four-level hierarchy: **Tenant → Capacity → Workspace → Item** | Microsoft Learn — Fabric concepts | Confirmed |
| V3 | F-SKU naming convention; **F64** is the threshold for Power BI viewer-free entitlement | Microsoft Learn — Fabric licensing | Confirmed |
| V4 | Microsoft Entra Agent ID supports **agent blueprints + federated identity credentials** for non-human (agent) principals | Microsoft Learn — Entra Agent ID | Confirmed |
| V5 | Foundry hosted-agent container requirements: **linux/amd64**, image pushed to **Azure Container Registry**, **Application Insights** auto-injected | Microsoft Learn — Foundry Agent Service hosted agents | Confirmed |
| V6 | Azure AI Content Safety primitives: **Prompt Shields (GA), Protected Material, Groundedness Detection, Custom Categories** | Microsoft Learn — Azure AI Content Safety | Confirmed |
| V7 | Container image signing using **Microsoft Notation CLI + Azure Key Vault** signing keys (CNCF Notary v2) | Microsoft Learn — ACR + Notation | Confirmed |
| V8 | OneLake is the **single logical lake per tenant**; shortcuts replace data copies | Microsoft Learn — OneLake | Confirmed |
| V9 | Direct Lake mode is exclusive to Fabric semantic models on F-SKU capacities | Microsoft Learn — Direct Lake | Confirmed |
| V10 | Activator (Real-Time Intelligence) is the eventing/alerting layer for Eventstream-fed signals | Microsoft Learn — Real-Time Intelligence | Confirmed |

---

## 3. Deviations (edits required)

### D1 — Bicep API version for Fabric capacities is **wrong**

**Where it appears:** Deployment Guide, anywhere the Bicep snippet `Microsoft.Fabric/capacities@2025-01-15-preview` appears (primary instance in Ch 6A and the Bicep appendix).

**What Microsoft Learn says now:** The Azure Verified Module (AVM) `avm/res/fabric/capacity` and Microsoft.Fabric resource provider reference list **`2023-11-01`** as the stable, GA API version. The `2025-01-15-preview` version exists but is preview-only and not recommended for production deployment templates.

**Recommended edit:**
- **Replace:** `Microsoft.Fabric/capacities@2025-01-15-preview`
- **With:** `Microsoft.Fabric/capacities@2023-11-01`
- Add a note: *"If you need preview-only features such as [feature], pin to the preview API. Otherwise the stable `2023-11-01` is the production default."*

### D2 — Logic Apps Hybrid hosting fabric is **under-specified**

**Where it appears:** Deployment Guide Ch 5/6 and Services Guide §32A where Logic Apps Hybrid is positioned as a "trigger + HTTP entry point."

**What Microsoft Learn says:** Logic Apps Hybrid (Standard, Hybrid hosting option) runs on **Azure Arc-enabled Kubernetes** — specifically, on an **Azure Arc-enabled AKS or any conformant Kubernetes cluster** registered with Arc, with the **App Service Kubernetes Environment (`Microsoft.App/connectedEnvironments` / `Microsoft.Web/kubeEnvironments`)** providing the runtime. It is **not** the same as Container Apps on `Microsoft.App/managedEnvironments`.

**Recommended edit:** In Ch 5 (deployment topology) and §32A (trigger pattern), add one paragraph:

> *Logic Apps Hybrid runs on an Azure Arc-enabled Kubernetes cluster — typically AKS — registered as a connected environment via the App Service Kubernetes Environment provider. This is the same Arc-enabled fabric used by Container Apps on Arc, but the resource provider is `Microsoft.Web/kubeEnvironments`, not `Microsoft.App/managedEnvironments`. SQL Server is required for the runtime state store.*

### D3 — Foundry hosted-agent **sandbox sizing not stated**

**Where it appears:** Services Guide Ch 11 / Deployment Guide Ch 6 hosted-agents section.

**What Microsoft Learn says:** Foundry hosted agents run in a managed sandbox with explicit SKU choices ranging from **0.25 vCPU / 0.5 GiB** to **2 vCPU / 4 GiB**. Cold-start latency and concurrency caps differ by SKU.

**Recommended edit:** Add a small table to the hosted-agents section:

| Sandbox SKU | vCPU | Memory | Best for |
|---|---|---|---|
| XS | 0.25 | 0.5 GiB | Lightweight tool agents, classifiers |
| S | 0.5 | 1 GiB | Standard reasoning agents |
| M | 1 | 2 GiB | RAG-heavy agents with larger context windows |
| L | 2 | 4 GiB | Multi-tool agents, long-running plans |

### D4 — Magentic builder API name is **wrong**

**Where it appears:** Pseudo-code blocks in Services Guide showing the Magentic pattern. Trilogy uses `BuildMagentic(...)`.

**What Microsoft Learn says:** The actual API in the Microsoft Agent Framework Python SDK is **`MagenticBuilder`** (a class) — used as `MagenticBuilder().participants(...).manager(...).build()`. The .NET SDK uses an equivalent fluent builder.

**Recommended edit:** Find/replace `BuildMagentic` → `MagenticBuilder()...build()` and adjust the surrounding pseudo-code to be a fluent chain rather than a single function call.

### D5 — Required RBAC role for hosted-agent deployment **not named**

**Where it appears:** Deployment Guide §11.5 (hosted agents permissions) and Services Guide Ch 11 sidebar.

**What Microsoft Learn says:** To deploy a hosted agent to a Foundry project you must hold the **`Azure AI Project Manager`** role at project scope (plus `AcrPush` on the registry and `Reader` on the resource group). For Microsoft Entra Agent ID, the named roles are **`Agent ID Administrator`** (tenant-wide) and **`Agent ID Developer`** (per-blueprint).

**Recommended edit:** Add an explicit "Required roles" callout box:

> **Required Microsoft Entra roles**
> - `Azure AI Project Manager` — deploy hosted agents to the Foundry project
> - `Agent ID Administrator` — create and manage agent identity blueprints tenant-wide
> - `Agent ID Developer` — author and version blueprints in delegated scope
> - `AcrPush` — push signed images to ACR
> - `Key Vault Crypto User` — sign with the Notation signing key

### D6 — `fmi_path` parameter on agent identity token requests **missing**

**Where it appears:** Services Guide Ch 14B (agent identity OAuth flow) and Deployment Guide Ch 5A.

**What Microsoft Learn says:** Federated agent-identity token requests to Microsoft Entra include the **`fmi_path`** parameter (Federated Managed Identity path) to scope the token to a specific agent blueprint instance.

**Recommended edit:** Update the OAuth pseudo-code to include `fmi_path` on the token request, and add a one-line gloss: *"`fmi_path` scopes the federated token to a specific blueprint instance — without it the broker cannot resolve which agent is asking."*

### D7 — Hosted-agent ACR network reachability constraint **not stated**

**Where it appears:** Deployment Guide Ch 6 / Ch 12A (networking).

**What Microsoft Learn says (current limitation):** Foundry hosted agents currently require the source ACR to be **reachable over the public endpoint** during agent deployment. Private-endpoint-only ACRs are not yet supported for hosted-agent ingest.

**Recommended edit:** Add this as a **known constraint** callout in Ch 12A (Networking), so readers do not design themselves into a corner with a private-endpoint-only ACR:

> **⚠ Current constraint (check Microsoft Learn for updates):** Foundry hosted-agent deployment pulls from ACR over the public endpoint. If your ACR is private-endpoint-only, you must either (a) enable a service endpoint exception for Foundry, or (b) stage the image via a public-reachable ACR for the deployment step. Microsoft has signaled private-endpoint support is on the roadmap.

### D8 — DSPM for AI: trilogy references the **classic** version

**Where it appears:** Services Guide Ch 14B (Purview) and Deployment Guide Ch 5A.

**What Microsoft Learn says:** Microsoft has shipped a **new DSPM for AI** experience in the Purview portal, distinct from the "classic" DSPM for AI surface. The new experience adds agent-specific signals, agent inventory, and risk-event correlation with Microsoft Entra ID Protection (`unfamiliarResourceAccess`, `signInSpike`, `failedAccessAttempt`, `riskyUserSignIn`, `threatIntelligenceAccount`).

**Recommended edit:** Distinguish the two surfaces explicitly. Recommend the **new DSPM for AI** as the default and keep the classic reference only for tenants that have not yet migrated.

### D9 — n8n / Logic Apps positioning needs a final consistency pass

**Where it appears:** Sprinkled across all three books wherever orchestration is discussed.

**What's been done:** Most references have been repositioned from "orchestrator" to "trigger + HTTP entry point" with Microsoft Agent Framework owning inter-agent coordination.

**Recommended final pass:** Grep all three HTML files for `n8n` and `Logic Apps` and verify every remaining occurrence either:
- positions them as **trigger / HTTP entry / lightweight integration**, OR
- is explicitly tagged as **laptop-only zero-cost dev substrate** (per the MVP memory note).

No occurrence should imply n8n or Logic Apps owns multi-agent orchestration — that is Microsoft Agent Framework's job in APEX-M.

---

## 4. Recommended additions (new Microsoft features)

These have shipped or matured since the earlier trilogy drafts. Each one strengthens the story.

### A1 — Microsoft Entra ID Protection for agents
ID Protection now emits agent-specific risk events: `unfamiliarResourceAccess`, `signInSpike`, `failedAccessAttempt`, `riskyUserSignIn`, `threatIntelligenceAccount`. **Where to add:** Services Guide Ch 14B (Security & Governance) — one paragraph + a small risk-event table.

### A2 — Task Adherence API in Azure AI Content Safety
A new Content Safety primitive that scores whether an agent's actions stayed within the bounds of its assigned task. Useful for the "did the agent do what we asked, and only what we asked" guardrail. **Where to add:** Services Guide Ch 14A (Responsible AI) — list it alongside Prompt Shields / Groundedness / Protected Material.

### A3 — Microsoft Sentinel `AIAgentsInfo` table + Defender AI agent alerts
Sentinel now has a dedicated `AIAgentsInfo` table; Defender ships pre-built alerts under the `AI.Azure_Agentic_*` family. **Where to add:** Deployment Guide Ch 6B (Sentinel + Defender) — replace any generic "alerts for AI" text with the named table and alert family.

### A4 — Microsoft Security Copilot Dynamic Threat Detection Agent
Security Copilot now offers a Dynamic Threat Detection Agent that authors and tunes Sentinel detections. **Where to add:** Deployment Guide Ch 6B — short callout that this is the recommended way to author APEX-specific detections rather than hand-writing KQL.

### A5 — Sentinel Custom Connector Builder agent + MCP server
Sentinel ships an agent that builds custom data connectors, and a Sentinel MCP server that AI agents can target. **Where to add:** Services Guide §32A (MCP) — note that Sentinel is one of the Microsoft-platform MCP endpoints APEX agents can call.

### A6 — Foundry Agent Service: Connected Agents & Computer Use
Two newer Foundry features worth a paragraph each: **Connected Agents** (agent-to-agent delegation hosted inside Foundry) and **Computer Use** (agent-controlled browser/desktop actions). **Where to add:** Services Guide Ch 11 — short description of when to use Foundry-hosted Connected Agents vs Agent Framework code-side workflow patterns.

---

## 5. Prioritized punch list

If you only do five things, do these:

| Priority | Edit | Effort | Why first |
|---|---|---|---|
| **1** | Fix Bicep API version `2025-01-15-preview` → `2023-11-01` (D1) | 5 min | Production templates will fail policy if they pin to preview |
| **2** | Name required RBAC roles in §11.5 (D5) | 15 min | Deployment teams cannot start without this |
| **3** | Distinguish new vs classic DSPM for AI (D8) | 30 min | Security architects will flag this immediately |
| **4** | Fix `MagenticBuilder` API name in pseudo-code (D4) | 10 min | Pseudo-code that won't compile undermines technical credibility |
| **5** | Add hosted-agent sandbox SKU table (D3) | 15 min | First question every deployment lead asks |

Then, in the next pass:

| Priority | Edit | Effort |
|---|---|---|
| 6 | Logic Apps Hybrid hosting clarification (D2) | 20 min |
| 7 | Add `fmi_path` to OAuth flow (D6) | 10 min |
| 8 | Add ACR public-endpoint constraint callout (D7) | 10 min |
| 9 | Final n8n / Logic Apps positioning grep (D9) | 30 min |
| 10 | Layer in additions A1–A6 (one per chapter sidebar) | 2–3 hrs total |

---

## 6. What I did **not** validate (out of scope for this pass)

- D365, Power Platform, Dataverse — the trilogy touches these but they were not the focus of this pass. Recommend a follow-up validation focused on the **Industry Solutions / D365 cross-references** in Services Guide Ch 1B and the Sellers Guide value-prop sections.
- Industry-specific schema claims (SCML, MERML, EHRML, etc.) — these are APEX framework artifacts, not Microsoft platform claims, so they are not on Microsoft Learn to validate against. They should be validated against the source schema definitions in the APEX repo instead.
- Pricing claims for F-SKU, Foundry, and Sentinel — these change frequently; recommend a dedicated FinOps pass against the current Azure Pricing Calculator before any client-facing release.

---

## 7. Bottom line

The trilogy's Microsoft-platform spine is **structurally sound**. The fixes are surgical — API versions, role names, one builder-API rename, a hosting-fabric clarification, and the new-DSPM-for-AI distinction. With the priority-1 through priority-5 edits applied, the Microsoft-platform content is ready for Account Team review. The additions in §4 are value-adds, not corrections — sequence them based on which Account Team conversations you are closest to.

— Keven
<!-- CFMP-V0.2-ADDENDUM -->

## CFMP v0.2 — APEX-M validation update (2026-05-23)

The APEX-M platform-validation matrix now includes a seventh Industry Pack: **Customer Focused Merchandise (CFMP) v0.2**, the first Pack organized around a customer-moment spine.

### What's validated as of Phase 1 live

- **Microsoft Agent Framework 1.6.0 (GA)** running gpt-5-mini against Azure OpenAI (Responses API, `api_version=v1`). Provider toggle to Anthropic verified in code.
- **apex_audit / apex_purview** vendored packages stamp a 14-field signed LedgerRow per `/agent/ask` and emit Atlas-shaped lineage edges (mcp→agent, agent→orchestration, orchestration→audit).
- **Azure Speech** (`en-US-AvaMultilingualNeural`) STT + TTS via `/agent/tts`.
- **Azure Container Apps** consumption-plan deployment (portal + orchestrator + ACR + cae-visionkit environment) in `rg-iot-visionkit` / `Global_RnD_Agentic_MERCH`.
- **PostgreSQL + pgvector** backing the 800-product MERML-aligned catalog with IVFFlat index and `+0.15` priced-row bias.
- **HITL consent gate** firing on cart-add ≥ $50 (configurable threshold).

### Proposed Interface #15 — Maps & Wayfinding

APEX-M binding: **Azure Maps Creator** (Indoor Maps + Wayfinding REST + Web SDK). Local `storemap.yaml` fallback active in `orchestrator/azure_maps.py` today; production activation on `DEMO_AZURE_MAPS_DATASET_ID` + key.

### Companion artifacts

- `docs/packs/CFMP-v0.2.md` — Pack design document
- `docs/packs/CFMP-Scenario-Chains-v0.2.xlsx` — 18-scenario workbook
- `docs/packs/APEX-Architecture-v5.1-with-CFMP-chapter.docx` — parent arch doc with new Chapter 26
- Live demo: <https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture>

<!-- /CFMP-V0.2-ADDENDUM -->
