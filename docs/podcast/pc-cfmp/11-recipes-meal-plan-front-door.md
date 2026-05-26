# Episode 11 · Recipes — the meal-plan front door

**Episode 11 · Recipes — the meal-plan front door** — the appended documentary deep-dive on the capture side of the meal-plan substrate. Episode Ten stood inside the household-composition substrate. Episode Eleven stands inside the *front door* of the meal-plan: the recipe library, where recipes come from, how they get into the customer's library, how cultural breadth lights up against a Flux PURPOSE event, and how the dietary-safety filter that Hassan defended at the SEARCH step in Episode Seven gets applied — contextually, gated by Flux — at recipe import. Seven sub-sections walk what the library is today versus what capture turns it into, the YouTube-to-recipe pipeline and the copyright-and-provenance line, friend-shared and family-heirloom recipes, restaurant meal repeat, holiday favorites coupling to Flux PURPOSE, fifteen cuisines of cultural breadth and the specialty-sourcing problem, and the allergen-aware import gate that lands the convergence Hassan and Vargas reached on tape.

**Builds on:** the show bible (00-show-bible-and-format) · Episodes 01–10 · `orchestrator/meal_planner.py` (the 10-step pipeline header — palette, perishable, budget, recipe-stitch, ledger row) · `CFMP-Mobile-Design-Document.md` §6 (the recipe and meal-plan touchpoints in the mobile UI) · Episode 7 substitution flow (dietary filter at SEARCH) · Episode 10 Flux PURPOSE event coupling
**Run time:** ≈ 42 minutes target
**Last updated:** 2026-05-25

---

## Cold Open

[Sound: a suburban Tuesday evening, the kind that always sounds like itself — a dishwasher in the next room running its quiet cycle, a forced-air furnace cycling on, a refrigerator's compressor humming through the open-plan kitchen, and somewhere upstairs a school-aged kid practicing the recorder for fifteen minutes that the practice chart says have to happen before screen time. The light is the gold-orange of low-angle May, slanting through the west-facing kitchen windows over the sink. The countertop is the granite Sarah's husband insisted on when they remodeled five years ago, the one she has spent five years wiping down twice a day. A tablet leans against the cookbook rail, the screen still showing the meal-plan for the week the agent surfaced Sunday afternoon. The dog, who is now ten years old and slower than he was in the cabin two months ago, is asleep under the kitchen island.]

Sarah Chen is at the island with her own coffee. Her eleven-year-old daughter Lily walks in from the back hall, still in her after-school clothes, and leans against the counter the way Lily leans against everything — one elbow planted, one hip cocked, one shoulder rolled forward in the slouch the orthodontist has been politely mentioning. *Mom.* Sarah looks up. *Mia's mom made this thing on Friday at the sleepover. It was like* — Lily gestures vaguely — *short ribs in this sauce that's like sweet and spicy and there were little Korean radish chunks and the whole thing was so good. Can you make it?* Sarah does the smile she has been doing for eleven years. *What was it called?* Lily, fishing — *galbi-jjim. Mia's mom said galbi-jjim.* And then she's gone, recorder upstairs, dog ambling after her.

Sarah picks up the tablet. She types *galbi-jjim* into the search bar of her preferred cooking-video channel, gets twenty results, picks the one with the most views from a creator she has watched before. The video opens — a Korean-American chef in a sunlit kitchen, narrating in English, captioning in Hangul. Sarah taps the share-sheet button at the top of her CFMP app and pastes the video URL into the *capture this for me* affordance. The progress indicator does its thing for forty seconds. The app surfaces a draft recipe. *Galbi-jjim — braised short ribs, Korean — five servings — three hours total time — five active.* Below the recipe: an ingredient list with one chip flagged amber. *Gochujang — specialty — found at two of your three saved providers. Korean radish — specialty — found at one provider.* Below that: a second amber chip. *Contains soy. No conflicts with current household allergen profile.* Below that, a soft gray banner. *Mia is peanut-allergic. This recipe is peanut-free; no flag.* Sarah taps *save to library.* The recipe tags itself *Korean*, *family-friend-shared*, *Mia's-mom*, and *braised.* The provenance row records the video URL, the channel name, the capture timestamp, and the agent that did the extraction. Two months later, when Sarah's mother-in-law — the Flux PURPOSE event from Episode Ten that activated on a Tuesday in late July — comes to stay for a week, the meal-plan engine pulls the library's Korean tag and surfaces *galbi-jjim* as a Wednesday-night candidate, with a one-tap shopping-list expansion that routes the gochujang and the Korean radish to the right provider.

[Sound: a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start with that tap. Sarah pastes a YouTube URL and forty seconds later the recipe is in her household library, provenance-stamped, allergen-checked, specialty-sourced. That's the front door we have not opened yet. The engine — `meal_planner.py`, the ten-step pipeline — is real. The recipe library is a real table. What is *not* real, today, is the capture side. Episode Eleven is about closing the gap between the engine and the front door.

**REID:** And the framing. Episode Ten stood inside the household-composition substrate. Episode Eleven stands inside the *meal-plan front door.* Which is the side the design has barely opened. We've shipped lots; we've shipped composition; we have not shipped capture. This is the side that turns CFMP from a grocery app into a household library — the side where the Korean grandmother's kimchi recipe lives, where the southern aunt's cornbread lives, where the Polish neighbor's pierogi lives. The episode walks seven sub-sections: the library today versus tomorrow, YouTube to recipe, friend-shared and family heirloom, restaurant meal repeat, holiday favorites and the Flux PURPOSE coupling, the fifteen cuisines of cultural breadth, and the allergen-aware import gate.

**KEVEN:** Welcome back to the CFMP Podcast. Episode Eleven. *Recipes — the meal-plan front door.* Appended episode. A reading. A disagreement — Hassan and Vargas converging on contextual filtering. Three carry-forwards.

**REID:** Let's go.

---

> **Episode framing admission:** this episode is the **Recipe Capture v2 vision**. Today the recipe library is seeded (`recipe_library` table is populated, the catalog_specialist's `recipe_for_items` works, the Meal-Plan pipeline stitches recipes into the 7-day plan). The **capture flows** described below — YouTube extraction, friend-shared imports, family heirloom recipes, restaurant meal repeats, holiday-favorites coupling to Flux PURPOSE events, cuisine-breadth across fifteen cultures — are the **front-door design**, not built today. As of 2026-05-25 the engine works; the front door does not. The CFMP Mobile Roadmap (see `CFMP-Mobile-Roadmap.md`'s parity backlog) is where these land.

## What ships today vs. what's planned

> **Episode honesty calibration · 2026-05-25**
> This episode covers the recipe library, the Meal-Plan composition pipeline, the capture flows (YouTube, friend-shared, family heirloom, restaurant repeat, holiday-favorites), the Flux PURPOSE coupling, the fifteen-cuisine breadth surface, and the allergen-aware import gate. The podcast walks the architecture as designed. Phase 1 live, Phase 2 planned, and v2 vision are distinguished below so the listener (and the seller) walks in knowing the score. The CFMP Capabilities Map at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` is the authoritative live-state source.

**Phase 1 live (today):** Meal-Plan composition (10-step pipeline), `recipe_library` seeded, catalog_specialist `recipe_for_items`, cuisine-tagging in `Gold_VV_Catalog`, MERML 796-SKU catalog.

**Phase 1 partial / in-progress:** Meal Plan shopping-list UI (ITEM column blank, UNIT/LINE $0.00, recipe slug-to-title not resolved).

**Phase 2+ planned (not live today):** YouTube-to-recipe capture, friend-shared recipe import, family-heirloom recipes (Mom's dishes, generational tagging), restaurant meal repeat (AI reverse-engineer), holiday favorites plus Flux PURPOSE coupling, cuisine-breadth discovery surface (fifteen cultures), specialty-ingredient sourcing via providers, allergen-aware import gate.

**v2 vision (architectural commitment, not designed yet):** family heirloom plus voice narration; restaurant reverse-engineering as a discipline.

---

## The conversation

### The recipe library today vs. tomorrow

**KEVEN:** Start with what already exists. Open `orchestrator/meal_planner.py`. The header is the cleanest specification of what the engine does. Ten steps. *One — read the customer's taste palette from `customer_profile.preferences`. Two — read `perishable_inventory`; anything expiring this week gets boosted. Three — read `customer_events`; guest visits flip household_size for that day.* And right there in step three, the design names the Flux PURPOSE coupling — *guest visits flip household_size.* That is the line that Episode Ten walked from the household-composition side; Episode Eleven walks it from the meal-plan side. The same event; two surfaces.

**REID:** Steps four through ten.

**KEVEN:** *Four — read `customer_budget`; weekly cap drives an upper bound on cost. Five — read `auto_orders`; items already arriving this week count as on-hand. Six — select recipes from `recipe_library` and stitch them into a plan. Seven — aggregate a shopping list from missing required_skus. Eight — tag leftover-friendly dinners so the next day's lunch is the reheat. Nine — surface quick-meal slash on-the-go suggestions for lunches. Ten — emit a hash-chained LedgerRow via apex_integration on every write.* Ten steps. Real code. Real tables — `customer_budget`, `meal_plans`, `meal_plan_slots`, `meal_plan_shopping`, `recipe_library`. The engine is *there.*

**REID:** And step six is the one this episode is about. *Select recipes from `recipe_library`.* What's in the recipe library?

**KEVEN:** Today, the seeded set. A few dozen recipes the team wrote by hand to make the engine demonstrable. Pasta with marinara. Sheet-pan chicken thighs. Stir-fry with whatever protein is on hand. The seeded set is enough to demo the pipeline; it is not enough to be a *library.* A library is what a household builds over time — the recipes the customer has captured from a friend, from a YouTube channel, from a cooking-show clip, from a vacation memory, from grandmother's index card box, from the cooking-class the daughter took for her birthday and brought home as a folder of stained printouts. The library is where the household's *food identity* lives. The seeded set is the engine's training wheels.

**REID:** So the gap is on the capture side.

**KEVEN:** The gap is entirely on the capture side. The engine — the palette match, the perishable boost, the budget bound, the recipe stitch, the leftover tag, the LedgerRow — is real. What does not yet exist is the front door — the way a recipe gets *into* `recipe_library` in the first place. The naive answer is *you type it in.* That answer fails every single power-user moment. Sarah does not type the YouTube recipe; Sarah captures it. The eleven-year-old does not type the friend's recipe; the eleven-year-old shares the link. The grandmother does not type her kimchi recipe; the grandmother dictates it into the family-heirloom flow with a photo of the crock and the daughter's voice narrating the back-and-forth. The seven sub-sections that follow are the seven capture surfaces.

**REID:** And the architectural payoff of treating capture as its own discipline.

**KEVEN:** Two architectural payoffs. *One — every captured recipe carries provenance.* The video URL, the friend's contact, the grandmother's name, the restaurant on vacation. Provenance turns the library into a *kitchen library* — recipes have a history, a story, an audit trail of where they came from. That history is what makes the recipe feel like the household's recipe and not a stock library entry. *Two — every captured recipe carries a contextual filter readiness.* The allergen profile, the dietary categories, the cuisine tag, the specialty-ingredient flag, the cost estimate. The engine downstream consumes those tags without re-running classification; capture is where the classification happens, once, on import. *Capture is where the recipe earns its place in the engine.*

### YouTube → Recipe

**REID:** Walk the YouTube flow. The cold open did the customer side. Walk the architecture side.

**KEVEN:** The customer pastes a video URL into the *capture this for me* affordance on the meal-plan tab. The mobile client sends the URL to the orchestrator. The orchestrator dispatches a *recipe-capture specialist agent* — a child agent on the agent fleet from Episode Two. The capture agent runs three classifiers and one extractor.

The first classifier is *is this a recipe video?* Because YouTube URLs are not all cooking videos. A music video, a news clip, a how-to about plumbing — the agent has to reject those gracefully. The classifier reads the video metadata, the channel category, the thumbnail, and the first ten seconds of the transcript. If the confidence falls below the threshold, the agent surfaces *this does not look like a recipe video; want to add it as a generic note instead?*

The second classifier is *what cuisine is this?* The model reads the title, the description, the spoken language hints in the transcript, the visible ingredient overlays in the captioning. Korean, Italian, Mexican, Indian, Thai. The cuisine tag becomes a column in the recipe_library row and a tag on the recipe for downstream search.

The third classifier is *what dietary categories does this carry?* Vegetarian, vegan, gluten-free, dairy-free, peanut-allergen, soy-allergen, shellfish-allergen. The model reads the ingredient overlays plus the spoken ingredient list. Categories become tags; the allergen-aware filter in section seven consumes them.

The extractor is the heart of the flow. It reads the video transcript with timecodes, identifies the ingredient-list moment in the video — usually the first sixty to ninety seconds, sometimes a re-stated list near the end — extracts each ingredient with its quantity and unit, identifies the step-by-step instructions from the rest of the transcript with timecodes mapped to *step one through step N,* and infers servings and total time. The extractor is built on a Foundry-hosted vision-and-language model — `gpt-5-vision` for the overlay reading, `gpt-5-mini` for the transcript parsing. The same Foundry tenant Episode Two named; the same governance.

**REID:** And the provenance row.

**KEVEN:** The provenance row is the part that has to be right. Every captured recipe writes a `recipe_provenance` row with the source type — *youtube*, *friend-shared*, *family-heirloom*, *restaurant-reverse*, *holiday-favorite*, *manual-entry*, *cooking-class* — the source URL or contact, the channel or person name where applicable, the capture timestamp, the capture-agent identifier, the customer's tenant identifier, and the trace_id from the capture orchestration. The provenance row is permanent; it never gets deleted when the recipe gets edited; the editing pattern is *new revision, old revision preserved.* The audit chain holds.

**REID:** And here I press. The copyright question. Sarah captured a recipe from a YouTube creator who makes their living posting that recipe. The creator wrote the recipe. The creator filmed the recipe. The creator put the recipe on YouTube to drive traffic to their channel and their cookbook and their sponsorships. We just had an LLM read the transcript and put the recipe in Sarah's library. *Did we just steal the recipe?*

**KEVEN:** Defended. The legal frame on recipes is that *the ingredient list and the procedural steps are factual.* United States copyright law explicitly excludes from protection the *listing of ingredients or contents* and the *idea, procedure, process, system, method of operation.* What is protectable is the *literary expression* — the headnote, the chef's commentary, the story around the recipe, the specific photographs and the specific phrasing of the prose. The capture extractor produces a *structured form* — ingredients with quantities, steps as a sequence — and explicitly does not extract the headnote prose. The structured form is the factual core; the expressive form is the YouTube video, which stays where it lives.

The second defense is provenance. The captured recipe in Sarah's library shows *source: YouTube — chef name — video title — link.* Click the link, you go to the original video. The capture is not republication; the capture is *a structured index into a video Sarah watched, kept private to Sarah's household tenant.* The recipe is never republished beyond Sarah's household — not shared to other CFMP customers without Sarah's explicit action, not used as training data for any model, not exfiltrated to any cloud aggregation. The capture is a *household-private structured note* with a permanent link back to the creator's work.

The third defense is the option to *link instead of capture.* The customer's preferences include a per-source policy — *capture structured form,* *link-only,* or *capture with one-click attribution post to the creator.* The default is capture-with-link, but the customer can flip the preference; some customers prefer their library to be a curated set of links so the creator gets the view-through. The architecture respects the customer's stance.

**REID:** And the Microsoft surface.

**KEVEN:** The capture agent runs on Azure AI Foundry. The Foundry tenant the rest of the fleet runs on. The recipe-capture specialist is a `gpt-5-mini` agent with two tool calls — *fetch-transcript* against the YouTube data API, and *extract-recipe-structure* against a Foundry-hosted model deployment. The extractor's output is JSON, validated against the recipe schema, written to the `recipe_library` and `recipe_provenance` tables in Postgres. The same Postgres instance Episode Two named. The same audit chain — every capture writes a hash-chained LedgerRow with the capture's trace_id, identity stamp, and effect bundle. The live architecture page at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` shows the orchestrator Container App where this runs; the recipe-capture specialist is one more agent inside the fleet that diagram already carries.

### Friend-shared + family heirloom

**REID:** The two most emotional capture surfaces. Walk friend-shared first.

**KEVEN:** Friend-shared is the simplest capture path technically and the highest-value path emotionally. Sarah's friend Maria texts her a recipe. The text might be a link to a website, a YouTube URL, a forwarded message, or — most commonly — a screenshot of the recipe from Maria's grandmother's cookbook. The customer hits the share-sheet from the messaging app, picks CFMP, and the recipe-capture agent runs the appropriate extractor by source type. The link goes through the URL flow we just walked. The screenshot goes through an OCR-plus-vision flow — extract the recipe from the image, structure it. The provenance row records *source: friend-shared — Maria — capture from screenshot — captured Tuesday.*

The architectural distinction is the *attribution copy* the library renders. Maria's recipe in Sarah's library shows *from Maria,* not *anonymous import.* The library is a *kitchen library,* and a kitchen library knows where each recipe came from. When Sarah scrolls her library and sees *galbi-jjim — from Mia's mom* and *roast chicken — from Maria* and *pierogi — from Aunt Helen's church cookbook,* the library is the household's social-and-food history. That is what makes the library a library and not a list.

**REID:** And the family-heirloom case.

**KEVEN:** Family-heirloom is the highest-affinity capture path in the entire episode. Grandmother's recipes. The kimchi the Korean grandmother makes every fall when the napa cabbage is in season. The cornbread the southern aunt makes for Sunday dinner. The pierogi the Polish neighbor brings to every block party. The bagels the New York grandfather used to make on Sunday mornings before his hands stopped letting him knead. *These recipes do not exist in a database anywhere on the internet.* They live in an index card box, in a stained printout, in the grandmother's head, in the rhythm of three generations watching her do it.

The family-heirloom flow is the most respectful flow in the capture toolkit. The customer opens *capture family heirloom* on the meal-plan tab. The flow walks the customer through five fields. *Recipe name.* The name the family calls it — *Grandma Park's kimchi,* not *traditional fermented napa cabbage.* *Photo of the dish.* A photo the customer takes — the dish on the family table, the dish in the cooking process, the dish in the grandmother's hands. *Voice narration — optional but high-value.* The customer hits record; the grandmother walks through the recipe; the audio is transcribed by Azure Speech; the agent extracts the structured form from the transcript and presents both — the structured form for the engine, the audio for the library. The library plays the audio back when Sarah opens the recipe; the audio is the grandmother's voice telling the recipe; the recipe will outlive the grandmother and the library knows it. *Ingredients and steps.* Either typed or carried from the transcription. *Family tags.* The flow surfaces *family, generational, heirloom,* and lets the customer add custom tags — *Sunday-dinner, fall-only, Mom's, Dad's-side.*

**REID:** And the architectural respect.

**KEVEN:** Two pieces of architectural respect. *One — the family-heirloom recipes are tagged for the engine to weight them higher in surfacing.* When the meal-plan engine ties between two candidate recipes, the one tagged *family* wins. The household's own recipes outrank the seeded set; the seeded set is the fallback. *Two — the family-heirloom recipes are the most rigorously household-private subset of the library.* Even within the capture-with-link default, family-heirloom recipes default to *no-link-out,* because there is no source URL — the source is the household. The recipe does not leave the tenant. The recipe does not appear in any aggregated view, any analytics surface, any external feed. The Korean grandmother's kimchi is the household's kimchi; the cloud is what cloud is for; the household is what household is for. Episode Twelve will name this line explicitly; Episode Eleven plants the substrate it rests on.

**REID:** This is the moment CFMP becomes more than a grocery app.

**KEVEN:** This is the moment CFMP becomes more than a grocery app. The grocery app turns the chore into a managed system; the kitchen library turns the household's *food identity* into a managed library. The recipe captures, the cuisine breadth, the family heirloom flow, the voice narration — these are the surfaces that earn the household over years, not weeks. A grocery app is a Tuesday convenience. A kitchen library is a Sunday-dinner-with-grandma. The sustained engagement looks different.

### Restaurant meal repeat

**REID:** The reverse-engineering case. The customer ate something on vacation. They want it at home. Walk the flow and the AI-plagiarism question.

**KEVEN:** The flow opens from the *capture from memory* affordance. The customer narrates — voice or text — *recreate that lamb tagine we had at the place in Marrakech, the one with the saffron and the apricots and the almonds on top, I think there was preserved lemon, the lamb was so tender it fell apart with a spoon.* The capture agent parses the narration into a dish-class hypothesis — *Moroccan lamb tagine with preserved lemon, apricots, almonds, slow-braised.* It surfaces three to five candidate interpretations of the dish-class. *Sweet tagine — the apricots are dominant.* *Savory tagine — the preserved lemon is dominant.* *Northern Moroccan style — almonds and apricot prominent, ginger-cinnamon balance.* *Berber style — long slow braise, less spice.* The customer picks the interpretation closest to their memory. The agent generates a draft recipe in the cuisine's idiom, with ingredient quantities sized to the customer's household and the candidate restaurant style.

The customer iterates. *Less cinnamon.* *More preserved lemon.* *The lamb was definitely lamb shoulder, not leg.* *They served it with that flatbread, the one shaped like a half-moon — what's that called?* The agent refines, surfaces the flatbread candidate — *m'semen, the Moroccan flaky pan flatbread* — and offers to add it as a sidecar recipe. The customer accepts. The two recipes save together, both tagged *Moroccan, restaurant-recreation, vacation-memory*, with provenance *source: restaurant-reverse — customer-described — Marrakech vacation March 2026.*

**REID:** And here I press. The AI-plagiarism question. The restaurant has a recipe. The restaurant's chef has a specific approach. We just had an LLM produce *the restaurant's lamb tagine* from a memory. *Did the chef just get plagiarized?*

**KEVEN:** Defended hard. The agent is not extracting *that restaurant's specific recipe.* The agent has no access to the restaurant's kitchen, the chef's notes, the proprietary technique. What the agent is doing is *teaching the customer the dish-class.* The output is not *Restaurant X's lamb tagine;* the output is *Moroccan lamb tagine, in the style the customer described, sized to the customer's household, with the customer's specified ingredients.* It is the same thing as asking a cooking school *I had this dish on vacation, teach me how to make one like it.* The cooking school does not call the restaurant for the recipe; the cooking school teaches the *genre.* The agent is the cooking school.

The second defense is in the provenance. The captured recipe in Sarah's library shows *source: restaurant-recreation — interpretation of customer's memory — not a recipe owned by any restaurant.* The recipe never claims to be the restaurant's recipe. The provenance line acknowledges the recipe is an *interpretation* — explicit, on the record, in the customer-facing UI. The customer knows what they are saving. If they later visit the restaurant again and decide their interpretation was off, they can iterate the recipe further; the agent revisits the dish-class and refines.

The third defense is the *no restaurant data ingested* posture. The agent never queries a restaurant's menu API for proprietary recipes. The agent never scrapes the chef's social media for technique notes. The agent never reads the chef's cookbook past the structured ingredient lists that are factual under copyright law. The information used is the cuisine-genre knowledge in the model, plus the customer's own memory and iteration. *The recipe is the customer's interpretation, in the cuisine's idiom, refined with the customer's iteration.*

**REID:** And the case where the customer wants the chef's actual recipe.

**KEVEN:** If the chef has published the recipe — a cookbook, a website, a YouTube channel — the customer captures it from that published source through the appropriate flow. The YouTube flow if it's on YouTube; the link-capture flow if it's on a recipe website; the manual-entry flow if it's from a cookbook the customer owns. Each of those carries the source as provenance and respects the published copyright posture. The restaurant-reverse flow exists for the cases where the chef hasn't published — the dish exists only in the restaurant's kitchen — and the customer wants to make *something like it* at home. The two flows are not in tension; they cover different customer moments.

### Holiday favorites + Flux PURPOSE coupling

**REID:** The coupling to Episode Ten. The PURPOSE event hands a context flag to the meal-plan; the recipe library lights up the cuisine-breadth and the family-heirloom recipes. Walk it.

**KEVEN:** Holiday favorites are date-keyed recipes. The recipe carries a *seasonal_window* tag — Thanksgiving for the third week of November, Christmas for the last week of December, Easter for the spring Sunday that calendars know, Cinco de Mayo for May fifth, Hanukkah for the Jewish calendar dates, Lunar New Year for the lunisolar dates the calendar widget resolves, Diwali for the Hindu calendar dates, Ramadan for the lunar Islamic month, the Fourth of July, Juneteenth. Each holiday is a tag on a recipe; each tag carries a date-key that the meal-plan engine resolves against the calendar.

The household profile carries a *celebrated holidays* list. Sarah's household celebrates Thanksgiving, Christmas, Easter, and Lunar New Year — the Lunar New Year because Sarah's mother-in-law is Chinese and the household has adopted the celebration. The household does not celebrate Hanukkah; the household has no Jewish members; the meal-plan engine does not surface Hanukkah recipes in December unless explicitly added. The holiday tagging is *participatory,* not assumed.

When a celebrated holiday's date approaches — the engine looks ahead two weeks — the meal-plan surfaces the household's holiday-tagged recipes for that holiday as candidates. The Thanksgiving roast turkey from grandmother's index card. The Christmas cookie recipe from Lily's preschool. The Easter ham from Sarah's husband's family. The Lunar New Year dumplings from the mother-in-law's family. *Date-keyed recipes resurface in the right season.* The seller carries this as a real engagement moment — the meal-plan turning into the holiday-planning calendar with one tap.

**REID:** And the Flux PURPOSE coupling.

**KEVEN:** The Flux PURPOSE coupling is where Episode Eleven and Episode Ten interlock. Sarah's mother-in-law visits Tuesday — the PURPOSE event from Episode Ten the cold open of *that* episode could have walked. The Flux event transitions to `active` on Tuesday morning. The Cue Bus emits an event. The meal-plan engine subscribes. The engine reads the PURPOSE event's affected_member_numbers, finds the mother-in-law's transient guest profile, reads her cuisine preference — *Korean* — and her dietary profile — *Type Two diabetes, low-glycemic preferred.* The engine flips three filters at once. *Cuisine-breadth surface: Korean recipes light up in the candidate set.* *Family-heirloom filter: Korean-tagged family-heirloom recipes from the library — galbi-jjim from the cold open of *this* episode, the kimchi the mother-in-law made last fall on her last visit and Sarah captured to the family-heirloom flow — get the affinity boost.* *Holiday-favorites filter: if Lunar New Year is within the visit window, the dumpling recipes and the long-life-noodle recipe surface for the appropriate day.*

The result is a meal-plan for the week that is *Korean-leaning, family-heirloom-weighted, diabetes-friendly,* with the mother-in-law's favorite dishes appearing on the days the customer would expect them. *This is where Lane Nine — the Recipe lane — and Lane Two/Seven — the Flux lane — compose into a real customer moment.* The right recipe at the right time for the right guest. The Flux event sets the context; the recipe library is what the context lights up against; the meal-plan is the rendered result.

**REID:** And the architectural elegance.

**KEVEN:** The architectural elegance is that *neither lane has to know about the other to compose.* Lane Two/Seven — Flux — emits lifecycle events on the Cue Bus. Lane Nine — Recipes — emits no events; it just provides a queryable library with tags. The composition happens at the meal-plan engine, which subscribes to the Cue Bus events and queries the recipe library by tag. *Two lanes; one bus; one engine; the customer experience.* The substrate Episode Ten built carries Episode Eleven without modification.

### Cuisine breadth — the fifteen cultures + specialty sourcing

**REID:** Walk the cultures. Fifteen of them. Why fifteen, and what does each one demand.

**KEVEN:** Fifteen because fifteen covers the cultural breadth of the customer base the design has researched. Japanese, Chinese, Mexican, South American — Peruvian, Brazilian, Argentinian — Korean, Italian, English, German, Spanish, Indian, Thai, Vietnamese, Mediterranean — Greek, Lebanese, Turkish bands — Seafood and pescatarian as a cross-cuisine band, and regional American — Southern, Cajun, New England, Southwestern, Pacific Northwest. The fifteen is not a hard limit; the substrate grows as customer demand surfaces new cuisines — Ethiopian, Filipino, Caribbean, Persian. Each cuisine carries a cuisine row in the `cuisine_catalog` table with the canonical name, the regional sub-styles, the typical ingredient categories, and the *specialty-ingredient* list.

The specialty-ingredient list is the operational hinge. Each cuisine has a small set of ingredients that are *cuisine-defining* and *not commonly stocked* at general-merchandise stores. Korean cooking needs *gochujang* — the fermented chili paste — and *gochugaru* — the Korean chili flake — and *doenjang* — the soybean paste. Mexican cooking needs *masa harina* — the nixtamalized corn flour — and *chiles in adobo* and *Mexican chocolate.* Mediterranean cooking needs *sumac* — the tangy red spice — and *za'atar* — the spice blend — and *good extra-virgin olive oil at a real price point.* Japanese cooking needs *miso* — multiple varieties — and *dashi ingredients* — kombu, bonito flakes — and *good rice vinegar.* Thai and Vietnamese cooking need *fish sauce* — a specific brand the customer has chosen, often varying widely in saltiness and funk between brands — and *Thai chiles* and *kaffir lime leaves.* Indian cooking needs *whole spices* in fresh quantity — cumin seeds, cardamom pods, cloves, cinnamon sticks, mustard seeds — and *asafoetida* and *ghee* and *toor dal* and *basmati rice at quality.* Each cuisine names its specialty list; each list goes into the `cuisine_catalog` row; the meal-plan engine and the fulfillment plug-in tier consume the list together.

**REID:** And the cross-coupling to Lane Four.

**KEVEN:** This is where Episode Eleven crosses into Episode Seven — the fulfillment plug-in tier. Each fulfillment provider — each retailer plug-in registered in the `FulfillmentProvider` ABC — declares its *capabilities* at registration time. Episode Seven walked the `handles_pharmacy` capability flag — the retailer plug-in declares whether it can fulfill prescription items. Episode Eleven adds the parallel flag: *`handles_ethnic_specialty: list[cuisine]`* — the retailer plug-in declares which cuisine specialty inventories it carries. Provider A — a national general-merchandise chain — declares *handles_ethnic_specialty: [italian, mexican]* because it stocks the Italian and Mexican specialty aisles. Provider B — a Korean-American grocer in the neighborhood — declares *handles_ethnic_specialty: [korean, japanese, chinese]* because it stocks all three East Asian specialty inventories with depth. Provider C — a Mediterranean specialty store — declares *handles_ethnic_specialty: [mediterranean, mediterranean-lebanese, mediterranean-turkish]* and is the one the customer routes to for the za'atar and the sumac and the good olive oil.

When the meal-plan engine stitches a Korean-leaning week, the shopping list is split by cuisine. The everyday items — the chicken, the onions, the garlic, the eggs, the rice — go to the customer's default provider. The Korean specialty items — the gochujang, the Korean radish, the gochugaru — query the `handles_ethnic_specialty` capability and route to the Korean-American grocer. The customer sees one consolidated meal-plan view; the architecture has two coordinated fulfillment lots underneath. *The grocery app stitches the cuisine across providers; the customer does not.*

**REID:** And the substrate test.

**KEVEN:** The substrate test is the same one Episode Seven set for substitution. *Does the system stitch the customer's intent across providers, or does it strand the customer at a single provider that can't meet the cuisine?* A naive system strands. A correct system stitches. The `handles_ethnic_specialty` capability is the bridge; the cuisine tag on the recipe is the trigger; the fulfillment quote aggregator is the engine that does the stitching. The customer who is cooking Korean this week gets the Korean specialty at the Korean grocer and the rest at their default; the customer who is cooking Mediterranean next week gets the Mediterranean specialty at the Mediterranean specialty store and the rest at their default. *The cultural breadth is where CFMP earns the household that doesn't cook the same thing every week.* The household that cooks Korean Monday, Italian Tuesday, Mexican Wednesday, Thai Thursday, regional-American Friday — that household needs the substrate to stitch across providers without making the customer think about it. The substrate stitches.

### Allergen-aware import gate

**REID:** Section seven. The convergence point. Hassan defended the dietary filter at SEARCH in Episode Seven; Vargas pushed back on the rendering side. Walk how that defense-in-depth pattern applies to the recipe-capture path.

**KEVEN:** The pattern is the same; the surface is different. Episode Seven walked the substitution flow — the customer searches for *peanut butter* in a peanut-allergic household; the dietary filter fires at the SEARCH step; the search results never contain peanut products; the rendering step has nothing to filter because nothing made it to the renderer. The architectural principle: filter *upstream,* not at the surface. The principle is sound; the implementation is by-search.

Episode Eleven asks the same question of the recipe-capture path. Sarah captures a YouTube recipe — a Thai pad thai with peanuts. The household allergen profile says Lily is peanut-allergic. *Where does the filter fire?* The naive answer is *at the meal-plan render — when the engine surfaces pad thai for Wednesday dinner, it warns the customer.* That answer fails the same way Episode Seven said it fails — the recipe is already in the library, the engine has to remember the allergen every time it considers the recipe, the warning is at the latest possible moment. The Hassan position is *fire the filter at import.* The recipe-capture agent runs the allergen extractor as part of the import flow; if the recipe contains peanut and the household profile says peanut-allergic, the import flow surfaces a contextual flag — *this recipe contains peanut; your household profile flags peanut allergy; do you want to save it anyway, restrict it, or substitute the peanut?*

**REID:** And here is where the disagreement from Episode Seven extends. Vargas's position. Walk it.

**KEVEN:** Vargas pushed back on the global block in Episode Seven and pushes back again here. The household allergen profile is *not symmetric.* Lily is peanut-allergic; Sarah and her husband are not. Sarah likes pad thai. Sarah eats pad thai when Lily is at a friend's house for the night, or when the family is at a restaurant where Sarah orders the peanut version and Lily orders the peanut-free version, or when Sarah is at her parents' house for the weekend and Lily is with her husband. *Sarah's own library should respect Sarah's own choices.* A blanket block on every peanut recipe at import is, in Vargas's framing, *too aggressive — the customer's own library should not be policed by the system to a level the customer didn't consent to.*

**REID:** And the convergence.

**KEVEN:** The convergence is the same one Episode Seven reached, applied to the recipe-capture surface. *The filter is contextual, gated by Flux.* Specifically: the allergen filter at import fires at full strength when a Flux PURPOSE event in the active window flags a sensitive guest is present. Lily's friend Mia is over for the week — a Flux PURPOSE event with `affected_member_numbers` carrying Mia's transient guest profile, which carries Mia's peanut allergy as a guest-declared dietary flag. While that Flux event is `active`, the recipe-capture flow refuses to import a peanut recipe without an explicit *I understand a sensitive guest is present and I am saving this recipe for the post-visit window* confirmation. Outside the Flux window — Mia is not visiting, the only peanut-sensitive member is Lily and Lily is at her grandparents' for the weekend — the import flow is less aggressive. The recipe imports with the contextual flag; the engine remembers the flag for surfacing-time; the engine surfaces the recipe only on days Lily is not in the household's active eaters set per the Flux composition fold.

**REID:** Hassan accepts the contextuality.

**KEVEN:** Hassan accepts the contextuality *because Flux is the substrate that knows.* The reason the global block failed Hassan's defense-in-depth in Episode Seven was the rendering filter not knowing the search; the reason the search filter worked was the search step knowing what to filter against. Episode Eleven's recipe-capture filter has access to *more substrate than the search filter had* — it has the Flux composition fold. The filter can know *who is in the household this week, who is a sensitive guest, who is a non-eater of this allergen.* The filter is more informed; the filter can be more contextual without losing the safety property. Hassan signs off on the contextual version because the substrate carries the information needed to make the contextuality defensible.

**REID:** And Vargas accepts the filter.

**KEVEN:** Vargas accepts the filter *because Flux gates it sensibly.* The reason Vargas pushed back on the global block was the customer-experience harm of the system policing the customer's own choices when the policing was not warranted. The Flux-gated filter only enforces when the substrate has identified a context that warrants the enforcement — a sensitive guest is present, a child is in the active eaters set, an event has flagged a dietary constraint for the window. Outside those contexts, the customer's own library respects the customer's own choices. *The architecture is the answer.* The disagreement converged on the architecture, not on either party giving up the position.

**REID:** And the implementation.

**KEVEN:** The implementation reuses the same filter code from the Lane Four substitution flow. The `dietary_filter` module — same module, same allergen taxonomy, same per-household profile fold — is invoked at the recipe-capture step against the Flux composition fold for the *active window plus the next four weeks.* If any active or near-future Flux PURPOSE event flags a sensitive guest, the filter is strict. Otherwise, the filter is contextual — the import succeeds with a tag, the engine surfaces the recipe only on days the sensitive member is in the active eaters set or not. *Same filter; different invocation policy; gated by Flux.* The substrate from Episode Ten is the gate; the filter from Episode Seven is the engine; Episode Eleven is the surface where the two compose.

---

### A reading I want to do

**REID:** Two candidates. Samin Nosrat's *Salt Fat Acid Heat* — the cookbook-shaped argument that all of cooking, across all cultures, is variations on four principles, salt and fat and acid and heat, applied with cultural specificity. Or J. Kenji López-Alt's *The Food Lab* — the recipe-reverse-engineering argument that recipes are not lists of ingredients but *teachable structures* with mechanisms you can name and tune. I lean Nosrat for this episode because cuisine-breadth is the heart of the section six argument, and Nosrat's frame — *all cuisines share the four principles; the cultural variation is in which fats, which acids, which heats* — is the cleanest articulation of why a fifteen-cuisine library is not fifteen unrelated things but fifteen variations on one teachable structure. Read Nosrat and the cuisine catalog stops looking like a clever feature; it looks like the right way to organize cooking knowledge across cultures.

The pairing with Kenji is worth doing for the restaurant-reverse flow in section four. Kenji's argument that a recipe is *a procedure with mechanisms* — the Maillard reaction is at this temperature, the emulsion holds at this fat-to-acid ratio, the gluten develops at this hydration — lands the architectural point that the restaurant-reverse agent is *teaching the customer the genre,* not extracting the chef's specific recipe. Kenji's frame gives the seller and the engineer the vocabulary to defend the AI-plagiarism question with conviction. The agent is doing what a good cooking-school instructor does — teaching the genre — not what a recipe-pirate does — copying the chef's specific work. Different.

**KEVEN:** And the pairing carries the carry-forward. *Recipes are not lists of ingredients; they are teachable structures.* The captured recipe in CFMP's library is the structured form, with provenance, with cuisine tag, with dietary tags, with the variation specifics. That is exactly the form the engine can reason over. The reading lands the architectural choice in the canonical food-writing literature; the architecture is not exotic; the architecture is the canonical form of cooking knowledge applied to a substrate.

---

### One disagreement

**REID:** The substrate from section seven. Hassan versus Vargas. Walk it clean.

**KEVEN:** Hassan's position. *Every captured recipe must run the allergen filter at search-equivalent — meaning at import. No exceptions. No override. The cost of a missed allergen is unbounded.* The argument is the same defense-in-depth he made in Episode Seven on the substitution side. The render-side filter is not enough; the search-side filter is the canonical place. Translated to recipe capture, the import-side filter is the canonical place. Anything weaker is a system that *can* miss an allergen — even with the best rendering filter downstream, the import step is the cheapest place to assert the property. *The recipe-capture flow either filters at import or it doesn't carry the safety property at all.*

**REID:** Vargas's position.

**KEVEN:** Vargas's position. *Too aggressive. The customer's own library should respect the customer's own choices. Sarah is not Lily; Sarah's own dietary profile is not peanut-allergic. When Sarah is cooking pad thai on a Friday night when Lily is at a sleepover, the system does not need to nag her about peanuts.* The argument is the customer-experience-harm argument, but more specifically — the harm of the system telling the customer what to put in her own library when the customer's own behavior says *I am the eater here, not the constrained member.* The system policing the recipe library to a level the customer didn't consent to is a brand harm of its own. Not unbounded — but real.

**REID:** And the convergence.

**KEVEN:** The convergence is the *contextual filter,* gated by Flux. The filter fires at full strength when a Flux PURPOSE event in the active or near-future window flags a sensitive guest present — Mia is over for the week, Sarah's mother-in-law is here for ten days with the diabetes constraint, the daughter's friend is staying through the weekend with the shellfish allergy. The filter fires at a *contextual* strength — *recipe imports with a tag, surfaces only on days the sensitive member is not in the active eaters set* — when no such Flux event is active. The customer's own library respects the customer's own choices in the steady state; the filter sharpens when the household composition flags a constraint that overrides the steady state. *The architecture is the answer.*

Hassan accepts the contextuality because Flux is the substrate that knows; the filter is more informed than the global block, not less. Vargas accepts the filter because Flux gates it sensibly; the customer's autonomy is preserved in the steady state. The two positions converged on a third — *the contextual, Flux-gated filter* — that is stronger than either's starting position and weaker than neither's bottom line. The disagreement converged on the substrate.

**REID:** And the principle generalizes.

**KEVEN:** The principle generalizes to every other tension between safety and autonomy in CFMP. *The substrate decides; the substrate is what knows the context.* The Flux composition fold is the substrate. The dietary-profile-by-member is the substrate. The audit chain is the substrate. The architecture's job is to make the substrate available to every surface that needs to make a contextual call; the surface's job is to call the substrate; the customer's job is to live in a system where the calls are right because the substrate is right. The disagreement is the architecture; the disagreement *is* the architecture.

---

### What to carry forward

The three durable takeaways.

1. **Recipes are CFMP's meal-plan front door.** The engine — `meal_planner.py`, the ten-step pipeline reading palette, perishable, budget, recipe-stitch, ledger row — already exists. What is the v2 work is the *capture* side — the YouTube flow, the friend-shared flow, the family-heirloom flow, the restaurant-reverse flow, the holiday-favorites flow. Capture is where the library becomes the household's library. The seller carries this — *the engine is real; the front door is the work; capture turns the seeded set into the kitchen library.*

2. **Cultural breadth is where the cookbook becomes a household library.** The fifteen cuisines — Japanese, Chinese, Mexican, South American, Korean, Italian, English, German, Spanish, Indian, Thai, Vietnamese, Mediterranean, Seafood, regional American — each carry a specialty-ingredient list. The fulfillment plug-in tier from Episode Seven adds the `handles_ethnic_specialty` capability flag; the meal-plan engine splits the shopping list by cuisine across providers; the customer gets the cuisine without thinking about the store. The seller carries this — *the cuisine breadth is the cookbook becoming the library; the operational answer is cuisine-by-cuisine specialty sourcing.*

3. **Privacy preview — captured recipes stay in the household tenant.** The Korean grandmother's kimchi recipe is not Microsoft's; the kimchi recipe is not the cloud's; the kimchi recipe is the family's. The provenance row, the audio narration, the photo of the dish, the family tags — none of it leaves the tenant. Episode Twelve walks this in full as the privacy story for CFMP. Episode Eleven plants the line that makes the privacy claim defensible at the substrate. The seller carries this — *capture is private by design; the kitchen library is the household's; the cloud is what cloud is for; the household is what household is for.*

---

## Further reading

- **Source docs**
  - `orchestrator/meal_planner.py` — the ten-step pipeline header that names the engine the front door feeds
  - `CFMP-Mobile-Design-Document.md` §6 — the recipe and meal-plan touchpoints in the mobile UI; the share-sheet capture affordance the cold open uses
  - `orchestrator/recipe_capture.py` — the recipe-capture specialist agent the YouTube flow dispatches (forthcoming in v2)
  - `db/05_recipe_provenance.sql` — the `recipe_library`, `recipe_provenance`, and `cuisine_catalog` schema (forthcoming in v2)
  - `CFMP-Mobile-Flux-Design.md` — the Flux PURPOSE event family that couples to the meal-plan engine (Episode Ten anchor)
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture`
- **Microsoft Learn**
  - Azure AI Foundry agents — `https://learn.microsoft.com/azure/ai-foundry/agents/` — the agent runtime the recipe-capture specialist deploys to
  - Azure AI Search — `https://learn.microsoft.com/azure/search/` — vector retrieval over the recipe library for cuisine-and-tag query
  - Azure AI Speech — `https://learn.microsoft.com/azure/ai-services/speech-service/` — the transcription service the family-heirloom voice-narration flow uses
  - Azure Container Apps — `https://learn.microsoft.com/azure/container-apps/` — the orchestrator host
- **Industry / research**
  - Samin Nosrat, *Salt Fat Acid Heat* — the four-principle framework for cooking across cultures; the architectural argument for why fifteen cuisines are not fifteen unrelated things
  - J. Kenji López-Alt, *The Food Lab* — recipes as teachable structures with named mechanisms; the vocabulary for the restaurant-reverse defense
  - The SchemaOrg `Recipe` schema — `https://schema.org/Recipe` — the canonical structured form the recipe-capture extractor targets; ingredients, steps, servings, total time, cuisine, nutrition

---

*Episode Eleven is the appended documentary deep-dive on the meal-plan front door. Episode Ten set the household-composition substrate the front door rests on. Episode Twelve walks the privacy substrate the captured library lives inside.*
