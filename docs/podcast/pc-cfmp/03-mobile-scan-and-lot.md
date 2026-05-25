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

**KEVEN:** Start with the noun. Because if I had to defend one architectural decision in CFMP across every audience — the team, the seller, the architect on the other side of the table — it is this one. The system organizes itself around the lot. Everything else stair-steps from there.

**REID:** Define it. Carefully. Not the version you put on a slide. The version that survives an architecture review.

**KEVEN:** Carefully. A lot is *a bounded set of intents about commerce in a household over a window of time*. Bounded — it has edges. Intent — what the household *means* to do, not just what it has done. Commerce — the buying-and-consuming domain. Household — the boundary of ownership, because grocery is a household sport. Window of time — every lot has a lifecycle.

**REID:** And the structural properties.

**KEVEN:** Four. Identity — every lot has a stable identifier, a kind, optionally a user-given label. Audit — every state change, every membership change, every transition is a row in the substrate we walked last episode. Membership — products belong to lots; quantities and per-item state at the lot level, not as orphaned line items floating in a transaction blob. And lifecycle — the lot moves through states, and the state machine is the same regardless of kind. The kinds vary; the lifecycle is constant.

**REID:** And the four lifecycle states.

**KEVEN:** Four states. *Draft* — the lot exists, the user or the agent has named the intent, but the lot has not yet acted on the world. The Sunday-morning meal-plan-becoming-a-list. The peanut-free birthday EventLot before anyone has tapped buy. *In-flight* — the lot has committed. The cart has checked out, the pickup is staged, the delivery is on a truck, the auto-replenish has placed the order, the StayLot's first leg of pre-stocking is en route to the cabin. *Settling* — the goods have arrived, the household is consuming them, the receipt has spawned a PantryLot whose items are working through breakfasts and lunches and dinners. *Closed* — archived. Either consumed cleanly, thrown out, or carried over into the next lot. The lot has handed off its remainder and stopped accepting new intent.

**REID:** Draft, in-flight, settling, closed. Now I press. Why "lot." Why not "list." Why not "cart." Why not "basket," which is what the customer says out loud in the parking lot.

**KEVEN:** A list is a snapshot. It captures what I am thinking about at the moment I write it down. No identity after I close the notes app. Doesn't know whether I bought what was on it. Doesn't know whether what I bought got consumed. A frame in a movie; not the movie. A cart is a transaction. It closes the instant the payment processor returns. It doesn't know whether the pickup happened, whether the substitution was accepted, whether the romaine wilted before anyone made the salad. The act of buying; not the act of having bought. A basket — and I take the term seriously because the customer speaks it — has no audit trail across surfaces. The basket in the loyalty app, the basket in the delivery app, and the basket in the meal-plan app are three different baskets, none of which know about each other. The basket is what the customer wishes existed; not what any system implements.

**REID:** And the lot.

**KEVEN:** The lot is the noun that survives all three. Identity outliving the list, audit trail outliving the cart, cross-surface coherence the basket can finally cash in on. The list is a query against the lot. The cart is a transaction against the lot. The receipt is a stamp against the lot. The pantry is what the lot turned into. The next meal plan is a query against what the lot left behind. The lot is the noun the agent fleet acts on, because the fleet needs an artifact with identity, audit, and membership to act safely.

**REID:** Two use cases by name. Concrete. So the listener can hold the noun in their head.

**KEVEN:** *UC-91 — create a PlanLot from shop-this-plan on the active meal plan.* Sarah on a Sunday morning, the agent composes a seven-day meal plan, she taps *shop this plan,* and the system spawns a PlanLot. Draft. Auditable. Membership-bearing. The state machine handles the transition to CartLot at checkout. The audit chain records parentage with the `derived_from_lot_id` field — the CartLot knows the PlanLot it came from, the PickupLot or DeliveryLot knows the CartLot, and so on. The trace is end to end. *UC-95 — checkout a CartLot, transition to PickupLot for BOPIS or DeliveryLot for delivery, parentage chain preserved.* The state-machine transition is the audited move. The kind changes. The parentage holds.

**REID:** And the agent fleet acts on those lots. Trips owns the shopping-trip lifecycle and reads the CartLot becoming the PickupLot becoming the PantryLot. Replenish owns the SubscriptionLot. Coupons composes against any lot. Pharmacy operates inside the CareLot. Concierge reasons over the active lots to decide whether to nudge. Every specialist has the lot in front of it as the noun of work. None of them has a list or a cart. They have lots.

**KEVEN:** The architecture commitment is that the lot is the unit of work *everywhere*. If one corner of the system treats a lot as a list, the value of the noun collapses. The discipline is non-trivial. The payoff is what the rest of the episode walks.

### The four lot archetypes

**KEVEN:** Now the archetypes. We named four in Episode One. Today we go deeper — the customer moment for each, then the architectural distinction. Because the four are not four flavors of the same lot. The four exercise different parts of the state machine, different ownership models, different audit scopes, different policy surfaces. The archetypes are *forcing functions* for the architecture.

**REID:** Walk them.

**KEVEN:** First. *Shopping Trip.* The canonical lot. In-store or delivery, in-flight while the customer is transacting. Sarah on a Saturday morning, the pickup window opens at ten, the lot moves from draft when she compose-and-pays on Friday night, to in-flight when the picker walks the aisles, to settling when the bags hit the trunk, to closed when the PantryLot it spawned starts depleting. The architectural distinction — the Shopping Trip exercises *transition density.* Every state has live operational meaning. The customer needs prep state in flight. The picker needs substitution-approval signals from the customer in flight. The store needs handoff confirmation at settling. The Shopping Trip justifies the live-operational-state surfaces — the prep-state field on the PickupLot card, the *packed by 10:42* timestamp on the Lots Strip, the interactive substitution flow in UC-82. The state machine has to be real, not decorative.

**REID:** Second.

**KEVEN:** *Auto-Replenish.* The recurring lot the customer almost never opens. The agent maintains it. Sarah set up milk, bread, diapers, eggs, coffee, and the kid's cereal as auto-replenish six months ago; now those items show up on a cadence the Replenish specialist computes from household consumption signals. The customer-moment is the *absence* of a moment — Sarah notices only when something goes wrong, or when the agent surfaces a skip-decision nudge. The architectural distinction — Auto-Replenish lives at the boundary of *agent ownership.* The agent is the primary actor; the customer is the consenter and the occasional override. The audit scope captures the agent's reasoning at every cadence step — why this week, why this quantity, why this substitution — because the customer's trust depends on being able to ask, six weeks later, *why did you order me four gallons of milk on the week we were on vacation?* The substrate has to answer. Auto-Replenish is where the per-action audit row most clearly earns its rent.

**REID:** Third.

**KEVEN:** *StayLot.* The trip-driven lot. Marcus Thompson and four friends rent a cabin for a long weekend, and the lot follows them. The customer-moment is the absence of *the first two hours of vacation spent at a grocery store* — staples twenty-four hours before check-in, a cold leg within two hours of check-in, a mid-stay top-up the morning of day two. Multi-leg. Multi-actor. Friend co-editing. The architectural distinction — StayLot exercises *displacement.* The household is not a fixed address. The delivery target is temporary. Collaborators may not all be loyalty members. The state machine supports multi-leg fulfillment as first-class — three DeliveryLots derived from one StayLot, with leg-numbered audit rows, with property-tokenized delivery targets so the backend never aggregates against the host's address.

**REID:** Fourth.

**KEVEN:** *CareLot.* The cross-household lot. The diabetic-friendly snacks shipped to Sarah's mother's address, paid on Sarah's card, audit-attributed to Sarah-acting-on-behalf-of-mother, with the consent boundary blocking the mother's pharmacy refills from crossing into Sarah's view. The customer-moment is *delegation under constraint* — Sarah can reorder the snacks; Sarah cannot see what her mother takes at bedtime. The architectural distinction — CareLot exercises *the four-identity chain.* The audit row carries the agent identity, the operator identity, the source identity, and the auditor identity. HIPAA-aware when the recipient has prescriptions; the Pharmacy specialist enforces redaction at the agent layer, the consent ledger records the delegation, the row records the cross-identity action. Without CareLot the substrate could be lighter. With it the substrate is exactly what Episode Two unpacked.

**REID:** Four archetypes. Shopping Trip exercises the state machine. Auto-Replenish exercises agent ownership. StayLot exercises displacement. CareLot exercises the four-identity chain. Each one *forces* a part of the architecture. Drop any one of them and the architecture contracts to a smaller shape than it has to be. Keep all four and the architecture has to be the shape the design document commits to. The archetypes are not features. The archetypes are constraints on the substrate.

**KEVEN:** Said cleanly. The architecture is the answer to the archetypes. Not the other way around.

### The SCAN interaction

**KEVEN:** Now the verb. Because if the lot is the noun, the scan is what the customer *does* — the interaction that defines what the surface feels like, the interaction the home screen of the Mobile PWA is dominated by.

**REID:** Scan-first versus search-first. Walk it.

**KEVEN:** Most retail apps lead with search. A search box at the top, a category grid below it, a deals carousel at the bottom. The user is expected to know what they want, type it, and pick from a results list. CFMP leads with scan. The home screen opens directly on the camera viewport, the camera auto-starts on app open with cached permission, the user does not have to tap *scan* to begin — the scan is the default state of the surface. The chat composer is a thin secondary strip below the viewport. Search is a fallback inside the composer, not a peer surface. The bottom nav collapses to three tabs — Home, Lots, Me — to avoid pulling the user away from the camera.

**REID:** And the ScanFirst design document commits to this verbatim. I want you to read the design decision word for word, because the strength of the architectural claim depends on the design having actually said it.

**KEVEN:** Reading it verbatim. From the ScanFirst design document, section two, the SIPO principle row labelled *one primary action.* Quote — *The home screen is dominated by a camera viewport. Tapping scans. No other affordance competes for primacy.* End quote. That is a design commitment, not a suggestion. The home screen is dominated by the camera. There is no other primary affordance. The chat composer exists, the Lots Strip exists, the bottom nav exists — but none of them is the primary action. The primary action is scan. The system has already chosen for the user.

**REID:** And the four things that get scanned.

**KEVEN:** Four things, deliberately broad. *A UPC barcode on a product.* Sarah holds a box of pasta, points the camera, the BarcodeDetector resolves the GTIN-13, the resolver returns the canonical product entity. *A coupon barcode on a shelf.* The yellow rail-mounted coupon from the cold open. The retailer's coupon catalogue composed against the household's loyalty memberships at the MCP layer, the saving on the Scan Result Card before the customer reaches checkout — instead of a marketing-domain web page on a cellular dead zone. *A QR code on a recipe card.* The QR resolves to a RecipeLot, ingredients pre-composed against the household's pantry, missing items handed to the Catalog specialist. *A photo of a label* for products without a barcode. The farmers'-market jar of jam Sarah picked up on Saturday. The user taps to capture a still, the image goes through Azure Computer Vision OCR plus the Catalog specialist's LLM identification, and the jam becomes a member of the PantryLot it should have been in all along.

**REID:** Four scan modes. Unified at the API. The mobile does not distinguish. The system resolves through strategies in order — barcode-detect first, then QR-anchor, then OCR-and-LLM fallback. Zero-decision entry. *Simple in. Powerful out.*

**KEVEN:** And every one of those four is a *fact* handed to the agent fleet. The canonical product comes back through the MCP boundary as a structured object, not a string. The coupon comes back as a Gold-view composition that already factored the loyalty memberships, not a URL. The recipe comes back as a RecipeLot with members, not a wall of text. The jam comes back as a resolved canonical product. The scan is the trigger. The agent composes downstream. The fact is what makes the composition trustworthy.

**REID:** And the obvious push. *Isn't this just a barcode reader?* Every grocery app has had one since twenty-fourteen. Yuka does barcode resolution. Google Lens does product identification. What is CFMP doing that those do not?

**KEVEN:** CFMP treats the scan as *the front door to an agent fleet*, not as a feature in a feature menu. Yuka tells you what the product is. Lens tells you where to buy it. Neither composes against your household's loyalty memberships, your pantry, your dietary policy, your active meal plan, the recall feed, your active StayLot, your CareLot delegation, and your auto-replenish history all in one pass — because neither has an agent fleet behind the scan. CFMP does. The scan hands the agent a *known entity*, and the Coupons specialist, the Catalog specialist, the Pharmacy specialist when the entity is regulated, the Concierge specialist when it triggers a moment, all compose against that entity in parallel. The Scan Result Card surfaces the smart default. The scan is one tap. The composition behind it is the work of the fleet.

**REID:** And the architectural argument I want to land. *The scan is the front door because the front door has to hand the agent a known entity, not a string.* If the front door is a search box, the agent receives a string and has to guess. Guesses fail. Guesses hallucinate. Guesses are the failure mode of every chat-first retail surface that ever shipped. The scan is the front door because the scan returns a fact. The MCP boundary is what makes the scan a fact. Which is the next section.

### The MCP boundary on Mobile

**KEVEN:** The MCP boundary. We walked it in general terms in Episode Two. Today we walk it on Mobile specifically — because the Mobile surface is where the customer's hand meets the architecture, and where the architecture argument either holds or leaks.

**REID:** Restate the principle in plain language for the listener who skipped Episode Two.

**KEVEN:** Every action a Mobile agent takes hits a composed Gold view, never a raw source. The Gold view is the contracted, governed, per-scenario business model — the shape the agent is allowed to see. The MCP server — Model Context Protocol — is the typed, audited interface between the agent and the Gold view. The agent issues a tool call. The MCP server validates the call against the contract. The MCP server composes the Gold view from Silver canonical state. The MCP server returns a structured result and stamps an audit row. The agent does not get to query Silver directly. The agent does not get to write SQL. The agent does not get to invent a tool name and have it succeed. The boundary is a runtime property, not a documentation artifact.

**REID:** Walk one end-to-end path. The cold-open path. The scan-coupon path. Step by step.

**KEVEN:** Sarah is in the diaper aisle. She points the camera at the yellow coupon. The Mobile PWA's BarcodeDetector resolves the barcode locally. The Mobile posts to the orchestrator at `ca-visionkit-orchestrator` with the barcode, the household's `member_number`, a Mobile-minted trace identifier, and the `X-User-Action` header naming the UC. The orchestrator's auth middleware verifies the Entra token. The orchestrator routes the intent to the Coupons specialist. The Coupons specialist composes a tool call against the Gold-view-for-coupons through the MCP server. The MCP server validates the call — specialist permitted, tool exists, household has consented, trace identifier present. The MCP server composes the Gold view by joining the household's loyalty memberships across linked retailers with the retailer's coupon catalogue, filtered by Sarah's dietary policy and her active lots. The Gold view returns a structured result — matching coupon, saving amount, redemption window, channel cue. The MCP server stamps the audit row. The Coupons specialist returns the saving. The output-safety classifier validates the response. The Mobile renders the Scan Result Card with the saving as the primary action — *apply this coupon, save one dollar at checkout* — and the haptic confirmation fires.

**REID:** And the audio cue.

**KEVEN:** The Concierge specialist, in parallel, decides whether the moment warrants a Sonos cue. In Sarah's case — in the store, on her phone, saving already on the screen — the answer is no. If Sarah had been at home, finishing a meal plan, and the same coupon had matched against a planned item in tomorrow's pickup, the Concierge would have queued the cue. Episode Six — the Sonos channel — takes the audio leg. Today is the visual leg, on Mobile, end to end. The customer sees a saving on a card. The customer never sees the seven services, the four data tiers, the two specialists, the consent check, the audit row, the trace identifier, the Gold composition, the loyalty-membership join. The architecture absorbs the complexity. The customer sees the win.

**REID:** And the harder argument. *This is where the architecture argument lives — not in the agent code but in the boundary.* The agent's prompt is interesting; the agent's reasoning is interesting; the model version is interesting. None of that is the architecture. The architecture is the property that the agent *cannot* see the raw source, cannot compose SQL, cannot invent a tool name, cannot bypass the contract — by construction, at the runtime layer, enforced by the credential boundary and the registered toolkit and the MCP server's validation. The contract is what the seller defends in front of a CIO who has been burned by generative AI hallucinating against a production database. The contract is what the regulator inspects when she asks, *what did the agent have access to.* The contract is the architecture.

**KEVEN:** Conceded. The agent code is not the moat. The boundary is the moat. The agent code can change every quarter — a model deprecates, a prompt evolves, a specialist gets re-tuned — and the architecture holds, because the boundary holds. CFMP picked the boundary first, and built the agents inside it. The wrong order — agents first, boundary retrofitted — produces the agentic systems that fail their first audit.

### Six UCs at the centre

**KEVEN:** Now the use cases. I want to pull six SCAN and LOT use cases from the Mobile Use Cases catalogue by their real numbers, name the customer moment in one line, and name the architectural touchpoint each one exercises. So the listener can carry the catalogue with them, instead of carrying a vague impression.

**REID:** Six. Real numbers. Move.

**KEVEN:** *UC-64 — scan a product.* Customer moment — Sarah holds a box of pasta in aisle nine and points her phone at the barcode. Architectural touchpoint — the front door. The BarcodeDetector runs locally; the resolver hits the MCP boundary; the canonical product entity comes back as a fact; the Scan Result Card renders. This is the UC the entire Scan-First design rests on. Every other scan UC composes from this one.

**KEVEN:** *UC-66 — render the Scan Result Card with context-aware primary action.* Customer moment — the card appears, the primary action is *add to cart* because Sarah is in the store, or *adjust auto-replenish* because Sarah has bought this before, or *find equivalent* because Sarah's linked store does not carry it, or *allergen warning* because the product violates her household's dietary policy. Architectural touchpoint — the Catalog specialist's smart-default selection, executed inside the MCP boundary, output-safety-classified before render. This is the UC where the agent fleet's value is most legible to the customer — the *one tap saves the right thing.*

**KEVEN:** *UC-72 — add a scanned product to list, auto-replenish, or pickup lot.* Customer moment — Sarah taps the primary action on the card and the item lands on the active lot in one tap. Architectural touchpoint — the scan-to-lot bridge. The scan returns a canonical product; the customer's tap commits a lot membership; the LedgerRow records the membership change with parentage to the scan. The continuity from front door to lot is what makes the lot live as a noun across the surface.

**KEVEN:** *UC-29 — clip a coupon — instantiated as the scan-coupon path from the cold open.* Customer moment — Sarah scans the yellow rail-mounted coupon, the saving lands on the card, the coupon is clipped to her loyalty account, the redemption is queued against the next eligible transaction. Architectural touchpoint — the Coupons specialist composing a Gold view across the household's loyalty memberships, returning the match through the MCP boundary, stamping the audit row, surfacing the saving as the primary action. The cold open's six-dollar miss becomes a one-dollar save, instead of a marketing-domain web page that does not load on bad cellular.

**KEVEN:** *UC-74 — bulk scan-in a non-CFMP haul to create a PantryLot.* Customer moment — Sarah is at the kitchen counter on a Saturday, unloading the haul from the farmers' market, the warehouse-club run, the corner market, the things that did not come through CFMP. She opens the app, taps the bulk-scan affordance, and runs the camera across each item one after another — no Scan Result Card between scans, no confirmation taps, just the camera and the haptic confirming each capture. The session closes when she taps done, and the ScanLot it created spawns a PantryLot the agent fleet now knows about. Architectural touchpoint — bulk scan mode as the bridge for non-CFMP commerce into the audited inventory. Without this UC, the PantryLot is only as complete as what flowed through CFMP. With this UC, the PantryLot is as complete as the customer takes the sixty seconds to make it.

**KEVEN:** *UC-96 — bind a StayLot to a vacation-rental property.* Customer moment — Marcus Thompson pastes the iCal URL from his cabin booking into CFMP. The StayLot creates itself, bound to the property identifier and the date range. Architectural touchpoint — the displacement archetype made concrete. The lot has a delivery target type of `rental_property`, a delivery target reference tokenized to the platform listing, a stay-start and stay-end date, a collaborators array Marcus can invite his friends into. The state machine handles the multi-leg fulfillment downstream — UC-99 schedules the staged deliveries, UC-100 closes out the stay with leftover handling. UC-96 is the seed. Every other StayLot capability composes from this one.

**REID:** Six UCs. Real numbers from the catalogue. *UC-64, UC-66, UC-72, UC-29, UC-74, UC-96.* Front door, smart default, scan-to-lot bridge, coupon composition, bulk inventory bridge, displacement seed. Every other SCAN and LOT use case in the catalogue — and the catalogue has more than a hundred of them — composes from these six. The listener should carry the six. The catalogue is the rest.

**KEVEN:** Said cleanly. The six is what the seller demonstrates. The catalogue is what the engineer ships.

### The honest comparison

**KEVEN:** Now the comparison. Because CFMP is built on Microsoft, and this is the CFMP Podcast, and we are not going to pretend the lot model and the scan-first interaction are exclusive to one cloud. The credibility of the rest of the series depends on the honesty of this section.

**REID:** Walk it. AWS first. GCP second. Microsoft last. Be honest.

**KEVEN:** AWS first. AWS could implement the lot model. Postgres or Aurora for the schema. Bedrock Agents for the fleet — capable, mature, productized. The Mobile is a PWA on Container Apps or ECS Fargate. The MCP boundary on Lambda or Fargate, with IAM enforcing credentials and Lake Formation governing the data plane. The audit substrate lands in CloudTrail at the platform layer and in Aurora for the application LedgerRow, with S3 Object Lock as the WORM tier and Audit Manager as the auditor's view. The four-identity chain composes through Cognito and IAM. CareLot redaction composes through Macie and Lake Formation row-level security. *It works. It ships.* AWS would assemble it from Bedrock plus Lake Formation plus Cognito plus Macie plus CloudTrail plus Audit Manager plus S3 Object Lock — six to twelve weeks in a competent platform team.

**REID:** GCP.

**KEVEN:** GCP. Vertex AI Agent Engine for the fleet — capable, mature, productized. Cloud SQL for the schema. The MCP boundary on Cloud Run with Workload Identity enforcing credentials and Dataplex governing the data plane. The audit substrate lands in Cloud Audit Logs at the platform layer — and Cloud Audit Logs has a real GCP advantage worth naming, write-once-immutable as a platform property, not an add-on — and in Spanner for the application LedgerRow, with Security Command Center as the posture surface. Cloud Identity for the four-identity chain. Sensitive Data Protection — formerly Cloud DLP — for CareLot redaction. *It works. It ships.* Same six to twelve weeks.

**REID:** And Microsoft.

**KEVEN:** Microsoft. Azure AI Foundry for the agent fleet. Container Apps for Mobile, Portal, orchestrator. Postgres Flexible Server for the schema. The MCP boundary on the orchestrator with Entra enforcing credentials and Fabric OneLake governing the data plane. The audit substrate lands in Purview Audit at the platform layer and in Postgres for the application LedgerRow with WORM retention; Purview's DSPM for AI catches AI-relevant classification. Entra for the four-identity chain. DSPM for AI plus Purview Information Protection plus the Pharmacy specialist's isolated Postgres tenancy for CareLot redaction. *It works. It ships.* Microsoft assembles fewer integration points because Foundry, Purview, and Entra are productized as one console with one bill and one identity surface.

**REID:** The seller's pivot.

**KEVEN:** *The Microsoft win is productized density.* One product for the agent fleet — Foundry. One for the audit substrate — Purview. One for identity — Entra. AWS would assemble seven productized services, GCP six, Microsoft three. *Not capability — both other clouds have the capability.* The difference is the assembly tax — build cost of integration, operate cost of multiple identity surfaces, audit-firm-credibility cost of assembling evidence across multiple consoles. The seller does not pitch capability — every architect has heard that pitch from three clouds and is tired of it. The seller pitches density — fewer seams, fewer bills, fewer dashboards, fewer skills to hire — and defends on the assembly tax.

**REID:** *Concede that all three clouds can build the lot. The seller earns the recommendation on density.* That is the line. It survives an architect from AWS or GCP in the room — because it does not deny their capability. It concedes capability and pivots to the cost axis the customer actually pays. *The architecture decides; the cloud follows.* CFMP committed to Microsoft because productized density compresses the seams the CareLot, Auto-Replenish, StayLot, and Shopping Trip all depend on. Other clouds carry the design. Microsoft carries it with fewer seams.

### A reading I want to do

**REID:** A reading. I want to recommend something on scannable-UI ergonomics, because the CFMP design commits to scan-first as the front door, and the design only holds if the scan ergonomics actually serve the customer in the moment of use. The argument I want to make with the reading is — the camera-first interaction has a literature, the literature is mature, and the design should be read against it.

**KEVEN:** Name it.

**REID:** Two options. The popular one — the Nielsen Norman Group on mobile camera UIs and scannable interfaces. Their work on barcode scanning ergonomics specifically — the latency budget between camera-up and barcode-resolved before users abandon, the importance of the haptic-and-visual confirmation pair, the failure mode where users assume the scan failed because the app did not acknowledge fast enough — is the right starting point for any team building a scan-first surface. Short, empirical, tells you what the user expects within four hundred milliseconds. The CFMP commitment to camera-auto-start and to the haptic-on-resolve is the literature-informed move.

**KEVEN:** And the more rigorous one.

**REID:** Apple's Human Interface Guidelines section on the camera. The HIG is opinionated, from the platform vendor, and captures the assumptions iOS users bring to a camera-bearing surface. CFMP Mobile runs on iOS Safari, and Sarah's archetype is on iOS more often than not. The HIG on permission prompts, the camera-active indicator, photo-capture privacy expectations, the difference between *the camera is on* and *the camera is recording* — all of those are constraints the design has to honor. Read it to understand the platform constraint. The design respects it.

**KEVEN:** Reid's recommendation lands. The scan ergonomics are not where the design is being novel; the design is borrowing from a mature literature and applying it to a new artifact — the agent fleet behind the scan. Same posture as the audit-substrate reading from Episode Two. *The chain is old. The application is new. The discipline is what makes the application work.*

### One disagreement

**REID:** One disagreement. The one I want on tape.

**KEVEN:** Put it on tape.

**REID:** *Scanning at home is product fluff. Nobody wants to scan their own pantry. The in-flight in-store scan is the demo opener. The home scan is over-engineered.* The customer who scans the yellow coupon in aisle eleven is the customer the design exists to win. The customer who scans the empty milk carton on a Tuesday evening to add milk to Saturday's Auto-Replenish lot is the customer the design imagines exists. The first one is real. The second one is wishful thinking. Bulk scan-in is a feature in search of a moment.

**KEVEN:** I will concede the in-store scan is the demo. The cold open opened on Sarah in the diaper aisle for a reason — that moment converts. The coupon-that-did-not-load is the friction every customer has felt, and the saving-that-just-appeared is the architectural payoff that lands in three seconds on a sales call. The in-store scan is the opener. I will give you that.

**REID:** Now defend the home scan.

**KEVEN:** Defending it. The home scan is the *retention loop*. The customer who scans the empty milk carton on a Tuesday is not a customer in search of a feature. The customer is taking thirty seconds to do something that turns the app from a transactional surface into a managed system. The empty carton becomes a member of the Auto-Replenish lot for Saturday's delivery. The milk arrives. The customer never thinks about milk again. The moment that converted Sarah was the in-store coupon save. The moment that *kept* Sarah is the one where the milk just shows up because she scanned the carton on a Tuesday and the system handled the rest. The in-store scan is the demo opener. The home scan is the retention bet.

**REID:** And the data. Real adoption numbers on home scanning. Because every consumer pantry-inventory app for the past fifteen years has tried to get users to scan their pantry, and every one of them has had abandonment rates that should make the design wary.

**KEVEN:** Conceded honestly. The home-scan adoption number for v1 is going to be low. The pantry-inventory category has a graveyard, and the graveyard exists because users will not maintain a manually-built fridge model. *Sofia Alvarez* in the Lots Expert Focus panel — the design captures her directly — *do not try to model the fridge; users will not keep it accurate; model the receipt and let the agent infer the rest.* The design takes the lesson. The PantryLot auto-spawns from the confirmed delivery or pickup — UC-73 — so the receipt is the lot, and the customer pays nothing to maintain it. The bulk-scan-in UC-74 is the bridge for the haul that did not come through CFMP. The home scan, in the v1 design, is the *opt-in* on top of the auto-spawned PantryLot, not the foundation. The retention bet is that the customers who do opt in see enough lift to keep the behavior, and the design is built to grow with the StayLot pattern — the cabin pre-stock, the parent's-house care delivery, the friend's-house party — where the home-scan analogue is the bulk-scan on arrival, and the moment is concrete and scoped enough that the user will actually do it.

**REID:** Converge.

**KEVEN:** Converging. *In-store SCAN is the demo opener. Home SCAN is the retention bet. Both ship.* The demo opens on the in-store moment because that is where the architectural payoff is most legible. The retention is the cumulative win across the home-scan path, the StayLot bulk-scan-on-arrival path, the CareLot bulk-scan-at-the-recipient's-pantry path. The design ships both. The seller leads with the demo. The product earns its retention with the rest. Neither is fluff. Each has a job.

**REID:** Converge accepted. The line for the seller — *the in-store scan opens the conversation; the home scan is the lock-in.* Carry it.

### What to carry forward

**KEVEN:** Three things into Episode Four. Numbered, because the listener carries them.

**KEVEN:** *One — the lot is the noun.* Four archetypes. Shopping Trip, Auto-Replenish, StayLot, Care-Lot. One state machine — draft, in-flight, settling, closed. The lot is the artifact every agent in the fleet acts on. The lot is the artifact every audit row attaches to. The lot is the artifact every customer surface composes against. Every conversation about CFMP returns to the lot. If the conversation drifts to a list or a cart, pull it back to the lot. Carry that.

**KEVEN:** *Two — SCAN hands the agent a fact, not a guess.* The MCP boundary is what makes the scan a fact. The agent receives a canonical product entity, a composed coupon view, a resolved RecipeLot, an OCR'd label match — never a string the agent has to interpret. The scan is the front door because the front door has to hand the agent a known entity. The boundary is what makes the guess unavailable. The boundary is the architecture. Carry that.

**KEVEN:** *Three — the seller's pivot is productized density.* Foundry, Purview, Entra. Three productized services where AWS would assemble seven and GCP would assemble six. The architecture decides; the cloud follows. CFMP committed to Microsoft because the productized density compresses the integration seams the CareLot, the Auto-Replenish lot, the StayLot, and the Shopping Trip all depend on. The seller does not pitch capability — every other cloud has the capability. The seller pitches density and defends it on the assembly tax. *Concede that all three clouds can build the lot; the seller earns the recommendation on density.* Carry that.

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
