# Episode 02 · The Commercial Arc

**Source:** *Professional APEX-M Sellers Guide* — Part I, Chapter 2 (§2.1 – §2.7) + §3.7 Independence posture toward Microsoft
**Run time:** 30 minutes (≈ 5,000 words)
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: phone call, slight ambient road noise — Keven is driving]

**KEVEN:** OK, I'm going to tell you the moment that taught me what the procurement defense script actually does. Two years ago. I'd been working a pursuit at a Fortune-100 retailer for fourteen weeks. Beautiful relationship with the CIO. Beautiful business case. ROI math signed off by their CFO's chief of staff. We're at the goal line. Statement of work in legal. And on a Wednesday morning, the head of procurement calls me. He says, *"Keven, we love what Deloitte is proposing. We just need you to compete this against three of your peers."*

[pause]

**JORDAN:** Oh no.

**KEVEN:** Right. *Three of my peers.* For a deal that I have spent fourteen weeks de-risking, where their CIO has already chosen us. The procurement office, doing their job, was about to commoditise me into a price war I couldn't win — because the other three firms hadn't done the discovery, hadn't built the schema, hadn't pre-sized the architecture. They were going to bid 60% of my number on 30% of the value, and the CFO would see two numbers and pick the smaller one.

**JORDAN:** And what did you do?

**KEVEN:** I read them the procurement defense paragraph. The one that's now in section two point seven of the Sellers Guide. I'll tell you exactly what it says before this episode is over.

**JORDAN:** Did you keep the deal?

**KEVEN:** Yes. I'm Keven Markham —

**JORDAN:** I'm Jordan. APEX Sellers Podcast, Episode Two. *The Commercial Arc.*

---

## Theme Statement

**KEVEN:** Today we're doing Chapter Two — the money chapter. The Sellers Guide structures this as the *commercial arc* — meaning the journey from a first conversation to a Wave Three relationship that's running for five years.

**JORDAN:** Six things to cover.

**KEVEN:** Six things. The two-contract model. The three-wave envelope. The value-delivery chain — Scenario, Solution, Use Case, Service, Persona, KPI. The human-oversight spectrum — HITL, HOTL, HIC. The ROI math. And then funding — DCIF, value share, what we *cannot* touch. Plus that procurement defense script, because I promised.

**JORDAN:** Let's go.

---

## The Story

### The two-contract model

**JORDAN:** Section two point one — the two-contract model. Why does this exist?

**KEVEN:** Because the single biggest commercial confusion in agentic AI is: *who pays whom for what.* A client gets one slide deck from us and one from Microsoft, and they don't understand whether they're buying Deloitte services or Microsoft software or both or how it works.

The Sellers Guide makes this explicit. Two contracts. Always.

**Contract One — the Microsoft enterprise agreement.** The client signs this directly with Microsoft. It covers Fabric capacity, Foundry consumption, Purview SKUs, Entra ID P2 licenses, Copilot if relevant. This is *software*. Deloitte does not sit in the middle of this transaction.

**Contract Two — the Deloitte services contract.** The client signs this with us. It covers discovery, design, build, deploy, run, and adopt. This is *services and IP application*.

**JORDAN:** And why is that structure important — beyond just being clear?

**KEVEN:** Three reasons.

One — *Independence*. Deloitte cannot resell Microsoft software at margin to clients we audit. The two-contract structure makes the boundary clean.

Two — *transparency*. The client sees exactly what they're paying for from each party. No hidden margin in software.

Three — *scalability*. When the client wants to expand Microsoft consumption — add another Fabric capacity unit, light up Copilot for another business unit — they don't have to re-paper with us. They just call their Microsoft AE.

**JORDAN:** OK. So when a CIO says "what's this going to cost me" — what do you say?

**KEVEN:** You say *"two numbers"* — and you walk them through the Wave One commercial envelope. Which is the next thing.

### The three-wave envelope

**KEVEN:** Section two point two. Three waves. Memorise the time-boxes and the deliverables.

**Wave One — six to nine months. The Foundation Wave.** Deliverable: one Service in production, behind a real workload, with audit-ready evidence and a measured KPI. The point of Wave One is *prove this works on our data with our governance.* Usually one to two agents, one orchestration, the Fabric medallion, the first Purview policy pack.

**Wave Two — nine to fifteen months. The Expansion Wave.** Deliverable: three to five additional Services live, the agent portfolio composing into cross-Service orchestrations, the data foundation extended to cover the second and third business units. The point of Wave Two is *prove the framework scales horizontally inside the enterprise.*

**Wave Three — eighteen-plus months. The Run Wave.** Deliverable: APEX is the operational AI fabric of the business. New agents are deployed by client teams, with Deloitte as advisor. The framework is part of the run-state. New industry Practices may be activated.

**JORDAN:** I want to push on the time-boxes. Six to nine months for Wave One — how does that actually break down?

**KEVEN:** Roughly: weeks one through six is discovery and Business Value Assessment. Weeks six through twelve is detailed design and the data foundation build — that's where canonical schema pays for itself. Weeks twelve through twenty is agent build and orchestration. Weeks twenty through thirty is HITL piloting, audit pipeline, and production cutover. The math is forgiving in either direction by about four to six weeks.

**JORDAN:** And the failure mode that pushes Wave One past nine months?

**KEVEN:** Always one of three things. The data isn't where they said it was. The governance approval process inside the client is longer than disclosed. Or scope creep — somebody decides Wave One should be "three Services, not one." The Sellers Guide has a sub-section on each.

### Envelopes — the dimension you don't see at first

**JORDAN:** OK. The guide has this concept — *envelope.* Section two point two A. And it's overloaded. There's a commercial envelope, a data envelope, a schema envelope. What do they all mean?

**KEVEN:** Great question and the source has this exactly right. There are six envelopes in APEX. Let me name them and then collapse.

One — **commercial envelope.** What the SOW covers. Hours, weeks, dollars.
Two — **data envelope.** What datasets the agent can read.
Three — **schema envelope.** What semantic contract the agent operates under.
Four — **persona envelope.** Which user roles can invoke the agent.
Five — **decision envelope.** What classes of decision the agent can take versus refer.
Six — **audit envelope.** What's emitted to Purview, retained, and reviewable.

**JORDAN:** And these nest.

**KEVEN:** They nest. The commercial envelope is the outermost — it bounds everything. Inside it, the data envelope bounds what the agent sees, the schema envelope bounds how it interprets, the persona envelope bounds who can ask, the decision envelope bounds what it can answer with versus *refer* with, and the audit envelope is the cross-cutting log of everything.

**JORDAN:** And the practical use of this in a sales meeting?

**KEVEN:** When a buyer says *"can the agent do X?"*, you answer in envelope terms: *"In Wave One, the commercial envelope covers this Service. The data envelope is these three datasets. The schema envelope is the build-record schema. The persona envelope is the warranty engineer. The decision envelope is recommend-not-act. The audit envelope is full hash-chain to Purview."* That paragraph wins architect conversations.

**JORDAN:** That's a lot to remember.

**KEVEN:** Section two point two A. Memorise the six. They'll come back over and over.

### The value-delivery chain

**JORDAN:** Section two point two B. The value-delivery chain. Scenario, Solution, Use Case, Service, Persona, KPI. Six links. Walk me through it.

**KEVEN:** OK, and the way to remember the chain is — it reads top-to-bottom from the buyer's strategic priority all the way down to the metric you'll commit to.

**Scenario** — the *business situation*. "Warranty costs are climbing and supplier recovery is slow."

**Solution** — the *named productised answer.* "Warranty Traceability and Cost Avoidance" — that's a Service in AXLE.

**Use Case** — the *specific workload.* "When a warranty cluster appears in field data, identify the manufacturing root cause."

**Service** — the *technical implementation.* The agents, orchestrations, data, governance for that Use Case.

**Persona** — the *human in the loop.* The warranty engineer. The plant quality lead. Their decision authority.

**KPI** — the *measurable outcome.* Time-to-root-cause, supplier-recovery dollars, escape-rate reduction.

**JORDAN:** And the practical use?

**KEVEN:** When you sit with a CIO, you start at Scenario. When you sit with a CFO, you finish at KPI. When you sit with a Chief Data Officer, you live in Service. The chain lets you enter at any link and walk the conversation in either direction. The Sellers Guide has four worked examples — RC, HLS, ER, AXLE — in section two point two B point three through point six.

**JORDAN:** I want to push on the KPI piece. Sellers always want to promise a number. When do we commit to a KPI in the contract?

**KEVEN:** Never in Wave One. Wave One *establishes* the baseline and *measures* the delta. The KPI gets committed to in Wave Two with confidence, or in a value-share construct. The Sellers Guide is very direct about this — section two point six. We'll get to value-share in a few minutes.

### HITL, HOTL, HIC — the oversight spectrum

**JORDAN:** Section two point two C. Three modes of human oversight. Let me make sure I have these.

**KEVEN:** Yeah:

**HITL — Human In The Loop.** Every decision requires explicit human approval before the agent acts. Slowest, highest assurance.

**HOTL — Human On The Loop.** The agent acts, the human reviews after. Faster, still governed, used for reversible decisions.

**HIC — Human In Control.** The agent recommends only. The human takes the action. Used for highly regulated or irreversible decisions.

**JORDAN:** And how do you choose for a given workload?

**KEVEN:** Three rules.

Rule one — *if the decision is irreversible, default to HITL or HIC.* You don't HOTL a payment authorisation.

Rule two — *if the regulator requires explicit approval, you have no choice — HITL.* Healthcare clinical decisions, for example.

Rule three — *if the workload is high-volume and reversible, HOTL is the right answer.* That's how you get the velocity gains.

**JORDAN:** And the conversation with the CCO?

**KEVEN:** The CCO needs to hear three things — *you have classified every agent decision against the oversight spectrum, the classification is in policy not in code, and the audit trail proves the mode was honoured.* That's the section two point two C point five paragraph. Memorise it.

### Service tiers and pricing

**JORDAN:** Section two point three — service tiers and volume pricing. Quick one.

**KEVEN:** Three tiers, and these are *consumption* tiers, not *capability* tiers. The capability is the same across tiers. What varies is the SLA, the model tier, and the throughput.

**Tier One — Standard.** Default model, default SLA, default throughput. The pricing reference for everything.

**Tier Two — Premium.** Higher model tier, tighter SLA, higher throughput. About 1.8 to 2.2 times the Standard price for the same Service.

**Tier Three — Sovereign / Dedicated.** Dedicated capacity, residency guarantees, custom SLAs. About 3 to 4 times Standard. Used for HLS, FedCiv, and a couple of ER deployments.

**JORDAN:** And the volume curve?

**KEVEN:** Volume discounting kicks in at the Microsoft consumption layer through their volume agreements, not through Deloitte services pricing. We don't discount services on volume — we add scope.

### The ROI math

**KEVEN:** OK. Section two point four. The CFO conversation. ROI math, three worked examples in the Sellers Guide. Let me do one — RC.

**RC client. Four hundred stores. Wave One.**

- *Investment:* Deloitte Wave One services — call it 2.8 million dollars. Microsoft consumption Wave One — about 600K dollars annualised. Total Wave One outlay — approximately 3.4 million dollars.
- *Returns, Year One:* Shrinkage reduction at three percent across four hundred stores — that varies widely but the conservative model in the Sellers Guide is 4.2 million dollars. Labour redeployment from analytics workflow automation — 1.1 million dollars. Markdown optimisation — 1.8 million dollars. Total Year One returns — approximately 7.1 million dollars.
- *Net Year One return:* 3.7 million dollars over investment. That's a 109% Year One ROI.
- *Three-year cumulative:* About 21 million dollars in value against approximately 6.5 million in total Deloitte plus Microsoft cost.

**JORDAN:** Let me push. Those numbers feel high to a sceptical CFO.

**KEVEN:** They should. And the way the Sellers Guide handles it — section two point four point four — *why the math is defensible* — is to *not* lead with the topline. You lead with the *delta* you can baseline. You measure the current-state shrinkage. You agree on the methodology *before* you commit to a number. The number in the model is what the framework can support — the number on the contract is what the client agrees they can measure.

**JORDAN:** And we never put the topline in the SOW.

**KEVEN:** Never. Wave One SOW commits to *the measurement infrastructure and the first Service.* The value is a *projection*, not a contractual obligation. Value-share constructs are the only place we accept dollar-denominated commitments — and that's a separate conversation, section two point six.

**JORDAN:** OK. There are two more examples in the guide — HLS payer and AXLE OEM. Listeners should read both. We won't do them in audio.

**KEVEN:** Right.

### Funding paths — Independence-compliant

**JORDAN:** Section two point five. Funding. And this is the most important Independence section in the entire commercial chapter. Read it like a lawyer.

**KEVEN:** Two valid funding paths, one forbidden one. And the structure here is *Independence by design.*

**Valid path one — direct client funding.** The client pays Deloitte directly for services from their own budget. Cleanest. The default. The way ninety percent of APEX engagements get funded.

**Valid path two — DCIF, the Digital Cloud Investment Fund.** Microsoft has a program where strategic accounts can get co-investment for cloud-adoption transformations. DCIF funds the *client's* costs — Microsoft consumption, sometimes training. It does *not* fund Deloitte services. That's a feature, not a bug — keeps Independence clean.

**JORDAN:** And the forbidden path?

**KEVEN:** ECIF.

**JORDAN:** What is ECIF?

**KEVEN:** Enterprise Commitment Investment Fund. It's a Microsoft fund that pays *partners* to deliver services to clients. Sounds great, right? Microsoft pays Deloitte to do client work. Independence problem — if Deloitte is being paid by Microsoft to deliver services that Deloitte then audits the outcomes of — *we are conflicted.* So Deloitte's Independence Office has bright-line prohibited ECIF for services delivered to clients we audit, which is most of our enterprise client base.

**JORDAN:** And what do you do if a Microsoft AE offers ECIF on a deal?

**KEVEN:** You say, *"We can't take ECIF. Let's talk about DCIF for the client side, and we'll find direct client funding for the Deloitte side."* And then you call your Independence partner that afternoon.

**JORDAN:** Never use ECIF as a positive funding path. Never mention it in client proposals.

**KEVEN:** Never. The Sellers Guide has the language explicitly — section two point five point five.

### Value-share

**JORDAN:** Section two point six. Value-share. Quickly — when does this work?

**KEVEN:** Three conditions all true.

One — the baseline is measurable today, before APEX. You have to know what the current-state KPI is.

Two — the attribution to APEX is isolatable. If you can't draw a clean line from the agent to the value, value-share creates audit problems.

Three — the client has the operational discipline to honour the measurement. You'd be surprised how many don't.

When those three are true — value-share is a powerful sales motion. You take a portion of upside in exchange for portions of fee at risk. When any one is false — don't do it. The Sellers Guide is direct: section two point six point two — *when value-share is inappropriate.*

### The procurement defense script

**KEVEN:** OK. Section two point seven. The promised payoff from the cold open. Procurement defense.

The script is one paragraph. Here it is, almost verbatim — and you should know this by heart because you will need it.

[reading]

*"We appreciate procurement's role in compressing cost. The compression you're seeking already lives in the structure of this deal. The Microsoft software is contracted directly with Microsoft at their best volume pricing — Deloitte is not in that margin. The Deloitte services are scoped tightly to a Wave One that ends with a measured KPI — meaning the value you are buying is measurable before Wave Two. If you would prefer to compete this services scope, we'll cooperate fully. We would simply ask that the competing bids be required to demonstrate (a) pre-existing canonical schema for your industry, (b) production-ready Purview governance templates, and (c) the named agent reference architecture for this Use Case — none of which can be assembled in a competitive-bid window. The compression target is not Deloitte's services price — it's the Wave One time-to-value, which is already 50% compressed against industry-standard custom builds."*

[pause]

**JORDAN:** That is a beautiful paragraph.

**KEVEN:** Memorise it. It works. What it does — it accepts the procurement officer's job, refuses to compete on price *within the framework of pre-existing assets*, and reframes the compression to time-to-value.

**JORDAN:** And the deal you mentioned in the cold open — that paragraph held.

**KEVEN:** Held the deal. We delivered Wave One. Wave Two is in market now.

### One more thing — Independence from Microsoft

**JORDAN:** Section three point seven, which is technically Chapter Three but it lives here commercially. Two minutes on Independence.

**KEVEN:** Right. And this is the part of the commercial arc that distinguishes Deloitte from every system integrator and partner-channel firm operating in the Microsoft ecosystem. *We do not co-sell with Microsoft.* We do not take partner-channel compensation. We do not flow Microsoft licensing through our contracts. We do not participate in revenue-sharing or partner-incentive economics on client engagements.

**JORDAN:** Let me push on that. Why so strict?

**KEVEN:** Two reasons. The first is Independence proper — most of our enterprise clients are also audit clients, and a financial flow from Microsoft to Deloitte tied to a client engagement creates a conflict the Independence Office will not accept. The second is *positioning credibility.* When we recommend the Microsoft stack to a CIO, the recommendation has to be defensible as a *technical and business* choice — not a *compensated* choice. The moment compensation enters the recommendation, the recommendation loses authority. Sellers who understand this win deals; sellers who don't, struggle in the room.

**JORDAN:** So what *does* the relationship with Microsoft look like, in practice?

**KEVEN:** It's a *platform recommendation* relationship, not a *commercial partnership.* In practice — three things.

One — *we recommend Microsoft technology because, for agentic AI at enterprise scale, the composed stack is the right answer.* We make that case on the technical and commercial merits. Sellers Guide Chapter Four — competitive positioning — is the script for *why Microsoft*. We use it because we believe it.

Two — *operational coordination with Microsoft field teams is appropriate and expected.* When a client needs Microsoft technical resources, capacity sizing input, or roadmap visibility, we help them get it. That coordination is client-benefiting and entirely separate from any commercial relationship between Deloitte and Microsoft.

Three — *the client's Microsoft licensing relationship is the client's relationship to manage with Microsoft directly.* Deloitte does not sit in the licensing transaction. We covered this in the two-contract model at the start of the episode — *Microsoft contracts directly with the client; Deloitte contracts directly with the client.* Two parallel, independent commercial threads.

**JORDAN:** And what does this mean operationally for a seller in a pursuit?

**KEVEN:** It means — *you walk into client meetings as Deloitte. Not as a Microsoft partner. Not as a co-seller. As Deloitte.* The Microsoft stack is the platform we deploy on. Microsoft is the client's other vendor relationship, not your team. The pursuit motion, the SOW, the value case, the engagement plan — all originate from Deloitte and stand on their own merits. Microsoft's involvement happens through the client, not through us.

**JORDAN:** And the failure mode if a seller forgets this?

**KEVEN:** Two failure modes. *One — proposing joint commercial motion in conversations with Microsoft AEs.* That triggers Independence review, often kills the deal. *Two — letting the client perceive that Deloitte and Microsoft are commercially aligned.* That destroys our advisory authority and turns us into resellers in the buyer's mind. Both avoidable by remembering — we are platform-aligned, not partnership-compensated. Section three point seven of the Sellers Guide is the bright-line reference.

---

## APEX Facts

**JORDAN:** APEX Facts. Eight in ninety seconds. Go.

**KEVEN:** Fact One — number of contracts in an APEX deal?

**JORDAN:** Two. Microsoft EA and Deloitte SOW.

**KEVEN:** Fact Two — three Wave envelopes?

**JORDAN:** Wave One six to nine months, Wave Two nine to fifteen, Wave Three eighteen-plus.

**KEVEN:** Fact Three — number of envelopes in APEX?

**JORDAN:** Six. Commercial, data, schema, persona, decision, audit.

**KEVEN:** Fact Four — six links in the value-delivery chain?

**JORDAN:** Scenario, Solution, Use Case, Service, Persona, KPI.

**KEVEN:** Fact Five — three oversight modes?

**JORDAN:** HITL, HOTL, HIC.

**KEVEN:** Fact Six — service tier multiplier from Standard to Sovereign?

**JORDAN:** Three to four times.

**KEVEN:** Fact Seven — valid funding paths?

**JORDAN:** Direct client funding and DCIF. *Never ECIF. Never partner-channel compensation.*

**KEVEN:** Fact Eight — the procurement defense compression target?

**JORDAN:** *"Not Deloitte's services price — Wave One time-to-value, already 50 percent compressed."*

**KEVEN:** Time.

---

## Adopt / Hold

**JORDAN:** Adopt versus Hold on the commercial arc. Keven, I'll take Adopt this time.

**KEVEN:** OK, do Adopt.

**JORDAN:** Adopt the commercial arc as a *thinking framework* on every deal — even the deals that don't end up in the seven Practices. The waves, the envelopes, the value chain, the oversight spectrum — these are *cognitive tools*. They let you have a coherent conversation with a CIO, a CFO, and a CCO in the same meeting without contradicting yourself. The single biggest reason sellers lose enterprise AI deals is incoherence across audiences. The commercial arc fixes that.

**KEVEN:** OK Hold. When does the commercial arc framework *not* serve the deal?

**JORDAN:** Two cases.

Case one — *very small or very technical pilots.* If the client wants to spend 200K on a quick proof, don't make them sit through "the six envelopes." Pitch a focused Service with a four-week scope. The commercial arc is for the deal that wants to be a Wave One — not the deal that wants to be a Lighthouse pilot.

Case two — *clients who are already deep into a framework of their own.* If they've already built their own commercial mental model — their own waves, their own KPIs — don't impose APEX's vocabulary on them. Translate. Use their language. The Sellers Guide has the translations in Chapter Four — section four point four — *how to respond in the room.*

**KEVEN:** Synthesis?

**JORDAN:** Use the arc as your *internal* model on every deal. Externalise it as much as the client wants. With sophisticated buyers — externalise the whole thing, they love the structure. With less mature buyers — translate it into their language, but stay coherent inside your own head.

**KEVEN:** That's right.

---

## Lessons

**KEVEN:** Monday-morning lessons.

One — **on your next deal, write down which seat each stakeholder occupies in the value chain.** Who cares about the Scenario? Who cares about the KPI? Who's between? You'll spot the missing buyer immediately.

Two — **read the procurement defense paragraph until you can deliver it from memory.** Section two point seven. It's about 180 words. Practise it.

Three — **never offer a contractual KPI commitment in Wave One.** If a client pushes, redirect to a Wave Two value-share. The Sellers Guide has the language.

Four — **if a Microsoft AE offers ECIF, say no, and call Independence the same day.** No exceptions.

Five — **rehearse the Independence-from-Microsoft language until it's second nature.** *"Deloitte recommends the Microsoft stack on the merits. Deloitte does not take partner compensation. Two contracts — one with Microsoft, one with us — independent of each other."* That paragraph belongs in your first CIO conversation, your first procurement conversation, and your first conversation with anyone from Microsoft's account team.

---

## Carve Outs

**JORDAN:** Carve out time. Mine — section two point two B point three through point six. The four worked examples of the value-delivery chain — RC, HLS, ER, AXLE. Read them all. The chain feels abstract until you see four worked examples back-to-back, then it clicks.

**KEVEN:** Mine — section two point four point four. *Why the ROI math is defensible.* Three pages. It's the answer to every "those numbers feel high" objection. When a CFO pushes back on your model, you're not arguing the number — you're arguing the methodology. Section two point four point four is the methodology.

---

## Sign-off

**KEVEN:** That's it for Episode Two. Next episode — the Four Pillars. Fabric, Foundry, Copilot, Purview. The Microsoft stack that makes APEX run. The one where every seller has to be able to position all four in five minutes flat — independently, on the technical and commercial merits.

**JORDAN:** See you there.

[outro]

---

**End of Episode 02 · The Commercial Arc**
*≈ 5,150 words · ≈ 31:00 at 165 wpm*
