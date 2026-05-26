# Episode 08 · Identity, Consent, HIPAA & Senior Accessibility

**Episode 08 · Identity, consent, HIPAA & senior accessibility** — six-thirty on a Tuesday evening. Diana drops in on her father Robert. The kitchen speaker is mid-cue, naming his prescription, when the vision kit on the counter sees a second silhouette walk in. The drug name redacts in flight. The cue resumes with a vaguer phrasing. The ledger row records the original cue and the redacted-as-delivered cue side by side. Diana hears the speaker; she does not hear the drug name. Robert says *yes*. We open on the moment four cross-cutting safety layers — Adebayo, Chen, Yamamoto, Russo — all fire at once on a ten-second exchange, and then we walk the substrate that made them compose rather than fight.

**Builds on:** the show bible (00-show-bible-and-format) · Episodes 01–07 · CFMP Mobile Design Document §4.5, §4.7, §8 in full · CFMP Sonos Design Document §4.7, §6.7, §8.1, §8.6, §8.7, §8.9 · CFMP Mobile Identity & Onboarding · CFMP Mobile Entra External ID Provisioning Runbook
**Run time:** ≈ 42 minutes target
**Last updated:** 2026-05-25

---

## Cold Open

[Sound: a kitchen on a Tuesday evening at six-thirty. The hum of a refrigerator settling into its compressor cycle. A kettle on a gas range that has been turned off, the metal still ticking. The shuffle of slippered feet. A small TV in the next room playing a baseball game at the volume that means someone is half-listening. The thump of a screen door easing closed — not slammed, eased — the way a daughter who has been visiting since she was a child closes the door.]

It is six-thirty on a Tuesday evening, and Robert Park is at the counter of his kitchen, holding the day's mail in his left hand and a glass of water in his right. The Era 100 on the shelf beside the toaster — same Ava voice his daughter Sarah hears in her kitchen across town, same household Diana paired into the Sonos cloud eight months ago — has just begun a cue. *Robert, your Lisin—* — and the cue stops mid-syllable. Three-tenths of a second of silence. The Vision AI Kit on the counter, the device with the camera Robert calls *the eye*, has detected a second person entering the kitchen at six-thirty-one and fourteen seconds. The presence service emits the new occupancy count. The drug-name redaction in the Pharmacy specialist's pipeline fires. The cue text rewrites — *Robert, an item is due Friday. Want me to add it to your Friday list?* — and the speaker resumes with the rewritten text, in the same Ava voice, with no audible seam. Robert does not know the cue almost said *Lisinopril*. He hears *an item*. He says *yes*. The cue completes.

Diana has just walked through the kitchen door with a casserole dish in a tote bag — Tuesday-evening drop-in, second one this month, the rhythm she and Robert settled into since her mother passed. She sets the bag on the counter. She hears the last half of the cue — *an item is due Friday* — and she hears her father say *yes*. Twenty seconds later her phone buzzes once. She glances at the notification. *A refill was confirmed for your father.* No drug name. No pharmacy. No dose. The notification is the caregiver-redacted parallel ping the Pharmacy specialist composed at the same moment, routed through the caregiver-share channel Diana opted into at the Preference Center six months ago. She acknowledges with a thumb. She does not ask Robert what the refill was. She knows the refill happened. She does not know which refill. That is the design.

The ledger row records both halves. *Composed text — Robert, your Lisinopril is due Friday.* *Delivered text — Robert, an item is due Friday.* *Suppression reason — presence_count_change, hipaa_gate.* *Caregiver parallel ping — Diana — redacted.* The trace identifier is shared across the originating Pharmacy compose, the redacted Sonos cue, and the caregiver mobile ping. Six weeks from now, if a regulator asks the same question Episode Two opened on, the answer will be on the screen in three minutes.

[Sound: a coffee shop, gentle ambient. The cold-open vignette closes. Keven and Reid open the episode.]

**KEVEN:** I want to start there. Six-thirty on a Tuesday. The cue that started saying *Lisinopril* and finished saying *an item*. The buzz in Diana's back pocket twenty seconds later. The ledger row recording the cue that was almost said and the cue that was actually said.

**REID:** And the moment turns on four cross-cutting layers firing on the same ten seconds. Adebayo on the consent that made the caregiver-share channel exist. Chen on the drug-name gating that rewrote the cue mid-sentence. Yamamoto on the senior-zone defaults that made the Era 100 the surface Robert hears at all. Russo on the channel field that recorded *sonos_cloud* in the ledger row, not *mobile_airplay*, because the cue was high-risk and the bridge was not allowed. Four experts. Ten seconds. One audit chain. The trust substrate IS the architecture today.

**KEVEN:** Welcome back to the CFMP Podcast. Episode Eight. *Identity, consent, HIPAA, and senior accessibility.* In Episode Six we walked the speaker channel as ambient. Today we walk the substrate beneath the speaker. The four-identity chain. The consent gradient. The HIPAA gating. The senior-accessibility defaults. The AirPlay-channel audit tagging that names the bridge as a feature *and* a known-blindspot in the same ledger row.

**REID:** Six sub-sections. A reading, a disagreement, three carries. Let's go.

---

> **Cold-open admission:** the scenario you just heard — Diana drops in, the kitchen Sonos cue rewrites mid-syllable from *Lisinopril* to *an item* — depends on three things that **do not exist in the live system today**: a Pharmacy specialist agent, a Vision-Kit presence-detection signal wired into the cue-composition path, and a drug-name-redaction substrate in `compose_cues`. As of 2026-05-25 the live agent fleet has four specialists (catalog · wayfinder · auto_replenish · concierge) — no Pharmacy. The cold open describes the **design**; the sprint roadmap is where it becomes code. The architectural commitments below — the four-identity chain, the consent gradient, the audit chain — are honest, with the live state called out per item in the honesty header.

## What ships today vs. what's planned

> **Episode honesty calibration · 2026-05-25**
> This episode covers the four-identity chain, the consent gradient, the HIPAA gating substrate, the senior-accessibility defaults, and the AirPlay-channel audit-tagging discipline. The podcast walks the architecture as designed. Phase 1 live, Phase 2 planned, and v2 vision are distinguished below so the listener (and the seller) walks in knowing the score. The CFMP Capabilities Map at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` is the authoritative live-state source.

**Phase 1 live (today):** HITL greater-than-or-equal-to-fifty-dollar cart-add gate, LedgerRow in-memory, `auth_mock.py` (mock identity), audit chain partial, trace_id propagation, Preference Center concept (dietary-prefs chips visible).

**Phase 1 partial / in-progress:** four-identity chain (concept partial; full chain depends on Entra swap), consent gradient (preferences chips exist; full gradient is design), audit chain Bronze/Silver/Gold (Bronze partial).

**Phase 2+ planned (not live today):** Entra External ID (`auth_entra.py` swap — currently `auth_mock.py`), HIPAA presence-gating (depends on Pharmacy spec plus vision presence), drug-name redaction, caregiver delegation flow, WORM ledger to OneLake Delta, live Purview lineage upload.

---

## The conversation

### Identity — the four-identity chain

**KEVEN:** Start with identity. Every other layer is conditioned on identity — consent is consent of whom to whom, HIPAA is HIPAA-of-whom, accessibility is accessibility-for-whom. If identity is fuzzy, the rest is a marketing diagram.

**REID:** Walk the chain.

**KEVEN:** Four identities, all distinct, all traceable. *One — customer.* Robert. His member number is `KP-2089-44531`, bound to his customer profile from his phone-OTP at T1, bound to his WebAuthn passkey at T2, bound to his Sonos household via the OAuth grant he and Diana walked through eight months ago. The Sonos household record carries his member number, his default zone, his consent-recorded-at timestamp. The cue addresses Robert by name because the cue knows Robert is the audience.

*Two — operator.* Priya from Episode Five's cold open. Deloitte-staffed in v1; retailer-tenant role inside the Portal's multi-tenant scaffold in v2. Priya owns an *operator* credential — federated through Entra workforce, scoped to customer-operations, with corporate-IP allowlist on the Container Apps ingress. When Priya opens Robert's trace at seven-fifteen, the Portal logs her as the *viewer*, not the *actor*. The audit chain distinguishes the operator who looked from the customer who acted.

*Three — source-system.* The pharmacy partner's system-of-record. The pharmacy holds the prescription; the CFMP Pharmacy specialist receives a refill-window signal — *Lisinopril, ten milligrams, refill due Friday* — through an MCP boundary, with the source-system identity tagged on the call. The ledger row records the source. If a regulator asks *where did the system get the drug name*, the answer is on the row — *source-system: pharmacy-partner, record-id: Rx-77831*. The drug name did not come from a hallucination. The system of record is named.

*Four — auditor.* The regulator from Episode Two. A read-only identity in the Portal, scoped to the audit-export surface, federated through the customer's Entra tenant or through a Deloitte Independence-side federation depending on the engagement. When the auditor opens the trace, the Portal logs the access. The audit substrate audits its own auditors. Adebayo's discipline, made structural.

**REID:** And the property the chain has to hold.

**KEVEN:** *Each identity is independently revocable, independently auditable, and never compounded into a master credential.* Robert can revoke Diana's caregiver-share without revoking his member number. The operator credential rotates without disturbing the customer. The source-system rotates on the pharmacy's schedule. The auditor is per-engagement, time-bound. *No single credential opens all four doors.*

**REID:** And Entra continuity.

**KEVEN:** The Acceleration Framework's *Identity Continuity* principle realized on Microsoft. The customer identity lives in Entra External ID — the CIAM tenant the Provisioning Runbook walks through, phone-OTP at the verification ceremony, member number minted CFMP-side, session token issued by the orchestrator. The operator identity lives in the customer's Entra workforce tenant. The auditor identity lives in Entra B2B — guest user, time-bound. The source-system OAuth client federates *to* Entra for outbound consent. *Four identity surfaces, one platform, one continuity story.*

**REID:** And here I press. Where does the chain break in v1?

**KEVEN:** Honest answer. *In v1, the source-system identity for the pharmacy partner is a manually-rotated OAuth client credential, not yet federated through Entra B2B.* The credential lives in Key Vault, rotated manually on a ninety-day schedule, with the rotation event logged. The audit chain records the source-system correctly — the row says *source-system: pharmacy-partner* — but the underlying credential is not yet on the same federation rails as the other three. That gap is named, on the roadmap, closed in v2.

**REID:** Named gap. Aspired in v1, enforced in v2, recorded honestly. Move to consent.

### Consent — the consent gradient

**KEVEN:** Consent tells us *what they have agreed to*. Read Adebayo first.

**REID:** *"Speech is data. A voice in a household is observation. Every speaker bound to a member requires recorded consent and a kill-switch in Preference Center."* Adebayo, verbatim, Sonos Section Eight-Point-One.

**KEVEN:** Four classes of consent, each separately scoped, each separately revocable.

*Data consent.* The customer agrees that CFMP can store data — lots, profile, dietary flags, household composition, shopping history. The consent given at T1 phone-OTP, with the Privacy Notice published before the sign-in lands. Revocable only by erasure — UC-108, biometric-gated for T2, phone-OTP-gated for T1. Erasure is the nuclear option. Data consent is the bottom of the gradient.

*Voice consent.* The customer agrees that CFMP can speak in the household. The OAuth grant the customer walks through to bind a Sonos household to her member number. The consent record lives in `sonos_consent_log` — append-only, sealed into the audit substrate. Revoked in the Preference Center by tapping *disconnect Sonos*. Disconnecting Sonos stops the speaker; it does not erase the member. Fully revocable, separately from data.

*Presence consent.* The customer agrees that CFMP can observe the household — the Vision Kit on the counter, the *who-is-here* signal the drug-name redaction depends on. Recorded when the customer enables the Vision Kit, with a separate prompt explaining purpose, data path, retention. Separately revocable. A customer who keeps voice and disables presence keeps the speaker but loses drug-name gating — *which means drug names are no longer spoken at all*, because the gate cannot verify single-occupancy. The system fails safe. The audit row records *presence_consent_disabled*.

*Caregiver-share consent.* The most subtle. The customer agrees that another member can receive parallel awareness. Diana's caregiver-share. Bi-directional: Robert grants, Diana accepts. Either party can revoke at any time; revocation is mutual-immediate. If Robert revokes, Diana's pings stop. If Diana revokes — *I do not want to know about my father's refills* — Robert's grant stays, the routing stops, Robert is notified. The only consent class requiring two parties to record, because the caregiver has her own autonomy.

**REID:** And the OAuth consent surface from Sonos Section Four-Point-Seven.

**KEVEN:** Every Sonos household is bound one-to-one to a member number. The OAuth flow goes through the Sonos consent screen — Sonos shows the customer *CFMP is requesting access to your household speakers, with these capabilities, with this revocation surface*. The Sonos consent screen is the vendor surface; the Preference Center is the CFMP surface; both have to exist, both have to be revocable independently. The customer upset about a cue she did not want to hear can revoke in either place; she finds *a* surface and the consent revokes.

**REID:** And here I press. How does the design handle a customer revoking voice consent mid-trip? Sarah, in the store, hands full, three cues queued. She taps *disconnect Sonos*. What happens to the cues already mid-flight?

**KEVEN:** *Revocation is immediate at the Cue Bus middleware, not at the speaker.* The moment the tap posts to the orchestrator, the voice-consent gate flips for that member. Cues composed but not yet handed to Sonos cloud are marked *suppressed* with reason `voice_consent_revoked`. Cues already handed to Sonos cloud but not yet played — the WebSocket directive is in flight — cannot be unsent at the speaker layer, but the resilient path from Episode Six can be cancelled. The Portal mirror records *cue composed, not spoken, voice consent revoked*. Mendez's no-silent-side-effects rule applies. The customer who cares can see the row.

**REID:** And the edge — the cue that does play because the speaker had it before revocation propagated.

**KEVEN:** The row records *delivered before revocation*, with millisecond-level timestamps showing the race. Truth, not marketing. *The system raced; the speaker won by two-hundred milliseconds; the cue played; the customer revoked; the row records what happened.* When the design cannot prevent a race, the design records the race honestly.

**REID:** Move to HIPAA.

### HIPAA — Chen's drug-name gating

**KEVEN:** Chen's framing.

**REID:** *"Spoken drug names are HIPAA disclosures. Treat them like text on a chart."* Doctor Mei Lin Chen, Section Eight-Point-Six of the Sonos design. The Mobile companion — *"Prescription data is HIPAA-regulated. Isolate from day one."*

**KEVEN:** Walk the cold open in code.

**REID:** Walk it.

**KEVEN:** Six-thirty. The Pharmacy specialist composes. The compose step calls `trip_audio.compose_cues` — the privacy-aware spoken-content discipline from Sonos Section Six-Point-Seven — and asks `presence.who_is_here(zone)`. The Vision Kit's occupancy signal returns *one person, Robert*. The cue proceeds with the drug name. *Robert, your Lisinopril is due Friday.* TTS synth begins; WAV uploads to blob; Sonos cloud directive fires; the speaker plays. *Robert, your Lisin—*

Six-thirty-one and fourteen seconds. The Vision Kit emits *two people, owner plus unidentified*. The presence service propagates a *presence_changed* event onto the cue bus. The HIPAA gate checks every in-flight cue. The Lisinopril cue is presence-dependent. The middleware fires *recompose*. The presence check returns *more than the owner*. The cue text rewrites to *Robert, an item is due Friday*. The Cue Bus issues *stop-and-replay* to the speaker via the Sonos cloud directive — the AudioClip API supports preemption — and the replay starts from the beginning with the redacted text. Three-tenths of a second total, below the conversational floor; Robert hears a normal pause.

The ledger records *both versions*. Field thirteen — cue text — as *composed* and *delivered*, two separate fields. The Portal shows operators the side-by-side. *Composed — Robert, your Lisinopril is due Friday.* *Delivered — Robert, an item is due Friday.* *Suppression reason — presence_count_change, hipaa_gate.* The system's caution is visible. The audit chain audits the redaction itself.

**REID:** And Diana's parallel ping.

**KEVEN:** Same trace. Same compose. The caregiver-share routing is a *separate channel* in the Cue Bus fan-out. Episode Six's Cue Bus was three channels — primary, resilient, mirror. Today we name a fourth — *caregiver-parallel*. It composes its own cue text from the parent intent, applies its own redaction — the caregiver receives information about the *action*, never the *PHI* — and routes through Web Push to Diana's mobile. The ping reads *a refill was confirmed for your father*. No drug name. No pharmacy. No dose. Chen's rule: *treat drug names like text on a chart.* The chart is Robert's. Diana is on the care team for Robert's life, not for Robert's chart. The architecture honors the distinction.

**REID:** V1 versus v2 scope.

**KEVEN:** *V1 — home only.* Drug names spoken only in the home zone, only when home presence confirms single-occupancy, only when the home Sonos household is the binding. The in-store endcap from Episode Six's cold open does not speak Lisinopril. It speaks coupon-savings, route cues, item-picked — none of them PHI. *V2 — retailer-tenant Pharmacy zones with `purpose='hipaa'`.* The `sonos_zones.purpose` field carries the explicit HIPAA flag. The default zone is `default`; the presence zone is `presence`; the mobile-bridge zone is `mobile-bridge`; `purpose='hipaa'` is reserved for v2 retailer Pharmacy zones — the in-store pharmacy counter, the counseling room, the pickup window — where the speaker speaks the drug name only when the zone is HIPAA-marked and the customer has authenticated at the counter. *HIPAA zones are explicit, not inferred.*

**REID:** And the storage layer.

**KEVEN:** Prescription data lives in a *separate Postgres tenancy* from operational data. Chen's discipline. The Pharmacy specialist queries a different database than the Trips specialist queries for lots. The HIPAA-isolated database has its own service principal, its own audit log, its own backup retention. The MCP boundary fronting the prescription record carries `tenancy='hipaa'` on every read. *The customer's drug record never sits in the same row as the customer's grocery list.* The architecture honors the difference at the storage layer, not just at the cue layer.

**REID:** Compose-time redaction at the cue layer. Tenancy isolation at the storage layer. Both. Move to senior accessibility.

### Senior accessibility — Yamamoto's framing

**KEVEN:** Yamamoto's line.

**REID:** *"For the highest-LTV segment, the speaker isn't a feature. It's the entire interface."* Robert Yamamoto, Sonos Section Eight-Point-Seven. The Mobile companion — *"Older shoppers are the highest-LTV grocery segment."*

**KEVEN:** The 65+ segment lives on the speaker the way the 35-year-old segment lives on the phone. Robert's surface is the speaker, with the phone as the occasional escalation. The design owes the senior segment defaults that recognize that. Read the defaults.

**REID:** *Default volume plus four decibels for users 65+.* *Default cadence slower — one-hundred-thirty words per minute, not one-forty-five.* *Quiet hours default starts later — twenty-two-hundred, not twenty-one-thirty — seniors stay up later than the design assumed.* *Trip cues mode "verbose" — full route announcements, not abbreviations.*

**KEVEN:** Each default defends a property the segment loses if it is set wrong. *Plus four decibels* — Hassan's hearing-safety ceiling is seventy-five decibels absolute; sixty-four at one meter stays well below but lands meaningfully above the default sixty. The cue is audible with the refrigerator running and the baseball game in the next room. *One-thirty words per minute* — Chowdhury's default is one-forty-five; one-thirty is paced for the listener who needs the cue to *land* before the next word arrives. *Quiet hours at twenty-two-hundred* — Yamamoto's hard-won correction. The original twenty-one-thirty was the median household; the senior cohort surfaced the gap — *I am not asleep at nine-thirty, I am reading, I might still want a cue.* The cohort retains an override to push further. *Verbose trip cues* — Sarah's segment hears *aisle three, beverages*; Robert's segment hears *next stop is aisle three, that's the beverages aisle, two aisles down from where you are now*. The verbose mode meets Robert's orientation where it already is. Informative, not condescending — the design pays explicit attention to the line.

**REID:** And the Mobile side.

**KEVEN:** Larger touch targets — fifty-six pixel minimum on Home and Lots for 65+, up from forty-four. Higher default font size — one-twenty percent on every text surface, with override to one-fifty or two-hundred. Voice-over compatibility — every interactive surface has an accessible name, a role, a state; the assistive-tech audit runs every release. Simpler journey flows — the *Simple Mode* toggle from UC-204 through UC-209. *Voice-call OTP fallback* — UC-209 — for the customer who does not have a smartphone, the OTP arrives as a voice call, not SMS, digits spoken slowly, confirmed once. *The customer who does not text gets through onboarding anyway.* The architecture refuses to assume the smartphone is universal.

**REID:** And here I push. Yamamoto's framing is for the highest-LTV segment. The discipline generalizes. Name it.

**KEVEN:** *Accessibility is the design quality test for everyone.* The defaults the senior segment needs — louder cue, slower cadence, verbose route, larger touch target — are the defaults *everyone* benefits from when the conditions match. Sarah at six-twenty-eight on a Saturday with her hands wet on a colander is, in that moment, indistinguishable from Robert at six-thirty on a Tuesday with the day's mail in his left hand — both customers are hands-not-free, attention-half-engaged, audio-as-the-primary-channel. The senior defaults are general-case defaults under the right conditions. Disability is contextual as often as it is permanent. The senior cohort is the design's most demanding accessibility-research input; everyone benefits.

**REID:** The senior cohort is the design quality test for everyone. Move to AirPlay audit-tagging.

### AirPlay channel audit-tagging — Russo's catch

**KEVEN:** Russo's line.

**REID:** *"AirPlay bypasses every server-side audit you have. Tag the channel explicitly."* Tamara Russo, Sonos Section Eight-Point-Nine.

**KEVEN:** Russo's catch is the one the architecture would have missed without her.

**REID:** Walk it.

**KEVEN:** Episode Six walked the AirPlay-bridge as the universal escape hatch — the Tuesday-demo property, thirty-second first-cue, no-OAuth-required path. The bridge is a *feature*. It is also a *blind spot*. Sonos cloud — the autonomous transport — sees every cue, logs every directive, fires the webhook, signs the LedgerRow with `channel: sonos_cloud`. AirPlay — the resilient transport — is invisible to the server. The phone fetches the WAV from blob; iOS AirPlay 2 routes the audio to the Roam; the Roam plays. *The server does not know the Roam played it.* The server knows the WAV was fetched; it does not know the audio came out of the Roam versus the phone's own speaker. The audit substrate cannot, by construction, see the AirPlay leg.

Russo's catch — *if the architecture pretends the AirPlay leg is the same as the Sonos cloud leg, the audit chain has a hole the regulator will eventually find.* The honest move is to *name the hole on every row*. The Speech LedgerRow's `channel` field is *mandatory*, with `mobile_airplay` as a *first-class value* — same status as `sonos_cloud`, `mobile_local`, `portal_mirror`. Every row carries the channel.

**REID:** And the phone's self-report.

**KEVEN:** The mobile is required to report its AirPlay state. iOS's `navigator.audioSession` surfaces the routing — *Bluetooth, AirPlay receiver, device speaker*. The PWA reads the state and posts it back with every cue completion. The audit row records *audio_route_reported: airplay_receiver*. The phone cannot prove the AirPlay receiver was the Roam; the phone cannot prove a Bluetooth speaker did not snake in; *but the phone reports what it knows*. The honesty is layered.

**REID:** And the high-risk-cue gate.

**KEVEN:** *For high-risk cues — alerts, refills, payment — only the Sonos-cloud path is allowed.* If the cloud path fails for a high-risk cue, the AirPlay path is *not* tried. The cue is suppressed with a banner — *alert was suppressed: speaker not on direct channel*. The audit substrate records *cue_suppressed, reason: high_risk_path_unavailable*. The system tells the customer *I did not say what I would have said, and here is why*. The customer can re-trigger; the operator can phone-confirm; the regulator can audit the suppression.

**REID:** Why suppression instead of degraded fallback.

**KEVEN:** Because *the wrong audience hearing a high-risk cue is worse than the right audience missing it*. The AirPlay path cannot prove the audience. The receiver could be the household Roam, a Bluetooth speaker an overnight guest brought, a CarPlay system the phone forgot to disconnect from. The Sonos cloud path can prove the audience — the household is bound to the member, the zone is registered, the speaker is the speaker the customer consented to. For a coupon cue, the proof does not matter. For a refill cue — a drug name about to be spoken in someone else's house — the proof is load-bearing. The architecture refuses to speak high-risk cues on a channel it cannot prove.

This is the line I want sellers to carry. *The bridge is a feature AND a known-blindspot, named explicitly in the ledger row.* Not *the bridge is a feature, the audit gap is hidden*. Not *the bridge is a workaround, we will fix it later*. The bridge is a *first-class transport* with a known audit gap — both claims compose. The gap is *on every row*. Six weeks from now, when the regulator asks why a particular refill cue did not play, the row shows *cue suppressed because the bridge was the only path and the bridge is not allowed for high-risk cues*. The regulator does not have to discover the gap; the architecture surfaces it. *Auditability is what makes a known-blindspot survivable.*

**REID:** Tag the channel. Carry that. Move to synthesis.

### The four cross-cutting safety layers — recap and synthesis

**KEVEN:** The four layers, each mapped to a cue or screen the listener has heard about. *Adebayo on consent* — four classes, all recorded, all revocable. Data class at T1 onboarding. Voice class at the Sonos OAuth grant. Presence class at the Vision Kit enable. Caregiver-share class at Robert-grants-Diana-accepts. *Chen on HIPAA* — drug names gated by presence at compose time, isolated tenancy at storage, caregiver redaction by-design. The cue rewrites mid-syllable when presence changes. The prescription record never sits in the same row as the grocery list. Diana's ping reads *a refill was confirmed*, never *Lisinopril*. *Yamamoto on senior accessibility* — defaults that recognize the 65+ cohort lives on the speaker as the entire interface. Volume plus four decibels, cadence one-thirty, quiet hours at twenty-two-hundred, verbose trip cues, larger touch targets, voice-call OTP. *Russo on the channel audit-tag* — `channel` field mandatory, the bridge is a known-blindspot named explicitly, high-risk cues refuse the bridge. Four experts. Four disciplines. One audit chain.

**REID:** The unifying claim.

**KEVEN:** *The trust substrate IS the architecture, not an afterthought.* Identity, consent, HIPAA, accessibility are first-class architecture decisions — encoded in the cue object's fields, encoded in the ledger row's mandatory channel, encoded in the Postgres tenancy isolation, encoded in the Preference Center's class-separated toggles. The team did not bolt safety on after the speaker shipped; the team designed the speaker *around* safety. The cold open's three-tenths-of-a-second silent rewrite is not a feature added in version three. It is the substrate the team designed in version zero.

**REID:** Every layer is a test, not a promise.

**KEVEN:** The marketing language for safety is *promise* — *we promise to protect your data; we promise to honor your consent; we promise to safeguard prescription information.* Promises do not survive an audit. Promises do not survive a regulator. *Tests* survive. The presence check is a test. The consent gate is a test. The high-risk gate is a test. The senior-default bundle is a test. Every test is a row. Every row is auditable. Every audit is replayable. The substrate is the architecture; the architecture is the trust.

**REID:** That is the bar. Defended by the design, not by the marketing. Carry it.

### A reading I want to do

**REID:** A reading. Two threads tonight, because the substrate sits at a rich intersection.

**KEVEN:** Take the HIPAA side.

**REID:** The reading I keep coming back to is the *HHS Office for Civil Rights guidance on HIPAA and AI* — the bulletins issued through twenty-twenty-four and twenty-twenty-five, especially the guidance on the *minimum necessary* standard when AI systems handle protected health information. The guidance formalizes a principle the design has been treating as load-bearing without naming the source. *The minimum necessary information for the recipient.* Diana receives *a refill was confirmed*; that is the minimum necessary for a caregiver to know the care moment happened. Robert receives the drug name; that is the minimum necessary for the customer to act. The bystander in the kitchen receives *an item*; that is the minimum necessary for a non-recipient. The OCR guidance, read alongside the *Right to Access* enforcement actions from the same period, gives the design a third-party-validated line for *why* the cue rewrites. Not because Chen says so; because the standard says so, and Chen designed the system to the standard. The bulletins are public. Engineers building HIPAA-touching agent systems in twenty-twenty-six should keep the HHS OCR bulletin index open in a browser tab.

**KEVEN:** And the senior-UX thread.

**REID:** Two sources. *AARP's annual technology-adoption studies* — the *Tech Trends and the 50-Plus* report is the single best longitudinal data set on what older adults actually do with smartphones, speakers, wearables. The twenty-twenty-five report's chapter on smart speakers is what Yamamoto's defaults are calibrated against — the time-of-day usage curves, the volume preferences, the *what the speaker is allowed to say in front of which household members* survey responses. The AARP data is the defensible source. *Nielsen Norman Group on accessibility* — Sarah Gibbons's articles and the *Web Accessibility for Older Users* guideline — is the practitioner-side companion. NN/g's discipline is that accessibility tests for *temporary, situational, and permanent* disabilities; the senior segment's defaults benefit the hands-full Sarah and the hands-wet Sarah for the same reasons they benefit Robert. The pairing is — *AARP for the cohort data, NN/g for the design principles.*

**KEVEN:** HHS OCR for HIPAA. AARP and NN/g for senior UX. Three threads, all defensible.

### One disagreement

**REID:** The cleanest tension the substrate has is between Yamamoto and Adebayo. The seam between the senior-accessibility defaults and the household-privacy defaults.

**KEVEN:** Put it on tape.

**REID:** Yamamoto. *Bump the default volume plus four decibels for users 65+ and start quiet hours later — twenty-two-hundred as the default for the 65+ segment.* The data is the AARP cohort research and Yamamoto's own ethnography. The senior cohort is harder of hearing, stays up later, finds the median defaults *too quiet, too early*. The defaults the design ships should match the cohort it serves.

Adebayo. *A higher default volume plus later quiet hours is a louder system in someone else's house.* Robert lives in a townhouse. The wall between his kitchen and the neighbor's bedroom is drywall and a stud cavity; at sixty-four decibels at one meter, a refill cue at twenty-two-fifteen is audible in the neighbor's bedroom. Robert's spouse in the master bedroom goes to bed at nine-thirty. A caregiver staying overnight in the guest room did not choose the couch. The senior-accessibility defaults raise the volume *for the listener Yamamoto is optimizing for* — and raise the cost for *every other person in the household and the neighboring household*. Privacy is at stake — whose speech in whose ears. Household-noise is at stake — whose sleep in whose room. The cohort is not the only stakeholder; the cohabitants are stakeholders too.

**REID:** Where do they converge?

**KEVEN:** *Per-zone overrides.*

**REID:** Walk it.

**KEVEN:** *Senior zones — kitchen, master bedroom — get the louder defaults and the twenty-two-hundred quiet-hours start.* These are zones the senior cohort lives in. Yamamoto's defaults apply.

*Public zones — living room when guests detected, dining when household-plus-one detected — get the quieter defaults and the twenty-one-hundred quiet-hours start.* When the Vision Kit detects more than the household in the living room, the public-zone defaults take over. The volume drops to sixty decibels. Quiet hours start at twenty-one-hundred; cues defer to morning briefing. Adebayo's discipline applies.

The `sonos_zones` table's `purpose` field — `default`, `presence`, `mobile-bridge`, `hipaa` — extends to *senior* and *public* as additional values, each with its own bundle. *The zone is the resolution unit for the disagreement.* The household is not one cohort; the household is several cohorts in several rooms. The defaults respect the rooms.

**REID:** And the Preference Center.

**KEVEN:** Both defaults are surfaced per-zone, with the customer's override on every value. Robert sees the kitchen bundle and the living-room bundle and the master-bedroom bundle, each editable, with the senior default pre-populated, with the *why this default* explanation inline. *The kitchen volume is set to sixty-four decibels because you are in the 65+ segment; adjust lower if your spouse sleeps light.* Every override is audit-recorded.

**REID:** Convergence accepted. *Per-zone overrides, customer-editable, audit-recorded.* Carry it.

### What to carry forward

**KEVEN:** Three things into Episode Nine. Numbered.

**KEVEN:** *One — the trust substrate IS the architecture.* Identity, consent, HIPAA, accessibility are first-class architecture decisions, encoded in the cue object's fields, in the ledger row's mandatory channel, in the Postgres tenancy isolation, in the Preference Center's class-separated toggles. Not bolted on. Adebayo on consent, Chen on HIPAA, Yamamoto on accessibility, Russo on the channel audit-tag — four cross-cutting layers, one audit chain. Every layer is a *test*, not a *promise*. Carry that.

**KEVEN:** *Two — the Preference Center is the customer's kill switch.* Every consent class — data, voice, presence, caregiver-share — revocable in one place. Every redaction rule visible. Every senior-default override editable per-zone. Every audit row carries the trace identifier the customer can replay. The customer's autonomy lives at one URL the customer remembers, and that URL composes through Entra so the customer's identity in M365 is the same identity that signs into the Preference Center. Not a hidden setting. A first-class surface. Carry that.

**KEVEN:** *Three — tag the channel.* AirPlay is a feature; the bridge is a feature; the bridge is *also* a known-blindspot, named explicitly in the ledger row's channel field. `sonos_cloud`, `mobile_airplay`, `mobile_local`, `portal_mirror`, `caregiver_parallel` — each a first-class value, each on every row. High-risk cues refuse the bridge. The architecture prefers silence-the-customer-can-audit to speech-the-substrate-cannot-verify. The seller carries the line — *the bridge is a feature AND a known-blindspot, named explicitly* — and the listener trusts the architecture more, not less, because the gap is on the row. The live architecture page at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` carries the channel-tagging in the audit chain panel; open it on a client call when the question comes up. Carry that.

**REID:** Three carries. The trust substrate IS the architecture. The Preference Center is the kill switch. Tag the channel. Into Episode Nine.

**KEVEN:** Next episode — *the seller's playbook. CFMP on APEX-M.* The architectural pitch, the six discovery openers, the honest claims and the overclaims, the pushback handling, the roadmap, the close. Seven episodes land in the field, with a script the Account Team carries into the Monday-morning client call. Today we walked the safety substrate that makes the speaker deployable in a senior's kitchen. Next episode we walk the substrate that makes the architecture sellable in a Microsoft seller's account-plan.

[Sound: the closing sting. ~6 seconds.]

---

## Further reading

- **Source docs**
  - CFMP Mobile Design Document — `C:\code\iot_device\docs\packs\CFMP-Mobile-Design-Document.md` — §4.5 (Three-tier Identity), §4.7 (Consent Gradient), §4.8 (APEX Audit Chain), §8 in full (cross-cutting quality layers — Adebayo §8.1, Chen §8.8, Yamamoto §8.12, Liu §8.13, Security trio §8.16). Identity, consent, HIPAA, senior, and security disciplines as the architectural layer beneath every other section of the design.
  - CFMP Sonos Design Document — `C:\code\iot_device\docs\packs\CFMP-Sonos-Design-Document.md` — §4.7 (Household Tenancy), §4.8 (Speech LedgerRow), §6.7 (Privacy-aware spoken content), §8 in full (Sonos quality layers — Adebayo §8.1, Chen §8.6, Yamamoto §8.7, Russo §8.9). The speaker-channel specializations of the four cross-cutting disciplines this episode walks end to end.
  - CFMP Mobile Identity & Onboarding — `C:\code\iot_device\docs\packs\CFMP-Mobile-Identity-Onboarding.md` — the three-tier identity model (T0 anonymous, T1 phone-OTP, T2 WebAuthn passkey), member-number resolution rules, identity propagation through the stack. The customer-identity surface of the four-identity chain.
  - CFMP Mobile Entra External ID Provisioning Runbook — `C:\code\iot_device\docs\packs\CFMP-Mobile-Entra-Provisioning-Runbook.md` — the step-by-step provisioning of the Entra External ID tenant for CFMP, the SignUpOrSignIn user flow, phone-OTP verification, app registration. The identity-continuity realization on Microsoft for the customer surface.
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — the Entra column on the identity row carries the four-identity surface from the v1 customer-and-operator pair through the v2 retailer-tenant and auditor extensions. The Sonos cloud integration on the external column carries the OAuth grant for voice consent. The Postgres tier carries the HIPAA-isolated tenancy for the Pharmacy specialist and the `sonos_zones.purpose` field for the senior, public, and HIPAA zones. The audit chain panel carries the mandatory channel field with `sonos_cloud`, `mobile_airplay`, `mobile_local`, `portal_mirror`, and `caregiver_parallel` as the first-class values. Open it on every client call where identity, consent, HIPAA, or accessibility is on the agenda.
- **Microsoft Learn**
  - Microsoft Purview — `https://learn.microsoft.com/purview/` — the productized governance, compliance, and data-classification surface the customer's M365 tenant most likely already owns. The four-identity chain's auditability composes through Purview's audit logs.
  - DSPM for AI — `https://learn.microsoft.com/purview/ai-microsoft-purview` — Microsoft's Data Security Posture Management for AI products, including the AI Hub for prompt-and-response classification, sensitivity-label propagation onto generated content, and the audit-log integration with Purview.
  - Microsoft Entra — `https://learn.microsoft.com/entra/` — the identity platform the customer, operator, source-system, and auditor surfaces federate through. Entra External ID for the CIAM customer surface; Entra workforce for the operator; Entra B2B for auditor and source-system.
  - Responsible AI in AI Foundry — `https://learn.microsoft.com/azure/ai-foundry/responsible-ai/` — the productized responsible-AI surface hosting the content-safety classifier, prompt-injection defense, structured-output validators, refusal training.
- **Standards**
  - HHS HIPAA enforcement guidance — `https://www.hhs.gov/hipaa/for-professionals/index.html` — the HHS Office for Civil Rights bulletin index, including the AI-and-HIPAA guidance, the minimum-necessary standard, the Right to Access enforcement actions. Chen's discipline is calibrated against this.
  - EU AI Act — the European Union's risk-tiered AI regulation, with high-risk-AI obligations that govern healthcare-adjacent agent systems. The Pharmacy specialist's risk classification under the Act is the substrate the v2 retailer-tenant Pharmacy zones inherit.
  - NIST AI Risk Management Framework — `https://www.nist.gov/itl/ai-risk-management-framework` — the United States' voluntary risk-management framework for AI systems, mapping to the *govern, map, measure, manage* functions. CFMP's cross-cutting safety layers map cleanly to NIST AI RMF's measure-and-manage discipline; the audit chain is the measurement substrate.
- **Industry / research**
  - Nielsen Norman Group on accessibility — Sarah Gibbons's articles and the *Web Accessibility for Older Users* guideline are the practitioner-side companion to Yamamoto's framing. The principle that accessibility tests for temporary, situational, and permanent disabilities — the principle that makes the senior defaults general-case defaults under the right conditions.
  - AARP technology-adoption studies — the annual *Tech Trends and the 50-Plus* report is the longitudinal data source the senior-accessibility defaults are calibrated against. The smart-speaker chapter from the twenty-twenty-five report is the source Yamamoto's volume, cadence, and quiet-hours defaults derive from.
- **Sibling series cross-reference** — Cross-Cloud Agentic Episode 04 — *Governance, Identity & Safety* — the framework-level treatment of identity continuity, consent gradients, and audit-substrate disciplines across AWS, Google Cloud, and Microsoft. The Acceleration Framework principle this episode realizes on Microsoft.

— end of episode 08 — Episode 09 (the seller's playbook) closes the series —
