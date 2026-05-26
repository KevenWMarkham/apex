# The Zero Day Warranty Podcast · Audio Files

Five MP3 episodes — the Toyota Zero Day Warranty agentic-scenario podcast covering the Microsoft AXLE foundation (Episodes 1-3) and the NVIDIA extension (Episodes 4-5). Each episode is wrapped with a royalty-free opening and closing music sting in an industrial G-major register (see *Music* section below).

Voices via **Microsoft Edge Neural TTS** (`edge-tts`). Concatenated with **ffmpeg**.

## Episodes

| # | File | Duration | Size | Source script |
|---|---|---|---|---|
| 01 | `01-the-zero-day-warranty-idea.mp3` | **34:14** | 11.8 MB | `01-the-zero-day-warranty-idea.md` |
| 02 | `02-four-data-domains.mp3` | **39:17** | 13.5 MB | `02-four-data-domains.md` |
| 03 | `03-the-24-step-agent-and-the-microsoft-platform.mp3` | **38:33** | 13.2 MB | `03-the-24-step-agent-and-the-microsoft-platform.md` |
| 04 | `04-nvidia-at-the-station.mp3` | **39:42** | 13.6 MB | `04-nvidia-at-the-station.md` |
| 05 | `05-omniverse-and-the-90-day-path.mp3` | **40:01** | 13.7 MB | `05-omniverse-and-the-90-day-path.md` |
| — | `summary-for-chris-crotts.mp3` *(10-min client-shareable summary)* | **10:04** | 3.5 MB | `summary-for-chris-crotts.md` |
| | **SERIES TOTAL** (5 main episodes) | **3 h 12 min** | **65.8 MB** | |

Each episode runtime above includes the 5-second opening sting + the 6-second closing sting + 0.6s of silence between stings and voice. Spoken-content runtime is approximately 11.6 seconds shorter per episode.

The runtime came in longer than the original 28-32-minute design target because the episode scripts ran ~6,000 words each and edge-tts at its current voice rate reads slightly slower than the conversational-pace estimate. The content is complete and intact; the longer runtime is a function of voice cadence, not bloat.

## Voice cast

| Host | Voice (edge-tts) | Personality cue |
|---|---|---|
| **Keven** *(the practitioner)* | `en-US-AndrewNeural` | Warm · Confident · Trilogy continuity host · 22+ years on Microsoft platform |
| **Mia** *(the senior automotive partner)* | `en-US-MichelleNeural` | Natural conversational register matching Andrew · 18 years on automotive accounts · Manufacturing-IT and Quality-leadership background |

This is the **seventh distinct voice pairing** in the APEX podcast family:

| Podcast | Pairing |
|---|---|
| Sellers | Andrew + Brian (boardroom) |
| Services v2 | Andrew + Emma (delivery team) |
| Deployment | Andrew + Ava (war room) |
| Disney Account | Andrew + Emma Multilingual (account team) |
| Disney Studios | Andrew + Ava Multilingual (Studios account team) |
| DTNA | Andrew + Brian Multilingual (industrial-account, Class 8 trucks) |
| **Toyota (this)** | **Andrew + Michelle** (Toyota Zero Day Warranty agentic scenario) |

Mia's voice is the **Michelle** neural voice — a newer-generation natural-quality voice that matches Andrew's conversational register. Replaced an earlier audition of Aria, which read as too synthetic for the conversational format. Distinct from the prior female voices in the APEX family (Emma, Ava, Emma Multilingual, Ava Multilingual).

## Music — royalty-free, industrial G-major register

Each episode begins with a **5-second opening sting** and ends with a **6-second closing sting** synthesised entirely from scratch via ffmpeg additive synthesis. The Toyota stings are in the **automotive-brand-family register** — identical to DTNA's industrial G-major chord — deeper, warmer, grounded, with a manufacturing-floor feel that sits naturally with TPS / Jidoka / Andon vocabulary used throughout the series.

- **Opening sting** — ascending G3-D4-G4-B4 power chord · warm horn-like timbre · low harmonic content · slight echo
- **Closing sting** — sustained G-major chord with low fundamental and high-fifth sparkle · gradual resolution

### Explicit disclosure

- The stings are **not** derived from, and do not quote, any copyrighted composition — Toyota-related, NVIDIA-related, or otherwise.
- They were generated programmatically by `_build_music.py` using only ffmpeg's `sine` lavfi source and standard filters (`afade`, `aecho`, `amix`, `volume`). No sample libraries, no external audio assets.
- They share the automotive-brand-family register with the DTNA podcast — the same G-major industrial sting set — by design.

### Why this matters for the Account Team

Using actual copyrighted Toyota music (any Toyota corporate identity audio, the Lexus "L/Certified" sound logo, or anything from Woven by Toyota's marketing) — or any NVIDIA-branded sound design — in a podcast that names Toyota and NVIDIA directly would be a copyright issue against the client and the platform vendor. The synthesised stings are the safe path.

If a different sting is preferred — for example, a properly licensed orchestral cue from a royalty-free music library — replace `opening_sting.mp3` and `closing_sting.mp3` and re-run `python _apply_music.py`.

## Format

- **Codec:** MP3 (LAME, libmp3lame)
- **Bitrate:** 48 kbps
- **Sample rate:** 24 kHz
- **Channels:** mono
- **Inter-turn pause:** 350 ms
- **Sting-to-voice silence:** 300 ms

Standard podcast-grade encoding. Identical format to the six prior APEX podcasts for tooling consistency.

## How to regenerate

If episode scripts change:

```bash
cd C:\Stage\Clients\Industries\APEX\docs\podcast\pc-toyota-zero-day-warranty

# Regenerate voice audio for one episode
python _build_audio.py 03-the-24-step-agent-and-the-microsoft-platform.md

# Or all five
python _build_audio.py --all

# Then re-wrap with music stings
python _apply_music.py
```

If a different music sting is preferred:

```bash
# Replace opening_sting.mp3 and/or closing_sting.mp3 with the preferred files
# (24kHz mono MP3 recommended)

# Then re-wrap all episodes from the unstinged originals
python _apply_music.py
```

The `_apply_music.py` script keeps stingless backups in `audio/_originals/` so the wrap operation is reversible and idempotent.

## Structure of the audio folder

```
audio/
├── 01-the-zero-day-warranty-idea.mp3                  ← episode with stings applied
├── 02-four-data-domains.mp3
├── 03-the-24-step-agent-and-the-microsoft-platform.mp3
├── 04-nvidia-at-the-station.mp3
├── 05-omniverse-and-the-90-day-path.mp3
├── _originals/                                        ← stingless backups (do not edit)
│   ├── 01-the-zero-day-warranty-idea.mp3
│   ├── 02-four-data-domains.mp3
│   ├── 03-the-24-step-agent-and-the-microsoft-platform.mp3
│   ├── 04-nvidia-at-the-station.mp3
│   └── 05-omniverse-and-the-90-day-path.mp3
└── README.md
```

## Series content overview

Five episodes anchored on the Toyota Zero Day Warranty agentic scenario:

- **Ep 1 — The Zero Day Warranty Idea** · the warranty-cluster moment · 8-12-weeks-across-six-teams current state · Toyota's TPS and Jidoka heritage · CEO Priority 3 (Manufacturing Excellence & Industry 4.0) · the four-domain hypothesis · the $4.2M / $2.8M / 340% reference scenario · Toyota's existing Microsoft and NVIDIA footprints
- **Ep 2 — Four Data Domains** · the vehicle build record · connected vehicle warranty data · quality events on the line · assembly line telemetry · Bronze → Silver → Gold medallion on OneLake · why these four · Silver as canonical foundation · Microsoft Industry Cloud for Manufacturing
- **Ep 3 — The 24-Step Agent and the Microsoft Platform** · Microsoft Fabric + Agent Framework + Purview + LEDGER hash chain · the 24-step agent in 6 phases × 4 steps · HITL = quality engineer · the $4.2M / $2.8M / 340% calculation walked transparently · Independence-from-Microsoft posture explicit
- **Ep 4 — NVIDIA at the Station (Day-0 Prevention)** · the inversion thesis · Metropolis vision-AI · DeepStream pipelines · Jetson edge inference · RAPIDS for accelerated analytics · the two-fabric architecture · where the stacks compose vs negotiate
- **Ep 5 — Omniverse, Toyota's NVIDIA Estate, and the 90-Day Path** · Woven by Toyota / Woven City · Toyota Drive on NVIDIA · Omniverse for plant simulation · NeMo for domain LMs · Triton Inference Server · NVIDIA AI Enterprise · the 90-day pilot path · three sponsor candidates · BVA + ECIF + Azure Credits funding · the three-contract Independence model

## Notes

- **Audience.** Internal Deloitte Account Team prep **and** client-shareable. Spoken content uses client-safe terminology only — internal codenames (BRML, CVML, QEML, AAML, ORCH-01, SB06, APEX-M) are confined to the series README's internal-mapping table and to the "From the APEX framework" subsection of each episode's Further Reading. They never appear in the audio.
- **Independence from Microsoft.** Explicitly stated in Episodes 1, 3, and 5 — Deloitte recommends; Toyota contracts directly with Microsoft and NVIDIA on their own paper; Deloitte services on Deloitte paper; three contracts, no co-sell, no compensation flows from platform vendors to Deloitte for influencing Toyota choices.
- **Creative-authorship boundary not applicable.** Unlike the Disney Studios podcast where WGA/SAG-AFTRA AI provisions are binding, the Toyota Zero Day Warranty scenario does not touch creative work. The relevant boundary here is **operator dignity** — agents augment TPS, never replace operator judgement. This is named explicitly throughout the series.
- **Reference numbers.** The $4.2M / $2.8M / 340% / 8-12 weeks anchor is consistently the only Toyota-specific number across all five episodes. These are framework reference-scenario figures from a representative-plant model, not Toyota-specific commitments. Episode 3 says this explicitly.
- **Companion artefacts.** Two HTML documents support the podcast and live at `Automotive/Toyota/02_projects/FY27_Pipeline/Fabric_Connected_Vehicle_Analytics/`:
  - `ZeroDayWarranty_Calculations_and_References.html` — calculation breakdown, 24-step chain math
  - `ZeroDayWarranty_Architecture_Diagrams.html` — architecture pack with Microsoft + NVIDIA tabs
  Either or both can be sent to Chris Crotts after the discovery conversation.
- **Companion podcasts in this folder family.** `../pc-sellersguide/` (10 episodes · framework-wide selling) · `../pc-servicesguide/` (12 episodes · framework-wide architecture) · `../pc-deploymentguide/` (6 episodes · framework-wide operations) · `../pc-disney-account/` (6 episodes · Disney company-wide) · `../pc-disney-studios/` (5 episodes · Disney Studios sub-business) · `../pc-dtna-account/` (5 episodes · DTNA, the parallel automotive account podcast).
