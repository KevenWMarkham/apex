# Episode 03 · The Four Pillars

**Source:** *Professional APEX-M Sellers Guide* — Part II, Chapters 5–8 (Fabric · Foundry · Copilot · Purview)
**Run time:** 30 minutes (≈ 5,000 words)
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: whiteboard squeak, light meeting hum]

**KEVEN:** Late last year I was in a meeting with three Deloitte partners and four Microsoft directors trying to qualify a deal at a global pharmaceutical company. And I will never forget the moment we lost it. The Microsoft side was pitching Foundry — *here are the models, here is the agent orchestration, here is the safety stack* — and the Deloitte side was pitching Fabric — *here is the data foundation, here is the medallion, here is OneLake* — and the head of the client's AI center of excellence looks at us and says, *"Are these the same product or two different products?"*

[pause]

**JORDAN:** Oh no.

**KEVEN:** And in that moment I realised — every seller in that room knew their *pillar.* Nobody could position the *composition.* The reason we lost — well, the reason we *paused* the deal, which is a polite loss — is that the buyer couldn't tell where one product ended and the next began. So today's episode is the one that fixes that.

**JORDAN:** I'm Jordan.

**KEVEN:** I'm Keven Markham. APEX Sellers Podcast, Episode Three. *The Four Pillars.*

---

## Theme Statement

**KEVEN:** Part Two of the Sellers Guide is four chapters — Fabric, Foundry, Copilot, Purview. We're going to do all four in thirty minutes. The discipline here is not to go deep on any one — the Sellers Guide is the depth. The discipline is to teach you to *position all four in the same conversation* without contradicting yourself.

**JORDAN:** And the punchline you're aiming for —

**KEVEN:** The punchline is — Fabric is *where the data lives*, Foundry is *where the agent thinks*, Copilot is *where the user types*, Purview is *what the auditor reads*. If you remember nothing else, remember that sentence. It's the one I should have had in the pharma meeting.

**JORDAN:** Let's go.

---

## The Story

### Pillar One — Fabric (Chapter 5)

**KEVEN:** Microsoft Fabric. The unified data plane. Chapter Five is the longest chapter in the Sellers Guide for a reason — Fabric is the foundation, and most sellers under-position it because Fabric feels less exciting than agents.

**JORDAN:** Open with the definition.

**KEVEN:** Fabric is a *unified SaaS data platform* that combines what used to be Synapse, Data Factory, Power BI, Real-Time Intelligence, and OneLake into a single SKU on Azure. The technical innovation is OneLake — *one* logical data lake, with shortcuts and mirroring across every workload. The commercial innovation is the *capacity unit* — you buy a capacity number, and that capacity covers all the workloads.

**JORDAN:** And why does APEX need Fabric specifically?

**KEVEN:** Section five point one, but let me boil it down. Three reasons.

One — *the medallion is built in.* Bronze, Silver, Gold layers are first-class Fabric constructs. APEX's canonical schemas anchor at the Silver layer day one — Silver is where canonical meaning lives in the framework.

Two — *agents need a Gold view to query.* Foundry agents call out to data through APEX's MCP servers. The MCP servers need a stable, joinable, semantically-consistent data layer. Fabric Gold *is* that layer.

Three — *Purview lineage is native.* Every Fabric artefact is automatically classified, lineaged, and audit-traced in Purview. That's the audit half of APEX.

**JORDAN:** The five Fabric integration patterns. Section five point two. Quickly.

**KEVEN:** Five patterns, and you should know which one to recommend for which kind of source.

**Pattern One — Mirrored Database (CDC).** Real-time mirroring from operational databases. SQL Server, Postgres, Cosmos DB. The data appears in Fabric within seconds. Use when the source is operational and the agent needs near-real-time.

**Pattern Two — Eventstream / Eventhouse.** Real-time event ingestion. IoT, telemetry, application logs. Use for streaming workloads.

**Pattern Three — Data Pipeline (scheduled batch).** Classic ETL. Use when the source is a SaaS app with batch export, or when intraday is acceptable.

**Pattern Four — Dataflow Gen2 (REST pull).** API-driven pull. Use when you need light transformation in transit and the source has a REST endpoint.

**Pattern Five — Custom Endpoint (webhook).** Push from the source into Fabric. Use when the source can push but can't be mirrored.

**JORDAN:** And how do you pick?

**KEVEN:** Section five point two — the pattern selection decision. Two questions. Is the source operational or analytical? Is the latency requirement minutes, seconds, or sub-second? Those two answers narrow you to one or two patterns. The Sellers Guide has the decision table.

**JORDAN:** Capacity sizing. Section five point three. Sellers always get asked.

**KEVEN:** Yeah. The rule of thumb in the Sellers Guide — Wave One for a mid-market enterprise is typically an F64 capacity. Wave Two scales to F128 or F256 depending on agent volume and BI overlay. Sovereign workloads, regulated industries, go to dedicated capacities. The capacity-sizing conversation is *advisory* — you guide the client through the workload analysis, the client signs the capacity purchase with Microsoft.

**JORDAN:** Co-existence with Databricks and Snowflake. Section five point — what is it — section on co-existence. Because every Fortune-500 has one or both.

**KEVEN:** Right. And the line in the Sellers Guide that I want every listener to memorise — *"We are Fabric-first. We are not Fabric-only."* Section five point — the "honest positioning" section.

Three interop patterns with Databricks — Delta share between Fabric and Databricks, Fabric mirroring of Databricks Unity Catalog, and side-by-side workspace patterns. Each one fits a different state of the client. Section five point — Fabric-Databricks co-existence.

With Snowflake — same shape, three patterns. Section right after.

**JORDAN:** And the honest position.

**KEVEN:** Honest position — Fabric is the *primary data plane for APEX agents.* Databricks and Snowflake co-exist for the workloads they already serve, and we don't try to displace them in Wave One. Wave Two may consolidate, or may not, depending on the client's economics. We don't argue the platform — we deliver agentic value on Fabric and let the data-platform conversation evolve.

### Pillar Two — Foundry (Chapter 6)

**JORDAN:** OK. Foundry. Pillar two. The intelligence plane.

**KEVEN:** Azure AI Foundry. It is *the* Microsoft platform for agent development and operation. The Foundry value proposition in one sentence — section six point one — *"Foundry is the unified runtime for model-based intelligence, agent orchestration, and the safety, evaluation, and observability planes that surround them."*

**JORDAN:** Let me push. Microsoft has Azure OpenAI, Azure AI Foundry, Azure AI Agent Service, and the new Microsoft Agent Framework. How do these relate?

**KEVEN:** Great question and the Sellers Guide is direct on this — section six point two.

- **Azure OpenAI** — the underlying model API. GPT-4o, GPT-4.1, o1, etc. The thing the agent calls under the hood.
- **Azure AI Foundry** — the unified *platform* for building, evaluating, deploying agents and the surrounding safety / observability planes.
- **Azure AI Agent Service** — the *runtime service* inside Foundry that hosts the agent loop, tool calls, and approval flows.
- **Microsoft Agent Framework** — the *SDK* — the code you write to define the agent. Hosts on Foundry / Agent Service in production.

**JORDAN:** So the cleanest mapping —

**KEVEN:** *Agent Framework* is what the engineer writes. *Foundry* is where it runs. *OpenAI* is what it thinks with. *Agent Service* is the runtime service that wires it together.

**JORDAN:** Section six point nine — agent orchestration patterns. The multi-agent pattern library.

**KEVEN:** Yeah. Six patterns, and every Service in APEX uses one of them.

**Sequential** — agents run in order, output feeds the next. Most common pattern for root-cause investigation.

**Parallel-fan-out** — one parent agent dispatches to N child agents in parallel, aggregates results. Used when you need to examine many cohorts at once.

**Hierarchical** — a parent agent supervises child agents that each have their own tools. The most common APEX pattern.

**Loop / iterate** — an agent re-runs itself until a quality threshold is met. Used in writing, classification, and proposal generation.

**Debate** — two agents argue, a third adjudicates. Used in clinical decision support, in regulatory pattern matching.

**Router** — an agent picks which downstream agent or tool to call. Used at the top of complex orchestrations.

**JORDAN:** And the *parent-child* pattern specifically — section six point thirteen.

**KEVEN:** That's the control-plane pattern that makes APEX orchestrations auditable. The parent agent owns the audit trail. Child agents emit local trace, parent stitches the trail together, audit echo lands in Purview. The Sellers Guide spends fifty lines on this because the audit row is the thing the CCO cares about, and parent-child is how it works.

**JORDAN:** Section six point ten — the APEX audit row.

**KEVEN:** Memorise this one. Every agent call emits a row with — *who called* (persona), *what was called* (tool), *with what input* (parameters), *with what output* (result), *under what policy* (Purview classification), *at what timestamp* (immutable). That row is hash-chained, written to OneLake, echoed to Purview's audit. That's the chain of custody. That's the artefact your client's auditor reads.

**JORDAN:** Section six point twelve — file-first context. This is a Keven hobby horse.

**KEVEN:** [slight laugh] OK, briefly. File-first context is the APEX position that *context loaded from files* beats *context loaded from knowledge graphs or vector databases* for most enterprise agent workloads. Reasons — files are version-controlled, files are auditable, files are stable across model versions. Knowledge graphs and vectors have a role — they are *not* the primary context mechanism in APEX. Section six point twelve has the full argument. We'll re-visit this in Episode Seven.

**JORDAN:** Foundry capacity and cost.

**KEVEN:** Section six point eight. Capacity is bought as PTUs — Provisioned Throughput Units — for steady workloads, or pay-as-you-go for variable. The cost conversation with the CFO is — *PTUs for the predictable agents, PAYG for the discovery and exploration workloads.* Mid-market Wave One Foundry consumption is typically 350K to 700K dollars annualised, which we covered last episode.

### Pillar Three — Copilot (Chapter 7)

**JORDAN:** Pillar three. Copilot. Chapter seven. And this one is interesting because most clients *already have* Copilot.

**KEVEN:** Right. And the position APEX takes — section seven point three — is, *"APEX is the framework that gives Microsoft 365 Copilot a measurable business outcome."* That's the trick. Copilot adoption is universal. Copilot ROI attribution is universally weak. APEX is what attaches the Copilot license fee to a P&L line.

**JORDAN:** The Copilot product landscape. Section seven point two.

**KEVEN:** Three layers.

**Microsoft 365 Copilot** — the productivity copilot. Email, documents, Teams meetings. Adoption is broad but value attribution is hard.

**Copilot Studio** — the *low-code agent builder* — the citizen-developer path. Used to build domain copilots that compose with APEX agents.

**Vertical Copilots** — Sales Copilot, Finance Copilot, Service Copilot — domain-specific. Used when the client has a deep Dynamics footprint.

**JORDAN:** And the role of Copilot inside an APEX engagement.

**KEVEN:** Two roles.

Role one — *the user surface.* The persona-facing UI for many APEX agents is a Copilot. The user types into Copilot, the Copilot calls a Foundry agent via the Agent Framework, the agent calls APEX MCP tools, the tools query Fabric Gold. Copilot is the *front door*, Foundry is the *brain*, Fabric is the *memory*, Purview is the *recorder*.

Role two — *ROI attribution.* When APEX attaches measurable outcomes to Copilot-front-doored workflows, the client can finally justify the Copilot per-seat license at the CFO level. Section seven point three is the script for the CFO conversation.

**JORDAN:** Copilot Studio. Section seven point five. The net-new vertical opportunity.

**KEVEN:** Copilot Studio is the channel through which Deloitte ships vertical Copilots. We build APEX agents in Agent Framework, we wrap them in Copilot Studio for the persona-facing layer, and the client deploys both. The commercial pattern — Deloitte builds the Service, the client deploys the Copilot Studio assets at scale.

**JORDAN:** Section seven point six — when Copilot does not fit.

**KEVEN:** Two cases. One — *highly regulated decision flows where the audit trail must originate from the agent, not the UI.* Use a custom UI on top of Foundry, not Copilot. Two — *industrial / OT workloads where the persona is not at a desktop.* Use a custom mobile or terminal UI. Copilot is for knowledge workers — that's the realistic scope.

### Pillar Four — Purview (Chapter 8)

**KEVEN:** OK. Purview. Chapter eight. And this is the pillar that I think is *most* under-positioned by sellers, because Purview is a *governance* product and governance feels like overhead.

**JORDAN:** And the reframe?

**KEVEN:** The reframe is — *Purview is what makes the deal landable.* Without Purview, the CCO blocks. Without the CCO, the SOW doesn't sign. Purview is the *unlock* for everything else. Section eight point one — *the audit-ready promise* — is the opening line for the CCO conversation.

**JORDAN:** Section eight point two — Purview capabilities APEX uses.

**KEVEN:** Five things.

One — **Data classification.** Every dataset in Fabric is automatically classified — PII, PHI, financial, public, sensitive. APEX uses the classification to *enforce* policy at the agent layer.

Two — **Sensitivity labels.** Labels persist with data as it moves. An agent that reads a labelled dataset emits labelled output. The label *propagates*.

Three — **DLP — Data Loss Prevention.** Policies prevent labelled data from leaving the boundary. An APEX agent that tries to send labelled PII to an external tool gets blocked.

Four — **Audit and lineage.** Every agent call, every tool call, every data access is logged with full lineage. *That* is the audit trail.

Five — **DSPM for AI** — Data Security Posture Management for AI. The newer Purview capability that monitors which AI workloads access which sensitive data. The CCO dashboard.

**JORDAN:** Section eight point three — per-Practice Purview intensity. Quick.

**KEVEN:** Not every Practice uses Purview equally. HLS — *very* heavy. PHI everywhere, regulator-grade requirements. ER — *medium-heavy*, especially in utilities with critical infrastructure data. AXLE — *medium*, mostly for IP-classified design data and supplier-confidential information. RC — *medium-light*, focused on PII and PCI. TMT — *medium*, with telecom-CPNI rules. The Sellers Guide has a per-Practice intensity table — section eight point three.

**JORDAN:** Section eight point five — *"do we really need Purview?"* That objection is going to come up.

**KEVEN:** Three responses.

Response one — *"yes, because the auditor is going to ask, and an answer without Purview is bespoke."*

Response two — *"yes, because the cost of *not* having Purview is a deployment delay at the CCO sign-off gate. Days you lose at the CCO gate cost more than the Purview license."*

Response three — *"yes, because Purview is the *only* place all the AI activity is in one auditable record. The alternative is reconstructing the audit from Foundry logs, application logs, network logs — and your auditor will not accept reconstructed evidence."*

**JORDAN:** Section eight point eight — audit architecture end-to-end.

**KEVEN:** This is the architect-conversation answer. Five-stage flow.

Stage one — **agent emits.** Every Foundry agent call writes a trace.
Stage two — **APEX wraps.** The audit row I described earlier — who, what, with what, under what policy.
Stage three — **OneLake stores.** The audit row lands on Fabric Gold, immutable, hash-chained.
Stage four — **Purview echoes.** Purview picks up the audit row and integrates with its native lineage and DLP.
Stage five — **Auditor reads.** Your client's auditor accesses Purview directly, with their own credentials, and reviews the trail.

**JORDAN:** And the line for the architect.

**KEVEN:** *"Audit is not bolted on. Audit is a first-class output of every agent call, native to Foundry, persisted to OneLake, surfaced through Purview. The auditor reads Purview. Nobody reconstructs."* Section eight point eight.

### How the four compose

**JORDAN:** OK. Last twelve minutes — how the four pillars actually compose. Because this is the thing I wish you'd said in the pharma meeting.

**KEVEN:** Yes. Here's the composition in one paragraph.

[reading]

*"Fabric is where the data lives. The medallion is on Fabric. The canonical schemas anchor at Fabric Silver. Foundry is where the agent thinks. The agent is built in Agent Framework, runs on Agent Service inside Foundry, and calls out to data through APEX's MCP tools that read Service-specific Gold marts — Gold marts that pull from the Silver canonical. Copilot is where the user types. The user invokes the agent through Copilot, which calls the Foundry agent, which calls Fabric. And Purview is what the auditor reads. Every step of that chain emits classified, labelled, lineaged audit records that land in Purview as a unified evidence package."*

**JORDAN:** That is the paragraph.

**KEVEN:** That is the paragraph. If a CIO asks *"how do the four Microsoft pillars compose for APEX?"* — you give that paragraph. Section six point six in the guide gives a longer version, but that's the version for the room.

**JORDAN:** And the seller who confuses these pillars —

**KEVEN:** — loses the deal. Because the buyer concludes that the seller doesn't understand the product. The pharma deal we lost — the reason was each Deloitte and Microsoft person pitched *their* pillar. Nobody pitched the composition. Once you can pitch the composition, the four pillars stop being four products and start being one architecture.

---

## APEX Facts

**JORDAN:** APEX Facts. Eight in ninety seconds.

**KEVEN:** Fact One — Microsoft Fabric capacity for mid-market Wave One?

**JORDAN:** F64. Scaling to F128 or F256 for Wave Two.

**KEVEN:** Fact Two — number of Fabric integration patterns?

**JORDAN:** Five. Mirrored DB, Eventstream, Pipeline, Dataflow Gen2, Custom Endpoint.

**KEVEN:** Fact Three — APEX position on Databricks and Snowflake?

**JORDAN:** Fabric-first, not Fabric-only. Three interop patterns each.

**KEVEN:** Fact Four — what Agent Framework is, in one word?

**JORDAN:** SDK. Hosts on Foundry / Agent Service in production.

**KEVEN:** Fact Five — number of agent orchestration patterns?

**JORDAN:** Six. Sequential, parallel-fan-out, hierarchical, loop, debate, router.

**KEVEN:** Fact Six — fields in the APEX audit row?

**JORDAN:** Who, what, input, output, policy, timestamp. Hash-chained.

**KEVEN:** Fact Seven — two roles of Copilot in APEX?

**JORDAN:** User surface. ROI attribution mechanism for the M365 license.

**KEVEN:** Fact Eight — five-stage Purview audit flow?

**JORDAN:** Agent emits, APEX wraps, OneLake stores, Purview echoes, auditor reads.

**KEVEN:** Time.

---

## Adopt / Hold

**KEVEN:** Adopt versus Hold on the four pillars. Jordan, Adopt.

**JORDAN:** Adopt the four-pillar composition as your *opening architecture pitch* on every APEX deal — full stop. The Fabric-Foundry-Copilot-Purview paragraph belongs at minute three of the first architect conversation. The buyer needs to *see* that you understand how the four compose before they're going to trust you to deliver. It's the architectural credibility test.

**KEVEN:** Hold. When is the four-pillar pitch the *wrong* pitch?

**JORDAN:** Two cases.

Case one — *clients deeply invested in non-Microsoft platforms for one of the four layers.* If they're committed to Databricks for data, you don't open with Fabric. You open with — *"Foundry agents will read from your Databricks Unity Catalog through these interop patterns…"* You lead with composition, not displacement.

Case two — *very early in a discovery conversation where you haven't earned architectural credibility yet.* If you walk in to a CIO who's never met you and open with four-pillar architecture, you sound like a vendor. You earn that conversation by first showing them a Use Case that matters to *their* P&L. Then architecture.

**KEVEN:** Synthesis?

**JORDAN:** Lead with *outcome*, then earn the right to *architecture.* In the architecture conversation, the four-pillar paragraph is non-negotiable. But you don't lead with it.

---

## Lessons

**KEVEN:** Monday-morning lessons.

One — **memorise the composition paragraph.** Fabric is where data lives, Foundry is where the agent thinks, Copilot is where the user types, Purview is what the auditor reads. Drill it.

Two — **know which pillar maps to which client conversation.** Fabric is the CDO conversation. Foundry is the architect conversation. Copilot is the M365 owner conversation. Purview is the CCO conversation. Different buyers care about different pillars; come prepared with the right composition for the seat in the room.

Three — **on every architecture conversation, draw the audit trail end-to-end.** Five stages — agent emits, APEX wraps, OneLake stores, Purview echoes, auditor reads. Drawing it on a whiteboard wins the architect.

Four — **for the CCO meeting, lead with Purview.** Not Fabric, not Foundry. Purview. Section eight point six is the CCO pitch.

Five — **when a client says they have Databricks or Snowflake — don't argue. Co-exist.** Section five point co-existence. Three interop patterns. Pick the one that fits.

---

## Carve Outs

**JORDAN:** Carve out. Mine — section six point eleven. *Microsoft Orchestrator Agent Types — Semantic Kernel, Copilot Studio, Agent365.* This is the section that tells you which Microsoft-native orchestration mechanism to recommend for which kind of workload. It's the most architectural and least-known piece of the entire Microsoft agent story. Twenty minutes of reading. Worth it.

**KEVEN:** Mine — section five point five. *Why APEX on Fabric — the architectural acceleration case.* Five sub-sections. It's the rigorous version of why we are Fabric-first. When an architect at the client says *"why not just use Fabric out of the box?"* — section five point five point seven, the rehearsed responses, is the script.

---

## Sign-off

**KEVEN:** That's it for Episode Three. Next episode — the Seven Industries. RC, HLS, ER, AXLE, TMT, TH, ICE. Buyer personas, priority Services, where APEX differentiates in each. The whirlwind tour of the seven Practices.

**JORDAN:** See you there.

[outro]

---

**End of Episode 03 · The Four Pillars**
*≈ 5,200 words · ≈ 31:30 at 165 wpm*
