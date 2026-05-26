# Episode 02 · The Customer Experience Six

**Builds on:** Disney Ep 1 (three segments, six pressure points) · Trilogy — Services Ep 3 (medallion / canonical) · Services Ep 4 (MCP + agent) · Services Ep 5 (retail margin / loyalty churn pattern)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: a domestic Sunday-evening living room. TV ambient. A "next episode" countdown.]

**KEVEN:** I want to start with a moment that probably happened in twenty million households last Sunday night. *Eight PM Pacific.* The Mandalorian or a Marvel show or *Bluey* or whatever is finishing. The countdown to next episode is ten seconds. Five. Three. *And the home screen autoplays into "Continue watching" or "You might like."*

[pause]

**RILEY:** And the experience hinges on —

**KEVEN:** The experience hinges on *what comes next.* A relevant recommendation keeps the viewer engaged. An irrelevant one is a discomfort moment. *Multiply by twenty million households per night times 365 nights times five global streaming brands at Disney*, and you have one of the largest at-scale recommendation problems in the world. Plus the cousins of that problem — ESPN highlight generation, international content localisation, the moment a Marvel film launches into a market and finds an audience. *That entire universe of moments is what the Customer Experience Six is about.*

Six APEX scenarios. Six Disney pressure points. Each one with a measurable KPI signal. *We walk all six this episode.* Each one developed fully, no jumping.

**RILEY:** I'm Riley.

**KEVEN:** I'm Keven Markham. Disney Account Podcast. Episode Two. *The Customer Experience Six.*

---

## The conversation

### Why CX is the right starting place

**RILEY:** Set up why we lead with CX.

**KEVEN:** Three reasons.

One — *CX is the most-visible-to-Disney's-leadership* set of scenarios. The Chief Customer Officer, the Presidents of Streaming, the Studio leadership, the Parks experience leaders — they all live in the customer experience. *The metrics they're held to live in the customer experience.*

Two — *the data foundation for CX scenarios is the cleanest at Disney.* Disney has invested heavily in the customer-and-loyalty data estate. Disney+, Hulu, ESPN+, Parks loyalty (MagicBand+, MyDisney accounts) — these systems generate the cleanest data in the Disney portfolio. *Bronze-to-Silver-to-Gold landing for CX scenarios is faster than for operational scenarios.*

Three — *CX scenarios produce KPI signals on quarterly cadence.* The Account Team can show measurable lift within a Wave 1 ninety-day window. *Compared to operational or build-related scenarios, CX gives a faster ROI-demonstrable result.*

For all three reasons, the Account Team's Wave 1 entry at Disney almost always starts in CX.

### Scenario one — Streaming-churn prediction

**KEVEN:** First scenario. *Streaming-churn prediction across Disney+, Hulu, and ESPN+.* KPI signal — *minus nineteen percent churn.*

The Disney context. Each streaming service has its own subscriber base and its own churn dynamics. Disney+ churn skews family-driven — kids' content drives retention. Hulu churn skews general-entertainment-driven. ESPN+ churn skews sport-season-driven. *Three different churn shapes; three different intervention windows.* The Disney challenge — operating these as a portfolio means you can intervene with *cross-service* offers that wouldn't make sense in any single-service company.

The pain point. Disney's churn measurement is sophisticated. Their churn *intervention* is still mostly manual. Marketing managers see weekly churn reports, design email campaigns, A/B test them, deploy them. *The cycle from signal to action takes weeks.* Customers who were going to churn often do, before the intervention reaches them.

The agent strategy. The streaming-churn agent watches subscriber behaviour continuously. It identifies elevated churn risk per subscriber, reasons about which service-and-offer combination is most likely to retain that specific subscriber (Disney+ bundled with Hulu? ESPN+ trial added? a specific Marvel premiere targeted?), and surfaces the recommendation to the loyalty team for approval. *The cycle from signal to recommendation compresses to hours, not weeks.*

The architectural shape. The agent reads from a customer-and-loyalty canonical at Silver — combining Disney+, Hulu, ESPN+, and parks-loyalty data via the canonical schema we covered in the Services Podcast. The Gold mart shapes per-subscriber churn features. MCP tools narrowly retrieve churn signal, customer LTV, eligible-offer-set, and inventory-aligned offers. The agent reasons. The recommendation lands in a marketing-operator review queue.

The KPI signal — *minus nineteen percent churn* on the targeted cohort over the prior quarter's baseline. For Disney's scale, that's *meaningful annualised revenue protection.* The Account Team should be careful — the framework's reference scenarios produce ranges, not point estimates; the precise Disney number depends on the engagement.

**RILEY:** And the seller's hook for this scenario —

**KEVEN:** *"Your churn measurement is sophisticated. Your intervention is still weekly-cadence. We can compress that cycle to daily. Wave 1, ninety days."*

### Scenario two — Personalised content recommendations & rails

**KEVEN:** Scenario two. *Personalised content recommendations and rails.* KPI — *plus twenty-three percent engagement.*

The Disney context. Every streaming service has a recommendation engine. Disney's engines have evolved through ML generations — first generation matrix-factorisation, then deep-learning-embeddings, now they're entering an agentic-augmented generation. *The structural challenge for Disney specifically* — content from Marvel, Pixar, Lucasfilm, ABC, FX, Searchlight, Nat Geo, and a hundred other production groups must all be surfaced. *Coherent recommendations across a heterogeneous content portfolio is the Disney-specific challenge.*

The pain point. Generic recommendation engines treat *every Marvel film as similar to every Marvel film.* In reality, the user who watched *Black Panther* may have completely different taste from the user who watched *Thor: Ragnarok.* Subtle distinctions within franchise content matter enormously for retention. *And the rails — the curated "this Sunday's family movie" or "espresso-quick episodes for your commute" rails — those need to compose with the personalisation.*

The agent strategy. The content-recommendation agent doesn't replace the recommendation engine. The agent *composes* on top of the engine. The engine produces candidate recommendations. The agent reasons about *which subset to surface in which rail at which moment for which user* — given the user's recent behaviour, their session context, the time of day, the household composition, the new-release calendar. The agent's output is *the actual rail layout for that user at that moment.*

The architectural shape. Same canonical foundation as Scenario One — customer-and-loyalty Silver. The Gold mart shapes per-user session features in real time. MCP tools query the underlying recommendation engine, retrieve user context, retrieve new-release inventory, retrieve rail templates. The agent composes the rail.

The KPI — *plus twenty-three percent engagement* on the agent-curated rails versus the prior algorithm-only rails.

### Scenario three — Cold-start boost for Marvel/Pixar/Lucasfilm launches

**KEVEN:** Scenario three. *Cold-start boost for new releases — Marvel, Pixar, Lucasfilm.* KPI — *plus forty-one percent cold-start uptake.*

The Disney context. When a major film launches on Disney+ — say a new Marvel original or a Pixar feature — there's a *cold-start moment.* The film is in the catalog. The recommendation engine has no behavioural data on it yet (because nobody's watched it yet). *The first twenty-four hours are critical.* If the launch finds its audience quickly, it builds momentum. If it doesn't, it sits in the catalog uncirculated. *For premium-content launches with hundreds of millions of dollars of investment behind them, the cold-start performance is strategically important.*

The pain point. Generic recommendation engines handle cold-start through *content-similarity-modelling* — *"this new Marvel film is similar to that prior Marvel film, surface it to users who watched that prior Marvel film."* The problem — *not every new film is similar to a prior film.* Sometimes the new film is a genre-bridge — Marvel doing something unusual, Pixar doing an experimental short, Lucasfilm trying a new format. *Generic similarity collapses to bad recommendations for non-similar content.*

The agent strategy. The cold-start agent reasons about *which user cohorts have the highest probability of engaging with this specific new release*, given the release's content fingerprint, the season, the competitive landscape (what else is launching), the marketing context. It then surfaces the release in those cohorts' rails *with prioritised placement* during the launch window.

The architectural shape. Same Silver foundation. The Gold mart adds *content-launch-context* features — release metadata, marketing-campaign context, competitive-launch calendar. MCP tools span subscriber data and content metadata.

The KPI — *plus forty-one percent cold-start uptake* — measured as the percentage of the engagement-target cohort who view the release in the first seventy-two hours, versus the prior generic-similarity baseline.

**RILEY:** And the seller's hook —

**KEVEN:** *"Your cold-start matters most for the most expensive content. The agent reasons about your cohorts the way a senior marketer would — but at the catalog scale.* Wave 1 — pilot on the next two launches. *Show the lift before the third launch."*

### Scenario four — Password-sharing detection & paid-sharing playbook

**KEVEN:** Scenario four. *Password-sharing detection plus the paid-sharing playbook.* KPI — *plus eight million dollars per year* in the reference scenario.

The Disney context. Netflix demonstrated in 2023-2024 that converting password-sharers into paid accounts is *highly revenue-accretive.* Disney has begun implementing similar paid-sharing programs. The challenge — *detecting password-sharing accurately enough to enforce, and gracefully enough to retain.* False positives hurt; they alienate legitimate household users. False negatives leak revenue. The agent reasons about the household-vs-sharing distinction continuously.

The pain point. Naive password-sharing detection — *"if the account is being used in two regions on the same evening, it must be shared"* — produces *too many false positives.* The legitimate-household pattern looks similar to sharing. Travellers, college students, family members in vacation locations — all look like sharing to a naive detector. *The Disney-specific pain* is the brand consequence of false positives. Disney customers are *invested in the relationship.* A wrongful detection that triggers a payment-required prompt is a brand event.

The agent strategy. The password-sharing agent reasons about *probability of paid-sharing-eligibility* per account. It considers IP-pattern stability, device-pattern stability, viewing-pattern composition (kids-and-adults patterns vs. separate-household patterns), geographic-distance over time, and account-history factors. It produces a *recommendation* with a *confidence score.* The marketing-operations team approves or modifies. Approved cases enter the paid-sharing flow with a personalised offer. *Graceful upgrade, not enforcement.*

The architectural shape. Customer-and-loyalty canonical. Gold mart adds per-account behavioural-pattern features. MCP tools retrieve account histories, device-and-IP patterns, viewing patterns. The agent's HITL gate ensures every recommendation is human-approved before the customer sees a flow change.

The KPI — *plus eight million dollars per year* in the reference scenario for a comparable streaming portfolio. At Disney's scale, the number is materially larger; the precise number is in the BVA, not the public materials.

### Scenario five — ESPN auto-highlight detection & clipping

**KEVEN:** Scenario five. *ESPN auto-highlight detection and clipping.* KPI — *minus seventy-four percent production time.*

The Disney context. ESPN produces *enormous* volumes of highlight content. Football games. Basketball games. Baseball games. Soccer matches. Tennis matches. Each game produces hundreds of potential highlight clips — touchdowns, goals, dunks, key moments. Today, ESPN production teams manually identify clip candidates, edit them, package them for various channels (ESPN+, social, partner platforms). *The labour intensity at the per-game level is significant. The labour intensity at the multi-game-per-day, multi-sport level is enormous.*

The pain point. *Production teams can't keep up* with the volume of clip opportunities. ESPN ends up surfacing fewer clips than the audience would consume, simply because production-team capacity is the bottleneck. Meanwhile competitors with leaner production are scaling clip output through automation.

The agent strategy. The auto-highlight agent watches the live game feed. It identifies clip candidates — using game-state signals, play-by-play feeds, audio cues (crowd reaction), and visual cues (vision models trained on highlight patterns). The agent produces *candidate clips* with metadata — the play description, the timestamp, the recommended edit-in / edit-out points, the suggested social caption. *Production teams review and approve* in a much-compressed cycle. *Volume of clips goes up. Production-team time per clip goes way down.*

The architectural shape. Real-Time Intelligence for the live-game stream. Bronze ingestion of play-by-play and live video. Silver for the canonical play-event schema. Gold for per-game highlight-candidate features. MCP tools retrieve game state, play context, and historical clip patterns. The agent recommends clips; production teams sign off.

The KPI — *minus seventy-four percent production time* per clip on the agent-augmented workflow.

**RILEY:** And for ESPN-DTC specifically —

**KEVEN:** ESPN-DTC will demand clip volume at a level ESPN linear didn't need. *The auto-highlight Service is structurally important to making ESPN-DTC operationally viable at scale.* That's the strategic framing for the conversation with ESPN leadership.

### Scenario six — Auto-dub / subtitle for international Disney+ markets

**KEVEN:** Scenario six. *Auto-dub and subtitle generation for international Disney+ markets.* KPI — *minus sixty-two percent localisation time.*

The Disney context. Disney+ operates in over fifty international markets. Each market requires content localised — *dubbed audio in the local language, subtitles, regulatory-required content labels.* Today, localisation is a long-lead, multi-vendor, multi-quality-gate process. *A new film or series often takes weeks to localise into the full set of international languages.*

The pain point. *Time-to-market in international markets lags behind the U.S. launch.* The lag is measurable competitive disadvantage. International subscribers see content months after U.S. subscribers in some cases. Localisation isn't optional — Disney's international subscriber growth depends on doing it well.

The agent strategy. The auto-dub-and-subtitle agent reads the source content, generates draft localised dub audio and subtitle tracks using current speech and language models, identifies quality-gate concerns (regional dialect appropriateness, brand-tone consistency, regulatory language flags), and surfaces for human linguistic-quality review. *The human reviewers focus on edge cases.* The agent does the bulk of the routine localisation. Throughput goes up dramatically. Time-to-international-launch compresses.

The architectural shape. Bronze ingestion of source content audio and metadata. Silver canonical for content-and-localisation schema. Gold for per-content per-market localisation assets. MCP tools span content metadata, regional regulatory rules, prior localisation patterns. The agent emits draft localisation; linguistic experts approve.

The KPI — *minus sixty-two percent localisation time* per asset.

### How the six compose

**RILEY:** And the cross-scenario composition —

**KEVEN:** This is the Disney-specific magic. The six CX scenarios *share architectural foundation.* Same canonical at Silver. Same MCP boundary pattern. Largely the same Bronze ingestion patterns. *The Service-engineering effort for the second scenario is a fraction of the first. The third is a fraction of the second.*

For the Account Team — *the way to position Wave 1 is, "we deliver scenario one in Wave 1, and Wave 2 brings scenarios two and three at incremental cost; by Wave 3, all six are in production."* That sequence is *credible* because the framework's compounding asset thesis is real and Disney's data estate supports it.

### A reading I want to do

**RILEY:** I want to read something from a recent Disney earnings call.

**KEVEN:** Read it.

**RILEY:** [reading, paraphrased]

*"We are investing significantly in technology and AI to enhance the consumer experience across our portfolio. We see opportunities in recommendation, content production, and operational efficiency. We expect these investments to compound over multiple years and to differentiate the Disney consumer experience as the streaming category matures."*

[pause]

**KEVEN:** Note what's *not* in that quote. *Not* a vendor name. *Not* a technology architecture. *Not* a specific number. Disney leadership has stated the *commitment* publicly. The *execution* is what they need partners and platforms for.

**RILEY:** And the partner-and-platform conversation is *exactly* what APEX gives the Account Team to deliver.

### One disagreement

**KEVEN:** Pushback.

**RILEY:** I want to push on the *sequence we just walked.* Six scenarios, in this order — streaming churn, personalisation, cold-start, password-sharing, ESPN highlight, auto-dub. *I think for the actual Account Team motion at Disney, the right Wave-1 entry isn't churn. It's password-sharing.*

**KEVEN:** Why?

**RILEY:** Three reasons. *One — the eight-million-dollar reference KPI is concrete and net-new revenue, not retention.* Disney leadership listens to net-new revenue more than retention. *Two — Netflix has demonstrated the play.* Disney leadership is already aligned that paid-sharing is correct strategy. The framework's job is to *enable execution*, not to make the case. *Three — the password-sharing agent has the highest brand-risk profile, which means it has the highest demand for governance.* That's where APEX's audit-row-and-Purview posture is the most differentiated. Lead with our strongest differentiation.

**KEVEN:** I think you might be right. Churn has more familiar architecture. Password-sharing has more strategic visibility plus more governance differentiation. *Wave 1 = password-sharing detection might be the right entry.* Churn becomes Wave 2.

**RILEY:** Agree.

### What to carry forward

**KEVEN:** Two things.

One — *six CX scenarios, all anchored on the same customer-and-loyalty Silver canonical.* The compounding asset thesis applies; the second scenario is a fraction of the first.

Two — *Wave 1 entry candidate is password-sharing detection,* not churn — because of strategic visibility and the governance-differentiation play.

**RILEY:** Next episode — *The Operations Eight.* Network and infrastructure scenarios across streaming delivery and Parks IoT, plus the Engineering R&D and cyber scenarios. Different from CX — different velocity tiers, different buyer set.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn — relevant for CX scenarios

- **Microsoft Cloud for Media** · Microsoft Learn
- **Azure AI for content** · Microsoft Learn
- **Real-Time Intelligence for streaming events** · Microsoft Fabric Learn
- **Azure Cognitive Services Speech for auto-dub** · Microsoft Learn

### Microsoft Tech Community blogs

- **"Personalisation architectures at streaming scale"** · Microsoft AI Blog
- **"Real-time content delivery on Azure"** · Microsoft Industry Blog
- **"Speech and language for media localisation"** · Microsoft AI Blog

### Industry context

- **MoffettNathanson research on streaming** · proprietary but cited in earnings calls and industry coverage
- **MIDiA Research — streaming benchmarks** · annual reports
- *"Streaming churn dynamics in 2025"* · Variety industry coverage
- *"Cold-start in recommender systems"* · ACM RecSys conference papers
- *"The economics of password sharing"* · 2023-2024 Netflix earnings calls and subsequent industry analysis
- **NAB Show — broadcast technology**
- **SMPTE — Society of Motion Picture and Television Engineers**

### From the APEX Trilogy podcasts

- **Services Podcast Ep 3 — *The Medallion in Depth*** — the Silver canonical concept used here
- **Services Podcast Ep 4 — *The Agent and Its Tools*** — the MCP boundary pattern
- **Services Podcast Ep 5 — *The Retail Margin Squeeze*** — the loyalty churn pattern that maps to streaming churn

---

**End of Episode 02 · The Customer Experience Six**
*≈ 5,800 words · target 30 minutes at conversational pace*
