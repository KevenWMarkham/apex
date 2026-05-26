# Episode 02 · Four Data Domains

**Builds on:** Toyota Ep 1 (Zero Day Warranty idea) · Services Podcast Eps 3-4 (medallion architecture and agent foundation) · AXLE Practice (BRML/CVML/QEML/AAML schema families)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: a whiteboard. A marker squeaking. A data architect mid-sentence.]

**MIA:** I want to start in a small conference room, somewhere in Plano. Two days after the warranty cluster on a Tuesday night in Georgetown. A data architect is at a whiteboard. There are coffee cups. There are two quality engineers, a manufacturing-IT lead, and someone from Toyota Connected on the call screen. The architect is drawing.

[pause]

**KEVEN:** What is she drawing.

**MIA:** *Four boxes.* She draws them in a row across the whiteboard. The first box she labels *vehicle build record.* The second box she labels *connected vehicle warranty data.* The third box she labels *quality events on the line.* The fourth box she labels *assembly line telemetry.*

Then she draws a line under all four boxes and writes one word — *VIN.* And she draws an arrow from the VIN line up to a fifth box that she labels *the agent.*

The room is quiet. Somebody says — *we already think this way.* Somebody else says — *we just don't compose this way.* The architect nods. *That's the whole episode.*

[pause]

**KEVEN:** And the question I want to put on the table for the next thirty minutes —

**MIA:** Which of those four boxes is going to produce the most causal signal once the agent can reach across all of them. *Hold that question.* We'll come back to it at the end. I have a strong answer; Keven has a different one; the listener can decide.

**KEVEN:** *The Zero Day Warranty Podcast. Episode Two. Four Data Domains.* I'm Keven Markham.

**MIA:** I'm Mia. Let's get into it.

---

## The conversation

### The four-domain hypothesis

**KEVEN:** Set the stage. In Episode 1 we landed on a hypothesis — four data domains, composed per VIN, with an audit-ready agent reading across them. *Why these four?*

**MIA:** Because *these four are how Toyota already thinks.* That's the only honest reason. If we walked into a room at TMNA and proposed five domains, or three, the conversation would stall on the schema fight. When we walk in proposing four — *vehicle build record, connected vehicle warranty data, quality events on the line, assembly line telemetry* — heads nod. Those four already map to four organizational boundaries inside Toyota.

**KEVEN:** Name the boundaries.

**MIA:** *The vehicle build record* belongs to Manufacturing — the per-plant manufacturing-IT organization that owns the build systems on the line. *Connected vehicle warranty data* belongs to Toyota Connected North America — the subsidiary that runs the connected-vehicle data estate. *Quality events on the line* belongs to plant Quality — the operators, inspectors, and quality engineers who own the in-process signal. *Assembly line telemetry* belongs to Production Engineering and to Asset Management — the people who instrument and maintain the equipment itself.

Four data domains. Four custodians. *And historically — four separate data conversations.* The agent doesn't take ownership away from any of those teams. The agent makes their data composable.

**KEVEN:** And the hypothesis. State it the way the Account Team should state it.

**MIA:** *Compose those four domains at per-VIN granularity, on a single canonical foundation, and you unlock Zero Day Warranty.* The composition is the unlock. Not any one of the four — *the joining of all four.* The agent's job is to reason across the join. The platform's job is to make the join cheap, repeatable, and governed.

**KEVEN:** And the eight-to-twelve-weeks number.

**MIA:** The eight to twelve weeks is *almost entirely the join.* The senior engineers in Ep 1 — Quality, Manufacturing Engineering, Supplier Quality, Toyota Connected, Warranty Engineering, Finance — most of their calendar time goes to *getting the four domains lined up against the VINs in the cluster.* The root-cause judgement, once the data is composed, is days not weeks. *The reconciliation toil is the weeks.* Take the toil away and the calendar collapses.

**KEVEN:** So this episode is the architecture of the toil-removal.

**MIA:** This episode is *the data foundation* that the agent in Episode 3 stands on. We walk the four domains one at a time. We walk how they land on Microsoft Fabric. We walk the medallion architecture and why the canonical schemas anchor where they anchor. And we walk what a per-VIN composed view actually looks like.

### The vehicle build record domain

**KEVEN:** Start with the first one. *The vehicle build record domain.*

**MIA:** This is the foundational layer. *Every VIN's complete factory history.* When the vehicle started down the line, when it left, which plant, which line within the plant, which station-by-station path, which shift, which tool, which supplier lot for every installed part, which operator-cohort was at each station. That's the per-VIN truth of the build.

**KEVEN:** And the systems it lives in today.

**MIA:** Multiple systems. *MES* — the manufacturing execution system that tracks the vehicle through stations. *Quality-traceability systems* that tie torque readings and dimensional measurements back to the VIN. *Supplier-traceability systems* that record which lot of which part was installed on which vehicle — sometimes by serial number, sometimes by lot range. *Asset-management systems* that record which tool was at which station at which time. *Workforce systems* that record which operator cohort was on which shift at which station.

It is not one system. It is the *composed view across those systems* that is the vehicle build record. And today, the composed view exists — but it is composed *by hand*, against a specific VIN list, when somebody opens a ticket.

**KEVEN:** Walk why this matters for warranty.

**MIA:** Take the cluster from Episode 1. Three thousand vehicles. Sensor harness intermittent failure mode. The clusters spans build weeks 12 through 14. The engineer at her desk at eleven o'clock at night needs to answer one question — *what was different about those builds?*

*Different* is the entire question. Different from what? Different from the vehicles built in weeks 9, 10, 11, that did *not* show the failure. Different from the vehicles built in weeks 15, 16, that also did not show the failure. The differences live in the build record. *A specific torque setting on a specific station that drifted that week. A specific supplier lot of harness that arrived and was consumed in that window. A specific tool that approached end-of-life on its calibration cycle. A specific operator-cohort rotation that put new operators at a station where the standard work has a known difficulty curve.*

Any of those could be the cause. *All of those live in the build record domain.* And until the agent can ask the question across all of them at once, the senior engineers ask it by hand, one dimension at a time.

**KEVEN:** And the operator-cohort dimension. We have to handle this carefully.

**MIA:** *Carefully.* The build record knows which operator cohort was at which station for which shift. That dimension is analytically important — operator-cohort rotation is a real driver of variance in build quality, and Toyota's training and rotation discipline is one of the strengths of TPS. But the dimension is also *culturally sensitive.* Toyota's culture treats the operator with care. The agent must compose this dimension *with safeguards.*

What safeguards. *The agent surfaces cohort patterns, not individual blame.* The agent's output reads *operators in their first thirty days at this station experience higher variance on this torque step* — not *operator A is the cause of the defect.* The framing is training, tooling, station ergonomics, standard-work clarity. *Never individual.* The operator's dignity is non-negotiable. Episode 1 said that; it stays true here.

**KEVEN:** And the granularity.

**MIA:** *Per-station, per-shift, per-tool, per-lot, per-cohort.* Each row of the build record is one VIN at one station at one moment. Four thousand VINs in a cluster, twenty-five stations on the relevant portion of the line — that's a hundred thousand row-events for one investigation. The agent loves that. The senior engineer with a spreadsheet does not.

**KEVEN:** And one more thing about this domain — the supplier-lot dimension.

**MIA:** The supplier-lot dimension is *one of the highest-leverage signals in the build record.* When a warranty cluster traces to a specific lot of a specific part from a specific supplier within a specific arrival window — that's the chargeback evidence we talked about in Episode 1. *The supplier lot lives in the build record.* Composed with the field-claim data, you have the chargeback case.

We'll come back to supplier-lot in the disagreement at the end of this episode. *Hold the thought.*

### The connected vehicle warranty data domain

**KEVEN:** Domain two. *Connected vehicle warranty data.*

**MIA:** *Connected vehicles produce field signal.* When a Camry or a Tundra or a Highlander in the field experiences a fault, the vehicle reports. Modern Toyotas are highly instrumented — diagnostic trouble codes, sensor traces, environmental telemetry, mileage at the moment of fault, the conditions the vehicle was operating under. *All of that lands somewhere.*

For Toyota, that somewhere is Toyota Connected North America. Toyota Connected runs on Azure. The data estate sits on Microsoft cloud today, *which is one of the architectural reasons the platform discussion in this podcast is what it is.* The infrastructure to land and reason against connected-vehicle data is already in place. The question is how to compose it with the other three domains.

**KEVEN:** And the kinds of signal we get.

**MIA:** Three layers. *Warranty claim filings* — the dealer-coded record. Customer brought the car in, dealer diagnosed, repair was performed, the labour code and parts code got recorded. That's the traditional warranty data and it's the layer most people think of first. *Field telemetry* — what the vehicle actually reported around the moment of failure. Sensor readings, fault codes, the time-series in the seconds and minutes before and after. *Customer-experience signal* — complaint categorization, customer-survey responses, the qualitative side of the claim.

The traditional warranty claim is the *summary.* The field telemetry is the *evidence.* The customer signal is the *context.* The agent reads all three.

**KEVEN:** And the per-VIN tie.

**MIA:** *The VIN is the universal key.* Every field claim ties back to a specific VIN. Every telemetry signal ties back to the same VIN. *That VIN is the same VIN that has a build record.* The join is mechanical — *VIN to VIN.* What's difficult today is not the join in concept; what's difficult is that the connected-vehicle warranty data lives in a different building, in a different system, owned by a different team, with a different intake process from the build record data. The data is joinable in principle. It is not joined in practice. *That is what the canonical foundation fixes.*

**KEVEN:** And the time dimension matters here too.

**MIA:** It matters a lot. *Time-from-build-to-claim* is one of the most diagnostic features in the entire warranty data set. A failure mode that surfaces at three months tells you something different from one that surfaces at three years. A failure mode that surfaces only after the vehicle has experienced a specific environmental condition — extreme cold, extreme heat, sustained vibration — tells you something else again. The connected vehicle reports those conditions. The agent reasons across them.

**KEVEN:** And how rich the signal is now versus ten years ago.

**MIA:** *Dramatically richer.* Ten years ago a warranty claim was a labour code, a parts code, a free-text customer-complaint string, and a mileage number. Today the same claim sits next to *hundreds* of telemetry channels recorded around the event. The Account Team should be clear-eyed about this — Toyota has not been standing still. The connected-vehicle data estate at Toyota Connected has been built up over years. *The raw material is there.* What is missing is the *composition* with the factory minute. That's what this episode is about.

### The quality events on the line domain

**KEVEN:** Domain three. *Quality events on the line.*

**MIA:** This is the *in-process* signal. What happened *while* the vehicle was being built — not after it shipped. Every inspection, every measurement, every defect callout, every rework, every Statistical Process Control reading, every andon-cord event during the build.

**KEVEN:** Walk Statistical Process Control briefly.

**MIA:** *SPC* — Statistical Process Control. The plant-floor discipline of continuously measuring critical process parameters — a torque, a dimension, a clearance, a temperature — and watching the distribution. When the distribution drifts out of control limits, the line knows. SPC has been an automotive manufacturing discipline for decades. *Toyota's quality teams live in SPC charts.* The data is there.

The same goes for *dimensional inspections* — every critical measurement at every station. *Visual-system catches* — increasingly, machine-vision systems on the line catch surface or assembly defects automatically. *End-of-line audits* — the final inspection before the vehicle leaves the plant. *Holds and rework* — when a vehicle is pulled off the line for correction. *Andon events* — when an operator stops the line.

Every one of those is a row of quality signal tied to a VIN at a moment.

**KEVEN:** And where the data lives today.

**MIA:** *Largely locally, per plant.* Each plant has its own quality systems, its own SPC infrastructure, its own holds-and-rework tracking. *The data is rich.* The composition across plants is uneven. A pattern that emerges across multiple plants — a torque-step variance that shows up at three sites, not just one — is *very* diagnostic. But seeing the pattern requires the data to be composed across plants, *which it largely is not today.*

**KEVEN:** And the pattern detection.

**MIA:** This is where this domain *earns its keep.* Compose the quality-event signal across plants, across shifts, across stations. *The cross-station, cross-shift, cross-plant pattern detector* is what the composed quality-event domain becomes. A specific defect type starting to drift up at three plants over the last two weeks is the kind of pattern that — in the current state — gets noticed eight weeks later, after the field claims start rolling in. In the composed state, the pattern is visible *while it is happening.*

**KEVEN:** And the relationship to Jidoka.

**MIA:** *Direct.* Jidoka is — when a defect is detected, the line stops, and the problem is fixed at source. Today, Jidoka operates at the *station* level. The operator at the station catches the defect, pulls the andon, the line stops. The composed quality-event domain is — *Jidoka at the network level.* A defect signal accumulating across stations, shifts, and plants is itself an andon. *The agent raises the andon for the patterns no single station can see.* It is not replacing the operator's andon authority. *It is adding a layer of pattern detection above it.*

**KEVEN:** And the operators get the credit for the original andon discipline.

**MIA:** *Always.* The agent reads what the operators already produce. Without the operators pulling the andons, without the inspectors recording the measurements, without the SPC charts being maintained — the data the agent reasons against does not exist. *The agent stands on the operators' work.* The Account Team should never frame this as the agent doing what the operators do not. The agent does what *no human can do — see the signal across the whole network at once.*

### The assembly line telemetry domain

**KEVEN:** Domain four. *Assembly line telemetry.*

**MIA:** This is the equipment side. The *operational-technology* layer — OT, as opposed to IT. The data the production-line equipment itself emits while it is running. *Tool torque-and-angle traces. Robotic-cell cycle times. Conveyor speeds. Fixture state. Environmental conditions — humidity, temperature, vibration. Maintenance events on the equipment itself.*

If the quality-event domain is *what the inspector saw*, the assembly-line-telemetry domain is *what the equipment was doing while the inspector was looking.* It is the substrate beneath the quality signal.

**KEVEN:** And where it lives today.

**MIA:** *Plant historians.* In automotive manufacturing the OT data has historically been captured in time-series historians on the plant floor. AspenTech IP.21 is one. OSIsoft PI is another. Newer systems are emerging that sit closer to the cloud, but the historian remains the workhorse for OT signal. *These systems are excellent at what they do — high-frequency time-series storage, fast retrieval of equipment traces.* They are not excellent at being joined to the connected-vehicle warranty data sitting in Toyota Connected's Azure estate.

**KEVEN:** That's the integration gap.

**MIA:** That is the integration gap. *Bringing the OT signal into joinable form with the IT signal* is technical work — protocol translation, time-series resampling, VIN-to-equipment alignment by station-and-time-stamp. It is *not* trivial. But it is also *not novel.* OPC UA is the open standard for OT-to-IT integration. The Microsoft platform has well-established patterns for ingesting OPC UA into Fabric. *The work is known. The work has not been done at the Toyota network scale.*

**KEVEN:** And why it matters for warranty.

**MIA:** Take the harness cluster again. The build record tells you the vehicle was at station 14 at 02:47 on a Wednesday. The quality event tells you no defect was recorded at that moment. *The assembly line telemetry tells you the torque tool on station 14 was reading at the high end of its calibration band at 02:47 on that Wednesday — and had been drifting for the previous six hours.* Suddenly the cluster is explainable. *The defect that no inspector caught was traceable through the OT signal once it was joined to the build record.*

That join is the high-leverage move. Today it takes days of manual reconciliation. Composed in Fabric with the canonical schemas at Silver, the join is a query.

**KEVEN:** And the equipment-state side.

**MIA:** *Equipment events themselves are diagnostic.* A robotic cell that flagged a calibration alert and got reset by a maintenance technician during the relevant build window is a row of signal. A fixture changeover that happened mid-shift — when normally changeovers happen between shifts — is a row of signal. A conveyor speed adjustment for a downstream bottleneck that subtly affected upstream station dwell times is a row of signal.

The equipment is *talking.* Today nobody is listening across the whole network. The composed assembly-line-telemetry domain is what enables the agent to listen.

### Why these four, not three or five

**KEVEN:** Step back. *Why these four, not three or five.*

**MIA:** Because four maps cleanly to Toyota's actual organization. *Three* loses something. *Five* conflates.

**KEVEN:** Walk the three case first.

**MIA:** If you collapse to three domains, the natural collapse is to fold assembly line telemetry into either the quality-event domain or the build-record domain. Either way you lose. *Folded into quality events*, you lose the equipment-state signal that lives independent of any specific inspection — the tool drift that nobody flagged because it never crossed the alarm threshold. *Folded into the build record*, you lose the time-series character of the OT signal — it becomes a per-station snapshot rather than a continuous trace. Both collapses destroy information. The fourth domain earns its place by *catching the signal the other three would miss.*

And that fourth domain is also where the Day-0 prevention conversation enters in Episode 4. *Inline vision at the station* — the NVIDIA layer — extends the assembly-line-telemetry domain at the inspection-station level. If we don't have a clean fourth domain, the NVIDIA composition gets architecturally awkward.

**KEVEN:** And the five case.

**MIA:** If you add a fifth, the natural fifth is *supplier-quality scorecards.* A supplier-managed view of how the supplier's own production is performing. *And the reason not to make this a fifth domain* is — it conflates a Toyota-internal signal with a vendor-managed signal. The supplier-quality scorecard is the supplier's representation of their own data. *Toyota's internal record of what arrived* lives in the build record, in the lot-level traceability data. That's a Toyota-controlled signal. *The supplier scorecard is useful context* — but it belongs as a *supplementary feed*, not as a fifth canonical domain.

Make it a fifth domain and you start fighting governance battles you don't need to fight. Keep it as a supplementary feed alongside the four, and the canonical foundation stays clean.

**KEVEN:** And these four stair-step into the next episode.

**MIA:** *Directly.* The four domains we just walked become the canonical layer in the medallion architecture. *Silver* — the canonical layer in Microsoft Fabric's medallion pattern — is where these four domains live. *Gold* is where the agent reaches in for per-VIN composed views. *Bronze* is the raw landing per source. We're about to walk that.

### Medallion on OneLake — Bronze, Silver, Gold

**KEVEN:** OK. Bring in the Microsoft Fabric piece. The medallion architecture.

**MIA:** *Microsoft Fabric is the unified data platform.* OneLake is the underlying lake — a single tenant-resident storage layer that every Fabric workload reads from and writes to. *The medallion architecture is the layered pattern within OneLake.* Three layers. Bronze, Silver, Gold.

**KEVEN:** Define each.

**MIA:** *Bronze.* The raw landing zone. Source data lands in Bronze as-is — with minimal transformation, source schemas preserved. The build record arrives in Bronze in whatever shape Manufacturing IT's source systems produce. The connected-vehicle warranty data arrives from Toyota Connected in the shape Toyota Connected emits it. The quality-event data arrives per plant in plant-native form. The assembly-line telemetry arrives from the historians in their native time-series form.

Bronze is *append-only.* You never edit Bronze. You preserve the raw evidence. *Audit-ready posture starts at Bronze* — every record has a provenance, every record has an arrival timestamp, every record is traceable back to its source system.

**KEVEN:** *Silver.*

**MIA:** Silver is *the canonical layer.* This is the load-bearing one. *Silver enforces the cross-system canonical form for each of the four domains.* The build record has one canonical schema at Silver — regardless of which plant's MES it arrived from, the Silver representation is the same. The connected-vehicle warranty data has one canonical schema at Silver — regardless of which Toyota Connected data feed produced it. Same for quality events. Same for assembly line telemetry.

*Silver is where the four domains become four canonical domains.* This is the point I want the Account Team to internalize most cleanly. *Canonical anchors at Silver. Not at Gold.*

**KEVEN:** Say more about why.

**MIA:** Two reasons. *One — Silver is where the cross-system reconciliation happens once.* If you anchored canonical at Gold, every Gold query would have to do the reconciliation work. With canonical at Silver, the reconciliation is paid for once at ingest and amortized across every downstream use. *Two — Silver is the layer that survives.* Gold views compose for specific query patterns; those query patterns change. A Gold view that worked for the warranty agent today might not serve the predictive-maintenance use case next year. *Silver is stable. Silver is the canonical record.* Gold is the working surface.

**KEVEN:** And *Gold.*

**MIA:** *Gold* is where the data is *composed for the agent's query patterns.* Per-VIN joinable composite views. Per-cohort aggregations. Per-supplier-lot rollups. The shapes the agent needs to reason against, materialized for fast access. Gold is opinionated — *Gold is shaped to the question.* The warranty agent needs per-VIN composed views; Gold builds them. A future production-planning agent might need different shapes; Gold builds those too. Same Silver, different Gold projections.

**KEVEN:** And the Microsoft Industry Cloud for Manufacturing alignment.

**MIA:** *This pattern is not invented for Toyota.* The Common Data Model that ships inside Microsoft Industry Cloud for Manufacturing already organizes manufacturing data along very similar lines. *Toyota is not signing up to a bespoke schema family* — Toyota is signing up to the pattern Microsoft has built the manufacturing industry cloud around. Which means the Silver canonical schemas at Toyota inherit decades of manufacturing-data-model thinking, not a Deloitte-bespoke shape. *That matters for adoption.* The platform speaks the domain language; the domain doesn't bend to the platform.

**KEVEN:** And the governance posture.

**MIA:** *Microsoft Purview* sits over the whole medallion. Bronze, Silver, Gold — all governed end-to-end. Lineage is visible from the agent's Gold-view consumption back to the Bronze source landing. Sensitivity classification, access policies, audit trails — Purview handles all of it. *That governance posture is the architectural reason the agent in Episode 3 can be audit-ready.* We're laying the foundation here; Episode 3 walks the audit chain on top.

### Per-VIN joinability at the Gold layer

**KEVEN:** And the per-VIN joinable framing. Walk what that actually means.

**MIA:** *Every Gold view is queryable by VIN.* That's the operational commitment. The agent's reasoning pattern is — *given this VIN, what does the world look like across all four domains?* The Gold layer answers that question in one query.

**KEVEN:** Walk an example.

**MIA:** Take a specific VIN in our harness cluster. *Camry, built at Toyota Motor Manufacturing Kentucky, week 13.* The agent issues a query — *give me this VIN's composed view.* Gold returns — *the complete build record for that VIN. The connected-vehicle warranty data for that VIN, with field telemetry and any claim filings. The quality events captured during that VIN's build. The assembly-line telemetry around the windows when that VIN was at each station.* All four domains, joined on VIN, returned as one composite. *That is one row of evidence in the agent's reasoning.*

**KEVEN:** And then scale that up.

**MIA:** Now do it for four thousand VINs in the cluster. Four thousand composite rows. The agent runs cohort analysis across them — *which combination of build conditions, supplier lots, quality events, and equipment states correlates with the failure mode at statistical significance.* That's the reasoning we talked about in Episode 1. The Gold layer is what makes the reasoning possible.

**KEVEN:** And the latency.

**MIA:** The Gold views are pre-composed for the agent's read patterns. The query that returns a per-VIN composite is *seconds, not minutes.* The query that returns four thousand of them is still seconds — Fabric handles that fan-out natively. *The eight-to-twelve-weeks-of-toil compresses because the join is no longer manual.* That compression *is* the Zero Day Warranty unlock. Everything else in the architecture is in service of it.

**KEVEN:** And the agent's reach.

**MIA:** *The agent only reads Gold.* That's a discipline. The agent does not query Silver directly. The agent does not query Bronze. *Gold is the agent's surface.* When the agent needs a new shape, the platform team builds a new Gold view. Silver stays clean; Bronze stays raw; Gold absorbs the query-pattern evolution. *This is how the platform stays governable as the agent's reasoning grows.*

### Microsoft Industry Cloud for Manufacturing context

**KEVEN:** And the Microsoft Industry Cloud for Manufacturing context. Briefly — because we'll return to it in Ep 3.

**MIA:** *Microsoft Industry Cloud for Manufacturing is the umbrella.* It is the family of Microsoft capabilities pre-aligned to manufacturing data and AI use cases — Fabric for data, Foundry for the agent runtime, Power Platform for the surfacing layer, Dataverse for the operational data, all connected by a Common Data Model for manufacturing.

The point for the Account Team is this. *Toyota benefits from being inside that pattern rather than inventing a bespoke schema family.* The Silver canonical schemas at Toyota for the four data domains align to the Common Data Model that ships in the industry cloud. *Toyota's data engineers can read industry-standard documentation.* Toyota's vendors and integrators can speak a common language. The platform is doing the heavy lifting that a custom architecture would otherwise put on Toyota.

**KEVEN:** And the Account Team posture on it.

**MIA:** *Deloitte recommends Microsoft Industry Cloud for Manufacturing as the platform for the Zero Day Warranty agentic scenario at Toyota.* That recommendation rides on the technical merits — the Common Data Model fit, the Fabric data foundation, the Purview governance, the Foundry agent runtime. *Toyota contracts with Microsoft directly for the licensing.* Microsoft paper, Microsoft and Toyota. *Toyota contracts with Deloitte directly for the services.* Deloitte paper, Deloitte and Toyota. Two contracts. *No compensation flows from Microsoft to Deloitte for the platform recommendation.* Said the same way every time. The Account Team should be fluent in stating it.

### A reading I want to do

**KEVEN:** I want to read briefly from Microsoft's manufacturing documentation on why a composable data foundation matters more than any one model on top.

**MIA:** Read it.

**KEVEN:** [reading, paraphrased from Microsoft Industry Cloud for Manufacturing documentation, with cross-reference to SAE International production-data standards commentary]

*"The capability that distinguishes manufacturers who realize value from AI is rarely the model. It is the data foundation underneath the model. A unified, canonical, per-asset-joinable data layer — covering the production process, the equipment, the product as built, and the product as it performs in the field — is the prerequisite. The model becomes a surface on that foundation. Manufacturers who invest in the foundation first compound; manufacturers who chase the model first stall."*

[pause]

**MIA:** *The foundation IS the product.* The agent is the surface. Strip the agent off — the Silver canonical foundation across four domains is still valuable. It enables predictive maintenance, it enables production planning, it enables supplier-quality coordination, it enables any future agent built on top. *The foundation compounds.* Build the foundation once and every future use case rides on it.

The flipside is — without canonical Silver, no agent layer compounds. You build agent one against one set of data hacks; agent two requires another set; agent three is a re-platform. *The foundation IS the product.* That's the line that should land with any Toyota CIO listening.

### One disagreement

**MIA:** Pushback time.

**KEVEN:** Go.

**MIA:** I want to push back on the implicit ranking of the four domains. The question I set up in the cold open — *which domain produces the most causal signal?* — I have an answer that is going to disagree with the answer most data architects would give.

The conventional answer is — *the build record.* The build record is where supplier lots live; supplier lots are where the chargeback money is; therefore the build record is the most operationally valuable domain. *I half-agree.* I think the supplier-lot dimension within the build record is one of the most operationally underused signals in automotive manufacturing — and Toyota's supplier-quality team often has signal the build-record team itself does not surface. The supplier dimension is where the dollars are.

But my actual answer is different. *I think the assembly-line-telemetry domain is the most underexploited.* Specifically — the tool-drift, equipment-state, and environmental signal that lives in the historians today and almost never gets joined to anything. *That domain catches the defects no inspector caught.* Composed properly, it is the silent productivity engine of the whole architecture. The build record tells you what happened. The assembly line telemetry tells you *why.* That's the higher-value layer.

**KEVEN:** Counter.

**MIA:** Counter.

**KEVEN:** I agree on supplier-lot importance — that one is real, that one is where the chargeback recovery dollars are, and I think the Account Team should be able to talk about supplier-lot signal fluently. *The politically harder signal, though, is the operator-cohort dimension.* And operator-cohort lives in the build record.

Here's why it's the harder one. Supplier-lot is a *vendor-facing* signal. Toyota can have that conversation; the supplier expects it. *Operator-cohort is internal.* Toyota's TPS culture protects operator dignity carefully — for very good reasons. Forty years of TPS discipline says the operator is the heart of the system; the agent that surfaces cohort-level patterns has to do it *with the cultural safeguards built in*, not as an afterthought.

If we get that wrong, we lose the room. *If we get it right*, we give Toyota a new capability — surfacing training, tooling, and ergonomics opportunities at the cohort level — that respects the culture and improves the outcome. *That capability is more valuable, in my view, than any single supplier-lot finding* — because it strengthens the operator-side of the kaizen loop. Toyota's people get better; the system gets better.

**MIA:** So you're saying the build-record domain is where the politically loaded signal sits, and that's actually the deepest value layer because handling it well is what differentiates a respectful agent from a tone-deaf one.

**KEVEN:** That's what I'm saying. *The assembly-line-telemetry signal you named is technically high-leverage — agreed. The build-record operator-cohort signal is culturally high-leverage — and that's where the long-term value lives.* Both are real. The agent needs to handle supplier-lot natively, equipment-state forensically, and operator-cohort with care.

**MIA:** Reluctantly accepted with a friendly amendment. *Three high-leverage threads inside the four domains. Supplier-lot for the dollars. Equipment-state for the diagnosis. Operator-cohort for the culture.* The Account Team should be fluent in all three.

**KEVEN:** *All three.* And the answer to my opening question — *which domain produces the most causal signal* — is honestly *the join.* No single domain answers the warranty question alone. The composition is the answer.

**MIA:** Which is the whole episode.

### What to carry forward

**KEVEN:** Three things.

**MIA:** Go.

**KEVEN:** *One — the four domains map to four Toyota org boundaries.* Vehicle build record at Manufacturing IT. Connected vehicle warranty data at Toyota Connected. Quality events at plant Quality. Assembly line telemetry at Production Engineering and Asset Management. *Four data domains. Four custodians. The agent makes their data composable; the agent does not take ownership away from any of them.*

*Two — Silver is the canonical layer. Gold composes for the agent.* Bronze is raw landing. Silver is where the four domains take canonical form across systems. Gold is where the per-VIN joinable composite views live for the agent to read. *Anchoring canonical at Silver is the discipline.* It is what makes the foundation compound.

*Three — per-VIN joinability at Gold is the unlock that makes Zero Day Warranty possible.* The agent asks "what does the world look like for this VIN?" and gets a composite answer across all four domains in one query. *The eight-to-twelve-weeks of manual reconciliation collapses because the join is no longer manual.* That is the architectural commitment Episode 3 stands on.

**MIA:** And the Independence frame, said the same way. *Deloitte recommends Microsoft Fabric, Microsoft Industry Cloud for Manufacturing, and Microsoft Purview for the Zero Day Warranty data foundation. Toyota contracts with Microsoft directly for the platform. Toyota contracts with Deloitte directly for the services. Two contracts. No compensation flows from Microsoft to Deloitte for the platform recommendation.* Said exactly that way.

**KEVEN:** Said exactly that way.

**MIA:** Next episode — *The 24-Step Agent and the Microsoft Platform.* Microsoft Fabric plus Microsoft Agent Framework plus Microsoft Purview. The 24-step agent end to end. The hash chain and the audit echo walked. *The $4.2M, $2.8M, 340% reference scenario walked one step at a time.* The agent we have been pointing at across two episodes — finally on tape.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn
- **Microsoft Fabric overview** · [learn.microsoft.com/fabric](https://learn.microsoft.com/fabric/) — unified data platform, OneLake foundation
- **OneLake** in Microsoft Fabric — single tenant-resident lake under the medallion
- **Medallion architecture** in Microsoft Fabric — Bronze, Silver, Gold layered pattern
- **Microsoft Industry Cloud for Manufacturing** — manufacturing-aligned platform and Common Data Model
- **Common Data Model for Manufacturing** — canonical schemas the four domains align to at Silver
- **Power BI** for Gold-layer composition and reporting surfaces
- **Microsoft Purview** (deeper in Ep 3) — lineage, audit, and governance over Bronze / Silver / Gold

### Automotive data standards
- **AIAG** (Automotive Industry Action Group) — supplier-quality and traceability frameworks, PPAP, FMEA
- **SAE International** — production data and quality engineering standards
- **ISO/TS 16949** (now **IATF 16949**) — quality management for automotive production
- **OPC UA** — the open standard for OT/IT integration; how plant historians compose with Fabric

### Industry coverage
- **Automotive News** · [autonews.com](https://www.autonews.com/) — connected-vehicle and manufacturing-data coverage
- **Reuters Automotive** — supplier-quality and warranty-cost reporting
- **WardsAuto** — assembly-line and plant-floor reporting

### From the APEX framework (internal coordination only — not on-mic)
- **AXLE Practice** — Build Record (BRML), Connected Vehicle (CVML), Quality Event (QEML), Assembly Asset (AAML) canonical schema families that the four spoken domains map to
- **Services Podcast Eps 3-4** — medallion architecture and agent foundation under this episode
- **Companion HTML pack** — `ZeroDayWarranty_Architecture_Diagrams.html` for the four-domain visual reference

---

**End of Episode 02 · Four Data Domains**
*≈ 5,800 words · target 30 minutes at conversational pace*
