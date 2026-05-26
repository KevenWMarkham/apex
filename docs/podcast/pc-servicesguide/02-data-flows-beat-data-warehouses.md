# Episode 02 · Data Flows Beat Data Warehouses

**Arc:** Foundation (2 of 4) · **Builds on:** Ep 1 (the three eras, agentic-era bottleneck = governance) · **Foundation laid:** Data-first thesis · brief medallion preview · how agents differ from BI consumers
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: keyboard typing, then a long pause]

**MORGAN:** Three months ago I had a conversation with a CIO of a mid-sized manufacturer. The conversation went like this. He said — *"Morgan, I've spent the last decade and forty million dollars building my data warehouse. It's the cleanest, most governed enterprise data warehouse in our industry. If your APEX framework needs data, my warehouse is where you'll find it."*

[pause]

**KEVEN:** And your response —

**MORGAN:** My response was — *"That's wonderful. And we'll absolutely use it. But the data warehouse is not where the agent is going to live."*

And you could see his face change. Because he had spent ten years and forty million dollars on infrastructure that — in his mind — *was* the data architecture of the company. And what I was telling him was — *that infrastructure stays. We don't tear it down. But the agent doesn't run on top of it. The agent runs on something that flows through it.*

**KEVEN:** And he heard it as —

**MORGAN:** He heard it as *"your warehouse is obsolete."* Which is not what I was saying. But the *vocabulary* difference between *data at rest* — which is what a warehouse is — and *data in motion* — which is what an agent needs — is a vocabulary difference enterprises haven't caught up with yet.

That's what this episode is about.

**KEVEN:** I'm Keven Markham.

**MORGAN:** I'm Morgan. Services Podcast Episode Two. *Data Flows Beat Data Warehouses.*

---

## The conversation

### Picking up from where Episode One left us

**KEVEN:** Let me anchor where we left off in Episode One. We walked the three eras — dashboards, then analytics-and-ML, then agents. And we said the new bottleneck is *governing the agent in production.* Hold that frame.

What we didn't unpack last episode — *and what we need to unpack now* — is *what kind of data architecture the agent actually needs.* Because that's the load-bearing question that every subsequent episode rests on. The medallion. The canonical schemas. The MCP layer. They're all answers to that question. And before we go into each of them in depth, we need to set up *the question itself.*

**MORGAN:** And the question is —

**KEVEN:** *What does an agent need from data that a dashboard or an ML model didn't?*

Three things. Let me walk through them, one at a time, no jumping.

### Need one · stable semantic meaning, queryable in real time

**KEVEN:** Need one. The agent needs *stable semantic meaning, queryable in real time.* Let me unpack what each of those means and why both matter.

**MORGAN:** Start with stable semantic meaning.

**KEVEN:** OK. In the dashboard era, *"customer"* might have meant five different things in five different reports. The marketing dashboard's "customer" was anyone who'd ever bought. The CRM dashboard's "customer" was anyone with an active account. The finance dashboard's "customer" was anyone with billable activity in the last quarter. These were *different definitions* embedded in different reports, and humans reading the dashboards mentally translated between them.

That works for humans. It doesn't work for agents. Because an agent has to *take action* on the data. If the agent reads "customer" and thinks it means *one* thing while the downstream system the agent calls thinks it means *another* thing — the action goes to the wrong entity. The blast radius is real. Money flows incorrectly. Comms go to wrong people. The agent's audit trail records a decision that, in the context of the *intended* customer, looks wrong.

**MORGAN:** So the agent requires the entity definitions to be *unambiguous* across the whole system.

**KEVEN:** Unambiguous. And — this is the structural insight — *consistently unambiguous over time.* Not just at deployment. Year one. Year three. After three reorgs, four acquisitions, and a CDO change. The semantic meaning has to be *stable.*

That stability is what we'll later call *canonical schema.* Pre-built definitions of the core business entities — customer, order, claim, build record, vehicle, encounter — that are agreed *once* and enforced everywhere. We'll go deep on this in Episode Three.

**MORGAN:** And the real-time piece —

**KEVEN:** That's the second half. *Queryable in real time.* In the dashboard era, "real time" meant "last night's data refreshed by morning." In the analytics era, "real time" meant "the model scoring pipeline processed in the last fifteen minutes."

In the agentic era — and *especially* for transactional and operational workloads — real time means *seconds to single-digit minutes.* The agent is being invoked during a customer interaction, during a transaction, during an operational decision window. The data the agent reads has to reflect the world as it *currently exists*, not as it existed six hours ago.

**MORGAN:** And the data warehouse can't do that.

**KEVEN:** The data warehouse *cannot* do that, by design. Data warehouses were built for batch analytics. They optimise for *consistency of historical state at query time.* The trade-off — they require batch ETL to refresh. Even the best modern warehouses refresh in minutes, not seconds. And the *operational source systems* — the systems the data originates from — don't change just because somebody plugged in a warehouse. The transactions still happen continuously. The warehouse always lags.

For an agent making transactional decisions, that lag is the difference between *useful* and *useless.*

**MORGAN:** And the answer is —

**KEVEN:** The answer is — *the agent reads from a different layer.* Not the warehouse. A flow-shaped layer that reflects the operational reality with single-digit-second latency. We'll call this layer Gold in the medallion vocabulary — but the conceptual point comes first. Agents need flow, not warehouse.

### Need two · governed, classified, lineage-traceable

**MORGAN:** OK. Need two.

**KEVEN:** Need two. The agent needs data that is *governed, classified, and lineage-traceable.*

Let me unpack each.

*Governed* means — every column, every record, every dataset has known sensitivity. Known retention. Known access controls. Known refresh cadence. The agent that reads the data inherits the data's governance. If the data is classified as PII, the agent's output that touches it is also classified as PII. If the data has 7-year retention, anything derived from it has at least 7-year retention. *The classification propagates with the data through the agent.*

*Classified* — more specifically — every dataset carries its sensitivity label and its compliance domain. PHI for healthcare data. PII for personal data. PCI for cardholder data. Trade-secret for IP. Sector-specific. Region-specific. The label rides on the data wherever it goes.

*Lineage-traceable* means — for any agent decision, the auditor can walk backward from the decision to the source data that informed it. Not "approximately." *Specifically.* What rows from which tables at what point in time were read by the agent that produced this output.

**MORGAN:** And the data warehouse can do some of this.

**KEVEN:** The data warehouse can do *some.* Modern warehouses have classification tooling. Lineage tooling. Governance overlay. What they typically *can't* do is — connect that governance forward through the agent's reasoning step. Once data leaves the warehouse and enters the agent's context window, the warehouse's lineage stops. There's a hand-off boundary that historically was *opaque.*

In the agentic era, the boundary can't be opaque. *Every agent decision is itself a data product.* The agent's output is a record. That record has to inherit the lineage of the inputs that produced it. That requires the lineage discipline to extend *through the agent*, not stop at it.

**MORGAN:** And that's a property of the medallion plus the MCP boundary —

**KEVEN:** Right. And we'll develop both of those across the next two episodes. The lineage-through-the-agent property is one of the framework's quietest but most important architectural commitments.

### Need three · narrow, decision-shaped, MCP-readable

**KEVEN:** Need three. The agent needs data that is *narrow, decision-shaped, and MCP-readable.*

This one is subtle. Let me work through it slowly.

**MORGAN:** Take your time.

**KEVEN:** In the dashboard era, the data layer was designed to support *exploration.* The analyst clicked around. Drilled into different dimensions. Filtered. Pivoted. The data layer had to be *flexible* — broad surface area, many dimensions, many measures, joins in every direction. That flexibility was the *point.*

In the analytics era, the data layer was designed to support *training.* The data scientist needed lots of features. Lots of history. Wide tables. Feature stores. The flexibility was different — feature-flexible rather than dimension-flexible — but still *broad.*

In the agentic era, the agent does *not* need broad. The agent needs *narrow.* The agent is asking *one specific question at a time*, on behalf of *one specific decision.* "Does this loyalty member's recent behaviour indicate elevated churn risk?" "What's the warranty-claim history for this VIN cohort?" "What's the current temperature reading for this store cooler?"

Each of these is a *narrow query.* The agent doesn't want to *explore* the data. The agent wants to *retrieve the specific information needed to inform the specific decision being made right now.*

**MORGAN:** And the implication for the data layer is —

**KEVEN:** The data layer's surface area, *for agent consumption*, is *narrower* than the warehouse's surface area. Not because the warehouse is wrong. But because the *agent's needs are different.* The Gold marts we'll develop in Episode Three are *shaped for the agent's decisions.* Not for exploration. Not for training. For the specific, narrow, decision-shaped retrievals the agent needs.

**MORGAN:** And the MCP piece — MCP-readable.

**KEVEN:** MCP — Model Context Protocol — is the wire protocol the agent uses to call out to its data and tools. The agent doesn't open a database connection. The agent doesn't write SQL. The agent calls a *tool* — a structured function that has a name, a typed input, and a typed output. The tool reaches into the Gold mart, executes the narrow retrieval, returns the structured answer.

The data layer has to be *shaped for those tools.* Pre-aggregated. Pre-joined. Pre-filtered to the dimensions the tool exposes. Because if the tool has to do a complex query at agent-invocation time, the latency budget collapses and the agent's reasoning slows to the point of unusability.

**MORGAN:** And the data warehouse —

**KEVEN:** The data warehouse doesn't *need* to be MCP-readable in any specific way. The MCP layer doesn't live on the warehouse. It lives on a Gold mart that's shaped specifically for the agent. Which is, again, a *different layer* — not a replacement for the warehouse, but a *new* layer downstream of it.

### Where this leaves us

**MORGAN:** OK. Let me try to land where we are.

**KEVEN:** Go.

**MORGAN:** The agent's three needs — stable semantic meaning queryable in real time; governed and lineage-traceable; narrow and decision-shaped through MCP — they're collectively *a different shape of data* than the warehouse provides.

The warehouse stays. But there's a *new layer downstream of the warehouse* that the agent actually reads.

**KEVEN:** Exactly.

**MORGAN:** And that new layer is the medallion. Bronze, Silver, Gold. Built specifically for the agentic era. Co-existing with the warehouse, not replacing it.

**KEVEN:** Exactly. And what's beautiful — this is what I wanted that CIO from the cold open to hear — is that the *investment* in the warehouse is not lost. The warehouse remains the analytic substrate. The historical reporting substrate. The reconciliation substrate. *All of that work has long-term value.* What APEX adds is the *agentic layer* alongside it. Same data feeding both. Different consumers shaping the data differently.

### A reading I want to do

**KEVEN:** I want to read something. It's from the Microsoft Fabric documentation, but it's not a how-to. It's a paragraph from a Microsoft Tech Community blog post from 2024 that I think articulates the shift better than anything else I've read. I'll link it.

**MORGAN:** Read it.

**KEVEN:** [reading]

*"The most common misunderstanding we encounter when introducing Fabric to enterprises with mature data estates is that Fabric is being positioned as a replacement for their existing warehouse. It is not. Fabric is positioned as an additional plane — a unified plane — that complements existing investments. The medallion architecture on OneLake is the new working layer for agentic and real-time workloads. The existing warehouse continues to serve its historical purpose. The two layers compose."*

[pause]

**MORGAN:** Good paragraph.

**KEVEN:** That's the frame. *Composition, not replacement.*

### One specific disagreement

**MORGAN:** OK let me push on something.

**KEVEN:** Please.

**MORGAN:** The way we just framed it — *the warehouse stays, the agentic layer adds alongside* — that's *technically* correct but it can become a *strategic* trap for the engagement. Because in practice, when an enterprise sees a new architectural layer being added, the natural CFO question is — *"so when can we retire the old one?"*

And the answer that comes from the framework's mouth is *"never, they compose."* And the CFO hears — *"so we're paying for two."*

**KEVEN:** Right.

**MORGAN:** I think the framework needs to be honest with itself that there *is* an eventual rationalisation. Not at Wave One. Not at Wave Two. But over years — five, ten — some workloads that today run on the warehouse will migrate to the medallion. The warehouse footprint will *shrink.* Not vanish — shrink.

**KEVEN:** And the reason it matters that we're honest about it —

**MORGAN:** The reason it matters is — when a CFO asks the question, the seller has to be able to say — *"yes, the warehouse will rationalise over time. Here's the indicative trajectory. Here's what stays in the warehouse permanently. Here's what migrates."* That's a credible answer. *"They compose forever"* sounds like consultant-speak.

**KEVEN:** I think you're right. The framework's *technical* claim — they compose — is true. The framework's *commercial* claim — they compose forever, no rationalisation question — is *not* honest with the buyer.

**MORGAN:** Yeah.

**KEVEN:** And the seller who says *"long-term the warehouse rationalises down to the workloads that can't move"* has a better conversation than the seller who pretends the question doesn't exist.

**MORGAN:** Agree.

**KEVEN:** That's the synthesis. *Composition for the foreseeable. Rationalisation eventually for workloads that can move. Permanent residence in the warehouse for workloads that can't.*

### What to carry forward

**KEVEN:** OK. Three things to carry into Episode Three, where we go deep on the medallion.

One — *the agent needs a different data shape than the warehouse provides.* The warehouse stays, but a new layer lives downstream of it.

Two — *that new layer has three properties* — stable semantic meaning real-time-queryable; governed, classified, and lineage-traceable through the agent; and narrow, decision-shaped, MCP-readable.

Three — *the medallion architecture is the framework's specific answer to those three properties.* Bronze, Silver, Gold. We've previewed it. Next episode we go inside it.

**MORGAN:** Good.

**KEVEN:** Episode Three — *The Medallion in Depth.* The architecture every Service deploys onto. The reason we can ship 38 cataloged Services without rebuilding the data foundation each time.

**MORGAN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn

- **Microsoft Fabric — Lakehouse and Delta tables** · [Microsoft Learn](https://learn.microsoft.com/fabric/data-engineering/lakehouse-overview)
- **Microsoft Fabric — Real-Time Intelligence overview** · [Microsoft Learn](https://learn.microsoft.com/fabric/real-time-intelligence/)
- **OneLake — the OneDrive for data** · [Microsoft Learn](https://learn.microsoft.com/fabric/onelake/)
- **Direct Lake mode in Power BI** · [Microsoft Learn](https://learn.microsoft.com/fabric/get-started/direct-lake-overview)

### Microsoft Tech Community blogs

- **"Why we built OneLake"** · Microsoft Fabric Blog
- **"Composing Fabric with existing data investments"** · Microsoft Fabric Blog
- **"Medallion architecture for agentic workloads"** · Azure AI Blog

### Architecture references

- **The Medallion lakehouse architecture** · [Microsoft Learn](https://learn.microsoft.com/azure/databricks/lakehouse/medallion) — originally documented for Databricks, the conceptual model maps cleanly to Fabric
- **Azure Well-Architected Framework — Data and AI workloads** · Microsoft Learn

### Industry context

- *"The Data Warehouse Toolkit"* · Ralph Kimball — foundational reading for understanding what the warehouse era was designed to do (so you know what it *isn't* designed to do)
- *"Designing Data-Intensive Applications"* · Martin Kleppmann, O'Reilly — Chapter on batch vs streaming systems, particularly relevant for the real-time-vs-warehouse contrast in this episode
- *"The state of data and AI 2025"* · Gartner Magic Quadrant for Data and AI Governance
- *"Lakehouse: A New Generation of Open Platforms"* · Armbrust et al., CIDR 2021 — the academic paper that introduced the lakehouse pattern

### From the APEX Trilogy

- **Services Guide — Foreword** — frames the data-first thesis
- **Services Guide — Bronze → Silver → Gold chapter** — the architectural detail this episode previewed and Episode 3 will develop
- **Sellers Guide — *"Why Canonical Schema Is the Acceleration Kernel"*** — the commercial framing of the canonical-meaning property

---

**End of Episode 02 · Data Flows Beat Data Warehouses**
*≈ 5,600 words · target 30 minutes at conversational pace*
