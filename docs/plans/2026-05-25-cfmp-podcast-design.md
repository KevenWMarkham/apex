# CFMP Podcast — Design

**Date:** 2026-05-25
**Status:** Design approved · ready for writing-plans handoff
**Owner:** kmarkham@deloitte.com · Deloitte MS Technology & Services Practice
**Output location:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cfmp\`
**Source material:** `C:\code\iot_device\docs\packs\` — CFMP-Mobile-Design-Document.md, CFMP-Sonos-Design-Document.md, CFMP-Mobile-Use-Cases.md, CFMP-Mobile-Shopper-Experts.md, CFMP-Mobile-All-Experts-Panel.md, CFMP-Mobile-Roadmap.md, CFMP-Sonos-UC-Catalog.md, CFMP-Sonos-Roadmap.md, plus the Mobile and Sonos sprint orchestrators and expert focus docs.

## Goal

An 8-episode audio-first podcast series on the Customer Focused Merchandise Pack (CFMP) — the agent-powered, multi-surface grocery & loyalty system Deloitte's MS Technology & Services Practice has designed on APEX-M. The series serves two audiences in one arc: the CFMP project team and new hires (architecture-honest onboarding) and Deloitte Account Teams positioning CFMP with Microsoft platform clients (seller-pivotable framing).

## Series identity

- **Format:** 8 episodes, 35–45 minutes each, two-host conversational, scripted.
- **Hosts (continuity with the Cross-Cloud Agentic series):**
  - **Keven** — the Microsoft platform practitioner; 22 years on Microsoft; positions CFMP-on-APEX-M; lands the seller pivot.
  - **Reid** — the cross-cloud principal architect; pushes back whenever a claim cannot be defended; the honesty enforcer on design tradeoffs and where AWS / GCP would do it differently.
- **Brand:** "the Acceleration Framework" is the framework name on-tape; APEX-M is the productized realization. CFMP is the application pack the series teaches.
- **Tone:** confident, grounded, opinionated where the design is opinionated, honest where the design has tradeoffs.
- **Cold-open style:** every episode opens with a moment-in-the-day vignette (Sarah, Robert, Diana, Marcus) drawn from the design docs, then the architectural payoff.

## Episode arc

| # | Title (working) | What it covers | Primary docs |
|---|---|---|---|
| 01 | **Sarah's day — the customer problem CFMP exists to solve** | The persona-led why · the five archetypes · the unifying noun (LOT) · the headline interaction (SCAN) · how success is measured | Mobile §1–2, Shopper-Experts |
| 02 | **The agent fleet & the APEX audit chain** | The architectural spine · the agent fleet (gpt-5-mini) · the LedgerRow · trace_id propagation · why "every action is a row" is the trust substrate | Mobile §5, Sonos §4.8, APEX |
| 03 | **Mobile · SCAN & LOT** | The unifying noun and the headline interaction · ScanFirst design · the lot model · UCs at the centre | Mobile §4, ScanFirst-Design, Lots-Expert-Focus |
| 04 | **Mobile · Trips, Replenish, and the home channel** | The four primary surfaces of Mobile · trip life-cycle · auto-replenish · the home channel · Preferences | Mobile §3, §6–7, Preferences-Expert-Focus, UI-Revamp |
| 05 | **Portal · operator console & B2B multi-tenant** | The Portal — what it is and who uses it · architecture view · retailer multi-tenant · SOC 2 scope (Liu) · operator workflows | Mobile §5 (Portal touchpoints), and the Portal endpoints referenced in both docs |
| 06 | **Sonos · the ambient voice channel** | Why a speaker · the Voice Channel as peer · the Cue, the Cue Bus, the Zone · ducking and cadence · AirPlay-bridge resilience · Azure-native deployment | Sonos §1–8, Sonos-UC-Catalog |
| 07 | **Identity, consent, HIPAA & senior accessibility** | The cross-cutting quality layers — Adebayo on consent, Chen on presence-gated drug names, Yamamoto on the speaker as the senior interface, Russo on AirPlay audit-tagging | Mobile §8, Sonos §8 |
| 08 | **The seller's playbook — CFMP on APEX-M** | Positioning CFMP for an Account Team · the six discovery openers · the engagement envelopes · roadmap · the close | Mobile §9, Sonos §9, Roadmaps |

Each episode includes: a cold open, the conversation in five-to-eight sections, a "reading I want to do" (Reid), a "one disagreement" (modeled honestly), and a "what to carry forward".

## Audience framing

Two audiences served by one arc:
- **CFMP project team & new hires.** The series doubles as onboarding — the personas, the architecture, the design decisions, the expert cast. A new engineer or designer who listens to all 8 episodes knows why every concept exists.
- **Deloitte Account Teams positioning CFMP.** The series is pivotable to a client conversation — the openers, the value framing, the architecture-first move that earns the platform recommendation. Episode 8 is built for them.

## Azure deployment architecture — a thread through the series

Every episode names the Azure realization of the surface it covers. The live `/architecture` page — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture` — is the **canonical visual reference** for the seller; it shows the Azure Container Apps topology (mobile, portal, orchestrator), Azure Speech, Blob storage, Postgres, the agent fleet, the APEX audit chain, the Sonos Cloud Control API as an external integration, and the East US 2 region. The series uses this page as:

- **Episode 2's deployment-topology anchor** — Reid screen-shares the page (in the visual companion / show notes) while Keven walks through the four-layer stack on Azure-native infrastructure. The cold open's regulator-replay question lands a trace across exactly these services.
- **Episode 5's hero artifact** — the Portal episode features the `/architecture` page directly. Keven describes it as a deliberate seller artifact: "open the URL on a client call, and the architecture argument is already on the screen."
- **A recurring reference in every other episode** — Mobile (3, 4) names `ca-visionkit-mobile`; Sonos (6) names the orchestrator's outbound to `control.api.sonos.com` and the Azure Speech + Blob pipeline; Identity (7) names Entra and the storage of the OAuth refresh token; the Playbook (8) cites the URL as the seller's opening visual.

Each episode includes the live URL in its `## Further reading` block under a "Live architecture" heading.

## Content discipline

- Generic on-tape — no real retailer names; "the retailer" stands in for Kroger and any others mentioned in the source docs. The fictional design personas (Sarah, Robert, Diana, Marcus) keep their names; they are not real people.
- Independence-minded — recommendations on technical and economic merits, honest about where AWS or GCP would lead.
- Forbidden vocabulary: no "co-sell", "alliance", "strategic partnership", "channel partner".
- The framework is "the Acceleration Framework"; APEX is Microsoft's productized realization (named only where the discussion turns to Microsoft attachment). CFMP is the application built on top.
- Two contracts model when the commercial arc is mentioned (consistent with the prior series).

## Deliverable scope

- **In scope now:** 8 episode scripts (`.md`) plus a `00-show-bible-and-format.md` defining hosts, runtime targets, cold-open style, section structure, content discipline, and a recurring-element checklist. Scripts written to the prior series' standard (full dialogue, stage directions, length and pacing matched).
- **Deferred (decide after scripts approved):** audio production — edge-tts voices, stings, ffmpeg assembly, mp3 output (the pattern from `pc-cross-cloud-agentic`). Audio is a meaningful separate effort; defer until the scripts are landed and reviewed.
- **Location:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cfmp\` (matches sibling podcasts in that directory).

## What the show bible defines

- Host voices, recurring patterns, the cold-open formula, the five-to-eight section template, the closing "carry forward" formula.
- The voice cast (deferred audio decision but the bible names the intended voices — Andrew Multilingual for Reid, a paired female neural voice for Keven if revisiting voice choices, matching the prior series for continuity).
- Per-episode runtime targets (~38–42 min each; ±5 min acceptable).
- Pacing rules carried from the Cross-Cloud bible (no dogpiling, single disagreement per episode resolved or named-as-unresolved, every episode ends on a carry-forward).
- The recurring "Reid's reading" / "one disagreement" / "what to carry forward" structure.

## Verification (when implementation runs)

- 9 markdown files exist (`00-show-bible-and-format.md` + 8 episode scripts).
- Each episode has the required structural elements (Cold Open, The conversation, Reid's reading, One disagreement, What to carry forward, Further reading).
- Word counts target ~5,000–6,500 words per episode (~38–42 min at 145 wpm spoken).
- Content discipline check passes: no real-retailer names, no forbidden vocabulary, generic Independence-minded posture intact.
- Source-doc fidelity: every architectural claim traceable to the CFMP-Mobile or CFMP-Sonos design docs.

## Out of scope (YAGNI)

- Audio production (deferred, separate decision after scripts).
- New design content not present in the CFMP source docs — the podcast teaches what is designed; it does not extend the design.
- A separate study guide HTML (the Cross-Cloud series' v1+v2+v3+v3.1+v3.2 study-guide deliverable is its own pattern; CFMP gets one if requested later).
- Per-episode show notes or audiograms — not in scope for v1.

---

**Next:** invoke `superpowers:writing-plans` for the bite-sized implementation plan.
