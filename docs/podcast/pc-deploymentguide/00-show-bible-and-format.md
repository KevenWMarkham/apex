# Show Bible · The APEX Deployment Podcast

This document defines the format and house style for the six-episode deployment-side series. Read it before producing or narrating any episode. The shift in style from the prior two Trilogy podcasts is intentional and substantial — read this carefully.

---

## 1. The core shift — conversation, not chapter walk

The Sellers Podcast and Services Podcast both adopted a *guided-tour* approach to the source guide:

> **KEVEN:** Chapter Five. *The Real-Time Hub pattern.* Five sections. Let me hit them. Section five point one — the RTI components. Eventstream — the ingestion. Eventhouse — the KQL queryable store…

That format is informative but sounds like an audiobook. It's the host *reading the source aloud* with light reactions.

The Deployment Podcast deliberately rejects that pattern. Instead:

> **KEVEN:** So the thing I keep coming back to with streaming in APEX — most teams get the *components* right and the *teeing* wrong.
>
> **SAM:** Wait — teeing?
>
> **KEVEN:** Yeah. Picture it. Events coming in. The engineer's looking at this saying — *do I send these to Eventhouse so I can query them, or do I land them in OneLake so the batch jobs see them?* And they argue about it for a sprint. And the answer is — you don't pick. You tee.
>
> **SAM:** [laughs] I have *literally* had that argument. Three weeks. Two engineers, one whiteboard.

Same content. No section numbers. Story-led. The architecture emerges from the conversation about an experience.

---

## 2. The conversation rules

These are not stylistic preferences. They are the operating rules of this podcast.

### Rule 1 · No chapter or section numbers in dialogue

The hosts know the framework. They don't cite it like a study guide. Things they don't say:

- ❌ "Chapter Seven. *PII Classification.* Section seven point one — the four tiers…"
- ❌ "Section three point three — the MCP host…"
- ❌ "Section one B point three is the counterfactuals…"

Things they *do* say:

- ✅ "The PII story in APEX is the thing everybody underestimates…"
- ✅ "The whole point of the MCP layer is — the agent doesn't have a connection string…"
- ✅ "There's a passage in the guide I want to read you because it lands differently out loud…"

When a reading does happen, it's intentional and brief — 30–60 seconds — and both hosts react. Then back to conversation.

### Rule 2 · One big idea per episode

Not "walk Part IV." One architectural argument, developed across the episode. The 25-minute conversation builds toward a synthesis. Listeners should be able to summarise the *thesis* of the episode in one sentence.

### Rule 3 · The hosts disagree for real

Sam is not a yes-man. Sam has run production. Keven has a framework view. They genuinely have different priors and they land on synthesis, not consensus. If an episode has no real disagreement, it's not done.

### Rule 4 · Specificity is everything

- ❌ "I was sitting in a meeting with a CIO…"
- ✅ "Tuesday before Memorial Day. Plano. The CIO's office. Yellow legal pad on the table. Empty Diet Coke can. He'd been up since five."

Specificity is a credibility signal. It's also what makes audio listenable.

### Rule 5 · Quote the guide as a *moment*

Once or twice per episode — not more — one host has a passage they want to read aloud. They name why: *"There's a paragraph in the deployment guide I want to read you because every time I re-read it, I find something new."* They read it. Both react. The reading is *the moment*, not a citation.

### Rule 6 · Tangents that earn their length

Acquired earns its three-hour episodes by letting tangents breathe. Our 25-minute episodes can afford one or two real tangents — they tie back. The tangent should *change* what you hear next, not just decorate it.

### Rule 7 · Drop the announced segments

The Sellers and Services Podcasts had explicit segment announcements — *"OK, time for APEX Facts."* This podcast doesn't do that. The rhythms still exist — recap, fact-trade, debate, synthesis — but they happen *because the conversation moves there*, not because someone announces them.

If the structure feels needed, use it lightly:
- A brief "OK so where does that leave us" moment serves as synthesis without announcing one.
- A "here's the thing I'd put in the notebook" moment serves as a lesson without announcing one.

### Rule 8 · Slow the pace

Acquired episodes have *silences*. Pauses. Hosts thinking aloud. Mid-sentence reconsiderations. *"Hmm, actually — let me come at that differently."* This is impossible to fake with text-to-speech, but the script can write the conversational gestures that imply it — half-finished thoughts, "wait, back up," "no, actually…", filler words used purposefully.

---

## 3. The voices

| Host | edge-tts voice | Why |
|---|---|---|
| **Keven** | `en-US-AndrewNeural` | Continuity across the Trilogy. Conversation/Copilot family. |
| **Sam** | `en-US-AvaNeural` | "Expressive, Caring, Pleasant, Friendly." Conversation/Copilot family — same natural register as Keven, female voice for vocal contrast. Different from Emma (Services Podcast) — Ava reads warmer, more involved, more "I care about the platform" energy. |

The Sellers Podcast was Andrew + Brian (both male). The Services Podcast was Andrew + Emma. The Deployment Podcast is Andrew + Ava. Each Trilogy volume has its own audio signature so the listener always knows which show they're in.

---

## 4. Sam's character — production-experienced

Sam isn't a delivery architect. Sam runs the platform *after* delivery is done. The persona:

- Has stood up multiple APEX tenants
- Has been paged for a real incident on at least one
- Lives with the consequences of architectural decisions made earlier in the engagement
- Has strong opinions about what's *operable* versus what's *theoretically correct*
- Is not afraid to say *"that pattern is great on paper but doesn't survive Day-90"*

Sam's interruptions are the *operator interruptions* — "what does that look like at 3 AM," "who carries the pager for that," "is that an incident or a ticket."

Keven respects Sam. The conversation has the texture of two senior practitioners who've worked together before and trust each other to push back.

---

## 5. The recurring rhythms (not segments)

Each episode has these *rhythms* but doesn't announce them:

| Rhythm | What it does | How long |
|---|---|---|
| **Opening scene** | A real (anonymised) deployment moment — named tenant, specific time, specific stakes | 3–5 min |
| **The argument** | The episode's one big idea, developed through conversation | 15–18 min |
| **The reading** | One or two passages from the guide, read aloud, reacted to | 1–2 min |
| **The disagreement** | A specific point where the hosts genuinely diverge, then converge | 3–5 min |
| **The takeaway** | What stays with the listener — not announced, just lands | 1–2 min |

Total: ~25–30 minutes per episode at conversational pace.

---

## 6. House style additions specific to deployment content

- **Tenant names are anonymised by archetype.** *"The Tier-1 telecom we onboarded last summer…"* — never the company name.
- **Production failures are described with respect.** The team that broke something is not the villain of the story; the architecture or the gap is.
- **The Independence-from-Microsoft posture carries over.** Deloitte doesn't co-sell. We *recommend* the Microsoft platform on the merits. Audio language reflects this without belabouring it.
- **Sam reads from operational artefacts** (runbooks, incident postmortems, alert thresholds) the same way Keven reads from the guide. Reading from a real artefact is a credibility move.

---

## 7. Length discipline

25–30 minutes per episode. 4,500–5,200 words at conversational pace. Cut the opening scene first if the script runs long. Never cut the disagreement or the reading.

---

## 8. The implied listener

A platform engineer or SRE who's been handed an APEX tenant onboarding and is preparing for it on Sunday night. They want the *operator's gloss* — what's worth memorising, what's worth re-reading, where the rough edges are.

Treat them like a peer. Don't perform. Talk to them.
