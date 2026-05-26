# The APEX Services Podcast · v2 · `pc-servicesguide`

A **twelve-episode** audio companion to Volume II of the APEX Trilogy — the *Professional APEX-M Services Guide*. Structured around **business needs**, not chapter walks. Each episode builds on the prior episode — the series is a **stair-step**, not a set of independent tours.

> **v2 design intent.** The original 8-episode version (archived in `archive-v1/` and `archive-v1-audio/`) read too much like a tour of the source guide — citing chapter numbers, listing technical implementations, switching topics every 90 seconds. v2 reorganises around the listener's actual need: *how does APEX address a real business problem.* Each episode opens with historical and industry context, develops one architectural idea fully before moving to the next, and ends with curated external reading.

---

## What's different in v2

| Dimension | v1 (archived) | v2 (this) |
|---|---|---|
| **Organising principle** | Tour the source guide chapter by chapter | Start with a business need; walk strategy → service → KPI |
| **Structure** | 8 self-contained episodes | 12 episodes, stair-step — Episode 8 makes no sense without Episodes 1-4 |
| **Opening** | "Today we're covering Part Two" | Historical + industry context · how we got here · why this pain matters |
| **Pace** | 90 seconds per concept · jumps between topics | 4-6 minutes per concept · fully developed · no topic-switching |
| **Citations** | "Chapter 5A.7 — threshold-to-action mapping" in dialogue | Hosts know the framework; no source-citations in audio. External reading goes in `Further Reading` section of the .md |
| **External resources** | None | Microsoft Learn modules, Tech Community blog posts, Architecture Center, HBR/McKinsey/industry sources cited per episode |
| **Episode coherence** | Each ep is a standalone | Foundation Eps 1-4 set up concepts that business-need Eps 5-11 reference and build on |
| **Total runtime** | ~2 h 30 min | Expected ~5 h |

---

## The hosts

**Keven** *(the practitioner)* · `en-US-AndrewNeural` — continuity host across the Trilogy.

**Morgan** *(the delivery architect)* · `en-US-EmmaNeural` — senior solution architect, brings the "what actually breaks in delivery" lens.

Same voice cast as v1, same conversational chemistry rules. What changes is *what they talk about and how.*

---

## The twelve episodes

### Foundation arc (Eps 1-4) — concepts later episodes depend on

| # | Title | Builds | Foundation laid |
|---|---|---|---|
| 01 | **The Bottleneck Moved** | (none — opener) | Historical macro: dashboards → decisions → agents. Why now. |
| 02 | **Data Flows Beat Data Warehouses** | builds on Ep 1 | The data-first thesis. Brief medallion intro. Sets up Ep 3. |
| 03 | **The Medallion in Depth** | builds on Eps 1-2 | Bronze, Silver, Gold. Velocity tiers. Why Silver is the anchor. |
| 04 | **The Agent and Its Tools** | builds on Eps 1-3 | MCP, the Agent Framework, why agents don't read databases. |

### Business-need arc (Eps 5-11) — each walks one real pain end-to-end

| # | Title | Practice · Service | Builds on | Business KPI |
|---|---|---|---|---|
| 05 | **The Retail Margin Squeeze** | RC · Loyalty Churn (RC-CX-01) | Foundation | Loyalty-driven retention; gross margin |
| 06 | **The Warranty Cost Spiral** | AXLE · Zero Day Warranty (AXLE-WRTY-01) | Foundation + Ep 5 (Practice fluency) | Warranty cost · supplier recovery · 8-12 week investigation → minutes |
| 07 | **Cold-Chain Shrink in Grocery** | RC · Cold-Chain Excursion (RC-SUPCHN-01) | Foundation + Ep 5 | Shrink dollars · margin protected per excursion |
| 08 | **The Healthcare Prior-Auth Crisis** | HLS · Prior Authorisation (HLS-CLIN-05) | Foundation + Ep 5-7 (governance maturity) | PA turnaround time · denial rate · clinician hours saved |
| 09 | **The Energy-Transition Operations Gap** | ER · Outage Triage (ER-NET-01) | Foundation + streaming patterns from Ep 7 | SAIDI/SAIFI · restoration time |
| 10 | **The IROPs Cascade** | TH · IROPs Recovery (TH-OPS-01) | Foundation + orchestration depth | Rebooking velocity · CSAT in disruption |
| 11 | **The Contact-Center Labour Squeeze** | TMT · Agent Assist (TMT-CC-01) | Foundation + all business eps (cross-Practice synthesis) | AHT · FCR · CES · attrition |

### Synthesis arc (Ep 12)

| # | Title | What it does |
|---|---|---|
| 12 | **What the Catalog Becomes When You've Heard the Whole Series** | Pulls the foundation + seven business-need stories together. Where APEX goes next. The framework as a compounding asset. |

---

## How a v2 episode is structured

Each business-need episode (5-11) follows the same arc — but the *content* varies:

1. **Historical opening** (3-5 min) — how the industry got to where it is. Real dates, real numbers, real shifts.
2. **The pain today** (3-5 min) — the KPI being squeezed. The economic stakes.
3. **Why the incumbent approach is breaking** (3-5 min) — what dashboards / BI / RPA / SaaS can't solve.
4. **The strategy** (3-5 min) — APEX's response in plain English.
5. **The Service that delivers it** (5-7 min) — the actual APEX Service. References medallion (Ep 3) and agent/MCP (Ep 4) from the foundation.
6. **The KPI impact** (3-5 min) — what changes when the Service is in production.
7. **Where it goes next** (1-2 min) — Wave 2 expansion thinking.

Then a `Further Reading` section in the .md — Microsoft Learn, Microsoft Tech Community, Architecture Center, plus industry-context references (HBR, McKinsey, industry trade publications).

Foundation episodes (1-4) are structured slightly differently — they're more conceptual — but follow the same pacing discipline (4-6 min per concept, no topic-switching).

---

## Listening paths

- **First-time listener**: linear, Episodes 1 through 12.
- **Already familiar with the framework, want a specific business angle**: read Episode 1, then jump to the relevant business-need episode.
- **Architect onboarding**: Foundation arc (1-4), then any single business-need episode end-to-end.
- **Practice lead for a specific industry**: Episodes 1, 2, 3, 4, then the business-need episode for that Practice, then Episode 12.

---

## Files in this folder

```
pc-servicesguide/
├── README.md                              ← you are here
├── 00-show-bible-and-format.md            ← v2 design principles (read before writing/narrating)
├── 01-the-bottleneck-moved.md             ← Foundation arc
├── 02-data-flows-beat-data-warehouses.md
├── 03-the-medallion-in-depth.md
├── 04-the-agent-and-its-tools.md
├── 05-the-retail-margin-squeeze.md        ← Business-need arc
├── 06-the-warranty-cost-spiral.md
├── 07-cold-chain-shrink-in-grocery.md
├── 08-the-healthcare-prior-auth-crisis.md
├── 09-the-energy-transition-operations-gap.md
├── 10-the-irops-cascade.md
├── 11-the-contact-center-labour-squeeze.md
├── 12-what-the-catalog-becomes.md         ← Synthesis arc
├── _build_audio.py                        ← TTS pipeline (Keven=Andrew, Morgan=Emma)
├── archive-v1/                            ← v1 scripts (8 episodes, chapter-led structure)
└── archive-v1-audio/                      ← v1 MP3s
```

---

*The implied listener: a Deloitte practitioner — solution architect, engagement lead, senior consultant — who's about to walk into a client conversation about agentic AI and wants the* business *framing first, the* architecture *second. The audio is their preparation.*
