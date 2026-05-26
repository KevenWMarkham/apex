# The APEX Deployment Podcast · Audio Files

Six MP3 episodes generated from the markdown scripts in the parent folder. Voices via **Microsoft Edge Neural TTS** (`edge-tts`). Concatenated with **ffmpeg**.

## Episodes

| # | File | Duration | Size | Source script |
|---|---|---|---|---|
| 01 | `01-from-demo-to-deployable.mp3` | **17:28** | 6.3 MB | `01-from-demo-to-deployable.md` |
| 02 | `02-the-platform-foundation.mp3` | **15:49** | 5.7 MB | `02-the-platform-foundation.md` |
| 03 | `03-building-the-tenant.mp3` | **15:29** | 5.6 MB | `03-building-the-tenant.md` |
| 04 | `04-service-and-agent-layers.mp3` | **17:13** | 6.2 MB | `04-service-and-agent-layers.md` |
| 05 | `05-the-motion.mp3` | **16:25** | 5.9 MB | `05-the-motion.md` |
| 06 | `06-day-zero-day-two-chaos.mp3` | **17:34** | 6.3 MB | `06-day-zero-day-two-chaos.md` |
| | **TOTAL** | **1 h 39 min** | **36.0 MB** | |

## Voice cast

| Host | Voice (edge-tts) | Personality cue |
|---|---|---|
| **Keven** *(the practitioner)* | `en-US-AndrewNeural` | Warm · Confident · Authentic · Honest — Conversation/Copilot family (Trilogy continuity host) |
| **Sam** *(the platform engineer)* | `en-US-AvaNeural` | Expressive · Caring · Pleasant · Friendly — Conversation/Copilot family · different texture from Emma in Services Podcast |

The female second-voice choice differentiates this podcast vocally from the Sellers Podcast (Andrew + Brian) and the Services Podcast (Andrew + Emma). Three Trilogy podcasts, three distinct audio signatures.

## Format

- **Codec:** MP3 (LAME, libmp3lame)
- **Bitrate:** 48 kbps
- **Sample rate:** 24 kHz
- **Channels:** mono
- **Inter-turn pause:** 350 ms

Standard podcast-grade encoding. Identical format to the other two Trilogy podcasts for tooling consistency.

## How to regenerate

```bash
cd C:\Stage\Clients\Industries\APEX\docs\podcast\pc-deploymentguide
python _build_audio.py 03-building-the-tenant.md       # one episode
python _build_audio.py --all                            # all six (sequential)
```

The synth path includes exponential-backoff retry on transient Microsoft TTS 503 errors (5 attempts, 8 → 128 sec backoff).

## Series content overview

Six episodes cover Volume III of the Trilogy:

- **Ep 1** — From Demo to Deployable · the three operational truths · same image / two substrates · structural Independence
- **Ep 2** — The Platform Foundation · identity, secrets, audit trust as the floor everything stands on
- **Ep 3** — Building the Tenant · Day-Zero motion · Entra → Fabric + Purview → Sentinel sequencing
- **Ep 4** — Service and Agent Layers · deployable Services · agent reuse · SHA-digest pinning · RAI overlays
- **Ep 5** — The Motion · pre-deployment security gate · staged agent upgrades · rollback discipline
- **Ep 6** — Day-Zero, Day-2, Chaos · chaos engineering · Day-2 standards · CI/CD · FinOps · series finale

## Notes

- The Deployment Podcast was written in the **conversational style** (no chapter/section number citations in dialogue) following user feedback on early podcast versions.
- Format note — this podcast's six episodes are organised around *operational disciplines* (foundation, building, motion, chaos), not around the source guide's chapter structure.
- Companion podcasts in this folder family — `pc-sellersguide/` (Sellers Podcast · seven episodes) and `pc-servicesguide/` (Services Podcast v2 · twelve episodes, business-need-led).
