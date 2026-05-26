# The APEX Services Podcast · v2 · Audio Files

Twelve MP3 episodes — the rebuilt Services Guide podcast structured around business needs (not chapter walks). Stair-step structure throughout — each episode references prior episodes by concept; the series accumulates understanding.

Voices via **Microsoft Edge Neural TTS** (`edge-tts`). Concatenated with **ffmpeg**.

> **v2 supersedes v1.** The 8-episode v1 series (chapter-led, audiobook-feel) is archived in `../archive-v1/` and `../archive-v1-audio/`. v2 is the active series.

## Episodes

### Foundation arc (Eps 1-4) — concepts later episodes depend on

| # | File | Duration | Size | Foundation laid |
|---|---|---|---|---|
| 01 | `01-the-bottleneck-moved.mp3` | **14:37** | 5.1 MB | Historical macro · three eras of enterprise data · why agentic AI is sellable *now* |
| 02 | `02-data-flows-beat-data-warehouses.mp3` | **15:06** | 5.3 MB | Data-first thesis · three needs of agentic data · brief medallion preview |
| 03 | `03-the-medallion-in-depth.mp3` | **17:14** | 6.0 MB | Bronze · Silver · Gold · velocity tiers · canonical at Silver |
| 04 | `04-the-agent-and-its-tools.mp3` | **17:11** | 6.0 MB | MCP boundary · Agent Framework · audit row · Purview as the auditor's interface |

### Business-need arc (Eps 5-11) — each walks one real pain end-to-end

| # | File | Duration | Size | Business KPI |
|---|---|---|---|---|
| 05 | `05-the-retail-margin-squeeze.mp3` | **19:48** | 7.0 MB | RC-CX-01 Loyalty Churn · margin retention |
| 06 | `06-the-warranty-cost-spiral.mp3` | **16:05** | 5.7 MB | AXLE-WRTY-01 Zero Day Warranty · supplier-recovery $ |
| 07 | `07-cold-chain-shrink-in-grocery.mp3` | **13:30** | 4.8 MB | RC-SUPCHN-01 Cold-Chain Excursion · shrink avoided |
| 08 | `08-the-healthcare-prior-auth-crisis.mp3` | **15:17** | 5.4 MB | HLS-CLIN-05 Prior Authorisation · clinician hours saved |
| 09 | `09-the-energy-transition-operations-gap.mp3` | **13:35** | 4.8 MB | ER-NET-01 Distribution Outage · SAIDI/SAIFI |
| 10 | `10-the-irops-cascade.mp3` | **12:56** | 4.6 MB | TH-OPS-01 IROPs Recovery · rebooking velocity |
| 11 | `11-the-contact-center-labour-squeeze.mp3` | **13:01** | 4.6 MB | TMT-CC-01 Agent Assist · AHT/FCR/CES/attrition |

### Synthesis arc (Ep 12)

| # | File | Duration | Size | What it does |
|---|---|---|---|---|
| 12 | `12-what-the-catalog-becomes.mp3` | **13:59** | 4.9 MB | Pulls foundation + 7 business cases together · the compounding-asset thesis |
| | **SERIES TOTAL** | **3 h 02 min** | **64 MB** | |

## Voice cast

| Host | Voice (edge-tts) | Personality cue |
|---|---|---|
| **Keven** *(the practitioner)* | `en-US-AndrewNeural` | Warm · Confident · Authentic · Honest — Conversation/Copilot family (continuity host across the Trilogy) |
| **Morgan** *(the delivery architect)* | `en-US-EmmaNeural` | Cheerful · Clear · Conversational — same Conversation/Copilot family as Keven, female voice for vocal contrast |

Same voice cast as v1 final pass. The *content* changed; the voice signature stayed for listener familiarity.

## Format

- **Codec:** MP3 (LAME, libmp3lame) · 48 kbps · 24 kHz · mono · 350 ms inter-turn pause
- Standard podcast-grade encoding; universally playable.

## How to regenerate

```bash
cd C:\Stage\Clients\Industries\APEX\docs\podcast\pc-servicesguide
python _build_audio.py 03-the-medallion-in-depth.md       # one episode
python _build_audio.py --all                              # all twelve (sequential)
```

The synth path includes exponential-backoff retry on transient Microsoft TTS errors (5 attempts, 8 → 128 sec backoff). One transient hit Ep 11 during this generation; retry handled it cleanly.

## What v2 does differently from v1

User feedback on v1 (the 8-episode chapter-led version):

> "I could not follow the conversation. It was not a dialog but a listing of technical implementations and chapter references. I would like a stair-step dialog where foundation is laid and builds upon itself. The dialog should have narrative, overview, and historical foundation. More detail without switching technical topics. Start with a key business need and follow a step-by-step strategy to deliver a service for the business need to affect the KPIs."

v2 addresses every line:

- **Business-need-led structure** — Episodes 5-11 each open with one real industry pain (retail margin, warranty, cold chain, prior auth, energy, IROPs, contact center); the architecture follows the need.
- **Stair-step** — Foundation Episodes 1-4 lay concepts later episodes reference by concept (not by episode number).
- **Historical context** — Every episode opens with 3-5 min of industry/historical context before any architecture.
- **One topic, fully developed** — 4-6 minutes per concept; no topic-switching.
- **No chapter or section numbers in dialogue** — Hosts know the framework; they don't recite its index.
- **External resources** — Every .md ends with a `Further Reading` section covering Microsoft Learn paths, Tech Community blogs, Architecture Center references, and industry sources (HBR, McKinsey, NRF, AMA, IATA, EPRI, Gartner, etc.).

## Length comparison: v1 vs v2

| Series | Episodes | Total runtime | Words |
|---|---|---|---|
| v1 (archived) | 8 | ~2 h 31 min | ~40,000 |
| **v2 (this)** | **12** | **3 h 02 min** | **~65,000** |

v2 is longer because each topic gets the breathing room the user asked for.

## Notes

- All references to **canonical schemas** anchor at **Silver**, not Gold — the corrected architectural framing.
- All Microsoft-relationship references reflect Deloitte's **Independence-from-Microsoft posture** — recommendation on the merits, not partner-channel compensation.
- ICE = "Industrial · Construction · Equipment" per the Services Guide source.
- Episode 12 ties to the Sellers Podcast and Deployment Podcast — the Trilogy is structured as a composable three-podcast series. See `../pc-sellersguide/` (10 episodes) and `../pc-deploymentguide/` (6 episodes).
