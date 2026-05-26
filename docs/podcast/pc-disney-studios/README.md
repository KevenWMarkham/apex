# The Disney Studios Account Podcast · `pc-disney-studios`

A **five-episode** internal Account Team podcast for the Deloitte team working **The Walt Disney Studios** business and its component studios — **Walt Disney Pictures · Pixar · Marvel Studios · Lucasfilm · 20th Century Studios · Searchlight Pictures.**

Built on top of the APEX Trilogy podcasts and parallels the Disney Account Podcast (`pc-disney-account/`) and DTNA Account Podcast (`pc-dtna-account/`) structure. **Account-specific to the Studios business** — distinct from the Disney Account Podcast's company-wide framing.

> **Internal use only.** This podcast names the studios directly because it's internal Deloitte Account Team preparation.

---

## Why this podcast exists

The Disney Account Podcast covers Disney across all three operating segments — Entertainment, Sports, Experiences. *The Studios business is one corner of Entertainment.* It has distinctive economics, distinctive talent dynamics, distinctive operational rhythms, and distinctive technology-investment patterns that don't appear cleanly in the company-wide podcast.

Specifically, the Studios business is structurally different from the streaming and parks businesses because:

1. **Content economics are project-by-project.** Each film or series is a discrete production with its own greenlight decision, budget, schedule, and risk profile. Streaming and parks are continuous-operations businesses; Studios is a portfolio-of-bets business.

2. **Hit/miss volatility dominates.** A single tentpole that misses can wipe out a year of margin for a studio. Conversely, a hit can fund the next slate. Risk management at the title level is structural.

3. **Talent compensation and rights are complex.** Above-the-line talent (lead actors, directors, writers, showrunners), residuals, music synchronization, IP rights, and union agreements (WGA, SAG-AFTRA, DGA, IATSE) shape the cost structure and the operational workflow.

4. **The VFX and animation pipelines are long-cycle.** Pixar's animation cycle is 4-5 years per feature. Marvel's VFX-heavy productions stretch 18-24 months in post. The pipeline is the bottleneck.

5. **Marketing economics rival production economics.** Theatrical marketing spend for a tentpole can equal or exceed production spend. Trailer testing, premiere strategy, awards campaigns are all decision-heavy.

6. **Windowing decisions are strategic.** Theatrical-only vs. theatrical-plus-streaming vs. streaming-direct decisions reshape revenue, marketing, and talent relationships.

Each of these areas has agentic-AI applications that are *specific to the studios business* and don't map cleanly to the streaming-and-parks playbook.

---

## The hosts

**Keven** *(the practitioner)* — `en-US-AndrewNeural` · Trilogy continuity host.

**Eden** *(the senior entertainment-account partner)* — `en-US-AvaMultilingualNeural` · 12+ years on entertainment, studio, and content-production accounts. Has been in production-office meetings on the Burbank lot, walked the Pixar campus in Emeryville, sat in Marvel Studios development sessions. Plays the role of *"OK but how the President of [Studio] actually thinks about this is…"* — keeps the conversation grounded in studio-specific operational reality.

This is the sixth distinct voice pairing in the podcast family:

| Podcast | Pairing |
|---|---|
| Sellers | Andrew + Brian |
| Services v2 | Andrew + Emma |
| Deployment | Andrew + Ava |
| Disney Account (company-wide) | Andrew + Emma Multilingual |
| DTNA Account | Andrew + Brian Multilingual |
| **Disney Studios (this)** | **Andrew + Ava Multilingual** |

---

## The five episodes

| # | Title | Centered on |
|---|---|---|
| 01 | **The Disney Studios Account** | Strategic context · six studios under Disney Entertainment · the content economics of theatrical vs streaming · current strategic pressures (cost inflation, hit/miss volatility, windowing, talent) · why APEX *now* for studios |
| 02 | **Content Development & Greenlight Plays** | IP/franchise opportunity scoring · greenlight decision support · audience science (preview testing, sentiment) · talent and casting intelligence · pitch and development packet generation |
| 03 | **Production Plays** | Production schedule and budget intelligence · VFX pipeline optimisation · Pixar animation pipeline · post-production workflow · production safety and wellness · localisation production planning |
| 04 | **Marketing, Distribution & Rights Plays** | Trailer performance and audience testing · marketing campaign optimisation · theatrical-vs-streaming windowing · awards campaign management · rights compliance and content reuse · music synchronisation clearance |
| 05 | **The Ladder for Disney Studios + Account Team Playbook** | L1 wedge across the six studios · L2 Wave 1 · L3 Studios-wide CoE · L4 transformation · 30-Min Framework studio-tuned · Independence specifics · 90-day calendar |

Total run time target: ~2 hours 30 min.

## Companion artefact

**`Disney_Studios_Agentic_Plays.xlsx`** — 15 curated plays across Content Development, Production, Marketing & Distribution, and Rights & Licensing. Three sheets: Plays · Summary · How To Use.

---

## How this podcast relates to the Trilogy and other account podcasts

```
Sellers Podcast (general framework)  ───┐
                                          ├──> Disney Account Podcast (company-wide TMT-MED)
Services Podcast (delivery architecture)─┤
                                          ├──> Disney Studios Podcast (this · studios-specific)
Deployment Podcast (operations)         ─┤
                                          └──> DTNA Account Podcast (AXLE)
```

Specific cross-references:

- **Sellers Podcast Ep 4** — *The Seven Industries* — defines TMT-MED as the Practice this account sits within
- **Disney Account Podcast Ep 1** — *The Disney Account* — covers Disney's three segments and the company-wide strategic frame
- **Disney Account Podcast Eps 2-3** — *CX Six and Operations Eight* — cover streaming and operations plays; *Studios is the other Entertainment sub-business*
- **Services Podcast Ep 5** — *The Retail Margin Squeeze* — the loyalty / customer retention pattern; relevant for the audience-science play
- **Services Podcast Ep 11** — *The Contact-Center Labour Squeeze* — the agent-assist pattern; relevant for VFX-pipeline-coordination and post-production-workflow plays

---

## The six Disney Studios in scope

| Studio | Headquarters | Primary product |
|---|---|---|
| Walt Disney Pictures | Burbank, CA | Disney-branded family theatrical features |
| Pixar Animation Studios | Emeryville, CA | Animation features (long cycle) |
| Marvel Studios | Burbank, CA | Marvel Cinematic Universe theatrical + Disney+ originals |
| Lucasfilm | San Francisco, CA | Star Wars theatrical + Disney+ originals |
| 20th Century Studios | Century City, CA | Mass-market theatrical (post-Fox acquisition) |
| Searchlight Pictures | Beverly Hills, CA | Specialty / awards-focused theatrical |

Plus the related TV studios (ABC Signature, 20th Television, Touchstone Television, etc.) which sit alongside the film studios under Disney Entertainment.

---

## Files in this folder

```
pc-disney-studios/
├── README.md                                       ← you are here
├── 00-show-bible-and-format.md                     ← format + Studios-specific style notes
├── 01-the-disney-studios-account.md                ← Episode 1
├── 02-content-development-and-greenlight.md        ← Episode 2
├── 03-production-plays.md                          ← Episode 3
├── 04-marketing-distribution-rights.md             ← Episode 4
├── 05-ladder-and-playbook.md                       ← Episode 5
├── Disney_Studios_Agentic_Plays.xlsx               ← 15-play curated artefact
└── _build_audio.py + _build_music.py + _apply_music.py + _build_plays_xlsx.py
```

---

*The implied listener: a member of the Deloitte Account Team working the Disney Studios sub-business — partner, senior manager, manager, senior consultant — who is preparing for a Studios-leadership conversation and wants the* studio-specific *application of APEX without re-listening to the company-wide podcast.*
