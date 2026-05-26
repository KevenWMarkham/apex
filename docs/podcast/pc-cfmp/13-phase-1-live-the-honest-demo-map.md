# Episode 13 · Phase 1 Live — the honest demo map

**Episode 13 · Phase 1 live · the honest demo map** — Monday morning, 8:47 AM. The seller has the customer's CIO and architect on a 9 AM call, and they have asked her to walk what CFMP can do *today*. Not the v2 vision. Not the roadmap. Not the design slides. *What ships? What can the architect verify on the screen by 9:30?* The seller opens two browser tabs — the Portal `/architecture` page on one, the Portal home page on the other — and rehearses every claim against what the architect will see if he opens the same URL on his own laptop. This episode is the rehearsal. The honest demo map. Eight sub-sections, every claim cited to a live tile on the live page. The roadmap conversation is a different conversation. *This episode does not have it.*

**Builds on:** the show bible (00-show-bible-and-format) · Episodes 01–12 · the live `/architecture` page at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` · `CFMP-Capabilities-Map.html` (the honest status histogram) · `CFMP-Mobile-Sprint-Orchestrator.md` · `CFMP-Mobile-Roadmap.md` · `CFMP-Fulfillment-Sprint-Orchestrator.md` · `CFMP-Sonos-Sprint-Orchestrator.md`
**Run time:** ≈ 40 minutes target — the discipline of the documentary deep-dive
**Last updated:** 2026-05-26

---

## Cold Open

[Sound: a Monday morning at eight-forty-seven. A second-floor home office on the cooler side of the house, the window cracked one inch for the small breeze that smells of cut grass three lawns over. A laptop fan on its low setting. A coffee cup on a coaster, two-thirds full, set down at eight-thirty-six and now barely off the heat plate's curve. Outside, a school-bus pass three blocks over — the long diesel hum, the brakes, the doors opening, the doors closing, the diesel hum receding. Inside, two browser tabs open side-by-side on a thirty-two-inch monitor — the Portal `/architecture` page on the left, the Portal home page with the chat panel and the dietary chips on the right. The seller has a notebook open beside the keyboard, the kind of notebook that has the bottom-third filled with bullet points and the top-third filled with arrows and circles. The page numbers are dog-eared.]

It is eight-forty-seven on a Monday morning, and the seller has the customer's CIO and architect on a nine-o'clock call. They are not hostile. They are, in fact, the kind of customer she likes — the architect is sharp, the CIO is direct, and both of them have done the reading. The Account Team Partner forwarded her the prep note Friday afternoon, and the prep note had one paragraph that mattered. *They have read the design memo. They liked the architecture. They want to see what ships today, not the v2 vision. The architect is going to open his own laptop and walk the same URL while you walk yours. He is going to verify every claim against the page in front of him. If you say it, he will check it. Please do not say anything you cannot show.*

She has the page on the left monitor. She has the seven Portal pages bookmarked. She has the chat panel ready with a sample query that exercises the catalog specialist's tool surface, and a follow-up that crosses into the wayfinder specialist's routing tools, and a third that triggers the concierge specialist's weather composition. She has the architecture page's last-five-LedgerRows tile pinned, because she wants the architect to see a real audit row scroll in while they are talking. She has the dietary-chips strip set to *gluten-free* plus *dairy-free*, because she wants the architect to see the catalog filter change in real time. She has the cue-playback path ready on the mobile PWA in the second tab on her phone, with the AirPlay-bridge already paired to a Sonos Era 100 on the credenza behind her, because she wants the cue to play out of the right speaker when the orchestrator hands it back.

Eight-forty-eight. She picks up the phone. The number is in her favorites. *Reid. Last sanity check. I am walking the live system Monday morning. Help me line up every claim with what they will see.*

Reid does not need the preamble. He has been waiting for this call since Friday. He says — *This is the right call. The series so far walks the architecture as designed. Episode Thirteen is the un-aspirational version — what is in code, what is on the screen, what the regulator could verify in three minutes. Let's go through it.* And then he says the line she is going to repeat to herself between every section of the demo. *This episode is the honest demo map. Every word is verifiable on the slash-architecture URL the seller just put on her screen. Anything that requires explanation of what is coming next, this episode does not name. The roadmap docs do.*

She writes the line in the notebook above the bullet points. She underlines *every word verifiable*. She underlines *the roadmap docs do*.

[Sound: the small click of a pen cap going back on. The coffee cup lifting and setting back down. A cardinal somewhere outside the cracked window. Cut to a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start with that line of yours. *This episode is the honest demo map. Every word is verifiable on the slash-architecture URL.* Because this is the episode that calibrates everything we have said for twelve episodes against what the architect will see if he opens the page on his own laptop.

**REID:** And the discipline is the point. Twelve episodes walked the architecture as designed — the agent fleet that will eventually ship, the audit chain that will eventually run on WORM-tier OneLake Delta, the Sonos channel that will eventually take the direct Cloud Control path, the fulfillment tier that will eventually fan out across three providers. *The architecture as designed.* That is the rigorous, complete picture. Episode Thirteen is the inverse. Episode Thirteen is the architecture as *shipped*. The honest seller has both — and the honest seller does not mix them in the same breath on a demo call.

**KEVEN:** Welcome to the CFMP Podcast. Episode Thirteen. *Phase 1 live · the honest demo map.* This is a documentary deep-dive. It is the seller's *what can I demo Monday?* reference episode. Eight sub-sections. The three Container Apps. The four-specialist agent fleet. The five MCP servers. The data tier. The cloud AI services. The audit chain today. The Sonos channel today. The chat panel that does the demo's headline interaction. Every claim cites a tile on the live page. A reading, a disagreement, three carries.

**REID:** Let's go.

---

> **Episode framing admission:** this is the canonical 1:1 walkthrough of what the live system actually does today. *Phase 1 LIVE, full stop.* The rest of the series — Episodes 02 through 12 — walks the architecture as designed. Episode 13 is the demo conversation. The roadmap conversation is Episode 09 plus the four sprint orchestrator docs in `docs/packs/`. Do not mix the two conversations in the same breath.

## What ships today

> **Episode honesty calibration · 2026-05-26**
> This episode is the contract with the architect on the other end of the demo. *Every word verifiable on the slash-architecture URL.* Anything not on this page lives in the roadmap docs. The CFMP Capabilities Map at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` is the authoritative live-state source. The status histogram on the capabilities map page tells the story in one glance — *approximately forty-three green completed, thirty-two yellow in-progress, twenty-four white not-started, eighteen question-mark proposed.* The seller pitches the green. The seller names the yellow as in-progress when asked. The seller does not pitch the white or the question-mark on a demo call.

**Phase 1 live (today):** three Container Apps (`ca-visionkit-portal` · `ca-visionkit-orchestrator` · `ca-visionkit-mobile`); four specialists (catalog · wayfinder · auto_replenish · concierge) with their real toolsets; five MCP servers (parsml · cxml · merml · weather · ledger); Postgres `pg-visionkit-4459` plus pgvector with nineteen tables; Blob `stapexdemo50097` with apex-docs at eighty-two megabytes; IoT Hub `iothub-visionkit-7665`; Azure OpenAI `aoai-apex-demo` hosting gpt-5-mini plus gpt-4.1-mini times four; Azure AI Speech `speech-apex-demo` with `en-US-AvaMultilingualNeural`; Azure AI Vision `cv-apex-demo` with the 1024-dim embeddings; Azure Maps `maps-visionkit` with the Web SDK plus tiles plus Weather Services; LedgerRow with fourteen fields and the HITL gate stamp; trace_id propagation across surfaces; Portal chat panel that ties it all together; Sonos cue path via the mobile-PWA AirPlay-bridge.

**Not live today (Phase 2+ roadmap, named for honesty only):** sixth MCP `fulfillment-mcp`; Pharmacy, Trips, Coupons specialists; WORM-persisted LedgerRow; live Purview lineage upload to `/atlas/v2/entity/bulk`; Sonos direct Cloud Control via OAuth; Custom Vision SNPE for on-device inference; Azure Maps Creator for real-retailer Drawing Packages; Entra External ID swap (today `auth_mock.py`).

The rule of the episode is *the green list is the demo; the not-live list is the roadmap conversation, not this conversation*.

---

## The conversation

### The three Container Apps in East US 2

**KEVEN:** Picture the architect on the other end of the call, opening the URL on his own laptop. The first thing his eye lands on is *three boxes side by side near the top of the page.* Three places the customer's life happens — *the customer's app, the operator's console, the agent's home.* That's the deployment surface, in one glance. The architect has verified the region and the service count in fifteen seconds. *Three Container Apps in East US Two.* One ACR. One subscription. One resource group.

**REID:** Name them in order. The way the page names them.

**KEVEN:** *One — `ca-visionkit-portal`.* Next.js fifteen. The Portal the operator uses, the surface the seller will share in five minutes. Seven pages live today. The home page at slash, with the chat panel and the dietary chips. *Meal-Plan* at slash-meal-plan, where the seven-day plan renders and the shopping list expands. *Concierge* at slash-concierge, the proactive-moments surface. *Auto-Orders* at slash-auto-orders, the subscription view. *Profile* at slash-profile, the customer profile surface. *Architecture* at slash-architecture, the page we are walking right now. *Kiosk* at slash-kiosk, the in-store self-service surface. Seven pages. All live. All shipping. The architect can open every one of them in his own browser while we talk.

*Two — `ca-visionkit-orchestrator`.* Python. The agent runtime. Hosts the parent `gpt-5-mini` orchestrator and the four specialist children. Talks to the five MCP servers over the typed tool boundary. Emits LedgerRows. Propagates the trace_id. This is the brain. The Portal calls into it from the chat panel; the Mobile PWA calls into it from the scan flow and the meal-plan flow; the Sonos cue path calls into it from the speak-array composition.

*Three — `ca-visionkit-mobile`.* Next.js fifteen. PWA. The Scan-First Home MVP at slash-preview. The mobile surface where Sprint One is in progress today. The PWA the customer installs on her phone. The surface that carries the AirPlay-bridge to the Sonos in the kitchen.

**REID:** Three Container Apps. One Azure region. One ACR — `acrvisionkit4459`. That is the deployment surface a seller can demo today. The architect opens the live slash-architecture URL — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — and sees these three boxes at the top of the page. He clicks each one. The box opens. The box names the live URL, the resource type, the deployment status. No mystery. No aspirational asides. *Three boxes. Three URLs. Three live services.*

**KEVEN:** And the seller's discipline at this point is to say only what the box says. *Three Container Apps in East US Two on the standard Container Apps offering. One ACR. One subscription. One resource group.* That is the deployment surface. The architect verifies the surface in fifteen seconds. The conversation moves to the next tier.

### The four-specialist agent fleet

**KEVEN:** Tier two on the page. Picture Sarah typing one question into the chat panel — *what should I make for dinner Wednesday.* Behind the panel, a planning brain reads the question, decides which kind of thinking it needs, and hands the question to the right specialist. The architect sees the routing happen on his own laptop in real time. *Live today — the parent orchestrator plus four specialist children.* Walk the four.

**REID:** Walk the four. Then walk what is *not* in the fleet today.

**KEVEN:** The parent is `gpt-5-mini`. It does intent decomposition and routing. The four specialists are each a `gpt-4.1-mini` wrapping a tight tool surface. *One — `catalog_specialist`.* Its tool surface is `search · get_product · recipe_for_items · suggest_pairings`. Four tools. The specialist that owns the SKU truth, the recipe composition, the pairing suggestion. Sarah types *I want to make galbi-jjim Wednesday* into the chat panel, the parent routes the intent to the catalog specialist, the specialist composes against the seven-ninety-six-SKU MERML catalog, and the answer comes back with the items, the prices after discount, and the dietary flags inline.

*Two — `wayfinder_specialist`.* Its tool surface is `SKU → planogram → walking route over Azure Maps`. The specialist that turns a list into a walk. The customer in the store opens the slash-kiosk page, scans a few items, asks for the most-efficient route across the store, and the wayfinder specialist runs the planogram lookup, composes the order, and renders the walking route on the Azure Maps tile.

*Three — `auto_replenish_specialist`.* Its tool surface is `list_shipments · enroll · pause · get_customer_360`. The specialist that owns the subscription pattern. The customer opens the slash-auto-orders page, sees the items she has on cadence, pauses one for the week she is traveling, enrolls a new one for the kid's diapers. The specialist runs each tool against the `Gold_VV_AutoOrders` and `Gold_VV_Customer360` Gold views via the parsml and cxml MCPs.

*Four — `concierge_specialist`.* Its tool surface is `list_concierge_moments · get_weather · generate_concierge_moments`. The specialist that owns the proactive-moments surface. The customer opens the slash-concierge page on a Saturday morning, and the concierge specialist composes the moments — *the forecast is sixty-eight and overcast this afternoon, the romaine in the pantry is on day six, the kid's birthday is next Saturday* — into a small set of cues the customer can act on or dismiss.

**REID:** Four specialists. Four toolsets. Three to five tools per specialist. *That is the agent fleet that ships.* And the discipline I want to land for the seller now — *Pharmacy is not in the fleet today.* The cold open of Episode Two walked a Pharmacy specialist responding to a regulator question about a Robert Park refill. That episode is the architecture as designed. Episode Thirteen is the demo. *In the demo, Pharmacy is not in the fleet.* The seller does not say *and Pharmacy* on a Monday-morning call.

**KEVEN:** Same for *Trips.* Same for *Coupons.* The design names all three. Episode Two named all three. Today's live fleet is the four — catalog, wayfinder, auto_replenish, concierge. The Pharmacy, Trips, and Coupons specialists are in the sprint roadmap, not in the deployment. The architect opens the orchestrator's registered-specialist list — it is on the architecture page, in the agent-fleet tile — and sees four entries. Not seven. Four. *Demo the four. Roadmap the rest.*

**REID:** And the chat-panel exercise — the seller can pose a question that triggers each of the four, visible end-to-end. Pose a *find me low-sugar dairy-free snacks* question. The parent routes to catalog. Catalog returns. Pose a *route me to the aisle for the eight items on my list at the kiosk* question. The parent routes to wayfinder. Wayfinder returns. Pose a *show me my shipments arriving this week* question. The parent routes to auto_replenish. Auto_replenish returns. Pose a *what should I be thinking about for the weekend* question. The parent routes to concierge. Concierge returns. *Four questions, four specialists, four toolsets exercised, all visible on the screen.* That is the demo of the fleet.

### The five MCP servers

**KEVEN:** Tier three on the page. The boundary every agent call passes through to reach the customer's data. *Sarah's catalog question; Sarah's profile; Sarah's auto-replenish history; Sarah's weather; the audit row that captures all of it — five governed surfaces, five servers, one boundary discipline.* The architect verifies the boundary by counting the boxes on the tier — five — and clicking each one. Five MCP servers, live today.

**REID:** Walk them. Then name what is not there.

**KEVEN:** *One — `parsml-mcp`.* Composes against `Gold_VV_AutoOrders`. The parsml namespace is the auto-replenish subscription substrate — shipments, cadences, pauses, enrollments. The auto_replenish_specialist calls into parsml; parsml validates the tool call against the typed schema; parsml composes the Gold view from the canonical Silver model; parsml returns the structured result; parsml stamps the audit row on the way back. The architect opens the parsml tile on the page and sees the tool surface, the Gold view it composes, the audit emission discipline.

*Two — `cxml-mcp`.* Composes against `Gold_VV_Customer360`. The cxml namespace is the customer-profile substrate — preferences, allergens, dietary categories, household composition, the saved providers. Multiple specialists call into cxml — the catalog specialist when it needs the dietary filter, the concierge specialist when it needs the proactive-moments context, the auto_replenish specialist when it needs the customer's address for shipment.

*Three — `merml-mcp`.* Composes against `Gold_VV_Catalog`. The merml namespace is the catalog substrate — *seven-hundred-and-ninety-six SKUs seeded in Postgres today.* Real data. Real prices. Real allergen tags. Real cuisine tags. The catalog specialist's four tools all compose against merml.

*Four — `weather-mcp`.* Composes against `Gold_VV_Weather`. The weather substrate. Calls out to Azure Maps Weather Services for the forecast surface. The concierge specialist uses it for the *forecast is sixty-eight and overcast* cue. The wayfinder specialist uses it for the *will it be raining when you walk to the car* nudge.

*Five — `ledger-mcp`.* Composes against `apex_ledger_rows`. In-memory today. The audit-emission substrate. Every state change in any specialist's flow gets a LedgerRow through ledger-mcp. The fourteen-field shape. The trace_id. The model version. The HITL gate stamp when the cart-add exceeds fifty dollars. Every row is emitted; every row is visible; every row is queryable through the architecture page's last-five-rows tile.

**REID:** Five MCP servers. Now the discipline — *the sixth MCP, `fulfillment-mcp`, does not exist today.* Episode Seven walks that design. The fulfillment provider ABC, the quote-aggregator fan-out, the recommendation score, the substitution flow with dietary safety at search. *All of that is the design.* On the demo, the seller does not say *and we have fulfillment-mcp*. The seller says *we have five MCP servers today, and the sixth one — the fulfillment-mcp — is in the next sprint, here is the orchestrator doc, here is when it lands.* That is the two-conversation discipline. The five are the demo. The sixth is the roadmap.

**KEVEN:** And the architect's verification — he opens the MCP-tier section of the architecture page, counts the boxes, finds five, asks where fulfillment is. The seller answers — *not yet; in the sprint roadmap; here is the document.* The architect signs off because the answer matches the screen. The honesty moat holds.

### The data tier — Postgres, Blob, IoT Hub

**KEVEN:** Tier four on the page. *Where Sarah's household actually lives in the cloud.* Her lots, her profile, her pantry, the catalog she searches against, the audio files of every cue she's heard, the structured detection JSON from the camera on her counter. *Three primary stores. All live.* The architect walks them in fifteen seconds.

**REID:** Walk them. Then name the numbers.

**KEVEN:** *One — `pg-visionkit-4459`.* PostgreSQL Flexible Server with pgvector enabled. Nineteen tables. Thirty-two megabytes today. The state store. The customer profiles, the auto-orders, the meal-plans, the recipe library seeded, the seven-ninety-six SKUs of the MERML catalog. The vector embeddings for the catalog's semantic-search surface — the catalog specialist's `search` tool runs the embedding-distance query against pgvector when the customer types a natural-language query like *something spicy and Korean for Wednesday*. Real Postgres. Real tables. Real rows. Real embeddings.

*Two — `stapexdemo50097`.* Standard Storage account. Three containers that matter for the demo. *Audio-in* — receives the customer's microphone uploads for the speech-to-text path. *Audio-out* — holds the cue WAV files Azure Speech text-to-speech produced for the playback path. *Frames* — holds the Vision Kit's selective-uplink frames for the exception path. Plus a fourth container the architect should see — *apex-docs* — which holds *four-thousand-three-hundred-and-fifteen APEX documents at eighty-two megabytes total.* That is the documentation substrate for the agent's grounding when the customer asks a question that needs to land on a documentation passage.

*Three — `iothub-visionkit-7665`.* Azure IoT Hub. Device-to-cloud telemetry from the Vision AI Dev Kit. When the device is online — and the device's audio HAL is not always — the IoT Hub receives the structured detection JSON the local-inference runtime emits. The frames stay on the device; the structured JSON is what comes up the wire.

**REID:** *This is the substrate. Thirty-two megabytes of catalog in pgvector. Eighty-two megabytes of docs in Blob. Real Postgres. Real Blob. Real IoT Hub.* The numbers are small because the demo is small. The shape is real. The shape is what the architect verifies. *Shape, not scale, is the demo's claim.* When the architect asks *will this scale*, the answer is *the Azure substrate underneath scales — Flexible Server scales to terabytes, Blob is unbounded, IoT Hub scales to millions of devices. The shape is the same. The fill is the demo's fill.* Honesty about scale; honesty about shape; both honest in the same breath.

**KEVEN:** And the seller's discipline — *do not pitch the numbers as if they are the demo's claim*. The demo's claim is *the shape ships*. The seven-ninety-six SKUs prove the catalog substrate is real; the four-thousand-three-hundred-and-fifteen docs prove the grounding substrate is real; the IoT Hub proves the device path is real. *Three primary stores, all live, all verifiable on the page.* The architect signs off.

### The cloud AI services

**KEVEN:** Tier five on the page. *The Microsoft services the agent fleet actually calls.* The models that answer Sarah's question. The voice that speaks the answer in her kitchen. The image recognition that resolves the jar of gochujang in her hand. The maps that route her through the store. The telemetry that lets the regulator's three-minute replay land. *Five services deployed, all called from the orchestrator.*

**REID:** Walk them.

**KEVEN:** *One — Azure OpenAI.* The resource is `aoai-apex-demo`. It hosts the orchestrator's `gpt-5-mini` deployment for the parent, plus four `gpt-4.1-mini` deployments — one per specialist. Five deployments on one resource. The architect opens the Azure OpenAI tile on the page and sees the deployment list.

*Two — Azure AI Speech.* The resource is `speech-apex-demo`. Speech-to-text for the mic-input path on the Mobile PWA's scan-and-talk flow. Text-to-speech for the cue path — `en-US-AvaMultilingualNeural` is the default voice the show bible specified, and it is the same Ava voice across the Portal browser-speaker fallback, the Mobile PWA's audio-out, and the Sonos cue. *Same voice across surfaces.* The architect hears the voice when the seller plays a cue back from the chat panel; the customer hears the same voice when the cue plays on the Sonos. *Voice continuity is a real property of the demo.*

*Three — Azure AI Vision.* The resource is `cv-apex-demo`. Image embeddings — *one-thousand-twenty-four-dimensional.* The Catalog specialist uses the embeddings for the scan-resolver flow today — when the customer's phone uploads a frame of the gochujang on the shelf, the resolver runs the embedding match against the catalog's image-embedding table and returns the canonical SKU. The architect opens the Vision tile and sees the embedding dimension.

*Four — Azure Maps.* The resource is `maps-visionkit`. The Web SDK is loaded in the Portal's wayfinder surface for the route render. The tiles are loaded for the map view. The Weather Services API is called by `weather-mcp` for the forecast surface. *Three Azure Maps surfaces live in the demo — SDK, tiles, weather.*

*Five — Application Insights and OpenTelemetry.* Not a Cognitive Service in the formal sense, but the telemetry substrate that ties the trace_id end-to-end. The orchestrator emits OTel traces; Application Insights collects them; the architecture page's *last five LedgerRows* tile reads from the same span store. The architect can pivot from a LedgerRow to its OTel trace in two clicks.

**REID:** Five live cloud AI services. Now the discipline — *Custom Vision SNPE for on-device inference is planned, not live.* The Vision Kit's on-device model runs today, but the SNPE-quantized Custom Vision pipeline that compresses a custom model into the device's neural processor is the v2 commitment from Episode Twelve, not a service the seller demos today. Similarly — *Azure Maps Creator for real-retailer Drawing Packages is planned.* The wayfinder's planogram-to-route render today uses synthetic store maps, not the customer-retailer's actual Drawing Package. The seller does not say *and we are integrated with your store layouts today*; the seller says *the wayfinder substrate runs against synthetic planograms today; integrating against your Drawing Package is the v2 commitment.*

**KEVEN:** *Five live services. Two named-as-planned for honesty.* The architect signs off because the architecture page distinguishes the live tiles from the planned tiles with visible status indicators. The capabilities-map histogram colors the live ones green and the planned ones white or question-mark. The seller does not have to remember the distinction; the page enforces it.

### The audit chain — what's there today

**KEVEN:** Tier six on the page. *The substrate that lets the regulator's three-minute replay from Episode Two be a real moment, not a marketing diagram.* Every state change in Sarah's life with the system becomes a row on this chain. *Fourteen fields per row. Signed in-memory today.* Walk the fields the architect counts.

**REID:** Walk them. The architect will count them.

**KEVEN:** The fourteen fields. *`row_id`, `parent_row_id`, `trace_id`, `tenant`, `actor_kind`, `actor_id`, `action`, `payload_hash`, `timestamp`, `model_apex`, `manifest`, `policy`, `prompt`, `hitl_status`.* The architect verifies the count and the names against the schema-tile on the page. Then he checks the values — *the model_apex field reads `apex/gpt-5-mini`, the manifest field reads `cfmp-v0.2`, the policy field reads `cfmp-policy-v0.1`, the prompt field reads `cfmp-prompt-v0.3-ground-truth`, the hitl_status reads `pending` if the cart-add exceeded fifty dollars and `not_applicable` otherwise.* Every field is populated. Every field is verifiable. The architect signs off on the schema before he asks the next question.

*The trace_id propagates.* From the Mobile PWA — when Sarah scans the gochujang — through the orchestrator — when the parent routes to catalog — through the MCP — when catalog calls into merml-mcp for the product lookup — through the response — when the specialist composes the answer — through the cue path — when the speak-array goes to Azure Speech text-to-speech — and out to the Sonos through the AirPlay bridge. *One trace_id across five surfaces.* The architecture page's last-five-rows tile shows the rows live; clicking a row pivots to the full trace; the trace shows every span across every surface that carried the same identifier.

**REID:** And the HITL gate. *On a cart-add greater-than-or-equal to fifty dollars, the LedgerRow stamps `hitl_status=pending` and surfaces a human-in-the-loop confirmation chip in the customer's surface.* The architect verifies the gate by triggering it on the demo — the seller adds a forty-eight-dollar cart, the row goes through with `hitl_status=not_applicable`; the seller adds an eighty-dollar cart, the row goes through with `hitl_status=pending` and the confirmation chip appears. *The gate is a live property of the demo.*

**KEVEN:** And the discipline. *This is what the regulator gets in three minutes — every step, every model version, every tool call, every consent stamp. Today. In memory.* The architect asks the obvious question — *what happens when the orchestrator restarts; do you lose the rows?* The answer is *yes; today the LedgerRow store is in-memory; the rows persist for the orchestrator's lifetime; restart wipes the buffer.* That is honest. The seller does not pretend otherwise. The seller names the live state — *in-memory today* — and names the trajectory only when the architect asks — *WORM persistence to OneLake Delta is the Phase Two commitment; here is the document; here is the sprint.*

**REID:** Two more honest pieces. *Bronze landing is partial.* Four internal sources are wired today. Plus ninety seeded mocks for the demo coverage. The Bronze layer of the medallion is real for the wired sources; the un-wired sources are mocked at the Bronze tier so the Silver-to-Gold composition has something to compose against. The seller names that — *Bronze partial; full landing is the Phase One completion sprint.* And — *Purview lineage emits offline today.* The orchestrator produces Atlas-shaped lineage edges in the LedgerRow's metadata; the live `/atlas/v2/entity/bulk` upload to Microsoft Purview is the Phase Three commitment. Today the edges exist as data; they do not yet flow to the catalog surface in real time.

**KEVEN:** *In-memory today, persisting tomorrow. Atlas-shape today, uploading tomorrow.* The seller names both honestly. The architect verifies both on the page. The honesty moat holds.

### The Sonos channel — what's the live path

**KEVEN:** Tier seven on the page. *Sarah's kitchen speaker today.* Live, ships, plays back in the room. The architect can hear the cue on the seller's own kitchen speaker over the call. *The Sonos channel ships today via the phone's AirPlay bridge.* Walk the live path.

**REID:** Walk it.

**KEVEN:** The customer pairs her Mobile PWA — the slash-preview page or any Portal page rendered through the PWA — to a Sonos Roam or a Sonos Era One-hundred over Apple AirPlay Two. The pairing is done once, at install time, through the iOS AirPlay-target selector. The phone then becomes the AirPlay source; the Sonos becomes the AirPlay target. When the orchestrator hands back a cue — the catalog specialist says *the gochujang is in aisle six*, the concierge specialist says *the romaine is on day six and the forecast is overcast* — the speak-array goes to Azure Speech text-to-speech, the WAV comes back, the WAV plays through the phone's audio-out, AirPlay routes it to the Sonos. The customer hears the cue in the room she is in.

**REID:** And the audit-tag. Russo's catch from Episode Eight.

**KEVEN:** Russo's catch. *Every Sonos cue's LedgerRow carries `channel: mobile_airplay`.* That field is on the row. The architect sees it when the row scrolls into the last-five-rows tile. The audit is honest about the path — the cue did not go through Sonos's Cloud Control API; it went through the AirPlay bridge from the phone. The audit names the bridge. *Audit-tagged honesty about the path.*

**REID:** Now the discipline. *The direct Sonos Cloud Control path — `play_audioClip` via OAuth — is in the roadmap. It is not the live path today.* The Sonos Cloud Control integration is Episode Six's design; the Sonos sprint orchestrator names the work. Today the seller demos the AirPlay-bridge path. The seller does not demo the direct path. The seller does not say *and we are integrated with Sonos Cloud Control today*. The seller says *the cue plays on a Sonos in the room today via the AirPlay bridge from the phone; the direct Cloud Control path is the next sprint; here is the document.* The architect signs off because the audit-row tag matches the screen.

**KEVEN:** And the seller's option to play the cue in the room during the demo. *Pair the phone, hit the chat panel question that produces the cue, the room hears it.* The customer's architect — even on a remote call — hears the cue play back through the seller's Sonos in real time, with the seller's voice naming the audit row that just stamped `channel: mobile_airplay`. The cue is the demo's small piece of theater; the audit tag is the demo's piece of honesty. *Both in one breath.*

### What the seller's chat panel does today

**KEVEN:** Tier eight. *The demo's headline moment — the chat panel where Sarah's experience renders end-to-end.* The seller types a question. The architect watches the routing happen. The cue plays in the seller's room. The cart updates. The HITL gate fires if it should. *One trace across eight surfaces, visible on the architect's own screen.*

**REID:** Walk it end-to-end.

**KEVEN:** The seller opens the Portal home page. The chat panel is on the right side. The dietary-prefs chips are above the input — *Gluten-free, Dairy-free, Vegan, Low-sugar, Nut-free, Keto.* Six chips. The seller toggles *Gluten-free* plus *Dairy-free* on. The chips light up; the catalog specialist's filter set updates in real time; the architect sees the request payload in the network tab if he opens dev tools.

The seller types *what should I make for dinner Wednesday that fits these.* The chat panel posts to the orchestrator. The parent does intent decomposition — *the customer wants a dinner suggestion within her dietary filters; route to catalog specialist with the meal-plan tool surface.* The catalog specialist runs `recipe_for_items` against the seven-ninety-six-SKU MERML catalog with the gluten-free plus dairy-free filter applied. The response comes back with three candidate dinners. The chat panel renders them. Each candidate has a *speak* field — the spoken-narration form for the cue path. The seller taps the play icon on the first candidate. The speak field goes to Azure Speech text-to-speech with the `en-US-AvaMultilingualNeural` voice. The WAV comes back. The WAV plays. *If the phone is in AirPlay-paired mode*, the WAV plays through the Sonos in the room; *if not, it plays through the browser speaker directly.* The architect hears the cue.

The seller then clicks the *add to plan* button on the recommended dinner. The cart updates. The price totals. If the cart total now exceeds fifty dollars, the HITL gate fires — `hitl_status=pending` shows on the LedgerRow tile, a confirmation chip appears in the customer's surface, the seller demonstrates the human-in-the-loop confirmation. *Visible end-to-end. Today.* The trace_id is the same across the chat post, the orchestrator's intent decomposition, the catalog specialist's tool call, the merml-mcp's Gold view composition, the speech text-to-speech, the cue playback, the cart-add, and the LedgerRow stamp. *One trace across eight surfaces.* The architect verifies the propagation by clicking the row and walking the spans.

**REID:** Eight sub-sections. Every one has a click-through equivalent on the slash-architecture URL. Anything I did not name lives in the roadmap docs. *That is the rule of this episode.*

---

### A reading I want to do

**REID:** A reading. This one is short and it is the discipline of the episode, not a separate intellectual frame. I want to recommend the principle of *demo discipline* from the early enterprise-software practitioners who built credibility loops before the agentic era.

The canonical version is Aaron Levie's early Box-dot-com demo discipline — the principle Levie articulated on stages and on tape in the twenty-twelve through twenty-fifteen window when Box was building enterprise trust against incumbents twenty times its size. *A seller's demo should track the product one-to-one, no aspirational asides.* The argument is short and it is right. The customer's architect is not deceived by aspirational asides; the architect is *eroded* by them. Every claim that does not match the screen costs trust on the next claim that does. The credibility loop compounds in either direction — the more the screen matches the pitch, the more the architect signs off on the parts of the pitch that can not be screened; the more the screen does not match, the less the architect signs off on anything.

The companion reading is Tom Tunguz's writing on enterprise-software-demo trust — his early-twenty-tens analyst notes on conversion through demo discipline, the pattern that *the deals that close are the deals where the demo tracked the product, and the deals that get stuck in evaluation purgatory are the deals where the demo over-promised against what shipped.* The pattern is verified across hundreds of enterprise-software conversion analyses Tunguz published over his decade-plus as a venture-backed analyst. *Over-promising in the demo is the most common cause of stalled evaluations.* The fix is the inverse — demo less than you can show; let the architect ask for the next thing; pivot to the roadmap conversation when asked, not when un-asked.

Reid's framing — *the honest demo is the credibility loop. Anything the architect cannot verify on his own screen breaks the trust. This episode is the discipline.* The reading sharpens the episode's argument from intuition to method. Levie names the principle. Tunguz documents the conversion math. CFMP's slash-architecture page is the substrate that makes the principle ship-able — the page is the architect's screen; the page is the contract; the page is the credibility loop. The seller who walks the page tile-by-tile, claims-the-tile, then-pivots-to-the-roadmap-when-asked, runs the conversion-math-winning version of the demo. Levie and Tunguz together teach the conversion math. CFMP gives the conversion math its substrate.

**KEVEN:** And the carry-forward of the reading. *The honest demo is not less ambitious than the over-promising demo; it is more ambitious. The ambition is the credibility loop, not the headline feature list.* The architect remembers the credibility loop a week later. The architect does not remember the feature list. The credibility loop is what gets the second meeting. The feature list is what gets a polite *we will be in touch.* Levie taught it; Tunguz documented it; CFMP's page makes it operationally feasible.

---

### One disagreement

**REID:** One disagreement. And it is the one the brief named, and I want to be on the record arguing it because I think it matters to the seller's working discipline.

**KEVEN:** I want to push first. Because I think the seller has to be allowed to *mention* what is coming next. The customer wants to know the trajectory, not just the snapshot. The CIO on the nine-o'clock call is not buying a snapshot; the CIO is buying a partnership over eighteen months. The seller who refuses to even *name* what is coming next in the same conversation as the demo is — in my view — being too disciplined. Too pure. Too monkish. *Let her say it ships in Sprint Two.* The customer wants to hear it. The Account Team needs the seller to hear it.

**REID:** And I am going to push back hard. Because the *too pure, too monkish* framing is exactly the framing that erodes the credibility loop. Listen — there is a difference between *the seller naming the roadmap when asked* and *the seller naming the roadmap mid-demo, unprompted, in the same breath as a live claim.* The first is fine. The second is the conversion-math killer. Tunguz's data is clear — the deals that stall are the deals where the demo and the roadmap mix in the same sentence. The architect cannot tell which claims to verify. He goes home. He does not verify any of them. He sends the polite *we will be in touch.*

**KEVEN:** Defend the discipline more sharply then. Because I am not arguing for *the demo and the roadmap in the same sentence*. I am arguing for *the seller's freedom to name what is next when the moment is right*.

**REID:** Defend it this way. *Two conversations. Demo first, end-to-end, every claim verifiable on the screen. Then — and only then — the pivot.* The seller runs the demo to completion. The eight tiers on the page. The architect verifies each one. *The architect signs off on the demo before the roadmap conversation starts.* Then — *now let me walk the roadmap; here is what is not on this page yet, and when it lands.* The roadmap conversation has full freedom. The roadmap conversation can name *and Pharmacy is in Sprint Three, and fulfillment-mcp is in Sprint Two, and WORM persistence is in Sprint Four.* All of that is fine *in the roadmap conversation.* None of that is fine *in the demo conversation.* The two conversations are *sequential*, not *concurrent*. Sequence is the discipline.

**KEVEN:** And the test for the seller.

**REID:** The test for the seller is *the architect signs off on the demo before the roadmap conversation starts.* The seller runs the eight tiers. The architect verifies each one on his own screen. The architect says — out loud, in some form — *okay; I have verified what ships today; show me what is next.* That sentence is the gate. *That sentence is the pivot.* Before that sentence — the demo conversation, with its full discipline. After that sentence — the roadmap conversation, with its full freedom. The conflation Keven was defending is the conflation of *the demo conversation* with *the roadmap conversation*. The discipline I am defending is the *sequence.*

**KEVEN:** Conceded. The disagreement converges on *two-conversation discipline.* The seller runs the demo first, end-to-end, every claim verifiable on the screen. Then the seller pivots — *now let me walk the roadmap — here's what's not on this page yet, and when it lands.* The roadmap conversation has full freedom. The demo conversation does not. *This episode is the demo conversation. The roadmap conversation is Episode Nine and the Mobile, Sonos, and Fulfillment roadmap docs.* I concede the sequence is the discipline; the sequence is what protects the credibility loop.

**REID:** Converge. *Two conversations. Demo first. Roadmap second.* That is the discipline. Carry it.

---

### What to carry forward

The three durable takeaways. Numbered, because the seller carries them.

1. **The `/architecture` URL is the contract.** Every claim in this episode tracks something the architect can verify on the page. The three Container Apps in East US Two — verifiable. The four-specialist agent fleet — verifiable, with the registered-specialist list visible in the agent-fleet tile. The five MCP servers — verifiable, with the namespaces and Gold views named on each tile. The data tier — verifiable, with the resource names and the row counts and the megabyte sizes named on the storage tiles. The cloud AI services — verifiable, with the resource names and the deployments and the embedding dimensions named on the AI tiles. The audit chain — verifiable, with the fourteen-field schema named and the last-five-rows scrolling live. The Sonos AirPlay-bridge path — verifiable, with the `channel: mobile_airplay` tag visible on the audit row. The chat-panel end-to-end — verifiable, with the trace_id propagating across the eight surfaces. *Eight tiers. Eight verifications. One page.* Anything not on the page lives in the roadmap docs. The page is the contract. Carry that.

2. **Two-conversation discipline.** The demo conversation walks what ships today. The roadmap conversation walks what is planned. *Sequence, not concurrence.* The seller runs the demo end-to-end first, with the architect verifying each tier on his own screen. When the architect signs off — out loud, in some form — *the seller pivots to the roadmap conversation.* The roadmap conversation has full freedom; the demo conversation does not. The pivot sentence is the gate. *Demo first. Roadmap second.* The conversion math winners run the two conversations in sequence. The conversion math losers conflate the two in the same breath. Carry that.

3. **Episodes Two through Twelve walk the architecture as designed. This episode walks the architecture as shipped. The honest seller has both.** The series is the seller's working substrate over time. Episode Two earns the architecture-as-designed argument with the agent fleet and the audit substrate. Episode Twelve earns the privacy-as-architectural argument. Episode Nine earns the Independence-minded-pitch argument. *Each of those episodes is the long version of a topic.* Episode Thirteen is the *short version of every topic, calibrated against today's screen.* The seller pulls the long version when the architect asks the deep question; the seller pulls the short version when the architect asks the *what can I see today* question. The honest seller has both. Carry that.

---

So when the customer's architect opens the slash-architecture URL on his own laptop at nine o'clock on a Monday morning — the seller's demo is *already aligned with what he sees on his screen*. The three Container Apps are where the page says they are. The four specialists are the four specialists. The five MCP servers are the five MCP servers. The Postgres rows are the Postgres rows. The Azure Maps Web SDK is the Azure Maps Web SDK. The fourteen-field LedgerRow is the fourteen-field LedgerRow. The AirPlay-bridge tag is the AirPlay-bridge tag. *Every claim matches the screen.* The architect signs off on the demo. The CIO leans forward. The seller pivots — *now let me walk the roadmap.* The roadmap conversation begins. The conversion math holds.

Two conversations. Demo first. Roadmap second. The honest seller has both.

[Sound: the closing sting. ~6 seconds.]

---

## Further reading

- **Source docs**
  - The live `/architecture` page at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — this episode's authoritative source; the contract every claim cites against
  - `CFMP-Mobile-Sprint-Orchestrator.md` — the audit-driven gap closure sprint plus the Mobile-Portal Parity sprint; where the Mobile-side roadmap conversation lives
  - `CFMP-Mobile-Roadmap.md` — the Mobile parity backlog; the customer-facing roadmap that names the YouTube-to-recipe, friend-shared imports, and other capture flows in trajectory order
  - `CFMP-Fulfillment-Sprint-Orchestrator.md` — where the sixth MCP `fulfillment-mcp` lands; the FulfillmentProvider ABC, the three mock providers, the quote-aggregator, the substitution flow with dietary-safety enforced at search
  - `CFMP-Sonos-Sprint-Orchestrator.md` — where the direct Sonos Cloud Control path via OAuth lands; the planned replacement of the AirPlay-bridge as the primary path while keeping AirPlay as the fallback
  - `CFMP-Capabilities-Map.html` — the honest map; the status histogram on the capabilities page (approximately forty-three green completed, thirty-two yellow in-progress, twenty-four white not-started, eighteen question-mark proposed); the visual reference for the green-versus-yellow-versus-white discipline this episode walks
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — the deployment topology page that *is* this episode; open on a client call; *walk it tile-by-tile; let the page do the work the slide deck used to have to do*
- **Microsoft Learn**
  - Azure Container Apps — `https://learn.microsoft.com/azure/container-apps/` — the runtime substrate for the three Container Apps in East US Two
  - Azure OpenAI — `https://learn.microsoft.com/azure/ai-services/openai/` — the model-hosting substrate for the orchestrator's `gpt-5-mini` and the four specialists' `gpt-4.1-mini` deployments
  - Azure AI Speech — `https://learn.microsoft.com/azure/ai-services/speech-service/` — the voice substrate for the cue playback path, including the `en-US-AvaMultilingualNeural` neural voice the show bible specified
  - Azure AI Vision — `https://learn.microsoft.com/azure/ai-services/computer-vision/` — the image-embedding substrate for the catalog specialist's scan-resolver flow
  - Azure Maps — `https://learn.microsoft.com/azure/azure-maps/` — the Web SDK plus tiles plus Weather Services for the wayfinder specialist's routing and the concierge specialist's forecast
- **Industry / research**
  - Aaron Levie — early Box-dot-com demo discipline; talks and tape from the twenty-twelve through twenty-fifteen window; the canonical *track the product one-to-one, no aspirational asides* principle the episode is built around
  - Tom Tunguz — analyst writing on enterprise-software-demo trust; the conversion-math case that over-promising in the demo is the most common cause of stalled evaluations; the documentation of *the demo that tracks the product converts, the demo that over-promises stalls*
  - Apple Human Interface Guidelines — the *honest demos* posture across the macOS and iOS HIG sections that name the discipline as a first-class design value; useful as the consumer-software counterpart to Levie's enterprise-software argument
- **Sibling series cross-reference**
  - Cross-Cloud Agentic Episode 08 (*The Seller's Playbook*) at `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\08-the-sellers-playbook.md` — the framework-level treatment of the seller's working substrate; the sign-off line on that episode is reserved for the series finale equivalent (CFMP Episode 09), not for documentary deep-dives like this one

---

*Episode Thirteen is the honest demo map. The rest of the series walks the architecture as designed; this episode walks the architecture as shipped. Eight tiers, every one verifiable on the live slash-architecture URL. The seller's two-conversation discipline is the carry — demo first, roadmap second, the architect signs off on the demo before the roadmap conversation starts. The conversion math winners run the two conversations in sequence. CFMP's slash-architecture page is the substrate that makes the discipline ship-able.*
