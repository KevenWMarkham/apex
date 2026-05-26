# Episode 02 · The Manufacturing & Quality Plays

**Builds on:** DTNA Ep 1 (four brands, three strategic themes) · Trilogy — Services Ep 3-4 (medallion + agent foundation) · Services Ep 6 (Warranty Cost Spiral deep dive)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: a heavy industrial ambient. Distant compressor pulse. A pneumatic tool engages briefly.]

**KEVEN:** I want to start at the Detroit Diesel engine test bay in Redford, Michigan. A DD15 engine — fifteen-litre, six-cylinder, the workhorse powertrain for Class 8 on-highway tractors — is on the test stand at three in the morning. The engine has just completed its hot-test cycle. The technician on duty pulls the data, reviews the standard validation outputs, signs the test ticket. The engine goes to crate-and-ship for delivery to the truck plant the next morning.

[pause]

**MARCUS:** And the part of the story that matters —

**KEVEN:** The part of the story that matters is — *that engine, eight months from now, might generate a warranty claim from a fleet customer in Oklahoma reporting a sensor failure.* Today, the time from that field claim to a confirmed manufacturing-root-cause-understood is eight to twelve weeks. The supplier-recovery window expires at 90 days. *Most root-causes don't get confirmed inside the window.* The OEM eats warranty cost that could have been recovered from the supplier.

That's the manufacturing-and-quality pain at DTNA. Multiplied across hundreds of thousands of engines, axles, transmissions, and trucks manufactured per year. *It's a cost problem of structural scale.* This episode is about the AXLE Practice plays that compress that pain.

Six plays this episode. Each one with a specific DTNA pressure point, a specific KPI signal, and a specific seller's path.

I'm Keven Markham.

**MARCUS:** I'm Marcus. DTNA Account Podcast. Episode Two. *The Manufacturing & Quality Plays.*

---

## The conversation

### Why manufacturing-and-quality is the AXLE flagship

**MARCUS:** Set up the framing.

**KEVEN:** The AXLE Practice is built around the recognition that *commercial vehicle manufacturing has been digital for decades but has been agentic for none of them.* The data exists. The MES (manufacturing execution system) data, the quality-event data, the supplier-quality data, the connected-vehicle field data — all of it. *What hasn't existed until recently is the agentic layer that composes across all of it to produce decisions.*

The six manufacturing-and-quality plays I'm going to walk are *the highest-fit plays for DTNA in the AXLE Practice catalog.* Every one of them touches data that already exists at DTNA, in systems DTNA already operates. *None of these plays requires DTNA to build a new data foundation.* They require the agentic layer to compose what's there.

That's why these plays are typically Wave 1 entry candidates. *The shortest path to a working APEX agent in DTNA's tenant runs through manufacturing-and-quality.*

### Play one — Zero Day Warranty Traceability and Cost Avoidance (AXLE-WRTY-01)

**MARCUS:** Walk play one. The flagship.

**KEVEN:** Zero Day Warranty Traceability and Cost Avoidance. AXLE-WRTY-01. The flagship play in the AXLE Practice and arguably the highest-fit play for DTNA across the entire framework.

The DTNA context. *Warranty cost as a percentage of revenue in commercial trucking has roughly doubled since 2000.* Multi-million-dollar claim clusters are routine. A single defective supplier lot in a critical engine component can produce millions of dollars in field claims if it escapes detection. *And the chargeback window — the contractual period during which the OEM can recover costs from the supplier — is typically 90 days.* If the investigation cycle takes 8-12 weeks (the industry norm), the chargeback window closes before recovery is possible.

The pain point. Investigation latency *is* the binding constraint on warranty cost recovery. Not knowing what failed. Not knowing whether to recall. Not knowing whom to charge back. *Knowing all of those things faster.*

The agent strategy. The warranty agent takes a cluster signal — *"we're seeing elevated claims in Cascadia units built in week 12-14 of last year"* — and walks each VIN back to its complete build record. Build station, shift, operator cohort, tool wear-cycle, supplier lot. Cross-references with quality-event data from the build, connected-vehicle telemetry from the field, assembly-asset telemetry from the production window. Identifies the *statistically significant cohort × station × tool × supplier-lot interaction* that explains the cluster. Produces an audit-defensible chargeback evidence package.

*Investigation cycle — from 8-12 weeks to minutes.* Engineer review and approval — 2-5 days. Chargeback motion through legal — still weeks. But the *engineering investigation* compresses to inside the contractual recovery window.

The architectural shape. Four AXLE canonical schema families joining on VIN at Silver — build record, connected vehicle, quality event, assembly asset. Gold mart shapes per-VIN feature vectors and per-cohort statistical aggregations. The agent has approximately 8 MCP tools spanning the four canonical families and the chargeback-evidence assembly.

**MARCUS:** And the KPI signal at DTNA specifically —

**KEVEN:** Reference scenarios suggest *25-40 percent improvement in chargeback recovery rate*, which at DTNA's scale translates to *tens of millions of dollars annually.* Plus *15-30 percent reduction in defective units escaping for a given root-cause type* — because faster root-cause means faster remediation on the line, which means fewer subsequent vehicles built with the same defect.

**MARCUS:** Seller's hook?

**KEVEN:** *"Your warranty investigation cycle is the binding constraint on supplier-recovery dollars. We can compress the engineering investigation from weeks to days. Wave 1 — ninety days. Pilot on one cluster. Show the numbers before Q-end."*

### Play two — Predictive Maintenance, Plant Equipment (AXLE-ASSET-01)

**KEVEN:** Play two. Predictive maintenance for plant equipment.

**MARCUS:** DTNA's manufacturing footprint includes thousands of major pieces of capital equipment — stamping presses, robotic welding cells, paint-line equipment, assembly torque tools, test stands. *Unplanned equipment downtime is the single largest controllable operational variance.* A Cascadia line going down for two hours costs the OEM real revenue — production schedule slippage, expedited shipping for components needed downstream, overtime to recover, customer-delivery risk for fleets expecting trucks at specific dates.

The current state. Calendar-based maintenance. Some reactive maintenance. Some condition-based maintenance for specific high-value assets. *The line is data-rich; the data isn't continuously composed for predictive intervention.*

The agent strategy. The predictive maintenance agent reads equipment telemetry continuously (vibration, current draw, temperature, throughput, cycle counts), reasons about developing maintenance needs *before* failure, recommends maintenance windows that minimise production-schedule impact (overnight closes during low-demand, between-shift swaps), and surfaces the recommendation to plant maintenance leadership. *Engineering team approves.*

The architectural shape. Streaming Bronze from the plant's PI Historian or equivalent. Silver maps to the AXLE assembly-asset family canonical. Gold per-equipment health features and per-class anomaly aggregations. Agent uses Real-Time Intelligence eventhouse for the streaming signal, with Activator for threshold-firing.

The KPI signal. *Unplanned downtime reduction 25-40 percent on covered equipment.* Maintenance-cost optimisation 15-20 percent. *Production-schedule reliability improvement* which downstream affects fleet-customer-delivery promises.

**KEVEN:** And the Wave-positioning —

**MARCUS:** Wave 1 for a specific plant — typically Mt. Holly or Cleveland NC as the pilot site. The equipment-telemetry data foundation is stronger at the more recently modernised plants. *Pick the plant with the cleanest equipment-telemetry foundation for the first pilot.*

### Play three — Quality Escape Detection and Root Cause (AXLE-QUAL-01)

**MARCUS:** Play three. Quality escape detection.

**KEVEN:** Different from Play 1 (Warranty Traceability) — *Play 3 is upstream of the field claim.* Quality Escape Detection identifies build defects *before they ship.*

The DTNA context. Quality events on the line — inspection failures, measurement out-of-spec, defect callouts — are recorded daily. Most are resolved at the workstation level. *Some are missed.* The missed ones become quality escapes — defective units shipping to customers. Field claims, recalls, brand damage downstream.

The pain point. *Most quality systems are reactive — they catch what's visible.* They don't continuously correlate quality events to identify *patterns* that the line operator wouldn't see. A specific torque-tool wearing in a specific way, on a specific shift, in combination with a specific supplier-lot variation — the pattern is invisible to humans, visible to an agent reasoning across the data.

The agent strategy. The quality escape agent reads quality-event streams continuously, correlates against build records, identifies emerging defect-pattern clusters *before they accumulate into a multi-million-dollar field claim.* Engineering team approves intervention — line-side investigation, tool replacement, supplier callback, additional inspection station.

The architectural shape. Streaming Bronze for quality-event data. Silver maps to the AXLE quality-event canonical (joining on VIN). Gold per-line and per-pattern emerging-cluster features. The agent uses pattern-matching across multiple AXLE families — quality event, build record, assembly asset.

The KPI signal. *Quality escapes per 1000 units reduction 30-50 percent on covered patterns.* Reduces downstream warranty-claim feed.

**MARCUS:** Note the architectural reuse —

**KEVEN:** This is the compounding-asset thesis at work. *Play 3 uses three of the same four AXLE canonical families as Play 1.* Once Play 1 lands at DTNA, the Silver foundation is largely in place for Play 3. *Wave 2 incremental cost is dramatically lower than Wave 1.* This is the framework's commercial pitch made real at DTNA — and the Account Team should position it explicitly during Wave 1 conversations.

### Play four — Plant-Floor Agent Assist for Manufacturing Engineers

**MARCUS:** Play four. Plant-floor agent assist.

**KEVEN:** Plant-floor manufacturing engineering at DTNA is *information-composition work.* Manufacturing engineers compose across engineering-change-notice systems, supplier-quality systems, equipment-condition data, training records, and standard work documents to diagnose line issues and recommend interventions.

The pain point. *The composition is manual.* When a line issue surfaces, the manufacturing engineer toggles between five-to-eight systems to gather context. *Mean-time-to-engineering-decision* on the floor is longer than it needs to be.

The agent strategy. *The contact-center agent-assist pattern* from the Services Podcast applied to the manufacturing floor. The agent listens to or observes the engineer's diagnostic activity, surfaces relevant context from across systems in real time, drafts intervention recommendations, captures the decision and outcome for downstream learning.

*Engineer approves and acts.* The agent doesn't decide; the agent composes.

The architectural shape. Cross-family canonical access — manufacturing engineering documents, equipment telemetry, supplier-quality signal, training records. Gold mart shapes per-engineer per-issue context views. The MCP tool surface is broad — typically 10-15 narrow tools spanning the systems the engineer composes across.

The KPI signal. *Manufacturing-engineering decision velocity 30-50 percent improvement.* Lower variance in engineering responses (which translates to higher line consistency). Engineer satisfaction — the work becomes "engineering decisions" not "system navigation."

**MARCUS:** And the cross-Practice pattern —

**KEVEN:** *This is the same architectural pattern as the contact-center agent-assist from Services Podcast Episode 11.* The Service is portable. The framework's cross-Practice reuse thesis applies — the team that delivers contact-center agent-assist can deliver manufacturing-engineering agent-assist with substantially shared engineering investment.

### Play five — Supplier Traceability and Quality Coordination

**MARCUS:** Play five. Supplier traceability.

**KEVEN:** Commercial truck supply chains are *complex and tiered.* DTNA's Tier 1 suppliers feed Tier 2 and Tier 3 below them. A single component on a Cascadia traces back through multiple supplier tiers. *When a quality issue surfaces, identifying which tier's lot is responsible is investigative work.*

The pain point. *Supplier-quality coordination is partly digital and partly relationship-driven.* Tier 1 suppliers have well-instrumented data; Tier 2 and Tier 3 are variably digital. Identifying defect-pattern correlation across tiers takes engineering judgment plus data.

The agent strategy. The supplier-traceability agent maintains a continuous supplier-quality posture view — *which suppliers are trending toward emerging risk, which lots are correlated with field quality signal, which tier-2 supplier issues are driving tier-1 events.* Supplier-quality team reviews emerging signals and prioritises supplier coordination.

The architectural shape. Heavily reliant on supplier-quality data that DTNA has been digitising over years. The supplier-quality canonical at Silver. Gold per-supplier per-lot quality features.

The KPI signal. *Supplier-quality issue mean-time-to-detect compression* — typically weeks to days. *Supplier-coordination cycle compression.* *Tier-2 issue prevention* — fewer surprises from upstream tiers.

**MARCUS:** And the strategic frame —

**KEVEN:** *This play is partly about supplier-relationship maturity.* APEX's supplier-traceability capability gives DTNA a stronger position in supplier negotiations and in supplier-quality coordination conversations. *Beyond the dollar value of incident reduction*, the play strengthens the *commercial leverage* DTNA has with its supplier base.

### Play six — Production Planning and Scheduling Agent

**KEVEN:** Play six. Production planning.

**MARCUS:** Production planning at DTNA is *cyclical and forecast-driven.* Demand forecasts from sales-and-operations planning, capacity assessments from manufacturing, supplier-commitment status, raw-material lead times, plant labour planning — all compose into the production schedule. *In a stable cycle, the planning is manageable.* In a volatile cycle — like the post-pandemic period — the variance overwhelms the planning cadence.

The pain point. *Planning cycles are too slow for cyclical volatility.* Monthly S&OP, weekly production reviews. By the time a planning adjustment is implemented, the market signal that motivated it has shifted.

The agent strategy. Production-planning agent reads continuously across demand signal, supplier-commitment status, plant-capacity signal, labour-availability. *Surfaces planning-adjustment recommendations* with explanation of the trigger. Planning leadership approves.

*The agent doesn't replace S&OP.* The agent gives S&OP a faster, more continuous decision substrate.

The architectural shape. Cross-system canonical at Silver covering demand, supply, capacity, labour. The Gold mart shapes per-product, per-plant, per-line capacity-and-demand reconciliation. The MCP tool surface spans the four-or-five major input systems.

The KPI signal. *Production-plan revision cycle compression — typically weekly cadence to daily continuous.* *Forecast accuracy improvement +10-15 percent on covered product lines.* *Reduction in expedited-shipping cost from supply-demand mismatch.*

**MARCUS:** And the Wave-positioning —

**KEVEN:** Wave 2 typically — depends on the Wave 1 canonical foundation being in place. *Production planning is data-foundation-heavy because the data lives in multiple legacy systems (ERP, MES, S&OP planning).* Wave 1 in warranty or quality escape pays down some of that foundation.

### Cross-cutting observations

**MARCUS:** Step back. What does the Account Team take away across the six manufacturing-and-quality plays?

**KEVEN:** Three things.

One — *Zero Day Warranty is the headline play.* If the Account Team has one shot at a Wave 1 conversation, this is it. *Dollar visibility, executive engagement, clean reference-scenario story.*

Two — *Plays 1 through 5 share architectural foundation.* AXLE canonical families. Silver-at-anchor discipline. The compounding-asset thesis is *enormously* valuable at DTNA because the framework has already paid for the foundation; Plays 2 through 5 cost incrementally less to deploy.

Three — *Play 6 (production planning) is the strategic-CFO conversation.* CFO conversations about working-capital optimisation and supply-demand reconciliation land here. *Wave 2 or 3 placement; positioning starts in Wave 1.*

### A reading I want to do

**MARCUS:** I want to read from a recent industry analysis on commercial-truck warranty trends.

**KEVEN:** Read it.

**MARCUS:** [reading, paraphrased]

*"The structural increase in commercial-truck warranty costs over the past two decades reflects vehicle complexity growing faster than warranty-management capability. The OEMs that compress investigation latency through agentic AI and cross-system data composition will recover materially more supplier-chargeback revenue and reduce warranty escapes through faster line-side intervention. The capability gap between leading and lagging OEMs on warranty management is widening."*

[pause]

**KEVEN:** *The capability gap is widening.* That's the urgency framing for any DTNA CFO or warranty executive. *Wait, and competitors close the gap. Move now, and DTNA leads.*

### One disagreement

**KEVEN:** Pushback.

**MARCUS:** OK. The *six plays we walked* are the AXLE Practice's curated manufacturing-and-quality scenarios. I want to push on whether there's a *seventh play* the Account Team should consider — *generative-engineering for vehicle design and validation.*

**KEVEN:** Go.

**MARCUS:** The Sellers Guide mentions generative-engineering as a wedge for AXLE. *For DTNA specifically*, the use case includes powertrain design optimisation (especially for the eAxle and electrification powertrains), validation simulation, and engineering change-notice generation. The data foundation here is *engineering data*, not manufacturing data — different and less directly leveraged from Wave 1 manufacturing investment.

It's a *Wave 3+ play* — strategic, technically interesting, but slower-cycle than the manufacturing-floor plays. *The Account Team shouldn't lead with it. The Account Team should be aware of it for the strategic-CTO conversation about engineering velocity.*

**KEVEN:** Agree. *Six manufacturing-and-quality plays for Wave 1-2 entry. Generative-engineering as a Wave 3+ strategic frame for the CTO conversation.*

**MARCUS:** Yes.

### What to carry forward

**KEVEN:** Three things.

One — *Zero Day Warranty is the flagship play for DTNA.* AXLE-WRTY-01. CFO and quality executive conversation. The starting point for most Wave 1 engagements.

Two — *Five additional manufacturing-and-quality plays share architectural foundation.* Predictive maintenance, quality escape, plant-floor agent assist, supplier traceability, production planning. The compounding-asset thesis lands here.

Three — *Generative engineering is a Wave 3+ strategic frame*, not a Wave 1 entry. Useful for the CTO conversation; not the lead play.

**MARCUS:** Next episode — *The Connected Vehicle & Aftermarket Plays.* Detroit Connect diagnostic acceleration. Dealer network performance. Parts demand forecasting. Service-bay agent assist. Fleet customer experience. Driver-facing in-cab assistance. Six plays touching the customer side of DTNA's business.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn — relevant for manufacturing-and-quality

- **Microsoft Cloud for Manufacturing** · Microsoft Learn
- **Azure IoT for industrial telemetry** · Microsoft Learn
- **Microsoft Fabric Real-Time Intelligence for plant data** · Microsoft Learn

### Industry context

- **AIAG (Automotive Industry Action Group)** — quality and supplier-quality standards · [aiag.org](https://www.aiag.org/)
- **SAE International** — Class 8 truck engineering and quality standards · [sae.org](https://www.sae.org/)
- **NHTSA recall database** — Class 8 truck recall history · [nhtsa.gov](https://www.nhtsa.gov/)
- *"Commercial truck warranty cost trends"* — industry analyst publications (ACT Research, FTR)
- *"Supplier quality in commercial-vehicle production"* — AIAG publications

### From the APEX Trilogy podcasts

- **Services Podcast Ep 3-4** — the medallion and agent foundation
- **Services Podcast Ep 6 — *The Warranty Cost Spiral*** — the deep dive on the play that opens this episode
- **Services Podcast Ep 11 — *Contact-Center Labour Squeeze*** — the agent-assist pattern that maps to plant-floor agent-assist

---

**End of Episode 02 · The Manufacturing & Quality Plays**
*≈ 5,600 words · target 30 minutes at conversational pace*
