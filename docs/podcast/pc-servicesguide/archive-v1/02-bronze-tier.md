# Episode 02 · Bronze Tier — Ingesting the Real World

**Source:** *Professional APEX-M Services Guide* — Part II (Chapters 4, 5, 5A, 6, 7)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: Slack notification ping, then another, then a third in rapid succession]

**MORGAN:** It's two-fifteen on a Wednesday. I'm in the middle of a sprint review. And in my Slack DMs I get three messages from three different team members in five minutes.

Message one — *"the Bronze pipeline is failing — the SOR changed the column order."*

Message two — *"Real-Time Intelligence Eventhouse is dropping events — we're at queue depth fifteen thousand."*

Message three — *"Purview just flagged a PII leak in the Silver build — I think someone left customer names un-tokenized."*

[pause]

**KEVEN:** And the part of you that wants to fix all three at once —

**MORGAN:** — is the wrong part of me. Because all three problems live at the Bronze tier. And in delivery, the Bronze tier is where most of your operational risk lives — and most of your governance risk — and most of the variance you cannot predict in advance. Part Two of the Services Guide is the chapter every data engineer on APEX has to internalise. Today we walk it.

**KEVEN:** I'm Keven Markham.

**MORGAN:** I'm Morgan. APEX Services Podcast, Episode Two. *Bronze Tier — Ingesting the Real World.*

---

## Theme Statement

**KEVEN:** Part Two of the Services Guide. Five chapters. Chapter Four — Source-of-Record inventory by industry. Chapter Five — the Real-Time Hub pattern with Fabric Real-Time Intelligence. Chapter 5A — Data Velocity, Thresholds, and Activator — from signal to decision. Chapter Six — Ingestion and Tokenization. Chapter Seven — PII Classification and the pii-unlock identity.

**MORGAN:** And the through-line —

**KEVEN:** The through-line is — *Bronze is where the messy real world hits the platform.* Every operational risk, every governance risk, every velocity question lives here. The discipline of Bronze design is the discipline of the entire engagement.

---

## The Story

### SOR inventory by industry (Chapter 4)

**MORGAN:** Chapter Four. Source-of-Record inventory. The chapter starts with a pattern — section four point one — *the SOR pattern across the catalog.* What's the pattern?

**KEVEN:** Every Practice has a *predictable* set of SORs. For RC — point of sale, e-commerce, ERP for inventory and pricing, the loyalty system, the customer service system, the warehouse management system. For HLS — the EHR, the claims platform, the patient portal, the lab system, the PACS imaging system. For AXLE — the MES, the PLM, the warranty system, the connected-vehicle telematics platform, the dealer DMS. The Sellers Guide names the Practices. The Services Guide names the *systems.*

**MORGAN:** Section four point two. SOR-to-Bronze connection pattern.

**KEVEN:** Four canonical connection patterns. They map almost one-to-one to the Fabric integration patterns we covered in the Sellers Podcast Episode Three.

**Mirrored Database** — for operational databases. SQL Server, Postgres, Cosmos DB, Snowflake. Fabric pulls live CDC into OneLake. No ETL.

**Eventstream / Eventhouse** — for streaming sources. IoT, telemetry, application events. Section four point three.

**Pipeline ingestion** — for SaaS sources with batch APIs. Salesforce, ServiceNow, Workday. DataFactory pipelines on schedule.

**Custom endpoint** — webhook-style push. For sources that can push but can't be mirrored.

**MORGAN:** Section four point four — the SOR connection inventory file. This is the artefact that every engagement produces in week one.

**KEVEN:** Yes. The SOR connection inventory. It's a structured document — YAML or JSON — that catalogues, for every Service in scope: the SOR name, the source-system owner, the data steward, the connection pattern, the ingestion identity, the PII classification, the Bronze landing location, the refresh cadence, and the SLA expectation. *Every* Service. The file is the source of truth for the engagement's data state.

**MORGAN:** And the failure mode if you don't build it.

**KEVEN:** The failure mode is — twelve weeks in, somebody asks *"where does the customer phone number come from in this Service?"* and nobody knows. The inventory prevents that.

### Real-Time Hub pattern (Chapter 5)

**MORGAN:** Chapter Five. The Real-Time Hub pattern. Microsoft Fabric Real-Time Intelligence. And this is the chapter that explains how APEX handles *streaming* Bronze.

**KEVEN:** Right. Five sections. Let me hit them.

**Section five point one — the RTI components.** Eventstream — the ingestion. Eventhouse — the KQL queryable store. Reflex / Activator — the trigger engine. Real-Time Dashboard — the live visualisation. Together they form what APEX calls *the Real-Time Hub.*

**Section five point two — the pattern.** Streaming events arrive at Eventstream. Eventstream tees the stream to two destinations — Eventhouse for query-and-trigger, and OneLake delta tables for batch downstream. That tee is critical. It means *the same stream feeds both the real-time trigger plane and the analytical Bronze.*

**MORGAN:** Section five point three. The excursion-trigger example. This is the worked example.

**KEVEN:** Cold-chain excursion. The classic RC scenario. A store cooler temperature reading every fifteen seconds. Eventstream picks it up. Activator fires a threshold rule — *"if cooler temperature greater than thirty-eight degrees for more than three consecutive readings."* The trigger invokes the cold-chain excursion agent through an MCP tool. The agent emits the response — alert, recommended action, recall scope — and the audit row lands in Purview within five seconds end-to-end. Section five point three has the full sequence diagram.

**MORGAN:** Section five point four — streaming-Bronze versus batch-Bronze in the same Service.

**KEVEN:** This matters in delivery. Most Services need both. The cold-chain Service needs *streaming Bronze* for the cooler events and *batch Bronze* for the daily sales feed. Same Service. Two ingestion patterns. The Bronze layer accepts both. The Silver canonical reconciles them. That's the discipline.

### Data velocity, thresholds & Activator (Chapter 5A)

**KEVEN:** Chapter 5A. *Data Velocity, Thresholds and Activator — From Signal to Decision.* This is one of the densest chapters in the Services Guide. Thirteen sub-sections. The core idea is the *four-tier velocity spectrum* — section 5A point one.

**Tier One — Real-Time Streaming via Eventhouse.** Sub-second to single-digit-seconds latency. KQL-queryable. The Activator engine fires here. Section 5A point two.

**Tier Two — Semi-Real-Time via Direct Lake and Mirrored Database.** Seconds to minutes latency. Direct Lake makes OneLake delta tables queryable by Power BI without refresh. Mirrored Database makes operational DBs queryable through OneLake in near-real-time. Section 5A point three.

**Tier Three — Periodic Feeds via Data Pipelines and Scheduled Refresh.** Minutes to hours latency. The classic ETL path. Section 5A point four.

**Tier Four — Redis Hot Cache.** Used for working memory and episodic memory in agent loops. Sub-millisecond. Section 5A point five. We'll come back to this in Episode Seven when we cover LEDGER and the superagent learning loop.

**MORGAN:** And the practical use of the four-tier spectrum?

**KEVEN:** In design, you classify every data dependency against the spectrum. Section 5A point ten — *Composing Tiers Across a Single Service.* Most Services use three of four tiers. A cold-chain Service uses Tier One for cooler events, Tier Three for daily sales, Tier Four for the agent's working memory of which stores are in excursion this week. The Tier classification is a *design artefact*, not just a concept.

**MORGAN:** Section 5A point six — thresholds taxonomy. The Activator side.

**KEVEN:** Right. Four threshold patterns.

**Static thresholds** — a fixed number. Cooler over thirty-eight degrees.

**Dynamic thresholds** — calculated from rolling statistics. Cooler more than two standard deviations above its own seven-day baseline.

**Composite thresholds** — combinations of conditions. Cooler over thirty-eight AND door-open count over five in the last hour AND no manual override.

**ML-driven thresholds** — a model produces the threshold. Used for anomaly detection where the threshold itself is non-stationary.

**MORGAN:** And the threshold-to-action mapping — section 5A point seven.

**KEVEN:** Three action classes. **Notify** — surface an alert. **Trigger** — invoke an agent or workflow. **Act** — execute an autonomous action under policy. The three correspond to the HITL / HOTL / HIC spectrum from the Sellers Guide. The action class is selected at design time based on reversibility and regulator posture.

**MORGAN:** Microsoft Fabric Activator deep dive — section 5A point eight.

**KEVEN:** Activator — formerly Reflex — is the rule engine inside RTI. It evaluates Eventhouse KQL queries continuously and fires actions when thresholds breach. It's the *trigger plane* for everything in APEX that's not user-initiated. Section 5A point nine has per-Practice use cases — section 5A point eleven has the trigger-to-decision audit trail. The audit row is critical: every Activator trigger produces a row showing the rule version, the input data window, the threshold value, the breach value, the action fired, the downstream agent invocation ID. That row is hash-chained into the APEX audit.

**MORGAN:** Section 5A point twelve. Anti-patterns.

**KEVEN:** Three. *Don't put business logic in Activator rules* — Activator triggers; logic lives in agents. *Don't use Activator for non-time-sensitive decisions* — pipelines do that better, cheaper. *Don't fan out Activator triggers to many destinations* — fan out from the agent or the orchestration; keep Activator as the trigger boundary.

### Ingestion and tokenization (Chapter 6)

**MORGAN:** Chapter Six. Ingestion and tokenization. The chapter that explains the data-engineering side of Bronze.

**KEVEN:** Yes. Section six point one — the ingestion pipeline in stages. Four stages.

**Stage one — connect.** The Fabric pipeline establishes a connection to the SOR using the ingest identity.

**Stage two — extract.** Pulls bytes. Validates basic schema.

**Stage three — tokenize.** Section six point two. Any identified PII is replaced with a token. The mapping lives in a tokenization vault. The original value never reaches Bronze.

**Stage four — land.** The tokenized payload lands in the Bronze lakehouse with metadata.

**MORGAN:** The tokenization pattern. Section six point two. Walk me through.

**KEVEN:** The pattern uses a deterministic tokenizer. *Same input always produces the same token within a tokenization scope.* That means downstream joins still work — a customer's tokenized ID in the orders table matches the same customer's tokenized ID in the loyalty table. The actual customer ID is never seen by Bronze, Silver, Gold, or the agent — except through the pii-unlock identity, which is Chapter Seven.

**MORGAN:** Section six point three. The ingest identity.

**KEVEN:** The ingest identity is a managed identity bound to the DataFactory pipeline. It has read on the SOR, write on the Bronze lakehouse, and call on the tokenization service. It does *not* have access to anything else. Especially not agents. Especially not Gold. The blast radius of an ingest identity compromise is bounded.

**MORGAN:** Section six point four. DataFactory pipeline patterns.

**KEVEN:** Four pipeline patterns that APEX uses, by source shape. **Single-tenant SOR mirror.** **Multi-source merge.** **Streaming-with-replay**. **API-poll with backfill.** Each has a template in the Services Guide. Sprint planning becomes a question of picking the right template and customising it — not designing from scratch.

### PII classification and pii-unlock (Chapter 7)

**MORGAN:** Chapter Seven. PII Classification and the pii-unlock identity. The governance chapter of Bronze. Walk me through.

**KEVEN:** Right. The model is — *every Bronze table is automatically classified for PII at landing.* Microsoft Purview's classifiers run. Sensitivity labels are applied. The label *propagates downstream* with the data into Silver, into Gold marts, into MCP tool responses, into agent outputs.

**MORGAN:** And the pii-unlock identity?

**KEVEN:** This is the elegant part. The *normal* path through APEX — Bronze to Silver to Gold to MCP tool to agent — *never sees the un-tokenized PII.* The agent sees tokens. The Power BI reports see tokens. The audit trail records tokens.

When a *human* needs to act on real PII — a customer service rep needs the actual phone number to call the customer — they invoke the pii-unlock identity. The pii-unlock identity is a *separate*, audited, high-privilege identity that has read access on the tokenization vault. It returns the un-tokenized value for *exactly one* token, logs the access, and the audit trail captures the row.

**MORGAN:** Who can hold pii-unlock?

**KEVEN:** Section seven point — the pii-unlock identity policy. It's policy-controlled in Entra. A user is granted pii-unlock for specific token namespaces, for specific business purposes, with time-bounded delegations. The CCO sees the access log. Purview audits every unlock. The auditor reads the trail.

**MORGAN:** And the practical effect?

**KEVEN:** The practical effect is — *the data flowing through the agent stack is PII-free by construction.* The agent cannot leak PII because it doesn't have it. The Power BI dashboards cannot leak PII because they don't have it. The unlock is a separate, narrow, audited path used only by humans for specific operational moments. That's the governance posture that makes APEX deployable in regulated industries.

**MORGAN:** And the engineering rule?

**KEVEN:** The engineering rule — *no Bronze table is created without an applied sensitivity classification.* No exceptions. If a Bronze table lands without a classification, the pipeline is broken. The platform refuses. Section seven point — *the pipeline classification gate.*

### Pulling Part II together

**MORGAN:** Synthesis. Five takeaways for a data engineer.

**KEVEN:** Five takeaways.

One — *the SOR connection inventory is a week-one deliverable.* Don't skip it. Don't defer it.

Two — *the Real-Time Hub tees Eventstream into both Eventhouse and OneLake.* That tee is the architecture. Don't break it.

Three — *every Service classifies its data against the four velocity tiers in design.* Tier classification is a design artefact.

Four — *tokenization happens at ingest, before Bronze landing.* PII never reaches Bronze in cleartext. The agent never sees PII.

Five — *Activator triggers — not business logic.* Logic lives in agents and orchestrations. Activator is the trigger boundary.

---

## APEX Facts

**MORGAN:** APEX Facts. Eight rapid.

**KEVEN:** Fact One — week-one Bronze deliverable artefact?

**MORGAN:** SOR connection inventory.

**KEVEN:** Fact Two — four velocity tiers?

**MORGAN:** Real-time Eventhouse, semi-real-time Direct Lake / Mirrored DB, periodic pipeline, Redis hot cache.

**KEVEN:** Fact Three — four threshold patterns?

**MORGAN:** Static, dynamic, composite, ML-driven.

**KEVEN:** Fact Four — three Activator action classes?

**MORGAN:** Notify, trigger, act.

**KEVEN:** Fact Five — Eventstream tee destinations?

**MORGAN:** Eventhouse and OneLake delta.

**KEVEN:** Fact Six — what identity ingests SOR data?

**MORGAN:** The ingest identity — a managed identity bound to the DataFactory pipeline.

**KEVEN:** Fact Seven — where does cleartext PII live in the APEX stack?

**MORGAN:** Only in the tokenization vault, accessed via pii-unlock identity for specific human operational moments.

**KEVEN:** Fact Eight — Activator anti-pattern?

**MORGAN:** Don't put business logic in Activator rules. Triggers only.

**KEVEN:** Time.

---

## Adopt / Hold

**MORGAN:** Adopt versus Hold on Bronze patterns. Keven, Adopt.

**KEVEN:** Adopt — *the Eventstream-to-Eventhouse-and-OneLake tee as the canonical streaming-Bronze pattern.* Single ingestion, two consumption paths — real-time trigger and analytical Bronze — perfectly aligned with the APEX layering. Every streaming Service uses this.

**MORGAN:** Hold. When does this pattern get over-applied?

Two cases.

Case one — *very high-volume telemetry where the tee creates double-cost.* For a hundred-thousand-events-per-second sensor feed, you may decide Eventhouse is the *only* Bronze for the streaming side, and the analytical Bronze gets a periodic export from Eventhouse rather than the live tee. Section five point — has the cost trade-off. This is an optimisation; default is still the tee.

Case two — *if your streaming source has its own real-time queryable store already* — Snowflake real-time tables, for instance — *and the engineering cost of doubling that into Eventhouse exceeds the architectural value.* In that case, Microsoft-hosted MCP for RTI may let you bridge directly. Section 1A point ten covers the preview.

**KEVEN:** Synthesis?

**MORGAN:** Default to the tee. Optimise when cost actually bites. Don't optimise prematurely.

---

## Lessons

**KEVEN:** Monday-morning lessons.

One — **on sprint zero, write the SOR connection inventory.** Even rough. Even with "TBD" against half the fields. Get it on paper.

Two — **for every Service, run the four-velocity classification exercise in design.** Where does each data input land on the spectrum? Mismatched velocity drives most operational pain in delivery.

Three — **never write an Activator rule that contains business logic.** Threshold-and-trigger only. If you find yourself writing logic in KQL, stop. Move it into the agent.

Four — **before any Bronze pipeline goes to production, run a Purview classification check.** Make sure every column got a sensitivity label. The pipeline-classification gate is real.

Five — **on day one of the engagement, decide who holds pii-unlock and document the policy.** Section seven point — the pii-unlock identity policy. This is the conversation that runs longest with the client's CCO. Get it scheduled in week one.

---

## Carve Outs

**MORGAN:** Carve outs. Mine — read Chapter 5A end-to-end. *Data Velocity, Thresholds and Activator.* The four velocity tiers and the four threshold patterns are the framework you'll come back to on every Service. Memorise the table on section 5A point one.

**KEVEN:** Mine — read the *Deployment Guide* section on Bronze operations in parallel with this. The Services Guide tells you how to *build* Bronze. The Deployment Guide tells you how to *run* Bronze in production — pipeline monitoring, Eventhouse capacity management, tokenization vault rotation. The two together are the full Bronze story.

---

## Sign-off

**KEVEN:** That's it for Episode Two. Next episode — *Silver Tier — Where Canonical Lives.* Part Three of the Services Guide. From raw to Silver — the conformance layer. The schema library deep dive. Industry schemas — fourteen families. Quality, lineage, Microsoft Purview. Entra ID and Purview governance deep dive. The most architecturally important episode of the series.

**MORGAN:** See you there.

[outro]

---

**End of Episode 02 · Bronze Tier — Ingesting the Real World**
*≈ 5,100 words*
