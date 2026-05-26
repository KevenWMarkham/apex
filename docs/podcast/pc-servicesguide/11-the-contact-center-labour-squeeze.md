# Episode 11 · The Contact-Center Labour Squeeze

**Arc:** Business-need (7 of 7 — final business-need episode) · **Builds on:** Foundation + all business-need episodes (cross-Practice synthesis) · **Service delivered:** TMT-CC-01 Agent-Assisted Contact-Center · **KPI:** AHT · FCR · CES · attrition reduction
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: contact-center ambient — distant voices, keyboard typing, headset clicks]

**MORGAN:** I want to start with a number that captures the labour problem in one statistic. Globally, the customer-service industry employs more than *15 million* contact-center agents. In the U.S. alone — over 3 million. *And the annual attrition rate in U.S. contact centers is between 30 and 45 percent.* That means one in every three contact-center agents leaves their job every year. *Every year, the industry has to recruit, hire, and train more than a million replacement agents in the U.S. alone.*

[pause]

**KEVEN:** And the cost of that —

**MORGAN:** The cost is — *thousands of dollars per replacement.* Recruiting, training, and ramp time before the new agent is productive. Industry-wide, contact-center turnover costs U.S. employers in the *tens of billions of dollars per year.* And — here's the thing that makes it strategic, not just operational — *the experience of the customer who interacts with a high-attrition contact center is reliably worse than the experience at a low-attrition one.* High attrition feeds bad experience, which feeds more attrition, which feeds worse experience. It's a doom loop.

That's what this episode is about. The contact-center labour squeeze. The Service that arguably addresses it more directly than any other Service in the framework. And — critically — *why this Service shows up across multiple Practices.*

I'm Morgan.

**KEVEN:** I'm Keven Markham. Services Podcast Episode Eleven — the last business-need episode. *The Contact-Center Labour Squeeze.*

---

## The conversation

### Historical opening · how contact centers got to where they are

**KEVEN:** Walk the arc.

**MORGAN:** OK. Contact centers in their modern form date to the 1970s.

1970s and 80s — *call centres as cost centres.* The telephone was the only channel. Agents answered with paper scripts, paper customer records, paper escalation procedures. *Manageable* because call volumes were modest and inquiry types were limited.

1990s — *CRM systems and skill-based routing.* The CRM gave agents structured customer records. Skill-based routing matched calls to specialised agents. *Productivity rose.* But the *nature* of customer-service work didn't change much — the agent was still the primary problem-solver, reaching for system after system to compose the answer to the customer's question.

2000s — *channels multiplied.* Email, web chat, then social media. Each new channel required *new agent skills, new tools, new processes.* The agent's job became *channel-fragmented* — different tools for different channels, different data views, different procedures. *Complexity went up. Training time went up. Agent stress went up. Attrition went up.*

2010s — *self-service deflection.* IVR systems, FAQ websites, web-form self-service, chatbots. The thesis — *deflect simple inquiries before they reach the agent; let agents handle the complex ones.* The actual outcome — *the easy inquiries got deflected. The agents got the hard inquiries.* Which meant — *every interaction the agent handled was now a complex one.* The agent's job became harder on average. Burnout accelerated.

2020s — *the current era.* Post-pandemic, customer expectations for fast resolution have risen permanently. Agents are handling more complex interactions than ever. *Attrition is at historic highs. The labour market for contact-center talent is brutal.* Something has to give.

### The pain today

**MORGAN:** Operational pain.

**KEVEN:** Three pains.

Pain one — *the agent spends most of the call composing information across systems.* On a typical call, the agent toggles between five to ten systems — CRM, billing, order management, knowledge base, troubleshooting tools, internal procedures. *Eighty percent of the average-handle-time is system-navigation and information-composition.* Twenty percent is actual customer interaction. *The customer waits while the agent searches.*

Pain two — *the agent's job has become unsustainable.* The complexity of the work, the pace of channel-switching, the volume of information to retain, and the customer's heightened impatience combine into burnout. *Attrition at 40 percent annually isn't a recruiting problem. It's an architectural problem.*

Pain three — *the customer experience is unreliable.* The same inquiry handled by Agent A in 6 minutes might take Agent B 18 minutes. Same outcome — wildly different experience. *The variance itself is the customer-experience problem.* Customers can't predict whether their call will be quick or grinding.

### Why prior eras of technology couldn't fix this

**KEVEN:** Prior eras.

**MORGAN:** CRM and skill-based routing — *helpful but didn't close the gap.* Bots and IVR — *deflected the easy and made the hard harder.* Speech analytics and quality-management systems — *measured the problem but didn't change it.*

The agentic-era's contribution — *the agent does the system-composition work while the customer service representative talks to the customer.* That is the structural shift. The contact-center agent's job changes from *"information composer and customer talker"* to *"customer talker, with information composed for me in real time."*

### The strategy · agent-assisted customer service representative

**KEVEN:** And the strategy —

**MORGAN:** Agent-assisted customer service. The AI agent listens to the call in real time. Composes the customer context from across systems. Surfaces account information, recent interaction history, current entitlement, likely next-best action — *to the human agent* — in real time as the conversation unfolds. The customer service representative talks to the customer with *the information they need available immediately.*

The human agent's value-add becomes the *conversation* — listening, empathy, judgment, escalation decisions. The AI agent's value-add is the *information work* — composition across systems, retrieval, draft response, audit emission.

The math changes — *AHT drops because the system navigation drops.* *FCR rises because the human agent has the full picture.* *CSAT rises because the customer feels heard rather than waited-on.* *Attrition drops because the job is sustainable.*

### The Service that delivers it · TMT-CC-01

**MORGAN:** Architecture.

**KEVEN:** TMT-CC-01 — *Contact-Center Agent Assist.* Flagship TMT Service. And — crucially — the most-replicated Service in the framework, because the pattern shows up in retail, healthcare, telecom, financial services, energy.

Bronze. Multiple streams. The contact-center platform's call-event stream. The CRM for customer record. Order management. Billing. Service-history. Plus the in-call speech-to-text stream for real-time analysis. Bronze is mixed-velocity — streaming for call events and STT, batch for the steady-state customer record sources.

Silver. Canonical schemas — *the customer-and-interaction family* — which spans multiple Practices. The same canonical that RC uses for loyalty, that HLS uses for patient-member-interaction, that TMT-TEL uses for subscriber care. *This is one of the framework's most cross-Practice canonicals.*

Gold. The Service's Gold mart shapes per-call composed views — for any active call, the customer context, recent interactions, current entitlement, predicted intent, recommended next-best-action.

**MORGAN:** And the agent —

**KEVEN:** The agent has around eight MCP tools — narrower than the Service might suggest because the work is *focused on contextual retrieval for the human agent.* *Get_customer_context.* *Get_recent_interactions.* *Get_current_entitlement.* *Get_intent_signal.* *Get_next_best_action_recommendation.* *Draft_response_summary.* *Submit_for_review.* *Plus a routing tool for escalation patterns.*

The orchestration pattern is *router with parallel retrieval.* The agent runs continuously alongside the call. The router decides what to retrieve based on conversation flow. The retrievals run in parallel for low latency.

### KPI impact

**MORGAN:** Numbers.

**KEVEN:** Four dimensions — the contact-center metrics every COO of customer service watches.

*AHT — Average Handle Time.* The framework's reference scenario shows 25-40 percent AHT reduction. For a center doing one million calls a year at 8 minutes AHT, that's 4-6 million minutes of agent capacity returned.

*FCR — First Call Resolution.* Reference scenario shows 10-20 point FCR improvement. *Fewer callbacks. Fewer escalations. Lower volume in absolute terms.*

*CES — Customer Effort Score / CSAT.* Reference scenario shows meaningful improvement — typical 15-30 point improvements in CSAT during agent interactions.

*Attrition.* The slowest-moving but most-strategic metric. Reference scenarios show *5-10 percentage point reduction* in annual attrition after 12-18 months of agent-assist deployment, because the job becomes sustainable. Compounds.

Engagement-level annual value for a major telecom or financial-services client with thousands of contact-center agents is in the *hundreds of millions of dollars annually* — combining labour cost reduction, AHT efficiency, FCR-driven volume reduction, and attrition-cost avoidance.

### Why this Service is cross-Practice

**MORGAN:** Talk about why this Service shows up everywhere.

**KEVEN:** This is the *cross-Practice synthesis* moment for the series.

The contact-center pattern — *human agent talking to a customer, AI agent doing the system composition* — is the same in retail customer service, in telecom care, in healthcare member services, in financial services customer service, in airline disruption support.

The *canonical data* changes per Practice. Retail uses RC's customer-and-loyalty. Telecom uses TMT's subscriber-care. Healthcare uses HLS's member-encounter. *But the Service architecture is the same.* The MCP tools, the orchestration pattern, the agent-assist UX — all reusable.

*This is the framework's deepest example of asset reuse.* A team that has built the contact-center Service for one Practice can deploy it in a second Practice in a fraction of the time. The canonical-at-Silver investment is what enables that reuse. *The contact-center Service is the framework's proof point for the compounding asset thesis.*

### A reading I want to do

**KEVEN:** From a Gartner report on contact-center technology, 2024.

**MORGAN:** Read it.

**KEVEN:** [reading]

*"Agent-assisted contact-center technology has moved from emerging to mainstream in 18 months. Enterprises adopting it before 2025 are achieving operational results that materially differentiate their customer experience and labour economics. By 2027, agent-assist will be table-stakes across major contact-center operators. Enterprises without it will face structural cost and quality disadvantages they cannot close through hiring."*

[pause]

**MORGAN:** *Table-stakes by 2027.* That's the urgency message for the buyer who hasn't started.

### One disagreement

**MORGAN:** Pushback.

**KEVEN:** Go.

**MORGAN:** I want to push on the *agent-as-information-composer* framing. Because in practice, the most effective agent-assist implementations I've seen *also* coach the human agent in real time. *"Your customer just expressed frustration — slow down. Acknowledge."* *"This customer has called four times this month — the language pattern that worked last call was X."* *"You're in the closing minutes — confirm next steps explicitly."*

That's not information composition. That's *behavioural coaching.* It's controversial. Agents either love it or feel surveilled. The framework's posture should be explicit about whether coaching is in or out of scope for the Service.

**KEVEN:** That's a real design question. My read of the framework's current posture — *coaching is optional and is set per-deployment with the client.* Some clients want it on aggressively, some want it off entirely. The Service supports both. The deployment chooses.

The deeper point — coaching, when used, must be *enacted through the human agent's own choice.* The framework's HITL discipline applies to the agent's coaching too. Suggestions, not commands. *Surfacing the option, not enforcing the behaviour.* The human agent is the professional.

**MORGAN:** Agree.

### What to carry forward

**MORGAN:** Two things.

One — *agent-assist contact-center is the framework's most cross-Practice Service.* The pattern reuses across RC, HLS, TMT, ER, and TH. A team that builds it once can deploy it again. The compounding asset is real.

Two — *the human-AI collaboration model — AI composes information, human conducts conversation — generalises beyond contact center.* This same pattern shows up in claims adjudication, in clinical case management, in financial advisory, in incident response. The contact-center Service is just the most-visible example.

**KEVEN:** Next episode — the synthesis. The final episode. *What the Catalog Becomes When You've Heard the Whole Series.* We pull everything together.

**MORGAN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn

- **Microsoft Dynamics 365 Customer Service** · Microsoft Learn
- **Copilot Studio for customer service** · Microsoft Learn
- **Azure AI for contact center** · Microsoft Learn

### Microsoft Tech Community blogs

- **"Agent-assist patterns in production"** · Microsoft Industry Blog
- **"Real-time customer-service AI on Azure"** · Microsoft AI Blog

### Industry context

- **Gartner Magic Quadrant for Contact Center as a Service** · annual
- **Forrester Wave for Contact Center AI**
- **ICMI (International Customer Management Institute)** · contact-center benchmarks
- *"The state of contact center 2024"* · McKinsey
- *"Contact-center attrition and AI economics"* · Boston Consulting Group, 2024
- **Customer Effort Score literature** · CEB / Gartner (origin of CES metric)

### From the APEX Trilogy

- **Sellers Guide — *Technology Media Telecom Practice* chapter**
- **Sellers Guide — *Microsoft Contact Center + Voice* chapter** — the cross-Practice horizontal motion
- **Services Guide — *TMT Service Catalog* chapter** — TMT-CC-01 in detail
- **Services Guide — *Cross-Service Composition* chapter** — the reuse pattern that makes this Service portable

---

**End of Episode 11 · The Contact-Center Labour Squeeze**
**End of Business-need arc**
*≈ 5,200 words · target 30 minutes at conversational pace*
