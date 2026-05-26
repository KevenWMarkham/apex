# Episode 06 · Day-Zero, Day-2, Chaos

**Source:** *Professional APEX-M Deployment Guide* — Part VI (Failure Scenarios & Chaos Engineering · Day-Zero in Practice — A First-Tenant Walkthrough · CI/CD & FinOps Deep Dive · Day-2 Operations & Engineering Standards · Surfacing APEX-M in Microsoft 365 + Power Platform · Composing Client-Approved Adapters with APEX-M)
**Run time:** ≈ 25–30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: laptop fan, then the unmistakable bing of a Teams call coming in]

**SAM:** It's a Saturday morning in August. I'm doing nothing in particular. My laptop is open on the kitchen table. And I'm getting a Teams call from an engagement lead I work with.

[pause]

**KEVEN:** Saturday morning Teams call. Never good.

**SAM:** Never good. I pick up. She says — *"Sam, we just ran a chaos exercise. Killed the agent runtime on the staging tenant. Everything fell over and we don't know why."*

**KEVEN:** OK.

**SAM:** And the *good* part of that sentence is — *we just ran a chaos exercise.* This was a planned, scoped, controlled exercise. They picked a Saturday. They picked the staging tenant — not production. They killed the agent runtime *on purpose.* And things broke.

**KEVEN:** And the breakage was the point.

**SAM:** The breakage was the point. The whole reason you run chaos exercises is to find the things you didn't know were broken until something broke them. So she's not calling because there's a fire. She's calling because the exercise *worked* — it surfaced something — and she wants help understanding what they found.

**KEVEN:** And what they found turned out to be —

**SAM:** They found that the MCP server, when the agent runtime went away, didn't gracefully time out. It held connections open, ran out of socket file descriptors, and became unresponsive itself. *Even though* the agent was supposed to be the failure, the MCP server *also* became a failure mode. Cascading.

**KEVEN:** Which they would never have found in regular operation. Because regular operation doesn't kill the agent runtime to see what happens.

**SAM:** Right. And the fix — once they understood it — was small. A timeout configuration on the MCP server's downstream calls. Ten minutes of code, an hour of testing, deploy in their next regular cycle. *Not* an emergency. *Not* a 3 AM incident. A Saturday morning learning exercise that became a known-issue, scheduled-fix.

**KEVEN:** And that's the case for chaos engineering in production-ready APEX deployments.

**SAM:** That's the case.

**KEVEN:** I'm Keven Markham.

**SAM:** I'm Sam. APEX Deployment Podcast. Final episode. Day-Zero, Day-2, Chaos.

---

## The conversation

### Chaos engineering — why APEX does this

**KEVEN:** OK. Let me set this up. Chaos engineering is a discipline borrowed from Netflix, originally. *"Inject failures deliberately so you find out how systems fail before customers do."* The framework's deployment guide has a chapter on this — and what I want to argue is *the framework's chapter is right to include it.*

**SAM:** Why right?

**KEVEN:** Because APEX deployments are — structurally — *complex multi-component systems with delayed failure modes.* The agent runtime. The MCP server. The Gold mart. The Silver canonical. The platform layer. Five layers of moving parts. Each has its own failure mode. The interactions between them have *their own* failure modes that don't show up unless you provoke them.

*Without chaos exercises, you discover those interaction failure modes the worst possible way — in production, on a Friday, with the client watching.* The chaos exercise is the *alternative way of discovering them* — controlled, scheduled, on staging, with learning as the goal.

**SAM:** And the framework's specific chaos patterns —

**KEVEN:** Six patterns the deployment guide names.

*Agent runtime kill.* The one I just described. Confirm the upstream caller gracefully handles agent unavailability.

*MCP server kill.* Confirm agents fail gracefully when their tool layer disappears.

*Gold mart unavailability.* Confirm MCP servers return useful errors when their backing data is unreachable.

*Identity revocation.* Revoke a workload identity. Confirm everything that uses it fails *informatively* — and is recoverable when the identity is restored.

*Network partition.* Simulate the agent runtime losing access to the Gold mart's region. Confirm appropriate retry behaviour.

*Secret rotation mid-flight.* Rotate a secret while the system is running. Confirm consumers pick up the new value cleanly.

**SAM:** And the cadence —

**KEVEN:** Framework recommends monthly chaos exercises on staging for mature engagements. Once per quarter minimum.

**SAM:** And the rule about who runs them —

**KEVEN:** The platform engineer runs them. The agent team is *informed* but not driving. The engagement lead approves the exercise window. The client's security team *can* be informed if they care — though for staging-only exercises, often they don't need to be.

**SAM:** And what *never* gets chaos-tested —

**KEVEN:** Production tenants. Never. The framework is explicit on this. You can run chaos on a *parallel* of production — like a near-clone in staging — but never on the production tenant with real client workloads.

**SAM:** Why?

**KEVEN:** Because real users are real. Their experiments aren't ours to run.

### Day-Zero in practice — the walkthrough

**SAM:** OK. Let me bring up the *Day-Zero in Practice* chapter — because I think this chapter is the most under-read in the entire deployment guide.

**KEVEN:** Mm.

**SAM:** And the reason it's under-read is — it doesn't *look* important. The chapter is *a walkthrough* of one specific first-tenant onboarding. Step by step. With timestamps. With actual commands. With the *real* friction points the team hit. With the conversations with the client they had to have. It reads almost like a journal.

**KEVEN:** And that's why it's valuable.

**SAM:** That's why it's valuable. Because most documentation tells you *what to do.* This chapter tells you *what it feels like to do it.* The timing. The questions you'll get from the client at three different points. The thing that fails the first time. The fix.

**KEVEN:** And the architectural reason this chapter is in the guide —

**SAM:** The architectural reason is — *the framework recognises that the first tenant onboarding is qualitatively different from the second.* On the first, you don't yet have intuition for the friction points. The walkthrough is a substitute for intuition. Read it before your first tenant onboarding and you have *somebody else's intuition* to draw on.

**KEVEN:** And the limitation of the walkthrough —

**SAM:** Limitation is — every tenant is different. The walkthrough is *one path through* the motion. Yours will deviate. The walkthrough gives you the shape. It doesn't give you the script.

### CI/CD and FinOps — the operational economics

**KEVEN:** OK. Let me bring up the chapter that's most about operational economics. CI/CD and FinOps.

**SAM:** Yeah.

**KEVEN:** CI/CD first. The framework's CI/CD posture is —

**SAM:** Three pipelines, mapping to the three layers.

Platform CI/CD. Bicep changes. Triggered by Platform-repo merges. Deploys to a test platform, runs platform-validation tests, gated to production by named approval.

Service CI/CD. Service-Bicep and manifest changes. Triggered by Service-repo merges. Deploys to a staging Service-deployment, runs Service-validation tests, gated by the pre-deployment security gate we covered in Episode Five.

Agent CI/CD. Agent code changes. Triggered by Agent-repo merges. Builds new image, signs, mirrors. Promotes via traffic split. We covered this in Episode Four.

Three pipelines. Three layers. Three lifecycles. They don't cross.

**KEVEN:** And the failure mode if they cross —

**SAM:** Same as Episode One. Agent prompt change triggers Platform rebuild. Platform deploy triggers all Services to redeploy. Lifecycle collapse. Brittle pipeline. We covered the why; here's the *how to prevent.* Three pipelines. Strict separation.

**KEVEN:** OK. FinOps. Cost discipline.

**SAM:** Right. The framework's position on FinOps is — *Microsoft consumption is a real cost line on the client's books, and APEX deployments are responsible for it.* Not in the sense that Deloitte pays it — Deloitte doesn't pay Azure bills. In the sense that the deployment makes choices that determine the bill. And those choices should be conscious.

**KEVEN:** And the framework's tools for that —

**SAM:** Three.

One — *cost dashboards per tenant.* The deployment provisions Azure Cost Management views scoped to the tenant's subscription. The client's FinOps team sees real-time spend.

Two — *capacity right-sizing recommendations.* Fabric capacity, Foundry consumption, Container Apps scale. The framework recommends starting capacities for Wave One Services. The deployment includes monitoring that surfaces when capacity is over-provisioned (and underutilised) or under-provisioned (and throttling).

Three — *consumption alerts.* If a Service's daily Foundry consumption deviates from baseline by more than a threshold, an alert fires. *Often* this catches mistakes — like an agent that's looping inappropriately and burning model tokens. *Sometimes* it catches success — like a Service suddenly being used more heavily, which is a happy problem.

**KEVEN:** And the rule of thumb the framework uses —

**SAM:** Wave One spend should be predictable within plus or minus twenty percent of forecast. If you're outside that band, something is wrong with either the forecast or the deployment.

### Day-2 operations — the standards

**SAM:** OK. Let me hit Day-2 ops. Because *Day-2* is the language the deployment guide uses for *"running the tenant after Day-Zero is done."*

**KEVEN:** Yeah.

**SAM:** And the framework has *engineering standards* for Day-2. Boring stuff. But important.

**KEVEN:** Walk me through.

**SAM:** Five standards.

One — *on-call rotation defined and documented.* Who's on call. For what windows. What they're responsible for. How they escalate. Documented before the tenant goes live, not after the first 3 AM page.

Two — *runbooks for the top ten anticipated incidents.* Agent stops responding. MCP server returns errors. Gold mart query latency spikes. Identity expiration. Network connectivity loss. Each has a runbook. Even a one-page runbook is enormously better than nothing.

Three — *postmortem template and cadence.* When an incident happens — and incidents happen — there's a defined postmortem. Within forty-eight hours. Blameless. Five-Whys analysis. Action items with owners. The postmortems accumulate over time and become the engagement's institutional memory.

Four — *upgrade cadence.* Platform layer — quarterly. Services — engagement-driven. Agents — continuous-as-merged. Discussed at engagement steering committee. Not surprises.

Five — *capacity planning.* Quarterly review of consumption trends. Adjust capacity tier if needed. Forecast next quarter. Discussed with client's FinOps lead.

**KEVEN:** Five standards. Day-2 is a real discipline.

**SAM:** Real discipline. And the engagement that *under-invests* in Day-2 standards is the engagement that's constantly firefighting. The standards prevent the fires.

### Surfacing in M365 and Power Platform — the last-mile

**KEVEN:** Last topic before we close. *Surfacing APEX-M in Microsoft 365 and Power Platform.* The last-mile chapter.

**SAM:** Yeah. Let me set this up.

The agent runtime is in Azure. The user *isn't* in Azure. The user is in Teams, in Outlook, in a SharePoint site, in a Power App. The user's experience plane lives in the M365 ecosystem. The agent's brain lives in Foundry. *The surfacing* is how those connect.

**KEVEN:** And the framework's position is —

**SAM:** Three patterns.

Pattern one — *Copilot Studio bot wraps the agent.* The user types into Copilot Studio in Teams. Copilot Studio invokes the APEX agent via HTTP. The agent's structured output is rendered as a Copilot card. The user is in Teams the whole time; they never see Azure.

Pattern two — *Power Automate flow invokes the agent.* For workflow scenarios — a form submission, a calendar event, a SharePoint list update — Power Automate calls the agent as an HTTP step. The agent's output drives the next Power Automate step. Common for back-office automation.

Pattern three — *Custom web app or Teams app embeds the agent.* For more sophisticated UX needs, a custom application embeds the agent. Same agent. Different surface.

**KEVEN:** And the rule about where governance lives —

**SAM:** Governance lives at the agent. Not at the surface. The audit row emits regardless of which surface invoked the agent. The RAI overlay enforces regardless. The pii-unlock rules apply regardless. The surface is the surface; the agent is the agent.

**KEVEN:** And the temptation —

**SAM:** Temptation is to put governance logic in Copilot Studio because it's *closer to the user.* Don't. Surface-layer governance is brittle and ungovernable. The agent's audit-and-policy boundary is the floor.

### Where Sam and Keven disagree

**SAM:** OK. Last pushback of the series.

**KEVEN:** Bring it.

**SAM:** Chaos engineering. The framework recommends monthly cadence for mature engagements, quarterly minimum. I want to argue that *for many engagements, monthly is too frequent and quarterly is correct as a permanent cadence.*

**KEVEN:** OK.

**SAM:** Reasons. One — monthly chaos exercises consume real engineering time. A good chaos exercise is a full day. Plus the postmortem. Plus the fix engineering if something surfaced. Twelve days a year on chaos alone is a meaningful slice of engineering capacity.

Two — for a mature engagement, monthly chaos starts surfacing diminishing returns. The first few exercises find the structural issues. After six months, you're often *re-confirming* known-good behaviour. Which is fine, but is it worth a day per month?

Three — the framework's *monthly minimum* implicitly assumes Day-Zero plus six months is "mature." Some engagements take longer to mature. Forcing monthly cadence before the engagement is ready creates the wrong kind of exercise — chaos for chaos's sake.

**KEVEN:** I'd push back on this in a specific way. The *cadence* is monthly, but the *exercise* doesn't have to be the same exercise every month. Rotate through the six chaos patterns. Each pattern monthly is *too* much, but *the practice* of running a chaos exercise monthly keeps the team's reflexes sharp.

**SAM:** Mm.

**KEVEN:** What I'd concede is — for very mature engagements, where the team has run dozens of chaos exercises and the system has stabilised, *quarterly* is acceptable. *Quarterly is the floor.* Monthly is the recommendation while the team is still building the chaos discipline.

**SAM:** OK. *Monthly while building the discipline. Quarterly as the steady-state floor for mature engagements.*

**KEVEN:** Yes. And the engagement lead's job is knowing where they are on that spectrum.

**SAM:** Agree.

### The closing thought

**KEVEN:** OK. Series-closing thought. I want to land this somewhere.

**SAM:** Go.

**KEVEN:** Six episodes. Demo to deployable. The platform foundation. Building the tenant. Service and agent layers. The motion. Day-Zero, Day-2, chaos. *What does it all add up to.*

**SAM:** I'll take a swing.

**KEVEN:** Please.

**SAM:** *Deployment is a discipline.* Not a project. Not a phase. Not a hand-off from build to ops. A *discipline.* Something you do over the years that an engagement runs. Something with patterns, motions, gates, exercises. Something the team gets better at by practice.

The framework's contribution isn't that it discovered deployment. Every consulting firm does deployment. The framework's contribution is that it *codified* the deployment discipline — Bicep modules, security gates, motion patterns, chaos exercises, runbooks — into a *productized* set of artefacts that compounds across engagements. The fifth tenant benefits from what the first tenant learned. The tenth tenant benefits from what the fifth corrected.

**KEVEN:** That's well put.

**SAM:** And the listener of this podcast — somebody who's about to be in the deployment chair — the value of internalising the framework is *they don't have to learn it the painful way.* The painful learnings are already in the artefacts.

**KEVEN:** And the broader thing I'd add — across the whole Trilogy.

**SAM:** Go.

**KEVEN:** The Sellers Podcast told you how to win the deal. The Services Podcast told you how to design and build it. This podcast told you how to deploy and run it. Three volumes. Three audiences. One framework. Each layer earns its keep.

And the engineer or operator who's listened to all three has the *whole* picture. Pursuit through delivery through production. *That* practitioner is the one who can carry an APEX engagement end-to-end. And the firm's investment in the Trilogy is to *create* that practitioner.

**SAM:** Yep.

**KEVEN:** That's the Trilogy. That's the deployment podcast. That's the series.

---

## Final sign-off

**SAM:** Thanks for listening to the APEX Deployment Podcast. Six episodes. About three hours of audio. If you go to your next Day-Zero kickoff with the three-layer cake in your head, the three operational truths on your notepad, and the eight-item security gate as your floor of trust — this series did its job.

**KEVEN:** And if you don't — re-listen to Episode One on your commute. Iterate. The framework rewards revisiting.

I'm Keven Markham.

**SAM:** I'm Sam. This was the APEX Deployment Podcast. See you in the war room.

[outro music · long]

---

**End of Episode 06 · Day-Zero, Day-2, Chaos**
**End of Series · End of Trilogy**
*≈ 5,200 words · series total ≈ 30,000 words*
