# Episode 04 · Service and Agent Layers

**Source:** *Professional APEX-M Deployment Guide* — Part III (What Is a Deployable Service · Service Composition Atop Platform · Multi-Service per Tenant) + Part IV (Agent Anatomy and the Image Pipeline · Agent Reuse Across Services · Deploying Microsoft Agent Framework Agents · Deploying Responsible AI Controls · Versioning and Compatibility)
**Run time:** ≈ 25–30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: a quiet office, somebody clicking through a deployment dashboard]

**SAM:** I want to start with a question I got asked about six months into running my first APEX tenant. Engagement lead came over to my desk. She said — *"Sam, we've got the second Service approved. We're adding warranty intake. When can we start the build?"*

[pause]

**KEVEN:** And your answer was —

**SAM:** My answer was — *"We can start *today*. We're not doing a build. We're doing a* deployment*."* And the engagement lead, who is excellent, looked at me a little blankly, because in her experience, *adding a new capability to a tenant* meant a project. Sprints. Architecture review. Build. Test. UAT. Three months at minimum.

**KEVEN:** Yep.

**SAM:** And the thing she had to internalise — the thing the *whole* framework is structured around — is that *Service deployment is fundamentally different from Service development.* When the framework's been built well, *deploying a new Service into an existing tenant takes days, not months.* Because you're not building. You're parameterising productized assets and dropping them onto a platform that's already there.

**KEVEN:** And that's the entire architectural payoff of the three-layer cake.

**SAM:** Yes.

**KEVEN:** I'm Keven Markham.

**SAM:** I'm Sam. APEX Deployment Podcast. Episode Four. Service and Agent Layers.

---

## The conversation

### What "deployable Service" actually means

**KEVEN:** OK. So *deployable Service.* That's actually a phrase worth pausing on, because I think it captures something the framework is doing right.

**SAM:** Talk through it.

**KEVEN:** In most consulting engagements, when you hear *"Service,"* it means *a thing the consulting firm is building.* It's bespoke. It's per-client. It's a delivery artefact.

In APEX, *"Service"* means *a thing in the catalog.* It's pre-defined. It's reusable. It's the unit of value-delivery the framework has standardised on. The 38 Services in the Sellers Guide — those are *real artefacts,* not categories.

**SAM:** And the *deployable* qualifier means —

**KEVEN:** *Deployable* means — it has Bicep, it has an agent composition, it has a Gold-mart shape, it has a KPI envelope, it has a manifest declaring what it consumes and what it emits. *Everything required to put it into a tenant exists already.* You don't design it. You configure it.

**SAM:** And in operational terms —

**KEVEN:** Deploying a catalogued Service into an existing tenant is — pick the Service from the catalog, fill in the per-tenant parameters, run the Bicep, validate. The Bicep deploys the Service's Gold mart, deploys the Service's MCP server, deploys the agent images at the right version, wires the audit emission. Three to five days, if the platform layer is clean.

**SAM:** And if the platform layer is dirty —

**KEVEN:** If the platform layer is dirty, you're not deploying a Service — you're remediating the platform. Don't confuse those motions.

### The Service Bicep — and the parameter discipline

**SAM:** OK so let me dig into the Bicep side of this, because this is where I think a lot of teams get confused.

**KEVEN:** Yeah.

**SAM:** The Service's Bicep — when you actually look at it — is *thin.* A few hundred lines, sometimes less. Because the heavy lifting is in the platform Bicep, and the Service Bicep is just *adding the Service-specific resources on top.*

**KEVEN:** And the thinness is the point.

**SAM:** The thinness is the point. If your Service Bicep is two thousand lines, you've duplicated platform-layer stuff into the Service layer. Which means when the platform Bicep evolves, your Service Bicep is out of sync.

**KEVEN:** What's actually *in* a thin Service Bicep?

**SAM:** Four things, roughly.

One — the Service's Gold mart. The Fabric lakehouse, the materialised views, the tables. Created with the platform's Fabric workspace as a parent — so the Service's Gold mart inherits the platform's identity model, the platform's network rules, the platform's audit feed.

Two — the MCP server hosting. Typically a Container Apps revision or an Azure Function. Bound to the platform's managed identity for the Service.

Three — the agent compositions for the Service. Which agent images compose into this Service. Their versions, by SHA digest. Their MCP-tool registrations.

Four — the Service-specific Purview policy overlay. Sensitivity labels, DLP rules, retention specific to this Service that ride on top of the platform's defaults.

**KEVEN:** And what's deliberately *not* in the Service Bicep —

**SAM:** Anything platform-layer. Identity definitions. Workspace creation. Capacity provisioning. Sentinel rules. Network. All of that is platform. The Service Bicep *consumes* the platform's outputs as inputs.

**KEVEN:** And the engineering rule that flows from this —

**SAM:** Never duplicate platform resources into a Service. If your Service Bicep is creating something that already exists at the platform layer, you've broken the model. Find the platform's output for that thing and reference it.

### Multi-Service per tenant — the moment the architecture earns its money

**KEVEN:** OK. Multi-Service per tenant. This is the moment the architecture earns its money. Let me set this up.

**SAM:** Go.

**KEVEN:** Single-Service tenant — that's the MVP. Easy. You've stood up a platform layer. You've dropped one Service onto it. Everything works.

Now your second Service is approved. You're not standing up a new tenant. You're adding to the existing one. *Two* Services running on the *same* platform layer. They share the identity model, the audit floor, the network. They have *separate* Gold marts, *separate* MCP servers, *separate* agent compositions.

**SAM:** Right.

**KEVEN:** And the temptation — the temptation that has to be resisted — is *to let the two Services share things they shouldn't share.*

**SAM:** What things?

**KEVEN:** Gold marts especially. Some bright engineer says — *"hey, both Services need the customer entity. Let's put the customer Gold mart in a shared place."* And they create a *cross-Service* shared Gold mart. Which sounds great. Until Service A wants to change the customer Gold mart shape for its own reasons. Now Service A's change blocks Service B's progress. Two Services that were independent are now coupled.

**SAM:** And the framework's position is —

**KEVEN:** Don't share Gold marts. Both Services build their own Gold marts from the *same Silver canonical.* The canonical is shared. The marts aren't.

**SAM:** And the duplication cost is —

**KEVEN:** Small. The Silver canonical is the work. Materialising it into two Gold shapes is fast. The duplication is *cheap* and the independence is *valuable.*

**SAM:** And the same goes for MCP servers.

**KEVEN:** Same goes for MCP servers. Each Service has its own. Don't share. Don't multiplex. The MCP server is part of the Service's deployable unit.

### The agent layer — images, registries, SHA digests

**SAM:** OK. Down to the agent layer. The deepest layer. The layer that, when done well, is also boring.

**KEVEN:** Talk me through it.

**SAM:** The framework's pattern is — agents are *immutable container images.* Built in a Deloitte authoring registry. Signed with cosign. Mirrored to the client's tenant registry. Pulled at runtime by *SHA digest,* not by tag.

**KEVEN:** Why SHA digest, not tag?

**SAM:** Because tags are mutable. The tag `1.4.0` today could point to a different image tomorrow if somebody re-pushes. SHA digest is the actual content. It can't change. If the agent runtime is bound to a SHA, the agent is the agent — forever.

**KEVEN:** And the operational reason this matters —

**SAM:** Reproducibility of incidents. If something goes wrong with the agent at 2 AM, you want to know *exactly* what code ran. The SHA tells you. The tag would have told you *one of the things that could have been running.* Big difference.

**KEVEN:** And the agent base image — let me read a quick passage from the guide because this is the bit I think is most architecturally underrated.

**SAM:** Go.

**KEVEN:** [reading]

*"Every agent in APEX is built from the same base image. The base image carries the Microsoft Agent Framework runtime, the MCP client libraries, the audit emission helpers, the secret-resolution helper, the observability hooks. Individual agent images add only the agent's instructions, the agent's tool registrations, and the agent's persona. The base image is the engineering investment that compounds across the catalog."*

[pause]

**SAM:** That last sentence. *"The engineering investment that compounds across the catalog."* That's the deepest insight.

**KEVEN:** Yeah. Because — every time the framework improves the base image — every time audit emission gets sharper, every time secret resolution gets faster, every time observability gets better — *all 38 cataloged Services* get those improvements simultaneously. There's no per-Service migration. You bump the base. You rebuild the agent images on the new base. The catalog moves.

**SAM:** And this is part of why agent versioning is so important. Because the version isn't just the agent's persona — it's *the agent's persona on a specific base version.*

**KEVEN:** Right.

### Agent reuse across Services

**KEVEN:** Let me dig into agent reuse. Because this is the architectural payoff for the layering.

**SAM:** Go.

**KEVEN:** *The Analyst.* This is an agent in the cataloged MVP. It analyses data, identifies patterns, drafts recommendations. The MVP Service — pricing and revenue — uses it. But *The Analyst* is *useful* in more than that one Service.

**SAM:** Sure.

**KEVEN:** A different Service — say loyalty churn — also wants an analytical agent that does pattern-finding. *Do you build a new agent for that Service?*

**SAM:** No. You reuse *The Analyst.* Same image. Same SHA. Different tool registrations and different persona context, but the same underlying agent.

**KEVEN:** And the architectural payoff is —

**SAM:** One image, two Services. Maintained once. Improved once. Audited consistently. The agent layer is the *most* reusable layer. The reuse compounds value across the catalog.

**KEVEN:** And the rule for *when* an agent is reusable —

**SAM:** When its purpose is *abstract enough* to apply to multiple Services. *The Analyst* is reusable because pattern-finding is a generic capability. *The Briefer* is reusable because summarising-for-an-executive is a generic capability. *The Operations Lead* is more debatable because operations-specific knowledge varies.

**KEVEN:** Right.

**SAM:** And when an agent is *not* reusable — when it really is Service-specific — the framework's position is *that's fine.* Don't force reuse. But default to reuse. Build the *case* for Service-specific.

### Responsible AI controls — the part I think gets underdone

**SAM:** Let me bring up RAI controls. Because I think this is a thing teams under-implement.

**KEVEN:** Yeah.

**SAM:** RAI in APEX is — Azure AI Content Safety in the pipeline. Custom blocklists per Practice. Tool-approval flows for state-changing actions. Audit emission for refusals. *And* — this is the part — *per-Service customisation overlays.*

**KEVEN:** Talk through the overlays.

**SAM:** The framework ships *baseline* RAI controls. Standard checks. Standard blocklist patterns. The base agent image has them wired in. *Every* agent runs them.

But each Practice has its own additions. HLS has clinical-advice refusal patterns. Financial Services has investment-advice refusal patterns. Government has classified-data refusal patterns. Those are *overlays* — they layer on top of the baseline, they don't replace it.

**KEVEN:** And the failure mode if you skip the overlays —

**SAM:** You ship an agent that doesn't refuse the things its industry requires it to refuse. The CCO finds out at the worst possible time.

**KEVEN:** And the engineering rule —

**SAM:** Every Service declares its RAI overlay in the Service manifest. Before deployment, the Service manifest is reviewed by the client's RAI lead — or whoever owns Responsible AI on the client side. The deployment runner enforces the overlay being applied.

**KEVEN:** And the framework's tooling for this —

**SAM:** The pre-deployment security gate — we'll cover that in Episode Five — checks for RAI overlay presence. If the manifest doesn't declare one, the gate fails. The Service doesn't deploy.

### Versioning — the discipline of compatibility

**KEVEN:** OK. Last big thing for this episode. Versioning. And compatibility. Because this is where the three-layer cake either works or breaks.

**SAM:** Yeah.

**KEVEN:** The framework uses semver-like versioning. Platform v0.1.0. Service v1.2.0. Agent v1.4.0. Independent. They compose.

**SAM:** And the compatibility rules —

**KEVEN:** Two rules.

Rule one — *Service version declares a compatible platform version range.* Service v1.2.0 might declare "compatible with platform v0.1.0 through v0.3.x." The deployment runner verifies. If incompatible, deployment is refused.

Rule two — *Service version declares compatible agent image versions.* Service v1.2.0 might declare "agent The Analyst v1.3.0 through v1.4.x." Again, deployment runner verifies. Again, refused on incompatibility.

**SAM:** And the why —

**KEVEN:** The why is — *upgrades are independent.* Platform can be upgraded without re-deploying every Service, as long as the Services declare compatibility with the new platform version. Agent images can be upgraded without re-deploying every Service that uses them.

**SAM:** And the failure mode you avoid —

**KEVEN:** "We can't upgrade the platform because Service X breaks." That's the failure mode. With versioning discipline, you know *exactly* which Services will break on a platform upgrade. You upgrade them first. Then upgrade the platform. No surprise breakage.

### Where Sam and Keven disagree

**SAM:** OK. Pushback time.

**KEVEN:** Go.

**SAM:** Agent reuse. I want to push on the *default to reuse* posture. Because I think in delivery — especially when a team is under pressure — *default to reuse* can lead to a thing I'd call *agent stretching.*

**KEVEN:** Stretching?

**SAM:** Yeah. Where the team takes a reusable agent that *almost* fits a new Service, and they *almost-fit it* by piling on persona context and tool registrations. And the agent that started as *The Analyst* ends up doing five different things across five Services — but its prompt has become a mess of conditional context, its tools have proliferated, its behaviour is harder to reason about.

**KEVEN:** Right.

**SAM:** And the *correct* answer for that fifth Service might have been — *fork the agent.* Build a Service-specific variant. Even if it costs more engineering. Because the cost of keeping the reusable agent maintainable as it serves five different purposes is *higher* than the cost of building a separate one for the fifth.

**KEVEN:** I think you're describing a real anti-pattern. Where I'd push back is — *don't reflexively fork.* The fork-vs-reuse decision should be made consciously, with the cost-of-maintenance weighed against the cost-of-divergence.

**SAM:** Agree.

**KEVEN:** And the *signal* that it's time to fork —

**SAM:** The signal is — *when the agent's prompt has more than two distinct persona-context branches, fork.* Two is the maximum. Three branches and it's three different agents pretending to be one.

**KEVEN:** That's a good rule of thumb.

**SAM:** I'd put that in the runbook for every engagement. *"Two persona-context branches max per agent. If you're tempted to add a third, fork."*

### What stays with me

**KEVEN:** Synthesis.

**SAM:** Yeah.

**KEVEN:** Three things.

One — *Service deployment is fundamentally different from Service development.* Deploying a catalogued Service to an existing tenant is days, not months. Because you're configuring, not building.

Two — *Service Bicep is thin. Agent images are immutable. Both lean on the platform.* The architectural payoff of the layering is that adds to the tenant become straightforward.

Three — *reuse compounds value. Forking is sometimes correct. The decision is conscious, not reflexive.* Two persona-context branches max per agent.

**SAM:** And I'd add — *RAI overlays are not optional.* Every Service declares one. Every overlay is reviewed by the client's RAI lead. The deployment gate enforces. The CCO never asks *"how do you handle the industry-specific refusal patterns,"* because you've already shown them the overlay before they had to ask.

**KEVEN:** Yep.

---

## What to read next

**KEVEN:** Read the chapters on the Service Bicep structure and the agent image pipeline. They're shorter chapters than they look. The Bicep one is the operational reference; the image pipeline one is the build-and-trust reference.

**SAM:** And read the versioning chapter twice. It's small but every sentence matters. Compatibility ranges. SHA-digest pinning. Independent upgrade paths. The mechanics of *not* breaking production with an upgrade.

**KEVEN:** Next episode — *The Motion.* Adding a Service to a live tenant. Agent upgrades across clients. The pre-deployment security gate. Rollback. DR. The rhythm of ops.

**SAM:** See you there.

[outro]

---

**End of Episode 04 · Service and Agent Layers**
*≈ 5,100 words*
