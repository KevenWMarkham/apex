# The APEX Services Podcast · Audio Files

Eight MP3 episodes generated from the markdown scripts in the parent folder. Voices via **Microsoft Edge Neural TTS** (`edge-tts`). Concatenated with **ffmpeg**.

## Episodes

| # | File | Duration | Size | Source script |
|---|---|---|---|---|
| 01 | `01-why-services-are-data-first.mp3` | **20:55** | 7.4 MB | `01-why-services-are-data-first.md` |
| 02 | `02-bronze-tier.mp3` | **19:42** | 6.9 MB | `02-bronze-tier.md` |
| 03 | `03-silver-tier.mp3` | **17:46** | 6.3 MB | `03-silver-tier.md` |
| 04 | `04-gold-tier.mp3` | **14:38** | 5.2 MB | `04-gold-tier.md` |
| 05 | `05-orchestrations.mp3` | **20:30** | 7.2 MB | `05-orchestrations.md` |
| 06 | `06-the-service-catalog.mp3` | **19:21** | 6.8 MB | `06-the-service-catalog.md` |
| 07 | `07-superagents-and-practitioners.mp3` | **19:46** | 7.0 MB | `07-superagents-and-practitioners.md` |
| 08 | `08-the-services-era.mp3` | **18:35** | 6.6 MB | `08-the-services-era.md` |
| | **TOTAL** | **2 h 31 min** | **53.4 MB** | |

## Voice cast

| Host | Voice (edge-tts) | Personality cue |
|---|---|---|
| **Keven** *(the practitioner)* | `en-US-AndrewNeural` | Warm · Confident · Authentic · Honest — Conversation/Copilot family (same as Sellers Podcast) |
| **Morgan** *(the delivery architect)* | `en-US-EmmaNeural` | Cheerful · Clear · Conversational — same Conversation/Copilot family as Keven, female voice for vocal contrast |

The Conversation/Copilot voice family choice (vs. the News/Novel family used briefly with Aria) makes both voices sound naturally conversational rather than broadcast-tuned. Vocal pitch contrast (male + female) helps listeners track speakers through dense technical passages.

## Format

- **Codec:** MP3 (LAME, libmp3lame)
- **Bitrate:** 48 kbps
- **Sample rate:** 24 kHz
- **Channels:** mono
- **Inter-turn pause:** 350 ms

Standard podcast-grade encoding. Identical format to the Sellers Podcast for tooling consistency.

## How to regenerate

```bash
cd C:\Stage\Clients\Industries\APEX\docs\podcast\pc-servicesguide
python _build_audio.py 03-silver-tier.md       # one episode
python _build_audio.py --all                    # all eight (sequential)
```

The synth path includes exponential-backoff retry on transient Microsoft TTS 503 errors (5 attempts, 8 → 128 sec backoff).

## Series content overview

Eight episodes cover Volume II of the Trilogy:

- **Ep 1** — Why Services Are Data-First · Part I (Foundations of Service Data — medallion, Fabric, canonical schemas, MCP)
- **Ep 2** — Bronze Tier · Part II (SOR inventory, Real-Time Hub, four velocity tiers, ingestion + tokenization, PII + pii-unlock)
- **Ep 3** — Silver Tier · Part III (conformance, 14 schema families, industry schemas, Quality + Purview, Entra + governance)
- **Ep 4** — Gold Tier · Part IV (lakehouse patterns, per-Service Gold marts, agent MCP tool surface)
- **Ep 5** — Orchestrations · Part V (workflow patterns, archetypes, Agent Framework deep dive, RAI, n8n, Logic Apps, cross-Service composition)
- **Ep 6** — The Service Catalog · Part VI (38 Services across RC · HLS · ER · AXLE · TH · TMT · ICE)
- **Ep 7** — Superagents & Practitioner Tracks · Parts VII–VIII (LEDGER + Redis, RC-E2E-03 in a day, HLS worked example, design patterns, cost modeling)
- **Ep 8** — The Services Era · Part IX (Service envelopes, Microsoft Agent Stack, Foundry deep dive, agent context, Sentinel + Defender, integration surfaces, change management) + series finale

## Notes

- The Services Guide source uses **"Industrial · Construction · Equipment"** for ICE (Chapter 24). Audio uses this form throughout.
- Episode 3 reinforces — **canonical schemas anchor at Silver, not Gold.** This was a correction made during production.
- The Services Podcast is the delivery-side counterpart to `pc-sellersguide/`. Same Trilogy, different audience.
- Voice was switched from Aria (News/Novel-tuned, felt broadcast-y) to Emma (Conversation/Copilot-tuned, natural conversational register) in a regen pass on 2026-05-12.
