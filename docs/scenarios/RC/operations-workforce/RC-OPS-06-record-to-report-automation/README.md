# Record-to-report (R2R) close automation

**Practice:** RC — Retail & Consumer
**Scenario index:** RC-OPS-06 (featured promotion candidate)
**Reference client (Wave 1):** **Nike, Inc.** — currently building
**Source:** APEX-Stacked-Architecture-Narrated.html

> **Status: BUILDING FOR NIKE.**
> Nike is the flagship reference deployment for the R2R close-automation scenario under the RC (Retail & Consumer) practice. AXLE is reserved for automotive manufacturers, so retail/consumer R2R work — including Nike's multi-entity close — lives here in RC.

## Scenario
Multi-entity month-end and quarter-end close for a global consumer brand with DTC, wholesale, licensing, and digital channels. Controllers spend the first 4–6 business days of close in spreadsheet reconciliation, intercompany matching, FX revaluation, and journal posting before any analytical work begins. Audit trail is fragmented across ERP, consolidation, and e-mail approvals — materially increasing SOX evidence collection effort and restatement risk.

## Solution
Close-orchestration agent fleet that (1) ingests sub-ledger balances from SAP S/4HANA + peripheral systems, (2) runs intercompany matching + FX revaluation + accrual proposals as parallel agents, (3) proposes journal entries with confidence score, (4) routes above-threshold entries through HITL via Teams Adaptive Card, and (5) writes every decision to the 14-field APEX audit row for SOX evidence. Commercial envelope gates any proposal >$ threshold to a Controller approval path.

## Use Case
**Close-day-1-to-close-day-4 automation.** Reads `FINML.SubLedger`, `FINML.IntercoMatch`, `FINML.FXRate`, `FINML.JournalProposal`, `SOXML.AuditEvidence`. Parent orchestration composes 6 agents: Balance-Fetch, Intercompany-Match, FX-Reval, Accrual-Propose, JE-Compose, Evidence-Write. Wave 2 pilot scope = one legal entity (Nike USA DTC), Wave 3 = global rollout across all entities and brands (Nike Brand, Converse, Jordan).

## Service
**RC-E2E-06 Finance Close Automation** + **RC-E2E-11 Controls & Audit Evidence**. Commercial envelope gated by entity materiality tier. Wave 2 at single-entity pilot with ~15 controllers; Wave 3 enterprise close across ~40 entities and 3 consolidation layers.

## Persona
**Primary:** Deirdre Chen · Corporate Controller
Approves above-threshold journal entries and intercompany true-ups via Teams Adaptive Card; every approval writes to audit row with actor, timestamp, entry ID, supporting-evidence links, and confidence score.

**Secondary:** Marcus Okafor · SOX Program Lead
Reviews control-exception feed and audit-row sampling; exports SOX-quarter evidence packet directly from LEDGER without manual collation.

## KPI
- Close cycle: **day 6 → day 3** (−50% elapsed time)
- Controller hours reclaimed: **+22 hrs / controller / close**
- Manual journal entries: **−65%** (auto-proposed + HITL-approved)
- SOX evidence collation: **4 weeks → 3 days** per quarter
- Restatement risk: all material entries audit-row attributed (§16.13 reference deployment)

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

**W1 — Foundation (Nike, now → Q2 FY26)**
- SAP S/4HANA connector + balance-fetch agent
- Intercompany-match agent (single-entity scope)
- APEX audit-row wiring to LEDGER plane
- HITL Teams Adaptive Card for JE approval

**W2 — Pilot (Nike USA DTC entity, Q3 FY26)**
- FX-reval + accrual-propose agents live
- Full 6-agent orchestration on one entity's monthly close
- SOX evidence export (pilot quarter)
- Commercial envelope tuning per materiality tier

**W3 — Scale & Fuse (Nike global, Q1–Q2 FY27)**
- Rollout across ~40 entities (Nike Brand, Converse, Jordan, regional holdcos)
- Consolidation-layer orchestration (local GAAP → US GAAP)
- Fusion with MERML pricing data for revenue-recognition corner cases (discounts, returns, licensing)
- Multi-currency, multi-GAAP close at enterprise scale

## Why this scenario belongs in RC (not AXLE)

Nike is a **retail & consumer** company — apparel, footwear, DTC, wholesale. AXLE is reserved for **automotive OEMs and tier-1 suppliers**. Any retail/consumer R2R work — including the Nike build — is scoped under **RC**. R2R patterns do port across industries (finance close is universal), but the reference implementation, sub-ledger shapes, persona set (Corporate Controller, Brand Finance), and commercial envelope tuning are all retail/consumer-specific.

Cross-Practice notes:
- **AXLE** will want its own R2R scenario (AXLE-OPS-NN) tuned for OEM multi-plant cost-accounting + warranty accruals — not this one.
- **HLS** R2R will handle 340B drug-pricing accruals + DSH reconciliation — its own scenario.
- **ER** R2R handles commodity hedge accounting + revenue recognition at delivery — its own scenario.

## Artifacts to land in this folder

- `APEX-R2R-build-guide.md` — step-by-step build for Nike Wave 1
- `APEX-R2R-walkthrough.docx` — narrative walkthrough for sellers (retail/consumer framing)
- `APEX-R2R-nike-reference.md` — Nike-specific deployment notes (entities, channels, GAAP mix)
- `tests/` — pytest fixtures with synthetic sub-ledger data; Testcontainers Postgres for schema validation
- `artifacts/` — close-calendar diagrams, JE-proposal screenshots, Adaptive Card mockups, sample audit-row JSON
- `manifests/` — agent manifests for Balance-Fetch, Intercompany-Match, FX-Reval, Accrual-Propose, JE-Compose, Evidence-Write; parent orchestration manifest; policy manifest (materiality thresholds)

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Nike account folder (reference client): `C:\Stage\Clients\Industries\Consumer\Brands-Lifestyle\Nike\01_account\`
- Narrated architecture: [../../../reference/APEX-Stacked-Architecture-Narrated.html](../../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../../APEX%20-%20Design%20and%20Build/APEX_Design.md](../../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
- APEX Sellers Guide (Runtime Plane, LEDGER feedback loop): [../../../book/Professional-APEX-Sellers-Guide.html](../../../book/Professional-APEX-Sellers-Guide.html)
