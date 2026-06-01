# LA28 Telco-Agentic Anchor Podcast Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Produce a 9-episode sellers / pursuit podcast walking the 24-month build-to-LA28 motion milestone by milestone (M0 Denver kickoff → M8 Wave-2 scaling), with Rashmi + Keven as the hosts (continuity with the DTNA Account Podcast), narrative-first prose, real anchor-partner naming (AT&T · LA28 · NBCU · Walmart · Marriott · etc.), and Independence-language discipline ("Microsoft platform engagement" — never "alliance" or "partner").

**Architecture:** One show bible defining the recurring format; nine episode scripts authored faithfully against the source tracker (`C:\Users\kmarkham\Downloads\APEX-Agentic-Telco-Olympics-Tracker (7).html`). Each episode mirrors one milestone with the milestone's seller-tasks + cross-Practice coordination + anchor-partner moves as the spine. Same narrative tone discipline carried from the CFMP re-tone (cold-open moment, technical-aside rule, business-outcome close).

**Tech Stack:** Markdown only (scripts). Audio production deferred per established pattern.

**Design doc:** `docs/plans/2026-05-26-la28-telco-agentic-podcast-design.md`.

**Target folder:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-la28-olympics-telco\` (mkdir as needed).

**Authoritative source:** `C:\Users\kmarkham\Downloads\APEX-Agentic-Telco-Olympics-Tracker (7).html` — every milestone, every seller-task, every anchor-partner reference traces to this file.

---

## Notes for the executor

- Hosts: **Rashmi + Keven**. Speaker markers: `**RASHMI:**` and `**KEVEN:**`. Rashmi = Deloitte hand who knows the framework + practice coordination. Keven = Microsoft platform practitioner (22 years on Microsoft, VP of Deloitte's Microsoft Technology & Services Practice).
- Content discipline (non-negotiable):
  - **Independence language** — "Microsoft platform engagement," **never** "co-sell," "alliance," "strategic partnership," "channel partner," "alliance partner."
- **Microsoft commercial instruments off-tape (Independence)** — Deloitte audits Microsoft. Hosts do NOT name, describe, or reference Microsoft funding programs or consumption-commitment vehicles anywhere on tape. Forbidden tokens (case-sensitive acronyms): `ECIF`, `MACC`. Forbidden phrases (case-insensitive): `co-investment`, `joint-motion`, `joint motion`, `pull-through`. Any "Microsoft platform engagement" content stays on-the-merits — the platform is recommended for its technical fit; Microsoft handles its commercial conversation directly with the anchor on its own paper.
  - **Anchor-partner naming** — real entities named as themselves (AT&T · LA28 · NBCUniversal · Walmart · American Airlines · Marriott · Expedia · Airbnb · Hertz · Uber · OpenTable · Viator · Toyota Connected · AutoNation · Progressive · Sazerac · CVS · etc.). Internal C-suite by **title and role**, never invented names (DTNA Rule 1 carries).
  - **LA28 / IOC brand discipline** — TOP-program scope respected; NBCU rights conversation respected; trademark deference.
  - **Narrative tone** — every sub-section opens with a concrete pursuit moment before any framework term; technical vocabulary in asides; sub-section closes on what the seller does Monday.
  - **No section number citations on tape** (the hosts know the framework — DTNA discipline carries).
- Episode shape (every episode follows):
  - `# Episode NN · <Title>` + Builds-on header
  - `## Cold Open` (300-400 word vignette)
  - `## The conversation` with 5-7 `### ` sub-sections
  - `### A reading I want to do` (Rashmi or Keven recommends; 1-2 paragraphs)
  - `### One disagreement` (real tension between hosts, named or converged)
  - `### What to carry forward` (2-3 numbered, seller-actionable)
  - `## Further reading` (tracker + adjacent podcasts + anchor-partner public materials)
- Word target per episode: **5,200–6,500 spoken words** (verify band 4,800–7,500). Spoken-only count excludes `[stage directions]`, headings, and speaker tags.
- Tasks 2–10 each modify a single new file; run sequentially. Commit each episode independently.

---

## Task 1: Create the show bible

**Files:**
- Create: `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-la28-olympics-telco\00-show-bible-and-format.md`

**Step 1: Write the file**

The show bible defines the recurring format. Cover:

- **Series identity** — title (*The LA28 Telco-Agentic Anchor Podcast*), one-line pitch, audience (DMTSP Account Teams + TMT-led + cross-Practice leads).
- **What makes this podcast different** — extend the DTNA show bible's comparison table with a new column. Audience: DMTSP / pursuit. Industry: TMT-led, cross-Practice. Voice cast: Andrew + Brian Multilingual (DTNA continuity). Distinctive content: 9-milestone pursuit motion · 11 channels × 9 Practices · LA28 brand discipline.
- **The 9-milestone arc** — restate titles + one-line each.
- **Hosts** — Rashmi + Keven character sheets (background, voice, vocabulary, what each pushes on).
- **Episode shape** — Cold Open → The conversation (5-7 sub-sections) → A reading I want to do → One disagreement → What to carry forward → Further reading.
- **Cold-open style** — moment-in-the-pursuit vignettes: a seller's inbox, an AT&T NOC engineer, an LA28 ops desk, a Super Bowl-weekend pilot household, a Game-day Adaptive Card landing on a CEO's screen, a Casey Wasserman BD call.
- **Content discipline** — Independence language; LA28 / IOC brand discipline (TOP-program scope, NBCU rights, Olympic trademark deference); anchor-partner naming rule (real entities as themselves; internal C-suite by title-and-role); the forbidden vocabulary list; the no-section-number-citation rule.
- **The 9 Practices × 11 Channels coordination grid** — TMT · TH · RC · AXLE · ER · HLS · ICE · FSI · GPS · (Risk · Cross) × Home · Travel · Retail · Mobility · Auto · CPG · Energy · Health · Industrial · Finance · Public.
- **Recurring elements** — `A reading I want to do`, `One disagreement`, `What to carry forward`, the quote-and-react moment (one per episode, primary source).
- **Voice cast (deferred audio)** — Andrew Neural (Rashmi / Keven — assign based on the DTNA precedent) + Brian Multilingual; opening + closing sting timing carried from the sibling DTNA series.
- **Pacing rules from the sibling DTNA show bible** — no chapter/section citations, 3-5 min historical context to open, one concept developed (4-6 min) before transitioning, real disagreement per episode, no announced segments.
- **Pre / During / Post / Handoff structure** within each episode (milestone runway → the moment → the handoff to the next milestone).

Target length: ~2,200–2,800 words.

**Step 2: Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-la28-olympics-telco"
python -c "
t=open('00-show-bible-and-format.md',encoding='utf-8').read()
for s in ['Rashmi','Keven','Cold Open','LA28','Independence','Microsoft platform engagement']:
    assert s in t, 'missing '+s
for forbid in ['co-sell','channel partner','strategic partnership','alliance partner']:
    assert forbid.lower() not in t.lower(), 'forbidden term: '+forbid
# 'alliance' may appear in the discipline section as the term to avoid — explicit mention is OK in the rule itself; verify not used as a positive descriptor
print('show bible OK; words:', len(t.split()))
"
```

**Step 3: Commit**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git add docs/podcast/pc-la28-olympics-telco/00-show-bible-and-format.md
git commit -m "feat: LA28 podcast show bible"
```

---

## Task 2: Episode 01 · The pursuit · DMTSP Denver kickoff (M0)

**Files:**
- Create: `pc-la28-olympics-telco/01-the-pursuit-denver-kickoff.md`

**Source (read first):** the tracker's M0 block in `APEX-Agentic-Telco-Olympics-Tracker (7).html`. Specifically: M0 `name`, `monthsBefore: 25`, `days: 'M-25 → M-22 · Denver kickoff 10 Jun 2026'`, `primary: 'DMTSP all-hands · top-down endorsement'`, the seven `objectives`, and the sellerTasks (DMTSP Denver meeting, pre-Denver brief, Denver deck preparation, DMTSP Microsoft Platform Lead coordination, per-Practice 1:1 briefs, US Industry Leader brief). **Note:** the tracker source contains "joint-motion shape" language — Independence-clean podcast vocabulary replaces this with "Microsoft platform engagement coordination" or "platform-engagement shape" (see Independence rule above).

**Cold Open seed:** Early June 2026. The TMT VP is in her hotel room in Denver the night before the DMTSP all-hands kickoff. The single-page charter the M&P Leader will see in the morning is on her laptop. The list of nine Practice Principals she'll brief one-by-one over the next two weeks is in her notebook. The campaign she's bringing to Denver — *the build to LA28, twenty-five months out* — is a question of endorsement, not architecture. *"Do we go after this together or not."* The morning meeting is at 9am Mountain. She closes the laptop. Open Rashmi + Keven on the moment.

**Section beats** (six `### ` sub-sections):
1. **### The Denver kickoff** — what the M0 meeting needs to land: top-down M&P Leader endorsement; the LA28 campaign presented to all DMTSP sellers; the 8-milestone roadmap as the artifact; the year activity plan agreed.
2. **### Per-Practice principals — the nine 1:1s** — TMT · TH · RC · AXLE · ER · HLS · ICE · FSI · GPS. Each Principal gets a charter brief + a seller-team naming ask + the anchor-LCSP brief plan. The cross-Practice coordination motion starts here.
3. **### The Microsoft platform engagement framework** — the canonical Independence language is drafted and circulated. Microsoft AE/CSA assignments framework (role-level, neutral). *"Microsoft platform engagement"* — the phrase that travels the next 24 months is set in this section and carries through every subsequent episode. Microsoft's commercial-instrument conversations remain off-tape (Deloitte audits Microsoft).
4. **### The capacity commitments** — AI Institute + D&A Practice + ML Engineering capacity commitment framework. Without these, the pursuit doesn't ship.
5. **### Risk Advisory pre-clear** — per-anchor Independence pre-clear list submitted to National Office. The pre-clear motion runs *concurrently* with the BD motion, not sequentially.
6. **### The validation gate** — what M0 must deliver before M1 unlocks: DMTSP Denver kickoff complete; M&P Leader endorsement secured; Microsoft platform engagement framework agreed (Independence-clean language committed across all 24 months); per-Practice seller teams named; per-anchor LCSP brief cadence agreed; AI Institute capacity framework agreed; Risk Advisory pre-clear list submitted.

**A reading I want to do** — Rashmi recommends something on **pursuit-team-charter discipline** or the **DMTSP top-down endorsement pattern** — a real Deloitte internal pattern reference (or an external pursuit-management piece like Geoffrey Moore's *Crossing the Chasm* applied to anchor-account pursuit). 1-2 paragraphs.

**One disagreement** — Rashmi argues the M0 kickoff should commit *Wave-1 only* (AT&T + LA28). Keven argues the Wave-2 syndication conversation (T-Mobile · Verizon · Charter · Lumen) needs to be opened at M0 in soft form so the relationship pipeline isn't cold when Wave-1 closes. They converge on: Wave-1 firm commit at M0; Wave-2 soft pre-warming begins concurrently but no contractual conversation until AT&T proof point.

**What to carry forward** — three things, numbered, seller-actionable: (1) the M0 kickoff IS the campaign; (2) the per-Practice 1:1 brief cadence is the coordination motion's spine; (3) Microsoft platform engagement language sets the Independence frame for the whole 24 months.

**Length target:** 5,200–6,200 spoken words.

**Verify + Commit** — same shape as Task 1. Markers: `## Cold Open` · `### A reading I want to do` · `### One disagreement` · `### What to carry forward` · `## Further reading` · `**RASHMI:**` · `**KEVEN:**` · `Denver` · `DMTSP` · `M0`. Commit: `feat: LA28 podcast — episode 01 the pursuit · Denver kickoff (M0)`.

---

## Task 3: Episode 02 · The anchor · AT&T + LA28 commit (M1)

**Files:**
- Create: `pc-la28-olympics-telco/02-the-anchor-att-la28-commit.md`

**Source:** M1 from the tracker. `monthsBefore: 24`, `primary: 'AT&T + LA28 BD'`, objectives: AT&T Wave-1 charter; LA28 sponsorship rights review (TOP-program scope); NBCUniversal rights conversation; Microsoft Azure CAF capacity reservation for 2028 Q3; pursuit team formed. SellerTasks across TMT · TH · CROSS · RISK · GPS.

**Cold Open seed:** Mid-summer 2026. The TMT VP is on a call with AT&T's Chief Customer Officer + CTO at AT&T headquarters. Two slides on the screen — *the Agentic Marketplace at LA28*. The CCO asks one question: *"Who's the bill owner?"* The answer is AT&T. Wave-1. The CTO asks one question: *"What's the platform commitment?"* The answer is Microsoft Azure. Foundry. CAF capacity reserved through 2028 Q3. The call lasts forty-two minutes. The Wave-1 charter is verbally committed by minute thirty-eight. Open Rashmi + Keven on the moment.

**Section beats:**
1. **### AT&T as the Default Telco anchor** — Wave-1 charter signed; AT&T owns the Bill; the Default Home Channel becomes Wave-1 deliverable. T-Mobile / Verizon / Charter / Lumen pre-warmed for Wave-2 syndication post-LA28.
2. **### The LA28 sponsorship rights conversation** — Casey Wasserman BD team. TOP-program scope clarification. What's in scope as a platform-vendor positioning vs. what requires TOP-program sponsorship.
3. **### The NBCUniversal rights conversation** — NBCU Sports + Olympics counsel. Scope-boundary conversation BEFORE any Media Channel commitment lands at M3. The watch-party / Peacock cross-promo conversation has to be respectful of NBCU's exclusive rights.
4. **### The Microsoft Azure platform commitment** — CAF capacity for projected Games load; Microsoft AE alignment; reference-architecture fidelity. The platform engagement is named explicitly; the Independence language holds. Microsoft's commercial conversation with AT&T stays on Microsoft's paper, not Deloitte's.
5. **### Pursuit team formation** — Deloitte pursuit team formed with named leads from TMT · TH · RC · AXLE · ER · HLS · ICE · FSI · GPS + Risk Advisory. Weekly Practice-leads sync established. LA City Mayor's office opened (long lead times for federal/state coord).
6. **### The validation gate** — AT&T Wave-1 charter committed; LA28 sponsorship scope confirmed; NBCU scope-boundary conversation opened; Microsoft CAF reservation confirmed; pursuit team formed and cadence running; per-anchor Independence pre-clear maturing.

**Reading** — Keven recommends a piece on **anchor-account commit-to-Wave-1 discipline** — Sonepar Pursuit Tracker pattern reference (the model the LA28 tracker borrows from) or an enterprise-software-anchor-customer essay.

**Disagreement** — Rashmi: open NBCU at M1 so the Media Channel scope conversation has runway. Keven: NBCU is sensitive — the conversation has to lead with respect for their exclusive rights; soft-touch only at M1, formal scope at M3. They converge on a soft introduction at M1 + a respectful scope conversation that explicitly defers commitment to M3.

**Carry-forward** — (1) Wave-1 anchor commit IS the unlock for everything downstream; (2) the LA28 sponsorship rights conversation is separate from the platform-vendor positioning conversation — keep them separate on tape; (3) Microsoft platform engagement is the Independence-language commitment that holds for 24 months.

**Length:** 5,400–6,400.

**Verify + Commit.** Markers add: `AT&T` · `LA28` · `Casey Wasserman` · `NBCU` · `Microsoft platform engagement`. Commit: `feat: LA28 podcast — episode 02 the anchor · AT&T + LA28 commit (M1)`.

---

## Task 4: Episode 03 · The default channel · Home goes live in shadow (M2)

**Files:**
- Create: `pc-la28-olympics-telco/03-the-default-channel-home-shadow.md`

**Source:** M2 from the tracker. The Default Home Channel goes live in shadow mode (no customer-facing impact yet) — AT&T NOC + Microsoft Foundry + A2A Swarm runtime + the vault. Telemetry flowing; agents composing; nothing visible to the customer until M3 onwards.

**Cold Open seed:** Late autumn 2026. An AT&T NOC engineer on a Wednesday night at 11:47pm Eastern. The Default Home Channel went live in shadow ten minutes ago. The first agent composes a recommendation for a real AT&T household. The recommendation is correct. The household never sees it — the channel is in shadow. But the trace_id is propagating, the vault is sealing the audit row, the A2A Swarm is composing within the bounded MCP surface. The platform commitment from M1 just became real. Open Rashmi + Keven on the moment.

**Section beats:**
1. **### Shadow mode — what it means and why** — the channel runs end-to-end against real telemetry but with no customer impact. Every recommendation, every agent composition, every audit row is real; the *delivery* is suppressed. Why this matters for AT&T's risk posture and for Deloitte's pre-launch confidence.
2. **### The Default Home Channel architecture** — the TMT delivery architects' build; the AT&T NOC integration; the agent fleet running on Microsoft Foundry; the A2A Swarm runtime; the vault sealing audit rows. (Technical terms named once, with care.)
3. **### What "Default" means and why it matters** — Default Home is the canonical channel pattern that other Channels plug into. Get the pattern right at M2; the plug-ins (M3 + M4) land more cleanly.
4. **### The first observations** — what the shadow telemetry surfaces about household patterns, about recommendation quality, about latency, about cost. The early observations shape the M3 sign-up conversations.
5. **### The Microsoft platform engagement holds** — AT&T's first real-load test of the Microsoft Azure commitment. CAF capacity, Foundry throughput, vault throughput. The platform-engagement framework from M1 meets reality at M2.
6. **### The validation gate** — Default Home Channel live in shadow; recommendation quality meets agreed bar; latency within budget; cost within model; A2A Swarm + vault audit substrate composing end-to-end; AT&T NOC team comfortable with the steady-state ops posture.

**Reading** — Rashmi recommends a piece on **shadow-mode launches in regulated environments** (banking-platform pre-launch shadow patterns, or aviation control-system gate-validated launch patterns).

**Disagreement** — Keven: M2 should end with a small live cohort (~50 AT&T households) to validate the customer-facing experience. Rashmi: shadow only at M2; live customer cohort is M3 work after the Wave-1 plug-in Channels are signed. They converge on M2 shadow-only with a *pre-staged* small cohort selection ready to flip at M3.

**Carry-forward** — (1) Default is the pattern; get it right at M2; (2) shadow mode is the platform's contract with the anchor — real load, no customer impact; (3) the Microsoft platform engagement either holds at M2 or it doesn't — this is where the M1 commitment meets reality.

**Length:** 5,300–6,300.

**Verify + Commit.** Markers add: `Default Home Channel` · `shadow` · `Foundry` · `A2A Swarm` · `vault`. Commit: `feat: LA28 podcast — episode 03 the default channel · Home shadow (M2)`.

---

## Task 5: Episode 04 · The first plug-ins · Travel + Retail + Media signed (M3)

**Files:**
- Create: `pc-la28-olympics-telco/04-the-first-plug-ins-travel-retail-media.md`

**Source:** M3. Travel + Retail + Media Channels signed. TH anchors (American Airlines AAdvantage, Marriott Bonvoy, Expedia API Partnerships, Airbnb Identity, Hertz, Uber, OpenTable, Viator). RC anchor (Walmart — Walmart+, Pharmacy, Auto Care, Sam's Club). Media (NBCU/Peacock scope-bounded).

**Cold Open seed:** January 2027. The TH VP is in a hotel lobby in Bethesda, Maryland after a Marriott Bonvoy team meeting. Her phone has three signed term sheets queued. American Airlines AAdvantage. Marriott Bonvoy. Expedia API Partnerships. The Travel Channel is officially three-of-eight signed by lunchtime. The Walmart team flies in Friday. The NBCU scope-bounded conversation is on the calendar Tuesday. The first plug-ins are landing. Open Rashmi + Keven on the moment.

**Section beats:**
1. **### The Travel Channel — 8 anchors** — AA · Marriott · Expedia · Airbnb · Hertz · Uber · OpenTable · Viator. What each anchor brings; what each requires in return; how they compose in the trip-mode customer journey.
2. **### Walmart anchors the Retail Channel** — Walmart+ + Walmart Pharmacy + Walmart Auto Care + Sam's Club. The errand-chain scenario that Walmart's surfaces compose end-to-end.
3. **### The Media Channel — scope-bounded** — NBCUniversal / Peacock conversation respects NBCU's exclusive rights. The watch-party + Peacock cross-promo opportunity is real but bounded.
4. **### The cross-Practice coordination intensifies** — TMT lead, TH and RC as primary, FSI for payments, Risk for Independence on every anchor MOU. The weekly Practice-leads sync becomes the operational rhythm.
5. **### Anchor-partner sign-up motion** — informal calls (M1) → workshops (M3-week-1) → MOU drafting (M3-week-3) → signed term sheets (M3-week-6). The pattern.
6. **### The validation gate** — Travel Channel: ≥6 of 8 anchors signed (8 nice-to-have); Retail: Walmart signed; Media: NBCU scope-bounded MOU drafted; cross-Practice MOUs comply with Risk Advisory's per-anchor pre-clears; Independence language in every signed document.

**Reading** — Keven recommends a piece on **multi-anchor channel sign-up cadence** — Sonepar Pursuit Tracker pattern reference (multi-anchor M3 phase), or a B2B enterprise-channel-anchor essay.

**Disagreement** — Rashmi: 6-of-8 Travel anchors is enough to ship M3. Keven: 7-of-8 is the threshold; missing two anchors leaves a customer-journey gap in the trip-mode scenarios. They converge on 7-of-8 as the gate with the 8th anchor as a stretch.

**Carry-forward** — (1) Wave-1 plug-ins close M3; (2) the cross-Practice MOU pattern from M3 is the template for M4; (3) anchor-MOU language is Risk-pre-cleared per-anchor before signature.

**Length:** 5,400–6,500.

**Verify + Commit.** Markers add: `American Airlines` · `Marriott` · `Expedia` · `Walmart` · `NBCUniversal`. Commit: `feat: LA28 podcast — episode 04 first plug-ins · Travel + Retail + Media (M3)`.

---

## Task 6: Episode 05 · The second wave · Mobility + Auto + CPG (M4)

**Files:**
- Create: `pc-la28-olympics-telco/05-the-second-wave-mobility-auto-cpg.md`

**Source:** M4. Mobility (Toyota Connected · AutoNation · Progressive UBI) · Auto · CPG (Sazerac). The second wave of plug-ins.

**Cold Open seed:** Spring 2027. The AXLE Account Lead is in Plano, Texas at Toyota Connected's office. The Toyota team has just confirmed that vehicle telemetry — engine health, OBD-II faults, tire pressure, range — can be wired into the Channel's trip-mode composition. Toyota Connected becomes the Mobility-Auto anchor. The Progressive UBI conversation is at 2pm. The Sazerac BTAC-analog limited release conversation is Thursday in Frankfort, Kentucky. The second wave is moving. Open Rashmi + Keven on the moment.

**Section beats:**
1. **### Toyota Connected as the Mobility-Auto anchor** — what vehicle telemetry adds to the trip-mode composition; the integration patterns; the consumer-consent posture.
2. **### Progressive UBI — usage-based insurance as a Channel surface** — how trip-mode insurance riders compose; the FSI Practice's role in the M4 wave.
3. **### Sazerac as the CPG anchor** — BTAC-analog limited-release allocation across LA28-host-city licensed retailers; age-verification posture; the Industrial-grade allocation logic.
4. **### AutoNation dealer routing** — the dealer-coordination layer that ties Toyota Connected's vehicle alerts to AutoNation service scheduling.
5. **### Cross-Channel composition intensifies** — Mobility + Auto + CPG compose with Travel + Retail + Home in single customer-journey traces. The agent fleet's composition discipline is tested here.
6. **### The validation gate** — Toyota Connected MOU signed; AutoNation routing wired; Progressive UBI scope agreed; Sazerac allocation tested in one host-city retailer; cross-Channel composition produces clean traces; Risk Advisory pre-clears matured.

**Reading** — Rashmi recommends a piece on **vehicle-telemetry-as-experience-surface** (Toyota Connected positioning, or a connected-vehicle-platform pattern essay).

**Disagreement** — Keven: M4 should add a second OEM anchor (Ford? GM?) for breadth. Rashmi: focus is the win; Toyota Connected is enough for M4; a second OEM is M8 Wave-2 syndication work. They converge on Toyota-only at M4 with second-OEM held for Wave-2.

**Carry-forward** — (1) Wave-1 is now 5 plug-ins (Travel + Retail + Media + Mobility/Auto + CPG); (2) cross-Channel composition is the test of the platform's discipline; (3) FSI's UBI surface is the bridge to Wave-2 financial-services plays.

**Length:** 5,300–6,300.

**Verify + Commit.** Markers add: `Toyota Connected` · `AutoNation` · `Progressive` · `Sazerac` · `Mobility`. Commit: `feat: LA28 podcast — episode 05 second wave · Mobility + Auto + CPG (M4)`.

---

## Task 7: Episode 06 · The dress rehearsal · Super Bowl LXII (M5)

**Files:**
- Create: `pc-la28-olympics-telco/06-the-dress-rehearsal-super-bowl.md`

**Source:** M5. Super Bowl LXII (Feb 2028) as live cross-Channel test event. All 6 Channels active simultaneously for 2,000-5,000 AT&T pilot households in the host metro. IROPS rebook + hotel walk + ground-mobility scenarios validated live. Load test 1.5x projected LA28 peak. After-action review with all anchor partners.

**Cold Open seed:** Friday morning of Super Bowl LXII weekend, February 2028. The TMT Delivery Architect is at the LA-host-city ops desk. The 2,847 pilot households are configured. All six Channels are live. The first IROPS event of the morning — an inbound flight to the host city diverted to a secondary airport — fires the trip-mode composition: AA rebook + Marriott walk + Hertz pickup + Uber reroute. Single customer-journey trace. Four anchors. One Channel composition. The Super Bowl is the dress rehearsal — the 1.5x load test of LA28. Open Rashmi + Keven on the moment.

**Section beats:**
1. **### Why Super Bowl LXII** — the only live cross-Channel test that approaches LA28 scale in the build window. 1.5x projected LA28 peak load; all 6 Channels active; all anchor partners staffed.
2. **### IROPS + hotel walk + ground-mobility** — the three reliability scenarios that have to compose end-to-end during a real reservation-disruption event. The 4-anchor trace from AA → Marriott → Hertz → Uber.
3. **### Walmart errand-chain + Sazerac allocation at host-city scale** — pharmacy + GM + TLE chain executed; BTAC-analog limited release tested at one licensed retailer; age-verification flow exercised.
4. **### Toyota + AutoNation + Progressive vehicle scenarios** — pre-Game tire-check + UBI-rider + dealer routing validated.
5. **### ER demand-response + HLS cross-state Rx + ICE venue BMS** — energy, health, industrial surfaces all live for the first time at Super Bowl scale.
6. **### After-action review** — what worked, what didn't, what needs to be fixed before LA28 in five months. The findings shape M6.
7. **### The validation gate** — all 6 Channels active during Super Bowl weekend; IROPS scenarios produce clean traces; load test exceeds 1.5x LA28 projected peak; after-action review completed with all anchor partners; M6 remediation backlog scoped.

**Reading** — Keven recommends a piece on **dress-rehearsal-as-engineering-discipline** (NASA mission rehearsal patterns, or large-event-software dress rehearsal essays from the Olympics opening-ceremony software literature).

**Disagreement** — Rashmi: the 1.5x load test is enough; over-provisioning beyond is wasteful. Keven: the LA28 venue-peak unknown is wide; 2x is the right margin. They converge on 1.75x as the target.

**Carry-forward** — (1) Super Bowl is the only live cross-Channel test before LA28 — make it count; (2) the after-action review IS the M6 backlog; (3) anchor-partner staffing model at Super Bowl is the staffing model at LA28.

**Length:** 5,400–6,400.

**Verify + Commit.** Markers add: `Super Bowl` · `IROPS` · `pilot households` · `load test` · `cross-Channel`. Commit: `feat: LA28 podcast — episode 06 dress rehearsal · Super Bowl LXII (M5)`.

---

## Task 8: Episode 07 · The home stretch · California + venue + transit (M6)

**Files:**
- Create: `pc-la28-olympics-telco/07-the-home-stretch-california-venue-transit.md`

**Source:** M6. M-4 → M-1. LA28 readiness — California government coordination, venue BMS integrations, transit coordination, cross-state Rx, GPS Practice leading public-sector coordination, ICE Practice on venue + transit.

**Cold Open seed:** April 2028. The GPS Account Lead is in the LA Mayor's office, sitting across from the Chief Information Officer. The conversation is about Games-window data-sharing between the LA28 organizing committee, the City of LA, the State of California, and the federal coordination teams. The CIO asks: *"What happens when a federal alert needs to reach a Channel-enrolled household in real time?"* The answer involves three Practices, two cloud platforms, one Channel architecture, and the Independence-language posture. The conversation runs an hour and twelve minutes. Open Rashmi + Keven on the moment.

**Section beats:**
1. **### California + federal coordination** — LA Mayor's office + CA Governor's office + federal teams. Long lead times; the GPS Practice has been working this since M1.
2. **### Venue BMS integration** — ICE Practice on stadium/venue building-management-system data flows. Spectator-throughput metrics feeding Channel mobility routing.
3. **### Transit coordination** — LA Metro + ride-share integration. The Mobility Channel during Games-window crowd peaks.
4. **### Cross-state Rx (HLS)** — CVS cross-state pharmacy refill for traveling families during the Games window. Tested at Super Bowl, productionised at M6.
5. **### M6 remediation backlog** — every finding from the Super Bowl after-action review now in flight. The M5 → M6 handoff is the M6 work.
6. **### The validation gate** — California + federal coordination MOUs signed; venue BMS data flowing for selected venues; transit coordination in production; cross-state Rx exercising at scale; M5 backlog 100% remediated; ops command center stood up in LA.

**Reading** — Rashmi recommends a piece on **public-sector coordination for large-event programs** (Olympic Games public-private coordination case studies, or FEMA / DHS large-event coord essays).

**Disagreement** — Keven: production ops command center should be in Redmond (Microsoft HQ adjacency). Rashmi: command center in LA — physical proximity to venue + LA28 + AT&T regional ops matters more than platform-team adjacency. They converge on dual command — primary in LA, mirrored in Redmond.

**Carry-forward** — (1) public-sector coordination has long lead times — M1 starts the conversation, M6 closes it; (2) the dress-rehearsal-to-M6 handoff is the production-readiness gate; (3) the ops command center is the Games-window face of the pursuit.

**Length:** 5,300–6,300.

**Verify + Commit.** Markers add: `LA Mayor` · `California` · `venue` · `transit` · `M5 backlog`. Commit: `feat: LA28 podcast — episode 07 home stretch · California + venue + transit (M6)`.

---

## Task 9: Episode 08 · Sixteen days · LA28 Games live (M7)

**Files:**
- Create: `pc-la28-olympics-telco/08-sixteen-days-la28-games-live.md`

**Source:** M7. Jul 14 → Jul 30, 2028. Opening Ceremony · 16-day Games window · all-hands ops. Wedge events captured (IROPS rebook · hotel walk · BTAC pickup · eldercare continuity). Closing Ceremony. Daily 8am PT Adaptive Card to AT&T CEO + LA28 leadership. Zero brand-event incidents.

**Cold Open seed:** Day 7 of the LA28 Games — Sunday morning, July 20, 2028. The AT&T CEO's executive briefing is at 8am PT. The Adaptive Card lands on her phone at 7:58. Six rows. Channel-by-Channel status. Yesterday's wedge events — three IROPS rebooks, eleven hotel-walks, four cross-state Rx refills, one Sazerac BTAC pickup at the LA28 host-city retailer. Zero brand-event incidents. The CEO opens the card while her coffee is still brewing. *Channel ops are green.* She forwards the card to her board chair with one line — *"This is what we built."* Open Rashmi + Keven on the moment.

**Section beats:**
1. **### The production ops command center** — 24/7 coverage in LA; mirrored in Redmond; live dashboards; all anchor partners staffed. The first hours of the Games are the test.
2. **### Daily Adaptive Card to AT&T CEO** — 8am PT cadence; Channel-by-Channel status; wedge events captured; escalations. The Card IS the executive-briefing artifact.
3. **### The trip-mode scenarios run live** — AA + Marriott + Expedia + Airbnb daily standup; trip-mode scenarios overnight; day-ahead trip-volume forecast.
4. **### NBCU ride-along live** — watch-party suggestions + Peacock cross-promo (with disclosure) firing during competition windows. The Media Channel respects NBCU's rights.
5. **### Walmart errand-chain + Sazerac allocation live** — pharmacy refills for travelers + host-city BTAC pickup events captured.
6. **### Toyota + AutoNation + Progressive vehicle scenarios live** — trip-mode insurance riders + dealer-coordination + UBI continuous.
7. **### ER demand-response + HLS cross-state Rx + ICE venue BMS live** — energy demand-response events fired during venue peak; cross-state Rx exercising for traveling families; venue BMS data feeding mobility routing.
8. **### The validation gate** — Opening Ceremony clean; 16-day window operating at projected scale; wedge events captured and resolved; Closing Ceremony clean through final day; daily Adaptive Card delivered every morning; zero brand-event incidents.

**Reading** — Keven recommends a piece on **Olympic-period software operations** — IOC technology-partner case studies from prior Games (Atos / Alibaba), or the software-ops-at-Olympic-scale literature.

**Disagreement** — Rashmi: the daily Adaptive Card to the AT&T CEO should also go to the LA28 organizing committee CEO. Keven: separate Cards by audience — AT&T sees operational truth; LA28 sees partner-commitment-status truth. They converge on dual Cards with shared underlying data, audience-tuned framing.

**Carry-forward** — (1) the production ops command center IS the Games-window experience; (2) the daily Adaptive Card is the executive contract — show up every morning; (3) zero brand-event incidents is the gate that makes M8 case-study credible.

**Length:** 5,500–6,500. This is the densest episode.

**Verify + Commit.** Markers add: `Opening Ceremony` · `Closing Ceremony` · `Adaptive Card` · `wedge events`. Commit: `feat: LA28 podcast — episode 08 sixteen days · LA28 Games live (M7)`.

---

## Task 10: Episode 09 · The wrap · Case study + Wave-2 syndication (M8)

**Files:**
- Create: `pc-la28-olympics-telco/09-the-wrap-case-study-wave-2.md`

**Source:** M8. Post-Games. Wrap + case study + scaling plan. T-Mobile · Verizon · Charter · Lumen Wave-2 contracting. Framework-level scaling.

**Cold Open seed:** August 2028. Two weeks after the Closing Ceremony. The TMT VP is in her home office at 6am Pacific. The LA28 case study is on her screen — single-page executive summary, supporting data, the wedge-event narratives, the audit-chain replay capability demonstrated to the regulator who visited during week-two. The case study lands on AT&T's CEO desk in two hours. The Wave-2 syndication conversation starts later in the week — T-Mobile in Bellevue Monday; Verizon in Basking Ridge Tuesday; Charter in Stamford Wednesday; Lumen in Monroe Thursday. Four conversations. One case study. *The pattern travels.* Open Rashmi + Keven on the moment.

**Section beats:**
1. **### The case study** — the single artifact that compresses 24 months of pursuit + 16 days of operations into the seller's substrate. Audience: AT&T board, LA28 leadership, Wave-2 anchor candidates, the Microsoft platform team, Deloitte's M&P Leader.
2. **### Wave-2 syndication — T-Mobile · Verizon · Charter · Lumen** — the conversation each carrier has been pre-warmed for since M1. The case study IS the credibility currency.
3. **### Framework-level scaling** — what changes when the pack becomes templatised. The Acceleration Framework's productized-density argument lands here.
4. **### What the regulator saw** — the audit-chain replay capability tested during the Games window. The regulator-readiness story.
5. **### Cross-Practice handoffs** — Toyota → other OEMs (Wave-2 AXLE); Walmart → other retailers (Wave-2 RC); CVS → other pharmacies (Wave-2 HLS). The plays propagate.
6. **### The Independence-minded close** — Deloitte's posture through 24 months. *"Microsoft platform engagement"* language held. Independence pre-clears maturity. The brand strength after the Games.
7. **### What Rashmi and Keven each carry forward into the next pursuit** — Rashmi on cross-Practice coordination; Keven on Microsoft platform engagement. The series sign-off.

**Reading** — Rashmi recommends a piece on **post-pursuit case-study discipline** — Geoffrey Moore on tornado-phase scaling, or a tech-industry post-anchor-deal scaling essay.

**Disagreement** — Keven: the case study is the salesperson — lead with what AT&T got. Rashmi: the case study is the framework-credibility play — lead with what shipped. They converge on dual case studies — an AT&T-buyer version and a framework-credibility version, sharing data, audience-tuned framings.

**Carry-forward** — three series-finale takeaways: (1) Wave-1 anchor + LA28 win IS the proof point for Wave-2 syndication; (2) Microsoft platform engagement language held for 24 months — the Independence brand is intact; (3) the case study IS the salesperson — make it travel.

**Length:** 5,400–6,400.

**Verify + Commit.** Markers add: `Wave-2` · `T-Mobile` · `Verizon` · `Charter` · `Lumen` · `case study`. Commit: `feat: LA28 podcast — episode 09 the wrap · case study + Wave-2 (M8)`.

---

## Task 11: Final verification

**Files:** verify only.

**Step 1: Structural + content discipline verification**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-la28-olympics-telco"
python -c "
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
files=sorted(f for f in os.listdir('.') if f.endswith('.md'))
assert len(files)==10, f'expected 10 md files, got {len(files)}'
assert files[0]=='00-show-bible-and-format.md'
needed=['## Cold Open','### A reading I want to do','### One disagreement','### What to carry forward','## Further reading']
# Case-insensitive phrase forbids (Independence + commercial-instrument hygiene)
forbidden_ci=['co-sell','channel partner','strategic partnership','alliance partner','co-investment','joint-motion','joint motion','pull-through']
# Case-sensitive acronym/name forbids (avoid 'specific'/'Pacific' false positives for ECIF; lock out legacy Marcus)
forbidden_cs=['ECIF','MACC','Marcus','MARCUS']
total=0
print(f'{\"file\":<60} {\"words\":>6} {\"runtime\":>7}')
print('-'*78)
for f in files[1:]:
    t=open(f,encoding='utf-8').read()
    for s in needed: assert s in t, f'{f}: missing {s}'
    for s in forbidden_ci: assert s.lower() not in t.lower(), f'{f}: forbidden phrase {s}'
    for s in forbidden_cs: assert s not in t, f'{f}: forbidden token {s}'
    assert '**RASHMI:**' in t and '**KEVEN:**' in t, f'{f}: missing host markers'
    spoken=re.sub(r'\[[^\]]*\]','',t)
    spoken=re.sub(r'^#{1,6} .*\$','',spoken,flags=re.M)
    spoken=re.sub(r'\*\*(RASHMI|KEVEN):\*\*','',spoken)
    wc=len(spoken.split())
    total+=wc
    assert 4800<=wc<=7500, f'{f}: word count {wc} out of band'
    print(f'{f:<60} {wc:>6} {wc/145:>5.1f}m')
print('-'*78)
print(f'{\"TOTAL (9 episodes)\":<60} {total:>6} {total/145:>5.1f}m')
# Required anchor-partner names appear somewhere in the series
all_text='\n'.join(open(f,encoding='utf-8').read() for f in files)
required_anchors=['AT&T','LA28','NBCUniversal','Walmart','American Airlines','Marriott','Toyota Connected','AutoNation','Progressive','Microsoft platform engagement']
for a in required_anchors:
    assert a in all_text, f'missing required anchor reference: {a}'
print('all required anchors present')
print('content discipline clean')
"
```

**Step 2: Commit (if fixes were needed)**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git commit -am "fix: LA28 podcast verification fixes" || echo "no fixes needed"
```

---

**End of plan.** 11 tasks. Estimated effort: ~3–4 hours (show bible + 9 ~5,800-word episodes + verification).
