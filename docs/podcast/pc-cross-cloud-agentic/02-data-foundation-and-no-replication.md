# Episode 02 · Data Foundation and The No-Replication Principle

**Builds on:** Episode 1 (the five principles) · Trilogy — Services Eps 3-4 (medallion + MCP boundary)
**Run time:** ≈ 32 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: a data architect's office. Late night. The hum of a desktop fan. Two open laptops on the desk, both half-asleep. A whiteboard behind the desk with three columns scrawled in red marker — *Bronze · Silver · Gold* — and arrows pointing every direction except the right one. A coffee mug. A printout of an SOW with a yellow highlight running through the words *bulk extract.*]

**KEVEN:** I want to start tonight with the data architect's recurring nightmare. The one I have heard from a different practitioner in a different industry every six weeks for the last two years. Always the same shape.

**REID:** Walk it.

**KEVEN:** The architect is in their third project of the year. Different sponsor each time. Different business case each time. But every project arrives at the same paragraph in the SOW. *Bulk-extract the source data into a new lake.* SAP nightly extracts running at two in the morning, landing into a fresh Azure Data Lake. Snowflake replications running every four hours into a different fresh lake on the AWS side. The streaming sources — Kafka topics, change-data-capture from the operational systems — pulling down into yet another lake on a third project. The pile of copies grows. The lineage decays. The governance scope explodes.

**REID:** And every copy is somebody's full-time job to keep alive. Every replication pipeline is a thing that breaks at three in the morning and pages somebody. Every fresh lake is a new audit boundary that someone has to map back to the original sources.

**KEVEN:** Exactly. And the worst version of this story — the part I want to land before we even open the architecture — is that the agent the architect is being asked to build sits on top of all of those copies. So when the auditor asks *where did that recommendation come from*, the answer is, well, the agent read from this lake, which was extracted from that warehouse, which was loaded from that operational system on Tuesday, which itself was reconciled from those three upstream systems on Monday. Four hops back to the source. And every hop is a place where the data might have drifted from the authoritative system.

**REID:** And every hop is a place where the regulator stops trusting you. I have watched that audit conversation. It does not end well.

**KEVEN:** So the antidote — the principle that this episode is built on — is *No Replication.* Principle four from Episode 1. Sources stay untouched. The Gold Tier is composed from the sources via virtualization, mirroring, shortcuts, federation — never via bulk replication. The systems of record keep serving operations. The data warehouses keep serving BI. The streams stay live and authoritative. And the agent's audit trail can point one hop back to the source, not four.

**REID:** This episode is the one I have been waiting for. Because this is the episode where Microsoft has — today — productized the broadest expression of *don't replicate.* And it is also the episode where I get to be honest about where Google Cloud genuinely wins. We will get to BigQuery Omni. I am not going to soften it.

**KEVEN:** Good. Don't soften it. Episode two. *Data Foundation and the No-Replication Principle.* Let's go.

---

## The conversation

### Why the medallion architecture is the right starting frame

**KEVEN:** Before we name a single product, we have to frame the substrate. And the frame the series uses is the medallion. Bronze, Silver, Gold. Three tiers. The agent talks to Gold. Gold is composed from Silver. Silver is composed from Bronze. Bronze is the raw landing zone. That is the discipline.

**REID:** Let me add the nuance before you go further. The medallion is not new. The medallion is decades-old data-engineering practice. It existed before Databricks named it. It existed before Fabric named it. Bronze landing, Silver canonical, Gold composed — that is what serious data engineers have been doing under different names since the early data-warehouse era. So when somebody pitches the medallion to you like it is a 2024 innovation, push back. It is not.

**KEVEN:** Agreed. And the question that matters for this series is — *what is different about the medallion under an agentic workload?* Because the framing is old. The shape of Gold is new. Under a BI workload, Gold is shaped for analyst questions. *Show me revenue by region by quarter.* Pre-aggregated cubes. Slowly-changing dimensions handled carefully. Time-series at fixed grains. The Gold Tier under BI is the warehouse — denormalized, indexed for the predictable query patterns the BI team has been running for years.

**REID:** And under an operational workload, Gold is shaped differently again. *Give me this customer's current state.* Per-entity views. Low-latency joins. Operational data store patterns. Different shape.

**KEVEN:** And under an agentic workload, Gold is shaped for *agent reasoning patterns.* Which is a third shape. Not pre-aggregated BI cubes. Not low-latency operational views. Agents need per-entity composed context — every domain that touches this entity, every event in this entity's lifecycle, every signal from every adjacent system, joined together at the entity grain. That is a new shape of Gold. The agentic twist is that Gold is shaped *for* the agent, not for the analyst and not for the operator.

**REID:** And this is the part most architectures get wrong. They point the agent at the BI Gold Tier — at the warehouse — and they wonder why the agent's reasoning feels brittle. The agent is reasoning over a substrate that was never shaped for it. The substrate was shaped for somebody else's question. The agent is borrowing a tool that was made for a different hand.

**KEVEN:** And the fix is not to throw away the BI Gold Tier. The warehouse still has a job. The BI team still has questions. The fix is to compose a separate Gold Tier — agent-shaped — that lives alongside the warehouse and reads from the same Silver. The warehouse and the agent's Gold Tier are siblings, not the same thing.

**REID:** Siblings. Both children of Silver. Different shapes because they serve different consumers.

### Silver is canonical, not Gold

**KEVEN:** And this is the rule I want to nail down hard, because most architects get it backwards. Silver is the canonical layer. Gold is the composed layer. Not the other way around. The vocabulary is fuzzy across vendors — some references to the medallion use *Gold* to mean the canonical, single-version-of-truth layer, the place where customer is defined once and consistently. And then there is no clean layer above that for composition. So composition happens ad-hoc inside the BI tool or inside the application. And the architecture loses the discipline.

**KEVEN:** Let me walk it the way I want it walked. *Silver is canonical.* Silver is where the cross-system reconciliation happens. *Customer* is defined once, in one canonical schema, with one set of attributes, even though the source systems define customer six different ways. *VIN* is defined once. *Policyholder* is defined once. *Product* is defined once. *Account* is defined once. The canonical contract lives in Silver. Every downstream consumer trusts Silver to mean what it says.

**REID:** And Gold sits above that.

**KEVEN:** *Gold is composed per scenario.* Per-customer composed views. Per-VIN composed views. Per-policyholder, per-product, per-account composed views. Gold composes from Silver. Gold is where the agent reads. Gold is shaped for the reasoning question — *what does the world look like for this entity right now?* — and it joins together everything in Silver that touches that entity.

**REID:** So the agent talks to Gold. Gold composes from Silver. Silver enforces the canonical contract. Bronze is the raw landing layer.

**KEVEN:** That is the rule. And it is worth its own moment because once you have it backwards, every architecture conversation drifts. Every governance conversation drifts. The lineage breaks. The agent ends up reading something that nobody can defend as authoritative. Silver canonical. Gold composed. Said exactly that way.

**REID:** I have corrected this in field reviews more times than I can count. Architects who put the canonical contract in Gold and then have nowhere clean to compose from. The medallion only works when the canonical layer is the middle and the composition layer is on top.

**KEVEN:** Silver canonical. Gold composed. The discipline that protects every downstream conversation.

### Why agentic AI needs Gold-Tier-shaped views, not warehouse views

**KEVEN:** Now let's go deeper on why the agent's Gold Tier is shaped differently from the warehouse. Because this is the part where the architectural conversation either lands or collapses. The data warehouse — the BI Gold Tier, call it that — optimizes for one workload pattern. *Aggregate.* Group, filter, roll up, slice, dice. Pre-aggregated cubes. Materialized views computed nightly. Star schemas with conformed dimensions. Slowly-changing dimensions managed with surrogate keys. Time-series at fixed grains — daily, weekly, monthly. The warehouse is a magnificent piece of engineering. It is optimized for the questions analysts ask.

**REID:** And the questions analysts ask are predictable. Revenue by region. Cohort retention by quarter. Funnel conversion by channel. The warehouse pre-computes for those questions because those questions repeat.

**KEVEN:** Agent reasoning is different. The agent does not ask *revenue by region.* The agent asks *what does the world look like for this customer right now, given everything we know.* That is a per-entity question, not an aggregate question. The agent needs every signal that touches that customer — every transaction in the last ninety days, every service interaction, every product owned, every adjacent household member, every risk flag, every preference, every regulatory state — joined together at the customer grain. And it needs the same shape for the next customer. And the next. And the agent does not know which customer it will be reasoning about next.

**REID:** So pre-aggregation does not help. Pre-aggregation makes the answer *worse,* because the agent loses the granular signal it needs to reason. The warehouse strips out the per-event detail the analyst does not need. The agent needs that detail back.

**REID:** And the warehouse's slowly-changing-dimension handling — surrogate keys, effective dates, type-two history — that is built for *time-travel analytics.* For the analyst question *what did the customer look like as of last quarter.* The agent does not need that. The agent needs *what does the customer look like now,* with the relevant history attached as features.

**KEVEN:** Different workload. Different shape. Both legitimate. The mistake is forcing them onto the same substrate.

**REID:** So the architectural commitment is — the warehouse keeps doing its job. The BI team keeps querying it. The CFO's dashboards keep refreshing. *And* the agent's Gold Tier lives alongside it, composed from the same Silver, shaped per-entity, optimized for the reasoning question.

**KEVEN:** Two consumers. Two Gold Tiers. One Silver. One Bronze. The discipline holds.

### Microsoft Fabric — Mirroring, Shortcuts, Eventstreams

**KEVEN:** Now let's go cloud by cloud. I am going to start with Microsoft because Microsoft has, today, productized this broadest. Three capabilities that together express the no-replication principle across batch, lakehouse, and streaming. Mirroring. Shortcuts. Eventstreams. *Fabric Mirroring* first. Microsoft has productized managed mirroring of external sources into OneLake. Snowflake. Databricks. Cosmos DB. Azure SQL. Azure PostgreSQL. The list is growing. The mechanic is — the source data stays where it lives. Snowflake stays Snowflake. Databricks stays Databricks. Cosmos stays Cosmos. But a live-ish reflection of the data appears in OneLake, in Delta format, queryable by every Fabric workload — including the agent's Gold Tier composition pipeline.

**REID:** And the reflection is not a copy in the bulk-ETL sense.

**KEVEN:** The reflection is not a bulk copy. It is a change-data-feed-driven mirror. Source changes propagate. The source remains authoritative. The audit trail can point back to the source. The governance scope does not double because the mirror inherits lineage that connects back to the originator. Then *Fabric Shortcuts.* Different mechanic again. A shortcut is a pointer. You point at an S3 bucket, an ADLS path, a Dataverse table — and from the Fabric side, the data appears as if it lives in OneLake. But it does not live in OneLake. It lives where it lives. The metadata in OneLake says *here is the path; here is the schema; here is the access control.* The actual bytes never move.

**REID:** So a Fabric workload can query an S3 bucket without copying the bucket.

**KEVEN:** Without copying the bucket. The compute is on the Fabric side. The storage is on the AWS side. The agent's Gold Tier composition pipeline can reach across the shortcut and pull from S3 as if it were native OneLake. No replication. No ETL. The lineage tracks back to S3. And then *Fabric Eventstreams.* The streaming side of the same principle. Real-time sources — Kafka topics, Event Hubs streams, IoT Hub feeds — flow into Fabric without becoming persistent copies. The stream passes through. The agent's Gold Tier composition can consume the stream live. And when the regulated case requires persistence — for audit, for replay — Eventstreams can persist into OneLake as Bronze, with explicit retention policy. The default is pass-through. The persistence is opt-in.

**REID:** Let me validate that from the field. I have shipped Fabric Mirroring on Snowflake in production for one client. It works as advertised. The mirroring lag is single-digit minutes in the steady state. The reflection schema matches the source schema. The Purview lineage propagation is the differentiator — when you look at the lineage graph for a Fabric Gold table that composed from a Mirrored Snowflake source, the lineage carries through to the original Snowflake object. That is genuinely productized in a way that nobody else has caught up to yet.

**KEVEN:** And the Shortcut into S3 — I have walked that one with a client too. The architectural conversation is shorter than the team expects, because the answer is *we do not need to copy your S3 lake; we will shortcut to it.* The pushback you usually get to a Microsoft proposal — *you are going to make us replicate everything into Azure* — that pushback evaporates when you can answer it with Shortcuts.

**REID:** Three capabilities. Batch reflection via Mirroring. Lakehouse pointer via Shortcuts. Streaming pass-through via Eventstreams. Plus Purview lineage threading through all three. That is the broadest productized expression of *don't replicate* on any cloud today.

**KEVEN:** That is the claim. And I will defend it.

**REID:** You will defend it on the multi-modality breadth axis. I am going to push back on the cross-cloud axis in a few minutes. But the multi-modality breadth claim — Fabric is the densest. Conceded.

### GCP BigQuery Omni + BigLake — the strongest cross-cloud federation

**REID:** Let me take this one. Because this is where Google Cloud genuinely leads. *BigQuery Omni.* Google's productized cross-cloud query engine. Here is what it does. You have data sitting in an S3 bucket — AWS-side. You have data sitting in Azure Blob Storage — Microsoft-side. From a single BigQuery query surface, you can query both of those external buckets directly. And — this is the part that matters — the compute that runs the query runs *in the source cloud.* The query travels. The data does not.

**KEVEN:** Explain the compute placement.

**REID:** When the BigQuery Omni query targets an S3 bucket, BigQuery runs the compute on AWS infrastructure — provisioned for the Omni service, but living in the AWS region where the bucket lives. The bytes never cross the cloud boundary. The query result comes back to the BigQuery client. The egress cost is the query result, not the source data. Same mechanic for Azure Blob — the compute runs on Azure infrastructure in the region where the blob lives. The query result returns to BigQuery. The bulk source data stays put.

**KEVEN:** And this is the strongest cross-cloud federation story on the market today.

**REID:** Today, period. There is no productized equivalent on Microsoft or AWS that does this — compute-in-the-source-cloud cross-cloud federated query — at the same level of maturity. Microsoft has Shortcuts, which is a pointer, not a compute-pushdown. AWS has Athena Federated Query, which we will get to, but Athena's federation pattern is per-source-connector and the compute runs on AWS. BigQuery Omni is the only one that runs the compute in the source cloud across all three majors. And then *BigLake* is the broader umbrella. BigLake is Google's way of giving you BigQuery-style governance — row-level security, column-level security, fine-grained policies — over data that lives in Cloud Storage, in external object stores, in open table formats. Iceberg tables. Hudi tables. Delta tables in some cases. BigLake is the access-control overlay that makes Omni-style federation governable. Dataplex sits over that — the governance and lineage layer. Catalog, classification, lineage tracking, data quality. The three together — Omni for the cross-cloud query, BigLake for the access control, Dataplex for the governance — is a credible, productized cross-cloud Gold Tier story. If the client's data lives partly on S3, partly on Blob, partly on GCS, and the client wants one query surface that does not require copying any of it, BigQuery Omni is, today, the answer.

**KEVEN:** I concede the point. Honestly. The honest seller posture is — when the client's primary architectural constraint is *we have data in three clouds and we do not want to copy any of it into a fourth place to query it,* the right recommendation can be BigQuery Omni. Not Microsoft. Not Fabric.

**REID:** And the seller who can say that with conviction is the seller who wins the room. Because the client knows you know. And they will trust you on the next recommendation when Microsoft genuinely is the right answer.

**KEVEN:** The architectural honesty is the commercial leverage.

### AWS Athena Federated Query + Lake Formation — capable, more assembly

**REID:** Now AWS. The honest read here is — AWS can build the same Gold Tier the framework calls for. The integration is more assembly. The capabilities are real. The productization is denser on some pieces and thinner on others. Start with *Athena Federated Query.* The federation engine. The mechanic — Athena queries external sources through per-source connectors. There is a Snowflake connector. A MongoDB connector. A Postgres connector. MySQL. DynamoDB. CloudWatch. Redshift. Each connector is its own Lambda-backed service. Each connector has its own version. Each connector has its own security and identity configuration.

**KEVEN:** So the federation surface is real, but assembled per-source.

**REID:** Assembled per-source. The capability is there. The operational tax is real. When the client adds a new source — say, a new operational database — that is a new connector deployment. Each connector has its own lifecycle. Each connector has its own performance profile. Each connector has its own update cadence. Compared to Fabric Mirroring, which presents one unified mirroring surface productized by Microsoft, Athena Federated Query is more do-it-yourself. The access-control overlay is *AWS Lake Formation.* Row-level filters. Column-level masking. Cell-level controls. Tag-based access policies. Lake Formation is genuinely strong on fine-grained access — arguably the most granular productized access-control story across the three clouds at the data-lake layer. If the regulated requirement is *this analyst can see these rows but not those rows, and these columns are masked for that analyst,* Lake Formation handles it. And underneath, *AWS Glue Data Catalog* is the metadata layer. Tables, schemas, partitions, classifications. Glue is the schema-of-record for the AWS data lake pattern. Athena queries through Glue. Lake Formation policies apply against Glue-cataloged objects. The lake is held together by Glue. The table format — *Iceberg* is increasingly the answer on AWS. Iceberg tables on S3, cataloged in Glue, governed by Lake Formation, queried by Athena — that is the modern AWS lake-house pattern. Iceberg gives you schema evolution, time travel, partition evolution, and the open-format interoperability that the framework calls for. AWS has embraced Iceberg meaningfully — including managed Iceberg services and tight Glue integration.

**KEVEN:** Honest assessment.

**REID:** Honest assessment — AWS can build the Acceleration Framework's Gold Tier. The pieces are all there. Athena for query. Lake Formation for access control. Glue for the catalog. Iceberg for the table format. S3 for the substrate. The integration is multi-service assembly. The engineering scope is real. It is achievable. It is not as productized in one unified surface as Fabric is.

**KEVEN:** And from the seller's perspective.

**REID:** From the seller's perspective — if the client is AWS-primary and the engineering team has invested in the Glue plus Lake Formation plus Athena plus Iceberg pattern, do not try to displace it. Compose with it. Microsoft's Shortcuts can shortcut into the AWS lake. Foundry can talk to a Gold Tier composed on S3. The Microsoft value lands at the runtime and governance layers, not by ripping out a working AWS data foundation.

**KEVEN:** That is the right call.

**REID:** And the operational nuance — I have shipped this pattern. The connector versioning is the operational tax. Every new source connector is its own deployment, its own lifecycle, its own runbook. Fabric Mirroring abstracts that. Athena Federated Query exposes it. Neither is wrong. They are different productization choices.

### Per-entity joinability at Gold — the unlock

**KEVEN:** I want to slow down here, because this next piece is the unlock that makes the agent's reasoning actually work. And it is cloud-independent. It is the principle, not the product.

**REID:** Lay it out.

**KEVEN:** *Per-entity joinability at Gold.* The agent asks a question shaped like *what does the world look like for this entity right now?* For this customer. For this VIN. For this policyholder. For this product. For this account. And what comes back from Gold is a composed view — joined across every domain in Silver that touches that entity — at the entity grain.

**REID:** Walk what that means concretely.

**KEVEN:** Concretely — pick a customer. The agent's Gold view for that customer might compose — every transaction in the last twelve months from the operational ledger. Every service interaction from the contact-center system. Every product owned from the policy or account master. Every adjacent household member from the relationship graph. Every preference from the marketing profile. Every risk flag from the compliance system. Every regulatory disclosure from the legal record. All of those, joined together at the customer grain, served up as one composed substrate the agent can reason over.

**REID:** And without that, the agent has to stitch.

**KEVEN:** Without that, the agent has to make eight tool calls into eight different upstream systems and stitch the answer together at reasoning time. Which is brittle. The agent runs out of context. The latency stacks up. Each upstream system has its own failure mode. Each upstream system has its own access policy. The agent's audit trail becomes eight separate audit trails that have to be reconciled. With per-entity joinability at Gold, the agent makes one read against one composed view. The audit trail is single-source. The latency is bounded. The access policy is uniform. The agent reasons over one substrate, not eight fragments. The reasoning is dramatically more credible. And this is cloud-independent. The pattern works on Fabric — composing Gold tables over Silver, in Delta format, in OneLake. The pattern works on BigQuery — composing Gold views over Silver, with BigLake governance, queryable through Omni for cross-cloud sources. The pattern works on the AWS lake-house — composing Gold Iceberg tables over Silver, cataloged in Glue, governed by Lake Formation. The pattern is the principle. The product is the implementation.

**REID:** And this is one of the cleanest tests of whether a seller actually understands the framework. The seller who says *use Fabric* without naming per-entity joinability does not actually understand why Fabric helps. The seller who can name the per-entity joinability requirement first, and then walk through how Fabric expresses it, is the seller who can defend the recommendation on cross-examination.

**KEVEN:** Per-entity joinability at Gold. Independent of cloud. The discipline that makes agent reasoning credible.

### Vector store strategy across the three clouds

**KEVEN:** Now a related substrate. Vector stores. Because agentic AI is almost always paired with retrieval-augmented patterns, and retrieval patterns need an embedding store. Microsoft side first. *Azure AI Search* — formerly Cognitive Search — is the integrated vector and hybrid-search service. Native vector indexing. Hybrid retrieval that blends vector similarity with keyword and BM25 scoring. Productized as a managed service. The agent's RAG layer typically lands here in a Microsoft buildout. *Azure Cosmos DB for NoSQL* — vector indexing built in, useful when the application already lives in Cosmos. *Azure Database for PostgreSQL* — the pgvector extension, useful when the team is comfortable in Postgres and wants the operational simplicity of one database for relational and vector together. AWS side — *Amazon OpenSearch Service* — the AWS workhorse for vector and hybrid search. Mature. Productized. *Aurora PostgreSQL with pgvector* — same pattern as the Microsoft Postgres option, AWS flavor. *Bedrock Knowledge Bases* — the managed RAG abstraction. Bedrock takes care of chunking, embedding, indexing, retrieval. It hides the vector store underneath. Useful when the team wants to skip the plumbing. And GCP — *Vertex AI Vector Search* — Google's managed vector index. *AlloyDB for PostgreSQL with pgvector* — same pattern. *BigQuery vector* — vector indexing inside BigQuery itself, useful when the embeddings are produced as part of a broader BigQuery pipeline and the team wants one substrate.

**REID:** Let me add the operational view. Vector store choice is the *cheapest* architectural decision to migrate later. The index is rebuildable in hours. The embeddings, if you have kept the source documents, are regeneratable. Compare that to migrating a 50-terabyte data lake — that is a months-long project. The vector store can move over a weekend.

**KEVEN:** So you are saying — do not agonize over it early.

**REID:** Do not agonize over it early. Pick the one that fits the rest of the architecture, ship the agent, and revisit the vector store choice when you have actual cost and quality data from production. The vector store is not where the lock-in lives. The lock-in lives in the data foundation and the runtime and the governance substrate.

**KEVEN:** And the cost line — embedding costs are their own line item. We will go into the FinOps of that in episode six. For now — vector store is cheap to change, embedding compute can be expensive at scale, plan accordingly.

**REID:** Plan accordingly. And do not let a vector-store benchmark debate eat three weeks of your engagement calendar. It is not where the value lands.

### Streaming-source architecture — Kafka, EventHub, Kinesis, Pub/Sub

**KEVEN:** Let's talk streaming. Because real-time signals are increasingly the substrate the agent reasons over. And the no-replication principle applies here too — maybe more strictly than on the batch side. First, the sources. *Kafka* is the cloud-neutral open-standard. *Azure Event Hubs* is the Microsoft-side equivalent — Kafka-protocol-compatible. *AWS Kinesis* — Kinesis Data Streams and Kinesis Data Firehose. *Google Cloud Pub/Sub.* Different products, same architectural slot. Then the integration patterns — *Fabric Eventstreams* I mentioned earlier — pass-through from Kafka, Event Hub, IoT Hub into the OneLake side. The default is pass-through. Persistence is opt-in. *AWS Kinesis Data Firehose* can land streaming data into S3 as Bronze, into OpenSearch, into Redshift, into a generic HTTP endpoint — the integration is broad. *GCP Pub/Sub* can fan out to BigQuery directly, to Cloud Storage, or to Dataflow for transformation before landing. The no-replication discipline for streaming is — the stream stays live and authoritative. The source-of-truth is the stream itself, not a periodic snapshot of the stream. The agent's Gold Tier composition either reads the stream live, or — when regulatory requirements demand persistence for replay — persists into Bronze with explicit retention. Watermarking handles late-arrival events. The composition layer reconciles late-arrivals against the canonical entity view in Silver.

**REID:** And here is the operational truth that does not get said enough. Stream architecture decisions are *harder* to migrate than batch decisions. Once a stream is in production — once consumers depend on the topic, once the retention policy is set, once the partitioning is committed — changing the stream architecture is a real engineering project. Months of coordination. Compare that to batch — you can rerun a batch job. You cannot rerun a stream that has already passed by.

**KEVEN:** Get streaming right early.

**REID:** Get streaming right early. And if the architecture is genuinely undecided, pick the cloud-neutral substrate — Kafka — and use the cloud-specific products as the ingestion and consumption layer. The protocol portability is real. The product portability is more limited.

**KEVEN:** Cloud-neutral substrate, cloud-specific touch points. Reasonable default — not the only default, but the one that costs the least to change later.

### A reading I want to do

**KEVEN:** I want to read briefly — paraphrased — from the kind of register Gartner, Forrester, and IDC have been publishing through 2024 and 2025 on data-foundation patterns for agentic AI workloads. Specifically on federation versus replication trade-offs and the cost of repeated ETL.

**REID:** Go.

**KEVEN:** [reading, paraphrased from industry-analyst register on data fabric, data mesh, and federated-query market analyses — Forrester Wave on data fabric, Gartner analytic-platforms research, IDC data-integration market forecast]

*"The enterprise data integration market has, for the last decade, oscillated between two architectural commitments. The first — replicate the data into a central platform; trade governance complexity for query simplicity. The second — federate against the data in place; trade query overhead for governance simplicity and operational fidelity. The agentic AI workload has, for the first time, made the second commitment the architecturally correct one. The cost of replicated copies under agentic workloads compounds — through governance scope expansion, lineage decay, and audit-trail multiplication — at a rate that materially exceeds the cost savings from query pre-computation. Productized federation capabilities — managed mirroring, cross-cloud query federation, lakehouse shortcuts — have matured in the 2024 to 2026 window to a point where federation is now the recommended default for agentic data foundations in regulated and cross-cloud enterprises."*

[pause]

**REID:** *The recommended default.* That phrasing matters. Five years ago the industry was treating federation as a niche pattern for compliance-constrained or sovereignty-constrained cases. Today the analyst position is that federation is the default for agentic workloads.

The industry has been talking about data virtualization for fifteen years. Most of that conversation was aspirational. The products were thin. The governance was bolted on after. What is different now is productized mirroring with native governance integration. Fabric Mirroring with Purview lineage propagation is — today — the strongest example of that productization. BigQuery Omni is the strongest cross-cloud example of the same principle. The pattern has finally been productized to the point where the architectural recommendation can stop being aspirational.

**KEVEN:** Productized, governed, defendable. Three conditions that had to land for federation to become the default. All three landed in this window.

### One disagreement

**REID:** Pushback. And it is the one you knew was coming.

**KEVEN:** Go.

**REID:** *BigQuery Omni is the strongest cross-cloud federation story on the market today.* Period. Not *one of the strongest.* The strongest. If a client's data lives partly on S3 and partly on Azure Blob and they want one query surface that runs the compute in the source cloud — there is no productized equivalent on Microsoft. There is no productized equivalent on AWS. Fabric Mirroring does not cross clouds the way Omni does. Athena Federated Query has connectors but the compute does not run in the source cloud at the same level of maturity. If the client's primary architectural constraint is cross-cloud federation, the right answer is Google Cloud. Microsoft seller has to be able to say that.

**KEVEN:** I concede the cross-cloud axis. Stated cleanly — on the productized cross-cloud federated query specifically, with compute-in-the-source-cloud as the differentiator, BigQuery Omni leads. Microsoft does not have a like-for-like. AWS does not have a like-for-like. The honest call is to say that out loud.

**REID:** And then pivot, because there is a pivot.

**KEVEN:** Here is the pivot — and it is a legitimate pivot, not a deflection. The broader productization picture is wider than the cross-cloud axis. Fabric Mirroring plus Shortcuts plus Eventstreams plus Purview lineage integration is — today — the broadest productized expression of *don't replicate* across batch, streaming, and lakehouse, with native governance threading through all three. Cross-cloud federation is one axis. Multi-modality breadth is another. Lineage propagation through the governance substrate is a third. Microsoft leads on the breadth axes. Google leads on the cross-cloud axis. AWS is most assembly-required across all axes.

**REID:** So both can be true.

**KEVEN:** Both can be true. The seller's job is to be precise about which axis the client cares about. If the client's data is genuinely spread across three clouds and the architectural priority is one query surface that does not move bytes — recommend Google honestly. If the client's data lives mostly on Azure and a handful of Snowflake or S3 sources, with batch and streaming and lakehouse all in scope, and the governance integration is the priority — Microsoft leads. If the client is AWS-primary and the engineering team has the depth to compose Athena plus Lake Formation plus Glue plus Iceberg — compose with that and recommend Microsoft at the runtime and governance layers.

**REID:** That is the honest seller posture. Convergence.

**KEVEN:** Convergence. Both right on different axes. The discipline is naming the axis the client actually has.

**REID:** Sellers — write that one down. *Name the axis the client has.* Then choose the cloud that wins that axis. Do not lead with the cloud and try to bend the axis.

### What to carry forward

**KEVEN:** Three things.

**REID:** Go.

**KEVEN:** *One — the medallion: Bronze landing, **Silver canonical, Gold composed**. Silver is the canonical layer. Gold composes per-scenario for the agent's reasoning patterns. Get this rule right or every architecture conversation drifts. The warehouse is a sibling Gold Tier shaped for BI. The agent's Gold Tier is shaped for per-entity reasoning. Both children of Silver. Both legitimate.*

*Two — Principle four in action: virtualization, mirroring, shortcuts, federation. Sources stay untouched. Microsoft Fabric Mirroring plus Shortcuts plus Eventstreams with Purview lineage propagation is the broadest productized expression today. BigQuery Omni is the strongest cross-cloud federated query, period. AWS is most assembly-required — Athena Federated Query plus Lake Formation plus Glue plus Iceberg can build the same Gold Tier, more assembly involved.*

*Three — per-entity joinability at Gold is the unlock. The agent asks "what does the world look like for this entity?" and Gold returns the composed view. Independent of cloud. The pattern is the principle. The product is the implementation.*

**REID:** And the seller's posture from the disagreement — name the axis the client has. Cross-cloud federation as the priority means lead with Google honestly. Multi-modality breadth plus governance integration as the priority means Microsoft leads. AWS-primary engineering depth means compose with the AWS lake and bring Microsoft in at runtime and governance. Three different right answers depending on the axis. The architectural honesty is the commercial leverage.

**KEVEN:** Three different right answers. And the seller who can name them all is the seller the CIO trusts on the next question.

**REID:** Next episode — *Agent Runtime: Talking to Gold, Not SORs.* Foundry. Bedrock. Vertex AI. Model availability across providers. The MCP boundary discipline. Human-in-the-loop patterns. The runtime layer that sits on top of the Gold Tier we just built.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn
- **Microsoft Fabric** — overview, OneLake, and the unified workload model
- **Microsoft Fabric Mirroring** — managed mirroring for Snowflake, Databricks, Azure SQL, Cosmos DB, Azure PostgreSQL
- **Microsoft Fabric Shortcuts** — references to external data lakes (S3, ADLS, Dataverse) without copy
- **Microsoft Fabric Eventstreams** — streaming ingestion patterns into OneLake
- **OneLake** — unified data lake for Fabric
- **Microsoft Purview** — governance, lineage, and DSPM for AI
- **Azure AI Search** — integrated vector store with hybrid search
- **Azure Cosmos DB for NoSQL** — vector indexing patterns
- **Azure Database for PostgreSQL** — pgvector extension

### Google Cloud documentation
- **BigQuery Omni** — cross-cloud federated query with compute in the source cloud
- **BigLake** — unified access control across Cloud Storage and external object stores
- **Google Cloud Dataplex** — governance, lineage, classification, and data quality
- **Vertex AI Vector Search** — managed vector index
- **AlloyDB for PostgreSQL** — pgvector patterns
- **Cloud Pub/Sub** — streaming ingestion

### AWS documentation
- **Amazon Athena Federated Query** — per-source connector federation engine
- **AWS Lake Formation** — row-level, column-level, and cell-level access control
- **AWS Glue Data Catalog** — metadata layer for the lake-house
- **Apache Iceberg on AWS** — the modern table format for S3 lake-houses
- **Amazon OpenSearch Service** — vector and hybrid search
- **Amazon Aurora PostgreSQL** — pgvector
- **AWS Bedrock Knowledge Bases** — managed RAG abstraction
- **Amazon Kinesis Data Streams and Firehose** — streaming ingestion

### Data-engineering and analyst sources
- **Forrester** — data fabric and data mesh research; the Wave on enterprise data integration
- **Gartner** — analytic platforms and federated query market coverage
- **IDC** — data integration market forecast and federation-versus-replication analysis
- **The medallion architecture** — Bronze, Silver, Gold under modern data-engineering practice

### From the Acceleration Framework
- **Episode 1** — The Agentic Stack and the Five Principles
- **Trilogy Services Ep 3** — medallion architecture under the agentic stack
- **Trilogy Services Ep 4** — the MCP boundary at the agent runtime layer

---

**End of Episode 02 · Data Foundation and The No-Replication Principle**
*≈ 6,200 words · target 32 minutes at conversational pace*
