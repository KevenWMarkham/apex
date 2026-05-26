# Episode 10 · Flux — Household composition and presence events

**Episode 10 · Flux — household composition and presence events** — the depth episode for the household-composition substrate. Episode Nine was the series finale. Episode Ten is the appended documentary deep-dive — we stand inside the substrate beneath every multi-location, multi-season, multi-life-stage household. Marcus Thompson at the cabin on a late-September weekend; a partial-absence event detected but not yet active; Sarah opens the Preference Center and taps approve; the home Auto-Replenish pauses; the cabin StayLot pattern picks up the slack; the trace_id propagates through the suspension. We open on that one tap because that one tap is the entire architectural ethic of the substrate — the agent says what it would do without doing it; the customer holds the spending key; effects fire only on `active`, never on `proposed`. Seven sub-sections walk what Flux is, the seven kinds across five families, the four-state lifecycle, why PERMANENT_DEPARTURE is HITL-only by design, the move pattern, the PURPOSE coupling to Recipes, and the Azure-native deployment that bridges into Privacy.

**Builds on:** the show bible (00-show-bible-and-format) · Episodes 01–09 · CFMP Mobile Flux Design Document §§0–12 in full · CFMP Mobile Lots Expert Focus §§1, 11 · CFMP Mobile Identity & Onboarding (household roster) · `orchestrator/flux.py` (the 7-kind / 5-family naming) · `db/04_flux_events.sql` (the lifecycle states + the back-pointer onto lots)
**Run time:** ≈ 40 minutes target
**Last updated:** 2026-05-25

---

## Cold Open

[Sound: a cabin in late September. The Sierra foothills. Tall ponderosa pines in a stand around a one-story timber-frame on a gravel pad. The light is long and bronze through the west-facing windows at four-fifteen in the afternoon — the angle the year takes on once equinox has passed and the days are visibly shorter every weekend. A wood stove ticking through its warm-up. A dog asleep on a braided rug in front of the stove, paws twitching through some dream. The radio is on low — a college football game from somewhere east, the announcer's voice the only human sound in the cabin. Outside, a single jay calls from the fence line. The access road up to the cabin is gravel; it closes at the first heavy snow, which the forecasts are starting to mention in a way they did not three weekends ago.]

Marcus Thompson is at the cabin for the third weekend in a row. The autumn run, the locals call it — the four or five weekends in late September and early October when the trout are still rising on the upper reach and the road is still passable and the cabin is still warm enough to sleep in without the propane heat running through the night. His two kids, eleven and nine, came up with him this weekend. Sarah dropped them off at the trailhead Friday afternoon; she will pick them up at the same trailhead Sunday evening. The kids are at the creek. Marcus is on the porch with a coffee that has gone cold twice and been microwaved once.

His phone buzzes. A notification from CFMP. Marcus opens it. *Proposed Flux event — partial absence — Friday September 26 through Sunday September 28 — kids visiting cabin — auto-replenish at the home cadence will continue unless you approve.* Below the line, four small chips. *Approve. Dismiss. Customize. Not now.*

Marcus doesn't tap any of them. The notification is not addressed to him. He's the visited household, not the visiting one. The notification is being shown to Sarah on her phone, four hundred and seventy miles away, in a town in the Central Valley where she is at her kitchen island with her own coffee and her own meal-planner open and her own week ahead of her. The CFMP household profile registered the pattern three weekends ago. The agent watched the GPS bloom of the kids' phones go quiet at the home zone every other Friday at four. The agent watched it repeat. The agent does not auto-pause anything. The agent surfaces the *proposed* event to Sarah because Sarah is the account holder; she opens the Preference Center; she sees the proposed partial absence with the use-it-up suggestion below it — *the spinach will not last another week and the kids won't be home for it.* She taps approve. The event flips from `proposed` to `approved` to `active`. The home Auto-Replenish for kid-coded items pauses for three weeks. The cabin StayLot pattern picks up the slack — Marcus's grocery delivery to the cabin's trailhead pickup point is already loaded. The trace_id from the proposal propagates through the suspension; the LedgerRow records who approved, when, against which event, with what consequence. The same one identifier ties the proposal to the approval to the pause to the cabin delivery. Eight hops; one trace.

[Sound: a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start there. Marcus on the porch. The kids at the creek. The notification on Sarah's phone four hundred miles south. The agent didn't pause anything until Sarah tapped approve. The HITL gate is the architectural ethic the whole episode rotates around. Episode Ten is the depth episode for the household-composition substrate.

**REID:** And the framing matters. Episode Nine closed the series. The sign-off was *see you in the field.* Episode Ten is something else — a documentary deep-dive on the one substrate the architecture has been hinting at across nine episodes but has not stood inside. We've shipped lots; we haven't shipped composition. This is the substrate beneath every multi-location, multi-season, multi-life-stage household — the cabin pattern, the college kid home for the summer, the parent who moves in, the partner who travels for work, the move across the country, the holiday gathering, the loss that the system refuses to ever auto-detect because the cost of being wrong is unbounded.

**KEVEN:** Welcome back to the CFMP Podcast. Episode Ten. *Flux — household composition and presence events.* Appended episode. Seven sub-sections. What Flux is. The seven kinds across five families. The detected-proposed-approved-active lifecycle. PERMANENT_DEPARTURE as HITL-only by design. The move pattern. The PURPOSE coupling to Recipes. The Azure-native deployment that bridges into Privacy. A reading. A disagreement. Three carry-forwards.

**REID:** Let's go.

---

## The conversation

### What Flux is

**KEVEN:** Start with the noun. Because the noun is doing the architectural work, and the noun is what most teams get wrong. *Flux* — capital F — is the household-composition-plus-presence-event surface in CFMP. The Flux Design document opens with a single working definition. A FLUX EVENT is a tracked, time-bounded change in household composition or presence that triggers a coordinated, HITL-approved set of effects across replenishment, meal planning, expiration warnings, and proactive nudges. Read that twice; the words are load-bearing. *Tracked.* Every Flux event is a row in a table. *Time-bounded.* Every Flux event has a start date; most have an end date. *Change in composition or presence.* Either the roster changed or somebody who's still on the roster isn't here this week. *HITL-approved.* The human approves before effects fire. *Coordinated set of effects.* The auto-replenish, the meal plan, the perishable warnings, the nudges — they all move together; they all read from the same event.

**REID:** And the framing the design document leads with — composition is a first-class sibling of lots.

**KEVEN:** First-class sibling of lots. Not a property of a customer. Not a property of a lot. *A sibling.* That is the move. In a naive design, the household is a column on the customer profile — `customer.household_size = 4` — and life events update the column. That works until the kids visit the cabin, the spouse travels for work, the in-laws come for two weeks, the older kid leaves for college and comes back for the summer and then leaves again. The column can't hold any of that. The column is a snapshot of a number; what the system actually needs is an event log.

The Flux Design document, Section One — *A FLUX EVENT has a kind, a window, an affected member set, a status, a provenance, and an effect bundle.* Six properties. Every Flux event is a row with those six. The current state of the household is a *fold* over the event log — start with the onboarding roster, replay every approved Flux event in chronological order, the resulting composition is what's true today. That is event-sourcing applied to household state. The household is not a row in a table; the household is a fold over an event log.

**REID:** And why composition has its own model.

**KEVEN:** Three reasons, each load-bearing. *One — a person isn't a property of a lot; they're an actor across many lots.* Sarah is in the meal-plan lot Tuesday night, the pickup-lot Wednesday morning, the pantry-lot Thursday afternoon when she scans the gochujang into the cabinet. The person traverses lots. The lot doesn't own the person. *Two — the household isn't a property of a customer; it's a composition that changes over time.* The household at onboarding is not the household three years later. *Three — composition events have downstream effects that are themselves time-bounded.* A vacation pause on Sarah's home Auto-Replenish has a start and an end; a permanent arrival of a new child has a start and no end. The event needs to outlive any single lot it touches because the effect on auto-replenish or meal-plan extends across many lots.

**REID:** And the audit consequence.

**KEVEN:** The audit consequence is the cleanest part of the model. *Every Flux event is event-sourced. Every state transition writes a LedgerRow. The trace_id propagates from the detection through the proposal through the approval through the activation through every downstream effect.* When a regulator or a customer-service agent or the customer herself asks *why did the auto-replenish pause from September twenty-sixth through October seventeenth?* the answer is one query — find the active Flux event for that window, walk its trace_id, the eight hops are right there. The household is event-sourced; the audit chain is the receipt.

### The seven kinds across five families

**REID:** Walk the seven. By family. In the order the design document gives them.

**KEVEN:** Five families. Seven kinds. The `flux.py` header names them verbatim — *ABSENCE, ARRIVAL, DEPARTURE, PURPOSE, PLACE.* I'm going to walk each family in order, name the kind, give the customer moment, and name the architectural distinction. Because the families are not a taxonomy convenience; the families *cluster the effects.* An ABSENCE family event pauses things. An ARRIVAL family event un-pauses things. A DEPARTURE family event archives things. A PURPOSE family event spikes things. A PLACE family event re-baselines things. The family names the shape of the effect bundle.

**REID:** Family one. ABSENCE.

**KEVEN:** *ABSENCE — the household shrinks.* Two kinds. *`vacation`* — the whole household is away. Sarah and the kids and the dog all leave Friday for Tahoe; the home is empty for ten days. The effect is *pause replenish, keep the home channel quiet, let the perishables get used up before departure.* The pre-clearout meal plan that consumes the romaine and the chicken and the herbs before Friday morning, that's a vacation effect. The Sonos cue at six-thirty in the kitchen that's not running because nobody's home, that's a vacation effect. The auto-orders that don't deliver on Saturday because nothing is going to be there to receive them, that's a vacation effect. *Pause the home, keep the audit chain quiet.*

The second ABSENCE kind is *`partial_absence`* — a recurring partial absence, the cabin pattern, the spouse traveling for work two weeks of every month, the kid at sleepaway camp every July. *Reduce volume but don't pause.* The math is different — the household is still consuming, just less of it. Per-member consumption shares enter the math. The naive default is `(active_members / total_members)` as a cadence multiplier; the smarter version is per-SKU per-member shares learned from purchase history. Akira Watari's domain — the operations researcher on the Flux panel — has the math.

The cabin pattern from the cold open is a `partial_absence`. The kids visit Marcus at the cabin during shoulder seasons. The home cadence reduces for the kid-coded items — the snack budget, the milk volume, the kid-specific yogurt — but the adult-coded items continue. The agent detected the pattern after three repeating weekends and surfaced a *proposed* event. Sarah approved. The math reduced the relevant SKUs; the rest continued.

**REID:** Family two. ARRIVAL.

**KEVEN:** *ARRIVAL — the household grows.* Two kinds. *`arrival`* — a temporary influx. A guest visits. The college kid is home for the summer. The in-laws are here for a week. Grandparents are visiting for Thanksgiving weekend. The effect is the inverse of partial-absence — *flip household_size briefly upward, restore the visiting member's preferences if they were previously a household member, add their dietary categories to the meal-plan grammar, scale the snack budget up.* The cuisine-breadth capability from Episode Eleven lights up here — the Korean grandmother visits, the meal-plan grammar expands to include Korean breakfast porridges, the shopping list includes Korean specialty ingredients, the cabin StayLot pattern handles the guest's accommodation if the guest is at a different address. ARRIVAL is the un-pause family.

The second ARRIVAL kind is *`permanent_arrival`* — a new household member. A child born. A partner moving in. An aging parent moving in permanently. The effect is the same as `arrival` but with no end date. The roster updates. The dietary profile expands. The cadence permanently scales. The auto-replenish absorbs the new mouths. The household-budget conversation surfaces gently in the concierge moments — *your typical food spend has gone from X to Y per week; want to discuss budgeting?* — not a pitch, a service.

**REID:** Family three. DEPARTURE. The sensitive one.

**KEVEN:** *DEPARTURE — the household shrinks permanently.* One kind. *`permanent_departure`* — HITL-only, never inferred. A child off to college and not coming back. A divorce. A death. An estrangement. The system refuses to detect these. The system *only* accepts a permanent_departure when a human initiates it — either the customer through a deliberate Preference Center path, or an operator through a support call where the customer has asked. The reasons for the refusal we'll walk in Section Four; this is the family where the design's ethic shows up loudest.

**REID:** Family four. PURPOSE.

**KEVEN:** *PURPOSE — composition unchanged but demand spikes.* One kind. *`event`* — a one-off purpose. Hosting Thanksgiving. A birthday party. The Super Bowl gathering. The dinner party Saturday night. The backyard wedding. *The household is the same size every other day.* What changes is the demand for one window. The effect is *no cadence change, but a one-shot order suggestion sized to the guest count, accounting for what's already in the pantry, with recipe coupling to the cuisine the host has indicated.* The Lunar New Year gathering, the Thanksgiving feast, the in-laws for the week — each PURPOSE event hands a *context* to the meal-plan engine that says *a guest is here this week with this cuisine preference,* and the Recipe capability does the rest. We'll walk that coupling in Section Six.

**REID:** Family five. PLACE.

**KEVEN:** *PLACE — the household relocates.* One kind. *`move`* — the household moves to a new address. New home. New closest stores. New aisle layouts. New pickup window viability. The effect is a *cascade re-baseline.* The auto-replenish re-targets to the closest store. The home channel re-registers if a new Sonos household identifier is needed. The customer-profile addresses gain a new primary. The audit chain carries both the old and the new address so a regulator who asks *where did this happen?* can read the answer in the LedgerRow.

**REID:** Seven kinds. Five families. Each family clusters the shape of the effects. Each kind is a row in the `flux_events` table with a CHECK constraint on the kind column. The `flux.py` API has one entry point that branches on kind; the SQL schema is one table with one column. The architectural elegance is that the surface is small.

**KEVEN:** Small surface; large semantic reach. *Seven kinds carry every household-composition pattern the design has been able to surface across two years of customer research.* That is the test of a good substrate.

### The detected → proposed → approved → active lifecycle

**REID:** The lifecycle. Four states. The state machine the design document gives in Section Two. Walk it from the top.

**KEVEN:** Four primary states. *Detected* — the signal has arrived. The calendar OAuth saw a multi-day event titled *vacation*; the geofence saw all paired phones leave the home zone for forty-eight hours; the seasonal-pattern recognizer saw the cabin pattern repeat for the third time; the customer said something in voice that parsed to a Flux intent. *The agent registers what it saw, scores its confidence, and writes a `detected` row.* No effects. No nudge. No notification. The customer doesn't see anything yet. The Bronze tier signal lives in the agent's transient reasoning.

*Proposed.* The agent has decided this signal is worth surfacing. The customer sees a nudge in the Preference Center or a concierge moment on the home screen. *Going to Tahoe Friday? I can pause auto-orders and suggest a use-it-up meal plan.* The proposed state shows the *effect bundle* — the concrete things the agent would do — alongside the proposal. The customer can see exactly what would change before approving. The customer's options at this state are *approve, dismiss, customize, not now.*

*Approved.* The customer has tapped approve. The LedgerRow is written. The effect bundle is committed. *No effects have fired yet.* The Flux event sits in `approved` until its `start_date` arrives. A vacation approved on Tuesday for a Friday departure waits in `approved` from Tuesday afternoon through Friday morning. The meal-plan adjusts because the meal-plan reads from `approved` and looks ahead — that's a planning effect, not a runtime effect — but the auto-orders don't pause until the start date passes.

*Active.* The start date arrives. The state transitions from `approved` to `active`. *This is the moment the runtime effects fire.* The auto-orders pause. The cadence multiplier engages. The Sonos cadence law shifts. The concierge banner shows. The home channel goes quiet. *Effects fire only on `active`, never on `proposed`.* That invariant is in the `flux.py` header. The header calls it out in capital letters because it is the architectural defense against false positives.

**REID:** And the other two states the diagram shows.

**KEVEN:** *Dismissed.* The customer said no to the proposal. The Flux event records the dismissal and remembers it. If the same pattern surfaces again in the future the agent considers the prior dismissal as a Bayesian prior — *the customer said no last time; the next propose threshold is higher.* The dismissal is information, not a wall.

*Superseded.* A newer, more specific event replaces an older, less specific one. Sarah approves a `vacation` for June 10-17 for the whole family. Two days later she approves a `partial_absence` for the spouse traveling June 12-14. The planner detects the overlap, asks the customer *merge or override?*, and on her selection either merges the effects or marks the older event `superseded` and lets the newer one carry the effect. *Newer specific supersedes older general.*

**REID:** And here I press. Why a four-state machine? Why not just `detected` and `approved`? Why an intermediate `proposed` state at all? Why not just have the agent show what it would do and the customer either says yes or doesn't?

**KEVEN:** Defended. Because the `proposed` state is where the agent says what it would do *without doing it.* That is not a UI distinction; that is an architectural distinction. In a two-state model, the moment the agent decides the signal is worth acting on, the customer's tap is *the only thing between the signal and the effect.* A misfired tap, a misread notification, a child grabbing the phone — and the effect fires. In a four-state model, there is a published, persisted, queryable artifact between detection and effect. The `proposed` row is a thing the customer can see, the support team can see, the auditor can see, and crucially the customer can *un-tap.* They can dismiss a proposal that already shows in their Preference Center; they can change the window before approving; they can ask the agent to explain the effect bundle.

The four states also separate *intent* from *time.* `Approved` means the customer has consented to the effect bundle; `active` means time has caught up to the start date. A vacation approved on Tuesday for a Friday departure is `approved` for three days before becoming `active`. During those three days the meal-plan adjusts but the auto-orders don't pause yet — because the auto-orders run on the active state, not on the approved state. The lifecycle separates the *agreement* from the *engagement.* Two-state would conflate them.

**REID:** And the cold-open walks one full lifecycle. Walk it back.

**KEVEN:** Marcus's partial-absence. *Detected* — the GPS pattern repeats three weekends in a row; the seasonal-pattern recognizer flags it; the confidence score crosses the threshold. *Proposed* — the agent surfaces in Sarah's Preference Center; the effect bundle reads *reduce kid-coded auto-orders by forty percent; pause kid-yogurt subscription this weekend; redirect this week's snack budget toward shelf-stable items.* *Approved* — Sarah taps approve at her kitchen island four hundred and seventy miles south. *Active* — the start date is the same Friday; the runtime fires; the home cadence reduces; the cabin StayLot delivers what the kids need at the trailhead pickup point. Four states. One trace_id. Eight hops. One audit chain.

### PERMANENT_DEPARTURE — HITL-only by design

**REID:** The hard one. The family of one. The kind the design refuses to ever auto-detect. Walk why.

**KEVEN:** Three reasons. *One — the harm of a false positive is unbounded.* A false-positive `vacation` is annoying; the customer gets a notification asking if they're going somewhere, they say no, the system moves on. A false-positive `arrival` is annoying; the system suggests more snacks, the customer says no thanks. A false-positive `permanent_departure` is *grief amplification at scale.* The system says *we noticed Sarah hasn't scanned in a while; should we remove her from your household roster?* The customer reads it as an obituary the algorithm wrote. The brand has done a kind of harm that no amount of accuracy in the other ninety-nine percent of cases makes up for. The math is asymmetric: the upside is *we detected a life event slightly faster;* the downside is *we caused the grief amplification.* No threshold exists where the expected value clears.

*Two — the cases requiring this kind cluster exactly where human judgment is non-negotiable.* The Flux Design document lists them. A grandparent passes away. A divorce. A child off to college and not coming back. An estrangement. A custody change. Each of these is a case where the customer is in a moment of intentional, often painful decision. The right experience is the customer arriving at the Preference Center on their own time, on their own terms, and saying *please update the roster.* The wrong experience is the system arriving at the decision and asking the customer to confirm.

*Three — the operational reality.* The signal that would have to be inferred is *absence of presence.* A person who hasn't scanned anything in N days. The signal is noisy in every direction. The college kid hasn't scanned because she lost her phone for two weeks. The spouse hasn't scanned because he's depressed and the depression flare has him not cooking. The grandparent hasn't scanned because she's in a hospital after a fall that's recoverable. *Absence of presence is not departure.* The system cannot honestly tell them apart. The design recognizes this and refuses to try.

**REID:** And the operator-initiated path.

**KEVEN:** *Operator-initiated permanent_departure.* A customer calls support. The customer says *my husband passed away.* The support agent has training, has a script, has a privacy policy, has a compassion protocol — Dr. Maya Patel, the family-systems therapist on the Flux panel, wrote the protocol with the Tier-One compliance lead Adebayo. The agent confirms the request, confirms the customer's identity, confirms the action with the customer in plain language, and writes the Flux event with `source='operator-initiated'` and the customer's chosen `sensitivity_mode` — neutral, celebration, or mourning. The default is neutral. The mourning mode is a hard mute on every nudge that would reference the deceased. The Sonos cue never says the name again. The system goes quiet.

**REID:** And the customer-initiated path.

**KEVEN:** *Customer-initiated permanent_departure.* Preference Center → Household → Remove member. The Preference Center surfaces a deliberate, multi-step confirmation flow. *This will permanently update your household roster. Continue?* If the customer continues, the second screen offers the sensitivity-mode selector — *neutral, celebration, or mourning* — with copy that names what each mode does without judgment. The Flux event writes with `source='customer-initiated'`. The roster updates. The auto-replenish recalibrates. The Sonos cue cadence shifts. *The system never asked the customer to make this decision; the customer arrived at it on their own.*

**REID:** And the architectural ethic showing up.

**KEVEN:** *The design refuses to optimize for the metric it cannot honestly measure.* That is the line. Hassan, the AI-safety lead from the All-Experts panel, has it in the Flux design document under the cross-cutting work package — *red-team on the permanent_departure inference path; assert no auto-inference path exists.* That is the test. The test isn't *the inference is accurate;* the test is *there is no inference path.* The architecture defends the boundary by not having a code path that crosses it. If the code path doesn't exist, the misfire cannot happen. *Architectural ethic enforced by architectural absence.*

### PLACE — the move pattern

**REID:** PLACE. The move. The hard test of every other capability. Walk it.

**KEVEN:** *Move* is the kind that exercises every other capability. Because a move changes the customer's relationship with every part of the system at once. Walk the cascade.

*The customer profile.* The addresses list gains a new primary. The old address moves to secondary or archive depending on the customer's choice — sometimes it stays for tax-and-receipt reasons, sometimes it's gone entirely. The Flux event records both addresses with the same trace_id so the audit chain carries the transition.

*The auto-replenish.* The cadence math doesn't change — the household is the same size — but the *target* changes. The closest store re-resolves. The pickup window viability re-resolves. The drive-time math re-runs. The perishables velocity may shift; a new climate, a new commute, a new walking pattern around the new neighborhood, all change the rate at which milk and produce get consumed. The auto-replenish recalibrates over the first thirty days at the new address.

*The home channel.* The Sonos household identifier may change. If the customer moved the speakers, the same household identifier carries; if the customer left them and got new speakers at the new address, the home channel re-registers. The cue cadence law re-runs against the new floor plan — a one-bedroom apartment is a different cue surface than a three-bedroom house.

*The fulfillment plug-ins.* The retailer plug-ins re-resolve their nearest store and their pickup-slot availability against the new address. A retailer that delivered to the old address may not deliver to the new one; the agent flags this in the proposed move event's effect bundle so the customer sees it before they commit.

*The audit chain.* This is the cleanest part. *The audit chain carries old and new addresses in the same trace.* A regulator who asks *where did this happen?* in six months can read both addresses in the LedgerRow; the trace_id binds them. The chain doesn't forget the old address; the chain records the transition explicitly.

**REID:** And the SQL piece.

**KEVEN:** The SQL schema makes this clean. `db/04_flux_events.sql` carries the `flux_events` table with the `start_date` and `end_date` columns and the `affected_member_numbers` array. A `move` event has a `start_date` of the move date and a `null` end_date — the move is open-ended; you're at the new address until further notice. The schema also adds a back-pointer on the `lots` table — `source_flux_event_id` — so any lot derived from a Flux event can be queried in either direction. A move that triggers a one-time *unpack the kitchen* shopping list creates a lot whose `source_flux_event_id` points to the move event; completing the move auto-closes the lot, and closing the lot auto-completes any unfinished move-related effects.

**REID:** And the architectural test.

**KEVEN:** *Does the system follow the household, or does it stay stuck at the old address?* That is the test. A naive system stays stuck — the auto-orders keep delivering to the old place, the meal-plan keeps recommending recipes for the old climate, the home channel keeps trying to reach a speaker that's no longer there. A correct system follows. The `move` event is the *handle* that triggers the follow. Every downstream capability subscribes to the event; every downstream capability re-baselines on the start date. The cascade is wide; the trigger is one row.

### PURPOSE — guests, holidays, and the Recipe coupling

**REID:** PURPOSE. The family that touches Recipes. The Lunar New Year visit. The Thanksgiving guests. The Korean grandmother for the week. Walk the coupling.

**KEVEN:** PURPOSE events flip household_size for the meal-plan window. *They do not change cadence.* Cadence is the steady-state replenish rate; PURPOSE doesn't move it. What PURPOSE does is *hand a one-window context to the meal-plan engine.* The context says *a guest is here from Friday through Tuesday, with this cuisine preference and these dietary constraints.* That context becomes input to the recipe-set suggestion engine. The output is a meal-plan for the window that respects the cuisine, accommodates the dietary constraints, and accounts for what's already in the pantry.

The Korean grandmother visiting Sarah Chen for ten days. The PURPOSE event records the visit with `kind='arrival'` and `source='manual'` because Sarah typed it in — *Grandma Park arrives Friday, leaves second Sunday* — and the affected_members_numbers carries an arrival entry for the grandmother's transient guest profile. The cuisine-breadth capability we'll walk in Episode Eleven lights up: the meal-plan grammar expands to include Korean breakfast porridges, kimchi-jjigae for dinner Wednesday, a Korean shopping list with the specialty ingredients the home pantry doesn't have, and the home channel cadence law shifts to accommodate a guest who's awake earlier than Sarah is — Grandma's coffee starts at five-forty in the morning, the kitchen Sonos cue defers to seven.

**REID:** And the cross-coupling.

**KEVEN:** The cross-coupling is between Lane Two/Seven — the Flux lane — and Lane Nine, the Recipe lane. *The Flux event sets context; the Recipe engine consumes context.* The two lanes communicate through the Cue Bus that Episode Six built and Episode Seven extended. A Flux event transitioning to `active` emits an event on the Cue Bus; the Recipe engine subscribes; the meal-plan grammar adjusts for the window. The same Cue Bus that carries fulfillment-status events from Episode Seven carries Flux-lifecycle events. *One bus; many subscribers; the substrate is uniform.*

This is also where the cabin StayLot pattern comes in. Marcus's cabin from the cold open is a StayLot — a vacation-rental-style delivery lot with `stay_start_date` and `stay_end_date` and a delivery target. When Sarah's `partial_absence` Flux event activates, the cabin StayLot's delivery schedule fills the gap — the kid-coded groceries the kids would have consumed at home get delivered to the trailhead pickup point near the cabin instead. *The home-side effect is Flux pause; the destination-side effect is StayLot delivery.* Same trace_id, two lots, one coordinated experience. Completing the Flux event auto-completes the StayLot; the architecture closes both halves of the loop.

**REID:** And the EventLot.

**KEVEN:** And the EventLot. The Thanksgiving Flux event — `kind='event'`, `start_date` is the Thursday, `end_date` is the Sunday — instantiates an EventLot for the cooking. The EventLot links the recipes, seeds the shopping list, tracks consumption against the event. *The Flux event is the household-side abstraction; the EventLot is the operational-side abstraction.* Different lifecycles; one user-visible flow. The customer sees one Thanksgiving in the app; the architecture has two coordinated objects underneath.

### Azure-native deployment and the privacy substrate

**REID:** Section seven. The deployment story. And the bridge into Episode Twelve, the privacy episode.

**KEVEN:** Walk the deployment. `orchestrator/flux.py` runs in `ca-visionkit-orchestrator` — the orchestrator Container App in East US Two. The same Container App that hosts the agent fleet, the cue bus, the fulfillment plug-in tier from Episode Seven. The Flux module is in-process with the rest of the orchestrator; it does not need its own service; the right unit of isolation is the class.

The SQL state lives in the same Postgres instance the rest of the demo backend uses. `db/04_flux_events.sql` is idempotent — safe to re-run — and the schema is in place ready for the `DEMO_PG_CONN` flip from in-memory to Postgres-backed storage. The `flux_events` and `flux_patterns` tables, the back-pointer on `lots`, the back-pointer on `auto_orders` for resume-after-pause, the three indexes for the common query patterns — they're all in the SQL.

The Flux lifecycle events flow on the Cue Bus — the same one Episode Six built for Sonos and Episode Seven extended for fulfillment. A Flux event transitioning from `proposed` to `approved` emits a cue-bus event; a Flux event transitioning from `approved` to `active` emits another; subscribers in `auto_orders.py`, `meal_planner.py`, and `concierge.py` consume them and apply their side of the effect bundle. *One bus; many subscribers; the substrate is the same for fulfillment and for composition.*

The audit chain is the same hash-chained, identity-stamped LedgerRow from Episode Two. Every Flux state transition writes a row. The trace_id propagates from the detection through the proposal through the approval through every downstream effect. The eight-hop replay from Episode Two extends naturally — for a Flux event, the hops are *signal-detected, classified, proposed, surfaced, approved, activated, effects-fired, completed.* Same shape; same chain; same replayability.

The live architecture page — *`https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture`* — shows the orchestrator Container App, the Postgres instance, the Cue Bus, the LedgerRow ingest. The Flux substrate is not separately diagrammed because the Flux substrate runs inside the orchestrator Container App; the deployment topology Episode Two and Episode Five walked already carries it. Open the URL on a client call; the Flux substrate is already on the screen.

**REID:** And the bridge into Privacy.

**KEVEN:** The bridge is the cleanest part. *Flux events are household-private.* The composition data — who's in the household, who's away this week, who moved in last month, who's at the cabin on autumn weekends — *never leaves the home tenant.* The aggregations are local. The cloud sees the lifecycle states — `approved`, `active`, `completed` — but the cloud does not see the underlying observations. The geofence ping that bloomed at the home zone on Friday at four does not propagate to a cloud service for analysis. The classifier that decided the cabin pattern was repeating ran inside the orchestrator's transient reasoning and *never wrote the observation out.* What writes out is the *proposed event* — *kid pattern detected, propose partial_absence* — and the proposed event carries only the inferred lifecycle state, not the path that led to it.

This is Privacy at the substrate. *The household composition is the household's.* The cloud is what cloud is for — productized capability density, governed gold, model portability. The cloud is *not* what cloud is not for — exfiltrating the customer's living-pattern observations to a service that the customer didn't agree to. Episode Twelve walks this in full — the consent surface, the geofence retention policy, the per-member tracking consent flow, the DPIA. Episode Ten plants the substrate the privacy story rests on.

**REID:** And the architectural line.

**KEVEN:** *Composition data stays in the household tenant; the cloud sees what cloud needs to see; nothing more.* That is the line. The substrate is privacy-by-design because the substrate is *household-scoped by design.* The shape of the data and the shape of the consent are the same shape. Episode Twelve will name that explicitly. Episode Ten plants the substrate that makes the line defensible.

---

### A reading I want to do

**REID:** Vaughn Vernon. *Implementing Domain-Driven Design.* The event-sourcing chapter — chapter eight in the original, the one that walks the move from a snapshot-of-state model to an event-log model. Or alternatively Greg Young's talk *Event Sourcing versus CRUD* — he gave it at QCon in 2010 and the talk has aged better than most of what came out of that decade. Either reading lands the same architectural point: *the current state of an aggregate is a fold over an event log, not a row in a table.* That is the Flux substrate's foundational move. The household is not `customer.household_size = 4`; the household is the fold of every approved Flux event from onboarding through today.

The reading is worth doing because the Flux design carries the event-sourcing pattern *without naming it event-sourcing.* The design document calls it *lifecycle* and *state machine* and *fold,* but the words *event sourcing* don't appear in the document's prose. Vernon and Young are the canonical sources for the pattern; reading either of them after working through the Flux design clarifies why the choice was made and what the choice buys. *The household composition becomes queryable across time, replayable, auditable, undoable.* All four of those properties are gifts of the event-sourcing pattern, not gifts of any specific implementation. The seller who has read Vernon can name the pattern in the room when an architect asks *how does this handle the divorce-then-remarriage case?* — the answer is *we replay the event log up to the new approval; the prior approved events are still there, marked superseded or completed, and the audit chain carries the full transition.*

**KEVEN:** And the second reading I'd pair with it — Pat Helland's *Memories, Guesses, and Apologies.* Helland's argument is that in any distributed system the records you keep are some mix of *memories* — what happened — *guesses* — what we inferred — and *apologies* — what we got wrong and had to walk back. Flux has all three. The `active` events are memories. The `proposed` events are guesses. The `dismissed` and `superseded` events are apologies, in the architectural sense — the system inferred something that turned out to be wrong or out-of-date, and the record of the walk-back is itself part of the chain. Pairing Vernon with Helland gives the engineer both the *what* and the *why* of the substrate.

---

### One disagreement

**REID:** Here's where I push. PERMANENT_DEPARTURE as HITL-only. I get the architectural ethic. I get the asymmetry of the false-positive cost. But the consequence of the design choice is *real life-events are caught months late.* The grandfather who passed away in March — the system keeps ordering his coffee until June. The auto-replenish stays at the old cadence. The brand looks oblivious. *Stale auto-replenish on a deceased customer's coffee is its own kind of harm.* My position: the system *should* be able to infer permanent_departure with very high confidence — say, ninety-five percent or above on a multi-signal fusion — and surface it as a *proposed* event with a confirmation prompt. Not auto-approve. Surface for human confirmation. The same HITL gate. But surfaced, not silent. Otherwise the system runs stale.

**KEVEN:** I push back. The asymmetry isn't where you're placing it. *The cost of being right ninety-nine percent of the time is the one percent case ruining the brand.* The right ninety-nine cases get a slightly faster system response — the deceased grandfather's coffee stops three weeks earlier than it would have if Sarah had called support herself. The wrong one case is the *grief amplifier.* The system shows Sarah a notification that reads *we noticed your husband hasn't scanned in a while; should we update the household?* and Sarah is widowed three months in and the algorithm just wrote the obituary one more time. That experience is *unrecoverable.* The brand harm is durable; the relationship does not come back from it. The expected value of the inference, even at ninety-five-percent confidence, does not clear the unbounded downside.

**REID:** And here is where I press harder. The unbounded-downside framing is itself a choice. The customer can opt out of the inference. The customer can say at onboarding *please do not ever surface life-event inferences in my Preference Center.* If she opts in, she has explicitly agreed to the surface — the surface is no longer a surprise; the surface is something she asked for. The architectural absolutism is *the system shall never infer this* — the calibrated position is *the system shall never infer this without explicit, opt-in, ongoing consent to the inference.* Different. The first one ships stale-by-design; the second one ships fresh-by-default-for-consenting-users.

**KEVEN:** And here I converge partway. *The system surfaces a permanent_departure as a `proposed` event when the pattern is clear and the customer has explicitly opted into life-event inference at onboarding.* The proposed event renders in the Preference Center with extreme tact — Maya Patel's copy guidelines from the Flux design's Section Four-Point-Five — *we noticed a change in scan patterns over the last several months; some customers find it helpful to update their household roster after a major life event; you can review options here when you're ready.* No naming the person. No celebratory framing. No urgent prompt. Just a gentle, dismissible, persistent affordance the customer can act on when they're ready. The active state never fires from inference. The active state fires only on explicit customer or operator approval. *Proposed yes; active no.*

**REID:** Converged. The softer pattern. The opt-in inference produces a `proposed` event with tactful copy; the `proposed` event never auto-activates; the customer's explicit approval is the only path to `active`. The architecture's ethic holds — the action stays HITL — but the *surface* respects that the customer may be running stale and may want a gentle reminder that the option to update exists.

**KEVEN:** And the implementation detail that closes it. The opt-in lives on the customer profile — `life_event_inference: true | false` — defaulted to *false.* The customer turns it on at onboarding if they want it; the customer can turn it off at any time. The geriatric-care setting Diana Park's profile has from Episode Eight defaults the parent's life-event-inference toggle to *false* and surfaces a separate conversation about caregiver-side configuration. The substrate respects the calibration; the architecture stays consistent.

---

### What to carry forward

The three durable takeaways.

1. **Composition is a sibling of lots, not a property.** The household is event-sourced. Every Flux event is a row. The current household state is a fold over the event log. A naive design puts household_size on the customer profile and updates the column; CFMP puts the change on the event log and lets the customer state be the replay. This is the architectural move that lets the substrate carry multi-location, multi-season, multi-life-stage households without falling apart. The seller carries this — *the household is not a column; the household is a fold.*

2. **HITL gating before effects is the architectural ethic.** Effects fire on `active`, never on `proposed`. The `proposed` state is where the agent says what it would do *without doing it.* The customer's tap is the only path from intent to engagement. The PERMANENT_DEPARTURE family extends this further — the system refuses to infer the family at all, because the false-positive cost is unbounded. *Architectural ethic enforced by architectural absence.* The seller carries this — *the agent says what it would do without doing it; the customer holds the spending key.*

3. **Flux is privacy at the substrate.** Composition data stays in the household tenant. The cloud sees lifecycle states; the cloud does not see the underlying observations. The geofence pings and the seasonal-pattern detections live in the orchestrator's transient reasoning and never write out as identifiable household-living data. This is the bridge into Episode Twelve — the privacy episode — and it is the line that makes the privacy claim defensible. *The household composition is the household's.* The seller carries this — *the cloud is what cloud is for; the household is what household is for; the line between them is the substrate's privacy story.*

---

## Further reading

- **Source docs**
  - `CFMP-Mobile-Flux-Design.md` — the design document Episode Ten draws from, in full
  - `db/04_flux_events.sql` — the `flux_events` and `flux_patterns` schema, the back-pointer on `lots`, the back-pointer on `auto_orders`, the three indexes, the touch-updated-at triggers
  - `orchestrator/flux.py` — the in-memory CRUD plus lifecycle state machine, the public API surface, the 7-kind / 5-family naming, the lifecycle invariants in the header comment
  - `CFMP-Mobile-Lots-Expert-Focus.md` — Section 11 (StayLot) and Section 1.1 (EventLot), the two lot kinds the Flux substrate couples to
  - `CFMP-Mobile-Identity-Onboarding.md` — the household roster the Flux events fold over
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture`
- **Microsoft Learn**
  - Azure Container Apps revisions and scaling — `https://learn.microsoft.com/azure/container-apps/`
  - Postgres on Azure — `https://learn.microsoft.com/azure/postgresql/`
  - Azure Container Apps observability and the trace_id propagation pattern — `https://learn.microsoft.com/azure/container-apps/observability`
- **Industry / research**
  - Vaughn Vernon, *Implementing Domain-Driven Design* — the event-sourcing chapter; the canonical reference for the fold-over-event-log pattern Flux applies to household state
  - Greg Young, *Event Sourcing versus CRUD* — the QCon 2010 talk that introduced the pattern to a generation of engineers; still the cleanest forty-five minutes on why the pattern matters
  - Pat Helland, *Memories, Guesses, and Apologies* — the framing that maps cleanly onto the Flux state machine; `active` events are memories, `proposed` events are guesses, `dismissed` and `superseded` events are apologies
  - Dr. Maya Patel et al., protocols for major-life-event support in patient-facing applications — the tact guidelines that govern the `permanent_departure` sensitivity_mode toggle

---

*Episode Ten is the appended documentary deep-dive on the household-composition substrate. Episode Eleven walks the Recipe capability that couples to PURPOSE events. Episode Twelve walks Privacy at the substrate.*
