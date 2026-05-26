# Episode 01 · The Moment

**Source:** *Professional APEX-M Sellers Guide* — Front matter ("The Moment") + Part I, Chapter 1 (Foundations · §1.1 – §1.6A)
**Run time:** 30 minutes (≈ 5,000 words)
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: ambient — quiet executive conference room, faint HVAC hum]

**KEVEN:** Three weeks ago, I was in a CIO's office in Plano, Texas. North of Dallas. Big Fortune-50 manufacturer, you'd recognise the logo. And the CIO — call him David — looks across the table at me and he says, *"Keven, I have eleven AI proofs-of-concept in my organisation right now. Eleven. And I cannot get one of them into production with an auditor that I trust. Tell me what you do differently."*

[pause]

**KEVEN:** And I thought — that is the question. That is the question every Fortune-500 CIO is going to ask in the next eighteen months. Not "can you build an agent?" Everybody can build an agent. The question is, *"can you put one in production, behind my real data, in front of my real customers, and survive my CCO, my CFO, and my external auditor?"*

**JORDAN:** [coming in] And what did you say?

**KEVEN:** I said — I'll tell you the framework, I'll show you the architecture, and I'll show you a worked example by Thursday. And on Thursday we walked him through APEX. Two weeks later we had a Business Value Assessment scoped.

**JORDAN:** That is the moment.

**KEVEN:** That is the moment. So today we're going to talk about *why* that moment exists right now, what APEX actually is in a sentence — and a sentence after that — and the five forces that mean every senior buyer on a Fortune-500 ELT is going to be asked this question in the next four quarters. I'm Keven Markham.

**JORDAN:** And I'm Jordan. This is the APEX Sellers Podcast — Episode One. *The Moment.*

[transition]

---

## Theme Statement

**JORDAN:** OK Keven, set the table. What are we covering in the next twenty-six minutes?

**KEVEN:** Front matter of the Sellers Guide and all of Part One, Chapter One. So: what APEX stands for, what an APEX Practice actually is, the five forces, the three executive pains, the first-meeting qualifier — and the piece I think is the most important sentence in the entire guide, which is section one point six: *why canonical schema is the acceleration kernel.*

**JORDAN:** Why is *that* the most important sentence?

**KEVEN:** Because everything else — the four Microsoft pillars, the seven industry Practices, the thirteen anchor accounts, the pursuit motion — all of it composes on top of canonical schema. If a listener walks away from this episode remembering one thing, it should be: APEX accelerates because the schemas are already built. Without that, you're back to a twelve-month custom build. With it, you're at six to nine months for Wave One.

**JORDAN:** Got it. Let's go.

---

## The Story

### What APEX stands for — and what it doesn't

**KEVEN:** So. APEX. Let's start with the literal acronym. The Sellers Guide has it on page one, but here's the thing — sellers never say the literal acronym to clients. We say "APEX" as a brand. But internally you should know it: **Agentic Platform for Enterprise eXecution.**

**JORDAN:** And the "M" in APEX-M?

**KEVEN:** Microsoft. The branded edition that runs on Fabric, Foundry, Copilot, and Purview. There's an APEX core that is platform-agnostic in theory. In practice we sell APEX-M — and we sell it as a Deloitte offering, independently, on the technical and commercial merits of the platform recommendation.

**JORDAN:** OK, and what *isn't* APEX? Because this is going to come up immediately.

**KEVEN:** Three things. One, APEX is not a software product. Deloitte doesn't sell you a license. The licenses are Microsoft's. APEX is the *framework* that turns the licenses into outcomes.

**JORDAN:** So how does the client pay for APEX?

**KEVEN:** They pay Deloitte for the implementation services. They pay Microsoft for the consumption. Two contracts.

**JORDAN:** And the second thing it isn't?

**KEVEN:** It isn't a single agent. It's a portfolio framework. We're delivering — depending on the Practice — anywhere from six to twenty agents in Wave One, all composed into orchestrations, all governed by the same Purview policy stack.

**JORDAN:** Third?

**KEVEN:** It isn't novel research. Everything in APEX is built from Microsoft's published platform capabilities. What's novel is the *composition* — the way we've pre-built the canonical schemas, the agent patterns, the orchestrations, and the audit pipeline so the client doesn't have to.

### What an APEX Practice actually is

**JORDAN:** Let me push on this — you keep using the word "Practice." It's overloaded. What does Practice mean in APEX?

**KEVEN:** Great catch. In APEX, a Practice is a *bundled, industry-specific reference implementation*. Five reusable assets per Practice:

1. **Canonical schemas** — the data contracts for that industry
2. **A library of agents** — the named workloads
3. **Orchestrations** — the multi-agent patterns
4. **Governance policy templates** — Purview classifications and labels
5. **A pursuit playbook** — the commercial motion

**JORDAN:** And how many Practices are there?

**KEVEN:** Seven, today. RC — Retail and Consumer. HLS — Healthcare and Life Sciences. ER — Energy and Resources. AXLE — which is Automotive. TMT — Tech, Media, Telecom. TH — Travel and Hospitality. And ICE — Industrial Commercial Equipment.

**JORDAN:** Why those seven?

**KEVEN:** They're the seven where Deloitte already has deep industry IP, where Microsoft has anchor accounts at the C-level, and where the agentic AI ROI math actually pencils out at the CFO level. The Sellers Guide has a whole chapter on each one — Part Three, chapters nine through fifteen. We'll cover all seven in Episode Four.

**JORDAN:** OK. And just so we're crisp — what's the difference between a Practice, a Service, an agent, and an orchestration? Because these all sound like the same thing.

**KEVEN:** Right, the guide has a section on this exact confusion — one point one A point five. So:

- **A Practice** is the *industry bundle*. AXLE is a Practice.
- **A Service** is a *productised workload* within a Practice. "Warranty Traceability and Cost Avoidance" is a Service inside AXLE.
- **An agent** is the *atomic AI unit* — a single LLM-powered worker that does one thing. There are usually several agents inside a Service.
- **An orchestration** is the *control-plane composition* — the parent agent that drives twenty-four child agents in sequence and emits the audit trail.

**JORDAN:** So Practice is the catalogue. Service is the SKU. Agent is the component. Orchestration is the recipe.

**KEVEN:** That's exactly how I'd put it to a CIO. Borrow that.

### The five forces — why now

**JORDAN:** OK. So why is this sellable *today*? You've described five forces in the Sellers Guide. Walk me through them.

**KEVEN:** Yeah, section one point two. Five forces, and any one of them on its own would not be enough. All five together are why every Fortune-500 CIO has agentic AI on their FY26 or FY27 plan.

**Force One — the decision-velocity gap.** Enterprise decisions that used to take six weeks now have to happen in two days. The data exists. The humans can't read it fast enough. This is the gap agents fill.

**JORDAN:** Example.

**KEVEN:** Warranty root-cause at an OEM. Eight to twelve weeks across six teams to figure out why a cluster of field claims happened. The window in which it actually matters — when you can still recover from the supplier — is closing in days. The agent does it in minutes. We covered that scenario in the Toyota outreach, by the way; episode four of this podcast will hit AXLE in detail.

**Force Two — agentic AI inflection.** The models crossed a threshold somewhere around late 2024. Agents that reason multi-step, call tools, and emit structured audit are now reliable enough for production. Two years ago this didn't work. Today it does. The window to be first-mover with your buyers is right now.

**Force Three — regulatory acceleration.** EU AI Act, NIST AI RMF, SEC AI disclosures, healthcare specifics, financial-services specifics. Every regulator on the planet is writing AI rules. Clients who don't have a governance story by mid-2026 are exposed. This is the Purview half of the conversation — we'll go deep in Episode Three.

**JORDAN:** Let me push on Force Three. Is the regulatory pressure pulling clients toward us, or pushing them toward "let's not do anything"?

**KEVEN:** Honest answer? It depends on the buyer. If you're talking to a CCO or a Chief Risk Officer, regulatory pressure is *the* reason they pick a governed framework like APEX over a hand-rolled solution. If you're talking to a business unit head who doesn't own risk, it's a tax — they want to ignore it. So you have to choose your sponsor.

**Force Four — data sovereignty and PII complexity.** Cross-border data, residency requirements, sector-specific PII rules. Trying to do agentic AI without a unified governance layer is a non-starter at the enterprise. Purview is the answer.

**Force Five — knowledge-worker shortage.** Demographics. Boomer retirements in industries like utilities and manufacturing. There aren't enough people to do the analytical work even if budget was infinite. Agents are not a labour-cost-arbitrage play, they're a *capacity-creation* play. That framing matters enormously with CHROs.

**JORDAN:** So summary on the five forces — the buyer's organisation cannot keep up with the data, the technology just crossed the line into usable, the regulators are forcing the question, the data complexity makes ungoverned solutions untenable, and they don't have the headcount to throw at it anyway.

**KEVEN:** That's the elevator. That's why this isn't a 2027 conversation, that's a 2026 conversation.

### The three executive pains

**JORDAN:** OK. So the macro forces are real. What are the *specific* executive pains APEX solves? Because forces don't sign contracts. Pains do.

**KEVEN:** Right. Section one point three. Three pains. And you should know which pain each buyer feels — because they're not the same person.

**Pain One — "my AI investments are stranded."** This is the CIO. They've spent two years funding pilots. None of them have made it to production. They have eleven POCs and zero P&L impact. Their CFO is asking pointed questions in QBRs. APEX answers this with: *here's a framework that gets you to production in six to nine months for Wave One, with audit-ready evidence the day it ships.*

**Pain Two — "I can't trust the output."** This is the CCO, the Chief Risk Officer, sometimes the General Counsel. They've seen the demos. They believe the technology *could* work. They don't believe their organisation can govern it. APEX answers with: *Purview, the hash chain audit, HITL gates by policy, every agent call logged.*

**Pain Three — "I'm losing on velocity."** This is the line-of-business executive. Their competitor is shipping faster. Their customer is asking why claims take three weeks. Their plant is generating data they can't analyse. APEX answers with: *the time-to-decision compresses from weeks to minutes for the workloads in our seven Practices.*

**JORDAN:** And how do you know which pain to lead with?

**KEVEN:** Section one point five — the first-meeting qualifier. Five questions you ask in the first twenty minutes. We won't go through all five right now, but the most powerful one is: *"What did your last AI-enabled change to a business process actually deliver, measured in dollars or hours?"* If they can answer cleanly — you're in a Wave Two conversation. If they can't — you're in a Wave One conversation. And the qualifier tells you who's actually authorised to buy.

**JORDAN:** And what if they can't answer it at all? Like they look at you and have no metric?

**KEVEN:** Then either you've found a real opportunity — they need APEX to *establish* their measurement baseline — or you've found a buyer who can't sponsor work. The Sellers Guide has a whole sub-section, one point five A, called the Red Flag / Go-No-Go cheat sheet. Ten red flags. Ten green flags. Forty-five-minute go-no-go decision. Use it. It saves quarters.

### The canonical-schema kernel

**JORDAN:** OK. The promised punchline. Section one point six. Why is canonical schema the kernel?

**KEVEN:** Here's the thing — every AI vendor in 2026 can demo an agent. Every one of them. The demos are uniformly impressive. The reason most of those agents never make it to production is not the model. It's the *data*. The data doesn't fit. The schema doesn't exist. The joins don't work. The semantics aren't shared across teams. The agent gives different answers depending on which team's dataset it was pointed at.

**JORDAN:** So canonical schema is —

**KEVEN:** Canonical schema is the pre-built data contract for each industry. For RC — Retail and Consumer — we've got the canonical schema for orders, returns, store ops, loyalty, supply chain. Pre-built. Lives on Fabric Silver layer — that's the medallion tier where canonical meaning is anchored. Joinable. Documented. Day one.

For AXLE — automotive — we've got the canonical schema for vehicle build records, connected vehicle warranty, quality events, assembly telemetry. Four schema families. All joinable by VIN. All anchored at Silver, ready to feed the per-Service Gold marts the agents consume.

**JORDAN:** And the acceleration math?

**KEVEN:** Section one point six point two. Without canonical schema — twelve to eighteen months to build the data foundation before you can put an agent in front of it. With canonical schema — six to twelve weeks of mapping and customisation. The agent goes live in Wave One.

**JORDAN:** Let me push on this. *Pre-built* schemas — clients always say "my data is unique. Your generic schema won't work."

**KEVEN:** Best objection in selling. Here's the response. The canonical schemas are *built on top of industry standards.* For HLS — FHIR. For RC — GS1, schema dot org commerce extensions. For AXLE — AIAG, SAE J-standards. For ER — CIM for utilities, OSDU for oil and gas. These aren't generic — they're the *standards your industry already uses for regulatory reporting.* Your data is unique in the *values*, not in the *structure*.

**JORDAN:** Got it. So the line is —

**KEVEN:** The line is: "Your schema isn't a snowflake. Your *data* is. And we don't replace your data — we map it onto a contract that the agents already know how to read."

**JORDAN:** That's a clean line.

**KEVEN:** Use it. It works. Section one point six point eight has the longer version for architects.

### Where this leaves us

**JORDAN:** OK. So coming out of Chapter One — a seller should be able to do what, exactly?

**KEVEN:** Three things.

One — articulate APEX in one sentence to any executive: *"APEX is the framework Deloitte uses to put governed, audit-ready agentic AI into production on the Microsoft platform, in six to nine months for Wave One, across seven industry Practices."*

Two — diagnose the buyer's pain quickly. Stranded investment? CIO. Trust gap? CCO. Velocity gap? LOB. Lead with the pain that matches the seat.

Three — qualify in or out in the first forty-five minutes. Section one point five A. Ten red flags, ten green flags. Don't waste a quarter on the wrong deal.

**JORDAN:** And the canonical schema thing — when does that come up?

**KEVEN:** It comes up the moment a CIO or Chief Data Officer says, *"how is this going to be faster than the eighteen months my last platform migration took?"* That's when you say *canonical schema*. Section one point six A. Read it. Memorise the standards list.

---

## APEX Facts

**KEVEN:** OK Jordan, APEX Facts. Six in ninety seconds. Go.

**JORDAN:** Fact One — APEX stands for?

**KEVEN:** Agentic Platform for Enterprise eXecution. M is for Microsoft.

**JORDAN:** Fact Two — number of Practices?

**KEVEN:** Seven. RC, HLS, ER, AXLE, TMT, TH, ICE.

**JORDAN:** Fact Three — number of forces making this sellable now?

**KEVEN:** Five. Decision velocity, agentic inflection, regulation, sovereignty, knowledge-worker shortage.

**JORDAN:** Fact Four — number of executive pains?

**KEVEN:** Three. Stranded investment, trust gap, velocity gap. CIO, CCO, LOB.

**JORDAN:** Fact Five — Wave One time to production with canonical schema?

**KEVEN:** Six to nine months. Without canonical schema — twelve to eighteen. That's the kernel.

**JORDAN:** Fact Six — the first-meeting qualifier question to memorise?

**KEVEN:** "What did your last AI-enabled change to a business process actually deliver, measured in dollars or hours?" If they can answer — Wave Two. If they can't — Wave One.

**JORDAN:** Time.

---

## Adopt / Hold

**JORDAN:** OK, Adopt versus Hold. I'll take Hold this time. Keven, give me Adopt.

**KEVEN:** Adopt — APEX is the right pitch when you're talking to a Fortune-500 organisation that has tried at least one AI pilot, has senior sponsorship at the CIO or CCO level, has Microsoft already in the stack — even partially — and has a measurable business outcome they care about more than the technology. Doesn't have to be all four. Three out of four and you're in a good deal.

**JORDAN:** OK. Hold. When is APEX the *wrong* pitch? And I'm going to be strict about this because the worst thing a seller can do is push APEX into a deal it doesn't fit. Hold case number one — if the client has *no* AI investments yet, you're too early. APEX is a "rationalise and accelerate" framework. There has to be something to rationalise. Pitching APEX to a CIO who hasn't started is going to bounce off as "we're not ready."

**KEVEN:** Fair. The Sellers Guide has the qualify-out script in one point four. The phrase is — *"This is probably a 2027 conversation for you. Let's reconvene when you've got your first pilot in market."*

**JORDAN:** Hold case number two — if the client is committed to a single-vendor SaaS strategy. They've gone all-in on Salesforce Einstein, or all-in on ServiceNow, or all-in on Palantir Foundry. APEX is composable on the Microsoft platform. If they don't have Microsoft as a strategic platform bet, this is going to feel like an unwelcome platform argument.

**KEVEN:** And the Sellers Guide is direct about this — Chapter Four, section four point seven, the disqualification decision tree.

**JORDAN:** Hold case number three — if the buyer isn't authorised to spend. This sounds basic, but I've seen sellers spend ten weeks building a thesis for a director-level sponsor who can't approve a Business Value Assessment. You need a sponsor who can write a check or authorise one.

**KEVEN:** Yeah, and that's the qualifier checklist — section one point five.

**JORDAN:** So synthesis — APEX is for buyers who have *started, struggled, and are looking for a framework to rationalise their AI portfolio.* Not buyers who are starting, not buyers who are committed elsewhere, not buyers who can't transact. Three out of four green-flag conditions, you're in. Less than two, qualify out fast.

**KEVEN:** That's exactly right.

---

## Lessons

**KEVEN:** OK Jordan, lessons. What does a seller do on Monday morning after this episode?

**JORDAN:** Three things.

One — **memorise the one-sentence pitch.** APEX is the framework Deloitte uses to put governed, audit-ready agentic AI into production on the Microsoft platform. Six to nine months, Wave One, seven industry Practices. Don't paraphrase. Use those words.

Two — **carry the first-meeting qualifier in your head.** Five questions. The most important one — "what did your last AI-enabled change deliver, measured in dollars or hours?" That single question will tell you in two minutes whether you're in a Wave One or a Wave Two deal — or no deal at all.

Three — **read the red-flag cheat sheet** — section one point five A — before every new pursuit. Forty-five minutes. Worth it.

**KEVEN:** And I'll add a fourth — *find an existing AI initiative inside the account.* If the buyer has eleven stranded pilots, you have eleven opportunities to demonstrate APEX value. Start with the most expensive one that's furthest from production.

---

## Carve Outs

**KEVEN:** Carve outs. What should our listener read next, Jordan?

**JORDAN:** My carve out — section one point six A, the Industry-Standard Schemas section. The connection between canonical schema and industry standards — FHIR, GS1, OSDU, J-standards — is the single best architect-and-CIO talking point in the book. Read it. Memorise the standards list. You'll use it within two pursuits.

**KEVEN:** Mine — go back to "The Moment" — the opening section before Chapter One even starts. Re-read it slowly. It's the macro setup for everything we just covered, and it's also the language to use in your first three minutes of a CIO meeting.

**JORDAN:** That's a good one.

---

## Sign-off

**KEVEN:** That's it for Episode One. Next episode — *The Commercial Arc.* The three waves, the value-delivery chain, ROI math, DCIF, value-share, and the procurement defense script. The money chapter.

**JORDAN:** See you there.

[outro music]

---

**End of Episode 01 · The Moment**
*≈ 5,050 words · ≈ 30:30 at 165 wpm*
