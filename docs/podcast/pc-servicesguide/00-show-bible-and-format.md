# Show Bible · The APEX Services Podcast · v2

This document is the *design rulebook* for the v2 series. It explicitly supersedes the v1 show bible (archived). The shift from v1 to v2 is design-level — read this carefully before writing or narrating any episode.

---

## 1. Why v2 exists

User feedback on v1 (verbatim, paraphrased):

> *"I could not follow the conversation. The challenge was it was not a dialog but a listing of technical implementations and chapter references. I would like a stair-step dialog where foundation is laid and builds upon itself. The dialog should have narrative, overview, and historical foundation. It should provide more detail in areas being covered without switching around the technical topics. More time can be spent on each topic to expand the discussion, meaning there will be more podcasts in the series created. Please reference blog sites and learning sites when building the .md files for the chapters. I would also start with a key business need and follow a step-by-step strategy to deliver a service for the business need to affect the KPIs."*

v2 addresses every line of that feedback. The rules below are direct translations.

---

## 2. The seven design rules

### Rule 1 · Business-need-led, not chapter-led

Episodes 5-11 each open with **a specific business pain** — retail margin compression, warranty cost spiral, cold-chain shrink, prior-auth backlog, energy operations gap, IROPs cascade, contact-center labour squeeze. The architecture follows the need. Never the other way around.

Foundation episodes (1-4) are exceptions — they establish the architectural floor that later episodes reference.

### Rule 2 · Stair-step build-up

The series is a stack. Episode 1 lays Foundation A. Episode 2 references A and lays Foundation B. Episode 3 references A and B and lays Foundation C. Etc.

By Episode 5, the listener has *internalised* the foundation. The hosts can say *"the agent reads the Service's Gold mart through the MCP boundary we discussed in Episode 4"* without re-explaining MCP. The series accumulates understanding.

**Implication for writing:** every episode after Ep 1 has at least one explicit callback to a prior episode. Not as filler — as load-bearing.

### Rule 3 · Historical and industry context as the opening

Every business-need episode opens with **historical/industry context** — 3-5 minutes setting up *how the industry got to where it is.* Real dates. Real numbers. Real shifts.

Examples:
- Retail margin squeeze: 1985 grocery margin was 1.8%. Today it's 1.4%. Forty years of compression.
- Warranty cost: warranty as a percentage of automotive revenue has roughly doubled since 2000.
- Prior auth: AMA estimates 88% of physicians describe PA burden as "high or extremely high."

The history is *load-bearing.* It earns the architecture by setting up the necessity.

### Rule 4 · One topic, fully developed, before transitioning

Each concept gets **4-6 minutes** of fully developed dialogue. No 90-second drive-bys. No ricocheting between unrelated topics. If you want to talk about MCP, talk about MCP for five minutes. Then transition deliberately.

**Implication:** episode length grows. v1 episodes were ~20 min. v2 episodes target **25-35 min.** Total series time grows from ~2.5 hours to ~5 hours.

### Rule 5 · No chapter or section numbers in spoken dialogue

The hosts know the framework. They don't recite its index.

- ❌ "Chapter 5A point seven — threshold-to-action mapping"
- ✅ "The way the framework thinks about thresholds — there are basically four kinds…"

If a source needs to be quoted, one host says *"there's a paragraph I want to read you,"* reads it, both react. Once or twice per episode max.

### Rule 6 · Each .md ends with a curated `Further Reading` section

External resources at the end of every script:

- **Microsoft Learn modules** — specific paths for products discussed (Fabric, Foundry, Agent Framework, Purview, Sentinel, etc.)
- **Microsoft Tech Community / Microsoft Source blog posts** — for the architectural patterns
- **Microsoft Architecture Center** — reference architecture diagrams
- **Industry context references** — HBR, McKinsey, Gartner, industry trade publications, regulator publications where relevant
- **The relevant chapters of the APEX Trilogy** — Sellers Guide for commercial framing, Services Guide for architecture, Deployment Guide for operations. Named, not section-numbered.

Hosts can mention these *organically* in audio — *"there's a great Microsoft Learn module on Fabric capacity sizing — show notes."* But the bulk of the reading list lives in the .md.

### Rule 7 · Business KPI is the closing beat

Every business-need episode (5-11) closes by returning to the **KPI impact** the Service produces. What changes in the client's P&L. What changes in the operator's life. What changes for the customer. Not vague — specific numbers from the framework's reference scenarios.

---

## 3. Episode template (business-need episodes 5-11)

Each business-need episode follows this seven-beat structure. Hosts don't *announce* the beats — they flow through them.

| Beat | Length | Content |
|---|---|---|
| **1. Historical opening** | 3-5 min | How the industry got here. Real dates, names, shifts. |
| **2. The pain today** | 3-5 min | The KPI being squeezed. The economics. The human cost. |
| **3. Why the incumbent approach is breaking** | 3-5 min | What dashboards / BI / RPA / SaaS can't solve. Why the human-in-the-loop is overloaded. |
| **4. The strategy** | 3-5 min | APEX's response in plain English — agent-led decision support governed by the canonical data layer. |
| **5. The Service that delivers it** | 5-7 min | The actual APEX Service. Walks the data flow — referencing the medallion (Ep 3) and agent/MCP (Ep 4) foundation. Stays on this topic for the full window. |
| **6. The KPI impact** | 3-5 min | What changes when the Service runs. Reference scenario numbers from the framework. |
| **7. Where it goes next** | 1-2 min | Wave 2 expansion. The next adjacent Service. The compounding effect. |

**Total spoken content:** 22-32 minutes. Plus `Further Reading` in the .md.

---

## 4. Episode template (foundation episodes 1-4)

Foundation episodes are more conceptual. Same pacing discipline (4-6 min per topic), but the structure is:

| Beat | Length |
|---|---|
| **1. Why this concept exists** (the historical/industry necessity) | 4-6 min |
| **2. The concept itself** (developed fully) | 8-12 min |
| **3. How it shows up in practice** (real engagement-style anecdotes) | 5-7 min |
| **4. What the listener should carry forward to later episodes** | 2-3 min |

---

## 5. Voice cast (unchanged from v1)

| Host | Voice (edge-tts) | Persona |
|---|---|---|
| **Keven** | `en-US-AndrewNeural` | Practitioner; continuity host across the Trilogy |
| **Morgan** | `en-US-EmmaNeural` | Senior solution architect; "what actually breaks in delivery" lens |

Conversational chemistry rules carry forward from v1 — disagreement is real, anecdotes are specific, no announced segments.

---

## 6. Stair-step concept map

This is the dependency graph the writer uses to plan callbacks:

```
Ep 1: The Bottleneck Moved
  └─ historical macro · why now · dashboards → decisions → agents

Ep 2: Data Flows Beat Data Warehouses (depends on Ep 1)
  └─ data-first thesis · brief medallion preview · agent reads data flows

Ep 3: The Medallion in Depth (depends on Eps 1-2)
  └─ Bronze, Silver, Gold · velocity tiers · canonical at Silver

Ep 4: The Agent and Its Tools (depends on Eps 1-3)
  └─ MCP · Agent Framework · agent reads Gold via MCP · audit row

Ep 5: Retail Margin Squeeze (Foundation + RC fluency)
Ep 6: Warranty Cost Spiral (Foundation + Ep 5 — Practice extension)
Ep 7: Cold-Chain Shrink (Foundation + Ep 5 + streaming Bronze deep)
Ep 8: Healthcare Prior-Auth (Foundation + governance maturity from prior)
Ep 9: Energy-Transition Operations (Foundation + streaming patterns from Ep 7)
Ep 10: IROPs Cascade (Foundation + orchestration depth)
Ep 11: Contact-Center Squeeze (Foundation + all business eps — cross-Practice synthesis)

Ep 12: What the Catalog Becomes
  └─ pulls everything together · compounding value · where APEX goes next
```

Every business-need episode (5-11) MUST reference at least one prior episode by concept (not by episode number — by *idea*).

---

## 7. House style — preserved from v1

- **No co-sell language.** Deloitte does not co-sell with Microsoft. Recommendation is on the merits.
- **ICE = Industrial · Construction · Equipment** per the Services Guide source.
- **Canonical schemas anchor at Silver**, not Gold.
- **Independence-safe** language throughout (no "audit," only "audit-ready evidence").
- **Anchor accounts are anonymised** by archetype where named.

---

## 8. Length targets

| Episode | Target |
|---|---|
| Foundation (1-4) | 5,000-5,500 words |
| Business-need (5-11) | 5,500-6,500 words |
| Synthesis (12) | 5,500-6,500 words |
| **Series total** | **~70,000 words** · **~5 hours audio** |

---

## 9. What v2 is *not*

- Not a marketing podcast
- Not a feature-by-feature tour of Microsoft products
- Not an audiobook of the Services Guide
- Not a chapter walk-through
- Not generic "how to think about agentic AI"

It is: a working practitioner's guide to the *business cases* APEX serves, with the architecture grounded in seven specific, named pains and the Services that address them.
