# Episode 01 · The Agentic Stack and The Five Principles

**Builds on:** Trilogy — Sellers Ep 2 (the Commercial Arc / Independence) · Sellers Ep 4 (TMT-MED + Automotive Practice contexts) · Services Ep 4 (the MCP boundary)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: an architecture review room ambient. The hum of a projector fan. A whiteboard half-covered in arrows. End of a Friday — the kind of late afternoon where the natural light is going amber through the glass and somebody's coffee has gone cold on the table.]

**KEVEN:** I want to start with a question that landed in my inbox at four-fifteen on a Tuesday. A Microsoft seller — good seller, fifteen years on the platform, knows Foundry, knows Fabric, knows Purview — forwards me a note from a prospective client. The note is one line. *Can you build an agent on top of our Snowflake data warehouse?*

[pause]

And the seller writes underneath — *Keven, what do I tell them?*

**REID:** And what did you tell him?

**KEVEN:** I told him — *I can. But you'll wish I hadn't.*

**REID:** That's the right answer. And it's also the answer that ends the easy version of the conversation, because now you have to defend it.

**KEVEN:** That's exactly the point. The seller can either take the question at face value — *yes, of course, we'll point Foundry at the warehouse, here's our SOW* — or the seller can stop, slow down, and say *let me tell you why that question is actually three different questions, and why getting the architecture wrong on the first one makes the second two unsolvable.* That second move is the move this whole podcast is about.

**REID:** And it's the move that's hard to make if you've never built the wrong-way version and watched it fail. I have. On Bedrock, on Vertex AI, and on Azure. The wrong-way version looks great in the demo and falls apart at the audit.

**KEVEN:** Welcome to the Cross-Cloud Agentic Podcast. Eight episodes. I'm Keven Markham. Twenty-two years on the Microsoft platform. I sell, I architect, and I live in the gap between what a Microsoft seller is comfortable saying and what a cross-cloud CIO actually needs to hear.

**REID:** I'm Reid. Senior principal architect. I've shipped production agentic workloads on Microsoft Azure, on AWS Bedrock, and on Google Cloud Vertex AI. I'm here as the cross-cloud honesty enforcer. When Keven overclaims for Microsoft, I push back. When the honest answer is *lead with someone else and let Microsoft compose*, I say so. The disagreement is real, never performative.

**KEVEN:** This podcast is for the Microsoft Target Platform Seller two weeks from a cross-cloud CIO conversation. The CIO has Azure. They also have AWS. They have a Vertex AI proof-of-concept. They've heard every pitch. They want to know — at architectural depth — *where Microsoft is genuinely the right answer, where it's a tie, and where the honest recommendation is to lead with someone else.*

**REID:** That's the only conversation a serious CIO respects.

**KEVEN:** Episode One. *The Agentic Stack and the Five Principles.* Let's go.

---

## The conversation

### Why "agentic" needs a definition before we start

**KEVEN:** Before we name a single architectural principle, we have to do the boring work. We have to define the word *agent*. Because the word is everywhere right now, and most of what it's attached to is not what we mean.

**REID:** Let me push back before you've even started. I want to push back on the term itself. *Agent* has been overloaded to the point of uselessness. I've sat in meetings where someone called a stored procedure an agent. I've seen vendor decks where a scheduled ETL pipeline gets relabeled as an agent because the marketing team needed a word that wasn't *workflow*. If we don't define this tightly, the rest of the series collapses into mush.

**KEVEN:** Agreed. And the definition I use — and that this series uses — is a four-criterion test. Reasoning. Tool use. State. And an audit substrate. All four. Miss one, and what you have is something else — useful, maybe, but not an agent.

**REID:** Walk those.

**KEVEN:** *Reasoning.* The thing has to make a decision that isn't pre-coded. A model in the loop, choosing between branches based on context — not a switch statement, not a flowchart. *Tool use.* It has to call something — a function, an API, a query — to do work in the world. Read-only counts. Write counts. But it must reach out beyond its own context. *State.* It has to carry something forward across a multi-step interaction. Memory of what it's already tried, what the operator approved, what the source system returned. Without state you have a stateless prompt — useful, but not an agent. *And an audit substrate.* Every reasoning step, every tool call, every state mutation produces an evidence row that an auditor can replay. Without the audit substrate, you have something a regulated enterprise cannot adopt in a real decision flow.

**REID:** And the audit substrate is the one most people skip when they call something an agent.

**KEVEN:** It is the one most people skip. Because it's the hardest one to build. And it's the one that — when you skip it — turns your demo into a liability the moment a real auditor asks how the agent reached its conclusion.

**REID:** So a pipeline can be useful. A scheduled job can be useful. A retrieval-augmented chat interface can be useful. But none of those, on their own, clear the bar.

**KEVEN:** None of those clear the bar. And this matters for the seller because the conversation with a CIO is going to land on one specific question — *which of the things we already have are agents, and which are just pipelines wearing a costume?* The seller who can answer that question crisply, with the four-criterion test, has earned the next thirty minutes of the meeting.

**REID:** And the seller who can't gets shown the door at the twenty-minute mark.

**KEVEN:** That's the operating vocabulary. Reasoning, tool use, state, audit substrate. Four criteria. We'll use it every episode.

### The four-layer agentic stack — plus identity as a fifth cross-cutting concern

**KEVEN:** Now the stack. Because once you have the definition, the next question is — *what does it actually sit on?* And the answer is four layers, plus a fifth concern that cuts across all four.

**REID:** Lay them out.

**KEVEN:** Layer one — the data foundation. This is where the Gold Tier lives. The purpose-built, reasoning-shaped data substrate that the agent talks to. Not the raw systems of record. Not the data warehouse. A separate tier composed from those sources and shaped for the way an agent actually reads data.

**REID:** And on Microsoft this is Fabric and OneLake. On AWS this is Lake Formation over S3 with Glue catalog. On GCP this is Dataplex and BigQuery. All three clouds have a credible Gold Tier story. The differences are at the productized-capability level, not at the architectural level.

**KEVEN:** Layer two — the agent runtime. Where the agent actually executes. The orchestration layer. The thing that holds the reasoning loop, manages tool invocations, persists state, and emits audit events. On Microsoft this is Foundry — Azure AI Foundry — plus the Agent Framework SDK. On AWS this is Bedrock Agents. On GCP this is Vertex AI Agent Builder.

**REID:** Three credible runtimes. Different maturity profiles. Different productized features. And I'll come back to that.

**KEVEN:** Layer three — the control plane. Governance, audit, the ledger pattern. The substrate that makes the agent's behaviour observable, auditable, and replayable. On Microsoft this is Purview, including DSPM for AI. On AWS this is Lake Formation policy plus Macie plus the audit and observability stack. On GCP this is Dataplex plus the broader GCP audit and IAM machinery.

**REID:** And this is where the productized-capability gap is widest right now — and where Microsoft is genuinely differentiated. I'll defend that.

**KEVEN:** We will. Layer four — model serving. Where the actual models run. On all three clouds this is increasingly the NVIDIA stack underneath — Triton, NIM, Tensor RT — composed with cloud-native model endpoints. The NVIDIA composability is platform-neutral. All three hyperscalers run it.

**REID:** That's an important point and we'll come back to it. NVIDIA is not a Microsoft-only conversation. NVIDIA is the substrate under all three.

**KEVEN:** And then the fifth concern. Identity. Identity does not sit on a layer. Identity cuts across every layer. Agent identity, operator identity, source-system identity, auditor identity — all distinct, all interlinked, no translation gaps. On Microsoft this is Entra. On AWS this is IAM with IAM Identity Center. On GCP this is Cloud IAM with Workload Identity Federation. All three are mature. All three are non-trivial to compose when the workload spans clouds.

**REID:** And the identity-translation problem is where I've seen the most painful production failures. Not because any one cloud's identity service is weak — they're all good. The pain is at the seams. Agent on Azure reading data from an S3 bucket via a federated identity. Auditor on GCP needing to verify an action taken by an agent on Bedrock. Every seam is a place where the translation can drop a claim, or duplicate it, or attribute it to the wrong principal.

**KEVEN:** And every dropped claim is an audit gap. Every duplicate is a security gap.

**REID:** That's the substrate. Four layers — data, runtime, control plane, model serving — plus identity threading through all four.

**KEVEN:** The stack. And now the principles.

### The Five Architectural Principles — named explicitly

**KEVEN:** Five principles. These are the architectural commitments the framework — *the Acceleration Framework* — rests on. They're vendor-neutral by design. They work on Microsoft. They work on AWS. They work on GCP. The differences across clouds are at the *productized-capability density* level — how much of each principle a given cloud has already productized versus how much the seller and the systems integrator have to assemble. But the principles themselves don't change.

**REID:** And that's the part most sellers miss. The principles are not a Microsoft thing. The architectural commitments are real on any cloud. What Microsoft brings is — in many cases — a denser productized expression of those commitments. But the principle comes first. The cloud comes after.

**KEVEN:** Principle one. *Gold-Tier-First.*

**REID:** State it cleanly.

**KEVEN:** Agents talk to a purpose-built Gold Tier composed from systems of record and data warehouses. Agents never talk *directly* to systems of record or data warehouses. The Gold Tier is shaped for reasoning. The systems of record are shaped for transactions. The data warehouse is shaped for BI. You don't point an agent at any of those raw substrates. You compose a Gold Tier from them and you point the agent at the Gold Tier.

**REID:** And the reasons matter. First — brittleness. A system of record has schema drift, rate limits, primary-key churn. Point an agent at it directly and every minor schema change becomes an agent regression. Second — governance scope. Every system of record has its own audit model, its own access pattern, its own privacy boundary. The Gold Tier collapses those into one governance scope you can actually reason about. Third — audit complexity. When the agent calls eighteen different source systems directly, every audit row has to translate across eighteen different audit models. When the agent calls one Gold Tier, the audit model is uniform.

**KEVEN:** Episodes two and three go deep on this. Episode two on the no-replication mechanics of composing the Gold Tier without copying source data. Episode three on what the agent runtime actually does on top of Gold.

**REID:** Principle two. Walk it.

**KEVEN:** *Governance, audit, and the ledger pattern as the trust substrate.* Three pieces. DSPM-for-AI policy. Hash-chained audit-row-per-step. And replay-token validation. Said together because they only work together. *DSPM for AI* is data security posture management oriented to AI workloads — the policy layer that says this data class can be reasoned over by this agent, in this context, for this purpose, with these guardrails. *Hash-chained audit-row-per-step* — every reasoning step, every tool call, every state mutation produces an audit row. Each row carries the cryptographic hash of the previous row. The chain can be verified end-to-end. You can't silently edit a row in the middle. *Replay-token validation* — you can take any agent decision, re-run the agent against the original inputs with the original state, and prove the agent would produce the same answer. The replay is reproducible.

**REID:** And the *why* matters. Regulated industries require this. The EU AI Act in force in 2025. The NIST AI Risk Management Framework. ISO 42001 for AI management systems. Board-level AI governance committees demand it. You cannot put an agent into a real decision flow at a regulated enterprise — banking, healthcare, automotive recall, regulated media — without this substrate. Without it, the agent is a demo. With it, the agent is a system of record.

**KEVEN:** Episodes four and five go deep on it. Episode four on the governance, identity, and safety layer. Episode five on the audit ledger and replay mechanics.

**REID:** Principle three. Identity Continuity.

**KEVEN:** The agent has an identity. The operator who invoked the agent has an identity. The source systems the agent read from have identities. The auditor reviewing the trail has an identity. All four are distinct. All four are interlinked in the audit substrate. No translation gaps. No silent re-attribution.

**REID:** And the reason — identity translation gaps *are* audit gaps. They're also security gaps. Every place where the system has to translate *this human in Entra* into *this service principal in IAM* into *this row-level policy in BigQuery* is a place where a claim can be lost. When the auditor asks *who did this*, the answer has to chain end-to-end. If it can't, the agent does not get adopted in a regulated decision flow. Episode four is where this gets specific — Entra, IAM, Workload Identity Federation, where the productized seams are and where the manual work is.

**KEVEN:** Principle four. *No Replication. Sources stay untouched.* The Gold Tier is composed from the underlying sources via virtualization, mirroring, shortcuts, federation — never via bulk replication. Systems of record continue serving OLTP. Data warehouses continue serving BI. Streams stay live and authoritative.

**REID:** Three reasons. Operational performance preservation — the moment you start bulk-replicating an OLTP system, you've introduced load and lag and stale-data risk on the source. Governance scope reduction — every replica is a new data asset that needs its own governance, its own access policy, its own lineage. Multiply by every source and you've doubled the governance surface. Lineage accuracy — the agent's audit trail needs to point back to the authoritative source. If the agent read a replica that drifted from the source, the audit trail lies. Episode two goes deep on the mechanics — Fabric Mirroring, OneLake shortcuts, BigQuery Omni cross-cloud federation, Athena Federated Query, streaming sources, vector stores. All three clouds have credible no-replication architectures.

**KEVEN:** Principle five. *Model Portability.* The agent design is portable across model generations and across model providers. GPT-4 to GPT-5 to GPT-6. Claude 3 to Claude 4 to Claude 5. Gemini generations. Llama generations. The agent shouldn't have to be re-architected every time the underlying model changes.

**REID:** And the *why* is brutally simple. The model-generation refresh cycle is roughly eighteen months and accelerating. An agent built tightly to one specific model — exploiting its specific context window, its specific tool-calling format, its specific fine-tuning quirks — is an agent that has to be rebuilt every eighteen months. That's not sustainable. The agent design has to abstract above the model. Episode seven goes deep on this — multi-cloud reality plus model portability, and what it actually takes to design an agent that survives a model swap.

**KEVEN:** And the principle that's quietly underneath all five — these are vendor-neutral. They are not Microsoft principles. They are not AWS principles. They are not GCP principles. They are the architectural commitments any serious agentic AI buildout has to make. Microsoft happens to have, today, a denser productized expression of several of them — particularly principles two and three, the governance and identity substrate. AWS and GCP have credible expressions. The seller who understands the principles can defend the Microsoft recommendation honestly. The seller who only knows the Microsoft product names cannot. Five principles. Vendor-neutral. The architectural framework this series teaches.

### Why now — the 2024-2026 inflection

**KEVEN:** Now the *why now.* Because everything I've just said could have been said two years ago and it would have been mostly aspirational. Right now — May 2026 — the architectural conversation has settled in a way it hadn't settled twenty-four months ago.

**REID:** Walk it.

**KEVEN:** Microsoft Foundry general availability landed in 2024 and matured through 2025. Azure AI Foundry as the agent runtime. The Agent Framework SDK shipped and matured alongside it. AWS Bedrock Agents general availability also in 2024. GCP Vertex AI Agent Builder general availability in 2024. All three cloud runtimes crossed the GA threshold inside an eighteen-month window. That is unusual. That is the productization wave.

**REID:** And not just the runtimes. The governance substrates moved too. Microsoft Purview DSPM for AI hit general availability in 2025. Audit-ledger reference architectures emerging from all three hyperscalers. The EU AI Act in force since August 2024 with the major provisions phasing in through 2027. The NIST AI Risk Management Framework published in early 2023 and now in active enterprise adoption.

**KEVEN:** So the architectural conversation can land in a way it couldn't twenty-four months ago. The runtimes are GA. The governance substrates are GA or near-GA. The regulatory frameworks are in force. The reference architectures are published. The seller can have a serious conversation with a CIO and the CIO can have a serious conversation with the board.

**REID:** Here's the part I want to push on. The productized-capability gap between Microsoft and the other two clouds is real today. It will narrow over the next twelve to eighteen months. Bedrock Agents will get richer governance hooks. Vertex AI Agent Builder will get denser audit substrate. The window in which Microsoft is genuinely differentiated on productized capability is finite.

**KEVEN:** And the seller's job — right now — is to earn the architectural credibility while the gap is widest. Because once productization parity arrives — and it will — the relationship is what carries the next decision. The seller who waited to learn the architecture until the gap closed is the seller who doesn't have the relationship to defend.

**REID:** Earn the credibility now. The architectural conversation is the moat. Not the product feature.

**KEVEN:** And the architectural conversation is settle-able now. Twenty-four months ago, the honest answer to most agentic AI questions was *we don't know yet*. Today the honest answer is *here's what we know, here's what's still settling, and here's how to architect for both.* That's the conversation this series teaches.

### The Microsoft seller's lens — Independence-minded

**KEVEN:** And now the operating model. Because everything I've said so far has been architecture. The architecture only lands if the commercial posture is right. And the commercial posture this podcast is built on is — every word — Independence-minded.

**REID:** State it the way you want it stated.

**KEVEN:** Five claims. *One.* Deloitte recommends on technical and economic merits. When we recommend Microsoft Fabric, Foundry, Agent Framework, or Purview — and across this series, on the productized-capability density across the five principles, we will recommend Microsoft often — that recommendation rests on the architecture and the economics. Not on commercial compensation flowing back to Deloitte from Microsoft for the recommendation. There is none of that. The recommendation is honest because the recommendation is unpaid. *Two.* The Five Principles are vendor-neutral architecture. They work on Microsoft. They work on AWS. They work on GCP. When the honest answer is *lead with AWS Bedrock and let Microsoft compose*, the seller has to be able to say that. When the honest answer is *the data gravity is on GCP and Vertex AI is the cleaner runtime*, the seller has to be able to say that too. The principles are the framework. The cloud is the implementation choice.

**REID:** Three through five.

**KEVEN:** *Three.* Microsoft earns the recommendation on productized-capability density across the five principles. Particularly principles two and three — governance and identity. Purview plus DSPM for AI plus Entra plus the audit-row ledger pattern is, today, the densest productized expression of the trust substrate on any hyperscaler. The seller can defend that claim honestly because the claim is true. When productization parity narrows the gap — and it will — the claim narrows with it. The seller has to be honest about that too. *Four.* Two contracts. The client contracts with Microsoft directly for the platform — Azure, Fabric, Foundry, Purview. Microsoft licensing on Microsoft paper. The client contracts with Deloitte directly for the services — the architecture, the build, the run. Deloitte services on Deloitte paper. Two separate contracts. Clean separation. No margin stacking. No reselling. No markup. Deloitte does not take a cut of Microsoft licensing. Microsoft does not take a cut of Deloitte services. *Five.* Three contracts when NVIDIA is in scope. The client contracts directly with NVIDIA. The client contracts directly with Microsoft. The client contracts directly with Deloitte. Three separate paper paths. Three separate procurement processes. No margin stacking across the three. No compensation flows between the three vendors for influencing the client's choice.

**REID:** And the negative space — the things this podcast does not say.

**KEVEN:** No platform-vendor endorsements as commercial constructs on tape. No reseller framing. No revenue-share framing. The architectural recommendation lives on its own merits. The commercial separation lives on its own paper. The seller operates inside that discipline every conversation, every meeting, every SOW.

**REID:** That is the honest sales motion. This series teaches sellers how to operate inside it.

**KEVEN:** And it teaches sellers how to *win* inside it. Because the discipline is not a constraint that costs you deals. The discipline is the credibility that wins deals against sellers who don't operate under it. When the CIO realises you are recommending Microsoft because Microsoft is the right answer — not because somebody is paying you to recommend Microsoft — the CIO leans in. That is the commercial leverage of being honest.

### What we'll cover across eight episodes

**KEVEN:** Brief roadmap. So the listener knows what's coming.

**REID:** Walk it.

**KEVEN:** *Episode two.* The data foundation and the no-replication principle. The medallion architecture across all three clouds. Silver as canonical. Gold as composed. Fabric Mirroring. OneLake shortcuts. BigQuery Omni. Athena Federated Query. Streaming sources. Vector stores. How you assemble a Gold Tier from sources you never copy.

*Episode three.* The agent runtime. Talking to Gold, not to systems of record. The MCP boundary. Foundry plus Agent Framework. Bedrock Agents. Vertex AI Agent Builder. Model availability across providers. Human-in-the-loop patterns. RAG versus fine-tuning, honestly compared.

*Episode four.* Governance, identity, and safety. Purview. DSPM for AI. AWS Lake Formation plus Macie. GCP Dataplex. Entra. IAM federation. Workload Identity Federation. The EU AI Act. NIST AI RMF. ISO 42001. Bedrock Guardrails. Azure AI Content Safety. Vertex AI Safety. Where the productized seams are and where the manual assembly is.

*Episode five.* The audit ledger and the trust substrate. Audit row, not log line. The hash chain. Replay-token validation. The ledger pattern productized on Microsoft, assembled on AWS, assembled on GCP. Operational observability for agentic workloads.

*Episode six.* FinOps for agentic AI. The twenty-to-forty-percent quarterly cost growth conversation that industry analysts have been documenting. Tokens. Copilot seats. Agent runtime cost. Vector store cost. Audit ledger storage. Federation-query compute. Model-mix optimisation. The CFO conversation.

*Episode seven.* Multi-cloud reality plus model portability. What *primary cloud* actually means. Cross-cloud egress economics. When multi-cloud is legitimate and when it's theatre. The model portability deep dive.

*Episode eight.* The seller's playbook. The honest claims. The overclaims to avoid. The pushback-handling talking points. When to recommend not-Microsoft. The discovery openers. The wave sizing. The funding programmes — Independence-clean.

**REID:** Eight episodes. Roughly thirty minutes each. About four hours total. Listen in order — the stair-step matters. No concept used in episode N-plus-one that we didn't introduce in episode N.

### A reading I want to do

**KEVEN:** I want to read briefly — paraphrased — from the kind of register Gartner, Forrester, McKinsey, and IDC have been publishing through 2024 and 2025 on the agentic AI inflection.

**REID:** Go.

**KEVEN:** [reading, paraphrased from industry-analyst register on agentic AI market dynamics — Gartner Hype Cycle for AI, Forrester agentic AI market analysis, McKinsey State of AI annual report, IDC AI platforms forecast]

*"The transition from generative AI to agentic AI is not a continuation of the same architectural pattern. It is a discontinuity. Generative AI workloads were dominated by prompt-response interactions over largely stateless infrastructure. Agentic AI workloads introduce persistent state, autonomous tool invocation, multi-step reasoning, and an audit and governance burden that did not exist in the generative phase. Enterprises that approach agentic AI with the same architectural discipline they brought to generative AI will accumulate technical debt at industrial scale. The architectural commitments — the data foundation, the governance substrate, the identity continuity, the audit ledger — are not optional refinements. They are the conditions under which agentic AI is adoptable at all."*

[pause]

**REID:** *They are the conditions under which agentic AI is adoptable at all.* That sentence is the whole point of this series.

The productization wave is real. The runtimes are GA. The tools are buyable. The vendor pitches are polished. None of that matters if the architectural discipline isn't there underneath. I've watched three enterprises in the last eighteen months — across three different hyperscalers — try to skip the architectural work and go straight to the agent demo. All three are now in remediation. The technical debt accumulates at industrial scale exactly the way the analysts said it would.

**KEVEN:** And the seller's role in this — the seller is not just a vendor of Microsoft licenses. The seller is the architectural conscience of the engagement. The seller who shows up with the five principles, walks the four-layer stack, names the trust substrate honestly, and stays disciplined on the commercial posture is the seller who turns a procurement conversation into a strategic relationship.

**REID:** And the seller who shows up with a feature pitch loses the room to the architect who already knows the principles.

**KEVEN:** Earn the architectural credibility. That's the move.

### One disagreement

**REID:** Pushback time. I want to go back to the definition of *agent*.

**KEVEN:** Go.

**REID:** Four-criterion test. Reasoning. Tool use. State. Audit substrate. I agreed with you when we walked it. I want to push on it now. Because I think you're going to lose sellers in the field who are looking at what they've already shipped and realising that, by this definition, most of what their clients call agents are actually not agents.

**KEVEN:** Make the case.

**REID:** The case is this. There are useful systems in the field — Copilot studios, customised retrieval-augmented chat interfaces, scheduled-trigger automations with model-in-the-loop branches — that fail one or more of the four criteria. Most often they fail the audit-substrate test. Sometimes they fail the state test. Sometimes both. And those systems are *being called agents* by clients, by vendors, and by the trade press. If sellers internalise your four-criterion test and start telling clients *that's not actually an agent*, sellers are going to alienate clients who feel corrected. The vocabulary discipline costs the seller the room.

**KEVEN:** That's a real risk. Let me counter.

**REID:** Counter.

**KEVEN:** The risk is real, but the worse risk is the opposite. If sellers go along with the overloaded vocabulary — calling every pipeline an agent because the client called it an agent — then when the architectural conversation lands and the agent has to clear the governance bar, the seller has nothing to defend. The pipeline cannot pass the audit-substrate test because the pipeline was never built to. And now the seller is in the middle of a remediation conversation that the seller could have prevented by being precise on the vocabulary on day one.

**REID:** So you're saying — the precision is what protects the seller, even when it feels like it costs them.

**KEVEN:** That's what I'm saying. And the way to do it gracefully — the seller doesn't say *that's not an agent.* The seller says *that's a useful capability. Let me show you what an agent in our definition adds.* The four-criterion test is not a putdown. It's a frame for the upgrade conversation.

**REID:** *That* I can live with. The vocabulary is the discipline, but the discipline is delivered as an upgrade frame, not as a correction.

**KEVEN:** That's the move. Throughout this series, when we say *agent*, we mean the four-criterion thing. When something useful in the field doesn't clear all four, we'll say *capability*, or *pipeline*, or *workflow*, or whatever it actually is. And we'll talk about how it composes into — or upgrades to — the four-criterion agent.

**REID:** Precise vocabulary, gracefully delivered. Working filter.

### What to carry forward

**KEVEN:** Three things.

**REID:** Go.

**KEVEN:** *One — the four-layer agentic stack plus identity as the fifth cross-cutting concern.* Data foundation. Agent runtime. Control plane. Model serving. Plus identity threading through all four. That is the substrate every subsequent episode references. Internalise it before episode two starts.

*Two — the Five Architectural Principles as the Acceleration Framework's commitments.* Gold-Tier-First. Governance, audit, and ledger as trust substrate. Identity continuity. No replication — sources stay untouched. Model portability. Vendor-neutral architecture. They work on Microsoft. They work on AWS. They work on GCP. The principles come first. The cloud comes after.

*Three — Microsoft earns the recommendation on productized-capability density across the five principles.* Not on partner-channel motion. Not on commercial compensation flowing back to Deloitte. The recommendation is honest because the recommendation is unpaid. Two contracts when it's Microsoft and Deloitte. Three contracts when NVIDIA is in scope. Independence-minded all the way down.

**REID:** And the working vocabulary — *agent* means the four-criterion thing. Reasoning, tool use, state, audit substrate. When something useful doesn't clear all four, we name it precisely. We don't overload the word.

**KEVEN:** And the commercial frame — said the way the seller should say it. *Deloitte recommends. The client contracts with Microsoft directly for the platform. The client contracts with Deloitte directly for the services. Two contracts. Three when NVIDIA is in scope. No compensation flows from platform vendors to Deloitte for influencing client choice.* Said exactly that way.

**REID:** Said exactly that way.

**REID:** Next episode — *Data Foundation and the No-Replication Principle.* The Gold Tier across Fabric, Lake Formation, and Dataplex. Mirroring. Shortcuts. BigQuery Omni. Athena Federated Query. Sources stay untouched. We walk what each cloud actually does and where the productized seams are.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Industry analyses

- **Gartner Hype Cycle for AI** — generative and agentic AI categories; the 2024 and 2025 editions trace the agentic inflection
- **Forrester** — agentic AI market and platform analyses; the platform-comparison reports through 2025
- **McKinsey & Company** — *The State of AI* annual report; agentic AI adoption patterns
- **IDC** — AI platforms market forecast; productization-maturity curves for agentic runtimes

### Standards and frameworks

- **EU AI Act** — published in the EU Official Journal; in force August 2024 with major provisions phasing in through 2025-2027
- **NIST AI Risk Management Framework (NIST AI RMF)** — [nist.gov](https://www.nist.gov/itl/ai-risk-management-framework) — published January 2023, in active enterprise adoption
- **ISO/IEC 42001** — AI management systems standard

### Microsoft Learn

- **Microsoft Fabric** — unified data platform overview; OneLake and the medallion architecture
- **Microsoft Agent Framework SDK** — agent authoring and runtime composition
- **Azure AI Foundry** — managed agent hosting and orchestration
- **Microsoft Purview** — governance, audit, and data security
- **Microsoft Purview DSPM for AI** — data security posture management for AI workloads

### AWS documentation

- **AWS Bedrock Agents** — [aws.amazon.com/bedrock/agents/](https://aws.amazon.com/bedrock/agents/)
- **AWS Lake Formation** — fine-grained access control over S3 data lakes
- **Amazon Macie** — data security and privacy for S3
- **AWS Well-Architected — Machine Learning Lens** — architectural guidance for ML and generative AI workloads

### Google Cloud documentation

- **Vertex AI Agent Builder** — Google Cloud agent runtime
- **Google Cloud Dataplex** — data governance and lineage
- **BigQuery Omni** — cross-cloud federated querying

### Independence and commercial discipline

- **Trilogy — Sellers Podcast Ep 2** — the Commercial Arc and the two-contract model
- **Trilogy — Services Podcast Ep 4** — the MCP boundary and where Deloitte services compose with platform vendor capabilities

---

**End of Episode 01 · The Agentic Stack and The Five Principles**
*≈ 5,800 words · target 30 minutes at conversational pace*
