# The APEX Deployment Podcast · `pc-deploymentguide`

A six-episode audio companion to **Volume III of the APEX Trilogy** — the *Professional APEX-M Deployment Guide* (`/docs/book/Professional-APEX-M-Deployment-Guide.html`). Produced in a deliberately conversational style — closer to *The Acquired* podcast at its loosest than the Sellers or Services Podcast versions.

> **Companion series:** Third volume of the audio Trilogy. Sellers Podcast (`pc-sellersguide/`) covers how to win the deal. Services Podcast (`pc-servicesguide/`) covers how to design and build it. This one covers how to *deploy and run* it.

---

## What's different about this series

The Sellers and Services Podcasts had a tendency to *read the source guide aloud* — citing chapter and section numbers, walking the table of contents, reading aggregated summaries. That format is informative but doesn't sound like a podcast — it sounds like an audiobook of a reference document.

This series is built differently:

- **No chapter or section numbers in spoken dialogue.** The hosts know the framework cold; they don't recite its index. If the source needs to be pointed to, it's *"there's a paragraph in the guide I want to read you"* — followed by an actual reading and reaction.
- **Story-led, not topic-led.** Each episode opens with a specific deployment moment — a named (anonymised) tenant, a real failure, a Sunday at 11 PM — and the architectural points emerge from the story.
- **The hosts disagree for real.** Not interview format. Two practitioners who think differently about how production should run.
- **One big idea per episode.** Not "walk the chapter." One architectural argument, developed across 25–30 minutes.
- **Pace is slower.** Tangents that earn their length. Quotes from the guide. Personal anecdotes with specificity.

---

## The hosts

**Keven** *(the practitioner)*
Continuity host across all three Trilogy podcasts. Same Andrew voice. Knows the framework from pursuit through delivery through production. On this podcast, when he says "I was in the room," he means the war room — not the boardroom.

**Sam** *(the platform engineer)*
Senior platform engineer. Has stood up APEX deployments at four different tenants. Has been paged at 3 AM for one of them. Plays the role of *"OK but in production, this is what actually breaks at scale."* Sam is not a delivery architect (that was Morgan in the Services Podcast) — Sam runs the platform after delivery is done.

The dynamic: Keven thinks in patterns. Sam thinks in incidents.

---

## The six episodes

| # | Title | Source coverage | Centered on |
|---|---|---|---|
| 01 | **From Demo to Deployable** | Part I — Foundations of Deployment | Why deployment is its own discipline; the three-layer cake; substrate-aware architecture; the Independence posture when you're in the production chair |
| 02 | **The Platform Foundation** | Part II — Layer 1: APEX Platform (anatomy + identity + audit trust + network) | Identity, secrets, audit trust as the floor everything stands on. The architectural reason platform layer exists. |
| 03 | **Building the Tenant** | Part II concrete chapters + Part V Day-Zero | The actual Day-Zero motion — bringing up Fabric, Entra, Purview, Sentinel as one coordinated stand-up, not four separate projects |
| 04 | **Service and Agent Layers** | Parts III + IV combined | Deployable Services, multi-Service tenants, agents as immutable images, RAI controls, versioning |
| 05 | **The Motion** | Part V (Deployment Motion) | Adding Services to a live tenant, agent upgrades across clients, rollback discipline, the pre-deployment security gate |
| 06 | **Day-Zero, Day-2, Chaos** | Part VI — Practitioner Tracks + series close | Production discipline — chaos engineering, walkthrough, CI/CD, FinOps, Day-2 ops, surfacing in M365 and Power Platform |

Target run time: ≈ 3 hours total. Each episode is a self-contained conversation, not a chapter summary.

---

## How this differs from the other two Trilogy podcasts

| Dimension | Sellers Podcast | Services Podcast | Deployment Podcast |
|---|---|---|---|
| Audience | Sellers, account leads | Solution architects, engagement leads | Platform engineers, SREs, ops leads, change managers |
| Second host | Jordan — strategist/skeptic | Morgan — delivery architect | Sam — platform engineer who's been on call |
| Skepticism style | "But the CFO will ask…" | "But on day fourteen of build…" | "But at 3 AM on a Sunday when the agent is throwing 429s…" |
| Voice cast | Andrew + Brian (both male) | Andrew + Emma (m + f, conversation-tuned) | Andrew + Ava (m + f, conversation-tuned, different texture from Emma) |
| Format | Acquired-style segments (Cold Open · APEX Facts · Adopt/Hold · Lessons · Carve Outs) | Same segments | **Conversational throughout — segments emerge organically, not announced** |
| Dominant texture | Pursuit prep | Architecture & build prep | War-room prep |

---

## Files in this folder

```
pc-deploymentguide/
├── README.md                        ← you are here
├── 00-show-bible-and-format.md      ← format spec + house style (conversational rules)
├── 01-from-demo-to-deployable.md    ← Episode 1
├── 02-the-platform-foundation.md    ← Episode 2
├── 03-building-the-tenant.md        ← Episode 3
├── 04-service-and-agent-layers.md   ← Episode 4
├── 05-the-motion.md                 ← Episode 5
├── 06-day-zero-day-two-chaos.md     ← Episode 6
└── _build_audio.py                  ← TTS pipeline (Keven=Andrew, Sam=Ava)
```

After audio generation, an `audio/` subfolder appears with the six MP3s and a folder-level README.

---

*The implied listener: a platform engineer or SRE who's about to onboard a client tenant for the first time, or who's been running one and wants to compare notes. The audio is them and a more-experienced colleague driving to the airport together, talking shop.*
