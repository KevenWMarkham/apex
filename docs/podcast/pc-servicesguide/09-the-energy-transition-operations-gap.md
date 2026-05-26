# Episode 09 · The Energy-Transition Operations Gap

**Arc:** Business-need (5 of 7) · **Builds on:** Foundation + Eps 5-8 (streaming patterns from Ep 7, governance maturity from Ep 8) · **Service delivered:** ER-NET-01 Distribution Outage Triage · **KPI:** SAIDI · SAIFI · restoration time · crew dispatch efficiency
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: rain, wind, faint thunder]

**MORGAN:** I want to start in October 2022. Hurricane Ian had just made landfall in southwest Florida. Within twelve hours, more than two million utility customers were without power. The investor-owned utilities responding had something north of *forty thousand line workers* converging from twenty-eight states. The logistical operation to *get the lights back on* was — and is — one of the most complex peacetime mobilisations in the U.S.

And inside the utility control rooms during the response — *the dispatchers were drowning.* Tens of thousands of outage tickets. Crews requesting work. Customers calling. Equipment statuses changing minute by minute. The dispatchers — career professionals, deeply experienced — were operating at the limit of what humans can process.

[pause]

**KEVEN:** And the question that always gets asked afterward —

**MORGAN:** And the question always asked afterward — *could we have restored faster.* And the answer, every time, is *yes, with better triage.* Not better crews — the crews were heroic. Not better equipment — the equipment performed. *Better triage.* Better matching of which crew to which job in which sequence under which constraints. *That* is the bottleneck. And in a world where the energy transition is making the grid more complex year over year, *triage is going to keep being the bottleneck* unless something fundamental changes.

That's what this episode is about. The energy-transition operations gap. The reason traditional control-room tools can't keep up. The Service that closes the gap.

I'm Morgan.

**KEVEN:** I'm Keven Markham. Services Podcast Episode Nine. *The Energy-Transition Operations Gap.*

---

## The conversation

### Historical opening · how grid operations evolved

**MORGAN:** Let me walk the arc, because the operational story of the U.S. grid over forty years is — pretty interesting and most non-utility people haven't seen it laid out.

1970s and 80s — *the analog era.* Distribution control rooms operated through paper, phone, and CRT-style displays of basic circuit status. Outage management was — somebody called the utility, the call center took the report, the dispatcher routed a crew. The system worked because *the grid was relatively simple* — generation was centralised, flows were one-directional from generators through transmission through distribution to customers, the operational state of the network changed slowly.

1990s — *SCADA went digital.* Supervisory Control and Data Acquisition systems automated remote monitoring. Dispatchers got real-time visibility into substation states. *Big advance.* But the work of *managing the outage response* — deciding which crew goes where in what sequence — was still humans on phones with maps.

2000s — *outage management systems matured.* Tools like OSI Monarch, GE Smallworld OMS, Schneider/Itron OMS gave dispatchers structured ticket management, crew tracking, customer notification. *More progress.* But these systems were still operating on a *centralised, top-down model.* The dispatcher decided. The system tracked the dispatcher's decisions.

2010s — *distributed energy resources arrived in scale.* Rooftop solar. Battery storage. Electric vehicles. The grid started getting *bidirectional* — power flowing both ways. Voltage management became more complex. The dispatcher's job got harder. The OMS tools didn't fundamentally change to address the new complexity.

2020s — *the current era.* Massive grid investment driven by the energy transition. New transmission to connect remote renewables. Distribution-level smart meters at scale. EV charging concentration shifting load patterns. Climate-driven weather events more frequent. *The grid is more complex. The pace of operational events is faster. And the human dispatcher capacity has not grown.* The gap is what this Service is for.

### The pain today

**KEVEN:** Operational pain in concrete terms.

**MORGAN:** Three pains.

Pain one — *event volume during major outage exceeds dispatcher capacity.* During a hurricane response, blue-sky days, or wildfire-driven public safety power shutoffs, a regional utility can see *tens of thousands of outage events.* Tens of thousands of customers calling. Hundreds of crews to coordinate. The dispatcher's job, in those conditions, becomes *impossible without algorithmic assistance.*

Pain two — *the data needed for good triage lives in many systems.* Customer outage reports in the CIS. Sensor and SCADA data in the OMS. Crew location and skills in the workforce management system. Asset condition history in the GIS. Weather forecasts from external feeds. Predictive damage models from grid-modernisation programs. *No single system holds the composite view.* The dispatcher mentally composes — under time pressure — what an agent could compose continuously and reliably.

Pain three — *SAIDI and SAIFI are highly visible regulatory and customer-trust metrics.* SAIDI — System Average Interruption Duration Index — *minutes of outage per customer per year.* SAIFI — System Average Interruption Frequency Index — *number of interruptions per customer per year.* These are reported to public utility commissions. They are publicly compared across utilities. Bad SAIDI/SAIFI means regulatory pressure, rate-case difficulty, customer churn (in deregulated markets), and reputational damage. *Triage quality directly drives these metrics.*

### Why prior eras of technology didn't close the gap

**KEVEN:** And the prior eras —

**MORGAN:** OMS dashboards surfaced *what was happening.* They didn't *do triage.* The dispatcher did. Predictive damage models — used in major-storm response — improved the dispatcher's *forecast* but not the dispatcher's *decision-execution.* They couldn't dispatch crews; the dispatcher did.

ML-driven outage prediction was a real advance in the 2015-2022 era. Utilities like Pacific Gas & Electric, ConEd, and others built models that predicted equipment failures before they happened. *Useful.* Didn't fix the triage bottleneck during *actual* events, because predicting which crew should do what next during an active response is a *composition-and-reasoning* problem, not a prediction problem.

### The strategy · agent-assisted distribution outage triage

**MORGAN:** And the agentic strategy —

**KEVEN:** The Service is — agent-assisted distribution outage triage. The agent monitors the active event stream. The agent composes the dispatcher's mental model continuously and reliably. The agent recommends — *for each crew currently available, the next best job based on customer impact, restoration time, asset condition, weather risk, crew skills, and operational constraints.* The dispatcher reviews and approves.

The dispatcher remains *in control.* The agent is a *force multiplier* — it lets one dispatcher handle ten times the event volume she could handle alone, with the same quality of judgment.

### The Service that delivers it · ER-NET-01

**KEVEN:** Walk me through the architecture.

**MORGAN:** ER-NET-01 — *Distribution Outage Triage.* The flagship ER Service.

Bronze layer is heterogeneous. Streaming sources — SCADA telemetry, AMI smart-meter outage signals, customer service interaction events. Batch sources — GIS asset data, workforce skills and certifications, historical outage patterns, weather forecasts. Streaming Bronze through Eventstream. Batch Bronze through DataFactory pipelines.

Silver. Canonical schemas — the ER utility-network family, which is grounded in the Common Information Model (CIM, IEC 61970/61968). Asset identity, network topology, customer-to-asset linkage, all reconciled at Silver. Plus the workforce and weather Silver tables.

Gold. The Service's Gold mart shapes per-event triage views. For each active outage event — affected customer count, asset condition score, estimated restoration time at various crew/equipment assignments, regulatory-priority flags (medical-baseline customers, critical infrastructure), weather constraints.

**KEVEN:** And the agent —

**MORGAN:** The agent has roughly ten MCP tools. *Get_active_events.* *Get_event_impact_assessment.* *Get_crew_availability.* *Get_asset_condition.* *Get_weather_constraints.* *Get_regulatory_priorities.* *Recommend_crew_assignment.* *Recommend_resource_request.* *Submit_dispatcher_review.* *Plus one read-only escalation tool for events that require human-only judgment.*

Agent instructions tell it — *given the current active event state and the available crew, recommend the next-best assignment sequence; explain the reasoning; surface tradeoffs; route to the dispatcher for approval.*

**KEVEN:** And the dispatcher's view —

**MORGAN:** The dispatcher sees agent recommendations overlaid on the OMS. *Crew Alpha-7 is currently free. Recommended next assignment: Event 14523, affecting 247 customers including 3 medical-baseline customers, estimated 75-minute restoration. Reasoning: weather window favourable; closest crew with required certifications; medical-baseline priority elevated. Approve / Modify / Hold.*

The dispatcher approves or modifies. The OMS dispatches per the dispatcher's decision. The audit row captures the recommendation, the dispatcher's decision, the outcome.

### KPI impact

**KEVEN:** Impact.

**MORGAN:** Three dimensions.

*SAIDI improvement.* The framework's reference scenario shows 10-20 percent SAIDI improvement during major events when the agent is in the dispatch loop versus the same utility's historical performance. For a utility with 4 million customers and a baseline of 90 SAIDI minutes per customer-year, that's 9-18 minutes per customer-year of improved service — millions of customer-minutes of restored service value.

*Dispatcher productivity.* Crisis-event dispatcher capacity 3-5x what it was without the agent. Which means utilities can handle more severe events with the same dispatcher staffing, or smaller staffing for routine operations.

*Regulatory and rate-case posture.* Utilities operating well on SAIDI/SAIFI have a better posture in rate cases before the public utility commission. The value of *better rate-case outcomes* is enormous — sometimes hundreds of millions in approved capital recovery.

### Where it goes next · Wave Two

**KEVEN:** Wave Two for utilities —

**MORGAN:** Adjacent Services. *ER-GRID-05 — Demand-Response Orchestration.* Customer-side energy management coordinated with grid state. *ER-NET-04 — Distribution-Level Voltage Optimisation.* Continuous voltage management as DERs proliferate. *ER-QUAL-01 — Environmental Compliance Monitoring.* Cross-cutting compliance for grid operations.

The Practice's Wave Three play is *distribution operations as a continuously-agented function.* Outage triage was the entry point. By Wave Three, the agent assists across the entire control-room workflow.

### A reading I want to do

**KEVEN:** From an Electric Power Research Institute publication on grid operations, 2024.

**MORGAN:** Go.

**KEVEN:** [reading]

*"The combination of distributed energy resources, climate-driven weather volatility, and aggressive decarbonisation timelines is producing a grid that requires faster, more contextual, more interconnected operational decision-making than the historical control-room operating model can sustain. Utilities that adopt agent-assisted operational decisioning, properly governed and integrated with existing OMS and SCADA infrastructure, will achieve materially better reliability metrics while accommodating the operational complexity of the transition. Utilities that do not — will face a widening gap between their operational reality and their stakeholder expectations."*

[pause]

**MORGAN:** That last sentence is the moment for utility CIOs. *A widening gap between operational reality and stakeholder expectations.*

### One disagreement

**KEVEN:** Pushback.

**MORGAN:** I want to push on the *agent recommends, dispatcher approves* posture. Because during a major event, the *speed* of decision matters enormously. If the dispatcher has to review every recommendation, the bottleneck shifts from "dispatcher decides" to "dispatcher approves." Same person, marginally faster.

I think the maturity model has to be — *for low-risk, well-patterned dispatches, auto-execute under policy. For high-risk or novel dispatches, dispatcher review.* The split is set by the operations leadership. The audit trail captures everything.

**KEVEN:** I agree, *with the same caveat we used in healthcare* — the *threshold* for auto-execution is set jointly with regulator-facing leadership and reviewed publicly. *And* the dispatcher retains *override and revoke* on auto-executed actions. The dispatcher is never replaced — the dispatcher is *augmented* with high-volume routine decisions executing in parallel with their attention to the high-stakes ones.

**MORGAN:** Yes.

### What to carry forward

**MORGAN:** Two things.

One — *streaming-dominant Services exist outside retail.* The pattern from Episode 7 generalises to industrial operational domains.

Two — *the regulatory dimension of certain Services is part of the value case.* For utilities, SAIDI/SAIFI improvement is *rate-case-relevant.* The financial value isn't just the operational improvement — it's the *regulatory posture* that follows.

**KEVEN:** Next episode — *The IROPs Cascade.* Travel and Hospitality. Airline operations. The most pacy demo in the entire framework.

**MORGAN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn

- **Microsoft Cloud for Sustainability — Energy industry solutions** · [Microsoft Learn](https://learn.microsoft.com/industry/sustainability/)
- **Azure IoT for industrial** · Microsoft Learn

### Microsoft Tech Community blogs

- **"Smart-grid AI on Azure"** · Microsoft Energy Blog
- **"Real-Time Intelligence for utility operations"** · Microsoft Fabric Blog

### Industry context

- **Electric Power Research Institute (EPRI)** · [epri.com](https://www.epri.com/) — utility-industry research
- **Edison Electric Institute** · [eei.org](https://www.eei.org/) — investor-owned utility industry
- **IEEE Power & Energy Society** · grid-engineering publications
- **U.S. Energy Information Administration** · [eia.gov](https://www.eia.gov/) — public energy data
- **Common Information Model (CIM)** · IEC 61970/61968 standards
- *"Grid Modernisation and AI"* · Bain & Company, 2024
- *"The energy transition and operational complexity"* · McKinsey Energy Insights

### From the APEX Trilogy

- **Sellers Guide — *Energy & Resources Practice* chapter**
- **Services Guide — *ER Service Catalog* chapter** — ER-NET-01 in detail
- **Services Guide — *Real-Time Intelligence and Activator* chapter** — the streaming engineering reused from Episode 7

---

**End of Episode 09 · The Energy-Transition Operations Gap**
*≈ 4,900 words · target 30 minutes at conversational pace*
