# Episode 05 · Orchestrations

**Source:** *Professional APEX-M Services Guide* — Part V (Chapters 16, 17, 18, 19, 20, 21, 22)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: laptop fan ramping up under heavy load]

**KEVEN:** Six weeks ago, an APEX engagement I'm advising hit a moment that taught me something I think every engagement should know. The orchestration was working. The agents were calling MCP tools correctly. The audit trail was emitting. And then a sprint reviewer said, *"This is great. But can you show me what happens when the third agent in the chain fails?"*

[pause]

**MORGAN:** And nobody had ever tried.

**KEVEN:** Nobody had ever tried. So they ran a test. They forced a failure on the third agent. And the parent orchestration *kept going.* The fourth agent ran on the missing output. The fifth agent ran on the corrupted state of the fourth. The orchestration finished. The user got an answer that looked perfectly normal. And the audit trail showed nothing wrong — because every individual step had emitted a successful trace.

**MORGAN:** That's an orchestration that's *technically* working.

**KEVEN:** That's an orchestration that's *technically working and structurally broken.* The whole point of orchestration is composition. The whole point of composition is that the *whole* must be more reliable than any *part*. If a child failure poisons the rest of the chain silently, you don't have an orchestration. You have a sequence of agents that happens to call each other. Part Five of the Services Guide is the chapter that prevents that.

**MORGAN:** I'm Morgan.

**KEVEN:** I'm Keven Markham. APEX Services Podcast, Episode Five. *Orchestrations.*

---

## Theme Statement

**MORGAN:** Part Five. Seven chapters. The biggest Part of the Services Guide. Walk me through.

**KEVEN:** Chapter Sixteen — *Workflow Design Patterns.* Chapter Seventeen — *Agent Orchestration Archetypes — Deep Dive.* Chapter Eighteen — *Microsoft Agent Framework Deep Dive.* Chapter Nineteen — *Responsible AI and Azure AI Content Safety.* Chapter Twenty — *n8n on Laptop.* Chapter Twenty-One — *Azure Logic Apps Hybrid.* Chapter Twenty-Two — *Cross-Service Composition.*

**MORGAN:** That's a lot for one episode.

**KEVEN:** It is. We move fast. The depth is the chapter — we're going to land the architecture beats, not read the code.

---

## The Story

### Workflow design patterns (Chapter 16)

**KEVEN:** Chapter Sixteen. *Workflow Design Patterns.* This is the chapter that defines *what a workflow even is in APEX.*

Section sixteen point — *the three layers of workflow.* Bottom layer is *agent step.* Middle layer is *orchestration* — a directed graph of agent steps. Top layer is *Service workflow* — the end-to-end business process from trigger to outcome to audit.

**MORGAN:** And the design discipline.

**KEVEN:** Section sixteen point — *workflow as a first-class artefact.* Every Service ships its workflow as a *declared, versioned, reviewable* document. Not as code embedded in an orchestration. The workflow document is — in YAML or JSON — the sequence of agent invocations, the parameters, the branches, the failure handlers, the audit emission points.

**MORGAN:** Why declarative?

**KEVEN:** Three reasons. *Reviewability* — the engagement lead can read the workflow. *Verifiability* — the security architect can audit it. *Testability* — the workflow can be replayed in test environments with mocked tool returns.

**MORGAN:** Section sixteen point — *the failure-handling discipline.*

**KEVEN:** Yes, the prevention of the cold-open story. Three rules.

Rule one — *every agent step declares a failure-mode-classifier.* When the step fails, the classifier categorises — recoverable, partial-result, unrecoverable. The classification drives the next step.

Rule two — *unrecoverable failures terminate the orchestration with an audit event.* Not silently. Not "best effort." Hard stop. The user sees a graceful error. The audit captures the failure.

Rule three — *partial-result failures emit explicit partial markers.* Downstream steps that consume the partial result *must* declare they accept partial input. Otherwise the orchestration terminates.

**MORGAN:** And that's what prevents silent corruption.

**KEVEN:** That's what prevents silent corruption.

### Agent orchestration archetypes (Chapter 17)

**MORGAN:** Chapter Seventeen. *Agent Orchestration Archetypes — Deep Dive.* The Sellers Guide mentioned six patterns. The Services Guide goes deeper. Let me walk them.

**KEVEN:** Yes. Six archetypes, with implementation patterns for each.

**Archetype one — Sequential.** Steps in order. Output of each feeds the next. Used for the warranty root-cause chain. Section seventeen point — *the sequential pattern.* Implementation pattern — parent orchestrator agent invokes child step agents in a `for` loop with shared context.

**Archetype two — Parallel fan-out.** Parent dispatches N child agents in parallel, aggregates results. Used for cohort analysis. Section seventeen point — *the parallel fan-out pattern.* Implementation — `asyncio.gather` over child invocations, then aggregator agent.

**Archetype three — Hierarchical.** Parent supervises child agents, each child has its own tools. The most common APEX pattern. Section seventeen point — *the hierarchical pattern.* Parent owns audit emission for the whole tree.

**Archetype four — Loop/iterate.** Agent re-runs itself until a quality threshold. Used in writing, classification, proposal generation. Section seventeen point — *the loop pattern.* Implementation — agent emits a self-evaluation; orchestrator decides whether to re-invoke.

**Archetype five — Debate.** Two agents argue; third adjudicates. Used in clinical decision support and regulatory pattern matching. Section seventeen point — *the debate pattern.*

**Archetype six — Router.** Top-of-orchestration agent picks the downstream path. Used as the entry agent for many Services. Section seventeen point — *the router pattern.*

**MORGAN:** Section seventeen point — *parent-child audit composition.* Critical.

**KEVEN:** Yes. The parent orchestrator owns the audit trail. Child agents emit local traces. The parent stitches the trail. The composed audit row has — parent invocation ID, child step ID, child agent ID, tool calls, results, timings. The auditor reads a single hierarchical audit story from the parent's perspective, drilling into children as needed.

### Microsoft Agent Framework deep dive (Chapter 18)

**MORGAN:** Chapter Eighteen. *Microsoft Agent Framework Deep Dive.* Possibly the most important chapter in Part Five for engineers.

**KEVEN:** Yes. And the chapter explicitly grounds the relationship between the framework, the runtime, and the platform. Let me walk the key beats.

**Section eighteen point — the framework versus the runtime.** Microsoft Agent Framework is the SDK — the Python or .NET code an engineer writes to define an agent. Azure AI Foundry Agent Service is the runtime that hosts the agent in production. Same agent code; different deployment targets.

**Section eighteen point — the framework primitives.** Three primitives matter most.

**Primitive one — Agent.** The base class. Defines the agent's instructions, model, tools, and persona.

**Primitive two — Tool.** The thing the agent can call. In APEX, tools are MCP tools — declared in the Service's MCP server, registered into the agent at instantiation.

**Primitive three — Run.** The execution unit. An agent run is bounded — input, tool calls, intermediate state, output, audit. Every run gets a run ID. The audit trail is keyed on run IDs.

**Section eighteen point — local development pattern.** The framework supports running agents *locally* during development. Same code that ships to Foundry. Local Redis. Local MCP server. The development loop is — write agent, run locally against test data, deploy to Foundry for integration testing.

**Section eighteen point — structured outputs.** Critical. APEX agents always emit *structured* outputs, not free text. The agent's output schema is declared in the Service manifest — what fields, what types, what constraints. The framework's response-format support enforces this at the model layer.

**MORGAN:** Tool approval flow — section eighteen point —.

**KEVEN:** The Foundry tool-approval pattern. When an agent's run wants to invoke a write tool — one that changes external state — the run pauses, emits an approval request, and waits. A human approver — or another policy-driven check — approves or rejects. The run resumes. This is how APEX implements HITL inside the framework. The pattern is *first-class* in Foundry's Agent Service.

**MORGAN:** Section eighteen point — *agent versioning and rollout.*

**KEVEN:** Agents are versioned like code. Foundry Agent Service supports side-by-side versions and traffic splitting. The APEX pattern is — *agent version N runs at full traffic; new version N+1 runs at five percent; canary metrics drive promotion or rollback.* Section eighteen point — has the rollout protocol.

### Responsible AI and Content Safety (Chapter 19)

**MORGAN:** Chapter Nineteen. *Responsible AI and Azure AI Content Safety.* The governance chapter of the orchestration story.

**KEVEN:** Yes. Two arms.

**Arm one — RAI principles applied to APEX.** Fairness, reliability, safety, privacy, security, inclusiveness, transparency, accountability. Section nineteen point — *operationalising RAI in APEX.* Each principle has concrete APEX-pattern mappings. Privacy maps to pii-unlock. Transparency maps to the audit row. Accountability maps to the run ID and the persona claim.

**Arm two — Azure AI Content Safety integration.** Every agent input and output passes through Content Safety. The default checks — hate, violence, self-harm, sexual, jailbreak attempts. Section nineteen point — *the integration pattern.* Content Safety runs in the framework's prompt-and-response pipeline. Failures emit an audit event and produce a graceful agent refusal.

**MORGAN:** And the customisation pattern.

**KEVEN:** Section nineteen point — *custom blocklists and policy.* Practice-specific. HLS has custom blocklists around clinical advice the agent must refuse. RC has custom blocklists around financial-advice refusal. AXLE has custom blocklists around safety-critical claims the agent must escalate. The customisations live in the Service manifest, enforced by Content Safety at runtime.

### n8n on laptop (Chapter 20)

**MORGAN:** Chapter Twenty. *n8n on Laptop.* Interesting choice for a Microsoft-stack book. Why is n8n here?

**KEVEN:** Because n8n is the *developer loop* for orchestration prototyping. Section twenty point — *the local-laptop development pattern.* An engineer can prototype an orchestration in n8n on a laptop in two hours — drag-drop workflow, mock tools, see the flow run end-to-end. Once the shape is right, the workflow is ported to either Agent Framework directly or Azure Logic Apps for production.

**MORGAN:** And the actual workflow migration.

**KEVEN:** Section twenty point — *the migration pattern.* n8n exports JSON. APEX has a tool that translates n8n JSON into the APEX workflow declaration format. The tool isn't perfect — it covers the common patterns — but it shortcuts the prototype-to-production gap for orchestration teams.

**MORGAN:** Section twenty point — *when n8n stays in production.*

**KEVEN:** Rarely. APEX position — *n8n is a development tool. Production runs on Agent Framework, Foundry Agent Service, or Logic Apps.* Exceptions: small internal-only workflows where n8n is fine. Not client-facing.

### Azure Logic Apps hybrid (Chapter 21)

**MORGAN:** Chapter Twenty-One. *Azure Logic Apps Hybrid.* Why hybrid?

**KEVEN:** Because some Service workflows have steps that are best as agent steps and steps that are best as classic connector-based steps. Examples — *send email, update CRM, post to Teams, write Excel.* These are *not* good agent tasks. They're API integrations. Logic Apps has hundreds of pre-built connectors. The pattern — *agent steps live in Agent Framework, connector steps live in Logic Apps, the two compose.*

**MORGAN:** Section twenty-one point — *the composition pattern.*

**KEVEN:** Yes. Three patterns.

Pattern one — *Logic Apps as orchestrator.* The Logic App is the workflow; it calls Agent Framework agents as HTTP endpoints. Common for connector-heavy workflows.

Pattern two — *Agent Framework as orchestrator.* The agent orchestrator calls Logic Apps as tools — wrapping a Logic App as an MCP tool. Common for agent-led workflows that need occasional connector reach.

Pattern three — *side-by-side.* Both run in parallel; an event-driven trigger sequences them. Used for workflows where the agent and the connector path are equal-citizen siblings.

**MORGAN:** And the choice.

**KEVEN:** Section twenty-one point — *the orchestrator-choice decision.* Two questions. *Which steps dominate by count?* If most steps are connector calls, Logic Apps orchestrator. If most steps are agent reasoning, Agent Framework orchestrator. *Where is the audit trail anchored?* APEX prefers Agent Framework anchored — the audit row format is native there. Use Logic Apps orchestrator only when the connector dominance is overwhelming.

### Cross-Service composition (Chapter 22)

**MORGAN:** Chapter Twenty-Two. *Cross-Service Composition.* The last chapter of Part Five — and the chapter that handles Wave Two complexity.

**KEVEN:** Right. By Wave Two, the client has three to five Services in production. They will, inevitably, want a higher-order workflow that spans them. *"Run loyalty-churn analysis, then trigger the personalised-outreach Service, then trigger the inventory-allocation Service if the loyalty-churn cohort needs replenishment."*

That's a cross-Service composition.

**MORGAN:** And the pattern.

**KEVEN:** Section twenty-two point — *the cross-Service orchestrator.* It's an orchestration *of orchestrations.* Sits in a dedicated cross-Service workspace. Calls each Service's parent orchestrator as a high-level tool. Each Service maintains its own audit trail; the cross-Service orchestrator maintains the *composition* audit trail. The auditor reads either level depending on the question.

**MORGAN:** Section twenty-two point — *the composition policy contract.*

**KEVEN:** Critical. Cross-Service compositions are *policy-bounded.* The cross-Service workspace has its own Purview policy template. The composition declares which Services it may invoke. The composition's persona — the user identity acting through the cross-Service orchestrator — must have permissions on *all* invoked Services. Not just the orchestrator.

**MORGAN:** And the failure mode.

**KEVEN:** Section twenty-two point — *partial-success in compositions.* If the loyalty Service succeeds but the inventory Service fails — what's the composition outcome? The declaration handles this. Some compositions are *all-or-nothing* — failure cascades; everything rolls back. Some are *best-effort* — partial success is acceptable and surfaced. The declaration in the Service manifest is explicit. Don't leave this implicit.

### Pulling Part V together

**MORGAN:** Synthesis. Five beats for orchestration.

**KEVEN:** Five beats.

One — *workflow is a first-class declared artefact.* YAML or JSON. Reviewable. Versioned. Testable.

Two — *failure handling is explicit per step.* Three classes — recoverable, partial-result, unrecoverable. Silent corruption is the enemy.

Three — *Microsoft Agent Framework is the SDK. Foundry Agent Service is the runtime. MCP tools are the data boundary.* Get those primitives right and the rest follows.

Four — *Content Safety is in the pipeline by default.* Customise blocklists per Practice. Audit refusals.

Five — *cross-Service composition is its own discipline.* Its own workspace, its own policy template, its own audit composition. Don't wing it.

---

## APEX Facts

**MORGAN:** APEX Facts. Eight rapid.

**KEVEN:** Fact One — three layers of workflow?

**MORGAN:** Agent step, orchestration, Service workflow.

**KEVEN:** Fact Two — three failure-mode classifications per step?

**MORGAN:** Recoverable, partial-result, unrecoverable.

**KEVEN:** Fact Three — six orchestration archetypes?

**MORGAN:** Sequential, parallel-fan-out, hierarchical, loop, debate, router.

**KEVEN:** Fact Four — three Agent Framework primitives?

**MORGAN:** Agent, Tool, Run.

**KEVEN:** Fact Five — what enforces structured outputs?

**MORGAN:** The framework's response-format support, declared in the Service manifest.

**KEVEN:** Fact Six — RAI principles operationalised in APEX?

**MORGAN:** Eight. Privacy maps to pii-unlock; transparency maps to audit row; accountability maps to run ID and persona claim.

**KEVEN:** Fact Seven — n8n role in APEX?

**MORGAN:** Local prototyping tool. Not production. Migration tool exports to APEX workflow format.

**KEVEN:** Fact Eight — cross-Service composition workspace?

**MORGAN:** Dedicated. Own Purview policy template. Composition's persona needs permissions on all invoked Services.

**KEVEN:** Time.

---

## Adopt / Hold

**MORGAN:** Adopt versus Hold. Keven, Adopt.

**KEVEN:** Adopt — *declarative workflows in YAML or JSON as the source of truth, even before the orchestration code exists.* Write the workflow document first. Get the reviewer sign-off. Then build it. The discipline of writing the workflow forces every failure case, every audit emission, every persona check to surface in design. Three hours of writing prevents three sprints of refactor.

**MORGAN:** Hold. When does declarative-first slow things down?

Two cases.

Case one — *very early prototyping.* When you don't yet know what the workflow shape is, writing a declarative spec is premature. Prototype in n8n. Discover the shape. Then formalise.

Case two — *very small workflows.* A two-step workflow doesn't need a declarative document — the code *is* the document. Apply judgment. The declarative-first rule kicks in at maybe four or more steps.

**KEVEN:** Synthesis?

**MORGAN:** Prototype freely, formalise as you scale. By the time the workflow is in a sprint, declarative is mandatory.

---

## Lessons

**KEVEN:** Monday-morning lessons.

One — **for every Service workflow, write the declarative document first.** Steps, parameters, branches, failure handlers, audit emission points. Then code.

Two — **for every agent step, declare the failure-mode classifier.** Recoverable, partial-result, unrecoverable. No exceptions.

Three — **for every cross-Service composition, file a Purview policy template before the build sprint.** The compliance review is the gating step. Schedule it early.

Four — **stand up n8n on laptop for orchestration prototyping in week one.** It's the fastest path from idea to "I see how the workflow flows."

Five — **for every agent in the framework, declare the structured output schema in the Service manifest.** Don't let agents emit free text. The downstream debugging savings are enormous.

---

## Carve Outs

**MORGAN:** Carve outs. Mine — Chapter Eighteen, *Microsoft Agent Framework Deep Dive,* the sections on structured outputs and tool approval. The two patterns are the highest-leverage primitives in the entire framework. Read them twice, code an example, internalise both.

**KEVEN:** Mine — Chapter Twenty-Two end-to-end. *Cross-Service Composition.* Even if you're in Wave One. The chapter is what tells you whether your Wave One architecture *survives* into Wave Two. If your Wave One Services can't compose cleanly with each other, you've made a Wave Two-blocking decision. Read the chapter early.

---

## Sign-off

**KEVEN:** That's it for Episode Five. Next episode — *The Service Catalog.* Part Six. Seven chapters — one per Practice. The thirty-eight Services that ship with APEX-M. RC has seven. HLS has four. ER has six. AXLE has five. TH has five. TMT has six. ICE has five. We tour the catalog.

**MORGAN:** See you there.

[outro]

---

**End of Episode 05 · Orchestrations**
*≈ 5,200 words*
