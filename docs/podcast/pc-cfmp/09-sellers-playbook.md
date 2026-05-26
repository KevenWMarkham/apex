# Episode 09 · The Seller's Playbook — CFMP on APEX-M

**Episode 09 · The seller's playbook — CFMP on APEX-M** — Friday afternoon. A real seller's inbox. The CIO of a prospect has asked the Account Team a single line: *Can CFMP run on AWS?* The Account Team wants the answer to be *yes*. The Independence-minded posture wants the answer to be *it depends — here is the honest version*. This is the moment the whole series has been pointing to. We close the series on the seller's working substrate — the architectural pitch, the six discovery openers, the five honest claims, the four overclaims to avoid, the six pushbacks handled in the room, when to recommend NOT Microsoft, the sprint roadmap, the Independence-minded close. Eight episodes of architecture compress into one Friday-afternoon working document. The pack is portable. The productization on Microsoft is what's denser. The seller earns the recommendation on merits. The series closes here.

**Builds on:** the show bible (00-show-bible-and-format) · Episodes 01–08 · CFMP Mobile Design Document §9 (Roadmap), §10 (Open questions) · CFMP Sonos Design Document §9 (Roadmap), §10 (Open questions) · CFMP Mobile Roadmap · CFMP Sonos Roadmap · Cross-Cloud Agentic Episode 08 *The Seller's Playbook*
**Run time:** ≈ 42 minutes target
**Last updated:** 2026-05-25

---

## Cold Open

[Sound: a seller's home office on a Friday afternoon in late May. The light is long and amber through a north-facing window. A laptop open on the desk, a coffee cup cold in the saucer, an inbox notification chime in the background — soft, two-tone, the muted variant the seller has learned to leave on for the one inbox folder that actually matters. Outside, a lawnmower three houses over. The desk surface has three pieces of paper on it. The first is the Acceleration Framework's five principles, printed and annotated by hand. The second is a list of six discovery openers, each one written in a single sentence the seller can ask out loud. The third is the architecture stack — Mobile, Portal, Sonos — printed on Deloitte letterhead with the live `/architecture` URL handwritten across the top in blue ballpoint pen, because the seller has learned that URL is the screen-share that does more work than any deck slide ever has.]

Friday afternoon. The seller — a Microsoft platform specialist on a Consumer-industry account — refreshes her inbox at three-forty-seven in the afternoon, because the kid's soccer game starts at four-thirty and she wants the inbox at zero before the second-half whistle. Six new messages since lunch. Five are noise. The sixth is from the Account Team Partner for the prospect she has been working for three weeks, a global retailer the Account Team has been courting since the prior fiscal year. Subject line — *forward from prospect CIO — please advise*. The body forwards a single-line question from the CIO. *Can CFMP run on AWS?* No preamble. No softening. The CIO is reading the design memo the Account Team sent her on Tuesday and she has asked the question every serious CIO asks by the second read.

The Account Team Partner has appended his own line. *Want to say yes to keep the door open. What's the honest answer?*

The seller stares at the screen. She knows the Acceleration Framework underneath CFMP is vendor-neutral by design. She knows the Microsoft productization is what's denser today. She knows the partner-channel motion would say *yes of course it runs on AWS — call our AWS counterpart — happy to help*. She knows the Independence-minded motion would say *yes, the framework is portable; here is the honest comparison; here is why we are recommending Microsoft on merits*. She knows which of the two answers wins the next three deals and loses the long-term relationship, and she knows which of the two wins the relationship and might lose this specific deal. She has fourteen minutes before she needs to walk out of the door for the soccer game. She picks up her phone and dials her colleague Reid.

[Sound: a coffee shop on a Friday afternoon, ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start there. Friday afternoon. The seller's inbox. The CIO's question. *Can CFMP run on AWS?* That is the inbox question the entire series has been pointing at. Eight episodes of architecture, the audit chain, the agent fleet, the mobile and portal and Sonos surfaces, the fulfillment plug-in tier, identity and consent and HIPAA — and the CIO asks the one question that decides whether the seller walks into Monday's meeting as an advisor or as a vendor representative.

**REID:** And the answer is not *yes*. And it is not *no*. It is the right version of *it depends*.

**KEVEN:** The right version of *it depends*. Which is — *yes, the framework is portable. The Acceleration Framework is vendor-neutral by design. CFMP could be built on AWS or on GCP. What you are paying for on Microsoft is productized density — Fabric plus Foundry plus Purview plus Entra in one console with one bill and one identity story. The architecture is portable. The productization on Microsoft is what's denser. We recommend Microsoft on merits — not because it is the only place CFMP can run, but because it is the place CFMP ships with the most done.*

**REID:** Said exactly that way. And the seller who can say that — out loud, on a Friday afternoon phone call, without flinching — earns the next conversation. The seller who says *yes of course it runs on AWS, our partners over there are great, let me make a connection* concedes the architecture conversation in the first sentence.

**KEVEN:** Welcome to *The CFMP Podcast*. Episode Nine. *The seller's playbook — CFMP on APEX-M.* The series finale. We are going to walk what is on those three pages on the seller's desk. The architectural pitch. The six discovery openers. The five honest claims. The four overclaims to avoid. The six pushback-handling talking points. When to recommend NOT Microsoft. The sprint roadmap that turns the architecture into a calendar. The Independence-minded close. And then we close the series on a sign-off the show bible reserves for this one episode.

**REID:** Eight sub-sections. A reading. A disagreement. Three carry-forwards. The sign-off. Let's go.

---

## The conversation

### The architectural pitch

**KEVEN:** Lead with architecture. That is the headline. The pitch is not *Microsoft is better*. Every CIO in 2026 has heard that pitch from every Microsoft seller they have met. The pitch that earns the room is different. *There is a right way to build agentic AI for your customer. It is the Acceleration Framework. Five vendor-neutral principles. APEX-M is Microsoft's productized realization. CFMP is the application pack on top. The architecture decides; the cloud follows.*

**REID:** Walk the layer cake. The seller needs the picture.

**KEVEN:** Four layers. The seller draws this on a whiteboard with four boxes. *Top — the customer surface.* The Mobile PWA Sarah uses to scan a barcode and build a meal-plan lot. The Portal Priya uses to handle exceptions and answer the chat panel. The Sonos speaker Robert hears in the kitchen at six-thirty on a Tuesday evening when the cue starts to say *Lisinopril* and rewrites in flight to *an item*. Three surfaces. One pack. Mobile, Portal, Sonos.

*Second from top — the application pack.* CFMP. The agent fleet from Episode Two — a parent orchestrator and a fleet of specialist children — Trips, Replenish, Coupons, Pharmacy, Concierge. The lot model from Episode Three — twelve kinds of lots across four stages. The home channel from Episode Four. The retailer multi-tenant scaffold from Episode Five. The cue and cue bus from Episode Six. The four-identity chain, the consent gradient, the HIPAA presence gating, and the senior accessibility defaults from Episode Eight. *That is the pack.* The pack is what Deloitte built; it is what is licensable, deployable, productizable.

*Third from top — APEX-M.* Microsoft's productized realization of the Acceleration Framework. *Fabric for the Gold Tier.* OneLake. Bronze on landing, Silver canonical, Gold per-scenario. *Foundry for the agent runtime.* The orchestrator and the specialist children running as agent threads, the model catalog backing them, the evaluation harness on top. *Purview for the trust substrate.* The catalog, the lineage, the sensitivity classification, the DSPM-for-AI surface. *Entra for the identity continuity.* Customer, operator, source-system, auditor — four identities, one platform. *Cost Management for the FinOps story.* The four layers feed one bill. The seller names that.

*Bottom — the Acceleration Framework.* Five vendor-neutral principles. *Gold-Tier-First.* Agents reason against governed gold, not raw SORs and not federated chaos. *Governance plus audit plus ledger.* The hash-chained, identity-stamped, replayable audit row that Episode Two and Episode Five built around. *Identity continuity.* Customer to operator to source-system to auditor, all on the same federation rails. *No replication.* Sources stay where they are; mirror and federate rather than copy. *Model portability.* The agent is decoupled from the model behind it. Five principles. Vendor-neutral. The substrate beneath everything above.

**REID:** And the seller's draw-it-on-the-whiteboard line.

**KEVEN:** *The Acceleration Framework decides what to build. APEX-M decides what's productized today. CFMP decides what surfaces ship in the merchandise pack. The cloud recommendation follows from the architecture, not the other way around.* Four sentences. The seller carries those four sentences as muscle memory.

**REID:** And why this pitch wins where the *Microsoft is better* pitch loses.

**KEVEN:** Three reasons. *One — it leads with architecture, not with vendor.* The CIO is paid to make architectural decisions, not to retire a Microsoft seller's quota. *Two — it is cloud-neutral in substance.* The principles are vendor-neutral by design. The seller can say that out loud and survive the CIO's outside-advisor walking through the door fifteen minutes later. *Three — it earns the right to make the Microsoft recommendation later.* Once the architectural commitments are agreed, the cloud choice becomes a productization-density comparison. That is a conversation Microsoft can win honestly on most principles. The pitch lands the architecture first. The platform recommendation follows on merits.

### The six discovery openers — verbatim, by principle

**REID:** The six openers. Verbatim. Phrased the way the seller would use them in the room. One per principle plus one for the home channel — because CFMP has a surface the framework alone does not have a principle for.

**KEVEN:** *Opener One — Gold-Tier-First.* The seller asks — *"When a new AI workflow starts today, does it get a fresh copy of the data, or does it compose against sources in place?"* What it surfaces — the data-foundation conversation. *They get a fresh copy* — Wave 1 foundation problem; CFMP wants the Gold Tier on Fabric, mirroring not replicating, virtualizing where it can. *They compose against sources in place* — sophisticated team that already gets Principle One. The architecture move that follows — Fabric Mirroring on Postgres lots, OneLake shortcuts on the retailer catalog, Eventstreams for the receipts feed. One question; three architectural conversations.

**REID:** Opener Two.

**KEVEN:** *Opener Two — Governance, audit, and the ledger pattern.* The seller asks — *"If an external auditor asked you to reproduce an agent decision from six weeks ago, could you?"* What it surfaces — the trust substrate conversation. *No, we'd have a log file but not a replay* — the gap CFMP fills with the LedgerRow and the trace_id propagation Episode Two walked. *Yes, we hash-chain every step* — sophisticated architect who will recognize the ledger pattern. The architecture move that follows — the hash-chained, identity-stamped, replayable audit chain, eight hops per cue, identity-bound, productized as reference architecture on Foundry. The substrate is the conversation.

**REID:** Opener Three.

**KEVEN:** *Opener Three — Identity continuity.* The seller asks — *"Is your identity reality one primary cloud with a federated SaaS workforce, or genuinely cross-cloud workloads?"* What it surfaces — the identity-continuity conversation. *One primary cloud* — Entra wins on enterprise SaaS federation; the four-identity chain from Episode Eight slots in cleanly. *Genuinely cross-cloud* — Workload Identity Federation on GCP is the strongest cross-cloud agent identity primitive; the seller concedes honestly and pivots to where Entra leads on SaaS. The architecture move that follows — Entra External ID for the customer, Entra workforce for the operator, Entra B2B guest for the auditor, federation for the source-system. One identity platform, four surfaces.

**REID:** Opener Four.

**KEVEN:** *Opener Four — No replication.* The seller asks — *"How many copies of customer data does an AI use case create today?"* What it surfaces — the replication-cost conversation. *Three or four — we copy from each SOR into a lake, then from the lake into a feature store, then sometimes into a vector store* — the CFO conversation about why AI costs run thirty-five percent quarter-over-quarter on storage alone. *Zero — we mirror and federate* — sophisticated architect already aligned to Principle Four. The architecture move that follows — Fabric Mirroring on the SORs, shortcuts on the catalog, federation through to BigQuery or Snowflake if the customer has overwhelming gravity there. The sources stay where they are.

**REID:** Opener Five.

**KEVEN:** *Opener Five — Model portability.* The seller asks — *"If the model behind your agent were deprecated tomorrow, how long would it take to swap it?"* What it surfaces — the model-abstraction conversation. *Weeks — we'd have to rewrite the agent* — the four-discipline conversation about model decoupling, evaluation harness, and the abstraction layer between the agent and the model. *Hours — we have an abstraction layer and we routinely swap* — sophisticated architect; the seller acknowledges Bedrock's multi-vendor lead on the model catalog honestly. The architecture move that follows — the orchestrator running on gpt-5-mini today, the children running on the same family for cost, the abstraction layer that lets the seller swap a child to Claude on Foundry tomorrow if the customer's evaluation harness says so. The model is a configuration, not a commitment.

**REID:** Opener Six. The home channel.

**KEVEN:** *Opener Six — the home channel.* The seller asks — *"What does your customer hear from your brand when they're not looking at a screen?"* What it surfaces — the ambient-channel conversation. Nine times out of ten the answer is — *nothing.* Email goes to a folder the customer never opens; SMS is reserved for delivery confirmations; push is filtered by the operating system. *They don't hear anything* — the surface CFMP opens with Sonos; the cue, the cadence law, the per-zone defaults, the AirPlay-bridge for the zero-config first-run. *We have an ambient channel* — rare; the seller asks what they have and pivots. The architecture move that follows — the Sonos cue from Episode Six, the cadence law that protects the customer from intrusion, the cue bus that mirrors every spoken cue into the Portal chat panel for visible audit. The brand becomes a voice the customer trusts.

**Opener Seven — Privacy is architectural, not a setting.**

**KEVEN:** *"Does your assistant listen to everything in your home — or only what you ask?"* That is the opener that lands the C-suite in 2026. The Alexa pattern won the consumer market; the next architecture wins the boardroom. The opener surfaces the customer's quietest concern — the household whose conversations live in a public-cloud datacenter is the household whose loyalty data, audit chain, and platform relationship are owned by the vendor, not the customer.

**REID:** And the architecture move that follows is the *un-Alexa* substrate — voice on device, Vision Kit local inference, MCP boundary as privacy boundary, customer-owned identity in Entra External ID, and the v2 trajectory toward telco-edge orchestrator with on-device LedgerRow witnesses.

**KEVEN:** The seller pitches what is true today — voice stays on the phone, vision stays on the device, identity stays the customer's — and what is committed tomorrow — telco-edge orchestrator, on-device witness. The depth on this lives in Episode Twelve.

**REID:** Open the architecture page on the call. Point at the boundaries. Ask the architect to find the leak. *There isn't one.* That is the moat.

**REID:** Six openers. The seller carries them in their head. Twenty minutes into any agentic-AI discovery conversation, the seller has surfaced the architectural pain across five principles plus the home channel — without a single vendor-loyalty pitch.

**KEVEN:** No vendor framing. No partner-channel motion. No *Microsoft is better*. Six questions; six conversations; the framework does the rest.

### Six honest claims sellers can defend

**REID:** Five claims. Each one defendable in front of a sophisticated client architect, and in front of the Deloitte AI team architect who has shipped on Bedrock and Vertex and is listening from the back of the room.

**KEVEN:** *Claim One — productized-capability density is real on Microsoft today.* Fabric plus Foundry plus Purview plus Entra in one console, one bill, one identity story, one support contract. AWS approximates the surface area as Lake Formation plus Bedrock plus Macie plus IAM Identity Center plus CloudTrail — five products, three teams, three contracts. GCP approximates as BigQuery plus Vertex AI plus Dataplex plus Cloud Identity — closer to productized than AWS, the closest competitor on naturalness. *Microsoft is broadest productized today.* True; defendable; the seller can walk the comparison out loud.

**REID:** Claim Two.

**KEVEN:** *Claim Two — the Sonos channel is Azure-native, no LAN bridge, no on-prem dependency.* The cue is composed by `ca-visionkit-orchestrator` in Container Apps in East US 2. The WAV is synthesized by Azure Speech — `en-US-AvaMultilingualNeural` for the default, `en-US-AndrewNeural` for alerts. The WAV is staged in Blob storage on `stapexdemo50097` with a fifteen-minute SAS URL. The Sonos Cloud Control API at `control.api.sonos.com` accepts a `play_audioClip` call against the household, references the SAS URL, and the speaker plays. *Cloud to cloud to speaker, no LAN required.* The AirPlay-bridge is the zero-config escape hatch — when OAuth is not yet provisioned, when the customer's Wi-Fi blocks outbound to `control.api.sonos.com`, when the demo needs to ship without paperwork — the phone PWA plays the WAV and the iOS Control Center routes to the Roam over AirPlay 2. *Cloud-primary, bridge-fallback.* True; in code; defendable.

**REID:** Claim Three.

**KEVEN:** *Claim Three — the audit chain is replayable, hash-chained, identity-stamped, and the trace_id propagates across surfaces.* Episode Two walked it; Episode Five walked it on the live `/architecture` page; Episode Eight walked the cross-surface case where a single ten-second moment produces a Mobile compose, a Sonos cue, a redacted Sonos cue, and a caregiver mobile ping — all four bound by a shared trace identifier, all four written into the ledger, all four replayable in three minutes when a regulator asks. *Eight hops per cue, fourteen fields per row, HMAC-SHA256 chain, append-only retention.* True; verifiable; the seller can point the architect at the URL.

**REID:** Claim Four.

**KEVEN:** *Claim Four — the consent gradient and the HIPAA presence-gating are real, defensible, in code.* Four classes of consent — data, voice, presence, caregiver-share — each separately recorded, separately scoped, separately revocable. The presence gate from Episode Eight that rewrote the Lisinopril cue mid-syllable to *an item* when the kitchen occupancy changed from one to two — not a marketing diagram; the rewrite happens in the Pharmacy specialist's pipeline, fires off the presence service, gets recorded in the ledger row with *suppression_reason: presence_count_change, hipaa_gate*. The senior accessibility defaults — Yamamoto's per-zone volume and cadence overrides — in code, configurable, audited. *The consent surface is real software, not slides.*

**REID:** Claim Five.

**KEVEN:** *Claim Five — the architecture is portable; the productization is what's denser on Microsoft.* The seller has to say this fifth one out loud. The Acceleration Framework's five principles are vendor-neutral by design. CFMP can be built on AWS — Bedrock for the agent runtime, Lake Formation plus Glue plus Athena for the Gold Tier, Macie plus CloudTrail plus QLDB for the trust substrate, IAM Identity Center for the federation. CFMP can be built on GCP — Vertex AI for the agent runtime, BigQuery plus BigLake plus Dataplex for the Gold Tier and governance, Cloud Identity plus Workload Identity Federation for the federation. *The framework is portable. The productization density is the Microsoft pivot.* The fifth claim is the one that earns the architect's respect, because the fifth claim is the one a partner-channel seller cannot say.

**Claim Six — Privacy is architectural, not a setting.**

**KEVEN:** Voice stays on the device the customer chose — the phone's microphone runs local STT, the Sonos speaker plays cues the cloud sends but never captures audio cloud-side. Vision Kit runs local inference — frames don't routinely leave the home; only event packets do. The MCP boundary is the privacy boundary — every agent tool call hits composed Gold, never raw sources. Customer identity lives in Entra External ID — the customer's tenant, the customer's audit chain, the customer's data export at any time. *This is the inverse of the Alexa pattern, and it is in code today.* The v2 commitment — telco-edge orchestrator and on-device LedgerRow witness — extends the substrate; it does not invent it. The seller can point an architect at the `/architecture` page and ask them to find the leak.

**REID:** And this is the C-suite headline for 2026. The household burned once by surveillance is the household that listens carefully to the *architecture* answer. Privacy as a *setting* — toggles you can turn on, trust us to honor them — has lost credibility; the customer has been burned too many times. Privacy as *architectural* — the data never leaves the place it's supposed to leave, you can verify by reading the page — is the credibility play. The architecture page IS the moat.

**REID:** Five claims. All defensible. All honest. All survive scrutiny when the prospect's outside advisor walks through the door.

### Four overclaims to avoid

**REID:** The four overclaims. Each one a sentence a seller might say naively. Each one collapses the moment a real architect pushes.

**KEVEN:** *Overclaim One — "CFMP only runs on Microsoft."* False. The framework is portable. The five principles are vendor-neutral. The pack ships denser on Microsoft today; it does not ship *only* on Microsoft. The seller who says this loses the architect in the first sentence. *Do not pitch this.*

*Overclaim Two — "We are AI-first."* Empty. Every vendor in 2026 is AI-first. Every PowerPoint deck in the consumer-industry vertical leads with the phrase. The CIO has heard it forty times this quarter. It carries no information; it earns no credibility. The phrase has been worn smooth by overuse. *Do not pitch this.*

*Overclaim Three — "The customer never has to touch glass."* Aspirational. The CFMP demo touches glass — Sarah scans a barcode on her phone, Sarah taps to confirm the meal plan, Sarah opens the Lots tab to inspect the StayLot. The Sonos cue is a peer channel, not a replacement for the screen. Some flows always will be screen-mediated — checkout confirmation, payment authorization, the consent surface itself. The customer-never-touches-glass pitch collapses on the first demo question. *Do not pitch this.*

*Overclaim Four — "It's HIPAA-compliant."* False on the framing. No software is *HIPAA-compliant*. Processes and Business Associate Agreements and operational controls are HIPAA-compliant. CFMP is *HIPAA-aware in design* — the presence gating, the drug-name redaction, the caregiver-share consent class, the audit row that records the redacted-as-delivered text. The seller who says *HIPAA-compliant* in front of a healthcare-vertical CIO loses the room and earns a polite redirect from the client's General Counsel. The architecturally honest phrase is *HIPAA-aware in design, with the operational controls the customer's compliance team brings.* *Do not pitch this.*

**REID:** Four overclaims. The seller learns to *not say* each one. The discipline of not saying them is what protects the long-term relationship. The four overclaims are the four shortest paths to losing the room.

**KEVEN:** Said that way. The discipline pays off every time the seller does not say them.

### Six pushback-handling talking points

**REID:** The six pushbacks. Every serious CIO conversation produces at least one. The seller needs the verbatim language ready.

**KEVEN:** *Pushback One — "Can CFMP run on AWS?"* This is the inbox question we opened on. The response, verbatim — *"Yes. The framework underneath CFMP is the Acceleration Framework — five vendor-neutral principles that are portable to AWS. You would build the agent runtime on Bedrock, the Gold Tier on Lake Formation plus Glue plus Athena, the trust substrate on Macie plus CloudTrail plus a QLDB-backed ledger, the identity continuity on IAM Identity Center. The architecture is portable. What we are recommending on Microsoft is productization density — Fabric plus Foundry plus Purview plus Entra in one console, one bill, one identity story. The pack ships denser on Microsoft today. If your data gravity is on AWS, we would design on AWS and tell you so. That is the honest comparison."* The seller concedes the framework is portable and pivots to the productization density. The CIO trusts the answer.

**REID:** Pushback Two.

**KEVEN:** *Pushback Two — "Isn't this just a grocery app?"* The disagreement from Episode One. Every serious architect asks this on the second read of the design memo. The response, verbatim — *"Four things no shipped grocery app does. One — the cross-retailer compose-from-anywhere lot; Sarah builds a meal plan that pulls produce from one source, gochujang from a second, diabetic snacks from a third, in one lot with one checkout intent. Two — the audit chain that lets a caregiver participate in a senior's grocery and pharmacy without seeing protected information; Diana acts on behalf of Robert, the information boundary is enforced at the agent layer, the regulator can replay the chain. Three — the agent that composes a meal plan from pantry plus allergies plus budget plus stock; no retailer has the pantry, no recipe app has the cart, no delivery app has the allergies. Four — the StayLot that follows the household to the cabin; it is a generalized displacement pattern, not a logistics integration. CFMP is a pack — an agentic substrate that the grocery surface happens to use. The substrate is the difference."* Four examples. The seller draws the architecture-versus-feature distinction.

**REID:** Pushback Three.

**KEVEN:** *Pushback Three — "Will the retailer sign? You're asking us to onboard a multi-tenant agent platform on a single retailer's customer base, which is the kind of conversation that runs eighteen months."* The Jennifer Liu push from Episode Five. The response, verbatim — *"Liu's expert read is eighteen months on the multi-tenant retailer signature, gated on SOC 2 Type II. The CFMP roadmap honors that timeline. v1 ships single-retailer with Deloitte-staffed operations; the retailer multi-tenant scaffold is on the v2 deferred backlog. The eighteen-month path is in the design — SOC 2 clock starts at S8, retailer onboarding kicks off in the back half of year two. The pack is engineered to wait for the signature; the architecture does not force the timeline to fight the retailer's compliance cycle."* The seller names the timeline honestly and shows the roadmap accommodates it.

**REID:** Pushback Four.

**KEVEN:** *Pushback Four — "The speakers feel intrusive. We are not going to ship a product that talks to customers in their kitchens."* The response, verbatim — *"That instinct is the right instinct, and it is the instinct the design is built around. The cadence law from Episode Six caps cues at three per hour per zone, with quiet hours per household, with a one-voice rule that prevents the Era 100 and the Roam from cross-talking, with the AirPlay-bridge as the zero-config first-run path so the customer hears the cue on a speaker they have already paired into their own household — not on a device CFMP provisioned. The per-zone defaults are configurable in the Preference Center. The cue acceptance rate target is eighteen percent — meaning ninety percent of cues exist to be useful and ten percent are tolerated as the cost of an ambient channel. If the cue is not earning its place in the household, the cadence law fires and the cue queues to morning briefing. The speaker is a peer channel, not a megaphone."* The seller names the intrusion concern and walks the controls.

**REID:** Pushback Five.

**KEVEN:** *Pushback Five — "We're AWS-primary at the data foundation. The warehouse is on Redshift, the operational lake is on S3, ten years of customer transactions are already there. Microsoft is a workforce productivity decision, not a data foundation decision."* The response, verbatim — *"Acknowledged, and that is exactly the conversation Principle Four is designed to have. CFMP would compose against Redshift and S3 in place — Fabric Mirroring on the operational sources, OneLake shortcuts on the analytical lake, no replication into a new lake. The Gold Tier sits where the gold already lives; the agent fleet reasons against it without copying it. If the data gravity argument tips the design toward building the Gold Tier on AWS — Lake Formation plus Glue plus Athena composing inside AWS — we would tell you so and design that. The architecture is portable. The recommendation follows the gravity."* The seller concedes the gravity and shows the architecture honors it.

**REID:** Pushback Six.

**KEVEN:** *Pushback Six — "Microsoft compensation is influencing your recommendation. You are a Microsoft seller telling me to buy Microsoft. How do I know the architecture pitch is not a marketing wrapper."* The hardest one. The response, verbatim — *"The two-contract operating model. You contract with Microsoft directly on Microsoft paper for the platform. You contract with Deloitte directly on Deloitte paper for the services. Two contracts. No reseller margin. No compensation flows from Microsoft to Deloitte for influencing your cloud choice. You can verify by checking that Deloitte's revenue from this engagement comes from your contract with us, not from Microsoft's contract with you. The recommendation is on technical and economic merits. If your architecture pointed to AWS, our recommendation would be AWS. The Independence is in the operating model; it is verifiable."* The seller says this without flinching. The two-contract framing is verifiable on paper.

**REID:** Six pushbacks. Six verbatim responses. The seller carries them like a doctor carries differential diagnoses — pattern-match the question, deliver the answer, watch the room.

### When to recommend NOT Microsoft

**REID:** The credibility play. The section every Microsoft seller has to be able to walk. *When does the honest recommendation point away from Microsoft.* The Independence-minded seller says this out loud. The partner-channel seller does not. Three scenarios. Walk them.

**KEVEN:** *Scenario One — overwhelming Snowflake or BigQuery investment.* The customer has spent five or seven or ten years building on Snowflake. The Gold Tier already lives there. The warehouse already lives there. The data engineering team is Snowflake-native. The same applies to BigQuery — five years of BigQuery, the data team writes BigQuery SQL in their sleep, the BI layer is on Looker, the cost optimization is already tuned. *Fighting that investment is the wrong battle.* The cost case for migrating the Gold Tier to Fabric dominates the productization-density argument. The honest seller says — *"compose with what you have. Fabric Mirroring on the Snowflake gold; OneLake shortcuts on the BigQuery dataset. The agent fleet reasons against the existing gold. The cost case for migration is not there. Microsoft composes at the seams; we recommend AWS or GCP for the data foundation."* The seller says this out loud and earns the room.

**REID:** Scenario Two.

**KEVEN:** *Scenario Two — genuinely cross-cloud-spread workloads.* The customer's operational data is split — the retail SORs on AWS, the analytical warehouse on GCP, the workforce on Microsoft. *BigQuery Omni is the strongest cross-cloud federation primitive on the market today.* Federated query from BigQuery against S3, against ADLS. The honest seller acknowledges that. *"If your workload is genuinely cross-cloud-spread and you need federated query across S3 and ADLS in one engine, BigQuery Omni is the right answer for that workload. We can compose CFMP against it. Microsoft is not the lead on that primitive."* The seller concedes Principle Four to GCP for that workload and pivots to where Microsoft leads on the other principles.

**REID:** Scenario Three.

**KEVEN:** *Scenario Three — GCP-native identity reality.* The customer's enterprise architecture office has standardized on GCP Workload Identity Federation. The cross-cloud agent identity is on GCP rails. Entra would be the *secondary* IdP, not the primary. *Workload Identity Federation has the cleanest cross-cloud agent-identity primitive — short-lived, scoped, rotated.* The honest seller acknowledges that. *"If your identity reality is GCP Workload Identity Federation primary, the agent identity continuity argument runs the other way. Entra leads on enterprise SaaS federation — M365, SAP, Salesforce, Workday, the application gallery. GCP leads on cross-cloud agent identity. The pick depends on which surface you are optimizing. If the agent identity is your primary problem, we would design on GCP."*

**Scenario Four — the customer wants always-listening public-cloud AI.**

**KEVEN:** This is the scenario where the seller honestly pivots — the customer who *wants* an Echo in every kitchen, a Google Home in every bedroom, the always-listening pattern, the vendor-owned voice waveform, the household-loyalty data in the vendor's account. CFMP is the *un-Alexa*; it is not the right fit for the customer who wants the Alexa pattern with a different label. The seller says so honestly.

**REID:** And the credibility this earns is the credibility the customer carries to the *next* conversation. The customer who hears *"this is not the right architecture for what you described — Amazon's pattern is, and you should choose them"* is the customer who calls again when the next architectural decision lands. *Honesty is the moat. The seller who says 'choose Alexa once' is the seller the architect calls forever.* The privacy architecture is the value, not a feature to toggle off — and the seller says that plainly.

**REID:** *The sellers who name these three scenarios honestly earn more credibility than sellers who never name them.* The CIO who hears the seller acknowledge the three earns the right to be trusted on every recommendation where Microsoft genuinely is the right answer. *The credibility compounds.* The seller who never says it is the seller the architect assumes is selling Microsoft regardless of the architecture. The seller who says *lead with AWS* once — in the right scenario — is the seller the architect calls again for the next engagement.

**KEVEN:** The credibility currency. The seller who says it once buys a year of trust. The seller who never says it loses the next renewal.

### The roadmap — sprints, phasing, v2 deferred

**REID:** The execution layer. The architecture conversation lands on a calendar. Read Mobile §9 and Sonos §9 — and turn it into something a CIO can put a date next to.

**KEVEN:** Two roadmaps, one delivery. *The Mobile roadmap from Design Document §9.1 — eight sprints, each one calendar week, each one demoable at the end.* S0 — foundations and Scan MVP; open the app, scan a barcode, result card, three-tab nav. S1 — lots foundation; PantryLot auto-spawns, Lots Strip, Lots tab, lot detail. S2 — intent lots, cart, push; scan-to-cart-to-checkout cycle. S3 — map subsystem; in-store map overlay, walk directions. S4 — list and deals; Sunday circular, loyalty balance, promo pricing. S5 — BOPIS and subscriptions and the retailer aggregator. S6 — StayLot, third-party delivery aggregator, care and event; the vacation-rental pre-stocking end-to-end. S7 — polish, accessibility, telemetry; Lighthouse ≥ eighty-five; every UC telemetered. *Eight Mobile sprints. Plus parallel Sprint 0 — Compliance, SRE, AI Safety streams running cross-cutting.*

**REID:** The Sonos sprints.

**KEVEN:** *The Sonos roadmap from Design Document §9.1 — six sprints, slotted into Sprints 3-5 of the parent Mobile plan plus a tail.* S0 — OAuth, ledger, schema; connect a household via Sonos cloud; first cue from server to Roam. S1 — trip audio cues, the must-ships; pick item on phone, Roam confirms, announces coupon. S2 — Concierge and Pharmacy audio, with HIPAA gates; refill reminder spoken, caregiver gets the redacted ping. S3 — multi-zone and StayLot; Roam follows the household to the cabin via AirPlay-bridge fallback. S4 — voice-in and wake word; *hey CFMP* on phone PWA, conversational reply on speaker. S5 — polish, telemetry, A/B framework; cue-acceptance rate ≥ eighteen percent, latency SLO p95 ≤ one-point-eight seconds. *Six Sonos sprints. Plus parallel Sprint minus-one — Sonos developer account, voice talent decision.*

**REID:** And the v2 deferred backlog.

**KEVEN:** Both roadmaps name what does *not* ship in v1, on purpose. *Mobile v2 deferred — chargeback evidence packets, chaos engineering, controlled-substance pharmacy, prior-auth coordination, formulary lookup, cultural meal-plan templates in full, carbon-footprint per cart, local-source visualization, the wellness signal for seniors, the multi-tenant retailer provisioning, the retailer white-label, diary studies, the telco set, mTLS private-network deployment, the local-first architecture in full, audit-export download.* Sixteen items, named, deferred, on the backlog. *Sonos v2 deferred — retailer in-store Sonos zones, custom-trained CFMP voice instead of stock Ava, multi-language voice per household, wake word on the Sonos itself, audio-only loyalty-program walkthroughs, spoken receipt summarization, CarPlay integration for car-zone, group-call household conferencing.* Eight items, named, deferred. The roadmap is honest about what's not in v1.

**REID:** And the decision queue.

**KEVEN:** Two-hundred-seventeen decisions in the Mobile queue across the original docs and the all-experts panel. Thirty-eight decisions in the Sonos queue across compliance, AI safety, performance, SRE, voice UX, pharmacy, senior accessibility, B2B, mobile security, and strategic. Per Sonos Design Document §9.4 — *thirty-eight decisions outstanding* on the Sonos side alone. The Mobile decision queue is broken down in Mobile Design Document §9.4 — two-hundred-seventeen total across the eighteen domains. *That is the substrate the project team works through, one decision at a time, with the human-in-charge calling the strategic ones.*

**REID:** And the eight Mobile strategic open questions. The six Sonos strategic open questions. The seller carries these as the things the customer will decide *with* Deloitte, not the things Deloitte decides *for* the customer. DPIA timing — S0 or production-only. Red-team budget — outsourced or internal. HIPAA scope — Covered Entity or Business Associate. SOC 2 timing — start now or at S8. Multi-region cost ceiling. Cloud-LLM data handling — default or private. Local-LLM model pick. Field-research vendor or internal. *The eight Mobile open questions are the eight architectural commitments the seller surfaces inside the first ninety days of the engagement.*

**KEVEN:** Two roadmaps. Fourteen sprints across both. Twenty-four v2-deferred items. Two-hundred-fifty-five outstanding decisions. The roadmap is honest, paced, and demoable every week. The seller walks into the room with a calendar — not a vision deck.

### The close — Independence-minded posture and the two-contract model

**REID:** The closing. Bring the operating model home. The architecture decides; the cloud follows; the commercial discipline is what makes the recommendation defensible.

**KEVEN:** The Independence-minded operating model. *Deloitte recommends on technical and economic merits.* The two-contract model. *Customer contracts directly with the platform vendor on platform paper.* Microsoft on Microsoft paper for the Azure subscriptions, Fabric capacity, Foundry consumption, Purview licensing, Entra licensing. *Customer contracts directly with Deloitte on Deloitte paper for the services.* Separate paper. *No margin stacking.* Deloitte does not mark up Microsoft licensing. *No partner-channel motion.* The seller operates as an independent advisor.

**REID:** And the verbatim sentence the seller says when the question comes.

**KEVEN:** Five sentences. *One — the recommendation is on merits, not on compensation.* *Two — the customer contracts with the platform vendor on platform paper.* *Three — the customer contracts with Deloitte on Deloitte paper, separately.* *Four — no reseller margin.* *Five — the seller's commercial relationship with the customer is on Deloitte paper only.* Five sentences. The seller memorizes them. The seller can say them on a phone call on a Friday afternoon without flinching.

**REID:** And the productization window.

**KEVEN:** The productization gap is open and finite. Microsoft is broadest productized today across Fabric, Foundry, Purview, and Entra; the gap narrows through 2026 and 2027 as AWS and GCP invest. *The twelve-month window is when the lead is most defensible.* The seller earns the Microsoft recommendation now. The architecture is portable; if the productization landscape shifts in eighteen months, the architecture survives the shift. *The relationship that the seller builds on the architecture carries the next decision*, whatever the productization picture looks like in 2027.

**REID:** And the long game.

**KEVEN:** *The Independence-minded seller plays to the renewal, not to the close.* The partner-channel seller wins one deal and loses the next two. The Independence-minded seller wins the deal that earns the relationship; the relationship retires more quota over five years than the partner-channel motion does. The discipline is hard. The compounding is real. *The seller who walks into Monday's meeting with the architecture-first pitch, the six discovery openers in their head, the five honest claims and the four overclaims as muscle memory, the six pushbacks ready, and the three scenarios where the recommendation points away from Microsoft — that seller earns the room, earns the recommendation, and earns the next conversation.*

**REID:** The series finale closer.

**KEVEN:** Three pages on the desk by Friday afternoon. Monday morning, the seller walks in and the framework holds. *Lead with architecture. The cloud recommendation follows on merits. Honesty is the moat. The productization window is open and finite. Earn the recommendation now; the relationship carries the next decision.*

### A reading I want to do

**KEVEN:** Reid, last reading of the series.

**REID:** Last reading. I want to come back to where Episode One started, and I want to put a sharper frame around it for the seller. I want to recommend Christensen, *Competing Against Luck*, one more time — but this time read for the seller, not for the designer.

**KEVEN:** Go.

**REID:** Episode One read Christensen for the design — *Sarah hires CFMP to do a job that has five frictions*. That reading still holds. The reading I want to do tonight is different. *The CIO across the table on Monday morning is hiring the seller to do a job.* That job is not — *sell me Microsoft*. The CIO has fifteen Microsoft sellers in their inbox already. The job the CIO is hiring the seller to do is — *help me make the architectural decision I am paid to make, without me having to do the comparison work myself, and without me being conflated with the compensation*. That is the job the seller is being hired for. Christensen's frame is the same frame; the customer is different. The customer of the seller is the CIO, and the job the seller is hired to do is *trustable architectural advice*.

**KEVEN:** Said exactly that way. The reading lands.

**REID:** And there is a companion reading I want to pair it with. I want to recommend a recent piece on *positioning architecture-first versus product-first*. There is a growing body of writing — strategy practitioners, analysts, design partners — arguing that B2B technology sales in 2026 are bifurcating into two motions. *Product-first sellers* lead with the product; the architectural pitch is window dressing on a SKU comparison. *Architecture-first sellers* lead with the architecture; the product recommendation follows on merits. The piece I want to recommend is the architecture-first read of that bifurcation. The argument lines up with Christensen's job-to-be-done frame — the CIO is hiring the architecture-first seller because the job is *trustable architectural advice*, not *help me close a deal with a specific vendor*. The two readings reinforce each other.

[pause]

**KEVEN:** *The job the CIO is hiring the seller to do is trustable architectural advice.* That is the line I want carried out of this episode. The seller who understands the job is the seller who survives the comparison and earns the renewal. Christensen, *Competing Against Luck*, second reading, for the seller. And the positioning-architecture-first companion. The two together sharpen the same blade from two angles, the same way Episode One paired Christensen with the Ulwick HBR article. Read both. They land.

### One disagreement

**REID:** The disagreement. Series finale. The disagreement has to be real one more time. *The multi-cloud-CFMP question.* A serious customer will ask, on Monday morning, whether CFMP can be ported to AWS or GCP — and the honest answer matters. The seller has to be able to say it without flinching. And we have to land what *the honest answer* actually is.

**KEVEN:** Walk your position.

**REID:** *The honest answer is — yes, fully portable. Here is the migration path.* That is what the architect across the table needs to hear. The framework is vendor-neutral by design; the migration path from Microsoft to AWS or GCP has to *exist*, not be theoretical. Bedrock for the agent runtime, Lake Formation plus Glue plus Athena for the Gold Tier, Macie plus CloudTrail plus QLDB for the trust substrate, IAM Identity Center for identity. Same shape. Same audit row. Same lot model. If the seller cannot walk that migration path in five sentences, the *yes-it's-portable* claim is marketing. I want the seller to be able to walk it.

**KEVEN:** And my position. *Yes, the architecture is portable; the productization on Microsoft is what's denser.* The seller leads with productization density, not with migration path. The migration path exists in principle; it does not exist as a one-click button. Most customers run on one primary cloud at the application-pack layer. The right pitch is — *here is what's denser today on Microsoft; here is what's portable in the architecture if you change your mind in three years*. The seller pivots on density, not on uniqueness, and does not over-promise on the migration path.

**REID:** And I press. Does the migration path *actually exist* or is it theoretical?

**KEVEN:** Honest answer. It exists at the framework layer; it is theoretical at the productized-pack layer today. The five principles are portable; the LedgerRow schema is portable; the lot model is portable; the agent fleet pattern is portable. *What is not portable as a button is the productization itself.* If the customer chose to migrate CFMP from APEX-M to an AWS realization in 2027, the project would be a six-to-nine-month engineering investment, not a configuration change. The seller should not say *here is the one-click migration to AWS*. The seller should say *the architecture is portable; the productization is denser on Microsoft today; if you migrate in 2027, it is an engineering project with a known shape, not a rebuild from scratch.*

**REID:** Convergence point. *Portable-by-default, single-cloud-by-default-execution.* The same framing the Cross-Cloud Agentic series Episode Eight converged on for continuity. *The architecture is portable. The customer almost always runs on one primary cloud at execution. CFMP-on-APEX-M is the densest of the three productizations today. The migration path exists in principle as an engineering project, not as a button.*

**KEVEN:** Said exactly that way. *Portable-by-default, single-cloud-by-default-execution.* The seller carries the convergence. The seller does not over-promise the migration; the seller does not under-claim the portability. The architecture is the architecture; the productization is what's denser; the customer chooses where to run.

**REID:** Converge. The disagreement is named and the convergence is on tape.

### What to carry forward

**KEVEN:** Three things. Series finale.

**REID:** Go.

**KEVEN:** *One — lead with architecture; the cloud recommendation follows on merits.* The seller does not pitch Microsoft. The seller pitches the right way to build agentic AI for the customer — the Acceleration Framework, the five principles, the four-layer stack, the pack on top. The cloud recommendation follows from the architectural commitments. The seller earns the recommendation; the seller does not assume it.

*Two — honesty is the moat.* The seller who says *lead with AWS* once — in the right scenario — is the seller the architect calls again. The four overclaims are the four shortest paths to losing the room; the discipline is to not say them. The three scenarios where the recommendation points away from Microsoft are the credibility currency. The Independence-minded operating model is verifiable on paper. The honesty is what differentiates the seller from every other Microsoft seller in the CIO's inbox.

*Three — the productization window is open and finite.* Microsoft is broadest productized today across Fabric, Foundry, Purview, and Entra. The gap narrows through 2026 and 2027. The architecture is portable; the productization is denser today. The seller earns the recommendation now. The relationship that the seller builds on the architecture is the asset that carries the next decision, whatever the productization picture looks like in 2027. *Play the long game.*

**REID:** Lead with architecture. Honesty is the moat. The window is open and finite. Three carry-forwards. The series finale.

### The sign-off

**KEVEN:** Eight episodes. Sarah's day. The agent fleet and the audit chain. Mobile, Scan, and Lot. Mobile, Trips, Replenish, and the home channel. The Portal as the operator console and the multi-tenant scaffold. Sonos as the ambient voice channel. Identity, consent, HIPAA, and senior accessibility. And tonight — the seller's playbook. The pack is real. The architecture is honest. The Microsoft productization is denser today. The portability is on paper for the day a customer needs it. The audit chain is replayable. The consent gradient is in code. The cadence law protects the customer in their own kitchen. The four-identity chain is on the same federation rails. *That is CFMP on APEX-M.* The seller carries it into Monday's meeting.

**REID:** I am Reid. Cross-cloud principal architect. Two decades across Microsoft, AWS, and GCP buildouts. The honest comparison is the long-term seller's edge. Thank you for listening to *The CFMP Podcast*.

**KEVEN:** I am Keven. Vice President, Deloitte's Microsoft Technology and Services Practice. Twenty-two years on the Microsoft platform. The architecture decides; the cloud follows; the seller earns the recommendation on merits. *See you in the field.*

[Sound: the closing sting. ~6 seconds. The series ends.]

---

## Further reading

- **Source docs**
  - CFMP Mobile Design Document — `C:\code\iot_device\docs\packs\CFMP-Mobile-Design-Document.md` — §9 (Roadmap), §9.1 the eight-sprint plan, §9.3 the v2 deferred backlog, §9.4 the two-hundred-seventeen decisions in the queue, §9.5 the eight strategic open questions; §10 (Open questions) and §10.4 the twelve strategic decisions for kmarkham
  - CFMP Sonos Design Document — `C:\code\iot_device\docs\packs\CFMP-Sonos-Design-Document.md` — §9 (Roadmap), §9.1 the six-sprint plan, §9.3 the v2 deferred backlog, §9.4 the thirty-eight decisions, §9.5 the six strategic open questions; §10 (Open questions) and §10.4 the open questions for kmarkham
  - CFMP Mobile Roadmap — `C:\code\iot_device\docs\packs\CFMP-Mobile-Roadmap.md` — the consolidated phasing and decision-tracking layer over the design
  - CFMP Sonos Roadmap — `C:\code\iot_device\docs\packs\CFMP-Sonos-Roadmap.md` — the Azure-native sprint sequencing for the speaker channel
- **Sibling series cross-reference**
  - Cross-Cloud Agentic Podcast — Episode 08, *The Seller's Playbook* — `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\08-the-sellers-playbook.md` — the cross-cloud version of the same seller's substrate; converged on the same *portable-by-default, single-cloud-by-default-execution* framing
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — the deployment topology the seller screen-shares on the client call; the architecture argument is already on the screen when the meeting opens
- **Microsoft Learn**
  - Cloud Adoption Framework — `https://learn.microsoft.com/azure/cloud-adoption-framework/` — the customer-side adoption framing the seller maps the architectural pitch to
  - Azure Well-Architected Framework — `https://learn.microsoft.com/azure/well-architected/` — the operational-excellence and security frames the seller cites when the CIO asks about non-functional commitments
  - Azure AI Foundry — `https://learn.microsoft.com/azure/ai-foundry/` — the productized agent runtime the seller names when walking the four-layer stack
  - Microsoft Fabric — Mirroring, Shortcuts, OneLake, medallion architecture
  - Microsoft Purview — catalog, lineage, access, sensitivity, DSPM for AI
  - Microsoft Entra External ID — CIAM tenant configuration for the customer-side identity
- **Industry / research**
  - Clayton Christensen, Taddy Hall, Karen Dillon, David Duncan — *Competing Against Luck: The Story of Innovation and Customer Choice* (HarperBusiness, 2016) — Episode One read it for the designer; tonight we read it for the seller; the job the CIO hires the seller to do is *trustable architectural advice*
  - A positioning *architecture-first versus product-first* read of the 2026 B2B technology-sales bifurcation — the architecture-first motion is the long-game seller's edge; pairs with Christensen as the rigorous companion to the narrative argument
  - Tony Ulwick — *Turn Customer Input into Innovation* (Harvard Business Review, January 2002) — the rigorous outcomes-driven version of the jobs-to-be-done framing the seller can use to structure the discovery openers

— end of episode 09 — end of *The CFMP Podcast* — series complete —
