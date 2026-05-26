# Episode 01 · The Zero Day Warranty Idea

**Builds on:** Toyota IAS QWS pillar · APEX AXLE framework · ORCH-01 anchor scenario · Trilogy — Sellers Ep 4 (TMT-MED Practice / Automotive Practice context)
**Run time:** ≈ 28 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: a Toyota assembly plant ambient. A faint hum of conveyors, the distant rhythm of a stamping press shutting down for the night. 11 PM. A monitor humming in a quiet quality office.]

**MIA:** I want to start at eleven o'clock on a Tuesday night in Georgetown, Kentucky. Toyota Motor Manufacturing Kentucky. The Camry line ran third shift today and just wound down. Most of the plant is quiet. *The quality office is not.*

There is one quality engineer still at her desk. Two monitors. The left monitor has a connected-vehicle warranty dashboard open — claims aggregated by VIN, by build week, by failure mode. The right monitor has a spreadsheet. The spreadsheet is what she has been building for the last six hours.

[pause]

**KEVEN:** And what she's looking at —

**MIA:** What she's looking at is a *warranty cluster.* A specific failure mode — let's call it a sensor harness intermittent — showing up at a higher rate than baseline across vehicles built in a specific window. Three weeks of build data. She's pretty sure something happened during those three weeks. She does not yet know what. She does not yet know whether it was a supplier lot, a station, a tool, a shift, a torque setting, an operator-cohort training gap, or some interaction between two or three of those things at once.

And what she knows, right now, sitting at her desk at eleven o'clock at night, is that *she's about to start an investigation that will take eight to twelve weeks.*

**KEVEN:** Walk me through what that means.

**MIA:** It means tomorrow morning she opens a ticket with Manufacturing IT to pull the build records for every VIN in the cluster. Manufacturing IT takes the request, schedules it against their queue, and gets her data back in two or three days — sometimes a week. While she waits, she emails Supplier Quality at the parts division because three of the claims mention a connector. Supplier Quality reaches out to the lot vendor. The lot vendor wants the VIN list. She sends it. A few days pass.

Meanwhile, she's also pinging Toyota Connected because she wants the raw telematics — *not* the warranty claim summary, the underlying field data. That's a different team in a different building running a different system. Different intake process.

Then Warranty Engineering needs to be brought in to compose the causal model once the data starts arriving. And Finance is hovering because *if this turns out to be a supplier issue, there's a chargeback eligibility question.* Six teams. Six handoffs. Each handoff has a queue.

**KEVEN:** And the clock is running.

**MIA:** The clock is running. Every day that investigation drags is another day vehicles built in adjacent weeks may carry the same defect into the field. Every day is another day the supplier could ship more of the same lot. *Every day is a day we cannot do Hansei properly* — we cannot reflect and improve at source, because we don't yet know what source is.

[pause]

**KEVEN:** Eight to twelve weeks. Across six teams. For one warranty cluster.

**MIA:** For *one* warranty cluster. In a normal month there are several. Stack them up and the quality organisation is running a permanent backlog of investigations. The engineer at her desk at eleven o'clock at night is not unusual. She is the *system working as designed* — and the design is past its expiration date.

**KEVEN:** This podcast is about what changes when we can compose the data she needs *and trace it in minutes, not weeks.* Five episodes. I'm Keven Markham, Deloitte's Microsoft Technology and Services Practice. Twenty-two years on the Microsoft platform.

**MIA:** I'm Mia. Eighteen years on automotive accounts, mostly on the manufacturing-IT and quality-leadership side. I've sat in those quality reviews. I've watched the eleven-o'clock-on-a-Tuesday-night moment happen. This podcast is for the Account Team — and for any Toyota colleague who happens to be listening. The Zero Day Warranty Podcast. Episode One. *The Zero Day Warranty Idea.*

---

## The conversation

### Why warranty cost reduction matters at Toyota right now

**KEVEN:** Set the industry context. Why is warranty cost reduction the right conversation at Toyota in 2026?

**MIA:** Three layers. The macro layer, the Toyota-specific layer, and the timing layer.

The macro layer first. *Warranty cost is a structural drag on every automaker's P&L*, and connected-vehicle data has made the drag visible in a way that didn't exist ten years ago. Trade press — Automotive News, Reuters Automotive, WardsAuto — have been writing for years that as vehicles become more electronically integrated, warranty claim volume scales faster than investigation capacity. The data deluge is real. The investigation muscle has not scaled with it. *That gap is where warranty cost compounds.*

**KEVEN:** And the Toyota-specific layer.

**MIA:** Toyota's CEO of North America, Tetsuo Ogawa — Ted Ogawa — has been explicit in public communications about *Manufacturing Excellence and Industry 4.0* as a strategic priority for the region. He has talked about it in the press, at industry events, in TMNA's own communications. That is not a vague aspiration. That is the most senior executive in North America saying *we are going to lead in modernised manufacturing.* The Account Team should treat that as the umbrella that everything else hangs under.

Warranty cost reduction is one of the cleanest expressions of that priority. *It is measurable. It is causal. It is auditable. And it lives at the intersection of the factory, the connected vehicle, and the supply chain* — which is exactly where modernised manufacturing has to land if it is going to be more than a slogan.

**KEVEN:** And the timing layer.

**MIA:** The timing layer is the connected vehicle. Toyota Connected has been building up its data estate for years now. The warranty data that exists in the connected fleet today is *vastly* richer than the warranty data of even five years ago. We're no longer dependent on a dealer-recorded claim text and a labour-code mapping. The vehicle itself reports — and the data lands in a place we can reason against.

The point being — the raw material has arrived. *The investigation muscle has not been re-armed to match it.* That is the gap.

**KEVEN:** So the case for now is — the data is here, the executive priority is named, and the cost of the slow investigation is structural.

**MIA:** That's the case. And the kicker — *the slow investigation is also a credibility tax.* When it takes three months to come back to a supplier with evidence, the supplier conversation is harder. When it takes three months to come back to the plant team with a finding, the operators on the line have already moved on to the next month's build. *Toyota's culture is built around fast feedback to source.* Slow investigation breaks that loop.

### The current state — 8 to 12 weeks across six teams

**KEVEN:** Walk the current state in more detail. I want every Account Team listener to feel where the time goes.

**MIA:** OK. Six teams. Let me name them and what they do.

*Manufacturing IT.* They own the build-record systems — the per-VIN factory history. Every station the vehicle passed through, the tool that was used, the torque reading on a critical fastener, the operator who was at that station that shift, the supplier lot for every consumable part installed. That data exists, but it lives across multiple plant-floor systems — MES, quality systems, supplier traceability, asset management. Extracting a clean per-VIN view for a cluster of, say, four thousand vehicles is *not* a one-query exercise. It's a multi-system pull, reconciled, validated. *Days.*

*Quality.* The plant Quality team owns inspection and measurement data — every gauge reading, every visual check, every dimensional measurement captured during the build. When the build-record data comes back, Quality needs to overlay their inspection data and look for anomalies. *More days.*

*Supplier Quality.* The supplier-facing arm. When the cluster points at a component, Supplier Quality reaches out to the supplier — and the supplier wants the VIN list and the failure mode definition before they'll do their own internal investigation. The supplier then takes time to look at their lot records. *Often weeks*, because the supplier is fielding similar requests from other customers.

*Toyota Connected.* The connected-vehicle data team. They hold the field telematics, the in-vehicle diagnostic codes, the actual signal traces — not the warranty claim summary, the underlying signal. When you want to understand *what the vehicle was doing when it failed*, this is the team. Different building, different system, different intake.

*Warranty Engineering.* The team that composes the causal model. They take the build-record data, the inspection data, the supplier evidence, the field telematics, and they construct a hypothesis — *this cohort, at this station, with this supplier lot, under these conditions, produces this failure mode at this rate.* That is hard, multi-variable, statistical work. They're good at it. They are also a small team carrying a large queue.

*Finance.* Warranty reserve, chargeback eligibility, accounting treatment. When the hypothesis converges, Finance needs to be looped in to determine whether the supplier can be charged back, on what evidence, under what contract terms. That is its own approval process.

**KEVEN:** Six teams. And the handoffs are where the time is.

**MIA:** The handoffs are where *most* of the time is. Each team does its work in days. The queues between teams add weeks. *Investigator time on a significant warranty cluster — call it four hundred hours of professional time across the six teams.* The calendar time stretches that into eight to twelve weeks.

**KEVEN:** And those four hundred hours — those are not low-judgement hours. Those are senior engineers, senior quality leaders, senior supplier-quality professionals.

**MIA:** Those are the people you most want doing root-cause thinking and the people you can least afford to have doing data reconciliation. Today the work is *60-70% reconciliation and 30-40% root-cause judgement.* The audit-ready agent flips that ratio.

### Toyota's production context — TPS, Jidoka, the 14 NA plants

**KEVEN:** Before we go into the agentic hypothesis, we have to ground this in Toyota's manufacturing culture. The audience needs the right vocabulary, and it needs to be used correctly.

**MIA:** Yes. Carefully. Toyota *invented* modern manufacturing discipline. Every word we use here is borrowed from a body of practice that has been refined for seventy years.

The framework is the *Toyota Production System* — TPS. Two pillars. *Just-in-time*, which is the flow discipline — the right part, in the right place, at the right time. And *Jidoka*, which is the quality discipline.

**KEVEN:** Define Jidoka properly.

**MIA:** *Jidoka* is sometimes translated as "autonomation" or "automation with a human touch." The principle — when a quality problem is detected, the line stops, and the problem is fixed at source before any more product is built downstream of it. The operator has the authority and the obligation to stop the line. The mechanism is the *andon* — the cord, the light, the signal. *Pulling the andon is not failure. Pulling the andon is the system working.*

**KEVEN:** And Genchi Genbutsu.

**MIA:** *Genchi Genbutsu* — "go and see." When something happens on the line, you do not analyse it from a desk. You go to the spot, you look, you talk to the operators who were there. You ground your understanding in the actual place. The opposite of management-by-spreadsheet.

*Kaizen* — continuous improvement, owned by the team closest to the work. *Hansei* — reflection. After a defect, after a recall, after any quality event — what do we learn. Hansei is built into the calendar; it is not optional.

**KEVEN:** And Toyota's North American footprint. Where this happens.

**MIA:** Fourteen North American manufacturing operations. The flagship — *Toyota Motor Manufacturing Kentucky* in Georgetown, the largest Toyota plant in the world by volume, where the Camry is built. *Toyota Motor Manufacturing Indiana* in Princeton, where the larger SUVs and the Sienna are built. *Toyota Motor Manufacturing Texas* in San Antonio, where Tundra and Sequoia are built. *Toyota Manufacturing Alabama* — engines. *Mazda Toyota Manufacturing* in Huntsville, a joint operation with Mazda for Corolla Cross and CX-50. Plus operations in Mississippi, West Virginia, Tennessee, North Carolina, and several Canadian sites under TMMC.

All fourteen operations run TPS. Every one of them. *And every one of them is at a different stage of digital tooling maturity.* Some sites have rich modernised plant-floor data estates. Some are still building those out. The agent we are about to talk about has to land into that real heterogeneity — and respect it.

**KEVEN:** And the framing I want to be very clear on.

**MIA:** Yes. *The agent augments TPS. It does not replace TPS.* Jidoka is the operator's authority. Genchi Genbutsu is the engineer's discipline. Kaizen is the team's ownership. Hansei is the organisation's memory. *None of those move from the human to the agent.*

What moves to the agent is the *reconciliation toil* — the work of pulling data from six systems, joining it by VIN, aligning it by time, computing the cohort statistics. That work today consumes the senior engineer's hours. *Take that work off her plate and you give her her time back.* Her time then goes back into the higher-judgement work — the supplier conversation, the design feedback, the operator dialogue, the kaizen workshop.

**KEVEN:** *The audit-ready agent extends TPS. It makes Hansei faster and earlier.*

**MIA:** That is exactly the frame. Faster Hansei. Earlier Hansei. *And the operator is still the heart of the system.*

### The Zero Day Warranty hypothesis — compose four domains, single audit-ready agent

**KEVEN:** OK. The hypothesis. State it cleanly.

**MIA:** The hypothesis is this. *There are four data domains Toyota already thinks in.* Today they live in separate systems, with separate teams, and the work of joining them is what consumes the eight to twelve weeks. If we compose them into a single per-VIN view and put a reasoning agent on top — an agent that is *audit-ready by construction* — what takes eight to twelve weeks today takes minutes.

**KEVEN:** Name the four domains.

**MIA:** Said the way Toyota would say them.

*The vehicle build record.* Every VIN's complete factory build history. When the vehicle was built, where, on which station, with which tool, on which shift, by which operator cohort, and from which supplier lot for every consumable part. This is the per-VIN truth of what happened on the assembly line.

*Connected vehicle warranty data.* Claims and failure modes reported by connected vehicles in the field, tied back to VIN. Not just the dealer-coded labour record — the underlying signal evidence. When the vehicle reports a fault, what was it doing.

*Quality events on the line.* Every inspection, measurement, dimensional check, defect, rework, and andon event captured during the build. The plant-floor record of *every quality signal that happened while the vehicle was being assembled.*

*Assembly line telemetry.* Equipment state, throughput, asset events, station-level conditions on the production floor. Tools, fixtures, conveyors, environment. What the equipment was doing while the vehicle was on it.

**KEVEN:** And the join key is the VIN.

**MIA:** The join key is the VIN, plus the time stamps. *A given VIN passed through a given station, at a given minute, while a given tool was at a given state, while a given operator cohort was on shift, while a given supplier lot was being installed, and produced a given quality event at a given moment. That is one row of evidence.* Compose four thousand of those for a warranty cluster and the agent has the substrate it needs to reason.

**KEVEN:** And the reasoning.

**MIA:** The reasoning is cohort-by-station-by-tool-by-supplier-by-shift interaction analysis. *Which combination of conditions correlates with which failure mode at statistical significance.* That is hard work today. It is the work Warranty Engineering does manually over weeks. An agent built on a clean per-VIN composition can do that work in minutes — *and produce an evidence package an engineer signs off on, not a black-box answer.*

**KEVEN:** That last point. Critical.

**MIA:** Non-negotiable. *The agent does not make a chargeback decision. The agent produces an evidence package and a human signs.* The Quality engineer at her desk at eleven o'clock at night is *still the protagonist* of this story. The agent gives her her hours back. The agent does not take her judgement away.

**KEVEN:** And audit-ready.

**MIA:** Every decision the agent makes is one audit row. Hash-chained — meaning each row references the cryptographic hash of the prior row, so the chain cannot be silently edited after the fact. Replay-validated — meaning you can take any agent decision and re-run it against the original inputs and prove the agent would produce the same answer. Microsoft Purview audits those rows the same way it audits any other governed asset. *That is the architectural reason Toyota Quality and Toyota Legal can adopt an agent in the warranty path at all.* Episodes 2 and 3 walk it. For now — internalise that audit-ready is not a slogan. It is the load-bearing wall.

### The $4.2M / $2.8M / 340% reference scenario

**KEVEN:** And the reference numbers. The headline that follows us across the rest of the series.

**MIA:** Let me walk one reference scenario. *And I want to be careful with the language* — this is a reference scenario from the framework's catalogued material, not a claimed Toyota result.

The setup. A connected-vehicle warranty cluster surfaces — call it three thousand vehicles showing the same intermittent failure mode at a rate above baseline. The cluster spans roughly three build weeks. Today that triggers the eight-to-twelve-week investigation.

In the reference scenario, the agent composes the four domains per VIN and runs the cohort interaction analysis. It surfaces — *with statistical significance* — that a specific supplier lot, present in vehicles built in weeks 12 through 14, accounts for *$4.2 million* in projected warranty cost across the affected VINs.

**KEVEN:** That number is the field cost.

**MIA:** That number is the projected warranty cost — claims that have come in plus claims projected from the failure rate against the affected population. Four-point-two million dollars of warranty exposure traceable to one lot from one supplier across one three-week window.

**KEVEN:** And then the chargeback path.

**MIA:** The agent produces a *chargeback evidence package.* That package is — the supplier lot identification, the affected VIN list, the failure-mode tie-out per VIN, the build-record evidence showing the lot was installed during the relevant window, the field-claim evidence tying the failure mode back to the part, and the audit chain proving how the agent reached the conclusion. *That package goes to Supplier Quality, who signs.* It goes to Finance, who signs. It goes to the supplier as a chargeback notice.

In the reference scenario, *$2.8 million* of that $4.2M is recovered as a supplier chargeback. The recovery rate exceeds what the manual chargeback process typically achieves on a comparable cluster — *by 340 percent.*

**KEVEN:** Why? Why is the recovery rate that much higher?

**MIA:** Two reasons. First — *evidence quality.* The manual process produces a chargeback case that is roughly defensible. The agentic process produces a chargeback case that is *forensically* defensible — every join is hash-chained, every conclusion is replay-validated, every assumption is explicit. Suppliers contest weak evidence; they don't contest forensic evidence in the same way. Second — *speed.* Cases recovered within ninety days of the failure carry materially higher recovery rates than cases recovered nine months later, when invoices are paid and quarters have closed. The agentic timeline closes cases inside that ninety-day window. The manual timeline rarely does.

**KEVEN:** That number — *$4.2 million, $2.8 million, 340 percent* — is the reference. It is going to come up every episode.

**MIA:** Every episode. Same way every time. And every time the *reference scenario* qualifier comes with it. The Account Team should never quote a Toyota-specific dollar figure off this number. *Toyota will compute its own number when the time comes.* This is the reference.

### Toyota's Microsoft and NVIDIA footprints — already in flight

**KEVEN:** Now situate this on the platform side. *Toyota's existing footprint* — what they already license, what they already run.

**MIA:** Two estates that matter here, and both are already in motion.

The Microsoft estate. *Toyota Connected North America runs on Azure.* That is not a Deloitte proposal — that is Toyota's standing architecture. The connected-vehicle data we just talked about lives on Microsoft cloud today. Toyota's broader IT estate has been on Microsoft productivity, identity, and cloud services for years. *Microsoft Industry Cloud for Manufacturing* — the family of capabilities that brings Fabric, Foundry, Power Platform, and Dataverse together for manufacturing data use cases — is directly aligned with the Manufacturing Excellence priority Ted Ogawa has named.

**KEVEN:** And on the NVIDIA side.

**MIA:** *Woven by Toyota* — the technology subsidiary that came out of Toyota Research Institute Advanced Development — is running NVIDIA Omniverse for *Woven City*, the connected-city development project east of Mount Fuji. Omniverse is the city-scale digital-twin platform. NVIDIA has talked about this publicly; Toyota has talked about it publicly; it is on the record.

On the autonomous-vehicle side, *Toyota's autonomous driving development uses NVIDIA Drive* — the Drive platform for AV simulation and in-vehicle compute. Again, both companies have spoken publicly about this. The NVIDIA estate at Toyota is real, growing, and already integrated into how Toyota does advanced engineering.

**KEVEN:** And the point for the Account Team.

**MIA:** The point is this podcast is *not introducing new vendors* to Toyota. Both Microsoft and NVIDIA are platforms Toyota already uses. *What this podcast is about is how to compose them — specifically, for the Zero Day Warranty agentic scenario.* The data foundation sits on Microsoft Fabric, the agent reasons through Microsoft Agent Framework, the governance comes through Microsoft Purview. NVIDIA shows up later — Episodes 4 and 5 — as the *Day-0 prevention* extension at the station, and as the existing Omniverse and Drive estates that compose into the same picture.

**KEVEN:** And how we talk about Deloitte's role.

**MIA:** Carefully and accurately. *Deloitte recommends.* The recommendation is Microsoft Fabric, Agent Framework, and Purview for the Zero Day Warranty agentic scenario at Toyota. That recommendation is on the technical and economic merits — the platforms are the right fit for the problem and for Toyota's existing estate.

*Toyota contracts with Microsoft directly for the licensing.* Microsoft paper, Microsoft and Toyota. *Toyota contracts with Deloitte directly for the services.* Deloitte paper, Deloitte and Toyota. Two contracts. *No compensation flows from Microsoft to Deloitte for the platform recommendation.* That is the model. It is going to be named again in Episode 5 the same way. The Account Team should be fluent in stating it that way on a Toyota call.

### What we'll cover across the five episodes

**KEVEN:** And the roadmap. Briefly.

**MIA:** Five episodes. This one — the idea, the current state, the hypothesis. *Episode 2 — Four Data Domains.* The vehicle build record, the connected-vehicle warranty data, the quality events on the line, the assembly line telemetry — what each one looks like, how each one lands on Microsoft Fabric, and what the per-VIN joinable view looks like in Gold. *Episode 3 — The 24-Step Agent and the Microsoft Platform.* The full agent walk-through. Fabric plus Agent Framework plus Purview. The hash chain. The replay token. The reference-scenario math walked one step at a time.

*Episode 4 — NVIDIA at the Station.* Day-0 prevention. Metropolis, DeepStream, Jetson, RAPIDS. Why inline vision at the station composes with the Microsoft data fabric rather than competing with it. *Episode 5 — Omniverse, Toyota's NVIDIA Estate, and the 90-Day Path.* Woven City and Omniverse. Toyota Drive. NeMo and Triton. The 90-day one-plant pilot plan. The Account Team handoff.

**KEVEN:** Two and a half hours of audio. *One scenario. Walked the way Toyota would expect it to be walked.*

### A reading I want to do

**KEVEN:** I want to read briefly from a recent industry register on connected-vehicle warranty cost.

**MIA:** Read it.

**KEVEN:** [reading, paraphrased from an Automotive News / SAE International register]

*"As vehicles have become more electronically integrated, warranty claim volume has grown materially faster than the investigative capacity of most automakers' quality organisations. The structural result — warranty cost per unit is rising even as per-unit defect rates have, in many programmes, fallen. The bottleneck is not in detection; the bottleneck is in causal attribution. Until that bottleneck moves, warranty cost will continue to outpace the underlying improvement in build quality."*

[pause]

**MIA:** *The bottleneck is in causal attribution.* That sentence is the whole point. The detection problem is largely solved — the connected vehicle reports, the dashboard lights up. What does not move at the speed of the data is the *attribution* work that turns a claim into a known root cause with an evidence package.

And the cost of the slow attribution is not just dollars. *It is credibility.* The engineer at her desk at eleven o'clock at night is doing her best work inside a system that gives her tools twelve weeks too slow. When the supplier conversation happens three months after the cluster surfaced, the supplier's response is shaped by that delay. When the operator-cohort feedback gets to the line, the operators have already moved on. *The audit-ready agent gives Toyota faster answers — and more durable trust, with suppliers and with its own people.*

### One disagreement

**MIA:** Pushback time.

**KEVEN:** Go.

**MIA:** I want to push on the *order of the platform conversation.* Conventional sequencing — and the way Episodes 2 through 5 unfold — leads with the Microsoft data foundation and brings NVIDIA in at Episode 4. *I want to argue that for an operator-first, Jidoka-rooted account like Toyota, NVIDIA at the station — Day-0 prevention — is the more strategic entry, and we should lead with it.*

**KEVEN:** Make the case.

**MIA:** Three reasons. *One — Toyota's deepest cultural commitment is preventing defects at source, not attributing them after the fact.* Jidoka is "stop the line when a defect is detected." NVIDIA at the station — inline vision AI catching the defect *as it happens* — is the more direct fit to that cultural commitment. We're closer to TPS by leading there.

*Two — Day-0 prevention stops cost before it accumulates.* The Zero Day Warranty agent recovers $2.8M after the cost has already been incurred. Inline prevention at the station may stop the cost from ever being incurred. The dollar economics are stronger upstream. Why are we starting downstream?

*Three — NVIDIA is already in Toyota's vocabulary.* Woven City, Toyota Drive. We are not introducing NVIDIA at Toyota. We are extending Toyota's existing NVIDIA estate into the plant. *That is a familiar conversation. The Microsoft Fabric conversation, while right, may feel more like a new vector.*

**KEVEN:** Three good reasons. Now the counter.

**MIA:** Counter.

**KEVEN:** The counter is — *the warranty cost is already being incurred today.* Toyota Connected is generating warranty data right now. The $4.2M reference scenario is not theoretical; warranty clusters are happening and the slow investigation is happening alongside them. *That cost is bleeding today.* The Microsoft data foundation stops the bleeding inside ninety days, on data that already exists, with platforms Toyota already licenses. That is the fastest demonstrable economic move.

*Two — the Toyota CFO conversation lands first on the data and the dollars.* The CFO is going to see the $4.2M reference number in the connected-vehicle data domain — the warranty data — before she sees a station-vision pilot proposal. Lead where the CFO is already looking.

*Three — NVIDIA at the station is real and it matters. But it requires a plant-floor deployment, edge hardware, vision-model training, and station-level integration work that is a longer pilot. Six to nine months. The Microsoft data-fabric pilot is ninety days.* The first win has to be the fast win. *Then* NVIDIA composes on top.

**MIA:** So you're saying — the foundation comes first because the foundation can demonstrate value in ninety days against data that already exists, and NVIDIA is the *next move* on the platform, not the *first move.*

**KEVEN:** That's what I'm saying. *And the right answer might be that both happen in parallel — the data fabric pilot at ninety days, the station-vision pilot at six months, converging on the same warranty agent.* But if we're picking the lead, the lead is the foundation. The economics, the speed-to-value, and the CFO sightline all argue that way.

**MIA:** Reluctantly accepted. *Foundation first. NVIDIA composes on top.* And I want Episode 4 to honour the cultural argument I just made — Day-0 prevention is not the *second priority*; it is the *natural next move* that gets us closer to Toyota's actual cultural commitment.

**KEVEN:** Episode 4 will honour it. *And I think when Toyota hears that framing, they'll lean into it.*

### What to carry forward

**KEVEN:** Three things.

**MIA:** Go.

**KEVEN:** *One — the four-domain hypothesis is the foundation.* The vehicle build record, the connected-vehicle warranty data, the quality events on the line, the assembly line telemetry. Composed per VIN, joined on time, reasoned over by a single agent. That is the architectural commitment everything else rests on.

*Two — operator dignity is non-negotiable.* The agent augments TPS. It never replaces operator judgement. Jidoka is the operator's. Genchi Genbutsu is the engineer's. Kaizen is the team's. Hansei is the organisation's. *What moves to the agent is the reconciliation toil — not the judgement.* Any take that drifts from that gets cut.

*Three — audit-ready is the load-bearing wall.* Every agent decision is one row. Hash-chained. Replay-validated. Echoed through Microsoft Purview. *That is the architectural reason this can land in the warranty path at all.* Episodes 2 and 3 walk it; every episode references it.

**MIA:** And the Independence frame the Account Team needs to be fluent in. *Deloitte recommends. Toyota contracts with Microsoft directly for the platform. Toyota contracts with Deloitte directly for the services. Two contracts. No compensation flows from Microsoft to Deloitte for the platform recommendation.* Said exactly that way.

**KEVEN:** Said exactly that way.

**MIA:** Next episode — *Four Data Domains.* Vehicle build record, connected-vehicle warranty data, quality events on the line, assembly line telemetry — on Microsoft Fabric with per-VIN joinable Gold views. We walk what each domain looks like, what the medallion architecture does to it, and what the per-VIN Gold view actually composes into.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Toyota official

- **Toyota Newsroom** · [pressroom.toyota.com](https://pressroom.toyota.com/) — TMNA press, executive communications, Manufacturing Excellence updates
- **Toyota Connected North America** — connected-vehicle platform and data estate background
- **TMNA investor and corporate communications** — Manufacturing Excellence and Industry 4.0 priority context
- **Tetsuo "Ted" Ogawa CEO communications** — public addresses and TMNA priority statements naming Manufacturing Excellence
- **Toyota Production System primer** — [lean.org](https://lean.org/) overview of TPS, Jidoka, Andon, Genchi Genbutsu, Hansei, Kaizen
- **Woven by Toyota** · [woven.toyota](https://woven.toyota/) — Woven City and Toyota's advanced-development subsidiary

### Industry publications

- **Automotive News** · [autonews.com](https://www.autonews.com/) — warranty cost coverage, Toyota plant coverage, connected-vehicle reporting
- **Reuters Automotive** — connected-vehicle, supplier-quality, and warranty coverage
- **WardsAuto** — manufacturing and assembly-line reporting on TMNA plants
- **SAE International** — production safety, quality engineering, and connected-vehicle standards
- **AIAG** (Automotive Industry Action Group) — supplier quality frameworks, PPAP, FMEA standards
- **Society of Automotive Analysts** — automotive economics and warranty-cost commentary

### Microsoft Learn — referenced briefly here, depth in Episodes 2-3

- **Microsoft Fabric** overview — unified data platform, OneLake, medallion architecture
- **Microsoft Agent Framework SDK** — agent authoring and orchestration on Azure AI Foundry
- **Microsoft Purview** — governance, audit, and DSPM for AI
- **Microsoft Industry Cloud for Manufacturing** — manufacturing-aligned data and AI capabilities

### NVIDIA — referenced briefly here, depth in Episodes 4-5

- **NVIDIA Omniverse** — city-scale and plant-scale digital twins; Woven City reference
- **NVIDIA Drive** — autonomous-vehicle development platform; Toyota AV reference
- **NVIDIA Developer Blog** — Metropolis, DeepStream, Jetson, RAPIDS reference material for Episode 4

### From the APEX framework

- **AXLE Practice — ORCH-01 Warranty Root-Cause** — the internal anchor scenario this podcast translates
- **BRML schema family** (referenced in Episode 2 as the "vehicle build record domain")
- **Companion HTML pack** — `ZeroDayWarranty_Calculations_and_References.html` + `ZeroDayWarranty_Architecture_Diagrams.html` (in `Automotive/Toyota/02_projects/FY27_Pipeline/Fabric_Connected_Vehicle_Analytics/`)

---

**End of Episode 01 · The Zero Day Warranty Idea**
*≈ 5,500 words · target 28 minutes at conversational pace*
