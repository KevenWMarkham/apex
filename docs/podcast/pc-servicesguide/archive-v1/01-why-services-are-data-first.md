# Episode 01 · Why Services Are Data-First

**Source:** *Professional APEX-M Services Guide* — Part I (Foreword + Chapters 1, 1A, 1B, 2, 3)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: laptop keyboard, faint office hum]

**KEVEN:** Six months ago, I was sitting with a solution architect on day fourteen of an APEX engagement. And by day fourteen, this engagement was on fire. The agent was technically running. The orchestration was firing. The Gold dashboard was lighting up. But every other answer the agent produced was wrong — confidently wrong — and nobody could explain why.

[pause]

**MORGAN:** Let me guess where this is going.

**KEVEN:** You probably can. Because the *real* problem wasn't the agent. The agent was doing exactly what we'd asked it to do. The problem was that the data the agent was reading at Gold layer wasn't actually the data the data engineers thought they'd shipped. There was a Bronze pipeline that had silently changed schema two sprints earlier. The Silver conformance layer had kept running but had started dropping fields. Gold was reading partial Silver. Agent was reading partial Gold. The whole thing was a polite, well-orchestrated, *audit-trail-emitting* hallucination.

**MORGAN:** And that's the moment that taught you —

**KEVEN:** That's the moment that taught me — and the moment the Services Guide opens with as Chapter Zero — *the Service is the data flow.* The agent isn't the Service. The orchestration isn't the Service. The data flow from Bronze to Silver to Gold to agent and back to audit *is* the Service. Everything else is decoration on top of it.

**MORGAN:** I'm Morgan.

**KEVEN:** I'm Keven Markham. APEX Services Podcast, Episode One. *Why Services Are Data-First.*

---

## Theme Statement

**MORGAN:** OK Keven, what are we covering?

**KEVEN:** Part One of the Services Guide. Six chapters. The Foreword — Chapter Zero — sets the data-first thesis. Chapter One introduces the medallion in Microsoft Fabric — Bronze, Silver, Gold. Chapter 1A is the Fabric deep dive. Chapter 1B is the medallion deep dive — specifically, *why canonical lives in Silver.* Chapter Two is the canonical schema families. And Chapter Three is MCP and the Service Tool Catalog — how agents reach the data.

**MORGAN:** So this episode is the entire architectural foundation.

**KEVEN:** Yes. If a listener takes one episode of this whole series, this is the one. Everything else composes on top.

---

## The Story

### The data-first thesis (Chapter 0)

**KEVEN:** Chapter Zero. The Foreword. *Why Services are Data-First.* The Services Guide opens with three rules. Memorise these.

**Rule One — the KPI envelope lives on the data, not the agents.** Section zero point three. If you measure agent-emitted KPIs, you're measuring the agent's *self-report*. That's how the engagement I just described drifted for six weeks before anyone caught it. The KPI has to live on the Gold-layer data the agent reads — independently observable, lineage-traceable back to source, queryable by humans without invoking the agent.

**MORGAN:** Let me ground that. In actual delivery — that means every Service has at least one Power BI report that *doesn't* go through the agent. Built from Gold directly.

**KEVEN:** Always. That's the audit-independence pattern.

**Rule Two — every Service is a data flow.** Section zero point two. From SOR through Bronze, Silver, Gold, MCP tool, agent, audit. Six waypoints, all logged, all auditable. If you can draw the data flow, you understand the Service. If you can't, you don't.

**Rule Three — the agent never reads Bronze.** Ever. Section zero point two again. Agents only read MCP tools. MCP tools only read Gold marts. Gold reads Silver. Silver reads Bronze. The layering is a security boundary, an audit boundary, *and* a semantic boundary.

**MORGAN:** Three rules. The one delivery teams violate most often is —

**KEVEN:** Rule Three. They get clever. They wire an agent to a Bronze table because *"it's faster, the data is fresher, why route through Silver."* Six weeks later, the audit story collapses. Don't.

### The medallion in Microsoft Fabric (Chapter 1)

**MORGAN:** Chapter One — the medallion in Fabric. Three tiers, each with a contract. Walk me through.

**KEVEN:** OK. Section one point one. Three tiers, side by side.

**Bronze.** Raw. As-received. Schema may drift. Bronze accepts everything the SOR sends. No business logic. No transformation. Just landed bytes with metadata — source system, ingestion timestamp, the Bronze pipeline run ID, the ingest identity, the PII classification.

**Silver.** Conformed. Canonical. This is the *anchor of stable meaning* — Chapter 1B section one B point two. Silver is where you enforce the canonical schema. Silver is where you reconcile multiple sources of the same entity. Silver is the boundary at which "VIN" means one thing and "customer_id" means one thing.

**Gold.** Service-shaped. Decision-ready. One Silver source fans out to many Gold marts — one per Service. Gold is denormalised, optimised for the queries the agent's MCP tools will run, with pre-aggregated metrics and pre-joined dimensions.

**MORGAN:** And the Fabric mapping — section one point two —

**KEVEN:** In Fabric, Bronze typically lives as a *lakehouse with raw files* in OneLake. Silver typically lives as a *lakehouse with delta tables* — the canonical schema enforced by the table definitions. Gold lives as either a *lakehouse* or a *warehouse* depending on whether you need T-SQL or notebooks against it. And the semantic model on top of Gold powers Power BI in Direct Lake mode.

**MORGAN:** OneLake security in user-identity mode. Section one point five. Recent GA.

**KEVEN:** Yes. This matters in delivery. User-identity mode means Fabric enforces row-level and table-level security per the *invoking user's* Entra ID — even when the invocation comes through an MCP tool. Before user-identity mode, you had to do this in the Gold mart definitions, which was brittle. Now the platform enforces. Section one point five also covers the primary-workspace pattern.

### Microsoft Fabric deep dive (Chapter 1A)

**MORGAN:** Chapter 1A. Microsoft Fabric deep dive. Fourteen sub-sections, this is the chapter every architect on an APEX engagement needs to internalise.

**KEVEN:** Right. Let me hit the points that matter operationally.

**The four-level hierarchy** — section 1A point one. Tenant, capacity, workspace, item. Each level has identity, access, and cost implications.

**Capacity SKUs** — section 1A point three. F-SKUs. F-2 through F-2048. Capacity Units are the billing unit. An F-64 — typical mid-market Wave One starting size — gives you sixty-four capacity units, throttled and burstable.

**The five Fabric workloads** — section 1A point four. Data Factory for pipelines. Data Engineering for notebooks. Data Warehouse for T-SQL. Real-Time Intelligence for streaming. Power BI for the semantic-model and reporting layer. All five share one OneLake.

**MORGAN:** Lakehouse versus warehouse. Section 1A point five. The question that comes up in every design.

**KEVEN:** The rule of thumb — *lakehouse for the data engineer's primary workspace, warehouse for the analyst's primary workspace.* If your team is mostly notebooks, Delta tables, Spark, ML — lakehouse. If your team is mostly T-SQL, stored procedures, dimensional modelling — warehouse. They co-exist in the same OneLake; choose by the consumer.

**Real-Time Intelligence as the trigger plane** — section 1A point six. RTI is the workload that turns event streams into actions. Eventhouse for KQL queries. Activator for threshold-driven triggers. This is the plane Episode Two will go deep on.

**Mirroring — live SOR replication** — section 1A point seven. Fabric can mirror SQL Server, Postgres, Cosmos DB, and Snowflake — bringing the data into OneLake in seconds, no ETL. This is the easy-button Bronze for operational sources.

**Direct Lake** — section 1A point eight. Power BI semantic models that read OneLake delta tables directly — no copy, no refresh schedule. This is the architectural difference between "BI on top of Fabric" and "BI bolted on next to Fabric." Use Direct Lake.

**OneLake shortcuts** — section 1A point nine. Cross-workspace, cross-cloud. Means you can point a Silver lakehouse at a Bronze lakehouse in another workspace — or even at an S3 bucket — without copying. The shortcut is the *primary mechanism* by which the medallion tiers connect in APEX.

**The APEX workspace pattern** — section 1A point thirteen. Important. APEX uses a *per-Practice workspace plus a shared canonical workspace.* The canonical workspace holds the Silver schema definitions and the canonical lookup tables. The per-Practice workspaces hold the practice-specific Bronze, the practice-specific Gold marts, and the Service-specific items. Shortcuts wire them together.

**MORGAN:** And the deeper why on workspaces — domain-level governance, capacity isolation, the team-level scopes.

**KEVEN:** Right. Section 1A point eleven — Fabric Domains. APEX uses domains to map to data-mesh boundaries — Practice domain, shared-canonical domain, governance domain. The Sellers Guide talks about "the four pillars composing" — at the implementation level, this is the workspace and domain pattern.

### Why canonical lives in Silver (Chapter 1B)

**KEVEN:** Chapter 1B. Medallion deep dive. And the chapter's animating argument — section 1B point three — *why canonical must sit at Silver. The counterfactuals.*

**MORGAN:** Let me push on this. Why not canonical at Gold? It's denormalised anyway, you could enforce the contract at Gold.

**KEVEN:** Three reasons. One — *if canonical is at Gold, every Service builds its own canonical*. You end up with five different "warranty record" definitions across five different Services. The contract isn't shared. Two — *you lose the audit boundary*. Silver is where Purview's lineage diagram becomes coherent. Three — *Gold marts evolve quickly, Silver evolves slowly*. Canonical needs to be the stable layer.

**MORGAN:** And the counterfactual at Bronze?

**KEVEN:** Canonical at Bronze means you're rejecting data at ingestion if it doesn't match the contract. SORs change schemas frequently. Bronze has to absorb that. If canonical is at Bronze, you're constantly losing data. Section 1B point one — *the five classes of source variance Bronze absorbs.*

**MORGAN:** Five-class enumeration. Worth listing.

**KEVEN:** Schema drift. Late-arriving fields. Type changes. Encoding changes. Identifier shifts. Bronze absorbs all five. Silver normalises. That's the division of labor.

**MORGAN:** And the one-to-N fan-out — section 1B point four. Silver to Gold marts. This is the section that most directly affects sprint planning.

**KEVEN:** Yes. One Silver canonical, many Gold marts. RC Practice — section 1B point four — *one Silver canonical for "order"* fans out to maybe six Gold marts: a returns mart, a fraud mart, a markdown-optimisation mart, a loyalty mart, a supply-allocation mart, a store-ops mart. Each Service has its own Gold mart. They share the Silver. They never collide.

### Canonical schema families (Chapter 2)

**MORGAN:** Chapter Two. The canonical schema families. The Sellers Guide names four for AXLE. How many total across the framework?

**KEVEN:** Fourteen — section two point one. Let me name them at category level. The retail order family — the customer-and-loyalty family — the supply-and-inventory family. The clinical-encounter family — the claims-and-utilization family — the pharma-trial family. The utility-network family — the upstream-energy family — the chemicals-process family. The build-record family — the connected-vehicle family — the assembly-asset family — the quality-event family. And the traveller-profile family. Fourteen.

**MORGAN:** Naming conventions — section two point two.

**KEVEN:** Practice-prefixed, family-suffixed. *RC-Order-Header*, *AXLE-BuildRecord-Station*, *HLS-ClinicalEncounter-Patient*. Predictable. Greppable. Searchable in Fabric's data catalog.

**MORGAN:** Cross-schema relationships — section two point three. The places where families *legitimately* join.

**KEVEN:** AXLE BuildRecord and AXLE QualityEvent join on VIN. AXLE ConnectedVehicle and AXLE BuildRecord join on VIN. RC Order and RC Loyalty join on customer ID. HLS ClinicalEncounter and HLS Claims join on encounter ID. These joins are *first-class* in the canonical — declared, governed, lineaged. Not ad-hoc.

### MCP and the Service Tool Catalog (Chapter 3)

**MORGAN:** Last chapter in Part One. Chapter Three. MCP — Model Context Protocol — and the Service Tool Catalog.

**KEVEN:** Yes. And this is the chapter that determines *how the agent actually reads the data.* Section three point one — what MCP is, operationally.

MCP is the protocol the agent uses to call out for context and tools. In APEX, every Service exposes a *catalog of MCP tools*. The tools are the only way the agent reaches Gold data. The agent doesn't have a connection string to OneLake. The agent has a list of tools.

**MORGAN:** Section three point four — *why agents don't talk to Microsoft Fabric directly.*

**KEVEN:** Three reasons.

One — *security and identity.* The MCP server enforces user-identity-mode security. Direct agent-to-Fabric would require service-principal access, which leaks the row-level boundary.

Two — *semantic stability.* The MCP tool is the place we *narrow* what the agent can ask. If the Gold mart has fifty columns and the Service needs the agent to think about ten, the MCP tool exposes ten. The agent can't hallucinate columns it doesn't have access to.

Three — *audit.* Every MCP tool call is logged with parameters, result hash, timestamp, persona. That's the *agent's* row in the APEX audit trail. Without the MCP boundary, the audit is reconstructed from logs. With the MCP boundary, it's emitted natively.

**MORGAN:** Section three point three — *the MCP host and the Microsoft platform.* Where do MCP servers actually run in APEX?

**KEVEN:** Three options. Azure Container Apps, with managed identity bound to the Fabric capacity. Azure Functions, for very lightweight per-tool servers. Or Microsoft-hosted MCP servers for RTI — section 1A point ten — which Microsoft is rolling out in preview.

**MORGAN:** And Microsoft Agent Framework as MCP consumer — section three point five.

**KEVEN:** Yes. Agent Framework is the SDK. The agent code calls MCP tools through the framework's tool interface. The framework handles the protocol, the discovery, the structured-output validation. The engineer writes business logic; the framework wires the protocol.

### Pulling it together

**MORGAN:** OK. Synthesis for Part One. Six chapters. What does an architect walk away with?

**KEVEN:** Five non-negotiables.

One — *the Service is the data flow.* Not the agent. The flow.

Two — *Bronze absorbs source variance. Silver anchors canonical meaning. Gold serves Service-shaped marts.* In that order. Don't move the boundaries.

Three — *agents read MCP tools. MCP tools read Gold. Period.*

Four — *canonical schemas are pre-built. Fourteen families. Use them. Don't invent a new "order" schema.*

Five — *the APEX workspace pattern in Fabric is one canonical workspace plus per-Practice workspaces, wired with shortcuts.* Don't fight this.

**MORGAN:** That's the foundation.

**KEVEN:** That's the foundation. Every other episode of this series sits on top of it.

---

## APEX Facts

**MORGAN:** APEX Facts. Eight rapid.

**KEVEN:** Fact One — three rules of data-first?

**MORGAN:** KPI on data not agents. Service is the data flow. Agent never reads Bronze.

**KEVEN:** Fact Two — three medallion tiers and what each owns?

**MORGAN:** Bronze absorbs variance. Silver anchors canonical. Gold serves marts.

**KEVEN:** Fact Three — Fabric capacity SKU for mid-market Wave One?

**MORGAN:** F-64. Sixty-four capacity units.

**KEVEN:** Fact Four — five Fabric workloads?

**MORGAN:** Data Factory, Data Engineering, Data Warehouse, Real-Time Intelligence, Power BI.

**KEVEN:** Fact Five — canonical schema families total count?

**MORGAN:** Fourteen.

**KEVEN:** Fact Six — Power BI mode that reads OneLake without copying?

**MORGAN:** Direct Lake.

**KEVEN:** Fact Seven — what hosts an MCP server in APEX?

**MORGAN:** Azure Container Apps, Azure Functions, or Microsoft-hosted MCP for RTI in preview.

**KEVEN:** Fact Eight — APEX workspace pattern?

**MORGAN:** One canonical workspace plus per-Practice workspaces. Wired with OneLake shortcuts.

**KEVEN:** Time.

---

## Adopt / Hold

**MORGAN:** Adopt versus Hold. Keven, Adopt.

**KEVEN:** Adopt — *the APEX medallion in Fabric, exactly as documented.* For every APEX engagement, this is the default. Don't redesign the medallion. Don't introduce a fourth tier. Don't blur Silver and Gold. The pattern is proven, the Purview lineage is built around it, and the canonical schemas only land cleanly on this pattern.

**MORGAN:** Hold. When is the default medallion the *wrong* call?

Two cases.

Case one — *if the client has an existing Bronze-equivalent landing zone that's working* — like a mature Databricks Bronze on Delta Live Tables — *and the team has institutional knowledge there.* Don't migrate Bronze for Bronze's sake. Use Fabric OneLake shortcut to read the existing Bronze. Skip the work.

Case two — *if the velocity profile is dominated by sub-second telemetry where Bronze landing in OneLake is too slow.* Then RTI Eventhouse becomes your effective Bronze for the streaming path. Two parallel ingestion patterns. We'll cover this in Episode Two.

**KEVEN:** Synthesis?

**MORGAN:** Default is the medallion. Exception is when an existing pattern is operationally cleaner — and then you wire it in with OneLake shortcuts rather than re-engineering. The shape of the medallion is non-negotiable. The plumbing under Bronze can adapt.

---

## Lessons

**KEVEN:** Monday-morning lessons for a delivery team.

One — **on every new APEX engagement, draw the data flow before you write any code.** Six waypoints — SOR, Bronze, Silver, Gold, MCP tool, agent — on a whiteboard. Two hours. The drawing is the design.

Two — **memorise the three data-first rules.** They're the test you apply every time an engineer wants to optimise something. "Should the agent read Bronze for this hot path?" — no. Always.

Three — **when you stand up the Fabric workspaces, build the canonical workspace first.** Even if your engagement is one Practice. The shared canonical needs a home — and once you put it inside a Practice workspace, you'll regret it the moment Practice number two arrives.

Four — **never let an MCP tool expose a column the agent doesn't need.** Section three point four. The MCP tool is the narrowing point. Narrow it.

Five — **add a sanity Power BI report on every Service that reads Gold directly.** Doesn't go through the agent. The KPI envelope lives on the data, not the agent. Section zero point three.

---

## Carve Outs

**MORGAN:** Carve outs. Mine — read Chapter 1B point three through point six together. *Why canonical lives in Silver — the counterfactuals* — plus the *one-to-N fan-out from Silver to Gold marts.* That's the deepest architectural argument in the book and it's where most design mistakes get made.

**KEVEN:** Mine — read the parallel sections in the *Sellers Guide* and the *Services Guide* side by side. Sellers Guide section one point six A — *Industry-Standard Schemas and the APEX / AXLE Canonical Design.* Services Guide Chapter Two — *Canonical Schema Families.* The Sellers Guide is the commercial framing. The Services Guide is the implementation framing. Same content, different angle. Reading both is how you learn to translate between the seat the buyer is in and the seat the engineer is in.

---

## Sign-off

**KEVEN:** That's it for Episode One. Next episode — *Bronze Tier — Ingesting the Real World.* Part Two of the Services Guide. Source-of-Record inventory by industry. The Real-Time Hub pattern. The four velocity tiers. Ingestion and tokenization. PII classification and the pii-unlock identity. The chapter every data engineer on an APEX engagement needs cold.

**MORGAN:** See you there.

[outro]

---

**End of Episode 01 · Why Services Are Data-First**
*≈ 5,000 words*
