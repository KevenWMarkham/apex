# Episode 07 · Superagents & Practitioner Tracks

**Source:** *Professional APEX-M Services Guide* — Parts VII + VIII (Chapters 25–29)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: standup meeting hum, a chair creak, someone clearing their throat]

**MORGAN:** Six weeks into the engagement, the engineering lead pulled me aside after standup and said, *"Morgan, the agent is wrong less than it was six weeks ago. But I have no idea why. We haven't changed the prompt. We haven't changed the model. We haven't retrained anything. The agent is just... better."*

[pause]

**KEVEN:** That's the superagent learning loop working.

**MORGAN:** That's the superagent learning loop working, *invisibly,* exactly the way it was designed to. The agent is reading the LEDGER. The LEDGER is reading the Redis cache. The Redis cache is being warmed by every HITL approval, every operator correction, every agent run that produced a measurably good outcome. And six weeks of those signals — written through Gold staging, hash-chained into LEDGER, surfaced to the agent at runtime through context windows — *that* is how an APEX agent gets better without anyone touching the code.

**KEVEN:** And the chapter that says this.

**MORGAN:** Chapter Thirty in the Services Guide. *LEDGER plus Redis Cache — the Superagent Learning Loop.* Today we walk it. Then we walk the practitioner-track chapters that show how a new APEX engineer goes from zero to a working Service in a single day. Two parts, four chapters, one episode.

**KEVEN:** I'm Keven Markham.

**MORGAN:** I'm Morgan. APEX Services Podcast, Episode Seven. *Superagents and Practitioner Tracks.*

---

## Theme Statement

**KEVEN:** Two Parts in one episode. Part Seven is one chapter — Chapter Thirty — *LEDGER plus Redis Cache.* Part Eight is four chapters — Chapter Thirty-One *From Zero to RC-E2E-03 in a Day,* Chapter Thirty-Two *HLS-E2E-04 a Second Worked Example,* Chapter Thirty-Three *Agent Design Patterns,* and Chapter Thirty-Four *Performance and Cost Modeling.*

**MORGAN:** And the through-line.

**KEVEN:** Two through-lines. *Agents learn over time when the learning loop is wired in.* And — *a practitioner can run a Service in a day if the framework is real.* The two are the same idea from different angles. The first is *the agent gets better.* The second is *the engineer gets faster.*

---

## The Story

### Chapter 30 — LEDGER + Redis Cache (Part VII)

**KEVEN:** Chapter Thirty. *LEDGER plus Redis Cache — The Superagent Learning Loop.*

Let me anchor what LEDGER is. LEDGER is the *hash-chained, append-only record of every agent decision* in APEX. Section thirty point — *LEDGER as the audit-and-learning substrate.* LEDGER serves two purposes — it's the *audit trail* the auditor reads, and it's the *learning substrate* the agent reads.

**MORGAN:** Two purposes, one substrate.

**KEVEN:** One substrate. That dual-purpose is intentional. Every agent decision generates a LEDGER row — input context, tool calls, output, persona, run ID, timestamp, downstream HITL approval or correction, outcome metric. The auditor reads it forward — *"what did the agent do?"* The agent reads it backward — *"in past situations like this, what was the outcome?"*

**MORGAN:** And the Redis cache?

**KEVEN:** Section thirty point — *Redis as the working-memory hot path.* LEDGER is on OneLake — durable, hash-chained, query-by-Spark. But LEDGER is too slow for the agent to read at every invocation. Redis is the hot cache — *the agent's working memory.* Three hot caches.

**Cache one — episodic memory.** Recent runs by this agent type, indexed for fast retrieval. *"In the last seven days, how did this agent handle similar inputs?"*

**Cache two — outcome memory.** Recent HITL outcomes — what got approved, what got corrected. Drives the agent's *self-evaluation.*

**Cache three — context warming.** Pre-computed prompt prefixes — frequently-recurring instruction context. Avoids the LLM having to ingest the same boilerplate every time.

**MORGAN:** And the loop.

**KEVEN:** Section thirty point — *the loop, end-to-end.* Five stages.

Stage one — *agent runs.* Emits a LEDGER row to OneLake. Writes a thin summary to Redis episodic-memory cache.

Stage two — *outcome lands.* A HITL approver acts. An operator corrects. A downstream metric resolves the agent's decision good or bad. The outcome is appended to the LEDGER row. The Redis outcome-memory cache is updated.

Stage three — *next agent invocation reads context.* The Microsoft Agent Framework's context-builder reads Redis episodic-memory and outcome-memory. The relevant past examples land in the prompt as few-shot context.

Stage four — *agent decides with context.* The model sees the past. Implicit pattern-matching. Better decisions on average.

Stage five — *periodic reconciliation.* Every twenty-four hours, a reconciliation job walks LEDGER, rebuilds the Redis caches from authoritative state, surfaces metric drift. This is the *learning observability* loop.

**MORGAN:** And the audit story.

**KEVEN:** *The LEDGER row is the audit row.* No separate audit pipeline. The same row that drives learning drives auditing. *"Same substrate, dual purpose"* — section thirty point one. This is the architectural elegance of LEDGER.

**MORGAN:** Section thirty point — *what LEDGER is *not*.*

**KEVEN:** It's not a model fine-tuning system. It does *not* re-train the model. It does *not* update model weights. It writes context that the model reads. The model is unchanged. APEX positions explicitly against the "agentic fine-tuning" pattern that's emerging in other frameworks — because fine-tuning is a governance nightmare and an Independence problem. LEDGER is *retrieval-based learning.* Auditable. Reversible. Transparent.

**MORGAN:** And the engineering reality.

**KEVEN:** Section thirty point — *operationalising LEDGER.* Three things.

One — *every Service ships with a LEDGER schema definition.* What fields go in the row. What classifies the outcome. What the success metric is.

Two — *the Redis caches have eviction policies tuned per Service.* Some agents need a week of episodic memory; some need only the last twenty-four hours.

Three — *the reconciliation job has alerts.* If LEDGER and Redis drift, somebody is paged.

### Chapter 31 — From Zero to RC-E2E-03 in a Day (Part VIII)

**MORGAN:** Chapter Thirty-One. *From Zero to RC-E2E-03 in a Day.* This is the chapter that says — *a new engineer can build a working Service in a single day.* Walk me through.

**KEVEN:** Section thirty-one point — *the eight-hour scaffold.* Eight hours, structured.

**Hours one and two — provisioning.** Spin up the per-Practice workspace, the canonical workspace, the bootstrap Gold mart from the Service template, the MCP server skeleton.

**Hours three and four — connect Bronze.** Pick the SOR connections. Wire them. Run a test pipeline. Validate landing.

**Hours five and six — Silver conformance.** Map the Bronze tables to the canonical schemas. Run the conformance pipelines. Validate Silver outputs.

**Hours seven and eight — Gold and agent.** Materialise the Gold marts. Register the MCP tools. Wire the agent. Run end-to-end against test data. Validate the audit emission.

**MORGAN:** And the actual Service in the worked example.

**KEVEN:** RC-E2E-03 — *Returns Fraud Detection.* A version of the RC-RISK-01 Service from the catalog, simplified for the practitioner walkthrough. The chapter has step-by-step instructions, screenshot captures, code snippets. The engineer follows along. By end-of-day, they have a working agent that classifies returns as low-fraud-risk, medium-risk, or high-risk-with-human-review.

**MORGAN:** Section thirty-one point — *the verification checkpoints.*

**KEVEN:** Six checkpoints. After each two-hour block, there's a verifier. *"Can you query Bronze and see rows? Can you query Silver and see conformed output? Can you invoke the MCP tool and get structured data?"* If a checkpoint fails, the engineer pauses, fixes, then continues. The structure prevents day-eight discovery that something was broken at hour three.

**MORGAN:** And the learning value.

**KEVEN:** Section thirty-one point — *what an engineer knows after this exercise.* They've touched every layer. They've used every primary tool — Fabric workspace, OneLake, conformance notebook, MCP server, Agent Framework, Foundry deployment. They've seen what audit emission looks like. They are *catalog-ready* — they can pick up any other catalog Service and apply the same eight-hour structure.

### Chapter 32 — HLS-E2E-04, a Second Worked Example

**MORGAN:** Chapter Thirty-Two. *HLS-E2E-04, a Second Worked Example.* Why two worked examples?

**KEVEN:** Because RC-E2E-03 is *batch-dominant.* HLS-E2E-04 is *streaming-and-governance-dominant.* The engineer who has done one is ready for either Practice; the engineer who has done both is ready for any Practice. Section thirty-two point — *the contrast structure.*

**MORGAN:** What does HLS-E2E-04 actually do?

**KEVEN:** A simplified prior-authorisation draft Service. Reads incoming PA requests from the EHR. Classifies against policy. Drafts the response. HITL approver reviews. The orchestration involves streaming Bronze for incoming requests, Purview policy enforcement for PHI handling, a more sophisticated HITL approval flow than RC-E2E-03.

**MORGAN:** And the additions over RC-E2E-03.

**KEVEN:** Three additions.

One — *the streaming Bronze path.* Eventstream into the workspace. The engineer wires it.

Two — *the Purview policy deployment.* The HLS policy template is applied. The engineer sees PHI labels propagate.

Three — *the HITL approval pattern.* The Foundry tool-approval flow is wired. The engineer sees a paused run, an approval action, a resumed run.

**MORGAN:** And the time?

**KEVEN:** Section thirty-two point — *the twelve-hour version.* HLS-E2E-04 is twelve hours, not eight. The streaming Bronze and the governance overhead account for the extra four hours. Still doable in a day-and-a-half for a focused engineer.

### Chapter 33 — Agent Design Patterns

**MORGAN:** Chapter Thirty-Three. *Agent Design Patterns.* The pattern library.

**KEVEN:** Section thirty-three point — *catalogued patterns.* Many. Let me hit the three I think every engineer should internalise.

**Pattern one — the *narrow-and-call* pattern.** The agent's instructions tell it to ask one specific question, call one tool, and return the structured answer. No multi-step reasoning. The pattern fits high-volume, low-complexity inference — risk scoring, classification, draft generation. Section thirty-three point — has the prompt template.

**Pattern two — the *reasoning-with-evidence* pattern.** The agent reasons across multiple tools, cites which tool returned which evidence, and renders a structured conclusion with explicit citations. Fits decision-support workloads. Section thirty-three point — has the citation grammar.

**Pattern three — the *human-as-collaborator* pattern.** The agent works through a problem incrementally, surfacing checkpoints to a human in real-time chat. The human can redirect. Fits exploratory analytical work. Section thirty-three point — has the conversation-state pattern.

**MORGAN:** And the practical guidance.

**KEVEN:** Section thirty-three point — *pattern-to-Service mapping.* For each Service in the catalog, the manifest declares which pattern its primary agent uses. Returns fraud is narrow-and-call. Clinical decision support is reasoning-with-evidence. The cross-Service orchestrator agents are usually router-plus-narrow-and-call composed.

**MORGAN:** Section thirty-three point — *anti-patterns.*

**KEVEN:** Three.

*Don't write *generalist* agents that try to do many things.* You end up with brittle prompts and unpredictable behaviour. Multi-step orchestration of focused agents always beats one generalist.

*Don't let the agent emit free-text decisions.* Structured outputs always. We covered this in Episode Five.

*Don't put policy in prompts.* Policy belongs in Purview, in Content Safety, in tool-approval flows. The prompt should be *behavioural guidance,* not policy enforcement.

### Chapter 34 — Performance and Cost Modeling

**MORGAN:** Chapter Thirty-Four. *Performance and Cost Modeling.* The chapter every engagement lead should read in week two.

**KEVEN:** Yes. Three dimensions.

**Dimension one — Foundry consumption cost.** Section thirty-four point — *the per-Service Foundry cost model.* Inputs are model tier, tokens per call, calls per invocation, invocations per day, agent-step depth. The model produces a per-day Foundry cost estimate. APEX ships a calculator template.

**Dimension two — Fabric capacity cost.** The capacity SKU times the price-per-CU times the utilisation. Section thirty-four point — *the Fabric cost model.* The model accounts for streaming Eventhouse charges separately because they're measured differently from analytical pipelines.

**Dimension three — engineering cost.** Section thirty-four point — *delivery effort by Service archetype.* Batch-dominant Services like RC-CX-01 — eight to twelve sprint-weeks. Streaming-dominant Services like RC-SUPCHN-01 — twelve to sixteen weeks. Cross-family complex Services like AXLE-WRTY-01 — sixteen to twenty-four weeks.

**MORGAN:** And the performance side.

**KEVEN:** Section thirty-four point — *latency budgets.* APEX agents are tiered by latency expectation. Tier-A agents — sub-second response — for inline transaction-augment. Tier-B agents — under five seconds — for interactive analytical sessions. Tier-C agents — under sixty seconds — for batch or near-batch workloads.

The latency budget drives the design. Tier-A agents use lightweight models, narrow-and-call patterns, aggressive Redis context warming. Tier-C agents can use frontier models with deeper reasoning.

**MORGAN:** And the takeaway.

**KEVEN:** *Cost and performance are not Service-after-the-fact. They are Service-design inputs.* The cost model is filled in at design time, not after Wave One. The latency budget is declared in the Service manifest, not discovered in production.

### Pulling Parts VII and VIII together

**MORGAN:** Synthesis. Six beats.

**KEVEN:** Six.

One — *LEDGER is the dual-purpose substrate.* Audit and learning, same row.

Two — *Redis caches are the agent's working memory.* Episodic, outcome, context-warming.

Three — *APEX learns through retrieval, not fine-tuning.* Independence-safe. Reversible. Transparent.

Four — *an engineer can ship a working Service in eight to twelve hours given the framework.* Two worked examples in the guide. Three other Practices follow the same shape.

Five — *three agent design patterns cover almost every Service.* Narrow-and-call, reasoning-with-evidence, human-as-collaborator.

Six — *cost and performance are design-time inputs.* Not afterthoughts.

---

## APEX Facts

**MORGAN:** APEX Facts. Eight rapid.

**KEVEN:** Fact One — LEDGER dual purpose?

**MORGAN:** Audit substrate. Learning substrate. Same row.

**KEVEN:** Fact Two — three Redis caches?

**MORGAN:** Episodic memory, outcome memory, context warming.

**KEVEN:** Fact Three — how APEX agents learn?

**MORGAN:** Retrieval. Not fine-tuning. Past examples land in the prompt.

**KEVEN:** Fact Four — RC-E2E-03 build time?

**MORGAN:** Eight hours, end-to-end, batch-dominant.

**KEVEN:** Fact Five — HLS-E2E-04 build time?

**MORGAN:** Twelve hours. Adds streaming Bronze, Purview policy, HITL approval.

**KEVEN:** Fact Six — three agent design patterns?

**MORGAN:** Narrow-and-call, reasoning-with-evidence, human-as-collaborator.

**KEVEN:** Fact Seven — three APEX latency tiers?

**MORGAN:** Tier A sub-second. Tier B under five seconds. Tier C under sixty seconds.

**KEVEN:** Fact Eight — how cost is treated in APEX design?

**MORGAN:** Design-time input. Cost model filled in before build, not after.

**KEVEN:** Time.

---

## Adopt / Hold

**MORGAN:** Adopt versus Hold. Keven, Adopt.

**KEVEN:** Adopt — *LEDGER plus Redis as the standard learning substrate for every APEX Service.* Don't build a custom logging system. Don't build a custom learning pipeline. The substrate is shared. It's audited. It's Independence-safe. Use it.

**MORGAN:** Hold. When does the standard substrate not fit?

Two cases.

Case one — *truly stateless one-shot agents* — like a single-call classification with no downstream HITL. The learning loop adds overhead with no benefit. Section thirty point — has the carve-out for stateless agents.

Case two — *very low-volume Services* where the Redis cache costs more than the learning benefit. Section thirty point — has the volume thresholds. Roughly — under five hundred invocations per day, the learning gains rarely show up.

**KEVEN:** Synthesis?

**MORGAN:** Default to LEDGER plus Redis. Carve out for stateless or very-low-volume. The default is correct for ninety-plus percent of catalog Services.

---

## Lessons

**KEVEN:** Monday-morning lessons.

One — **for every new Service, declare the LEDGER schema in the Service manifest.** What fields. What classifies outcome. What the success metric is. The declaration is one-page; the value compounds.

Two — **run the eight-hour RC-E2E-03 walkthrough as the onboarding exercise for every new engineer.** Section thirty-one point — has the structure. Six hours of focused engineer time. Catalog-ready engineer at the end.

Three — **for every agent in a Service, declare which design pattern it uses.** Narrow-and-call, reasoning-with-evidence, or human-as-collaborator. The declaration drives prompt design, MCP-tool design, and Redis-cache configuration.

Four — **fill in the cost model in week three of every engagement.** Not month six. The cost model surfaces architectural decisions before they're sunk.

Five — **declare the agent's latency tier in the manifest.** Tier A, B, or C. Don't let it be discovered in production.

---

## Carve Outs

**MORGAN:** Carve outs. Mine — Chapter Thirty in full. The LEDGER plus Redis learning loop. Read it twice. The substrate is the architectural elegance that makes APEX agents *feel* alive — and it's the chapter that, when an engineer truly groks it, they become an APEX-architect rather than an APEX-engineer.

**KEVEN:** Mine — Chapter Thirty-Three, the agent design patterns. Read the prompt templates inline. Then read the *Sellers Guide* section on agent orchestration patterns side-by-side. The Sellers Guide is the *commercial* language for what the engineer is building; the Services Guide is the *implementation* language. Both perspectives, same content. Reading both is how you learn to translate between architect and seller.

---

## Sign-off

**KEVEN:** That's it for Episode Seven. Last episode coming up — *The Services Era.* Part Nine of the Services Guide. Seven chapters. Service envelopes and the experience plane. The Microsoft Agent Stack. Azure AI Foundry deep dive. Agent context — secure, audited, decision-driving. Microsoft Sentinel and Defender. Integration surfaces — M365, Power Platform, Dynamics 365, Graph. And change management — from the Application Era to the Services Era. The finale.

**MORGAN:** See you there.

[outro]

---

**End of Episode 07 · Superagents & Practitioner Tracks**
*≈ 5,200 words*
