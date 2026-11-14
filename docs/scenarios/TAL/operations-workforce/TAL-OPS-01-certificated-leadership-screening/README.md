# Certificated leadership screening

**Practice:** TAL — Talent (draft edition)
**Scenario index:** 01 of 1 (draft)
**Edition:** [APEX · Talent Edition](../../../../../apex-tal/README.md)

## Scenario
District personnel offices screen certificated leadership applicants (assistant principals, principals) by hand. A reviewer reads a 6-to-15-document packet, checks required qualifications against the board-approved posting, scores a weighted rubric and writes a recommendation. Evidence is rarely cited, conflicts between documents are easy to miss, and the same rubric is applied unevenly across applicants.

## Solution
Assess, Score and Compose agents read the tokenized packet, check required qualifications (met / verify / not met), build an evidence ledger with sources, flag cross-document conflicts, propose rubric ratings with cited evidence, and draft interview questions from the gaps. The screening committee decides at the step-16 HITL gate; Advance stays locked while qualifications are unverified or material findings are open. Every rating, override and decision is written to the hash-chained ledger.

## Use Case
High School Assistant Principal screening against a 100-point, 8-criterion district rubric. Reads `TALML.POSTING_REQUIREMENT`, `TALML.CREDENTIAL`, `TALML.EMPLOYMENT_RECORD`, `EVDML.SOURCE_DOCUMENT`. Writes `EVDML.EVIDENCE_CLAIM`, `EVDML.CONSISTENCY_FINDING`, `EVDML.QUALIFICATION_CHECK`, `SELML.RUBRIC_SCORE`, `SELML.SCREENING_DECISION`.

## Service
TAL-Ops-01 Certificated Screening. Wave 2 for one posting family; Wave 3 across every posting, fused with onboarding and credential renewal.

## Persona
Primary: HR analyst, Personnel Services. Prepares the packet review and verifies flagged items.
Approver: Screening committee. Decides at the HITL gate.

## KPI
Reference figures to validate in pilot (synthetic, not client claims): reviewer effort per packet ~3.5 h → ~30 min · 100% of criteria with cited evidence · 100% of applicants scored against the same rubric.

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

| Wave | Steps | Talent specialization |
|---|---|---|
| W1 | 1–10 | Application export as SOR · PII tokenizer · `TALML`/`EVDML` Silver · posting library, rubric and credential lookup over MCP · committee identities in Entra · ledger · committee card in Teams |
| W2 | 11–18 | Application submitted → orchestrator → Assess → Score → Compose → **HITL gate (16)** → draft action + evidence-write → KPI rollup |
| W3 | 19–24 | Every posting and applicant · fuse with onboarding and credential renewal · HR + position control · Purview lineage and retention · calibrate rubric against hire outcomes · time-to-fill and leader retention |

## Artifacts in this folder

- `artifacts/TAL-OPS-01-demo.html` — interactive demo of the W2 pilot run, the HITL gate and the ledger. All people, district and school names are fictional.
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Edition: [../../../../../apex-tal/README.md](../../../../../apex-tal/README.md)
- Edition manifest: [../../../../../apex-tal/data/schemas.manifest.json](../../../../../apex-tal/data/schemas.manifest.json)
- Practice overview: [../../README.md](../../README.md)
