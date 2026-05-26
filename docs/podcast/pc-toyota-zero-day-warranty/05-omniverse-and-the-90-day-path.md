# Episode 05 · Omniverse, Toyota's NVIDIA Estate, and the 90-Day Path

**Builds on:** Toyota Eps 1-4 (the full architecture) · Sellers Podcast Ep 2 (the commercial arc / two-contract model) · Sellers Podcast Ep 8 (the four-level ladder) · Disney Account Podbook Ep 5 (account-team playbook pattern) · Trilogy — Services Podcast Ep 4 (MCP boundary) · NVIDIA developer docs (Omniverse, NeMo, Triton, NVIDIA AI Enterprise)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: a digital-twin Woven City scene. Quiet, almost futuristic ambient. A faint synth pad. The soft hum of a render farm warming up. A simulation timestep tick — bup, bup, bup — almost subliminal.]

**MIA:** I want to start at the base of Mount Fuji. *Susono City, Shizuoka Prefecture.* Toyota's Woven City — the prototype mobility-and-software city Toyota has been building for years. In the version of this scene I want you to picture, it is running as a real-time digital twin. *Not a rendering. Not a marketing animation. A live, physics-grounded, sensor-fed simulation of the city itself* — autonomous shuttles, energy grid, pedestrian flows, building systems, test vehicles on the test loops. *All of it, mirrored in software, in real time.*

[pause]

**KEVEN:** And the platform that twin runs on.

**MIA:** *NVIDIA Omniverse.* Public reference — Woven by Toyota and NVIDIA have been operating Woven City as a city-scale Omniverse simulation since the project's early phases. *Not hypothetical. Operational today.* NVIDIA's own communications and Toyota corporate releases cover it; trade press has been writing about it for years.

[pause]

**KEVEN:** Which means Toyota is already running NVIDIA Omniverse — at the scale of a city.

**MIA:** *At the scale of a city.* The question this episode walks is — *what would it mean to run Omniverse at the scale of a plant?* For the same Zero Day Warranty data we built across Episodes 1 through 4. *Toyota is already an NVIDIA customer. The conversation is not about adding NVIDIA. It is about extending what Toyota already runs into a new operational domain.*

**KEVEN:** And the second NVIDIA reference point at Toyota — *Toyota Drive on NVIDIA.* Announced in 2025. Toyota Motor Corporation uses the NVIDIA Drive platform for autonomous-vehicle development. *Different workload than Woven City — same operational comfort with NVIDIA at Toyota.*

**MIA:** Two confirmed public footprints. Woven City on Omniverse. Toyota Drive on NVIDIA. *And the rest of this episode walks how the Zero Day Warranty extension uses different parts of that same estate — Omniverse for plant simulation, NeMo for the language layer, Triton at scale, NVIDIA AI Enterprise as the supported bundle. Plus the 90-day pilot path, the sponsor question we left open in Episode 1, the funding model, and the Account Team handoff.* This is the series finale. The Zero Day Warranty Podcast. Episode Five. *Omniverse, Toyota's NVIDIA Estate, and the 90-Day Path.*

**KEVEN:** I'm Keven Markham.

**MIA:** I'm Mia. Let's walk what extending the estate looks like.

---

## The conversation

### Toyota's existing NVIDIA estate — two clear footprints

**KEVEN:** Anchor the credibility before we walk anything else. *Toyota is not a new NVIDIA customer.*

**MIA:** Two public footprints. *Woven by Toyota and Woven City* — Toyota's mobility-and-software subsidiary, headquartered in Japan, running Omniverse for the city-scale digital twin at the base of Mount Fuji. References in Toyota Newsroom, in Reuters Automotive coverage, in NVIDIA's developer-blog coverage. *Not a pitch — reporting on what already exists.* And *Toyota Drive on NVIDIA*, announced in 2025 — Toyota Motor Corporation using the NVIDIA Drive platform for autonomous-vehicle development. References in NVIDIA press, Reuters Automotive, automotive trade publications. *Different workload, same NVIDIA operational relationship at Toyota.*

**KEVEN:** And the consequence for the Zero Day Warranty conversation.

**MIA:** *The runway is short.* Toyota's IT, engineering, and procurement organizations already have working processes for NVIDIA. *Procurement does not have to onboard a new supplier. Engineering does not have to learn an unfamiliar stack. Legal does not have to negotiate a first-time agreement.* The Zero Day Warranty extension uses different parts of the NVIDIA estate than Woven City or Drive — Metropolis, DeepStream, and Jetson at the station from Episode 4; now Omniverse for plant simulation, NeMo for the language layer, Triton at scale, NVIDIA AI Enterprise as the supported bundle. *But the operational comfort with NVIDIA already lives at Toyota. We are extending an existing customer relationship, not initiating one.*

**KEVEN:** *Extending, not initiating.* That framing matters. When Chris Crotts hears NVIDIA in the conversation, the response is not "we don't run NVIDIA" — it is "we run NVIDIA over there; where would it go over here." *The conversation gets to the operational question fast.*

**MIA:** And the honest framing. *NVIDIA is named as a capability that fits this architecture, not as a Deloitte recommendation the way Microsoft is.* Toyota already chose NVIDIA. *Our job is to name accurately where the existing NVIDIA estate composes with the Microsoft data fabric to deliver the Zero Day Warranty posture.*

### Omniverse for plant simulation — the digital-twin extension

**KEVEN:** Now the headline extension. *Omniverse at the plant.*

**MIA:** *NVIDIA Omniverse is the simulation platform.* At Woven City scale, it operates as a city-scale digital twin. *At plant scale, the same platform applied to a manufacturing line* — the geometry of the plant, the equipment at each station, the material flow, the operator paths, all available as a live, sensor-fed twin.

**KEVEN:** And the relationship to the data foundation from Episode 2.

**MIA:** *Omniverse extends the four-domain Microsoft Fabric foundation into a physically-grounded simulation layer.* The same canonical Silver on OneLake the agent reasons across — vehicle build record, connected vehicle warranty data, quality events, assembly telemetry, plus the inference-event stream from Episode 4 — gets projected into a 3D simulation that plant engineering can interact with.

**KEVEN:** Walk what that unlocks.

**MIA:** *Counterfactual simulation.* The thing plant engineering most wants to do — and today most struggles to do — is *ask the line a what-if question without disrupting the line.* What if we changed this station's torque setting by half a Newton-meter? What if we re-sequenced the inspection on station forty-two? What if this supplier's lot-to-lot variance increased — would our station-level catch rate hold? *Today the answer is a physical trial, or a small computational model disconnected from production data. With Omniverse against the canonical Silver, the answer is simulate it against the actual data and see what happens.*

**KEVEN:** And the audit posture.

**MIA:** *The audit posture from Episode 3 wraps the simulation just like it wraps the agent.* Every simulation run produces a record — what scenario, against what data snapshot, with what assumptions, producing what outcome. *That record lands on Bronze the same way every other event lands.* The LEDGER hash chain references it when the agent or the engineer cites a simulation result. *If a Quality Director three months later wants to know why a particular line change was approved, the answer includes the Omniverse simulation that informed the decision — replayable, hash-chained, governed.*

**KEVEN:** And the practical pattern.

**MIA:** *Ask the digital twin first. Validate on the line second.* Counterfactuals that today take a week of plant time to physically trial — or that today simply don't get trialled because the risk is too high — get tested in the twin in hours. The ones that look promising get validated on the line in a controlled run. *The line itself becomes the system of record, not the experimentation surface. Faster experimentation than physical plant changes, with the audit posture intact.*

**KEVEN:** And the framing for the listener.

**MIA:** *Woven City taught Toyota how to operate Omniverse at one elevation. Zero Day Warranty extends that capability to a different elevation — the plant.* Same platform. Different scope. *Most automakers are starting Omniverse adoption from zero. Toyota is starting from a working Woven City deployment. That is a structural advantage.*

**KEVEN:** *A structural advantage.* Hold that — it comes back at the close.

### NeMo — domain language models and retrieval

**KEVEN:** Now the language layer. *NVIDIA NeMo.*

**MIA:** *NVIDIA NeMo is the framework for building and training domain-specific language models.* Not a single model — the toolkit for adapting language models to a specific domain. Pretraining hooks, fine-tuning workflows, retrieval components — what NVIDIA calls NeMo Retriever. *The framework that turns a general-purpose LLM into a domain LM for a specific corpus.*

**KEVEN:** And the Toyota fit.

**MIA:** *The four-domain corpus and the language that surrounds it.* Warranty claim narratives — dealer-written, technician-written. Build record metadata — station names, tool IDs, supplier part identifiers in plant-specific shorthand. Quality event descriptions, inspector notes, defect taxonomies. Supplier specifications — engineering drawings, material certificates, often in supplier-specific format. Technical service bulletins from the field organization. *That whole corpus is language-heavy, domain-specific, and today not searchable as a single body of knowledge.*

**KEVEN:** Walk the use cases.

**MIA:** Three. *First — the quality engineer asks a natural-language question of the corpus.* "Show me every warranty claim in the past eighteen months that mentions intermittent sensor harness behavior on Camry-platform vehicles built in Kentucky." Today that takes a structured query, a content-search pass, and a manual review. *With NeMo Retriever over the four-domain corpus, the agent answers in seconds — grounded in canonical Silver, with the audit row showing exactly which records the answer references.*

*Second — the chargeback evidence package prose.* Episode 3's phase five — the agent drafts the chargeback evidence package. *With NeMo in the drafting step, the agent produces fluent prose grounded in the audit-row chain — Toyota-specific prose, calibrated to how Toyota Quality writes supplier communications.* The supplier reads a document that sounds like Toyota wrote it.

*Third — multilingual retrieval.* Toyota is a global enterprise. Tier-1 supplier specs come in Japanese, English, Spanish, multiple European languages. *NeMo handles the multilingual retrieval natively.* Query in English, the relevant Japanese-language document is found, the relevant section surfaced, the translation generated. *Grounded in the actual supplier document, not hallucinated.*

**KEVEN:** And the relationship to the Agent Framework runtime.

**MIA:** *NeMo augments the Agent Framework — does not replace it.* The agent on Foundry still does the reasoning chain — the 24 steps, the cohort logic, the statistical work, the audit-row writing. *NeMo provides the language interface and the retrieval layer the agent calls when language work is the right tool.* Another endpoint in the agent's toolbelt. The agent reasons; NeMo retrieves and generates; the audit chain captures both.

**KEVEN:** And the hosting question.

**MIA:** *NeMo runs on the inference fabric inside Toyota's Azure tenant — the same NIM and Triton fabric from Episode 4.* No data crosses to a NVIDIA-hosted environment. *Toyota's data stays in Toyota's tenant. NeMo is the framework; the model, the corpus, the inference are all inside Toyota's perimeter.*

### Triton Inference Server — model serving at scale

**KEVEN:** Now the operational substrate. *Triton.*

**MIA:** *NVIDIA Triton Inference Server is the open-source inference-serving platform.* Episode 4 named Triton briefly; this episode opens it up. *Triton is the server underneath NIM's packaging. NIM is a pre-packaged endpoint for a specific model; Triton is the general-purpose platform that can host any model from any source.*

**KEVEN:** Walk what Triton hosts in the Zero Day Warranty architecture.

**MIA:** Three families of models. *Vision-AI models from Metropolis and DeepStream* — the Episode 4 stack — running on Triton at the Jetson devices at the cells. *Domain LMs from NeMo at the cloud or hybrid layer* — the chargeback-prose drafter, the multilingual retriever, the warranty-narrative classifier — hosted on Triton inside Toyota's Azure tenant. *Custom Toyota-trained models* — warranty-cohort classifiers, supplier-lot anomaly scorers, station-level defect predictors, predictive maintenance models. *Whatever Toyota trains in-house, Triton serves with the same SLA.*

**KEVEN:** And the value of consolidating on one inference platform.

**MIA:** *Consistent inference SLAs across the entire model estate.* Triton handles dynamic batching, multi-model concurrency, hardware abstraction, model versioning. *The same operational pattern serves a vision model at the station and a language model in the cloud.* One platform, one operational discipline, one observability surface.

**KEVEN:** And model portability.

**MIA:** *Models from any source.* Hugging Face transformers, NVIDIA's own NIM packages, in-house Toyota training output, open-source CV models from Metropolis, fine-tuned domain LMs from NeMo. *All run on Triton with the same deployment pattern.* If Toyota swaps a model in year three for a better one from a different source, the Triton operational layer doesn't change. *Model decisions become reversible — and that matters because the model landscape is moving fast.*

**KEVEN:** And the relationship to NIM.

**MIA:** *NIM is Triton with packaging on top.* A NIM is a specific model with the right runtime configuration, the right batching parameters, the OpenAI-compatible endpoint shape — bundled. *Triton is the platform NIM rides on.* For the workloads where NIM is the right fit, deploy NIM. For workloads where Toyota wants its own model with its own tuning, deploy directly on Triton. *Both end up on the same platform inside Toyota's tenant.*

### NVIDIA AI Enterprise — the umbrella

**KEVEN:** And now the commercial umbrella. *NVIDIA AI Enterprise.*

**MIA:** *NVIDIA AI Enterprise is the licensed, enterprise-supported software suite from NVIDIA.* The umbrella over CUDA-X, Triton, NIM, RAPIDS, NeMo, the Metropolis vision components, the Omniverse runtime — all of it. *The supported, production-grade bundle.* Not open-source self-service. *Enterprise support, security updates, lifecycle management, license-bounded usage.*

**KEVEN:** And the commercial unit Toyota licenses.

**MIA:** *Toyota licenses NVIDIA AI Enterprise from NVIDIA.* Direct license, NVIDIA paper. Just as Toyota licenses Microsoft Fabric from Microsoft on Microsoft paper. *Two separate platform contracts.* And — this is the Independence framing the Account Team needs to be fluent in — *Deloitte recommends the architecture; Toyota contracts with NVIDIA and Microsoft separately; Deloitte's services live on a third, separate Deloitte contract with Toyota.*

**KEVEN:** Spell out the three-contract model.

**MIA:** *Three contracts. Three actors. Two platform suppliers.*

Contract one — *Microsoft and Toyota.* Microsoft Fabric, Microsoft Agent Framework on Foundry, Microsoft Purview. Microsoft licenses Toyota directly on Microsoft paper. *Deloitte does not resell. Deloitte does not mark up. Deloitte does not take margin.*

Contract two — *NVIDIA and Toyota.* NVIDIA AI Enterprise covering Omniverse, NeMo, Triton, NIM, RAPIDS, the Metropolis stack. NVIDIA licenses Toyota directly on NVIDIA paper. *Same posture. Deloitte does not resell. Deloitte does not mark up. Deloitte does not take margin.*

Contract three — *Deloitte and Toyota.* The architecture work, the implementation, the change management, the Account Team continuity. Deloitte paper, Deloitte and Toyota. *Services only. No software.*

**KEVEN:** And the generalization from Episode 3.

**MIA:** *Episode 3 stated the two-contract model when the conversation was Microsoft-only.* This episode generalizes that to three contracts when both Microsoft and NVIDIA are involved. Same posture. *The recommendation is Deloitte's, on the merits. The licensing relationships are between Toyota and each platform supplier separately. The services relationship is between Deloitte and Toyota. No compensation flows from any platform supplier to Deloitte for the recommendation.*

**KEVEN:** And the reason to state it explicitly.

**MIA:** *Because a Toyota listener has to be able to repeat the model back accurately.* If a Toyota Procurement leader asks Chris Crotts about Deloitte's commercial relationship with NVIDIA, the answer is — *Deloitte does not have a commercial relationship with NVIDIA on this work. Toyota licenses NVIDIA AI Enterprise from NVIDIA directly. Deloitte recommends the architecture on the technical merits, and Deloitte provides the services on a separate Deloitte contract. That's the entire commercial picture.* That answer, said cleanly, is what makes the engagement clean.

### The 90-day pilot path — one Toyota plant, end to end

**KEVEN:** Now the operational close. *The 90-day path.* One Toyota plant. End to end. Five phases.

**MIA:** Walk them.

**KEVEN:** *Days 1 through 15 — Discovery.* Five things confirmed in order. *Executive sponsor* — Quality leadership at one of the plants, or Toyota Connected North America, or Manufacturing IT. We come back to that question in a minute. *Pilot plant* — Georgetown, Princeton, San Antonio, North Carolina, or one of the other ten. The choice balances data accessibility, executive sponsorship, and warranty-cluster history. *Business Value Assessment scope* — the BVA work begins; Microsoft funds the discovery via the Account Team. *Data access path* — which warranty cluster from the past eighteen months becomes the test case. *Microsoft Account Team coordination* — engaged in week one, operationally not commercially.

*Days 15 through 30 — Data access plus canonical mapping.* Map the four-domain canonical to Toyota's actual systems — vehicle build record to MES and build traceability, connected vehicle warranty data to Toyota Connected's existing Azure estate, quality events to plant Quality systems, assembly telemetry to line and asset systems. *Stand up Bronze on OneLake. Begin the Silver canonical mappings.* Silver does not have to be complete in this window; the first two domains is enough to begin the agent build in parallel.

*Days 30 through 60 — Agent build and HITL design.* The longest phase. *Build the 24-step agent chain on Agent Framework, hosted on Foundry, against Toyota's Silver canonical.* Six phases — detect, trace, compose, validate, recommend, attest. *Implement the LEDGER hash chain and the Microsoft Purview audit echo.* Every step writes an audit row.

*Design the HITL gate.* Which quality engineer or quality director signs the chargeback package. What the Teams Adaptive Card looks like for her. The escalation path if she rejects. *Half technical, half cultural. The plant team must believe the agent is augmentation, not replacement — and that belief is built by the design, not declared after the fact.*

**MIA:** And the NVIDIA-side work in this window.

**KEVEN:** *RAPIDS on the Fabric GPU compute goes in early* — the agent's latency budget depends on it. *NeMo for the chargeback-prose drafting in phase five* comes in later in the window if time allows, or in a follow-on window. *Triton hosts whatever models the agent calls; the substrate is in place from the start.* Omniverse and Metropolis are not in scope for the 90-day pilot — those are follow-on waves.

*Days 60 through 75 — Validation cycle.* The pilot's truth test. *Test the agent against a known historical warranty cluster* — chosen from the past eighteen months, where the manual investigation already concluded. *That historical conclusion is the baseline.* Run the agent against the same input data. See whether it reaches the same conclusion. *Where does it agree, where does it disagree, where does it surface a dimension the manual investigation missed.* If the agent reaches the same conclusion in twelve minutes that the manual process reached in eight weeks — that is the proof point. *Plus the audit-row replay test* — an External Audit Reviewer samples the agent's rows and replays them. *If the chain replays cleanly, the chain is operationally trustworthy.* That trust is what makes Quality leadership and Legal willing to put their names next to the agent's output.

*Days 75 through 90 — Pilot decision.* Quality leadership reviews. Validation output, audit-row replay, cost recovery from the historical cluster — all on the table. *Go or no-go for Wave 1 production deployment.* Go means Wave 1 begins — the agent moves from pilot to production, the cohort expands, the Account Team moves into Wave 1 SOW execution. *No-go means what was learned, what would have to be different — not a failure, a data point.* The pilot architecture is reusable; the next pilot starts from the same canonical foundation.

**MIA:** And the relationship to the four-level ladder.

**KEVEN:** *The 90 days is the L1-to-L2 transition.* The Crotts conversation is L1. The 90-day pilot is L2. Wave 1 deployment at the pilot plant is L2-to-L3. Cross-plant scaling across the fourteen North American plants is L3-to-L4. *L4 — Toyota leads connected-vehicle quality globally — is the multi-year horizon, named in passing, never pitched as the entry move.*

### Sponsor possibilities — three options for the Crotts conversation

**KEVEN:** Now the question Episode 1 deferred. *Who should sponsor this.*

**MIA:** Three candidate sponsors, in plain language.

*Candidate one — Quality leadership at the plants.* The plant-Quality VPs and the broader Toyota Quality leadership chain. *Most operationally invested.* They live the eleven-o'clock-on-a-Tuesday-night moment from Episode 1. They feel the warranty cost in their plant P&L. The chargeback recovery question lands directly in their world. *They have the clearest budget for a quality-improvement pilot. They are the natural buyer for Zero Day Warranty if the pitch is framed as quality-investigation acceleration.*

*Candidate two — Toyota Connected North America.* Headquartered in Plano. Owns the connected-vehicle data foundation, which already runs on Azure. *Structurally invested in connected-vehicle data composition.* They sit on one of the four data domains — the largest and most actively-instrumented one. If the pitch is framed as a connected-vehicle analytics extension, Toyota Connected is the natural sponsor. *They also have the shortest data path. Their environment is the most ready to integrate.*

*Candidate three — Manufacturing IT.* The cross-plant IT organization that owns the build-record systems and the line-side data plane. *Cross-plant integration is their world.* They feel the pain of multi-system pulls across fourteen plants more than anyone. If the pitch is framed as a foundation play — the canonical Silver that enables not just Zero Day Warranty but a portfolio of downstream agents — Manufacturing IT is the natural sponsor. *They can fund the substrate that everyone else builds on.*

**KEVEN:** Three candidates. Three different framings of the same underlying scenario.

**MIA:** *Three candidates. And a real choice to be made.* I have a strong opinion on which is the right entry point. Keven and I disagree on it, and we are going to disagree on tape in a minute.

### Microsoft Account Team coordination — BVA, ECIF, Azure Credits

**KEVEN:** Before the disagreement — the funding model.

**MIA:** Three Microsoft mechanisms. *BVA, ECIF, Azure Credits.*

*BVA — Business Value Assessment.* Seventy-five thousand to two hundred thousand dollars. *Microsoft funds the discovery work that validates the business case.* The Independence-clean pattern matters here. *Microsoft funds Toyota's discovery; Deloitte does the discovery work on a Deloitte contract with Microsoft, not with Toyota. Toyota receives the discovery without paying for it.*

*ECIF — Enterprise Customer Investment Fund.* Two hundred thousand to five hundred thousand. *Microsoft funds POC implementation.* Same Independence-clean pattern — Deloitte's POC work is contracted between Deloitte and Microsoft, with Toyota as the beneficiary.

*Azure Credits.* One hundred thousand to five hundred thousand. *Microsoft funds Toyota's Azure consumption during the pilot.* Bronze, Silver, Gold workloads on OneLake; the Agent Framework runtime on Foundry; the Purview audit echo; NIM and Triton on AKS GPU node pools. *The credits cover that consumption.*

**KEVEN:** And the total picture.

**MIA:** *Microsoft's contribution potential — four hundred thousand to one point two million dollars.* That is what Microsoft can put behind the pilot across BVA plus ECIF plus Azure Credits. *Toyota's out-of-pocket cost for the pilot can be effectively zero, or very close, when the funding mechanisms are coordinated.* That is what makes the pilot accessible — no internal Toyota budget hurdle has to clear before the work can start.

**KEVEN:** And NVIDIA-side funding.

**MIA:** *Different mechanisms.* NVIDIA Inception is a startup program — not applicable to Toyota. NVIDIA has customer-engineering credits and Solution Architect support for enterprise deployments, available case-by-case. *NVIDIA AI Enterprise licensing follows a more traditional commercial model.* The Account Team should not assume funding parity with Microsoft. *Coordinate with NVIDIA for technical support and engineering enablement, not for funding offsets.*

**KEVEN:** And the Independence framing inside the funding model.

**MIA:** *Said cleanly.* When Microsoft funds discovery or POC work, Microsoft is paying Deloitte for a service that benefits Toyota. *Deloitte is not paid by Microsoft to influence Toyota's platform decision.* The platform decision is Deloitte's recommendation on the merits and Toyota's licensing choice on Toyota's terms. *The funding mechanism is for execution work, not for influence.*

### A reading I want to do

**KEVEN:** I want to read briefly from coverage of production digital-twin deployments in heavy industry. Paraphrased.

**MIA:** Read it.

**KEVEN:** [reading, paraphrased from NVIDIA Developer Blog coverage of production digital-twin deployments, cross-referenced with Reuters Automotive coverage of Industry 4.0 advancement and SAE International's production-digital-twin literature]

*"The production digital twin is the next operational unlock for Industry 4.0. The automakers that move first will not be the ones that adopt the simulation platform fastest — they will be the ones that compose the simulation with their canonical operational data and their existing field-failure telemetry. The unlock is not the twin itself. The unlock is the composition of the twin with the audit-ready data foundation that makes the twin's predictions trustworthy enough to act on. Toyota is positioned to lead this composition because of two foundations that already exist — the Woven City Omniverse capability at the city scale, and the Toyota Drive engineering relationship at the autonomous-vehicle scale. The plant-scale composition is the bridge between those two foundations and the field warranty data they have not yet been composed against."*

[pause]

**MIA:** *The unlock is the composition.* Toyota leads when it goes from "running Omniverse" to "running Omniverse at the production line, composed with the four-domain Microsoft Fabric foundation, with the audit chain wrapping both." *That is what the Zero Day Warranty pilot is. The bridge.* And the bridge has to be built deliberately — the city-scale capability does not auto-extend to plant scale, and the plant-scale capability does not auto-compose with the operational data. *That work is the engagement. That is what the 90 days produces — the first working composition.*

### One disagreement

**MIA:** Pushback. *I want Toyota Connected as the entry sponsor.*

**KEVEN:** Make the case.

**MIA:** Toyota Connected North America is the easiest start. *They already run on Azure. They already have the connected-vehicle data foundation. They are headquartered in Plano — fifteen minutes from Allen, where Keven lives.* Data path shortest. Procurement simplest. Microsoft Account Team coordination most natural — Toyota Connected is already a Microsoft customer for the connected-vehicle workload.

If I am picking the easiest L1-to-L2 transition path, *Toyota Connected is it.* The pilot moves fast because the data foundation is partially in place. *The simpler the start, the faster the value. Pick the sponsor with the shortest path to first proof.*

**KEVEN:** Counter.

**MIA:** Counter.

**KEVEN:** *Quality leadership at the plants has the urgency and the budget. Toyota Connected has the data, but Quality has the pain.*

The data foundation Toyota Connected runs is the substrate for what Quality cares about — *warranty cost reduction, chargeback recovery, faster supplier conversations.* But Toyota Connected itself does not feel the warranty-cost-as-percentage-of-revenue conversation the way the plant Quality VPs feel it. *Toyota Connected's KPI is data-platform reliability. The warranty-cost KPI lives with Quality.*

If I lead with the buyer who feels the pain, the pilot lands where the four-point-two-million-in-cluster-value number actually moves a P&L line. *The Quality VP signs because her warranty cost line goes down. Toyota Connected signs because the project is interesting. Different motivations. Lead with the buyer whose motivation is direct.*

And on data access — Quality leadership can request data from Toyota Connected as an internal Toyota matter. *Faster than an external engagement would be. We do not have to start with the data owner if the data is requestable.*

**MIA:** And the resolution.

**KEVEN:** *Two-track, not one.* Lead with Quality leadership as the named primary sponsor. *They sign the SOW. They own the outcome. They sit at the executive-review table at day ninety.* Position Toyota Connected as the data-foundation enabler — second-most-important name on the project, but not the primary sponsor. *And position Manufacturing IT as the cross-plant scaling enabler — not the entry sponsor, but the L3 sponsor; the move from one plant to fourteen flows through their organization.*

**MIA:** Reluctantly accepted. *Quality leads, Toyota Connected enables, Manufacturing IT scales.* All three names on the page from the start. *Don't pick one and exclude the others.*

**KEVEN:** *Three names. One primary. All three essential.* That is the answer to the question Episode 1 opened.

**MIA:** And in the Crotts conversation, *the question stays open* — Chris will have a better internal read than we do. *Name the three candidates, share the framing, let Chris tell us which has the best internal momentum right now. The framing arms the conversation; it does not pre-decide it.*

### What to carry forward — series finale

**KEVEN:** Five things — series finale.

**MIA:** Go.

**KEVEN:** *One — Zero Day Warranty and Day-0 Prevention close the loop in opposite directions.* The agent we walked across Episodes 1 through 3 traces failures back to the factory minute in minutes, not weeks. The inline vision-AI we walked in Episode 4 catches defects inside the factory minute, before any vehicle ever ships. *Together, they are the full posture.* Same four data domains. Same audit chain. Opposite directions on the clock. *The cheapest defect is the one that never escapes the cell. The next cheapest is the one investigated same-day.*

*Two — the Microsoft platform is the data fabric; the NVIDIA platform is the inference fabric; NVIDIA AI Enterprise is the umbrella.* Microsoft Fabric for the unified data layer on OneLake. Microsoft Agent Framework on Foundry for the agent runtime. Microsoft Purview for the audit chain. NVIDIA Metropolis, DeepStream, and Jetson for vision-AI at the station. NVIDIA RAPIDS for accelerated analytics on Fabric. NVIDIA NIM and Triton for the inference fabric inside Toyota's Azure tenant. NVIDIA NeMo for the domain language layer. NVIDIA Omniverse for plant simulation. *NVIDIA AI Enterprise is the licensed bundle over all of it.* Two platforms, two licenses, one tenant, one identity plane.

*Three — the 24-step agent in six phases, with the LEDGER hash chain and the Microsoft Purview audit echo, is the audit-ready production substrate.* Detect, trace, compose, validate, recommend, attest. Twenty-four audit rows. Every decision replayable. *The audit trail is the product. The Quality VP signs because she trusts the chain that surrounds the agent. The chain is the trust unit.*

*Four — the 90-day pilot path leads to a single Toyota plant; Quality leadership is the primary sponsor, with Toyota Connected and Manufacturing IT as essential partners.* Discovery in the first fifteen days. Data access and canonical mapping through day thirty. Agent build and HITL design through day sixty. Validation cycle through day seventy-five. Pilot decision through day ninety. *Microsoft funding through BVA, ECIF, and Azure Credits — four hundred thousand to one point two million in total — makes the pilot accessible with effectively zero Toyota out-of-pocket cost.*

*Five — Independence from Microsoft and from NVIDIA is non-negotiable.* Deloitte recommends on the technical merits. *Toyota contracts separately with Microsoft for the Microsoft platform.* Toyota contracts separately with NVIDIA for NVIDIA AI Enterprise. Toyota contracts separately with Deloitte for the services. *Three contracts. Three actors. Two platform suppliers. No compensation flows from any platform supplier to Deloitte for the recommendation.* The Account Team should be fluent. A Toyota listener should be able to repeat it back.

**MIA:** Five things. *And the rule that sits above all five — operator dignity. TPS culture is preserved.* The agent augments the senior quality engineer. The vision-AI augments the operator at the station. *The architecture serves the people. Not the other way around.* That rule shows up in the data classification, in the cohort-not-individual policy, in the HITL design, in the cultural agreements that go in front of every plant deployment. *Said in Episode 1. Said again in Episode 4. Said one more time here, because this is the episode where the architecture climbs to its full height and the rule has to climb with it.*

**KEVEN:** Climbs with it. *Said.*

### Call to action

**MIA:** And the close. *What does the Account Team do with all of this.*

**KEVEN:** Five episodes have built the case. About two and a half hours of preparation now sits in the listener's podcast app. *The next move is a thirty-minute discovery conversation with Chris Crotts at TMNA.* The outreach email is drafted. The follow-on artefacts — the Calculations and References document, the Architecture document with the full Microsoft and NVIDIA tabs — are ready if Chris asks. *The conversation does not pitch a 90-day pilot. The conversation tests the hypothesis that warranty cost reduction and build-record-driven root-cause are currently on Toyota's radar. The conversation surfaces who the natural sponsor is — Quality, Toyota Connected, or Manufacturing IT. The conversation is L1.*

**MIA:** And the trajectory beyond L1.

**KEVEN:** *The 90-day pilot at one plant is the L1-to-L2 transition. Wave 1 production deployment is the L2-to-L3 transition. Cross-plant scaling across the fourteen North American plants is the L3-to-L4 transition.* The Account Team's job from this episode forward is *one move at a time, in order.* Confirm interest at L1. Scope the pilot at L2. Deliver Wave 1 at L3. Scale at L4. *Each move is a discrete conversation; the conversations are sequential; the trajectory is the journey.*

**MIA:** And the discipline at each move.

**KEVEN:** *The discipline is the architecture.* Every conversation honors the four data domains, the 24-step chain, the audit posture, the operator-dignity rule, the Independence framing. *None of those is optional. None of those can be compromised for a shorter Wave 1 timeline.* The framework's commercial promise is conditional on the engagement honoring the architectural commitments. *That moment of conscience is what the Account Team protects.*

**MIA:** And the immediate next step.

**KEVEN:** *Send the email to Chris.* Schedule the thirty minutes. *In-person at the TMNA Plano offices if that works; virtual if it does not.* Listen for whether warranty cost reduction is on the FY26 or FY27 agenda. Listen for which of the three sponsor candidates Chris points to first. *Take the conversation from there.*

### Sign-off

**KEVEN:** Thanks for listening to the Zero Day Warranty Podcast. Five episodes. About two and a half hours.

**MIA:** Eighteen years on automotive accounts. *This is the cleanest agentic scenario I've worked on at this scale.* Cleanest because the operational story — the eleven-o'clock-on-a-Tuesday-night moment from Episode 1 — is real, lived, and shared across every plant Quality organization I've sat with. Cleanest because the four data domains are not a constructed schema; they are how Toyota already thinks. *And cleanest because the audit posture is what makes me say so.* I have watched agentic-AI demos that promised the moon and could not survive a single supplier contest. The audit chain that wraps this agent is what would survive. *The chain is the trust unit. That is why this scenario is the one I would put my name next to.*

**KEVEN:** I'm Keven Markham. Vice President, Deloitte's Microsoft Technology and Services Practice. *See you in the field.*

[outro music · long]

---

## Further reading

### NVIDIA developer / docs

- **NVIDIA Omniverse** — simulation and digital-twin platform · [developer.nvidia.com/omniverse](https://developer.nvidia.com/omniverse)
- **NVIDIA NeMo** — framework for domain language models and retrieval · [developer.nvidia.com/nemo](https://developer.nvidia.com/nemo)
- **NVIDIA Triton Inference Server** — open-source inference-serving platform · [developer.nvidia.com/triton-inference-server](https://developer.nvidia.com/triton-inference-server)
- **NVIDIA AI Enterprise** — licensed, supported production bundle · [www.nvidia.com/en-us/data-center/products/ai-enterprise](https://www.nvidia.com/en-us/data-center/products/ai-enterprise/)
- **NVIDIA Developer Blog** — production digital-twin and industrial-AI deployment coverage · [developer.nvidia.com/blog](https://developer.nvidia.com/blog)

### Toyota official / NVIDIA references (public)

- **Woven by Toyota** — Toyota's mobility-and-software subsidiary; Woven City Omniverse digital twin · [woven.toyota](https://woven.toyota/)
- **Toyota Newsroom** — Woven City coverage and updates
- **Reuters Automotive** — Toyota Drive on NVIDIA announcements (2025)
- **NVIDIA press releases** — Toyota Drive partnership references
- **Automotive News** — Toyota Manufacturing and connected-vehicle coverage

### Microsoft Learn — funding and platform

- **Microsoft Azure for Manufacturing** · [learn.microsoft.com/azure/industry/manufacturing](https://learn.microsoft.com/)
- **Microsoft Industry Cloud for Manufacturing** — Common Data Model for Manufacturing alignment
- **Microsoft Fabric** — unified data layer, OneLake, medallion architecture · [learn.microsoft.com/fabric](https://learn.microsoft.com/fabric/)
- **Microsoft Agent Framework on Azure AI Foundry** — agent runtime
- **Microsoft Purview** — governance and DSPM for AI
- **Microsoft Customer Investment Funds** (BVA / ECIF / Azure Credits — internal coordination only, not on-mic)

### Industry context for the 90-day path

- **Automotive News** — Toyota Manufacturing coverage · [autonews.com](https://www.autonews.com/)
- **Reuters Automotive** — Toyota North America operations and Industry 4.0 adoption
- **SAE International** — production digital twin standards and vision-AI for assembly
- **MIT Industrial Performance Center** — production digital twin literature
- **WardsAuto** — plant technology and connected-production coverage

### From the Trilogy and prior account podcasts

- **Sellers Podcast Ep 2 — *The Commercial Arc*** — two-contract model (generalized to three-contract here)
- **Sellers Podcast Ep 7 — *The Pursuit Motion*** — pursuit discipline
- **Sellers Podcast Ep 8 — *The Sellers Dream*** — four-level ladder
- **Sellers Podcast Ep 9 — *Functional-Area Discovery*** — 30-Min Framework (relevant for the Crotts conversation)
- **Services Podcast Ep 4** — MCP boundary and agent runtime
- **Services Podcast Ep 6** — Purview and the LEDGER hash chain
- **Services Podcast Ep 7** — Real-Time Intelligence and streaming-Bronze pattern
- **Disney Account Podcast (6 episodes)** — account-team-playbook structure this episode borrows from
- **DTNA Account Podcast (5 episodes)** — parallel automotive account-specific structure

### Zero Day Warranty Podcast — earlier episodes

- **Episode 01 — *The Zero Day Warranty Idea*** — the eleven-o'clock-on-a-Tuesday-night moment and the four-domain hypothesis
- **Episode 02 — *Four Data Domains*** — vehicle build record, connected vehicle warranty data, quality events, assembly telemetry
- **Episode 03 — *The 24-Step Agent and the Microsoft Platform*** — Fabric, Agent Framework on Foundry, Purview, LEDGER hash chain
- **Episode 04 — *NVIDIA at the Station — Day-0 Prevention*** — Metropolis, DeepStream, Jetson, RAPIDS, NIM, Triton, the two-fabric architecture

### From the APEX framework (internal coordination only — not on-mic)

- AXLE Practice — the Zero Day Warranty scenario and ORCH-01 24-step orchestrator
- Companion HTML pack — `ZeroDayWarranty_Calculations_and_References.html` and `ZeroDayWarranty_Architecture_Diagrams.html` (both in `02_projects/FY27_Pipeline/Fabric_Connected_Vehicle_Analytics/`)
- Outreach draft — `Outreach_Crotts_ZeroDayWarranty.md` (the email this series is preparation for)
- Toyota Account Snapshot — `Toyota_Account_Snapshot.md` (sponsor candidates, Microsoft Account Team context)

---

**End of Episode 05 · Omniverse, Toyota's NVIDIA Estate, and the 90-Day Path**
**End of the Zero Day Warranty Podcast — series complete**
*≈ 5,800 words · target 30 minutes at conversational pace · series total ≈ 28,000 words across 5 episodes*
