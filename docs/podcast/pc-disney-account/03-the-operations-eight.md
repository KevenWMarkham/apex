# Episode 03 · The Operations Eight

**Builds on:** Disney Eps 1-2 (three segments, CX foundation) · Trilogy — Services Ep 3 (Real-Time Intelligence) · Deployment Ep 3 (Day-Zero / streaming patterns) · Services Ep 9 (Energy Operations — streaming-pattern reference)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: a quiet operations centre. Fans hum. Screens glow.]

**RILEY:** I want to start at four AM Pacific time. The Anaheim Operations Center for Disneyland. The graveyard shift is two hours from handoff. The team is monitoring — the night ride-systems checks, the inbound food deliveries for the morning, the maintenance windows that close before the park opens at eight. *And on a parallel screen* — somebody is monitoring the streaming delivery health for Disney+ globally. *Different teams. Different operations centres. Different KPIs. All running twenty-four hours a day.*

[pause]

**KEVEN:** And the operations footprint at Disney —

**RILEY:** The operations footprint at Disney is *enormous and heterogeneous.* Six parks worldwide. Cruise Line operations. Streaming delivery infrastructure across the planet. ESPN's live-broadcast infrastructure. Internal IT serving roughly two hundred thousand employees. Cyber operations protecting an enormous customer database and content library. *Every one of these operations centres exists and runs continuously today.* The agentic-AI opportunity here isn't *to replace* any of these centres. It's to *augment* the humans who run them so they can handle the scale and complexity that's still growing.

That's what this episode is about. Eight scenarios. Four in Network and Infrastructure — streaming delivery and Parks IoT. Four in Engineering R&D, Internal IT, and Cyber. *Operational depth at Disney scale.*

**RILEY:** I'm Riley.

**KEVEN:** I'm Keven Markham. Disney Account Podcast. Episode Three. *The Operations Eight.*

---

## The conversation

### Why operations matters even though CX is the entry

**KEVEN:** Set up where this fits.

**RILEY:** Episode Two covered the Customer Experience Six — the scenarios the Account Team typically uses as Wave 1 entry. *Operations is where the long-term value compounds.* After Wave 1 in CX has delivered, the natural next conversation at Disney is — *"where else does this scale?"* The Operations Eight is the answer.

The Operations Eight are *not* the right Wave 1 entry. They're *typically* Wave 2 or Wave 3. They have longer build cycles because operational data foundations are messier than customer data. *They also have larger long-term value* because they touch every-day operations.

The Account Team should understand this sequence — *CX first to land the relationship, Operations second to expand it.*

### Network and Infrastructure — the four scenarios

**KEVEN:** Walk me through the Network and Infrastructure group. Four scenarios.

**RILEY:** Let me set the context first, then walk each one.

The context — Disney's network-and-infrastructure footprint covers two very different domains. *Streaming delivery* — the CDN, the encoding pipelines, the playback telemetry, the buffering and quality-of-experience signals. *Parks IoT* — the ride-system instrumentation, the guest-flow sensors, the maintenance telemetry, the F&B operations sensors. *Both are operationally intensive. Both have agentic-AI applications. They are not the same.*

The four scenarios in the group split — roughly two on streaming side and two on Parks side. Let me name them with the framework's pattern even though the precise scenario codes are TMT-NET-01 through whichever applies.

**Streaming-delivery scenario one — quality-of-experience anomaly triage.** *The pain* — Disney+ delivers to two hundred million subscribers. Quality issues — buffering, codec failures, regional CDN problems — manifest unevenly. *The current detection cycle is operator-driven, with dashboards.* The agent strategy — agent watches the delivery telemetry continuously, identifies emerging quality issues at the regional or device-family or content-type level, recommends the operations response (CDN reroute, encoding-pipeline adjustment, content-replacement). *Time-to-detection compresses from hours to minutes.* The KPI is *playback-failure-rate reduction* and *time-to-quality-recovery.*

**Streaming-delivery scenario two — predictive capacity scaling.** *The pain* — Disney+ launches a major new release (Marvel premiere, Star Wars episode drop) and the load profile changes dramatically. The current scaling is reactive — auto-scalers respond after demand arrives. The agent strategy — agent reasons about the predicted load profile *before* the release lands, using historical launch patterns, marketing-campaign signals, current subscriber-base composition. Recommends capacity pre-scaling — encoding pipeline, CDN, edge cache. *The infrastructure team approves the scaling plan.* The KPI is *cost of overprovisioning reduction* (you don't pre-scale for a non-event) and *availability during launch* (you don't under-scale for a hit).

**Parks IoT scenario one — predictive ride-system maintenance.** *The pain* — every ride in every park is monitored. Ride downtime is operationally disruptive and guest-experience damaging. The current maintenance is largely calendar-based with reactive intervention. The agent strategy — agent reads ride-system telemetry, identifies developing maintenance needs *before* failure, recommends maintenance windows that minimise guest-impact (overnight closes during low-demand seasons rather than mid-day during peak). *Engineering team approves.* The KPI is *ride downtime reduction* and *maintenance cost optimisation.*

**Parks IoT scenario two — guest-flow optimisation.** *The pain* — Parks operate at near-capacity during peak periods. Crowd density at attractions varies dramatically. *The Disney IP at the ride-level is exceptional; the cross-park guest-flow data has historically been underutilised for real-time optimisation.* The agent strategy — agent reads guest-position telemetry (MagicBand+, location sensors), reasons about real-time flow patterns, recommends operational interventions (open additional rides, adjust dining peak hours, deploy character meet-and-greets to relieve congestion zones). *Park operations team approves.* The KPI is *peak-period guest satisfaction* and *operational-throughput-per-park-hour.*

**KEVEN:** And what these four share architecturally —

**RILEY:** All four are *streaming-Bronze-dominant.* All four use the Real-Time Intelligence Eventstream-to-Eventhouse pattern we covered in the Services Podcast — the cold-chain scenario in Episode 7 is the direct architectural analog. All four use Activator for threshold-based triggers. *All four are operational-data-foundation-heavier than the CX scenarios* — which is why they're typically Wave 2, not Wave 1.

### Engineering R&D, Internal IT, Cyber — the four scenarios

**KEVEN:** And the second group of four — Engineering R&D, Internal IT, Cyber.

**RILEY:** These cluster around *Disney's own engineering and operations teams.* These are *internal-facing* agents — the customers are Disney's own employees. Different shape from the customer-facing CX scenarios.

**Engineering R&D scenario — software-engineering productivity acceleration.** *The pain* — Disney's engineering organisation is large. Productivity gains compound enormously. *The current state* — engineers are increasingly using Copilot-style assistance in their development workflows, but the *organisation-wide* productivity story isn't measured cleanly. The agent strategy — agentic augmentation of code review, design-doc generation, technical-marketing content production, internal-documentation maintenance. *The Service is an agent-augmented engineering-productivity platform* deployed against Disney's own dev teams. The KPI is engineer-time-saved per task type, plus product-velocity downstream.

**Internal IT scenario — agent-augmented IT service-desk.** *The pain* — Disney's IT serving 200,000+ employees globally. The IT service-desk handles enormous ticket volume — password resets, access requests, software-deployment issues, hardware troubleshooting. *Current service-desk operations are sized to the volume.* The agent strategy — the contact-center pattern from Services Podcast Episode 11 *applied to IT.* Agent assists the human IT support tech with cross-system context, drafts response, recommends resolution path. AHT down, FCR up, ticket-resolution-time compressed. The KPI is the standard contact-center KPI cluster — *AHT, FCR, CES, attrition.*

**Cyber scenario one — security operations augmentation.** *The pain* — Disney's cyber operations protect an enormous attack surface. Customer-database, content-library, internal-IT, third-party-integration surface. Cyber-operations volume — thousands of alerts per day. *Alert fatigue is real.* The agent strategy — agent reasons about alert composition continuously, composes context across telemetry sources, recommends triage and response. The cyber-SOC analyst gets *prioritised, context-rich alerts* rather than firehose. The KPI is *mean-time-to-detect and mean-time-to-respond* improvements, plus analyst-throughput.

**Cyber scenario two — third-party-risk and supply-chain-security monitoring.** *The pain* — Disney's third-party ecosystem (vendors, content partners, technology suppliers) creates indirect security exposure. *Current third-party-risk programs are largely annual-assessment driven.* The agent strategy — continuous monitoring of third-party security posture, agentic reasoning about emerging risk signals, recommendation of which third parties to escalate. *Risk-management team prioritises.* The KPI is *third-party-incident reduction* and *response-time-to-emerging-risk improvement.*

**KEVEN:** And the buyer for each of these —

**RILEY:** Different from the CX scenarios. *Engineering R&D* — the CTO of the corporate technology organisation and the platform engineering leadership. *Internal IT* — the CIO's organisation, specifically the IT operations and service-desk leadership. *Cyber* — the CISO and the security operations leadership. *Each of these is a separate buyer from the CX leadership.* The Account Team needs different relationship paths for each.

### Cross-scenario observations across the eight

**KEVEN:** Step back. What does the Account Team need to know about *all eight* operations scenarios?

**RILEY:** Three things.

One — *all eight rely on operational data foundations that are messier than customer data foundations at Disney.* Ride systems were instrumented over decades; the telemetry quality varies. IT systems generate enormous logs but with varying signal-to-noise ratios. Cyber telemetry comes from many vendors and tooling layers. *Wave 1 in operations is harder, slower, and more expensive than Wave 1 in CX.* That's why the Account Team typically sequences CX first.

Two — *the buyers across the eight are fragmented.* CX has *maybe* three buyers across the six CX scenarios — the Chief Customer Officer, the President of Disney+, the President of Hulu. Operations has *eight or more* buyers — CTO, CIO, CISO, COO Experiences, head of Streaming Delivery, head of ESPN operations, head of internal IT operations, etc. *The relationship complexity is higher.*

Three — *the long-term value of operations scenarios is larger.* Customer-experience scenarios drive subscriber retention and revenue lift — meaningful, measurable, near-term. Operations scenarios drive *operational cost reduction and resilience* — which over a multi-year horizon compound to larger value, especially when combined across multiple operations centres. *The Wave 3 picture at Disney is largely operations-dominant.*

### A reading I want to do

**RILEY:** I want to read something from a Disney 2024 CapEx commitment.

**KEVEN:** Read it.

**RILEY:** [reading, paraphrased]

*"We are committed to invest approximately 60 billion dollars in our Experiences business over the next decade. This investment will expand capacity, enhance technology infrastructure across our parks and cruise operations, and accelerate our ability to deliver differentiated guest experiences. We see technology as a primary enabler of returns on this investment."*

[pause]

**KEVEN:** Sixty billion. Over ten years. *That's the scale of operational investment Disney is committing to.* The agentic-AI operations scenarios we've walked here aren't competing for that budget — they're *enabling* it. The agent that optimises guest flow at the parks is part of how Disney gets ROI on the parks investment. The agent that monitors streaming delivery quality is part of how Disney protects the streaming-DTC profitability commitment.

**RILEY:** And the Account Team's framing for the operations conversation —

**KEVEN:** *"You're investing sixty billion in Experiences. Our operations agents are how you protect and accelerate that return."* That's the framing for the COO of Experiences conversation.

### One disagreement

**KEVEN:** Pushback.

**RILEY:** OK. Let me push on the *agent-augmented IT service-desk* scenario. Because Disney's internal IT is *highly outsourced* — much of the front-line service-desk work is delivered by external providers, not by Disney employees. The economic model is different.

**KEVEN:** Different how?

**RILEY:** The cost of the service-desk *isn't a Disney employee-cost line.* It's an outsourced-services contract line. The agent's productivity lift doesn't *directly* save Disney money in headcount — it changes the economics of the outsourced contract. *Which may be valuable, but the conversation is different.* The CIO of Disney isn't motivated to lift productivity of contractors; the CIO is motivated to lift *quality of service* and *reduce contract-renegotiation friction.*

**KEVEN:** So the seller's framing for that specific scenario at Disney —

**RILEY:** *"Better service quality for your employees. Better internal NPS. Better re-negotiation leverage with your outsourcing partners."* Not — *"reduce service-desk cost." The cost is already paid; the value is qualitative.*

**KEVEN:** Good catch. *Each operations scenario has Disney-specific positioning.* Generic operations-cost-reduction pitches don't land at Disney the way they would at other clients. The Account Team has to understand which scenarios *can* claim cost-reduction (predictive ride maintenance — yes, it's Disney-employee labour) and which can't (IT service-desk — it's outsourced).

**RILEY:** Yes.

### What to carry forward

**KEVEN:** Two things.

One — *eight operations scenarios across two groups — Network/Infrastructure (streaming delivery + Parks IoT) and Engineering/Internal IT/Cyber.* Higher build-cost than CX; larger compounding long-term value.

Two — *operations scenarios at Disney require Disney-specific positioning.* Generic operations-cost-reduction framing doesn't always land. The Account Team customises by scenario.

**RILEY:** Next episode — *The Ladder for Disney.* How the four-level ladder from the Sellers Podcast climbs at Disney specifically. L1 wedge with a Disney-tailored heatmap. L2 Wave 1 candidate. L3 B2B fleet vision for TMT-MED Practice at Disney. L4 B2C transformation — what direct-to-consumer agentic looks like at Disney scale. Plus the two build/deploy meta-scenarios.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn — relevant for operations scenarios

- **Microsoft Fabric Real-Time Intelligence** · Microsoft Learn
- **Azure IoT for industrial / experiential** · Microsoft Learn
- **Microsoft Sentinel for security operations** · Microsoft Learn
- **Azure Monitor for operations telemetry** · Microsoft Learn

### Microsoft Tech Community blogs

- **"AI for operations centres"** · Microsoft Industry Blog
- **"Security-operations augmentation with AI"** · Microsoft Security Blog
- **"Predictive maintenance at consumer scale"** · Microsoft Manufacturing Blog

### Industry context

- **NAB Show — broadcast and streaming infrastructure**
- **SVTA — Streaming Video Technology Alliance** · industry standards
- *"Sports streaming infrastructure 2025"* · SportsTechie analysis
- **TEA (Themed Entertainment Association)** · Parks industry benchmarks
- *"The economics of theme-park operations"* · TEA Visitor Attendance Reports (annual)
- **MISTI / SANS** · security-operations frameworks

### Disney public materials

- **Disney 2024 Q1 transcript on Experiences capacity expansion** · IR
- **Disney CapEx commitment of $60B over 10 years** · press releases and IR materials
- **ESPN-DTC announcements** · 2024-2025 quarterly transcripts

### From the APEX Trilogy podcasts

- **Services Podcast Ep 3 — *The Medallion in Depth*** — Real-Time Intelligence patterns for streaming Bronze
- **Services Podcast Ep 7 — *Cold-Chain Shrink in Grocery*** — the streaming-Bronze pattern that maps to operations
- **Services Podcast Ep 9 — *The Energy-Transition Operations Gap*** — the operations-control-room pattern that maps to Disney's operations centres
- **Services Podcast Ep 11 — *The Contact-Center Labour Squeeze*** — the agent-assist pattern that maps to IT service-desk
- **Deployment Podcast Ep 3 — *Building the Tenant*** — the Day-Zero motion that brings the operations foundation up

---

**End of Episode 03 · The Operations Eight**
*≈ 5,800 words · target 30 minutes at conversational pace*
