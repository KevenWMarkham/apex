# APEX · Talent Edition

Industry edition of the APEX framework for talent acquisition and workforce selection, starting with K-12 certificated leadership hiring. Inherits from APEX Core v1.2.

**Edition code:** TAL
**Status:** Draft (manifest 0.1.0). Promote to 1.0.0 through the HITL gate before any account pins it.
**Inheritance declaration:** This edition conforms to APEX Core v1.2.
**Manifest:** `apex-tal/data/schemas.manifest.json` — conforms to the Core v1.2 schema-manifest contract.
**First scenario:** [`TAL-OPS-01` · Certificated leadership screening](../docs/scenarios/TAL/operations-workforce/TAL-OPS-01-certificated-leadership-screening/)

Validate the manifest with `npm run validate -- apex-tal` (or `node apex-core/tools/apex-validate.js apex-tal`).

## Canonical schemas

| Code | Domain | Entities | Purpose |
|---|---|---|---|
| `TALML` | Talent Acquisition | 6 | Postings and requirements, tokenized applicants, applications, credentials, employment history |
| `EVDML` | Screening Evidence | 4 | Source documents, claims with sources, cross-document findings, qualification checks |
| `SELML` | Selection Decisions | 4 | Weighted rubric criteria, proposed and final scores, the committee decision, screening KPIs |

## How the edition specializes the 24-step chain

The backbone stays fixed at 24 steps with one HITL gate at step 16. The edition supplies:

| Step | Canonical | Talent specialization |
|---|---|---|
| 1 | SOR | Application export (e.g. EDJOIN) and the HR system of record |
| 4 | Tokenizer / PII | Applicant names, contacts, DOB and credential numbers tokenized before any agent reads a packet |
| 5 | Silver canonical | `TALML` + `EVDML` |
| 7 | MCP | Posting library, district rubric, state credential lookup |
| 10 | HITL surface | AI-Services Cairn as the front door: voice, Teams and the office console over one tool layer, with a confirm gate and server re-check on every governed tool |
| 13–15 | Agents | Assess (gate, evidence, conflicts) → Score (weighted rubric) → Compose (interview and reference plan) |
| 16 | HITL gate | Screening committee decision. Advance stays locked while required qualifications are unverified or material findings are open |
| 17 | Act + evidence-write | Draft invitation, clarification request or regret notice; people send it |
| 18 | KPI rollup | `SELML.SCREENING_KPI` |

## Guardrails

- Agents draft; people decide and send. No decision leaves step 16 without a named approver.
- Missing proof is recorded as **verify**, never as **not met**.
- Only job-related information is screened. No medical, family or other protected details are sought or inferred.
- Every rating cites its evidence, and every reviewer override is logged.

## Open questions before 1.0.0

1. Practice placement: no public-sector or education practice exists in the scenario library yet. `TAL` sits beside the industry practices for now.
2. PII classes `DOB` and `GOV_ID` are new to the repo's vocabulary (existing: `CUSTOMER_ID`, `CONTACT`, `PII-DIRECT`). Confirm with Core maintainers.
3. Whether `EVDML` should stay its own schema or fold into `TALML`. Folding it would drop the edition below the 3-schema minimum.
