# APEX UC Harness — Step-by-step Use Case Test Harness

> ⚠️ **DEPRECATED 2026-05-07** — superseded by `Merch/MVP/docs/plans/2026-05-07-mvp-test-harness-design.md`.
> This draft was scoped wrongly: UCs are MVP-specific (Agentic Merch Q1, 20 UCs in `mvp-scope-q1-usecases.xlsx`), not APEX-wide, and the harness lives at `Merch/MVP/TestHarness/`, not `APEX/packages/apex-uc-harness/`. Do not implement against this design — it pulls in 13 cross-industry scenario folders that are out of scope. Kept for history; see the MVP-side design doc for current scope.

**Date:** 2026-05-07
**Author:** Keven Markham (with Claude pair)
**Status:** ⚠️ Deprecated. Replaced by MVP-side design + plan.
**Target package:** `packages/apex-uc-harness/` (in the APEX workspace)
**Related work:** `2026-04-21-apex-test-harness-design.md` (schema validation harness; reused here), `2026-05-05-agentic-merch-q1-mvp-design.md` (Merch W1 prototype; provides the Agentic Merch UCs)

---

## Purpose

Build a developer-facing web tool that lets a user **select a use case (UC)** from a unified catalog spanning the Agentic Merch fixtures and the cross-industry APEX scenario tree, and **step through it phase-by-phase** with inline pass/fail assertions visible at each step.

This is a *test* harness — every step has machine-checkable expected outcomes — not a demo tool. The cinematic Merch demo paths (Walkthrough §11.2) remain a separate surface; conflating the two is explicitly out of scope.

**Success criterion:** a developer can pick any of the 17 cataloged UCs from a localhost web menu, run it step-by-step (or all-the-way), see exactly what each phase emitted, see green/red on every assertion, and re-run any single step from a prior step's saved state without replaying the whole UC.

---

## Constraints locked during brainstorm

| # | Decision point | Choice |
|---|---|---|
| 1 | UC scope | **C** — both Agentic Merch fixtures and APEX scenario catalog (RC, HLS, ER, AXLE) |
| 2 | Interface | **B** — local web UI (FastAPI + HTMX) |
| 3 | Step semantics | **B** — phase from a per-UC `steps.yaml` (engine is generic; no hard-coded UC logic) |
| 4 | Pass/fail | **A** — expected outcomes declared inline in `steps.yaml`; harness is the test runner |
| 5 | Audience / UI relationship | **A** — developer-only, separate UI from the cinematic Merch demo paths |
| 6 | Build depth | **Approach 2** — Balanced MVP (3-4 weeks): engine + 17 UC `steps.yaml` + state journaling + reports |
| 7 | Package location | New `packages/apex-uc-harness/` inside APEX workspace |

---

## §1 — Architecture at a glance

**Package name:** `apex-uc-harness` (parallels `apex-test-harness`; "uc" because scope is broader than Merch).

```
packages/apex-uc-harness/
  pyproject.toml
  README.md
  src/apex_uc_harness/
    __init__.py
    _cli.py                 # apex uc-harness serve | run <uc-id> | list | report
    discovery.py            # scans for steps.yaml across configured roots
    spec/
      schema.py             # Pydantic models: UcSpec, StepSpec, ExpectSpec
      loader.py             # YAML → Pydantic with helpful errors
    runtime/
      engine.py             # StepEngine — executes one step, captures I/O, runs assertions
      state.py              # RunStore — journals each step to disk; rewind/replay
      registry.py           # Maps step kind → executor
    executors/
      agent_chain.py        # invokes apex-agentic-merch agents
      sor_seed.py           # reuses apex-test-harness PostgresContainerFixture
      http_call.py          # generic REST executor for scenario phases
      python_call.py        # arbitrary callable for custom scenario logic
      assert_only.py        # no-op step that just checks expectations
    assertions/
      kinds.py              # equals, schema_match, count, contains, ledger_row, hash_chain_valid, range, regex, not_empty
    reporting/
      markdown.py · json.py # run report writers
    ui/
      server.py             # FastAPI app
      routes.py             # /uc, /uc/{id}/run, /runs/{id}, /runs/{id}/step/{n}/execute
      templates/            # Jinja2 + HTMX
      static/               # minimal CSS, no design system
  tests/
    unit/                   # engine + state + executors + assertions
    integration/            # end-to-end against fake + real UCs
    fixtures/               # tiny synthetic UCs for harness self-tests
```

### Runtime model

Sync inline execution per HTTP request. When the UI fires "run next step," the FastAPI handler invokes `StepEngine.run_step(uc_id, step_idx, run_id)` synchronously and returns the result + journaled state pointer. No background workers, no job queue, no websockets. Slow LLM-backed steps just block the request and show an HTMX spinner. One user at a time; concurrency is not the problem this tool is solving.

### Two execution surfaces, one engine

1. **Web UI** — interactive, one step at a time, paused state visible
2. **CLI `apex uc-harness run <uc-id>`** — runs all steps headless, writes report. Same engine, no UI.

### Dependencies

```toml
dependencies = [
  "apex-core",
  "apex-agentic-merch",       # for the 4 Merch fixtures + 6-agent chain
  "apex-test-harness",        # for PostgresContainerFixture reuse
  "fastapi>=0.115",
  "uvicorn[standard]>=0.32",
  "jinja2>=3.1",
  "pydantic>=2.9",
  "pyyaml>=6.0",
]
```

---

## §2 — The `steps.yaml` schema

Each UC ships exactly one `steps.yaml` next to its existing artifacts. This is the spec — the harness has no UC-specific code, only this file driving generic executors.

```yaml
id: merch.fixture-2-demand
title: Apparel Week-16 — Demand Branch (Pricer fires)
domain: agentic-merch
version: 1
description: |
  Intent < baseline; chain APPROVES a markdown at the right depth.
  Pricer proposes 18% with 12 hero SKUs protected.

setup:
  - kind: sor_seed
    using: apex_test_harness.bronze_rc
    fixtures:
      - apex_agentic_merch.fixtures.fixture_2.bronze_rows

teardown:
  - kind: drop_schema   # reuses PostgresContainerFixture's per-run schema

steps:
  - id: 1-analyst
    title: The Analyst ranks Friday-close exceptions
    kind: agent_call
    using: apex_agentic_merch.runtime.analyst.run
    inputs:
      trace_id: "{{run.trace_id}}"
      tenant: appretl
    expect:
      - { assert: equals,        path: ranking[0].category, value: Apparel }
      - { assert: equals,        path: ranking[0].region,   value: Midwest }
      - { assert: ledger_row,    kind: exception_ranking }

  - id: 2-demand-checker
    title: Demand Checker computes intent + diagnosis
    kind: agent_call
    using: apex_agentic_merch.runtime.demand_checker.run
    inputs_from: 1-analyst.outputs.ranking[0]
    expect:
      - { assert: range,         path: intent_score, min: 0.20, max: 0.40 }
      - { assert: equals,        path: diagnosis,    value: demand }
      - { assert: ledger_row,    kind: intent_diagnosis }

  - id: 3-finance-lead
    title: Finance Lead applies 4 guardrails
    kind: agent_call
    using: apex_agentic_merch.runtime.finance_lead.run
    inputs_from: 2-demand-checker.outputs
    expect:
      - { assert: equals,        path: passed, value: true }
      - { assert: count,         path: violations, value: 0 }

  - id: 4-pricer
    title: The Pricer proposes markdown depth + hero list
    kind: agent_call
    using: apex_agentic_merch.runtime.pricer.run
    only_if: "{{ steps.2-demand-checker.outputs.diagnosis == 'demand' }}"
    inputs_from: 3-finance-lead.outputs
    expect:
      - { assert: equals,        path: depth_pct,            value: 18 }
      - { assert: count,         path: hero_skus_protected,  value: 12 }
      - { assert: range,         path: forecast_gm_recovery, min: 1900000, max: 2300000 }

  - id: 5-operations-lead
    title: Operations Lead stages the markdown action
    kind: agent_call
    using: apex_agentic_merch.runtime.operations_lead.run
    inputs_from: 4-pricer.outputs
    expect:
      - { assert: equals,        path: action.kind, value: markdown }
      - { assert: ledger_row,    kind: action_staged }

  - id: 6-briefer
    title: Briefer renders Done / Your Call / Watch
    kind: agent_call
    using: apex_agentic_merch.runtime.briefer.run
    inputs_from: 5-operations-lead.outputs
    expect:
      - { assert: contains,      path: tiles, value: your_call }
      - { assert: hash_chain_valid }
```

### Step kinds

| Kind | Executor module | Use |
|---|---|---|
| `agent_call` | `executors.agent_chain` | Invoke a Merch chain agent |
| `sor_seed` | `executors.sor_seed` | Seed Bronze rows in Postgres container (reuses `apex-test-harness`) |
| `python_call` | `executors.python_call` | Call any importable function (escape hatch for scenario phases) |
| `http_call` | `executors.http_call` | Generic REST call (for scenarios that hit local FastAPI services) |
| `assert_only` | `executors.assert_only` | No-op step purely for checking accumulated state |

### Assertion kinds

`equals` · `range` · `count` · `contains` · `schema_match` · `ledger_row` (asserts a row was written with the given kind) · `hash_chain_valid` · `regex` · `not_empty`

### Templating

- `{{run.trace_id}}` — current run metadata
- `{{steps.<step-id>.outputs.<jsonpath>}}` — prior step output
- `{{env.<VAR>}}` — environment variable

Jinja2 with `StrictUndefined`. Typos fail loudly instead of silently producing empty strings.

### Versioning

Top-level `version: 1`. The loader refuses anything it doesn't know how to parse. When the schema evolves, old `steps.yaml` files keep working until explicitly migrated.

### Why this shape works for both surfaces

- **Merch UCs:** 6 `agent_call` steps + setup/teardown. Done.
- **Scenario UCs (e.g., RC-CX-01 churn):** mix of `sor_seed` → `python_call` → `assert_only` → `python_call` → assertions. Same engine, no new code.

---

## §3 — UC discovery + selection

The selector menu enumerates UCs that live in two very different places: inside `apex-agentic-merch` and inside the loose `docs/scenarios/{Industry}/{Domain}/{UC-CODE}/` tree. Discovery is uniform regardless of where a `steps.yaml` lives.

### Roots configured in `pyproject.toml`

```toml
[tool.apex_uc_harness]
roots = [
  "packages/apex-agentic-merch/src/apex_agentic_merch/data/ucs",
  "docs/scenarios",
]
```

### Discovery rule

At startup, `discovery.scan(roots)` walks each root recursively, picks up every `steps.yaml`, and parses it through `spec.loader.load`. Each load produces a `UcSpec` (Pydantic model) or a `UcLoadError` — bad files don't crash the harness, they show up in the menu marked broken with the parse error inline.

### The `UcCatalog`

```python
@dataclass(frozen=True)
class CatalogEntry:
    spec: UcSpec | None              # None when load failed
    source_path: Path                # absolute path to steps.yaml
    domain: str                      # "agentic-merch" | "rc" | "hls" | "er" | "axle"
    uc_code: str                     # "merch.fixture-2-demand" | "RC-CX-01"
    title: str
    load_error: str | None

class UcCatalog:
    def all(self) -> list[CatalogEntry]: ...
    def by_domain(self) -> dict[str, list[CatalogEntry]]: ...
    def get(self, uc_code: str) -> CatalogEntry: ...
```

### Selector UI (single page at `/`)

```
┌──────────────────────────────────────────────────────────────────┐
│ APEX UC Harness                                                  │
├──────────────────────────────────────────────────────────────────┤
│ Filter: [____________]  Domain: [all ▾]  Status: [all ▾]         │
├──────────────────────────────────────────────────────────────────┤
│ ▸ Agentic Merch (4)                                              │
│   ✓ merch.fixture-1-supply       Apparel Wk-16 — Supply Branch   │
│   ✓ merch.fixture-2-demand       Apparel Wk-16 — Demand Branch   │
│   ✓ merch.fixture-3-mixed        Apparel Wk-16 — Mixed Diagnosis │
│   ✓ merch.fixture-4-block        Apparel Wk-16 — Guardrail Block │
│ ▸ Retail & Consumer (2)                                          │
│   ✓ RC-CX-01                     Loyalty Churn → Winback         │
│   ✓ RC-RISK-01                   Returns Fraud Detection         │
│ ▸ Health & Life Sciences (5)                                     │
│   ✓ HLS-CLIN-01                  Care Gap Closure                │
│   ⚠ HLS-CLIN-02                  Claims Denial Prevention  [yaml │
│                                  parse error: line 12 unknown    │
│                                  step kind 'fhir_call']          │
│   ...                                                            │
│ ▸ Energy & Resources (5)                                         │
│ ▸ Automotive (1)                                                 │
└──────────────────────────────────────────────────────────────────┘
```

### Status badges

| Glyph | Meaning |
|---|---|
| `✓` | loaded clean |
| `⚠` | parse error |
| `▶` | currently has an active run |
| `✓✓` | last run all-green |
| `✗` | last run had failures |

### Embedded design decisions

- **Filesystem rescan** via `?refresh=1`. Auto-rescan on file change is a YAGNI follow-on.
- **Menu doubles as inventory health-check.** Parse errors visible inline = no separate `lint` command needed.
- **`uc_code` is the stable id.** Used everywhere — URL slugs, run journal directories, report file names. Collisions across roots fail discovery loudly.
- **Group by industry domain** in the menu; status/recency sort options are post-MVP.

---

## §4 — Execution engine + state journaling

The hardest part. Three coupled jobs: run a step, journal everything to disk, support rewind/replay from any prior step.

### Run lifecycle

```
POST /uc/merch.fixture-2-demand/run
   → engine.start_run(uc) → returns run_id
   → creates .uc-runs/<run_id>/
       run.json                 (manifest: uc_id, started_at, run_id, trace_id)
       0-setup/
         inputs.json
         outputs.json
         result.json            (ok/skipped/error + duration_ms + assertions[])
       1-analyst/                ← created when step 1 runs
       2-demand-checker/
       ...
   → redirects to /runs/<run_id>

POST /runs/<run_id>/step/1/execute
   → engine.run_step(run_id, step_idx=1)
   → loads accumulated state from .uc-runs/<run_id>/{0..0}/outputs.json
   → resolves templating ({{steps.<id>.outputs.<path>}})
   → invokes executor (agent_chain | sor_seed | python_call | http_call | assert_only)
   → captures stdout/stderr to step.log
   → runs assertions, builds AssertionResult[]
   → writes inputs.json, outputs.json, result.json
   → returns StepResult JSON for the UI to render
```

### The `RunStore`

```python
class RunStore:
    def create_run(self, uc: UcSpec) -> RunId: ...
    def write_step(self, run_id: RunId, step_idx: int, payload: StepPayload) -> None: ...
    def read_step(self, run_id: RunId, step_idx: int) -> StepPayload: ...
    def state_at(self, run_id: RunId, before_step_idx: int) -> RunState: ...
    def list_runs(self, uc_id: str | None = None) -> list[RunMeta]: ...
    def fork(self, run_id: RunId, from_step_idx: int) -> RunId: ...
```

`state_at(run_id, before_step_idx=4)` is the rewind primitive — returns accumulated outputs of steps 0..3, ready to feed step 4.

### Two operations that build on `state_at`

1. **Re-run a single step.** UI button "Re-run from step 4" → `state_at(run_id, 4)` builds the input context → execute step 4 → overwrite `4-pricer/`. Steps 5+ become stale and get marked dirty in the UI; user can click "continue from here" to re-run them.
2. **Fork a run.** UI button "Branch from step 3" → `fork(run_id, from_step=3)` copies steps 0..2 into a new `<new_run_id>` directory and lets the user proceed with different inputs from step 3. Useful for "what if intent had been 0.45?" exploration without losing the original run.

### Journaled artifacts per step

| File | Contents |
|---|---|
| `inputs.json` | Resolved inputs after templating (so reruns are self-contained) |
| `outputs.json` | Whatever the executor returned (Pydantic dumped) |
| `result.json` | `{ok: bool, duration_ms, assertions: [{kind, ok, expected, actual, path}]}` |
| `step.log` | stdout + stderr (LLM raw responses, etc.) |
| `ledger.jsonl` | LEDGER rows produced this step (only for `agent_call` steps) |

### Why disk and not in-memory

The harness has to survive process restarts (Uvicorn auto-reload during dev), and "show me yesterday's run" is a real ask. JSON files in a `.uc-runs/` directory cover both with zero infrastructure. A per-run `.lock` file keeps two browser tabs from corrupting each other.

### Resource model per run

- One Postgres schema per run (reused across all steps in that run; dropped on `teardown`)
- One Ollama process if any `agent_call` step needs an LLM (reused across runs at the process level)
- All temp paths under `.uc-runs/<run_id>/` so cleanup is `rm -rf` of one directory

### What happens when a step fails

- Step's `result.json` records `ok: false` with the failing assertions
- Subsequent steps stay unrun (UI shows them grayed)
- "Continue anyway" button in UI lets the user proceed past a red step (writes `forced: true` to result.json)
- "Re-run from here" lets the user fix and retry

### Concurrency

One active run per UC per process. If the user clicks "Run" while a run is mid-step, the second request 409s with "run `<id>` is in progress." This is dev tooling; queueing is YAGNI.

---

## §5 — Web UI shape

Dev-only, minimal, no design system. HTMX over Jinja2 templates — server-rendered HTML, partial page swaps on action. No React, no JS framework, no build step.

### Three pages

1. **`/`** — UC catalog (per §3)
2. **`/uc/<uc_code>`** — UC detail + run launcher + recent run list
3. **`/runs/<run_id>`** — the stepper (the main view)

### The stepper layout

Two-column. Left: step list + controls. Right: details panel for the selected step.

```
┌──────────────────────────────────────────────────────────────────┐
│ run r-2026-05-07-1432  •  merch.fixture-2-demand  •  in progress │
├─────────────────────────┬────────────────────────────────────────┤
│ Steps                   │ Step 4 — The Pricer                    │
│                         │ ──────────────────────────────────────  │
│ ✓ 0  setup    23ms      │ Status: ✓ green (314 ms)               │
│ ✓ 1  Analyst  41ms      │                                        │
│ ✓ 2  Demand   89ms      │ Inputs                                 │
│ ✓ 3  Finance  12ms      │ ┌────────────────────────────────────┐ │
│ ▶ 4  Pricer   314ms     │ │ {"guardrail_pass": true,           │ │
│ · 5  Ops      —         │ │  "category": "Apparel",            │ │
│ · 6  Briefer  —         │ │  "intent_score": 0.31,             │ │
│ · 7  teardown —         │ │  "diagnosis": "demand"}            │ │
│                         │ └────────────────────────────────────┘ │
│ [▶ Run next step]       │ Outputs                                │
│ [▶▶ Run all remaining]  │ ┌────────────────────────────────────┐ │
│ [↻ Re-run from step 4]  │ │ {"depth_pct": 18,                  │ │
│ [⑂ Fork from step 3]    │ │  "hero_skus_protected": [..×12],   │ │
│ [📄 steps.yaml]         │ │  "forecast_gm_recovery": 2100000}  │ │
│ [📊 final report]       │ └────────────────────────────────────┘ │
│                         │ Assertions (3/3 ✓)                     │
│                         │   ✓ equals depth_pct == 18             │
│                         │   ✓ count  hero_skus_protected == 12   │
│                         │   ✓ range  forecast_gm 1.9M-2.3M       │
│                         │ Logs ▾                                 │
│                         │ LEDGER rows (1) ▾                      │
└─────────────────────────┴────────────────────────────────────────┘
```

### Step list controls

- Click any step → details panel updates (read-only view of journaled artifacts; no execution)
- `▶ Run next step` — runs the next pending step
- `▶▶ Run all remaining` — runs to completion or first failure
- `↻ Re-run from step N` (only enabled on previously-run steps) — calls the rewind primitive
- `⑂ Fork from step N` — creates a sibling run preloaded to step N's prior state

### Status badges in step list

| Glyph | Meaning |
|---|---|
| `✓` | green — passed, fresh |
| `✗` | red — failed |
| `▶` | currently running (visible for slow LLM steps via HTMX `hx-indicator`) |
| `·` | pending (not yet run) |
| `⊘` | skipped (`only_if` was false) |
| `~` | stale — was green but a prior step was re-run; needs re-run to be trusted |
| `!` | forced past a failure |

### Details panel sections (collapsible)

1. Status + duration
2. Inputs (resolved JSON, syntax-highlighted)
3. Outputs (JSON)
4. Assertions (one row each, expected vs. actual on failure)
5. Logs (stdout/stderr; collapsed by default)
6. LEDGER rows (only for `agent_call`; collapsed by default)
7. Raw step spec from `steps.yaml`

### Tech stack inside the UI

- Jinja2 templates
- HTMX 2.x (CDN-loaded; one `<script>` tag in base.html)
- Tailwind via CDN (no build step) — utility classes only, no design tokens
- Highlight.js for JSON syntax highlighting
- Zero JS files of our own — every interaction is `hx-post` returning HTML fragments

### Operational posture

- No auth, no CSRF, binds to `127.0.0.1` only. Dev tool; production-grade web hardening is YAGNI.
- Polish deliberately deferred: real-time log streaming (websockets), step diff between two runs, search across run history, exportable shareable run URLs.

---

## §6 — UC inventory, reporting, harness self-testing

### 6.1 UC inventory shipped in MVP

Approach 2 commits to authoring `steps.yaml` for every UC that already has artifact folders.

| Domain | UC code | Title | Steps (est.) | Source |
|---|---|---|---|---|
| Agentic Merch | `merch.fixture-1-supply` | Apparel Wk-16 — Supply Branch | 7 | New |
| Agentic Merch | `merch.fixture-2-demand` | Apparel Wk-16 — Demand Branch | 7 | New |
| Agentic Merch | `merch.fixture-3-mixed` | Apparel Wk-16 — Mixed Diagnosis (escalate) | 7 | New |
| Agentic Merch | `merch.fixture-4-block` | Apparel Wk-16 — Guardrail Block | 6 | New |
| Retail & Consumer | `RC-CX-01` | Loyalty Churn → Winback | 5 | Existing (README only) |
| Retail & Consumer | `RC-RISK-01` | Returns Fraud Detection | 5 | Existing |
| HLS — Clinical | `HLS-CLIN-01` | Care Gap Closure (population health) | 4 | Existing |
| HLS — Clinical | `HLS-CLIN-02` | Claims Denial Prevention | 5 | Existing |
| HLS — Clinical | `HLS-CLIN-03` | Clinical Decision Support — Oncology | 5 | Existing |
| HLS — Clinical | `HLS-CLIN-04` | Trial Patient Matching | 4 | Existing |
| HLS — Clinical | `HLS-CLIN-05` | Prior Auth Automation | 5 | Existing |
| Energy & Resources | `ER-NET-01` | Distribution Outage Triage | 4 | Existing |
| Energy & Resources | `ER-NET-02` | Pipeline Integrity / Leak Detection | 4 | Existing |
| Energy & Resources | `ER-NET-03` | Predictive Wellhead Maintenance (upstream O&G) | 4 | Existing |
| Energy & Resources | `ER-NET-04` | Refinery Yield Optimization | 4 | Existing |
| Energy & Resources | `ER-QUAL-01` | Environmental Compliance Monitoring | 4 | Existing |
| Automotive | `AXLE-ASSET-01` | Predictive Maintenance — Stamping Press OEE | 5 | Existing |

**Total: 17 UCs, ~80 steps to author.**

**Authoring posture for the 13 scenario UCs:** their existing folders are mostly `.gitkeep` placeholders. We are *defining* most of these scenarios as we author their `steps.yaml`. Where a real implementation doesn't exist yet, the step uses the `python_call` executor against a stub that returns canned data — the assertions still validate the *contract*, not the implementation.

### 6.2 Reporting

Every run produces two artifacts in `.uc-runs/<run_id>/`:

**`report.md`** — Markdown, suitable for pasting in PRs:

```markdown
# Run r-2026-05-07-1432

- UC: `merch.fixture-2-demand` — Apparel Wk-16 — Demand Branch
- Started: 2026-05-07 14:32:11Z  •  Finished: 2026-05-07 14:32:14Z  •  Duration: 2.4s
- Result: ✓ PASS (6/6 steps green, 18/18 assertions green)

| # | Step | Status | Duration | Assertions |
|---|---|---|---|---|
| 1 | The Analyst | ✓ | 41ms | 3/3 |
| 2 | Demand Checker | ✓ | 89ms | 3/3 |
| 3 | Finance Lead | ✓ | 12ms | 2/2 |
| 4 | The Pricer | ✓ | 314ms | 3/3 |
| 5 | Operations Lead | ✓ | 22ms | 3/3 |
| 6 | Briefer | ✓ | 8ms | 4/4 |
```

**`report.json`** — same data, machine-readable.

**Catalog-wide report:** `apex uc-harness report --all` runs every UC headlessly, writes a single `catalog-report.md` summarizing pass/fail across all 17 UCs.

### 6.3 Testing the harness itself

Three test layers:

**Unit (`tests/unit/`)** — pure functions, no I/O:
- `spec/loader.py` — round-trips for valid YAML, helpful errors for malformed
- `runtime/state.py` — `RunStore` create/write/read/state_at/fork
- `assertions/kinds.py` — every assertion kind with pass + fail cases
- `runtime/engine.py` — templating resolution, `only_if` evaluation, executor dispatch (with mock executors)

**Integration (`tests/integration/`)** — real engine, fake UCs:
- `fixtures/uc-trivial/steps.yaml` — 3-step UC with `assert_only` + `python_call`
- `fixtures/uc-postgres/steps.yaml` — exercises `sor_seed` + Testcontainers Postgres
- End-to-end run of each fixture UC asserting journal contents + final report

**Smoke (`tests/integration/test_real_ucs.py`)** — runs `merch.fixture-1-supply` and `merch.fixture-2-demand` end-to-end as canaries that the engine works against actual production UCs. `@pytest.mark.smoke`.

**Coverage target:** 90% on `src/apex_uc_harness/{spec,runtime,assertions,executors}/`. UI templates and CLI excluded.

**No UI tests for v1.** Playwright integration is real overhead; engine tests cover the meat.

---

## §7 — Decision log

| Decision | Choice | Why |
|---|---|---|
| UC scope | Both Merch + scenarios | Single selector beats two surfaces; engine is generic enough to cover both |
| Interface | Local web UI | "Step-by-step" reads naturally as paged UI; matches Merch `serve` pattern |
| Step semantics | `steps.yaml` phases | Heterogeneous UCs need a per-UC spec; engine stays UC-agnostic |
| Assertions | Inline in `steps.yaml` | Single source-of-truth; harness IS the test runner |
| Audience | Dev-only | Conflating with cinematic Merch demo is feature bloat |
| Build depth | Approach 2 | Real coverage day one across both surfaces; debug ergonomics; defer pytest-plugin/CI integration to v2 |
| Package location | `packages/apex-uc-harness/` in APEX workspace | Composes existing packages without install gymnastics |
| State persistence | Disk under `.uc-runs/<run_id>/` | Survives Uvicorn auto-reload; "yesterday's run" is a real ask |
| Concurrency | One active run per UC per process | Dev tool; queueing is YAGNI |
| UI tech | HTMX + Jinja2 + Tailwind CDN | No build step; no JS framework; minimal surface |
| Auth | None; localhost-only bind | Dev tool; production hardening is YAGNI |
| Out of scope for v1 | Pytest plugin, conformance markers, diff view, real-time log streaming, Playwright | Approach 3 territory; revisit after `steps.yaml` shape is proven |

---

## §8 — Wave 2 expansion (out of scope for this design)

When v1 is green for all 17 UCs, plausible v2 work — explicitly NOT in this design:

1. **Pytest plugin** — `steps.yaml` as parametrized pytest collection; CI runs the same checks the UI runs
2. **Conformance markers** — match Sprint 26/29 governance posture
3. **Diff view** — "I changed input X, here's what changed in steps 3, 4, 5"
4. **Cross-UC LEDGER replay** — verify hash-chains spanning multiple runs
5. **Real-time log streaming** — websockets for long-running LLM steps
6. **Playwright UI tests** — only after the UI grows beyond what engine tests can cover
7. **Auto-rescan on file change** — `watchdog` for `steps.yaml` edits
8. **Catalog-wide CI lane** — `apex uc-harness report --all` in GitHub Actions

---

## Next step

Invoke `writing-plans` skill to produce the detailed implementation plan (phases, tasks, test-driven increments, week-by-week milestones) keyed off this design. The implementation plan should target a 3-4 week build with weekly demo-able milestones.
