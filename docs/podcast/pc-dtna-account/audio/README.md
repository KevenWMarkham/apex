# The DTNA Account Podcast · Audio Files

Five MP3 episodes — the Deloitte Account Team's internal podcast for Daimler Trucks North America. Each episode is wrapped with a royalty-free opening and closing music sting in an industrial-toned register (see *Music* section below).

Voices via **Microsoft Edge Neural TTS** (`edge-tts`). Concatenated with **ffmpeg**.

## Episodes

| # | File | Duration | Size | Source script |
|---|---|---|---|---|
| 01 | `01-the-dtna-account.mp3` | **17:15** | 6.1 MB | `01-the-dtna-account.md` |
| 02 | `02-manufacturing-and-quality.mp3` | **20:35** | 7.3 MB | `02-manufacturing-and-quality.md` |
| 03 | `03-connected-vehicle-and-aftermarket.mp3` | **18:53** | 6.7 MB | `03-connected-vehicle-and-aftermarket.md` |
| 04 | `04-the-ladder-for-dtna.mp3` | **19:16** | 6.8 MB | `04-the-ladder-for-dtna.md` |
| 05 | `05-the-account-team-playbook.mp3` | **18:47** | 6.6 MB | `05-the-account-team-playbook.md` |
| | **SERIES TOTAL** | **1 h 34 min** | **33.5 MB** | |

Each episode runtime above includes the 5-second opening sting + ~11 seconds of inter-segment silence + the 6-second closing sting. The spoken-content runtime is approximately 12 seconds shorter per episode.

## Voice cast

| Host | Voice (edge-tts) | Personality cue |
|---|---|---|
| **Keven** *(the practitioner)* | `en-US-AndrewNeural` | Warm · Confident · Trilogy continuity host |
| **Marcus** *(the senior account partner)* | `en-US-BrianMultilingualNeural` | Industrial-account register · 10+ years on Class 8 truck OEM accounts |

This is the fifth distinct voice pairing in the podcast family:

| Podcast | Pairing |
|---|---|
| Sellers | Andrew + Brian (two male, "boardroom") |
| Services v2 | Andrew + Emma (male + female, "delivery team") |
| Deployment | Andrew + Ava (male + female, "war room") |
| Disney | Andrew + Emma Multilingual (male + female, "account team") |
| **DTNA (this)** | **Andrew + Brian Multilingual** (two male, "industrial account") |

## Music — royalty-free, industrial-toned

Each episode begins with a **5-second opening sting** and ends with a **6-second closing sting** synthesised entirely from scratch via ffmpeg additive synthesis. The DTNA stings are in a *different sonic register* from the Disney bell-tree sparkle — *deeper, warmer, grounded* to suit the industrial-trucking brand register.

- **Opening sting** — ascending G3-D4-G4-B4 power chord · warm horn-like timbre · low harmonic content · slight echo
- **Closing sting** — sustained G-major chord with low fundamental and high-fifth sparkle · gradual resolution

### Explicit disclosure

- The stings are *not* derived from, and do not quote, any copyrighted composition — Daimler-related or otherwise.
- They were generated programmatically by `_build_music.py` using only ffmpeg's `sine` lavfi source and standard filters (`afade`, `aecho`, `amix`, `volume`). No sample libraries, no external audio assets.

## Format

- **Codec:** MP3 (LAME, libmp3lame) · 48 kbps · 24 kHz · mono · 350 ms inter-turn pause · 300 ms sting-to-voice silence
- Standard podcast-grade encoding identical to the other four podcasts in this family.

## How to regenerate

```bash
cd C:\Stage\Clients\Industries\APEX\docs\podcast\pc-dtna-account
python _build_audio.py 02-manufacturing-and-quality.md    # one episode
python _build_audio.py --all                              # all five (sequential)
python _apply_music.py                                    # wrap with stings (idempotent)
```

Stingless backups in `audio/_originals/`. The synth path has exponential-backoff retry on transient TTS errors.

## Series content overview

Five episodes for the Deloitte Account Team for Daimler Trucks North America:

- **Ep 1** — The DTNA Account · four brands (Freightliner, Western Star, Thomas Built, Detroit) · three strategic themes (electrification, autonomy, freight cycle) · AXLE Practice mapping
- **Ep 2** — The Manufacturing & Quality Plays · six AXLE-Practice scenarios — Zero Day Warranty, predictive maintenance, quality escape, plant-floor agent assist, supplier traceability, production planning
- **Ep 3** — The Connected Vehicle & Aftermarket Plays · six customer-facing scenarios — Detroit Connect diagnostic, dealer performance, parts forecasting, service-bay agent assist, fleet customer experience, in-cab driver assist
- **Ep 4** — The Ladder for DTNA · per-brand ladder · L1 wedge → L2 Wave 1 → L3 AXLE CoE → L4 fleet-customer transformation · electrification + autonomy strategic frames
- **Ep 5** — The Account Team Playbook · relationship map · 30-Min Framework DTNA-tuned · **Daimler Truck global Independence specifics** · Microsoft coordination · 90-day calendar

## Notes

- **Internal use only.** Names DTNA directly because it's internal Deloitte Account Team preparation.
- **Daimler Truck global Independence framing** — DTNA's parent (Daimler Truck Holding AG) is a publicly listed German company. Engagement scope coordination with Deloitte global Independence Office is required. Ep 5 covers this in operational detail.
- **AXLE Practice mapping** — most plays anchor to AXLE; some adjacencies into ICE (aftermarket parts) and TH (fleet customer experience).
- **Independence-from-Microsoft posture** preserved throughout — Deloitte does not co-sell; recommendation on the merits.

## Companion podcasts in this folder family

- **`../pc-sellersguide/`** — 10 episodes · framework-wide selling
- **`../pc-servicesguide/`** — 12 episodes · framework-wide architecture (v2)
- **`../pc-deploymentguide/`** — 6 episodes · framework-wide operations
- **`../pc-disney-account/`** — 6 episodes · TMT-MED account-specific · w/ Excel companion (23 plays) + Experiences brief
