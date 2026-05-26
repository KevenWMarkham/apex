# Episode 08 · The Services Era

**Source:** *Professional APEX-M Services Guide* — Part IX (Chapters 35–41)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: a deep exhale, then quiet]

**KEVEN:** Twenty-two years ago I started in the Microsoft technology consulting practice. Twenty-two years. And in that time I have worked through four eras of how enterprises consume Microsoft technology. The on-prem era. The cloud era. The application era. And now — the era we are in the middle of right this moment — the Services era. The era where Services, not applications, are the unit of work. Where agents, not screens, are the user interface. Where data flows, not data warehouses, are the architecture.

[pause]

**MORGAN:** And the Services Guide closes on that thesis.

**KEVEN:** The Services Guide closes on that thesis. Part Nine — seven chapters — *the Services Era.* What changes architecturally. What the Microsoft Agent Stack actually is. How Azure AI Foundry composes. How agent context actually works in production. How Sentinel and Defender wrap the agent stack with security. How M365, Power Platform, Dynamics 365, and Graph integrate. And finally — the change management chapter, the one I'd argue is the most important — *from the application era to the Services era.* How to actually take a client through this transition.

**MORGAN:** Series finale.

**KEVEN:** Series finale. Plus an Acquired-style wrap — Grading the Services Guide, Bull / Bear on APEX delivery, Lessons across all eight episodes, and Carve Outs.

I'm Keven Markham.

**MORGAN:** I'm Morgan. APEX Services Podcast, Episode Eight. *The Services Era.*

---

## Theme Statement

**MORGAN:** Format note. We compress Part Nine into eighteen minutes — seven chapters, brisk. Then ten minutes for the series wrap — Grading, Bull / Bear, Lessons, Carve Outs. Last show, full structure.

---

## The Story · Part IX Walkthrough

### Chapter 35 — Service Envelopes & the Experience Plane

**KEVEN:** Chapter Thirty-Five. *Service Envelopes and the Experience Plane.* Two ideas.

**Service envelopes** — section thirty-five point — *the four-envelope model for delivery.* Same word as the Sellers Guide six-envelope model, different cut. Delivery has *four* envelopes that matter operationally — *data, compute, governance, experience.* Each one bounds what a Service can do.

**The experience plane** — section thirty-five point — *what the user actually touches.* In Services-era thinking, the experience plane is *not* an application. It's a *surface* — a Copilot panel, a Teams card, a Power BI report, a Dynamics 365 form, a custom web UI — that surfaces the Service's output. The Service is platform-resident; the experience plane is the persona-facing edge.

**MORGAN:** And the implication?

**KEVEN:** The implication is — *you build the Service once, you surface it in many experiences.* Same warranty agent, surfaced in Teams for the warranty engineer, in the dealer portal for the dealer, in the call-center workflow for the CSR. One Service. Multiple experience surfaces. The Sellers Guide commercial framing says "build once, sell many times" — the Services Guide implementation framing says "build once, surface many times." Same idea, different lens.

### Chapter 36 — The Microsoft Agent Stack

**MORGAN:** Chapter Thirty-Six. *The Microsoft Agent Stack.* The naming the chapter introduces is critical for sellers and engineers alike. Walk me through.

**KEVEN:** Section thirty-six point — *the Microsoft Agent Stack defined.* Five layers.

**Layer one — model.** Azure OpenAI. GPT-4o, GPT-4.1, o-series, the small-model variants. The reasoning substrate.

**Layer two — runtime.** Azure AI Foundry Agent Service. Hosts agents, manages runs, handles tool approval, emits traces.

**Layer three — SDK.** Microsoft Agent Framework. The Python and .NET libraries an engineer writes against. Targets the runtime.

**Layer four — protocol.** Model Context Protocol — MCP. The wire format for agent-to-tool communication.

**Layer five — surface.** Copilot Studio, Microsoft 365 Copilot, custom UIs. Where the user meets the agent.

**MORGAN:** Five layers. Memorise the order.

**KEVEN:** Model, runtime, SDK, protocol, surface. APEX touches all five — and the *compositional discipline* is — *each layer has one Microsoft product. Don't mix.* If you start adding non-Microsoft components at the protocol or runtime layer, the audit-and-governance story collapses.

### Chapter 37 — Azure AI Foundry Deep Dive

**MORGAN:** Chapter Thirty-Seven. *Azure AI Foundry Deep Dive.* The runtime layer.

**KEVEN:** Section thirty-seven point — *the four Foundry capabilities APEX uses most.*

**Capability one — Agent Service.** The runtime that hosts an agent. Tool-approval flows. Run management. Tracing. We covered this in Episode Five.

**Capability two — Evaluation.** Foundry has built-in evaluators — semantic similarity, custom-rubric, code-based, model-graded. APEX uses these to evaluate agent quality continuously. Section thirty-seven point — *evaluation as a continuous discipline.*

**Capability three — Safety planes.** Model Gateway, Content Safety, Prompt Shields, Groundedness evaluators. APEX wires all four in the standard agent pipeline.

**Capability four — Observability.** OpenTelemetry-based tracing. Every agent run produces traces. Foundry exports them; APEX consumes them in the LEDGER plus Redis loop.

**MORGAN:** And the deployment topology.

**KEVEN:** Section thirty-seven point — *the Foundry workspace pattern for APEX.* Each Practice has its own Foundry workspace. Each Service has its own agent deployment within that workspace. Agents are versioned and traffic-split for safe rollout.

### Chapter 38 — Agent Context · Secure, Audited, Decision-Driving

**MORGAN:** Chapter Thirty-Eight. *Agent Context — Secure, Audited, Decision-Driving.* The chapter on what actually goes *into* the model prompt.

**KEVEN:** Three categories.

**Category one — file-first context.** Section thirty-eight point — *the file-first thesis.* APEX prefers context loaded from files — Markdown, JSON, structured docs — over context loaded from vector databases. Files are versioned, reviewable, auditable. Vectors are opaque. The argument is rigorous; the implementation is straightforward.

**Category two — retrieval-augmented context.** When files aren't enough — Practice-specific corpora, large reference libraries — APEX uses retrieval. The retrieval system is *governed* — Purview-classified, hash-chained, evaluated for groundedness.

**Category three — episodic context from LEDGER plus Redis.** The learning-loop context from Episode Seven. Past examples land in the prompt as few-shot.

**MORGAN:** And the discipline.

**KEVEN:** Section thirty-eight point — *the context discipline.* For every agent, declare in the Service manifest — *what goes into the context window, in what order, with what evidence stamp.* The declaration is the prompt structure. The auditor can read it. The architect can review it. The agent isn't a black box because the context isn't a black box.

### Chapter 39 — Sentinel & Defender

**MORGAN:** Chapter Thirty-Nine. *Microsoft Sentinel and Defender — Detection and Response.* The security-monitoring layer.

**KEVEN:** Right. Sentinel for SIEM-style detection across the APEX stack. Defender for endpoint, identity, and workload threat protection.

Section thirty-nine point — *what Sentinel watches in APEX.* Unusual MCP tool invocation patterns. Anomalous agent run frequencies. Failed tool approvals at scale. Pii-unlock invocation outside normal patterns. Data exfiltration signals through OneLake.

Section thirty-nine point — *what Defender watches.* Identity compromise — especially the privileged identities like pii-unlock and schema-admin. Endpoint compromise on developer workstations. Workload-level threats in Container Apps and Functions hosting MCP servers.

**MORGAN:** And the integration.

**KEVEN:** Section thirty-nine point — *the Sentinel-APEX integration pattern.* APEX ships *content packs* for Sentinel — pre-built detection rules, workbooks, and playbooks specifically for APEX agent activity. The packs are deployed with the engagement. They live alongside the client's other Sentinel content.

### Chapter 40 — Integration Surfaces

**MORGAN:** Chapter Forty. *Integration Surfaces — Microsoft 365, Power Platform, Dynamics 365, Microsoft Graph.* Where APEX touches the rest of the Microsoft enterprise.

**KEVEN:** Section forty point — *the four integration surfaces.*

**Microsoft 365 — primarily Copilot.** APEX agents surface as Copilot prompts. Cross-app context from M365 Graph available. The Sellers Guide chapter on Copilot's role as the user surface is the commercial framing for this.

**Power Platform — primarily Copilot Studio and Power Automate.** Citizen-developer extensions. APEX agents wrappable in Copilot Studio chat bots. Power Automate as a non-agent connector orchestrator — we covered Logic Apps for this in Episode Five; same shape, different product line.

**Dynamics 365 — agent embedment in CRM and ERP workflows.** Sales Copilot. Service Copilot. APEX Service agents callable from inside Dynamics workflows.

**Microsoft Graph — the cross-tenant data fabric.** Agents that need cross-app context — calendar, email, files — read through Graph. APEX agents use Graph through MCP tools that wrap Graph endpoints with the same audit-and-policy boundary.

**MORGAN:** And the architectural rule.

**KEVEN:** Section forty point — *integration via tools, not embedding.* APEX agents don't embed themselves in M365, Dynamics, or Power Platform. They expose themselves through MCP. The integration is *the integrating product calls APEX through MCP, not APEX runs inside the integrating product.* Keeps the agent's audit-and-governance boundary intact.

### Chapter 41 — Change Management

**MORGAN:** Chapter Forty-One. *Change Management — From the Application Era to the Services Era.* The last chapter of the Services Guide.

**KEVEN:** Yes. And honestly the most important chapter in the entire book. Because the *technology* of APEX is the easy part. The *organisational change* of moving from application-era thinking to services-era thinking is the hard part.

Section forty-one point — *the four cultural shifts.*

**Shift one — from "build an application" to "compose a Service."** Engineering teams used to scope projects by application. They now scope by Service in the catalog. The vocabulary changes. The work breakdown changes.

**Shift two — from "deploy a release" to "version an agent."** Releases used to be quarterly. Agents are versioned continuously, with traffic-split rollout. The cadence changes. The risk-management posture changes.

**Shift three — from "test before production" to "observe in production."** Application-era QA was test-environment heavy. Services-era operations is observability-heavy. The skill mix changes.

**Shift four — from "user trains on UI" to "user works with agent."** End-user experience changes most dramatically. Training shifts from "where do I click" to "how do I collaborate."

**MORGAN:** And the engagement implication.

**KEVEN:** Section forty-one point — *the change-management workstream in every APEX engagement.* From day one. Not an afterthought. The engagement has technical workstreams *and* a change workstream that runs the same length. The change workstream maps stakeholders, defines new operating roles, drafts the new operating procedures, runs adoption workshops.

If you skip this — the technology ships and the organisation doesn't adopt. We've seen it. Don't skip.

---

## The Series Wrap · Acquired-style

### Grading the Services Guide

**MORGAN:** OK. Eight episodes in. Time to grade. Keven — what does the Services Guide get right, what does it get wrong, what would you change?

**KEVEN:** Three dimensions.

**Dimension one — the architectural discipline.** *A-plus.* The medallion is rigorous. The Bronze/Silver/Gold contracts are precise. The MCP boundary is well-defended. The LEDGER plus Redis substrate is elegant. The chapter on canonical-lives-in-Silver alone is worth the price of the book. Architecturally, this is the most rigorous services-design framework I've seen.

**Dimension two — the catalog completeness.** *A-minus.* Thirty-eight Services across seven Practices is real coverage. RC and AXLE are deep. HLS has only four Services and feels slightly under-catalogued for the industry's complexity. TMT could use more Services in the content / media side. The minus is for *evenness* — the catalog is heavier in some Practices than others.

**Dimension three — the practitioner accessibility.** *B-plus.* The eight-hour walkthrough is excellent. The pattern library is excellent. But the book is *dense.* Forty-one chapters, thousands of lines of detail. A junior engineer encountering this for the first time will feel buried. The minus is for *on-ramp gradient* — the gradient is steep.

**MORGAN:** Overall?

**KEVEN:** A-plus on architecture. A-minus on catalog. B-plus on accessibility. Average — *A.* And specifically — this guide is the single best reference for *building* enterprise agentic AI I've encountered. The accessibility gap is fixable; the architecture and catalog are very hard to build, and they're here.

### Bull / Bear · the final pass

**MORGAN:** Bull / Bear, last time. I'll go Bull.

**Bull case.** The Services Guide ships an *operating architecture* for enterprise agentic AI that's three years ahead of what any other framework has. Medallion plus canonical plus MCP plus LEDGER plus Foundry plus Purview — composed coherently — is not something anyone else has assembled. The team that masters this guide is two years ahead of the engineering market. If Deloitte invests in *practitioner enablement* — bringing engineers up the steep on-ramp — the framework compounds enormously.

**Bear case.** Two real risks.

Risk one — *the Microsoft platform is moving fast.* Agent Framework changed naming twice in the past eighteen months. Foundry's safety planes are still maturing. Fabric IQ is emerging as a new layer. Some details in the guide will be stale within two quarters. The bear case is *living-document maintenance debt.*

Risk two — *the framework is more complex than the median client engineering team can absorb.* Some clients will need Deloitte to operate the Services era for them — they will not be self-sufficient. That's actually fine commercially, but it's a different positioning than the framework's *"you can run this internally after Wave Three"* aspiration.

**KEVEN:** Synthesis?

**MORGAN:** The framework wins if two investments happen — *continuous content refresh* and *practitioner enablement.* Without either, the framework's value caps. With both, it compounds.

### Lessons — series-wide

**KEVEN:** Series-wide lessons. Eight lessons. One per episode.

**Lesson One — Episode One.** *The Service is the data flow.* Not the agent. The flow. Six waypoints. Three rules. Memorise.

**Lesson Two — Episode Two.** *Bronze absorbs the messy real world.* SOR inventory in week one. Velocity classification in design. Tokenization before landing. PII never reaches Bronze in cleartext.

**Lesson Three — Episode Three.** *Silver is the anchor of stable meaning.* Identity reconciliation discipline. Fourteen canonical families. Canonical extensions go through a governance gate. Purview is the audit interface.

**Lesson Four — Episode Four.** *Gold is per-Service, shaped for decisions.* The MCP tool surface is the narrowing point. Read-only by default. Structured returns with source metadata.

**Lesson Five — Episode Five.** *Workflow is a first-class declared artefact.* Failure handling is explicit per step. Agent Framework is the SDK; Foundry Agent Service is the runtime. Content Safety is in the pipeline by default.

**Lesson Six — Episode Six.** *Thirty-eight Services in the catalog. Memorise the seven flagships.* Don't custom-build until you've checked the catalog. Service manifest declares everything.

**Lesson Seven — Episode Seven.** *LEDGER plus Redis is the dual-purpose substrate.* Audit and learning, same row. Retrieval-based learning. Never fine-tuning. Cost and performance are design-time inputs.

**Lesson Eight — this episode.** *The Services era is a cultural shift, not just a technical shift.* The change workstream is from day one, not an afterthought.

### Carve Outs · the series finale

**MORGAN:** Carve outs. Last time.

**KEVEN:** Mine — read the *full Trilogy.* You've now done Sellers and Services. Read the *Deployment Guide.* It's the operations runbook — how this all actually runs in a client tenant in production. The Trilogy is the firm speaking. One volume is one voice.

**MORGAN:** Mine — for every chapter in the Services Guide you've heard about in these eight episodes, *go open it and read it once.* The audio is the map. The map is not the territory. The chapter is the territory. Six hours of reading. Compounds for years.

**KEVEN:** And one I'd add — the Vuori Implementation Guide. The worked example of what an APEX engagement actually feels like from week one to Wave Three. If you have to live inside an APEX engagement, that's the document that shows you the shape.

---

## Final Sign-off

**KEVEN:** That's a wrap on the APEX Services Podcast. Eight episodes. Why Services Are Data-First. Bronze. Silver. Gold. Orchestrations. The Service Catalog. Superagents and Practitioner Tracks. And the Services Era. About forty thousand words. About four hours.

Thank you for listening. The implied listener for this series is somebody who builds and runs APEX engagements. If you walk into a sprint review Monday morning with the medallion contract in your head and the MCP tool design principles on your notepad — this series did its job.

**MORGAN:** And — read the Sellers Podcast, the Services Podcast, and the Deployment Podcast when it ships. The Trilogy speaks in three voices for a reason. All three are how you become fluent in APEX end-to-end.

**KEVEN:** I'm Keven Markham.

**MORGAN:** I'm Morgan. This was the APEX Services Podcast. See you in the workspace.

[outro music · long]

---

**End of Episode 08 · The Services Era**
**End of Series**
*≈ 5,250 words · series total ≈ 40,000 words*
