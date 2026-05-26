# Episode 04 · Gold Tier — Decision-Ready Data

**Source:** *Professional APEX-M Services Guide* — Part IV (Chapters 13, 14, 15)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: a chair pushing back, footsteps to a whiteboard]

**MORGAN:** Here's a moment that has happened to me four times on four different engagements. We're in the architecture review, sprint five-ish, and somebody — usually a smart engineer who is *trying to do the right thing* — says, *"the agent should just query Silver directly. It's already canonical. Why do we need Gold at all?"*

[pause]

**KEVEN:** And the answer is —

**MORGAN:** And the answer is — *because Silver answers the question "what is the truth," and Gold answers the question "what does the Service need to decide right now," and those are completely different shapes of data.* Silver is normalised. Silver is canonical. Silver is *slow.* Gold is denormalised. Gold is Service-shaped. Gold is *fast.* The agent doesn't need truth. The agent needs decision-ready truth, in a form it can read in two-hundred milliseconds, through an MCP tool that returns a stable contract.

**KEVEN:** And that's the third tier.

**MORGAN:** That's the third tier. Today's episode is the architecture of *the agent's view of the world.*

**KEVEN:** I'm Keven Markham.

**MORGAN:** I'm Morgan. APEX Services Podcast, Episode Four. *Gold Tier — Decision-Ready Data.*

---

## Theme Statement

**KEVEN:** Part Four of the Services Guide. Three chapters. Smaller than Bronze and Silver — but the chapters land harder because they're the last hop before the agent.

Chapter Thirteen — *Microsoft Fabric Lakehouse Patterns.* Chapter Fourteen — *Per-Service Gold Marts.* Chapter Fifteen — *Agent MCP Tool Surface.*

**MORGAN:** And the through-line.

**KEVEN:** *Gold is shaped for the agent's decision, not the analyst's question.* That single sentence is the entire design discipline.

---

## The Story

### Lakehouse patterns (Chapter 13)

**KEVEN:** Chapter Thirteen. *Microsoft Fabric Lakehouse Patterns.* Now — there's some terminology here that confuses people. Microsoft has "lakehouse" and "warehouse" as two separate items in Fabric. The chapter walks the choice.

**MORGAN:** Lakehouse versus warehouse for Gold. Let me push — when each?

**KEVEN:** Three rules of thumb.

Rule one — *if your Gold consumers are mostly notebooks, ML pipelines, Spark jobs, or Power BI Direct Lake — use a lakehouse for Gold.* Lakehouse gives you delta tables you can read from any compute engine.

Rule two — *if your Gold consumers are mostly T-SQL queries, stored procedures, traditional BI tools — use a warehouse for Gold.* Warehouse gives you a SQL endpoint with proper transaction semantics, and the analyst's tooling assumes T-SQL.

Rule three — *if your Service is agent-led — lakehouse.* Because the MCP tool layer is going to read through Spark or notebook or Direct Lake far more often than through T-SQL. The agent-led pattern is the dominant APEX pattern, so the default for Gold is *lakehouse*.

**MORGAN:** And the per-Service Gold layout. Section thirteen point — has the standard layout?

**KEVEN:** Yes. The APEX standard Gold layout — *per-Service lakehouse, with a small set of denormalised tables shaped for the MCP tools that consume them.* The Service might have five to ten Gold tables. Each table is denormalised — Silver canonical joins are pre-resolved — and indexed for the query patterns the MCP tools will run.

**MORGAN:** Section thirteen point — *materialised views and pre-computed aggregates.*

**KEVEN:** Right. Most agent queries don't need raw rows — they need *aggregations.* Last-30-days returns by SKU. Open warranty claims by VIN cohort. Current excursion status by store. These are pre-computed in Gold as materialised views, refreshed on the Service's freshness SLA. The agent's MCP tool reads the pre-computed answer, not the underlying rows.

**MORGAN:** And the freshness SLA — section thirteen point — *Gold freshness contracts.*

**KEVEN:** Each Gold mart declares a freshness contract. *"This table is no more than 90 seconds stale."* *"This aggregate is refreshed every 5 minutes."* The contract is part of the Service manifest. The conformance pipeline tags every Gold row with its source-Bronze-extraction time. The freshness contract is enforceable, observable, and queryable. If a Gold table is stale, the MCP tool raises that to the agent — and the agent can decide to surface the staleness in its answer.

### Per-Service Gold marts (Chapter 14)

**MORGAN:** Chapter Fourteen. *Per-Service Gold Marts.* The chapter that says — *one mart per Service.* Why?

**KEVEN:** Three reasons.

One — *isolation.* If a Service A is reshaping its Gold mart, Service B's mart is unaffected. They share Silver canonical; they don't share Gold.

Two — *agent stability.* The MCP tools consume *this Service's* Gold tables. They depend on stable contracts. A shared Gold layer would mean every Service's agent depends on schemas other Services could change.

Three — *capacity isolation.* Each Service's Gold lakehouse runs in its Practice workspace, against its own capacity quota. Heavy aggregation on Service A doesn't starve Service B.

**MORGAN:** Section fourteen point — the standard mart shape. Walk through.

**KEVEN:** Right. The APEX standard Gold mart has three layers within the lakehouse.

**Layer one — denormalised fact tables.** One table per primary fact the Service tracks. Returns, claims, excursions, build records. Each fact denormalised — Silver joins resolved.

**Layer two — pre-computed aggregates and materialised views.** The KPI-level views the agent reads constantly.

**Layer three — staging slots for agent ephemeral state.** When an agent needs to record intermediate state — *"I just generated this recommendation, the human is reviewing"* — it writes to staging Gold tables. These are Service-scoped, agent-writeable, time-bounded. They feed back into the LEDGER learning loop we'll cover in Episode Seven.

**MORGAN:** And the engineering pattern.

**KEVEN:** Section fourteen point — *the Gold-mart bootstrap.* Every new Service gets a bootstrap Gold mart from a template. The template includes — empty fact tables matching the Service's Silver-consumption manifest, the agent-staging slots, the freshness contract declarations, the materialised-view stubs. The data engineer fills in the materialised-view queries during the Service's build sprint.

**MORGAN:** Section fourteen point — *the multi-Service-on-same-Silver pattern.* Cross-Service composition at the data layer.

**KEVEN:** Yes. Two RC Services that consume the same RC Order canonical — say a returns-fraud Service and a markdown-optimisation Service — each have their own Gold mart. The Silver canonical is the shared anchor. The Gold marts are different shapes of the same truth, optimised for different decisions.

### Agent MCP tool surface (Chapter 15)

**MORGAN:** Chapter Fifteen. *Agent MCP Tool Surface.* The boundary between data and reasoning.

**KEVEN:** Yes. And this chapter is short — maybe the shortest in the Services Guide — but every paragraph matters.

Section fifteen point — *the tool catalog per Service.* Every Service declares its MCP tool catalog in the Service manifest. Typically five to fifteen tools. Each tool has a name, a description, an input schema, an output schema, and a Gold-table-read mapping.

**MORGAN:** Example.

**KEVEN:** Returns-fraud Service. MCP tools include — *get_returns_by_customer*, *get_recent_purchase_pattern*, *get_store_returns_rate*, *get_known-fraud-cohort*, *compute_risk_score*, *record_recommendation*. Each tool is small. Each tool has a tight schema. The agent uses these as building blocks.

**MORGAN:** Section fifteen point — *tool design principles.*

**KEVEN:** Five principles.

Principle one — *one tool, one purpose.* Don't build a "do_everything" tool. Build six small ones.

Principle two — *return structured data, not free text.* The agent will reason over the structured fields. Free text destroys reasoning fidelity.

Principle three — *include source metadata in every return.* Freshness timestamp, Gold-table version, Silver-canonical version. The agent's answer carries lineage.

Principle four — *narrow the input contract.* If the agent only needs to query by customer ID, the tool accepts customer ID. Not customer ID and a SQL where clause.

Principle five — *make tools read-only by default.* Write tools are a separate, audited category. Most APEX tools are read-only. Section fifteen point — *the read-write tool separation.*

**MORGAN:** Section fifteen point — *the MCP server architecture.* Where the tools actually run.

**KEVEN:** Same as Episode One — Azure Container Apps for most cases, Azure Functions for lightweight per-tool. Each Service has *its own MCP server.* The server is a small Python or TypeScript app that implements the MCP protocol, registers the catalog of tools, and routes tool invocations to the Gold-mart queries underneath.

**MORGAN:** And the identity?

**KEVEN:** Each MCP server runs under a managed identity bound to its Service's Gold lakehouse. *Read* permissions on Gold. Write permissions only on staging Gold tables. No access to Silver. No access to Bronze. The identity model means the MCP server can't accidentally leak.

**MORGAN:** Section fifteen point — *MCP server testing*.

**KEVEN:** Critical. APEX ships a *contract-test harness* for MCP servers. The tests assert — *for every tool, given the schema, every output conforms.* The tests run as part of CI. If a Gold-mart change breaks a tool's contract, CI fails. The agent's contract with data is stable.

### Pulling Part IV together

**MORGAN:** Synthesis. Three architectural beats for Gold.

**KEVEN:** Three beats.

One — *Gold is per-Service, lakehouse-default, shaped for decisions not for analysis.*

Two — *the MCP tool surface is the narrowing point.* Small tools. Read-only by default. Structured returns. Source metadata.

Three — *the agent never sees a database connection string.* The agent sees a tool catalog. The catalog enforces every other constraint downstream.

---

## APEX Facts

**MORGAN:** APEX Facts. Eight rapid.

**KEVEN:** Fact One — default Gold storage type in APEX?

**MORGAN:** Lakehouse. Warehouse only when analyst T-SQL is dominant.

**KEVEN:** Fact Two — three layers inside the standard Gold mart?

**MORGAN:** Denormalised facts, pre-computed aggregates, agent-ephemeral staging.

**KEVEN:** Fact Three — Gold-mart-per-what?

**MORGAN:** Per-Service. Shared Silver canonical, separate Gold marts.

**KEVEN:** Fact Four — typical MCP tool count per Service?

**MORGAN:** Five to fifteen.

**KEVEN:** Fact Five — MCP tool data return type?

**MORGAN:** Structured. Not free text. With source metadata.

**KEVEN:** Fact Six — default MCP tool permission?

**MORGAN:** Read-only. Write tools are a separate audited category.

**KEVEN:** Fact Seven — what enforces the agent-data contract?

**MORGAN:** The MCP server contract-test harness. CI runs them.

**KEVEN:** Fact Eight — what does the agent see at runtime, in terms of data?

**MORGAN:** A tool catalog. Never a connection string.

**KEVEN:** Time.

---

## Adopt / Hold

**MORGAN:** Adopt versus Hold. Keven, Adopt.

**KEVEN:** Adopt — *per-Service Gold marts as the default, full stop.* Don't share Gold across Services. The temptation will arise — *"both Services need this aggregate, let's put it in a shared mart."* Don't. Compute it twice if you have to. The isolation cost is small. The cross-Service coupling cost is enormous.

**MORGAN:** Hold. When is per-Service Gold the wrong answer?

Two cases.

Case one — *legitimately shared reference data.* The store-master, the product-master, the dealer-master — these don't belong in any one Service's Gold. They're shared reference. They live in a *shared reference lakehouse* that all Services' MCP tools can shortcut to. Section thirteen point — *the shared-reference pattern.*

Case two — *Wave Two cross-Service orchestrations* that need a unified view. When you compose three Services into a higher-order orchestration, you may legitimately need a higher-order Gold mart that joins across the Service Gold marts. But this is *Wave Two+ design* — not Wave One.

**KEVEN:** Synthesis?

**MORGAN:** Wave One Gold is per-Service. Wave Two may introduce composed Gold marts for cross-Service workloads. Shared reference data lives in a dedicated shared-reference lakehouse, not in any single Service.

---

## Lessons

**KEVEN:** Monday-morning lessons.

One — **on Service kickoff, list the five-to-fifteen MCP tools your agent will need first. Write the tool contracts. Then design the Gold mart that supports them.** Top-down from the agent's API, not bottom-up from the data.

Two — **make every MCP tool return source metadata.** Freshness timestamp. Silver-canonical version. Gold-mart version. The agent's audit trail benefits. The debugging benefits more.

Three — **never let an MCP tool accept a free-form SQL clause.** Narrow inputs. Always. If you find yourself parameterising the SQL, stop. Build another tool.

Four — **stand up the MCP contract-test harness before you write the second tool.** It pays for itself in week two.

Five — **declare freshness contracts on every Gold mart.** Even if the answer is "best effort, no SLA." The declaration forces a design conversation that prevents later disasters.

---

## Carve Outs

**MORGAN:** Carve outs. Mine — section fifteen point — *MCP tool design principles* — five rules. Read them twice. They're the single best engineering checklist in the Services Guide. Print them. Put them next to your monitor.

**KEVEN:** Mine — Chapter Fourteen, the section on *agent-ephemeral staging slots in Gold.* This is the connection point between the data layer and the LEDGER learning loop. The staging slots are how the agent's intermediate state becomes data the system learns from. We'll go deep in Episode Seven, but the seed of that conversation is in Chapter Fourteen. Read it now, re-read it later.

---

## Sign-off

**KEVEN:** That's it for Episode Four. The medallion is now complete. Next episode — *Orchestrations.* Part Five of the Services Guide. Seven chapters. Workflow patterns. Agent orchestration archetypes. Microsoft Agent Framework deep dive. Responsible AI. n8n on laptop, Logic Apps hybrid. Cross-Service composition. The biggest Part in the book.

**MORGAN:** See you there.

[outro]

---

**End of Episode 04 · Gold Tier — Decision-Ready Data**
*≈ 4,950 words*
