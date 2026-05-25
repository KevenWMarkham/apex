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

The screen renders a spinner for less than four seconds. Three quotes return in parallel. The partner pickup is free with a window the next morning at ten; all fourteen items are in stock. The same-day delivery is sixty minutes out, nine ninety-nine fee, ninety-five percent in stock — the gochujang is the one flagged unavailable. The warehouse-club delivery is ninety minutes out, eleven ninety-nine fee, ninety-nine percent in stock. The agent's recommendation surfaces above the three: *"split the order — gochujang via the warehouse-club delivery because it has it in stock and it arrives tonight, the school snacks via the same-day delivery because they are cheapest there, the rest of the plan via the partner pickup Saturday morning at no fee."* The reason renders below the recommendation in eight words: *"Cheapest by ten dollars and one hundred percent in stock."*

Sarah taps confirm. Three orders flow.

Three hours later, just before noon, her phone buzzes. *"Heads up — the same-day delivery is out of the gochujang you asked for. Want the same brand from a different shopper, a different brand, or a refund?"* Three chips on the sheet. One labeled *skip the decision — agent will choose*. Sarah taps the same-brand alternative. The provider acks. The row goes to the ledger. The dinner is back on the calendar.

[Sound: a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start on the four-second spinner. Because what happens in that four seconds is the whole architectural argument for this episode. Sarah's one tap fans out to three providers in parallel. Three quotes return. The agent ranks them. The recommendation lands with an eight-word reason. None of that is theoretical. All of it is happening inside one FastMCP server, three plug-in classes, one orchestrator, one audit chain.

**REID:** And this is the surface where the agent fleet stops being theoretical and starts buying things on Sarah's behalf. Through Episode Six, the fleet has been writing answers and rendering them. From this episode forward the fleet places orders, moves money, commits the customer to a transaction with a third-party logistics network we do not control. That is a different kind of surface. It deserves a different kind of architectural discipline.

**KEVEN:** Welcome back to the CFMP Podcast. Episode Seven. *Fulfillment · the plug-in tier.* Episode Six's carry-forward was the Cue Bus reuse for fulfillment status events. Today we open the plug-in tier. Seven sub-sections. Why a plug-in tier is an architectural move. The FulfillmentProvider ABC and the ProviderQuote shape. The quote-aggregator fan-out. The recommendation score. The substitution flow with dietary safety enforced at the search step. The Azure-native deployment of the sixth FastMCP server. And the discipline that v1 mocks are real architecture.

**REID:** A reading, a disagreement, three carries. Let's go.

---

## The conversation

### Why a plug-in tier

**KEVEN:** Start with the architectural framing, not the integration mechanics. Because the plug-in tier is a *move*, not a feature. Walk it.

**REID:** Walk it.

**KEVEN:** *Every grocery retailer and delivery network has its own API. Every customer wants the same thing — items, fast, fairly priced, with the right substitutes.* That sentence from Section One of the design document is the whole reason this tier exists. The retailer's API surface is a noise field — different authentication models, different rate limits, different idempotency semantics, different webhook patterns, different identifier shapes, different substitution semantics. If the agent fleet has to reason across that noise, the orchestrator becomes mostly retailer code within six months. The intelligence drowns in the integration.

The plug-in tier hides the retailer-specific noise behind a single abstract base class. Every retailer becomes a subclass implementing the same five methods. The agent fleet talks to the abstract base; the abstract base talks to the retailer. The customer's experience is uniform because the agent's reasoning is uniform because the interface is uniform.

**REID:** And here I press. Because the alternative move would be a microservice per provider. Each retailer gets its own service, its own deployment, its own owner. That is what most teams default to. Why an ABC and not a microservice per provider?

**KEVEN:** Defended. At v1 scale — three mocks today, three real providers in v2, perhaps eight in v3 — the cost of eight microservices is higher than the cost of eight plug-in classes inside one FastMCP server. Eight deployments, eight observability surfaces, eight scaling profiles, eight identity boundaries. The MCP tier was designed to host plug-ins in process. The right unit of isolation here is the class, not the service.

But that is the secondary defense. The primary defense is the *interface enforcement* the ABC produces. A microservice can publish a contract and drift from it one revision at a time. An ABC enforces the contract at *class instantiation time* — the Python interpreter will not let a subclass exist that does not implement every abstract method. The contract is the structural prerequisite for the class to load. The interface is the product, not a description of the product.

Vargas's line, from Section Four-Point-One, verbatim: *"The interface IS the product. Every provider must produce the same 5-tuple — price, ETA, sub-rate, in-stock percentage, carbon — so the agent fleet can reason about them uniformly."* The interface is the product. The provider implementations are the inventory.

**REID:** And the consequence.

**KEVEN:** The consequence is that the agent fleet can be written *once*. The Catalog specialist ranking quotes does not branch on provider identity. The Concierge specialist handling substitutions does not branch on provider identity. The audit ledger does not branch on provider identity. One specialist composes a recommendation across the union of quotes; one substitution flow handles every retailer's out-of-stock event; one LedgerRow shape records every fulfillment action. The provider becomes a *swappable implementation detail behind a uniform interface — exactly like a USB port doesn't care what's plugged in*. The design document uses that phrase explicitly, and the phrase is doing real architectural work. Carry that into the ABC walk.

### The FulfillmentProvider ABC and the ProviderQuote shape

**KEVEN:** The FulfillmentProvider ABC. Five abstract methods. Six class-level attributes. Twelve lines of Python that define the entire integration surface for grocery and delivery in CFMP. Walk the methods.

**REID:** Walk them.

**KEVEN:** Method one. `get_quote(lot, address) -> ProviderQuote`. The provider receives the Lot — items, dietary flags, member preferences — and the destination address, and returns one ProviderQuote. One call, one provider, one quote. The aggregator above will fan this out across all enabled providers in parallel.

Method two. `place_order(lot, address, substitution_policy) -> Order`. The customer has confirmed; the provider commits. The substitution policy is passed in explicitly — *prefer same brand*, *prefer same size*, *no substitutions, refund on out-of-stock* — because the policy varies by Lot and by member. The return is an Order — provider-side identifier, status, ETA, tracking URL.

Method three. `get_status(order_id) -> OrderStatus`. The polling path. The webhook is the noisy half of the resilience story; the polling path is the silent half, for reconciliation when a webhook is missed.

Method four. `confirm_substitution(order_id, sku, decision)`. The customer has just decided how to handle an out-of-stock event. The decision lands at the provider so the provider can complete the order, refund the missing item, or skip per the customer's choice.

Method five. `cancel_order(order_id) -> bool`. The customer changed her mind. The provider may or may not honor the cancellation. The return is the actual outcome, not the request.

Five methods. That is the entire grocery-and-delivery integration surface. Every retailer in CFMP, mock or real, today or in v2, implements these five.

**REID:** And the class attributes. Six of them.

**KEVEN:** *Id* — the stable identifier the registry uses. *Display* — the human-readable name. *Kinds* — the set of Lot kinds the provider accepts; the aggregator pre-filters on this. *Is real* — boolean; false for v1 mocks. *Handles pharmacy* — boolean; only the BOPIS partner pickup in v1, because Rx must stay in-pharmacy. *Service area zips* — the ZIP set the provider operates in, or None for nationwide. Six attributes plus five methods is the entire contract.

**REID:** And the ProviderQuote shape. Nine fields. Walk them.

**KEVEN:** The ProviderQuote is the atomic unit of comparison. Nine fields, from Section Four-Point-Two. *Provider id* matching the class attribute. *Total cents* — line items only, no fees, in integer cents. *Fee cents* — delivery or service fee, broken out so the customer sees the all-in cost. *ETA minutes* — minutes from now. *Substitution rate* — historical share of items that result in a substitution event; the higher, the more friction post-confirmation. *Carbon kilograms* — routing and last-mile estimate; small ranker weight, present because the design committed to a green nudge. *In stock percentage* — share of the Lot's items in stock right now. *Service area ok* — the provider's own check, redundant with the pre-filter but defensively present. *Raw* — provider-specific payload preserved for audit; the orchestrator never reads from raw; the support engineer reads it when something has gone wrong.

**REID:** And the property the quote shape earns the architecture.

**KEVEN:** *The quote shape is the API boundary — once frozen, mocks and real providers conform.* The shape is what the agent ranks against, what the UI renders, what the audit chain stores. The shape does not change when a real provider lands. The class implementation changes. The mock produced a deterministic in-stock-percent of ninety-five; the real provider queries the retailer's inventory and produces whatever the retailer reports right now. Same shape, same ranker, same UI, same audit.

**REID:** That is exactly the point. The abstraction is what lets v1 ship with mocks while the partnerships are still being negotiated.

**KEVEN:** Exactly. The v1 mocks are real classes producing real ProviderQuotes through the real ABC. The orchestrator does not know they are mocks. The audit chain does not know. The UI does not know. The customer does not know. The seller can demo against the mocks because the mocks are architecturally indistinguishable from real providers — *they implement the same ABC*. Move to the aggregator.

### The quote-aggregator fan-out

**KEVEN:** The quote-aggregator. `get_quotes` is the FastMCP tool the orchestrator calls when the customer taps *ship this Lot*. The tool fans out to all enabled providers in parallel using `asyncio.gather`, with a four-second timeout per provider, and returns the union of results. Walk the fan-out.

**REID:** Walk it.

**KEVEN:** The orchestrator's HTTP handler receives the Lot identifier from Mobile, loads the Lot — items, dietary flags, preferred address — and calls `fulfillment-mcp.get_quotes`. The MCP tool reads the registry and pre-filters two ways. *One* — the Lot's kind must intersect the provider's `kinds` set; a PickupLot does not get sent to a delivery-only provider. *Two* — the destination ZIP must intersect the provider's `service_area_zips`, or the service area must be nationwide.

After the pre-filter, the aggregator builds one coroutine per surviving provider calling that provider's `get_quote`, hands the list to `asyncio.gather` with a four-second timeout per provider and `return_exceptions=True`, and awaits concurrently. Within four seconds every provider has either returned a ProviderQuote or timed out. The aggregator returns the union — successful quotes plus error rows for timeouts.

**REID:** And the timeout-as-error-row discipline.

**KEVEN:** Critical detail. Timeouts produce a `{provider_id, error: "timeout"}` row. They are *not* dropped silently. The Catalog specialist sees the error row alongside the successful quotes. The UI sees it when it composes the comparison card. The result is the *"Shipt unreachable — two of three quotes shown"* affordance the design document calls out. The customer is not lied to about whether a provider was queried.

**REID:** This is the SRE pattern — degrade visibly, never silently.

**KEVEN:** Degrade visibly, never silently. The silent-degradation failure mode erodes trust. The customer who confirms a quote thinking three providers were considered when actually only two were is the customer who has been quietly lied to by the architecture. The LedgerRow records both the request and the timeouts; the operator on the Portal can replay the trace; the support engineer answering a *why was I sent to the warehouse-club delivery* question can point to the row.

**REID:** And the latency budget.

**KEVEN:** Five seconds end-to-end, from Section Eight-Point-Three. Okafor's wall. *"End-to-end quote should feel instant. Five seconds is the wall."* Four seconds per-provider timeout; the aggregator, the orchestrator's HTTP handling, the Catalog specialist's ranking, and the UI's render share the remaining second. The mock providers respond under a hundred milliseconds, which sets the credible bar for real providers. There is also a five-minute response cache keyed on Lot hash and address hash, so a tap-and-retap against a tweaked plan does not pay the latency twice.

**REID:** Five-second end-to-end. Error rows for timeouts. Cache by Lot hash and address hash. Move to the ranker.

### The recommendation score

**KEVEN:** The recommendation score. Composite, five factors, weighted, from Section Four-Point-Four of the design document. Walk the formula.

**REID:** Walk it.

**KEVEN:** The score for each quote is a weighted sum of five normalized factors. Factor one — price. *Minimum total over this quote's total.* The cheapest quote scores one on this factor; every other quote scores less than one in proportion. Factor two — ETA. *Minimum ETA over this quote's ETA.* The fastest quote scores one; every other in proportion. Factor three — reliability. *One minus the substitution rate.* The provider with the lowest substitution rate scores closest to one. Factor four — member preference. *The member's preference weight for this provider.* If the customer has used this provider before and rated it favorably, this factor lifts. Factor five — carbon. *Minimum carbon over this quote's carbon.* The greenest quote scores one.

The five factors are weighted at thirty, twenty-five, twenty, fifteen, and ten percent in v1. Price dominates; ETA is the second pull; reliability is the third; preference is the fourth; carbon is the fifth and smallest. The weights are tunable in Sprint Five behind an A/B framework; v1 ships with the defaults the design document committed to. The formula composes deterministically; the same set of quotes produces the same ranking every time. There is no LLM in the ranking step.

**REID:** And the reason string.

**KEVEN:** The reason string is the eight-word affordance the UI renders below the recommendation. *"Cheapest by three dollars and fifty cents and ninety-nine percent in stock."* *"Fastest by twenty minutes and one hundred percent in stock."* *"Most reliable in your zip and same-brand subs."* The string is composed by surfacing the *dominant factor* — the one that contributed the most to the winning quote's score margin over the second-place quote — plus a secondary detail the customer can verify. Eight words is the design's discipline. Maya Chen, from Section Six-Point-One: *"Show the WHY for the recommendation in eight words or less. Customers don't read paragraphs at checkout."*

**REID:** And here is where Hassan's line lands, because the reason string is not a polish concern. The reason string is the AI safety principle showing up in product design. Quote it.

**KEVEN:** Quoting it. Hassan, verbatim from Section Four-Point-Four of the design document: *"Surface the reason. A black-box rank loses customer trust the moment one provider 'mysteriously' loses three weeks in a row."* The rank is composed by software, not by an LLM, and the rank is deterministic, so there is no behavioral drift to defend against; but the *transparency* of the rank is what earns the customer's trust over time. The customer who sees an eight-word reason every week builds a mental model of what the ranker values — price, then speed, then reliability, then her own preferences, then carbon. The customer who sees no reason is left to infer; over time the inference goes adversarial. *"The system always picks the warehouse-club delivery; what is it earning on the side?"* The eight-word reason inoculates against that drift.

**REID:** This is the AI safety principle showing up in product design — the ranker must be explainable in eight words.

**KEVEN:** Explainable in eight words. That is the discipline. The ranker that can be explained in eight words is the ranker the customer can disagree with productively. The ranker that cannot be explained in eight words is the ranker the customer abandons. *Surface the reason.* Carry that.

There is also a deterministic fallback path the design earns for the case where the Catalog specialist returns a 5xx. The fallback is *lowest total cents first*, with the LedgerRow tagged `ranker=fallback_deterministic` so the operator on the Portal can see when the composite ranker was bypassed. The customer is still served a ranking; the audit chain records that the ranking was the fallback; the seller can defend the experience because the failure mode is named in the trace. Move to the substitution flow.

### The substitution flow — dietary safety enforced at the search step

**KEVEN:** The substitution flow. The highest-risk LLM moment in CFMP. The moment where the system has the most to lose and the customer has the most to lose. Walk it.

**REID:** Walk it.

**KEVEN:** A provider is mid-fulfillment. The shopper reaches the aisle for the item Sarah ordered and the item is out of stock. The provider fires an `item_oos` event. The event lands at `ca-visionkit-orchestrator /api/fulfillment/webhook`. The handler verifies the HMAC signature against the per-provider shared secret, checks the idempotency table keyed on the compound of provider identifier and provider-side event identifier, and calls `fulfillment-mcp.handle_substitution` with the order identifier and the out-of-stock SKU.

The substitution tool loads the order, the originating Lot, and — critically — the customer's `dietary_flags` from the profile. The dietary flags are the constraint set — *peanut allergy*, *gluten-free*, *kosher*, *no shellfish*, whatever the customer has set. The tool calls the Catalog specialist's product search with two arguments — the missing item's name, and the dietary flags as a *hard constraint*. The search returns only candidates that match the description *and* do not match any allergen flag. Candidates that would have matched the description but match an allergen are filtered out *before the LLM ever sees them*.

**REID:** And here is where Hassan's line lands again. Quote it.

**KEVEN:** Quoting it. Hassan, verbatim from Section Eight-Point-Two: *"Substitution is the highest-risk LLM moment in this product. Get it wrong, the customer eats peanut."* The product's safety bottom line. The substitution flow is where the LLM has the most authority to surface a recommendation the customer might tap fast — mid-fulfillment, provider waiting, timeout short. Get it wrong, the customer eats peanut.

The defense is structural. The filter is enforced *at the search step*, never at the rendering step. The search receives dietary flags as a hard constraint. Allergens are excluded *before the agent sees them*. The LLM cannot recommend an allergen because the LLM cannot see one. Defense in depth — the search step is the wall, and the rendering step does not have to be one.

**REID:** Defense in depth. The LLM never sees an allergen the customer can't eat.

**KEVEN:** Never. That is the property. And the *"Skip the decision — agent will choose"* affordance earns the same property. The agent's default in the skip path is the customer-marked-safe option ranked highest by the deterministic substitution scorer — same brand if available, same size, closest price. The agent applies a deterministic rule, not prose. The skip is a defense, not laziness.

**REID:** And here I press. If the search step filters out everything — if the dietary flags exclude every candidate in the provider's catalog for that item — what does the agent show?

**KEVEN:** Pressing accepted. The case is real and the design handles it. If the safe candidate set is empty, the substitution sheet renders the refund option, the skip option, and a single line of text — *"No safe alternative for your dietary needs; please choose refund or let the agent handle it."* Skip routes to refund automatically. The refund option is *always present* on the sheet for exactly this reason. *No alternative is never not the right answer when the safe set is empty.* The customer is never asked to choose between an allergen and a refund; the customer is offered the refund as the safe path. The LedgerRow records the empty safe set and the refund decision. The audit chain shows the Compliance team the dietary flags held even in the edge case.

**REID:** And the cue render.

**KEVEN:** The cue render reuses the Sonos Cue Bus from Episode Six. The substitution event composes a Cue and the Cue Bus fans it out across mobile push, Sonos cue, and Portal mirror. The customer hears the chime and the spoken line — *"Heads up — the same-day delivery is out of the gochujang you asked for. Tap the phone to choose."* The mobile renders three chips plus refund plus skip. The customer taps. The provider gets the answer. The LedgerRow seals. The substitution flow inherits every property the Cue Bus earned in Episode Six — path diversity, cadence law, one-voice rule, audit trace — without re-implementing any of them. Carry that into the deployment walk.

### Azure-native deployment — the sixth FastMCP server

**KEVEN:** Azure-native deployment. Section Five of the design document. The win, in the design's words — *zero new Container App, zero new external dependency, zero new monthly cost. The MCP tier was designed for exactly this kind of plug-in extension.* Walk the topology.

**REID:** Walk it. Because this is the bit Episode Two opened on the architecture page, and the fulfillment tier inherits the topology without adding a single new infrastructure box.

**KEVEN:** Walking it. The orchestrator is `ca-visionkit-orchestrator`, the Container Apps deployment Episodes Two and Five named. The orchestrator hosts the parent and the five specialists — Trips, Replenish, Coupons, Pharmacy, Concierge — plus the eight new fulfillment HTTP handlers under `/api/fulfillment/*` — quotes, place, list orders, detail, cancel, confirm substitution, webhook, list providers. The Catalog specialist gains three new tools — `get_fulfillment_quotes`, `place_fulfillment_order`, `suggest_substitutions`. No new Container App. The fulfillment HTTP surface lives in the existing orchestrator.

The MCP tier is `ca-visionkit-mcp`, the Container App that hosts the five existing FastMCP servers from prior episodes — cxml, parsml, merml, weather, ledger. The fulfillment tier adds a *sixth* FastMCP server, path-mounted under `/fulfillment` inside the same Container App. The new server is `fulfillment-mcp`. Five tools — `list_providers`, `get_quotes`, `place_order`, `get_order_status`, `handle_substitution`. The five tools call into the provider classes that live in the orchestrator's `providers/` package — `base.py` for the ABC and the dataclasses, and one file per provider — `instacart_mock.py`, `shipt_mock.py`, `kroger_bopis_mock.py` today, and `instacart_real.py`, `shipt_real.py`, `kroger_real.py` when the v2 partnerships land.

**REID:** Zero new infrastructure. Zero new monthly cost. Zero new external dependency.

**KEVEN:** Zero, zero, zero. The fulfillment tier ships without adding a single Container App, without adding a single Postgres database, without adding a single blob storage account, without adding a single Key Vault, without adding a single Azure Front Door rule, without adding a single virtual network, without adding a single private endpoint. The schema additions — four tables under §5.5 of the design document, `fulfillment_providers`, `fulfillment_orders`, `fulfillment_substitutions`, `fulfillment_webhook_events` — land in the existing Postgres Flexible Server. The Bronze audit tier lands new categories — `fulfillment_quote_request`, `fulfillment_quote_result`, `fulfillment_place`, `fulfillment_status`, `fulfillment_oos`, `fulfillment_sub_suggest`, `fulfillment_sub_decide`, `fulfillment_cancel` — into the existing audit chain. The architecture row on the live `/architecture` page gains one new cell — *Fulfillment plug-ins (3 mocks)* — alongside the existing agent fleet and MCP tier cells.

The seller's argument lands because the deployment lands. The customer's existing CFMP deployment is the existing deployment; the fulfillment tier is *additive*. Other delivery integration approaches require a new orchestration service, a new partner-network bridge, a new payment vault. CFMP-Fulfillment requires the customer to enable a new env var on the MCP Container App — `FULFILLMENT_PROVIDERS=instacart_mock,shipt_mock,kroger_bopis_mock` — and re-deploy the existing revision. The deploy is a label change. The cost delta is zero. The infrastructure delta is one row on the architecture page.

**REID:** And the webhook landing.

**KEVEN:** Provider webhooks land at `ca-visionkit-orchestrator /api/fulfillment/webhook`. The handler verifies the HMAC signature against a per-provider shared secret stored in Key Vault. The handler checks the idempotency table on the compound `(provider_id, provider_event_id)` to dedup retries. The handler fans the event into the substitution flow if it is an out-of-stock event, into the Cue Bus if it is a status update, into the audit chain in all cases. Every action is a LedgerRow — quote requested, quotes returned, order placed, status changed, OOS detected, substitution suggested, substitution decided, cancelled. Each carries the inheriting `trace_id` from the customer's original *"ship this Lot"* tap. The regulator's replay question from Episode Two lands a trace across the entire fulfillment chain.

The live `/architecture` URL is `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture`. Open it on a client call, and the new fulfillment tier shows up beside the agent fleet and the MCP tier. The seller's screen-share gains one cell. The buyer's mental model gains one row. The Azure spend gains zero dollars.

**REID:** One cell, one row, zero dollars. Move to the mocks-are-real-architecture commitment.

### Mocks are real architecture, not a stepping stone

**KEVEN:** The mocks-are-real-architecture commitment. The three v1 mocks — `instacart_mock`, `shipt_mock`, `kroger_bopis_mock` — are not prototypes. They are not throwaway. They are not *"we will replace this with the real thing in v2"*. They are *real architecture*. Walk the discipline.

**REID:** Walk it.

**KEVEN:** Each mock is a class that subclasses `FulfillmentProvider`. Each implements the same five methods every real provider class will implement. Each produces ProviderQuotes with the same nine fields. Each emits the same webhook events with the same shape. Each lands in the same Postgres tables. Each carries the same LedgerRows. The mocks are deterministic — `instacart_mock` has a twenty-percent substitution rate, a sixty-minute ETA, and a tunable in-stock-percent; `shipt_mock` has a one-percent substitution rate, a ninety-minute ETA, and a late-night-OK window; `kroger_bopis_mock` has a zero-percent substitution rate, hourly pickup slots, and the `handles_pharmacy=true` flag — but the determinism is for *testability*, not because the mocks are simpler than the real providers will be.

When the real provider lands — when `instacart_real.py` is implemented against the Connect API, when `shipt_real.py` lands behind the partner-program credentials, when `kroger_real.py` lands behind the Public API — *only the class implementation changes*. The orchestrator does not change. The MCP tooling does not change. The audit chain does not change. The substitution flow does not change. The Cue Bus does not change. The UI does not change. The seller's argument does not change. The customer's experience does not change. The Independence-minded posture in code is exactly this — *the customer-value-without-retailer-signoff is the default state*.

**REID:** This is what *"mocks are real architecture"* means. The abstraction is right today, not a prototype to be thrown away when the partnerships sign.

**KEVEN:** The abstraction is right today. That is the test. If the abstraction were a prototype, the team would be saying *"once we land the real provider we will rewrite the orchestrator's quote handling"*; *"once we land the real provider we will swap out the substitution flow"*; *"once we land the real provider we will redo the audit shape"*. None of that is true. The abstraction is final today. The implementation is mock today. When the implementation becomes real, the abstraction does not move.

That is also the Independence-minded posture showing up in code. The Portal episode argued that CFMP ships customer value *without* a retailer co-deployment agreement — the customer is the buyer, the retailer is the eventual integration partner, the system is operable today. The Fulfillment episode makes the same argument at the engineering layer. CFMP ships fulfillment value to the customer in v1 even with mocks, while Liu's legal team works the real DPAs for the v2 partnerships. The customer sees a working system today. The seller can demo a working system today. The buyer can run a pilot on a working system today. The retailer relationship is *additive*, not blocking.

**REID:** And the v2 transition story.

**KEVEN:** The v2 transition is a class swap. The roadmap names it explicitly — Sprint Pre-flight is the legal review of the mock-versus-real distinction, the sample API documentation review for Connect, Shipt-via-Target, and Kroger Public, and the DPIA addenda for each real provider. Sprints Zero through Five ship the mocks. The roadmap's v2 backlog ships the real classes. The deploy when the real classes land is a config change — `FULFILLMENT_PROVIDERS=instacart_real,shipt_mock,kroger_bopis_mock` — flipping one provider at a time. The customer's mental model does not change. The seller's argument does not change. The architecture is the same.

**REID:** Mocks today, reals tomorrow, abstraction unchanged. Move to the reading.

### A reading I want to do

**REID:** A reading. The episode sits at the intersection of two practitioner literatures — bounded-context design and clean-architecture dependency direction — and I want to name both.

The first is Eric Evans, *Domain-Driven Design*, Addison-Wesley, two-thousand-and-three. Twenty-three years old, still the canonical text on what a bounded context is and why it is the right unit of interface design. Evans's argument is that a bounded context is a region of the domain where a model means exactly one thing, and the interface between two contexts is the place where the meanings are translated. The FulfillmentProvider ABC is exactly an Evans bounded-context interface — *the agent fleet's model of a quote* and *the retailer's model of a quote* are different, and the ABC is where the translation happens. The retailer thinks in their own SKUs, their own service-area envelopes, their own substitution semantics; the agent fleet thinks in ProviderQuotes and dietary flags. The translation is the provider class. The bounded-context discipline is what makes the agent fleet write-once and the retailer integrations swap-many.

**KEVEN:** And the second.

**REID:** The second is Brandon Rhodes's PyCon talk *The Clean Architecture in Python*, two-thousand-and-fourteen, available on the PyCon US YouTube archive. Rhodes is the author of the python-jsonrpc-server and a long-time speaker on architectural discipline in Python. The talk applies Robert Martin's clean-architecture dependency direction — *dependencies point inward toward the domain core, never outward toward infrastructure* — to a Python codebase. The fulfillment tier is exactly that. The agent fleet is the domain core. The provider classes are the infrastructure ring. The dependency points *from* the provider class *to* the ABC, never the other way. The orchestrator imports the ABC; the provider classes implement it; the orchestrator never imports a specific provider class by name. The registry resolves by env var at startup. The dependency direction is what lets the mocks be real architecture — the core does not know which implementation is loaded; the core only knows the interface.

**KEVEN:** Evans on the principle, Rhodes on the practice.

**REID:** Evans on what a bounded context is. Rhodes on how to enforce the dependency direction so the boundary does not leak. Both worth a careful read for any engineer wiring an integration tier in twenty-twenty-six. The instinct to write a microservice per provider is the instinct that gets the *deployment* right and the *abstraction* wrong; Evans and Rhodes together name why.

**KEVEN:** Read them in that order — Evans first for the framing, Rhodes for the implementation. Move to the disagreement.

### One disagreement

**REID:** One disagreement. The cleanest tension the fulfillment tier carries — Tanaka versus Mendez. The SRE versus the customer-support principal. Put it on tape.

**KEVEN:** Put it on tape.

**REID:** Tanaka's position, from Section Eight-Point-Four of the design document. *"Three providers means three ways to fail. Plan for any of them going down."* The SRE's instinct — protect the platform, isolate the failure, prevent cascading degradation. Tanaka wants the circuit breaker to be *aggressive*. Three timeouts in sixty seconds for a given provider, mark the provider unhealthy for five minutes, no questions asked. The breaker takes the provider out of the rotation; the aggregator stops fanning out to that provider until the cooldown elapses; the customer is served the surviving providers' quotes. The platform is protected. The blast radius is contained.

Mendez's position, from Section Eight-Point-Six of the design document. *"When a provider screws up, the customer should hear from us first, not the receipt email."* The customer-support principal's instinct — never let the customer see the failure as a 503. When a provider fails, the agent absorbs the failure and *proposes a recovery action* in the same UI moment. The substitution-with-recovery cue from Section Three-Point-Five — *"Shipt is having issues right now. Want to send that gochujang via Instacart instead?"* The customer one-taps the alternative. The Lot's chosen provider is updated. A new `place_order` call goes out to the alternative. The LedgerRow records both the failed attempt and the recovered route. The customer never sees the 503.

Now the tension. Aggressive circuit-breaking might mark a provider unhealthy after a transient blip — a single bad sixty-second window during which the provider was actually mostly fine — and the customer still wanted that provider. Conservative circuit-breaking leaks failure UX — the customer waits four seconds, then four more, then four more, while the system keeps trying a provider that is genuinely down. Where is the line?

**KEVEN:** Both are right. The convergence layers them.

**REID:** Bring it.

**KEVEN:** *Circuit breaker and agent-mediated retry, layered.* Three layers, in order.

Layer one. *First failure — silent retry with exponential backoff.* The provider returned a 5xx or timed out. The orchestrator retries internally — a single retry with a backoff in the hundreds of milliseconds. The customer's spinner is still spinning; the customer has not been told anything; the system is absorbing the blip. If the retry succeeds, the customer sees a slightly slower quote but is otherwise unaffected. No LedgerRow surfaces failure; the row records the retry as metadata.

Layer two. *Second failure — propose recovery action to the customer in real time.* The retry failed; the provider is genuinely impaired. The orchestrator does not surface a 503; the orchestrator composes a recovery cue. *"The same-day delivery is having issues right now. Want to send your order to the warehouse-club delivery instead?"* The customer one-taps. The Lot's chosen provider is updated. A new `place_order` goes to the alternative. The customer experiences *agent absorbed the failure and gave me a choice*, which is exactly Mendez's commitment. The LedgerRow records the failed attempt, the recovery proposal, the customer's decision, and the new route. Mendez wins the immediate UX.

Layer three. *Third failure within sixty seconds — mark the provider unhealthy for five minutes.* The pattern is now multiple failures in a short window; the provider is impaired, not blipped. The circuit breaker trips. The aggregator stops fanning out to that provider for the next five minutes. New quotes are served from the surviving providers. The customer never sees a 503; the operations team sees the circuit-breaker state on the Portal as a system-tagged row in the trace. Tanaka wins the platform reliability. The breaker is the floor; the agent-mediated retry is the ceiling; the two together cover the full spectrum.

**REID:** And the failure mode if the convergence breaks.

**KEVEN:** If only the breaker fires — Tanaka without Mendez — the customer sees a clean error sometimes and waits in silence other times, depending on whether the breaker has tripped yet. The customer's mental model is *the system is fragile*. If only the agent-mediated retry fires — Mendez without Tanaka — the platform takes the brunt of a sustained provider outage; the orchestrator keeps trying the bad provider for every customer; the queue depth grows; the latency degrades for everyone. The customer's mental model is *the system is slow*. Layering them gives the customer's mental model the third reading — *the system absorbs failures and recovers*. That is the experience the architecture earns.

**REID:** Converge accepted. *Agent-mediated retry at the customer UX; circuit breaker at the platform reliability; both LedgerRows sealed.* Carry it.

### What to carry forward

**KEVEN:** Three things into Episode Eight. Numbered, because the listener carries them.

**KEVEN:** *One — the interface IS the product.* Vargas's line, verbatim. One ABC, many implementations. The FulfillmentProvider abstract base class is what lets the agent fleet reason across retailers without writing per-retailer agent code. The ProviderQuote shape is what lets the ranker compose a recommendation in eight words without branching on provider identity. The interface is the product. The provider implementations are the inventory. Carry that.

**KEVEN:** *Two — dietary safety is enforced at the search step.* Hassan's defense-in-depth posture. The LLM never sees an allergen the customer can't eat because the search step filters the candidate set before the LLM is invoked. The substitution flow is the highest-risk LLM moment in CFMP, and the architecture's response is structural — make the unsafe candidates invisible to the model, not just unrecommended. Get it wrong, the customer eats peanut. Don't get it wrong. Carry that.

**KEVEN:** *Three — mocks are real architecture, not a stepping stone.* When the real provider lands, only the class implementation changes — the orchestrator, the MCP tooling, the audit chain, the substitution flow, the UX, the seller's argument, the customer's experience — none of them change. That is the Independence-minded operating model showing up in code. The customer-value-without-retailer-signoff is the default state, the same way the Portal episode argued. CFMP ships fulfillment value in v1 with mocks while the legal team works the real DPAs. Carry that.

**REID:** Three carries. Interface is the product. Dietary safety at the search step. Mocks are real architecture. Into Episode Eight.

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
