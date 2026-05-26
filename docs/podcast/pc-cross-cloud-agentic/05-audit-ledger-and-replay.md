# Episode 05 · Audit, Ledger, and Replay — The Trust Substrate

**Builds on:** Episodes 1-4 (principles, data, runtime, governance + identity + safety) · Trilogy — Services Ep 6 (audit and lineage patterns)
**Run time:** ≈ 32 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: an audit office. Early morning. The hum of a copier still warm. A printout the size of a phone book on the corner of the desk, spiral-bound, the spine creased where someone has thumbed it open and closed three or four times already. A reviewer in a navy jacket. Coffee that has gone cold without anyone noticing. Outside, a city waking up. Inside, very quiet.]

**KEVEN:** I want to start tonight in a room that is going to define how agentic AI gets accepted into regulated enterprises through the back half of the twenty-twenties. An audit office. Seven in the morning. An External Audit Reviewer — meaning a partner from the client's third-party audit firm, the firm that signs the financial-statement opinion — has come in early. On the desk in front of her, spiral-bound, is a printout the size of a phone book. The printout is not a financial reconciliation. The printout is the agent's overnight reasoning chain.

**REID:** The whole chain.

**KEVEN:** The whole chain. Every step. Every tool call. Every data access. Every retrieval. Every human-in-the-loop approval. Hash-chained — every row pointing to the prior row by cryptographic hash, every modification downstream visibly inconsistent. Replay-token validated — meaning the reviewer can take this chain back to her own laptop, on her firm's hardware, offline from the client, and re-run it. Same model version. Same seed. Same inputs. Same answer. She will do exactly that this morning. Not because anyone has alleged the agent did anything wrong. Because the audit firm's methodology now requires it.

**REID:** Because the audit firm has decided agentic AI is in scope.

**KEVEN:** Because the audit firm has decided agentic AI is in scope. The agent makes recommendations that flow into journal entries. The journal entries flow into the financials. The financials carry the audit opinion. The audit opinion requires that the firm can trace every material conclusion back to its source — and now, where an agent participated, the chain has to be reviewable and reproducible. The audit row is no longer a by-product of the agent running. The audit row *is the product.*

**REID:** Say that again. Slowly.

**KEVEN:** Said slowly. *The audit row is the product, not the by-product.* The recommendation is one column in the row. The reasoning that produced it is the rest of the row. The reviewer doesn't pay for the recommendation. The reviewer pays for the row. And the row has to be cryptographically tamper-evident, lineage-complete, identity-stamped, and replayable offline. That substrate is what lets agentic AI cross into the regulated enterprise without breaking the audit posture that the regulated enterprise is built on.

**REID:** That is the episode.

**KEVEN:** That is the episode. *Audit, Ledger, and Replay — The Trust Substrate.* The audit-row-per-step pattern. The hash-chained ledger pattern — lowercase, descriptive, not a brand. Replay-token validation. HITL gates as audit events. The lineage thread from audit row back to source identity. The productized shape on Microsoft via Foundry plus Purview, the engineered-assembly shape on AWS, the engineered-assembly shape on GCP. And the disagreement Reid is going to bring, which is whether the whole pattern is overengineered for most workloads. Let's go.

---

## The conversation

### Why agentic AI requires a different audit pattern

**KEVEN:** Let's start with the why. The agentic-audit conversation starts with a misconception most enterprise AI teams are still working through. The misconception is — *we already audit our AI. We audit the model. We audit the training data. We have a model risk management committee. We are good.* The shape of the misconception is that the agentic audit shape is the traditional ML audit shape with one more layer on top.

**REID:** It is not the same shape. Walk the inversion.

**KEVEN:** Walking it. In traditional ML, the model's prediction is the artifact you audit. You audit the pipeline — the model, the training data, the validation, the monitoring. The prediction itself is atomic. One number, one label, one ranking. The prediction doesn't carry the audit weight, because it is a deterministic output of an audited model on a logged input. Agentic is the inversion. The agent's decision is not atomic. It is the composite of dozens of intermediate decisions. The agent received the question. Decomposed it. Decided which tools to invoke. Interpreted what they returned. Decided whether the data was sufficient. Asked the human for approval at a gate. The human responded. The agent revised. Produced the final recommendation. *Every one of those decisions is a step.* The audit substrate has to capture the chain. The model is auditable in the traditional sense. *The chain that composes the steps into the final decision is the new substrate that has to be auditable.*

**REID:** And this is the part I want to push on, because it is what most enterprise AI teams have not internalized. They audit the model. They audit the data. They have model cards, they have data lineage, they have monitoring dashboards. They do not audit the reasoning. They cannot, today, tell you for a recommendation the agent produced last Tuesday what the agent reasoned through, in what order, with what intermediate evidence, with what human gates. The reasoning chain is the gap. Until that gap is filled by architectural commitment, agentic AI is not auditable in the regulatory sense. That is the agentic-AI audit problem.

**KEVEN:** Said exactly that way. The reasoning chain is the gap. The substrate that fills it is the episode. And the consequence of not filling it — you cannot defend the agent in front of a regulator. You cannot defend it in front of an external audit firm. You cannot defend it in litigation discovery. The model card is not enough. The data lineage is not enough. The monitoring dashboard is not enough. The reasoning chain is the artifact, and if it doesn't exist as a tamper-evident, replayable record, the recommendations are unprovable. *Unprovable* in the legal-evidentiary sense. CISOs and Chief AI Officers in regulated industries know this. General counsel knows this. Audit committees are starting to know this. Which is why the substrate is no longer optional.

### "Audit row, not log line" — the discipline

**REID:** The discipline. Name it.

**KEVEN:** *Audit row, not log line.* Said exactly that way. The line I want sellers to carry into client conversations and have land. *Audit row, not log line.* Because the difference is the entire substrate.

**REID:** Walk the difference.

**KEVEN:** A log line is what most production systems already emit. Free-form text, written by an engineer for a future engineer, optimized for human reading during debug. *Agent received request at fourteen-thirty-two; called retrieval tool; received seven documents; produced response.* Unstructured. The fields are whatever the engineer thought to log. The schema is whatever shape the print statement took. The integrity is — there is no integrity. The log file is mutable. The retention is ops-cost-driven. The log line is debug-oriented.

**REID:** And the audit row.

**KEVEN:** The opposite. Structured — a defined schema with required fields, validated on emission. Machine-readable, optimized for replay and review, not for grep. The fields are mandated by the audit substrate's contract — timestamp, agent identity, operator identity, task identifier, parent step, model version, tools invoked, data accessed, output, output hash, parent-row hash. The integrity is cryptographic. Retention is governance-driven. The audit row is audit-oriented. As a list. Audit row has a defined schema; log line is free-form. Audit row has required fields; log line has whatever fields the engineer logged. Audit row is machine-readable; log line is human-readable. Audit row carries cryptographic integrity; log line carries none. Audit row is retained per governance; log line is retained per ops cost. Audit row is reviewed by auditors; log line is reviewed by engineers.

**REID:** And the architectural consequence.

**KEVEN:** The substrate has to be enforced *at the architecture layer.* Not at the engineering layer. Not as a discipline that depends on every developer remembering to write structured rows instead of print statements. The agent runtime has to emit audit rows by construction — every model call, every tool invocation, every retrieval, every HITL gate produces a row through a mandated emission path, validated against the schema, hashed, chained, persisted. The developer cannot opt out. The discipline is architectural. And the seller's discipline is to put the line in the room. *Audit row, not log line.* When the client's AI team starts talking about *we'll log the agent's behaviour for traceability* — that is the log-line answer. That answer does not survive contact with the External Audit Reviewer from the cold open. Saying it that way distinguishes the two architectures in one sentence.

### The hash-chained audit row pattern

**REID:** Now the pattern. The ledger pattern. Walk the row's content, the chain construction, and why the chain matters.

**KEVEN:** Walking it. Every agent decision lands as a structured row. Ten fields, in the canonical formulation most enterprise implementations converge on. *One — decision context.* Timestamp, agent identifier, task identifier, parent step identifier. *Two — agent identity.* The principal the runtime authenticated as. Entra service principal on Microsoft. IAM role on AWS. Service account on GCP. *Three — operator identity.* The human on whose behalf the agent is acting, propagated through the on-behalf-of token chain, plus any HITL approver identities that have intersected the chain.

**REID:** Four through ten.

**KEVEN:** *Four — model version.* The exact version that produced the output — GPT-4o-2024-11-20, Claude Sonnet 4.5, Gemini 2.5 Pro. Critical for model-risk management; an upgrade is a traceable event. *Five — tool calls invoked.* Which tools, with which arguments, returning what. *Six — data accessed.* Which Gold-view rows the agent touched, with sensitivity classification, under what policy. The lineage hook. *Seven — output.* The agent's decision at this step. Intermediate conclusion or final recommendation. *Eight — output hash.* Cryptographic hash of the row's content. Any change to content changes the hash. *Nine — parent-row hash.* The hash of the immediately prior row in the chain. The chaining mechanism. Modify any prior row's content; its hash changes; the next row's parent-row-hash field no longer matches; the chain becomes inconsistent at every row downstream. Tamper-evidence is cryptographic, not policy-based. *Ten — replay token.* The deterministic seed and sampling-parameter context the model call used.

**REID:** And the chain construction.

**KEVEN:** Every row carries the hash of the prior row. The first row in a task — the genesis row — points to the prior task's terminal row, or to a configured chain anchor. Each row is appended as the agent reasons. Append-only by architectural enforcement, not by policy. You cannot rewrite a prior row. You can only append. Modify any prior row and the chain from that point forward becomes inconsistent; the inconsistency is detectable by any auditor running chain validation. And the naming — be careful. The pattern is colloquially called *the ledger pattern.* Lowercase. Descriptive. By analogy to a financial ledger that records every transaction immutably. *Ledger pattern* is the descriptive architectural term. Not a brand. When you see it written all-caps, that is an internal product brand that does not belong on tape. On tape, every time, *ledger pattern,* lowercase, generic. Same way *event sourcing* is a generic architectural pattern. The ledger pattern is the third in that family for agentic AI.

**REID:** Said cleanly.

### Replay-token validation — the offline replay

**REID:** Now the killer feature. The chain is one half. Replay is the other. Walk it.

**KEVEN:** The killer feature for audit, and the part that distinguishes the agentic ledger pattern from any prior audit substrate. *An External Audit Reviewer can take any agent decision, take the chain that produced it, and replay the reasoning offline. They get the same result.* Same model version. Same replay token. Same inputs. Same state. Same output. Reproducibility — close enough to bit-for-bit that divergence is auditable. Which is what makes regulatory audit of agentic AI defensible.

**REID:** Mechanics.

**KEVEN:** Four pieces. *The replay token* — deterministic seed plus sampling-parameter context: temperature, top-p, top-k. Captured in every row alongside the model version and the prompt. *The model version pin* — the row captures the exact version; the replay environment calls that version specifically. If deprecated, the substrate has retained access for the retention period — itself an architectural commitment. *The input pin* — prompt, retrieved context, prior-step output, all captured or referenced. Hashes for large inputs; full content for small. *The state pin* — what the agent had decided, what it remembered, what was in context.

**REID:** And the execution.

**KEVEN:** The reviewer takes the chain, picks a step, feeds captured inputs back into the same model version with the same replay token. Same output. The reviewer compares against the recorded output. They match. The chain is validated. If they don't match — model behaviour drift across an upgrade the substrate didn't track, or a bug in the replay environment — the auditor flags the divergence. And the cloud-versus-offline distinction is the audit-firm preference. The replay can run on the client's cloud or *offline* — on the auditor's firm hardware, with the model environment downloaded and replayed locally. Audit firms increasingly want offline replay — *because the cloud is the client's environment, and the auditor's methodology calls for independent reproduction.* If the auditor can only replay in the client's cloud, the client could in principle tamper with the replay environment. The audit profession is asking for offline-replay capability through twenty-six and twenty-seven.

**REID:** Let me push here. I want to be honest about what offline replay costs, architecturally, before any seller pitches this as a one-line feature.

**KEVEN:** Push.

**REID:** *Deterministic replay requires architectural discipline upstream.* It is not free. The agent has to be designed for determinism from the runtime up. Temperature configured deterministically. Top-p and top-k configured deterministically. Sampling seedable and the seed captured. Retrieval grounding deterministic — the index queried with a deterministic embedding model, returning deterministic ranking, against a content state captured at the row's timestamp. The decomposition logic deterministic given the same model version and seed. If any layer is non-deterministic — say the retrieval index has been re-indexed since the row was written — the replay diverges and the chain is no longer auditable in the strict sense. Building for replay is a design discipline that starts at the agent runtime and propagates through every tool. The retrofit is hard. Building it in from the foundation is the only way.

**KEVEN:** Conceded cleanly. Deterministic replay is an architectural commitment at the foundation. Temperature, top-p, sampling — configured for determinism. Retrieval grounding — deterministic, with index state captured. Decomposition — deterministic given model and seed. None of that is free. The seller has to be honest that the audit substrate is not a feature you turn on; it is an architectural posture the agent design has to support from the runtime up. *Replay is architecture, not feature.* Carry that forward.

### HITL gates as audit events

**KEVEN:** Now the human side. We walked HITL in Episode Three as the gate that catches irreversible actions. Here, the HITL gate is also an audit event. Every approve, every modify-and-approve, every reject — writes its own row into the chain. The human is not adjacent to the chain. The human is *in* the chain.

**REID:** Walk the fields.

**KEVEN:** The HITL row carries — *operator identity.* Which human approved, under what role and authority, captured from the on-behalf-of token. *What was presented to the operator.* The agent's recommendation at the gate. The reasoning chain to that point. What evidence the agent had, what tools it called, what intermediate conclusions, why it is asking for review at this specific gate. Captured because if a regulator later asks *did the operator have enough information to approve this responsibly,* the chain answers — here is exactly what they saw. *What was decided.* Approve, modify-and-approve, or reject. If modify, the modifications captured structurally. *Why.* The operator's note. Structured fields where applicable — risk acknowledgement, deviation rationale, override justification — and free-form notes. *Timestamp.*

**REID:** And the consequence for the chain.

**KEVEN:** The chain becomes a record of human-machine collaboration in full. The agent's reasoning, woven with the human's interventions. Agent decided this, asked for review here, human modified here, agent continued, reached the next gate, human approved here. The full collaboration is in the chain. The human's decisions are first-class audit events, not annotations on top. And the regulatory consequence — *human approval cannot be claimed without being chained.* A regulated workflow that requires human approval — financial filings, clinical recommendations, customer-facing communications, material business actions — cannot satisfy the requirement with a checkbox in a workflow tool not woven into the audit chain. The approval has to be in the chain, with the operator identity, what was presented, the decision, the rationale. The HITL gate is part of the audit substrate.

**REID:** Said cleanly.

### Identity propagation into the audit row

**KEVEN:** Connection back to Principle Three from Episode Four. Identity continuity. Every audit row carries identity. We walked four identities in the prior episode. Agent, operator, source, auditor. All four propagate into the row.

**REID:** Walk the propagation.

**KEVEN:** *Agent identity in the row* — the principal the runtime authenticated as. Entra service principal, IAM role, GCP service account. Captured by the emission path. *Operator identity in the row* — the human on whose behalf the agent is reasoning, propagated through the on-behalf-of token chain. If a HITL gate has intersected, the approvers are also captured. *Source identities in the row* — when the agent reached into source systems, the federated identities used are captured. Any tool call into SAP, Salesforce, Workday carries the federated principal, traceable back to the agent that initiated the federation. *Auditor identity in the row, when accessed for review* — the principal that read the row to inspect it. The chain captures who has looked at the chain. Meta-auditable.

**REID:** And the forensic property.

**KEVEN:** *Who did what when, with what data, under what authority* — answerable at every step. Every row. The agent did what — captured. On behalf of whom — captured. Against what source data — captured, with the federated identity that made the source-system call. With what authorization — captured, as the role and policy state at execution. Reviewed by whom — captured. And the contrast with the CISO from Episode Four — her audit row showed the service principal had accessed the customer-PII table but did not show the human who configured the principal, did not show who authorized the access, did not show whether data crossed any sensitivity boundary. That row was a log line dressed up as an audit row. It had agent identity. It did not have operator identity, source identity, authorization context, sensitivity classification. The chain was broken at every dimension she needed. The ledger pattern, properly implemented, captures all of those dimensions at every step. The CISO with the ledger pattern in place could answer her own question — *how does this not happen at scale* — without leaving her chair. The substrate prevents the gap by construction.

### The lineage thread — audit row to source

**KEVEN:** From audit row back to source. The row says *the agent accessed Gold view X at row hash Y.* That is one end of the thread.

**REID:** Walk it.

**KEVEN:** *Audit row to Gold view.* The data-accessed field points to a Gold view — the per-scenario business model the agent queried. *Gold view to Silver canonical.* The catalog lineage from Episode Two points to the Silver canonical models that compose the Gold view. *Silver to Bronze reference.* Silver's lineage points to Bronze reference data — the landings of the source-system data, via mirroring, federation, or replication. *Bronze to source system.* Bronze's lineage points to the source system, with the federated source identity that pulled it.

**REID:** And the property.

**KEVEN:** *Full provenance, every step.* From the agent's recommendation at the top of the chain, drill down through the row, into the Gold view, through Silver, into Bronze, back to the source system, with the federated identity at every hop. The auditor can answer — *what data did the agent rely on, where did it come from, who authorized it to be there.* And the failure mode is *lineage that breaks at any step breaks the audit posture.* The substrate is only as defensible as its weakest lineage hop. Which is why the discipline from Episode Two — Purview-style propagated lineage, end to end — is not adjacent. It is the substrate that holds the audit chain together at the data layer. The data foundation is half of the audit substrate. The agent runtime emission is the other half. They compose. Neither carries the substrate alone.

**REID:** Said cleanly.

### The ledger pattern productized vs assembled

**REID:** Three clouds. How each supports the pattern. Walk Microsoft.

**KEVEN:** The honest claim. *On Microsoft, the ledger pattern is productized as reference architecture.* Not a single SKU. A documented reference pattern with productized building blocks named and integration documented. *Foundry Agent Service emits structured audit events natively.* Every model call, every tool invocation, every retrieval, every HITL gate — the runtime emits with canonical fields filled out by the runtime itself. The developer does not write the emission code. The runtime does.

**REID:** And the receiver.

**KEVEN:** *Microsoft Purview audit echo* — the Purview audit substrate that catches the Foundry emissions. The hash-chain pattern is documented as reference architecture on top of the Purview audit substrate. Microsoft has published the integration with sample implementations. The hash chain is implemented in the storage layer Purview emits into, with parent-row hashing at emission time. Replay-token validation on Foundry — model versions pinned, seeds captured, inputs referenced, replay environment documented. *The "this is how we build it" guidance is Microsoft-published.* And the honest claim about productization level — *it is reference architecture, not a single-SKU productized feature.* The integration is documented but the client's platform team still assembles. Foundry plus Purview plus storage plus replay environment. The reference compresses the integration scope. It does not eliminate it.

**REID:** And AWS.

**KEVEN:** AWS. Honestly. *Capable but the build is custom.* The capabilities are mature. The assembly is engineering. *Bedrock emits invocation events to CloudTrail and CloudWatch.* Every model invocation, every tool call through Bedrock Agents, every retrieval — events in CloudTrail as API audit records and CloudWatch as application logs. Mature substrate. Audit-firm-credible at the emission layer.

**REID:** And the hash chain.

**KEVEN:** Custom storage on top. Three honest options. *DynamoDB tables with hash-link columns.* Audit rows in a DynamoDB table designed for the audit shape, with a hash column and a parent-row-hash column, append-only by access control. Several enterprise implementations have done it. *Amazon QLDB.* I want to be honest. *QLDB is in maintenance mode as of twenty-twenty-four. Amazon has indicated it is not the future-path service for new workloads.* Existing QLDB workloads continue to run. New workloads building on QLDB today should be aware of the support trajectory. While QLDB's append-only ledger primitive is structurally well-suited to the audit-row pattern, recommending it as the substrate for a new agentic-audit build in twenty-twenty-six is not the right call. *OpenSearch with append-only discipline.* OpenSearch as the audit-row store, with write-once indexes and access policies enforcing immutability. The platform team builds it. And replay validation is custom on AWS. Store seed and input references in the row. Re-run on Bedrock with the captured seed against the pinned model version. Engineering work, not a productized button. Offline replay — pulling the chain to the auditor's environment and re-running on AWS-equivalent infrastructure — involves offline access to model checkpoints, which Bedrock supports for some models but not all. *The honest summary on AWS — capable, mature emission, custom hash-chain storage, custom replay, the QLDB maintenance-mode caveat. Engineering work — six to twelve weeks in a Wave One by a competent platform team — is real but achievable.*

**REID:** And GCP.

**KEVEN:** GCP. *Vertex AI Agent Engine emits events to Cloud Audit Logs and Cloud Logging.* Every agent invocation, every model call, every tool call. *Cloud Audit Logs are tamper-evident by default.* The GCP differentiator worth naming honestly. Write-once-immutable as a platform property. The underlying substrate has integrity built in at the platform layer. The hash chain on top still has to be assembled, but the substrate beneath it is tamper-evident before the chain is built. A real architectural advantage.

**REID:** And the hash chain on GCP.

**KEVEN:** Two patterns. *BigQuery append-only tables with content-hash columns.* Rows land in a BigQuery table designed for the audit shape, with hash columns. Append-only enforced by IAM and column-level controls. BigQuery is a strong substrate — analytics for the chain comes for free, audit queries run efficiently. *Cloud Storage with object retention locks.* For larger payloads — model checkpoints, large input snapshots, replay-environment images — retention locks and object versioning give the immutability guarantees the audit firm wants. Replay validation on GCP is custom, same shape as AWS. Store seed in BigQuery alongside the row. Re-run on Vertex with the captured seed. Same six-to-twelve-week range in a Wave One.

**REID:** Let me push here. The cross-cloud honesty matters. *AWS and GCP can both build the ledger pattern. The engineering scope on either is six to twelve weeks in a Wave One if done by a competent platform team. Microsoft's productized reference compresses some of that scope but not all of it.* The seller's claim should be — Microsoft has documented the integration; AWS and GCP have not, but have the capable building blocks. Whether documentation-versus-build matters depends on the client's Wave One timeline pressure, the platform-team experience, and the appetite for build-versus-reference. In some engagements the documented reference is worth real money. In others, the platform team would build it the way they want anyway.

**KEVEN:** Conceded cleanly. *The productization-versus-assembly gap on the ledger pattern is narrower than on DSPM for AI from Episode Four.* On DSPM for AI, Microsoft has a productized SKU and the others do not. On the ledger pattern, Microsoft has documented reference architecture; the others have capable building blocks. The seller should be precise about which comparison is in front of them.

### Why this matters — regulated industries and board-level governance

**KEVEN:** Why this matters for the seller carrying it into regulated-industry conversations. Five reasons.

**REID:** Walk them.

**KEVEN:** *Regulated industries.* Health and life sciences, financial services, regulated manufacturing, energy and utilities, public sector. The audit chain is a regulatory requirement, not a nice-to-have. The regulator does not accept *the agent recommended this and the model card is available* as evidence. The regulator expects the reasoning chain, the lineage thread, the identity propagation, the replay capability. *EU AI Act high-risk obligations.* From Episode Four. Article-level obligations on traceability, on logging, on documentation. The ledger pattern is the architectural substrate that satisfies those obligations. *NIST AI RMF Measure and Manage functions.* The Measure function requires evidence of how the system performs in production. The Manage function requires incident-response capability. Both require the substrate.

**REID:** Four and five.

**KEVEN:** *Board-level AI governance.* The audit committee, the risk committee, increasingly the full board want the answer to one question. *If something goes wrong, can we trace it?* The ledger pattern is the answer. *The External Audit Reviewer pattern from the cold open.* The third-party audit firm's offline-replay capability. Emerging through twenty-five and twenty-six. Expect standardization across twenty-six through twenty-eight as the major firms publish methodologies. The architecture has to support it now, because retrofitting after the firm starts asking is brutal.

**REID:** And the seller posture.

**KEVEN:** *If you sell agentic AI without an audit chain, you sell against a CISO and a Chief AI Officer who will correctly ask, how do I prove this is doing what it is supposed to be doing.* The ledger pattern is the answer. The seller who has not internalized it loses the room when the question is asked. And the question is being asked, increasingly, in twenty-twenty-six.

### Operational observability — alongside compliance audit

**REID:** The dual purpose. Walk it.

**KEVEN:** The substrate is not only for compliance. It also enables operational observability. Same rows. Different consumer. Different queries. *One substrate, multiple consumers.*

**REID:** Walk the operational use cases.

**KEVEN:** *Prompt failure rates by use case.* Which scenarios is the agent getting stuck on. Which prompts are bouncing through more retries than expected. *Tool-call latency distribution.* Which tools are slow, which are degrading, which are hitting fan-out limits. *Model-version drift detection.* When an upgrade happens, how is the behaviour distribution shifting — same prompts, different outputs at materially different rates. *Source-schema-drift surfacing.* When a source's data shape changes and the lineage propagates the change, where in the agent's reasoning is the change showing up. *Cost anomalies per agent.* Which agents are consuming more tokens than their workload calls for. Which is the lead-in to Episode Six on FinOps.

**REID:** And the substrate property.

**KEVEN:** *One substrate, two query patterns.* Compliance team queries one way — *show me every action this agent took on this customer's data over this date range, with the operator who authorized each step.* SRE team queries another way — *show me the latency distribution of the retrieval tool over the past twenty-four hours, broken out by Gold view.* Same rows. Different filters. Different aggregations. Different dashboards. Both queries valid. Both served by the same substrate. Build the substrate once. Instrument once. Compliance gets their views; SRE gets theirs; FinOps gets theirs; security gets theirs. *Build the substrate at the foundation; specialize the views.* Compliance is one consumer of a universal observability layer.

### A reading I want to do

**KEVEN:** I want to read briefly — paraphrased — from a composite of what Microsoft Learn publishes on Foundry audit, what NIST publishes on the AI RMF Measure function, and what the EU AI Act traceability obligations register requires. The shape of the published guidance is converging through twenty-twenty-five and twenty-twenty-six.

**REID:** Go.

**KEVEN:** [reading, paraphrased — composite of Microsoft Learn Foundry audit guidance, NIST AI RMF Measure function publications, and the EU AI Act high-risk traceability register]

*"The defensibility of an agentic AI system in front of a regulator, an external auditor, or a court of competent jurisdiction rests on the system's ability to reproduce the reasoning that produced any given decision. The model is auditable; the data is auditable; the predictions are auditable; but in a system where the recommendation is the composite of dozens of intermediate decisions, the audit substrate must capture the composition. The chain of reasoning, persisted with cryptographic integrity, reviewed by a principal whose identity is captured in the chain, replayable offline under the same model version and the same seed, is the substrate that distinguishes agentic AI that can be defended in a regulated environment from agentic AI that cannot. Organizations that treat this substrate as an architectural commitment — built at the runtime layer, propagated through the data layer, integrated with the identity layer — produce systems that survive contact with the audit profession. Organizations that treat it as a logging concern produce systems that do not."*

[pause]

**REID:** *The audit chain is the differentiator between agentic AI you can defend in front of a regulator and agentic AI you cannot.* That is the line. CISOs and Chief AI Officers in regulated industries know it. The architecture either has the substrate or it does not. The seller who walks into a regulated-industry conversation in twenty-twenty-six without being able to name the audit row, the hash chain, the replay capability, the lineage thread, and the identity propagation loses the room to whoever can.

**KEVEN:** Said exactly that way.

### One disagreement

**REID:** Pushback. The structural one. Because I think the architect can overplay the substrate, and the overplaying has costs.

**KEVEN:** Go.

**REID:** *The ledger pattern is overengineered for most enterprise AI workloads.* Said plainly. Measure the typical enterprise's agentic pilot portfolio — the substantial majority, call it eighty percent, are internal-use agents handling non-regulated data. The sales-productivity agent. The internal IT helpdesk agent. The marketing-content drafting agent. The internal analytics agent on non-regulated data. They do not need cryptographic hash chains. They do not need replay-token validation. They do not need offline-replay-capable substrates. Building the full ledger pattern around every internal pilot is a tax on the wrong workloads. The architectural commitment costs real engineering hours and runtime overhead. Paying it where the audit chain is not the requirement is effort going to the wrong place.

**KEVEN:** Conceded partially. The partial concession is the structural pivot the seller has to be precise about.

**REID:** Walk the pivot.

**KEVEN:** *The eighty percent of internal-use agents on non-regulated data can run with simpler observability.* Structured logging, basic identity capture, basic lineage to source — sufficient. Without the cryptographic hash chain. Without deterministic replay tokens. Without offline-replay capability. The cost of the full substrate on those workloads is not justified by the audit posture those workloads need.

**REID:** And the twenty percent.

**KEVEN:** *The twenty percent of workloads that touch regulated data, customer-facing decisions, board-visible recommendations, or material-financial-impact outputs require the full pattern.* Those are the workloads where the External Audit Reviewer from the cold open asks for the chain. The EU AI Act high-risk obligations attach. The regulator's scrutiny lands. And the seller's mistake is *starting without the substrate and trying to add it later.* The retrofit is brutal. The runtime has to be re-engineered for deterministic emission. The data foundation re-engineered for propagated lineage. The identity layer re-engineered for through-the-chain propagation. Months of work, with foundational decisions made wrong that cannot be unwound without going back to the foundation. The right move is *substrate at the foundation; enforcement intensity per-workload.* Build the substrate at the architecture layer — runtime emits structured rows, data layer propagates lineage, identity layer propagates through the chain. Non-negotiable at the foundation. Then *decide per-workload how much of the chain to enforce.* For the internal sales-productivity agent — emit rows, capture identity, capture lineage, but do not require offline-replay-capable model checkpoints. For the regulated workflow that feeds journal entries — emit rows, capture identity, capture lineage, hash-chain the rows, replay-token-validate the steps, support offline replay. *Same substrate. Different enforcement intensity. Per-workload.*

**REID:** And the convergence.

**KEVEN:** *The discipline lives at the architecture layer, not the workload layer.* Substrate is built once, at the foundation. Intensity is tuned per-workload. The internal pilot does not pay the full cost of the regulated workflow. But the regulated workflow does not pay the cost of being retrofitted onto a substrate not built for it. Both extremes wrong. The right answer is substrate at the foundation, intensity per-workload. *Architecture layer holds the discipline; workload layer tunes the intensity.*

**REID:** Convergence. Named cleanly.

**KEVEN:** Named cleanly. The eighty-twenty split is real. The architectural commitment is structural. The enforcement intensity is operational. The substrate has to be at the foundation. The intensity is decided per-workload.

### What to carry forward

**KEVEN:** Three things.

**REID:** Go.

**KEVEN:** *One — agentic AI requires a different audit pattern than traditional ML. The reasoning chain is the artifact, not the prediction. The substrate has to capture every model call, every tool invocation, every data access, every HITL approval as a structured audit row, not a free-form log line. Audit row, not log line. The discipline that distinguishes defensible agentic AI from unprovable agentic AI. Hash-chained for tamper-evidence. Replay-token validated for reproducibility. Identity-propagated for forensic traceability. Lineage-threaded back to source for provenance.*

*Two — the ledger pattern is productized as reference architecture on Microsoft via Foundry Agent Service plus Purview audit echo. AWS and GCP can build the equivalent. Bedrock and Vertex AI emit credible audit events into mature substrates. The hash chain is built on DynamoDB or OpenSearch on AWS, or BigQuery and Cloud Storage on GCP. QLDB on AWS is in maintenance mode and is not the future-path service for new builds. Cloud Audit Logs on GCP are tamper-evident at the platform layer — a real advantage. The engineering scope to build on AWS or GCP is six to twelve weeks in a Wave One. The productization-versus-assembly gap on the ledger pattern is narrower than on DSPM for AI.*

*Three — the substrate enables both compliance audit and operational observability. One substrate, multiple consumers. Compliance team queries one way; SRE team another; FinOps a third; security a fourth. Build the substrate at the foundation; specialize the views. And the enforcement intensity is tuned per-workload. The eighty percent of internal-use non-regulated workloads can run with lighter intensity. The twenty percent of regulated, customer-facing, board-visible, material-financial-impact workloads require the full pattern. Substrate at the foundation; intensity per-workload. Architecture layer holds the discipline; workload layer tunes the intensity.*

**REID:** And the seller's posture from the disagreement — substrate at the foundation is non-negotiable; enforcement intensity per-workload is the structural conversation with the client. Be precise. Do not pitch full-ledger-everywhere as the universal answer. Do not pitch no-ledger-anywhere as the cost-efficient answer. Pitch the substrate as the foundation and the intensity as the per-workload decision. Architecturally honest. Commercially defensible.

**KEVEN:** Architecturally honest, commercially defensible. The substrate is the foundation. The intensity is the per-workload decision.

**REID:** Next episode — *FinOps for Agentic AI.* The plus-twenty-to-forty-percent quarter-over-quarter AI consumption growth the analysts are citing. Tokens. Copilot seats. Agent runtime compute. Vector store storage. Audit-ledger storage — yes, the substrate from this episode costs real money to retain. Federation-query compute. Model-mix optimization across GPT, Claude, Gemini, Llama, smaller open-weights. The CFO conversation that is starting to land in every enterprise with more than three agentic workloads in production.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn
- **Azure AI Foundry Agent Service** — audit event emission and structured-row patterns
- **Microsoft Purview** — audit catalog, lineage, and identity propagation
- **Microsoft Purview DSPM for AI** — AI-aware data security posture management
- **Microsoft Entra ID** — service-principal and on-behalf-of identity propagation into audit rows

### AWS documentation
- **AWS CloudTrail** — API audit logging substrate for Bedrock and adjacent services
- **Amazon CloudWatch Logs** — application logging and event analytics
- **Amazon Bedrock** — model invocation audit emission patterns
- **Amazon DynamoDB** — append-only audit-row table patterns with hash-link columns
- **Amazon QLDB** — note: in maintenance mode as of 2024; existing workloads supported; new builds should evaluate DynamoDB or OpenSearch alternatives
- **Amazon OpenSearch Service** — log analytics and audit-row indexing
- **AWS Audit Manager** — compliance-evidence collection

### Google Cloud documentation
- **Cloud Audit Logs** — admin, data access, system event, and policy-denied logs; tamper-evident at the platform layer
- **Cloud Logging** — application logging substrate
- **Vertex AI Agent Engine** — agent runtime audit emission
- **BigQuery** — append-only audit-row tables with content-hash columns; analytics-ready audit substrate
- **Cloud Storage** — immutable storage with object retention locks for chain payloads and replay-environment artifacts

### Standards
- **NIST AI Risk Management Framework** — Measure and Manage functions; evidence and incident-response substrate
- **EU AI Act** — traceability and logging obligations for high-risk AI systems
- **ISO/IEC 42001** — AI management systems standard; audit certifiability

### Industry research
- **Gartner** — AI audit and trust market analyses
- **Forrester** — AI risk management research
- **IDC** — enterprise AI governance and assurance research

### From the Acceleration Framework
- **Episode 1** — Five Principles
- **Episode 2** — Data Foundation; Bronze-Silver-Gold lineage propagation
- **Episode 3** — Agent Runtime; HITL gate design
- **Episode 4** — Governance, Identity, Safety; Principle Two governance side and Principle Three identity continuity
- **Episode 6** (next) — FinOps for Agentic AI

---

**End of Episode 05 · Audit, Ledger, and Replay — The Trust Substrate**
*≈ 6,200 words · target 32 minutes at conversational pace*
