# ADR-005 · APEX T1–T4 classification ↔ Purview sensitivity-label mapping

**Status:** Accepted
**Date:** 2026-05-09
**Resolves:** Open question H.5 from the [Microsoft platform alignment delta](../../plans/2026-05-09-microsoft-platform-alignment-delta.md#h-things-to-validate-open-questions)

## Context

APEX uses a 4-tier classification model (T1–T4) defined in the Deployment Guide. Microsoft Purview Information Protection uses sensitivity labels with a customer-defined taxonomy — but the canonical Microsoft baseline is *Public / Internal / Confidential / Highly Confidential / Strictly Confidential* (5-level).

Question: how do APEX tiers map to Purview labels? Are they 1:1?

## Decision

**APEX T1–T4 maps cleanly to the standard Purview taxonomy with a defined collapse rule.**

| APEX tier | Purview standard label | Notes |
|---|---|---|
| **T1 — Public** | Public | Identical. No encryption. |
| **T2 — Internal** | Internal | Identical. No encryption. |
| **T3 — Confidential** | Confidential | PII / PCI. Encryption. EXTRACT usage right required for Foundry RAG. |
| **T4 — Highly Confidential** | Highly Confidential **OR** Strictly Confidential | PHI / regulated. Encryption. EXTRACT required. **The collapse rule below disambiguates.** |

### Collapse rule for T4 ↔ "Highly" vs "Strictly"

When a client's Purview taxonomy distinguishes Highly Confidential from Strictly Confidential, APEX T4 maps to whichever tier requires **dual control** (two-person approval) for unwrap. By Microsoft's typical guidance:

- **Highly Confidential** = encryption + EXTRACT-only access + audit
- **Strictly Confidential** = the above + dual-control unwrap + tighter retention

APEX T4 implies dual-control HITL (per Deployment Guide ch 9). Therefore:
- Tenant has 4-tier Purview taxonomy → APEX T4 = Highly Confidential
- Tenant has 5-tier Purview taxonomy with both Highly + Strictly → APEX T4 = **Strictly Confidential** (because of the dual-control implication)

The mapping is configurable per tenant in `apex-m/src/apex_m/classifier_purview.py` via the `label_map` constructor argument.

## Bidirectional propagation

The `SensitivityClassifierPurview` impl propagates labels in both directions:

- **APEX → Purview**: When APEX classifies an entity at T3, the Foundry agent emits the Purview "Confidential" label on outputs. M365 Copilot, Foundry RAG, and Azure AI Search all honor it.
- **Purview → APEX**: When APEX reads a Purview-labeled item from a SharePoint connector or Foundry RAG, the impl maps the Purview label back to APEX tier so APEX-internal policy stays consistent.

The reverse mapping is what closes the loop documented in Phase I.3 (Purview becomes the system of record for sensitivity classification; APEX honors not redefines).

## Engagement-time configuration

At each engagement:

1. Operator runs `apex_m.classifier_purview.SensitivityClassifierPurview.get_label_inventory()` against the client's tenant
2. If the client's Purview taxonomy differs from the default (e.g., uses 6 labels with a "Top Secret" tier above Strictly), operator overrides the `label_map` constructor argument
3. The override lands in the use case YAML's `agent_overrides` block so the wizard's render endpoint emits a service-specific environment variable

## Consequences

- **No data migration needed.** Labels are applied at write time + at agent-output time; existing Silver / Gold data stays untouched.
- **Wizard validation** at the Pre-deployment Security Gate (item #4) verifies the client's Purview taxonomy is reachable and the mapping resolves; gate red if unreachable.
- **APEX-G and APEX-A get analogous decisions.** APEX-G maps to Cloud DLP info-types; APEX-A maps to Macie classifications. Each variant ADR drafts equivalent collapse rules at port time.

## Status

Accepted. Default mapping live in `apex-m/src/apex_m/classifier_purview.py`. Per-tenant override mechanism added in a Phase I.3 follow-up sprint.
