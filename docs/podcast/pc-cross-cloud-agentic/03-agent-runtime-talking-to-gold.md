# Episode 03 · Agent Runtime — Talking to Gold, Not SORs

**Builds on:** Episodes 1-2 (the five principles + data foundation) · Trilogy — Services Ep 4 (MCP boundary)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: an engineering bullpen at the wrong hour. The kind of fluorescent-lit room where the carpet is industrial grey and the desks are open-plan. A pager going off — the actual hardware kind, because the on-call has one for the agentic platform now. The on-call's monitor is the only bright thing in the room. Three windows open. A Grafana dashboard. A terminal tailing logs. And a Slack channel with one red banner across the top — *PagerDuty: agent-runtime-prod-001 — SAP rate-limit breach — page 2 of 4.*]

**KEVEN:** I want to start tonight with a page. A real page, from a real on-call rotation, in the kind of bullpen that used to belong to a payments team and now belongs to an agentic platform team. The on-call is twenty-six minutes into the incident. The agent is hammering the SAP REST API at peak hour. The rate-limit breach has cascaded. Three downstream batch jobs are now backing up because SAP is throttling everything coming from the corporate network. The on-call is on the phone with the SAP basis team. The SAP basis team is asking — *who told you that you could point an autonomous system at our production REST endpoints?*

**REID:** And what did the on-call say?

**KEVEN:** The on-call said — *the architecture diagram. The architecture diagram said the agent reads from SAP.* And the SAP basis team said — *the architecture diagram is wrong.*

**REID:** That's the page that wakes you up at three in the morning. And it's the page that should have been prevented at the design review.

**KEVEN:** Prevented at the design review. By one architectural decision — does the agent's tool call land on a system of record, or does it land on a Gold view composed from that system of record? In the bullpen tonight, somebody answered that wrong. The agent's tool definition pointed at SAP directly. The reasoning loop made nineteen tool calls per session. Times the active agent population at peak hour. Times the number of cross-domain questions the operators were running. The math arrived at SAP's rate limit inside forty minutes.

**REID:** And SAP's rate limit was designed for transactional traffic. Order entry. Goods movement. Master-data lookups by human users behind GUIs. SAP was never designed for high-velocity, dynamic, cross-domain reads from a reasoning loop that decides at runtime which six tables to join.

**KEVEN:** And here's the painful part. Every architectural review at this enterprise — every one — had the principle on the slide. *Agents read from Gold. Agents do not read from systems of record.* The slide was there. The implementation skipped it. Because somebody on the build team decided that composing the Gold view *for this one entity type* was — *we'll get to it next sprint.* And next sprint never arrived. The agent shipped against the source.

**REID:** That's the Principle 1 violation in production. And the consequence is — the on-call is now in the conversation with SAP basis where the answer is *roll back the agent and we will rebuild this on Gold.*

**KEVEN:** Roll back the agent. Two weeks of regression. The trust with the SAP team is reset. The platform team's roadmap slips. And the next architectural review at this enterprise is going to be a different conversation, because the war story is now in the room.

**REID:** The war story is the curriculum. Welcome to Episode Three.

**KEVEN:** Episode Three. *Agent Runtime — Talking to Gold, Not SORs.* The runtime that sits on top of the Gold Tier we built in Episode Two. The MCP boundary discipline that prevents the page we just walked. Foundry, Bedrock, Vertex. Model availability honestly compared. Orchestration patterns. Human-in-the-loop. And the RAG-versus-fine-tuning-versus-distillation spectrum, said plainly. Let's go.

---

## The conversation

### The MCP boundary discipline — Principle 1 in action

**KEVEN:** Let's name the discipline first, before we name a single runtime. Because the runtime conversation only makes sense once the discipline is fixed. The discipline is — *the agent's tool calls land on Gold views. Never on systems of record. Never on the data warehouse. Never on the source-system REST API directly.* That is the MCP boundary. The agent reaches out through the Model Context Protocol surface — or its equivalent in whichever runtime — and the tool definitions on the other side of that boundary point at composed Gold artefacts. Period.

**REID:** And the reason matters, because every architect I've ever worked with has been tempted to take the shortcut at least once. The temptation is — *the source system already has a REST API. The schema is already defined. Just point the agent at it. We'll compose a Gold view later if we need it.* That sentence is the start of every page like the one we just walked.

**KEVEN:** Walk the four reasons. Plainly.

**REID:** Four reasons the discipline holds. *One — source systems weren't designed for agent traffic patterns.* Agent traffic is high-velocity, dynamic, cross-domain. A reasoning loop decides at runtime which fields it needs from which tables. Six concurrent operators, each running an agent, each making seven to twenty tool calls per reasoning chain — that's a traffic shape SAP never imagined. Same for the typical operational database. Same for the order-management system. *Two — source-direct access explodes governance scope.* Every system of record has its own access pattern, its own role model, its own audit policy. When the agent reads directly from all of those, the governance review has to enumerate all of them. Pointing the agent at one Gold view collapses that into one scope. *Three — source-direct access breaks audit posture.* The audit trail has to cross every source's logging conventions. With a Gold view, the audit row is uniform — the agent read this Gold artefact, at this timestamp, with Purview lineage propagating back to the underlying sources. *Four — schema-drift brittleness.* If the agent's tool definition points at the raw source, every minor schema event is a potential agent regression. The Gold view is a contract. Source changes flow into the Silver canonicalisation, which holds the contract steady. The agent's tool definition is stable across source-system change.

**KEVEN:** Four reasons. And the discipline is the same in all three runtimes we're about to walk. The runtime expresses the boundary differently. The discipline does not change.

**REID:** And one more piece — the MCP boundary is not just about the *first* tool call. It's about *every* tool call the agent makes across the entire reasoning chain. If six tool calls land on Gold and the seventh crosses to a source REST endpoint because the engineer was in a hurry — the discipline is broken. The auditor doesn't grade you on average. The auditor finds the one that crossed the boundary and the agent's audit posture collapses. No exceptions.

### Microsoft Agent Framework + Azure AI Foundry Agent Service

**KEVEN:** Microsoft first. Because Microsoft is where most of this listener base will start their build. And the Microsoft runtime has two distinct pieces that get conflated and shouldn't be.

**REID:** Separate them.

**KEVEN:** *Microsoft Agent Framework* is the open-source SDK. The thing the developer imports into a Python or .NET project. It defines the abstractions — the Agent, the Tool, the Thread, the Run. It manages the reasoning loop, registers tools, handles model invocation, dispatches tools, persists state across turns. It's model-agnostic by design — wire it to Azure OpenAI, to Anthropic via integration, to a local model, to anything that speaks a compatible chat-completions protocol.

**REID:** And the SDK is increasingly seen by the open-source community as the spiritual successor to Semantic Kernel — which it absorbs — combined with the AutoGen multi-agent patterns. The lineage is real. One of the more thoughtful pieces of model-agnostic agent abstraction in the open-source ecosystem today.

**KEVEN:** Second piece. *Azure AI Foundry Agent Service.* The managed hosting plane. You define your agent — tools, instructions, model — and Foundry hosts it. Persistent threads. Managed state. Native integration with Azure AI Search for the RAG layer. Native integration with the broader Azure AI portfolio — content safety, evaluations, model catalog. And the part that matters for this series — *Foundry Agent Service has native Purview audit echo.* Every tool invocation, every reasoning step, every model call, every state mutation produces a Purview audit event. The audit substrate isn't bolted on. It's part of the runtime's emission pattern. One lineage graph that connects the agent's decisions back through the Gold view back to the Silver and Bronze sources.

**REID:** That's the productized-capability density argument from Episode One in action. Foundry plus Purview is — today — the densest productized expression of *runtime plus audit substrate* on any cloud. State persistence, tool registration, identity continuity through Entra, audit echo into Purview — productized capabilities, not assembly exercises.

**KEVEN:** Tool definitions in Foundry point at Gold. Practically — a Fabric SQL endpoint over a Gold Delta table. A Power BI Direct Lake semantic model the agent calls as a tool. A Fabric warehouse query against a Gold composed view. A custom function registered as a tool that runs against a Gold artefact in OneLake. The tool surface is rich. The destination is always Gold.

**REID:** Now let me push back on the maturity story. Foundry Agent Service is GA. The single-agent runtime is solid. The multi-agent orchestration story — *this agent calls that agent which calls that agent* — is still maturing. If your design depends on hierarchical multi-agent orchestration on Foundry today, you are on the productization frontier. To be fair to Microsoft — the multi-agent maturity gap is roughly the same across all three clouds. None of the three has a fully productized multi-agent story at the same maturity as their single-agent runtime. Frontier on all three.

**KEVEN:** Frontier on all three. Conceded. And the Agent Framework SDK itself — separate from the hosted Foundry runtime — has credible multi-agent patterns in the AutoGen-derived lineage. A sophisticated team can hand-compose multi-agent today on the SDK and host it themselves. The productized managed-runtime version is what's catching up. That's the Microsoft runtime. Now AWS.

### AWS Bedrock Agents

**REID:** Let me take this one. I've shipped Bedrock Agents in production for a client whose data of record was on S3 at scale. The architecture was — Glue catalog, Iceberg tables on S3, Lake Formation policies, Athena as the query surface, Bedrock Agents as the runtime. End-to-end on AWS, which was the right call for that client.

**KEVEN:** Walk Bedrock Agents.

**REID:** *AWS Bedrock Agents* is the managed agent service. You define an agent — instructions, model, action groups. Bedrock hosts the reasoning loop. The interesting piece is *Action Groups* — how you give the agent tools. You define the tool surface in one of two ways. Either as an *OpenAPI specification* — JSON or YAML describing parameters, endpoint, response shape, security — pointing at a Lambda function or HTTPS endpoint. Or as a *Lambda function* with a more direct binding. Both patterns produce the same agent-side semantics. In the architecture I shipped, action groups pointed at Athena queries against Gold Iceberg tables, with Lake Formation policies governing column-level access. The MCP boundary discipline held — tool calls landed on Athena queries against Gold tables, not the operational sources behind them.

**KEVEN:** And the RAG layer on Bedrock.

**REID:** *Bedrock Knowledge Bases.* The managed RAG abstraction. You give it a source — typically an S3 bucket of documents — and Knowledge Bases handles chunking, embedding, vector indexing, retrieval. The vector store underneath is abstracted. You don't pick it. For teams who want to skip the vector-store decision entirely, genuinely useful. Then *Bedrock Guardrails* for content safety — topic restrictions, denied-topic enforcement, sensitive-information redaction, configurable per agent. Episode Four goes deep on the safety story across all three clouds.

**KEVEN:** And model availability on Bedrock — say it the way you mean it.

**REID:** Say it the way I mean it. *Anthropic Claude is native and excellent on Bedrock.* Anthropic and AWS have a deep integration. Latest Claude versions land on Bedrock first, often by weeks ahead of where they land elsewhere. The cadence on Bedrock is leading. If a client's preferred model is Claude and they want the newest version under support contract — Bedrock is the answer. Bedrock also hosts Meta Llama, Mistral, Cohere, Stability AI, Amazon Titan, AI21. Broadest model breadth of the three majors. If model selection is the dominant requirement, Bedrock has the lead today.

**KEVEN:** And the seller's posture when Bedrock is the right call.

**REID:** When the client's data gravity is AWS-resident and Claude is the preferred model — Bedrock is the right runtime. The Microsoft posture is *compose, do not displace.* Foundry doesn't have to be the agent runtime to land Microsoft value. Microsoft can compose at the Purview governance layer over the AWS data foundation, at the Power BI presentation layer, at the Copilot Studio orchestration layer for human-facing workflows. The runtime decision is not the only place Microsoft lands.

**KEVEN:** That's the honest move. Now Vertex.

### GCP Vertex AI Agent Builder + Agent Engine

**REID:** Vertex. The youngest of the three productized runtimes. I have the least production hours on Vertex personally — but I've stood it up and watched a client team ship a workload on it.

**KEVEN:** Walk it.

**REID:** *Vertex AI Agent Builder* is the no-code-to-low-code agent definition tooling. Google's pitch — stand up an agent in the console, define the tools, point at a knowledge source, deploy. The low-code surface is well-executed. For prototyping, for getting an agent into a sandbox quickly, Agent Builder is fast. Then *Vertex AI Agent Engine* is the managed hosting plane — same shape as Foundry Agent Service and Bedrock Agents. Deploy your agent, Agent Engine hosts the reasoning loop, manages state, dispatches tool calls. Agent Builder authors. Agent Engine runs. Plus *Agent Garden* — Google's curated set of templates and patterns. Reasoning agents, retrieval agents, function-calling agents, multi-step planning agents. Useful on-ramp.

**KEVEN:** Tool definitions point at BigQuery.

**REID:** Tool definitions commonly point at BigQuery views — the Gold Tier equivalent on GCP. Same MCP boundary discipline. And leveraging Episode Two — the Gold view can be composed via BigLake over external object stores, including S3 and Azure Blob via BigQuery Omni. Agent on Vertex, tool calls landing on BigQuery, data underneath cross-cloud federated. Clean architecture for a multi-cloud data estate.

**KEVEN:** And Workload Identity Federation.

**REID:** *Workload Identity Federation* is the GCP cross-cloud identity story. The agent on Vertex can assume a federated identity that maps to an AWS IAM role, or to a Microsoft Entra principal, to access cross-cloud resources without static credentials. Mature. For cross-cloud tool access, the productized answer. Genuinely strong.

**KEVEN:** And model availability.

**REID:** *Gemini family is native on Vertex.* Latest Gemini versions land first. Vertex also hosts Anthropic Claude via partnership integration, Meta Llama, Mistral, Codey for code-specific tasks, and a broad Model Garden of open-source models. Gemini-native is the lead.

**KEVEN:** And the maturity assessment.

**REID:** Honest assessment — Vertex Agent Builder is the youngest. GA in 2024. Google's investment cadence is real and accelerating. The console UX is excellent. Productization density compared to Foundry and Bedrock is catching up. Dataplex is the GCP governance substrate and it's strong, but the runtime-to-governance native echo is less productized than Foundry-plus-Purview today. Cross-cloud honesty — when the client is GCP-strategic, when data gravity is in BigQuery, when Gemini is preferred, Vertex is the right runtime. Microsoft posture is compose-do-not-displace. Same pattern as Bedrock.

**KEVEN:** Three runtimes. All GA. All credible. Different productization densities. Different model-native stories. Same architectural discipline underneath — MCP boundary, Gold-Tier-first tool destinations, audit substrate, identity continuity.

### Model availability — honest comparison

**KEVEN:** Let's spend a minute on the model side. Because in a lot of CIO conversations I'm in, model selection is the first question the client asks. And the honest answer is — the model you want determines, more than you'd expect, which runtime is the cleanest.

**REID:** Walk it.

**KEVEN:** *OpenAI models — GPT-4, GPT-4o, GPT-4.1, the o-series reasoning models — are native on Microsoft Foundry.* The OpenAI integration with Microsoft is the deepest of any model-provider-to-cloud relationship. Latest OpenAI models land on Foundry first. The Azure OpenAI Service hosts them. The Foundry agent runtime uses them as native models. If the client's preferred model is GPT, Foundry is the answer. OpenAI is also accessible from Vertex via partnership integration. The Foundry version is the lead.

**REID:** *Anthropic Claude — Claude 3.5, Claude 3.7, Claude 4, Claude 4.5 — is native on AWS Bedrock.* Latest Claude versions land on Bedrock first, often by weeks. Claude is also available on Vertex via the Anthropic-Google partnership integration. Claude is increasingly available on Foundry as well, through Microsoft's expanding model-catalog integration with Anthropic. But Bedrock is where the latest Claude runs first. If the client's preferred model is Claude and they want the absolute newest version under support, Bedrock is the answer.

**KEVEN:** *Google Gemini — the Gemini family — is native on Vertex AI.* Latest Gemini versions land on Vertex first. Gemini is accessible from Microsoft and AWS via API integrations, but the Vertex-native experience is the deepest. If the client's preferred model is Gemini, Vertex is the answer.

**REID:** *And the open-model ecosystem — Meta Llama, Mistral, Cohere, Stability AI, AI21, Amazon Titan — has its broadest selection on Bedrock.* The Bedrock model breadth is the widest. Vertex Model Garden is also broad. Foundry's model catalogue is expanding but historically led with OpenAI-native and is broadening through partnership integrations.

**KEVEN:** Say the takeaway plainly.

**REID:** The takeaway, plainly. *If model selection is the dominant requirement — pick the cloud where your preferred model is native.* Bedrock has the multi-vendor lead and the Claude lead. Foundry has the OpenAI lead. Vertex has the Gemini lead. That's the model-axis truth. For most enterprise agentic work, model selection is not the *only* axis — the governance substrate, the data foundation, the productized control plane matter more than which model is two weeks newer. But when the client has a hard model preference, the model choice and the runtime choice are coupled.

### Orchestration patterns

**KEVEN:** Now orchestration patterns. Once you have a runtime, the next question is — how does the agent break work into steps? Three common patterns. *Sequential chains* — step one's output feeds step two's input, linear. Simplest. Fits the largest share of agentic workflows. *Parallel decomposition* — the agent identifies independent sub-questions, dispatches them in parallel, synthesises results. Useful when sub-questions don't depend on each other. Latency wins. Cost can grow. *Hierarchical sub-agents* — top-level agent decomposes into sub-tasks, dispatches each to a specialised sub-agent with its own reasoning loop and tool set. This is the pattern the multi-agent maturity-gap conversation circles around — fully productizing it is still the frontier on all three runtimes.

**REID:** And the cloud-independence point matters. All three patterns work on all three runtimes. Foundry, Bedrock, Vertex Agent Engine — all support sequential, parallel, hierarchical. Pattern choice is architectural, not vendor-driven. The seller who pitches *Foundry has better orchestration patterns* loses the room when the architect asks what specifically. Differentiation is at the productization-density layer, not the pattern-availability layer. And pattern selection is a design decision, not a runtime decision. Pick the simplest pattern that fits the workload. Sequential first. Parallel when sub-questions are genuinely independent. Hierarchical when sub-tasks are different enough in nature that a single agent's tool set would balloon. Most enterprise designs land at sequential plus a small amount of parallel. Hierarchical is the right pattern in ten percent of cases, not fifty.

**KEVEN:** Simplest pattern that fits. The discipline that prevents over-engineering.

### HITL design patterns — deeper

**KEVEN:** Now Human-in-the-Loop. HITL. The next architectural commitment under the runtime — when does the agent ask a human, and when does it proceed autonomously? This is where regulated-enterprise designs separate from demo designs.

**REID:** Walk gate placement.

**KEVEN:** *Gate placement.* The HITL gate sits at one of two moments. *Before an irreversible action* — the agent is about to send the email, post the order, file the disclosure, push the config change. The action can't be undone by re-running the agent. The gate goes before. *After a reasoning chain composition* — the agent has a recommendation ready, but it requires sign-off before propagating into a system of record. The gate is at the synthesis point, not at every individual tool call. The agent doesn't stop and ask permission to read from Gold. It stops and asks for sign-off on the conclusion.

**REID:** And the failure mode I see most — gate placed wrong. Gate too early, every tool call asks for approval, the operator gets gate fatigue and rubber-stamps everything. Gate too late, the irreversible action happens before any human saw it, the regulator finds it in the audit and the agent gets pulled. Gate placement is design discipline, not a runtime feature.

**KEVEN:** Interface design.

**REID:** *Interface design for the HITL operator.* The operator approving the conclusion needs to see — the audit row, the reasoning chain, the data the agent read, the recommendation, and crucially the *why*. Not just the conclusion. The reasoning trace. If the operator sees only *approve this action*, the operator can't make an informed call.

**KEVEN:** Escalation paths and feedback loops.

**REID:** *Escalation paths* — the agent has a confidence threshold. Above, proceed. Below, escalate. The threshold is set per workflow, sometimes per action class. High-risk actions — financial movements, regulatory filings — get a low threshold, more escalations. Treat the threshold as a tuneable parameter, not a hardcoded constant. *Feedback loops* — HITL decisions train the next iteration. Accept signals, reject-with-reason signals, feed back through prompt-tuning, threshold adjustment, fine-tuning where appropriate. The HITL data is training data for the next iteration. And all three runtimes support HITL natively. Foundry through Agent Framework callbacks. Bedrock through action-group human-approval configuration. Vertex through agent-step approval. Mechanisms differ. Capability comparable.

**KEVEN:** Gate placement. Interface design. Escalation paths. Feedback loops. Consistent across all three runtimes. Implementation details differ. The architectural pattern doesn't.

### RAG vs fine-tuning vs distillation — the domain adaptation spectrum

**REID:** Now the domain adaptation question. Because this is where I hear the most architectural confusion in the field. Sellers will say *we'll fine-tune for the client's domain.* Other sellers will say *we'll do RAG.* Both can be right. Both can be wrong.

**KEVEN:** Walk the spectrum.

**REID:** Spectrum from cheapest to most expensive. *Prompt engineering.* No model training, no retrieval. You craft the system prompt and few-shot examples. Cheapest. Instant. Iterative. Honestly — brittle for complex domains. *RAG — retrieval-augmented generation.* The model doesn't change. The model retrieves relevant context from a knowledge store at inference time, conditions on it, produces an answer grounded in that context. Cheap to operate, cheap to update — you update the knowledge store, not the model. Current — add new documents today, the agent uses them tomorrow. Works on all three clouds — Foundry plus Azure AI Search, Bedrock plus Knowledge Bases, Vertex plus Vector Search. Default starting point for almost every enterprise agentic workload.

**KEVEN:** *Fine-tuning.*

**REID:** *Fine-tuning.* The model itself is trained further on a domain-specific dataset. The base model's weights adjust. More expensive — you need a training dataset, training infrastructure, an evaluation harness. Produces durable domain knowledge baked into weights. Supports specific behaviour changes — output format consistency, style, terminology — that RAG alone struggles to enforce. Right answer when domain knowledge is stable, when behaviour changes need enforcement prompt-alone can't deliver, when cost amortises over inference volume. Wrong when domain knowledge changes weekly, or when workload volume is too low to amortise training cost.

**KEVEN:** *Distillation.*

**REID:** *Distillation.* You take a large frontier model and use it to produce training data, then train a smaller domain-specific model to imitate the larger model's behaviour on the narrow domain. The result is a smaller model that runs cheaper at inference but performs near-frontier on the domain. Expensive up front — frontier-model output costs plus training infrastructure for the smaller model. Cheap to run after that.

**KEVEN:** And the field reality.

**REID:** Field reality — *most enterprise agentic work lands on RAG plus prompt engineering.* Roughly 80 percent of workloads I've seen are well-served by that combination. *Fine-tuning is the right answer for roughly 10 percent* — domain-specific behaviour or format consistency, where training cost amortises. *Distillation is the right answer for roughly 1 percent* — usually cost-driven at very high inference volume, not quality-driven. The other 9 percent are hybrids.

**KEVEN:** And the architectural commitment.

**REID:** Start with RAG. Measure. If the workload has limitations fine-tuning addresses, fine-tune the targeted component. Don't fine-tune by default. Don't pitch fine-tuning to a client who hasn't shipped a RAG baseline yet. The fine-tuning conversation should be evidence-driven from RAG baseline data, not aspirational from day one.

**KEVEN:** Start with RAG. Measure. Add fine-tuning where evidence supports it. Consider distillation only when inference cost at scale becomes dominant. The discipline that protects the client's budget and the seller's credibility.

### A reading I want to do

**KEVEN:** I want to read briefly — paraphrased — from the kind of register Gartner, the Anthropic developer blog, and the Microsoft Build keynote retrospectives have been publishing through 2025 on where the agent-runtime layer is going.

**REID:** Go.

**KEVEN:** [reading, paraphrased from industry-analyst and vendor-keynote register on the agent-runtime productization trajectory through 2025-2026]

*"The agent-runtime layer — the orchestration plane that hosts the reasoning loop, manages tool invocations, and persists state — is commoditising rapidly. Productized runtimes on all three major hyperscalers reached general availability in the 2024 to 2025 window, and the architectural feature parity between them is narrowing every quarter. The differentiation that matters for enterprise adoption is increasingly moving up the stack into the control plane — governance, audit, identity, content safety, evaluations — and down the stack into the data foundation. Architectures that depend on the runtime layer as the seat of differentiation are buying assets that will be at parity within twelve to eighteen months. Architectures that locate differentiation in the data foundation and the productized control plane are buying assets whose half-life is materially longer."*

[pause]

**REID:** *Differentiation is moving up to the control plane and down to the data foundation.* That sentence is exactly right and it's the sentence the seller has to internalise. The agent-runtime is converging. The race for runtime-differentiation has roughly twelve to eighteen months left in it. Whichever runtime you build on today, the runtime itself is not the moat.

Sellers who pitch *our agent runtime is better than theirs* are pitching the thing that's commoditising. Sellers who pitch *our productized control plane is denser and our data foundation is more compositional* are pitching the things that hold their value. The runtime conversation is the entry point. The architecture and control-plane conversation is what wins the engagement.

**KEVEN:** Entry point versus moat. The discipline that determines whether the seller is having a feature conversation or an architectural conversation.

### One disagreement

**REID:** Pushback. The one I've been waiting for.

**KEVEN:** Go.

**REID:** *Anthropic Claude is materially better on Bedrock today.* I want to defend that. Latest Claude versions land on Bedrock first, by weeks. The Anthropic-AWS integration is the deepest model-provider-to-cloud integration in the ecosystem after the OpenAI-Microsoft one. If a client's primary requirement is the best Claude experience under support — Bedrock is the answer. Not Foundry. Not Vertex. Bedrock. The Microsoft seller has to be able to say that without flinching.

**KEVEN:** Conceded. Stated cleanly — on the Claude-experience axis specifically, Bedrock leads. Latest Claude versions land there first. The runtime is designed around the Anthropic-AWS integration. If a client says *we want Claude and we want the newest version under contract* — Bedrock is the right runtime. Microsoft does not have a like-for-like Claude-native posture today, even though Claude is increasingly available on Foundry through Microsoft's expanding model-catalog work.

**REID:** And then pivot, because there's a pivot.

**KEVEN:** Here's the pivot — and it's legitimate, not a deflection. Most enterprise agentic work doesn't depend on which model is two weeks newer. It depends on the productized control plane and the Gold-tier discipline. The control plane — the audit substrate, the governance integration, the identity continuity, the content safety, the evaluations harness — is where the architecturally important differentiation lives. The model version is an axis. The control plane is foundational. For the eighty percent case where the client wants a Claude that's *current enough* — Claude on Foundry via Microsoft's expanded integration is current enough. The cost of running on Foundry, with native Purview audit echo and native Entra identity continuity and the rest of the productized control plane, is materially lower than the cost of standing the same control plane up on Bedrock and integrating Microsoft governance back in.

**REID:** So you're saying — when model choice is the dominant axis, pick the cloud where the model is native. When the architecture is the dominant axis, the model-version delta is negotiable.

**KEVEN:** That's what I'm saying. Model selection is real. For roughly ten percent of clients, the Claude-on-Bedrock difference is the decisive factor. For the other ninety percent, the productized control plane is the decisive factor and the model-version delta is Wave-One negotiable — meaning you can ship Wave One on whichever Claude version is current on Foundry, and the productization wave will close the gap before the architectural decision needs to be revisited.

**REID:** And the seller's posture.

**KEVEN:** The seller's posture is — name the axis the client has. If model selection is the dominant axis and Claude is the model, recommend Bedrock honestly. If the architecture and control-plane density is the dominant axis, the Foundry-plus-Claude path is competitive enough. The architectural conversation transcends the model-version conversation for most enterprise workloads. But the seller has to be able to recognise the ten-percent case where it doesn't.

**REID:** Convergence. Model selection per client is legitimate. Architecture choice transcends it for most cases. The discipline is naming which case the client is in.

**KEVEN:** Convergence. Named cleanly.

### What to carry forward

**KEVEN:** Three things.

**REID:** Go.

**KEVEN:** *One — the MCP boundary discipline. Agent tool calls land on Gold views. Never on systems of record directly. Never on the data warehouse. Never on a source-system REST endpoint. Principle One in action. Every tool call, every reasoning chain, every time. The bullpen page in the cold open is what happens when the discipline is skipped on even one tool call.*

*Two — all three runtimes — Foundry, Bedrock, Vertex AI Agent Builder plus Agent Engine — support the same architectural patterns. Sequential chains, parallel decomposition, hierarchical sub-agents. HITL with gate placement, interface design, escalation thresholds, feedback loops. The runtime is increasingly commodity. The architecture and the productized control plane is where the differentiation lives. The seller who pitches the runtime as the moat is pitching the thing that's commoditising.*

*Three — model selection is real. Claude is native on Bedrock. OpenAI is native on Foundry. Gemini is native on Vertex. For roughly ten percent of clients, the model-native axis is decisive. For the other ninety percent, model selection is Wave-One negotiable and the architecture choice is foundational. Start with RAG. Measure. Add fine-tuning where the evidence supports it. Consider distillation only when inference cost at scale becomes the dominant constraint.*

**REID:** And the seller's posture from the disagreement — name the axis the client has. Model dominant means lead with the cloud where the model is native. Architecture dominant means the productized control plane and Gold-tier discipline determine the runtime. Two different right answers depending on the axis. The architectural honesty is the commercial leverage.

**KEVEN:** Said exactly that way.

**REID:** Next episode — *Governance, Identity, and Safety for Agentic AI.* Purview, DSPM for AI, Entra, IAM federation, Workload Identity Federation, the EU AI Act, NIST AI RMF, ISO 42001, Bedrock Guardrails, Vertex Safety, Azure AI Content Safety. The control-plane episode. The episode where productized-capability density genuinely matters.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn
- **Microsoft Agent Framework SDK** — open-source SDK for agent authoring; model-agnostic abstractions; tool registration; reasoning loop
- **Azure AI Foundry Agent Service** — managed agent hosting plane; persistent threads; native Purview audit echo
- **Azure AI Foundry** — model catalog, evaluations, content safety integration
- **Microsoft Industry Cloud for Manufacturing** — agent patterns and reference architectures
- **Microsoft Copilot Studio** — low-code orchestration for human-facing workflows
- **Azure AI Search** — integrated vector store and hybrid retrieval for the RAG layer

### AWS documentation
- **AWS Bedrock Agents** — [aws.amazon.com/bedrock/agents/](https://aws.amazon.com/bedrock/agents/) — managed agent service
- **AWS Bedrock Knowledge Bases** — managed RAG abstraction; chunking, embedding, indexing, retrieval
- **AWS Bedrock Action Groups** — tool-definition mechanism via OpenAPI specifications or Lambda functions
- **AWS Bedrock Guardrails** — content safety, topic restrictions, denied-topic enforcement, sensitive-information redaction
- **AWS Bedrock Flows** — visual flow-composer for agent orchestration
- **AWS Lake Formation** — fine-grained access control for Gold-tier governance

### Google Cloud documentation
- **Vertex AI Agent Builder** — low-code agent authoring tooling
- **Vertex AI Agent Engine** — managed hosting plane for production agents
- **Vertex AI Agent Garden** — agent templates and reference patterns
- **Vertex AI Model Garden** — model availability and selection
- **Google Cloud Workload Identity Federation** — cross-cloud identity for tool access without static credentials
- **BigQuery** — Gold-tier substrate for Vertex agent tool calls

### Model provider documentation
- **OpenAI** — model availability across clouds; GPT-4o, GPT-4.1, the o-series reasoning models
- **Anthropic** — Claude availability on Bedrock, Vertex AI, and via Microsoft model-catalog integration
- **Google DeepMind** — Gemini family documentation
- **Meta Llama** — open-model availability across Bedrock, Vertex Model Garden, and Foundry catalog
- **Mistral, Cohere, AI21, Stability AI** — open-model breadth on Bedrock

### Standards
- **Model Context Protocol (MCP)** — emerging open standard for agent tool definitions and runtime integration
- **OpenAPI specifications** — used for tool definitions on Bedrock action groups and elsewhere
- **The medallion architecture** — Bronze, Silver, Gold as the substrate the agent runtime sits on top of

### From the Acceleration Framework
- **Episode 1** — The Agentic Stack and the Five Principles
- **Episode 2** — Data Foundation and the No-Replication Principle
- **Trilogy Services Ep 4** — the MCP boundary discipline at the agent-runtime layer

---

**End of Episode 03 · Agent Runtime — Talking to Gold, Not SORs**
*≈ 5,800 words · target 30 minutes at conversational pace*
