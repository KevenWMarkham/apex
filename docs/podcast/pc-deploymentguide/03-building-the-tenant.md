# Episode 03 · Building the Tenant

**Source:** *Professional APEX-M Deployment Guide* — Part II concrete chapters (Deploying Microsoft Entra ID & Purview · Deploying Microsoft Fabric · Deploying Microsoft Sentinel & Defender) + Part V Day-Zero Tenant Onboarding
**Run time:** ≈ 25–30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: a quiet conference room. Coffee being poured. Three people scribbling.]

**KEVEN:** Last spring I was in a kickoff meeting in Minneapolis. Tier-1 financial services firm. We'd won an APEX engagement — first-of-its-kind for the firm — and we were on Day-Zero. Six people around the table. The engagement lead. A platform engineer from our side. Sam was on the call by video. Two folks from the client's CIO org. A Microsoft architect for technical questions.

[pause]

**KEVEN:** And about forty minutes into the meeting, somebody from the client said — *"OK, so for the Fabric deployment, the Entra deployment, the Purview deployment, and the Sentinel deployment — those are four separate workstreams, right?"*

**SAM:** [laughs] Mm.

**KEVEN:** And I had to gently say — *"No. Those are four pieces of one workstream. Day-Zero is one motion. The four deployments are coordinated."* And you could see the client team trying to process that. Because in their world, four product deployments would absolutely be four separate workstreams. Four PMs. Four schedules. Four risk registers. Four steering committees.

**SAM:** And the reason it has to be one workstream —

**KEVEN:** The reason it has to be one workstream is that the four deployments are *not independent.* Fabric needs Entra identities. Purview needs Fabric workspaces to catalog. Sentinel needs Purview as a source of audit data. *The wiring between them is the deployment.* If you split them into four parallel projects, you spend six weeks de-coordinating decisions that should have been made together in one room on Day-Zero.

**SAM:** I'm Sam.

**KEVEN:** I'm Keven Markham. APEX Deployment Podcast. Episode Three. Building the Tenant.

---

## The conversation

### Day-Zero is a motion, not a date

**KEVEN:** OK so I want to start by clarifying what we mean by Day-Zero. Because *Day-Zero* — the word — has a specific meaning in the framework that's a little narrower than "the day the deployment starts."

**SAM:** Right. *Day-Zero* in the framework is the *motion* that brings a tenant from *nothing* to *ready to receive a Service.* It's not a single day in any literal sense — it's typically a multi-day exercise, sometimes a one-week exercise. But it's *one coherent motion* with a defined start and a defined end.

**KEVEN:** And the end-state of Day-Zero is —

**SAM:** A tenant with the platform layer deployed, the identities in place, the audit floor instrumented, and the *capacity* to host its first Service. The Service itself isn't deployed yet. Day-Zero ends *before* the first Service goes in. The first Service is a *separate motion.*

**KEVEN:** And that separation matters why?

**SAM:** Because it lets the platform layer be tested *as a platform layer* before any Service workloads are on it. You stand up Day-Zero. You run platform-layer validation tests. You confirm identities resolve, audit emits, networking flows. *Then* you add the first Service. If something's wrong, you know whether it's in the platform or the Service. Mix those motions and you can't tell.

### The order of operations

**KEVEN:** OK. So the four big deployments inside Day-Zero — Fabric, Entra, Purview, Sentinel. What's the order? Because the order matters.

**SAM:** Yeah. Let me walk it.

*Entra first.* You cannot do anything without identities. The workload identities, the service principals, the role assignments — those have to exist before Fabric will accept being provisioned, before Purview will index, before Sentinel will see anything. Entra is the *literal* foundation.

*Then Fabric, partially in parallel with Purview foundation.* Fabric provisioning is multi-step — capacity SKU, workspaces, lakehouses, OneLake security policies. Purview's foundation can be set up *while* Fabric is provisioning — the Purview account, the data map, the classification engine. They don't depend on each other to *start.*

*Then the integration between Fabric and Purview.* This is where the dependency lights up. Purview cannot catalog Fabric workspaces until Fabric workspaces exist *and* Purview's managed identity has been granted reader access on them.

*Then Sentinel.* Sentinel last because Sentinel is consuming signal from *everywhere else.* The Entra audit feed, the Fabric activity log, the Purview policy events, the network flows, the application telemetry. Until those other systems are emitting, Sentinel has nothing to monitor.

**KEVEN:** So roughly — Entra, then Fabric+Purview in parallel, then their integration, then Sentinel.

**SAM:** Right. Total clock time — for a well-prepared engagement — three to five business days for the Day-Zero motion. Plus rework if conditional-access policy hits something unexpected.

**KEVEN:** And the rework usually shows up where?

**SAM:** At the Fabric-Purview integration step. Conditional access tends to block the Purview managed identity from registering Fabric workspaces if the workspace is in a region the client's CA policy doesn't allow. That's a half-day to a day to resolve, depending on how fast the client's identity team responds.

### Where the framework's deployment patterns earn their keep

**KEVEN:** OK. The framework has Bicep modules — published, versioned — for each of these deployments. Walk me through why having the Bicep matter so much.

**SAM:** Three reasons.

One — *reproducibility.* Without Bicep, the deployment is somebody's checklist, which is somebody's memory, which is somebody's biases. With Bicep, the same parameter set produces the same deployment in any subscription. Tenant number five looks like tenant number one.

Two — *parameter discipline.* Bicep modules expose *the right parameters* — the ones that should vary per tenant — and *bury everything else.* If your Bicep parameter list has thirty parameters, you've exposed too much. If your Bicep parameter list has two parameters, you've under-parameterised. The framework's modules have *deliberately* chosen the parameter surface. Trust it.

Three — *the path from MVP to production is the same Bicep.* The MVP we talked about in Episode One — same Bicep modules. Just parameterised for the MVP scope. As the engagement grows, the modules don't get rewritten. They get *re-invoked* with different parameters.

**KEVEN:** And the temptation that teams have to resist —

**SAM:** Forking the Bicep. *"We have a special requirement for this client."* Don't fork. The framework's position is — *parameterise harder.* If your client's requirement isn't expressible in the existing parameters, file a framework extension. The extension goes back into the canonical modules. The next client benefits.

**KEVEN:** That's actually a deep point. The Bicep modules are the framework's *productized* deployment IP. Forking them per client breaks the asset.

**SAM:** And every engagement that's forked them has regretted it on tenant number three.

### A specific moment — the day Purview almost broke the deployment

**SAM:** Can I tell a specific story here?

**KEVEN:** Please.

**SAM:** OK. Tenant — different client from the cold-open one. We're on Day-Zero. Entra is done. Fabric is provisioning. Purview foundation is up. We get to the Fabric-Purview integration step. Run the Bicep. Get a *very* unhelpful error.

**KEVEN:** What was the error?

**SAM:** *"Insufficient privileges to complete the operation."* That's it. Nothing else.

**KEVEN:** Generic Azure error.

**SAM:** Generic Azure error. And I spent forty minutes trying to figure out which privilege was insufficient. Was it the deployment runner's identity? Was it Purview's managed identity? Was it the Fabric capacity admin? Was it a tenant-level Entra setting? Could have been any of those.

**KEVEN:** What was it?

**SAM:** Conditional access. The client had a CA policy that required *MFA for any service-principal-initiated change to Purview resources.* The deployment runner is a service principal. It doesn't have an MFA context. The policy rejected it. The Azure error didn't say "conditional access" — it just said "insufficient privileges."

**KEVEN:** [laughs] Of course.

**SAM:** Took forty minutes to figure out. Took five minutes to fix once we knew — the client's identity team added a CA exception for the deployment runner's service principal, scoped to the tenant onboarding window.

**KEVEN:** And the lesson —

**SAM:** Two lessons. One — Azure error messages around conditional access are *uniformly terrible.* When you see "insufficient privileges" on Day-Zero, your first suspicion should be CA, not RBAC. Save yourself forty minutes.

Two — *get the CA policy review onto the Day-Zero pre-work list.* Before the deployment, ask the client's identity team — *"What CA policies will be applied to the tenant? Are any of them likely to block service-principal-initiated changes?"* The answer is almost always yes. The remediation is almost always a temporary scoped exception. Plan for it in advance.

**KEVEN:** That's the kind of operational knowledge that doesn't appear in the Bicep modules. The Bicep does the right thing if the platform lets it. Operational knowledge is what gets you through the *"platform won't let it"* moments.

**SAM:** Right. And that's part of why the framework's deployment guide reads the way it does — it's not just the Bicep modules, it's the *narrative wrapper* around them. *"Here's what works. Here's what fails. Here's why."* That's the deployment guide's value-add beyond the modules.

### The audit feed wiring — the bit I want to land

**KEVEN:** OK, last big thing I want to cover for Day-Zero. The audit feed wiring.

**SAM:** Yeah.

**KEVEN:** Because this is the bit that, if you skip it on Day-Zero, you eat it later. The audit feed wiring is — Entra activity goes to a Log Analytics workspace. Fabric activity goes to that same workspace. Purview policy events go to that same workspace. The workspace is consumed by Sentinel for detection rules. The workspace is *also* readable by the auditor with their own credentials.

**SAM:** And the engineering details people miss —

**KEVEN:** *Workspace lifetime.* The Log Analytics workspace is deployed at Day-Zero with a retention setting. The default is short — thirty days. The framework's recommendation is *much longer* — typically 365 days, sometimes more depending on the client's compliance posture. If you skip setting that on Day-Zero, the retention is whatever the default was, and you've lost data that you can't recover.

**SAM:** And rotating that later is —

**KEVEN:** Possible but messy. Better to get it right on Day-Zero. Five-minute decision; multi-year consequence.

**SAM:** And *which* identities flow into the audit feed —

**KEVEN:** Every workload identity. Every service principal. Every managed identity. All of them. If an identity makes a change to a resource the audit feed cares about, it shows up. There's no "this one is service work, don't audit it" carve-out.

**SAM:** And the reason for that strict posture —

**KEVEN:** The reason is — when something goes wrong, the question is always *"who or what did that."* If you've allowlisted some identities out of audit because they're "just service work," you've made the answer unknowable for those identities. Don't do it.

### Where Sam and Keven disagree

**SAM:** OK. I want to take a contrary position.

**KEVEN:** Please.

**SAM:** The framework's pattern is — *Day-Zero is a tightly coordinated motion, run as one workstream.* I agree with that *as the goal.* I want to push on whether it's *always achievable.*

**KEVEN:** OK.

**SAM:** Because in some clients — particularly in regulated industries, particularly in clients with a strong CISO function — the four sub-deployments cross *organisational* boundaries on the client side. The Entra deployment goes through the identity team. The Fabric deployment goes through the data platform team. The Purview deployment goes through governance and compliance. The Sentinel deployment goes through security operations. Those four teams *do not coordinate well by default.*

**KEVEN:** They do not.

**SAM:** And so the framework's pattern — *"run Day-Zero as one motion"* — requires us to create coordination that doesn't naturally exist on the client side. Which is fine, in theory. In practice, on a complex client, that means our engagement lead is spending *forty percent of Day-Zero just orchestrating client-side stakeholders.* Which is real work. Which has to be planned for.

**KEVEN:** Yeah.

**SAM:** So my pushback is — the framework's Bicep modules and operational patterns assume *that the client coordination is solved.* In practice, *the engagement lead has to solve it.* And the deployment guide could be more explicit about that being part of the job.

**KEVEN:** I think you're right that the guide implies but doesn't say it explicitly. The engagement lead's Day-Zero job is half technical orchestration and half client-side stakeholder orchestration. And the stakeholder side is harder.

**SAM:** Yep.

**KEVEN:** I'd add — the way to defuse this *partially* is the kickoff meeting. The one I described in the cold open. Six people in a room. Engagement lead, client CIO-org, Microsoft architect, our platform engineer. If you can get the *right* six client-side stakeholders into that kickoff, you've done eighty percent of the stakeholder orchestration up front. The actual deployment then becomes the technical work.

**SAM:** Agree.

**KEVEN:** And if you *can't* get the right six people into Day-Zero kickoff — that's a red flag. That means the client doesn't have its act together for an APEX engagement and Day-Zero is going to be painful regardless.

**SAM:** Yep.

### What stays with me from Day-Zero

**SAM:** Let me try to synthesise.

**KEVEN:** Go.

**SAM:** Day-Zero is the motion that brings a tenant from *zero* to *ready for its first Service.* It's not four projects — it's one motion. Entra first, Fabric and Purview foundation in parallel, then their integration, then Sentinel. Three to five business days clock time for a well-prepared engagement.

The framework's Bicep modules are the productized IP — *use them, don't fork them.* If you find a gap, file an extension; don't customise locally.

The audit feed wiring at Day-Zero is the thing that, if you skip, costs you later. Get retention right. Get every identity into the feed. Provision the auditor role.

The hardest part of Day-Zero isn't the Bicep — it's the *stakeholder orchestration on the client side.* The engagement lead has to plan for that as a real workstream.

**KEVEN:** And the thing I'd add — Day-Zero is the chapter of the engagement that the client *most* judges you on. The agent demos, the architecture diagrams, the value cases — those are anticipation. Day-Zero is *the first thing you actually deliver* to them. If Day-Zero is clean — if it ends on schedule, on scope, with the tenant in good shape — the client trusts you for the rest of the engagement. If Day-Zero drags — you spend the rest of the engagement rebuilding trust.

**SAM:** Yep.

**KEVEN:** Twenty engagements I've watched, this pattern holds. Day-Zero predicts engagement health.

---

## What to read next

**KEVEN:** Read the Day-Zero Tenant Onboarding chapter end-to-end. It's the chapter that, when you actually go to do this, you'll re-read three times. And it cross-references each of the four sub-deployment chapters — Entra & Purview, Fabric, Sentinel & Defender. Use the cross-references.

**SAM:** And I'd add — read the section on conditional access and how it intersects deployment runners. It's a small section. It will save you forty minutes the first time and an hour the second time.

**KEVEN:** Next episode — *Service and Agent Layers.* Once the tenant is ready, what does it mean to drop a Service into it? And then drop another Service. And then upgrade an agent across both Services. The layers above the floor.

**SAM:** See you there.

[outro]

---

**End of Episode 03 · Building the Tenant**
*≈ 5,100 words*
