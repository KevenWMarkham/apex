# Episode 04 · The Agent and Its Tools

**Arc:** Foundation (4 of 4 — final foundation episode before business needs) · **Builds on:** Eps 1-3 (third era, three needs of agentic data, medallion) · **Foundation laid:** MCP boundary · Agent Framework · audit row · how the agent reaches Gold without breaking governance
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: a conversation winding down, somebody packing a laptop]

**KEVEN:** I want to start with a moment from a board meeting. Not mine — a client's. About a year ago. The client's CCO — Chief Compliance Officer — was in front of her board, presenting on the upcoming AI deployment. The board chair, who was a former bank CEO, asked her one question. And it was the only question that mattered.

[pause]

**MORGAN:** What was it?

**KEVEN:** He said — *"When this agent makes a decision that affects a customer, can you walk me back from the decision to every piece of data the agent saw before making it? Every row, every record, every classification, every policy that applied? Can you walk me back, on a single screen, in less than five minutes?"*

[pause]

**KEVEN:** And the CCO — who'd been working on the project for nine months — looked across the table at the engagement partner. And the engagement partner said — *"Yes. We can do that. Let me show you."*

And he showed them. On screen. Live. The audit chain.

The board chair sat back and said, *"That's the difference between this project and the three we've cancelled."*

**MORGAN:** That's the moment.

**KEVEN:** That's the moment the agent layer earns its keep. And it's not about the model. It's not about the prompt. It's about the *boundary* between the agent and the data — and how that boundary is *governed.* That's what this episode is about. The last foundation episode before we start with business needs.

I'm Keven Markham.

**MORGAN:** I'm Morgan. Services Podcast Episode Four. *The Agent and Its Tools.*

---

## The conversation

### Picking up

**KEVEN:** Anchor where we are. Episode One — the bottleneck moved to *governance of agents in production.* Episode Two — agents need a different shape of data than the warehouse provides. Episode Three — that shape is the medallion. Bronze absorbs, Silver anchors canonical, Gold shapes per-Service.

This episode — *how the agent actually reads from that medallion, and how every read becomes audit-traceable.* The architectural commitment that makes the board-chair conversation in the cold open possible.

**MORGAN:** And the central concept —

**KEVEN:** *The agent doesn't open a database connection.* That's the central commitment. Let me develop that fully.

### Why the agent doesn't talk to data directly

**KEVEN:** Take a step back to first principles. An agent — in the modern sense — is a large language model orchestrating a sequence of steps. It reasons. It needs context. It needs to act. Naively, you might think — *give the agent a database connection string. Let it write SQL. Let it query the warehouse.*

That's how a lot of early experimental agents were built in 2023, 2024. It works for demos. It does not work for production. Here's why.

**MORGAN:** Three reasons, in order of severity?

**KEVEN:** Three reasons.

One — *security and identity.* If the agent has a database connection, the agent has *whatever permissions that connection has.* Which means, to support the diverse questions the agent might ask, you grant the agent broad read access. Which means, *if the agent malfunctions or is compromised, the blast radius is the breadth of that access.* The connection is the leak.

The architecturally cleaner pattern — the agent has no connection. The agent has a list of *tools* it can call. Each tool is *narrow* — it reads only what's needed to answer one specific kind of question. The tool runs under its own identity, with its own narrow permissions. Even if the agent is compromised, the blast radius is *one tool at a time*, with the tool's own permission scope.

**MORGAN:** Defence in depth.

**KEVEN:** Defence in depth. Two — *semantic stability.* If the agent has a connection, the agent can write arbitrary SQL. Which means the agent can — and will — *invent column references that don't exist.* Hallucinate field names. Misjoin tables. Reason over data that doesn't mean what the agent thinks it means.

The architecturally cleaner pattern — the tool exposes a *narrow contract.* "Given a customer ID, return the customer's recent purchase pattern." Not "execute this SQL." The tool defines the question the agent can ask and the shape of the answer. The agent can't ask for things outside the contract.

Three — *audit.* If the agent has a connection, the database sees a sequence of queries. *Reconstructing* which queries came from which agent invocation, in which conversation, on behalf of which user — is forensics work. After-the-fact. Tedious. Often impossible to do reliably.

The architecturally cleaner pattern — every tool call is *natively* logged with the invocation ID, the user identity, the input parameters, the output, the timestamp. The audit row emits at the boundary. Not reconstructed. Native.

**MORGAN:** And the architectural answer for all three —

**KEVEN:** *Model Context Protocol.* MCP. The boundary layer between the agent and the data.

### MCP · the wire protocol of the agent

**KEVEN:** MCP is — at its core — a *protocol.* It's how the agent talks to its tools. Wire format. Defines how a tool is described. How the agent invokes it. How parameters are passed. How responses come back. How streaming and asynchronous flows work.

The reason MCP matters — and the reason Microsoft and Anthropic and a growing list of others have adopted it — is that it *standardises* the boundary. Before MCP, every framework had its own tool-calling convention. The OpenAI function-calling format was one. LangChain had another. Semantic Kernel had another. Anthropic's tool-use format was another. They were close but not identical, and shared tools across frameworks were difficult.

MCP is the convergence. *Same protocol across frameworks.* Same protocol across model providers. A tool you build in MCP is consumable by any MCP-aware agent framework. That's leverage.

**MORGAN:** And in the APEX architecture, MCP is the boundary that lives between —

**KEVEN:** Between the agent — running in the Microsoft Agent Framework, hosted on Azure AI Foundry Agent Service — and the Gold marts the tool reads from. The agent never sees Gold. The tool sees Gold. The agent sees the tool's output.

That boundary is the *one place* where the agent-to-data interaction is governed. Identity is enforced at the boundary. Audit is emitted at the boundary. Policy is applied at the boundary.

**MORGAN:** Concretely — where does the MCP server live in Azure?

**KEVEN:** Typically — Azure Container Apps, with a managed identity bound to the Service's Gold lakehouse. Sometimes — for very lightweight per-tool servers — Azure Functions. For the Microsoft-hosted Real-Time Intelligence MCP scenario, Microsoft hosts the server inside Fabric. Each Service has its own MCP server. Not shared. Not multiplexed. Service-isolated.

### The tools themselves · the design discipline

**KEVEN:** OK. Let me develop *the tools.* Because the tools are where the framework's architectural opinions become concrete.

The framework names five tool design principles. I want to walk each one slowly because they're the most-violated principles in early-engagement agent design.

**MORGAN:** Take your time.

**KEVEN:** Principle one — *one tool, one purpose.* Don't build a `do_anything()` tool. Build six small, focused tools. The agent picks which to call. The agent's reasoning is *clearer* when its tool set is *narrower per tool.* Counter-intuitive at first; obvious once you've debugged an over-broad tool.

Principle two — *return structured data, not free text.* The tool's output is a typed object. JSON. With declared fields, declared types, declared constraints. Not a paragraph. Not a markdown block. The agent reasons over fields. Free-text returns destroy reasoning fidelity.

Principle three — *include source metadata in every return.* Freshness timestamp. Silver-canonical version. Gold-mart version. The agent's eventual output carries lineage all the way back through the tool returns to the source data. *Without source metadata in the tool return, lineage breaks at the agent boundary.*

Principle four — *narrow the input contract.* If the agent only needs to query by customer ID, the tool accepts customer ID. Not customer ID *and* a SQL where-clause. Not customer ID *and* an arbitrary filter expression. Narrow. Always.

Principle five — *make tools read-only by default.* Write tools are a separate category — they require the Foundry tool-approval flow, they require human-in-the-loop approval before the agent's call executes. Most APEX tools are read-only. The agent reads, reasons, presents recommendations to humans who decide. Write-tool patterns are deliberate; not default.

**MORGAN:** And the failure mode of violating these principles —

**KEVEN:** Principle one violated — agent reasoning becomes opaque. Principle two violated — agent output becomes unstructured and downstream integration breaks. Principle three violated — lineage breaks, audit is incomplete. Principle four violated — agent can ask for things it shouldn't, security collapses. Principle five violated — agent takes actions humans didn't sanction.

Each principle is load-bearing.

### The agent's audit row

**KEVEN:** OK. The audit row. The mechanism that made the board-chair conversation in the cold open possible.

Every agent invocation produces an *audit row.* Structured. Hash-chained. Persisted to OneLake. Echoed to Purview. The row contains —

*Who* — the persona, the user identity, the workload identity.

*What* — the agent that ran. The version. The model that backed it. The Service the agent was operating within.

*Inputs* — the user's query or the trigger context. The data the agent received.

*Tool calls* — each MCP tool the agent invoked. Tool name. Parameters. Output. Latency.

*Outputs* — what the agent produced. Recommendations. Decisions. References.

*Policy context* — what Purview classifications applied. What RAI overlay was in effect. What HITL gate fired.

*Lineage* — Silver canonical versions. Gold mart versions. Source-data timestamps.

*Timestamp* — when, to the millisecond.

*Hash link* — the cryptographic hash linking to the prior row in the chain.

**MORGAN:** And the hash chain matters because —

**KEVEN:** Because it makes the audit *tamper-evident.* You can't retroactively insert a row without breaking the chain. You can't delete a row without leaving a hash gap. The chain is the *trust mechanism.* Without it, the audit log is just a log — vulnerable to tampering, vulnerable to gaps, vulnerable to challenge.

With the hash chain, the auditor can verify integrity *independently.* Read the chain. Verify the hashes. If the chain validates, the trail is intact. If it doesn't, the auditor sees exactly where the discrepancy is.

**MORGAN:** And the auditor accesses this through —

**KEVEN:** Through Purview. Native. The auditor — or the auditor's delegate — gets a Purview audit-reader role bound to their *own* Entra credentials. They query Purview directly. They see the chain. *Their access is not mediated by Deloitte.* They use their own credentials. They read the data themselves. The framework's posture is — Purview is the audit interface; we don't build a custom export.

That's why the board chair could see the chain in five minutes in the cold open. Because the chain existed natively, and the screen the engagement partner showed was *Purview*, not a custom report.

### The Microsoft Agent Framework · the SDK

**MORGAN:** Last big topic for this episode. The Microsoft Agent Framework.

**KEVEN:** Right. Let me set up the layering one more time because the naming gets confusing.

*Azure OpenAI* — the underlying model API. GPT-4o, GPT-4.1, o-series. The reasoning substrate.

*Azure AI Foundry Agent Service* — the runtime *service* that hosts the agent in production. Manages runs, manages tool-approval flows, emits traces, handles versioning and traffic-split.

*Microsoft Agent Framework* — the *SDK*. The Python and .NET libraries an engineer writes against to define an agent. The framework's primitives are Agent, Tool, Run. The Agent declares its instructions, model, persona, tool catalog. The Tool wraps an MCP endpoint. The Run is the bounded execution unit — input to output, with audit emission throughout.

**MORGAN:** And the relationship — same agent code, same framework, runs locally on a developer's laptop or in production on Foundry.

**KEVEN:** Right. That's the *deployment-substrate-agnostic* property the framework guarantees. The engineer writes the agent in Agent Framework. Same code runs against a local Foundry-equivalent during development. Same code runs against production Foundry Agent Service when deployed. The runtime substrate is configured at the edges — environment variables, identity bindings, MCP endpoints — not in the agent code itself.

That property is the developer-velocity property. New engineers can be productive on day one because the substrate doesn't change between dev and prod.

### A reading I want to do

**MORGAN:** I want to read something. From the Microsoft Agent Framework documentation. Specifically the framing of why the framework exists.

**KEVEN:** Go.

**MORGAN:** [reading]

*"Agent Framework is built around three primitives: Agent, Tool, Run. The Agent defines what reasoning is to happen. The Tool defines what the agent may reach for. The Run defines what bounds the execution. These three together give engineering teams a contract — the agent is whatever the Agent declares it to be, the agent may only reach for what the Tools allow, the agent's execution is bounded by what the Run permits. Outside these three, there are no implicit privileges."*

[pause]

**KEVEN:** That last sentence. *No implicit privileges.* That's the security property.

**MORGAN:** That's the security property. And it's the property that makes the boundary verifiable. The framework's commitments are *explicit*, not implicit.

### One disagreement

**KEVEN:** Disagreement time.

**MORGAN:** OK. Let me push on the *one tool, one purpose* principle. Because I think in practice there's a tension.

**KEVEN:** Go.

**MORGAN:** The principle pushes engineers toward many small tools. A Service might have ten, twelve, fifteen MCP tools. Each narrow. Each focused. *Beautiful in theory.*

In delivery — the engineers I work with say — *managing fifteen narrow tools is operational overhead.* Each one is a tested, versioned, deployed unit. The CI/CD pipeline grows. The contract-test harness grows. The on-call runbook grows.

I think there's a sweet spot around six to eight tools per Service. More than that, the operational tax becomes painful. The principle should be *one tool, one purpose — but not more than eight tools per Service.* If you find yourself needing the ninth tool, look hard at whether two of them could merge without violating the purpose-clarity principle.

**KEVEN:** I think that's a reasonable engineering refinement. The principle as stated in the guide is *purity-leaning.* Your refinement is *operationality-leaning.* I'd put them together as — *purity by default, with operational pressure to merge when you cross the eight-tool threshold.*

**MORGAN:** Yes.

### What to carry forward · this is the last foundation episode

**KEVEN:** OK. This is the *last foundation episode.* Episode Five opens with the retail margin squeeze and we never come back to the abstract architecture conversation. So I want to land the four foundation episodes in one paragraph.

**MORGAN:** Land it.

**KEVEN:** *We're in the third era of enterprise data — the agentic era. The new bottleneck is governance of agents in production. Agents need data shaped differently than warehouses provide — stable semantic meaning queryable in real time, governed and lineage-traceable, narrow and decision-shaped. The framework's answer is the medallion architecture: Bronze absorbs reality, Silver anchors canonical meaning, Gold shapes per-Service decisions. The agent reaches Gold through the MCP boundary — narrow tools, structured returns, source metadata, read-only by default. Every agent invocation produces a hash-chained audit row. Purview is the audit interface. The Microsoft Agent Framework is the SDK; Foundry Agent Service is the runtime; MCP is the wire protocol between the agent and its data.*

That's the foundation. Every business-need episode from here builds on it.

**MORGAN:** And what listeners should carry forward —

**KEVEN:** Three things.

One — *the agent doesn't open a database connection. Ever. The MCP boundary is the architectural commitment.*

Two — *the audit row is native, not retrofitted. Hash-chained. Purview is the auditor's interface.*

Three — *Agent Framework is the SDK; Foundry is the runtime; MCP is the protocol. Same agent code on laptop and in production — substrate-agnostic.*

**MORGAN:** Next episode — we shift. *The Retail Margin Squeeze.* Episode Five opens with the question — how did retail margins get to where they are, and what does the loyalty-churn Service do about it. Business need first. Architecture in support.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn

- **Model Context Protocol (MCP) — Introduction** · [modelcontextprotocol.io](https://modelcontextprotocol.io) — the spec, hosted by the MCP community
- **Microsoft Agent Framework — Quickstart** · [Microsoft Learn](https://learn.microsoft.com/agent-framework/quickstart/)
- **Microsoft Agent Framework — Agent, Tool, Run primitives** · [Microsoft Learn](https://learn.microsoft.com/agent-framework/concepts/)
- **Azure AI Foundry — Agent Service** · [Microsoft Learn](https://learn.microsoft.com/azure/ai-foundry/agents/)
- **Microsoft Purview — Audit and lineage for AI workloads** · [Microsoft Learn](https://learn.microsoft.com/purview/audit-search)

### Microsoft Tech Community blogs

- **"Why we adopted MCP"** · Microsoft AI Blog
- **"Designing MCP tools — the five principles in practice"** · Azure AI Blog
- **"Hash-chained audit for agentic AI"** · Microsoft Security Blog

### Architecture references

- **Azure Architecture Center — Agentic AI baseline** · Microsoft Learn
- **Microsoft Agent Framework — Sample agents on GitHub** · [github.com/microsoft/agent-framework](https://github.com/microsoft/) (search for current sample repos)
- **MCP server hosting patterns on Azure** · Microsoft Tech Community

### Industry context

- *"Tool-using agents — the structured-output revolution"* · Sequoia Capital, 2024
- *"The audit problem in agentic AI"* · MIT Technology Review, 2025
- *"Defence in depth for autonomous agents"* · ACM Queue
- **NIST AI Risk Management Framework — playbook for AI auditability** · [nist.gov](https://www.nist.gov/itl/ai-risk-management-framework)

### From the APEX Trilogy

- **Services Guide — *MCP and the Service Tool Catalog* chapter** — the implementation detail this episode summarised
- **Services Guide — *Agent MCP Tool Surface* chapter** — the five tool-design principles in depth
- **Services Guide — *The APEX Audit Row* section** — the audit-row schema this episode introduced
- **Deployment Guide — *Identity, Secrets, and Audit Trust* chapter** — the production-operations side of the audit posture

---

**End of Episode 04 · The Agent and Its Tools**
**End of Foundation arc — next episode starts the Business-need arc**
*≈ 5,600 words · target 30 minutes at conversational pace*
