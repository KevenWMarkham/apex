# ADR-001 · Foundry hosted-agent ACR public-reachability constraint

**Status:** Accepted
**Date:** 2026-05-09
**Resolves:** Open question H.1 from [`microsoft-platform-alignment-delta.md`](../../plans/2026-05-09-microsoft-platform-alignment-delta.md#h-things-to-validate-open-questions)

## Context

Microsoft Foundry Agent Service's Standard Setup with Private Networking has a documented limitation as of GA April 2026:

> *"Hosted agent container registry behind a private network: For hosted agents, the Azure Container Registry (ACR) that stores the agent's container image can't currently be placed behind a private network (private endpoint with public network access disabled). The ACR must be reachable over its public endpoint for the platform to pull the image."*

— [Microsoft Learn — Foundry Agent Service private networking limitations](https://learn.microsoft.com/azure/foundry/agents/how-to/virtual-networks#limitations)

This conflicts with Deloitte client tenants where the CISO chain mandates **no public egress** at any layer of the platform — including container registries.

## Decision

For **Stage / Prod tenants where the client mandates no-public-egress ACR**:

1. **Bypass Foundry hosted-agent runtime.** Deploy the agents as plain `Microsoft.App/containerApps` instead — Container Apps supports private ACR with private endpoints fully (per Microsoft Learn — [Container Apps + private ACR](https://learn.microsoft.com/azure/container-apps/networking)).
2. **Lose Foundry's managed threading + content safety.** Re-implement those concerns inside the agent code using Azure AI Content Safety + Cosmos for thread state. APEX-M's `ThreatProtectionDefender` impl wraps the same Content Safety Prompt Shields surface; the threading state model is documented in Phase I.3 follow-up work.
3. **Mark the deployment** with `apex-m-fallback-no-foundry-hosted: true` in resource tags so drift detection flags it for re-evaluation when Microsoft removes the ACR limitation.

For **all other Stage / Prod tenants** — the ACR limitation is acceptable: ACR has its own RBAC + network ACL controls; pulling images over its public endpoint is not the same as the Foundry agents themselves having public network egress (those run inside the delegated subnet).

## Consequences

- **Maintainability cost.** Two deployment paths (Foundry hosted vs Container Apps) mean two sets of Bicep modules. We accept this until Microsoft closes the gap.
- **Watch this space.** Track the Microsoft Learn article quarterly; when the limitation lifts, migrate fallback tenants back to Foundry hosted in their next major upgrade window.
- **Engagement signal.** Catch the ACR-public-egress conflict during Pre-deployment Security Gate item #13 (Standard Setup with Private Networking). The gate's verifier checks the client's ACR network policy and surfaces this fallback path automatically when no-public-egress is required.

## Status

Accepted. Fallback path scaffolded in Phase I.4 Bicep (provisional `provisionFoundry: false` switch in `apex-m/infra/bicep/platform/main.bicep`) — operator picks at platform deploy time. Re-evaluate ADR when Microsoft removes the limitation.
