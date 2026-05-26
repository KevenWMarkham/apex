# Episode 06 · The Service Catalog

**Source:** *Professional APEX-M Services Guide* — Part VI (Chapters 18–24)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-12

> **Note:** Different from the Sellers Podcast Episode 4 (which covered the seven *Practices* commercially). This episode covers the *thirty-eight Services* — the actual productised workloads inside the seven Practices that ship in the APEX catalog.

---

## Cold Open

[Sound: stack of papers shuffled on a desk]

**MORGAN:** Let me tell you the moment in delivery that taught me what the Service Catalog actually is. I was three weeks into an engagement. The client had asked us to *"build agentic AI for warranty cost reduction."* That's the briefing we had. Three sentences.

[pause]

**KEVEN:** And the trap there is —

**MORGAN:** And the trap is — three sentences could be five different Services. *Warranty Traceability and Cost Avoidance* is one. *Claim-fraud Triage* is another. *Supplier-recovery Acceleration* is a third. *Connected-vehicle warranty signal triangulation* is a fourth. *Dealer-facing diagnostic acceleration* is a fifth. Each one is a *real product* — pre-built canonical schemas, pre-built agent shape, pre-built Gold mart, pre-built KPI envelope. If you start the engagement without first deciding *which Service* you're building — even if all five eventually ship in Wave Two — you've built nothing, you've just argued for three weeks.

**KEVEN:** And the catalog is —

**MORGAN:** The catalog is the menu. Thirty-eight Services across seven Practices. You pick. You don't invent. Today's episode is the tour.

**KEVEN:** I'm Keven Markham.

**MORGAN:** I'm Morgan. APEX Services Podcast, Episode Six. *The Service Catalog.*

---

## Theme Statement

**KEVEN:** Part Six of the Services Guide. Seven chapters — one per Practice. *Chapter Eighteen — RC, seven Services. Chapter Nineteen — HLS, four Services. Chapter Twenty — ER, six Services. Chapter Twenty-One — AXLE, five Services. Chapter Twenty-Two — TH, five Services. Chapter Twenty-Three — TMT, six Services. Chapter Twenty-Four — ICE, five Services.* Thirty-eight Services total.

**MORGAN:** And we're not going to do all thirty-eight in detail.

**KEVEN:** No. We're going to tour each Practice — name the Services, hit the architectural shape, point to the flagship Service in each. The chapter is your reference; the audio is your map.

---

## The Story

### Chapter 18 — RC · Retail & Consumer · 7 Services

**KEVEN:** RC Practice. Seven Services. Largest single-Practice catalog.

The seven —

**RC-CX-01.** *Loyalty Churn Prediction and Winback.* The flagship RC Service. Predicts which loyalty members are about to churn; orchestrates a personalised winback. Uses Customer-and-Loyalty plus Order families.

**RC-MERCH-02.** *Markdown Optimisation.* Predicts the right markdown depth and timing per SKU per store. Inventory family.

**RC-SUPCHN-01.** *Cold-Chain Excursion — Store Cooler.* The streaming-Bronze flagship. Cooler events through RTI, excursion triggers via Activator, agent emits remediation. Uses streaming Bronze plus Supply-and-Inventory canonical.

**RC-RISK-01.** *Returns Fraud Detection.* High-volume agent inference at the return desk. Returns history, customer pattern, store pattern.

**RC-OPS-02.** *Store Labour Forecasting.* Predicts labour demand by department by hour. Store-operations family.

**RC-OPS-03.** *Planogram Compliance Verification.* Vision-enabled. Compares actual shelf state to planned planogram. Uses NVIDIA Metropolis at the store edge in some deployments.

**RC-COM-04.** *E-commerce Search Personalisation.* Agent-augmented search. Personalised ranking that respects intent.

**MORGAN:** Architectural pattern for RC.

**KEVEN:** Most RC Services are *medium-velocity, batch-dominant, with one or two streaming exceptions.* The Order family is the workhorse — six of the seven Services consume it. RC-SUPCHN-01 is the streaming standout. RC-OPS-03 is the vision standout. Otherwise — predictable shapes, predictable Gold marts.

**MORGAN:** Flagship?

**KEVEN:** RC-CX-01 — Loyalty Churn. Easiest to demo. Highest cross-buyer interest. Best starting Service for a Wave One.

### Chapter 19 — HLS · Healthcare & Life Sciences · 4 Services

**KEVEN:** HLS. Four Services. Fewer than RC but the deepest governance demands of any Practice.

**HLS-CLIN-01.** *Care Gap Closure for Population Health.* The flagship HLS provider Service. Identifies patients with open care gaps, routes outreach. ClinicalEncounter family plus Claims-and-Utilization.

**HLS-CLIN-02.** *Claims Denial Prevention.* The flagship HLS payer-adjacent Service. Pre-submission denial-likelihood scoring. Claims family.

**HLS-CLIN-03.** *Clinical Decision Support — Oncology.* Highest-regulatory-bar Service. Augmented decision support for oncologist treatment-planning. HITL by policy. Used in Wave Two typically.

**HLS-CLIN-05.** *Prior Authorisation Automation.* The high-velocity HLS workhorse. Prior-auth draft generation. ClinicalEncounter plus Claims families.

**MORGAN:** Note the numbering jump — 01, 02, 03, 05. What happened to 04?

**KEVEN:** Section nineteen point — *Service-numbering convention.* The catalog reserves numbers; sometimes Services are deprecated or merged. HLS-CLIN-04 was *Clinical Trial Patient Matching* — it now lives as a pharma-adjacent extension in Wave Two. The number reservation preserves the catalog's stable identity space.

**MORGAN:** Architectural pattern for HLS.

**KEVEN:** *Purview-heavy. HITL-default. ClinicalEncounter plus Claims families dominate.* Every HLS Service ships with a heavier policy template, longer audit retention, and a stricter HITL gating by default. The CCO conversation is bigger and starts earlier.

**MORGAN:** Flagship?

**KEVEN:** HLS-CLIN-05 — Prior Auth. Highest demand. Most directly P-and-L visible. Best Wave One pitch.

### Chapter 20 — ER · Energy & Resources · 6 Services

**KEVEN:** ER. Six Services. The OT-data-heavy Practice.

**ER-NET-01.** *Distribution Outage Triage.* Utilities flagship. Real-time outage classification and crew dispatch. Utility-Network family.

**ER-NET-02.** *Pipeline Integrity — Leak Detection.* Oil-and-gas midstream. Streaming SCADA + acoustic. Upstream-Energy family.

**ER-NET-03.** *Predictive Wellhead Maintenance — Upstream Oil & Gas.* Upstream-Energy family. Production-decline curves + equipment-state.

**ER-NET-04.** *Refinery Yield Optimisation.* Downstream. Chemicals-Process family adjacent.

**ER-QUAL-01.** *Environmental Compliance Monitoring.* Cross-segment. Emissions, water, waste. Heavy Purview integration.

**ER-GRID-05.** *Demand-Response Orchestration.* Utility-Network plus customer-side. The energy-transition flagship.

**MORGAN:** Architectural pattern for ER.

**KEVEN:** *Streaming-heavy. RTI-dominant. Activator triggers are dense. The four-velocity-tier spectrum is *fully* exercised in ER more than any other Practice.* Many ER Services have a tier-one streaming layer plus a tier-three periodic layer running in parallel.

**MORGAN:** Flagship?

**KEVEN:** ER-NET-01 — Distribution Outage Triage. Most-replicated utility Service. Best opening demo for a utility CIO conversation.

### Chapter 21 — AXLE · Automotive · 5 Services

**KEVEN:** AXLE. Five Services. The Practice that gets the most NVIDIA composition.

**AXLE-WRTY-01.** *Warranty Traceability and Cost Avoidance.* The Zero Day Warranty scenario we've documented externally. The flagship. Four AXLE canonical families joined on VIN. The most complex orchestration in the catalog.

**AXLE-ASSET-01.** *Predictive Maintenance — Stamping Press OEE.* Assembly-Asset family. Sub-second streaming for equipment-state.

**AXLE-QUAL-01.** *Quality Escape Detection and Root Cause.* Quality-Event family plus Build-Record. Vision-augmented at the station — Metropolis composition.

**AXLE-CONNVEH-02.** *Connected-Vehicle Diagnostic Acceleration.* Connected-Vehicle plus Build-Record families. Telemetry-driven.

**AXLE-DEALER-03.** *Dealer Network Performance Analytics.* Connected-Vehicle plus Customer-side. Cross-tier dealer performance.

**MORGAN:** Architectural pattern for AXLE.

**KEVEN:** *VIN-joined canonical across four families. NVIDIA composition for inline vision and supplier-cohort analytics is common. The most complex catalog architecturally — and the deepest data joins.*

**MORGAN:** Flagship?

**KEVEN:** AXLE-WRTY-01 — Warranty Traceability. The Zero Day Warranty scenario. Most external visibility, most external collateral, most-likely-to-arrive-with-a-supporting-pack.

### Chapter 22 — TH · Travel & Hospitality · 5 Services

**KEVEN:** TH. Five Services. The traveller-profile-centred Practice.

**TH-OPS-01.** *Airline IROPs Recovery Orchestration.* The flagship. Disruption-driven rebooking, crew, equipment, comms. Traveller-Profile family plus operational data.

**TH-OPS-02.** *Property Operations Optimisation.* Hotel-side. Housekeeping, maintenance, demand-driven labour.

**TH-CX-01.** *Personalised Stay Experience.* Lodging-flavoured. Traveller-Profile family central.

**TH-RM-01.** *Revenue Management Augmentation.* Cross-segment. Forecast-and-pricing decision support.

**TH-LOY-02.** *Loyalty-Driven Experience Personalisation.* The mileage-program-aware sibling of TH-CX-01.

**MORGAN:** Architectural pattern for TH.

**KEVEN:** *Traveller-Profile family is the spine. Operational data integrations are diverse — PMS, CRS, GDS, IROPs systems. Real-time matters during disruption events; mostly batch otherwise.*

**MORGAN:** Flagship?

**KEVEN:** TH-OPS-01 — IROPs Recovery. The narrative. The single most pacy demo in the entire APEX catalog.

### Chapter 23 — TMT · Technology · Media · Telecom · 6 Services

**KEVEN:** TMT. Six Services. The Practice with the toughest technically-savvy buyer.

**TMT-CC-01.** *Contact-Center Agent Assist.* The flagship for telecom. Cross-segment for any large contact center. Section twenty-three point — points to Chapter 36 in Part IX for the deeper agent-assist architecture.

**TMT-NET-01.** *Network Operations Anomaly Triage.* Telecom. Network-event canonical streaming.

**TMT-CONTENT-01.** *Content Rights and Royalty Reconciliation.* Media. The Purview-heaviest TMT Service.

**TMT-AD-02.** *Ad-Tech Optimisation.* Media. Cross-property attribution.

**TMT-DEV-01.** *Developer Productivity Accelerator.* Technology. Internal-engineering Service.

**TMT-CX-03.** *Customer Effort Score Acceleration.* Cross-segment. Telco-led, content-services-applicable.

**MORGAN:** Architectural pattern for TMT.

**KEVEN:** *Highly variable. Contact-center Services share an architecture across TMT and beyond. Network-events Services are streaming. Content / media Services are batch with heavy lineage. Developer-productivity Services are Copilot-Studio-heavy.* No single dominant pattern — pick the Service, pick the architecture.

**MORGAN:** Flagship?

**KEVEN:** TMT-CC-01 — Contact-Center Agent Assist. Most-demanded. Most-demonstrable. Reusable across TMT-TEL, RC, HLS payer, and others.

### Chapter 24 — ICE · Industrial · Construction · Equipment · 5 Services

**KEVEN:** ICE. Five Services. The heavy-equipment-and-aftermarket Practice.

**ICE-AFTERMKT-01.** *Field Service Dispatch.* Flagship aftermarket. Service-ticket triage, technician routing, parts availability.

**ICE-AFTERMKT-03.** *Warranty Intake and Fraud Triage.* The aftermarket sibling of AXLE-WRTY-01. Dealer-network warranty claim flow with fraud-screen.

**ICE-AFTERMKT-05.** *Predictive Parts Demand.* Service-parts forecasting. The aftermarket-margin driver.

**ICE-CONNECTED-06.** *Dealer Network Performance.* Sibling of AXLE-DEALER-03 but heavy-equipment-shaped.

**ICE-EAAS-04.** *Equipment-as-a-Service Uptime Management.* The newest Service in the catalog. EaaS contract management with uptime-guarantee fulfilment.

**MORGAN:** Architectural pattern for ICE.

**KEVEN:** *Heavy re-use of AXLE and RC canonical families.* Section twenty-four point — *the canonical inheritance pattern.* ICE-AFTERMKT Services use Connected-Vehicle plus Customer-and-Loyalty. ICE-CONNECTED uses Connected-Vehicle plus Build-Record. ICE-EAAS uses Build-Record plus a derived contract-and-asset bundle. *Architecturally, ICE is a composition of AXLE plus RC patterns, not a new pattern.*

**MORGAN:** Flagship?

**KEVEN:** ICE-AFTERMKT-01 — Field Service Dispatch. Most-replicated. Cleanest demo. Lowest-friction Wave One.

### The catalog at a glance

**MORGAN:** OK. Thirty-eight Services. What does the catalog tell us?

**KEVEN:** Four observations.

One — **the catalog is not flat. Each Service has a numbered identity that's stable across the framework's history.** RC-CX-01 means something specific; the *01* in the suffix never gets re-used for a different Service.

Two — **about twenty percent of Services are streaming-dominant. The rest are batch-dominant with streaming elements.** ER and AXLE skew streaming; HLS and TMT-content skew batch.

Three — **every Service maps to one or more canonical schema families** — the fourteen we covered in Episode Three. The mapping is in the Service manifest. No new canonical without a governance gate.

Four — **the flagship of each Practice is the right Wave One starting Service in most engagements** — RC-CX-01, HLS-CLIN-05, ER-NET-01, AXLE-WRTY-01, TH-OPS-01, TMT-CC-01, ICE-AFTERMKT-01. Seven Services. Memorise them.

---

## APEX Facts

**MORGAN:** APEX Facts. Eight rapid.

**KEVEN:** Fact One — total Services in the catalog?

**MORGAN:** Thirty-eight.

**KEVEN:** Fact Two — Practice with most Services?

**MORGAN:** RC. Seven.

**KEVEN:** Fact Three — Practice with fewest Services?

**MORGAN:** HLS. Four.

**KEVEN:** Fact Four — Service-numbering convention?

**MORGAN:** Service IDs are stable across catalog history. Numbers are not re-used.

**KEVEN:** Fact Five — most architecturally complex Service?

**MORGAN:** AXLE-WRTY-01. Four canonical families joined on VIN.

**KEVEN:** Fact Six — Practice that re-uses other Practices' canonicals?

**MORGAN:** ICE. Composes AXLE and RC patterns.

**KEVEN:** Fact Seven — flagship Service per Practice?

**MORGAN:** RC-CX-01, HLS-CLIN-05, ER-NET-01, AXLE-WRTY-01, TH-OPS-01, TMT-CC-01, ICE-AFTERMKT-01.

**KEVEN:** Fact Eight — Service manifest contents?

**MORGAN:** Consumed canonical families, MCP tool catalog, Gold mart shape, KPI envelope, governance template, persona declarations.

**KEVEN:** Time.

---

## Adopt / Hold

**MORGAN:** Adopt versus Hold. Keven, Adopt.

**KEVEN:** Adopt — *the catalog as the source of truth for what we build.* Don't invent a custom Service for an engagement unless you've checked the catalog first and verified no existing Service fits. Most engagements try to be custom; most should be re-uses. The catalog is the assets the firm has invested in. Use them.

**MORGAN:** Hold. When is a custom Service the right call?

Two cases.

Case one — *the engagement is genuinely novel.* The client has a workload that doesn't map to any flagship in any Practice. This is rare — about one in twenty engagements in my experience.

Case two — *the engagement is a *catalog extension play.* The client's investment funds the new Service, which then graduates into the framework catalog. This is a deliberate product-investment motion. Section six point — *catalog extensions and the contribution path.*

**KEVEN:** Synthesis?

**MORGAN:** Default to catalog. Custom only when truly novel or when funding a catalog extension intentionally. Don't accidentally custom.

---

## Lessons

**KEVEN:** Monday-morning lessons.

One — **memorise the seven flagship Services.** RC-CX-01, HLS-CLIN-05, ER-NET-01, AXLE-WRTY-01, TH-OPS-01, TMT-CC-01, ICE-AFTERMKT-01. They are your default Wave One picks.

Two — **on every new engagement, in week one, map the client's stated need onto Services from the catalog. Pick one. Just one.** Wave Two scope grows from there.

Three — **read the chapter for the Practice you're engaged in cover to cover.** Not the Sellers Guide chapter — the Services Guide chapter. The Services Guide tells you what's *in the Service.*

Four — **every Service has a Service manifest. Read it before you write code.** It tells you what canonical you consume, what MCP tools you need, what KPI you commit to.

Five — **don't redesign a catalog Service. Extend it.** If the client needs more, file a catalog-extension request. The contribution graduates back into the framework.

---

## Carve Outs

**MORGAN:** Carve outs. Mine — pick the Practice that matches your current engagement, and *read all the Services* in that chapter. Even the ones not in your scope. The breadth tells you what the Practice is *capable of* — which informs Wave Two conversations.

**KEVEN:** Mine — read both Chapter 21 (AXLE) and Chapter 24 (ICE) side by side. ICE's canonical-inheritance pattern from AXLE is the cleanest example of how the catalog composes across Practices. Once you see that pattern, you start to see all the composition opportunities in the catalog.

---

## Sign-off

**KEVEN:** That's it for Episode Six. Next episode — *Superagents and Practitioner Tracks.* Parts Seven and Eight. The LEDGER plus Redis learning loop — how APEX agents *learn over time.* Plus the practitioner-track chapters — zero to RC-E2E-03 in a day, the HLS worked example, agent design patterns, performance and cost modeling.

**MORGAN:** See you there.

[outro]

---

**End of Episode 06 · The Service Catalog**
*≈ 5,200 words*
