# Episode 07 · Fulfillment · The Plug-In Tier

**Episode 07 · Fulfillment · the plug-in tier** — Sarah's Sunday morning, three different sources for one weekly plan, one tap. Three quotes return in parallel. The agent recommends a split. Three orders flow. Three hours later, an out-of-stock event arrives mid-fulfillment; the substitution sheet lets her one-tap the safe alternative. We open on the moment the agent fleet stops being theoretical and starts buying things on Sarah's behalf. Then we walk why a plug-in tier is an architectural move, the FulfillmentProvider ABC, the ProviderQuote shape, the quote-aggregator fan-out, the recommendation score, the dietary-safety enforcement at the search step, the Azure-native deployment of the sixth FastMCP server, and the discipline that mocks are real architecture rather than a stepping stone.

**Builds on:** the show bible (00-show-bible-and-format) · Episode 01 (Sarah's Day) · Episode 02 (Agent fleet & audit chain) · Episode 03 (Mobile · SCAN & LOT) · Episode 04 (Mobile · Trips, Replenish, and the home channel) · Episode 05 (Portal · operator console and B2B multi-tenant) · Episode 06 (Sonos · the ambient voice channel) · CFMP Fulfillment Design Document §§1–10 in full · CFMP Fulfillment UC Catalog · CFMP Fulfillment Roadmap
**Run time:** ≈ 40 minutes target
**Last updated:** 2026-05-25

---

## Cold Open

[Sound: a Sunday morning kitchen at nine-fifteen. The low background hum of a refrigerator coming off a cycle. A coffee maker working through the last of its drip cadence. The soft clink of a ceramic mug being set down on a quartz counter. A child somewhere upstairs, awake but not yet down; the unmistakable cadence of a tablet game muted but still audible through a closed door. Sun on the floor through a window that has not been cleaned in three weeks.]

It is nine-fifteen on a Sunday morning, and Sarah Chen is at the kitchen island with the meal-planner open on her phone. The plan for the week is composed — five dinners, two lunches Thursday because of the school party, the usual breakfasts. The plan needs gochujang. Her store doesn't stock the gochujang. The school party is peanut-free; her eight-year-old's classmate has the allergy, and the snack list went home Friday in the backpack. There is a bag of romaine on sale at the same-day delivery provider she has used before. Three different sources, three different delivery patterns, normally three different apps and forty-five minutes of friction.

She taps **"ship this plan"** once.

The screen renders a spinner for less than four seconds. Three quotes return in parallel. The pickup option is free, with a window the next morning at ten; all fourteen items are in stock. The same-day delivery is sixty minutes out, nine ninety-nine fee, ninety-five percent in stock — the gochujang is the one flagged unavailable. The warehouse-club delivery is ninety minutes out, eleven ninety-nine fee, ninety-nine percent in stock. The agent's recommendation surfaces above the three, and the headline move is that it is a *split across pickup and delivery* in one decision surface: *"pickup the bulk of the plan tomorrow morning at no fee because it is the cheapest leg and everything is in stock; gochujang via the warehouse-club delivery tonight because you said you are cooking with it; the school snacks via the same-day delivery because that is where they are cheapest."* The reason renders below the recommendation in eight words: *"Cheapest by ten dollars and one hundred percent in stock."*

Sarah taps confirm. Three orders flow.

Three hours later, just before noon, her phone buzzes. *"Heads up — the same-day delivery is out of the gochujang you asked for. Want the same brand from a different shopper, a different brand, or a refund?"* Three chips on the sheet. One labeled *skip the decision — agent will choose*. Sarah taps the same-brand alternative. The provider acks. The row goes to the ledger. The dinner is back on the calendar.

[Sound: a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start on the four-second spinner. Because what happens in that four seconds is the whole architectural argument for this episode. Sarah's one tap fans out to three providers in parallel. Three quotes return. The agent ranks them. The recommendation lands with an eight-word reason. None of that is theoretical. All of it is happening inside one FastMCP server, three plug-in classes, one orchestrator, one audit chain.

**REID:** And this is the surface where the agent fleet stops being theoretical and starts buying things on Sarah's behalf. Through Episode Six, the fleet has been writing answers and rendering them. From this episode forward the fleet places orders, moves money, commits the customer to a transaction with a third-party logistics network we do not control. That is a different kind of surface. It deserves a different kind of architectural discipline.

**KEVEN:** Welcome back to the CFMP Podcast. Episode Seven. *Fulfillment · the plug-in tier.* Episode Six's carry-forward was the Cue Bus reuse for fulfillment status events. Today we open the plug-in tier. Eight sub-sections. Why a plug-in tier is an architectural move. The FulfillmentProvider ABC and the ProviderQuote shape. The quote-aggregator fan-out. The recommendation score. The substitution flow with dietary safety enforced at the search step. Online order pickup as a peer fulfillment shape alongside delivery. The Azure-native deployment of the sixth FastMCP server. And the discipline that v1 mocks are real architecture.

**REID:** A reading, a disagreement, three carries. Let's go.

---

> **Reader honesty admission:** the seven sub-sections that follow describe the **CFMP Fulfillment plug-in tier as designed**, not as it ships today. As of 2026-05-25, the live `/architecture` page lists five MCP servers — `parsml · cxml · merml · weather · ledger` — and **no `fulfillment-mcp`**. The episode walks the design; the sprint roadmap (see `CFMP-Fulfillment-Sprint-Orchestrator.md`) names the work to make it real. The substitution flow, the provider ABC, the BOPIS + pharmacy gate — every architectural decision discussed here is honest; the implementation is the next sprint.

## What ships today vs. what's planned

> **Episode honesty calibration · 2026-05-25**
> This episode covers the Fulfillment plug-in tier — provider ABC, quote-aggregator fan-out, recommendation scoring, substitution with dietary-safety-at-search, BOPIS as a peer fulfillment shape, and the Azure-native deployment of a sixth MCP server. The podcast walks the architecture as designed. Phase 1 live, Phase 2 planned, and v2 vision are distinguished below so the listener (and the seller) walks in knowing the score. The CFMP Capabilities Map at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` is the authoritative live-state source.

**Phase 1 live (today):** none — this entire episode is Phase 2 design.

**Phase 1 partial / in-progress:** Mobile `/api/fulfillment/*` route stubs (no live MCP server behind them).

**Phase 2+ planned (not live today):** `fulfillment-mcp` (sixth MCP server), FulfillmentProvider ABC, three mock providers (`instacart_mock`, `shipt_mock`, `kroger_bopis_mock`), quote-aggregator, `place_order`, substitution flow with dietary-filter-at-search, BOPIS plus pharmacy gate, status webhooks plus idempotency, cancel plus refund.

---

## The conversation

### Why a plug-in tier

**KEVEN:** Picture Sarah's life if every grocery retailer had to be its own app. The retailer she shops at twice a week. The same-day delivery service. The warehouse club for bulk. The boutique grocer for the gochujang. Each one a different login, a different account, a different cart, a different checkout. *That is Sarah's life today.* Every retailer has its own technology. Every customer wants the same thing — items, fast, fairly priced, with the right substitutes if something is out of stock. The plug-in tier is the architectural decision that *Sarah never has to know how many retailers are in the answer.* One tap. The system handles the rest.

**REID:** Walk the architectural move.

**KEVEN:** The retailer-by-retailer technology is a noise field — different rules, different timings, different ways of telling the system an item is out of stock. If the agent fleet had to reason across that noise, the system would become mostly retailer code within six months. *The intelligence would drown in the integration.* The plug-in tier hides the retailer-specific noise behind one abstract base class. Every retailer becomes a subclass implementing the same five methods. The agent talks to the base; the base talks to the retailer. *Sarah's experience is uniform because the agent's reasoning is uniform because the interface is uniform.*

**REID:** And here I press. The alternative move would be a microservice per retailer. Each one its own service, own deployment, own team. Most teams default to that. Why a single class hierarchy instead?

**KEVEN:** Defended. At the customer's scale — three mock retailers today, three real ones in v2, maybe eight ever — the cost of eight microservices is higher than the cost of eight classes inside one process. Eight deployments, eight monitoring surfaces, eight scaling profiles. But the primary defense isn't the operational cost. It's the *interface enforcement.* A microservice can publish a contract and drift from it one revision at a time, quietly. The class-based abstraction enforces the contract at *load time* — the language won't let a subclass exist that doesn't implement every method. *The contract is a structural prerequisite for the retailer to be a retailer in the system.*

One of the design team — Vargas — landed the line on this: *the interface is the product. Every retailer produces the same five-tuple — price, ETA, substitution rate, in-stock percentage, carbon — so the agent fleet can reason about them uniformly.* The interface is the product. The retailers are the inventory.

**REID:** And the customer-experience consequence.

**KEVEN:** The agent fleet is written *once.* The specialist that ranks quotes doesn't branch on which retailer it's looking at. The specialist that handles substitutions doesn't either. *One specialist composes a recommendation across the union of quotes. One substitution flow handles every retailer's out-of-stock event.* The retailer becomes a swappable implementation detail behind a uniform interface — *exactly like a USB port doesn't care what's plugged in.* Sarah doesn't see retailers; Sarah sees one trip view, one cart, one recommendation. *The customer is the better for it.* Carry that into the ABC walk.

### The provider contract — five things every retailer does

**KEVEN:** The contract that makes Sarah's one tap work. Picture what every retailer in Sarah's life has to be able to do — *quote, commit, report status, handle out-of-stock, cancel.* Five things. *Every retailer the system ever talks to implements those five.*

**REID:** Walk the five.

**KEVEN:** *Quote* — given Sarah's order and her address, what's the price, the ETA, how full the cart is, what the substitution rate looks like? *Commit* — Sarah confirmed; place the order. *Status* — what is the order doing right now? *Substitution* — Sarah just decided how to handle an out-of-stock item; record her choice. *Cancel* — Sarah changed her mind. Five methods. *That's the entire integration surface for every retailer the system ever talks to, mock or real, today or in v2.*

**REID:** And what each retailer declares about itself.

**KEVEN:** A handful of properties. *What kinds of trips it accepts* — pickup, delivery, stay-trip. *Whether it can handle prescriptions* — a hard structural property, not a runtime check. *Whether it covers the customer's ZIP.* Plus a few identifiers and labels. *Five methods plus a handful of properties. That's the contract.*

**REID:** And the quote shape — what the agent ranks against.

**KEVEN:** A small structured answer with the five things the customer cares about — *total price, fee, time-to-arrival or pickup, substitution rate, in-stock percentage* — plus a carbon estimate for a small green nudge. The shape is what the agent reasons over, what the card on Sarah's phone renders, what the audit chain records. *The shape is the boundary. Once frozen, every retailer — mock or real — conforms.*

**REID:** And the property the abstraction earns.

**KEVEN:** *The mock retailers in v1 are architecturally indistinguishable from real ones in v2.* The agent doesn't know they're mocks. The audit chain doesn't know. Sarah doesn't know. The seller doesn't have to dress them up — the mock is producing the same quote shape, the same substitution events, the same status updates the real provider will produce. *When the real provider lands, only the class implementation changes.* The orchestrator doesn't change. The substitution flow doesn't change. The card on Sarah's phone doesn't change. *Move to the aggregator.*

### The fan-out — three quotes in four seconds

**KEVEN:** Back to Sarah at nine-fifteen on Sunday. She taps *ship this plan.* The screen renders a spinner for less than four seconds. *In that four seconds, the system has asked every retailer the same question in parallel.* Walk what happens.

**REID:** Walk it.

**KEVEN:** When Sarah taps, the system loads her order — items, dietary flags, preferred address — and asks every eligible retailer for a quote. Eligibility is a structural pre-filter — *does this retailer accept this kind of trip, and does this retailer cover this ZIP?* A pickup-only retailer doesn't get asked about a delivery. A retailer that doesn't ship to Sarah's ZIP doesn't get asked at all. After the pre-filter, the surviving retailers are all asked at the same time. Within four seconds, every one has either returned a quote or timed out.

**REID:** And the timeout discipline. Because this is where most systems lie to the customer quietly.

**KEVEN:** Timeouts don't disappear. *They surface.* If one retailer times out, the card on Sarah's phone says *Shipt unreachable — two of three quotes shown.* The system isn't pretending all three retailers gave clean answers when only two did. *Sarah is not lied to about whether a retailer was queried.* The record on the audit trail captures both the request and the timeout; if Sarah ever asks Priya *why was I sent to the warehouse club instead of Shipt*, Priya has the row.

**REID:** This is the SRE pattern — degrade visibly, never silently.

**KEVEN:** *Degrade visibly, never silently.* The silent-degradation failure mode is what erodes trust. The customer who confirms a quote thinking three retailers were considered when only two were is the customer who has been quietly lied to by the architecture. The architecture refuses that.

**REID:** And the latency budget.

**KEVEN:** Five seconds end-to-end. *The end-to-end quote should feel instant; five seconds is the wall.* Four seconds per retailer to answer; the aggregation and ranking and rendering share the remaining second. The mock retailers respond in under a hundred milliseconds today, which sets the credible bar for the real ones. The system caches recent quotes for five minutes — so if Sarah taps, looks at the answer, tweaks the plan, and taps again, *she doesn't pay the latency twice.*

**REID:** Five seconds end-to-end. Timeouts surface. Cache by order shape. Move to the ranker.

### The recommendation — eight words

**KEVEN:** Now the eight words Sarah reads. *Cheapest by ten dollars and one hundred percent in stock.* Sarah reads that line in under a second. She knows why the system chose the pickup over the two deliveries. She doesn't need a paragraph. *Eight words is the discipline.*

**REID:** Walk the score.

**KEVEN:** The system reads each quote on five factors. *Price.* *Time to arrival.* *Reliability* — how often this retailer ends up substituting an item. *Sarah's own preference* — if she's used this retailer before and rated it favorably, that factor lifts. *Carbon.* The five factors are weighted — price the heaviest, then time, then reliability, then preference, then carbon. *The system isn't being clever. The system is being predictable.* The same set of quotes produces the same ranking every time. There is no LLM in the ranking step.

**REID:** And the eight-word reason. The line one of the design team — Maya Chen — landed on this.

**KEVEN:** *Show the why in eight words or less. Customers don't read paragraphs at checkout.* The reason names the dominant factor — *cheapest by ten dollars* — and one secondary detail Sarah can verify — *one hundred percent in stock.* Eight words. *Sarah reads it in a second and knows whether she agrees.*

**REID:** And here is where the line from the design team — Hassan, on transparency — lands.

**KEVEN:** *Surface the reason. A black-box rank loses customer trust the moment one retailer mysteriously loses three weeks in a row.* The ranking is composed by software, deterministic, no drift — but transparency is what earns Sarah's trust over time. The customer who sees an eight-word reason every week builds a mental model of what the system values — *price, then speed, then reliability, then her own preferences, then carbon.* The customer who sees no reason is left to infer. Over time, the inference goes adversarial. *The system always picks the warehouse club; what's it earning on the side?* *The eight-word reason inoculates against that.*

**REID:** The AI safety principle showing up in product design — the ranker has to be explainable in eight words.

**KEVEN:** Explainable in eight words. *The ranker the customer can disagree with productively is the ranker the customer trusts.* The ranker that can't be explained is the ranker she abandons. There's also a deterministic fallback for the case where the ranking step itself fails — *cheapest first.* The audit row tags that case so Priya can see when the composite ranker was bypassed. The customer is still served a ranking. *Move to the substitution flow.*

### The substitution flow — dietary safety at the search step

**KEVEN:** The highest-stakes moment in the whole product. Three hours into a fulfillment, the shopper reaches the aisle for the item Sarah ordered, and the item is out. *The system has thirty seconds to give Sarah a safe choice — and one of her household members has a peanut allergy.* Get this wrong, somebody eats peanut.

**REID:** Walk it.

**KEVEN:** The retailer fires an *out-of-stock* event. The system loads Sarah's order, finds the original lot, and — critically — pulls Sarah's dietary flags from the household profile. *The peanut allergy. The gluten preference. The kosher preference if she'd set one.* The system then asks the catalog specialist to find alternatives for the missing item — *with the dietary flags as a hard constraint.* The search returns only candidates that match the description *and don't match any allergen.* Candidates that match the description but would violate the allergy are filtered out *before the LLM ever sees them.*

**REID:** And the line from the design team that lands here — Hassan's.

**KEVEN:** *Substitution is the highest-risk LLM moment in this product. Get it wrong, the customer eats peanut.* The bottom line. The substitution flow is where the LLM has the most authority to surface something Sarah might tap fast — mid-fulfillment, provider waiting, timeout short. *The defense is structural.* The filter is enforced *at the search step*, never at the rendering step. Dietary flags are hard constraints. *The LLM cannot recommend an allergen because the LLM cannot see one.* Defense in depth — the search is the wall, and the rendering doesn't have to be.

**REID:** *The LLM never sees an allergen the customer can't eat.*

**KEVEN:** Never. That's the property. And the *skip the decision — agent will choose* option earns the same property. The system's default on skip is the customer-marked-safe option ranked highest by the deterministic substitution scorer — same brand if available, same size, closest price. *Deterministic. Not prose.* The skip is a defense, not laziness.

**REID:** And I press. What if the search comes back empty — the dietary flags exclude every candidate the retailer has for that item?

**KEVEN:** Real case, handled. The sheet shows *refund*, *skip*, and one line — *no safe alternative for your dietary needs; please choose refund or let the agent handle it.* Skip routes to refund automatically. *The refund option is always on the sheet for exactly this reason.* Sarah is never asked to choose between an allergen and a refund. *She's offered the refund as the safe path.* The record holds even in the edge case.

**REID:** And the way the customer hears about it.

**KEVEN:** Through the cue bus from Episode Six. The substitution event composes one cue, and the system fans it out — Sarah's phone gets a card, her kitchen speaker says *heads up — the same-day delivery is out of the gochujang you asked for. Tap the phone to choose.* Three chips plus refund plus skip. Sarah taps. The retailer gets the answer. The record seals. *The substitution flow inherits every property the cue bus earned — path diversity, cadence, one voice, audit thread — without re-implementing any of them.* Carry that into the pickup walk.

### Pickup as a peer to delivery

**KEVEN:** Now the move worth time. Pickup is *not* a stepchild of delivery in this architecture — pickup is a peer. The system doesn't write different code for pickup. *One contract handles both shapes. One ranker reasons over both. The customer doesn't pick a mode — the customer picks an answer.*

**REID:** Walk it.

**KEVEN:** Each retailer declares what kinds of trips it accepts. A pickup-only retailer declares *I do pickup.* A delivery-only retailer declares *I do delivery and stay-trips.* The same fan-out machinery handles both. *Sarah's Sunday tap can return a pickup quote alongside two delivery quotes, all in the same comparison card.* The quote shape carries both time-fields — a *time to arrival* for delivery, an *earliest pickup window* for pickup. The ranker reads whichever one is populated and normalizes it into the time factor of the score. *One quote shape, two trip shapes, one ranker.*

**REID:** And the economics, because the design document is bolder than the podcast has been. The recommendation in the example card isn't the same-day delivery — it's the pickup. *Saturday at ten, no fee, all fourteen items in stock.* The reason string the customer reads is *cheapest by nine ninety-nine and one hundred percent in stock.*

**KEVEN:** Pickup is the recommended option. The eight-word reason carries it. *Cheapest by ten dollars.* Sarah reads it in under a second, and the answer to *am I going past the store anyway* lands inside her own head in the next second. *The ranker doesn't have a thumb on the scale.* The customer decides.

**REID:** And the second move the contract carries — the pharmacy gate.

**KEVEN:** *Whether a retailer can handle prescriptions is declared on the retailer class — not as a runtime check, not after the LLM has seen the order. It's a structural property of the retailer.* The pre-filter checks two things — does the retailer accept this kind of trip, and if the order contains a prescription, does the retailer handle prescriptions? Today, only the in-pharmacy pickup retailer declares prescription handling. The same-day delivery retailers don't, and they never get asked about a prescription order.

**REID:** *This is the architecture-honest version of HIPAA.* The safety isn't a runtime check. It isn't a prompt politely asking the LLM not to surface a prescription to a non-pharmacy retailer. *It's an eligibility filter that fires before the LLM ever sees the prescription line.* The same defense-in-depth posture as the dietary filter — make the unsafe action structurally impossible upstream of the agent, not just unrecommended downstream of it.

**KEVEN:** Same posture. The LLM never sees a same-day delivery quote for a prescription because the aggregator never asked. The substitution flow never offers a delivery alternative for a prescription because the aggregator never quoted one. *The pharmacy stays in-pharmacy by structure, not by prose.*

**REID:** And Robert's Friday refill is the canonical pickup journey.

**KEVEN:** Friday morning. The system says — *your Lisinopril is due Friday. Want me to add it to your Friday pickup?* Robert says *yes* into his kitchen speaker. A passkey biometric confirms — *the smallest possible identity surface for the highest-trust action.* The system places the order at the pharmacy pickup retailer only — because that's the only one with prescription handling on its class. Friday at ten, Robert arrives at the store; the system knows he's there; the shopper brings his items out; the system mirrors the confirmation on the speaker and the panel. *That's the highest-trust path in CFMP — pickup is the architecture that earns the regulator's trust on prescriptions.*

**REID:** And Sarah's Sunday opening — *not* pickup-or-delivery.

**KEVEN:** Sarah's Sunday is pickup-PLUS-delivery, *one decision surface, one tap.* The system places three orders in parallel — one pickup, two delivery — and the cue bus mirrors all three status streams into one trip view. *The architecture is one contract with multiple trip kinds. The customer experience is one trip view with three legs.* The interface is the product, and the product is *pickup and delivery in one tap.*

**REID:** Sarah never thinks about which retailer handles which leg. Move to the deployment walk.

### The deployment — one new cell on the page

**KEVEN:** Picture the CIO opening the architecture page the seller has shared. The page she's been looking at since Episode Two has the three houses, the supporting services, the audit substrate, the speaker channel. *The fulfillment tier adds one cell.* No new infrastructure box. No new external dependency. No new monthly cost.

**REID:** Walk how that works. Because Episode Two opened on this page, and the fulfillment tier inherits the topology without adding a single new piece.

**KEVEN:** The agent fleet's home gains a handful of new HTTP handlers — *quote, place, status, substitute, cancel.* The catalog specialist gains a few new tools. *No new container service.* The existing MCP tier gains a sixth in-process server that hosts the new tools. *No new container service.* The retailer classes — the three mocks today, the real ones when partnerships sign — live as files alongside each other. *The customer's existing CFMP deployment is the existing deployment; the fulfillment tier is additive.*

The data additions land in the existing database. The audit substrate gains new row types. *The architecture page gains one new cell — fulfillment plug-ins, three mocks today, real retailers tomorrow — alongside the existing agent fleet and MCP cells.*

**REID:** Zero new infrastructure. Zero new monthly cost. Zero new external dependency.

**KEVEN:** Zero, zero, zero. The seller's argument lands because the deployment lands. *Other delivery-integration approaches require a new orchestration service, a new partner-network bridge, a new payment vault.* CFMP requires the team to enable a configuration flag and re-deploy the existing revision. *The deploy is a label change.* The infrastructure delta is one row on the page.

**REID:** And the retailer webhooks.

**KEVEN:** Retailer notifications — out-of-stock events, status updates, order completions — all land on the same handler. The handler verifies the signature against a per-retailer secret. It de-duplicates retries. It routes out-of-stock events into the substitution flow, status updates into the cue bus, every action into the audit chain. *Every action carries the same tracking thread Sarah's tap started with.* Six weeks later, a regulator's replay question lands across the entire fulfillment chain on one screen.

The page URL is `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture`. Open it on a client call. *The new fulfillment cell shows up alongside the existing agent fleet and MCP cells. The seller's screen-share gains one cell. The buyer's mental model gains one row. The Azure spend gains zero dollars.*

**REID:** One cell, one row, zero dollars. Move to the mocks-are-real-architecture commitment.

### Mocks are real architecture

**KEVEN:** The discipline that holds the whole tier together. *The three retailer mocks in v1 are not prototypes.* They are not throwaway. They are not *we'll replace them with the real thing in v2.* *They are real architecture.* Walk the commitment.

**REID:** Walk it.

**KEVEN:** Each mock is a class that implements the contract. Each produces the same quote shape, the same out-of-stock events, the same status updates, the same audit rows. *The agent doesn't know they're mocks. The audit chain doesn't know. Sarah doesn't know. The seller doesn't have to dress them up.* The mock retailers are deterministic — one has a twenty-percent substitution rate, one has one percent, one has zero — because deterministic mocks are testable, not because the mocks are simpler than the real retailers will be.

When the real retailer lands — when the integration to Instacart's Connect API ships, when the partnership with Shipt closes, when the Kroger Public API integration ships — *only the class implementation changes.* The orchestrator doesn't change. The substitution flow doesn't change. The audit chain doesn't change. The card on Sarah's phone doesn't change. The seller's argument doesn't change. *The customer's experience doesn't change.*

**REID:** This is what *mocks are real architecture* means. The abstraction is right *today*, not a prototype to be thrown away when the partnerships sign.

**KEVEN:** Right today. *If the abstraction were a prototype, the team would be saying once we land the real retailer, we'll rewrite the quote handling, we'll swap out the substitution flow, we'll redo the audit shape.* None of that is true. The abstraction is final. The implementation is mock today. When the implementation becomes real, the abstraction doesn't move. *That's the Independence-minded operating model showing up in code.* CFMP ships fulfillment value to the customer in v1 even with mocks, while the legal team works the real data-processing agreements for v2 partnerships. *The customer sees a working system today. The seller demos a working system today. The retailer relationship is additive, not blocking.*

**REID:** And the v2 transition.

**KEVEN:** A class swap. Sprint pre-flight is the legal review of the mock-versus-real distinction, the API documentation review, the privacy addenda for each real retailer. The deploy when the real classes land is a configuration change — *flipping one retailer at a time from mock to real.* The customer's mental model doesn't change. The seller's argument doesn't change. *The architecture is the same.*

**REID:** Mocks today, real retailers tomorrow, abstraction unchanged. The customer is the better for it — because the system works for her today and gets richer when the partnerships sign. Move to the reading.

### A reading I want to do

**REID:** A reading. The episode sits at the intersection of two practitioner literatures — bounded-context design and clean-architecture dependency direction — and I want to name both.

The first is Eric Evans, *Domain-Driven Design*, Addison-Wesley, two-thousand-and-three. Twenty-three years old, still the canonical text on what a bounded context is and why it is the right unit of interface design. Evans's argument is that a bounded context is a region of the domain where a model means exactly one thing, and the interface between two contexts is the place where the meanings are translated. The FulfillmentProvider ABC is exactly an Evans bounded-context interface — *the agent fleet's model of a quote* and *the retailer's model of a quote* are different, and the ABC is where the translation happens. The retailer thinks in their own SKUs, their own service-area envelopes, their own substitution semantics; the agent fleet thinks in ProviderQuotes and dietary flags. The translation is the provider class. The bounded-context discipline is what makes the agent fleet write-once and the retailer integrations swap-many.

**KEVEN:** And the second.

**REID:** The second is Brandon Rhodes's PyCon talk *The Clean Architecture in Python*, two-thousand-and-fourteen, available on the PyCon US YouTube archive. Rhodes is the author of the python-jsonrpc-server and a long-time speaker on architectural discipline in Python. The talk applies Robert Martin's clean-architecture dependency direction — *dependencies point inward toward the domain core, never outward toward infrastructure* — to a Python codebase. The fulfillment tier is exactly that. The agent fleet is the domain core. The provider classes are the infrastructure ring. The dependency points *from* the provider class *to* the ABC, never the other way. The orchestrator imports the ABC; the provider classes implement it; the orchestrator never imports a specific provider class by name. The registry resolves by env var at startup. The dependency direction is what lets the mocks be real architecture — the core does not know which implementation is loaded; the core only knows the interface.

**KEVEN:** Evans on the principle, Rhodes on the practice.

**REID:** Evans on what a bounded context is. Rhodes on how to enforce the dependency direction so the boundary does not leak. Both worth a careful read for any engineer wiring an integration tier in twenty-twenty-six. The instinct to write a microservice per provider is the instinct that gets the *deployment* right and the *abstraction* wrong; Evans and Rhodes together name why.

**KEVEN:** Read them in that order — Evans first for the framing, Rhodes for the implementation. Move to the disagreement.

### One disagreement

**REID:** One disagreement, customer-grounded. *When a retailer goes down on a Saturday afternoon, what does Sarah see — a clean error, a long silence, or a system that absorbed the failure and proposed an alternative?* Two voices on the team — the reliability voice and the customer-support voice — pulled different directions.

**KEVEN:** Put it on tape.

**REID:** The reliability voice. *Three retailers means three ways to fail. Plan for any of them going down.* The instinct is to protect the platform — three timeouts in sixty seconds, mark the retailer unhealthy for five minutes, take it out of the rotation. *The platform is protected. The blast radius is contained.* The breaker is aggressive.

The customer-support voice. *When a retailer screws up, Sarah should hear from us first, not the receipt email.* The instinct is to never let Sarah see a 503. When a retailer fails, the agent absorbs the failure and *proposes a recovery in the same UI moment.* *Shipt is having issues right now. Want to send that gochujang via Instacart instead?* Sarah one-taps. The order moves. *She never sees the failure as a failure.*

Now the tension. Aggressive circuit-breaking might mark a retailer unhealthy after a transient blip when Sarah still wanted that retailer. Conservative circuit-breaking leaks failure into Sarah's UX — she waits four seconds, then four more, while the system keeps trying a retailer that's down. *Where is the line?*

**KEVEN:** Both are right. The convergence layers them.

**REID:** Bring it.

**KEVEN:** *Three layers, in order.*

First failure — *silent retry.* The retailer timed out. The system retries internally with a short backoff. Sarah's spinner is still spinning; she hasn't been told anything; the system is absorbing the blip. If the retry succeeds, Sarah sees a slightly slower answer and is otherwise unaffected.

Second failure — *propose a recovery to Sarah in real time.* The retry failed; the retailer is genuinely impaired. The system doesn't surface an error. *Shipt is having issues right now. Want to send your order to the warehouse club instead?* Sarah one-taps. The order moves to the alternative. *Sarah experiences agent-absorbed-the-failure-and-gave-me-a-choice.* That's the customer-support voice winning the immediate UX.

Third failure within a minute — *mark the retailer unhealthy for five minutes.* The pattern is now multiple failures in a short window; the retailer is impaired, not blipped. The breaker trips. The system stops fanning out to that retailer for the next five minutes. New quotes are served from the surviving retailers. *Sarah never sees a 503*; Priya sees the breaker state on her console. *The reliability voice wins the platform reliability. The breaker is the floor; the agent-mediated recovery is the ceiling.*

**REID:** And the failure mode if the convergence breaks.

**KEVEN:** If only the breaker fires, *Sarah sees a clean error sometimes and waits in silence other times*, depending on whether the breaker has tripped yet. Her mental model is *the system is fragile.* If only the agent-mediated recovery fires, the platform takes the brunt of a sustained outage — *the system keeps trying the bad retailer for every customer; the queue depth grows; latency degrades for everyone.* Her mental model is *the system is slow.* Layering them gives Sarah the third reading — *the system absorbs failures and recovers.* That's the experience the architecture earns.

**REID:** Converge accepted. *Agent-mediated recovery at the customer's UX. Breaker at the platform.* The customer is the better for it — because Sarah's Saturday isn't broken by an integration she doesn't know exists. Carry it.

### What to carry forward

**KEVEN:** Three things into Episode Eight. Each one a thing a non-technical leader can carry into a Monday meeting.

**KEVEN:** *One — the interface is the product.* One contract, many retailers. Sarah doesn't see retailers; Sarah sees one trip view, one cart, one recommendation. *The agent fleet reasons across retailers without writing retailer-specific code, because every retailer produces the same quote shape and accepts the same five operations.* The interface is the product. The retailers are the inventory. Carry that.

**KEVEN:** *Two — dietary safety is enforced at the search step.* The substitution flow is the highest-stakes moment in the whole product — *get it wrong, somebody eats peanut.* The defense is structural: the LLM never sees an allergen the customer can't eat, because the search filters the candidate set *before* the LLM is invoked. Make the unsafe action invisible to the model, not just unrecommended downstream. *Get it wrong, somebody eats peanut. Don't get it wrong.* Carry that.

**KEVEN:** *Three — mocks are real architecture, and pickup and delivery are peers.* When the real retailer lands, only the class implementation changes — *the orchestrator doesn't change, the substitution flow doesn't change, the audit chain doesn't change, the card on Sarah's phone doesn't change.* That's the Independence-minded posture showing up in code. *CFMP ships fulfillment value to the customer in v1 with mocks while the legal team works the real partnerships for v2.* And the same abstraction that lets the mocks be real architecture lets pickup and delivery be *peer trip shapes* — one ranker, one cue bus, one trip view. The recommendation in the example card is often the pickup. Robert's Friday refill is the highest-trust path in the system. *Pickup is not a stepchild.* Carry that.

**REID:** Interface is the product. Dietary safety at the search step. Mocks are real architecture; pickup is a peer to delivery. Three carries. Into Episode Eight.

**KEVEN:** Next episode — *Identity, consent, HIPAA, and senior accessibility.* The four-identity chain finally walked end to end. Adebayo on consent at the OAuth grant boundary. Chen on the HIPAA-isolated pharmacy tenancy. Yamamoto on the senior-accessibility overrides. Russo on the AirPlay-channel audit tagging. Today we walked the plug-in tier that places orders on Sarah's behalf; next episode we walk the safety substrate that lets the system place orders, set reminders, and speak medication names without ever telling someone in the room what should stay between the system and the customer.

[Sound: the closing sting. ~6 seconds.]

---

## Further reading

- **Source docs**
  - CFMP Fulfillment Design Document — `C:\code\iot_device\docs\packs\CFMP-Fulfillment-Design-Document.md` — full, end to end. Part 1 (the customer's problem, the vision, success metrics, why now); Part 2 (personas — Sarah's Sunday split-delivery, Robert's Friday Rx pickup, Marcus's StayLot multi-leg — plus the non-human actors and the agent fleet's role); Part 3 (the five end-to-end journeys including Sarah's headline, Robert's Rx flow, Marcus's cabin pre-stocking, Diana's caregiver oversight, the provider-outage graceful recovery); Part 4 (the seven core concepts stair-stepped — the FulfillmentProvider ABC, the ProviderQuote shape, the Quote-Aggregator, the Recommendation Score, the Lot integration mask, the Substitution Flow, the APEX Ledger contract); Part 5 (the Azure-native architecture — the eight new HTTP endpoints, the three new agent tools, the sixth FastMCP server, the four new Postgres tables, the file-level structure); Part 6 (the comparison card UX, the substitution sheet UX, the cue cadence reuse, the provider visual identity, the address PII redaction); Part 7 (the 24-UC catalog with the 10 critical-path UCs and UC-F03 in full Cockburn); Part 8 (the cross-cutting quality layers — Adebayo, Hassan, Okafor, Tanaka, Voss, Mendez, Ortiz, Liu); Part 9 (the 6-sprint plan and the 32-item decision queue); Part 10 (glossary, contributor cast, open questions, quick-reference).
  - CFMP Fulfillment UC Catalog — `C:\code\iot_device\docs\packs\CFMP-Fulfillment-UC-Catalog.md` — all 24 fulfillment UCs in Cockburn format. UC-F01 through UC-F03 (quote and recommendation), UC-F04 through UC-F07 (order placement), UC-F08 through UC-F11 (substitution flow), UC-F12 through UC-F14 (StayLot multi-leg), UC-F15 through UC-F17 (provider plug-in lifecycle), UC-F18 through UC-F19 (identity gates), UC-F20 through UC-F21 (cancellation and refund), UC-F22 through UC-F23 (webhook and idempotency), UC-F24 (audit replay).
  - CFMP Fulfillment Roadmap — `C:\code\iot_device\docs\packs\CFMP-Fulfillment-Roadmap.md` — the 6-sprint execution layer over the design and UC catalog. Sprint -1 (legal review of the mock-vs-real distinction, sample API documentation review); S0 (Provider ABC, schema, the first mock); S1 (all three mocks plus the comparison card UI); S2 (substitution flow with dietary-safe ranking); S3 (StayLot multi-leg plus split-order UI); S4 (webhook hardening plus circuit breakers plus DLQ); S5 (polish plus telemetry plus A/B for ranking weights).
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — the hero artifact this episode anchors its deployment claims to. The fulfillment plug-in tier appears as a sibling cell to the agent fleet and the MCP tier; the new `fulfillment-mcp` FastMCP server is the sixth path-mount inside the existing `ca-visionkit-mcp` Container App; the new HTTP endpoints under `/api/fulfillment/*` extend the existing `ca-visionkit-orchestrator` surface; the four new Postgres tables land in the existing Flexible Server; the Bronze audit categories add eight new row types to the existing chain. One cell on the page, zero new infrastructure, zero new monthly cost. Open on every client call.
- **Microsoft Learn**
  - Azure Container Apps — `https://learn.microsoft.com/azure/container-apps/` — the platform hosting `ca-visionkit-orchestrator` and `ca-visionkit-mcp`. Revision-based deploy, scale-out by HTTP queue depth, native L7 ingress, path-mounted FastMCP servers in process. The platform the fulfillment tier ships into without any new infrastructure.
  - Azure AI Foundry Agent Service — `https://learn.microsoft.com/azure/ai-foundry/agents/` — the productized agent runtime the parent and specialist children are deployed against. The Catalog specialist that ranks ProviderQuotes and composes the eight-word recommendation reason is one of the five specialists hosted in this surface.
  - Model Context Protocol — `https://modelcontextprotocol.io/` — the protocol the FastMCP servers implement. The fulfillment-mcp server adds five tools to the existing MCP tier — `list_providers`, `get_quotes`, `place_order`, `get_order_status`, `handle_substitution` — without changing the protocol or the discovery surface.
- **Industry / research**
  - Eric Evans, *Domain-Driven Design* (Addison-Wesley, 2003) — the canonical text on bounded contexts as the basis for interface design. The FulfillmentProvider ABC is exactly an Evans-style bounded-context interface — the place where the agent fleet's model of a quote and the retailer's model of a quote are translated. The discipline is what makes the agent fleet write-once and the retailer integrations swap-many.
  - Brandon Rhodes, *The Clean Architecture in Python* (PyCon US, 2014) — the practitioner talk on dependency direction in Python. Available on the PyCon US YouTube archive. The fulfillment tier's dependency direction — orchestrator imports the ABC, provider classes implement it, orchestrator never imports a specific provider class by name — is exactly the discipline Rhodes names. The registry resolves implementations by env var at startup; the core is unchanged when the implementation swaps.
  - Nielsen Norman Group on cart-and-checkout friction — Raluca Budiu's articles on decision overload in checkout flows. The substitution sheet's *three options plus refund plus skip* cap is the design committing to Vargas's *"Four+ kills decisional capacity. Five+ kills the cart"* rule from Section Six-Point-Two. The NN/g practitioner discourse is the layer the design's UX commitments inherit from.
- **Sibling series cross-reference** — Cross-Cloud Agentic Episode 07 (forthcoming) — the framework-level treatment of plug-in integration tiers as bounded contexts, including the AWS and GCP equivalents to the FastMCP path-mount pattern that CFMP-Fulfillment generalizes from.

— end of episode 07 —
