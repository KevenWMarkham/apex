# APEX Deep Dive — Record-to-Report (R2R) Close Automation

**Scenario ID:** `RC-OPS-06-record-to-report-automation`
**Practice:** RC — Retail & Consumer
**Reference client (Wave 1):** Nike, Inc.
**Status:** Building — Wave 1 Foundation
**Document type:** Deep-dive build & sell guide
**Owner:** APEX — Design & Build

---

## 0. TL;DR

Month-end and quarter-end close at a global consumer brand is a 6–8 business-day sprint that consumes the first week of every period in reconciliation, intercompany matching, FX revaluation, and journal posting — before any analytical work starts. APEX collapses the mechanical portion of close to **Day 1–Day 3** by running a fleet of six purpose-built finance agents in parallel, proposing journal entries with a confidence score, and routing anything above a materiality threshold through a Human-in-the-Loop (HITL) approval via Microsoft Teams Adaptive Card. Every proposed entry, every approval, every override is written to the 14-field APEX audit row so the SOX evidence packet is generated — not collated — at quarter-end.

Target outcomes (Wave 3, Nike global):

- Close cycle **Day 6 → Day 3** (−50% elapsed)
- **+22 hrs / controller / close** reclaimed for analytical work
- **−65%** manual journal entries
- SOX evidence collation **4 weeks → 3 days** per quarter
- 100% of material entries audit-row attributed (§16.13 reference deployment)

---

## 1. Why This Scenario

### 1.1 Current-state pain

Close for a global public-company consumer brand is not one process — it is a chain of ~30 handoffs across ~40 legal entities, 3 brands (Nike Brand, Converse, Jordan), and 4 channels (DTC, Wholesale, Licensing, Digital). The first 4–6 business days of every period are spent on mechanical work that an agent can do as well or better than a human:

| Close day | What humans do today | Mechanical? |
|-----------|----------------------|-------------|
| **Day 1** | Pull sub-ledger balances, run trial balance | Yes |
| **Day 2** | Intercompany matching (IC AR ↔ IC AP reconciliation) | Yes |
| **Day 2–3** | FX revaluation per entity | Yes |
| **Day 3** | Accrual proposals (payroll, rebates, incentives, returns) | Mostly |
| **Day 3–4** | Journal entry composition + posting | Yes (mechanics) |
| **Day 4–5** | Consolidation (local GAAP → US GAAP) | Yes (mechanics) |
| **Day 5–6** | Flux/variance analysis — the actual accounting judgment | **No, keep with humans** |

The insight: everything on Day 1–4 is rule-governed mechanical work with audit trail requirements. That's exactly what APEX orchestration is for. Day 5–6 flux/variance analysis stays with the Controllers — with **more time to do it well**, because the prep work is done.

### 1.2 Why now

Three converging pressures make R2R a priority for consumer brands in FY26:

1. **SOX evidence cost is escalating.** Audit fees at large consumer brands are up double-digits YoY; manual evidence collation is the single biggest driver.
2. **Finance talent scarcity.** Controller headcount is flat or shrinking while transaction volume keeps growing (DTC expansion, international e-comm, licensing complexity).
3. **Close-cycle expectations are tightening.** Public company investors expect faster guidance updates; retail-specific revenue-recognition challenges (discounts, returns, markdowns) keep the close hard.

---

## 2. Target-State Architecture

### 2.1 Agent fleet

Six agents compose the R2R orchestration. Each owns a bounded domain, has its own manifest, and emits to the audit row.

```
┌─────────────────────────────────────────────────────────────────┐
│                   Parent: R2R Close Orchestrator                │
│                   (pattern: hierarchical + parallel)            │
└───────┬─────────────────────────────────────────────────┬───────┘
        │                                                 │
  ┌─────▼─────┐                                     ┌─────▼─────┐
  │ Balance-  │◄── SAP S/4HANA, sub-ledgers         │ Evidence- │──► LEDGER
  │  Fetch    │                                     │  Write    │    (SOX)
  └─────┬─────┘                                     └─────▲─────┘
        │                                                 │
        ├──► Interco-Match  ──┐                           │
        │    (parallel)       │                           │
        │                     │                           │
        ├──► FX-Reval ────────┼──► JE-Compose ────────────┤
        │    (parallel)       │    (HITL if >threshold)   │
        │                     │                           │
        └──► Accrual-Propose ─┘                           │
             (parallel)                                   │
```

| Agent | Responsibility | Input | Output | HITL? |
|-------|----------------|-------|--------|-------|
| **Balance-Fetch** | Pull sub-ledger balances at cutoff; normalize to FINML | SAP S/4HANA, peripheral sub-ledgers | `FINML.SubLedger` | No |
| **Interco-Match** | Match IC AR ↔ IC AP across entities; propose true-ups for mismatches | `FINML.SubLedger` per entity pair | `FINML.IntercoMatch`, JE proposals | If true-up > threshold |
| **FX-Reval** | Revalue monetary positions at period-end rates; propose unrealized gain/loss | `FINML.SubLedger`, `FINML.FXRate` | JE proposals | Rarely (rate source is authoritative) |
| **Accrual-Propose** | Propose accruals (payroll, rebates, returns, licensing royalties) using historical pattern + driver data | `FINML.SubLedger`, `FINML.DriverData` | JE proposals with confidence score | If confidence < 0.9 OR amount > threshold |
| **JE-Compose** | Compose the actual journal entry — accounts, dimensions, narrative, supporting-doc links | All proposals from above | Posted or pending JEs | **Always HITL for material entries** |
| **Evidence-Write** | Write decision record to audit row; assemble SOX evidence packet | Every action from every agent | `SOXML.AuditEvidence` | No |

### 2.2 Orchestration pattern

Pattern: **hierarchical with parallel fan-out** (see archetype catalog — this is a composition of archetypes `hierarchical-root` + `parallel-fanout-gather` + `hitl-gated-commit`).

- **Parallel phase (Close Day 1–2):** Balance-Fetch completes first (sequential prerequisite). Then Interco-Match, FX-Reval, and Accrual-Propose run in parallel across entities.
- **Serial phase (Close Day 2–3):** JE-Compose gathers all proposals, applies materiality filter, routes material entries through HITL, auto-posts non-material entries, writes everything to LEDGER.
- **Consolidation phase (Close Day 3):** Same orchestration re-runs one level up at consolidation layer (local GAAP → US GAAP).

### 2.3 Commercial envelope

The commercial envelope is the policy layer that decides "do this automatically vs. require human approval." For R2R, the envelope is tiered by **entity materiality × entry amount × confidence**:

| Entity tier | Amount | Confidence | Action |
|-------------|--------|------------|--------|
| Tier 1 (material) | Any | Any | Always HITL |
| Tier 2 (standard) | > $250K | Any | HITL |
| Tier 2 (standard) | ≤ $250K | ≥ 0.95 | Auto-post, notify |
| Tier 2 (standard) | ≤ $250K | < 0.95 | HITL |
| Tier 3 (immaterial) | ≤ $50K | ≥ 0.90 | Auto-post, log only |
| Any | Intercompany true-up > $100K | Any | Always HITL (both entities) |

Thresholds are Practice-level defaults; each tenant tunes in their manifest.

### 2.4 HITL experience

The Controller does **not** log into another tool. Adaptive Cards arrive in Teams with:

- Proposed JE (accounts, dimensions, amounts, narrative)
- Confidence score + the specific evidence the agent used
- One-click **Approve** / **Reject** / **Modify** buttons
- Optional comment field (free-text → audit row)

Approval writes to the audit row with actor, timestamp, entry ID, confidence at time of decision, and any modifications. No separate approval workflow tool needed.

---

## 3. Data Contracts (FINML / SOXML)

R2R uses two dialects of the APEX data contract language:

### 3.1 FINML — Finance shapes

```
FINML.SubLedger
  entity_id, account, dimension{cost_center, channel, brand, region},
  amount, currency, posting_date, doc_ref, source_system

FINML.IntercoMatch
  pair{entity_a, entity_b}, ar_row, ap_row, diff_amount, diff_currency,
  match_status{matched, unmatched, partial}, proposed_trueup

FINML.FXRate
  currency_from, currency_to, rate_type{spot, period_avg, period_end},
  rate_date, rate_value, source{ECB, Bloomberg, internal}

FINML.JournalProposal
  proposer_agent, entity_id, lines[{account, dim, debit, credit}],
  narrative, supporting_docs[uri], confidence, materiality_tier
```

### 3.2 SOXML — Audit evidence shapes

```
SOXML.AuditEvidence
  decision_id, scenario_id, agent_id, actor{human|agent}, actor_id,
  action, timestamp, entity_id, amount, currency,
  confidence, policy_applied, evidence_refs[uri],
  override_reason?, prior_decision_ref?
```

This maps directly onto the **14-field APEX audit row** defined in the APEX Design spec, with `scenario_id = RC-OPS-06-record-to-report-automation` for every R2R-origin row.

---

## 4. Nike-Specific Implementation Notes

### 4.1 Entity landscape

Nike's corporate structure matters for R2R orchestration scoping:

- **Brand holding:** Nike, Inc. (NKE)
- **Sub-brands:** Nike Brand, Converse, Jordan Brand — each with its own P&L
- **Regional operating entities:** NA, EMEA, Greater China, APLA (Asia-Pacific & Latin America)
- **~40 legal entities** across manufacturing sourcing, IP holding, DTC operating companies, wholesale subsidiaries
- **Reporting currency:** USD; **functional currencies:** USD, EUR, GBP, CNY, JPY, BRL, MXN, AUD, and more

### 4.2 Channel-specific close quirks

Different channels produce different revenue-recognition patterns that R2R agents must handle:

| Channel | Recognition pattern | Agent implication |
|---------|---------------------|-------------------|
| **DTC (Nike.com, Nike Direct stores)** | Point-of-sale, returns reserve, loyalty liability | Accrual-Propose must model returns + loyalty deferrals |
| **Wholesale (Foot Locker, Dick's, etc.)** | Shipment vs. arrival (Incoterms-dependent), markdown allowances | JE-Compose must honor contractual markdown credits |
| **Licensing** | Royalty-on-sales with minimum guarantees | Accrual-Propose uses licensee self-reporting + true-up pattern |
| **Digital (apps, SNKRS)** | Subscription vs. transactional, gift card liability | Separate deferred-revenue treatment |

### 4.3 Source systems

- **Primary ERP:** SAP S/4HANA (Nike has been consolidating onto S/4)
- **Peripheral:** channel-specific POS/e-comm platforms, licensing management system, treasury for FX
- **Consolidation layer:** SAP S/4HANA Group Reporting or BPC-equivalent
- **Audit working papers:** currently Excel + SharePoint; target state = APEX LEDGER SOX export

### 4.4 Wave-1 scope for Nike

**Scope:** One entity (Nike USA DTC), monthly close, 3 agents live (Balance-Fetch, Interco-Match, Evidence-Write).
**Out of scope for W1:** Consolidation layer, quarterly 10-Q evidence packet, licensing royalty accruals.
**Success criterion:** Controller reports a subjective time reclamation of ≥ 8 hrs for the pilot close, and audit-row coverage is 100% on posted entries.

---

## 5. Controls & SOX Posture

### 5.1 What auditors need

External auditors need three things to sign off on a control:

1. **Design:** The control is defined and appropriate for the risk.
2. **Operation:** Evidence the control operated as designed during the period.
3. **Exception handling:** Evidence that exceptions were identified, routed, and resolved.

APEX R2R produces all three natively:

- **Design** = the agent manifest + policy manifest (versioned, diffable)
- **Operation** = every decision in the audit row with timestamp + actor
- **Exception handling** = HITL override reasons + re-decision links in the audit row

### 5.2 SOX evidence packet (quarterly)

One artifact: `RC-OPS-06-sox-evidence-Q{n}-FY{yy}.zip`

Contains:
- Agent manifests as-of quarter-end (design evidence)
- Policy manifests as-of quarter-end
- Audit-row extract for the quarter (CSV + JSON)
- HITL approval log with Adaptive Card payloads
- Exception sampling worksheet (auto-prepared for auditor review)
- Reconciliation between posted JE count and audit-row count (tie-out)

Target: auditor can complete substantive testing in **days, not weeks**, because they are sampling from one canonical artifact instead of reconstructing it from email + Excel + screenshots.

---

## 6. ROI Model

### 6.1 Hours reclaimed

Assume Nike has ~150 controllers + assistant controllers touching close, 12 closes per year.

- **Today:** ~48 hrs per person per close spent on mechanical work (4 days × 12 hrs).
- **Target:** ~26 hrs per person per close (−22 hrs / person / close).
- **Total:** 150 × 22 × 12 = **~39,600 hrs/year reclaimed.**
- At blended $125/hr loaded cost = **~$4.95M/year in reclaimed capacity.**

That capacity converts to:
- More analytical close commentary (board-ready flux explanations)
- Faster response to ad-hoc CFO / investor-relations asks
- Reduced overtime during close weeks (retention + engagement)

### 6.2 SOX audit fee reduction

External audit fees at large consumer brands run $20M–$40M/year; the restatement-risk premium + evidence-hours line drives a meaningful fraction. APEX evidence packet target is a **10–15% fee reduction** by Wave 3 (supported by reduced evidence-collation hours on the audit side). At $30M baseline = **$3M–$4.5M/year fee avoidance.**

### 6.3 Close-day business value

Pulling earnings-release-ready numbers 3 days sooner has non-monetary value: faster guidance, faster executive decision cycles, reduced period-end stress. Not all of this monetizes but it does retain talent.

---

## 7. Wave Plan

### 7.1 W1 — Foundation (now → Q2 FY26)

**Target:** One entity (Nike USA DTC), 3 agents, monthly close.

Deliverables:
- `manifests/balance-fetch.yaml`
- `manifests/interco-match.yaml`
- `manifests/evidence-write.yaml`
- `manifests/r2r-orchestrator.yaml` (parent)
- `manifests/policy-materiality.yaml`
- SAP S/4HANA connector (read-only, pilot entity)
- Teams Adaptive Card for IC true-up approval
- Audit-row wiring end-to-end
- W1 exit review with Nike Corporate Controller

### 7.2 W2 — Pilot (Q3 FY26)

**Target:** Nike USA DTC entity, full 6-agent orchestration, monthly close × 3 cycles, one quarterly SOX packet.

Deliverables:
- FX-Reval + Accrual-Propose + JE-Compose live
- HITL flows for all materiality tiers
- Commercial envelope tuned to Nike's tier thresholds
- Pilot-quarter SOX evidence packet (Q3 FY26) reviewed by internal audit
- W2 exit: approval to scale

### 7.3 W3 — Scale & Fuse (Q1–Q2 FY27)

**Target:** All ~40 entities, all 3 brands, full consolidation layer, quarterly SOX for external audit.

Deliverables:
- Multi-entity orchestration (parallel at entity level)
- Consolidation-layer orchestration (local GAAP → US GAAP mapping)
- Multi-currency, multi-GAAP handling (IFRS local books + US GAAP consol)
- Fusion with MERML (pricing data) for returns + markdown + licensing edge cases
- External-audit walkthrough of evidence packet
- W3 exit: Controller org operating at steady state; hours reclaimed target validated

---

## 8. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Auditor rejects evidence packet format | Medium | High | Joint design session with external auditor in W1; anchor packet on SOC-2-adjacent patterns they already accept |
| Controllers resist HITL volume ("Teams noise") | Medium | Medium | Materiality thresholds aggressive; only 5–10% of entries should route to HITL by W2 steady-state; digest mode for low-priority notifications |
| SAP S/4HANA data quality gaps | Medium | Medium | Balance-Fetch validation layer; unknown/ambiguous balances route to a pre-close exception queue for Controller pre-clearing |
| Intercompany cross-entity timing mismatches | High | Medium | Interco-Match tolerates T+1 and T+2 timing diffs; flags only T+3 as exceptions |
| Confidence-score drift (model decay) | Low | High | LEDGER feedback loop re-scores accrual patterns quarterly; HITL override reasons become training signal |
| Independence concerns (Deloitte audits Nike?) | **Verify** | **Blocking if true** | Check Deloitte audit status; if audit client, engage Deloitte Digital / Advisory under appropriate independence framework — do not proceed assuming Consulting can lead |

### Independence call-out

Before selling this deeper at Nike, confirm Deloitte's independence posture. If Deloitte is Nike's external auditor, this work must be structured to preserve independence. The build is **client-software that Nike runs** — the agent manifests, policy manifests, and LEDGER are Nike artifacts; Deloitte's role is advisory and implementation enablement. Structure the statement of work accordingly and route through the independence office before contracting.

---

## 9. Cross-Practice Portability

R2R is the single most portable APEX scenario across Practices. The **orchestration pattern** (6-agent hierarchical + parallel + HITL-gated-commit) stays identical. What changes by Practice:

| Practice | Sub-ledger shapes | Accrual specialty | Persona |
|----------|-------------------|-------------------|---------|
| **RC (this)** | DTC + wholesale + licensing | Returns, rebates, markdowns, royalties | Corporate Controller, Brand Finance |
| **AXLE** | Plant cost accounting + warranty | Warranty accruals, sales incentives, dealer reserves | Plant Controller, Warranty Finance Director |
| **HLS** | Patient revenue + payor mix + 340B | 340B accruals, DSH reconciliation, payor true-ups | Hospital CFO, Revenue Integrity Director |
| **ER** | Commodity positions + hedges | MtM revaluation, hedge accounting, take-or-pay | Commodity Controller, Hedge Accounting Lead |
| **TMT** | Subscription + ad + licensing | Deferred revenue, content amortization, ad-return reserves | SaaS Controller, Revenue Accounting Lead |
| **TH** | Loyalty + deferred travel | Loyalty breakage, deferred voyage, cancellation reserves | Revenue Accounting Director |
| **ICE** | Project revenue + WIP | POC revenue, project-cost accruals, rebate reserves | Industrial Controller, Project Finance Lead |

The manifest library grows — but the orchestration graph is the same. That's the leverage of authoring R2R once under RC and extending it.

---

## 10. Next Steps

1. Validate Nike entity list and ERP state of play with Account Team (week of kickoff)
2. Joint design session on SOX evidence packet format with Nike Internal Audit + external auditor (W1)
3. Author W1 manifests (Balance-Fetch, Interco-Match, Evidence-Write, Parent, Policy)
4. Stand up pilot environment (read-only connector to one Nike USA DTC entity)
5. Shadow-run against a historical close to validate output before first live close
6. W1 exit review with Corporate Controller — gate to W2

---

## Appendix A — Linked artifacts (to be authored)

- `APEX-R2R-build-guide.md` — step-by-step build for W1 (target: Week 2 of project)
- `APEX-R2R-walkthrough.docx` — narrative walkthrough for sellers (retail/consumer framing)
- `APEX-R2R-nike-reference.md` — Nike-specific notes (entities, channels, GAAP mix)
- `manifests/*.yaml` — agent + orchestration + policy manifests
- `tests/test_balance_fetch.py`, `tests/test_interco_match.py`, etc. — pytest + Testcontainers harness
- `artifacts/close-calendar-current.png`, `artifacts/close-calendar-target.png`
- `artifacts/adaptive-card-je-approval.json` — sample Teams payload
- `artifacts/sox-evidence-packet-sample.zip` — reference packet format

## Appendix B — Cross-references

- Scenario README: [./README.md](./README.md)
- Practice overview: [../README.md](../README.md)
- Narrated architecture: [../../../reference/APEX-Stacked-Architecture-Narrated.html](../../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design (audit row, LEDGER, commercial envelope): [../../../APEX%20-%20Design%20and%20Build/APEX_Design.md](../../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
- APEX Sellers Guide (Runtime Plane, LEDGER feedback loop): [../../../book/Professional-APEX-M-Sellers-Guide.html](../../../book/Professional-APEX-M-Sellers-Guide.html)
- 47-archetype catalog: `packages/apex-orchestrator/src/apex_orchestrator/archetypes/catalog.py`
- Nike account folder (reference client): `C:\Stage\Clients\Industries\Consumer\Brands-Lifestyle\Nike\01_account\`
