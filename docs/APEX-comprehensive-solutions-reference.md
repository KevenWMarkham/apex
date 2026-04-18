# APEX

## Agentic Platform for Enterprise eXecution

### Reinventing Enterprise Decision-Making on Microsoft

**A Comprehensive Solutions Reference for the Intelligent Enterprise**

**April 2026 · Version 1.0 · CONFIDENTIAL**
**Deloitte Microsoft Technology & Services Practice**

---

## Preamble

This is the strategic reference for APEX — the Agentic Platform for Enterprise eXecution. It is written for executives who approve the investment, architects who design the implementation, and delivery leads who run the programme. If you are a developer looking for code-level detail, open the companion *APEX Developer Implementation Guide* alongside this document.

APEX is a **multi-industry platform**. It ships today as four Practices — Retail & Consumer, Healthcare & Life Sciences, Energy & Resources, and Industrial & Manufacturing — with 24 subscribable services across them. Where a companion framework like AXLE goes deep on one vertical, APEX goes broad across verticals while keeping one contract, one data plane, and one intelligence plane. The two are complementary: APEX is the platform; AXLE is an industry-deep programme that a client can adopt alongside (or inside) their APEX footprint.

This document sets out **what APEX is, why it matters now, what it ships with, and how clients land it**. The structure mirrors the reference document pattern Deloitte uses for flagship platform offerings: forces of change, AI journey, maturity model, human element, platform architecture, industry-practice chapters, implementation roadmap, appendices.

---

## Table of Contents

**Executive Summary** — What is APEX · Value Proposition · The Ask · Service Portfolio at a Glance

**Forces of Change** — Five converging pressures that make agentic platforms inevitable

**The AI Journey** — Five eras of enterprise AI; where APEX fits

**Decision-Automation Maturity Model** — Five levels from dashboards to autonomous

**IT Simplification** — The platform thesis · before/after · Microsoft-native architecture

**The Human Element** — Fears · generational handoff · re-designing knowledge work

**The APEX Framework** — Four-layer manifest model · schemas · MCP servers · services · gates

**How to Read This Document**

**Part I — Foundation** (chapter 1, strategic overview)

**Part II — Industry Practices** (chapters 2–5: RC, HLS, ER, AXLE)

**Part III — Cross-Practice Capabilities** (chapters 6–8: shared services, observability, governance)

**Part IV — Implementation & Delivery** (chapters 9–11: waves, onboarding, scaling)

**Part V — Future State** (chapter 12: the autonomous enterprise)

**Appendices** — Schema Reference · Service Registry · Personas · MCP Tools · Microsoft SKUs · Partner Ecosystem · Glossary

---

# Executive Summary

## What Is APEX?

APEX is a **manifest-driven, agentic platform** that turns enterprise events into resolved, auditable decisions. It runs on Microsoft Fabric as the data plane and Azure AI services as the intelligence plane, bound by a versioned contract that specifies every schema, every agent, every tool, every orchestration, and every human-in-the-loop gate.

Where traditional analytics answers *"what happened?"*, APEX answers three harder questions:

1. **What should happen next?** — agents reason over canonical data and propose an action
2. **Who must approve it, and under what rules?** — HITL gates mapped deterministically from the nature of the change
3. **What audit trail does the decision leave?** — every reasoning chain, tool call, and human approval is stitched into one traceable operation with append-only logs

An APEX deployment is not "a data platform with AI features bolted on." It is a **contract between data and decisions**, enforced in code and auditable end-to-end.

## The Value Proposition

For a client's CFO, COO, and CIO jointly, APEX delivers three measurable outcomes within the first twelve months:

- **Decision latency drops 5–10×**. Events that used to wait hours for a manager to triage are resolved in minutes with equal or better judgement quality, because the agent has done the data-gathering, correlation, and option-generation before the human even arrives at the decision.
- **Manager touch-time drops 60–80%**. Not because humans are removed from the loop, but because their time shifts from data-gathering to judgement. A typical APEX decision reduces manager touch from 15 minutes to 90 seconds.
- **Audit and compliance readiness is built-in**. Every decision is recorded with its inputs, its reasoning chain, its tool calls, its approver, and its rollback pointer. Regulatory filings that used to cost weeks of reconstruction ship in hours.

A typical APEX programme pays back in 12–18 months on decision-latency ROI alone, before counting write-off-avoided and regulatory-penalty-avoided.

## The Ask

APEX is a three-wave programme:

- **Wave 1 — Foundation** (months 1–6): Fabric workspace topology stood up, first Practice's canonical schemas deployed, 2–3 services live, first HITL decisions flowing.
- **Wave 2 — Intelligence** (months 7–12): full service catalogue of the first Practice live; cross-practice shared services (tokeniser, approvals, observability) instrumented.
- **Wave 3 — Optimisation** (months 13–18): second Practice added; cross-practice orchestrations introduced; tenant-scale KPIs trending on or above target.

Investment envelope per Practice: **$3–8M in Wave 1**, **$5–12M in Wave 2**, **$3–6M in Wave 3**. Expected ROI at month 18: **2–4× cumulative on Wave 1 services alone**.

## Service Portfolio at a Glance

APEX ships today with **24 subscribable services** across four Practices:

- **Retail & Consumer (RC): 8 services** — Cold Chain Excursion Response, Receiving Variance Dispute, ESL Pricing Integrity, Phantom-OOS Detection, Recall Response, BOPIS Exception Handling, Shrink & Void Anomaly, Customer Incident Triage.
- **Healthcare & Life Sciences (HLS): 6 services** — Discharge Ready Surveillance, Sepsis Early Warning, Revenue-Cycle Denial Recovery, Supply Expiry Management, Clinical Trial Matching, Patient Safety Incident.
- **Energy & Resources (ER): 5 services** — Meter Outage Detection, Grid Anomaly Response, Billing Exception Handling, Field Work-Order Optimisation, Regulatory Event Response.
- **Industrial & Manufacturing (AXLE): 5 services** — Line-Down Triage, Quality Excursion Response, Supply-Chain Disruption, Recall Traceability, Plant KPI Drift.

Each service is one subscribable SKU: scenario + personas + KPIs + SLOs + artifact bundle + prerequisites + commercial terms. Clients subscribe to services, not to "APEX". A client may start with two services and grow to a portfolio of twelve across two Practices.

---

# Forces of Change

Five forces are converging in 2026 to make agentic platforms not just possible but **operationally necessary**. APEX exists because these forces are real, measurable, and accelerating.

## Force 1: The Decision-Velocity Gap

Every enterprise function has the same story: the data arrives faster, the regulatory window shortens, the customer expects an answer sooner, but the **decision-maker capacity has not scaled**. A store manager in 2010 made fifty material decisions per shift. In 2026 the telemetry produces five hundred candidate decisions per shift. Humans triage what they can; the rest is silent drift — write-offs, compliance misses, customer churn.

Closing this gap by hiring is not viable. Closing it by "smarter dashboards" has been tried for a decade and has not worked — dashboards make the gap visible, not smaller. Closing it with agentic decision-automation is the only path that scales, **provided governance keeps pace**.

## Force 2: Agentic AI Has Reached Inflection

In late 2024 the combination of reasoning-model quality, tool-use reliability, and enterprise-grade agent runtimes crossed a threshold. Before the threshold, agents were a research demo. After it, agents are a production platform. By 2026 the question is no longer "can agents reason well enough?" — it is **"can your organisation operate agents responsibly and at scale?"**

This is not a technology question. It is a governance, contract, and observability question. APEX exists because the technology is ready but the **operating model** is not, and someone has to build the operating model.

## Force 3: Data Sovereignty and PII Complexity

Every industry APEX serves now faces an intersecting web of data obligations: GDPR, CCPA, HIPAA, PCI DSS, FDA 21 CFR Part 11, FERC reliability standards, ISO 27001, SOC 2 Type II, and increasing data residency requirements by nation and by sector.

A decision that crosses any of these boundaries without a documented contract is a compliance incident waiting to happen. APEX's manifest-and-contract model is not a convenience — it is **the minimum bar** for operating an agentic platform in regulated industry.

## Force 4: Regulatory Acceleration

The regulatory environment in every APEX Practice has shortened response windows and raised audit-evidence requirements. In healthcare, discharge and sepsis reporting moved from days to hours. In retail, FDA recall response expected in hours not days. In energy, FERC reliability filings shortened. In manufacturing, recall traceability windows have compressed.

None of these regulators will accept "our systems couldn't keep up" as a defence. APEX's **decision audit row** is designed to be regulatory evidence — stitched to the triggering event, every tool call, every approver, every action — and retained under customer-managed keys for the required window.

## Force 5: The Knowledge-Worker Capacity Shortage

Demographics are against us. Experienced knowledge workers — senior nurses, seasoned store managers, veteran billing analysts, long-tenured grid operators — are retiring faster than replacements are being trained. The institutional judgement that handled yesterday's ambiguous cases is walking out the door.

APEX's HITL gate model is designed to **preserve and encode** the judgement of today's experts. Every decision flow captures not just the approver's answer but the rationale; the approval audit rows are training data for the next generation of narrower agents that absorb the patterns. APEX is, among other things, a **knowledge-capture platform**.

## Forces of Change: Summary

| Force | Pressure | APEX response |
|---|---|---|
| Decision-velocity gap | Events outpace human triage | Agents do data-gathering; humans judge |
| Agentic AI inflection | Technology is ready; governance lags | Manifest-driven contracts + gates |
| Data sovereignty / PII | Regulators require contracted data flows | Canonical Silver + Purview + tokenisation |
| Regulatory acceleration | Windows shortened; evidence demanded | Decision audit rows as regulatory evidence |
| Knowledge-worker shortage | Experts retire; handoff is unfinished | HITL captures rationale; seeds narrower agents |

---

# The AI Journey

Enterprise AI moves in eras. Each era built on the previous one; none fully replaced it. APEX is the operating platform for **Era 5**.

## Era 1 — Rules & Automation (1980s–2010)

Rule engines, workflow automation, BPM. Decisions were encoded as trees of `if` clauses by analysts. Worked for narrow, high-volume, well-understood problems. Broke on ambiguity.

## Era 2 — Analytics & Business Intelligence (2010–2018)

Data warehouses, OLAP cubes, dashboards. The era of "let the operators see more data and they will decide better." Gave decision-makers visibility but did not reduce their burden; if anything, the dashboards added one more meeting.

## Era 3 — Predictive Machine Learning (2018–2023)

Models trained on historical data to predict outcomes: churn, fraud, failure, demand. Worked on narrow, well-labelled problems. Required specialist MLOps teams. Did not generalise — each model a bespoke project.

## Era 4 — Generative AI & Copilots (2023–2025)

LLMs enter the enterprise. Copilots augment individual productivity. The era of "chat with your data." Real value, but mostly at the individual level — the organisational operating model did not change.

## Era 5 — Agentic AI & Autonomous Operations (2025–2030)

Reasoning-tier models plus tool-use plus orchestration runtimes plus governance. Agents become **operational actors** with bounded authority, traced decisions, and defined human escalation. This is the era APEX is built for.

## AI Integration Levels

Within Era 5, organisations sit at one of five integration levels. Move up one level per programme wave.

```
Level 0   No AI in the decision path
Level 1   AI as insight (dashboards, recommendations)
Level 2   AI as assistant (Copilot in Teams, Word, Excel, code IDEs)
Level 3   AI as advisor (structured recommendations on specific decisions)
Level 4   AI as agent with HITL (APEX target — Wave 2 end state)
Level 5   AI as autonomous operator (North Star — selected services only)
```

Most clients enter APEX at **Level 1 or 2** and exit Wave 1 at **Level 3**, Wave 2 at **Level 4**, and Wave 3 ready to pilot **Level 5** on the safest services.

---

# Decision-Automation Maturity Model

The APEX maturity model replaces the Industry 4.0 model used for manufacturing. It is the single self-assessment we run with clients on day one.

```
┌────────────────────────────────────────────────────────────────────┐
│ Level 1 · DASHBOARDS                                               │
│   Humans read, humans decide. Latency: hours.                      │
│   Failure mode: silent drift; backlog builds; outliers missed.     │
├────────────────────────────────────────────────────────────────────┤
│ Level 2 · ALERTS                                                   │
│   System pushes signals; humans decide. Latency: minutes-to-hours. │
│   Failure mode: alert fatigue; false positives teach operators to  │
│   ignore; true positives get lost in the noise.                    │
├────────────────────────────────────────────────────────────────────┤
│ Level 3 · RECOMMENDATIONS                                          │
│   System proposes specific actions with rationale; humans approve. │
│   Latency: minutes. Manager touch-time: 3–5 minutes per decision.  │
│   Failure mode: recommendations not trusted; approval backlog;     │
│   rationale unverifiable.                                          │
├────────────────────────────────────────────────────────────────────┤
│ Level 4 · ORCHESTRATED HITL  (APEX TARGET)                         │
│   Agents act within gates tuned to risk class. Bulk of decisions   │
│   are ACK_ONLY or ZERO_TOUCH; the consequential ones are HITL.     │
│   Latency: seconds-to-minutes. Manager touch-time: 60–90 seconds   │
│   per HITL decision. Full audit trail.                             │
├────────────────────────────────────────────────────────────────────┤
│ Level 5 · AUTONOMOUS  (NORTH STAR)                                 │
│   Selected high-volume, well-bounded services run with no gate at  │
│   steady-state; humans monitor exceptions only. Latency: seconds.  │
│   Reached only after 6+ months at Level 4 with proven track        │
│   record and formal audit approval.                                │
└────────────────────────────────────────────────────────────────────┘
```

### Self-Assessment: Where Is Your Enterprise Today?

Most APEX clients, on day one, sit at **Level 1 or Level 2** for the function they want APEX to transform. A smaller number are at **Level 3** already — typically where a prior programme shipped recommendation systems that were partially adopted.

**Wave 1 targets Level 3.** Agents reason and propose; humans approve every decision. Trust is built by volume — the first 500 approvals are typically unanimous-or-close-to-it, which earns the programme the credibility to proceed.

**Wave 2 targets Level 4.** Once decision quality is proven on a service, its HITL gate is down-shifted for the bulk cases (ACK_ONLY) while keeping HITL on the consequential cases (high-$, high-regulatory, high-customer-impact). Manager touch drops by an order of magnitude.

**Wave 3 targets pilot Level 5** on a narrow subset of services where the cost/benefit of a gate is clearly negative (e.g., phantom-OOS restocking decisions at $5 of inventory risk) — with an audit review at 6-month intervals.

---

# IT Simplification

## The Platform Thesis

Before APEX, a typical Fortune 500 enterprise has **twelve to twenty point tools** for decision-support in each function: dashboards, alerting systems, recommendation engines, ticketing, audit archives, communications apps, approval workflows, and so on. Each tool has its own data model, its own identity layer, its own operations discipline, and its own vendor contract.

After APEX, the enterprise has **one platform** with many services. The data model is canonical. The identity layer is Entra ID. The operations discipline is one App Insights workbook per tenant. The vendor contract is Microsoft plus Deloitte-delivered Practice content.

## Before APEX vs. After APEX

| Concern | Before APEX | After APEX |
|---|---|---|
| Data model | 20 product-specific models | One canonical schema family per domain |
| Identity | Per-tool local identity + SSO patchwork | Entra ID + managed identity end-to-end |
| Decision audit | Distributed across tool logs | One append-only `silver_decision_audit` table |
| Compliance evidence | Manually reconstructed | Query a single audit table |
| Tool sprawl | 12–20 point tools per function | 1 platform, multiple services |
| Onboarding new function | 12–18 months; custom build | 4–6 weeks; subscribe to catalog |
| Vendor relationships | Dozens | Microsoft + Deloitte |
| Cost transparency | Per-tool, hard to aggregate | Per-tenant, per-service, fully tagged |

## APEX as the Intelligence Layer

APEX does not replace the client's Systems of Record. ERP stays. WMS stays. EHR stays. SCADA stays. POS stays. APEX sits **on top** as the intelligence layer — canonicalising SOR data in Silver, exposing Gold feature views to agents, orchestrating decisions, and closing the loop back to the SOR via controlled write paths (e.g., ledger staging, work-order creation).

This thesis matters because it bounds the ask. APEX is not an eighteen-month rip-and-replace. It is a four-to-six-month overlay that starts producing measurable value in months, not years.

## The Microsoft-Native Stack

APEX runs on a seven-layer Microsoft-native stack. Every layer is a product the client either already has in their enterprise agreement or can add through their existing Microsoft relationship.

```
L7  Experience         Teams · Power Platform · Copilot · M365 · Associate mobile
L6  Orchestration      Azure AI Agent Service · Logic Apps · Durable Functions
L5  Intelligence       Azure AI Foundry · Azure OpenAI · Azure AI Search · Embeddings
L4  Protocol           MCP servers (Container Apps / Functions)
L3  Data plane         Fabric Lakehouse · Warehouse · Eventstream · OneLake
L2  Integration        Data Pipelines · Dataflow Gen2 · Mirrored Databases
L1  Foundation         Entra ID · Managed Identity · Purview · App Insights · Azure Monitor
```

Every arrow between layers is an identity-authenticated, trace-instrumented, managed-by-infrastructure-as-code boundary. No weak seams.

---

# The Human Element

A platform that replaces decisions without involving the humans who used to make them fails — politically, operationally, and often legally. APEX is designed around the opposite thesis: **agents change the nature of knowledge work, not the presence of knowledge workers.**

## The Fear Factor

On every APEX engagement, the same four fears surface in the first weeks. They must be answered directly.

### Fear 1: "Will AI replace me?"

The honest answer: your role changes, but it doesn't disappear — and the new role is higher-leverage than the old one.

A store manager's shift before APEX was 65% data-gathering (walking aisles, reading dashboards, opening spreadsheets) and 35% decision-making. After APEX it inverts: 15% data-gathering, 85% judgement. The role becomes consequential in a way it wasn't when the operator spent most of the shift chasing data. Empirically, the manager who was going to quit stays longer after APEX ships, because the work becomes more interesting.

### Fear 2: "Can I trust an agent's decision?"

The honest answer: you will not be asked to. You will be asked to **approve** the agent's proposed decision, with full visibility into how it reached it.

Every APEX HITL card shows the reasoning chain, the tools called, the data read, and the specific recommendation. The approver can approve, modify, or reject. In Wave 1, the HITL gate is wide — every consequential decision goes through a human. In Wave 2, patterns emerge: decisions of class X are unanimously approved 98% of the time, so they downgrade to ACK_ONLY. The approver did not lose control; they redirected their attention to the decisions that still warrant it.

### Fear 3: "What about auditability and compliance?"

The honest answer: auditability is better than what you have today, not worse.

Today's decision audit is mostly implicit: a Teams thread, an email chain, a spreadsheet comment, sometimes a notebook. Reconstructing a decision for a regulator is a week's work. Under APEX, the decision audit is explicit: one row in a Silver table, with operation_Id, input_hash, output_hash, decider_oid, rationale, and rollback pointer. Customer-managed keys. Immutable. Query-able. Regulators have responded well.

### Fear 4: "We've tried this before and it failed."

The honest answer: it probably did, and probably for one of three reasons — the data wasn't canonical, the governance wasn't contractual, or the change management was underfunded. APEX addresses all three. But the fear should not be dismissed; it should be interrogated, and the specific prior-failure-modes should be named in the kickoff workshop.

## The Generational Handoff

The experienced operators in every client organisation are also, almost by definition, the people whose judgement has not been captured in any system. They retire and the institutional knowledge walks out the door. APEX's HITL capture is the single most underappreciated aspect of the platform: every approved decision encodes expert judgement as training data for the next generation of narrower agents, which absorb the patterns the expert never wrote down.

This is why the hardest-to-automate decisions are also the ones that should go through APEX first. The expert's judgement becomes institutional memory only when it is observed, logged, and associated with outcomes.

---

# The APEX Framework

The platform itself is organised in four lifecycle layers, five artifact lanes, a canonical schema model, an MCP server taxonomy, a service catalogue, and a HITL gate model. This section is a strategic survey; the companion Developer Implementation Guide is the depth reference.

## The 4-Layer Manifest Model

```
L1  CONTRACT    apex-core — specification, validators, bump rules
L2  EDITION     a versioned release of L1 (e.g., Core v1.2.0)
L3  PRACTICE    an industry bundle: RC · HLS · ER · AXLE
                 (schemas + agents + MCP + orchestrations + gates + services + personas + KPIs)
L4  TENANT      a client instance; pins a Practice release; subscribes to services
```

Every change to APEX flows top-down. A Core change ripples to every Edition; an Edition change ripples to every Practice; a Practice release lands at a client only when the tenant pins it. Clients are never forced to upgrade on APEX's schedule; they upgrade on their schedule, within a policy.

> **Terminology note.** Earlier APEX material used the term *Fleet* for L3. As of Core v1.2.1 the canonical term is *Practice*, because L3 bundles much more than agents — it includes the full complement of artifacts listed above. Backward-compatible shims retain the old name in code through Core v1.2.x; removed in Core v1.3.

## The Canonical Schema Model

Every Practice carries one or more **canonical schema families** — versioned JSON/Delta definitions that decouple agents from SOR variation. A client with Manhattan WMS and a client with SAP EWM both produce rows that look identical at the `MERML.STORE_INVENTORY_POSITION` layer.

- **SCML** — Supply-Chain Markup Language (receiving, cold chain, recalls, lot trace) · RC + HLS + AXLE
- **MERML** — Merchandising Markup Language (prices, inventory, markdowns, voids) · RC
- **CXML** — Customer Experience Markup Language (orders, loyalty, incidents, substitutions) · RC + HLS
- **HLSCML** — Healthcare & Life Sciences Markup Language (encounters, observations, claims) · HLS
- **ERCML** — Energy & Resources Markup Language (meter readings, grid events, work orders) · ER
- **AXLECML** — Industrial & Manufacturing Markup Language (production events, quality, genealogy) · AXLE

Each schema family has its own manifest, its own SemVer cadence, and its own backward-compat rules. Every entity carries the five-field canonical envelope (`event_id`, `event_ts`, `entity_id`, `source_system`, `source_system_ts`) that makes cross-entity joins possible.

## The MCP Server Taxonomy

APEX uses the open Model Context Protocol (MCP) as the typed contract between agents and the outside world. Servers are organised into three classes:

- **Domain servers** — one per schema family (`scml-mcp`, `merml-mcp`, `hlscml-mcp`, `ercml-mcp`, `axlecml-mcp`, `cxml-mcp`)
- **Utility servers** — cross-cutting platform services (`fabric-mcp`, `policy-mcp`, `telemetry-mcp`, `approvals-mcp`, `tokenizer-mcp`, `ledger-mcp`)
- **External servers** — wrapped third-party sources (`fda-mcp`, `ferc-mcp`, `edi-mcp`, `vendor-portal-mcp`, `pharma-recall-mcp`)

This taxonomy is not cosmetic. Domain servers segregate identity (PHI-read grants stay within `hlscml-mcp`). Utility servers isolate operational concerns. External servers contain third-party dependency blast radius.

## The Service Model

A **service** is the commercial unit. One service = one scenario + one primary persona + measurable KPIs + committed SLOs + a bundle of artifacts + prerequisites + tiered commercial terms. Clients subscribe to services, not to APEX wholesale. A service manifest is a first-class APEX artifact, validated by the same tooling that validates schema and practice manifests.

The full 24-service catalogue is at **Appendix B**.

## The HITL Gate Model

Every decision an APEX service produces resolves through a gate. Four gate kinds, mapped from the nature of the change:

| Gate | Behaviour | Typical bump |
|---|---|---|
| **ZERO_TOUCH** | Apply silently; log as auto-taken | PATCH |
| **ACK_ONLY** | Apply + notify; acknowledgement optional | MINOR |
| **HITL** | Present + wait for approve/reject/modify | MAJOR |
| **ESCALATION** | Route to a cross-functional owner | context-dependent |

The mapping from SemVer bump to gate kind is **deterministic by default** and **overridable by tenant policy**. A high-risk tenant (e.g., a HIPAA health system) may set `MINOR → HITL` globally. A low-risk tenant may set `MINOR → ZERO_TOUCH` on selected services. The default matrix is conservative.

## Medallion Architecture in APEX Terms

- **Bronze** — landed SOR data in SOR-native shape, 30–90 day retention, read only by Silver transforms
- **Silver** — canonicalised, tokenised, contract-compliant; 7+ year retention; source of truth
- **Gold** — materialised feature views; 90 day rolling; agent-read path only

Agents never read Bronze. Agents rarely read Silver. Agents primarily read Gold, via an MCP tool, under managed identity, with trace instrumentation and tenant-scoped RLS.

---

# How to Read This Document

This document has five parts plus appendices.

- **Executive readers** read the Executive Summary plus the chapter introduction for each Practice in Part II. Ten to fifteen minutes total.
- **Architects** read Parts I, III, and IV end-to-end, plus the Practice chapter most relevant to their client engagement. Two to three hours.
- **Delivery leads** focus on Part IV (Implementation) and the Practice chapters in scope. One to two hours.
- **Client account teams** use the Executive Summary plus Part II as the service catalogue for commercial conversations.

Every chapter follows the same eight-section pattern, inherited from Deloitte's reference-document discipline: **the Story · Forces Driving Change · the Human Reality · AI Integration Maturity · Decision-Automation Positioning · KPI Dashboard · the Solution · Implementation & Transformation**. The repetition is the point — once a reader has the pattern, they can navigate any chapter quickly.

---

# Part I — Foundation

## 1.1 The Story

It is 6:16 on a Tuesday morning. At Store 100 in Senatobia, Mississippi, a dairy reefer has been drifting above the 41°F threshold for four hours. The store manager, Marisol Reyes, is not yet on-site — doors open at 07:00. Without APEX, she will arrive at 06:45, notice the temperature log, and have thirty minutes to triage 412 units of dairy inventory before customers arrive. Her options are coarse: dump it all, sell it and hope, or phone the regional team and miss the open. The write-off will be $1,847 if she dumps, an indeterminate amount if she sells, and a disciplinary event if she opens late.

With APEX, by the time Marisol arrives at 06:08 (having been paged by a Teams card at 06:05), the Cold Chain Excursion Response service has already done the work. The excursion is classified, the inventory is segmented into 291 save-viable and 121 destroy units by product category and the FDA food safety threshold, a targeted write-off of $534 is staged in the ledger, and the HITL card is waiting for her approval. She reads the card on her phone over coffee at 06:10, approves at 06:11, and is on the floor at 6:20 — eight minutes ahead of yesterday's schedule, with 71% of the inventory saved.

This story is not a demo. It is the shift that APEX service `APEX-RC-CXP-01` runs at Store 100 every time a reefer breaches. The entire transaction — detection, reasoning, HITL gate, decision, audit, ledger write — completes in under eight minutes, with 90 seconds of Marisol's time.

This is Part I's argument: decision-automation inside a gated, auditable platform is the **new operating baseline**. Not an aspiration. The baseline.

## 1.2 Forces Driving Change

The five forces from the framework chapter land differently in each client engagement. In Part I we consider them at the enterprise level — the C-suite's view. The key pattern to recognise in a kickoff workshop is which **two or three** forces are most acute for this client. That ordering determines the first-Practice-first-service prioritisation.

## 1.3 The Human Reality

At enterprise level, the human reality is a chief executive who is accountable for decisions their organisation is not making fast enough, a CIO whose tool portfolio has outgrown the operating model, a CFO whose audit readiness is a quarterly fire drill, and a COO whose frontline operators are leaving faster than they can be replaced. APEX addresses all four.

## 1.4 AI Integration Maturity

The enterprise-level AI integration maturity is usually heterogeneous across functions. Retail operations may be at Level 2, finance at Level 3, clinical at Level 1, compliance at Level 1. APEX does not require enterprise homogeneity; it advances the functions that subscribe, function by function.

## 1.5 Decision-Automation Positioning

Part I anchors the platform at Level 4 (Orchestrated HITL) as the Wave 2 end state. The CEO's strategic narrative to the board is "we moved our operations from Level 2 to Level 4 on the decisions that matter most, in twelve months, with full auditability." That is a defensible board narrative.

## 1.6 KPI Dashboard

Four enterprise KPIs we track across every Practice:

- **Decision latency p95** — target 5–10× improvement from baseline in the first twelve months
- **Manager touch-time per consequential decision** — target 60–80% reduction
- **Audit readiness (time to reconstruct a decision)** — target hours-to-minutes, not weeks
- **Service subscription depth** — number of services live per tenant; target 8+ by month 18

## 1.7 The Solution: APEX Platform

Part I's solution is the platform itself — the four-layer manifest model, the canonical schemas, the MCP taxonomy, the service catalogue, the HITL gate model, and the Microsoft-native stack. Individual Practices elaborate in Part II.

## 1.8 Implementation & Transformation

Wave 1 decisions — which Practice first, which service first, which tenant first — are the make-or-break moment. The pattern that works: **start with the Practice whose pain is most acute and whose SOR data is most accessible**. For most retail clients that is RC Cold Chain or OSA. For most health systems it is HLS Discharge or Denial. For utilities, Meter Outage. For manufacturers, Line-Down Triage.

Pick one Practice. Pick two or three services within it. Run Wave 1 to ship them. Use the Wave 1 proof to fund Wave 2.

---

# Part II — Industry Practices

## Chapter 2: Retail & Consumer (RC) Practice

### 2.1 The Story

At 8:36 on a Tuesday morning, at a regional grocery chain, customers begin ringing up promotional pricing on a SKU that shouldn't be on promotion. The electronic shelf label gateway has been stale since 03:00; the ERP scheduled the regular price to take effect at 06:00; 127 tags never received the update. Four rings later — four customers, four price complaints just waiting to happen — the POS anomaly detector flags the pattern, the `APEX-RC-ESL-03` service activates, the pricing analyst gets a HITL card naming exactly which gateway is affected and which 127 SKUs to force-refresh, and the issue is contained before a fifth ring.

Retail runs on hundreds of signals per store per minute. Without APEX, a handful of them reach a human in time to matter. With APEX, the ones that are consequential are triaged, staged, and presented; the rest are auto-resolved or logged for review.

### 2.2 Forces Driving Change

Retail has every one of the five forces operating at once, but three dominate:

- **Decision-velocity gap** is acute in retail operations. Store managers face a firehose; most of it sticks to dashboards nobody watches.
- **Regulatory acceleration** on food safety and recalls is sharp. FDA recall response windows have compressed; customer contact expectations have tightened.
- **Knowledge-worker shortage** on the retail frontline is a demographic emergency. Tenured store managers and department leads leave for roles with less chaos; replacements are green.

### 2.3 The Human Reality

The RC persona who benefits most is the Store Manager on Duty — "Marisol" in the Store 100 examples throughout this document. Marisol does not want to be replaced by an agent. She wants the platform to handle the data-gathering so she can spend her shift on the things that require judgement: disciplinary conversations, customer service escalations, team coaching, the unusual. APEX's pitch to Marisol is "you will spend your shift on the work you trained for, not the work the dashboards force on you."

Secondary RC personas: Regional Operations Director, Merchandising Analyst, Loss Prevention Lead, Customer Care Agent, Compliance Officer. See Appendix C for role specifications.

### 2.4 AI Integration Maturity

Typical RC baseline: **Level 2** (alerts in a dashboard). Wave 1 target: **Level 3** (HITL recommendations on first 2–3 services). Wave 2: **Level 4** (gate-tuning on mature services). Level 5 pilots in Wave 3 are typical for Phantom-OOS Detection (low-$ consequence per decision).

### 2.5 Decision-Automation Positioning

RC is the Practice where the platform proves itself. The Cold Chain story at Store 100 is the demo every stakeholder sees, because it is the most tangible — tangible temperatures, tangible dollars, tangible ninety-second manager touch. After the RC pilot, the rest of the portfolio sells itself.

### 2.6 KPI Dashboard

Four KPIs every RC client tracks:

- **Write-off avoided, $ / store / month** — target ≥ 65% of at-risk inventory saved on cold-chain events
- **Manager touch-time, seconds / HITL decision** — target ≤ 90 sec (industry baseline 6–12 min)
- **Customer incident time-to-triage, minutes** — target ≤ 15 min for Tier-2 food safety
- **Vendor dispute recovery rate, %** — target ≥ 70% on receiving variances

### 2.7 Solution Portfolio & Architecture

Eight services in the RC Practice. Each service entry below names the scenario, the primary persona, the core KPIs, the included artifacts, and the tier.

**APEX-RC-CXP-01 — Cold Chain Excursion Response** (Pro / Enterprise · GA v1.2)
Scenario: refrigeration unit breaches threshold > 2h. Persona: Store MOD. KPIs: writeoff avoided ≥ 65%, time-to-brief ≤ 10 min, manager touch ≤ 90 sec. Bundles SCM-A04/A05/A06 + SCML.COLD_CHAIN_TELEMETRY + ORCH-03. Gate: HITL. Prereqs: Monnit IoT + Manhattan WMS + F8. Onboarding 14 days.

**APEX-RC-RVD-02 — Receiving Variance Dispute** (Essentials / Pro / Enterprise · GA v1.2)
Scenario: RFID portal reads short of ASN. Persona: Store MOD. KPIs: variance recovered ≥ 70%, days-to-closure ≤ 5. Bundles SCM-A01/A02 + MER-A01 + ORCH-02. Gate: ACK_ONLY. Prereqs: Manhattan WMS + EDI-856 + F8.

**APEX-RC-ESL-03 — ESL Pricing Integrity** (Pro / Enterprise · GA v1.2)
Scenario: ESL stale vs. ERP schedule. Persona: Merchandising Analyst. KPIs: stale tag count reduction ≥ 80%, time-to-remediate ≤ 30 min. Bundles MER-A02/A03 + ORCH-04. Gate: ACK_ONLY.

**APEX-RC-OSA-04 — Phantom-OOS Detection** (Pro / Enterprise · GA v1.2)
Scenario: shelves empty while perpetual shows stock. Persona: Store MOD. KPIs: phantom-OOS caught ≥ 90%, time-to-restock ≤ 35 min. Bundles MER-A04/A05 + ORCH-05. Gate: ACK_ONLY.

**APEX-RC-RCL-05 — Recall Response** (Enterprise · GA v1.2)
Scenario: FDA / USDA / vendor recall issued. Persona: Compliance Officer. KPIs: affected customers contacted ≥ 98%, time-to-contain ≤ 4 h. Bundles SCM-A01/A02 + MER-A11/A12 + CX-A01 + ORCH-07. Gate: ESCALATION.

**APEX-RC-BPX-06 — BOPIS Exception Handling** (Pro / Enterprise · GA v1.2)
Scenario: BOPIS item OOS at pick. Persona: Customer Care Agent. KPIs: substitution acceptance ≥ 70%, customer response ≤ 120 sec. Bundles CX-A03/A04 + ORCH-06. Gate: HITL.

**APEX-RC-SHK-07 — Shrink & Void Anomaly** (Enterprise · GA v1.2)
Scenario: correlated void / return / CCTV patterns. Persona: Loss Prevention Lead. KPIs: evidence sealed ≥ 85%, false accusation ≤ 1%. Bundles MER-A10/A11/A12 + ORCH-08. Gate: ESCALATION.

**APEX-RC-CXI-08 — Customer Incident Triage** (Pro / Enterprise · GA v1.2)
Scenario: customer-reported food-safety incident. Persona: Customer Care Agent. KPIs: Tier-1 response ≤ 15 min, cross-store correlation ≥ 95%. Bundles CX-A01/A02 + SCM-A02 + ORCH-09. Gate: HITL → ESCALATION.

### Architecture Components (RC)

- Canonical Silver schemas: SCML, MERML, CXML (subsets)
- Primary SORs: Monnit IoT, Manhattan WMS, POS, ESL Gateway, FDA Recall Feed, Customer Incident Portal
- Capacity: F8 entry-level, F16 recommended for > 25 stores, F32 for > 250 stores
- Identity groups: `store-mod`, `regional-ops-director`, `merchandising-analyst`, `loss-prevention-lead`, `customer-care-agent`, `compliance-officer`

### 2.8 Implementation Roadmap (RC)

**Wave 1 — Foundation** (months 1–6) · $3–5M typical
- Provision Practice + Tenant workspaces (dev/test/prod)
- Connect Monnit IoT + Manhattan WMS + POS; land Bronze
- Silver transforms for SCML + MERML core entities
- Deploy services CXP-01 and RVD-02; first HITL decisions at one pilot store
- Wave exit: 30-day track record; stakeholder approval for Wave 2

**Wave 2 — Intelligence** (months 7–12) · $5–8M
- Full RC catalogue (CXP, RVD, ESL, OSA, BPX, CXI) at the pilot region
- Gate-tuning on mature services (CXP-01 HITL → ACK_ONLY for non-Critical severities)
- Cross-practice observability workbook
- Wave exit: region-wide rollout; KPI trend lines on-target

**Wave 3 — Optimisation** (months 13–18) · $3–5M
- National rollout
- SHK-07 and RCL-05 (highest-consequence services) added
- Pilot Level-5 autonomous on OSA-04 for low-$ thresholds

---

## Chapter 3: Healthcare & Life Sciences (HLS) Practice

### 3.1 The Story

At 14:32 on a Wednesday, at an urban academic medical centre, a customer-reported food-safety style pattern surfaces — but in healthcare it is different: a patient has been transferred to ICU with early-sepsis indicators that were visible in the vitals-and-labs stream six hours earlier. The labs that should have triggered an alert were buried in a queue reviewed once per shift.

With `APEX-HLS-SEP-02` running, the pattern is triangulated across vitals, labs, and the encounter record four to six hours earlier than clinical recognition. A HITL card lands on the charge nurse's device with the suggested escalation — respect the nurse's judgement, but present the pattern. Early detection of sepsis at this margin saves lives and reduces length-of-stay by days.

### 3.2 Forces Driving Change

HLS is under every force at maximum intensity:

- **Regulatory acceleration** — reporting windows shrink annually; 21 CFR Part 11 signature requirements; HIPAA enforcement posture stiffens
- **Knowledge-worker shortage** — nursing, hospitalist, and informaticist shortages are acute and getting worse
- **Data sovereignty** — PHI handling must be perfect; the margin for error is zero
- **Decision-velocity gap** — clinical decisions with strong time-value-of-information profiles

### 3.3 The Human Reality

The HLS persona most transformed by APEX is the **charge nurse** — "Samantha" in client parlance — whose shift is 40% clinical judgement and 60% bed management, orderly-tracking, and chart-reading. The platform shifts that balance. Charge nurses who have been through an APEX pilot are the programme's best ambassadors.

Secondary HLS personas: clinical informaticist, revenue-cycle analyst, pharmacy supply lead, trial coordinator, patient safety officer, compliance officer.

### 3.4 AI Integration Maturity

HLS baseline is often **Level 1** — raw dashboards in Epic or Cerner, not tied to decisions. Wave 1 target: **Level 3** on discharge readiness and denial recovery (two services with the most tractable data). Wave 2 expands to clinical-time-critical services (sepsis) with stricter gate posture. Level 5 pilots are rare in HLS due to the regulatory posture.

### 3.5 Decision-Automation Positioning

HLS is the Practice where gate policy matters most. Default gate posture on clinical services is **HITL everywhere** and stays HITL across Waves 2 and 3. The gain is not gate-downgrade; the gain is earlier detection and better evidence packaging for the human.

### 3.6 KPI Dashboard

- **Length-of-stay reduction, hours / admission** — target 8–14h median reduction on discharge service
- **Sepsis early detection, hours** — target detection 4–6h ahead of clinical recognition with ≤ 8% FPR
- **Denial recovery, $ / month** — target 40–60% recovery rate on eligible denials
- **Patient safety incident triage, time-to-classification** — target ≤ 4 h for severe incidents

### 3.7 Solution Portfolio & Architecture

Six services in the HLS Practice.

**APEX-HLS-DSR-01 — Discharge Ready Surveillance** (Pro / Enterprise · GA v1.2)
Scenario: predict discharge readiness 24h ahead. Persona: Charge Nurse. Bundles HLS-A01/A02 + HLSCML.PATIENT_ENCOUNTER + ORCH-10. Gate: ACK_ONLY. Prereqs: Epic EHR (CDC + ADT) + F32 + HIPAA.

**APEX-HLS-SEP-02 — Sepsis Early Warning** (Enterprise · GA v1.2)
Scenario: vitals + labs triangulation. Persona: Charge Nurse. Bundles HLS-A03/A04 (reasoning-tier) + ORCH-11. Gate: HITL. Prereqs: Epic ADT + FHIR + labs + HIPAA + 21 CFR Part 11.

**APEX-HLS-RVC-03 — Revenue-Cycle Denial Recovery** (Pro / Enterprise · GA v1.2)
Scenario: denial received; root cause + appeal draft. Persona: Revenue Cycle Analyst. Bundles HLS-A05/A06 + ORCH-12. Gate: HITL. Prereqs: 837/835 feed + EHR coding + HIPAA + SOX.

**APEX-HLS-SUP-04 — Supply Expiry Management** (Pro / Enterprise · GA v1.2)
Scenario: medications approaching expiry. Persona: Pharmacy Supply Lead. Bundles SCM-A07/A08 + ORCH-13. Gate: ACK_ONLY (HITL if recall). Prereqs: pharmacy inventory + FDA/pharma recall feeds + HIPAA.

**APEX-HLS-CTM-05 — Clinical Trial Matching** (Pro / Enterprise · GA v1.2)
Scenario: patient-to-trial matching. Persona: Clinical Trial Coordinator. Bundles HLS-A07 (reasoning) + ORCH-14. Gate: HITL. Prereqs: EHR + trials registry + HIPAA.

**APEX-HLS-PSI-06 — Patient Safety Incident** (Enterprise · GA v1.2)
Scenario: near-miss / incident triage. Persona: Patient Safety Officer. Bundles HLS-A08/A09 + ORCH-15. Gate: ESCALATION. Prereqs: incident reporting system + EHR + HIPAA + 21 CFR Part 11.

### Architecture Components (HLS)

- Canonical Silver schemas: HLSCML (full family)
- Primary SORs: Epic EHR (CDC + ADT + FHIR + labs), pharmacy inventory, trials registry, denial/claim feeds
- Capacity: F32 baseline (reasoning-tier models raise token spend)
- Identity: clinical identity groups per role with segregated PHI-unlock managed identity; Purview labels on all silver_* PHI tables

### 3.8 Implementation Roadmap (HLS)

**Wave 1** · $4–7M · months 1–6
- Epic integration (CDC + FHIR) — longest lead-time item; start day one
- DSR-01 live on one unit as pilot
- HIPAA audit readiness pack shipped

**Wave 2** · $6–10M · months 7–12
- RVC-03 at health-system scale
- SEP-02 pilot on ICU + step-down (highest-risk, strictest gate)

**Wave 3** · $4–6M · months 13–18
- System-wide rollout of DSR + RVC
- CTM-05 and PSI-06 added
- System compliance dashboard as single pane of glass

---

## Chapter 4: Energy & Resources (ER) Practice

### 4.1 The Story

At 03:47 on a Monday morning, a grid anomaly propagates across three substations in a utility's northern region. The signal appears in SCADA nine seconds after the event. Traditional practice would hand it to a grid-ops engineer for manual classification — a task that takes minutes under load. With `APEX-ER-GRD-02` running, the anomaly is classified in seconds as a line-to-ground fault with high load-shed probability, a recommended operator action (breaker sequence) is staged, and a HITL card lands on the lead dispatcher. Total time to decision: 38 seconds. Customer-minutes-interrupted reduced by two orders of magnitude relative to the manual path.

### 4.2 Forces Driving Change

ER is the Practice with the tightest time-value-of-information curves. A minute of inaction on a grid event is measurable in customer impact and regulatory cost.

- **Regulatory acceleration** — FERC reliability standards and NERC audit posture tighten yearly; state PUCs add retail-side scrutiny
- **Decision-velocity gap** — grid ops decisions are the hardest part of this force: second-level SLOs on Critical events
- **Knowledge-worker shortage** — grid operators with deep experience are retiring; training pipeline is inadequate
- **Data sovereignty** — less of a PII issue, more of a critical-infrastructure data sensitivity issue

### 4.3 The Human Reality

The ER hero persona is the **grid operations engineer** — sits in the control room, carries the weight of every outage. APEX's pitch is that the agent does the first-pass classification in the seconds before the engineer's coffee is even cold, so the engineer's first human action is informed rather than reactive.

Secondary ER personas: meter ops lead, field dispatcher, billing ops analyst, regulatory affairs officer.

### 4.4 AI Integration Maturity

ER baseline is **Level 2**, sometimes **Level 3** at the largest utilities. Wave 1 target: Level 3 on meter and billing services. Wave 2 adds the critical-infrastructure services (GRD-02, REG-05) at strict HITL. Level 5 is unlikely for grid ops given the regulatory posture.

### 4.5 Decision-Automation Positioning

ER is where the SLO discipline matters most. Grid anomaly detection p95 ≤ 30 sec is non-negotiable. APEX's instrumentation makes these SLOs measurable and contract-able.

### 4.6 KPI Dashboard

- **Outage detection accuracy, %** — target ≥ 95% with FPR ≤ 2%
- **Customer-minutes-interrupted, %** — target 30–60% reduction YoY on covered events
- **FERC reporting on-time, %** — target 100% (any miss is a regulatory event)
- **First-time-fix rate on field dispatches, %** — target ≥ 80%

### 4.7 Solution Portfolio & Architecture

Five services in the ER Practice.

**APEX-ER-MTR-01 — Meter Outage Detection** (Pro / Enterprise · GA v1.2)
Scenario: AMI meter reads missing. Persona: Meter Ops Lead. Bundles ER-A01/A02 + ORCH-16. Gate: ACK_ONLY. Prereqs: SAP ISU + AMI head-end + SOX.

**APEX-ER-GRD-02 — Grid Anomaly Response** (Enterprise · GA v1.2)
Scenario: SCADA anomaly classification + operator action. Persona: Grid Ops Engineer. Bundles ER-A03/A04 (reasoning) + ORCH-17. Gate: HITL (ESCALATION on large events). Prereqs: SCADA + OMS + DMS + SOX + FERC.

**APEX-ER-BIL-03 — Billing Exception Handling** (Pro / Enterprise · GA v1.2)
Scenario: billing anomaly classification + routing. Persona: Billing Ops Analyst. Bundles ER-A05/A06 + ORCH-18. Gate: ACK_ONLY. Prereqs: SAP ISU + CIS + SOX.

**APEX-ER-FWO-04 — Field Work-Order Optimisation** (Pro / Enterprise · GA v1.2)
Scenario: crew dispatch optimisation. Persona: Field Dispatcher. Bundles ER-A07/A08 + ORCH-19. Gate: ACK_ONLY. Prereqs: MS Field Service + GIS + SAP PM.

**APEX-ER-REG-05 — Regulatory Event Response** (Enterprise · GA v1.2)
Scenario: FERC / PUC regulatory event. Persona: Regulatory Affairs. Bundles ER-A09/A10 + ORCH-20. Gate: ESCALATION. Prereqs: FERC + state PUC portals + SOX.

### Architecture Components (ER)

- Canonical Silver schemas: ERCML (full family)
- Primary SORs: SAP ISU, AMI head-end, SCADA, OMS, DMS, CIS, MS Field Service, FERC feed
- Capacity: F32 baseline for grid telemetry volume
- Identity: grid-ops-engineer, meter-ops-lead, field-dispatcher, billing-ops-analyst, regulatory-affairs

### 4.8 Implementation Roadmap (ER)

**Wave 1** · $3–5M · MTR-01 + BIL-03 on pilot region
**Wave 2** · $5–8M · Add FWO-04, rollout MTR+BIL to full territory
**Wave 3** · $4–7M · GRD-02 pilot (most consequential, strictest gate); REG-05 at enterprise scale

---

## Chapter 5: Industrial & Manufacturing (AXLE) Practice

### 5.1 The Story

At 09:14 on a Thursday, Line 6 at a tier-1 automotive stamping facility halts. The press is down. Every minute costs the plant between $3,000 and $8,000 depending on the model running. Traditionally the triage is manual: the plant supervisor calls the tool-and-die lead, they walk down, they look, they discuss, they call maintenance. Ten to twenty minutes before root-cause hypothesis. With `APEX-AXLE-LDT-01` running, the classification — mechanical vs. material vs. quality vs. operator — lands on the supervisor's device within 60 seconds of the halt, with specific recommendations and a HITL card.

### 5.2 The Relationship to the AXLE Programme

APEX's AXLE Practice is **complementary to, not a replacement for**, the full AXLE programme. The AXLE Comprehensive Solutions Reference details a fourteen-chapter strategic programme for automotive-adjacent manufacturing; this chapter summarises how AXLE-as-APEX-practice fits into a multi-industry APEX deployment.

Clients adopting APEX multi-industry will typically take the AXLE Practice's five services as part of a cross-industry programme. Clients adopting AXLE as their strategic manufacturing transformation will use the full AXLE programme and may reference APEX-AXLE services inside it. The overlap is deliberate and additive.

### 5.3 AI Integration & Human Reality (AXLE in APEX)

Personas: plant supervisor, quality engineer, supply chain planner, plant manager, recall coordinator. See Appendix C.

Baseline typically **Level 2**. Wave 1 targets Level 3 on LDT-01 and KPI-05. Strict gates retained for QEX-02 and RCL-04.

### 5.4 Solution Portfolio (AXLE in APEX)

Five services summarised; full AXLE programme in the separate AXLE Comprehensive Reference:

- **APEX-AXLE-LDT-01 — Line-Down Triage** · HITL gate · Plant Supervisor primary
- **APEX-AXLE-QEX-02 — Quality Excursion Response** · HITL gate · Quality Engineer primary
- **APEX-AXLE-SCD-03 — Supply-Chain Disruption** · ACK_ONLY · Supply Planner primary
- **APEX-AXLE-RCL-04 — Recall Traceability** · ESCALATION · Recall Coordinator primary
- **APEX-AXLE-KPI-05 — Plant KPI Drift** · ACK_ONLY · Plant Manager primary

### 5.5 Implementation Roadmap (AXLE Practice)

Typical Wave 1 · $4–6M · LDT-01 + KPI-05 at one plant
Typical Wave 2 · $6–10M · Add QEX-02 + SCD-03 at plant-group level
Typical Wave 3 · $4–6M · RCL-04 enterprise-wide; consider graduating into the full AXLE programme if the client commits to that trajectory.

---

# Part III — Cross-Practice Capabilities

Every APEX deployment uses a shared set of capabilities that cut across Practices. These are not optional add-ons; they are the platform spine.

## Chapter 6: Shared Services

Six utility MCP servers ship with every APEX deployment, regardless of which Practices are subscribed. They are the seam between Practice-specific content and the platform's governance, identity, and audit machinery.

**`fabric-mcp` — Generic Gold-view gateway.** When an agent needs a feature view not covered by a domain MCP, it reads through `fabric-mcp`. All reads are tenant-scoped, managed-identity-authenticated, and trace-instrumented.

**`policy-mcp` — HITL gate resolution and upgrade-policy lookup.** Converts a decision's SemVer bump class into the tenant's chosen gate, looking up the tenant manifest's `auto_upgrade_policy`. Also handles RBAC checks against persona catalog assignments.

**`telemetry-mcp` — Trace event emission.** Threads App Insights `operation_Id` across every agent call, tool call, and HITL wait. The service that makes the Azure Monitor workbook possible.

**`approvals-mcp` — Teams / Power Automate adaptive-card orchestrator.** Sends decision cards to approvers; polls for decision; returns result. Implements timeout and escalation paths.

**`tokenizer-mcp` — PII tokenisation and audit-logged reverse-lookup.** Stable, reversible-only-with-audit. Honours consent flags. The critical seam where compliance is enforced programmatically, not by convention.

**`ledger-mcp` — Staging for write-offs, corrections, adjustments.** Every write-back to an SOR or internal ledger goes through here first, staged and audit-logged before execution.

Together these six servers are the **platform contract**. A Practice that bypasses them is out of compliance with Core.

## Chapter 7: Observability & Trust

APEX's observability is designed around a single principle: **every consequential event gets one operation_Id that stitches the end-to-end story**. From SOR event to Bronze write to Silver transform to EventGrid publish to orchestration start to agent invocation to MCP tool calls to HITL wait to decision audit row to rollback pointer — one trace, one ID, one queryable history.

### The One Workbook

Every APEX deployment ships with a single Azure Monitor workbook that answers, for any tenant, five questions at once:

1. **Is the orchestration succeeding?** (24h orchestration success rate, per orchestration_id)
2. **Is the decision arriving on time?** (mean-time-to-decision, p50/p95/p99)
3. **Is the HITL queue healthy?** (real-time queue depth per gate owner)
4. **Has anything drifted?** (schema drift incidents over 7 days)
5. **Are the tools healthy?** (MCP tool failure rate per tool, 24h)

Every panel ties to an alerting rule that pages the owning team when SLOs burn. Every panel has per-tenant scoping.

### Trust, Audit, and the Regulatory Posture

APEX's audit trail is not an afterthought. `silver_decision_audit` is a first-class Silver table with:

- Append-only writes (no UPDATE, no DELETE)
- Customer-managed keys
- ACL write-once with broad read for compliance officers and observability managed identity
- Retention per practice compliance policy (7 years HLS/ER under SOX; 5 years RC/AXLE default; longer per contract)
- Exportable in a form that regulators have accepted in engagements to date

This is the single biggest differentiator in conversations with compliance officers. It is not an advantage measurable in ROI; it is a **floor**.

## Chapter 8: Versioning, Governance, and HITL Gates

### The Manifest Lifecycle

Every APEX artifact — schemas, practices, agents, orchestrations, services, tenants — lives under SemVer discipline. Every change is classified MAJOR / MINOR / PATCH deterministically. Every classification maps to a default HITL gate. Every tenant overrides defaults via policy.

The automation is **deterministic, not contested**. `classify-bump.js` returns the same answer for the same diff every time. The political debate about "how significant is this change?" is moved out of Slack and into code.

### The Gate Matrix

```
                Default gate    Tenant can override to
PATCH           ZERO_TOUCH      ACK_ONLY or HITL
MINOR           ACK_ONLY        ZERO_TOUCH or HITL
MAJOR           HITL            ACK_ONLY (never ZERO_TOUCH for MAJOR)
```

High-risk tenants (HIPAA health systems, critical-infrastructure utilities) commonly set `MINOR → HITL` globally. Low-risk tenants (retail pilots, single-plant AXLE deployments) may set `MINOR → ZERO_TOUCH` on selected non-consequential services.

### Canary Release Discipline

Every agent version reaching Prod takes **5% of traffic for 72 hours** before full cutover. Rollback criteria are encoded in the release manifest, and any SLO burn rolls traffic back automatically with a page to the owning team. The client never sees a bad release — bad releases roll themselves back.

---

# Part IV — Implementation & Delivery

## Chapter 9: The Three-Wave Deployment

The APEX delivery pattern is three waves of roughly six months each. Each wave has crisp exit criteria tied to measurable outcomes, not tooling milestones.

### Wave 1 — Foundation (months 1–6)

**Investment envelope:** $3–8M per Practice, typically $4–6M for the first Practice.

**Deliverables:**
- Fabric workspace topology stood up (Dev/Test/Prod × Practice/Tenant)
- Identity groups and managed identities provisioned
- First Practice's canonical schemas deployed; `validate-practice` green
- 2–3 services from the first Practice live in one pilot tenant
- First HITL decisions flowing; decision audit rows accumulating
- Azure Monitor workbook operational

**Exit criteria (all must hold):**
- ≥ 30 days continuous HITL decision flow at pilot
- SLOs met for ≥ 21 consecutive days
- ≥ 3 KPIs trending on or above target
- Stakeholder sign-off for Wave 2 scope

### Wave 2 — Intelligence (months 7–12)

**Investment envelope:** $5–12M per Practice.

**Deliverables:**
- Full service catalogue of the first Practice live at pilot scale
- Gate-tuning on mature services (HITL → ACK_ONLY where proven)
- Second tenant onboarded (or pilot → production rollout)
- Cross-practice shared services fully instrumented
- Compliance evidence pack reviewed with the client's audit function

**Exit criteria:**
- Full Practice catalogue at pilot scale
- Gate-tuning approved for at least one service
- Compliance pack accepted
- Manager-touch-time KPI ≥ 60% improvement from baseline on at least two services

### Wave 3 — Optimisation (months 13–18)

**Investment envelope:** $3–6M per Practice.

**Deliverables:**
- Full rollout of the first Practice at enterprise scale
- Optional: add a second Practice at Wave-1 level, running Waves 1 and 2 in parallel
- Cross-practice orchestrations piloted (e.g., a supply-expiry event in HLS that triggers a recall trace in AXLE)
- Level-5 autonomous pilot on one or two narrowly bounded services

**Exit criteria:**
- Enterprise-scale KPI trends on-target
- Second Practice subscribed (if client path includes multi-Practice)
- Autonomous pilot cleared by audit review

## Chapter 10: Onboarding a New Tenant

The onboarding of a new tenant is a defined sequence with known durations. A typical tenant onboarding runs 4–6 weeks end-to-end.

**Week 1 — Provision.** Create the three tenant workspaces (dev/test/prod). Apply identity groups. Shortcut the Practice workspace's reference tables. Deploy the tenant manifest.

**Week 2 — Connect.** Stand up SOR connectors (Eventstream / Mirrored DB / Data Pipeline / Dataflow Gen2 depending on SOR). Land Bronze data. Verify row counts and latency.

**Weeks 3–4 — Canonicalise.** Run Silver transforms; apply PII tokenisation; verify canonical envelope compliance. Deploy Gold feature views. Agents can now read.

**Week 5 — Shadow.** Run the subscribed services in shadow mode (decisions generated, logged, but not acted). Calibrate against the client's prior human decisions. Tune thresholds.

**Week 6 — Go live.** First live HITL decisions. Monitor hourly for three days, daily for three weeks. Hand over to steady-state operations.

## Chapter 11: Scaling the Service Portfolio

Once Wave 1 is live, adding services to an existing tenant follows a much shorter cadence — typically 2–4 weeks per service, because the workspace topology, identity, and monitoring are reusable.

The cost envelope for adding a service to a running tenant is **$200K–$600K** depending on SOR connections required. This is the math that makes the catalogue's growth pattern realistic: clients don't add services one a year; they add them two or three a quarter once the platform is live.

---

# Part V — Future State

## Chapter 12: The Autonomous Enterprise

By the end of Wave 3, a client's APEX deployment looks like this:

- Two to three Practices live with their full service catalogues
- Consistent Level 4 operation on the majority of services; Level 5 pilot on two to four
- Manager touch-time 60–80% below baseline across services
- Decision audit rows as the single source of truth for compliance reconstruction
- Cross-practice orchestrations introducing genuinely novel decision flows (a supply-expiry event in HLS that queries the pharma-recall feed and opens a case in the AXLE recall-traceability service)

What comes next is incremental. Level 5 is not a step-change; it is a graduated trust reallocation where specific services, on the evidence of 6–12 months of Level 4 quality, have their gates removed with audit approval. No dramatic product launch. Just continued, disciplined movement up the maturity ladder.

The autonomous enterprise is not "no humans in the loop." It is **humans in the loop on the decisions that warrant them**, with everything else running silently, audibly, and correctly.

---

# Appendix A: APEX Schema Reference

Canonical schema families, by Practice. Every entity carries the five-field envelope (`event_id`, `event_ts`, `entity_id`, `source_system`, `source_system_ts`) plus `pii_tokenized` and, where applicable, `scd2_current`.

## SCML — Supply-Chain Markup Language

Used across RC, HLS, and AXLE. Entities include COLD_CHAIN_TELEMETRY, TEMPERATURE_EXCURSION, ASN, STORE_RECEIVING_EVENT, RECEIVING_DISCREPANCY, DSD_INVOICE, RECALL_NOTICE, LOT_TRACE, LOT_EXPIRATION_STATE.

## MERML — Merchandising Markup Language

RC Practice. Entities include STORE_INVENTORY_POSITION, PRICE_RECORD, PRICE_TAG_STATUS, PROMOTION_ACTIVATION, OSA_EVENT, POS_VOID, SHRINK_EVENT, CYCLE_COUNT_VARIANCE, MARKDOWN_EVENT, WASTE_EVENT.

## CXML — Customer Experience Markup Language

RC and HLS Practices. Entities include FULFILLMENT_ORDER, PICK_EXCEPTION, SUBSTITUTION_EVENT, LOYALTY_STATE, CUSTOMER_INCIDENT.

## HLSCML — Healthcare & Life Sciences Markup Language

HLS Practice. Entities include PATIENT_ENCOUNTER (PHI-tokenised), CLINICAL_OBSERVATION, CARE_PLAN, VITALS, LAB_RESULT, CLAIM_DENIAL, CODING_RECORD, TRIAL_PROTOCOL, ELIGIBILITY_CRITERIA, PATIENT_SAFETY_EVENT, INCIDENT_CLASSIFICATION.

## ERCML — Energy & Resources Markup Language

ER Practice. Entities include METER_READING, OUTAGE_EVENT, GRID_ANOMALY, CUSTOMER_SERVICE_STATE, SCADA_TELEMETRY, BILLING_EXCEPTION, RATE_SCHEDULE, WORK_ORDER, CREW_STATE, ASSET_HEALTH, REGULATORY_EVENT, RELIABILITY_METRIC.

## AXLECML — Industrial & Manufacturing Markup Language

AXLE Practice. Entities include PRODUCTION_EVENT, ASSET_HEALTH, MATERIAL_FLOW, QUALITY_EXCURSION, GENEALOGY, PRODUCT_LOT, SUPPLIER_EVENT, PURCHASE_ORDER, INVENTORY_POSITION, RECALL_NOTICE, SHIPMENT, KPI_SNAPSHOT.

Full per-entity reference — including column lists, SCD2 status, PII classes, and change history — is in the companion per-Practice build specs.

---

# Appendix B: Service Catalog Master Registry

All 24 services at a glance. One line per service: ID, name, Practice, tier, primary persona, gate, Core version.

| ID | Name | Practice | Tier | Primary persona | Gate | Version |
|---|---|---|---|---|---|---|
| APEX-RC-CXP-01 | Cold Chain Excursion Response | RC | Pro / Ent | Store MOD | HITL | 1.2.0 GA |
| APEX-RC-RVD-02 | Receiving Variance Dispute | RC | Ess / Pro / Ent | Store MOD | ACK_ONLY | 1.2.0 GA |
| APEX-RC-ESL-03 | ESL Pricing Integrity | RC | Pro / Ent | Merch Analyst | ACK_ONLY | 1.2.0 GA |
| APEX-RC-OSA-04 | Phantom-OOS Detection | RC | Pro / Ent | Store MOD | ACK_ONLY | 1.2.0 GA |
| APEX-RC-RCL-05 | Recall Response | RC | Enterprise | Compliance Officer | ESCALATION | 1.2.0 GA |
| APEX-RC-BPX-06 | BOPIS Exception Handling | RC | Pro / Ent | Customer Care Agent | HITL | 1.2.0 GA |
| APEX-RC-SHK-07 | Shrink & Void Anomaly | RC | Enterprise | Loss Prevention Lead | ESCALATION | 1.2.0 GA |
| APEX-RC-CXI-08 | Customer Incident Triage | RC | Pro / Ent | Customer Care Agent | HITL | 1.2.0 GA |
| APEX-HLS-DSR-01 | Discharge Ready Surveillance | HLS | Pro / Ent | Charge Nurse | ACK_ONLY | 1.2.0 GA |
| APEX-HLS-SEP-02 | Sepsis Early Warning | HLS | Enterprise | Charge Nurse | HITL | 1.2.0 GA |
| APEX-HLS-RVC-03 | Revenue-Cycle Denial Recovery | HLS | Pro / Ent | Rev-Cycle Analyst | HITL | 1.2.0 GA |
| APEX-HLS-SUP-04 | Supply Expiry Management | HLS | Pro / Ent | Pharmacy Supply Lead | ACK_ONLY | 1.2.0 GA |
| APEX-HLS-CTM-05 | Clinical Trial Matching | HLS | Pro / Ent | Trial Coordinator | HITL | 1.2.0 GA |
| APEX-HLS-PSI-06 | Patient Safety Incident | HLS | Enterprise | Patient Safety Officer | ESCALATION | 1.2.0 GA |
| APEX-ER-MTR-01 | Meter Outage Detection | ER | Pro / Ent | Meter Ops Lead | ACK_ONLY | 1.2.0 GA |
| APEX-ER-GRD-02 | Grid Anomaly Response | ER | Enterprise | Grid Ops Engineer | HITL | 1.2.0 GA |
| APEX-ER-BIL-03 | Billing Exception Handling | ER | Pro / Ent | Billing Ops Analyst | ACK_ONLY | 1.2.0 GA |
| APEX-ER-FWO-04 | Field Work-Order Optimisation | ER | Pro / Ent | Field Dispatcher | ACK_ONLY | 1.2.0 GA |
| APEX-ER-REG-05 | Regulatory Event Response | ER | Enterprise | Regulatory Affairs | ESCALATION | 1.2.0 GA |
| APEX-AXLE-LDT-01 | Line-Down Triage | AXLE | Pro / Ent | Plant Supervisor | HITL | 1.2.0 GA |
| APEX-AXLE-QEX-02 | Quality Excursion Response | AXLE | Enterprise | Quality Engineer | HITL | 1.2.0 GA |
| APEX-AXLE-SCD-03 | Supply-Chain Disruption | AXLE | Pro / Ent | Supply Planner | ACK_ONLY | 1.2.0 GA |
| APEX-AXLE-RCL-04 | Recall Traceability | AXLE | Enterprise | Recall Coordinator | ESCALATION | 1.2.0 GA |
| APEX-AXLE-KPI-05 | Plant KPI Drift | AXLE | Pro / Ent | Plant Manager | ACK_ONLY | 1.2.0 GA |

---

# Appendix C: Persona Catalog

The 22 personas defined in `persona-catalog.json`. Each service's `personas.primary` and `.secondary` references these IDs.

| ID | Name | Practices | One-line role |
|---|---|---|---|
| store-mod | Store Manager on Duty | RC | Front-line shift owner; primary HITL approver for in-store decisions |
| regional-ops-director | Regional Operations Director | RC | Cluster oversight; escalation target for multi-store patterns |
| compliance-officer | Compliance Officer | RC / HLS / ER | Regulatory accountability; consumes recall & incident output |
| merchandising-analyst | Merchandising Analyst | RC | Price, assortment, ESL state; pricing-integrity decisions |
| loss-prevention-lead | Loss Prevention Lead | RC | Shrink investigations; consumes escalations |
| customer-care-agent | Customer Care Agent | RC / HLS / ER | Customer-facing resolver; substitution and incident gates |
| charge-nurse | Charge Nurse | HLS | Unit-level clinical lead; HITL for clinical surveillance |
| clinical-informaticist | Clinical Informaticist | HLS | Bridges clinical workflow and data |
| revenue-cycle-analyst | Revenue Cycle Analyst | HLS | Denials, claims, reimbursement |
| supply-chain-pharm | Pharmacy Supply Lead | HLS | Medication and supply expiry |
| trial-coordinator | Clinical Trial Coordinator | HLS | Patient-trial matching and enrolment |
| patient-safety-officer | Patient Safety Officer | HLS | Incident review and reporting |
| grid-ops-engineer | Grid Operations Engineer | ER | Real-time grid state; HITL for anomaly responses |
| field-dispatcher | Field Dispatcher | ER | Work-order optimisation and crew assignment |
| meter-ops-lead | Meter Operations Lead | ER | Meter reading, outage detection, revenue assurance |
| billing-ops-analyst | Billing Operations Analyst | ER | Billing-exception resolution |
| regulatory-affairs | Regulatory Affairs Officer | ER / HLS | Regulatory filings and compliance events |
| plant-supervisor | Plant Floor Supervisor | AXLE | Shift-level production lead; HITL for line-down |
| quality-engineer | Quality Engineer | AXLE | Quality excursions, traceability, CAPA |
| supply-chain-planner | Supply Chain Planner | AXLE / RC | Supply-disruption triage and expediting |
| plant-manager | Plant Manager | AXLE | Plant-wide KPIs, executive escalation |
| recall-coordinator | Recall Coordinator | AXLE / RC / HLS | Traceability and customer notification for recalls |

---

# Appendix D: MCP Tool Catalog

MCP servers organised by class. Each server exposes one or more tools; only representative tool names shown.

## Domain Servers

- **scml-mcp** — `read_cold_chain_telemetry`, `read_excursion_events`, `read_lot_trace`, `read_asn`, `read_receiving_variance`
- **merml-mcp** — `read_store_inventory`, `read_price_record`, `read_tag_status`, `read_osa_event`, `read_void_record`
- **cxml-mcp** — `read_fulfillment_order`, `read_pick_exception`, `read_customer_incident`, `read_loyalty_state`
- **hlscml-mcp** — `read_patient_encounter`, `read_vitals`, `read_lab_result`, `read_claim_denial`, `read_trial_match`
- **ercml-mcp** — `read_meter_reading`, `read_grid_anomaly`, `read_outage_event`, `read_work_order`, `read_billing_exception`
- **axlecml-mcp** — `read_production_event`, `read_quality_excursion`, `read_genealogy`, `read_supplier_event`

## Utility Servers

- **fabric-mcp** — generic Gold-view reads
- **policy-mcp** — `resolve_gate`, `get_upgrade_policy`, `verify_tenant_access`
- **telemetry-mcp** — `emit_trace_event`, `emit_decision_audit`
- **approvals-mcp** — `send_teams_card`, `poll_decision`, `escalate`
- **tokenizer-mcp** — `tokenize`, `reverse_tokenize` (audit-logged), `lookup_consent`
- **ledger-mcp** — `stage_writeoff`, `stage_credit`, `stage_correction`

## External Servers

- **fda-mcp** — FDA recall & threshold feeds
- **ferc-mcp** — FERC regulatory notice feed
- **edi-mcp** — EDI 856/850/810 vendor messaging
- **pharma-recall-mcp** — pharma-specific recall feeds
- **trials-registry-mcp** — ClinicalTrials.gov lookup
- **nhtsa-mcp** — NHTSA recall feed (AXLE RCL-04)
- **scada-mcp** — SCADA telemetry adapters (ER GRD-02)
- **sap-qm-mcp** — SAP Quality Management integration (AXLE QEX-02, RCL-04)

---

# Appendix E: Microsoft Product & SKU Reference

APEX consumes the following Microsoft products. Each client deployment is sized based on the services subscribed.

| Product | Role in APEX | Typical SKU for a Wave-1 deployment |
|---|---|---|
| Microsoft Fabric | Data plane (OneLake, Lakehouse, Warehouse, Eventstream) | F8 entry · F16 common · F32 for high-volume |
| Azure AI Foundry | Agent authoring + AI Search + embeddings | Pay-as-you-go |
| Azure AI Agent Service | Agent runtime | Pay-as-you-go |
| Azure OpenAI | Foundation models (gpt-4.1 / reasoning tier) | Pay-per-token |
| Logic Apps Standard | Declarative orchestrations | Standard plan |
| Durable Functions | Stateful orchestrations | Elastic Premium for reliability |
| Azure Container Apps | MCP server hosting | Consumption or dedicated |
| Entra ID P2 | Identity, managed identity, conditional access | Per-user |
| Microsoft Purview | Lineage, DLP, sensitivity labels | Per-capacity |
| Microsoft Defender for Cloud | Security posture | Per-resource |
| Azure Monitor / App Insights / Log Analytics | Observability | Pay-per-GB |
| Microsoft Teams | HITL approval UI | M365 E5 |
| Power Platform | Dashboards, approval flows, admin tools | Per-app or per-user |
| Copilot Studio | Optional conversational surfaces | Per-environment |

Most clients can map APEX consumption onto an existing Microsoft EA without net-new licensing beyond the Fabric capacity and the pay-as-you-go AI spend.

---

# Appendix F: Partner Ecosystem

APEX is delivered as a Deloitte-Microsoft joint offering. Third-party partners extend specific Practices:

- **RC**: Manhattan Associates (WMS), Coca-Cola Beverages (DSD reference integration), Monnit (IoT), Honeywell-Vocollect (voice-pick integration optional)
- **HLS**: Epic, Oracle Health (Cerner), Infor Lawson (rev-cycle), IQVIA (trials registry)
- **ER**: SAP ISU, OSIsoft PI, GE GridOS, Itron (AMI)
- **AXLE**: Rockwell FactoryTalk, PTC ThingWorx, Siemens Opcenter, Plex MES

Partner integrations land at the Bronze ingest layer via the matching Mirrored Database, Eventstream, or Pipeline pattern. None of them influence the Silver canonical contract.

---

# Appendix G: Glossary

**Agent.** A reasoning component that runs in Azure AI Agent Service. Has a system prompt, tool allow-list, model, and manifest.

**ACK_ONLY.** A HITL gate kind meaning "notify + auto-apply." Default for MINOR bumps.

**Bronze.** The Medallion layer where SOR data lands in SOR-native shape. Read-only for Silver transforms.

**Canonical envelope.** Five universal fields on every Silver row: `event_id`, `event_ts`, `entity_id`, `source_system`, `source_system_ts`.

**Classify-bump.** The deterministic SemVer classifier at `apex-core/tools/classify-bump.js`. Returns MAJOR / MINOR / PATCH given before-and-after manifest state.

**Contract (L1).** The normative apex-core specification.

**Decision audit row.** Append-only Silver row capturing every HITL decision, its inputs, outputs, approver, rationale, and rollback pointer.

**Durable Functions.** Azure's stateful orchestrator runtime. APEX uses it for long-running orchestrations.

**Edition (L2).** A versioned release of Core.

**Entra ID.** Microsoft's identity platform (formerly Azure AD).

**ESCALATION.** A HITL gate kind meaning "route to a cross-functional owner."

**Eventstream.** Fabric's real-time ingest item. Sink target is Bronze Delta.

**Fabric.** Microsoft's unified SaaS data platform. APEX's data plane.

**Fleet.** Deprecated — see *Practice*. `validate-fleet.js` is a backward-compat shim retained through Core v1.2.x.

**Gold.** The Medallion layer with materialised feature views read by agents via MCP.

**HITL.** Human-in-the-Loop. The gate kind requiring human approval.

**L1 / L2 / L3 / L4.** The four APEX lifecycle layers — Contract, Edition, Practice, Tenant.

**Logic Apps.** Azure's declarative orchestration runtime. APEX uses it for short-running orchestrations.

**Managed identity.** An Azure-managed service principal tied to a resource. Used for service-to-service auth without secrets.

**Manifest.** A JSON document declaring the shape/version/content of an APEX artifact.

**MCP.** Model Context Protocol. The open standard for typed agent-tool contracts.

**Medallion.** The Bronze/Silver/Gold data architecture APEX uses in Fabric.

**OneLake.** Fabric's cross-workspace storage layer.

**Orchestration.** A DAG of agent calls with a HITL gate at the decision. Named `ORCH-nn`.

**Persona.** A role that interacts with an APEX service. Catalogued in `persona-catalog.json`.

**Practice (L3).** An industry-specific bundle of schemas + agents + MCP tools + orchestrations + gates + services + personas + KPIs. Renamed from "Fleet" in Core v1.2.1.

**Purview.** Microsoft's data governance product. Used for lineage, DLP, labels.

**SCD2.** Slowly Changing Dimension Type 2 — historical-record pattern.

**Service.** A subscribable SKU. Bundles schemas, agents, MCP tools, orchestration, and a gate. ID format `APEX-<practice>-<domain>-<nn>`.

**Silver.** The Medallion layer holding canonicalised, tokenised, contract-compliant data.

**SLO.** Service Level Objective. APEX-standard keys: `detection_p95_sec`, `decision_p95_min`, `false_positive_rate`, `availability_pct`.

**SOR.** System of Record.

**Tenant (L4).** A client's APEX instance.

**Tokenisation.** Replacement of a PII value with a stable opaque token at the Silver boundary.

**Trace.** An App Insights operation chain stitching every downstream event under one operation_Id.

**Workspace.** A Fabric organisational unit. APEX uses per-Practice and per-Tenant workspaces.

**ZERO_TOUCH.** A HITL gate kind meaning "apply silently." Default for PATCH bumps.

---

*End of APEX Comprehensive Solutions Reference v1.0.*

