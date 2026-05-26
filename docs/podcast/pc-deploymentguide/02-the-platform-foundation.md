# Episode 02 · The Platform Foundation

**Source:** *Professional APEX-M Deployment Guide* — Part II (Anatomy of the Platform Layer · Identity, Secrets, and Audit Trust · Network and Observability)
**Run time:** ≈ 25–30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: phone vibrating on a wooden surface, then again, then a third time]

**SAM:** Two-fourteen AM. A Wednesday in October. My phone is on the nightstand. I'm not on call but I'm one of three escalation contacts for a tenant we'd brought up six weeks earlier. The text says: *agent invocations failing across the board. Workload identity returning 403. Need eyes.*

[pause]

**KEVEN:** Mm.

**SAM:** I get up. I open the laptop in the kitchen. I look at the logs. And what I see is — every agent run for the last seventeen minutes has failed with the same error. *AADSTS700016 — application not found in directory.* Which is the kind of error message that means somebody, somewhere, deleted something they shouldn't have deleted.

**KEVEN:** Yep.

**SAM:** So I'm sitting there in the kitchen, and I'm trying to figure out what happened. And — here's the part of the story that matters — I can answer that question in seven minutes. *Seven minutes.* Because the platform layer keeps a separate, immutable audit trail of every identity-related action against the tenant. Service principal creations, deletions, role assignments, secret rotations — they all land in one place. I open that view. I scroll back seventeen minutes. And right there is a row that says *"service principal apex-agent-runtime deleted by user `[client admin name]` at 01:55:43."*

**KEVEN:** [exhales] Oh boy.

**SAM:** The client's IT admin, doing a cleanup pass on a different project — same tenant, different subscription — saw a service principal he didn't recognise, googled the name, didn't find anything internal, and deleted it. Because he was being a good steward of identity hygiene.

**KEVEN:** Right.

**SAM:** The reason I could resolve this in twenty minutes total — including waking up, opening the laptop, finding the incident, calling the client lead, getting the SP recreated, watching invocations recover — the reason I could do all that *and go back to bed* — is because the platform layer was built with an *identity-and-audit floor* that made the question answerable. If the platform layer hadn't been built that way, that would have been a four-hour outage and a six-hour postmortem.

**KEVEN:** I'm Keven Markham.

**SAM:** I'm Sam. APEX Deployment Podcast. Episode Two. The Platform Foundation.

---

## The conversation

### The platform layer as a floor

**KEVEN:** So I want to start with the framing the guide uses, which is — *the platform layer is a floor.* Everything else stands on it. Every Service. Every Agent. Every runtime. They all sit on top of a layer that you build once per tenant and then mostly leave alone.

**SAM:** Mostly.

**KEVEN:** Mostly. And the parts that make that floor are — *identity, secrets, audit, network, observability.* Five things. Boring things. Things engineers usually under-invest in because they don't sound exciting. But the *quality* of that floor is what determines whether the tenant is operable. Like — the whole story you just told only works because the floor was good.

**SAM:** Right.

**KEVEN:** And actually let me read a passage from the guide on this because I think it's one of the more underrated paragraphs in the whole book.

**SAM:** Go.

**KEVEN:** [reading]

*"The platform layer is the slowest-moving layer in APEX. It gets deployed once when a tenant is onboarded, gets touched lightly during quarterly upgrades, and otherwise sits there doing its job. The temptation, especially for a delivery team under pressure, is to under-invest in it — because it's not visible to the client. Resist that temptation. The platform layer is the layer that, when wrong, causes every Service to fail simultaneously. Get it right once."*

[pause]

**SAM:** That last line. *"Causes every Service to fail simultaneously."* That's the thing.

**KEVEN:** Yeah.

**SAM:** Because — picture the alternative. You've got six Services running on a tenant. The agent layer of one Service has a bug. *One* Service has a hiccup. The other five are fine. Your blast radius is one Service.

**KEVEN:** Right.

**SAM:** Now picture the platform layer goes sideways. The identity layer — like in my story. The key vault goes read-only. The container registry rotates a credential nobody knew was going to rotate. Suddenly *all six Services are down.* That's your full-tenant outage. That's the call you don't want to take.

**KEVEN:** And the framework's answer is — that's the layer you spend the most engineering rigour on, even though it gets the least visible credit.

**SAM:** Yep.

### Identity is the hardest part

**KEVEN:** OK. Let me ask you — of the five floor components — identity, secrets, audit, network, observability — which one do teams get wrong most often?

**SAM:** Identity. Not close.

**KEVEN:** Talk to me about why.

**SAM:** Multiple reasons. One — identity in Microsoft platforms is *layered.* You have Entra ID at the tenant level. You have managed identities at the workload level. You have service principals for things that can't use managed identities. You have role assignments that scope across resource groups. You have conditional access policies that apply to everything but sometimes don't apply the way you expect. There are five or six different mechanisms doing things that *look* the same but aren't.

**KEVEN:** Right.

**SAM:** Two — identity is the place where the *client's* posture meets the *framework's* posture. Every other layer, the framework owns the design. Identity, the *client* has opinions. Their CISO has standards. Their IT has conventions. Their compliance team has audit requirements. So you can't just deploy the reference architecture — you have to *negotiate* the identity model with the client.

**KEVEN:** And the negotiation tends to surface things —

**SAM:** The negotiation tends to surface things the framework didn't anticipate. *"We don't allow service principals without a six-month review cadence."* *"All managed identities have to be in this naming convention."* *"You can't assign Contributor at the subscription level under any circumstances."* All reasonable client requirements. None of them in the framework's defaults.

**KEVEN:** So how do you handle that?

**SAM:** Three patterns I've used. One — *get the identity conversation onto the agenda for the engagement kickoff.* Not week six. Week one. The longer it gets delayed, the more rework it causes.

Two — *map every identity in the framework to a *role* before naming it.* Don't propose "apex-agent-runtime" as a name. Propose "the workload identity that runs the agent containers, has read access to the key vault for prompt secrets, and has tool-call access to the Gold lakehouse." Once the role is agreed, the naming is the client's call. They will rename it anyway, so just let them.

Three — *expect the conditional-access policy to break your reference deployment, and plan for it.* Every client has a conditional-access policy. It will block something. Usually it blocks workload identity from a non-allowlisted region or from a non-allowlisted device-class. The first deployment after CA policy application is the deployment that fails. Plan for the test pass to be after CA policy is fully applied, not before.

**KEVEN:** That third one is the one I see teams discover painfully.

**SAM:** Every time. Conditional access is the great equaliser. You think the deployment is done. CA policy gets applied at the tenant level. Suddenly all your workload identities can't authenticate from your deployment runner. Two days of rework.

### Secrets — the part that looks simple and isn't

**KEVEN:** OK. Second floor component — secrets. Walk me through what makes secrets hard.

**SAM:** Three things.

One — *what counts as a secret.* This sounds obvious. It's not. API keys are obviously secrets. Connection strings are secrets. But — are PII reference values secrets? Are prompt template versions secrets? Are agent identifiers secrets? Different clients answer those differently. And the framework's defaults won't match every client.

Two — *secret rotation.* The framework supports rotation. Of course it does — every Microsoft secret store does. But *who triggers the rotation, what notifies the consumers, how do you avoid downtime during rotation* — those are decisions. And if the decisions are made implicitly — which is what happens when nobody talks about them — somebody finds out at 3 AM that a rotation cycled a secret and the agent runtime couldn't pick up the new value.

Three — *the developer experience.* This is the one most teams miss. The whole zero-cost-laptop story we talked about in Episode One — that depends on the secret-handling pattern *being the same on laptop and on production*, just pointing to different stores. If the laptop has secrets in a `.env` file and production has them in Key Vault, *the code path that reads them has to be identical.* Otherwise you've built two codepaths, which is exactly the substrate-coupling thing we said you shouldn't do.

**KEVEN:** And the right pattern there is —

**SAM:** Read all secrets through one helper. The helper checks an environment variable to decide whether to read from `.env` or Key Vault. The agent code calls the helper with a key name. The helper returns the value. The agent never knows where it came from.

**KEVEN:** Boring.

**SAM:** Beautifully boring.

**KEVEN:** I think that's actually a theme that runs through the whole platform layer — *the right designs are boring.* They don't impress anyone. They just work for years.

**SAM:** Yep.

### Audit trust — the part the auditor actually reads

**KEVEN:** Third floor component — audit. And actually I want to use a specific phrase from the guide here — *audit trust*. Not just "audit." *Audit trust.* The trust part matters.

**SAM:** Yeah, walk me through that.

**KEVEN:** OK. The framework's position is — emitting audit events isn't enough. You also have to make those events *trustworthy* — meaning tamper-evident, lineage-coherent, time-ordered, and accessible to an auditor with their own credentials. Without those properties, the audit log is just *a log.* Logs can be tampered with. Logs can be rewritten. Logs can be missing rows. The audit trail is meant to survive those threats.

**SAM:** And the framework's mechanism for that is — the hash chain.

**KEVEN:** Right. Every audit row is hash-linked to the prior row. You can't insert a row retroactively without breaking the chain. You can't delete a row without leaving a gap. The chain *is* the trust.

**SAM:** And the auditor's role —

**KEVEN:** The auditor walks up to Purview with their *own* Entra credentials, queries the audit data, sees the chain. They don't trust Deloitte's word for it. They don't trust a custom export. They read the data with their own access to the client's tenant. *That* is what makes the audit posture credible.

**SAM:** And the engineering rule that flows from this —

**KEVEN:** Two rules. One — *every audit emission must be designed before the audit-emitter is deployed.* Not after. You don't retrofit audit. You design it in.

Two — *the auditor's access path is provisioned on Day-Zero of the tenant.* Not month six. The auditor role is provisioned at the same time as the platform layer. Even if the auditor isn't going to use it for a year. Provision it, document it, hand the client the playbook for how to grant the read-role to whoever they pick.

**SAM:** And the failure mode if you skip these —

**KEVEN:** Failure mode is — month six the client's external auditor is on a call asking *"how do I read the audit data,"* and your team is hand-building a CSV export, which then becomes the auditable artefact, which is *unauthenticated*, which means the auditor doesn't really have audit posture. You've moved from *audit trust* to *audit fiction.* Bad place to be.

### Where Sam and Keven disagree

**SAM:** OK. Can I push on something?

**KEVEN:** Please.

**SAM:** The framework says — five floor components. Identity, secrets, audit, network, observability. I want to argue that *observability is wrong as a floor component.* I want to argue it's *application-layer.*

**KEVEN:** [laughs] OK. Make the argument.

**SAM:** The argument is — Sentinel, Defender, App Insights, Log Analytics — these are infrastructure. They are. They get deployed at the platform layer. Fine. But *what gets emitted to them* is a Service-layer and Agent-layer concern. The platform layer can set up the Sentinel workspace and the App Insights instance, but it can't *meaningfully* observe a workload it doesn't understand. So I think the framework conflates *deploying observability tooling* with *operating observability.* Those are different jobs.

**KEVEN:** Hmm.

**SAM:** And the consequence of conflating them — at the team I worked on, the platform team thought they "owned observability" because they deployed Sentinel. The agent team thought they didn't have to *use* Sentinel because the platform team owned it. Result — Sentinel was deployed and nobody was looking at it. We had Sentinel-as-checkbox, not Sentinel-as-defence.

**KEVEN:** [pause] OK. I think you're right that the conflation is dangerous. But I'd push back on the conclusion. The reason observability is in the floor — I think — is *not* because the platform team owns the alerts. It's because *the wiring* belongs at the platform layer. The Service can't choose whether to emit telemetry. The Service can't choose whether to be Sentinel-instrumented. The platform makes that mandatory. The Service-and-agent teams then *consume* the platform's observability — but the platform decides the rules.

**SAM:** So the platform layer is *the policy*, and the Service-and-Agent layers are *the operators*.

**KEVEN:** Yes.

**SAM:** OK. I can live with that framing. Where I think the framework is *implicitly* unclear is — *who's on call for what.* The platform layer being the policy doesn't tell you who gets paged when the policy fires.

**KEVEN:** That's a fair gap. And honestly I think that's a thing every engagement has to decide locally — the framework can't prescribe the on-call rotation.

**SAM:** Agree.

**KEVEN:** But the *thing* I'd add — and this is something we'll come back to in the chaos episode — every engagement should write down its on-call rotation in the first month and stick to it. Don't let the rotation be implicit. Implicit on-call is what makes a 3 AM page take four hours to resolve.

**SAM:** Yep.

### What stays with me from the floor

**KEVEN:** Let me try to land this episode somewhere. The platform layer is the floor everything stands on. The five components — identity, secrets, audit, network, observability — are boring infrastructure that, when done right, become invisible. The *point* of doing them right is invisibility. You don't get credit for the floor — you get a tenant that works.

**SAM:** And I'd add — the floor is the thing that determines whether 3 AM pages can be resolved in twenty minutes or four hours. The story I opened with — twenty minutes. Because the floor was good. If the floor had been bad, that would have been a four-hour-plus story and the client wouldn't have trusted us afterward.

**KEVEN:** Yeah.

**SAM:** Which I think is the deepest takeaway from this whole layer. *Quality at the floor compounds.* Three years in, the engagements that invested in the floor are the ones that are still running clean. The engagements that under-invested are the ones that are constantly firefighting infrastructure.

**KEVEN:** And the engagement that compromises the floor at sprint five thinking they'll fix it later —

**SAM:** — is the engagement that's still in fix-it-later mode at sprint forty-five.

**KEVEN:** Yep.

---

## What to read next

**KEVEN:** If you read one thing from the deployment guide before the next episode — read the chapter on the anatomy of the platform layer. It's the architectural overview. Once you have the picture in your head, every later chapter slots in.

**SAM:** And I'd add — read the chapter on identity, secrets, and audit trust. It's denser, but it's the chapter that pays the most rent. Every concrete tenant onboarding I've done, I've returned to that chapter at least three times.

**KEVEN:** Next episode — *Building the Tenant.* Day-Zero. The actual stand-up. Fabric, Entra, Purview, Sentinel deployed as one motion. The story of what happens in what order.

**SAM:** See you there.

[outro]

---

**End of Episode 02 · The Platform Foundation**
*≈ 4,950 words*
