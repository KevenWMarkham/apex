# CFMP Podcast Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Produce a complete 8-episode scripted podcast series on the Customer Focused Merchandise Pack (CFMP) — covering Mobile, Portal, and Sonos surfaces of CFMP on APEX-M — to onboard the project team and equip Deloitte Account Teams.

**Architecture:** One show-bible markdown file defining the recurring format, hosts, and content discipline; then 8 episode-script `.md` files of ~5,000–6,500 words each (approx. 38–42 min spoken). All output to `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cfmp\`, mirroring the structure of the sibling `pc-cross-cloud-agentic` series.

**Tech Stack:** Markdown only (this plan covers scripts; audio production is deferred). Source material in `C:\code\iot_device\docs\packs\`.

**Design doc:** `docs/plans/2026-05-25-cfmp-podcast-design.md`.

---

## Notes for the executor

- Hosts: **Keven** (Microsoft platform practitioner, 22 years on Microsoft, positions CFMP on APEX-M) and **Reid** (cross-cloud principal architect, honesty enforcer). Same character continuity as the Cross-Cloud Agentic series.
- **Recurring Azure deployment thread.** Every episode names the Azure realization of its surface (Container Apps `ca-visionkit-mobile` / `ca-visionkit-portal` / `ca-visionkit-orchestrator` in East US 2, Azure Speech for TTS, Blob `stapexdemo50097/audio-out`, Postgres for the state store, the Sonos Cloud Control API as an external integration). Each episode's `## Further reading` includes a **Live architecture** entry with the canonical URL: `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture`. Episode 2 (Agent fleet & audit chain) anchors the deployment topology; Episode 5 (Portal) features the page as the seller's screen-share artifact.
- Content discipline: generic on-tape — no real retailer names (use "the retailer"); fictional design personas (Sarah, Robert, Diana, Marcus) keep their names; Independence-minded; framework = "the Acceleration Framework", APEX = Microsoft's productized realization; no co-sell / partner / alliance / strategic-partnership vocabulary.
- Episode structure (every episode follows): `# Title` · YAML-ish header (kicker, hosts, runtime, principles) · `## Cold Open` · `## The conversation` with `### ` sub-sections (5–8) · `### A reading I want to do` (Reid) · `### One disagreement` · `### What to carry forward` · `## Further reading` (categorised list of source docs / external references).
- Speaker lines use `**KEVEN:**` and `**REID:**` markers; bracketed stage directions in `[brackets]`; emphasis with `**bold**` sparingly.
- Word target: ~5,000–6,500 spoken words per episode (excluding Further reading). Spoken-only word count (exclude `[stage directions]`, speaker tags, headings).
- Tasks 2–9 each modify a single new file; they can be run in any order after Task 1, but **must be run sequentially** (do not parallelise implementer subagents).

---

## Task 1: Create the show bible

**Files:**
- Create: `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cfmp\00-show-bible-and-format.md`

**Step 1: Write the file**

The show bible defines the recurring patterns every episode follows. It must cover:

- **Series identity** — name ("The CFMP Podcast"), audience (CFMP project team + Deloitte Account Teams), one-line pitch.
- **Hosts** — Keven and Reid character sheets (background, voice, vocabulary patterns, what they push on, the honesty-enforcer dynamic).
- **Episode format** — section structure, expected word count, cadence rules (no dogpiling, single disagreement per episode resolved or named, every episode ends on carry-forward).
- **Cold-open style** — every episode opens with a moment-in-the-day vignette drawn from the design docs (the personas: Sarah's day, Robert's evening, Diana's drop-in, Marcus's cabin trip, or an operator's morning), then the architectural payoff.
- **Content discipline** — the generic / Independence-minded / framework-naming rules above; the forbidden vocabulary list.
- **The eight-episode arc** — restate the titles and one-line themes.
- **Voice cast (deferred audio)** — names the intended voices for future audio production: Andrew Multilingual for Reid, a paired female neural voice for Keven (revisit at audio time); opening/closing sting timing carried from the sibling series; runtime target.
- **Recurring elements** — Reid's "a reading I want to do", "one disagreement", "what to carry forward". Spell out the formula for each.
- **Speaker formatting** — `**KEVEN:**` / `**REID:**`, stage directions in `[brackets]`, no emojis in body text.

Target length: ~1,800–2,400 words.

**Step 2: Verify**

```bash
python -c "
t=open(r'C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cfmp\00-show-bible-and-format.md',encoding='utf-8').read()
for s in ['Keven','Reid','Cold Open','carry forward','Acceleration Framework']:
    assert s.lower() in t.lower(), 'missing '+s
for forbid in ['co-sell','channel partner','strategic partnership']:
    assert forbid.lower() not in t.lower(), 'forbidden '+forbid
print('show bible OK, words:', len(t.split()))
"
```

**Step 3: Commit**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git add docs/podcast/pc-cfmp/00-show-bible-and-format.md
git commit -m "feat: CFMP podcast show bible"
```

---

## Task 2: Episode 01 — Sarah's day · the customer problem CFMP exists to solve

**Files:**
- Create: `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cfmp\01-sarahs-day.md`

**Sources to read first** (`C:\code\iot_device\docs\packs\`):
- `CFMP-Mobile-Design-Document.md` §§ 1 (Why), 2 (Who — five personas), §1.3 (What success looks like).
- `CFMP-Mobile-Shopper-Experts.md` (the five archetypes; Maya Chen quotes).

**Cold Open seed:** Sarah Chen, Sunday morning. Three apps open — loyalty, Instacart, Pinterest. Kids demanding breakfast. The romaine is wilted in the fridge. Keven and Reid open over coffee; Reid: "this is the moment CFMP exists to solve."

**Section beats** (six `### ` sub-sections under `## The conversation`):
1. The shape of Sarah's week — the five frictions (the Sunday triple-app, the Tuesday coupon that won't load, the Wednesday last-minute party list, the Thursday wilted romaine, the Friday remote-care of her mother).
2. The five archetypes — Sarah, Robert, Diana, Marcus, and the fifth shopper (read Shopper-Experts for the fifth's name + identity).
3. The unifying noun — LOT. Why a noun and not a feature. The four lot types (shopping, replenish, stay, care).
4. The headline interaction — SCAN. Why scan-first, not search-first.
5. What success looks like — the three target metrics (from Mobile §1.3) and why each is a behaviour-change signal not a vanity stat.
6. The cross-cutting principle — auditability as the trust substrate; preview of Episode 2.

**Reid's reading** — name a recent piece of design/research on persona-driven product design or jobs-to-be-done.

**The disagreement** — Reid argues "this is just a grocery app dressed up". Keven counters with the auto-replenish + StayLot + identity + audit chain — none of which a grocery app does. They converge: it's a *pack*, not an app, because the surfaces and the audit substrate are the point.

**Carry-forward** — three things: (1) the unifying noun (LOT); (2) the headline interaction (SCAN); (3) why the audit chain is mentioned in episode 1 of a customer-experience podcast.

**Further reading** — the source docs (Mobile §1–2, Shopper-Experts), plus 2–3 external references on persona-driven design / jobs-to-be-done.

**Length target:** ~5,200–6,000 spoken words. Verify ≥ 4,800 and ≤ 7,000.

**Verify + Commit** (template same as Task 1; assert `## Cold Open`, `### A reading I want to do`, `### One disagreement`, `### What to carry forward`, `## Further reading` all present; assert "Sarah", "LOT", "SCAN" appear; assert no forbidden vocabulary). Commit: `feat: CFMP podcast — episode 01 Sarah's day`.

---

## Task 3: Episode 02 — The agent fleet & the APEX audit chain

**Files:**
- Create: `pc-cfmp/02-agent-fleet-and-audit-chain.md`

**Sources:**
- `CFMP-Mobile-Design-Document.md` §§ 4–5 (Core concepts + architecture), §8 (Cross-cutting quality layers — Adebayo on audit).
- `CFMP-Sonos-Design-Document.md` §4.8 (Speech LedgerRow).
- Cross-Cloud Episode 5 (`pc-cross-cloud-agentic/05-audit-ledger-and-replay.md`) for the audit framing language (consistency between series).

**Cold Open seed:** A regulator asks the CFMP team to reproduce a recommendation made six weeks ago for a customer. Three minutes later, the trace is on the screen — every tool call, every model version, every human override.

**Section beats** (seven sub-sections):
1. What the agent fleet is — gpt-5-mini parent + specialist children (Trips, Replenish, Coupons, Pharmacy, etc.); why parent-child rather than one big agent.
2. The MCP boundary — every agent tool call hits a composed Gold view, never raw source.
3. The LedgerRow — the categories, the schema, why "every action is a row" is the design's central commitment.
4. Trace-ID propagation — how a single trace ties Mobile → Portal → Sonos → ledger so a regulator's question lands in one query.
5. Replay — what a ledger replay actually proves and what it doesn't.
6. **The Azure deployment topology** — Container Apps `ca-visionkit-mobile`, `ca-visionkit-portal`, `ca-visionkit-orchestrator` in East US 2; Azure Speech for TTS; Blob `stapexdemo50097/audio-out`; Postgres as the state store; Sonos Cloud Control API as an external integration. Reid walks through the live `/architecture` page as Keven narrates how the cold open's regulator-replay question lands a trace across exactly these services.
7. The pivot to Microsoft — Purview Audit, Foundry observability, DSPM for AI — the productized stack on APEX-M; honest about where AWS/GCP would build it themselves.

**Reid's reading** — audit chain / hash-chain literature (e.g., classic Merkle trees in operational systems).

**The disagreement** — Reid: the full ledger is overkill for 80% of agent calls. Keven concedes for genuinely-internal-only flows; the substrate stays, the enforcement intensity is per-workload. (Same converge as Cross-Cloud Ep 5 — keep it consistent.)

**Carry-forward** — the row is the product, not the by-product. APEX productizes it; the architecture is what makes it cloud-portable.

**Length:** ~5,200–6,200 words.

**Verify + Commit** as Task 2. Commit: `feat: CFMP podcast — episode 02 agent fleet & audit chain`.

---

## Task 4: Episode 03 — Mobile · SCAN & LOT

**Files:**
- Create: `pc-cfmp/03-mobile-scan-and-lot.md`

**Sources:**
- `CFMP-Mobile-Design-Document.md` §4 (Core concepts).
- `CFMP-Mobile-ScanFirst-Design.md`.
- `CFMP-Mobile-Lots-Expert-Focus.md`.
- `CFMP-Mobile-Use-Cases.md` (a sampling of SCAN/LOT UCs).

**Cold Open seed:** Sarah at the store on Tuesday — scans the bottom-shelf coupon barcode, the legacy web page doesn't load on cellular, she pays full price. CFMP-SCAN turns that miss into a save.

**Section beats:**
1. The LOT model — definition; what is a lot, what isn't; lot lifecycle states.
2. The four lot archetypes — Shopping Trip, Auto-Replenish, StayLot, Care-Lot — each with a one-sentence customer moment.
3. The SCAN interaction — scan-first design; what gets scanned (coupon barcode, product, QR, photo of a label); the SCAN → routed-to-agent pattern.
4. The MCP boundary on Mobile — every action hits a composed view; product details come from the Gold tier, not raw retailer API.
5. The UCs at the centre — pick ~6 representative SCAN/LOT use cases from CFMP-Mobile-Use-Cases.md and discuss them.
6. The honest comparison — AWS and GCP could implement the LOT model; what makes the APEX-M productization the seller's pivot.

**Reid's reading** — research on scannable-UI ergonomics, mobile camera-first interaction patterns.

**The disagreement** — Reid: scanning at home (out of the store) is fluff. Keven: the auto-replenish-from-pantry scan is the highest-NPS interaction in the design — concedes the in-flight in-store scan is the demo opener, but home scan is the retention loop.

**Carry-forward** — the LOT model; SCAN as the headline interaction; the MCP boundary as the architecture discipline this episode introduces.

**Length:** ~5,200–6,200 words.

**Verify + Commit.** Commit: `feat: CFMP podcast — episode 03 Mobile SCAN & LOT`.

---

## Task 5: Episode 04 — Mobile · Trips, Replenish, and the home channel

**Files:**
- Create: `pc-cfmp/04-mobile-trips-replenish-home.md`

**Sources:**
- `CFMP-Mobile-Design-Document.md` §§ 3 (Journey maps), 6 (Key design elements), 7 (Use cases).
- `CFMP-Mobile-Preferences-Expert-Focus.md`.
- `CFMP-Mobile-UI-Revamp.md`.

**Cold Open seed:** Thursday — Sarah opens the fridge, the romaine she bought Sunday is wilted, $4 wasted, dinner pivots. The new CFMP replenish flow would have flagged it Sunday night.

**Section beats:**
1. The trip life-cycle — pre-trip, in-flight, settle, post-trip; touchpoints across the three surfaces.
2. Auto-replenish — the pantry model, the prediction, the human-in-the-loop confirmation, the savings.
3. The home channel — kitchen-radio metaphor; voice channel as a peer (preview Sonos episode 6); when the Mobile is the home channel without a Sonos.
4. Preferences and the "1 voice" rule — Maya Chen's "one CFMP voice, one persona" — how preferences flow through every channel.
5. UI revamp tradeoffs — what changed, what didn't, the smart-default-from-Vargas pattern.
6. Senior mode + accessibility hooks — Yamamoto on the speaker as the senior interface; the Mobile a11y patterns that mirror.

**Reid's reading** — kitchen-radio interaction research / ambient computing literature.

**The disagreement** — Reid: proactive replenish-suggestions risk a creepy-uncle feel. Keven: opt-in, transparent, evidence-based; the design's consent gradient solves it. They converge on "proactive only after the customer has bought the same SKU twice".

**Carry-forward** — the four primary surfaces of Mobile; the consent gradient as the design's privacy substrate; preview of the Portal episode.

**Length:** ~5,200–6,200 words.

**Verify + Commit.** Commit: `feat: CFMP podcast — episode 04 Mobile Trips Replenish home`.

---

## Task 6: Episode 05 — Portal · operator console & B2B multi-tenant

**Files:**
- Create: `pc-cfmp/05-portal-operator-console-multitenant.md`

**Sources:**
- `CFMP-Mobile-Design-Document.md` §5 (Architecture — Portal touchpoints; the live URL is the `/architecture` page).
- `CFMP-Sonos-Design-Document.md` §5 (Portal proxies, SonosStatusBadge).
- `CFMP-Mobile-All-Experts-Panel.md` — Liu on B2B / multi-tenant; Mendez on operator UX.

**Cold Open seed:** Monday 7am — an operator opens the Portal architecture view; a Sonos household for a senior customer is showing red on the badge; one click into the incident view, the operator sees the missed-cue trace; calls the customer.

**Section beats:**
1. Who the Portal is for — operator personas; the seller / demo persona; the retailer-tenant admin (later).
2. **The `/architecture` page in detail** — the live URL `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` walked through end-to-end: the three Container Apps, Azure Speech, Blob, Postgres, the agent-fleet panel, the audit-chain panel, the Sonos Cloud Control external dependency, the East US 2 region, what each box on the diagram does. Why it's a deliberate seller artifact: "open the URL on a client call, the architecture argument is already on the screen."
3. The chat panel — operator-in-the-loop; trace-ID-anchored chat; mirror of speaker cues (per Mendez "no silent side effects").
4. The Vision Kit / camera integration — what the operator sees of in-store devices.
5. B2B retailer multi-tenant — v1 home-only; v2 retailer-tenant Sonos provisioning; the SOC 2 scope from S0.
6. Independence on retailer co-deployment — Liu's "plan for 18 months of retailer non-decision" reality; the operator console runs without the retailer.

**Reid's reading** — operator-console research; SRE-as-a-product literature.

**The disagreement** — Liu vs. Mendez on retailer-tenant timing. Reid surfaces it; Keven brings them to convergence — v1 ships operator-internal, v2 opens retailer-tenant when SOC 2 has stretched to retailer scope.

**Carry-forward** — Portal is the seller and operator surface; the architecture page is a deliberate artifact; v1 home, v2 retailer.

**Length:** ~5,200–6,200 words.

**Verify + Commit.** Commit: `feat: CFMP podcast — episode 05 Portal operator console`.

---

## Task 7: Episode 06 — Sonos · the ambient voice channel

**Files:**
- Create: `pc-cfmp/06-sonos-ambient-voice-channel.md`

**Sources:**
- `CFMP-Sonos-Design-Document.md` in full (it's the canonical source for this episode).
- `CFMP-Sonos-UC-Catalog.md`.
- `CFMP-Sonos-Roadmap.md`.

**Cold Open seed:** Sarah walking through the retailer's store with both hands full — the endcap Sonos speaker says, in a calm voice, "you saved a dollar fifty on the Coke, next stop aisle three." She doesn't break stride.

**Section beats:**
1. Why a speaker, not just a phone — "screens demand attention; speakers don't."
2. Voice as a peer channel — Mobile, Portal, Sonos as peers of the same agent fleet; one answer, three render modes.
3. The Cue — the JSON noun; the WAV its render; the Sonos play its delivery.
4. The Cue Bus — fan-out to Sonos cloud (primary), Mobile (resilient), Portal (mirror); the ledger row.
5. Zones, ducking, and the cadence law — Chowdhury's rules; the one-voice principle; the volume policy.
6. The AirPlay-bridge fallback — phone-as-bridge; the demo path; the resilience story (the Sonos cloud 503 case).
7. Azure-native deployment — no laptop, no LAN bridge; the Sonos Cloud Control API; the OAuth flow.

**Reid's reading** — ambient computing literature; voice-UI cadence research.

**The disagreement** — Chowdhury on "the cue you almost said is the one you should have skipped" vs. Mendez on "no silent side effects" — Reid presses the tension. They converge: every spoken cue mirrors visually; the question is when to skip the speaker, not when to skip the trace.

**Carry-forward** — the speaker as ambient (not insistent); the Cue Bus as fault-tolerant to its own primary transport; one voice, one CFMP.

**Length:** ~5,800–6,500 words (this episode is denser — Sonos has more concept surface).

**Verify + Commit.** Commit: `feat: CFMP podcast — episode 06 Sonos ambient voice channel`.

---

## Task 8: Episode 07 — Identity, consent, HIPAA & senior accessibility

**Files:**
- Create: `pc-cfmp/07-identity-consent-hipaa-senior.md`

**Sources:**
- `CFMP-Mobile-Design-Document.md` §8 (the cross-cutting quality layers — Adebayo, Chen, Yamamoto, Russo).
- `CFMP-Sonos-Design-Document.md` §8 (the same experts on the speaker channel).
- `CFMP-Mobile-Identity-Onboarding.md` and `CFMP-Mobile-Entra-Provisioning-Runbook.md`.

**Cold Open seed:** Diana drops in on her father Robert at 6:30pm. The kitchen speaker is mid-cue: "Robert, your refill is due Friday—". The cue stops mid-sentence — the camera saw a second person enter the room. Drug-name redaction kicks in. The cue continues: "—an item is due Friday. Want me to add it to your list?"

**Section beats:**
1. Identity — the four-identity chain (customer, operator, source-system, auditor); Entra continuity; the Mobile-Identity-Onboarding flow.
2. Consent — Adebayo's consent surface; the four classes (data, voice, presence, caregiver-share); revocability in the Preference Center.
3. HIPAA — Chen's drug-name gating; presence detection; caregiver-redacted parallel awareness; v1 scope; the operator console implications.
4. Senior accessibility — Yamamoto's defaults for 65+ (volume +4dB, cadence 130wpm, quiet hours start later); the speaker as the highest-leverage accessibility surface.
5. AirPlay channel audit-tagging — Russo's "AirPlay bypasses every server-side audit" gotcha; the LedgerRow `channel` field as a first-class value.
6. The four cross-cutting safety layers — recap, and how each maps to a real cue/screen.

**Reid's reading** — HIPAA enforcement guidance for AI-mediated speech; senior UX research.

**The disagreement** — Yamamoto wants higher default volume; Adebayo wants stricter quiet-hours defaults. Reid presses; they converge on per-zone overrides — senior zones default louder, public zones default quieter, with the Preference Center as the override surface.

**Carry-forward** — the trust substrate IS the architecture; identity, consent, HIPAA, and accessibility are not afterthoughts; the Preference Center is the kill switch the customer can always reach.

**Length:** ~5,200–6,200 words.

**Verify + Commit.** Commit: `feat: CFMP podcast — episode 07 identity consent HIPAA senior`.

---

## Task 9: Episode 08 — The seller's playbook — CFMP on APEX-M

**Files:**
- Create: `pc-cfmp/08-sellers-playbook.md`

**Sources:**
- `CFMP-Mobile-Design-Document.md` §9 (Roadmap), §10 (Open questions).
- `CFMP-Sonos-Design-Document.md` §9 (Roadmap), §10 (Open questions).
- `CFMP-Mobile-Roadmap.md`, `CFMP-Sonos-Roadmap.md`.
- Cross-Cloud Episode 8 (`pc-cross-cloud-agentic/08-the-sellers-playbook.md`) — keep the seller-playbook structure consistent across the two series.

**Cold Open seed:** A real seller's-inbox question: "Can CFMP run on AWS?" Keven and Reid open the episode on whether to say yes, no, or the right "it depends".

**Section beats:**
1. The architectural pitch — CFMP on APEX-M, the framework first; the platform recommendation follows on merits.
2. The six discovery openers — one per principle plus an opener for the home channel; phrased verbatim so the seller can use them in the room.
3. Five honest claims a seller can defend.
4. Four overclaims to avoid.
5. Six pushback-handling talking points — including the "can it run on AWS?" answer.
6. When to recommend NOT Microsoft — the credibility play; what scenarios warrant honest pivot to AWS or GCP for the data foundation.
7. The roadmap — sprints, phasing, the v2 deferred backlog.
8. The close — Independence-minded posture; the two-contract model; the series sign-off.

**Reid's reading** — a recent piece on positioning architecture-first vs. product-first.

**The disagreement** — the multi-cloud-CFMP question. Reid: a serious customer will ask if CFMP can be ported. Keven: the framework is portable; the productization density on Microsoft is where the seller earns the recommendation. Honest tension; converge as "portable-by-default, single-cloud-by-default-execution".

**Carry-forward** — series finale: lead with architecture; honesty is the moat; the productization window is open and finite. Sign-off line consistent with the Cross-Cloud series ("see you in the field").

**Length:** ~5,400–6,200 words.

**Verify + Commit.** Commit: `feat: CFMP podcast — episode 08 the seller's playbook`.

---

## Task 10: Final verification

**Files:**
- Verify only.

**Step 1: Structural verification**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cfmp"
python -c "
import os, re
files=sorted(f for f in os.listdir('.') if f.endswith('.md'))
assert len(files)==9, f'expected 9 md files, got {len(files)}: {files}'
assert files[0]=='00-show-bible-and-format.md'
needed=['## Cold Open','### A reading I want to do','### One disagreement','### What to carry forward','## Further reading']
forbidden=['co-sell','channel partner','strategic partnership','alliance partner']
total_words=0
for f in files[1:]:  # episode files
    t=open(f,encoding='utf-8').read()
    for s in needed:
        assert s in t, f'{f}: missing {s!r}'
    for s in forbidden:
        assert s.lower() not in t.lower(), f'{f}: forbidden term {s!r}'
    spoken=re.sub(r'\[[^\]]*\]','',t)
    spoken=re.sub(r'^#{1,6} .*$','',spoken,flags=re.M)
    spoken=re.sub(r'\*\*(KEVEN|REID):\*\*','',spoken)
    wc=len(spoken.split())
    total_words+=wc
    assert 3500<=wc<=8000, f'{f}: word count {wc} out of band'
    print(f'{f}: {wc} words')
print(f'TOTAL spoken words across 8 episodes: {total_words}')
print(f'Estimated runtime at 145 wpm: {total_words//145} min, {(total_words//145)//8} min average/episode')
"
```

**Step 2: Content-discipline spot-check**

```bash
python -c "
import os
files=[f for f in os.listdir('.') if f.endswith('.md')]
# real retailer names to avoid
checks=['kroger','walmart','target','costco','safeway','albertsons','wegmans','publix','amazon fresh','instacart']
for f in files:
    t=open(f,encoding='utf-8').read().lower()
    for c in checks:
        assert c not in t, f'{f}: real retailer name {c!r} found (should be \"the retailer\")'
# fictional personas must be present (Sarah at least)
mention=open('01-sarahs-day.md',encoding='utf-8').read().lower()
assert 'sarah' in mention, 'Episode 01 must mention Sarah'
print('content discipline clean across 9 files')
"
```

**Step 3: Commit (if fixes were needed)**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git commit -am "fix: CFMP podcast verification fixes" || echo "no fixes needed"
```

---

**End of plan.** 10 tasks. Estimated effort: ~4–6 hours (show bible + 8 ~5500-word episodes + verification).
