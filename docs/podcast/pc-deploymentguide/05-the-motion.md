# Episode 05 · The Motion

**Source:** *Professional APEX-M Deployment Guide* — Part V (Networking & Observability Deep Dive · Day-Zero Tenant Onboarding · Pre-deployment Security Gate · Adding a Service to a Tenant · Agent Upgrades Across Clients · Rollback, DR, Reusable-Asset Discipline)
**Run time:** ≈ 25–30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: a Slack DM notification, then typing]

**KEVEN:** I want to start with a message I got at 4:47 PM on a Thursday from an engagement lead I work with. The message said — *"Keven, we're rolling out the agent v1.5.0 across all six tenants tonight. First tenant goes at 9 PM. If anything looks weird in the LEDGER feeds, ping me."*

[pause]

**SAM:** And your reaction was —

**KEVEN:** My reaction was — *"OK. Good. You've got it set up the right way."*

Because the *whole sentence* — *agent v1.5.0 across all six tenants tonight* — is a sentence that *could not have existed* eighteen months earlier in our practice. Six tenants? Coordinated upgrade? Tonight? With the engagement lead confident enough to ping me with a *plan,* not a *question*?

That's what the deployment motion looks like when it's mature.

**SAM:** Yep.

**KEVEN:** And the way you get there is — the deployment motion has *patterns.* Adding a Service. Upgrading an agent across tenants. Running the pre-deployment security gate. Rolling back. The DR exercise. Those patterns aren't decorations. They're the *rhythm* of how the practice actually runs.

**SAM:** I'm Sam.

**KEVEN:** I'm Keven Markham. APEX Deployment Podcast. Episode Five. The Motion.

---

## The conversation

### What "the motion" means

**KEVEN:** OK. Term first. *The motion.* It's a phrase the deployment guide uses repeatedly. Let me explain what I think it means.

**SAM:** Go.

**KEVEN:** Most consulting frameworks describe *delivery* but not *operations.* They say — *"design the thing, build the thing, deploy the thing."* And then the thing exists. And operations is somebody else's problem.

APEX is different because operations *isn't* somebody else's problem. The same framework that designs and deploys the thing also runs it. Adds to it. Upgrades it. Rolls it back when needed. The framework doesn't *end* at first deployment. The framework continues.

*The motion* is the framework's language for that continuation. The repeated patterns that happen *after* a tenant is live and *during* the years it runs. Adding a Service. Upgrading. Rolling back. Each is a *motion* — a well-defined, repeatable, low-surprise activity.

**SAM:** And the value of having them defined —

**KEVEN:** Two values. One — *predictability.* A team that's never added a Service to an existing tenant before can read the motion guide and know what's going to happen. There are no surprises if the motion is followed.

Two — *teachability.* New engineers can be brought up to speed on the motions in a sprint. They don't need three years of pattern-matching to know how the framework operates.

**SAM:** And the failure mode if you don't define them —

**KEVEN:** Every engagement does its own thing. The first one figures it out painfully. The fifth one figures it out painfully again, because nobody wrote down what the first one learned. The framework's documented motions are the *write-down*.

### The pre-deployment security gate

**SAM:** OK. Let's start with what I think is the *most* underrated motion. The pre-deployment security gate.

**KEVEN:** Yeah.

**SAM:** The framework's position is — before any Service deploys into any tenant, it passes through a structured security review. Pre-deployment. Not post-deployment audit. *Pre.* The gate is a *checklist plus a sign-off*. The checklist is concrete. The sign-off is from a named individual.

**KEVEN:** Walk me through what's on the checklist.

**SAM:** Roughly eight things.

One — *Manifest review.* The Service's manifest is read. Consumed canonical families. MCP tools. KPI commitments. Persona declarations. RAI overlay. Everything declared is verified.

Two — *Image signature verification.* The agent images this Service composes are verified cosign-signed by the Deloitte authoring registry. No unsigned images. No images from unknown registries. Mirrored to the client tenant registry, verified there too.

Three — *Identity verification.* The workload identities the Service will use are confirmed to exist at the platform layer, with the correct role assignments, with no over-broad permissions.

Four — *Network path validation.* The MCP server, the Gold mart, the agent runtime — all on permitted networks. No back-channels. No outbound traffic to anything not explicitly allowlisted.

Five — *Audit emission test.* A dry run of the agent — using test data — confirms audit rows emit to Purview correctly. Hash chain extends. Sensitivity labels propagate.

Six — *Conditional access verification.* The Service's deployment runner has CA-policy compatibility verified for the deploy window. No surprises like our Episode Three Purview story.

Seven — *Secrets check.* Every secret the Service needs is in Key Vault. Rotation cadence agreed. Consumer notification path tested.

Eight — *RAI overlay verification.* The Service's RAI overlay is loaded, the agent refuses test inputs that should be refused, the audit row for refusals lands correctly.

**KEVEN:** Eight items. Pre-deployment.

**SAM:** Eight items, pre-deployment.

**KEVEN:** And the sign-off is —

**SAM:** A named individual — usually the client's CCO or their delegate — signs off that the gate has passed. Their signature is on the audit record. *Their* skin in the game.

**KEVEN:** And the rule the framework is explicit about —

**SAM:** *No deployment without the gate.* No exceptions. No "we'll catch it in UAT." No "the CCO is on holiday, we'll backfill." If the gate hasn't run, the deployment doesn't happen.

**KEVEN:** And the operational consequence —

**SAM:** Two consequences. One — your engagement runs *smoother* than ones that skip gates. Because the things gates catch are things that *would* break later.

Two — your client's CCO trusts your team. Because the gate is the thing the CCO *can see* every deployment going through. They don't have to spot-check. They can rely.

**KEVEN:** And teams that have skipped gates —

**SAM:** Have eventually had to add them back, after a near-miss or an actual incident. So you can put them in now or put them in later. Either way, you end up with gates.

### Adding a Service to a live tenant

**KEVEN:** OK. Pattern two. Adding a Service to a tenant that's already running other Services. This is the motion you described at the top.

**SAM:** Right.

**KEVEN:** Walk through the motion.

**SAM:** Eight-ish phases.

One — *announce.* Engagement-side: confirm the new Service is approved and budgeted. Client-side: confirm the client's CCO knows it's coming. The CCO's calendar gets the security gate scheduled.

Two — *prepare manifest.* The new Service's manifest is built. What canonical it consumes. What MCP tools it exposes. What agents it composes. What its KPI envelope is.

Three — *prepare Bicep.* The Service-specific Bicep parameters are filled in for this tenant.

Four — *security gate.* The pre-deployment security gate runs. Eight items. Sign-off.

Five — *deploy.* Run the Bicep. Gold mart materialises. MCP server spins up. Agent images mirror from authoring registry to client registry. Audit emission wires.

Six — *validate.* The Service runs against canary data. Outputs verified. Audit verified. RAI overlay verified live. Performance acceptable.

Seven — *enable.* The Service is exposed to its real users. Watched closely for the first hours. Watched routinely for the first week.

Eight — *document.* The deployment record — what version of Bicep, what agent images by SHA, what manifest hash, what gate-pass sign-off, what time the Service went live — goes into the tenant's deployment ledger. Permanently.

**KEVEN:** Clock time for the whole motion?

**SAM:** Three to ten business days, depending on client coordination speed and gate scheduling. Once you've done it a few times — three days. Tense first time — ten.

**KEVEN:** And the part you *can't* compress —

**SAM:** The security gate. Don't try. The gate is the floor of trust. If you skip it to compress timeline, you've burned the trust you've spent eighteen months building.

### Agent upgrades across clients

**SAM:** Pattern three. The motion you opened with — agent v1.5.0 across six tenants tonight.

**KEVEN:** Yeah. Walk me through what's happening underneath.

**SAM:** The framework's pattern is — *agent upgrades are coordinated, not parallel-uncoordinated.* The base image gets a new version, with agent-specific patches. The new image is built, signed, mirrored to all client registries. The Services that depend on those agents declare compatibility (per Episode Four). Then the rollout begins.

The rollout itself is *staged.* It's not — *push to all six tenants simultaneously and pray.* It's — *tenant one tonight at nine, validate for three hours, if good then tenant two tomorrow night at nine, validate, then tenant three, et cetera.* Each tenant is its own deploy. Each is independently verifiable.

**KEVEN:** And the value of staging —

**SAM:** If something is wrong with the upgrade, you find out on tenant one. Not on tenant six. You've eaten *one* incident, not six. And tenant six can have the upgrade *delayed* until the issue is resolved.

**KEVEN:** And the technology that makes this work —

**SAM:** The traffic-split capability in Foundry's agent service. The new agent version runs alongside the old one. Traffic is split — five percent on new, ninety-five percent on old initially. If new behaves, the split shifts. Twenty-five. Fifty. Seventy-five. Hundred. Each shift is a decision. Each decision is logged. If at any shift the new version misbehaves, the split is reverted.

**KEVEN:** And the rollback capability —

**SAM:** Native. Foundry agent service supports it. Rolling back from v1.5 to v1.4 is a configuration change. No re-mirror needed. No re-deploy. Just shift traffic back to the old SHA.

**KEVEN:** And the rule of thumb for how to stage —

**SAM:** Smallest blast radius first. Lowest-traffic tenant first. Most internal tenant first. The first canary should be a tenant where, if it breaks, the impact is *easy to recover from.* Not your largest production tenant.

### Rollback discipline

**KEVEN:** OK. Pattern four. Rollback. And rollback discipline.

**SAM:** Yeah. Let me say something that's *important* about rollback.

**KEVEN:** Go.

**SAM:** Rollback is not a feature you turn on once. Rollback is a *discipline* you practice. The technology is there. The skill is using it well, fast, under pressure, with the right communication. And teams that haven't *practiced* rollback are slow at it when it matters.

**KEVEN:** And the discipline includes —

**SAM:** Three things.

One — *every deploy has a rollback plan written before the deploy.* Not after. Written by the same person doing the deploy. *"If this goes wrong, this is the SHA we return to, this is the command, this is who needs to know."*

Two — *the rollback path is verified in pre-production.* Not theoretical. Verified. Roll forward to the new version, then roll back to the old, in a test environment. Confirm it works.

Three — *the team has practiced rollback in a controlled exercise.* Once per quarter at minimum. Pick a tenant. Roll forward an innocuous change. Roll back. Time it. Document the friction points.

**KEVEN:** And the team that hasn't practiced —

**SAM:** Is slow when it matters. The wrong time to learn how to roll back is during an incident.

### DR — the disaster recovery posture

**KEVEN:** OK. Pattern five — disaster recovery. Less of an everyday motion, more of an annual posture.

**SAM:** Right. DR is about — *if the worst happens, can we bring this tenant up somewhere else.*

**KEVEN:** And in APEX specifically —

**SAM:** APEX is mostly Azure-native, so the DR posture leans on Azure's regional capabilities. The agent images are in registries that can replicate cross-region. The Bicep modules can be parameterised to deploy in a different region. The Fabric data has geo-redundancy options. Sentinel and Purview have their own DR stories.

The framework's posture is — *DR is a deliberate engagement decision, not a default.* Some clients require active-passive across regions. Some accept higher RTO. Some are mission-critical and require active-active. The deployment guide doesn't prescribe one; it offers the patterns and the engagement chooses.

**KEVEN:** And the exercise cadence —

**SAM:** Annual DR exercise. At minimum. Pick a region. Bring up the tenant there. Validate. Tear down. Document what worked and what didn't.

### Where Sam and Keven disagree

**SAM:** OK. Pushback.

**KEVEN:** Go.

**SAM:** The pre-deployment security gate. I want to push on the *eight items, no exceptions* framing.

**KEVEN:** OK.

**SAM:** Because in my experience, after you've done eight gates on the same tenant, items two through five are *predictable yes.* The image signatures are verified by the build pipeline anyway. The identities haven't changed since gate one. The network paths haven't changed. *Item one — the manifest review — is the gate that actually catches things.* Items six through eight catch things sometimes. Items two through five are checkbox.

**KEVEN:** And your conclusion is —

**SAM:** My conclusion is — over time, on a mature tenant, the gate should *focus more deliberately on the items that matter for this specific Service.* Manifest review for sure. RAI overlay for sure. The others — verify they haven't drifted, but spend the *engineering attention* on the items that vary.

**KEVEN:** I think you're describing the gate *evolving*, not the gate *shrinking*. And I'd agree that on a mature tenant, the eight items take different amounts of attention. The risk is — if you publicly say *"we focus on items one, seven, and eight,"* somebody hears *"we skip items two through six,"* and the discipline erodes.

**SAM:** Yeah.

**KEVEN:** The framework's position — and I'd defend this — is *the eight items always run.* They might run *fast* on a mature tenant — like, three of them are pipeline-automated. But they run. Because the discipline of always running them is what catches the day when something has drifted and you didn't notice.

**SAM:** Mm. OK. I'll concede that. *Eight items always run, but the engineering attention is rebalanced as the tenant matures.*

**KEVEN:** Yes.

**SAM:** That's a better formulation.

### What stays with me

**KEVEN:** Synthesis.

**SAM:** Yeah. Four things.

One — *the motion is the language for what happens after Day-Zero.* Adding Services, upgrading agents, gating deployments, rolling back. Defined patterns. Predictable. Teachable.

Two — *the pre-deployment security gate is the floor of trust.* Eight items, named sign-off, no exceptions. The discipline is what makes the CCO trust the engagement.

Three — *agent upgrades stage. Traffic-split. Smallest blast radius first.* The technology is there. The skill is using it well.

Four — *rollback is a discipline, not a feature.* Practice it. Quarterly minimum. The wrong time to learn rollback is during an incident.

**KEVEN:** And I'd add — *the engagement lead's job in the motion is half-coordination, half-conscience.* Coordination — getting the right stakeholders into the right meetings at the right times. Conscience — refusing to skip the gate when timeline pressure is high. The lead who can do both is the lead who runs a mature engagement.

**SAM:** Yep.

---

## What to read next

**KEVEN:** Read the chapter on the pre-deployment security gate end-to-end. Then re-read it. The eight items are concrete. Memorise them. Every Service deployment goes through them.

**SAM:** And read the chapter on agent upgrades across clients. Because the staging discipline is the difference between confidently rolling out v1.5 across six tenants and accidentally taking out all six.

**KEVEN:** Next episode — final one. *Day-Zero, Day-2, Chaos.* The practitioner-track chapters. Failure scenarios, chaos engineering, CI/CD, FinOps, Day-2 operations. The series closes.

**SAM:** See you there.

[outro]

---

**End of Episode 05 · The Motion**
*≈ 5,050 words*
