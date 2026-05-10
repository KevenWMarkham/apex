# ADR-003 · APEX audit row schema vs Purview Audit schema

**Status:** Accepted
**Date:** 2026-05-09
**Resolves:** Open question H.3 from the [Microsoft platform alignment delta](../../plans/2026-05-09-microsoft-platform-alignment-delta.md#h-things-to-validate-open-questions)

## Context

Roadmap.md BL.P.77 ships a **14-field APEX audit row** with HMAC signing, content-addressed input/output hashes, three-version stamps (manifest / policy / prompt), and downstream-effect cross-references. APEX-M Deployment Guide §11 designed it as the system-of-record for every agent decision.

Microsoft Purview Audit captures every AI interaction natively at the platform layer (per [Purview AI Agent 365 docs](https://learn.microsoft.com/purview/ai-agent-365)) including agent-to-human, human-to-agent, agent-to-tools, and agent-to-agent flows.

Two systems of record for the same data is not OK.

## Decision

**Microsoft Purview Audit becomes the system of record. APEX audit row demotes to a KPI-attribution overlay.**

Concretely:

1. Every APEX-M agent decision **writes to Microsoft Purview Audit first** via the platform-managed Purview pipeline (the Foundry hosted-agent runtime emits the audit event automatically; no APEX code path needed). Purview retention + WORM contract + signed delivery are Microsoft's responsibility.

2. APEX-M's overlay row in Fabric SQL ledger table writes **second**, after Purview emits. The overlay row carries:
   - `decision_ledger_id` (foreign key to Purview Audit's event id)
   - `service_code`, `scenario_id`, `agent_id` (APEX-scoped fields not in Purview's native schema)
   - KPI-attribution joins (`g_markdown_outcome_attribution` consumes this overlay; Purview Audit doesn't model service-code attribution natively)
   - The 14 APEX-specific fields stay, but **only as overlay context** — they are not the immutable record.

3. The `apex-m.audit_purview.AuditLedgerPurview` impl has `is_primary=True`. The `AuditLedgerFabricOverlay` impl has `is_primary=False`. Per the APEX-Core protocol contract, downstream consumers prefer the primary; the overlay is for KPI work only.

4. **HMAC signing of the overlay** (per Roadmap.md BL.P.84) stays — it's still the right WORM protection for the overlay row — but it is no longer the audit defense. Purview Audit's tamper protection is.

## Consequences

- **Compliance posture improves.** Microsoft Purview Audit + DSPM for AI is the canonical Microsoft compliance surface; SEC + regulatory audit teams already understand it. APEX's bespoke 14-field schema was an audit defensibility risk because it wasn't anchored in a recognized control.
- **Implementation simplifies.** APEX no longer needs to maintain the WORM contract on its own (signing key rotation, immutability proofs, retention enforcement) for the system-of-record path. Purview owns those.
- **Existing apex-audit package stays.** It moves from "system of record" to "KPI attribution overlay" — the same code, scoped down. Roadmap.md BL.P.77–84 entries update to reflect.
- **No data migration cost.** Existing Lab tenants haven't been deployed; the demotion is paper-only at this point.

## Status

Accepted. APEX-M concrete impl already in place at `apex-m/src/apex_m/audit_purview.py` per Phase I.3. APEX-M Deployment Guide §11 update + Roadmap.md amendment are a Phase I.3 follow-up sprint.
