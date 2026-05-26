# Episode 03 · The Medallion in Depth

**Arc:** Foundation (3 of 4) · **Builds on:** Eps 1-2 (third era, three needs of agentic data, composition with warehouse) · **Foundation laid:** Bronze, Silver, Gold layers · velocity tiers · canonical at Silver
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: pen scratching on paper]

**MORGAN:** I want to start with a whiteboard moment. About a year ago — early 2025 — I was in a room with a data architect from a national grocery chain, doing an APEX engagement kickoff. He had thirty years of experience. He had built the company's enterprise data warehouse in the early 2000s. He'd watched it evolve. He'd watched the cloud migration. He had a healthy skepticism of any vendor introducing a new architectural concept.

He drew the medallion on the whiteboard from memory. Bronze. Silver. Gold. Three layers. He'd seen the diagram. And he said — *"Morgan, I get it. I've read the Databricks whitepaper. I've read the Fabric documentation. What I don't understand is — why does APEX care which layer the canonical schema lives in? Why isn't this just a stylistic decision?"*

[pause]

**KEVEN:** And the answer matters.

**MORGAN:** The answer matters enormously. Because if you put canonical at the wrong layer, you don't just have a stylistically different architecture — you have an architecture that *can't scale* across multiple Services on the same tenant. Which is the entire point of the framework.

That's what this episode is about. The medallion isn't a diagram. It's a set of architectural commitments that determine whether the *next* Service you add to the tenant takes a week or three months.

**KEVEN:** I'm Keven Markham.

**MORGAN:** I'm Morgan. Services Podcast Episode Three. *The Medallion in Depth.*

---

## The conversation

### Picking up the thread from Episode Two

**KEVEN:** Let me anchor where we are. Episode One — the bottleneck moved. We're in the third era. Governance of agents in production is the new bottleneck. Episode Two — the agent needs a different data shape than the warehouse provides. Three properties. Stable semantic meaning real-time-queryable. Governed and lineage-traceable. Narrow and decision-shaped. The new layer that gives the agent what it needs — we previewed — is the medallion.

This episode goes inside that medallion. Bronze. Silver. Gold. We're going to spend real time on each. No jumping. Each layer gets developed fully before we move on.

**MORGAN:** And the framework is opinionated about each one. The opinions matter.

**KEVEN:** Let me start with Bronze.

### Bronze · the layer that absorbs reality

**KEVEN:** Bronze is the *landing layer.* The first place data lives once it enters the APEX environment. The defining property of Bronze is — *Bronze accepts whatever the source systems send.* Schema drift, late-arriving fields, type changes, encoding shifts, identifier mutations — Bronze absorbs all of it. Without rejecting.

**MORGAN:** And the reason it has to absorb without rejection —

**KEVEN:** Because operational source systems *change.* The point-of-sale platform pushes out a new release and adds three new fields. The warranty system gets migrated to a new platform and the field types shift. The connected-vehicle telematics provider changes its event schema in a minor version. *These changes happen continuously and Bronze has to keep flowing.*

If Bronze enforced strict schema, every source change would *break* the pipeline. The data engineer would be in incident mode every other Tuesday. Instead — Bronze flows. Late-arriving fields just appear. Type changes get captured as-is. Encoding gets preserved. The job of Bronze is *to be the most forgiving layer in the architecture.*

**MORGAN:** And how it's implemented in Fabric specifically —

**KEVEN:** Typically a lakehouse with raw files. Delta tables with permissive schema. Or — for streaming sources — an Eventstream tee'd into both Eventhouse (for KQL real-time) and OneLake delta (for batch downstream). The shape is — *raw landing, with metadata.* Source system. Ingestion timestamp. Pipeline run ID. Ingest identity. PII classification applied at landing.

**MORGAN:** And the things teams get wrong about Bronze —

**KEVEN:** Two things, mostly.

One — they try to *transform* in Bronze. They think — *"the field name is ugly in source, let me clean it up at ingest."* Don't. Bronze is *what the source sent.* Transformations live at Silver. If you do them at Bronze, you've made Bronze *non-forgiving* — every source change now requires a Bronze pipeline update.

Two — they try to *reconcile* in Bronze. They think — *"the same customer appears in two source systems, let me merge them at landing."* Don't. Reconciliation is a Silver discipline. Bronze accepts both records as-is and stamps them with their source. Silver is where the merge happens.

**MORGAN:** And the PII tokenisation —

**KEVEN:** Right — *that* happens at Bronze landing. *Before* the data is committed. Cleartext PII never reaches the Bronze delta tables. The deterministic tokeniser swaps real values for tokens at ingest. The mapping lives in a separate, locked-down vault. We talked about pii-unlock identity briefly in the v1 series; we'll revisit it in the prior-auth episode where governance becomes the deal.

**MORGAN:** OK. So Bronze — landing layer. Permissive schema. Tokenised PII. Source-stamped. Forgives change.

**KEVEN:** That's the definition. Now Silver.

### Silver · the anchor of stable meaning

**KEVEN:** Silver. This is the layer where Episode Two's first property gets *delivered.* Stable semantic meaning.

The job of Silver — *enforce the canonical schema.* Every entity that appears in Silver appears in *one* shape, agreed across the engagement, governed by a defined extension process.

**MORGAN:** And the canonical-schema concept —

**KEVEN:** Canonical schemas are *pre-built definitions* of the core business entities — customer, order, claim, encounter, build record, vehicle, traveller profile. They live in the framework's schema library — fourteen families across the seven Practices. RC has its order family, its customer-and-loyalty family, its supply-and-inventory family. HLS has its clinical-encounter family, its claims-and-utilization family. AXLE has its build record, connected vehicle, quality event, assembly asset families. Etc.

These aren't generic schemas invented in a vacuum. Each is *grounded in an industry standard.* The HLS clinical encounter is grounded in FHIR R4. The RC order is grounded in GS1 plus Schema.org Commerce. The AXLE build record is grounded in AIAG and SAE J-standards. The ER utility-network is grounded in CIM.

The framework's claim — and this matters commercially — is that *because the canonical schemas exist already, an APEX engagement doesn't spend the first six months building the data foundation.* The foundation is *pre-built.* The engagement maps the client's source-system Bronze data to the canonical Silver shape. Mapping is faster than designing.

**MORGAN:** And the reason canonical lives in Silver specifically — *not* in Bronze, *not* in Gold — was the question that data architect was asking in the cold open.

**KEVEN:** Right. Let me walk that argument carefully. Because it's the architecturally most important argument in the whole medallion.

**MORGAN:** Take it slow.

**KEVEN:** *Canonical can't live at Bronze.* Because Bronze absorbs schema drift. Bronze accepts what the source sent. If canonical lived at Bronze, Bronze would reject anything that didn't match canonical. We just discussed why that breaks. Bronze has to forgive change. Canonical can't forgive change — by definition, canonical *is* the unchanging contract. They're incompatible at the same layer.

**MORGAN:** And canonical can't live at Gold —

**KEVEN:** Canonical can't live at Gold because *Gold is per-Service.* Each Service has its own Gold mart, shaped for the Service's specific decisions, optimised for the Service's specific MCP tool surface. If canonical lived at Gold, every Service would build its own canonical version. *And the next Service that came along would build its own different version.* You'd end up with N versions of "customer" in N Services on the same tenant. The shared meaning collapses.

**MORGAN:** So canonical has to live at Silver. Between Bronze's forgiveness and Gold's per-Service shaping.

**KEVEN:** Exactly. Silver is the *only* layer where canonical is stable across all Services. The architectural commitment is — *canonical lives at Silver. Period. Across every APEX deployment, every Practice, every engagement.* That commitment is what lets the next Service drop in without rebuilding the data foundation.

**MORGAN:** And the conformance work to get from Bronze to Silver —

**KEVEN:** That's the work. The conformance pipeline reads Bronze, applies the conformance rules, writes to Silver. Four conformance dimensions — schema, identity, code-value, temporal. Schema conformance — Bronze fields map to canonical fields. Identity conformance — same-entity instances from multiple sources are reconciled. Code-value conformance — "MA" / "Massachusetts" / "Mass." all become one canonical state code. Temporal conformance — time zones normalised, effective-dated fields handled.

The conformance pipeline is where the *real* engineering happens. The pipeline runs on a Fabric notebook or a Spark job — typically scheduled, but can be streaming. The output is canonical Silver delta tables.

**MORGAN:** And what gets stamped on every Silver row —

**KEVEN:** Every Silver row carries — its source Bronze row IDs, the conformance pipeline version that produced it, the timestamp of conformance. So lineage is *concrete.* Any Silver record can be traced back to the Bronze rows it was built from, with the rule version that did the mapping. Purview reads this lineage natively. The auditor walks it.

### Silver to Gold · the fan-out

**MORGAN:** OK. So Silver is the anchor. What about Gold?

**KEVEN:** Gold is *per-Service.* The fan-out from Silver to Gold is one-to-many. *One* Silver canonical can serve *many* Gold marts.

Concrete example. RC Practice. The Silver canonical for "order" — a single canonical schema. Order header, order line, status history, fulfilment, returns, payment, promotions. Seven tables. Joined on order ID. One stable canonical shape.

Now there are seven RC Services in the catalog. Each one consumes some subset of the Order family and produces a *Service-specific Gold mart.*

The loyalty churn Service. Its Gold mart denormalises order data into customer-level features — recent order count, days-since-last-order, returns rate, channel mix, basket trend. Shaped for the churn-prediction agent.

The markdown optimisation Service. Its Gold mart denormalises order data into SKU-level features — sell-through rate by store, markdown depth elasticity, inventory aging curve. Shaped for the markdown-decision agent.

The returns fraud Service. Its Gold mart denormalises order data into return-event features — customer return history, store return rate, time-from-purchase distribution, basket-vs-return matching. Shaped for the fraud-risk agent.

*Same Silver canonical. Three different Gold marts. Three different Services. They never collide.*

**MORGAN:** And the reason for the per-Service Gold shaping —

**KEVEN:** Two reasons. *Isolation* — Service A reshaping its Gold mart doesn't affect Service B. They share the Silver anchor; they don't share Gold. *Agent performance* — the agent's MCP tools query against the Gold shape that's been optimised for *this* Service's decisions. Aggregations are pre-computed. Joins are pre-resolved. The agent gets the answer in milliseconds, not seconds.

### Velocity tiers · the time dimension

**KEVEN:** OK. One more thing for Episode Three. *Velocity.* Because the medallion is a *spatial* concept — layers. Velocity is the *temporal* concept — how fresh is the data at each layer.

The framework names four velocity tiers.

Tier one — *real-time streaming via Eventhouse.* Sub-second to single-digit-second latency. KQL-queryable. The Activator engine fires here. Used for cold-chain excursions, sensor-driven anomalies, real-time risk scoring.

Tier two — *semi-real-time via Direct Lake and Mirrored Database.* Seconds to minutes latency. Direct Lake reads OneLake delta tables in Power BI without refresh. Mirrored Database makes operational DBs queryable in near-real-time. Used for transactional workloads where minute-scale latency is fine.

Tier three — *periodic feeds via Data Pipelines and Scheduled Refresh.* Minutes to hours latency. Classic ETL path. Used for batch-tolerant workloads.

Tier four — *Redis hot cache.* Sub-millisecond. Used for agent working memory — recent runs, recent outcomes, context warming. We'll see this in Episode Four when we cover agents.

**MORGAN:** And every Service mixes tiers.

**KEVEN:** Every Service uses multiple tiers. The cold-chain Service uses Tier 1 for cooler events, Tier 3 for daily sales, Tier 4 for the agent's working memory of which stores are currently in excursion. The warranty Service uses Tier 2 for the build-record-to-claim lookup, Tier 1 for connected-vehicle telemetry, Tier 3 for periodic supplier-lot summaries.

Tier assignment is a *design artefact.* During engagement design, you classify every data dependency against the four-tier spectrum. Mismatched velocity drives most operational pain — the team that built a Service assuming Tier 2 access and discovers the source only supports Tier 3 is the team that has to redesign halfway through Wave One.

### A reading I want to do

**KEVEN:** I want to read a short passage. This is from the Microsoft Fabric documentation — specifically the section on the OneLake architecture. I think it makes the *composition* point clean.

**MORGAN:** Read it.

**KEVEN:** [reading]

*"OneLake is one logical lake per tenant. Bronze, Silver, and Gold are not separate storage layers — they are zones within OneLake, distinguished by purpose, governance, and the kinds of consumers they serve. The same physical OneLake holds all three. The compute that reads each tier varies. The contracts each tier exposes vary. The lineage from Bronze through Gold is automatic and queryable through Purview."*

[pause]

**MORGAN:** That last sentence. *Automatic and queryable through Purview.* That's a lot of governance work being done quietly.

**KEVEN:** Quietly is the point. Most of the framework's hardest engineering is *quiet* — it just works. The Purview lineage is wired in by the platform, not by the data engineer. The data engineer focuses on the canonical mapping; Purview does the lineage. That's leverage.

### One disagreement

**MORGAN:** OK. Let me push on something. The framework is *very* prescriptive about — *canonical lives at Silver. Per-Service Gold marts. Don't blur.* I want to push on whether this is *always* the right call.

**KEVEN:** Go.

**MORGAN:** Consider a small engagement. Single Practice. Single Service. The client wants to ship in twelve weeks, not twenty. They don't need the scaffolding for *eventually adding seven Services* — they just need to ship one Service.

Is the canonical-at-Silver discipline *over-engineering* for that case?

**KEVEN:** I want to defend the discipline even for the small case. Here's why.

The framework's claim — and this is testable — is that *building the canonical Silver doesn't cost much more than building a Service-specific shape.* Because the canonical *already exists* in the schema library. The engagement is *mapping*, not *designing.* The marginal cost of using the canonical for a single-Service engagement is small.

The marginal *benefit* is the option value. The engagement that did the canonical mapping has a one-week path to adding the second Service. The engagement that *skipped* canonical to save a sprint has a six-week path. The CFO at the client sees both options *eventually.*

So my answer is — *for any engagement that has a credible Wave 2, do canonical at Silver from Wave 1.* The bar for "credible Wave 2" is low.

**MORGAN:** And for engagements that genuinely won't have a Wave 2 —

**KEVEN:** *Then* the lighter shape is defensible. But that's a small minority of engagements. Most clients buy APEX *because* they want a platform that supports multiple Services. Canonical at Silver is what lets the platform fulfill that promise.

**MORGAN:** OK. *Default to canonical at Silver. Light pattern only for engagements with no Wave 2 horizon.*

**KEVEN:** Yes.

### What to carry forward

**KEVEN:** OK. Three things to carry into Episode Four.

One — *Bronze absorbs reality. Silver anchors canonical. Gold shapes decisions per Service.* That's the medallion in one sentence.

Two — *canonical schemas pre-exist in the framework's schema library.* Fourteen families across seven Practices. Each grounded in industry standards. The engagement maps; it doesn't design.

Three — *velocity is a separate dimension.* Four tiers. Every Service uses multiple. Velocity is designed in, not discovered later.

**MORGAN:** And Episode Four —

**KEVEN:** Episode Four — *The Agent and Its Tools.* How the agent reaches Gold data without breaking governance. MCP. The Agent Framework. The audit row. The last foundation episode before we start with business needs.

**MORGAN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn

- **Microsoft Fabric — Medallion lakehouse architecture** · [Microsoft Learn](https://learn.microsoft.com/fabric/onelake/onelake-medallion-lakehouse-architecture)
- **Microsoft Fabric — Real-Time Intelligence Eventhouse** · [Microsoft Learn](https://learn.microsoft.com/fabric/real-time-intelligence/eventhouse)
- **Microsoft Fabric — Direct Lake mode** · [Microsoft Learn](https://learn.microsoft.com/fabric/get-started/direct-lake-overview)
- **Microsoft Purview — Data lineage in Fabric** · [Microsoft Learn](https://learn.microsoft.com/purview/concept-data-lineage)

### Microsoft Tech Community blogs

- **"Building canonical schemas on Fabric Silver"** · Microsoft Fabric Blog
- **"Why per-Service Gold marts beat shared Gold"** · Azure AI Blog
- **"The four velocity tiers — picking the right one"** · Microsoft Fabric Blog

### Architecture references

- **Azure Architecture Center — Medallion architecture in Fabric** · [Microsoft Learn](https://learn.microsoft.com/fabric/onelake/onelake-medallion-lakehouse-architecture)
- **OneLake reference architecture** · Microsoft Learn

### Industry context — schema standards referenced

- **FHIR R4** (Healthcare) · [hl7.org/fhir](https://www.hl7.org/fhir/)
- **GS1 standards** (Retail) · [gs1.org](https://www.gs1.org/)
- **AIAG quality standards** (Automotive) · [aiag.org](https://www.aiag.org/)
- **SAE J-standards** (Automotive) · [sae.org](https://www.sae.org/)
- **Common Information Model (CIM)** (Utilities) · IEC 61970/61968
- **OSDU Data Platform** (Oil & Gas) · [osduforum.org](https://www.osduforum.org/)

### Industry context — architectural

- *"Lakehouse: A New Generation of Open Platforms"* · Armbrust et al., CIDR 2021
- *"Designing Data-Intensive Applications"* — Chapter on stream processing · Martin Kleppmann
- *"Building the Data Lakehouse"* · Bill Inmon (yes, the same Inmon)

### From the APEX Trilogy

- **Services Guide — *From Raw to Silver* chapter** — the conformance discipline this episode summarised
- **Services Guide — *Schema Library Deep Dive* chapter** — the fourteen canonical families in detail
- **Services Guide — *Data Velocity, Thresholds & Activator* chapter** — the velocity-tier engineering this episode previewed

---

**End of Episode 03 · The Medallion in Depth**
*≈ 5,500 words · target 30 minutes at conversational pace*
