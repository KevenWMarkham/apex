# Client Intake — Cross-Cloud Agentic Study Guide

**Purpose:** Produce a comprehensive per-client briefing that prepopulates the Cross-Cloud Agentic study guide — the client profile, a position on all 24 axis questions, and the research behind each. Run this template in Claude.

## How to run

1. **Pick the client.** List the files already in this `clients/` folder (every `*.md` except this template). Show the operator that list and ask: refresh one of those, or create a new client? If new, ask for the client's name.
2. **Research the client** from public sources — recent news, earnings commentary, cloud and AI announcements, partnerships, leadership changes, job postings. Note what you find and what you could not.
3. **Position the client** on each of the 24 axes below. For each axis pick an integer **0–4**: `0` = strongly the left pole, `2` = neutral, `4` = strongly the right pole. Add a one-line rationale and a confidence flag (`high` / `medium` / `low` — use `low` where research was thin). The "MS-favorable pole" tells you which end strengthens a Microsoft-attached recommendation; it does not change the client's actual position — record where the client truly sits.
4. **Draft the client profile** — industry, current clouds, AI maturity, key signals.
5. **Write the output file** `clients/<client-slug>.md` per the "Output" section. `<client-slug>` is the lowercased, hyphenated client name.

## The 24 axes

Scale for every axis: `0` = strongly [left pole] · `2` = neutral · `4` = strongly [right pole].

### Episode 1 — The Agentic Stack
- **e1-ax1** — *Of the systems your teams already call "agents," how many satisfy all four criteria — reasoning, tool use, state, and an audit substrate?* — `pipelines relabelled as agents` ↔ `systems that meet all four criteria` — MS-favorable: right.
- **e1-ax2** — *When you evaluate a cloud for agentic AI, are you deciding on the agent runtime, or on the data foundation and control plane underneath it?* — `runtime-first selection` ↔ `architecture-first selection` — MS-favorable: right.
- **e1-ax3** — *If your preferred cloud reached capability parity with the others in eighteen months, what would still make it the right choice?* — `productization lead today` ↔ `durable architectural fit` — MS-favorable: right.

### Episode 2 — Data Foundation
- **e2-ax1** — *When a new AI project starts today, does it get a fresh copy of the data, or does it compose against sources in place?* — `bulk replication into a new lake` ↔ `federation & mirroring, sources untouched` — MS-favorable: right.
- **e2-ax2** — *Is the data your agents need spread across multiple clouds, or concentrated in one?* — `cross-cloud-spread data` ↔ `single-cloud-concentrated data` — MS-favorable: right.
- **e2-ax3** — *Does your warehouse's Gold layer serve analyst dashboards, or is there a substrate shaped for agent reasoning?* — `BI-shaped Gold (aggregation)` ↔ `agent-shaped Gold (per-entity composition)` — MS-favorable: right.

### Episode 3 — Agent Runtime
- **e3-ax1** — *Do your agents' tool calls land on composed views, or directly on source systems and the data warehouse?* — `source-direct tool calls` ↔ `Gold-Tier-routed tool calls` — MS-favorable: right.
- **e3-ax2** — *Is there a specific model your teams must use — and is that preference strong enough to choose the cloud?* — `model-dominant requirement` ↔ `architecture-dominant requirement` — MS-favorable: right.
- **e3-ax3** — *For your highest-value use case, have you tested retrieval (RAG) before reaching for fine-tuning?* — `retrieval-first adaptation` ↔ `training-first adaptation` — MS-favorable: left.

### Episode 4 — Governance & Identity
- **e4-ax1** — *Does your current data-loss-prevention policy tell an agent tool call apart from a human query?* — `human-era DLP` ↔ `AI-aware DSPM` — MS-favorable: right.
- **e4-ax2** — *Is your identity reality one primary cloud with a federated SaaS workforce, or genuinely cross-cloud workloads?* — `enterprise-SaaS-federation reality` ↔ `cross-cloud-workload-identity reality` — MS-favorable: left.
- **e4-ax3** — *Which AI risk framework will your auditors and board hold you to — EU AI Act, NIST AI RMF, ISO 42001?* — `lightly-governed posture` ↔ `regulated / board-visible posture` — MS-favorable: right.

### Episode 5 — Audit & Ledger
- **e5-ax1** — *If an external auditor asked you to reproduce an agent decision from six weeks ago, could you?* — `unprovable decisions` ↔ `replayable, hash-chained decisions` — MS-favorable: right.
- **e5-ax2** — *Of your planned agent workloads, which touch regulated data, customer-facing decisions, or board-visible outputs?* — `non-regulated internal-use (~80%)` ↔ `regulated / customer-facing / board-visible (~20%)` — MS-favorable: right.
- **e5-ax3** — *Is your agent activity captured as structured audit rows, or as free-form log lines?* — `free-form log lines` ↔ `schema-validated audit rows` — MS-favorable: right.

### Episode 6 — FinOps
- **e6-ax1** — *Can you state the cost-per-decision for your top three agent use cases — and the outcome value of each?* — `aggregate AI spend` ↔ `per-use-case cost-per-outcome` — MS-favorable: right.
- **e6-ax2** — *Do your agents default to the most capable model, or is the model selected per task?* — `default-to-largest-model` ↔ `disciplined model-mix` — MS-favorable: right.
- **e6-ax3** — *What is your AI consumption cost trajectory quarter over quarter — and is the growth attributed to workloads?* — `unattributed consumption growth` ↔ `workload-attributed consumption` — MS-favorable: right.

### Episode 7 — Multi-Cloud & Portability
- **e7-ax1** — *When you say "multi-cloud," do you mean workloads on multiple clouds, or individual workloads spanning clouds?* — `enterprise-level multi-cloud (the norm)` ↔ `workload-level multi-cloud (the exception)` — MS-favorable: left.
- **e7-ax2** — *What is driving the multi-cloud requirement — regulatory residency, data gravity, M&A — or lock-in aversion and vendor leverage?* — `legitimate multi-cloud drivers` ↔ `multi-cloud theatre` — MS-favorable: right.
- **e7-ax3** — *If the model behind your agent were deprecated tomorrow, how long would it take to swap it?* — `model-locked agent design` ↔ `model-portable agent design` — MS-favorable: right.

### Episode 8 — The Seller's Playbook
- **e8-ax1** — *Where did the client show the most pain — and is that pain a contained, measurable Wave 1?* — `pain-aligned Wave 1 entry` ↔ `scope-creep / boil-the-ocean` — MS-favorable: left.
- **e8-ax2** — *Is the client's cloud reality a deliberate strategy, or an inherited history of acquisitions and defaults?* — `strategic cloud posture` ↔ `inherited cloud history` — MS-favorable: right.
- **e8-ax3** — *Does the client's architecture team know AWS and GCP well enough to catch an overclaim?* — `sophisticated, cross-cloud-fluent client` ↔ `trusting, single-cloud client` — MS-favorable: right.

## Client profile fields

- **industry** — the client's primary industry.
- **clouds** — current cloud footprint (e.g. "AWS primary, Azure for M365").
- **aiMaturity** — where they are with AI/agents (e.g. "POCs in progress, no production agents").
- **signals** — key signals: recent news, earnings notes, leadership/org changes, stated AI priorities.

## Output

Write `clients/<client-slug>.md` with these sections:

1. `# <Client Name> — Cross-Cloud Agentic client briefing` and the date.
2. `## Profile` — the four profile fields, each with a sentence.
3. `## Axis positions` — for each of the 24 axes: the axis id, the chosen 0–4 position with the pole names, the one-line rationale, and the confidence flag.
4. `## Research sources` — a bulleted list of the public sources used.
5. `## Import data` — a single fenced `json` code block, exactly this shape (fill every axis you could position; omit an axis only if you truly could not form a view):

```json
{
  "schema": 3,
  "client": {
    "id": "<client-slug>",
    "name": "<Client Name>",
    "profile": { "industry": "", "clouds": "", "aiMaturity": "", "signals": "" },
    "axes": {
      "e1": { "e1-ax1": 0, "e1-ax2": 0, "e1-ax3": 0 },
      "e2": { "e2-ax1": 0, "e2-ax2": 0, "e2-ax3": 0 },
      "e3": { "e3-ax1": 0, "e3-ax2": 0, "e3-ax3": 0 },
      "e4": { "e4-ax1": 0, "e4-ax2": 0, "e4-ax3": 0 },
      "e5": { "e5-ax1": 0, "e5-ax2": 0, "e5-ax3": 0 },
      "e6": { "e6-ax1": 0, "e6-ax2": 0, "e6-ax3": 0 },
      "e7": { "e7-ax1": 0, "e7-ax2": 0, "e7-ax3": 0 },
      "e8": { "e8-ax1": 0, "e8-ax2": 0, "e8-ax3": 0 }
    },
    "paq": {}, "actions": {}, "notes": []
  }
}
```

The seller then opens the study guide → Overview tab → Client profile → **Import**, and selects this `.md` file. The guide reads the `json` block, loads the client, and prepopulates the profile, all 24 axis selectors, the likelihood bars, and the seller-action emphasis.
