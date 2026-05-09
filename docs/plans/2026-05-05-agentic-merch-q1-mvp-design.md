# Agentic Merch Q1 — Wave-1 MVP Design

**Date:** 2026-05-05
**Author:** Keven Markham (with Claude pair)
**Source-of-truth scope:** `06-artifacts/MVP-Sprint Plan with Backlog/APEX-Agentic-Merch-Q1-Walkthrough.docx`
**Target package:** `packages/apex-agentic-merch/`
**Engagement envelope:** RC-E2E-03 Wave-1 (4-6 weeks, $400K-$1.2M; W1 = laptop prototype with synthetic Apparel Week-16 fixtures)
**Status:** Brainstormed + design-approved 2026-05-05; ready for `writing-plans` to break into implementation tasks.

---

## Executive summary

Agentic Merch Q1 is the W1 reference implementation of the Apparel-Retailer engagement scoped in the existing `APEX-Agentic-Merch-Q1-Walkthrough.docx`. It is a **6-of-6 deployment of the APEX agent reference architecture** — Detect → Diagnose → Validate → Optimize → Act → Synthesize — running as a runnable laptop prototype with no Azure / Foundry / live-Teams dependencies. Synthetic Apparel Week-16 fixtures only.

The differentiated headline: the chain shows **both branches** in a single reference exception. When intent ≥ baseline AND root cause = supply, the chain BLOCKS the planner's markdown and triggers a rebalance + new-PO instead (DMM-bypass on supply disruption). When intent < baseline, The Pricer fires to optimize markdown depth + hero-SKU protection. APEX doesn't approve markdowns — it diagnoses whether a markdown is the right action and optimizes the depth when it is.

Build target: ~6 weeks, ~50 source files in a new `packages/apex-agentic-merch/` package, ~97 tests, ~12 new conformance markers, 1 new Sprint 18 reference manifest, 4 synthetic fixtures, 3 demo paths, 6 prepared deep-dive scenes. All composed from the existing 36-package APEX framework — no forks, no shadow code paths.

---

## §1 — Architecture overview

The full Detect → Diagnose → Validate → Optimize → Act → Synthesize sequence runs against synthetic Apparel Week-16 fixtures on a laptop. No Azure, no Foundry, no live Teams. Per Walkthrough §11.5, this is intentional — W1 proves the agentic flow with auditable rigor; W2 turns on live integrations.

```
┌────────────────────────────────────────────────────────────────────────┐
│  apex-agentic-merch  (new package; the Q1 Wave-1 prototype)            │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ 6-agent deterministic chain orchestrator                         │ │
│  │ Two-branch decision logic:                                       │ │
│  │   diagnosis=supply → DMM bypass → rebalance + new-PO             │ │
│  │   diagnosis=demand → Pricer (depth + hero) → markdown action     │ │
│  │ Done / Your Call / Watch Adaptive-Card preview (in-browser)      │ │
│  │ 4-guardrail rule engine (OTB · Margin · Markdown · AggSpend)     │ │
│  │ Decision-rights router (4 thresholds: $-tier + depth-tier)       │ │
│  │ LEDGER 14-field audit-row + hash-chain validator                 │ │
│  │ 3 canonical demo paths (exception loop · trending · audit)       │ │
│  │ Synthetic Apparel Week-16 fixtures (Docker volume)               │ │
│  │ docker-compose + Ollama for offline LLM                          │ │
│  └──────────────────────────────────────────────────────────────────┘ │
└────────────────────────┬───────────────────────────────────────────────┘
                         │ composes (no forks; no shadow code paths)
                         ▼
┌────────────────────────────────────────────────────────────────────────┐
│  EXISTING APEX FRAMEWORK (unchanged — composed only)                    │
│  apex-references  ·  apex-agents  ·  apex-services                     │
│  apex-orchestrator (Sprint 11 + Sprint 26)  ·  apex-merml/cxml/scml   │
│  apex-audit (LEDGER) · apex-compliance-lint · apex-design-tokens       │
└────────────────────────────────────────────────────────────────────────┘
```

### The 6-agent deterministic chain

| # | Walkthrough role | APEX manifest | Fires when |
|---|---|---|---|
| 1 | **The Analyst** (Agent 13) | `apex.rc.agents.store-ops-intelligence` | Always — ranks Friday-close exceptions by severity × consecutive-miss-count |
| 2 | **The Demand Checker** (Agent 1) | `apex.rc.agents.demand-sensing` | Always — computes intent score 0-1.0 vs. CXML.Signal baseline; emits diagnosis ∈ {supply, demand, mixed} |
| 3 | **The Finance Lead** (Agent 4) | 4-guardrail rule engine (deterministic) | Always — OTB · Margin · Markdown · AggregateSpend invariants |
| 4 | **The Pricer** (Agent 6, *new in W1*) | `apex.rc.agents.assortment-pricing` | **Only when diagnosis = demand** — proposes optimal markdown depth + hero-SKU protection list |
| 5 | **The Operations Lead** (Agent 8) | `apex.rc.agents.inventory-replenishment` | Always — stages action: rebalance + PO when supply, markdown action when demand |
| 6 | **The Briefer** (Agent 13.3 ADAPT) | `apex.rc.agents.markdown-cadence` (synthesis role) | Always — synthesizes Done / Your Call / Watch tiles |

The chain is deterministic: each agent emits a structured payload that round-trips through canonical schemas (MERML for plan/actuals/markdown/OTB, CXML for intent signal, SCML for lot/SKU/store) before the next agent reads it. No agent invents work outside its named role; every handoff produces a LEDGER row.

### Two demo branches

**Branch 1 — DMM Bypass on Supply Disruption** *(intent ≥ baseline AND root cause = supply)*
- Chain BLOCKS the markdown that would have executed
- Operations Lead stages a rebalance + new-PO instead
- Margin protected: the wrong markdown never fires

**Branch 2 — Intelligent Pricing on Demand Softness** *(intent < baseline OR root cause = demand)*
- Chain APPROVES a markdown — but at the right depth
- Pricer proposes 18% (not the planner's 25%) with 12 hero SKUs protected
- Forecast: $2.1M GM recovery vs. flat-25% cadence + +0.3pp loyalty engagement retained

### Decision-rights ladder (4 thresholds, 2 dimensions)

Inventory $-tier ladder (per Walkthrough §4.4):

| Threshold | Approver |
|---|---|
| Inventory action ≤ $50K | Planning Lead |
| Inventory action $50K-$100K | VP Supply Chain |
| Inventory action > $100K | Chief Merchant |

Pricing depth-tier ladder *(new for The Pricer)*:

| Threshold | Approver |
|---|---|
| Markdown depth ≤ 25% | Auto-approve (Zero-Touch) |
| Markdown depth 25-40% | Category DMM |
| Markdown depth > 40% | Chief Merchant |

Both ladders bind to the Sprint 11 4×4 gate kinds + variants (`ZeroTouchGate`, `AckOnlyGate`, `HitlGate`, `EscalationGate`).

### Three structural commitments (Walkthrough §4.5)

1. **Manifest-driven, not model-driven** — every per-tenant choice (LLM pin, threshold, approver routing, depth bands) declared in tenant manifest; agent code is tenant-agnostic
2. **Audit row, not log line** — 14-field LEDGER record on every agent decision; hash-chained; brief tiles deep-link to producing rows
3. **HITL is first-class, not bolted on** — Adaptive Card schemas versioned; webhook responses write back to LEDGER; timeout escalation declared

### W1 prototype boundaries (Walkthrough §11.5 explicit exclusions)

- Synthetic Apparel Week-16 fixtures only (no real plan/actuals streams)
- Local Docker + Ollama (no Azure, no Foundry)
- Operations Lead stages writes only (no live ERP / TMS / POS commits)
- Chief Merchant hardcoded (no live Entra)
- Adaptive Card preview only (no live Teams send)
- Single banner / category / region

---

## §2 — Components / new artifacts

### 2a — New reference deployment manifest

`packages/apex-references/src/apex_references/catalogs/agentic-merch.yaml` — 6th catalog entry alongside big-box-store / hospital / utility / plant / airline. Composes 5 RC anchor agents + 3 services (RC-E2E-03 anchor, RC-E2E-02 co-anchor, RC-E2E-01 backstop) + 7 use cases. F128 single-tenant capacity blueprint, MERML/CXML/SCML schemas, 4-6 week duration.

`packages/apex-references/src/apex_references/demo_scripts/agentic-merch.md` — 3-demo-path script mirroring §11.2 of the walkthrough.

### 2b — New `apex-agentic-merch` Python package

```
packages/apex-agentic-merch/
├── pyproject.toml
├── README.md
├── docker-compose.yml                # ollama + fastapi service + redis-stub
├── Dockerfile
├── src/apex_agentic_merch/
│   ├── _cli.py                       # apex agentic-merch serve | demo | scenes | lint
│   ├── runtime/
│   │   ├── chain.py                  # 6-agent deterministic chain orchestrator
│   │   ├── analyst.py · demand_checker.py · finance_lead.py
│   │   ├── pricer.py                 # NEW — Agent 6 wrapper
│   │   ├── operations_lead.py · briefer.py
│   ├── decision_rights/
│   │   ├── ladder.py · routes.py · thresholds.yaml
│   ├── guardrails/
│   │   ├── otb.py · margin.py · markdown.py · aggregate_spend.py · engine.py
│   ├── ledger/
│   │   ├── row_builder.py · store.py · replay.py
│   ├── ollama_client.py · llm_stub.py
│   ├── data/
│   │   ├── bronze/                   # 10 synthetic CSVs (plan, actuals, otb, etc.)
│   │   ├── silver/                   # Pydantic-shape JSON post-instantiation
│   │   ├── personas.yaml · fixtures.yaml
│   └── ui/
│       ├── server.py                 # FastAPI app
│       ├── adaptive_card/done_your_call_watch.py · card_renderer.py · webhook.py
│       ├── demo_paths/path_a · path_b · path_c
│       ├── trending/powerbi_mock.html · adaptive_latency.html
│       └── static/
└── tests/                            # ~97 tests
```

### 2c — Synthetic Apparel Week-16 fixtures

- 800 stores N.A., 4 regions, 12 categories, ~$3B annual category revenue
- Reference exception: Apparel category, Midwest region, Week 16 of FY27, miss = -12%, second consecutive miss, 24 SKUs understocked across 8 stores
- 4 fixture variants:
  - **Fixture 1** — Supply Branch (intent 0.72, diagnosis = supply, action = rebalance + $62K PO)
  - **Fixture 2** — Demand Branch (intent 0.31, diagnosis = demand, action = markdown 18% with 12 hero SKUs protected)
  - **Fixture 3** — Mixed Diagnosis (intent 0.55, diagnosis = mixed, escalation to Chief Merchant)
  - **Fixture 4** — Guardrail Block (intent 0.71, diagnosis = supply, but OTB headroom insufficient → blocked)
- Loyalty cohort of ~12K members for CXML.Signal grounding
- 12 weeks of margin-protected trending data for Path B dashboard

### 2d — Done / Your Call / Watch Adaptive Card schema

Tri-bucket card per Walkthrough §1.20:
- **DONE** — actions executed by ZeroTouch gates (auto-blocked markdown, rebalance staged)
- **YOUR CALL** — HITL decisions staged with two pre-modelled paths each (PO $62K with 5d vs. 9d ETA; markdown depth 18% vs. 22%)
- **WATCH** — observations under monitoring threshold (Cat-7 trending similar; Vendor-3 latency rising)

Schema lives in `ui/adaptive_card/done_your_call_watch.py` as versioned Python; in-browser preview renders the same JSON the W2 production version would send to Teams.

### 2e — CLI integration

```
apex agentic-merch serve                    # docker-compose up; opens browser at :8080
apex agentic-merch demo path_{a,b,c}        # run a specific demo path
apex agentic-merch chain run --fixture {1-4}# run 6-agent chain on a fixture
apex agentic-merch ledger inspect <trace>   # walk all LEDGER rows
apex agentic-merch ledger verify <trace>    # verify hash chain
apex agentic-merch lint                     # apex-compliance-lint
```

### 2f — Documentation

- `docs/plans/2026-05-05-agentic-merch-q1-mvp-design.md` (this file)
- `docs/agentic-merch-runbook.md` — presenter runbook
- `docs/agentic-merch-fixtures.md` — fixture catalog
- `Roadmap.md` snapshot update

---

## §3 — Data flow / 6-agent chain end-to-end

The architectural backbone — same chain on every fixture; only the branch and the produced action differ.

### Step-by-step Friday-night-to-Monday-morning trace

```
T+0   FRIDAY 9:43 PM — Performance close lands
       BRONZE → SILVER (Pydantic round-trip; CanonicalEnvelope + DataQualityMetadata)
T+0.1 STEP 1  THE ANALYST           → ExceptionRanking + LEDGER row 1
T+0.2 STEP 2  THE DEMAND CHECKER   → IntentDiagnosis + LEDGER row 2
T+0.3 STEP 3  THE FINANCE LEAD     → GuardrailReport + LEDGER row 3
              Branch decision (deterministic):
                diagnosis = supply  → Step 5
                diagnosis = demand  → Step 4
                diagnosis = mixed   → escalate to Chief Merchant
T+0.4 STEP 4  THE PRICER (only on demand) → MarkdownProposal + LEDGER row 4
T+0.5 STEP 5  THE OPERATIONS LEAD   → ActionPlan + LEDGER row 5/6
T+0.6 STEP 6  THE BRIEFER           → MondayBrief + LEDGER row 7
T+8h  MONDAY 8:00 AM — Adaptive Card delivered (preview-only in W1)
       Decision-rights router fires per item in YOUR CALL bucket
       (4 thresholds across 2 dimensions)
       On approve: WRITE TOOLS fire (preview-only in W1; LEDGER write-back only)
       CLOSEOUT LEDGER ROW (14 fields per Walkthrough §8.3)
       Hash chain: SHA256 link to predecessor row in same trace_id
```

### Schema mapping

| Agent | Reads (Silver) | Writes (LEDGER) | MCP tools |
|---|---|---|---|
| Analyst | MERML.Plan/Actuals/WeekOverWeek | exception ranking | `rc.assortment.get`, `rc.kpi.dashboard.get` |
| Demand Checker | CXML.Signal, MERML.AssortmentItem, weather, elasticity | intent diagnosis | `rc.demand.forecast.get`, `rc.customer.identity.lookup` (PII firewall) |
| Finance Lead | MERML.OTB/Margin/Markdown/AggregateSpend | guardrail report | none (deterministic) |
| **Pricer** | MERML.AssortmentItem/Markdown, elasticity, competitor, CXML.LoyaltyMember | markdown proposal | `rc.pricing.elasticity.get`, `rc.competitor.pricing.scan`, `rc.markdown.cadence.get` |
| Operations Lead | SCML.LotAllocation, MERML.OTB, MarkdownProposal | action staging | `rc.allocation.get`, `rc.lot.trace.get` |
| Briefer | all prior LEDGER rows for trace_id | brief synthesis | none (synthesis from LEDGER) |

### LEDGER closeout row (14 fields per Walkthrough §8.3)

```json
{
  "trace_id": "trc_2027-04-22_2143_appretl_apparel_midwest_wk16",
  "scenario_id": "rc-wbr-exception-triage-apparel",
  "service_id": "RC-E2E-03",
  "tenant_id": "appretl",
  "wbr_week": 16,
  "category": "Apparel",
  "region": "Midwest",
  "miss_pct": -0.12,
  "consecutive_miss_count": 2,
  "intent_score": 0.72,
  "diagnosis": "supply",
  "guardrail_otb_buffer_post": 0.21,
  "guardrail_margin_bps": 18,
  "actions_taken": ["rebalance_24sku_8stores"],
  "actions_staged": ["po_62k_apparel_8sku"],
  "approver_route": "vp_supply_chain",
  "margin_protected_usd": 142000,
  "decision_loop_hours": 5.7,
  "ledger_row_count": 11,
  "hash_chain_valid": true
}
```

### Classification posture (per APEX-CORE §5)

- MERML / SCML rows: `Internal`
- CXML.LoyaltyMember + CXML.Signal rows: `Restricted-PII` — tokenized at Bronze→Silver via `apex-tokenizer` (Sprint 5)
- Markdown / rebalance / PO actions: `Internal`
- LEDGER audit-row store: `Confidential` (matches Sprint 12 BL.P.84 WORM posture)

---

## §4 — Three canonical demo paths

The 45-min readout sequence: `Open (2 min) → Path A (8 min) → Path B (5 min) → Path C (8 min) → Engineering deep-dive Q&A (20 min) → Wave-2 commercial close (2 min)`.

### Demo Path A — *The Exception Loop* (8 min, both branches)

The cinematic headline. Runs the 6-agent chain twice — once on **Fixture 1** (supply branch) showing DMM bypass, once on **Fixture 2** (demand branch) showing The Pricer fires.

**Branch 1 — Supply (Fixture 1; ~4 min):** Friday close → Analyst ranks #1 of 7 → Demand Checker confirms intent 0.72 + diagnosis SUPPLY → Finance Lead passes guardrails with $190K headroom → DMM bypass strikes through planner's 25% markdown → Operations Lead stages rebalance ($46K) + new PO ($62K) → Briefer renders DONE/YOUR CALL/WATCH tiles.

**Branch 2 — Demand (Fixture 2; ~4 min):** Same exception severity, different signal. Demand Checker: intent 0.31 + diagnosis DEMAND. Finance Lead passes. **Pricer fires**: elasticity confidence 0.78 + 0.81 analog override → proposed depth 18% (vs. planner's 25%) + 12 hero SKUs protected → forecast $2.1M GM recovery. Operations Lead stages markdown action; Briefer renders demand-branch tiles.

### Demo Path B — *Margin-Protected Trending* (5 min)

Power-BI-styled mock dashboard. 12-week margin-protected line chart (range $80K-$185K/wk, mean $140K/wk). Auto-blocked-markdown distribution histogram. Adaptive-Card response-latency histogram (median 47 min, p95 82 min). Click any dot → drawer slides open showing the trace_id and 11 LEDGER rows that produced that week's number. "Open Audit Trail" button transitions to Path C.

### Demo Path C — *The Audit Trail* (8 min)

The deep-dive. 11 LEDGER rows for a single trace_id. Click row 3 → 14-field side-panel inspection (intent_score, prompt_sha, model_pin, replay_token). "Replay this decision" → output panel re-runs agent against captured inputs; result identical. "Verify chain" → all 11 hashes recompute; Merkle-root displayed. **Tamper-detection demo** (debug-mode only): mutate row 3's intent score → chain breaks at row 3. "Export for Audit" → CSV with replay_token_verified, hash_chain_valid, prompt_sha_matches_registry derived columns. Closeout: KPI back-reference graph showing which decisions contributed which margin-protected dollars.

### Independence + brand posture (across all 3 paths)

Per Sprint 29 `apex-compliance-lint` / Appendix N — every cinematic narration string runs through the linter at build time. No `partner` / `alliance` / `endorsed` / `Gold Partner` / `AI-powered` / `fully autonomous` language. Microsoft is `the platform`. Ollama is `the local LLM runtime`. The agent makes recommendations; the operator decides.

---

## §5 — Engineering deep-dive scenes (~20 min Q&A)

**6 prepared scenes** with hot-keys (`Ctrl+1` through `Ctrl+6`):

| # | Trigger question | Scene title |
|---|---|---|
| 1 | "How does this run on a laptop?" | The Docker + Ollama runtime |
| 2 | "What if we want to add a 7th agent?" | Manifest-driven agent extension |
| 3 | "Show me the 4-guardrail rule engine internals" | Deterministic guardrails as composable Pydantic validators |
| 4 | "How does the decision-rights ladder fire?" | Two-dimensional threshold router walked live |
| 5 | "Show me the LEDGER WORM + hash-chain cryptography" | Audit-row internals with cryptographic detail |
| 6 | "What changes from W1 to W2?" | The W1 → W2 transition map |

**5 bonus scenes** with letter keys: `p` (PII firewall), `i` (Independence lint), `c` (cancel propagation), `b` (Briefer logic), `n` (9-persona surface).

Each scene has 30-sec narration prepended + 30-sec take-away appended; presenter never has to remember exact words.

---

## §6 — Testing + governance

**Test inventory:** ~97 tests across 12 modules covering chain branches (supply / demand / mixed / guardrail-block), 4-rule engine + boundary cases, decision-rights router across 4 thresholds, LEDGER hash-chain + tamper detection, demo-path runnability, data-shape round-tripping, manifest-driven extension, cancel propagation, compliance lint.

**12 new conformance markers** pinning: 6-agent chain ordering · 3 branch outcomes · Pricer-only-on-demand · 4 named guardrails · 4 decision-rights thresholds · 14-field audit row · unbroken hash chain · replay-token round-trip · 3 demo paths runnable in budget · Independence-clean narration · W1 exclusions enforced · workspace files clean.

**Cross-package suite integration:** ~792 tests after agentic-merch lands (was 695). 24 conformance markers (12 existing + 12 new). CI lanes: `ci.yml` (conformance + cache governance + restricted terminology + standards licences) and `artifact-compliance.yml` (Independence + typography + color + responsive).

**Governance posture:** Sprint 26 invariants (cache-governance lint, Charter §3 annotations, fail-closed control plane, audit-row contract); Sprint 29 invariants (Independence pack, design tokens, color compliance, typography); Walkthrough §11.5 exclusions test-enforced; manifest re-sign required on agent add/remove.

**Build-time gates:** ruff + mypy → pytest 100% → compliance-lint → push → GitHub Actions → conformance markers → 4-lane artifact compliance → green → merge.

---

## §7 — W1 build sequence (6-week plan)

Per RC-E2E-03 Wave-1 envelope. Each week ends with a **demo-able milestone**.

### Week 1 — Foundation + scaffolding

Empty package compiles + reference manifest validates + Docker stack boots + 4 fixtures + tenant manifest + CLI stubs + CI green. Cross-package suite at ~700 tests.

### Week 2 — Chain backbone (Steps 1-3) + LEDGER

`runtime/chain.py` orchestrator + Analyst + Demand Checker + 4-guardrail engine + Finance Lead + LEDGER row builder + WORM store. Supply branch end-to-end runnable from CLI. Cross-package suite at ~720 tests.

### Week 3 — The Pricer + Operations Lead (Steps 4-5)

The Pricer wrapping `assortment-pricing` (NEW; only fires on demand branch) + decision-rights router + Operations Lead with action staging per branch + Briefer reading LEDGER for synthesis. Both branches end-to-end CLI-runnable. Cross-package suite at ~750 tests.

### Week 4 — Adaptive Card UI + Demo Path A wiring

FastAPI server + Adaptive Card schema + card renderer + webhook + Path A scene composer + Web Speech narration + Sprint 27 cinematic styling. Path A demo-ready end-to-end. Cross-package suite at ~770 tests.

### Week 5 — Demo Paths B + C + Deep-dive scenes

12-week trending pre-computed → dashboard mock + Path B composer + LEDGER inspector UI + replay-token verifier + hash-chain validator UI + tamper-detection demo + Path C composer + 6 deep-dive scenes wired to hot-keys + 5 bonus scenes. All 3 paths runnable. Cross-package suite at ~785 tests.

### Week 6 — Hardening + conformance + runbook

Compliance pass (Sprint 29 4-lane CI green) + ~97 tests green + ~12 new conformance markers green + cross-package suite at 792+ tests + presenter runbook + fixture catalog + Roadmap snapshot update + final dry-run + release tag `agentic-merch-q1-w1.0`.

### Risk mitigations

- Ollama RAM on colleague laptops → fallback to `qwen2.5:3b-instruct`
- The Pricer prompt drift → temperature=0 + `llm_stub` fallback for canned demos
- Hash-chain edge cases → reuse Sprint 12 `apex-audit` battle-tested impl
- Adaptive Card cross-browser → pin to Chromium engines
- Trending narrative arc → hand-curate 3 of 12 weeks for DMM-bypass + Pricer events
- Conformance markers fail late → run nightly from week 3

---

## Total deliverables at end of Week 6

- 1 new `packages/apex-agentic-merch/` Python package (~50 source files, ~97 tests)
- 1 new reference manifest in `apex-references/catalogs/agentic-merch.yaml`
- 1 demo script in `apex-references/demo_scripts/agentic-merch.md`
- 4 synthetic Apparel Week-16 fixtures
- 1 cinematic walkthrough HTML + Adaptive Card schema + LEDGER inspector UI
- 1 runbook + 1 fixture catalog
- ~24 conformance markers
- Sprint 18 reference catalog grown 5 → 6
- Cross-package suite at ~792 tests

---

## Open items / future work (out of W1 scope)

Per Walkthrough §3.4 + §11.5:

- Pricing optimization beyond markdown depth (Agent 7 — Promotion Optimization, Sprint 2)
- Multi-banner orchestration (W2)
- Real Apparel-Retailer plan/actuals streams (W2)
- Azure migration (W2)
- Live Operations Lead writes to TMS/POS (W2)
- Live Entra authentication (W2)
- Live Teams send (W2)

## Cross-references

- Source-of-truth scope: `06-artifacts/MVP-Sprint Plan with Backlog/APEX-Agentic-Merch-Q1-Walkthrough.docx`
- Sprint 11 — `apex-orchestrator` primitives + 4×4 gate kinds + variants
- Sprint 12 — `apex-audit` 14-field LEDGER row + WORM + hash chain + replay token
- Sprint 16 — `apex-agents` RC anchor catalog (5 of 10 anchors composed here)
- Sprint 17 — `apex-services` RC service catalog (3 of 13 services composed here)
- Sprint 18 — `apex-references` reference deployment pattern (this is the 6th)
- Sprint 19 — `apex-registries` archetype + persona + KPI registry
- Sprint 26 — `apex-orchestrator.control_plane` + manifest-driven config + workspace v0.2
- Sprint 27 — Stacked Architecture Narrated cinematic style + design tokens
- Sprint 29 — `apex-compliance-lint` + Appendix N design system + 4-lane pre-publish CI
