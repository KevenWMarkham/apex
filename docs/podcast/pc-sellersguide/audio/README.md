# The APEX Sellers Podcast · Audio Files

Ten MP3 episodes — the original 7-episode Sellers Guide arc plus 3 new episodes weaving in the Sellers Handbook content. Voices via **Microsoft Edge Neural TTS** (`edge-tts`). Concatenated with **ffmpeg**.

## Episodes

### Original Sellers Guide arc (Eps 1-7)

| # | File | Duration | Size | Source script |
|---|---|---|---|---|
| 01 | `01-the-moment.mp3` | **21:09** | 7.4 MB | `01-the-moment.md` |
| 02 | `02-the-commercial-arc.mp3` | **26:58** | 9.3 MB | `02-the-commercial-arc.md` |
| 03 | `03-the-four-pillars.mp3` | **24:05** | 8.5 MB | `03-the-four-pillars.md` |
| 04 | `04-the-seven-industries.mp3` | **21:05** | 7.4 MB | `04-the-seven-industries.md` |
| 05 | `05-anchor-accounts-part-1.mp3` | **17:46** | 6.2 MB | `05-anchor-accounts-part-1.md` |
| 06 | `06-anchor-accounts-part-2.mp3` | **16:25** | 5.8 MB | `06-anchor-accounts-part-2.md` |
| 07 | `07-pursuit-motion-and-lessons.mp3` | **18:49** | 6.6 MB | `07-pursuit-motion-and-lessons.md` |

### Sellers Handbook weave (Eps 8-10 · added 2026-05-13)

| # | File | Duration | Size | Source script |
|---|---|---|---|---|
| 08 | `08-the-sellers-dream-and-the-six-platforms.mp3` | **15:27** | 5.4 MB | `08-the-sellers-dream-and-the-six-platforms.md` |
| 09 | `09-functional-area-discovery.mp3` | **17:34** | 6.2 MB | `09-functional-area-discovery.md` |
| 10 | `10-the-four-level-ladder-and-the-lab.mp3` | **20:16** | 7.1 MB | `10-the-four-level-ladder-and-the-lab.md` |
| | **SERIES TOTAL** | **3 h 19 min** | **70 MB** | |

## Voice cast

| Host | Voice (edge-tts) | Personality cue |
|---|---|---|
| **Keven** *(the practitioner)* | `en-US-AndrewNeural` | Warm · Confident · Authentic · Honest |
| **Jordan** *(the strategist/skeptic)* | `en-US-BrianNeural` | Approachable · Casual · Sincere (slightly faster pace, lower pitch for contrast) |

Same voice cast across all ten episodes — continuity preserved between the original 7-episode arc and the 3-episode Sellers Handbook weave.

## Format

- **Codec:** MP3 (LAME, libmp3lame) · 48 kbps · 24 kHz · mono · 350 ms inter-turn pause
- Standard podcast-grade encoding; universally playable.

## How to regenerate

```bash
cd C:\Stage\Clients\Industries\APEX\docs\podcast\pc-sellersguide
python _build_audio.py 09-functional-area-discovery.md    # one episode
python _build_audio.py --all                              # all ten (sequential)
```

The synth path includes exponential-backoff retry on transient Microsoft TTS 503 errors.

## What's new in Eps 8-10

The Sellers Handbook (`/docs/book/Sellers-Handbook-Agentic-AI-on-Microsoft.html`) is the Microsoft-platform-aligned companion to the Sellers Guide. It adds three dimensions the Sellers Guide alone didn't cover:

- **Episode 8 — The Sellers Dream + Six Growth Platforms.** The unifying picture of how a seller climbs a single practice across years (four-level ladder). Extends the Four Pillars (Fabric/Foundry/Copilot/Purview) to Six Growth Platforms by adding Entra and Dynamics 365 as first-class.
- **Episode 9 — Functional-Area Discovery, the 30-Minute Framework.** Five-question script. One index card output (priority · pain · scenario · bundle · attach). Five functional areas covered (Finance & Risk · Operations & Supply Chain · Marketing & CX · Sales/Revenue/Merchandising · Technology/Data/Talent). Plus the Scenario → Service Mapping Catalog that closes each conversation.
- **Episode 10 — The Four-Level Ladder and the GSSC Lab.** L1 wedge ($25-75K) → L2 Wave 1 ($500K-$2M) → L3 B2B ($5-20M) → L4 B2C ($20-50M+) with the four unlock sentences. The GSSC Lab as the pre-built substrate that lets L1 ship in 5 days and Wave 1 ship in 30. The six-phase seller journey. Closing plays (10-Min Conversation · Objections · BVA-in-5-Bullets · Independence Cheat Sheet · One-Page Pitch Template).

## Editorial discipline applied

Eps 8-10 follow the **conversational style** established in the Services v2 podcast — no chapter/section number citations in spoken dialogue, historical/industry context at every opening, 4-6 minutes per concept with no topic-switching, real disagreement between hosts, one quote-and-react moment per episode, organic synthesis (no announced segments).

Each Handbook-weave episode references back to the original Sellers Guide arc by *concept*, not by episode number — the stair-step is preserved.

## Notes

- All ten episodes carry the **Independence-from-Microsoft** framing established in the original arc revisions — Deloitte does NOT co-sell with Microsoft; recommendation is on the merits.
- All references to **canonical schemas** anchor at **Silver**, not Gold — the corrected architectural framing.
- **ICE** terminology in the audio: per user-confirmed framing.
- The Sellers Handbook weave does not modify Eps 1-7 — they're preserved as-is. Eps 8-10 *extend* the series.
