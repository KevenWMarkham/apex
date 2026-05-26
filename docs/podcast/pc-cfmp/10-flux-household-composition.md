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

**KEVEN:** Start with the customer reality the noun has to hold. *Most grocery apps think the household is a number on a profile.* `Household_size = 4.` That works for the first six months Sarah has the app. Then her older kid leaves for college for nine months, comes back for the summer, leaves again. Marcus's kids visit the cabin three weekends in a row. The Korean grandmother is here for ten days. Sarah's mother is recovering from surgery and the family is taking turns staying with her. *The number-on-a-profile model can't hold any of that.* The household isn't a number. *The household is a sequence of lives intersecting over time.* Flux is the substrate that recognizes that.

**REID:** And the working definition.

**KEVEN:** A Flux event is *a tracked, time-bounded change in who's in the household — or who's away — that triggers a coordinated, customer-approved set of effects.* Read that twice; every word is load-bearing. *Tracked* — every event is on the record. *Time-bounded* — every event has a start; most have an end. *Change in who's in or who's away* — either the roster changed or somebody on the roster isn't here this week. *Customer-approved* — the customer says yes before anything happens. *Coordinated effects* — the auto-replenish, the meal plan, the wilted-romaine warnings, the cues all move together because they read from the same event.

**REID:** And the design move — composition is a first-class sibling of the lot, not a property of either the lot or the customer.

**KEVEN:** Sibling. Not a column. *That's the move.* The current household state is a *fold* over an event log — start with the onboarding roster, replay every approved Flux event in chronological order, the result is what's true today. *The household isn't a row in a table; the household is the replay.*

**REID:** And why this matters to the customer.

**KEVEN:** Three reasons. *One — a person isn't a property of a lot; they're an actor across many lots.* Sarah is in the meal-plan Tuesday, the pickup Wednesday, the pantry Thursday when she scans the gochujang. *The person traverses lots; the lot doesn't own the person.* *Two — the household isn't a property of a customer; it's a composition that changes over time.* The household at onboarding is not the household three years later. *Three — composition events have effects that themselves last over time.* A vacation pause has a start and an end; a new child has a start and no end. *The event has to outlive any single lot it touches.*

**REID:** And the audit consequence.

**KEVEN:** *Every change in the household is event-sourced; every transition writes a record; the tracking thread propagates from detection through proposal through approval through every effect.* When Sarah, six weeks later, asks *why did the auto-replenish pause from September 26 to October 17* — the answer is one query. *The household is event-sourced; the audit chain is the receipt.*

### The seven kinds across five families

**REID:** Walk the seven kinds. The customer moments first; the architectural distinction tucks under.

**KEVEN:** Five families, seven kinds. Each family clusters the *shape of the effects.* An absence family event pauses things. An arrival family event un-pauses things. A departure family event archives things. A purpose family event spikes things. A place family event re-baselines things. *The family names the shape of the effect.*

**REID:** Walk them.

**KEVEN:** *Absence — the household shrinks for a while.* Two kinds. *Vacation* — Sarah and the kids and the dog all leave Friday for Tahoe; the home is empty for ten days. The system uses up the romaine before departure, pauses the milk delivery for the week she's gone, lets the kitchen speaker stay quiet because nobody is home. *Partial absence* — the cabin pattern from the cold open. Marcus's kids visit the cabin three weekends in a row. The home cadence reduces for the kid-coded items — *the snack budget, the milk volume, the kid-specific yogurt* — but the adult items continue. The system noticed the pattern after three repeating weekends and surfaced it to Sarah. Sarah approved. The math reduced the relevant items; the rest continued.

*Arrival — the household grows.* Two kinds. *A visit* — a guest is here, the college kid is home for the summer, the Korean grandmother is here for ten days. The system briefly expands the household, restores the visitor's preferences if she's been here before, adds her dietary needs to the meal-plan grammar, scales the snack budget up. *Permanent arrival* — a new child, a partner moving in, an aging parent moving in for good. Same shape as a visit, with no end date. *The roster updates permanently.*

*Departure — the household shrinks permanently.* One kind. *Permanent departure* — the customer says, deliberately, in the Preference Center, that the roster has changed. *The system refuses to ever detect this on its own.* A child off to college and not coming back. A divorce. A death. An estrangement. The reasons for the refusal we'll walk in the next section.

*Purpose — the household is the same size but the demand spikes.* One kind. *Event* — Thanksgiving, the Super Bowl gathering, the dinner party Saturday night. *The household is the same household every other day.* What changes is the demand for one window. The system hands one shopping suggestion sized to the guest count, accounting for what's already in the pantry, with the recipes the host indicated.

*Place — the household relocates.* One kind. *Move* — Sarah's family moves to a new address. New closest stores, new pickup windows, new aisle layouts. *The system re-baselines everything against the new home.* The audit chain carries both addresses so the regulator who asks *where did this happen* in six months can read both in the record.

**REID:** Seven kinds. Five families. *Each family is the shape of the effect; each kind is one row in the event log.* A small surface with large semantic reach — every household-composition pattern the design surfaced across two years of customer research lands on one of these seven. *That's the test of a good substrate.*

**KEVEN:** Said cleanly. Seven kinds, all the household's life-shapes covered, customer says yes before anything happens.

### Detected, proposed, approved, active — the lifecycle

**REID:** The lifecycle. Four states. Walk it from the top.

**KEVEN:** *Detected.* The signal arrived. The system saw something — a calendar entry titled *vacation*, the phones leaving the home zone for forty-eight hours, the cabin pattern repeating for the third weekend, Sarah saying something in voice that parsed as an intent. *The system writes a record of what it saw and scores its confidence.* No effects. No notification. The customer doesn't see anything yet.

*Proposed.* The system has decided the signal is worth surfacing. *Sarah sees a soft moment in the Preference Center or on her home screen.* *Going to Tahoe Friday? I can pause auto-orders and suggest a use-it-up meal plan.* The proposal shows the *effect bundle* — the concrete things the system would do — alongside the question. *Sarah can see exactly what would change before she approves.* Her options — *approve, dismiss, customize, not now.*

*Approved.* Sarah tapped approve. The record is written. The effect bundle is committed. *No effects have fired yet.* The event sits in *approved* until its start date arrives. A vacation approved Tuesday for a Friday departure waits in *approved* from Tuesday afternoon through Friday morning. *The meal-plan adjusts because the meal-plan reads ahead — that's a planning effect, not a runtime effect — but the auto-orders don't pause until the start date passes.*

*Active.* The start date arrives. The state flips from *approved* to *active.* *This is the moment the runtime effects fire.* The auto-orders pause. The cadence multiplier engages. The kitchen speaker's cadence shifts. The home channel goes quiet. *Effects fire only on active, never on proposed.* That invariant is the architectural defense against false positives.

**REID:** And the other two states.

**KEVEN:** *Dismissed.* Sarah said no. The system remembers. If the same pattern surfaces again, the system raises its threshold — *the customer said no last time.* *Superseded.* A newer, more specific event replaces an older general one. Sarah approves a vacation for June 10-17 for the whole family; two days later she approves a partial-absence for the spouse traveling June 12-14. *The system asks her — merge or override? — and the older event is marked superseded.* *Newer specific supersedes older general.*

**REID:** And here I press, customer-grounded. *Why an intermediate "proposed" state at all?* Why not have the system show Sarah what it would do, and she taps yes or doesn't?

**KEVEN:** Because *the proposed state is where the system says what it would do without doing it.* That isn't a UI distinction; it's an architectural one. In a two-state model, the moment the system decides the signal is worth acting on, Sarah's tap is *the only thing between the signal and the effect.* A misfired tap, a misread notification, a child grabbing the phone — and the effect fires. *In a four-state model, there's a published, persisted, queryable artifact between detection and effect.* The proposal is something Sarah can see, the operator can see, the auditor can see, and *Sarah can un-tap* — she can dismiss a proposal already in her Preference Center; she can change the window before approving; she can ask the system to explain the effect bundle.

The four states also separate *intent* from *time.* Approved means Sarah consented to the effect; active means time has caught up to the start date. *The lifecycle separates the agreement from the engagement.* Two states would conflate them.

**REID:** And the cold-open walks one full lifecycle.

**KEVEN:** Marcus's partial absence. *Detected* — the cabin pattern repeats three weekends; the system flags it; the confidence threshold is crossed. *Proposed* — the system surfaces in Sarah's Preference Center with the concrete effect bundle. *Approved* — Sarah taps yes at her kitchen island four hundred and seventy miles south. *Active* — Friday's start date arrives; the runtime fires; the home cadence reduces; the cabin delivery handles the kid groceries at the trailhead. *Four states. One tracking thread. Eight hops. One audit chain.*

### Permanent departure — the kind the system refuses to infer

**REID:** The hard one. The family of one. The kind the design refuses to ever auto-detect. Walk why.

**KEVEN:** Three reasons. *One — the harm of a false positive is unbounded.* A false-positive vacation is annoying; Sarah gets a notification, she says no, the system moves on. A false-positive arrival is annoying; the system suggests more snacks, she says no thanks. *A false-positive permanent departure is grief amplification at scale.* The system says *we noticed Sarah hasn't scanned in a while; should we remove her from your household?* And Sarah's spouse — three months widowed — reads it as the obituary the algorithm just wrote. The brand has done a kind of harm that no amount of accuracy in the ninety-nine percent of right cases makes up for. *The upside is we detected a life event slightly faster. The downside is grief amplification.* No threshold exists where the expected value clears.

*Two — the cases this kind covers cluster exactly where human judgment is non-negotiable.* A grandparent passes away. A divorce. A child off to college and not coming back. An estrangement. A custody change. Each is a moment of *intentional, often painful decision.* The right experience is the customer arriving at the Preference Center on their own time, on their own terms, and saying *please update the roster.* The wrong experience is the system arriving at the decision first.

*Three — the operational reality.* The signal that would have to be inferred is *absence of presence.* A person who hasn't scanned in N days. *The signal is noisy in every direction.* The college kid hasn't scanned because she lost her phone for two weeks. The spouse hasn't scanned because he's depressed and not cooking. The grandparent hasn't scanned because she's in the hospital recovering from a fall. *Absence of presence is not departure.* The system cannot honestly tell them apart. The design recognizes this and refuses to try.

**REID:** And the operator-initiated path.

**KEVEN:** *Operator-initiated.* A customer calls support. The customer says *my husband passed away.* The support agent has training, a script, a compassion protocol — written with input from a family-systems therapist on the design team. The agent confirms the request, the customer's identity, the action in plain language, and writes the event with the customer's chosen sensitivity mode — *neutral, celebration, or mourning.* The default is neutral. The mourning mode is a hard mute on every nudge that would reference the deceased. *The kitchen speaker never says the name again. The system goes quiet.*

**REID:** And the customer-initiated path.

**KEVEN:** Preference Center → Household → Remove member. A deliberate, multi-step confirmation flow. *This will permanently update your household roster. Continue?* The second screen offers the sensitivity mode with copy that names what each mode does without judgment. *The system never asked the customer to make this decision; the customer arrived at it on their own.*

**REID:** And the architectural ethic showing up.

**KEVEN:** *The design refuses to optimize for the metric it cannot honestly measure.* That's the line. The test isn't *the inference is accurate.* The test is *there is no inference path.* *The architecture defends the boundary by not having a code path that crosses it.* If the code path doesn't exist, the misfire cannot happen. *Architectural ethic enforced by architectural absence.*

### The move — the kind that tests every other capability

**REID:** The move. The hard test. *Does the system follow the household when she moves?*

**KEVEN:** A move changes Sarah's relationship with every part of the system at once. *The customer profile* — the addresses list gains a new primary; the old address moves to secondary or archive depending on Sarah's choice. *The auto-replenish* — the cadence math doesn't change (the household is the same size) but the *target* changes; the closest store re-resolves, the pickup window viability re-resolves, the produce-consumption velocity may shift because Sarah's new neighborhood walks differently. *The home channel* — if Sarah took the speaker with her, the speaker identifier carries; if she got new speakers, the home channel re-registers. *The retailer plug-ins* — a retailer that delivered to the old address may not deliver to the new one. *The system flags this in the proposed move event's effect bundle so Sarah sees it before she commits.* *The audit chain* — carries old and new addresses in the same tracking thread, so the regulator who asks *where did this happen* in six months can read both addresses.

**REID:** And the architectural test.

**KEVEN:** *Does the system follow the household, or does it stay stuck at the old address?* A naive system stays stuck — the auto-orders keep delivering to the old place, the meal-plan keeps recommending recipes for the old climate, the speaker keeps trying to reach a device that's no longer there. *A correct system follows.* The move event is the *handle* that triggers the follow. Every downstream capability subscribes to the event; every downstream capability re-baselines on the start date. *The cascade is wide; the trigger is one row.* The customer is the better for it — because moving is hard enough without your grocery system being stuck at the old address.

### Purpose — guests, holidays, and the recipe coupling

**REID:** The family that touches recipes. The Lunar New Year visit. Thanksgiving guests. The Korean grandmother for ten days. Walk the coupling.

**KEVEN:** Picture Sarah's house with the Korean grandmother arriving Friday. *The household is the same household every other day of the year.* What changes is the meal-plan window for those ten days. Sarah types it in — *Grandma Park arrives Friday, leaves second Sunday.* The system records the visit. The cuisine breadth lights up — *the meal-plan grammar expands to include Korean breakfast porridges, kimchi-jjigae for dinner Wednesday, a Korean shopping list with the specialty ingredients the home pantry doesn't have.* *The kitchen speaker's cadence shifts to accommodate a guest who's awake earlier than Sarah is — Grandma's coffee starts at five-forty in the morning, the speaker defers to seven.*

**REID:** And the cross-coupling.

**KEVEN:** *The Flux event sets context; the recipe engine consumes context.* The two communicate through the cue bus from Episode Six. A Flux event becoming active emits a moment on the bus; the recipe engine subscribes; the meal-plan grammar adjusts for the window. *The same bus that carries fulfillment-status events from Episode Seven carries household-composition events.* One bus; many subscribers; the substrate is uniform.

This is also where Marcus's cabin from the cold open comes in. *Marcus's cabin is a stay-trip lot.* When Sarah's partial-absence event activates, the cabin lot's delivery schedule fills the gap — *the kid-coded groceries the kids would have consumed at home get delivered to the trailhead pickup point near the cabin instead.* The home-side effect is *pause*. The destination-side effect is *deliver.* Same tracking thread, two lots, one coordinated experience.

**REID:** And the event lot.

**KEVEN:** Same pattern for Thanksgiving. The Flux event records the household-side change; the event lot records the operational-side cooking — recipes, shopping list, consumption tracking. *Sarah sees one Thanksgiving in the app; the architecture has two coordinated objects underneath.*

### Azure-native deployment and the privacy substrate

**REID:** The deployment, and the bridge into Episode Twelve.

**KEVEN:** The substrate runs in the existing agent fleet's home. *No new container service. No new database. No new infrastructure box.* The Flux logic is in-process with the rest of the orchestrator; the right unit of isolation is the class. The state lives in the same database the rest of the system uses. The lifecycle events flow on the same cue bus the speaker channel and the fulfillment tier already use. *One bus; many subscribers; the substrate is uniform.*

The audit chain is the same hash-chained, identity-stamped record from Episode Two. Every state transition writes a row. The tracking thread propagates from detection through proposal through approval through every effect. *Same shape; same chain; same replayability.* The architecture page from Episode Two and Episode Five already carries the substrate; *open the URL on a client call and the Flux substrate is already on the screen.*

**REID:** And the bridge into privacy.

**KEVEN:** *Flux events are household-private.* The composition data — who's in the household, who's away this week, who moved in last month, who's at the cabin on autumn weekends — *never leaves the home tenant.* The aggregations are local. *The cloud sees the lifecycle states; the cloud does not see the underlying observations.* The phone-location ping that bloomed at the home zone on Friday at four doesn't propagate to a cloud service for analysis. The pattern-recognizer that decided the cabin pattern was repeating ran inside the orchestrator's transient reasoning and *never wrote the observation out.* What writes out is *the proposed event* — *kid pattern detected, propose partial absence* — and the proposed event carries only the inferred lifecycle state, not the path that led to it.

This is privacy at the substrate. *The household composition is the household's.* The cloud is what cloud is for — productized capability density, governed gold, model portability. *The cloud is not what cloud is not for — exfiltrating the customer's living-pattern observations to a service the customer didn't agree to.* Episode Twelve walks this in full — the consent surface, the geofence retention policy, the per-member tracking consent flow.

**REID:** And the architectural line.

**KEVEN:** *Composition data stays in the household tenant; the cloud sees what cloud needs to see; nothing more.* That's the line. *The substrate is privacy-by-design because the substrate is household-scoped by design.* The shape of the data and the shape of the consent are the same shape. Episode Twelve names that explicitly. Episode Ten plants the substrate that makes the line defensible.

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

**KEVEN:** Three things into Episode Eleven. Each one a thing a non-technical leader can carry into a Monday meeting.

**KEVEN:** *One — the household isn't a column, the household is a fold.* The household at onboarding is not the household three years later. *The number on a profile can't hold the kids visiting the cabin, the college kid home for the summer, the parent moving in, the move across the country.* The current household state is the replay of every approved change-event from onboarding through today. *That's the architectural move that lets the substrate carry every multi-location, multi-season, multi-life-stage household without falling apart.* The seller carries the line — *the household is not a column; the household is a fold.*

**KEVEN:** *Two — the system says what it would do without doing it.* Effects fire only when Sarah taps yes, and then only when time catches up to the start date. *The customer holds the spending key.* The system refuses to ever auto-infer a permanent departure — because *the false-positive cost is grief amplification, and no accuracy threshold clears that downside.* *Architectural ethic enforced by architectural absence.* The seller carries the line — *the system says what it would do without doing it; the customer holds the spending key.*

**KEVEN:** *Three — composition data is the household's.* The cloud sees the lifecycle states — approved, active, completed. The cloud does *not* see the underlying observations. The phone-location pings and the seasonal-pattern detections live in transient reasoning and never write out as identifiable household-living data. *This is the bridge into Episode Twelve, and it's the line that makes the privacy claim defensible.* The customer's household composition is the customer's. The cloud is what cloud is for; the household is what household is for. *The line between them is the substrate's privacy story.* Carry that.

**REID:** Composition is a fold, not a column. System says without doing. Composition is the household's. Three carries. Into Episode Eleven.

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
