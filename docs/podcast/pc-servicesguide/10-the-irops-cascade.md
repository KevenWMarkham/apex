# Episode 10 · The IROPs Cascade

**Arc:** Business-need (6 of 7) · **Builds on:** Foundation + Eps 5-9 (orchestration depth) · **Service delivered:** TH-OPS-01 IROPs Recovery Orchestration · **KPI:** Rebooking velocity · CSAT in disruption · crew-and-equipment recovery time
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: airport gate area · faint PA system · roller bags]

**KEVEN:** I want to start at 5:47 PM on a Wednesday in July. Atlanta. Hartsfield-Jackson airport. A line of thunderstorms moves through the Atlanta hub. Within forty-five minutes, the airport goes from normal operations to *ground stop.* By 7:00 PM, every gate is occupied. By 8:30 PM, every legal crew has timed out. By 9:30 PM — twelve thousand passengers are stranded mid-itinerary.

That's a Wednesday at the world's busiest hub. *That happens routinely.* Maybe three or four times per major hub per year. Plus all the smaller, less-newsworthy events at smaller hubs. The cumulative passenger-impact across U.S. aviation in a year is — *millions of disrupted itineraries.*

[pause]

**MORGAN:** And the cost to the airline —

**KEVEN:** The cost to the airline of a single major IROPs event at a major hub is *eight to thirty million dollars.* Rebooking costs, hotel vouchers, meal vouchers, crew overtime, equipment repositioning, customer-service labour, and — the largest line — *future revenue lost to passengers who chose another carrier next time.*

That's what this episode is about. The IROPs cascade. The most operationally violent moment in a service business. The Service that turns the response from chaos into choreography.

I'm Keven Markham.

**MORGAN:** I'm Morgan. Services Podcast Episode Ten. *The IROPs Cascade.*

---

## The conversation

### Historical opening · how IROPs response evolved

**KEVEN:** Walk the arc.

**MORGAN:** OK. Aviation IROPs response — irregular operations — has a long history. Let me compress it.

1970s and 80s — *paper-based recovery.* The dispatch office had maps, phones, paper flight plans. Recovery was — the senior dispatcher made decisions verbally, runners delivered rebooking instructions, gate agents wrote new boarding passes by hand. *Slow but coherent for the relatively small fleets of that era.*

1990s — *operations control systems digitised.* Sabre, Amadeus, in-house systems gave dispatchers structured visibility into fleet state. *Big advance.* The decisions still rested with humans; the tools tracked what humans had decided.

2000s — *automated rebooking emerged.* The reservation systems gained the ability to *propose rebookings* when a flight cancelled. The customer service rep accepted or modified. Speed improved. *Still — under major-event conditions, the volume overwhelmed the systems and the agents.*

2010s — *operations control centres got more sophisticated.* The major carriers built large, dedicated 24/7 operations centres. Real-time fleet visibility, crew tracking, customer-impact heat maps. *Beautiful situational awareness.* The decision-making was still primarily human. The bottleneck shifted from *not knowing what's happening* to *not being able to act on what's happening fast enough during major events.*

2020s — *the era we're in.* Increased weather volatility. Tighter operational margins. Crew shortages that make recovery harder. *And* — for the first time — agentic AI mature enough to handle the multi-domain reasoning IROPs recovery requires.

### The pain today

**MORGAN:** What's painful in concrete terms.

**KEVEN:** Three pains.

Pain one — *the rebooking decision is a graph problem at scale.* When a flight cancels, every passenger on it has a recovery option set — typically dozens of alternatives. Each alternative has different fit for that specific passenger — connection times, cabin class, loyalty tier, special service requirements, party-size constraints. Multiply across the 12,000 passengers in a hub-closure event, and you have *millions of edges* to evaluate. *Humans cannot navigate this graph. The systems weren't designed to navigate this graph either.* They evaluated each rebooking sequentially, in order of customer-call arrival. Which meant — *the highest-value loyalty members frequently got worse recovery than late callers, because the late callers had simpler options remaining.*

Pain two — *crew-and-equipment recovery is its own optimisation problem.* The same event that cancels passenger flights also strands crews and aircraft in wrong cities. Recovering the *operating schedule* requires reasoning about crew rest rules, aircraft maintenance intervals, crew-pairing legality, aircraft-routing feasibility. *Different problem from passenger recovery, but tightly coupled — the passenger recovery depends on what fleet and crew are actually flying tomorrow.*

Pain three — *customer experience during disruption shapes lifetime loyalty.* Passengers don't usually remember the on-time flights. They remember the *bad disruption.* And the bad disruption is — *waited four hours for a rebooking, got rebooked on a worse itinerary, no one ever apologised, no one offered proactive compensation, found out about the cancellation from the gate agent rather than via app notification.* *That* shapes their next booking decision. *Better recovery experience is the difference between churn and retention.*

### Why prior eras of technology couldn't fix this

**KEVEN:** And the prior eras —

**MORGAN:** Dashboards showed disruption state. Didn't recover it. ML optimised individual sub-problems — *crew-pairing optimisation, aircraft-routing optimisation, customer-rebooking optimisation* — *separately.* The three solutions ran in different systems and didn't compose. *And during a major event, the composition is exactly the work that needs to happen.*

The agentic era's advantage — *cross-domain reasoning across passenger, crew, equipment, weather, schedule, customer experience — done coherently in a single agent with structured tools across all the domains.* That's what the Service does.

### The strategy · agent-driven IROPs orchestration

**KEVEN:** And the strategy —

**MORGAN:** Agent-driven IROPs orchestration. The agent runs continuously during a disruption event. As cancellations cascade, the agent — for each affected passenger — composes the optimal recovery option considering customer-side factors (loyalty tier, party size, connection requirements, fare class) and operational-side factors (which flights have capacity, which crews are legal, which aircraft are positioned). The agent generates proactive customer communications — *"Mr. Smith, your 7 PM flight has been cancelled. We've rebooked you on the 9:15 PM with seat 4A in business as you prefer. Hotel voucher and meal credit have been added to your account. Tap to confirm or modify."*

Meanwhile, *in parallel*, the agent coordinates crew and equipment recovery — composing the operating schedule recovery that lets tomorrow's operation start clean.

The IROPs duty manager *supervises* — reviewing the agent's overall recovery plan, intervening for exception cases, handling the genuinely-novel scenarios. The agent handles the high-volume routine. The human handles the high-stakes exceptions.

### The Service that delivers it · TH-OPS-01

**MORGAN:** Architecture.

**KEVEN:** TH-OPS-01 — *Airline IROPs Recovery Orchestration.* Flagship TH Service.

Bronze. Multiple streams. The PSS — passenger service system — for booking and itinerary state. The CRS — central reservations system — for fare and inventory. The crew management system. The aircraft routing system. The weather feed. The IROPs event stream itself.

Silver. Canonical schemas — the TH traveller-profile family, plus the operational schemas for crew, equipment, schedule. Identity reconciliation across PSS and loyalty program is critical for the customer-side recovery. Asset and schedule reconciliation is critical for the operational-side recovery.

Gold. Multiple Gold marts within the Service — *passenger recovery mart, crew recovery mart, schedule recovery mart, customer communication mart.* The agent's MCP tools span these marts in coordinated fashion.

**MORGAN:** And the agent —

**KEVEN:** The agent has roughly fifteen MCP tools — more than typical because the cross-domain reasoning requires many narrow tools. Read tools for traveller profile, itinerary state, fare availability, crew availability, aircraft positioning, weather forecast. Write tools — gated by tool-approval — for proposing rebookings, drafting customer communications, triggering crew reassignment workflows.

The orchestration pattern is *hierarchical with parallel fan-out* — a top-level orchestrator agent coordinates several sub-agents in parallel (passenger-recovery, crew-recovery, equipment-recovery, customer-communication). The hierarchical pattern is what the framework discussed in earlier orchestration material.

### KPI impact

**MORGAN:** Impact.

**KEVEN:** Three dimensions.

*Rebooking velocity.* The framework's reference scenario shows 5-10x improvement in passenger rebooking velocity during major events. Twelve thousand passengers rebooked in *hours* instead of overnight.

*CSAT during disruption.* The framework's reference scenario shows 20-40 point CSAT improvement during disruption events versus the same airline's historical baseline. CSAT during disruption is the leading indicator of loyalty retention.

*Operational recovery time.* The schedule that's flying tomorrow morning is closer to its planned shape. *Aircraft and crew positioning errors recover one shift earlier.* Which compounds — fewer cascading cancellations on the next operating day.

Engagement-level annual value for a major carrier is in the *$100M-$300M range* — combining direct event-cost reduction, retention impact, and operational-recovery efficiency.

### Where it goes next · Wave Two

**KEVEN:** Wave Two for an airline —

*TH-OPS-02 — Property Operations Optimisation.* If the carrier has a hotel-and-property arm, adjacent operational Service.

*TH-CX-01 — Personalised Stay Experience / Personalised Travel Experience.* Customer-facing personalisation outside disruption windows.

*TH-LOY-02 — Loyalty-Driven Experience Personalisation.* The mileage-program-aware sibling.

Wave Three play — *the airline's operational AI is continuously-agented across all major decision domains.* IROPs is the entry point. Day-to-day operations agents follow.

### A reading I want to do

**MORGAN:** From an IATA report on airline operational resilience.

**KEVEN:** Read it.

**MORGAN:** [reading]

*"The operational-resilience capability of an airline — measured by how quickly the carrier returns to schedule integrity and customer-service quality after disruption — has emerged as the most reliable predictor of carrier brand strength in customer surveys conducted across major markets. Carriers investing in AI-driven operational orchestration are achieving recovery profiles that materially differentiate them from peers. The competitive gap is durable because the underlying capability — composed multi-domain agent orchestration — is not commoditisable through point solutions."*

[pause]

**KEVEN:** *Not commoditisable through point solutions.* That's the architectural moat.

### One disagreement

**KEVEN:** Pushback.

**MORGAN:** I want to push on whether the framework's *15 MCP tools* for this Service is too many. Episode 4's design principle was *one tool, one purpose.* Fifteen tools is *a lot* of one-purpose tools. The operational tax of maintaining fifteen tools on a complex Service is non-trivial.

**KEVEN:** I'd defend the number for IROPs specifically. *This Service is unusually cross-domain.* Passenger, crew, equipment, schedule, communication. Each domain legitimately needs several narrow tools. Fifteen is high for typical Services. For IROPs it's appropriate. The *signal* is whether the agent's reasoning is *clearer* with fifteen narrow tools or with fewer broader tools. For this domain, my experience says — fifteen narrow is clearer.

What I'd concede — *the contract-test harness investment for fifteen tools is substantial.* Engagement budget should reflect that. Don't pretend the Service is the same complexity as a five-tool RC Service.

**MORGAN:** Agree.

### What to carry forward

**MORGAN:** Two things.

One — *cross-domain orchestration is where agent-driven Services produce their largest value swings.* IROPs is the framework's pedagogical example. The pattern generalises to incident response in any operational domain.

Two — *recovery quality during disruption is a loyalty-shaping moment.* In service industries broadly, the moments of disruption are when customer loyalty is most malleable. Agentic Services that handle disruption well produce outsized lifetime-value impact.

**KEVEN:** Next episode — the last business-need episode. *The Contact-Center Labour Squeeze.* TMT Practice. Cross-Practice synthesis — the contact-center pattern shows up in retail, healthcare, energy, and travel too. The most-replicated Service in the framework.

**MORGAN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn

- **Microsoft Cloud for Travel and Hospitality** · Microsoft Learn
- **Azure AI for industry — Travel** · Microsoft Learn

### Microsoft Tech Community blogs

- **"Airline operations AI on Azure"** · Microsoft Industry Blog
- **"Multi-agent orchestration in production"** · Azure AI Blog

### Industry context

- **IATA (International Air Transport Association)** · [iata.org](https://www.iata.org/) — airline industry standards
- **A4A (Airlines for America)** · operational data
- **U.S. DOT Bureau of Transportation Statistics — Airline On-Time Performance** · public on-time and cancellation data
- *"The Economics of Airline IROPs"* · MIT Center for Transportation and Logistics
- *"Customer experience during disruption"* · McKinsey Travel Practice, 2024

### From the APEX Trilogy

- **Sellers Guide — *Travel & Hospitality Practice* chapter**
- **Services Guide — *TH Service Catalog* chapter** — TH-OPS-01 in detail
- **Services Guide — *Orchestration Archetypes* chapter** — the hierarchical-with-parallel-fan-out pattern used here

---

**End of Episode 10 · The IROPs Cascade**
*≈ 5,100 words · target 30 minutes at conversational pace*
