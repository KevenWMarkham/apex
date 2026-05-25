# The CFMP Podcast — Show Bible & Format

**Series:** The CFMP Podcast — *Customer Focused Merchandise Pack on the Acceleration Framework*
**Owner:** kmarkham@deloitte.com · Deloitte MS Technology & Services Practice
**Date:** 2026-05-25
**Status:** Canonical format guide · every episode follows the rules below.

---

## What this series is

An eight-episode scripted, two-host conversational podcast on the **Customer Focused Merchandise Pack (CFMP)** — the agent-powered, multi-surface grocery and loyalty system Deloitte has designed for clients on the Microsoft platform. The series teaches the design from first principles: who it's for, what it is, how it's built, why it's safe, and how a Microsoft seller positions it.

**One-line pitch.** *Grocery is the universal jobs-to-be-done. CFMP turns it from a chore into a managed system, on a vendor-neutral architecture (the Acceleration Framework) productized on Microsoft (APEX-M).*

**The unifying noun** is the **LOT** — a shopping trip, an auto-replenish, a stay-trip to the cabin, a care-trip for a parent. Every concept in the series stair-steps from the lot.

**The headline interaction** is **SCAN** — you scan to find, you scan to add, you scan to confirm.

**The intelligence** is the **agent fleet** — a parent orchestrator and a fleet of specialist children (Trips, Replenish, Coupons, Pharmacy, Concierge).

**The trust** is the **APEX audit chain** — every action is a row.

## Audience

Two audiences served by one arc:

1. **The CFMP project team and new hires.** The series doubles as onboarding. A new engineer or designer who listens to all eight episodes understands why every concept exists, who shaped each decision, and what tradeoffs were considered.
2. **Deloitte Account Teams positioning CFMP.** The series is pivotable to a client conversation — discovery openers, honest claims, pushback handling, the architectural pitch. Episode 8 is built directly for the field.

Every episode includes both framings — architecture-honest enough for the team, seller-pivotable for the field.

## Hosts

Two recurring hosts, carried forward from the Cross-Cloud Agentic series for brand continuity.

### Keven — Microsoft platform practitioner
- 22 years on the Microsoft platform; VP of Deloitte's Microsoft Technology & Services Practice.
- Knows the productization story end to end — Fabric, Foundry, Purview, Entra, Cost Management.
- Positions CFMP on **APEX-M** (Microsoft's productized realization of the Acceleration Framework).
- Voice: warm, confident, specific. Names products. Cites real numbers. Earns the recommendation; never claims more than the design delivers.
- Pet phrases: *"productized-capability density"*, *"the architecture decides; the cloud follows"*, *"earn the recommendation on merits"*.

### Reid — cross-cloud principal architect
- Cross-cloud architect; has built on AWS, GCP, and Microsoft at scale.
- The **honesty enforcer**. Pushes back the moment a claim cannot be defended.
- Names where AWS or GCP would do it differently — and where they would do it better.
- Voice: dry, precise, deliberate. Quotes the design doc back when Keven drifts. Asks the hard architecture question.
- Pet phrases: *"name the axis"*, *"what does the audit row prove?"*, *"if the model deprecates tomorrow, what happens?"*.

The dynamic: Keven leads with the design; Reid sharpens it; the listener gets a defended position, not a marketing argument.

## Episode arc

| # | Title | What it covers |
|---|---|---|
| 01 | Sarah's day — the customer problem CFMP exists to solve | Persona-led why; the five archetypes; the LOT noun; the SCAN interaction; success metrics |
| 02 | The agent fleet & the APEX audit chain | Architecture spine; gpt-5-mini parent/child; the LedgerRow; trace-ID propagation; the Azure deployment topology anchored on the live `/architecture` page |
| 03 | Mobile · SCAN & LOT | The lot model in depth; the four lot archetypes; scan-first design; the MCP boundary on Mobile |
| 04 | Mobile · Trips, Replenish, and the home channel | Trip life-cycle; auto-replenish; the home channel; preferences; UI revamp |
| 05 | Portal · operator console & B2B multi-tenant | The Portal as seller artifact; deep walk-through of the live `/architecture` page; chat panel; vision-kit integration; retailer multi-tenant |
| 06 | Sonos · the ambient voice channel | Voice as a peer channel; the Cue, the Cue Bus, the Zone; ducking; AirPlay-bridge fallback; Azure-native deployment |
| 07 | Identity, consent, HIPAA & senior accessibility | Four-identity chain; Adebayo on consent; Chen on HIPAA gating; Yamamoto on senior accessibility; Russo on AirPlay audit-tagging |
| 08 | The seller's playbook — CFMP on APEX-M | The architectural pitch; six discovery openers; honest claims and overclaims; pushback handling; the roadmap; the close |

## Episode format

Every episode follows this structure:

```
# <Episode title>

**Episode <NN> · <Title>** — short header with kicker

## Cold Open
A moment-in-the-day vignette (200–500 words) drawn from the design docs.
Keven and Reid open the episode on this moment.
Sets up the architectural payoff.

## The conversation

### <Section 1 title>
…
### <Section 2 title>
…
(5–8 sub-sections in this block)

### A reading I want to do
Reid recommends an outside reading that sharpens the episode's argument.
Brief — 1–2 paragraphs.

### One disagreement
Keven and Reid surface a real disagreement, model it honestly,
and either converge or name where they remain apart.

### What to carry forward
The 2–3 durable takeaways the seller / engineer brings into the next conversation.

## Further reading
- **Source docs** — the CFMP design docs this episode draws from
- **Live architecture** — `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture`
- **Microsoft Learn** — relevant Learn URLs
- **Industry / analyst** — external references
```

## Speaker formatting

- Speaker lines: `**KEVEN:**` and `**REID:**` (bold, in caps, with colon).
- Stage directions in `[brackets]` — used sparingly for music cues, pauses, tonal shifts.
- Emphasis with `**bold**` — only on the term being defined or the line being landed.
- No emojis in body text.
- No real client names; the fictional design personas (Sarah, Robert, Diana, Marcus) keep their names; retailers are "the retailer".

## Cold-open style

Every episode opens with a vignette — a real-feeling moment in a persona's day. The personas come from the design docs:

- **Sarah Chen** — power-user parent; the cook.
- **Robert Park** — senior shopper; the steady eddie.
- **Diana Park** — caregiver; the proxy (drops in on Robert).
- **Marcus Thompson** — the cabin/StayLot user.
- **An operator** — for the Portal episode.

The cold open lands a concrete moment, then Keven and Reid open the episode on it. The architectural payoff is named within the first two minutes — but the moment leads.

## Recurring elements (formulas)

### "A reading I want to do" (Reid)
A real outside reading — analyst note, book, paper, framework — that sharpens the episode's argument. One per episode. Reid is the recommender; Keven sometimes pushes on whether it actually lands. Keep it to 1–2 short paragraphs.

### "One disagreement"
Exactly one per episode. Keven and Reid surface a real architecture or product tradeoff. Two patterns:
- **Converge** — they reach a defended position together (most episodes).
- **Name as unresolved** — they leave it as an honest open question (1–2 episodes max in the series).
The disagreement is never manufactured. If the design has a real tension, name it.

### "What to carry forward"
2–3 durable takeaways. Numbered or bulleted. The seller and the engineer each get something they can use Monday morning. Closes the episode on a hand-off, not a wrap-up.

## Content discipline

These rules are non-negotiable:

- **No real client names.** The retailer is "the retailer" (not Kroger, Walmart, Target, Costco, Safeway, Albertsons, Wegmans, Publix, Amazon Fresh, Instacart, or any other real brand).
- **Fictional design personas keep their names.** Sarah Chen, Robert Park, Diana Park, Marcus Thompson — these are design personas, not real people.
- **The framework is "the Acceleration Framework".** APEX is its productized realization on Microsoft. CFMP is the application built on top.
- **APEX-M** is acceptable as the Microsoft-specific realization of APEX for the CFMP delivery.
- **Forbidden vocabulary:** *co-sell · alliance · strategic partnership · channel partner · alliance partner*. None of these on tape.
- **Independence-minded posture.** Recommendations are made on technical and economic merits. Honest where AWS or GCP would lead.
- **Two-contract model** when the commercial arc is mentioned — the customer contracts directly with the platform vendor and directly with Deloitte; no margin stacking.

## Azure deployment thread

Every episode names the Azure realization of the surface it covers:

- **Container Apps in East US 2** — `ca-visionkit-mobile` (the PWA), `ca-visionkit-portal` (the operator console), `ca-visionkit-orchestrator` (the agent fleet host).
- **Azure Speech** — neural voices for the Sonos channel (`en-US-AvaMultilingualNeural` default, `en-US-AndrewNeural` for alerts).
- **Blob storage** — `stapexdemo50097` storage account, `audio-out` container, 15-minute SAS URLs.
- **Postgres** — the state store (lots, profiles, ledger Bronze tier).
- **Entra** — identity and OAuth.
- **Sonos Cloud Control API** — external integration to `control.api.sonos.com`.

The **live `/architecture` page** is the canonical visual reference for the deployment:

```
https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io/architecture
```

Episode 2 (Agent fleet & audit chain) anchors the deployment topology — Reid walks the page while Keven narrates how a regulator's replay question lands a trace across exactly these services. Episode 5 (Portal) features the page as the seller's screen-share artifact — "open this URL on a client call, and the architecture argument is already on the screen." Every other episode names the Azure surface it lives on and cites the URL in **Further reading** under a "Live architecture" entry.

## Voice cast (for deferred audio production)

When audio production is approved separately, the planned voices are:

- **Keven** — a warm, mid-range female neural voice (revisit choice at audio time; the prior series uses Aria for parity).
- **Reid** — `en-US-AndrewMultilingualNeural` (carried over from the Cross-Cloud Agentic series for continuity).
- **Opening sting** — ~5 seconds, mirroring the sibling series.
- **Closing sting** — ~6 seconds, same family.

Runtime target per episode: **38–42 minutes** (±5 min acceptable) at ~145 wpm. Word target: **5,200–6,500 spoken words** per episode (excluding `## Further reading`).

## Pacing rules carried from the sibling series

- **No dogpiling.** One section makes one point; the next section makes the next.
- **Single disagreement** per episode — resolved or named-as-unresolved.
- **Every episode ends on carry-forward** — never on a wrap-up.
- **Vignette-first.** The cold open is a moment, not an abstract framing.
- **Honest about where Microsoft doesn't lead.** This is the credibility currency of the whole series.

## Sign-off

The series sign-off line (Episode 8 only): *"See you in the field."*

— end of show bible —
