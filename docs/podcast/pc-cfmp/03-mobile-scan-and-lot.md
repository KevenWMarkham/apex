# Episode 03 · Mobile · SCAN & LOT

**Episode 03 · Mobile · SCAN & LOT** — Sarah at the store on a Tuesday, a coupon barcode that will not load, a six-dollar miss. We open on the moment the legacy retailer app failed her, and we walk the architectural move that erases it — the lot model in depth, the four lot archetypes, scan-first design as the front door, and the MCP boundary on Mobile that makes the scan a fact instead of a guess.

**Builds on:** the show bible (00-show-bible-and-format) · Episode 01 (Sarah's Day) · Episode 02 (Agent fleet & audit chain) · CFMP Mobile Design Document §4 (Core Concepts) · CFMP Mobile ScanFirst Design · CFMP Mobile Lots Expert Focus · CFMP Mobile Use Cases (sampled SCAN/LOT UCs)
**Run time:** ≈ 40 minutes target
**Last updated:** 2026-05-25

---

## Cold Open

[Sound: a wide-aisle supermarket on a Tuesday afternoon, around four-twenty. Carts rolling on a hard polished floor. A faint announcement two aisles over about a cleanup. Somewhere closer, a child negotiating loudly about a fruit snack. The whir of a refrigerated cabinet kicking on. The plastic-on-plastic clatter of someone pulling a box from a shelf and putting it back.]

It is four-twenty on a Tuesday afternoon, and Sarah Chen is in the diaper aisle of her usual store because she remembers, with the particular sinking feeling of a parent who is going to be paying full price for something she could have planned for, that she forgot the diapers. She had not put them on the Sunday list. Sunday was the morning she spent forty-five minutes across three apps and never closed the loop. She is here for one item. She knows where it is. She picks the box up. And as she pulls it down from the second shelf she notices, taped to the shelf rail just below the price tag, a small yellow coupon — printed on cheap stock, a one-dollar offer with a barcode at the bottom, the kind the retailer puts on the shelf when a vendor wants to move volume.

One dollar. Twelve diapers. Worth a scan.

She opens the retailer's loyalty app, the one she has had on her phone for three years, the one she dutifully launches every time she walks into this store because she has been trained to. She finds the in-app scanner, three taps in. The camera comes up. She points it at the barcode. The barcode reads. The app spins. The app spins. The app spins. And then it tells her — *we couldn't load the offer right now, please try again* — because the bottom-shelf coupon barcode resolves to a web page on the vendor's marketing domain that the retailer's app proxies, and that proxy is going through the store's bad cellular signal in the back corner of aisle eleven, and the page does not render.

She tries once more. She does not have the patience for a third attempt. The kid is starting to escalate. She closes the app, drops the diapers into the cart, and walks to the checkout. Twelve diapers, full price. A six-dollar miss.

That is six dollars Sarah will never get back. Multiply it by every customer who ever tried to scan a shelf coupon in cellular dead-zone aisle eleven. Multiply that by every retailer with the same architecture. The opportunity cost is not six dollars. The opportunity cost is the loyalty mechanic the retailer paid the vendor to put in the store, evaporating at the moment of redemption, because the architecture handed the scan to a network round-trip instead of to an agent that already knew the answer.

[Sound: a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start there. Sarah in aisle eleven. The yellow coupon. The six dollars that walked out of the store with her.

**REID:** Because the six dollars is not the story. The architecture is the story. The shelf coupon resolved to a web page on the vendor's marketing domain that the retailer's app proxied through a cellular dead zone. Six choices, made by six different vendors, none of them coordinated, all of them stacking until the customer pays full price. That moment exists because no one in that stack treated the scan as anything other than a network round-trip. CFMP-SCAN treats it as a fact handed to an agent fleet, and the agent fleet composes against Gold-tier coupons across the household's loyalty memberships before the box leaves the shelf.

**KEVEN:** Welcome back to the CFMP Podcast. Episode Three. *Mobile · SCAN and LOT.* In Episode One we walked Sarah's week — the customer problem, the five archetypes, the lot as the unifying noun, scan as the headline verb. In Episode Two we opened the substrate underneath — the agent fleet, the MCP boundary, the LedgerRow, the trace identifier that lets a regulator's question land on twenty-three rows in three minutes. Today we open the surface that sits on top of that substrate. The lot model in depth. The four archetypes. Scan-first as the front door. And the MCP boundary on Mobile specifically — where Sarah's scan in aisle eleven becomes the fact the Coupons specialist composes against, instead of the URL the legacy app failed to load.

**REID:** And I am back as the honesty enforcer. When the design is doing something a thousand grocery apps could do, we name it. When it is doing something only the lot-and-scan architecture makes possible, we name that too. The architecture has to defend itself.

**KEVEN:** Six sections. The lot model in depth. The four archetypes. The SCAN interaction. The MCP boundary on Mobile. Six UCs at the centre. And the honest comparison. Let's go.

---

## The conversation

### The LOT model in depth

**KEVEN:** Picture Sarah on a Sunday evening. She's done her meal plan. The shopping intent for the week is named. It has a pickup time on Tuesday morning. There's a wilted-romaine warning queued for Thursday morning. There's a Saturday birthday party that needs peanut-free options for one of her daughter's friends. *All of that is one thing.* One bounded slice of her household's life. Not a list — a list is just words on a page. Not a cart — a cart closes at checkout. *A managed thing with a beginning and an end, that the system holds for her so she doesn't have to.* That's the lot.

**REID:** Define it for the room, the way it would survive an architecture review.

**KEVEN:** A lot is *a bounded slice of a household's commerce life over a window of time.* It has edges — when it starts, when it ends. It has intent — what the household means to do, not just what it has done. It has membership — the products that belong to it. And it has a lifecycle — it moves through stages the same way Sarah's week moves through days.

**REID:** And the customer-feel of the four stages.

**KEVEN:** Four moments Sarah lives. *Thinking about it* — the Sunday-evening meal plan that hasn't bought anything yet. *Coming to her* — the pickup is staged, the delivery is on a truck, the order is real. *Living with it* — the bags are in the kitchen, the household is eating from it, the romaine is approaching its end. *Done with it* — archived; consumed cleanly, or thrown out, or carried into next week's plan. The lot lives one of those four moments at every instant. The customer doesn't have to name them. The system tracks them.

**REID:** And the customer-feel comparison the listener will recognize.

**KEVEN:** A list is what Sarah is *thinking about*. A cart is what Sarah is *buying*. A basket — the word she'd say in the parking lot — is what Sarah is *carrying.* None of those three is *the thing her household is doing this week.* The list is a snapshot Sarah closes and reopens cold. The cart closes at checkout and vanishes. The basket has no memory across surfaces — her loyalty-app basket, her delivery-app basket, and her meal-plan basket are three different baskets that don't know about each other. *That's the household experience CFMP is replacing.* The lot is the thing all three of them were always pointing at. The list is one question against the lot. The cart is one transaction against the lot. The pantry is what the lot turned into. The next meal plan is a question against what the lot left behind.

**REID:** And the engineer's discipline behind the household feel.

**KEVEN:** Every specialist in the agent fleet has the lot in front of it as the noun of work. The catalog specialist composes against the lot. The wayfinder composes against the lot. The auto_replenish specialist owns its own lot. The concierge reasons over the lots Sarah has active and decides whether to nudge. *Nobody works on a list. Nobody works on a cart. The unit of work is the lot.* Two examples by name — when Sarah taps *shop this plan* on her Sunday meal plan, the system creates a lot in draft. When she checks out, the same lot transitions to pickup or delivery — *the parentage holds end to end,* so six weeks later when somebody asks where Sarah's Wednesday milk came from, the answer is one chain of lots.

**REID:** And the commitment. The lot is the unit of work *everywhere* or the noun is hollow. If one corner of the system reverts to thinking *list*, the household feel collapses. The discipline isn't free. The payoff is what the rest of the episode walks.

**KEVEN:** Said cleanly. The lot is the household's experience, named — and the system is built around it.

### The four lot archetypes

**KEVEN:** Four customer moments. Four kinds of lot. We named them in Episode One. Today we go deeper — what each one *feels like* to the customer, and what each one *forces* the architecture to be able to do. Because these four aren't four flavors of the same thing. Drop any one of them and the design contracts to a smaller, lesser version of itself. Keep all four and the architecture has to be the shape the design commits to.

**REID:** Walk them.

**KEVEN:** First — *the shopping trip.* Sarah on a Saturday morning. She placed the order Friday night, the pickup window opens at ten, the picker is walking the aisles right now. The lot is *live* — Sarah can see *packed by ten-forty-two* on her phone, the picker pings her with a substitution question about the rotini she wanted, she says yes, the lot updates. The bags hit her trunk and the lot transitions into her pantry. *Every minute of that trip is a moment that matters.* Architecturally, this is the lot that exercises live operational state — the prep-state badge, the substitution flow, the handoff confirmation. The state machine has to be alive, not decorative, because the customer is watching.

**REID:** Second.

**KEVEN:** *Auto-replenish.* The lot Sarah almost never opens. Six months ago she set up milk, bread, diapers, eggs, coffee, and the kid's cereal to just arrive on a rhythm the system learns. Now those items show up on schedules the system computes from how fast her household actually consumes them. The customer-moment is the *absence* of a moment — Sarah notices the lot only when something is unusual, or when the system surfaces a skip-this-week question because the household is on vacation. The architectural property this lot forces — *the agent has to be able to defend its own reasoning months later.* Six weeks after the fact, when Sarah asks *why did you order me four gallons of milk on the week we were away,* the system has to answer with the reasoning that produced the decision. Every cadence step is recorded — why this week, why this quantity, why this substitution. (The audit row earns its rent here as clearly as anywhere in the system.)

**REID:** Third.

**KEVEN:** *The stay-trip.* Marcus and four friends rent a cabin for a long weekend. The lot follows them — staples landing twenty-four hours before check-in, the cold leg arriving within two hours of arrival, a mid-stay top-up the morning of day two. *The first two hours of vacation are not spent at a grocery store.* Multi-leg deliveries. Friends co-editing the cart from their own phones. Payment splitting four ways. The household isn't a fixed address; the delivery target is temporary; not all collaborators are loyalty members. Architecturally, this lot forces *displacement* as a first-class concept — the property-tokenized delivery target, the multi-leg fulfillment as a structured plan, the friend invitations that don't require a loyalty account.

**REID:** Fourth.

**KEVEN:** *The care-trip.* The diabetic-friendly snacks shipped to Sarah's mother's address, paid on Sarah's card, with Sarah-acting-for-her-mother recorded in the chain — *and the boundary that keeps her mother's prescription refills out of Sarah's view, no matter how the app is poked at.* The customer-moment is *helping safely* — Sarah can do the grocery half of her mother's life without seeing the pharmacy half. The architectural property this lot forces — the four-identity chain we walked in Episode Two. Sarah-acting-as, her mother-the-account-holder, the system that took the action, the audit her mother will never see. Without this archetype the substrate could be lighter. With it, the substrate has to be exactly what Episode Two unpacked.

**REID:** Four customer moments. The shopping trip forces live state. Auto-replenish forces durable reasoning. The stay-trip forces displacement. The care-trip forces the identity chain. Each one bends the architecture to a shape it would otherwise not need. *The archetypes are not features. They are the constraints that make the substrate the shape it is.* Drop one and the substrate is smaller than the customer's life. Keep all four and the substrate matches the life it serves.

**KEVEN:** Said cleanly. The architecture is the answer to the four moments. Not the other way around.

### The SCAN interaction

**KEVEN:** Picture Sarah opening the app. Most retail apps would show her a search box at the top, a category grid below, a deals carousel at the bottom — and ask her to know, right now, what she wants. CFMP doesn't ask her anything. The app opens to her camera. The camera is already on. *No buttons. No menus. No decisions before she's even started.* The thing she would have done — point the phone at the product in front of her — is the thing the app expects her to do.

**REID:** Scan-first versus search-first. Walk it.

**KEVEN:** Search is still there. It tucks into the chat composer below the viewport, for the moments Sarah really does have a name in her head. But the *front door* is the camera. The system has already chosen the default the way her phone's default app is the keyboard when she opens a messenger — because the moment she's most often in is the one where she has a thing in her hand and doesn't know what to call it. (The design committed to this verbatim — the home screen is dominated by a camera viewport, tapping scans, no other affordance competes for primacy.)

**REID:** And the four things her camera can do for her.

**KEVEN:** Four things, all by pointing the same camera. *A product on the shelf* — Sarah holds a box of pasta, points the camera, gets the right product back in two seconds. *A coupon on a rail* — the yellow shelf coupon from the cold open, scanned in-aisle, the saving on the card before she reaches the checkout instead of a marketing web page that won't load. *A recipe card with a code on it* — the recipe resolves, ingredients composed against what Sarah already has in the pantry, the missing items added to her cart. *A label with no barcode at all* — the jar of jam she picked up at the farmers' market, captured as a photo, identified by the system, landing in the pantry where it should have been all along. *The Mobile doesn't ask Sarah to pick a mode.* The system tries barcode first, then QR, then photo identification — and she just points the camera at the thing.

**REID:** And every one of those four returns a *fact*, not a guess.

**KEVEN:** Every one. The product comes back as the right product, with the right price after Sarah's loyalty discount and the right dietary flags. The coupon comes back as the actual saving against her actual loyalty memberships, not a URL. The recipe comes back with its ingredients already cross-checked against her pantry. The jam comes back resolved. The scan is the trigger. The agent fleet does the work behind the scene. The card on Sarah's phone shows the answer.

**REID:** And the obvious push. *Isn't this just a barcode reader?* Every grocery app has had one since 2014. Yuka does it. Google Lens does it. What is CFMP doing that those do not?

**KEVEN:** CFMP treats the scan as *the front door to an agent fleet*, not as a feature in a feature menu. Yuka tells you what the product is. Lens tells you where to buy it. Neither composes against Sarah's household loyalty memberships, Sarah's pantry, Sarah's dietary policy, Sarah's active meal plan, Sarah's auto-replenish history, the live recall feed, and her active stay-trip and care-trip — all in one pass, behind one tap. CFMP does. The catalog specialist, the wayfinder, the auto_replenish, the concierge — all four read the scan and all four compose their part of the answer. The card shows the smart default. *One tap from Sarah. Four kinds of thinking behind it.*

**REID:** And the architectural argument worth landing. The scan is the front door because the front door has to hand the agent a known entity, not a string. A search box hands the agent a string and the agent has to guess. *Guesses are the failure mode of every chat-first retail surface that ever shipped.* The scan returns a fact. The MCP boundary is what makes it a fact. That's the next section.

### The MCP boundary on Mobile

**KEVEN:** Back to Sarah in the diaper aisle. She scans the yellow coupon. Three seconds later her phone shows *apply this coupon, save one dollar at checkout.* The saving is real, the loyalty membership is hers, the redemption window is open, the discount stacks correctly against her existing offers. *None of that was a guess.* This section is about why the answer Sarah got was a fact, not a story — and why the architect across the table from a CIO can promise it'll *keep* being a fact, even as models change underneath the system year over year.

**REID:** Restate the principle in plain language for the listener who skipped Episode Two.

**KEVEN:** Every time an agent answers something for Sarah, the agent has reached for a curated, governed view of the data — never the raw source. The agent doesn't write SQL. The agent doesn't compose a database query. The agent doesn't invent a tool that doesn't exist. The agent has a list of allowed questions it can ask, each one returning a structured fact, each one recorded on the audit trail on the way back. (Architecturally, that's the MCP boundary. Every agent tool call lands on a governed view; the runtime won't let it land anywhere else.)

**REID:** Walk Sarah's scan-coupon end to end.

**KEVEN:** Sarah points the camera at the yellow coupon. The barcode resolves locally on her phone — no round trip needed for that part. Her phone sends the resolved barcode up to the agent fleet, along with her household identifier and a tracking thread that will follow this moment everywhere it goes. *That thread is what would let a regulator, six weeks later, re-show Sarah this exact scan in three minutes.* The agent fleet routes the question to the specialist that knows coupons. That specialist composes one well-defined question against the governed view — *for this household's loyalty memberships, against this product, on this date, what's the best applicable saving?* The view returns a structured answer — the matching coupon, the saving amount, the redemption window. The system records the action. The card on Sarah's phone lights up with the one-dollar saving. Her phone gives her a soft haptic confirmation. From shelf to card — three seconds.

**REID:** And what about the kitchen — does her speaker say anything?

**KEVEN:** Not in this moment. Sarah is in the store, the saving is already on her screen, the kitchen speaker would be talking past her. The concierge specialist looked at the same moment and decided silence was the right answer. (If Sarah had been home, finishing a meal plan, and the same coupon had matched against a planned item in tomorrow's pickup, the speaker might have queued a soft cue. Episode Six walks that channel.) *Sarah sees one card. The architecture absorbs the complexity of the seven services, the four specialists, the consent check, the audit row, the tracking thread, the loyalty join.* She sees the win.

**REID:** And here's the harder argument worth landing. The agent's prompt is interesting. The agent's reasoning is interesting. The model version is interesting. *None of those is the architecture.* The architecture is the property that the agent literally cannot reach the raw source, cannot write SQL, cannot invent a tool — *by construction, enforced at runtime, not by a developer being well-behaved.* That's the contract a seller defends in front of a CIO who has been burned by generative AI improvising against a production database. That's the contract a regulator inspects when she asks *what did the agent have access to.* The contract is the architecture.

**KEVEN:** Conceded. The agent code is not the moat. The boundary is the moat. The agent code can change every quarter — models deprecate, prompts evolve, specialists get re-tuned — and the architecture holds. CFMP picked the boundary first and built the agents inside it. The wrong order — agents first, boundary retrofitted — produces the agentic systems that fail their first audit. The customer outcome is the part that matters: *the answer Sarah gets is right the first time, and right the same way every time.* That isn't a marketing claim. That's a property the runtime enforces.

### Six moments at the centre

**KEVEN:** Now the six moments that make the rest of the catalogue work. Not feature numbers — six *customer moments* the design rests on. The Mobile use-case catalogue has more than a hundred entries. Six of them are the spine. The rest compose from those six. If the seller can walk these six in a demo, the architecture argument is on the screen.

**REID:** Six. Move.

**KEVEN:** *Sarah scans a product in the aisle.* She holds a box of pasta in aisle nine, points the camera, two seconds later the right product is on her screen — the right brand, the right price after her loyalty discount, a dietary flag if the household profile would catch one. This is the front-door moment. Every other scan moment in the catalogue composes from this one.

**KEVEN:** *The card knows what Sarah is most likely to do.* The card that comes back from the scan doesn't just identify the product. It picks the right primary action for *this* moment — *add to cart* because Sarah is in the store, or *adjust auto-replenish* because Sarah has bought this before, or *find an equivalent* because her preferred store is out, or *allergen warning* because the product would violate her household's dietary policy. *One tap saves the right thing.* This is the moment where the agent fleet's value is most legible — the system has done the thinking, Sarah just confirms.

**KEVEN:** *The scan lands on the active lot.* Sarah taps the primary action and the item lands on the lot she's working — the Tuesday pickup, the auto-replenish cadence, the cabin trip, the meal plan she's still composing. *One tap from the camera to the lot.* No menu, no list-picker, no confirmation popup. The continuity from front door to lot is what makes the lot live as a noun across the surface.

**KEVEN:** *The yellow shelf coupon.* The cold-open moment. Sarah in the diaper aisle, the rail-mounted coupon, the camera up, the saving on the card in three seconds. The architecture composes the right offer against her loyalty memberships and her household's policy — *the six-dollar miss becomes a one-dollar save,* instead of a marketing page that won't load on bad cellular.

**KEVEN:** *Bulk-scanning the haul from outside CFMP.* Sarah at her kitchen counter on a Saturday, unloading the farmers'-market run, the warehouse-club trip, the corner market. None of those came through CFMP. She opens the app, taps the bulk-scan mode, and runs the camera across each item — no card between scans, no confirmation taps, just the haptic acknowledging each one. The session closes and the haul becomes part of the household's pantry the agent fleet now knows about. *Without this moment, the pantry is only as complete as what flowed through the app. With it, the pantry is as complete as Sarah takes sixty seconds to make it.*

**KEVEN:** *Marcus binds a stay-trip to his cabin booking.* He pastes the booking URL into CFMP. The lot creates itself, bound to the property and the date range, ready for his friends to join from their phones. From there the system can stage three deliveries against the cabin — staples a day ahead, the cold leg at check-in, the mid-stay top-up day two — without ever associating the cabin to Marcus's home address. *One link from his booking, a whole vacation grocery plan that doesn't require him to remember.*

**REID:** Six moments. Front door, smart default, scan-to-lot, coupon save, bulk pantry capture, stay-trip seed. The catalogue has a hundred more. Every one of them composes from these six. The seller demonstrates the six. The engineer ships the catalogue.

**KEVEN:** Said cleanly. Six moments. Six customer wins. *Carry them.*

### The honest comparison

**KEVEN:** Now the comparison the seller faces in the room. Because the CIO across the table has heard a *Microsoft is best* pitch from three different vendors this quarter, and the architect next to her has built production retail workloads on AWS or GCP and isn't here to be sold to. The credibility of the rest of the series depends on this section being honest.

**REID:** Walk it. AWS first, GCP second, Microsoft last. Be honest.

**KEVEN:** AWS first. Bedrock Agents for the fleet — capable, mature, productized. The audit substrate composes across CloudTrail at the platform layer, an application ledger in Aurora, S3 Object Lock as the immutable tier, Audit Manager as the auditor's view, Lake Formation governing the data plane, Macie for sensitive-data discovery. *It works. It ships.* A competent platform team assembles it in six to twelve weeks.

**REID:** GCP.

**KEVEN:** Vertex AI Agent Engine for the fleet — capable, mature, productized. Cloud Audit Logs at the platform layer — and GCP earns a real point worth naming, because the immutable audit log is a platform property, not an add-on. Add Dataplex for governance, Sensitive Data Protection for discovery, Security Command Center as the posture surface. *It works. It ships.* Same six to twelve weeks.

**REID:** And Microsoft.

**KEVEN:** Azure AI Foundry for the fleet. Microsoft Purview for the audit and the AI-aware data security posture management. Microsoft Entra for identity. *Three productized services, one bill, one console, one identity surface.* AWS would assemble seven productized services, GCP six, Microsoft three. *Not capability — both other clouds have the capability.* The difference is what an architect calls *assembly tax* — build cost of integration, operate cost of multiple identity surfaces, audit-firm-credibility cost of assembling evidence across multiple consoles.

**REID:** The seller's pivot.

**KEVEN:** *Concede capability. Pivot to density.* The Microsoft win is productized density. One product for the agent fleet, one for the audit substrate, one for identity. The seller doesn't pitch capability — every architect has heard that pitch from three clouds and is tired of it. The seller pitches the integration seams the customer has to maintain — fewer seams, fewer bills, fewer dashboards, fewer skills to hire — and defends on the cost the customer actually pays year after year.

**REID:** *Concede that all three clouds can build it. Earn the recommendation on density.* That's the line, and it survives an AWS or GCP architect in the room because it doesn't deny their capability. *The architecture decides; the cloud follows.* CFMP committed to Microsoft because the productized density compresses the seams the customer's life depends on — care-trips, auto-replenish, stay-trips, shopping trips. Other clouds carry the design. Microsoft carries it with the fewest seams. *The customer is the better for it — because fewer seams is fewer outages, fewer bills, and a system that stays affordable as it scales.*

### A reading I want to do

**REID:** A reading. I want to recommend something on scannable-UI ergonomics, because the CFMP design commits to scan-first as the front door, and the design only holds if the scan ergonomics actually serve the customer in the moment of use. The argument I want to make with the reading is — the camera-first interaction has a literature, the literature is mature, and the design should be read against it.

**KEVEN:** Name it.

**REID:** Two options. The popular one — the Nielsen Norman Group on mobile camera UIs and scannable interfaces. Their work on barcode scanning ergonomics specifically — the latency budget between camera-up and barcode-resolved before users abandon, the importance of the haptic-and-visual confirmation pair, the failure mode where users assume the scan failed because the app did not acknowledge fast enough — is the right starting point for any team building a scan-first surface. Short, empirical, tells you what the user expects within four hundred milliseconds. The CFMP commitment to camera-auto-start and to the haptic-on-resolve is the literature-informed move.

**KEVEN:** And the more rigorous one.

**REID:** Apple's Human Interface Guidelines section on the camera. The HIG is opinionated, from the platform vendor, and captures the assumptions iOS users bring to a camera-bearing surface. CFMP Mobile runs on iOS Safari, and Sarah's archetype is on iOS more often than not. The HIG on permission prompts, the camera-active indicator, photo-capture privacy expectations, the difference between *the camera is on* and *the camera is recording* — all of those are constraints the design has to honor. Read it to understand the platform constraint. The design respects it.

**KEVEN:** Reid's recommendation lands. The scan ergonomics are not where the design is being novel; the design is borrowing from a mature literature and applying it to a new artifact — the agent fleet behind the scan. Same posture as the audit-substrate reading from Episode Two. *The chain is old. The application is new. The discipline is what makes the application work.*

### One disagreement

**REID:** One disagreement, framed the way Sarah would frame it. *Is Sarah really going to scan her pantry on a Tuesday night?* The customer who scans the yellow coupon in the diaper aisle is the customer the design exists for. That moment converts. The customer who, after dinner, opens the app and scans the empty milk carton to nudge Saturday's auto-replenish — *is that real, or is that a feature we imagine Sarah using because we want her to?* Because the pantry-inventory category has a fifteen-year graveyard. Every app that tried to get users to maintain a fridge model has been abandoned by month three. The in-store scan is real. *Is the home scan slideware?*

**KEVEN:** I'll concede the in-store scan is the demo. Sarah in the diaper aisle is in the cold open for a reason — that moment converts. The coupon-that-didn't-load is a friction every customer has felt, and the saving-that-appeared-in-three-seconds is the architectural payoff that lands on a sales call. The in-store scan is the opener.

**REID:** Now defend the home scan.

**KEVEN:** The home scan is the *retention bet*. Sarah at her kitchen counter on a Tuesday isn't looking for a new feature — she's taking thirty seconds to do something that turns the app from a transactional thing she pulls out at the store into a system that runs in the background of her household. The empty milk carton becomes a member of Saturday's delivery. The milk arrives. *Sarah never thinks about milk again.* The moment that *converted* Sarah was the in-store coupon save. The moment that *kept* Sarah twelve weeks later is the one where the milk shows up because she scanned a carton on a Tuesday and the system handled the rest.

**REID:** And the honest concession on adoption.

**KEVEN:** Conceded honestly. The pantry-scan adoption number in the first release is going to be low. The graveyard exists because users will not maintain a manually-built fridge model — one of the design experts on the project, Sofia Alvarez, said it cleanly to the team: *don't try to model the fridge; users won't keep it accurate; model the receipt and let the agent infer the rest.* The design took the lesson. The pantry auto-spawns from the confirmed delivery — so the receipt *is* the lot, and Sarah pays nothing to maintain it. The home scan, in the v1 design, is the *opt-in* on top of the auto-spawned pantry, not the foundation. The retention bet is that the customers who do opt in see enough lift to keep going — and the design is built to grow with the stay-trip and care-trip patterns, where the home-scan analogue is the bulk-scan when Marcus arrives at the cabin, or when Sarah arrives at her mother's house. *The moment is concrete and scoped enough that the customer will actually do it.*

**REID:** Converge.

**KEVEN:** Converging. *In-store SCAN is the demo opener. Home SCAN is the retention bet. Both ship.* The demo opens on the in-store moment because that's where the architectural payoff is most legible. The retention is the cumulative win across the home-scan, the stay-trip arrival scan, the care-trip recipient scan. The seller leads with the demo. The product earns its retention with the rest.

**REID:** Converge accepted. The seller's line — *the in-store scan opens the conversation; the home scan is the lock-in.* Carry it.

### What to carry forward

**KEVEN:** Three things into Episode Four. Each one a thing a non-technical leader can carry into a Monday meeting.

**KEVEN:** *One — the lot is the household's life, named.* Four customer moments — the shopping trip, the auto-replenish, the stay-trip, the care-trip. One lifecycle — thinking about it, coming to her, living with it, done with it. The lot is what the agent fleet acts on. The lot is what every record attaches to. The lot is what every surface composes against. *If the conversation drifts to a list or a cart, pull it back to the lot — because the lot is what the customer is actually doing.* Carry that.

**KEVEN:** *Two — SCAN hands the agent a fact, not a guess.* Sarah points her camera, the system returns the right product, the right coupon, the right recipe match, the right pantry capture. Never a string the agent has to improvise around. (Architecturally that's what the MCP boundary enforces.) *The answer is right the first time, and right the same way every time.* The household trusts the system because that property holds, even on the third Tuesday of the month when nobody is paying attention. Carry that.

**KEVEN:** *Three — concede capability; pivot to density.* All three major clouds can build CFMP. Microsoft happens to assemble it under fewer integration points — fewer seams, fewer bills, fewer dashboards, fewer skills the customer has to hire. The seller doesn't pitch *capability* — every architect has heard that pitch three times and is tired. The seller pitches the integration seams the customer has to maintain year after year, and earns the recommendation on density. *The customer is the better for it — because fewer seams is fewer outages and a system that stays affordable as it scales.* Carry that.

**REID:** Lot. Scan-as-fact. Productized density. Three carries. Into Episode Four.

**KEVEN:** Next episode — *Mobile · Trips, Replenish, and the home channel.* The Trip lifecycle in flight. Auto-Replenish as the lot the agent maintains. The home channel as the surface beyond the in-store moment. The UI revamp the Mobile team committed to in the Lots Expert Focus session. The surface, walked deeper.

[Sound: the closing sting. ~6 seconds.]

---

## Further reading

- **Source docs**
  - CFMP Mobile Design Document — `C:\code\iot_device\docs\packs\CFMP-Mobile-Design-Document.md` — §4 (Core Concepts, in particular §4.1 SIPO, §4.3 SCAN as the primary action, §4.4 LOTS as the unifying noun, §4.6 the Agent Fleet, §4.8 the APEX Audit Chain)
  - CFMP Mobile ScanFirst Design — `C:\code\iot_device\docs\packs\CFMP-Mobile-ScanFirst-Design.md` — §2 the SIPO principle, §3 the Scan-First Home, §4 what scanning produces (three modes unified at the API, the Scan Result Card), §5 the Sourcing & Equivalence engine, §7 the UC-63..UC-72 catalogue
  - CFMP Mobile Lots Expert Focus — `C:\code\iot_device\docs\packs\CFMP-Mobile-Lots-Expert-Focus.md` — §1 working definition and twelve-kind taxonomy, §1.1 lifecycle transitions, §4 lot lifecycle across the three contexts, §5 the UC-73..UC-100 catalogue, §11 the StayLot deep-dive
  - CFMP Mobile Use Cases — `C:\code\iot_device\docs\packs\CFMP-Mobile-Use-Cases.md` — the cited UCs (UC-29, UC-64, UC-66, UC-72, UC-74, UC-96) in full Cockburn format
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — the canonical deployment topology page. Open on a client call; the architecture argument is already on the screen.
- **Microsoft Learn**
  - Azure AI Foundry Agent Service — `https://learn.microsoft.com/azure/ai-foundry/agents/` — the productized agent runtime that hosts the orchestrator and the specialists
  - Microsoft Fabric OneLake — `https://learn.microsoft.com/fabric/onelake/` — the data-tier surface the Gold-view compositions ultimately rest on
  - Microsoft Purview Audit — `https://learn.microsoft.com/purview/audit-solutions-overview` — the productized audit substrate that catches the orchestrator's LedgerRow emissions
  - Microsoft Entra External ID — `https://learn.microsoft.com/entra/external-id/` — the identity surface that anchors the four-identity chain
- **Industry / research**
  - Nielsen Norman Group on mobile camera UIs and scannable interfaces — the latency budgets, the haptic-and-visual confirmation pair, the abandonment patterns when the system misses the four-hundred-millisecond budget; the empirical baseline for any scan-first surface
  - Apple Human Interface Guidelines — the Camera section — `https://developer.apple.com/design/human-interface-guidelines/camera/` — platform constraints on permission prompts, the camera-active indicator, photo-capture privacy expectations the CFMP Mobile PWA respects on iOS Safari
  - Retail-environment cognitive-load research on barcode scanning — the family of academic work from Carnegie Mellon HCII, Stanford d.school, and MIT Media Lab on the difference between lab-environment scans and in-store scans competing with everyday cognitive distraction; informs the split between bulk-scan mode at the kitchen counter and single-scan-with-haptic mode in the aisle
- **Sibling series cross-reference** — Cross-Cloud Agentic Episode 05 (*Audit, Ledger, and Replay — The Trust Substrate*) at `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\05-audit-ledger-and-replay.md` — the framework-level treatment of the audit pattern that the MCP boundary on Mobile inherits

— end of episode 03 —
