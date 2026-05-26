# Toyota Zero Day Warranty Podcast — Design

**Date:** 2026-05-14
**Author:** Keven Markham (kmarkham@deloitte.com) · Deloitte's Microsoft Technology & Services Practice
**Status:** Design approved · ready for writing-plans handoff
**Source folders referenced:**
- `C:\Stage\Clients\Industries\Automotive\Toyota\` (account context)
- `C:\Stage\Clients\Industries\Automotive\Toyota\01_account\Outreach_Crotts_ZeroDayWarranty.md`
- `C:\Stage\Clients\Industries\Automotive\Toyota\02_projects\FY27_Pipeline\Fabric_Connected_Vehicle_Analytics\` (HTML companion pack)

---

## Goal

Create a 5-episode podcast series for the Toyota Account Team, anchored on the **Zero Day Warranty agentic scenario** (ORCH-01 Warranty Root-Cause from the AXLE framework · SB06 Warranty Traceability & Cost Avoidance from BRML). The series translates the existing two-document HTML pack (`ZeroDayWarranty_Calculations_and_References.html` + `ZeroDayWarranty_Architecture_Diagrams.html`) into narrative form, expanding to cover the NVIDIA integration that is not yet developed in the email or HTML pack.

## Audience

**Both internal Deloitte Account Team and client-shareable.** Spoken content avoids internal codenames (ORCH-01, BRML, AAML referenced by client-safe names — "the build record domain," "the assembly-line telemetry domain"). Internal mapping lives in episode preambles and the series README, not in the dialog. Independence-from-Microsoft framing (two-contract model, no co-sell language) preserved throughout.

## Architecture

**Pattern:** Conversational two-host podcast in the established APEX podcast family style (Keven + co-host dialog, stair-step pedagogy, real disagreement moments, quote-and-react from primary sources, Further Reading per episode).

**Voice cast:** Keven (en-US-AndrewNeural) + Mia (en-US-AriaNeural). Mia = automotive-engineering register: 18 years on automotive accounts, manufacturing-IT and quality-leadership background. Seventh distinct voice pairing in the APEX podcast family.

**Music sting:** Industrial G-major chord (DTNA-style register) synthesised via ffmpeg additive synthesis. Royalty-free. Automotive-brand-family consistency with DTNA.

**Folder:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-toyota-zero-day-warranty\` (consistent with prior six podcasts: pc-sellersguide, pc-servicesguide, pc-deploymentguide, pc-disney-account, pc-disney-studios, pc-dtna).

## Tech Stack

| Component | Tool |
|---|---|
| Script format | Markdown · **KEVEN:** / **MIA:** dialog markers |
| TTS | `edge-tts` (Microsoft Edge Neural TTS) |
| Audio concatenation | `ffmpeg` |
| Music sting synthesis | `ffmpeg` lavfi `sine` + filter chains (additive synthesis) |
| Output format | MP3 · 24kHz mono · 48 kbps · podcast-standard |
| Excel companion | None planned for this podcast (the HTML pack already serves this role) |

## Episode breakdown

| Ep | Title | Focus | Length |
|---|---|---|---|
| 1 | The Zero Day Warranty Idea | Warranty-cluster moment · 8-12 week / 6-team current state · Toyota's TPS + Jidoka context · CEO Priority 3 · the agentic hypothesis · $4.2M/$2.8M/340% reference scenario · Toyota's Microsoft and NVIDIA footprints | ~28 min |
| 2 | Four Data Domains | Build Record · Connected Vehicle · Quality Event · Assembly Asset · medallion on OneLake · per-VIN joinable Gold views · why these four | ~30 min |
| 3 | The 24-Step Agent and the Microsoft Platform | Microsoft Fabric + Agent Framework + Purview · LEDGER hash chain · DSPM for AI · 24-step agent chain · the $4.2M/$2.8M/340% calculation walked · Independence framing | ~32 min |
| 4 | NVIDIA at the Station (Day-0 Prevention) | Metropolis vision-AI · DeepStream pipelines · Jetson edge inference · RAPIDS for accelerated analytics · the two-fabric architecture | ~30 min |
| 5 | Omniverse, Toyota's NVIDIA Estate, and the 90-Day Path | Woven City Omniverse · Toyota Drive on NVIDIA · NeMo for domain LMs · Triton patterns · NVIDIA AI Enterprise · 90-day pilot plan · Crotts discovery follow-on · Microsoft Account Team coordination | ~30 min |

**Series total:** ~140 minutes · ~28,000 words across 5 episode scripts.

## Source coverage by episode

Each episode ends with a Further Reading section. Sources mapped:

- **Toyota official:** Toyota Newsroom · Toyota Connected NA · TMNA press/IR · Tetsuo Ogawa CEO communications · Woven by Toyota · Toyota Production System primer
- **Industry news/blogs:** Automotive News · Reuters Automotive · Bloomberg Mobility · WardsAuto · The Drive · Electrek · TechCrunch Transportation · ArsTechnica Cars
- **Microsoft Learn:** Microsoft Fabric · Azure AI Foundry · Microsoft Agent Framework SDK · Microsoft Industry Cloud for Manufacturing · Microsoft Purview · DSPM for AI · OneLake · Defender for IoT
- **NVIDIA developer/docs:** NVIDIA Developer Blog · NVIDIA Metropolis · DeepStream · Jetson · RAPIDS · Triton Inference Server · NIM microservices · NeMo · Omniverse · NVIDIA AI Enterprise
- **Industry/research:** SAE International · Society of Automotive Analysts · MIT Industrial Performance Center · AIAG · Industry 4.0 publications

## Production deliverables

| File | Purpose |
|---|---|
| `pc-toyota-zero-day-warranty/README.md` | Series overview · voice cast · audience disclosure · internal mapping table |
| `pc-toyota-zero-day-warranty/00-show-bible-and-format.md` | Style rules for Toyota-specific voice (TPS terms, Jidoka, audit-ready agent framing, Independence-from-Microsoft posture, creative-authorship NOT required since automotive — but talent/operator dignity respected) |
| `01-the-zero-day-warranty-idea.md` | Episode 1 script |
| `02-four-data-domains.md` | Episode 2 script |
| `03-the-24-step-agent-and-microsoft-platform.md` | Episode 3 script |
| `04-nvidia-at-the-station-day-zero-prevention.md` | Episode 4 script |
| `05-omniverse-toyota-nvidia-estate-and-90-day-path.md` | Episode 5 script |
| `_build_audio.py` | Voice synthesis (Andrew + Aria via edge-tts) |
| `_build_music.py` | Industrial G-major sting builder |
| `_apply_music.py` | Idempotent sting wrapper |
| `audio/01-*.mp3` through `audio/05-*.mp3` | Final podcast MP3s |
| `audio/README.md` | Episode durations · voice cast · music disclosure · regeneration instructions |

## Data flow

**Writing phase:** Author each episode markdown using the established APEX podcast family style. Each ~5,500-6,000 words with cold open, stair-step exposition, real disagreement moment, quote-and-react from primary sources, what-to-carry-forward closer, Further Reading.

**Audio generation phase:**
1. `_build_music.py` → generates `opening_sting.mp3` (5s) + `closing_sting.mp3` (6s)
2. `_build_audio.py --all` → parses each episode .md, generates per-segment MP3s via edge-tts (Andrew for KEVEN, Aria for MIA, 350ms inter-turn pauses), concatenates via ffmpeg, outputs `audio/0X-*.mp3`
3. `_apply_music.py` → wraps each episode with opening + 300ms silence + episode + 300ms silence + closing, backs up unstinged originals in `audio/_originals/`

## Error handling

- **edge-tts 503 rate limits:** retry with exponential backoff (5 attempts, 8 → 128 sec)
- **ffmpeg errors:** explicit cwd setting on concat operations to avoid path-resolution issues
- **Idempotence:** `_apply_music.py` keeps stingless backups in `_originals/`, so re-running is safe; parallel jobs do not wipe sibling `_tmp/` dirs

## Testing

- **Per-episode parse test:** confirm DIALOGUE_RE matches every KEVEN/MIA turn (script must emit segment count matching manual review)
- **Audio sanity check:** ffprobe duration on each generated MP3 should be within ±10% of target (~28-32 min)
- **Sting integrity check:** verify opening + closing sting MP3s are 5s ±0.3s and 6s ±0.3s respectively
- **Idempotence check:** running `_apply_music.py` twice should produce identical output (file size + duration unchanged on 2nd run)

## Out of scope

- An Excel play-book companion (the existing HTML pack and the Outreach_Crotts email cover this need)
- 24-Step Chain rows in APEX-Scenario-Chains.xlsx (the Zero Day Warranty scenario is already implicit in ORCH-01 / SB06 — no new scenario to add)
- Translation to Japanese (out of scope for v1; could be a future deliverable for Toyota global)
- Multi-host (3+) voice variations
- Interactive/branching episodes

## Open questions deferred to writing-plans

- Exact word count target per episode (28k total across 5 = ~5,600 each, but Ep 3 likely longer due to 24-step walk)
- Whether to introduce a third voice for direct-quote readings (Toyota newsroom quotes, NVIDIA blog quotes) or have KEVEN/MIA read them inline
- Specific NVIDIA product version anchoring (NIM v1.x, NeMo current, etc.) — defer to draft-time research

---

**Next step:** invoke `superpowers:writing-plans` to produce the bite-sized implementation plan with TDD-style task breakdown.
