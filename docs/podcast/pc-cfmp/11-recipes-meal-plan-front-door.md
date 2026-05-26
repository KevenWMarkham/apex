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

### The cookbook that knows your household

**KEVEN:** Start with what already works. *The system that composes Sarah's week-ahead meal plan already exists.* It reads her taste preferences, the perishables in her pantry, the guests visiting, her household budget, the items already in the auto-replenish — and stitches a seven-day plan that uses what's expiring, fits the budget, fits the household, and respects everyone's dietary constraints. The engine is real today. *What's not real yet is the front door.*

**REID:** And the front door is what this episode opens.

**KEVEN:** The front door is the *recipe library* — the place the engine pulls from. Today, the library is a seeded set the team wrote by hand. Pasta with marinara. Sheet-pan chicken thighs. *That's a stock cookbook, not Sarah's cookbook.* Sarah's cookbook is the recipes she's captured from a friend, from a YouTube channel, from a cooking-show clip, from the Marrakech restaurant on vacation, from grandmother's index card box, from the cooking class her daughter took for her birthday and brought home as a folder of stained printouts. *The library is where the household's food identity lives.* The seeded set is training wheels.

**REID:** So the gap is on the capture side.

**KEVEN:** The gap is entirely on the capture side. The engine works. What's missing is *the way a recipe gets into Sarah's library in the first place.* The naive answer is *you type it in.* That fails every single moment Sarah lives. *Sarah doesn't type the YouTube recipe. She captures it.* The eleven-year-old doesn't type the friend's recipe; she shares the link. The grandmother doesn't type her kimchi recipe; the grandmother dictates it with the daughter narrating the back-and-forth on the phone microphone while the cabbage is fermenting on the counter.

**REID:** And the architectural payoff of treating capture as its own discipline.

**KEVEN:** Two payoffs. *Every captured recipe carries provenance.* The video URL, the friend's contact, the grandmother's name, the restaurant on vacation. *Provenance turns the library into a kitchen library — recipes have a history, a story, where they came from.* That's what makes the recipe feel like the household's, not a stock entry. *Every captured recipe carries the dietary information up front.* The allergen profile, the cuisine, the specialty-ingredient flag — classified once at import, consumed many times downstream. *Capture is where the recipe earns its place in the engine. The engine is the cookbook; the captures are how the cookbook becomes Sarah's cookbook.*

### YouTube to recipe

**REID:** Walk the YouTube flow from the cold open's customer moment.

**KEVEN:** Sarah pasted the video URL into the *capture this for me* button on the meal-plan tab. Forty seconds later she had the structured recipe in her library. *What happened in those forty seconds?* The system asked three questions of the video and ran one extraction.

The three questions. *Is this actually a recipe video?* — because YouTube URLs include music videos and news clips and how-to videos about plumbing; the system rejects non-recipes gracefully. *What cuisine is this?* — Korean, Italian, Mexican, Indian, Thai; the cuisine becomes a tag the engine searches by. *What dietary categories does this carry?* — vegetarian, peanut, soy, shellfish; the categories become tags the allergen filter reads from.

The extraction. The system reads the video's transcript with timecodes, finds the ingredient-list moment in the video — usually the first sixty seconds — extracts each ingredient with its quantity and unit, finds the step-by-step instructions, and infers servings and total time. *Forty seconds of work. A structured recipe at the end.*

**REID:** And the provenance row.

**KEVEN:** Every captured recipe carries provenance — *source: YouTube, channel name, video title, link, capture timestamp.* The provenance is permanent; *the editing pattern is new revision, old revision preserved.* The audit chain holds.

**REID:** And here I press. The copyright question. Sarah captured from a YouTube creator who makes their living posting that recipe. *Did we just steal the recipe?*

**KEVEN:** Defended. *US copyright law explicitly excludes the ingredient list and the procedural steps from protection.* The protectable part is the literary expression — the headnote, the chef's commentary, the photographs, the specific phrasing of the prose. *The extractor produces a structured form — ingredients with quantities, steps as a sequence — and explicitly does not extract the headnote prose.* The structured form is the factual core; the expressive form is the YouTube video, which stays where it lives. The captured recipe in Sarah's library shows *source: YouTube, chef name, video title, link.* Click the link, you go to the original video. *The capture is not republication; the capture is a structured index into a video Sarah watched, kept private to Sarah's household tenant.* Never republished. Never used as training data. Never exfiltrated.

The third defense — the option to *link-only.* Sarah can flip the preference and her library becomes a curated set of links so the creator gets the view-through. *The architecture respects her stance.*

**REID:** And the runtime.

**KEVEN:** The capture runs on the existing agent fleet's home in the existing region. The same audit chain Episode Two named records the capture with the same tracking thread shape. *Open the architecture page on a client call and the recipe-capture flow is one more specialist on the fleet that's already on the screen.*

### Friend-shared and family heirloom

**REID:** The two most emotional capture surfaces. Walk friend-shared first.

**KEVEN:** Sarah's friend Maria texts her a recipe. *Maybe it's a link to a website. Maybe it's a forwarded message. Most commonly, it's a screenshot of the recipe from Maria's grandmother's cookbook.* Sarah hits the share-sheet from her messaging app, picks CFMP. The link goes through the URL flow we just walked. The screenshot goes through a photo-and-text extraction. *The provenance row records — source: friend-shared, Maria, screenshot capture, Tuesday.*

The architectural distinction is what the library *renders.* Maria's recipe in Sarah's library shows *from Maria*, not *anonymous import.* *The library is a kitchen library, and a kitchen library knows where each recipe came from.* When Sarah scrolls — *galbi-jjim from Mia's mom, roast chicken from Maria, pierogi from Aunt Helen's church cookbook* — the library is the household's social-and-food history. *That's what makes the library a library and not a list.*

**REID:** And the family-heirloom case.

**KEVEN:** *The highest-affinity capture in the whole toolkit.* Grandmother's recipes. The kimchi the Korean grandmother makes every fall when the napa cabbage is in season. The cornbread the southern aunt makes for Sunday dinner. The pierogi the Polish neighbor brings to every block party. The bagels the New York grandfather used to make on Sunday mornings before his hands stopped letting him knead. *These recipes do not exist in a database anywhere on the internet.* They live in an index card box, in a stained printout, in the grandmother's head, in the rhythm of three generations watching her do it.

The flow is the most respectful flow in the capture toolkit. Five fields. *The name the family calls it* — *Grandma Park's kimchi*, not *traditional fermented napa cabbage.* *A photo of the dish.* *Voice narration — optional but high-value.* The customer hits record; the grandmother walks through the recipe; the audio is transcribed; the system extracts the structured form from the transcript and *the library plays the audio back when Sarah opens the recipe.* The audio is the grandmother's voice telling the recipe. *The recipe will outlive the grandmother and the library knows it.* *Ingredients and steps.* *Family tags.*

**REID:** And the architectural respect.

**KEVEN:** Two pieces. *Family-heirloom recipes are weighted higher when the engine considers candidates.* When the meal-plan ties between two recipes, the one tagged *family* wins. *The household's own recipes outrank the seeded set.* And *family-heirloom recipes are the most rigorously household-private subset of the library.* The recipe doesn't leave the tenant. The recipe doesn't appear in any aggregated view, any analytics surface, any external feed. *The Korean grandmother's kimchi is the household's kimchi.* The cloud is what cloud is for; the household is what household is for. Episode Twelve names this line explicitly; Episode Eleven plants the substrate it rests on.

**REID:** This is the moment CFMP becomes more than a grocery app.

**KEVEN:** *The grocery app turns the chore into a managed system; the kitchen library turns the household's food identity into a managed library.* A grocery app is a Tuesday convenience. *A kitchen library is a Sunday-dinner-with-grandma.* The sustained engagement looks different.

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

### Holiday favorites and the household-composition coupling

**REID:** The coupling to Episode Ten. The composition event hands a context flag to the meal-plan; the recipe library lights up the cuisine breadth and the family-heirloom recipes. Walk it.

**KEVEN:** Holiday favorites are date-keyed recipes. Each recipe in the library can carry a *holiday* tag — Thanksgiving, Christmas, Easter, Cinco de Mayo, Hanukkah, Lunar New Year, Diwali, Ramadan, the Fourth of July, Juneteenth. *Each tag has a date that the calendar resolves.*

The household profile carries a *celebrated holidays* list. Sarah's household celebrates Thanksgiving, Christmas, Easter, and Lunar New Year — *Lunar New Year because Sarah's mother-in-law is Chinese and the household has adopted the celebration.* The household doesn't celebrate Hanukkah; the household has no Jewish members; the meal-plan doesn't surface Hanukkah recipes in December unless Sarah adds them explicitly. *The holiday tagging is participatory, not assumed.*

When a celebrated holiday's date approaches, the meal-plan surfaces the household's holiday-tagged recipes as candidates. *The Thanksgiving roast turkey from grandmother's index card. The Christmas cookie recipe from Lily's preschool. The Easter ham from Sarah's husband's family. The Lunar New Year dumplings from the mother-in-law's family.* Date-keyed recipes resurface in the right season. *The meal-plan turns into the holiday-planning calendar with one tap.*

**REID:** And the composition coupling.

**KEVEN:** Sarah's mother-in-law visits Tuesday — the household-composition event from Episode Ten. The event transitions to *active.* The meal-plan engine reads who's in the household this week, finds the mother-in-law's transient profile, reads her cuisine preference — *Korean* — and her dietary preference — *Type Two diabetes, low-glycemic.* *Three filters flip at once.* Korean recipes light up in the candidate set. Korean-tagged family-heirloom recipes — *the galbi-jjim from the cold open, the kimchi the mother-in-law made last fall on her last visit and Sarah captured to the family-heirloom flow* — get the affinity boost. *If Lunar New Year falls inside the visit window, the dumplings and the long-life noodles surface for the appropriate day.*

The result is *a meal-plan for the week that's Korean-leaning, family-heirloom-weighted, diabetes-friendly* — with the mother-in-law's favorite dishes appearing on the days Sarah would expect them. *This is where the recipe library and the household-composition substrate compose into a real customer moment.* The right recipe at the right time for the right guest. The composition event sets the context; the library is what the context lights up against; the meal-plan is the rendered result.

**REID:** And the architectural elegance.

**KEVEN:** *Neither side has to know about the other to compose.* Composition emits lifecycle events on the cue bus. The library provides a queryable surface with tags. The composition happens at the meal-plan engine, which subscribes to the bus and queries the library by tag. *Two surfaces; one bus; one engine; one customer experience.* The substrate Episode Ten built carries Episode Eleven without modification.

### Cuisine breadth — the cookbook that knows your household

**REID:** Now the substrate that lets the cookbook know fifteen cultures, not five. Walk it.

**KEVEN:** Picture Sarah's household over a month. Korean Monday because Lily wants the galbi-jjim. Italian Tuesday. Mexican Wednesday. Thai Thursday. Regional-American Friday — *southern, Cajun, New England, Southwestern, Pacific Northwest* depending on what's in season. The customer who cooks one cuisine every week of her life is a customer most apps can serve. *The customer who cooks fifteen cuisines across a year is the customer most apps strand.* The cuisine-breadth substrate is where CFMP earns the household that doesn't cook the same thing every week.

**REID:** Fifteen cuisines. What does each one demand?

**KEVEN:** Each cuisine in the system carries a small list of *defining ingredients* — the items that make the cuisine itself, that aren't usually stocked at a general-merchandise store. Korean needs gochujang, gochugaru, doenjang. Mexican needs masa harina, chiles in adobo, Mexican chocolate. Mediterranean needs sumac, za'atar, good olive oil at a real price point. Japanese needs miso, dashi ingredients, good rice vinegar. Thai and Vietnamese need fish sauce — a specific brand the customer has chosen — Thai chiles, kaffir lime leaves. Indian needs whole spices in fresh quantity, asafoetida, ghee, basmati rice at quality. *The list isn't decorative. The list is the operational hinge that lets the cookbook know which retailer to send Sarah to for which item.*

**REID:** And the cross-coupling to the fulfillment tier.

**KEVEN:** This is where Episode Eleven crosses into Episode Seven. Each retailer in the system declares what it can handle at registration time. Episode Seven named the prescription flag. Episode Eleven adds the cuisine flag — *what cuisine specialties does this retailer carry?* A national general-merchandise chain carries Italian and Mexican specialty aisles. A Korean-American grocer in Sarah's neighborhood carries Korean, Japanese, Chinese with depth. A Mediterranean specialty store carries Mediterranean, Lebanese, Turkish — the one Sarah routes to for the za'atar and the sumac.

When the meal-plan stitches a Korean-leaning week for the mother-in-law's visit, *the shopping list splits by cuisine.* The everyday items — chicken, onions, garlic, eggs, rice — go to Sarah's default store. The Korean specialty items — gochujang, Korean radish, gochugaru — route to the Korean-American grocer. *Sarah sees one consolidated meal-plan view. The architecture has two coordinated fulfillment lots underneath. The system stitches the cuisine across retailers; Sarah doesn't.*

**REID:** And the substrate test.

**KEVEN:** *Does the system stitch the customer's intent across retailers, or does it strand the customer at a single retailer that can't meet the cuisine?* A naive system strands. A correct system stitches. *The cultural breadth is where CFMP earns the household that doesn't cook the same thing every week.* The household that cooks Korean Monday, Italian Tuesday, Mexican Wednesday, Thai Thursday, regional-American Friday — that household needs the substrate to stitch across retailers without making the customer think about it. *The substrate stitches. The cookbook knows.*

### Allergen-aware import — the contextual filter

**REID:** The convergence point. Episode Seven defended the dietary filter at the search step. Walk how the same defense-in-depth applies to recipe-capture.

**KEVEN:** Episode Seven walked the substitution flow — Sarah searches for peanut butter in a peanut-allergic household; the dietary filter fires at the search step; the search results never contain peanut products; the rendering step has nothing to filter because nothing made it to the renderer. *Filter upstream, not at the surface.*

Episode Eleven asks the same question at the recipe-capture path. *Sarah captures a YouTube recipe — a Thai pad thai with peanuts. Lily is peanut-allergic. Where does the filter fire?* The naive answer is *at the meal-plan render — when the engine surfaces pad thai for Wednesday dinner, it warns Sarah.* That answer fails the same way — the recipe is already in the library, the engine has to remember the allergen every time it considers the recipe, the warning is at the latest possible moment. *Fire the filter at import.* The recipe-capture flow runs the allergen extractor as part of the import; if the recipe contains peanut and the household profile flags peanut allergy, the import flow surfaces a contextual flag — *this recipe contains peanut; your household profile flags peanut allergy; do you want to save it anyway, restrict it, or substitute the peanut?*

**REID:** And here is where the disagreement from Episode Seven extends. The customer-autonomy push.

**KEVEN:** The household allergen profile is *not symmetric.* Lily is peanut-allergic; Sarah and her husband are not. Sarah likes pad thai. *Sarah eats pad thai when Lily is at a friend's house for the night, or when the family is at a restaurant where Lily orders the peanut-free version, or when Sarah is at her parents' for the weekend.* Sarah's own library should respect Sarah's own choices. A blanket block on every peanut recipe at import is *too aggressive — the customer's own library should not be policed by the system to a level the customer didn't consent to.*

**REID:** And the convergence.

**KEVEN:** *The filter is contextual, gated by household composition.* The allergen filter at import fires at full strength when an active household-composition event flags a sensitive guest is present. Lily's friend Mia is over for the week — Mia's guest profile carries her peanut allergy. While that event is *active*, the recipe-capture flow refuses to import a peanut recipe without an explicit *I understand a sensitive guest is present and I'm saving this for the post-visit window* confirmation. Outside the event window — Mia isn't visiting, the only peanut-sensitive member is Lily and Lily is at her grandparents' — the import flow is less aggressive. *The recipe imports with the contextual flag; the engine surfaces the recipe only on days Lily is not in the active eaters set.*

**REID:** And both positions accept the convergence.

**KEVEN:** The safety voice accepts the contextuality *because the substrate is what knows.* The household-composition fold tells the filter who's in the household this week, who's a sensitive guest, who's a non-eater of this allergen. *The filter is more informed; the filter can be more contextual without losing the safety property.* The customer-autonomy voice accepts the filter *because the substrate gates it sensibly* — the customer's own library respects the customer's own choices in the steady state; the filter sharpens when the substrate has identified a context that warrants the enforcement. *The disagreement converged on the architecture, not on either party giving up the position.*

**REID:** And the principle generalizes.

**KEVEN:** *The substrate decides; the substrate is what knows the context.* The household-composition fold is the substrate. The dietary-profile-by-member is the substrate. The audit chain is the substrate. *The architecture's job is to make the substrate available to every surface that needs to make a contextual call.* The customer is the better for it — because the same filter that protects her household from accidental allergens *also respects her right to cook pad thai on a Friday when Lily is at a sleepover.*

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

**KEVEN:** Three things into Episode Twelve. Each one a thing a non-technical leader can carry into a Monday meeting.

**KEVEN:** *One — the engine is real; the front door is the work.* The system that composes Sarah's seven-day meal plan exists today. What's not yet live is the way recipes get *into* her library — *the YouTube flow, the friend-shared flow, the family-heirloom flow, the restaurant-reverse flow, the holiday-favorites flow.* Capture is where the seeded set becomes Sarah's cookbook. *The grocery app turns the chore into a managed system; the kitchen library turns the household's food identity into a managed library.* Carry that.

**KEVEN:** *Two — the cookbook knows your household.* Fifteen cuisines, each with its defining ingredients. The retailer plug-ins declare what cuisines they carry. The meal-plan splits the shopping list by cuisine and routes specialty items to the right retailer. *The customer who cooks Korean Monday, Italian Tuesday, Mexican Wednesday, Thai Thursday — that customer gets the cuisine without thinking about the store.* The substrate stitches. Carry that.

**KEVEN:** *Three — captured recipes stay in the household tenant.* The Korean grandmother's kimchi recipe is not Microsoft's. The recipe is not the cloud's. *The recipe is the family's.* The provenance row, the audio narration, the photo of the dish, the family tags — none of it leaves the tenant. Episode Twelve walks this in full. Episode Eleven plants the line that makes the privacy claim defensible at the substrate. *The cloud is what cloud is for. The household is what household is for.* Carry that.

**REID:** Engine real, front door is the work. The cookbook knows your household. Recipes stay in the tenant. Three carries. Into Episode Twelve.

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
