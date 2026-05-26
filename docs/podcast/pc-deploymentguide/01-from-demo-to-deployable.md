# Episode 01 · From Demo to Deployable

**Source:** *Professional APEX-M Deployment Guide* — Foreword + Chapters 1, 2, 3 (Three-Layer Cake · Substrate-Aware Architecture · Independence Posture)
**Run time:** ≈ 25–30 minutes target
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: laptop fan, then a notification chime, then silence]

**KEVEN:** OK. I want to start somewhere uncomfortable. About eight months ago I was on a video call with a delivery team that was four sprints into an APEX engagement — first one for the team — and they had the agent working. The agent was *good.* Like — answering correctly, structured output, the audit row landing in the right place. On a laptop. They had it running locally, they were doing demos on the engagement-lead's MacBook, the client had seen it. Everyone was excited.

[pause]

**KEVEN:** And the call was — the engagement lead saying, *"Keven, we have a problem. We can't get it off the laptop."*

**SAM:** [laughs softly]

**KEVEN:** Like, *literally.* They had Docker Desktop running the agent. They had Postgres in a container. They had n8n doing the orchestration locally. Everything was *working.* And the question they couldn't answer was — *how do we put this in the client's tenant.* Not "should we." *How.* They didn't have the Bicep. They didn't have the agent images in a registry the client could pull from. They hadn't even started the conversation about which Entra ID was going to issue the workload identity. And the client's CIO had asked for a deployment plan by the next Friday.

**SAM:** And how far away was Friday?

**KEVEN:** Eleven days.

**SAM:** [exhales] OK.

**KEVEN:** And I think about that call a lot. Because the team wasn't bad. The agent design was good. The data work was good. What had happened was — they had spent four sprints building a working *demo*, and they had treated *deployment* as a separate problem that would be solved later. And it turns out — deployment isn't a separate problem. Deployment is the *actual* problem. The agent quality, the data foundation, the orchestration — those are all solved. What's not solved is the *path from working-on-laptop to running-in-the-client's-tenant.*

**SAM:** I will tell you — I have been on the receiving end of that call. Twice.

**KEVEN:** Yeah.

**SAM:** Different shape, same gap. There's a thing that happens around sprint four or five where the team realises — *oh, the thing we built is not the thing we're going to operate.* And then there's this scramble to figure out what the operational thing looks like. Which is what this whole book is about.

**KEVEN:** I'm Keven Markham.

**SAM:** I'm Sam. This is the APEX Deployment Podcast. Episode One. From demo to deployable.

---

## The conversation

**KEVEN:** So I want to start with something the Foreword says that I think is the single most important sentence in this entire book. Can I read it to you?

**SAM:** Please.

**KEVEN:** [reading]

*"Two years ago the question was — can an LLM-driven agent reliably make a markdown decision a category manager will trust. That question is now answered. The bottleneck moved. Sellers can show a working agent on a laptop in twelve minutes. What they cannot show, easily, is the path from that laptop to a client's Azure tenant under a two-contract commercial model with cosign-signed images, customer-managed keys, an immutable audit ledger, and a Bicep deployment that another delivery team can run end-to-end in a different tenant next month. That is what this book is about."*

[pause]

**SAM:** Yep.

**KEVEN:** That paragraph is — that's the whole pitch. The agent works. Now do the *real* job.

**SAM:** And the framing of *"another delivery team can run end-to-end in a different tenant next month"* — that's the test, right? Like, the deployment isn't done if only the team that built it can run it. It's done when somebody who wasn't in the original sprint can take the same Bicep, the same images, the same runbook, and stand up a new tenant. That's the reusable-asset version of "done."

**KEVEN:** And that's why the MVP framing matters so much. The book is really direct on this — the MVP is a *reusable asset*, not a pilot. Built around one Service — the pricing-and-revenue decision Service — engineered from day one to generalise across all 38 Services in the catalog.

**SAM:** Let me push on that for a sec, because I think there's a thing engineering teams miss. "Reusable asset" sounds like marketing. In practice, what does that *actually* mean?

**KEVEN:** Mm. OK.

**SAM:** Like — what's the difference between a *pilot* and a *reusable asset* in the deployment chair?

**KEVEN:** Three things.

One — the *Bicep modules* are written to be parameterised across tenants. Not hard-coded to the first client's subscription ID.

Two — the *agent images* are built in a registry that's intended to be mirrored. The Deloitte authoring registry is where they're built and signed. They get *mirrored* to the client tenant's registry. Same image, two registries, two trust boundaries. That structure has to exist on day one of the MVP, even when there's only one client.

Three — the *audit ledger* is engineered as a hash chain from the first row, not retrofitted in sprint twelve.

**SAM:** And the test for whether you've actually built a reusable asset?

**KEVEN:** You can run the deployment in a clean tenant — with parameters changed, no other modifications — and the thing comes up.

**SAM:** [laughs] Right. The "clean tenant" test. Which sounds obvious. And which, I will tell you from being in the chair, almost no team can pass on the third tenant.

**KEVEN:** Why?

**SAM:** Because there's always one thing — *one thing* — that got hardcoded somewhere. Resource group name. Storage account naming. A connection string that was supposed to come from Key Vault and instead got pasted into an environment variable that nobody noticed. And the first time you bring up a second tenant, you find it. The second time, you find the *second* one. By the third tenant onboarding, you've found most of them and the deployment is actually portable.

**KEVEN:** So you're saying the MVP-as-asset thing isn't a one-pass exercise.

**SAM:** No. I'm saying it's a *three-tenant* exercise. The MVP claims to be a reusable asset after one. The empirical evidence says it's actually portable after three. And the discipline is — *learn each lesson, write it down, never make the same hardcoding mistake twice.*

**KEVEN:** OK. And actually that's a perfect bridge into the three operational truths the Foreword sets up — because the truths are basically the framework for *not* making those mistakes in the first place.

**SAM:** Let's hear them.

### The three operational truths

**KEVEN:** Three truths. Stated in the book in one sentence each. I want to land each one with you because they're going to come back over and over in this series.

**Truth one — three layers, three lifecycles.** Platform, Service, Agent. Each one has its own version, its own container registry, its own deployment cadence. Mixing them collapses lifecycles into a single brittle pipeline. Keeping them separate is the whole point of how the system is designed to scale.

**SAM:** And the failure mode if you collapse?

**KEVEN:** The failure mode is — every time an agent prompt changes, the platform gets redeployed. Which means every time an agent prompt changes, the *tenant has downtime.* Which is insane.

**SAM:** Yeah.

**KEVEN:** And the version of that I've seen — the most painful version — is the team that has *one* CI pipeline for everything. Agent code in the same repo as Platform Bicep. PR merge triggers everything. So a one-line prompt fix in *The Analyst* agent rebuilds the entire Platform layer in twenty-three minutes. And every client tenant that's on that platform — that's their twenty-three minutes too.

**SAM:** Mm. OK, so I'm going to take the other side on this for a second.

**KEVEN:** Please.

**SAM:** Because I want to push on the "three lifecycles" thing. In practice — especially on the third or fourth tenant — the team is under pressure. The deadlines are real. And it is *very* tempting to say — *"OK, we're just going to redeploy everything as one bundle for this onboarding, we'll re-separate them later."*

**KEVEN:** Yep.

**SAM:** And I have seen senior engineers do that. With good intentions. *"We'll fix it on the next one."* And it never gets fixed, because the next one is also under pressure.

**KEVEN:** Right.

**SAM:** So my question to you is — how rigid should we be on this? Is the rule *never blur the lifecycles*? Or is the rule *blur them when you have to, but flag it as tech debt and re-separate within two sprints?*

**KEVEN:** Honest answer? It's the second one. The book is rigid on the principle because *the principle has to be rigid* — but in delivery, on tenant number three or four, you're going to make a compromise. The discipline is — *you document it.* You write down what got collapsed. You write down why. You write down when you're going to un-collapse it. And then you actually go un-collapse it.

**SAM:** And the failure mode there is —

**KEVEN:** The failure mode is the team that compromises without documenting. Because the compromise becomes the architecture by accident. And eighteen months in, they discover they're operating a brittle pipeline that nobody remembers deciding to build.

**SAM:** OK. So the truth is — three lifecycles, full stop, *and* — when reality forces a compromise, document it explicitly.

**KEVEN:** Yes. Don't move that goalpost. The principle is the principle.

**SAM:** Truth two.

**KEVEN:** **Same image, two substrates.** The container image that runs on a delivery lead's laptop, under Docker Desktop, is the *same image* that runs in Azure Container Apps in production. Substrate awareness lives at the edges — environment variables, Bicep parameters — not inside the agent code itself.

**SAM:** Talk to me about why this matters.

**KEVEN:** Because the alternative is — you've got two codepaths. One for laptop, one for prod. And the laptop one works, and the prod one mostly works, and the place where they *don't* match becomes the place where bugs hide. The agent that worked beautifully in your demo throws a 429 at 11 PM Friday night in production and nobody can tell whether it's the agent or the substrate.

**SAM:** I lived this once. Different framework — wasn't APEX. But same shape. Laptop development used SQLite. Production used Postgres. Eighty percent of the queries behaved identically. The remaining twenty percent — completely different semantics around null ordering. *Which only showed up* when a real customer had a record where one column was null and we tried to order by it. Took a week to find. The reason it took a week to find was — *the developer who wrote the query had never seen the prod behaviour on their laptop.*

**KEVEN:** Right. And the APEX position is — that should never happen. The image is the image. The substrate is the substrate. If the image needs to talk to a database, it talks to Postgres on laptop and Postgres on Azure. If it needs to talk to a key store, it talks to a `.env` stub on laptop and Key Vault on Azure — *but the interface in the code is the same.* The substrate awareness is at the *connection* layer, not the *logic* layer.

**SAM:** And that's the *zero-cost laptop* design goal, right?

**KEVEN:** Yes. And this is actually one of my favourite design choices in the framework. The book says — *the developer's inner loop runs at zero Azure cost.* New developer clones the repo, runs `docker compose up`, exercises the entire MVP — agents, orchestration, ledger, harness — and ships a working change without ever provisioning an Azure subscription.

**SAM:** What's the orchestration choice that makes that work?

**KEVEN:** That's the elegant one. n8n on laptop, Azure Logic Apps in production. Same orchestration shape — different runtime. n8n is free, self-hosted, runs in a container. Logic Apps is the Microsoft-platform-native production answer. The workflow patterns translate cleanly between them.

**SAM:** And the reason that matters operationally —

**KEVEN:** The reason it matters operationally is — onboarding a new engineer onto an APEX engagement takes a day, not a sprint. Because they don't need an Azure subscription, they don't need a Microsoft tenant, they don't need procurement approval for cloud credits. They clone, run, work. The friction is zero.

**SAM:** OK. Truth three. This is the one I think people misunderstand most.

**KEVEN:** **Independence is structural, not stylistic.** The two-contract model isn't a preference. It isn't a way of *talking* about the relationship. It's a thing the deployment architecture has to *enforce.*

**SAM:** Explain that to somebody who hasn't read the Sellers Guide.

**KEVEN:** OK. Two-contract model — the client signs one contract with Microsoft, for the Azure consumption. The client signs a separate contract with Deloitte, for services. Deloitte does not sit between the client and Microsoft commercially. Deloitte recommends the Microsoft platform on the technical and commercial merits, builds the deployment, runs the engagement. But the licensing flows directly. And that two-contract structure is *enforceable in the deployment.* The Microsoft resources are in the client's subscription. The Deloitte-authored artefacts — the agent images, the Bicep — are licensed to the client, not resold. The boundaries are concrete.

**SAM:** And the place this becomes architectural, not just legal —

**KEVEN:** The place it becomes architectural is in *identity.* The workload identities that run inside the client's tenant are *the client's identities.* Deloitte doesn't hold them. Deloitte doesn't have a back-door identity into the client's tenant. When a Deloitte engineer needs to operate on the tenant, they do it through a customer-granted access path, time-bounded, audited, with the client's CCO seeing every action.

**SAM:** And the language that signals you've got this right —

**KEVEN:** *"Microsoft-native deployment."* *"Deloitte's Microsoft Technology and Services Practice."* Never *"co-sell."* Never *"partner-channel."* Never anything that implies a commercial flow between Deloitte and Microsoft tied to a specific client engagement. That's not stylistic. It reflects how the deployment is *actually wired.*

**SAM:** OK. Three truths. Three lifecycles, same image two substrates, structural Independence.

**KEVEN:** That's the floor. Every other chapter sits on top of those.

### Where this leaves us

**SAM:** Let me try to synthesise where we are.

**KEVEN:** Please.

**SAM:** The Sellers Podcast tells you how to win an APEX deal. The Services Podcast tells you how to design and build it. This podcast is about what happens *after* — the day the client signs, the team is staffed, the engagement kicks off, and somebody on day one looks around and says, *"so… how do we actually deploy this thing."* That's where we live.

**KEVEN:** Yeah. And I want to add one thing — the listener for this podcast is somebody who's about to be in the deployment chair. Maybe for the first time. Maybe inheriting a tenant from a team that didn't follow the framework rigorously. Maybe stood up a tenant a year ago and now needs to add a second Service to it. Different starting points, same destination.

**SAM:** And the message of this episode is —

**KEVEN:** The message is — *the demo is not the deployment.* You can show a working agent on a laptop in twelve minutes. You cannot make it operate, governed, audited, multi-tenant, repeatedly, in twelve minutes. That work is its own discipline. And the three operational truths are the floor of that discipline.

**SAM:** And one more thing — the *zero-cost laptop* goal. That's underrated. Because what it means is — *new team members get productive fast.* And in a domain where engineering capacity is the binding constraint, that matters more than people realise.

**KEVEN:** Big agree. I think the framework's biggest hidden advantage is — the on-ramp gradient for an engineer is *gentle*, even though the framework itself is sophisticated.

### The thing that stays with me

**SAM:** OK, before we close — there's something I want to put on the record. The reason I personally trust this framework is not the architecture. It's that the architecture *holds up under pressure.*

**KEVEN:** Say more.

**SAM:** Like — I've been in incidents at 2 AM where the agent is misbehaving, the client's on the call, the engagement lead is on the call, and the question is *what changed.* And in a framework with three separate lifecycles, three separate version lines, three separate audit trails — you can answer that question. *Quickly.* You can say — *"the platform layer hasn't changed in eleven days. The service deploy was two days ago. The agent image was promoted six hours ago. The most recent change is the agent image. Roll it back."* That's a five-minute conversation, not a two-hour forensics exercise.

**KEVEN:** Mm.

**SAM:** And the only reason that conversation is five minutes is because of the discipline we've been talking about. The three lifecycles. Same-image-two-substrates. Structural Independence. They're not philosophy. They're *what lets you sleep on Friday night.*

**KEVEN:** Yeah. That's the right note to end on, I think.

**SAM:** That's the episode.

---

## What to read next

**KEVEN:** One small thing before we sign off. If you only have time to read *one* thing from the deployment guide before our next conversation — read the Foreword. It's six pages. It frames everything. And it has the line I read earlier — the *"twelve minutes to demo, but the path to the client's tenant is the actual problem"* line. Internalise that line and the rest of the guide reads differently.

**SAM:** And if you have time to read *two* things — read the chapter on the three-layer cake right after it. Layer one is the platform, layer two is the service, layer three is the agent. Each is its own thing. Each has its own deployment cadence. The whole architecture downstream is built around keeping them separate.

**KEVEN:** Next episode — we go inside the platform layer. Identity. Secrets. Audit trust. The floor everything stands on.

**SAM:** See you there.

[outro]

---

**End of Episode 01 · From Demo to Deployable**
*≈ 5,100 words · ≈ 30 minutes at conversational pace*

*Note on style: this episode deliberately uses no chapter or section numbers in spoken dialogue. The hosts know the framework; they don't recite its index. When the source is pointed to, it's quoted aloud and reacted to. The intent is a conversation between two practitioners, not a tour through a reference document.*
