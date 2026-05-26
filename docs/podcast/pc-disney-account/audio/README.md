# The Disney Account Podcast · Audio Files

Five MP3 episodes — the Deloitte Account Team's internal podcast for The Walt Disney Company. Each episode is wrapped with a royalty-free opening and closing music sting (see *Music* section below).

Voices via **Microsoft Edge Neural TTS** (`edge-tts`). Concatenated with **ffmpeg**.

## Episodes

| # | File | Duration | Size | Source script |
|---|---|---|---|---|
| 01 | `01-the-disney-account.mp3` | **16:42** | 5.9 MB | `01-the-disney-account.md` |
| 02 | `02-the-customer-experience-six.mp3` | **19:50** | 7.0 MB | `02-the-customer-experience-six.md` |
| 03 | `03-the-operations-eight.mp3` | **16:11** | 5.7 MB | `03-the-operations-eight.md` |
| 04 | `04-the-ladder-for-disney.mp3` | **18:24** | 6.5 MB | `04-the-ladder-for-disney.md` |
| 05 | `05-the-account-team-playbook.mp3` | **18:02** | 6.4 MB | `05-the-account-team-playbook.md` |
| 06 | `06-the-curated-plays.mp3` | **35:03** | 12.4 MB | `06-the-curated-plays.md` (Excel: `../Disney_Agentic_Plays_BackOffice_Streaming.xlsx` · Brief: `../Disney-Experiences-Agentic-Play-Brief.md`) |
| | **SERIES TOTAL** | **2 h 04 min** | **43.9 MB** | |

Each episode runtime above includes the 5-second opening sting + ~11 seconds of inter-segment silence + the closing 6-second sting. The spoken-content runtime is approximately 11.6 seconds shorter per episode.

## Voice cast

| Host | Voice (edge-tts) | Personality cue |
|---|---|---|
| **Keven** *(the practitioner)* | `en-US-AndrewNeural` | Warm · Confident · Trilogy continuity host |
| **Riley** *(the senior account partner)* | `en-US-EmmaMultilingualNeural` | Conversational · multilingual register · 12 years on the Disney account |

The female second voice is the **Multilingual** Emma — chosen partly for thematic fit with Disney's international footprint (auto-dub scenario, international Disney+ markets), partly to give this podcast its own audio signature distinct from the three Trilogy podcasts.

The four podcasts now have four distinct voice cast pairings:

| Podcast | Pairing |
|---|---|
| Sellers | Andrew + Brian (two male, "boardroom") |
| Services v2 | Andrew + Emma (male + female, "delivery team") |
| Deployment | Andrew + Ava (male + female, "war room") |
| **Disney (this)** | **Andrew + Emma Multilingual** (male + female, "account team") |

## Music — royalty-free, no Disney IP

Each episode begins with a 5-second **opening sting** and ends with a 6-second **closing sting.** Both stings are **synthesised entirely from scratch** via ffmpeg additive synthesis — sine waves at musical frequencies, plus harmonics, plus light reverb. They evoke a bell-tree / sparkle register that media-and-entertainment company brand stings often share — but they do **not** quote, sample, or derive from any copyrighted melody.

### Explicit disclosure

- The opening sting is an **ascending C-E-G-C major arpeggio** with bell-like timbre. It is not from *Disney's* sonic identity, nor from any specific copyrighted source.
- The closing sting is a **descending C-G-E-C arpeggio resolving to a sustained C major chord** with warmer timbre. Same disclosure.
- The stings were generated programmatically by `_build_music.py` using only ffmpeg's `sine` lavfi source and standard filters (`afade`, `aecho`, `amix`, `volume`). No sample libraries, no external audio assets.

### Why this matters for the Account Team

Using actual copyrighted Disney music — for example, *"When You Wish Upon a Star,"* the Disney chime logo, or any Pixar/Marvel/Lucasfilm theme — in a podcast about Disney as a Deloitte client would be a copyright violation *against the client.* That would be an Independence problem and a relationship problem simultaneously. The synthesised stings are the safe path.

If the Account Team wants different music — for example, a properly licensed orchestral cue from a royalty-free music library, or a custom-composed cue commissioned through Deloitte's brand team — that's straightforward to swap in. Replace `opening_sting.mp3` and `closing_sting.mp3` and re-run `python _apply_music.py`.

## Format

- **Codec:** MP3 (LAME, libmp3lame)
- **Bitrate:** 48 kbps
- **Sample rate:** 24 kHz
- **Channels:** mono
- **Inter-turn pause:** 350 ms
- **Sting-to-voice silence:** 300 ms

Standard podcast-grade encoding. Identical format to the three Trilogy podcasts for tooling consistency.

## How to regenerate

If episode scripts change:

```bash
cd C:\Stage\Clients\Industries\APEX\docs\podcast\pc-disney-account

# Regenerate voice audio for one episode
python _build_audio.py 02-the-customer-experience-six.md

# Or all five
python _build_audio.py --all

# Then re-wrap with music stings
python _apply_music.py
```

If you want a different music sting:

```bash
# Replace opening_sting.mp3 and/or closing_sting.mp3 with your preferred files
# (24kHz mono MP3 recommended)

# Then re-wrap all episodes from the unstinged originals
python _apply_music.py
```

The `_apply_music.py` script keeps stingless backups in `audio/_originals/` so the wrap operation is reversible and idempotent.

## Structure of the audio folder

```
audio/
├── 01-the-disney-account.mp3              ← episode with stings applied
├── 02-the-customer-experience-six.mp3
├── 03-the-operations-eight.mp3
├── 04-the-ladder-for-disney.mp3
├── 05-the-account-team-playbook.mp3
├── _originals/                            ← stingless backups (do not edit)
│   ├── 01-the-disney-account.mp3
│   ├── 02-the-customer-experience-six.mp3
│   ├── 03-the-operations-eight.mp3
│   ├── 04-the-ladder-for-disney.mp3
│   └── 05-the-account-team-playbook.mp3
└── README.md
```

## Series content overview

Six episodes for the Deloitte Account Team for The Walt Disney Company:

- **Ep 1** — The Disney Account · three segments · six pressure points · 16 Disney-fit scenarios preview
- **Ep 2** — The Customer Experience Six · all six CX scenarios from the curated Disney portfolio
- **Ep 3** — The Operations Eight · Network/Infrastructure 4 + Engineering R&D 4 (Internal IT, Cyber)
- **Ep 4** — The Ladder for Disney · four-level ladder per segment · GSSC Lab for Disney demos · the two build/deploy meta-scenarios
- **Ep 5** — The Account Team Playbook · relationship map · 30-Min Framework Disney-tuned · Independence specifics · the 90-day calendar
- **Ep 6** — The Curated Plays (Back-Office + Streaming + Experiences) · 23 plays walked (12 back-office incl. CTO Portfolio Agent and Engineering Headcount Optimisation Agent · 10 streaming · 1 Experiences flagship) · Excel companion `Disney_Agentic_Plays_BackOffice_Streaming.xlsx` · Brief `Disney-Experiences-Agentic-Play-Brief.md`

## Notes

- **Internal use only.** This podcast names Disney directly because it's internal Deloitte Account Team preparation. The Trilogy podcasts anonymise Disney as "a global media and entertainment conglomerate."
- **Independence-from-Microsoft posture** preserved throughout — Deloitte does not co-sell, recommendation is on the merits, two-contract model with Microsoft.
- **Companion podcasts in this folder family** — `../pc-sellersguide/` (10 episodes · framework-wide selling) · `../pc-servicesguide/` (12 episodes · framework-wide architecture) · `../pc-deploymentguide/` (6 episodes · framework-wide operations).
