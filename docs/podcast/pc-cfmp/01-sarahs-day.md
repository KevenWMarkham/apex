# Episode 01 · Sarah's Day — The Customer Problem CFMP Exists to Solve

**Episode 01 · Sarah's Day** — five frictions in one week, one design that answers all of them. We meet the five archetypes, name the unifying noun, the headline interaction, and the success metrics — and we land on why the audit chain shows up in episode one of a customer-experience podcast.

**Builds on:** the show bible (00-show-bible-and-format) · CFMP Mobile Design Document §§ 1–2 · CFMP Mobile Shopper Experts panel
**Run time:** ≈ 40 minutes target
**Last updated:** 2026-05-25

---

## Cold Open

[Sound: a kitchen on a Sunday morning. The whoosh of a dishwasher mid-cycle. A child off-mic asking, *Mom, can I have waffles?* The clink of a coffee mug going down on a granite counter just a hair too hard.]

It is eight-fourteen on a Sunday morning and Sarah Chen has three apps open on her phone. The retailer's loyalty app, because the digital circular dropped overnight and she has not yet seen what is on sale this week. A grocery-delivery app, because the cart she half-built last Wednesday is still sitting there, two items short of the minimum for free delivery. And Pinterest, because somewhere on Friday night she pinned a sheet-pan dinner she now cannot find, even though she remembers it had something to do with gochujang and a quartered cabbage.

Her older daughter is asking about waffles. Her younger one has discovered the dog's water bowl. Sarah is forty-five minutes into what she had told herself, at seven-thirty, would be a ten-minute grocery plan. The meal she has finally landed on calls for gochujang. Her store does not carry it. She switches to a fourth app — the one that promises two-hour delivery on the things the regular delivery service does not stock — and now she is in a different account, a different cart, a different checkout, a different password reset, because she has not used this app since the holidays.

She does not finish. The kids win. Waffles happen. The grocery plan slides to Sunday night.

By Tuesday she is back at the store anyway because she forgot the diapers, and the bottom-shelf coupon barcode she scans goes to a web page that will not load on cellular. She buys the diapers full price. By Wednesday her older daughter announces — twelve minutes before bed — that her birthday party is THIS Saturday, and the list now needs to be peanut-free for one guest, vegan for another, and under a number Sarah will not say out loud. By Thursday the romaine she bought Sunday is wilted in the back of the fridge. Four dollars in the trash. Dinner pivots to whatever the freezer will surrender.

And then Friday she is at her mother's house, and her mother is out of the diabetic-friendly snacks she has come to rely on. Sarah opens her phone to reorder them — to her mother's address, not hers, on a different account she shares with her father, with a payment method that is not her own. Three taps in, she gives up. She drives to the store herself.

That is Sarah's week. Five distinct frictions. Five different moments where the technology she is using does not understand the shape of the life she is living.

[Sound: a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start there. Sarah's week. Because this is the moment CFMP exists to solve.

**REID:** Five frictions in seven days. None of them is the technology being broken in the technical sense — every one of those apps works, every one of them has a five-star review somewhere. The technology is broken in the *fit* sense. None of it understands that Sarah's grocery life is one continuous problem, and the apps keep handing her back fragments of it.

**KEVEN:** Welcome to the CFMP Podcast. Eight episodes. I'm Keven Markham, twenty-two years on the Microsoft platform. I run the Microsoft Technology and Services practice at Deloitte. I sell, I architect, and I live in the gap between a designer's intent and what a Microsoft seller can actually defend in front of a CIO.

**REID:** I'm Reid. Cross-cloud principal architect. I have built production retail and consumer workloads on AWS, on GCP, and on Microsoft. I'm here as the honesty enforcer. When the design is doing something distinctive, I will name it. When it is doing something every grocery app on the market does and dressing it up in agent language, I will name *that* too. The argument has to defend itself.

**KEVEN:** Episode One. *Sarah's day.* The customer problem the Customer Focused Merchandise Pack — CFMP — was built to solve. Let's go.

---

## The conversation

### The shape of Sarah's week

**KEVEN:** Let's walk the five frictions one at a time, because each one corresponds to a different piece of CFMP, and that is not a coincidence. The design started here. The architecture is the answer to the moments, not the other way around.

**REID:** Name the moments and the answers. I will push on each one.

**KEVEN:** Sunday morning. Three apps open. Sarah is trying to compose a week's worth of meals from four different surfaces that do not talk to each other. The CFMP answer is the *lot* — a single nameable object that holds the intent, and the agent fleet composes against it. The user does not move between apps; the agent composes between sources behind one surface.

**REID:** And here is where I push. Every grocery app will tell you they have a meal-plan-to-cart flow. The retailer apps have it. The delivery apps have it. Why is the CFMP answer different?

**KEVEN:** Two reasons. First, the existing flows are *intra-retailer* — the retailer's meal plan composes against the retailer's catalog. None of them can compose a meal plan that draws from *multiple sources* plus the pantry Sarah already has. CFMP composes across them because the lot is the unit of intent, not the catalog. Second, the existing flows are *one-shot* — the cart closes at checkout and disappears. The CFMP lot has a *lifecycle* — cart, pickup, pantry, next meal plan. The loop closes.

**REID:** A meaningful distinction. Whether it is *enough* of a distinction to matter to Sarah on a Sunday morning is the question I will hold open.

**KEVEN:** Hold it open. Tuesday — the coupon barcode that will not load on cellular. The CFMP answer is *scan-first*. When Sarah scans, the response is a fact — the canonical product, the offers available to her, the price after her loyalty discount, the alternative if her store is out. The agent has the offers cached against her profile; the scan is the trigger, not the network round trip.

**REID:** I will press harder. *Scan-first* is not a CFMP invention. Yuka does it. Google Lens does it. Every barcode-detect SDK does it.

**KEVEN:** Correct. What CFMP does that those do not is treat the scan as *handing the agent a known entity* — not as a lookup. Yuka tells you what the product is. Lens tells you where to buy it. CFMP scans, and the agent then composes — coupon, substitution, pantry check, lot membership, dietary block, route to aisle — all from the one scan. The barcode is the question the agent gets asked.

**REID:** Now I am with you. Move on.

**KEVEN:** Wednesday. Twelve-minutes-before-bed birthday party. Peanut-free for one guest, vegan for another, budget-aware. This is where the agent fleet earns its keep. The party is a *purpose-bound lot* — an EventLot. The agent gets the constraints, composes a list against the household's existing dietary policy plus the guests' constraints plus the budget plus the retailer's stock, and hands Sarah a list she can edit, not a list she has to build from zero.

**REID:** The composability claim only holds if the constraints are *first-class* — if peanut-free is a structured attribute the agent reasons about. Is it?

**KEVEN:** It is. The dietary policy is a row in the household profile with version history. The agent reads it on every compose. Episode eight walks the consent and HIPAA story.

**KEVEN:** Thursday. The wilted romaine. Four dollars in the trash. The CFMP answer is *the PantryLot* — a lot that comes into existence the moment a delivery is received, with each item carrying its provenance and its expected shelf life. The agent is allowed to *nudge* when something is approaching its end. Wednesday morning Sarah gets a soft prompt: the romaine will be best used tonight. Want to swap tomorrow's meal? She taps yes. The meal plan shifts. The romaine becomes dinner.

**REID:** And this is where the success metric lives or dies. Industry-average household food waste is twenty-four percent. The design target is under eight percent. The most specific behavior-change claim in the entire design document. If CFMP cannot move that number, much of the rest is a feature catalog.

**KEVEN:** Agreed. We come back to it. Friday — the remote care. Sarah at her mother's house, ordering diabetic-friendly snacks to her mother's address from her mother's account. The CFMP answer is *the CareLot*. A lot that lives in her mother's account, that Sarah is delegated to act inside of, with the audit chain recording every action — but with a strict information boundary. Sarah can reorder the snacks. Sarah cannot see her mother's pharmacy refills.

**REID:** And that is why the customer-experience podcast has to mention the audit chain in episode one. The user never sees it. But the *capability* — *I am over here, acting on behalf of someone over there, with constrained visibility* — is only safe to ship if the audit substrate is real.

**KEVEN:** Five frictions. Five moments. Five pieces of the design. Each one is a *fit* answer — the technology bending to the shape of Sarah's life instead of asking her to bend to it.

### The five archetypes

**KEVEN:** The design document does something I want to draw attention to. It does not start with a generic shopper. It starts with five named humans, each carrying a household, a device, a budget, a dietary reality, and a primary device profile. The breadth of the app — the architecture, the agent fleet, the lot taxonomy — is *forced* by the breadth of these five.

**REID:** Five is an interesting choice. Pick the number. Why not three? Why not seven?

**KEVEN:** Because every one of the five breaks a different capability. Drop any one of them and the design contracts to something narrower. I will walk them.

**KEVEN:** Sarah Chen. Thirty-eight. The cook. Household of four, one kid with a peanut allergen. Twenty-one hundred dollars a month. iPhone, mostly on the go, often one-handed with a stroller. Sarah is the *velocity* archetype. The design has to be fast, has to be forgiving, has to handle scanning while pushing a cart, has to compose meal plans across a week without her writing them. Without Sarah, the design becomes a leisurely browsing experience and the velocity disappears.

**REID:** Highest-frequency user. Not the highest-lifetime-value user. Keep going.

**KEVEN:** Robert Park. Seventy-one. The steady eddie. Lives alone. Daughter Diana has caregiver oversight. Four hundred and eighty dollars a month, diabetic, low-sodium, weekly prescription refills. Older Android, slower cellular, clumsy with biometric authentication. Robert is the *clarity* archetype. Large type, predictable navigation, voice prompts that wait for him, fallback paths that do not punish him when the camera fails. Without Robert, the design becomes a power-user toy and the senior population — the highest-lifetime-value population in grocery — falls out.

**REID:** Robert is where the accessibility architecture earns its keep. Simple-mode toggle, spoken directions, large-text mode — not nice-to-haves. Price of admission for the population that spends the most.

**KEVEN:** Diana Park. Forty-four. Robert's daughter. The proxy. She has her own household and on top of that she carries the cognitive load of monitoring her father's. Diana is the *delegation* archetype. She introduces the four-identity chain — Diana acting on behalf of Robert, with the audit chain recording who took the action on whose behalf, and the consent boundary blocking pharmacy information from crossing into Diana's view. Without Diana, the senior population becomes unreachable the moment they can no longer manage their own grocery.

**REID:** Diana forces the HIPAA-adjacency conversation into episode one. Pharmacy data is regulated. The CareLot pattern makes the delegation safe. Episode eight walks it; we name it here because Diana exists.

**KEVEN:** Marcus Thompson. Thirty-five. The coordinator. Books a cabin every year for himself and four friends. Marcus is the *displacement* archetype — the persona that proves the household is not a fixed address. He needs a lot that follows him, that friends co-edit, that splits payment, that stages deliveries against the property, that closes out cleanly when the trip ends. Without Marcus, the design assumes one household at one address, and the entire StayLot capability does not exist.

**REID:** Marcus hits the assumption every grocery app makes by default — that the household is one place. The StayLot is the most distinctive thing in the design, and it exists because Marcus exists.

**KEVEN:** And the fifth. Marcus Liu. Twenty-nine. The optimizer. Single-occupant household. Three hundred and eighty dollars a month. Pixel, urban Wi-Fi, sustainability-minded, intermittent fasting, high-protein. Marcus Liu is the *quick-reorder* archetype. Same six things every week, scan history remembers them, sustainability badges are honest, transaction takes under thirty seconds. Without him, the design over-rotates on family and senior use cases, and the largest growing demographic in urban grocery falls through.

**REID:** And Marcus Liu is the persona who least *needs* the agent. His pattern is so regular the system serves him with auto-replenish and a quick-reorder button. Which is a design forcing function — the agent fleet has to know when *not* to compose. When the answer is "the same thing you had last Tuesday," the agent should say that and get out of the way.

**KEVEN:** So that is the five. Sarah — velocity. Robert — clarity. Diana — delegation. Marcus Thompson — displacement. Marcus Liu — quick-reorder. Each one breaks a different capability. Drop any of them and the design contracts.

**REID:** I will accept five. I will note that there is a real argument for a sixth — the cross-shopper, the person with food insecurity who is shopping across SNAP-eligible items and value brands and bulk staples — but that conversation belongs to a later episode if the design picks it up.

### The unifying noun — LOT

**KEVEN:** Now the noun. Because if you ask me what the most important architectural decision in CFMP is, it is not the model, it is not the cloud, it is not the agent runtime. It is the noun the design organizes itself around.

**REID:** Name it.

**KEVEN:** The lot. A *lot* is a bounded set of intents about commerce in a household over a window of time. It has an identity. It has a kind. It has members. It has a lifecycle stage. It has bindings — to a time, to a place, to a purpose. It has provenance — how it came into being. It has telemetry — what was consumed, what was wasted, when.

**REID:** And the noun matters because?

**KEVEN:** Because every other grocery app organizes itself around a *list* or a *cart*. And a list is a snapshot. A cart is a transaction. Neither of them has an identity that survives the moment. The list goes stale and the user starts a new one. The cart closes at checkout and disappears. The lot is the first abstraction in this category that has an identity, a state, and an audit trail across the full lifecycle — from intent to fulfillment to consumption.

**REID:** Four lot archetypes. Walk them.

**KEVEN:** Four named patterns. The *Shopping Trip* — the canonical cart-becoming-pickup-becoming-pantry flow, where the lot moves through stages as the household does. The *Auto-Replenish* — the cadence-bound subscription pattern, where the lot is generated on a schedule from a household's consumption signal, and Sarah does not have to think about milk and bread and diapers ever again. The *StayLot* — the displacement pattern that follows the household to a cabin or a beach house or a parent's home for the holidays, with destination binding and friend co-editing and staged deliveries. And the *Care-Lot* — the delegation pattern, where one identity acts on behalf of another with a consent boundary and an audit trail.

**REID:** And the reason "lot" beats "list" or "cart" — restate it.

**KEVEN:** A list is what I am thinking about. A cart is what I am buying. A lot is *the thing itself* — the household reality that the list and the cart are both fragmentary views of. The list is a query against the lot. The cart is a transaction against the lot. The receipt is a receipt against the lot. The pantry is what the lot turned into. The next meal plan is a query against what the lot left behind.

**REID:** That is the argument. I will accept it. I will note that this is the kind of abstraction that pays off only if the system actually *uses* the lot as the unit of work everywhere — if the agent calls return lots, if the UI surfaces lots, if the audit chain records lots, if the analytics roll up against lots. The moment the abstraction leaks — the moment one corner of the system treats a lot as a list — the value of the noun collapses.

**KEVEN:** Which is why episode three goes deep on the lot model and the four archetypes. The architectural commitment is real; the engineering discipline to hold it is non-trivial. We will defend that in episode three.

### The headline interaction — SCAN

**KEVEN:** Now the verb. Because if the noun is the lot, the headline verb — the interaction that defines what the surface *feels like* — is the scan.

**REID:** And we are going to land on why scan-first, not search-first.

**KEVEN:** Right. Most retail apps lead with search. A search box at the top, a list of categories underneath, a deals carousel at the bottom. The user is expected to know what they want, type it, and pick from results. This works for the seventeen percent of grocery interactions that are a planned, named purchase. It fails for the other eighty-three percent — where the user has a thing in their hand, or a thing they saw on a shelf, or a photo a friend texted them, and they do not know what to call it.

**REID:** And the answer is — point the camera at it.

**KEVEN:** Point the camera at it. Sarah does not know the SKU for the gochujang. She does not know the brand. She does not know how to spell it. She knows it has a red label and a Korean character on it. She points the camera at it — the camera Yuka and Google Lens and Vivino have already taught her how to use — and the system takes it from there.

**REID:** Now I get to push. *This is just a barcode reader.* Every grocery app has a barcode reader. The retailer apps have had them since 2014. Why is the CFMP scan distinctive?

**KEVEN:** Two reasons. First, the scan is the *front door*, not a feature. The home screen is a camera viewport. There is no other primary affordance competing for attention. The user does not have to think *should I scan or should I search* — the system has already chosen scan, and the search is a fallback inside the chat composer. That is a design commitment, not a feature.

**REID:** Acceptable. And the second?

**KEVEN:** The second is more interesting. The scan hands the agent fleet a *fact*. Not a guess. A canonical product identifier, resolved against an open product catalog, normalized to the retailer's SKU when available, with allergen flags and nutrition and pricing already attached. The scan is what makes the rest of the agent fleet trustworthy — because every downstream composition is anchored on a known entity, not on an interpretation of the user's typing.

**REID:** And here is where you will pre-empt episode two. Why is the scan returning a *fact* and not a *guess*?

**KEVEN:** Because of the MCP boundary. The scan resolver is a Model Context Protocol tool — a typed, audited interface between the agent fleet and the catalog. The agent does not get to *infer* what the product is. The agent gets to *call* the scan resolver, which returns a structured fact, which the agent then composes against. The boundary is what makes the guess unavailable.

**REID:** And the audit chain records every call across that boundary.

**KEVEN:** Every call. Every scan, every catalog lookup, every coupon resolution, every alternative suggestion. The audit chain is what proves, on Tuesday, that the offer Sarah saw on Sunday was a real offer, that the price she was quoted was the price she would have paid, that the dietary block on the peanut product was triggered for the right reason. Episode two unpacks the agent fleet and the audit chain in full. Episode three goes deep on the lot. Today we are naming the surface.

**REID:** So scan-first is not a UX flourish. It is the architectural move that lets the agent fleet hand the customer a fact. I will accept that framing.

### What success looks like

**KEVEN:** Now the metrics. Because the design has to be measurable, and the design document commits to three numbers. Let's walk them.

**REID:** Read them. Don't paraphrase.

**KEVEN:** First metric. *Time from "I need groceries" to a complete order.* Target: under five minutes for a returning user. Today: roughly thirty to forty-five minutes on competing tools. That is the Sunday-morning metric. That is the friction we opened the episode on.

**REID:** And what makes it a behavior-change signal and not a vanity stat?

**KEVEN:** Because the friction itself is what causes Sarah to abandon. The forty-five-minute Sunday is the reason she does not finish her grocery plan, the reason she ends up at the store anyway on Tuesday, the reason the romaine wilts on Thursday. The five-minute target is not about speed for its own sake. It is about *completion*. If Sarah finishes on Sunday, the rest of the week's frictions collapse. The metric is a proxy for the entire downstream cascade.

**REID:** Second metric.

**KEVEN:** *Household food-waste rate.* Target: under eight percent. Industry average: twenty-four percent. Today, not measured by any competitor. This is the wilted-romaine metric.

**REID:** And this one I want to stress-test. Eight percent is a third of the industry average. The design claim is that CFMP will reduce household food waste by a factor of three. Defend it.

**KEVEN:** The design claim is built on three things working together. The PantryLot — the system knows what is in the household and when it arrived. The expiry tracking — each item carries an expected shelf life and the system knows when it is at risk. And the meal-plan re-composition — when an item is at risk, the agent re-composes tomorrow's meal to use it. None of those three on their own moves the needle. All three together is the bet. The bet is that the *information asymmetry* — Sarah not knowing what is about to expire — is the primary cause of waste, and closing the asymmetry closes most of the waste.

**REID:** I will accept that the bet is reasonable. I will also note that the metric is the most demanding claim in the design document, and the design has to hold itself accountable to measuring it honestly. If CFMP cannot measure household waste at the SKU level, the eight-percent target is unfalsifiable, and an unfalsifiable target is not a metric — it is a marketing line.

**KEVEN:** Agreed. The measurement story has to be real. PantryLot consumption events plus throw-out events plus shelf-life timing — those are the inputs. Whether the system actually captures them at the fidelity required is an engineering commitment, not a slogan.

**REID:** Third metric.

**KEVEN:** *DAU-over-MAU retention at week twelve post-install.* Target: at least thirty-five percent. Today: twelve to eighteen percent for the category leaders.

**REID:** And the behavior change is?

**KEVEN:** That this is the only one of the three metrics that measures whether Sarah actually comes back. Time-to-order measures one moment. Food-waste measures a household-level outcome. DAU-over-MAU at week twelve measures whether, three months after install, the app is still part of Sarah's life. Thirty-five percent at week twelve is roughly double the category average. The bet is that the lot — the persistent, lifecycle-bearing object — is what creates the return reason. Every other grocery app's retention falls off because each session is independent. The lot makes the session a continuation of the last session.

**REID:** And if the lot doesn't, the retention number doesn't move.

**KEVEN:** Correct.

**REID:** Three metrics. None of them is a vanity number. Each one corresponds to a specific design hypothesis. If any of the three misses, a piece of the design is wrong. That is what a metric set is supposed to do. I will accept the set.

### The audit chain — why we mention it in episode one

**KEVEN:** I want to close on something that may surprise the listener. This is a customer-experience podcast. Episode one is about Sarah. And I am about to mention, for the third time, the audit chain. Episode two will unpack it in full. Why does it belong here, in the persona episode?

**REID:** Because it is the trust substrate. And the trust substrate is the design, not an afterthought.

**KEVEN:** That is exactly it. Walk Sarah's week again. The wilted romaine — the agent told her on Wednesday that the romaine would be best used by tonight. Sarah has to *trust* that the recommendation is honest, that the system is not just nudging her to buy more produce. The cabin pre-stock for Marcus Thompson — Marcus is letting CFMP order groceries to an address that is not his home, paid for by friends he is splitting with. Marcus has to *trust* that the splits are right and the deliveries are real. The remote care for Sarah's mother — Sarah is acting on behalf of her mother. The mother has to *trust* that Sarah cannot see what she is not entitled to see. Every one of those trust claims is backed by an audit row. Every action is a ledger entry. Every cross-identity action is recorded with both identities and the basis of the delegation.

**REID:** And the user never sees those rows. The user just experiences the trust. The audit substrate is invisible — but it is the only reason the trust is real.

**KEVEN:** Episode two takes the audit chain apart. The hash-chained ledger. The trace-ID propagation across the agent fleet. The replay-token validation that lets a regulator re-run a decision and prove the agent would produce the same answer. Why we built it on Postgres with eventual OneLake promotion. How the four-identity chain — agent, operator, source, auditor — threads through every row.

**REID:** And the reason we name it in episode one, before we unpack it in episode two, is because the customer-experience claims in this episode are *not credible* without it. Sarah's Friday — the remote care for her mother — is a beautiful design moment. It is only a *safe* design moment because the audit chain exists. If the audit chain is bolted on later, the Friday moment cannot ship. The trust substrate has to exist on day one or the customer experience does not.

**KEVEN:** That is the bridge to episode two. The customer experience is the surface. The audit chain is the foundation. We named the surface today. We unpack the foundation next.

### A reading I want to do

**REID:** I want to recommend a reading. It is going to feel obvious to some of the audience, but I want to recommend it because the design document we are working from leans on it implicitly and I think it deserves to be named on tape.

**KEVEN:** Name it.

**REID:** Clayton Christensen, *Competing Against Luck.* It is the popular treatment of jobs-to-be-done — the framework Christensen developed and refined across his last decade. The argument is that customers do not buy products; they *hire* products to do a job. The job is anchored in a situation — a circumstance, a constraint, a moment in a life — and the job is what you have to design for. The product is the means. The job is the end. Christensen's example is the milkshake — the morning-commute milkshake hired to do the job of *making a long drive less boring without making me feel guilty*. The afternoon milkshake hired to do a completely different job — *placating a kid without spoiling dinner*. Same product. Two jobs. Two designs.

**KEVEN:** And the relevance to CFMP is —

**REID:** That Sarah's five frictions are five different jobs, and the design respects that. The Sunday-morning compose-a-week is a different job from the Tuesday in-store coupon scan, which is a different job from the Friday remote-care reorder. Christensen would tell you that if you design one product to do all three jobs, you will fail all three. CFMP's response is not to ship three apps — it is to ship one app with a noun architecture that *recognizes* the job from the context. The lot is the jobs-to-be-done abstraction made concrete.

**KEVEN:** I will push gently. Christensen's frame is powerful but it has a trap. The trap is that you can over-rotate on jobs and lose the architectural discipline. Every job becomes a feature, every feature becomes a screen, every screen becomes a tab. You end up with a six-tab nav and twenty-four use cases and the cognitive load Sarah cannot carry.

**REID:** Which is why CFMP went scan-first. The job-recognition happens *behind* one surface, not *across* many surfaces. Christensen would approve of that move. It is the right reading of his frame.

**KEVEN:** Agreed. *Competing Against Luck* is the one. I would pair it with a shorter read — the Tony Ulwick *Harvard Business Review* article from 2002, *Turn Customer Input Into Innovation*, which gives you the more rigorous, less narrative version of the same argument. Read both. They sharpen the same blade from two angles.

### One disagreement

**REID:** I have one disagreement, and I want to put it on tape.

**KEVEN:** Put it on tape.

**REID:** *This is just a grocery app dressed up in agent language.* The auto-replenish is a feature on every grocery app. The StayLot is a logistics integration that any of the major delivery platforms could build in a sprint. The loyalty layer is already done by every retailer with a CRM team. The scan-first home is a Yuka clone. The meal-plan composition is what every recipe app has tried for fifteen years. I can find each of these capabilities, individually, on a shipped product today. So what is the actual claim CFMP is making that no shipped product is currently making?

**KEVEN:** Four things no single shipped product does.

**KEVEN:** First — the cross-retailer compose-from-anywhere lot. No single retailer app lets Sarah build a meal plan that pulls produce from one source, the gochujang from a second, and the diabetic snacks from a third — all in one lot, with one checkout intent, because Sarah's job is *the meal*, not the retailer.

**REID:** And the retailers do not want to enable that — because the moment they do, they cede the customer relationship to the layer above. Which is exactly why this only works as an *agentic pack* rather than a retailer feature. The retailer is a *source*, not a *destination*.

**KEVEN:** Second — the audit chain that lets a caregiver participate in a senior's grocery and pharmacy without seeing protected information. Diana acts on behalf of Robert. Diana can reorder the diabetic snacks. Diana cannot see the prescription refills. The information boundary is enforced at the agent layer, the consent is recorded in the ledger, and the regulator can replay the chain. No retailer app ships this — because no commercial grocery app has the audit substrate.

**REID:** And CFMP has it because the framework underneath — the Acceleration Framework, productized on Microsoft as APEX-M — has it. The audit chain is not a CFMP feature. It is a pack-level capability.

**KEVEN:** Third — the agent that composes a meal plan from pantry plus allergies plus budget plus the retailer's stock. No retailer has the pantry. No recipe app has the cart. No delivery app has the allergies. The composition happens at the agent layer because the agent has access to all four sources at once — and the audit chain records every composition so the recommendation can be defended.

**REID:** And the composition only works if the agent calls across sources with a clean tool boundary — the MCP boundary we unpack in episode three.

**KEVEN:** Fourth — the StayLot that follows the household to the cabin. Not as a logistics integration that hardcodes a property type, but as a *generalized displacement pattern* — the household is mobile, the lot moves with it, the friends co-edit, the deliveries stage against the destination. The cabin is one instance. The beach house, the parent's house at Thanksgiving, the kid's college dorm — same pattern. The generalization is the move.

**REID:** A logistics integration ships one feature. A pattern ships an infinite family of features. I will accept the distinction.

**KEVEN:** So I concede your premise — *the individual capabilities exist in the market* — and reject your conclusion. It is not a grocery app dressed up. It is a *pack* — an agentic substrate that the grocery surface happens to use.

**REID:** I accept that framing. With one caveat. It only holds if Deloitte and the client follow through on the substrate commitment. If the audit chain becomes a log file, if the MCP boundary becomes a REST API, if the lot becomes a JSON blob — then we have built a grocery app dressed up in agent language. The discipline is the difference.

**KEVEN:** Agreed. The substrate is what makes it not a grocery app. The substrate is what every episode after this one defends.

**REID:** Converge. The pack is a pack, not a grocery app. The discipline is the next eight episodes.

### What to carry forward

**KEVEN:** Three things the listener carries forward into episode two.

**KEVEN:** One. The unifying noun is **lot**. Every conversation about CFMP — from the design review to the seller pitch to the regulator's audit — returns to the lot. If the conversation drifts to a list or a cart, it has drifted out of the architecture. Pull it back to the lot.

**KEVEN:** Two. The headline interaction is **scan**. Scan-first is not a UX flourish. It is the architectural move that lets the agent fleet hand the customer a fact instead of a guess. Every other capability — meal-plan composition, dietary block, coupon resolution, lot membership, route to aisle — is composed on top of the fact the scan returns.

**KEVEN:** Three. The audit chain is the trust substrate. Sarah's Friday — the remote care for her mother — is only safe to ship because the audit chain exists. Marcus Thompson's cabin pre-stock is only safe to ship because the audit chain exists. Diana's caregiver oversight of Robert is only safe to ship because the audit chain exists. Episode two takes the audit chain apart. The substrate is what makes the customer experience possible. The customer never sees it. They just trust the surface, because the substrate is real.

**REID:** Lot. Scan. Audit chain. Three nouns. Carry them into episode two.

**KEVEN:** Next episode — the agent fleet and the APEX audit chain. We walk the parent-orchestrator-and-child-fleet pattern, the ledger row, the trace-ID propagation, and the Azure deployment topology anchored on the live `/architecture` page. The substrate, unpacked.

[Sound: the closing sting. ~6 seconds.]

---

## Further reading

- **Source docs**
  - CFMP Mobile Design Document — `C:\code\iot_device\docs\packs\CFMP-Mobile-Design-Document.md` — sections 1 (Why) including §1.1 the day-in-the-life vignette, §1.2 the vision, §1.3 success metrics; section 2 (Who) with the five archetypes and the non-human actors
  - CFMP Mobile Shopper Experts — `C:\code\iot_device\docs\packs\CFMP-Mobile-Shopper-Experts.md` — the seven domain experts who stress-tested the design; archetype refinements
  - CFMP Mobile Lots Expert Focus — `C:\code\iot_device\docs\packs\CFMP-Mobile-Lots-Expert-Focus.md` — the lot taxonomy and the four-archetype lifecycle
  - CFMP Mobile Scan-First Design — `C:\code\iot_device\docs\packs\CFMP-Mobile-ScanFirst-Design.md` — the simple-in / powerful-out design pivot that made scan the front door
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — the deployment topology Reid walks in episode two
- **Industry / analyst**
  - Clayton Christensen, Taddy Hall, Karen Dillon, David Duncan — *Competing Against Luck: The Story of Innovation and Customer Choice* (HarperBusiness, 2016) — the popular treatment of jobs-to-be-done; the framework the five-archetype design rests on
  - Tony Ulwick — *Turn Customer Input into Innovation* (Harvard Business Review, January 2002) — the rigorous, outcomes-driven version of the same argument; pairs well with Christensen
  - IDEO — *The Field Guide to Human-Centered Design* (IDEO.org, 2015) — the design-research playbook for the kind of persona work the CFMP design document does; useful for teams trying to repeat the method on a different pack

— end of episode 01 —
