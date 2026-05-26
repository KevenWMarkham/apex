# Episode 05 · Portal · Operator Console & B2B Multi-Tenant

**Episode 05 · Portal · operator console and B2B multi-tenant** — Monday seven on the dot, an early-shift operator sees an amber badge on a senior member's household and walks a missed-cue trace back to a presence detection at nine thirty-one the night before. We open on the moment a Portal shipped to *operate the system* prevents a refill that should not have been spoken. We walk the live `/architecture` page end to end as the seller's screen-share artifact, name the chat panel as the operator's system of action, sketch the vision-kit integration, and defend the multi-tenant scaffold that makes the customer the buyer and the retailer the integration partner *eventually*.

**Builds on:** the show bible (00-show-bible-and-format) · Episode 01 (Sarah's Day) · Episode 02 (Agent fleet & audit chain) · Episode 03 (Mobile · SCAN & LOT) · Episode 04 (Mobile · Trips, Replenish, and the home channel) · CFMP Mobile Design Document §5 (Architecture — Portal touchpoints) · CFMP Sonos Design Document §5 (Portal proxies, SonosStatusBadge) · CFMP Mobile All Experts Panel (Liu §5.3, Mendez §3.6)
**Run time:** ≈ 41 minutes target
**Last updated:** 2026-05-25

---

## Cold Open

[Sound: an operations room at seven minutes past seven on a Monday morning. The faint mechanical click of an HVAC kicking down a notch as the building wakes up. Two monitors at low brightness, a desk lamp at warm color temperature, a paper cup of coffee being set down without ceremony. The soft electric hum of the floor under fluorescents that have not warmed up yet. Somewhere down the hall, a printer working through a queued job from over the weekend.]

It is seven-oh-seven on a Monday morning, and Priya — the early-shift operator, three years in customer operations, one year on CFMP, the kind of person who reads the overnight summary before she takes her coat off — has just opened the Portal architecture view on her left monitor and the household-incidents queue on her right. The architecture view is the page she keeps open by default; she pinned it on her first day, and on the days she does not need it she still likes the way it makes the system feel *present*. The incidents queue this morning has four amber rows. Three of them are noisy — a Sonos webhook retry on a household whose router rebooted overnight, a delivery-arrival mis-fire on a customer who left her phone in a coat pocket, a routine credential rotation that completed cleanly an hour late. The fourth amber row is the one Priya stops on. It is on Robert Park's household. It is a SonosStatusBadge amber on a refill confirmation that did not deliver.

She clicks into it. The Portal chat panel opens with the trace identifier already loaded — `tr_2026-05-24T21:31:08Z_KP-2089-44531` — and the incident timeline renders. Twenty-three rows. The Pharmacy specialist composed the refill confirmation cue at nine-thirty on a Sunday evening. The Concierge dispatcher resolved Robert's kitchen Sonos as the target zone. The Sonos Cloud Control client got as far as token refresh. And then, at nine-thirty-one and four seconds, the presence service emitted a second-person detection in the kitchen — the in-store camera kit the household has on a counter for grocery scanning, repurposed in off-hours as a room-presence sensor, saw a second silhouette enter frame. The cue was already in the queue. The drug-name redaction kicked in before the WAV was synthesized. The cue went to *suppressed* with the reason `presence_check_failed_drug_name`. The audit row sealed clean. Robert never heard *your evening refill of metformin is ready for pickup Friday*. He never heard anything at all.

Priya picks up the phone. She dials Robert's preferred number — the Portal surfaces it from the household record with the *do-not-call-before-seven* badge already cleared. *Good morning, Mr. Park, this is Priya at CFMP customer care, I want to confirm Friday's refill is still on your calendar.* Robert says yes, and that he had been wondering, and that his neighbor had stopped by Sunday night to drop off a casserole and stayed for an hour. The carry-forward lot is sealed. The Friday refill is confirmed by voice. Priya tags the trace with `human_followup_completed` and the amber row goes green. Seven-fifteen on a Monday morning. One incident, walked end to end, in the surface the system was built to be *operated from*.

[Sound: a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start there. Seven-oh-seven on a Monday. Priya, the architecture view on the left monitor, the amber row on Robert's household, the phone call at seven-fifteen. Because that moment is what the Portal *is*. Not a dashboard. A surface from which a human operates the system the customer experiences.

**REID:** And the moment turns on two things the architecture has already paid for, by Monday morning. *One* — the suppression decision the Sunday-evening cue did not deliver. The presence detection fired; the drug-name redaction held; the cue suppressed; the row sealed. That is the design protecting a customer's privacy without a human in the loop. *Two* — the human-in-the-loop that catches the consequence of the suppression. Robert did not hear the reminder. The Portal raises the missed cue to the operator. The operator picks up the phone. The system that protected the privacy is the same system that closes the loop. Both halves of the design.

**KEVEN:** Welcome back to the CFMP Podcast. Episode Five. *Portal · operator console and B2B multi-tenant.* In Episodes One through Four we walked Sarah's surface — the customer's mobile, the home channel, the trip life-cycle, the auto-replenish. Today we walk the other side of the glass. The operator's surface. The seller's surface. The live `/architecture` page that goes on every client screen-share. And the multi-tenant story — what it means that the customer is the buyer and the retailer is the eventual integration partner.

**REID:** Six sections. Who the Portal is for. The architecture page in detail — the hero section of the episode. The chat panel. The vision-kit. The B2B retailer multi-tenant story. And the Independence-minded posture on retailer co-deployment. The reading, the disagreement, the carries. Let's go.

---

## The conversation

### Who the Portal is for

**KEVEN:** Back to Priya at seven-oh-seven, two monitors open, the amber row on Robert's household. *That moment is what the Portal exists for.* Three different audiences open this surface, but it's the same surface — and the design decision that holds the whole thing together is that the three audiences see *one Portal, three readings of it.*

**REID:** Walk the three.

**KEVEN:** *Priya the operator.* The early-shift human who lands at seven on a Monday with twenty open incidents and ninety minutes to triage before the floor fills with customer calls. The Portal is *her* product. The incidents queue, the trace timeline, the household record with the *do-not-call-before-seven* badge — all of it is designed for the operator who closes the loop the system can't close alone. Priya is the design's center of gravity. *Every Portal feature first answers — does this help Priya?*

*The seller on a Wednesday client call.* The seller opens the same Portal Priya is looking at, but enters through the architecture view instead of the incidents queue. One tab, one screen-share, and the architecture argument is on the customer's monitor before the seller has finished the introduction. The seller's Portal isn't a slick demo — *it's Priya's production console.* Which is exactly why the buyer trusts it. The demo and the operations are the same surface; the customer is being shown the system she would actually inherit.

*The retailer-tenant administrator, eighteen or twenty-four months from now.* The retailer that signs the co-deployment agreement gets a slice of the Portal scoped to its stores. That view doesn't exist in the UI today — but the data model carries the tenant boundary from the first migration. We come back to that in section five.

**REID:** And the trap. *A console for three audiences risks pleasing none.* The classic enterprise-software dashboard built for the executive, the engineer, the analyst, and the auditor — readable by none of them. Defend why CFMP doesn't fall into it.

**KEVEN:** Conceded as the classic trap. The defense is that the *primitives* serve all three; only the *surface* adapts by role. Four primitives. The architecture page — the deployment as it actually runs. The chat panel — the operator's system of action. The vision-kit panel — the eye on the device fleet. The audit search — the trace identifier as the query handle. All three audiences use all four. Priya reads the architecture page as a *health surface* — green badges, amber badges. The seller reads it as a *credibility surface*. The retailer-tenant administrator, eventually, reads it as their *scope surface* — *here is my slice of the deployment.* One primitive, three readings.

**REID:** And the failure mode if the primitive splits.

**KEVEN:** Exactly the trap. The architecture view becomes three different pages. The chat panel becomes three different chats. The seller's screen-share demos a *different system* than Priya operates, which means the buyer is being shown a system she will not actually inherit. *The design's commitment to one Portal, three reads, is what keeps the seller honest.* The demo is the operations. The buyer sees what Priya will see Monday morning at seven-oh-seven.

**REID:** Said cleanly. Move to the architecture page itself.

### The /architecture page in detail

**KEVEN:** The hero section. Picture me on a Wednesday afternoon, twenty minutes into a thirty-minute architecture review with a CIO. She has heard the cloud-of-the-month pitch from three vendors this quarter. She wants to know what she'd actually be buying. *I don't open a slide deck.* I open one tab in the browser — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — and share my screen. The CIO is looking at the production deployment. The architecture argument is already in front of her before I've finished saying my name.

**REID:** Walk it the way Priya walks it Monday morning and the way you walk it Wednesday afternoon.

**KEVEN:** Top of the page. The region. *East US Two.* That seems like a metadata flourish — it isn't. The seller's first question from a CIO is usually *where does my data live.* East US Two is one of the Microsoft 365 paired regions for the East coast; it carries the AI capacity, the speech voices, the database, and the container runtime all in the same place. *Region is the first commitment, not the last.* The latency is low, the data residency is clean, and I don't have to explain why the AI traffic crosses a continent before it answers Sarah. The page leads with the region because the buyer's first question is the region.

Below the region marker, three boxes side by side. *The three houses Sarah's system lives in.* The customer's app — what Sarah holds in her hand. The operator's console — what Priya is looking at right now. The agent's home — where the planning brain and the four specialists run. Each one is a Microsoft container service in the same region. Same platform, three workloads, one bill. (The boxes are labelled `ca-visionkit-mobile`, `ca-visionkit-portal`, `ca-visionkit-orchestrator` — but the CIO doesn't need the names; she needs to see the three houses and that they line up.)

Why the container platform matters to her. Three properties without saying *Container Apps* three times. *Every code change produces a new revision; rollback is a label change, not a redeploy.* That is the seller's answer to *what happens when something breaks at three in the morning.* *Scale-to-zero on the surfaces that can afford it* — Priya's Portal goes to zero overnight; Sarah's app stays warm. *Native ingress* — the customer doesn't need an additional gateway product for the v1 deployment. Three properties. One platform.

Below the three houses, a ring of supporting services. *The voice engine* — Azure Speech, the neural voice that becomes Sarah's kitchen speaker cue. *The storage* — where every spoken cue audio file, every raw scan photo, every long utterance lives. *The database* — where every household's profile, lot, audit row, and consent setting lives, with a separately-isolated tenancy for the pharmacy data so health information never co-mingles with grocery. *The identity surface* — Microsoft Entra, where Sarah logs in with her phone, Robert with a passkey, Diana inherits her caregiver scope. And a smaller inset showing the *agent fleet* — the parent and the four specialists, each labelled with what it does for the customer.

Across the bottom of the page, the audit substrate. Three tiers. *Bronze* — the raw record of every event the system saw. *Silver* — the canonical model of lots, profiles, audit rows. *Gold* — the curated views the agents are allowed to read. The hash-chain spine runs through all three. *Sarah doesn't see this. The CIO does — and that's the point.* The audit substrate is what lets Priya answer the Monday-morning question. The substrate is what lets the seller close the architecture conversation.

On the right side, two arrows reach out of the diagram toward the customer's home. *The path to the Sonos cloud* — the warm voice that reaches Robert's kitchen. *The path to the customer's phone* — which acts as a bridge to the speaker when the household doesn't own a Sonos. The external integration is the only piece of the deployment that touches the customer's home network; everything else is in the cloud. *The customer is not buying an appliance; the customer is buying a service.*

**REID:** Now press on what's missing. The page is a curated reading of the truth. Name the curations honestly.

**KEVEN:** Two missing pieces, named honestly. *The gateway-and-WAF layer isn't on the page.* The v1 deployment uses the container platform's native ingress; that works at the customer-co-located scale. It doesn't work when the retailer signs in v2 and brings federated traffic, or when the deployment goes multi-region. The page should grow a gateway box when the deployment grows it. *The observability surface isn't on the page either.* Telemetry is load-bearing for the seller's reliability argument; the page today is control plane and data plane. It needs an observability plane in the next revision.

**REID:** A third I'd name — the *state-store decision* isn't visible. Postgres for everything, or is Cosmos hiding in a corner of the orchestrator? The buyer's architect will ask.

**KEVEN:** Conceded. The v1 commitment is Postgres for the state store; session-local observation lives on the device. There is no Cosmos in the v1 deployment. The page should *label* the commitment visibly so the question doesn't have to be asked. Next revision corrects it.

**REID:** And the live URL — say it again so the listener can paste it.

**KEVEN:** `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture`. Open it on a client call. The architecture argument lands while you're still introducing yourself.

**REID:** Said cleanly. Move to the chat panel.

### The chat panel

**KEVEN:** Back to Priya. She clicked the amber row. The chat panel opened. *And the panel didn't ask her what she was looking at* — the panel already knew, because the same tracking thread that started Sunday evening on Robert's kitchen speaker was already loaded as the conversation root. The panel turns the Portal from a *console you look at* into a *console you act from.* Walk the property.

**REID:** Walk it.

**KEVEN:** Every conversation in the Portal is anchored to a tracking thread. When Priya clicks the amber row, the panel opens with the thread already loaded. Every message Priya sends — to the agent fleet, to a colleague, to an automated runbook — carries that thread. Every system response carries it back. *The conversation isn't anchored to Priya's session.* Her session ends when she logs off; the thread persists as long as the customer's lot it serves. If Priya hands the incident off to the next-shift operator at four in the afternoon, the thread is the only thing she needs to hand over. The next operator opens the panel with the thread loaded, and the context arrives whole — the Sunday-evening cue, the suppression, the Monday-morning phone call, every conversation in between. *One trace, one query, one defense* — Episode Two's line, applied to Priya's seat.

**REID:** And the mirror property. The rule the team named *no silent side effects.*

**KEVEN:** Every cue the system spoke on the customer's surface shows up in the panel as a system message. The speaker spoke *your evening refill is ready for pickup Friday* on Robert's kitchen at nine-thirty Sunday — the panel shows that line as a system message. The cue was *suppressed* — as it was in the cold open — the panel shows that too, in plain language: *suppressed on kitchen — drug name redaction held — second person present.* Priya doesn't have to guess whether the speaker said something. The panel says, in human language, what the system did and what the system *didn't* do. That's the rule turned into a UI commitment. The customer is protected from the silent failure mode where Priya has to interrogate a log file to find out the speaker stayed silent.

**REID:** And the customer-experience consequence.

**KEVEN:** The panel is a *render* of the system's record, not a separate place where Priya types into a different system. Every spoken cue, every suppressed cue, every phone notification, every email, every action Priya takes — all of it is on the same record. When Priya picks up the phone at seven-fifteen and dials Robert, the call is recorded. When she tags the resolution, that's recorded. When her manager opens the incident the next morning to audit her work, the manager sees one chronological stream — Sunday-evening cue, suppression, Monday-morning amber, phone call, tag, resolution. *The hand-off isn't a Slack thread. The hand-off is the thread.* The operator's action and the system's action share the same substrate. *That's what makes the Portal a system of action, not a viewer.*

**REID:** Said cleanly. The chat panel is what turns the Portal from a viewer into a system. Move to the vision-kit.

### The vision-kit / camera integration

**KEVEN:** Back to the cold open. The reason the cue was suppressed at nine-thirty-one Sunday evening was that the kitchen-counter camera at Robert's home saw a second silhouette enter the frame. *Priya needs to know that happened.* She doesn't need to see the kitchen. She needs to see what the system inferred from the kitchen. That's the vision-kit panel.

**REID:** Walk it briefly.

**KEVEN:** The panel shows Robert's camera as a small tile — *device name, last-seen-online, presence status, current mode.* Presence status is the field that mattered in the cold open. The camera at Robert's counter is owned by the household, paired through Robert's consent. *The frames stay on the device.* Only the inference crosses the boundary into the Portal — *occupied, two people, last detected nine-thirty-one Sunday evening.* That isolation is the privacy commitment that makes the camera deployable in someone's kitchen in the first place. *Priya isn't watching Robert's kitchen. Priya is reading a presence inference.*

**REID:** And the retailer scale.

**KEVEN:** At retailer scale, when v2 ships, the panel grows tiles for the store cameras — the counter-scan cameras, the pickup-lane plate readers, the back-of-house cameras. Same property. The operator sees the inference, not the frames. The retailer's privacy posture is preserved by construction. The agent fleet uses the in-store presence to time the *pickup-ready* cue and to suppress proactive nudges in a crowded aisle. *The vision-kit feeds the agents; the operator reads the same inference stream the agents reason on.* Same substrate, two readings.

**REID:** And Episode Eight.

**KEVEN:** Episode Eight walks the consent layer in full — the four-identity chain that distinguishes a household camera, a delegated camera under caregiver consent, a retailer-owned in-store camera, and the public-space camera the design refuses to touch at all. *The operator never sees a frame, period.* The substrate enforces it. The panel makes the substrate legible to Priya.

**REID:** Said cleanly. The vision-kit is the operator's eye on the device fleet, with the privacy boundary preserved by the inference-only handoff. Move to multi-tenant.

### B2B retailer multi-tenant

**KEVEN:** Picture a retailer's procurement officer two years from now. The customer who's been using CFMP at home wants the pickup-lane speaker at the store to say *your pickup is ready in lane four* in the same warm voice she hears in her kitchen. *That experience only happens if the retailer signs.* This section is about the design's posture toward that signature — and the discipline that makes the customer's value not *depend* on the signature.

**REID:** Liu's hard truth, on tape — *plan for the retailer to NOT sign for eighteen months.* The honest read of retailer-procurement timelines. Four organizations on the retailer's side, each with its own quarterly planning cycle, each with its own risk-averse default. *Eighteen months is the fast case. Thirty months is the median. Never-signs is a real category.* The design has to ship value to the customer in all three.

**KEVEN:** The design ships value to the customer in all three. *The home-only configuration is the wedge.* Sarah buys CFMP, installs the app, connects her kitchen speaker, links the loyalty memberships she already holds at every retailer she shops at — and gets the full Episode Three-and-Four experience on day one. *No retailer signature required.* Her grocery week is improved by the lot management, the auto-replenish, the home channel, the trip life-cycle, the meal planning — all of it works without any retailer being a co-signer. The customer's retention bet at week twelve is *paid* on the strength of the home-only experience.

When a retailer signs, *more shows up.* The store speakers can address customers in the lane. The dairy-aisle speaker can announce Sarah's coupon savings. The retailer's loyalty integrates deeper. The voice persona stays warm and consistent — the same voice Sarah hears at home — because one voice is the rule. But the customer who shops at a retailer that *hasn't* signed doesn't get *less.* She gets the same home experience. *The retailer's signature unlocks additional surface area; the retailer's absence doesn't subtract.*

**REID:** And the discipline that makes the retailer's eventual signature even possible.

**KEVEN:** Compliance posture from sprint zero, even before any retailer is at the table. The pharmacy tenancy is isolated from the rest. The audit chain is real and attested. The identity surface supports federated retailer logins. When the retailer's procurement team asks for the security report, the report is already there — current, attested, with the retailer-relevant controls already audited. *The retailer doesn't have to wait for a six-month compliance cycle before they can sign; the compliance posture predates the partnership conversation.* That's Liu's line — *get the compliance posture right before pursuing partnerships, not after* — turned into an engineering commitment.

**REID:** And the data model commitment behind the v1-to-v2 transition.

**KEVEN:** The data model carries a *tenant boundary* in every table from day one. Lots, orders, profiles, audit rows, speaker households, camera devices — all of them have the column from the first migration. In v1, every row's tenant value is the same — there's only one tenant, the CFMP-operated one. The UI doesn't show the column. The query layer always filters on it. When the first retailer signs, the v2 deployment grows the UI and the access layer reads the caller's tenant from the federated login claim. *The data doesn't migrate. The UI grows. The data doesn't.*

**REID:** This is the part most teams get wrong. They ship single-tenant, the schema doesn't carry the column, and the multi-tenant retrofit becomes a six-month database migration. The CFMP team committed to the column on day one without committing to the UI on day one. *Small tax now. Large benefit later — the v2 ship is a UI feature, not a rebuild.*

**KEVEN:** Said cleanly. Move to the Independence posture.

### Independence on retailer co-deployment

**KEVEN:** Now the commercial discipline that lives underneath the design. The customer is the buyer. The retailer is the integration partner *eventually.* The two facts have to stay separated, in the design and in the contracting, or the design becomes leverage for a future retailer relationship instead of a system the customer can rely on today.

**REID:** And the contracting model.

**KEVEN:** Two contracts. The customer contracts directly with Microsoft for the cloud consumption — one bill, one tenant, one identity surface. The customer contracts directly with Deloitte for the CFMP delivery and the Portal Priya works from. *No third-party margin stacking.* When the retailer signs — eighteen months, thirty months, whenever — the retailer signs a separate, additive third contract for its own tenant consumption and its own integration. The customer's contract isn't affected. The customer can choose whether to onboard a newly-signed retailer or not. *The customer's experience is determined by the customer's choices, not by which retailers have signed up.*

**REID:** And the seller's argument.

**KEVEN:** *The customer-value-without-retailer-signoff is the design's default state, not a contingency plan.* The seller doesn't ask the customer to bet on a retailer signing in eighteen months. The seller shows the customer value on day one and names the retailer co-deployment as a *roadmap unlock*, not a *prerequisite.* The buyer hears it as honest because it is honest. The seller doesn't have to dress up the timeline. *The eighteen-month uncertainty is on the retailer's side. The customer's value is on the customer's side. The two sides are decoupled by the design.*

**REID:** Said cleanly. Carry that into the disagreement, because this is where it splits open.

### A reading I want to do

**REID:** A reading. I want to recommend the one that has been hanging over the cold open since the seven-fifteen phone call landed, because the cold open is, in its bones, an *observability* moment — the operator does not see the system directly; the operator sees an inference about the system, and the inference is what guides her action. *Charity Majors, observability as a product.* The body of work she has built over the last decade at Honeycomb, codified in *Observability Engineering* — the book she co-wrote with Liz Fong-Jones and George Miranda in twenty twenty-two — and in the years of essays she has published on the practitioner-facing internet. Majors' argument is that observability is not a backend concern that an SRE consumes from a Grafana dashboard; observability is a *product surface* that engineering and operations build *together*, with the same product discipline as any customer-facing feature. The dashboards, the trace timelines, the high-cardinality event streams — these are the operator's product. The operator is the user. The user has tasks; the tasks have success criteria; the surface is judged by whether the operator can complete the task without leaving the surface.

**KEVEN:** And the relevance to the Portal.

**REID:** The Portal is the design taking Majors' line seriously. The operator's task in the cold open is *understand what happened to a customer's refill confirmation between Sunday evening and Monday morning, and act on it*. The success criterion is *the customer's refill is confirmed by phone before noon Monday*. The surface — the architecture view, the incidents queue, the chat panel with the trace identifier already loaded, the household record with the phone number and the *do-not-call-before-seven* badge — is designed for that task end to end. The operator does not leave the surface. The operator does not open Slack, or jump into a separate observability tool, or page an engineer. The Portal is the *operator's product*, designed with the same product discipline the mobile is designed with for the customer. Majors' frame sharpens the design's defense because the design is doing what Majors says good observability surfaces do — treating the operator as a user, not an afterthought. The Portal is observability-as-a-product, applied to the CFMP system's operator console.

**KEVEN:** And the second reference I want to pair it with — briefly — is the chapter on console design in the Google SRE book, *Site Reliability Engineering*, the chapter on simplicity and the chapter on practical alerting. The argument there is parallel — the operator's surface is judged by *signal-to-noise ratio* and by *time-to-decide*, not by *information density*. The Portal's incidents queue in the cold open had four amber rows; three of them were noise; one was the signal. The surface presented all four with the same affordance, and trusted the operator to triage; the surface did not bury the signal under a hundred routine cues. Google's chapter on practical alerting names the discipline — *alert on symptoms, not causes; alert on what the operator can act on, not what the system tells you about*. Majors plus the SRE book — the Portal is a console designed in that tradition. The page is a *product*; the page respects the operator's time; the page surfaces signal and lets the operator triage noise.

**REID:** Pair them and the reading is complete. *Observability Engineering* on the principle; *Site Reliability Engineering* on the practice. The Portal is the design's expression of both.

### One disagreement

**REID:** One disagreement, the customer-grounded version. *Is Priya's Portal ready for retailer multi-tenant on day one, or is that engineering tax we're paying for an audience that may not exist for eighteen months?* Two voices on the design team — call them the *architecture-from-day-one* voice and the *Priya-comes-first* voice — pulled in opposite directions on this.

**KEVEN:** Put it on tape.

**REID:** The architecture-from-day-one position. *V1 ships multi-tenant scaffolding even without a signed retailer.* The architecture is right from day one only if the multi-tenant property is real from day one. Tenant identity in the data model. Tenant scoping in the access layer. Tenant-aware audit rows. Federated identity ready to accept a retailer's logins. The scaffolding pays the engineering tax now so the v2 retailer-onboarding is a *feature*, not a re-architecture. The fact that there is only one tenant in v1 is a *configuration*, not an *architecture.* The architecture is multi-tenant from the first migration.

The Priya-comes-first position. *V1 should be optimized hard for the operator.* Priya is the design's primary user. Every abstraction that doesn't serve her is a cost on her day. A tenant switcher that always shows the same tenant is cognitive distraction. A scoping predicate she never sees the consequence of is engineering overhead the team carries for an audience that may not exist for eighteen months. *Until the retailer signs, the design's center of gravity is Priya at seven on a Monday morning, and Priya doesn't need a tenant switcher.*

**KEVEN:** Both lines are right at the layer they're right at. The convergence has to honor both.

**REID:** Bring them.

**KEVEN:** The convergence. *V1 ships an operator-first Portal with multi-tenant scaffolding in the data model only.* The data model carries the tenant boundary from day one — the architecture-from-day-one win, paid in full. The UI is single-tenant — the Priya-comes-first win, paid in full. Priya never sees a tenant switcher in v1. The architecture page, the incidents queue, the chat panel, the vision-kit, the audit search — all of it as we walked in the cold open. The query layer enforces the tenant filter implicitly on every read; the v1 system always returns the same tenant. When the first retailer signs, the v2 ship grows the UI on the *same substrate.* *The data doesn't migrate. The UI grows. The migration is a feature, not a rebuild.*

The convergence resolves both. The architecture is right from day one in the substrate. *Priya is the primary user in the surface.* The two aren't in tension when the architecture pays its cost in the right layer.

**REID:** Converge accepted. *Data model multi-tenant from day one; UI single-tenant in v1; v2 grows the UI on the same substrate.* The customer is the better for it — because Priya's day stays clean, and when the retailer eventually signs, the rebuild Priya's manager would have to schedule never happens.

**KEVEN:** Said cleanly. Carry it.

### What to carry forward

**KEVEN:** Three things into Episode Six. Each one a thing a non-technical leader can carry into a Monday meeting.

**KEVEN:** *One — open the architecture page on every client call.* `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture`. The page is the production deployment, not a slide. The architecture argument is on the CIO's monitor before the seller has finished saying her name. *The demo is the production console; the production console is the most honest demo a buyer can see.* The seller doesn't dress up the deployment — the deployment is dressed up by being *the deployment.* Carry that.

**KEVEN:** *Two — the tenant boundary is in the data from day one; the UI grows on the same substrate.* Multi-tenant UI can wait; multi-tenant data cannot be retrofitted. The team carries one extra column on every relevant table from sprint zero. The v1 UI never shows it. When the first retailer signs eighteen months in, the v2 UI grows on the same substrate. *Small tax now. Large benefit later — the v2 ship is a feature, not a rebuild.* Carry that.

**KEVEN:** *Three — Priya is the design's primary user.* Every Portal feature first answers — *does this help Priya?* The seller's screen-share works because Priya's surface is honest. The retailer's eventual tenant view works because it grows from Priya's surface. Priya at seven on a Monday morning is the design's most important reader, *because she's the human who closes the loop the system can't close alone.* No silent side effects. The Portal has to show what the system did, has to show what the system *didn't* do, has to hand the thread off to the next-shift operator without context loss. *The customer is the better for it — because the operator who closes Priya's loop is the operator who calls Robert at seven-fifteen and confirms his refill.* Carry that.

**REID:** Architecture page on every call. Tenant column from day one. Priya as the primary user. Three carries. Into Episode Six.

**KEVEN:** Next episode — *Sonos · the ambient voice channel*. The Cue, the Cue Bus, the Zone, the ducking, the AirPlay-bridge fallback, the Azure-native deployment that lets the speaker talk to the cloud without any laptop or local appliance in the household. We have walked the operator's surface; next episode we walk the customer's *ambient* surface — the radio in Sarah's kitchen, the voice in Robert's evening, the channel that keeps the system present when the customer is not in the app.

[Sound: the closing sting. ~6 seconds.]

---

## Further reading

- **Source docs**
  - CFMP Mobile Design Document — `C:\code\iot_device\docs\packs\CFMP-Mobile-Design-Document.md` — §5 (Architecture — Portal touchpoints, the full-stack diagram, the live URL in the header, the file-level structure for the Portal proxies, the local-first deferred architecture that the Portal would have to grow to support v2 private-network deployments)
  - CFMP Sonos Design Document — `C:\code\iot_device\docs\packs\CFMP-Sonos-Design-Document.md` — §5 (Portal proxies for Sonos connect-and-callback-and-webhook, the SonosStatusBadge component contract, the architecture-page edit list for adding the Sonos Cloud row to the control plane), §6.9 (the visual mirror in the chat panel, Mendez's *no silent side effects* rule), §8.8 (Liu's B2B multi-tenant framing — *plan for the retailer to NOT sign for eighteen months*)
  - CFMP Mobile All Experts Panel — `C:\code\iot_device\docs\packs\CFMP-Mobile-All-Experts-Panel.md` — §3.6 (Diego Mendez on customer support and resolution, the *trace_id on every escalation* commitment, the *no silent side effects* posture turned into UC-165), §5.3 (Jennifer Liu on B2B retailer partnership, the SOC 2 Type II as table-stakes, the multi-tenant store-map provisioning workflow as v2, the white-label option deferred)
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — the hero artifact this episode walks. The Container Apps strip, the data and identity row, the audit chain panel, the Sonos Cloud Control external integration column, the East US 2 region marker. Open on every client call; the architecture argument is on the customer's monitor before the conversation has named a single Microsoft service.
- **Microsoft Learn**
  - Azure Container Apps overview — `https://learn.microsoft.com/azure/container-apps/` — the platform behind `ca-visionkit-mobile`, `ca-visionkit-portal`, and `ca-visionkit-orchestrator`. Revision-based deploy, scale-to-zero, native ingress; the seller's container-platform argument.
  - Azure AI Foundry — `https://learn.microsoft.com/azure/ai-foundry/` — the productized agent runtime that hosts the orchestrator and the five specialists. The Foundry surface is where the model-flexible architecture from Episode Two becomes a Microsoft-product story.
  - Microsoft Entra — `https://learn.microsoft.com/entra/` — identity, OAuth, B2B federation for the v2 retailer-tenant story. The B2B surface is what unlocks the retailer-administrator role in v2 without ever touching the v1 customer identity story.
- **Industry / research**
  - Charity Majors, Liz Fong-Jones, George Miranda — *Observability Engineering* (O'Reilly, 2022) — and the body of essays on Honeycomb's blog framing observability as a *product surface*, not a backend concern; the principle behind the Portal's operator-as-user posture.
  - Google's Site Reliability Engineering book (*Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly, 2016) — particularly the chapter on practical alerting (alert on symptoms, not causes; alert on what the operator can act on) and the chapter on simplicity in console design; the operational tradition the Portal's incidents queue is designed within.
- **Sibling series cross-reference** — Cross-Cloud Agentic Episode 04 (*Multi-Tenant Architecture and the Customer Boundary*) at `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\04-multi-tenant-and-customer-boundary.md` — the framework-level treatment of the data-model-tenant-id-from-day-one pattern the Portal's v1-to-v2 strategy inherits.

— end of episode 05 —
