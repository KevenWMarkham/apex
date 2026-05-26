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

**KEVEN:** Picture Sarah's Sunday again. The dishwasher mid-cycle, the kids asking about waffles, four apps open, none of them holding the *thing she's actually doing* — which is *feeding her household for a week.* Every app she has carries a fragment of that thing. None of them carries the thing itself. The single most important design decision in CFMP is that we named the thing. We gave the household's grocery reality a noun. Everything else hangs from that.

**REID:** Name it.

**KEVEN:** The lot. Sarah's Sunday-through-Saturday isn't a list and isn't a cart. It's a *bounded thing in her life* — what she's planning to feed her family, where the food comes from, when it's coming, what's still in the pantry from last week, who's coming over Saturday. That bounded thing has a name. It's the lot. It has a beginning and an end. It moves through stages — *I'm thinking about it · I've bought it · I've received it · I'm cooking from it · it's used up.* Every other grocery app organizes itself around the moment Sarah is in. CFMP organizes itself around the lot Sarah is living inside.

**REID:** And the customer-feel difference.

**KEVEN:** A list is what Sarah is thinking about right now. A cart is what Sarah is buying right now. Neither of them survives the moment. The list goes stale Tuesday and Sarah starts a new one. The cart closes at checkout and disappears. The lot is the *household's actual reality* — the thing the list and the cart are both fragmentary views of. Sarah doesn't have to rebuild the context every time she opens the app, because the lot is still there, still where she left it, still holding the meal plan and the pickup time and the dietary policy and the wilted-romaine warning all together.

**REID:** Four lot archetypes. Walk them as customer moments.

**KEVEN:** Four customer moments, four lots. *The shopping trip* — Sarah's Sunday-to-Tuesday cycle, where the lot starts as a meal plan and ends as the food in her fridge. *The auto-replenish* — the household rhythm Sarah doesn't want to think about; the milk that lands every Wednesday, the diapers every ten days, the things she stops having to remember. *The stay-trip* — Marcus's cabin weekend, the lot that follows the household to a different address, friends co-editing, payment splitting, deliveries staging against the cabin instead of his apartment. And *the care-trip* — Sarah ordering for her mother from her mother's account on a Friday afternoon, with the boundaries that let her help without seeing what she shouldn't see.

**REID:** And why "lot" beats "list" or "cart" — restate it for the room.

**KEVEN:** A list is what Sarah is thinking about. A cart is what Sarah is buying. A lot is *the thing itself* — the household reality the list and the cart are both partial views of. The list is one question against the lot. The cart is one transaction against it. The pantry is what the lot turned into. The next meal plan is a question against what the lot left behind. *One noun. Whole lifecycle.* Sarah's life doesn't end at checkout. The lot doesn't either.

**REID:** And the architectural discipline that backs this — every part of the system has to treat the lot as the unit of work. Every agent recommendation comes back as a lot operation. Every screen shows the lot Sarah is inside. Every audit row records what happened to the lot. The moment one corner of the system reverts to thinking *list*, the noun leaks and the household feel collapses. That discipline is the difference between a real abstraction and marketing language. Episode three defends it.

**KEVEN:** Said cleanly. The lot is the household's experience, named. It's what makes Sarah's Sunday-evening plan still useful to her Wednesday-morning self.

### The headline interaction — SCAN

**KEVEN:** Picture Sarah in a store, in the aisle, with the jar of gochujang in her hand. She doesn't know the brand. She doesn't know how to spell it. She knows her teenager wants it for a recipe and she knows there's a Korean character on the label. Most retail apps would have her type — and she'd guess at the spelling, and the search would miss, and she'd give up and put the jar back. CFMP lets her do what she already does with her phone for everything else in her life. *She points the camera at the jar.* Three seconds later the answer is on the screen — the right product, the price after her loyalty discount, whether it's safe for the allergens in her household.

**REID:** And the answer is — point the camera at it.

**KEVEN:** Point the camera at it. The home screen of the app is a camera viewport. There is no search box competing for her attention. The system has already decided — *the front door is the camera.* Search is still there, tucked into the chat composer for the moments she really does have a name in her head, but the default is scan. That's a design commitment.

**REID:** And I get to push. *This is just a barcode reader.* Every grocery app has had one since 2014. Yuka has it. Google Lens has it. Vivino has it. Why is the CFMP scan distinctive to Sarah's day?

**KEVEN:** Two reasons. First, the scan is the *front door*, not a feature buried four taps deep. Sarah doesn't have to decide *should I scan or should I search* before she's even started. The system has chosen for her. The cognitive load drops. The thirty-second cereal-aisle question becomes a three-second cereal-aisle answer.

**REID:** Acceptable. And the second?

**KEVEN:** The second matters more. When Sarah scans, the answer that comes back is *a fact, not a story.* The right product, the real price, the real dietary flags. The system doesn't make something up about a brand that isn't on the shelf. The system reads from the same governed product catalog the operator's tools see, the same catalog the buying team signs off on. The scan hands the agent a known entity, and every downstream recommendation — the coupon, the substitution, the meal-plan fit, the dietary block — composes on top of that known entity.

**REID:** And the property that makes the answer reliable.

**KEVEN:** Every catalog look-up runs through a governed boundary. The agent doesn't get to reach into raw inventory feeds and improvise. The agent gets to ask one well-defined question of a curated view and receive a structured answer. (The architecture has a name for that discipline — the MCP boundary. Episode two unpacks it.) And every call lands on the audit trail, so when Sarah comes back Tuesday and notices a price changed, the record of what she saw Sunday is still there, exactly as she saw it.

**REID:** So scan-first isn't a UX flourish. It's the architectural move that lets the system hand the customer a fact. I'll accept that framing. And the customer outcome is the part that matters — *the answer is right the first time, and right the same way every time.*

### What success looks like

**KEVEN:** Now the part where the design has to be honest with itself. Three numbers the team committed to — three numbers a year from now somebody is going to hold up and ask whether CFMP moved them. Each one is a Sarah-moment turned into a measurement.

**REID:** Read them. Don't paraphrase.

**KEVEN:** First number. *From "I need groceries" to a completed order — under five minutes for a returning customer.* Today, on competing tools, it's thirty to forty-five. That's Sarah's Sunday-morning friction translated into a measurement.

**REID:** And what makes it a behavior-change signal, not a vanity stat?

**KEVEN:** Because the friction is what causes Sarah to abandon. The forty-five-minute Sunday is the reason she doesn't finish her plan, the reason she ends up at the store on Tuesday, the reason the romaine wilts on Thursday. The five-minute target isn't speed for speed's sake. It's *completion.* If Sarah finishes on Sunday, the rest of the week's frictions collapse. The number is a proxy for the whole downstream cascade.

**REID:** Second number.

**KEVEN:** *Household food waste — under eight percent.* Industry average sits at twenty-four. Today, no competitor measures it at all. This is the wilted-romaine number.

**REID:** And this one I want to stress-test. Eight percent is a third of the industry average. The claim is that CFMP cuts household food waste by a factor of three. Defend it.

**KEVEN:** Three things working together. The household knows what's in the fridge and when it arrived, because the lot tracks it. Each item carries an expected shelf life and the system knows when it's at risk. And when something is at risk, the agent re-composes tomorrow's meal to use it. None of the three on its own moves the needle. All three together is the bet. The bet is that *Sarah not knowing what's about to expire* is the primary cause of waste, and closing that information gap closes most of the waste.

**REID:** I'll accept the bet is reasonable. I'll also press — if CFMP cannot measure household waste at the item level, the eight-percent target is unfalsifiable, and unfalsifiable is marketing, not measurement. The team has to commit to the instrumentation, not just the claim.

**KEVEN:** Agreed. The honest version is — consumption events, throw-out events, shelf-life timing, captured at the lot level. That's an engineering commitment, not a slogan.

**REID:** Third number.

**KEVEN:** *Twelve-week retention — at least thirty-five percent of installers still using the app daily-over-monthly three months in.* Category leaders sit at twelve to eighteen.

**REID:** And the customer behavior change behind the number?

**KEVEN:** This is the one that measures whether Sarah actually comes back. Time-to-order measures one moment. Waste measures a household outcome. The twelve-week number measures whether, three months after install, the app is still part of Sarah's life. Thirty-five percent is roughly double the category average. The bet is that the lot — the persistent thing Sarah's household is living inside — is what creates the return reason. Every other grocery app's retention falls off because each session is independent. The lot makes Sarah's Wednesday a continuation of her Sunday, not a fresh start.

**REID:** And if the lot doesn't, the retention number doesn't move.

**KEVEN:** Correct.

**REID:** Three numbers. None of them is vanity. Each one tracks a specific design hypothesis. If any one misses, a piece of the design is wrong — and the team will know which piece. That's what a measurement set is for. I'll accept it.

### The audit chain — why we mention it in episode one

**KEVEN:** Now I'm going to do something that might surprise the listener. This is a customer-experience podcast. Episode one is about Sarah. And I'm about to mention, for the third time, an audit chain — the kind of thing most product podcasts would put in episode seven, if they put it in at all. Episode two unpacks it in full. Why does it belong here, in the persona episode?

**REID:** Because it's the trust substrate. And the trust substrate is the design, not an afterthought.

**KEVEN:** That's exactly it. Walk Sarah's week again, and notice what every moment quietly depends on. The wilted romaine — Wednesday morning, the agent told her the romaine would be best used by tonight. Sarah has to *trust* the recommendation is honest, that the system isn't quietly nudging her to buy more produce. Marcus's cabin pre-stock — Marcus is letting the system order groceries to an address that isn't his home, paid for by friends he's splitting with. Marcus has to *trust* the splits are right and the deliveries are real. Sarah's Friday at her mother's house — Sarah is acting on behalf of her mother. Her mother has to *trust* that Sarah cannot see what she isn't entitled to see. Every one of those trust claims is backed, behind the scenes, by a record. Every action lands as a row on a chain. Every cross-identity action is recorded with both identities and the basis of the delegation.

**REID:** And the customer never sees a row. The customer just experiences the trust. The substrate is invisible — but it's the only reason the trust is real.

**KEVEN:** Episode two takes it apart. How every action becomes a record. How a regulator can re-show a six-month-old recommendation in three minutes. How a caregiver can act inside the system her father uses without his pharmacy data crossing the boundary. (Architecturally — a hash-chained ledger, trace identifiers carried across the agent fleet, the deployment topology you can walk on the live `/architecture` page.) But the reason it belongs in *this* episode is simpler than the architecture. The customer-experience claims we just walked are *not credible without it.* Sarah's Friday is a beautiful design moment. It's only a *safe* design moment because the substrate exists. If the substrate is bolted on later, Friday cannot ship.

**REID:** The customer experience is the surface. The audit chain is the foundation. Build the foundation late and the surface cracks. Build it on day one and the household trusts it without ever knowing why.

**KEVEN:** That's the bridge to episode two. We named the surface today. We unpack the foundation next.

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

**REID:** One disagreement, and I want to put it on tape in the form Sarah would put it. *Is this just a grocery app with new vocabulary?* Because Sarah doesn't care what we call the architecture. Sarah cares whether her Sunday gets shorter, her Wednesday gets calmer, her Thursday wastes less food. Every capability we walked today — auto-replenish, the cabin lot, the loyalty layer, the scan-first home, the meal plan — exists, individually, on something Sarah has already installed and probably abandoned. So what is CFMP actually doing that the eight apps on her phone don't?

**KEVEN:** Four things no shipped product is doing for Sarah today.

**KEVEN:** First — the lot that composes across retailers. No single retailer app lets Sarah build a meal plan that pulls produce from one source, the gochujang from a second, and her mother's diabetic snacks from a third — all in one lot, with one checkout intent, because Sarah's job is *the meal*, not the retailer. The retailers don't want to enable that; the moment they do, they cede the customer relationship to whichever layer is composing above them.

**REID:** Which is exactly why this only works as a *pack* — an independent layer that treats retailers as sources, not destinations. The retailers won't ship it because it's not in their interest. The customer needs it because her life isn't shaped to one retailer's catalog.

**KEVEN:** Second — Sarah-acting-for-her-mother, safely. Sarah can reorder her mother's diabetic snacks. Sarah cannot see her mother's prescription refills. The boundary is enforced where the agent lives, not where Sarah is asked to be careful. The household record captures both identities — Sarah-acting-as, her mother-the-account-holder — and the boundary records who saw what. No retailer app ships this. They don't have the substrate to ship it.

**REID:** And the substrate is what makes the Friday safe. Without it, Friday is a feature pitch nobody can defend in front of a privacy officer. With it, Friday is something Sarah can actually do.

**KEVEN:** Third — the meal plan composed from the pantry plus allergens plus budget plus the retailer's stock, all at once. No retailer has the pantry. No recipe app has the cart. No delivery app has the allergens. The composition only happens because the agent fleet sees all four at once — and the record of every composition is what makes the recommendation defensible months later when Sarah, or her caregiver, or her regulator, asks why.

**REID:** And the four-source composition only works because the agent calls across sources through a clean boundary. Episode two and three walk that boundary.

**KEVEN:** Fourth — Marcus's cabin lot. Not as a one-off cabin feature. As a *generalized pattern* — the household isn't a fixed address. The lot follows the household. The cabin is one instance. The beach house is another. Thanksgiving at the parents' house, the kid's college dorm, the grandmother's house for the holidays — same pattern. *One generalization. An infinite family of moments the customer doesn't have to re-explain to a new app every time.*

**REID:** A one-off ships a feature. A pattern ships every member of a family of features without re-engineering. I'll accept the distinction.

**KEVEN:** So I concede your premise — *the individual capabilities exist in the market* — and reject your conclusion. CFMP isn't a grocery app dressed up. It's an agentic *pack* — a substrate that the grocery surface happens to be the first application of. The customer feels the surface. The substrate is why the surface keeps working as the household's life changes.

**REID:** I'll accept that framing. With one caveat for the seller in the room. It only holds if the team follows through on the substrate commitment. If the audit chain becomes a log file, if the boundaries become a REST API, if the lot becomes a JSON blob — then we have built a grocery app with new vocabulary. The discipline is the difference between something Sarah relies on and something Sarah abandons in week eleven.

**KEVEN:** Agreed. The substrate is what makes it not a grocery app. The substrate is what every episode after this one defends — and what Sarah, indirectly, gets to rely on.

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
