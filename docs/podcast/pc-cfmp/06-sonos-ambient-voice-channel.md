# Episode 06 · Sonos · The Ambient Voice Channel

**Episode 06 · Sonos · the ambient voice channel** — Sarah's hands are full, the kid's backpack in one, the soccer cleats in the other, and the speaker on the endcap of aisle three says her name without her ever opening the app. That evening, her daughter asks what's for dinner and Sarah answers the kitchen, not the phone. We open on those two moments. Then we walk why a speaker is an architecture move and not a feature, what the Cue is, what the Cue Bus is, why the Cue Bus is fault-tolerant to its own primary transport, the cadence law that keeps the speaker calm, the AirPlay-bridge fallback that makes the Tuesday demo work behind any venue Wi-Fi, and the Azure-native deployment posture that ships the whole channel without a single laptop on the floor.

**Builds on:** the show bible (00-show-bible-and-format) · Episode 01 (Sarah's Day) · Episode 02 (Agent fleet & audit chain) · Episode 03 (Mobile · SCAN & LOT) · Episode 04 (Mobile · Trips, Replenish, and the home channel) · Episode 05 (Portal · operator console and B2B multi-tenant) · CFMP Sonos Design Document §§1–10 in full · CFMP Sonos UC Catalog · CFMP Sonos Roadmap
**Run time:** ≈ 42 minutes target
**Last updated:** 2026-05-25

---

## Cold Open

[Sound: a Saturday afternoon in a grocery store. The low brushing hiss of a refrigerated case venting. A cart wheel slightly out of true. A child's voice three aisles over asking for something and being told *not today*. The faint over-PA hum of a song that was new in twenty-eighteen and is now wallpaper. A scanner beeping twice at the register. Footsteps on polished concrete — a parent's footsteps, deliberate, not stopping.]

It is two minutes past three on a Saturday afternoon, and Sarah Chen is walking through the retailer's store with both hands full. Left hand — her eight-year-old's backpack, the strap looped around her wrist. Right hand — the older child's soccer cleats, knotted at the laces, still gritty from a tournament that ended ninety minutes ago. Her phone is in her back pocket. The phone holds the trip — twelve items, three already picked, the rest in a route the Trips specialist composed on the way over — and the phone is going to stay in that pocket until she gets to the register.

She passes aisle three. The endcap has a small speaker on it — a Sonos device, paired into her household's Sonos cloud from a thirty-second setup she did from the kitchen counter on a Sunday morning two weeks ago. She does not see the speaker as a CFMP device. She sees a speaker. The speaker, in a calm voice that sounds like a person she might know — not a synthesizer, a voice — says her name. *"Sarah, you saved a dollar fifty on the Coke. Next stop, aisle three, Beverages."* She does not break stride. She does not pull the phone. She turns left and walks to aisle three. The cleats swing at her side. The speaker has done its job. The phone, in her back pocket, has held the trip's state through the whole exchange.

Six hours later. Six twenty-eight on a Saturday evening. Sarah's eleven-year-old daughter, on a stool at the kitchen island with a half-done piece of homework, asks, with the bored sing-song of a child who has asked this question every night of her life, what is for dinner. Sarah is at the sink rinsing a colander of cherry tomatoes. She does not open the app. She says, to the Era 100 on the counter beside the toaster — the same household, the same voice she heard on the endcap — *"plan tomorrow's dinner, kid-friendly, peanut-free."* Twelve seconds pass. The speaker reads back, in the same calm voice, a plan — *chicken thighs with rice and the green beans you have in the fridge; nothing in the plan has peanuts.* Sarah does not touch glass. Her hands stay wet. She says *good* and the speaker confirms and the row goes to the ledger.

[Sound: a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start on both moments. The endcap at three-oh-two with both her hands full. The kitchen at six-twenty-eight over a colander of cherry tomatoes. Because the speaker channel is what those two moments rest on, and the speaker channel is not a feature. The speaker channel is an architectural move.

**REID:** And the move turns on a property the design earns explicitly. *Screens demand attention; speakers don't.* The line from Section One. The phone keeps the state; the speaker keeps the conversation. The phone was the system of record. The speaker was the system of presence. Two surfaces, one trace, one substrate. Today we walk why that distinction is load-bearing for the whole CFMP architecture, not a polish concern.

**KEVEN:** Welcome back to the CFMP Podcast. Episode Six. *Sonos · the ambient voice channel.* In Episode Four we named the home channel. In Episode Five we walked the Portal chat panel as the visual mirror of every cue the system ever spoke. Today we open the speaker channel up. Seven sub-sections. Why a speaker, not just a phone. Voice as a peer channel. The Cue, the WAV, the Sonos play. The Cue Bus. Zones and the cadence law. The AirPlay-bridge fallback. And the Azure-native deployment that lets the whole thing run without a single piece of hardware at the customer's house beyond the speaker the customer already owns.

**REID:** A reading, a disagreement, three carries. Let's go.

---

## The conversation

### Why a speaker, not just a phone

**KEVEN:** Start with the architectural question, not the product question. Because the design's commitment to voice-as-a-peer-channel is the thing the cold open's two moments rest on. Walk it.

**REID:** Walk it.

**KEVEN:** *Screens demand attention; speakers don't.* The design's first-principle line. The screen is a *foreground* surface — the customer who is on the screen has stopped doing whatever else, reached for the device, unlocked it, opened the app, put her eyes on the glass. In Sarah's two moments, that cost is unavailable. At three-oh-two on a Saturday with her hands full, she cannot stop. At six-twenty-eight with her hands wet and a child asking, she will not stop. The screen-only channel concedes both moments.

The speaker is an *ambient* surface. It meets the customer where she already is — in the store with her hands full, in the kitchen with her hands wet, in the car, at the cabin. The speaker offers information at the speaker volume of a radio. The customer who is listening hears it; the customer who is not listening misses it; the cue completes, the row seals, the moment ages. *A screen demands the customer; a speaker meets the customer.*

**REID:** And here I press. Because a lot of teams ship a speaker as a *feature* — *the app also has voice* — and get the worst of both surfaces. A voice that only works if the phone is in the room, only speaks when the app is foregrounded, asks the customer to look at the screen anyway. Sonos as a feature is a tax. Defend why CFMP's Sonos is not a feature.

**KEVEN:** Because the Sonos in CFMP is not the app's voice. The Sonos in CFMP is *a peer channel of the same agent fleet.* That sentence is the architecture move. The orchestrator does not know or care which surface produced the request. The Trips specialist composing a coupon-savings cue does not know whether the cue is going to render on Sarah's phone, on the Era 100 in her kitchen, on the endcap on aisle three, or on three at once. The specialist composes a *moment*. The Cue Bus renders it across the channels where Sarah is reachable. The speaker is not a render of the app; the speaker is a render of the *answer*.

**REID:** And the consequence of being a peer.

**KEVEN:** The consequence is that the speaker can carry the *whole conversation* when the conversation is one the speaker is the right channel for. The dinner-planning at six-twenty-eight — Sarah's *"plan tomorrow's dinner, kid-friendly, peanut-free"* — composed at the speaker, processed by the orchestrator, decomposed to the Trips specialist with a sub-call to Pharmacy for the peanut-allergen check, rendered back at the speaker. Twelve seconds, ear in to ear out, no glass touched. The conversation lives on the speaker because the speaker is a *first-class* channel, not a notification surface. Same property at the endcap — the cue is not a push notification Sarah opens her phone to read; the cue *is* the message.

**REID:** And the Roam. The persona that follows the household across zones.

**KEVEN:** The Roam follows the household out of the home. Kitchen is the daily; the endcap is the in-flight; the cabin Roam is the *traveling* version of the home channel. Marcus pulls into the cabin, the Roam is already paired to his phone via AirPlay, and the same Ava voice he hears in his kitchen tells him *welcome to the cabin, your groceries are in the fridge.* The speaker is *a channel*, not *a device*. The device is just the present rendering of the channel.

**REID:** Said cleanly. Move to the peer-channel mechanics.

### Voice as a peer channel

**KEVEN:** The peer-channel mechanics. Mobile, Portal, and Sonos are peers of the same agent fleet. Read the orchestrator's posture explicitly, because the posture is what makes the channel-as-peer claim true.

**REID:** Read it.

**KEVEN:** The orchestrator emits a *response object*. Not a *channel-specific message.* The response — the structured answer the parent and the specialists compose — is *channel-agnostic*. Each channel decides how to render. The mobile renders a chat bubble plus a card plus a `speak[]` array. The portal renders the same plus a system-message mirror. The Sonos renders a cue object — text, chime, voice, zone — and a `play_audioClip` call. *The orchestrator does not author for the channel. The channel renders the orchestrator's answer.*

**REID:** And Maya Chen's line, from Section Four-Point-One.

**KEVEN:** Maya Chen, from the shopper experts panel. *"If you treat voice as a render mode of the same answer, you don't double-write your agent. You write good answers, then choose how to say them."* The discipline is that the agent fleet writes *answers*, not *messages*. If the team falls into the trap of authoring two messages — one for the screen, one for the speaker — they are now maintaining two intent-resolution surfaces, two prompt libraries, two regression suites, two audit shapes. Within six months the voices drift; the customer hears the inconsistency; trust drops. The peer-channel discipline *prevents* the drift. One answer, three renders.

**REID:** And the consequence for the fleet.

**KEVEN:** The fleet is cheaper to operate because the answer is the unit of work. One coupon match — *dollar-fifty Coca-Cola coupon applied* — renders three ways. The mobile bubble. The Sonos cue. The Portal mirror. One LedgerRow the regulator can replay six weeks later. The cost discipline and the audit discipline collapse into one. Most agentic stacks today author per-channel — chatbot for the web, different prompt for push, third for the speaker if they have one. CFMP composed the discipline up front. *One agent fleet, one answer per intent, multiple renders.* Carry that into the Cue.

### The Cue, the WAV, the Sonos play

**KEVEN:** The Cue. Because the Cue is the noun that does the work in the speaker channel. The Cue is the JSON object. The WAV is its render. The Sonos play is its delivery. Walk the JSON.

**REID:** Walk it.

**KEVEN:** The Cue object from Section Four-Point-Two. Ten fields. *Id* — unique identifier for the cue. *Trace id* — inherited from the parent intent; every cue is reachable by the same trace ID Episode Two opened. *Text* — the exact words the speaker will say. *You just saved a dollar fifty with the Coca-Cola coupon.* Vargas's rule from Section Six-Point-Six — names not codes, *a dollar fifty* not *dollar sign one period five zero*, *Friday at two* not *fourteen-hundred hours*. *Voice* — the Azure Speech voice ID. *En-US-AvaMultilingualNeural* for default; *en-US-AndrewNeural* for alerts; never anything else. *Chime* — the four-chime library from Section Six-Point-Two. *Ding* for item-picked, *coupon* for savings, *route* for next-stop, *done* for trip-complete, *alert* for safety. *Priority* — *normal* or *alert*. Priority enforces the cadence law and gates the Andrew override and the volume ceiling.

*Lot ref* — the lot the cue belongs to. Episode Three's lot model is the spine. The audit row is reachable through the lot's audit tree. *Expires at* — the cue has a TTL. A coupon cue at three-oh-two is not useful at three-oh-eight; expired cues are suppressed rather than delivered late, and the row records the suppression. *Ducks music* — boolean. If the speaker is playing music, the cue requests the native Sonos *dialog priority high* ducking from Section Six-Point-Five. *Household zone* — kitchen, dining, mobile-bridge, car. The Concierge dispatcher resolves the zone before the cue is composed. *Audit hash* — the sha256 anchor the cue's row will seal with.

**REID:** And here I press. Ten fields is a lot. Voice is almost always Ava. Chime is almost always *ding*. Zone is almost always the default. Priority is almost always *normal*. Why are these on the cue instead of defaults applied at delivery?

**KEVEN:** Conceded the defaults could fill at delivery. Defend why they live on the cue. *Each field defends a property the cue would lose if it were inferred.* The voice field defends the *one-voice rule* — if it's on the cue, the audit verifies the Andrew voice was used exactly when priority required it. If voice is inferred at delivery, the audit can only prove delivery, not that the right voice was used. The chime field defends Patel's *chimes carry brand* property — the chime is part of the cue's content, not its envelope. The priority field defends the cadence law and the volume policy — alert cues have a higher ceiling, get Andrew, get the alert chime, never queue to morning briefing.

The zone field defends the privacy gating. The drug-name presence check from Section Six-Point-Seven asks *who is in this zone* before letting the cue speak. If zone is inferred at delivery, the privacy decision has to back out the composition; putting it on the cue means privacy gating happens at composition time. The ducks-music field is consent-bound — some cues duck, some never duck because the music is worth more than the cue. The cue declares its own contract. And the audit-hash is non-negotiable; the cue is an audit row in the making.

**REID:** Ten fields, each defended. Move to the Cue Bus.

### The Cue Bus

**KEVEN:** The Cue Bus. The Cue Bus is the server-side abstraction that takes a composed Cue and fans it out to the channels that can deliver it. Three channels. Primary, resilient, mirror. Walk the fan-out.

**REID:** Walk it.

**KEVEN:** A server event fires. *Mark picked.* Sarah's mobile has just posted that she picked the Coca-Cola twelve-pack. `shopping trips dot mark picked` completes; `refresh totals` runs; the coupon match returns a dollar-fifty coupon. `Trip audio dot compose cues` runs against the diff and produces a list of Cue objects — pick confirmation, coupon cue, and a route cue. Each gets handed to the Cue Bus.

The Cue Bus does three things, in parallel.

*One.* The *primary path.* Azure Speech synthesizes the cue text into a WAV; the WAV uploads to the `audio-out` container on the `stapexdemo50097` storage account with a fifteen-minute SAS URL; the orchestrator calls Sonos Cloud Control at `control.api.sonos.com`, passing the SAS URL, the volume, and the dialog-priority. Sonos cloud sends the play directive over its persistent WebSocket to the household's Roam or Era 100. The speaker fetches the WAV from blob over the *household's* Wi-Fi and plays it. Completion comes back via webhook. A LedgerRow seals with `channel: sonos_cloud`.

*Two.* The *resilient path.* In parallel — not serially — the Cue Bus appends the cue to the `speak[]` array on the mobile API response. The mobile is already getting a response to its `mark picked` POST; the cue rides along. The mobile fetches the WAV via the SAS URL and plays it. If the phone is AirPlay-connected to a Roam, audio routes there. If not, the phone is the speaker. A LedgerRow seals with `channel: mobile_airplay` or `channel: mobile_local`.

*Three.* The *mirror path.* In parallel, the Cue Bus pushes the cue text and metadata to the Portal SSE channel as a system message. The chat panel for the trace renders *spoken on kitchen — you just saved a dollar fifty with the Coca-Cola coupon.* The mirror does not deliver audio; the mirror records that the cue was composed and the audio was delivered. Mendez's rule from Section Six-Point-Nine — *never silent side effects.*

**REID:** And the property that makes the Cue Bus architecturally distinctive. *Fault-tolerant to its own primary transport.* Name it.

**KEVEN:** Naming it. *The primary and resilient paths fire in parallel, and the first to land on the speaker wins.* If Sonos cloud returns a five-oh-three on a Saturday afternoon — Sonos cloud is an external dependency, it has its own SREs and its own bad days — the primary path fails. The cue still arrives at the speaker because the resilient path is the mobile fetching the WAV directly and AirPlaying it to the same Roam. The customer experiences *cue plays on time*. The audit row records both attempts. Conversely, if the customer's phone is closed in a back pocket — the resilient path is degraded — the primary path lands the cue via Sonos cloud directly. Both paths fire; first to land wins. The losing path is *recorded as attempted* but does not double-speak — the cue's `id` is a deduplication anchor and the playback webhook closes the cue ID before the loser can deliver.

This is what I want sellers to understand. The architecture's resilience is not redundancy — two of the same thing, sized to take over. The resilience is *path diversity* — two architecturally different transports with different failure modes, racing. Sonos cloud is the *autonomous* transport — the cue arrives even when the phone is in a back pocket. Mobile-AirPlay is the *resilient* transport — the cue arrives even when Sonos cloud is degraded. The transports do not share failure modes. The probability of both failing for the same cue at the same moment is the product of two small numbers. The architecture pays for path diversity in implementation complexity and two audit rows per attempt. It gets back a delivery substrate dramatically more robust than either path alone.

**REID:** And the move generalizes. *Path diversity beats redundancy at the application layer for any architecture that crosses an external dependency.* The Cue Bus is the *pattern*, not just the implementation. Carry that. Move to zones and cadence.

### Zones, the cadence law, and the one-voice rule

**KEVEN:** Zones first. Because the zone is the property the Cue Bus is targeting when it composes the cue's `household_zone` field, and the zone is what makes the same household reachable from the kitchen, from the dining room, from the car, from the cabin. Walk the zone model.

**REID:** Walk it.

**KEVEN:** A household has zones. Section Four-Point-Four lists them — *kitchen*, *dining*, *mobile-bridge*, *car*. The kitchen zone is the Era 100 on the counter. The dining zone is the Roam on the table. The mobile-bridge zone is a Roam paired to Sarah's iPhone via AirPlay. The car zone is iPhone CarPlay, no Sonos at all. Four zones, one household, one persona. The Concierge dispatcher resolves zone by signal — camera presence routes to kitchen, phone location to car, a wake word to the speaker that heard it, an in-flight trip cue to mobile-bridge. If no signal is dispositive, the cue routes to the household's default zone.

**REID:** And the cadence law. Zones solve *where to speak*; cadence solves *when*. Read Chowdhury's rules from Section Six-Point-Three.

**KEVEN:** Reading them. *No more than one cue per six seconds.* Hassan's voice-fatigue threshold — speak more often and the speaker stops being calm and starts being insistent. *Coupon cue follows item-picked by one-point-five seconds.* Reyes-Garcia — separate the dopamine from the confirmation. *Route cue waits two seconds after item-picked.* Park-Johnson — don't dogpile direction onto confirmation. *Concierge cues defer to in-flight trip cues.* Sharma — never interrupt a Trip cue with a by-the-way. *Quiet hours — only alerts speak; after 9pm local, others queue to morning briefing.* Adebayo's night-owl tolerance and Yamamoto's senior override. The cadence law is *enforced* in the `cue_bus` middleware. A cue that violates cadence is queued; a cue queued past `expires_at` is suppressed with `ok: false`, `suppression_reason: cadence_violation`. Every suppression is auditable.

**REID:** And the one-voice rule. Cadence is *temporal* discipline; one-voice is *brand* discipline.

**KEVEN:** *One voice, one CFMP.* Section Six-Point-One. *Ava* — `en-US-AvaMultilingualNeural` — is the default. Friendly, clear, one hundred forty-five words per minute, the same person across kitchen, dining, mobile-bridge, car. The same person Sarah heard on the endcap and at her Era 100. *Andrew* — `en-US-AndrewNeural` — is the alert voice. Used only for the alert priority class. Hassan's distinct-voice-for-safety-class rule — when the listener hears Andrew, the listener should know without thinking *this is the alert voice*. Chowdhury, verbatim from Section Four-Point-Five: *"Two voices is the maximum. One default, one alert. Three voices and users stop noticing what the voice change means."*

**REID:** And the most defensible line. The one that earns the speaker its calm.

**KEVEN:** Chowdhury, verbatim: *"The cue you almost said is usually the cue you should have skipped."* The discipline that turns the speaker from an always-on-always-responding surface into a quiet-when-it-should-be surface. The cue the team almost composed but pulled back from is *usually* the right call. The cadence law is the *enforcement*; Chowdhury's posture is the *discipline* the law inherits. *The speaker's job is to know when not to speak.* The speaker that earns trust will be listened to when it speaks. The speaker that does not earn trust gets ignored within two weeks. Ambient presence requires earned silence.

**REID:** And the volume policy. Briefly.

**KEVEN:** Section Six-Point-Four. Default sixty decibels at one meter. Night mode drops to fifty-two after twenty-one-thirty. Seniors override to sixty-four — Yamamoto. Alert capped at seventy. Absolute ceiling at seventy-two, enforced server-side in `cue_bus` *and* verified by Sonos cloud via the household's max-volume safety setting. The hearing-safety NFR — zero cues over seventy-five decibels, zero cues that wake a sleeping household member after nine PM — is the success metric. The volume policy plus the cadence law plus quiet hours plus one-voice plus ducking — five disciplines together — are what make the speaker ambient and not insistent. Drop any one and the speaker becomes an Alexa.

**REID:** Five disciplines, one ambient property. Move to the AirPlay-bridge.

### The AirPlay-bridge fallback

**KEVEN:** The AirPlay-bridge fallback. Because the bridge is the property that makes the Tuesday demo work at any venue with a phone and a Roam, and the bridge is the property that gets a new customer from *just bought a Sonos* to *first cue plays* in thirty seconds without any account-linking step. Walk the bridge.

**REID:** Walk it.

**KEVEN:** The setup, from Section Five-Point-Three. The customer has a Sonos Roam, a phone, the PWA installed. The phone is on the same Wi-Fi as the Roam. In iOS Control Center, the customer taps the AirPlay button and selects the Roam. iOS's AirPlay 2 stack routes the phone's audio output to the Roam. The CFMP PWA is already fetching cue WAVs from `/api/agent/tts` and playing them through the phone's audio output. The phone's audio output is now the Roam. The cue plays on the Roam. The orchestrator was not involved in the bridging step. The audit row records `channel: mobile_airplay`; the Sonos itself is invisible to the server. *Zero new server endpoints. No LAN bridge. No Sonos Cloud OAuth required at the demo site.*

**REID:** And the Tuesday-demo path from Section Three-Point-Four.

**KEVEN:** The presenter walks into a venue thirty minutes before a demo. The venue's Wi-Fi has unknown egress posture. The venue may block outbound to `control.api.sonos.com` — many enterprise networks block large categories of consumer endpoints. The Sonos developer account may not be approved for the demo household. The presenter pairs the phone to the Roam via iOS Control Center. One tap. The audience sees the phone showing the Trip view, no Sonos toggle visible. The audience hears cues and chimes coming from the Roam on the table. The presenter never says *the phone is bridging*. The audience cannot tell the orchestrator-to-Sonos path is not direct. *The illusion is the deliverable.* The demo works whether or not the venue blocks Sonos cloud, whether or not the developer account is approved.

**REID:** And why this is *the universal escape hatch*, not a workaround. Defend it.

**KEVEN:** The bridge is not a workaround because the bridge is *not* a degraded path. The cue rendered through the bridge is the same cue. Same WAV bytes from the same Azure Speech. Same chime. Same voice. Same text. Actually slightly better latency, because the WAV goes from blob to phone to Roam over the same LAN instead of through the Sonos cloud round trip. The customer cannot tell which path delivered the cue.

The bridge is universal because *every venue with a phone and a Roam can run CFMP-Sonos in thirty seconds.* The customer who buys a Roam Friday at five PM, plugs it in, opens the PWA, taps AirPlay, selects the Roam — has CFMP-Sonos at five-oh-three. No developer account. No OAuth flow. No *please complete your Sonos household setup*. The Sonos cloud channel onboards over the following days, adding the autonomous-delivery property — the cue that arrives when the phone is closed. But the bridge gets the customer from zero to first cue at consumer-product speed.

**REID:** And the architectural consequence.

**KEVEN:** *The Sonos cloud OAuth flow is no longer on the critical path for the first user experience.* OAuth is on the critical path for the *autonomous* experience. It is not on the critical path for the *demonstrated value* experience. Most architectures depending on third-party OAuth do not have this property. CFMP-Sonos has it because the bridge is *engineered as a peer transport*, not as a polyfill. It is in the design at Section Five-Point-Three; it is in the Cue Bus fan-out; it is in the audit row's channel field as a first-class value. The bridge is *the design*, not a fallback to it.

**REID:** Tuesday demo works. Friday first-cue works. Cloud onboards additively. Move to the deployment.

### Azure-native deployment

**KEVEN:** Azure-native deployment. Section Five-Point-One of the design document. The win, in the design's words — *the Sonos talks to Azure over its own internet connection. The orchestrator never touches the venue LAN. There is no laptop. There is no Beelink. There is no Tailscale tunnel.* Walk the deployment.

**REID:** Walk it. Because this is the bit Episode Two opened on the architecture page, and the Sonos channel inherits the topology unchanged.

**KEVEN:** Walking it. The orchestrator is `ca-visionkit-orchestrator` — Azure Container Apps in East US 2, the deployment Episode Five walked end to end. The orchestrator hosts Trips, Replenish, Coupons, Pharmacy, Concierge, plus the new Sonos modules — `trip_audio.py`, `cue_bus.py`, `sonos_cloud.py`, `speech.py`. The orchestrator calls Azure Speech for the TTS — `en-US-AvaMultilingualNeural` for default, `en-US-AndrewNeural` for alerts — and streams the WAV bytes straight to blob.

The blob is `stapexdemo50097`, container `audio-out`. Every cue's WAV uploads with a fifteen-minute SAS URL. Fifteen minutes is the design's compromise between *short enough that the SAS is not a long-lived credential* and *long enough that a slow household Wi-Fi can still fetch the WAV before expiry*. The lifecycle policy purges WAVs at twenty-four hours — the bump is for audit replay, per Adebayo's Section Eight-Point-One.

The Sonos cloud call goes out of `ca-visionkit-orchestrator` over the public internet from East US 2 to `control.api.sonos.com`. The orchestrator presents a bearer token from the customer's OAuth grant. The token is encrypted at rest in Postgres on `sonos_households` — `oauth_refresh_token_enc` and `oauth_access_token_enc` as `bytea` columns with keys in Key Vault. Sonos cloud receives the `play_audioClip` directive, dispatches it over the household's WebSocket to the Roam or Era 100, and the speaker fetches the WAV from the SAS URL over the customer's home Wi-Fi. *The orchestrator is never on the customer's LAN.* The speaker is never directly addressed by the orchestrator.

The Postgres tier is the Flexible Server Episode Two named. The Sonos schema from Section Five-Point-Five is three tables — `sonos_households`, `sonos_zones`, `sonos_consent_log`. Household carries OAuth tokens, default zone, quiet-hours window, voice override, consent-recorded-at. Zones map Sonos group IDs to human-readable names and a purpose flag — `default`, `presence`, `mobile-bridge`, `hipaa`. The consent log is append-only, sealed into the audit substrate. *Speech is data* — Adebayo's line — and a voice in a household is observation.

**REID:** And the live page.

**KEVEN:** `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture`. Open it on a client call. Sonos cloud is on the page as the external integration column on the right — `control.api.sonos.com`, with the line from the orchestrator out, the OAuth bearer marker, the return path through the customer's home Wi-Fi. Azure Speech is in the data row. Blob `stapexdemo50097` is alongside it with the fifteen-minute SAS annotation. Postgres carries the schema additions. *The whole Sonos channel renders as one external integration plus three named cells in the existing data row.* No new infrastructure. That is the v0.2 posture from Section Five-Point-One. *No laptop, no LAN bridge, no Beelink.* The cloud orchestrator drives the speaker through Sonos Cloud Control; phone-as-AirPlay is the zero-config fallback.

**REID:** The seller's argument lands because the deployment lands. The customer's Sonos already exists; the customer's home Wi-Fi already exists; the orchestrator is the existing CFMP deployment. The Sonos channel is *additive*. Other speaker integrations require a hub, a bridge, an appliance. CFMP-Sonos requires the customer to tap *connect Sonos* in the Preference Center. Three taps. Done.

**KEVEN:** Move to the reading.

### A reading I want to do

**REID:** A reading. Two short ones, because the Sonos channel sits at a rich intersection — ambient computing *and* conversational UI. Mark Weiser's *The Computer for the 21st Century* is the obvious one, and we already mentioned it in Episode Four when we named the home channel — the kitchen-radio metaphor. Weiser's nineteen-ninety-one *Scientific American* piece is the original source for *the best computers are the ones that fade into the background*. The Sonos channel is taking that discipline seriously at the *audio* layer, not the screen layer, which is where most of Weiser's followers have stayed for three decades. We noted it before; we will not re-walk it.

**KEVEN:** And the second reading.

**REID:** *Cathy Pearl, Designing Voice User Interfaces.* O'Reilly, twenty-sixteen. Pearl was at Sensely and then at Google. The book is the practitioner canonical text on conversational UI — cadence, persona, recoverability, the *what-to-do-when-the-customer-interrupts* question. Pearl's framework names three properties every voice interface has to earn — *recognition* the listener can detect the system is speaking and from where; *recoverability* the listener can interrupt, correct, back out; *trust* the listener believes the system will not embarrass them in front of someone in the room. The CFMP Sonos channel pays each explicitly. Recognition through the chime library — Patel's five-cap unmistakable-in-two-hundred-milliseconds rule. Recoverability through the barge-in spec — any phone tap stops playback within five hundred milliseconds, the mobile cancels and sends a stop directive to Sonos cloud. Trust through the privacy-aware content rules — drug names gated by presence, dollar amounts gated to default zone, addresses never on a shared zone. Pearl's framework is the lineage the Section Six discipline inherits.

The pairing — *Weiser on the principle, Pearl on the practice*. Engineers building voice interfaces in twenty-twenty-six know Weiser by name; very few have read Pearl. Read Pearl.

**KEVEN:** Pearl is the book. The Nielsen Norman Group's published work — Raluca Budiu's articles and the NN/g webinars on conversational design — is the practitioner-discourse layer worth following alongside. Move to the disagreement.

### One disagreement

**REID:** One disagreement. The cleanest tension the Sonos channel has — Chowdhury versus Mendez. Both quoted earlier in the episode. The tension lives at the seam between the cadence law and the silent-side-effects rule. Put it on tape.

**KEVEN:** Put it on tape.

**REID:** Chowdhury's law. *"The cue you almost said is usually the cue you should have skipped."* The speaker that earns trust by knowing when not to speak. When in doubt, do not speak. The skipped cue is, in Chowdhury's read, *usually* the right call. Chowdhury's law is what makes the speaker *ambient*.

Mendez's rule. *"No silent side effects."* Section Six-Point-Nine, the design's auditability discipline. The portal mirror exists because of this rule. If the system did something, the customer or the operator must be able to *see that the system did it*. The system that takes silent action loses trust; the system whose actions are visible can be defended, audited, contested, reversed. Mendez's commitment is *legibility* — the architecture's actions are always readable somewhere.

Now press the tension. *If the cue is suppressed — Chowdhury — but the action happened, does Mendez's rule mean the cue must still surface visually in the Portal chat panel?* If Chowdhury says *the cue was borderline, the cadence middleware suppressed it before it spoke*, is there a Mendez obligation to show the operator the cue that was *almost* spoken? Or is the speaker's silence its own legitimate answer?

**KEVEN:** Both lines are right. The convergence distinguishes the *channel decision* from the *trace decision*.

**REID:** Bring it.

**KEVEN:** *Every cue mirrors visually in the chat panel, always. The question is when to skip the speaker, not when to skip the trace.* The Sonos channel can suppress audio — the cue was composed, the cadence law decided it was the cue Chowdhury says you usually skip, the speaker stayed silent, the customer heard nothing. The visual mirror *never* suppresses. The Portal chat panel shows the cue text with a system tag — *composed, not spoken, reason: cadence_violation* — and the operator sees the cue that was almost said. The LedgerRow records both halves. *The cue was composed. The speaker was muted.* The Compliance team can audit whether the suppression policy is over-aggressive; the seller can answer *why didn't the speaker say anything* by pointing to the row.

Chowdhury's law applies to the *audio render*. Mendez's rule applies to the *trace*. The same cue can be muted at the speaker and visible in the mirror at the same time. The disciplines apply at different layers — cadence at the render, audit at the trace.

**REID:** And the failure mode if the convergence breaks.

**KEVEN:** If the cadence law suppresses the cue *and* the mirror suppresses the cue, the system has taken a silent action — the agent composed something to say and decided not to say it — and no one but the cadence middleware knows. Compliance cannot audit; the operator cannot answer the customer's question; the seller cannot defend the silence. The system has crossed from *ambient* into *opaque* — and ambient becomes opaque the moment the system's silence is unauditable. The convergence prevents that. *Skip the audio; keep the trace.* The speaker can be calm and the system still legible.

**REID:** Converge accepted. *Chowdhury at the audio render; Mendez at the trace.* Carry it.

### What to carry forward

**KEVEN:** Three things into Episode Seven. Numbered, because the listener carries them.

**KEVEN:** *One — the speaker is ambient, not insistent.* Cadence law plus ducking plus quiet hours plus one-voice rule plus volume policy. Five disciplines, one ambient property. *Screens demand attention; speakers don't.* The Sonos channel is Weiser at the audio layer — the best computer is the one that fades into the background. Carry that.

**KEVEN:** *Two — the Cue Bus is fault-tolerant to its own primary transport.* Sonos cloud is the autonomous path; mobile-AirPlay is the resilient path; the Portal mirror is the visual proof. All three fire; first to land wins. The architecture's resilience is path diversity, not redundancy — two architecturally different transports with different failure modes, racing. The Cue Bus is the pattern; the discipline applies anywhere the system crosses an external dependency. Carry that.

**KEVEN:** *Three — one voice, one CFMP.* Ava is the default. Andrew is the alert voice. *Two voices is the maximum.* The chime library is five-capped, each chime unmistakable in two hundred milliseconds. One household, one persona, every zone. The customer who hears Ava on the Era 100 at six-twenty-eight on a Saturday evening hears the same Ava on the endcap the next Saturday at three-oh-two. Three voices and the trust dilutes. Carry that.

**REID:** Three carries. Ambient not insistent. Cue Bus fault-tolerant to its own primary transport. One voice, one CFMP. Into Episode Seven.

**KEVEN:** Next episode — *Identity, consent, HIPAA, and senior accessibility.* The four-identity chain finally walked end to end. Adebayo on consent at the OAuth grant boundary. Chen on the HIPAA-isolated pharmacy tenancy. Yamamoto on the senior-accessibility overrides that make the speaker the *radio that knows them*. Russo on the AirPlay-channel audit tagging. Today we walked the speaker as ambient; next episode we walk the safety substrate that makes the speaker deployable in a senior's kitchen.

[Sound: the closing sting. ~6 seconds.]

---

## Further reading

- **Source docs**
  - CFMP Sonos Design Document — `C:\code\iot_device\docs\packs\CFMP-Sonos-Design-Document.md` — full, end to end. Part 1 (the customer's problem and the speaker vision); Part 2 (personas and the household tenancy); Part 3 (the five end-to-end journeys including Sarah's hands-full grocery walk, Robert's evening Rx refill, Marcus's cabin StayLot, the Tuesday demo, the graceful failure recovery); Part 4 (the eight core concepts stair-stepped — Voice Channel as a peer, the Audio Cue, the Cue Bus, the Zone, the Voice Persona, Ducking, Household Tenancy, the Speech LedgerRow); Part 5 (the Azure-native architecture, the Sonos Cloud Control flow, the AirPlay-bridge fallback, the file-level structure, the schema additions); Part 6 (voice, chime library, cadence rules, volume policy, ducking spec, spoken text style guide, privacy-aware content, voice-in asymmetry, visual mirror); Part 7 (the 24-UC catalog summary, the 10 must-ship critical-path UCs, UC-S04 in full Cockburn); Part 8 (the cross-cutting quality layers — Adebayo, Hassan, Okafor, Tanaka, Chowdhury, Chen, Yamamoto, Liu, Russo); Part 9 (the 6-sprint plan and the 38-item decision queue); Part 10 (glossary, contributor cast).
  - CFMP Sonos UC Catalog — `C:\code\iot_device\docs\packs\CFMP-Sonos-UC-Catalog.md` — all 24 Sonos-channel UCs in Cockburn format. UC-S01 through UC-S06 (Trip audio cues), UC-S07 through UC-S10 (Concierge and Pharmacy), UC-S11 through UC-S14 (StayLot and multi-zone), UC-S15 through UC-S16 (AirPlay-bridge), UC-S17 through UC-S18 (resilience), UC-S19 through UC-S22 (OAuth, consent, quiet hours), UC-S23 through UC-S24 (voice-in and barge-in).
  - CFMP Sonos Roadmap — `C:\code\iot_device\docs\packs\CFMP-Sonos-Roadmap.md` — the 6-sprint execution layer over the design and UC catalog. Sprint -1 (developer-account application, voice persona decision, demo dry-run); S0 (OAuth, schema, ledger, AirPlay-bridge); S1 (Trip audio cues); S2 (Concierge plus Pharmacy with HIPAA gates); S3 (multi-zone plus StayLot); S4 (voice-in plus wake word); S5 (polish plus telemetry).
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — the hero artifact this episode anchors its deployment claims to. The Sonos cloud is the external integration column on the right; Azure Speech is in the data and identity row producing the WAVs; Blob `stapexdemo50097` `audio-out` is alongside it as the audio artifact tier with 15-minute SAS URLs; the Postgres state store carries the `sonos_households`, `sonos_zones`, and `sonos_consent_log` tables from Section Five-Point-Five; the `ca-visionkit-orchestrator` Container Apps deployment hosts the `trip_audio`, `cue_bus`, `sonos_cloud`, and `speech` modules that compose, fan-out, deliver, and synthesize every cue. Open on every client call.
- **Microsoft Learn**
  - Azure AI Speech — `https://learn.microsoft.com/azure/ai-services/speech-service/` — the productized text-to-speech service the channel's cue WAVs are synthesized from. `en-US-AvaMultilingualNeural` and `en-US-AndrewNeural` are the two voices the design commits to; the neural-voice quality from twenty-twenty-six is what made the speaker-as-associate-in-the-room metaphor land instead of feeling synthesized.
  - Azure Container Apps — `https://learn.microsoft.com/azure/container-apps/` — the platform hosting `ca-visionkit-orchestrator` and the platform Episode Five walked end to end. Revision-based deploy, scale-out by HTTP queue depth, native L7 ingress; the platform the new Sonos modules ship into without any new infrastructure.
  - Azure Blob storage — `https://learn.microsoft.com/azure/storage/blobs/` — the `stapexdemo50097` storage account hosts the `audio-out` container where every cue's WAV lands. SAS URLs are the access pattern; 15-minute TTL is the v0.2 default; 24-hour retention is the audit-replay policy from Adebayo's Section Eight-Point-One.
- **External**
  - Sonos Cloud Control API developer documentation — `https://developer.sonos.com/` — `control.api.sonos.com` is the cloud endpoint the orchestrator calls; `play_audioClip` is the primary call; `dialogPriority: HIGH` is the native ducking lever; household, group, and zone are the addressing primitives.
  - Apple AirPlay 2 platform documentation — the iOS Control Center AirPlay 2 stack is what routes the phone's audio output to the Sonos Roam when the bridge fallback is in use. Section Five-Point-Three of the Sonos design document is the CFMP-side spec.
- **Industry / research**
  - Cathy Pearl, *Designing Voice User Interfaces* (O'Reilly, 2016) — the practitioner-side canonical text on voice-UI design. Recognition, recoverability, and trust as the three properties every voice interface has to earn; the CFMP Sonos channel pays each through the chime library, the barge-in spec, and the privacy-aware spoken content rules respectively.
  - Mark Weiser, *The Computer for the 21st Century* (Scientific American, September 1991) — the original ambient-computing source previously cited in Episode Four. The Sonos channel is what Weiser's discipline looks like applied at the audio layer rather than the screen layer; the cadence law plus the one-voice rule plus the ducking plus the quiet hours are together what earn the ambient property.
  - Nielsen Norman Group on conversational UI design — Raluca Budiu's articles and the NN/g webinars are the contemporary practitioner-discourse layer; the kind of high-density operational reading the team is rewarded for; the engineer building voice interfaces in twenty-twenty-six should follow NN/g alongside Pearl's book.
- **Sibling series cross-reference** — Cross-Cloud Agentic Episode 06 (*The Ambient Channel and Cross-Cloud Voice*) at `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\06-ambient-channel-cross-cloud-voice.md` — the framework-level treatment of voice as a peer channel of an agent fleet, including the AWS Alexa Voice Service and Google Assistant equivalents to Sonos Cloud Control that the CFMP Sonos channel's path-diversity discipline generalizes from.

— end of episode 06 —
