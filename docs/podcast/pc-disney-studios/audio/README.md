# The Disney Studios Account Podcast · Audio Files

Five MP3 episodes — the Deloitte Account Team's internal podcast for the Disney Studios sub-business (Walt Disney Pictures, Pixar, Marvel Studios, Lucasfilm, 20th Century Studios, Searchlight Pictures). Each episode is wrapped with a royalty-free opening and closing music sting (see *Music* section below).

Voices via **Microsoft Edge Neural TTS** (`edge-tts`). Concatenated with **ffmpeg**.

## Episodes

| # | File | Duration | Size | Source script |
|---|---|---|---|---|
| 01 | `01-the-disney-studios-account.mp3` | **16:13** | 5.7 MB | `01-the-disney-studios-account.md` |
| 02 | `02-content-development-and-greenlight.mp3` | **15:14** | 5.4 MB | `02-content-development-and-greenlight.md` |
| 03 | `03-production-plays.mp3` | **16:36** | 5.8 MB | `03-production-plays.md` |
| 04 | `04-marketing-distribution-rights.mp3` | **15:20** | 5.4 MB | `04-marketing-distribution-rights.md` |
| 05 | `05-ladder-and-playbook.mp3` | **18:18** | 6.4 MB | `05-ladder-and-playbook.md` (companion: `../Disney_Studios_Agentic_Plays.xlsx`) |
| | **SERIES TOTAL** | **1 h 21 min** | **28.1 MB** | |

Each episode runtime above includes the 5-second opening sting + ~11 seconds of inter-segment silence + the closing 6-second sting. The spoken-content runtime is approximately 11.6 seconds shorter per episode.

## Voice cast

| Host | Voice (edge-tts) | Personality cue |
|---|---|---|
| **Keven** *(the practitioner)* | `en-US-AndrewNeural` | Warm · Confident · Trilogy continuity host |
| **Eden** *(the 12-year media/content account partner)* | `en-US-AvaMultilingualNeural` | Narrator-warm · multilingual register · 12 years on entertainment-and-content production accounts |

Ava Multilingual provides a distinct sonic register from the other five podcasts in the APEX family — appropriate for the Studios podcast's content-and-creative focus and Disney Studios' international footprint.

The six podcasts now have six distinct voice cast pairings:

| Podcast | Pairing |
|---|---|
| Sellers | Andrew + Brian (two male, "boardroom") |
| Services v2 | Andrew + Emma (male + female, "delivery team") |
| Deployment | Andrew + Ava (male + female, "war room") |
| Disney Account | Andrew + Emma Multilingual (male + female, "account team") |
| DTNA Account | Andrew + Aria (male + female, "industrial-account team") |
| **Disney Studios (this)** | **Andrew + Ava Multilingual** (male + female, "studios partner") |

## Music — royalty-free, no Disney IP

Each episode begins with a 5-second **opening sting** and ends with a 6-second **closing sting.** Both stings are **synthesised entirely from scratch** via ffmpeg additive synthesis — sine waves at musical frequencies, plus harmonics, plus light reverb. They evoke a bell-tree / sparkle register that media-and-entertainment company brand stings often share — but they do **not** quote, sample, or derive from any copyrighted melody.

### Explicit disclosure

- The opening sting is an **ascending F-A-C-F major arpeggio** with bell-like timbre. F major is brighter than the C major of the Disney Account podcast, giving Studios its own sonic identity within the Disney brand family. It is not from *Disney's* sonic identity, nor from any specific copyrighted source.
- The closing sting is a **descending F-C-A-F arpeggio resolving to a sustained F major chord** with warmer timbre. Same disclosure.
- The stings were generated programmatically by `_build_music.py` using only ffmpeg's `sine` lavfi source and standard filters (`afade`, `aecho`, `amix`, `volume`). No sample libraries, no external audio assets.

### Why this matters for the Account Team — especially for Studios

Using actual copyrighted music from any of Disney's studios — *When You Wish Upon a Star*, the Disney chime, the 20th Century fanfare, the Marvel Studios fanfare, the Pixar score, the Lucasfilm/Star Wars opening — would be a copyright violation against the client. For a podcast about Disney Studios as a Deloitte engagement target, the synthesised stings are the only safe path.

The Studios podcast is more sensitive to this than the Disney Account podcast because *the Studios sub-business owns the music IP we'd otherwise be tempted to reach for.* Synthesised stings remove all ambiguity.

If the Account Team wants different music — a properly licensed orchestral cue from a royalty-free music library, or a custom-composed cue commissioned through Deloitte's brand team — that's straightforward to swap in. Replace `opening_sting.mp3` and `closing_sting.mp3` and re-run `python _apply_music.py`.

## Format

- **Codec:** MP3 (LAME, libmp3lame)
- **Bitrate:** 48 kbps
- **Sample rate:** 24 kHz
- **Channels:** mono
- **Inter-turn pause:** 350 ms
- **Sting-to-voice silence:** 300 ms

Standard podcast-grade encoding. Identical format to the four prior APEX podcasts for tooling consistency.

## How to regenerate

If episode scripts change:

```bash
cd C:\Stage\Clients\Industries\APEX\docs\podcast\pc-disney-studios

# Regenerate voice audio for one episode
python _build_audio.py 03-production-plays.md

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
├── 01-the-disney-studios-account.mp3         ← episode with stings applied
├── 02-content-development-and-greenlight.mp3
├── 03-production-plays.mp3
├── 04-marketing-distribution-rights.mp3
├── 05-ladder-and-playbook.mp3
├── _originals/                                ← stingless backups (do not edit)
│   ├── 01-the-disney-studios-account.mp3
│   ├── 02-content-development-and-greenlight.mp3
│   ├── 03-production-plays.mp3
│   ├── 04-marketing-distribution-rights.mp3
│   └── 05-ladder-and-playbook.mp3
└── README.md
```

## Series content overview

Five episodes for the Deloitte Account Team for Disney Studios:

- **Ep 1** — The Disney Studios Account · six studios with creative autonomy · five strategic pressures · why APEX now at Studios specifically
- **Ep 2** — Content Development & Greenlight Plays · four plays (greenlight decision support, audience science, IP/franchise opportunity scoring, talent & casting intelligence)
- **Ep 3** — Production Plays · five plays (schedule & budget intelligence, VFX pipeline, Pixar animation pipeline, post-production workflow, production safety & wellness)
- **Ep 4** — Marketing, Distribution & Rights Plays · six plays (trailer performance, marketing campaign optimisation, windowing decision support, awards campaign management, rights compliance, music sync clearance)
- **Ep 5** — The Ladder for Disney Studios + Account Team Playbook · four-level ladder Studios-tailored · 30-Min Framework Studios-tuned · Independence specifics · 90-day calendar · companion: `Disney_Studios_Agentic_Plays.xlsx` (15 plays)

## Notes

- **Internal use only.** This podcast names Disney's studios directly because it's internal Deloitte Account Team preparation. The Trilogy podcasts anonymise Disney as "a global media and entertainment conglomerate."
- **Creative-authorship boundary** — every play respects the post-strike AI policy framework. WGA / SAG-AFTRA / DGA AI provisions are binding. The Account Team's framing is operational and analytical augmentation, never creative replacement.
- **Independence-from-Microsoft posture** preserved throughout — Deloitte does not co-sell, recommendation is on the merits, two-contract model with Microsoft.
- **Companion podcasts in this folder family** — `../pc-sellersguide/` (10 episodes · framework-wide selling) · `../pc-servicesguide/` (12 episodes · framework-wide architecture) · `../pc-deploymentguide/` (6 episodes · framework-wide operations) · `../pc-disney-account/` (6 episodes · company-wide Disney framing this podcast complements) · `../pc-dtna-account/` (5 episodes · parallel account-specific structure).
- **Scenario coverage** — 14 Studios-specific TMT scenarios added to `../../reference/APEX-Scenario-Chains.xlsx` (v1.3). Total APEX scenario library now 743.
