# ADR-004 · Foundry region coverage vs client target regions

**Status:** Accepted
**Date:** 2026-05-09
**Resolves:** Open question H.4 from the [Microsoft platform alignment delta](../../plans/2026-05-09-microsoft-platform-alignment-delta.md#h-things-to-validate-open-questions)

## Context

Microsoft Foundry Agent Service has documented region constraints, particularly for features like "Grounding with Bing Search" which is only supported in a defined list of regions. Some Deloitte client tenants will require deployment in regions outside that list — typically EU regulated (Switzerland, France, Germany), Middle East, India, or specific Australia regions for data-residency reasons.

Question: How does APEX-M handle clients whose target region isn't in Foundry's supported list?

## Decision

**Three-tier handling, decided per-engagement at the Pre-deployment Security Gate:**

### Tier 1 — Foundry-supported region (recommended)
The client's target region is in Foundry's [supported region list](https://learn.microsoft.com/azure/foundry/agents/concepts/limits-quotas-regions). Default APEX-M deployment, no special handling. Standard Setup with Private Networking applies.

### Tier 2 — Foundry-supported but feature-constrained
The client's target region supports Foundry hosted agents but not specific features (e.g., Bing grounding, certain models). APEX-M deploys with feature-aware fallbacks:
- If Bing grounding unavailable → use Azure AI Search RAG over the client's existing knowledge bases (no Internet grounding)
- If a specific model unavailable in-region → fall back to gpt-4o-mini or the closest in-region model; document the fallback in the use-case YAML's `agent_overrides[*].model` field

### Tier 3 — Region not Foundry-supported
The client's target region doesn't support Foundry Agent Service. Two paths:
- **Path A**: deploy APEX-M agents on plain Container Apps in the client's region (the same fallback as ADR-001 for ACR public-egress). Lose Foundry's managed threading + content safety; reimplement in agent code.
- **Path B**: split the deployment — agents run in a Foundry-supported region (proxy) while data + identity stay in the client's region. Cross-region traffic routed via private endpoints + ExpressRoute; data residency satisfied because data never leaves the client's region.

Choose Path A or B at the engagement level based on the client's data-residency policy. Path A is simpler; Path B keeps Foundry's full feature set.

## Decision matrix

| Client target region | Foundry support | Recommended path |
|---|---|---|
| US East / US West / North Europe / West Europe / UK South / Australia East / Japan East / Canada Central | Full | Tier 1 — default |
| Switzerland North / France Central / Germany West Central / Norway East / Sweden Central / South Africa North / Italy North / Brazil South / UAE North / Korea Central / Spain Central / Poland Central / India South | Most features (some constraints) | Tier 2 — feature-aware fallback |
| China / sovereign cloud / Government region | Limited or absent | Tier 3 Path A or B per engagement |

The list is informational and Microsoft updates it; verify at engagement time via the Foundry portal or `az cognitiveservices account list-kinds`.

## Consequences

- **Pre-deployment Security Gate** adds a region-check step: the wizard validates the target region against Foundry's current supported list at gate-evaluation time.
- **APEX-M Bicep platform module** accepts a `foundryFallbackToContainerApps: bool` parameter that flips the runtime to Container Apps when set. Wizard sets this automatically based on region check.
- **Per-engagement documentation**: every Tier 2 / Tier 3 deployment records the fallback choice in the engagement's audit trail with the Microsoft Learn region-list snapshot at the time.

## Status

Accepted. Region check + fallback Bicep param land in a Phase I.4 follow-up sprint; documented now so engagements can plan around the constraint.
