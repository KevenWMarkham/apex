# Episode 03 · The Connected Vehicle & Aftermarket Plays

**Builds on:** DTNA Eps 1-2 (four brands, manufacturing plays, AXLE canonical) · Trilogy — Services Ep 11 (Contact-Center pattern) · Sellers Ep 6 (Anchor accounts · dealer-network patterns)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: a depot ambient. Truck idling. Radio chatter faint.]

**MARCUS:** I want to start with a phone call. Seven-twelve AM Eastern. The dispatcher at a mid-sized fleet's terminal in Memphis. The phone rings. *"Truck 4172 — Cascadia, three years old, Detroit DD15 — it's parked at a rest stop in Arkansas. Driver says the dashboard lit up with a fault code. Engine derate. He can keep moving but only at fifty-five."* The dispatcher pulls up Detroit Connect on the screen, reads the active fault codes, and starts the triage. *"OK. Get the driver to the nearest Freightliner dealer. Call ahead. Tell them what code we're seeing."*

[pause]

**KEVEN:** And the conversation that happens at the dealer —

**MARCUS:** And the conversation that happens at the dealer is the one the AXLE Practice's connected-vehicle plays exist to compress. Today, that mechanic at the dealer pulls the same fault codes the dispatcher saw, plus more from a deeper diagnostic scan, opens up service manuals, calls back to engineering if needed, makes a judgement call on the repair. *Mean-time-to-confident-diagnosis is the bottleneck.* The fleet customer cares about uptime. The dealer wants throughput. The OEM wants to support the relationship. Everyone wants the same outcome — *fast, confident, durable repair* — and the agent-driven diagnostic story is how the framework delivers it.

That's the through-line for this episode. Six plays touching the *customer-facing* side of DTNA's business — connected vehicle, dealer network, parts, service, fleet experience, in-cab driver experience.

I'm Marcus.

**KEVEN:** I'm Keven Markham. DTNA Account Podcast. Episode Three. *The Connected Vehicle & Aftermarket Plays.*

---

## The conversation

### Why the aftermarket is structurally enormous

**KEVEN:** Frame the why.

**MARCUS:** Two structural facts about commercial trucking that matter for this episode.

*Fact one — the aftermarket is enormous.* In commercial trucking, the OEM sells a truck at low single-digit margins; the OEM makes its long-term economics on *parts and service* across the truck's 8-12 year operating life. *Aftermarket gross margin is multiples of new-truck margin per unit.* Anything that improves aftermarket performance — parts availability, service productivity, customer retention through the lifecycle — flows almost directly to profit.

*Fact two — the connected vehicle is the data backbone of aftermarket.* Detroit Connect generates continuous telemetry across the field fleet. Every fault code, every maintenance event, every operational metric. *The data is there.* What hasn't existed until recently is the agentic layer that composes the field data with manufacturing build records, dealer service history, parts inventory, and fleet-customer operational context — to deliver decisions at the speed customers expect.

The six plays in this episode are *all about composing the customer-facing data into decisions.*

### Play one — Connected Vehicle Diagnostic Acceleration (AXLE-CONNVEH-02)

**MARCUS:** Play one. Connected diagnostic acceleration.

**KEVEN:** The flagship customer-facing play. AXLE-CONNVEH-02.

The DTNA context. Detroit Connect generates fault codes, telematics, and operational events from the field. *Roughly hundreds of thousands of trucks in active service generating continuous telemetry.* When a fault appears, the diagnostic question is — *what is most likely failing, what should the mechanic check first, what parts will be needed, how confident are we?*

The pain point. *Diagnostic latency at the service bay.* The mechanic's first-touch diagnostic is judgement-driven, supported by service manuals and dealer-knowledge-base systems. *Confident-diagnostic time varies enormously by mechanic experience.* Senior mechanics diagnose faster and more confidently than junior. *Knowledge transfer is slow.*

The agent strategy. The diagnostic agent reads the connected-vehicle fault signal plus the VIN's full build record, service history, mileage and operational profile, and similar-pattern historical resolutions. *Recommends most-likely-root-cause with confidence score.* Surfaces the *recommended diagnostic sequence* — which scans to run, which components to inspect, in what order. Identifies *parts likely needed* so the service writer can pre-position inventory.

*Mechanic approves and acts.* The agent doesn't replace the mechanic; the agent *gives the mechanic senior-mechanic-quality first-touch reasoning.*

The architectural shape. Four AXLE canonical families joining on VIN (the same Silver foundation as Play 1 from Episode 2 — the warranty agent). Gold mart shapes per-VIN diagnostic-context views. The agent's MCP tools span fault signal, build record, service history, parts inventory.

The KPI signal. *Mean-time-to-confident-diagnosis 40-60 percent reduction.* *First-time-fix rate +15-25 percentage points.* *Parts-pre-positioned correctness +30 percent* — fewer cases where the mechanic discovers mid-repair that a needed part is back-ordered.

**MARCUS:** Why this is a high-fit Wave 1 alternative to the warranty play —

**KEVEN:** Three reasons we touched on in Ep 1. *Detroit Connect data foundation is mature. Customer-facing benefit is faster and more visible. Strategic momentum is aligned* — DTNA leadership is already prioritising connected vehicle. Wave 1 here builds on existing investment rather than creating a new initiative.

### Play two — Dealer Network Performance Analytics (AXLE-DEALER-03)

**MARCUS:** Play two. Dealer network performance.

**KEVEN:** DTNA's dealer network — *one of the largest commercial-truck dealer networks in North America.* Cumulative footprint spans hundreds of dealer locations across the U.S. and Canada. *Dealer performance varies enormously across the network.* Top-decile dealers operate at scale and profitability that bottom-decile dealers can't match.

The pain point. *Dealer-performance variance.* The OEM wants the whole network performing at top-decile levels — better service for customers, better profitability for dealers (which keeps them committed long-term), better aftermarket revenue capture. *Current dealer-performance management is mostly quarterly reviews with regional managers.* The signal is too slow to drive intervention.

The agent strategy. Dealer-performance agent reads continuously across dealer service throughput, parts revenue, customer-satisfaction signal, technician productivity, financial performance. *Identifies dealers trending toward at-risk* and *dealers performing exceptionally well.* Recommends regional intervention — coaching, additional training, capital investment support, or escalation. *Regional management approves.*

The architectural shape. Cross-system canonical at Silver — dealer financial, operational, customer-facing. Gold per-dealer composite-health view. MCP tools span dealer-business-system data.

The KPI signal. *Dealer-network performance distribution compression* — bottom-decile improvement specifically. *Aftermarket revenue capture per dealer +10-15 percent on cohort.* *Dealer-customer satisfaction improvement.*

**MARCUS:** And the cross-Practice pattern —

**KEVEN:** *This is the same architectural pattern as the ICE Practice dealer-network play.* DTNA dealer plays and heavy-equipment-OEM dealer plays share underlying canonical and architecture. *The cross-Practice reuse compounds.* A team that builds dealer-performance analytics for DTNA can deploy it at heavy-equipment-OEM clients with substantially shared engineering.

### Play three — Predictive Parts Demand Forecasting (ICE-AFTERMKT-05)

**KEVEN:** Play three. Parts demand forecasting.

**MARCUS:** Parts demand at the dealer is *the most operationally important number in aftermarket profitability.* Parts available when the customer needs them — fast service, satisfied customer, captured revenue. Parts not available — service delay, customer dissatisfaction, lost revenue.

The pain point. *Parts demand forecasting is cyclical, seasonal, and event-driven.* Maintenance schedules, seasonal patterns (winter vs summer), regional patterns, emerging-issue-driven demand surges (a fault pattern emerges and parts demand spikes for that component). *Current forecasting is largely statistical with planner overrides.* Misses on demand surges produce service delays.

The agent strategy. Parts demand agent reads continuously across — *historical demand patterns, current field-fleet operational signal, emerging-issue signal from quality and warranty data, seasonal patterns, dealer-specific demand.* Forecasts demand at multiple horizons. *Parts planning team approves inventory adjustments.*

The architectural shape. Cross-canonical access including field signal, supply chain, dealer activity. Gold per-part per-location demand forecast features.

The KPI signal. *Parts availability +5-10 percentage points* on covered SKUs. *Inventory-carrying-cost optimisation* — better forecasting reduces over-stocking. *Demand-surge response time compression* — the agent identifies an emerging issue and recommends parts pre-positioning before the surge fully arrives.

### Play four — Service-Bay Agent Assist for Mechanics

**MARCUS:** Play four. Service-bay agent assist.

**KEVEN:** Different from Play 1 (Connected Diagnostic) — *Play 4 is broader.* Diagnostic is the entry; the full repair workflow extends through tear-down, parts request, repair execution, validation, customer hand-off. *The agent assists throughout.*

The pain point. *Mechanic productivity variance.* Even given diagnosis, repair execution varies — service procedures, special-tool use, validation. New or less-experienced mechanics learn slowly. Senior mechanics become bottlenecks for complex repairs. *Knowledge transfer across the technician base is structural.*

The agent strategy. *Plant-floor agent-assist pattern applied to the service bay.* Agent assists the mechanic in real time — surfaces relevant service procedures, identifies special-tool requirements, drafts repair documentation, captures repair outcome for downstream learning. *Mechanic approves and executes.*

The architectural shape. The same agent-assist pattern from the Services Podcast contact-center episode — *narrowly applied to commercial-truck service.* MCP tool surface spans service procedures, parts catalog, telematics, prior similar repairs.

The KPI signal. *Repair-cycle compression 15-25 percent on covered repair types.* *First-time-fix rate +10-15 points.* *Mechanic productivity improvement.* *Customer wait-time compression* — directly affects fleet-customer satisfaction with the dealer service experience.

**KEVEN:** And the cross-Practice synthesis —

**MARCUS:** This is now the *third place* the agent-assist pattern has shown up in this Account Team's content — contact center, plant floor, service bay. *Disney Account Team uses the same pattern in IT service-desk.* The Sellers Handbook calls this out — *the agent-as-information-composer-for-the-operator pattern is the most-replicated APEX Service.* DTNA captures it three different times across this podcast.

### Play five — Fleet Customer Experience and Asset Utilisation

**MARCUS:** Play five. Fleet customer experience.

**KEVEN:** *This play is for the large fleet customers* who buy hundreds of trucks per year from DTNA. UPS, FedEx, J.B. Hunt, Schneider, Werner, Walmart Transportation. The relationship with these fleets is strategic — *multi-year frame agreements, volume commitments, joint engineering on spec'd configurations.* And the relationship can intensify or deteriorate based on the customer's *experience* with the trucks in operation.

The pain point. *Fleet customers want fleet-level operational intelligence.* Which trucks are at-risk for downtime in the next 30 days. Which routes are causing higher-than-expected maintenance. Which driver behaviours correlate with maintenance costs. Which Cascadia configurations are performing best. *DTNA has the data through Detroit Connect.* Composing it for fleet-customer insight has been partial; agentic AI compresses the composition.

The agent strategy. Fleet-customer-experience agent reads continuously across the customer's fleet data, identifies emerging operational concerns, surfaces them to the customer's fleet manager *and* to DTNA's account-team and dealer counterparts. *Joint operations conversations are agent-prepared.* The customer feels DTNA as a *partner* — not just an OEM that sold them trucks.

The architectural shape. Customer-side Detroit Connect data integrated with the customer's fleet management system (where possible). Gold per-customer-fleet operational view. The architecture has to respect *customer data sovereignty* — the customer's operational data is theirs; DTNA accesses with permission.

The KPI signal. *Fleet customer retention through frame-agreement cycles.* *Volume commitment increases.* *Per-customer aftermarket revenue capture lift.* *Customer NPS / advocacy lift.* These are slower-moving but strategically important metrics.

**KEVEN:** Note the L4 connection from the ladder —

**MARCUS:** This play is the *L4 transformation* play at DTNA. *Fleet-customer-experience transformation* is what L4 looks like in trucking. We'll come back to it in Episode 4.

### Play six — Driver-Facing In-Cab Assistance

**KEVEN:** Play six. Driver-facing in-cab assistance.

**MARCUS:** The driver is the daily user of the Cascadia. Driver experience affects *recruiting, retention, productivity, and safety* across the fleet customer base. *Driver shortage* has been a persistent industry challenge.

The pain point. *In-cab driver experience is functional but not assistive.* Drivers manage routing, hours-of-service compliance, dispatch communication, maintenance reporting, fuel optimisation — much of it through systems that don't compose well. The cognitive load is real.

The agent strategy. In-cab assistant agent provides contextual support — *route optimisation given current conditions, hours-of-service guidance, fuel-efficiency coaching, predictive-maintenance alerts directly to the driver, simplified communication with dispatch.* Driver retains full authority; agent assists.

The architectural shape. Edge-capable agent integrated with Detroit Connect telematics, the dispatch system, and the in-cab interface. *Different from the prior plays in that the agent runs partly at the edge* (in the truck) rather than entirely in the cloud.

The KPI signal. *Driver-satisfaction metrics improvement.* *Driver-retention rate lift on covered fleets.* *Fuel efficiency improvement +1-3 percent* — small but at fleet scale millions of dollars annually. *Hours-of-service compliance accuracy improvement.*

**KEVEN:** And the strategic frame —

**MARCUS:** *This is the play that touches the autonomy strategic theme.* The in-cab assistant agent is, in some sense, the *bridge* between today's driver-operated trucks and tomorrow's autonomous trucks. Skills, capabilities, and trust developed in driver-assistance applications transfer to autonomous-operation contexts. *Long-term strategic frame.*

### A reading I want to do

**MARCUS:** I want to read from an industry analysis on commercial-truck aftermarket economics.

**KEVEN:** Read it.

**MARCUS:** [reading, paraphrased]

*"Commercial-vehicle aftermarket revenue is structurally several times more profitable per unit than new-vehicle revenue. Yet aftermarket performance varies dramatically across OEM dealer networks, even within the same brand. The OEMs that deploy agentic AI across their connected-vehicle data, dealer-operations data, and fleet-customer data — composing the streams into operational decisions in real time — will capture materially higher aftermarket revenue, build stickier fleet-customer relationships, and ultimately operate higher-multiple businesses than competitors that do not."*

[pause]

**KEVEN:** *Higher-multiple businesses.* That's the CFO frame. The aftermarket isn't just a profit line; it's a *valuation argument.*

### One disagreement

**KEVEN:** Pushback.

**MARCUS:** Let me push on the *driver-facing in-cab assistant* play. *I think this play is too far ahead of where DTNA's strategic clock currently is.* The in-cab interface is a long-cycle product investment. Adding agentic capability to it requires close integration with the in-cab compute platform, the telematics modem, the driver-display software — all of which have multi-year product roadmaps. *The agent layer can't run faster than the underlying product platform allows.*

I'd downgrade Play 6 from a typical Wave 2 play to a *Wave 3+ strategic frame.* Real, important, but not in the next-three-year Account Team conversation.

**KEVEN:** And the consequence for the Account Team —

**MARCUS:** *Don't lead with the in-cab assistant in fleet-customer conversations* even though it sounds intuitive. Lead with the connected-vehicle diagnostic play (Play 1) because the diagnostic outcome benefits both driver and fleet operator. *The in-cab story is the long-tail play* the Account Team mentions when the conversation turns to autonomy and the strategic future. Position appropriately.

**KEVEN:** Agree. *Plays 1-5 are Wave 1-2 territory. Play 6 is Wave 3+ strategic frame.*

### What to carry forward

**KEVEN:** Three things.

One — *six connected-vehicle and aftermarket plays, anchored on Detroit Connect plus dealer-network and aftermarket data.* The compounding-asset thesis applies — Plays 1, 2, 4 in particular share architectural foundation with the manufacturing-and-quality plays from Episode 2.

Two — *Connected Vehicle Diagnostic Acceleration is the high-fit Wave 1 alternative to Zero Day Warranty.* For Account Teams with strong CTO or VP-Connected-Vehicle relationships, this is the right Wave 1 entry.

Three — *Fleet Customer Experience (Play 5) is the L4 transformation play* — the fleet-customer-side equivalent of B2C transformation. Strategic, long-term, multi-year.

**MARCUS:** Next episode — *The Ladder for DTNA.* Four-level ladder applied to DTNA. L1 wedge heatmap across brands. L2 Wave 1 candidates. L3 AXLE Practice CoE inside DTNA. L4 fleet-customer transformation. Plus the strategic frames of electrification and autonomy.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn

- **Microsoft Cloud for Automotive** · Microsoft Learn
- **Azure IoT for connected vehicle** · Microsoft Learn
- **Dynamics 365 Field Service** · Microsoft Learn — relevant for service-bay agent assist
- **Microsoft Fabric Real-Time Intelligence** · Microsoft Learn

### Industry context

- **American Trucking Associations (ATA) Technology & Maintenance Council (TMC)** — connected-vehicle and aftermarket benchmarks · [trucking.org](https://www.trucking.org/)
- **TMW Systems / Trimble Transportation** — dealer-management and fleet-management platforms
- **Detroit Connect product documentation** — DTNA public materials
- *"Commercial vehicle aftermarket trends"* — ACT Research and FTR Transportation Intelligence
- *"Dealer network productivity in commercial trucking"* — industry analyst publications

### From the APEX Trilogy podcasts

- **Services Podcast Ep 11 — *The Contact-Center Labour Squeeze*** — the agent-assist pattern applied here three times
- **Sellers Podcast Ep 5 — *Anchor Accounts, Part 1*** — dealer-network anchor pattern
- **Sellers Podcast Ep 6 — *The Warranty Cost Spiral* (Services Podcast)** — the architectural foundation shared with Connected Diagnostic

---

**End of Episode 03 · The Connected Vehicle & Aftermarket Plays**
*≈ 5,600 words · target 30 minutes at conversational pace*
