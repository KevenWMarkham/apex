# CFMP Capabilities Map + Eps 10–11 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a single self-contained interactive HTML capability map for CFMP (10 swimlanes, 80–100 capability boxes, episode + design-doc + code-file traceability, persona/opener/status filters), plus the two new podcast episodes that fill the largest design+code gaps the map surfaces (Ep 10 Flux, Ep 11 Recipes).

**Architecture:** Hand-authored capability inventory in a Python scanner (`_build_capabilities_map.py`) that walks `C:\code\iot_device\`, tags files by capability box, and emits the JSON the HTML embeds inline. The HTML mirrors the Cross-Cloud Study Guide's design language (warm-midnight palette, three-font stack, `.paq-details` collapse pattern). Two new podcast scripts written and audio-produced through the existing `_build_audio.py` + `_apply_music.py` pipeline.

**Tech Stack:** Markdown (scripts) · Python 3 (scanner + audio) · single self-contained HTML · vanilla JS · ffmpeg + edge-tts.

**Design doc:** `docs/plans/2026-05-25-cfmp-capabilities-map-design.md`.

---

## Notes for the executor

- Output location: `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cfmp\`.
- The two new episode files are **appended** (10, 11) — no renumber of existing episodes.
- Vanilla JS only; the map's script must pass `node --check`.
- Episode word target: 5,500–6,500 spoken (verify band 4,800–7,500).
- Commit each task with `git add <path>` then `git commit` (never `git commit -a`).

---

## Task 1: Episode 10 · Flux — Household composition & presence events

**Files:**
- Create: `pc-cfmp/10-flux-household-composition.md`

**Sources to read first:**
- Show bible: `pc-cfmp/00-show-bible-and-format.md` (READ FIRST — format, hosts, content discipline).
- Prior episodes for tone: 01–09 in same folder.
- **Primary source:** `C:\code\iot_device\docs\packs\CFMP-Mobile-Flux-Design.md` IN FULL.
- Code header: `C:\code\iot_device\orchestrator\flux.py` (first 60 lines).
- SQL: `C:\code\iot_device\db\04_flux_events.sql`.

**Episode brief** (cold open + 7 sub-sections + reading + disagreement + carry-forward + further reading):

*Cold open (~300 words):* Marcus Thompson at the cabin in late September. He's been there three weekends in a row. The household profile registers a `partial_absence` from the primary home (Sarah's house, the kids visit Marcus's cabin during shoulder seasons) — but it's *proposed*, not approved. The agent doesn't auto-pause Sarah's home auto-replenish because PERMANENT_DEPARTURE never fires from inference. Sarah confirms the partial_absence; the home Auto-Replenish pauses for three weeks; the cabin StayLot pattern picks up the slack. Open Keven and Reid on the moment — *"this is the substrate beneath every multi-location, multi-season, multi-life-stage household."*

*Conversation sub-sections:*
1. **What Flux is** — household composition + presence events as a *first-class sibling of lots*. Why composition has its own model (a person isn't a property of a lot; they're an actor across many lots).
2. **The 7 kinds across 5 families** — ABSENCE (vacation, partial_absence), ARRIVAL (arrival, permanent_arrival), DEPARTURE (permanent_departure — HITL-only, never inferred), PURPOSE (event — guest visits, holidays), PLACE (move). Each family with a customer moment.
3. **The detected → proposed → approved → active lifecycle** — and why effects fire only on `active`, never on `proposed`. The HITL gate as the architectural defense against false positives.
4. **PERMANENT_DEPARTURE — HITL-only** — why the design refuses to ever infer a permanent_departure (death, divorce, estrangement) — the harm/cost of a false positive is too large. Operator-initiated only.
5. **PLACE — the move pattern** — when a household relocates. The auto-replenish recalibrates, the home channel re-registers, the audit chain carries the old and new addresses.
6. **PURPOSE — guest visits + holidays** — guests flip household_size for the meal-plan (Lane 9). The Lunar New Year visit, Thanksgiving guests, the in-laws for the week. Ties into Ep 11 Recipes (cuisine-breadth for the visiting family).
7. **Azure-native deployment** — `flux.py` runs in the orchestrator; the SQL table sits in `db/04_flux_events.sql`; the lifecycle webhook events flow through the same Cue Bus as fulfillment events.

*Reading:* Reid recommends something on event-driven domain modeling — Vaughn Vernon's *Implementing Domain-Driven Design*, or Greg Young on event sourcing applied to household state. 1–2 paragraphs.

*Disagreement:* Reid argues PERMANENT_DEPARTURE should be inferable with very high confidence + a confirmation prompt — leaving it HITL-only means real life-events are caught months late. Keven defends: the false-positive cost is unbounded; HITL-only is the *honest* choice. Converge on a softer pattern — the system *suggests* PERMANENT_DEPARTURE as a `proposed` event, but never auto-approves; the customer sees the prompt and acts.

*Carry-forward:* (1) composition is a sibling of lots, not a property; (2) HITL gating before effects is the architectural ethic; (3) the move/visit/absence patterns are how CFMP follows the household through life.

*Further reading:* `CFMP-Mobile-Flux-Design.md` (full); `db/04_flux_events.sql`; `orchestrator/flux.py`; live `/architecture` URL; Vernon + Young.

**Length target:** 5,500–6,500 spoken words.

**Verify + commit** — same shape as prior episodes. Verify markers: `## Cold Open`, `### A reading I want to do`, `### One disagreement`, `### What to carry forward`, `## Further reading`, `**KEVEN:**`, `**REID:**`, `Flux`, `proposed`, `active`, `permanent_departure`. No forbidden vocabulary. Word count in band.

Commit: `feat: CFMP podcast — episode 10 Flux household composition`.

---

## Task 2: Episode 11 · Recipes — the meal-plan front door

**Files:**
- Create: `pc-cfmp/11-recipes-meal-plan-front-door.md`

**Sources:**
- Show bible.
- Prior episodes 01–10.
- Code header: `C:\code\iot_device\orchestrator\meal_planner.py` (first 30 lines — the 10-step pipeline).
- The Mobile design doc's existing recipe references — `CFMP-Mobile-Design-Document.md` §6 (any recipe/meal mentions).

**Episode brief:**

*Cold open (~300 words):* Sarah's daughter, mid-week, mentions a dish her friend's mom made at a sleepover — a Korean galbi-jjim. Sarah pulls up a YouTube video, asks CFMP: *"capture this for me."* The agent extracts the ingredients, steps, and servings; flags the gochujang and Korean radish (specialty); checks the household's allergen profile (peanut-free, the daughter's friend); confirms one of the BOPIS providers carries both specialty items. Recipe saved to the family library, tagged Korean + family-friend-shared. Two months later, when Sarah's mother-in-law visits (Flux PURPOSE event, Ep 10), the meal-plan resurfaces galbi-jjim as a Korean-week candidate. Reid: *"this is the meal-plan front door — the side the design has barely opened."*

*Conversation sub-sections:*
1. **The recipe library today vs. tomorrow** — the backend (`meal_planner.py` reads `recipe_library`) is real; the *capture* side is mostly absent. The episode is about closing the front door's gap.
2. **YouTube → Recipe** — paste a cooking-video URL; extract ingredients, steps, servings, timing. Captures the channel + creator as provenance. Reid presses on copyright/attribution; Keven: provenance-stamped, customer's own library, never republished.
3. **Friend-shared + family heirloom** — share via link/SMS; *mom's dishes* with photos + voice narration tagged `family` and `generational`. The Korean grandmother's kimchi recipe; the southern aunt's cornbread.
4. **Restaurant meal repeat** — *"recreate that lamb tagine from [the restaurant]"* — AI reverse-engineers; user iterates. The "I had this on vacation, want it at home" pattern.
5. **Holiday favorites + Flux PURPOSE coupling** — date-keyed recipes that resurface; Thanksgiving · Lunar New Year · Diwali · Easter · Cinco de Mayo · Hanukkah · Lunar New Year. Ties Lane 9 to Lane 2/7 Flux.
6. **Cuisine breadth — the 15 cultures** — Japanese · Chinese · Mexican · South American · Korean · Italian · English · German · Spanish · Indian · Thai · Vietnamese · Mediterranean · Seafood / Pescatarian · regional American. Specialty-ingredient sourcing across providers (gochujang, masa harina, sumac, miso, fish sauce). The honest cross-cuisine ingredient problem.
7. **Allergen-aware import gate** — Hassan's defense-in-depth applied to the recipe-capture path. The dietary filter fires at the SEARCH step; a captured recipe that fails the allergen profile gets the user a friendly *"this recipe contains peanut — your daughter's friend is in this week — flag it?"* before save.

*Reading:* Reid recommends a cooking research piece — Samin Nosrat's *Salt Fat Acid Heat* (cuisine-breadth as a teaching frame), or Kenji López-Alt's *The Food Lab* (recipe-reverse-engineering as a discipline).

*Disagreement:* Hassan vs. Vargas. Hassan: every captured recipe must run the allergen filter at search; no exceptions. Vargas: too aggressive — the customer's *own* library should respect their own choices ("I'm cooking peanut Pad Thai when my daughter's friend isn't here"). Converge: the filter is *contextual* — it fires when Flux says a sensitive guest is present in the active window, not as a global block.

*Carry-forward:* (1) recipes are CFMP's meal-plan front door; (2) capture is the v2 work; (3) cultural breadth is where the cookbook becomes a *household library*.

*Further reading:* `meal_planner.py`; design docs; live `/architecture`; Nosrat, López-Alt.

**Length target:** 5,500–6,500 words. (May reach 7,000 given breadth.)

**Verify + commit** — same shape. Markers: standard + `recipe_library`, `YouTube`, `cuisine`, `gochujang`, `Flux` (cross-ref).

Commit: `feat: CFMP podcast — episode 11 recipes meal-plan front door`.

---

## Task 3: Capability inventory + code scanner

**Files:**
- Create: `pc-cfmp/_build_capabilities_map.py`

**Step 1 — Define the inventory dataclass + 10 lanes**

```python
# pc-cfmp/_build_capabilities_map.py
"""
Scan the iot_device repo, map files to capability boxes,
emit JSON for the Capabilities Map HTML.
"""
from __future__ import annotations
from pathlib import Path
import json, re, sys, datetime
sys.stdout.reconfigure(encoding="utf-8")

IOT = Path(r"C:\code\iot_device")

LANES = [
    {"id":"L1","name":"Discovery & Lot Composition","emoji":"🛒","episode":"03","color":"#5DCAA5"},
    {"id":"L2","name":"Lot Lifecycle, Replenish & Home","emoji":"🛍️","episode":"04","color":"#AFA9EC"},
    {"id":"L3","name":"In-Store Experience","emoji":"🏪","episode":"03+04+06","color":"#F2A623"},
    {"id":"L4","name":"Fulfillment & Pickup","emoji":"🚚","episode":"07","color":"#E24B4A"},
    {"id":"L5","name":"Voice Channel · Sonos","emoji":"🔊","episode":"06","color":"#E8C547"},
    {"id":"L6","name":"Agent Orchestration & MCP","emoji":"🤖","episode":"02","color":"#6FB6E5"},
    {"id":"L7","name":"Trust, Identity, Consent & HIPAA","emoji":"🔒","episode":"08+02","color":"#9B7BE0"},
    {"id":"L8","name":"Operations, Portal & Multi-Tenant","emoji":"⚙️","episode":"05+02","color":"#3DD9C4"},
    {"id":"L9","name":"Recipe Capture & Cultural Breadth","emoji":"🍳","episode":"11","color":"#E87B3C"},
    {"id":"L10","name":"Pairings & Mixers","emoji":"🍷","episode":None,"color":"#C89D3A"},
]

PERSONAS = [
    {"id":"sarah","name":"Sarah Chen","emoji":"👩‍🍳","role":"Power-User Parent"},
    {"id":"robert","name":"Robert Park","emoji":"👴","role":"Senior Shopper"},
    {"id":"diana","name":"Diana Park","emoji":"🤝","role":"Caregiver"},
    {"id":"marcus","name":"Marcus Thompson","emoji":"🏔️","role":"Vacation Renter"},
    {"id":"priya","name":"Priya","emoji":"🛟","role":"Operator"},
]

OPENERS = [
    {"id":"O1","text":"How many AI copies of customer data do you create?","lanes":["L1","L6","L7"]},
    {"id":"O2","text":"When a regulator asks you to reproduce an agent decision, can you?","lanes":["L6","L7"]},
    {"id":"O3","text":"Is your identity reality one primary cloud or genuinely cross-cloud?","lanes":["L7"]},
    {"id":"O4","text":"What does your customer hear from your brand when they're not looking at a screen?","lanes":["L5","L3"]},
    {"id":"O5","text":"How does your operator know a refill cue was suppressed last night?","lanes":["L8","L7","L5"]},
    {"id":"O6","text":"How many providers can deliver a single agent-composed shopping plan?","lanes":["L4","L1"]},
]

# Curated capability boxes — hand-authored. Each carries:
#   id, lane, name, status, episode, design_ref, personas,
#   code_globs (list of relative paths or globs), gaps (list of one-liners)
# Status: "completed" | "in_progress" | "not_started" | "implemented_not_podcasted" | "gap" | "proposed"
# Curate ~8–12 boxes per lane = ~80–100 total.

CAPABILITIES = [
    # ----- Lane 1: Discovery & Lot Composition -----
    {"id":"C1.1","lane":"L1","name":"SCAN-first home screen","status":"completed",
     "episode":"03","design_ref":"CFMP-Mobile-ScanFirst-Design.md §2",
     "personas":["sarah","robert"],
     "code_globs":["mobile/app/page.tsx","mobile/components/ScanView*","orchestrator/scan_history.py"],
     "gaps":[]},
    {"id":"C1.2","lane":"L1","name":"LOT noun + 4 archetypes (Shopping/Replenish/Stay/Care)","status":"completed",
     "episode":"03","design_ref":"CFMP-Mobile-Design-Document.md §4",
     "personas":["sarah","robert","diana","marcus"],
     "code_globs":["orchestrator/lots.py","db/02_lots.sql"],
     "gaps":[]},
    {"id":"C1.3","lane":"L1","name":"Care-Lot — proxy shopping for a loved one","status":"in_progress",
     "episode":"01","design_ref":"CFMP-Mobile-Design-Document.md §2.1 (Diana), §4.5",
     "personas":["diana","robert"],
     "code_globs":["orchestrator/lots.py","orchestrator/customer_profile.py"],
     "gaps":["caregiver-delegation grant flow incomplete"]},
    {"id":"C1.4","lane":"L1","name":"Meal-Plan composition (10-step pipeline)","status":"in_progress",
     "episode":"04","design_ref":"CFMP-Mobile-Design-Document.md §6 + meal_planner.py header",
     "personas":["sarah"],
     "code_globs":["orchestrator/meal_planner.py"],
     "gaps":["recipe-library seeded only; capture front door not built (see Lane 9)"]},
    # (extend the controller to author the remaining ~8 lanes ×8-12 boxes)
    # ... See "Curation guidance" below for the full list.
]
```

**Step 2 — Curate ~80–100 boxes**

The implementer extends `CAPABILITIES` with hand-authored entries across all 10 lanes. **Curation guidance:**

- For lanes 1–8: read the prior episode briefs in `pc-cfmp/01-…md` through `pc-cfmp/09-…md` and the design docs in `C:\code\iot_device\docs\packs\`. Every named feature in an episode becomes a capability box. Episode + design refs from the matching `.md`.
- For lane 9 (Recipes): all boxes from Ep 11 brief; mostly `❓ proposed` since capture is v2.
- For lane 10 (Pairings & Mixers): use the design doc not yet written — mostly `❓ proposed`. The age-gate reuse (Lane 4 `handles_alcohol=true` pattern) is `🟡 partial` because the substrate (provider plug-in + identity HITL) exists.
- Cross-lane references via a `"see_also":["C4.7"]` list on a box.

**Step 3 — Walk the iot_device repo + emit JSON**

```python
def scan_files():
    files = []
    for root in ["orchestrator","mobile/app","portal/app","device_app","db","scripts"]:
        base = IOT / root
        if not base.exists(): continue
        for f in base.rglob("*"):
            if not f.is_file(): continue
            if f.suffix not in {".py",".ts",".tsx",".sql"}: continue
            if "node_modules" in f.parts or "__pycache__" in f.parts: continue
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            lines = text.count("\n") + 1
            role = extract_role(text)
            last_mod = datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat()
            files.append({
                "path": str(f.relative_to(IOT)).replace("\\","/"),
                "lines": lines, "role": role, "last_mod": last_mod
            })
    return files

def extract_role(text: str) -> str:
    # Python: first triple-quote docstring
    m = re.search(r'^"""(.+?)"""', text, re.S | re.M)
    if m:
        first_line = m.group(1).strip().splitlines()[0].strip()
        return first_line[:140]
    # TS/JSX: first /** … */ block
    m = re.search(r'^/\*\*(.+?)\*/', text, re.S | re.M)
    if m:
        return m.group(1).strip().splitlines()[0].strip().lstrip("* ").rstrip()[:140]
    return ""

def match_file_to_capability(file_path: str) -> str | None:
    import fnmatch
    for cap in CAPABILITIES:
        for pat in cap["code_globs"]:
            if fnmatch.fnmatch(file_path, pat) or file_path.startswith(pat):
                return cap["id"]
    return None

def main():
    all_files = scan_files()
    for cap in CAPABILITIES:
        cap["files"] = []
    unmapped = []
    for f in all_files:
        cap_id = match_file_to_capability(f["path"])
        if cap_id:
            for cap in CAPABILITIES:
                if cap["id"] == cap_id:
                    cap["files"].append(f)
                    break
        else:
            unmapped.append(f)
    out = {
        "generated_at": datetime.datetime.now().isoformat(),
        "lanes": LANES,
        "personas": PERSONAS,
        "openers": OPENERS,
        "capabilities": CAPABILITIES,
        "unmapped_count": len(unmapped),
        "unmapped_sample": unmapped[:20],
        "status_histogram": {},
    }
    for cap in CAPABILITIES:
        out["status_histogram"][cap["status"]] = out["status_histogram"].get(cap["status"], 0) + 1
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
```

**Step 4 — Verify scanner**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cfmp"
python _build_capabilities_map.py > _capabilities_data.json
python -c "
import json
d=json.load(open('_capabilities_data.json',encoding='utf-8'))
assert len(d['lanes'])==10
assert len(d['personas'])==5
assert len(d['openers'])==6
print(f'capabilities: {len(d[\"capabilities\"])}')
print(f'unmapped files: {d[\"unmapped_count\"]}')
print('status histogram:', d['status_histogram'])
assert len(d['capabilities'])>=60, 'need at least 60 curated boxes'
"
```

**Step 5 — Commit**

```bash
git add docs/podcast/pc-cfmp/_build_capabilities_map.py
git commit -m "feat: CFMP capabilities-map — scanner + curated inventory"
```

---

## Task 4: Build the Capabilities Map HTML

**Files:**
- Create: `pc-cfmp/CFMP-Capabilities-Map.html`

**Step 1 — Embed `_capabilities_data.json`**

Run `python _build_capabilities_map.py > _capabilities_data.json`. Inline the JSON into the HTML as `const CAP_DATA = {…};` at the top of the `<script>` block.

**Step 2 — Page structure**

Reuse the Cross-Cloud Study Guide's design language. Single self-contained HTML:

- `<head>`: title, Google Fonts (Fraunces / Instrument Sans / JetBrains Mono).
- `<style>`: warm-midnight palette + `:root[data-theme="light"]` light variant + lane colors from `CAP_DATA.lanes` (CSS custom properties); `.swim-lane` row, `.cap-box` card, `.cap-status-*` color modifiers, `.persona-ribbon`, `.opener-chips`, `.cap-side-panel` slide-in.
- `<body>`:
  - `<header>` title + theme toggle.
  - `<section class="openers">` six discovery-opener chips.
  - `<section class="persona-ribbon">` five persona icons.
  - `<section class="status-summary">` histogram bar (one stacked-bar showing the 6 status counts).
  - `<main class="lanes">` 10 swimlane rows; each row = lane header + capability boxes flowing horizontally.
  - `<aside class="cap-side-panel">` slide-in detail panel (initially hidden) showing the clicked box's full info + file list.
  - `<section class="gap-analysis">` aggregated 🔴 + 🟣 + ❓ lists at the bottom.
- `<script>`: `CAP_DATA` + render functions (`renderLanes()`, `renderPersonas()`, `renderOpeners()`, `openCapPanel()`); filter state (active personas, active openers, active statuses) + filter handlers (`toggleStatus()`, `togglePersona()`, `toggleOpener()`).

**Step 3 — Per-box render**

```js
function renderCapBox(cap) {
  const lane = CAP_DATA.lanes.find(l => l.id === cap.lane);
  const ep = cap.episode ? `Ep ${cap.episode}` : '(no episode)';
  const fileCount = (cap.files || []).length;
  return `
    <div class="cap-box cap-status-${cap.status}"
         data-cap-id="${cap.id}"
         data-personas="${(cap.personas||[]).join(',')}"
         data-lane="${cap.lane}"
         style="border-left-color:${lane.color}"
         onclick="openCapPanel('${cap.id}')">
      <div class="cap-status-dot"></div>
      <div class="cap-name">${cap.name}</div>
      <div class="cap-meta">
        <span class="cap-ep">${ep}</span>
        <span class="cap-files">${fileCount} file${fileCount===1?'':'s'}</span>
      </div>
      ${cap.gaps && cap.gaps.length ? `<div class="cap-gap">⚠ ${cap.gaps[0]}</div>` : ''}
    </div>
  `;
}
```

**Step 4 — Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cfmp"
python -c "
html = open('CFMP-Capabilities-Map.html', encoding='utf-8').read()
assert '<section class=\"openers' in html
assert '<section class=\"persona-ribbon' in html
assert 'class=\"swim-lane' in html
assert 'CAP_DATA' in html
assert 'cap-status-completed' in html
assert 'cap-status-proposed' in html
js = html.split('<script>')[1].split('</script>')[0]
assert js.count('{')==js.count('}'), 'JS imbalance'
open('_sgcheck.js','w',encoding='utf-8').write(js)
print('Capabilities Map HTML structurally OK')
"
node --check _sgcheck.js && echo "JS OK" && rm _sgcheck.js
```

**Step 5 — Commit**

```bash
git add docs/podcast/pc-cfmp/CFMP-Capabilities-Map.html docs/podcast/pc-cfmp/_capabilities_data.json
git commit -m "feat: CFMP capabilities-map HTML — 10 swimlanes, filters, side panel"
```

---

## Task 5: Audio for Eps 10 + 11

**Files:**
- Modify: `pc-cfmp/_build_audio.py` (extend EPISODES list).
- Modify: `pc-cfmp/_apply_music.py` (extend EPISODES list).

**Step 1 — Extend `_build_audio.py` EPISODES**

Add to the list:
```python
    "10-flux-household-composition.md",
    "11-recipes-meal-plan-front-door.md",
```

**Step 2 — Extend `_apply_music.py` EPISODES**

Add to the list:
```python
    "10-flux-household-composition.mp3",
    "11-recipes-meal-plan-front-door.mp3",
```

**Step 3 — Build audio for the two new episodes**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cfmp"
python _build_audio.py 10-flux-household-composition.md 11-recipes-meal-plan-front-door.md
```
(Each ~10–12 min wall time.)

**Step 4 — Apply stings**

```bash
python _apply_music.py
```
(Re-applies to all 11; the `_originals/` backup makes it idempotent for the existing 9, and wraps the new 2.)

**Step 5 — Verify**

```bash
ls audio/10-flux-household-composition.mp3 audio/11-recipes-meal-plan-front-door.mp3 && echo "OK"
```

**Step 6 — Commit**

```bash
git add docs/podcast/pc-cfmp/_build_audio.py docs/podcast/pc-cfmp/_apply_music.py docs/podcast/pc-cfmp/audio/10-flux-household-composition.mp3 docs/podcast/pc-cfmp/audio/11-recipes-meal-plan-front-door.mp3
git commit -m "feat: CFMP podcast — audio for episodes 10 (Flux) + 11 (Recipes)"
```

---

## Task 6: Final verification

**Files:** verify only.

**Step 1 — Episode + map + audio counts**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cfmp"
python -c "
import os, json
mds = sorted(f for f in os.listdir('.') if f.endswith('.md'))
assert len(mds) == 12, f'expected 12 .md (00 + 11 eps), got {len(mds)}'
mp3s = sorted(f for f in os.listdir('audio') if f.endswith('.mp3') and not f.startswith('_'))
# expect 11 episode mp3s after stings
print('md:', len(mds), '· episode mp3s:', len(mp3s))
assert len(mp3s) == 11
# capabilities map
html = open('CFMP-Capabilities-Map.html', encoding='utf-8').read()
assert 'CAP_DATA' in html
data = json.load(open('_capabilities_data.json', encoding='utf-8'))
assert len(data['lanes']) == 10
assert len(data['capabilities']) >= 60
print('lanes:', len(data['lanes']), '· capabilities:', len(data['capabilities']))
print('status histogram:', data['status_histogram'])
print('PASS')
"
```

**Step 2 — Smoke-test the map in a browser**

Open `CFMP-Capabilities-Map.html` in a browser: confirm 10 lanes render, persona ribbon toggles dim correctly, opener chips highlight lanes, clicking a capability box opens the side panel with the file list. Check the status histogram at the top reads back the counts in the JSON.

**Step 3 — Commit any fixes**

```bash
git commit -am "fix: CFMP capabilities-map verification fixes" || echo "no fixes needed"
```

---

**End of plan.** 6 tasks. Estimated effort: ~4–6 hours (2 episode scripts + scanner + HTML + audio + verify).
