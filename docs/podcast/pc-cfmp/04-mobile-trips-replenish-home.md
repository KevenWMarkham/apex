# Episode 04 · Mobile · Trips, Replenish, and the Home Channel

**Episode 04 · Mobile · Trips, Replenish, and the home channel** — Thursday evening, Sarah opens the fridge, the romaine is wilted in the back of the crisper, and the kids eat cereal again. The Sunday-morning version of CFMP saw the failure coming; Sarah didn't. We walk the trip life-cycle end to end, open the auto-replenish pantry model with the human-in-the-loop, name the home channel and why it matters when the customer never opens the app, and defend smart defaults over preference menus. We close on senior-mode accessibility hooks as the design's quality test.

**Builds on:** the show bible (00-show-bible-and-format) · Episode 01 (Sarah's Day) · Episode 02 (Agent fleet & audit chain) · Episode 03 (Mobile · SCAN & LOT) · CFMP Mobile Design Document §3 (Journey maps), §6 (Key design elements), §7 (Use cases) · CFMP Mobile Preferences Expert Focus · CFMP Mobile UI Revamp
**Run time:** ≈ 40 minutes target
**Last updated:** 2026-05-25

---

## Cold Open

[Sound: a suburban kitchen at six-forty-seven on a Thursday evening. The hum of the refrigerator compressor. The crinkle of a chip bag being closed off-mic. A child on the floor in the next room asking, in the bored sing-song of an eight-year-old, what's for dinner. The thunk of the refrigerator door opening. The cold whoosh of the crisper drawer rolling out. A small audible exhale.]

It is six-forty-seven on a Thursday evening, and Sarah Chen has just opened the bottom drawer of her fridge to pull out the romaine she bought on Sunday for tonight's dinner. The romaine is in the back of the crisper, where the romaine always ends up by Wednesday — behind the carrots she uses every other day and the bell peppers she rotated forward on Tuesday because the kid likes them in his school lunch. She pulls it out. The outer leaves are limp; the inner ones are translucent at the edges. It is not garbage; it is not salad. It is the in-between state that grocery stores call *salvageable* and parents on a Thursday evening call *not enough time.* She holds the bag for a second over the sink, considering. She drops it in the bin.

Four dollars. The chicken she had planned to thinly slice over those greens is in the fridge in a marinade that is now without a vehicle. She does not have the bandwidth to pivot at six-forty-seven on a school night. She stands at the counter for ten seconds looking at nothing. She opens the freezer. She pulls out tater tots from the last time she gave up. She sets the oven to four-twenty-five. She announces, with the false brightness of a parent already negotiating with herself about how this counts, that tonight is *breakfast for dinner.* The kids cheer. They will eat cereal and toaster waffles and the tater tots she has not yet decided whether to admit she is using as protein.

The Sunday-morning version of CFMP — the one with the agent fleet and the lot model and the audit chain — predicted this. The Replenish specialist noticed, four shopping cycles in a row, that romaine in Sarah's household never lasts past Wednesday. On Sunday night the Concierge specialist composed a moment — *the romaine you just bought is unlikely to last past Wednesday; want me to substitute napa cabbage in Thursday's meal, and order the romaine in a smaller pack on the next pickup?* The moment was sized for the kitchen Sonos speaker. It rendered at five-forty-two on a Sunday afternoon, while Sarah was making coffee for an early Monday and her phone was on the bedroom dresser. She did not hear it. The cue completed; the LedgerRow sealed; the moment moved on. By the time Sarah next opened her phone — Monday morning, dropping the kids off — the moment had aged into the *missed* state and was no longer surfaced as a primary action.

The wilted romaine is what the design fixes, not what the design assumes away. The Sunday-morning CFMP did see it coming. It also missed the channel Sarah was reachable on. Both halves of that sentence are the design.

[Sound: a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start there. Six-forty-seven on a Thursday. The bag of romaine over the sink. The Sunday cue that played to an empty kitchen.

**REID:** Because both halves of the design get tested in that moment. The prediction was correct — the consumption signal saw the wilt coming four cycles in advance. The channel discipline picked the kitchen speaker. And it landed on a Sunday afternoon when Sarah was upstairs. The design saw the romaine; the design missed the moment. The episode is about both — what the design gets right with trips and replenish, and what the home channel exists to harden.

**KEVEN:** Welcome back to the CFMP Podcast. Episode Four. *Mobile · Trips, Replenish, and the home channel.* In Episode One we walked Sarah's week. In Episode Two we opened the substrate. In Episode Three we walked the surface — the lot model, the four archetypes, scan-first. Today we go a layer deeper. The Trip life-cycle in motion. Auto-Replenish as the lot the customer almost never opens. The home channel — what happens when the customer is not on the phone. And the UI revamp the Mobile team committed to on the back of the Preferences expert focus.

**REID:** Six sub-sections. Trip life-cycle. Auto-Replenish. The home channel. Preferences and the one-voice rule. The UI revamp. Senior mode and accessibility. Let's go.

---

## The conversation

### The trip life-cycle

**KEVEN:** Start with the Trip. Because the Trip is the canonical lot — the one Episode Three named as exercising *transition density* — and we did not walk it end to end as a customer experience. Today we walk it. Let's take Sarah's weekly meal-plan-to-table cycle — Journey Two from Mobile Section Three — because it touches every state the design commits to.

**REID:** Walk it.

**KEVEN:** Pre-trip. Sunday morning. Sarah opens the app. The camera viewport is the default; the Lots Strip across the top shows the active PantryLot — fourteen items, three of which expire Wednesday. She taps the Lots tab. The agent has already composed a seven-day meal plan that uses the three expiring items in the first three dinners. Sarah edits two of the meals and taps *shop this plan.* A PlanLot is born. Draft state. Members composed against the household's dietary policy, the active loyalty memberships, and the FEFO ordering — first-expire-first-out, so the pantry is used before the cart is filled. Sarah promotes the PlanLot to a CartLot, drops in the diapers she forgot, hits checkout with Apple Pay. The system splits the CartLot into a PickupLot for Saturday morning and a DeliveryLot for Tuesday — pickup for the perishables, delivery for the staples. Two children of one parent CartLot, parentage preserved, audit chain intact.

**REID:** That is the pre-trip. Then in-flight.

**KEVEN:** In-flight. The PickupLot transitions to in-flight on Friday evening, when the store's picker accepts it. The Lots Strip updates to say *Sat pickup · packed by 10:42* — a live timestamp the picker's scan stream emits. Mid-flight, a substitution: the brand of yogurt Sarah ordered is out of stock. The Trips specialist composes a substitution panel and pushes it to Sarah's phone — one-tap accept, one-tap reject, one-tap pick a different brand. Sarah taps accept while she is in a meeting; the substitution lands; the LedgerRow records it with parentage to the request row. Saturday morning, Sarah pulls into the pickup lane. The geofence on the Mobile triggers; the picker is notified; Sarah scans the pickup QR; the PickupLot transitions to settling.

**REID:** Settling.

**KEVEN:** Settling. Sarah pulls into her driveway at ten-thirty-two. The Mobile detects the home geofence. A PantryLot auto-spawns from the PickupLot — UC-73 — with each item carrying its provenance, its expected shelf life from the Catalog specialist, and its quantity from the receipt. The Trips specialist hands off to the Replenish specialist; the Concierge specialist starts the expiry-tracking clock. Sarah carries bags into the house. She does not open the app. The settling state runs without her. Tuesday morning, the DeliveryLot arrives — separate parentage chain, its own PantryLot auto-spawn, merged into the household PantryLot at the membership level. The week proceeds.

**REID:** And the trip *ends* where. Because most retailers count it ended at the *register* — the receipt fires, the loyalty points post, the dashboard ticks. Some count it at *delivery* — the BOPIS handoff is the close. The design's commitment is that the lot is *closed* only after the PantryLot has either fully consumed or been archived. That is a much longer window than most systems even measure. Defend it.

**KEVEN:** Defending it. The Trips specialist's job is not done at the receipt. The job is to know whether the trip *served the household* — whether the food got eaten, whether the substitutions were right, whether the items the system suggested were items the customer was glad to have. That information lives in the PantryLot's consumption telemetry. The receipt is a *transition*; the closure is a *judgment*. The lot is closed when its PantryLot items have been consumed — per-item check-off either explicit through UC-13 or inferred from re-purchase patterns — thrown out and recorded as waste, or carried forward into the next PantryLot. The audit row at close summarizes the trip's *fitness* — items ordered, delivered, consumed, wasted, substitutions accepted, substitutions rejected. That row is what feeds back into the Replenish specialist's next prediction. The loop closes at consumption, not at checkout.

**REID:** And the architectural consequence.

**KEVEN:** The trip lifetime is *days*, not minutes. The LedgerRow chain has to be intact across that lifetime. The trace identifier minted at the Sunday-morning PlanLot has to be reachable seven days later when the Concierge specialist reasons about whether to nudge the next plan. The architecture is taking the lot's word seriously as a *bounded set of intents over a window of time*. Not a transaction. A window.

**REID:** And the touchpoints across the three surfaces — Mobile, Portal, Sonos.

**KEVEN:** Three surfaces, one trip. *Mobile* — Sarah's surface end to end. *Portal* — the operator's. The picker sees the PickupLot at *packing* state; substitution requests originate at the Portal and surface on Mobile. *Sonos* — the ambient channel. The romaine reminder on a Wednesday evening when Sarah is making dinner. The pickup-window-confirmed cue on a Friday morning. The delivery-arrived announcement when the door sensor fires on a Tuesday. One trace identifier propagating across all three. *One trace, one query, one defense* — Episode Two's line.

**REID:** The trip ends at consumption, not at checkout. The architecture holds the lifetime because the lot holds the lifetime. Move to Replenish.

### Auto-Replenish

**KEVEN:** Auto-Replenish. If the Trip is the canonical lot, Auto-Replenish is the lot the customer *almost never opens.* The Trip is the foreground experience. Auto-Replenish is the *background* — the thing the system does so the customer does not have to think about it. The customer trust requirement is sharper.

**REID:** Start with the prediction.

**KEVEN:** The pantry model. The Replenish specialist — a `gpt-4.1-mini` with a tight toolkit — has access through the MCP boundary to three sources composed into a Gold view. *First* — the household's order history, six months of receipts with item-level frequency, quantity, and seasonality. *Second* — the active PantryLot, with each item's provenance and expected depletion. *Third* — the household's confirmed auto-orders. The standing list — *milk weekly, diapers monthly, the kid's cereal every other week.* The specialist composes those three into a prediction — which SKU, what quantity, what week. The prediction is *conservative*. The customer who bought milk Tuesday for the last six weeks is going to need milk Tuesday in week seven. The system does not try to be clever; it tries to be right.

**REID:** And conservatism is a design choice, not a hedge. Why.

**KEVEN:** Because the failure modes are asymmetric. *Over-ordering* costs Sarah money she did not authorize and wastes a gallon of milk. The trust loss is large; the recovery is hard. *Under-ordering* costs Sarah a single line on next week's grocery list. The trust loss is small; the recovery is immediate. So the specialist sticks to the established pattern as the prediction. The clever cases — the dinner-party prediction, the kid-growth-spurt cereal escalation, the seasonal-shift produce swap — are *suggested*, not *enrolled*. The customer's standing approval governs enrollment; the specialist's prediction governs the standing-approval candidate list.

**REID:** And the human-in-the-loop. This is the line the design has to walk most carefully.

**KEVEN:** *The design never auto-orders without the customer's standing approval.* Non-negotiable. The standing approval is the customer's commitment, captured at enrollment — *milk, weekly, this brand, this quantity, this channel, with a substitution policy.* The specialist composes the standing list into a *proposed weekly order* every Sunday morning. The customer has a *modification window* — typically twenty-four to forty-eight hours — to skip an item, change a quantity, add a one-off. After the window closes, the order commits. The line for the seller — *the system places orders the customer already said yes to; it never decides on the customer's behalf.* If a customer asks six weeks later *why did you order me four gallons of milk* — the audit row says *because you set milk-weekly six months ago, you did not skip in the modification window, and the standing approval committed.* The substrate from Episode Two is what makes the seller's claim defensible.

**REID:** And the savings argument. Because if auto-replenish does not pay back, the customer churns through the first quarter and the retention bet dies.

**KEVEN:** Three components. *Time* — the customer who used to spend forty-five minutes on a Sunday morning now spends five. Auto-replenish is what *holds* that metric across weeks two through fifty-two. *Money* — the standing approval lets the Replenish specialist time orders against loyalty memberships and active promotions; for a household spending six hundred dollars a month, that is single-digit-percent automatic savings the customer never had to clip a coupon for. *Waste* — the per-item quantity prediction is calibrated against the household's *consumption*, not their *purchase history.* The system does not just order what they bought; it orders what they ate. The cold open is the failure case the calibration exists to prevent.

**REID:** And this is where I press on privacy. What you described is a system that knows what Sarah eats — not just what she buys, but what she finishes, throws out, pivots away from. A richer model of a household's interior life than most retailers have ever held. Once it exists, it is a target. For the data broker. For the subpoena. The privacy concern is not paranoid; it is structural.

**KEVEN:** Conceded as structural. The design's answer is the *consent gradient* — the three-tier framework from Mobile Section Four-Seven. *Session-local observation* — the in-session re-rank that fades on tab close. *Persistent inference* — the inferred preferences that live in Postgres with a required transparency surface. *Material action* — the standing approval for an auto-order, which requires an explicit confirmation event that promotes the inferred preference to an enrolled commitment. The system can *observe* Sarah's consumption patterns without asking. The system cannot *enroll* her in an auto-order without an explicit confirmation. Episode Eight walks the gradient in full. We preview it here because it is the design's answer to the privacy concern.

**REID:** Preview the line.

**KEVEN:** *The customer's autonomy lives in the gap between persistent inference and material action.* The system can know; the system cannot act on what it knows without the customer's standing yes. Auto-Replenish is the case study. Every standing approval is an explicit yes. Every modification window is a chance to say no. Every audit row records the basis. The customer who wants to revoke the inference hits the kill switch and the inferred rows are deleted. *Observation is liberal. Action is conservative. The gap is where the customer lives.* That is Vargas's line; Episode Eight walks it.

**REID:** The Replenish lot is the lot the customer almost never opens, and the architecture is what makes that absence safe. Move to the home channel.

### The home channel

**KEVEN:** The home channel. Because Auto-Replenish lands on the substrate question — *how does the customer who never opens the app stay in the loop?* — and the answer is the channel. The kitchen-radio metaphor.

**REID:** Name it carefully.

**KEVEN:** The Sonos speaker in Sarah's kitchen is not a smart speaker in the *Alexa or Google Home* sense — a thing you address with a wake word. It is a *radio* in the older sense — a thing in the background, that occasionally has something to say, that you can listen to without engaging, that you can ignore without ceremony. The radio is *ambient*. The radio is *calm tech*. The radio does not ask for attention; it offers information when the information is timely, and stops talking when the information is delivered. The Concierge specialist's nudges on the Sonos are radio cues — fifteen-second utterances, calm voice, no follow-up question unless the customer initiates. The cold open's missed cue is exactly this shape. If Sarah is in the kitchen, she hears it and answers. If she is not, the cue completes, the row seals, the moment ages. The radio does not chase her.

**REID:** And the architectural commitment — voice as a *peer* channel, not a *secondary* channel.

**KEVEN:** Mobile and Sonos are *peers*, both consuming the same agent answers from the same orchestrator. The Concierge specialist composes a moment as a *structured intent* — kind, severity, content, suggested actions. The dispatcher routes the moment to the appropriate channel based on location, recent device activity, time of day, and moment kind. If Sarah is at home and the kitchen Sonos is active, the moment routes there. If Sarah is on the bus and the Mobile is engaged, it routes there. If both are plausible, it routes to both with a parallel fan-out the LedgerRow chain records as a single trace with two channel rows. The agent does not author a different message for each channel; the agent authors a *moment*, and the dispatcher renders it in the channel's voice. *One moment, two channels.* The customer experiences the system as one system, not two apps.

**REID:** And when the Mobile *is* the home channel. The customer who does not own a Sonos.

**KEVEN:** The design's commitment is that the ambient channel works on the Mobile speaker too — through the AirPlay-bridge fallback Episode Two named on the architecture page. The Mobile becomes the AirPlay bridge to a HomePod or an Apple TV when those are available; the Mobile is *itself* the speaker when nothing else is. The Concierge moment that would have played on the kitchen Sonos plays on the Mobile speaker instead. The dispatcher's channel decision factors in the device the customer is most likely to *hear*, not the device most likely to *look at*. The audit row carries the channel value — `sonos_cloud`, `mobile_airplay`, or `mobile_speaker`.

**REID:** And the retention argument.

**KEVEN:** The customer who opens the app every day is the design's easy retention. The customer who *does not* open the app daily is the design's hard retention — and the hard retention is the bigger population. The customer who used to open the retailer's loyalty app every day has burned out by week six; the open rate decays from daily to weekly to monthly until the install becomes a deletion. The ambient channel is what *keeps the system present* in the customer's life when the customer is not actively engaging. The Concierge cue on Wednesday — *the romaine you bought is at the back of the crisper, want me to plan it into tomorrow's dinner?* — keeps the system *useful* in a moment the customer would not have opened the app to ask about. CFMP thinks about the customer, in the kitchen, in the moment, at the speaker volume of a radio. That is the retention bet for week twelve. The DAU-over-MAU target Episode One named only holds if the system *is present* on weeks when the customer does not open the app.

**REID:** And Episode Six is the depth.

**KEVEN:** Episode Six is the depth — the Cue, the Cue Bus, the Zone, the ducking, the AirPlay-bridge fallback, the Azure-native deployment. Today we name the channel as a Mobile concern, because the Mobile inherits the ambient role when there is no Sonos. *The home channel is what keeps the system in the customer's life when the customer is not in the app.*

**REID:** Said cleanly. Move to preferences.

### Preferences and the "one voice" rule

**KEVEN:** Preferences. Because everything we have walked turns on preferences. What the customer wants. What the customer does not want. What the customer wants *at this time of day, in this channel, in this voice.* The design commits to a posture that is contrarian to the way most retail apps are built. *Maya Chen's* line from the Shopper Experts panel — *one CFMP voice, one persona, across every surface.* The voice is the brand.

**REID:** Restate why. Most listeners will say *of course the voice is the same.*

**KEVEN:** Most retail apps have different voices on different surfaces — the loyalty app has marketing-voice, the chat support has support-voice, the in-store kiosk has utility-voice, the email has corporate-voice. The customer experiences the brand as fragmented, because the brand *is* fragmented at the implementation layer. CFMP commits to *one voice* across every surface — the Mobile chat composer, the Sonos cue, the Portal operator response, the email confirmation. Same vocabulary, same warmth, same defaults, same humor calibration. There is one prompt context for tone, one set of voice samples in Azure Speech, one set of microcopy strings on Mobile, one set of email templates, and they all reference the same persona spec.

**REID:** And the preference layer that flows through every channel.

**KEVEN:** Five categories worth naming. *Cadence* — how often the system speaks. Daily, weekly, only when something is wrong. *Allergens* — the household's dietary policy, which becomes hard rules at the agent layer; peanut-free is a hard block on Sarah's CartLot members, regardless of channel. *Store loyalty* — which linked retailers, which loyalty memberships, which substitution preferences. *Quiet hours* — when the Sonos channel is allowed to speak; the Mobile is allowed to ping; the email is allowed to send. *Language* — the customer's language. Five preference categories. One layer. Every channel honors all five. The Sonos cue at nine-fifteen in the evening does not fire because the customer set quiet hours from nine to seven. The Mobile push at the same hour does not fire either. The email goes to draft and sends at seven-oh-one. *One preference, all channels.*

**REID:** And here I press. The commitment to preferences-flowing-through-every-channel is going to produce, in the wrong design hands, a *hundred-toggle preference screen* no customer will ever complete. The retail-app graveyard is full of preference screens that promised customization and delivered abandonment. How does CFMP avoid that?

**KEVEN:** *Smart defaults beat preference menus.* Vargas's line from the Preferences expert focus — *the smart-default action is where you earn or lose trust. Get it right eighty percent of the time and users stop noticing recommendations exist; they just notice the app gets them.* Every preference has a *defensible default* — a value the agent fleet picks at enrollment time, based on the household's archetype, the device's platform, the region, the population priors. The preference *surfaces* only when the customer hits the friction. The customer who is happy with the default never sees the toggle. The customer who is not happy with the default sees the toggle exactly when they need it — in the moment the friction lands. Not in a settings page they have to discover.

**REID:** A concrete example.

**KEVEN:** A concrete example, from Mobile Section Six-Six — the Scan Result Card's smart default. The card has a primary action; the Catalog specialist picks it from context. *Add to cart* if Sarah is in the store. *Adjust auto-replenish* if Sarah has bought this before and it is on her standing approval. *Find equivalent* if her linked store does not carry it. *Allergen warning* if the product violates the household's dietary policy. *One primary action, picked for the moment.* The customer who wants a different action long-presses and gets the secondary options. The customer who is happy with the default just taps. The default is right eighty percent of the time per Vargas's calibration target; the long-press is the escape hatch for the twenty percent. No settings page. No toggle. The agent decided; the customer can override; the override is recorded as a signal that re-calibrates the default for next time.

**REID:** And the brand consequence.

**KEVEN:** *One voice* means the customer experiences the system as a coherent persona across every channel. *Smart defaults* means the persona shows up *already calibrated*, not asking the customer to configure her. The combination is a brand experience the customer reads as — *this thing knows me, and it sounds the same everywhere, and it does not ask me to fill out a form.* That is the retention substrate at the brand layer. Not a feature. A posture.

**REID:** Said cleanly. The voice is the brand. The default is the brand. The preference menu is the escape hatch. Move to the UI revamp.

### UI revamp tradeoffs

**KEVEN:** The UI revamp. Because the design we have been walking is not the design that was shipped first; the design shipped first was — to use the Mobile UI Revamp document's own phrasing — *functional but utilitarian. All-inline CSS, raw HTML inputs, emoji-only icons, dark theme only, no design tokens, no motion system, no real haptics.* The team brought in two platform experts — Sarah Kim on iOS, Devon Patel on Android — and the revamp lands a full design system.

**REID:** What changed.

**KEVEN:** Five strokes. *First* — the system font stack went away, replaced with Inter as the primary, Geist Mono for prices and receipts, with SF Pro on iOS and Roboto Flex on Android as platform-native fallbacks. The cross-platform consistency is real; the platform feel is preserved. *Second* — the color system went from thirteen hand-picked dark-tone hex values to a Material 3 token system — primary, secondary, tertiary, surface, container, with full light-and-dark variants triggered by `prefers-color-scheme`. Everything is a role, not a hex. *Third* — emoji-as-icon went away. The new icon system is Material Symbols Outlined as primary, with Lucide as fallback. Variable axes let the icon scale crisply at every size on every device. *Fourth* — the bottom navigation went from a five-tab emoji-and-label grid to a three-tab Material 3 BottomNav with a pill-shape active indicator and a Floating Action Button on Home for scan. *Fifth* — the motion system landed. Six motion patterns from Material 3 plus the iOS-spring easing for sheets, with a `prefers-reduced-motion` guard clamping every transition to one millisecond when the system preference is set.

**REID:** What was preserved.

**KEVEN:** Safe-area handling — the original already used `env(safe-area-inset-*)` correctly. The PWA manifest — production-grade from day one. The pinch-zoom accessibility win. The three-tab navigation pattern — already the design commitment after the Sprint 1 collapse from six to three; the revamp preserved the structure and updated only the chrome. The revamp is additive; it did not throw out the design's posture, it gave the posture a wardrobe.

**REID:** And the smart-default-from-Vargas pattern inside the revamp.

**KEVEN:** Three places it shows up. *First* — the theme picker. Three options — System, Light, Dark. Default is System; the customer who never opens settings gets the system-preference behavior. *Second* — the haptics system. The customer on Android gets `navigator.vibrate(10)` on a button press by default; the customer on iOS gets the audio-cue-plus-scale-animation substitute because Apple does not expose the Taptic Engine to PWAs. The platform detection picks it. The audio cue volume respects `prefers-reduced-motion` — the customer gets quieter cues without ever finding a settings toggle. *Third* — the Scan Result Card's primary action we already walked. Three smart defaults, three places the design did not build a settings screen.

**REID:** And I press on whether the revamp deepens or simplifies. Design revamps usually deepen — more components, more states, more complexity. Defend the claim it simplifies.

**KEVEN:** The revamp added components — fifteen primitives where there were maybe four. Added a motion system where there was none. Added a theme system where there was none. By a *count* metric, the revamp deepened. By the metric that matters — *what the customer has to decide* — the revamp simplified. The customer no longer decides between five different button paddings — there is one Button primitive with five variants picked by context. The customer no longer experiences inconsistent press feedback. The customer no longer hits a theme that does not respond to her system preference. The customer no longer sees icons that render differently on iOS than Android — Material Symbols renders the same. The complexity that landed in the design system is the complexity that *used to be in the customer's experience as inconsistency*. The revamp moved it from the surface to the system. That is the simplification.

**REID:** A concrete example.

**KEVEN:** The bottom sheet pattern. Section Six-Three — the Scan Result Card opens as a bottom sheet. In the original, the sheet had no transition — it snapped on. On iOS, that *feels* wrong; iOS users expect sheets to spring up with a three-hundred-eighty-millisecond ease-out-back. The revamp added the spring entrance with `cubic-bezier(0.32, 0.72, 0, 1)` and added the drag handle so the customer can swipe down to dismiss. The customer did not have to learn a new gesture; the customer who already knows iOS now finds CFMP behaves like iOS. The customer on Android gets the Material 3 emphasized-decel easing at three hundred milliseconds, which matches the rest of the Android ecosystem. *Same component, two platform-feel variants, picked by `navigator.userAgent`.* The customer never picks. The customer never even knows.

**REID:** The revamp deepened the system to simplify the experience. Move to senior mode.

### Senior mode and accessibility hooks

**KEVEN:** Senior mode and accessibility hooks. Because the design has, threaded through every section we have walked, a commitment to a population most retail apps fail — the senior shopper, Robert Park's archetype, the highest-lifetime-value population in grocery and the most-abandoned-by-app-design. The Mobile design's accessibility patterns are real, and they earn the design its credibility with the population that pays the most.

**REID:** Walk the patterns. Briefly.

**KEVEN:** From Mobile Section Six-Ten. *Large-text mode* — default on for users sixty-five and over, toggle for everyone in Me-then-Settings. The mode rescales the type tokens — every text role bumps up two steps. *Voice-first defaults* — the senior segment gets a voice-first mode where the chat composer surfaces a microphone affordance as the primary input. The voice input goes through Azure Speech on the way in and through the same agent fleet on the way back. *Simple mode toggle* — Yamamoto's recommendation; hides the Lots tab, reduces the chrome, collapses the navigation to two tabs — Home and Me — for the customer whose cognitive load is the design constraint. *Forty-four-by-forty-four point minimum touch targets* — the iOS HIG minimum; the revamp's Button primitive enforces it. *Material 3 ordered semantics* — `aria-current="step"`, `aria-live` for toasts, `focus-visible` everywhere. VoiceOver on iOS and TalkBack on Android both navigate the surface coherently.

**REID:** And Yamamoto's framing.

**KEVEN:** *The speaker is the highest-leverage accessibility surface for our oldest segment.* That line is in the design document, and it is the foundation of the Sonos channel's architectural priority. The customer who cannot see the small text on her phone can still hear the kitchen Sonos. The customer whose hands tremble too much to scan a barcode can still answer a Concierge moment with a one-syllable yes. The Sonos channel is not just a delight feature for power users; it is an accessibility surface for a population the visual app cannot reach as fully. Episode Six unpacks the channel; Episode Eight unpacks the full accessibility story across all surfaces.

**REID:** And the parallel on Mobile.

**KEVEN:** Larger touch targets — the senior-mode toggle bumps the Button primitive to sixty-by-sixty for the population that needs it. VoiceOver and TalkBack compatibility — every interactive surface has an `aria-label`, every state change has an `aria-live` announcement, every focus order is intentional. Simpler journey flows — the senior-mode collapse to a two-tab nav is the most aggressive case. The hand-off-to-a-caregiver pattern — the Diana role from Episode One, where the senior household member's lots can be delegated to a caregiver acting on their behalf, with the consent boundary blocking the regulated information the caregiver should not see. The hand-off is a delegation, not a takeover. Episode Eight walks Diana's role in full.

**REID:** *Accessibility is the design quality test.* Not just for seniors. Not just for declared disability. The accessibility patterns are the patterns *every* customer benefits from in *some* moment — large touch targets help when the customer is one-handed with a stroller, voice input helps when the customer has wet hands at the kitchen sink, simple mode helps when the customer is tired at the end of a long day, the screen reader's coherent navigation helps when the customer is using the phone in bright sunlight and squinting. The accessibility commitments are the *quality floor* of the entire design, because they are what catch the moments every customer ends up in. The senior segment forces it. Every other segment benefits.

**KEVEN:** The speaker is the highest-leverage accessibility surface. Accessibility is the design quality test. Move to the reading.

### A reading I want to do

**REID:** A reading. I want to recommend the one that has been hanging over this episode since the kitchen-radio metaphor landed, because the metaphor is borrowed and the listener should know from where. *Mark Weiser. The Computer for the Twenty-First Century. Scientific American, September nineteen-ninety-one.* Six pages. Short. The paper that named *ubiquitous computing* and, with it, the design posture we are now calling *calm tech.* Weiser was a research director at Xerox PARC, and the paper argues that the computers that matter most are the ones that *disappear into the environment* — that get out of the customer's foreground, that demand attention only when attention is warranted, that recede the rest of the time. He uses the analogy of the electric motor — once a single big motor in a workshop, now invisible in dozens of household appliances nobody thinks about. He predicts the most successful computing of the next thirty years will look the same. Calm. Embedded. Ambient. Out of the way.

**KEVEN:** And the relevance to the home channel.

**REID:** The home channel is the design taking Weiser seriously. The Sonos cue on a Wednesday — *the romaine is at the back of the crisper, want me to plan it into tomorrow's dinner* — is calm tech in exactly the sense Weiser meant. It demands attention only when warranted; it recedes the rest of the time; it works *in the environment the customer already lives in*, with the speaker that is already on the counter. The Mobile screen with its forty-five-minute Sunday-morning compose is the *anti*-calm-tech surface; the home channel with its fifteen-second timely cue is the calm-tech corrective. Both ship. The Mobile is the foreground; the home channel is the background; the design needs both. Weiser's frame sharpens the home-channel argument because it locates the home channel in a design tradition older than smart speakers and broader than CFMP. The radio metaphor is not a clever turn of phrase; it is the literature.

**KEVEN:** And I push gently. Weiser's frame has a trap, and the trap is that *calm* gets confused with *passive*. The home channel cannot be so calm that it is invisible; the customer needs to *learn* the channel exists, needs to *experience* the channel working, needs to *trust* the channel before the channel can recede. The first few weeks of a new CFMP install are louder than the long tail; the channel earns its calm through the customer's experience of it being right at the right moments, then settles into the radio posture. Weiser's frame is correct; the implementation has to season into it, not declare it on day one.

**REID:** Accepted. Calm tech is a destination, not a starting position. Pair Weiser with anything from the more recent ambient-computing literature — the work on peripheral displays from the early-two-thousands, or any of the calm-tech retrospectives now that voice assistants are mature enough to evaluate as a category. The point is the same — the home channel is in a tradition; the tradition is mature; the design borrows correctly.

### One disagreement

**REID:** One disagreement. The one closest to the line between *useful* and *creepy*.

**KEVEN:** Put it on tape.

**REID:** *Proactive replenish-suggestions risk a creepy-uncle feel.* The pitch sounds great in a design review — *the system noticed you are running low on eggs, want me to add them to Saturday's pickup?* The reality, for a meaningful slice of the customer base, is that *your fridge knows you are out of eggs* makes them recoil. There is a line between helpful and surveilling, and the line is thin, and where the line is depends on who the customer is and what kind of week they are having. The customer who is happy with auto-replenish on a Tuesday may find the same notification *invasive* on a Friday when they have just had a fight with their teenager. The proactive moment is the proactive moment whether the customer is in the right mood or not. The design's confidence that *opt-in plus transparency plus the kill switch* solves the surveillance posture is — I think — over-confident. It solves the *legal* problem. It does not solve the *moment-by-moment* mood problem.

**KEVEN:** Conceded that legal and moment-by-moment are different. The design's answer is layered. *First* — opt-in, transparent, evidence-based. The customer enrolls the standing approval explicitly; the customer sees the transparency surface that explains every inferred preference; the customer can hit the kill switch and the inferred rows are deleted. That is the legal floor. *Second* — the consent gradient. The system observes liberally, retains selectively, and acts conservatively. The proactive moment is *suggestion*, not *enrollment*. *Third* — the channel-and-cadence calibration. The Concierge specialist that fires a moment learns, from the customer's behavior, when to fire and when to stay quiet. The customer who dismisses three weather-driven nudges in a row gets the cadence dropped to *only when severe*, with a soft prompt that lets the customer revise further.

**REID:** And the threshold for when a proactive moment fires.

**KEVEN:** *The two-touch rule.* A proactive replenish-suggestion only fires after the customer has bought the same SKU twice — not once. A single purchase is *intent*; two purchases is *pattern*. The system waits for the pattern. And the channel for the suggestion respects the customer's consented channels — the customer who has opted into the home channel hears it there; the customer who has not, sees it on the Mobile. *Two-touch threshold. Consented channels only.* The cold open's wilted-romaine moment is the case study — Sarah bought romaine four Sundays in a row before the system spoke. The system did not jump on the first Sunday with a *we noticed you bought romaine, want it weekly?* nudge; the system waited until the pattern was four cycles deep before composing the substitution suggestion. The system speaks when the system has *earned* the right to speak.

**REID:** Converge.

**KEVEN:** *Proactive suggestions fire only after the two-touch threshold, only in consented channels, with the consent gradient as the substrate and the kill switch as the customer's recourse.* The wilted-romaine cold open works because Sarah bought romaine four Sundays in a row before the system spoke. The system that speaks on the first Sunday earns the creepy-uncle critique. The system that speaks on the fourth Sunday — *the romaine you keep buying is unlikely to last past Wednesday* — earns the customer's trust. The threshold matters; the channel matters; the cadence calibration matters. None of those guarantees the moment-by-moment mood; all of them tilt the design toward *helpful* and away from *surveilling*. The residual risk is the design's honest cost of doing business.

**REID:** Converge accepted. Two-touch, consented channels, consent gradient as substrate. The cold open works because the wait was long enough. Carry it.

### What to carry forward

**KEVEN:** Three things into Episode Five. Numbered, because the listener carries them.

**KEVEN:** *One — the four primary surfaces of Mobile.* Trip view, Replenish, Home, Preferences. Each maps to a phase of the customer's week. The Trip view is the foreground experience in motion — pre-trip compose, in-flight substitution, settling at the door, closed at consumption. Replenish is the background experience that runs against the customer's standing approval. The Home tab is the ambient surface — the camera viewport, the Lots Strip, the chat composer, the FAB. The Preferences surface is the escape hatch — the kill switch, the inferred preferences, the explicit edits — the surface the customer opens *only* when the friction lands. Four surfaces. Four roles. One design. Carry that.

**KEVEN:** *Two — the consent gradient is the design's privacy substrate.* Three tiers — session-local observation, persistent inference, material action. The system observes liberally, retains selectively, acts conservatively. The customer's autonomy lives in the gap between persistent inference and material action. Episode Eight unpacks the gradient in full. We previewed it here because Auto-Replenish does not work without it. Carry that.

**KEVEN:** *Three — smart defaults beat preference menus.* Every preference has a defensible default. The default is picked from population priors at enrollment and re-calibrated against the customer's behavior over time. The Preference Center exists for the customer who wants to see and edit; the Preference Center is not the default path. The customer who is happy with the defaults never opens the Preference Center; the customer who hits the friction sees the toggle exactly when she needs it. Vargas's line — *get the smart default right eighty percent of the time and users stop noticing recommendations exist; they just notice the app gets them.* Carry that.

**REID:** Four surfaces. Consent gradient. Smart defaults. Three carries. Into Episode Five.

**KEVEN:** Next episode — *Portal · operator console and B2B multi-tenant.* The Portal as the seller's artifact, the chat panel, the vision-kit integration, the retailer multi-tenant story, and the deep walk-through of the live `/architecture` page as the seller's screen-share. We have walked the customer surface for three episodes; next episode we walk the operator's surface and the seller's surface together.

[Sound: the closing sting. ~6 seconds.]

---

## Further reading

- **Source docs**
  - CFMP Mobile Design Document — `C:\code\iot_device\docs\packs\CFMP-Mobile-Design-Document.md` — §3 (Journey maps, in particular §3.2 Sarah's weekly meal-plan-to-table cycle and §3.4 Robert's pharmacy refill); §6 (Key design elements, in particular §6.5 the Home layout, §6.6 the Scan Result Card smart default, §6.7 the Lots Tab + Lot Detail unified template, §6.9 Voice UX, §6.10 Accessibility patterns); §7 (Use Case Catalog, in particular the critical-path UC-73 PantryLot auto-spawn, UC-89 Lots Strip on Home, UC-91 PlanLot from meal plan, UC-95 CartLot checkout, UC-101 Trace_id injection)
  - CFMP Mobile Preferences Expert Focus — `C:\code\iot_device\docs\packs\CFMP-Mobile-Preferences-Expert-Focus.md` — Vargas's seven-things-she-would-ship, the consent gradient §6, the Why-Am-I-Seeing-This transparency surface §7, the Preference Center §8, the sensitive-inference guardrails §9, the cook-vs-eaters household-graph problem §12
  - CFMP Mobile UI Revamp — `C:\code\iot_device\docs\packs\CFMP-Mobile-UI-Revamp.md` — the cross-platform design system, the Material 3 token system, the Inter + Geist Mono + Material Symbols typography stack, the smart-default-in-chrome pattern, the migration plan folded into the Sprint Orchestrator
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — the canonical deployment topology. The Mobile lives in `ca-visionkit-mobile`; the orchestrator hosts the Trips, Replenish, and Concierge specialists; the home channel routes through Azure Speech and the Sonos Cloud Control API.
- **Microsoft Learn**
  - Microsoft Fabric Mirroring — `https://learn.microsoft.com/fabric/database/mirrored-database/` — the data-tier mirroring substrate that lets the Replenish specialist's prediction reason over a near-real-time consumption signal without taxing the operational stores
  - Azure AI Foundry — `https://learn.microsoft.com/azure/ai-foundry/` — the productized agent runtime that hosts the orchestrator and the Trips, Replenish, Coupons, Pharmacy, and Concierge specialists
  - Azure AI Speech — `https://learn.microsoft.com/azure/ai-services/speech-service/` — the neural text-to-speech surface that gives the home channel its one-voice posture; `en-US-AvaMultilingualNeural` is the default; `en-US-AndrewNeural` for alerts
- **Industry / research**
  - Mark Weiser — *The Computer for the Twenty-First Century* (Scientific American, September 1991) — the foundational paper on ubiquitous computing and calm tech; the literature the home channel's kitchen-radio posture descends from
  - Nielsen Norman Group on ambient computing and notification design — the empirical work on when proactive prompts read as helpful versus invasive; informs the two-touch threshold and the channel-and-cadence calibration
  - Apple Human Interface Guidelines on Notifications and on Voice and Speech — `https://developer.apple.com/design/human-interface-guidelines/` — platform constraints on push cadence, attention budget, and voice-input ergonomics that the Mobile PWA respects on iOS Safari
- **Sibling series cross-reference** — Cross-Cloud Agentic Episode 05 (*Audit, Ledger, and Replay — The Trust Substrate*) at `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\05-audit-ledger-and-replay.md` — the framework-level treatment of the consent-and-audit pattern the Mobile surface inherits

— end of episode 04 —
