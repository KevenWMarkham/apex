# Toyota Zero Day Warranty Podcast Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a 5-episode internal+client-shareable podcast for the Toyota Zero Day Warranty agentic scenario covering the Microsoft AXLE foundation (Eps 1-3) and the NVIDIA extension (Eps 4-5), with full audio production.

**Architecture:** Markdown scripts (KEVEN / MIA dialog) parsed by `edge-tts` for voice synthesis, concatenated by `ffmpeg`, then wrapped with synthesised industrial G-major music stings. Mirrors the established APEX-podcast-family pattern proven across six prior podcasts (Sellers/Services/Deployment Trilogy + Disney Account/Studios + DTNA).

**Tech Stack:** Python 3.x · `edge-tts` (Microsoft Neural TTS) · `ffmpeg` (lavfi `sine` source for music + concat demuxer for audio) · Markdown for scripts · MP3 24kHz mono 48 kbps output.

**Design doc:** `docs/plans/2026-05-14-toyota-zero-day-warranty-podcast-design.md` — refer to this for episode framing, source-coverage lists, and Independence posture rules.

**Reference podcast (closest pattern):** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-dtna-account\` — same automotive-industrial register, similar 5-episode structure, same music-sting style. Use as the copy-template for audio/music build scripts.

---

## Task 1: Folder + Series README + Show Bible

**Files:**
- Create: `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-toyota-zero-day-warranty\README.md`
- Create: `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-toyota-zero-day-warranty\00-show-bible-and-format.md`

**Step 1: Scaffold the folder**

```bash
mkdir -p "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty"
```

**Step 2: Write `README.md`**

Match the pc-dtna-account README structure. Sections:
1. Series title & one-line description
2. Audience disclosure ("both internal Deloitte Account Team prep and client-shareable; spoken content avoids internal codenames")
3. Voice cast table (KEVEN=Andrew, MIA=Aria — note this is the seventh distinct pairing in the APEX family)
4. Episode list (5 episodes with one-line summaries)
5. Internal mapping table (client-safe term → internal nomenclature): "Zero Day Warranty agentic scenario" = ORCH-01 Warranty Root-Cause (AXLE) · SB06 (BRML), build record = BRML, connected vehicle = CVML, quality event = QEML, assembly asset = AAML, audit-ready agent = LEDGER hash chain + Purview audit echo
6. Independence framing reminder (two-contract model, no co-sell)
7. Companion HTML pack references (`ZeroDayWarranty_Calculations_and_References.html` + `ZeroDayWarranty_Architecture_Diagrams.html`)
8. Music + voice disclosure (royalty-free synthesised stings)

**Step 3: Write `00-show-bible-and-format.md`**

Match pc-dtna-account/00-show-bible. Sections:
1. **Voice rules** — KEVEN warm/confident/practitioner; MIA technical/engineering register, 18 years on automotive accounts, manufacturing-IT and quality-leadership background
2. **Toyota-specific style rules:**
   - Use TPS terms (Jidoka, Andon, Kaizen) accurately and respectfully; never as buzzwords
   - Honor operator/cast-member dignity (Toyota's TPS culture treats operators as the heart of quality)
   - Audit-ready framing is non-negotiable — every plays through Purview hash chain
   - Independence-from-Microsoft posture explicit (Deloitte recommends; Microsoft is platform; two contracts; never "co-sell")
   - NVIDIA framing is composable-with-Microsoft, not replacement-of
3. **Production rules** — stair-step pedagogy, cold-open scenes, real disagreement moments, quote-and-react from primary sources, what-to-carry-forward closers, Further Reading per episode
4. **Numbers** — anchor on the $4.2M warranty cost / $2.8M chargeback / 340% improvement / 8-12 weeks → minutes reference scenario; consistent across all 5 episodes

**Step 4: Verify**

```bash
ls "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/"
# Expected: README.md, 00-show-bible-and-format.md
wc -w "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/README.md"
# Expected: 600-1200 words
```

**Step 5: Commit**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git add docs/podcast/pc-toyota-zero-day-warranty/README.md docs/podcast/pc-toyota-zero-day-warranty/00-show-bible-and-format.md
git commit -m "feat: scaffold Toyota Zero Day Warranty podcast (README + show bible)"
```

---

## Task 2: Episode 1 — The Zero Day Warranty Idea

**Files:**
- Create: `pc-toyota-zero-day-warranty/01-the-zero-day-warranty-idea.md`

**Step 1: Write the script** (target ~5,500 words, ~28 min)

**Required sections in order:**

```markdown
# Episode 01 · The Zero Day Warranty Idea

**Builds on:** Toyota IAS QWS pillar · APEX AXLE framework · ORCH-01 anchor scenario
**Run time:** ≈ 28 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: a Toyota assembly plant ambient. 11 PM. A monitor humming.]

**MIA:** I want to start at eleven PM on a Tuesday. A quality engineer at a Toyota plant in Kentucky is staring at a monitor. The connected-vehicle data team just sent over a warranty cluster — a transmission fault pattern on Camry builds from a specific six-week production window. Three plants involved. Three suppliers in scope. Six teams about to be pulled into the investigation.

[pause]

**KEVEN:** And what she knows, right now —

**MIA:** *She knows it's going to take 8 to 12 weeks to trace this back to the factory minute.* That's the current state. Six teams across Manufacturing, Quality, Supplier Quality, Toyota Connected, Warranty, and Finance. Hundreds of hours of cross-system reconciliation...

[continues through cold open]

---

## The conversation

### Why warranty cost reduction matters at Toyota right now

### The current state — 8 to 12 weeks across six teams

### Toyota's production context — TPS, Jidoka, the 14 NA plants

### The Zero Day Warranty hypothesis — compose the four domains, single audit-ready agent

### The $4.2M / $2.8M / 340% reference scenario

### Toyota's existing Microsoft and NVIDIA footprints

### What we'll cover across the five episodes

### A reading I want to do

### One disagreement

### What to carry forward

---

## Further reading

### Toyota official
- Toyota Newsroom · [pressroom.toyota.com](https://pressroom.toyota.com/)
- Toyota Connected NA
- TMNA investor relations
- Tetsuo "Ted" Ogawa CEO communications
- Toyota Production System primer (lean.org · TPS overview)

### Microsoft Learn
- Microsoft Fabric overview
- Microsoft Agent Framework SDK
- Microsoft Purview

### Industry context
- Automotive News
- Reuters Automotive
- SAE International
- AIAG

### From the APEX framework
- AXLE Practice · ORCH-01 Warranty Root-Cause
- BRML schema family
- Companion HTML pack: ZeroDayWarranty_Calculations_and_References.html + ZeroDayWarranty_Architecture_Diagrams.html

---

**End of Episode 01**
*≈ 5,500 words · target 28 minutes at conversational pace*
```

**Key content beats:**
- Open cold with the quality engineer at 11 PM
- Establish 8-12 week / 6-team baseline with credibility
- Place in TPS / Jidoka context — Ogawa's CEO Priority 3
- Introduce the four-domain hypothesis (Build Record / Connected Vehicle / Quality Event / Assembly Asset) without diving deep — that's Ep 2
- Walk the $4.2M / $2.8M / 340% reference scenario tightly
- Note Toyota's existing Microsoft footprint (Toyota Connected on Azure) and NVIDIA footprint (Woven City Omniverse, Toyota Drive AV)
- Hook to Eps 2-3 (Microsoft AXLE deep dive) and Eps 4-5 (NVIDIA extension)
- Have a real disagreement: MIA pushes back on "should we lead with NVIDIA or with Microsoft" — KEVEN says "Microsoft foundation first because warranty data lives in Fabric; NVIDIA arrives as Day-0 prevention extension"

**Step 2: Verify parse + word count**

```bash
python -c "
import re, sys
text = open('C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/01-the-zero-day-warranty-idea.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|MIA):\*\*', text, re.MULTILINE))
print(f'words: {words} (target 5300-5800)')
print(f'segments: {segments} (target 50-90)')
assert 5000 < words < 6500, f'word count out of range: {words}'
assert 40 < segments < 100, f'segment count out of range: {segments}'
print('OK')
"
```

Expected: `OK` with words in range and segments in range.

**Step 3: Commit**

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/01-the-zero-day-warranty-idea.md
git commit -m "feat: write Toyota podcast Ep 1 — The Zero Day Warranty Idea"
```

---

## Task 3: Episode 2 — Four Data Domains

**Files:**
- Create: `pc-toyota-zero-day-warranty/02-four-data-domains.md`

**Step 1: Write the script** (target ~5,800 words, ~30 min)

**Required content beats:**
- Cold open: a data architect's whiteboard moment — drawing the four domains
- **Build Record domain (BRML, client-name: "Vehicle Build Record")** — every VIN's complete factory history per station/shift/tool/supplier-lot/operator
- **Connected Vehicle domain (CVML, client-name: "Connected Vehicle Warranty Data")** — claims and failure modes tied back to VIN
- **Quality Event domain (QEML, client-name: "Quality Events on the Line")** — inspections, measurements, defects captured during build
- **Assembly Asset domain (AAML, client-name: "Assembly Line Telemetry")** — equipment state, throughput, asset events
- Bronze → Silver → Gold medallion on OneLake
- Per-VIN joinability at Gold layer is the canonical foundation
- Why these four domains (not 3 or 5) — they map cleanly to Toyota's existing org boundaries (Manufacturing, Connected, Quality, Production Engineering)
- Microsoft Industry Cloud for Manufacturing context
- One disagreement: MIA says "the supplier lot dimension is the most operationally underused signal" — KEVEN agrees but notes operator-cohort signal is the politically harder one to surface

**Required structure:** Same template sections as Ep 1 (Cold Open, Conversation, Reading, Disagreement, What to Carry Forward, Further Reading)

**Step 2: Verify**

```bash
python -c "
import re
text = open('C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/02-four-data-domains.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|MIA):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5300 < words < 6500
assert 50 < segments < 110
print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/02-four-data-domains.md
git commit -m "feat: write Toyota podcast Ep 2 — Four Data Domains"
```

---

## Task 4: Episode 3 — The 24-Step Agent and the Microsoft Platform

**Files:**
- Create: `pc-toyota-zero-day-warranty/03-the-24-step-agent-and-microsoft-platform.md`

**Step 1: Write the script** (target ~6,200 words — slightly longer due to 24-step walk, ~32 min)

**Required content beats:**
- Cold open: imagining the agent's run-log at 7 AM — the 24 audit rows it just wrote overnight
- **Microsoft Fabric** as the unified data layer — Bronze/Silver/Gold on OneLake
- **Microsoft Agent Framework SDK** (hosted on Azure AI Foundry Agent Service) as the agent runtime
- **Microsoft Purview** for governance/audit + DSPM for AI for data security posture management
- **LEDGER hash chain** — every agent decision = a hash-chained audit row, replay-token validated
- Walk the 24-step agent chain end-to-end (don't enumerate all 24 — group into the 6 phases: Detect → Trace → Compose → Validate → Recommend → Attest)
- HITL gates — the quality engineer reviews the cohort × station × tool interaction before the chargeback evidence package is finalised
- The $4.2M / $2.8M / 340% calculation walked step-by-step (calculation transparency)
- Independence framing crisp: "Deloitte recommends what Toyota should build; Microsoft is the platform Toyota licenses directly; two contracts; no co-sell motion"
- One disagreement: MIA pushes that the 24-step chain feels long; KEVEN explains it's the audit posture that earns the long chain — each step is one audit row

**Step 2: Verify**

```bash
python -c "
import re
text = open('C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/03-the-24-step-agent-and-microsoft-platform.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|MIA):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5800 < words < 7000
assert 60 < segments < 130
print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/03-the-24-step-agent-and-microsoft-platform.md
git commit -m "feat: write Toyota podcast Ep 3 — The 24-Step Agent + Microsoft Platform"
```

---

## Task 5: Episode 4 — NVIDIA at the Station (Day-0 Prevention)

**Files:**
- Create: `pc-toyota-zero-day-warranty/04-nvidia-at-the-station-day-zero-prevention.md`

**Step 1: Write the script** (target ~5,800 words, ~30 min)

**Required content beats:**
- Cold open: vision-AI catching a defect at the station 0.4 seconds after it forms
- **The inversion thesis** — Zero Day Warranty (Eps 1-3) traces failures back to the factory minute; Day-0 Prevention catches them in the factory minute. Together they close the loop.
- **NVIDIA Metropolis** — vision-AI platform at the station
- **DeepStream pipelines** — streaming vision/sensor data into inference pipelines
- **Jetson edge inference** — on-station compute close to the camera
- **RAPIDS** for accelerated analytics at the Fabric layer (GPU-accelerated dataframe operations on the BRML/QEML data)
- **The two-fabric architecture** — Microsoft Fabric for warranty/build data; NVIDIA NIM/Triton for inline vision inference
- Where the stacks compose cleanly (Fabric ingests inference results from NIM/Triton)
- Where they negotiate (data sovereignty, latency requirements at the station, governance)
- One disagreement: KEVEN pushes that NVIDIA is "infrastructure for Toyota Day-0"; MIA pushes that NVIDIA is also "model authoring + retrieval (NeMo) which is Ep 5 territory"
- Reference Toyota's existing NVIDIA exposure as the credibility anchor

**Step 2: Verify**

```bash
python -c "
import re
text = open('C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/04-nvidia-at-the-station-day-zero-prevention.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|MIA):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5500 < words < 6500
assert 50 < segments < 110
print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/04-nvidia-at-the-station-day-zero-prevention.md
git commit -m "feat: write Toyota podcast Ep 4 — NVIDIA at the Station (Day-0 Prevention)"
```

---

## Task 6: Episode 5 — Omniverse, Toyota's NVIDIA Estate, and the 90-Day Path

**Files:**
- Create: `pc-toyota-zero-day-warranty/05-omniverse-toyota-nvidia-estate-and-90-day-path.md`

**Step 1: Write the script** (target ~5,800 words, ~30 min)

**Required content beats:**
- Cold open: a Woven City scene — Toyota already runs Omniverse at city scale; the bridge to plant scale
- **Toyota's existing NVIDIA estate:**
  - Woven by Toyota / Woven City — Omniverse for city-scale digital twin
  - Toyota Drive — NVIDIA Drive for autonomous vehicle development
- **Omniverse for plant simulation** — digital twin extension of the BRML/QEML/AAML data foundation
- **NVIDIA NeMo** for domain-language models and retrieval over warranty data + build records + supplier specs
- **Triton Inference Server** patterns — model serving at scale
- **NVIDIA AI Enterprise** as the umbrella licensing/support stack
- The 90-day pilot plan at one Toyota plant — discovery (week 1-2), data access (week 3-6), agent build (week 7-10), HITL validation (week 11-12), pilot decision (week 12-13)
- Where the Chris Crotts discovery conversation leads — Quality leadership at the plants, Toyota Connected, or Manufacturing IT as the sponsor
- Microsoft Account Team coordination — BVA ($75-200K), ECIF ($200-500K), Azure Credits ($100-500K) funding strategy
- Closing: the Zero Day Warranty journey across 5 episodes; the strategic case for Toyota to move first
- One disagreement: MIA argues Toyota Connected should be the entry point; KEVEN argues plant-side Quality leadership has the budget and urgency

**Step 2: Verify**

```bash
python -c "
import re
text = open('C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/05-omniverse-toyota-nvidia-estate-and-90-day-path.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|MIA):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5500 < words < 6500
assert 50 < segments < 110
print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/05-omniverse-toyota-nvidia-estate-and-90-day-path.md
git commit -m "feat: write Toyota podcast Ep 5 — Omniverse + Toyota NVIDIA Estate + 90-Day Path"
```

---

## Task 7: Build audio synthesis script

**Files:**
- Create: `pc-toyota-zero-day-warranty/_build_audio.py`

**Step 1: Copy `pc-dtna-account/_build_audio.py` as template**

```bash
cp "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-dtna-account/_build_audio.py" \
   "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/_build_audio.py"
```

**Step 2: Apply 3 edits to the copy**

Edit 1 — `VOICE_DANA` → `VOICE_MIA`, value `"en-US-AriaNeural"`:

```python
VOICE_KEVEN = "en-US-AndrewNeural"     # Trilogy continuity host
VOICE_MIA   = "en-US-AriaNeural"       # 18-yr automotive partner: Mfg-IT + Quality
```

Edit 2 — `DIALOGUE_RE` pattern speaker names `DANA` → `MIA`:

```python
DIALOGUE_RE = re.compile(
    r"^\*\*(KEVEN|MIA):\*\*\s*([\s\S]*?)"
    r"(?=^\*\*(?:KEVEN|MIA):\*\*|^##|^---|\Z)",
    re.MULTILINE,
)
```

Edit 3 — `EPISODES` list:

```python
EPISODES = [
    "01-the-zero-day-warranty-idea.md",
    "02-four-data-domains.md",
    "03-the-24-step-agent-and-microsoft-platform.md",
    "04-nvidia-at-the-station-day-zero-prevention.md",
    "05-omniverse-toyota-nvidia-estate-and-90-day-path.md",
]
```

Edit 4 — speaker-to-voice dispatch in `synth_episode()`:

```python
if speaker == "KEVEN":
    voice, rate, pitch = VOICE_KEVEN, RATE_KEVEN, PITCH_KEVEN
else:
    voice, rate, pitch = VOICE_MIA, RATE_MIA, PITCH_MIA
```

(Add `RATE_MIA = "-2%"` and `PITCH_MIA = "+0Hz"` near the other voice constants.)

Edit 5 — docstring header updated to Toyota Zero Day Warranty.

**Step 3: Smoke test — parse Ep 1, do NOT synthesize**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty"
python -c "
from _build_audio import parse_script
text = open('01-the-zero-day-warranty-idea.md', encoding='utf-8').read()
segs = parse_script(text)
print(f'parsed {len(segs)} segments')
speakers = set(s[0] for s in segs)
print(f'speakers: {speakers}')
assert speakers == {'KEVEN', 'MIA'}, f'unexpected speakers: {speakers}'
print('OK')
"
```

Expected: `OK` with both `KEVEN` and `MIA` in the speaker set, segment count matching Task 2 verification.

**Step 4: Commit**

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/_build_audio.py
git commit -m "feat: add Toyota podcast audio build script (Andrew + Aria voice pair)"
```

---

## Task 8: Build music sting builder

**Files:**
- Create: `pc-toyota-zero-day-warranty/_build_music.py`

**Step 1: Copy `pc-dtna-account/_build_music.py` as template**

```bash
cp "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-dtna-account/_build_music.py" \
   "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/_build_music.py"
```

**Step 2: Apply 1 edit** — update the module docstring header from "DTNA Account Podcast" to "Toyota Zero Day Warranty Podcast". Keep the musical structure identical (industrial G-major arpeggio + sustained chord) — this is the automotive-brand-family register and Toyota inherits it directly.

Replace lines 1-23 (the docstring) with:

```python
"""
Build royalty-free music stings for the Toyota Zero Day Warranty Podcast.

Two stings — opening and closing — synthesised entirely via ffmpeg from
sine-wave additive synthesis. Industrial G-major register, matching the
DTNA Account Podcast — automotive-brand-family consistency across the
APEX automotive podcasts. Heavy-duty, grounded, manufacturing-floor feel.

  opening_sting.mp3 (~5 sec)  ascending G3-D4-G4 power chord · warm horn timbre
  closing_sting.mp3 (~6 sec)  sustained G-major chord with low fundamental

Both files are 24kHz mono MP3 at 48 kbps — matching the podcast's encoding
parameters so they concat cleanly with the episode tracks.

NOTE: this is royalty-free synthesised audio. It is not, and is not derived
from, any copyrighted composition. The Account Team should be explicit about
this in any external use of these files.

Usage:
    python _build_music.py
"""
```

**Step 3: Run the build**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty"
python _build_music.py
```

Expected output:
```
Building opening_sting.mp3 ...
  -> opening_sting.mp3 (xx KB)
Building closing_sting.mp3 ...
  -> closing_sting.mp3 (xx KB)
Done.
```

**Step 4: Verify durations**

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 opening_sting.mp3
# Expected: 4.9 - 5.1
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 closing_sting.mp3
# Expected: 5.9 - 6.1
```

**Step 5: Commit**

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/_build_music.py docs/podcast/pc-toyota-zero-day-warranty/opening_sting.mp3 docs/podcast/pc-toyota-zero-day-warranty/closing_sting.mp3
git commit -m "feat: add Toyota podcast music stings (industrial G-major, automotive register)"
```

---

## Task 9: Build music sting applier

**Files:**
- Create: `pc-toyota-zero-day-warranty/_apply_music.py`

**Step 1: Copy `pc-dtna-account/_apply_music.py` as template**

```bash
cp "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-dtna-account/_apply_music.py" \
   "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/_apply_music.py"
```

**Step 2: Apply 1 edit** — update the `EPISODES` list to match the Toyota 5-episode filenames:

```python
EPISODES = [
    "01-the-zero-day-warranty-idea.mp3",
    "02-four-data-domains.mp3",
    "03-the-24-step-agent-and-microsoft-platform.mp3",
    "04-nvidia-at-the-station-day-zero-prevention.mp3",
    "05-omniverse-toyota-nvidia-estate-and-90-day-path.mp3",
]
```

Update the module docstring to refer to Toyota.

**Step 3: Lint check (no audio dir yet)**

```bash
python -c "import _apply_music; print('parsed OK')"
# Expected: parsed OK
```

**Step 4: Commit**

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/_apply_music.py
git commit -m "feat: add Toyota podcast music-sting applier"
```

---

## Task 10: Generate all 5 episode MP3s

**Files:**
- Create: `pc-toyota-zero-day-warranty/audio/01-*.mp3` through `audio/05-*.mp3`

**Step 1: Run the audio build (background, expect 30-90 minutes total for 5 episodes via edge-tts rate limits)**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty"
python _build_audio.py --all
```

For long-running execution, use background mode and let the harness notify on completion. Do NOT poll.

**Step 2: Verify all 5 MP3s exist + are in target duration band**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/audio"
for ep in 01-the-zero-day-warranty-idea 02-four-data-domains 03-the-24-step-agent-and-microsoft-platform 04-nvidia-at-the-station-day-zero-prevention 05-omniverse-toyota-nvidia-estate-and-90-day-path; do
  dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${ep}.mp3" 2>/dev/null)
  printf "  %s: %ss\n" "$ep" "$dur"
done
```

Expected: each duration between 1500 and 2100 seconds (25-35 min). Ep 3 likely longest.

**Step 3: Commit** (note — MP3s are binary; if `.gitignore` excludes audio/, skip git add for binaries)

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/audio/
git commit -m "feat: generate Toyota podcast Episodes 1-5 audio (edge-tts Andrew + Aria)"
```

---

## Task 11: Apply music stings to all 5 episodes

**Files:**
- Modify in place: `audio/01-*.mp3` through `audio/05-*.mp3`
- Create backups: `audio/_originals/01-*.mp3` through `audio/_originals/05-*.mp3`

**Step 1: Run the applier**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty"
python _apply_music.py
```

Expected output (one line per episode):
```
  -> 01-the-zero-day-warranty-idea.mp3  |  XX:XX  (stings applied)
  -> 02-four-data-domains.mp3  |  XX:XX  (stings applied)
... etc
Done.
```

**Step 2: Verify idempotence (run again, expect identical output)**

```bash
python _apply_music.py
# Expected: same durations as Step 1; no errors
```

**Step 3: Verify backups created**

```bash
ls audio/_originals/
# Expected: 5 backed-up MP3 files (the stingless versions)
```

**Step 4: Commit**

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/audio/
git commit -m "feat: apply Toyota podcast music stings to all 5 episodes"
```

---

## Task 12: Audio README

**Files:**
- Create: `pc-toyota-zero-day-warranty/audio/README.md`

**Step 1: Write audio README** matching the pc-dtna-account/audio/README.md structure.

**Required sections:**
1. Title + one-line description
2. Episode table with file name, duration (from ffprobe), file size, source script — filled with actual values from Task 11 output
3. Voice cast table — KEVEN (Andrew) + MIA (Aria) — note the seventh distinct pairing
4. Music disclosure section — royalty-free synthesised stings, automotive-industrial G-major register matching DTNA, explicit "not derived from any copyrighted Toyota or NVIDIA composition"
5. Format spec — MP3 24kHz mono 48 kbps, 350ms inter-turn pause, 300ms sting-to-voice silence
6. Regeneration instructions — `_build_audio.py`, `_build_music.py`, `_apply_music.py` order
7. Folder structure diagram (`audio/` + `audio/_originals/`)
8. Series content overview — 5 episodes with one-line summaries each
9. Notes: internal-use-and-client-shareable disclosure; Independence-from-Microsoft posture; companion HTML pack reference

**Step 2: Verify durations match actual files**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/audio"
for f in 0*.mp3; do
  dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f")
  size=$(du -k "$f" | cut -f1)
  printf "%-60s %ss  %s KB\n" "$f" "$dur" "$size"
done
```

Use this output to fill the README table accurately.

**Step 3: Commit**

```bash
git add docs/podcast/pc-toyota-zero-day-warranty/audio/README.md
git commit -m "docs: write Toyota podcast audio README"
```

---

## Final verification

After Task 12 commit:

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty"
ls -la
# Expected files:
#   README.md, 00-show-bible-and-format.md
#   01..05 .md scripts
#   _build_audio.py, _build_music.py, _apply_music.py
#   opening_sting.mp3, closing_sting.mp3
#   audio/  (folder with 5 final MP3s + _originals/ + README.md)
```

```bash
wc -w 0*.md
# Expected: each .md episode in 5,000-6,500 word range
```

```bash
git log --oneline | head -15
# Expected: 12 commits matching the task names above
```

---

## Notes for the executor

- **Order matters.** Tasks 2-6 (episode scripts) MUST complete before Task 7 (audio script needs scripts to test against), Task 7 before Task 10, Task 10 before Task 11, Task 11 before Task 12.
- **Tasks 2-6 can run in parallel** if dispatching via subagent-driven-development (each episode is independent content work).
- **Task 10 is long-running** (30-90 min via edge-tts) — use background execution and notification.
- **Idempotence:** Tasks 8, 10, 11 are idempotent — re-running them is safe and expected during development.
- **No external network needed** for music sting build (Task 8) — pure ffmpeg synthesis.
- **edge-tts (Task 10) does need network** to call Microsoft Edge Neural TTS endpoints.
- **Reference the design doc** `docs/plans/2026-05-14-toyota-zero-day-warranty-podcast-design.md` for any content-question that arises during script-writing tasks.
- **Reference the source pack** — `C:\Stage\Clients\Industries\Automotive\Toyota\02_projects\FY27_Pipeline\Fabric_Connected_Vehicle_Analytics\ZeroDayWarranty_Calculations_and_References.html` and `ZeroDayWarranty_Architecture_Diagrams.html` for the technical content, $4.2M/$2.8M/340% calculation breakdown, the 24-step chain, and the NVIDIA stack details.
- **Reference the Crotts outreach email** — `C:\Stage\Clients\Industries\Automotive\Toyota\01_account\Outreach_Crotts_ZeroDayWarranty.md` for tone, framing, and the internal-mapping table.
- **DRY rule:** the audio/music scripts copy verbatim from pc-dtna-account — do not invent a new pattern; the automotive-brand-family consistency is intentional.
- **YAGNI rule:** no Excel companion needed (HTML pack covers this); no APEX-Scenario-Chains.xlsx update needed (ORCH-01 / SB06 already cover this scenario).

---

**End of plan.** Total tasks: 12. Estimated effort: 8-12 hours for scripts (Tasks 1-6) + 30-90 min audio gen (Task 10) + 10 min everything else.
