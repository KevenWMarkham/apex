# Cross-Cloud Agentic Study Guide v2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extend the existing Cross-Cloud Agentic Podcast study guide HTML with a per-episode audio player + synced timeline + screen-pop, an opt-in APEX architecture-linkage and Microsoft self-learning section per episode, and an opt-in APEX stack overview — all in the one file, APEX content collapsed by default.

**Architecture:** A `_build_cues.py` script parses the 8 episode scripts into section cue data (word-count-estimated timestamps) and emits a JS object literal. That cue data plus a player strip, a "Go Deeper" collapsed section, and an APEX stack overview are added to the existing single self-contained HTML. Vanilla JS drives the audio player, timeline, and screen-pop. APEX content lives only inside collapsed `<details>` so the guide's default view stays generic.

**Tech Stack:** Python 3.x (cue generator) · HTML5 `<audio>` + vanilla JS · inline CSS/JS · no external dependencies except Google Fonts.

**Design doc:** `docs/plans/2026-05-15-cross-cloud-agentic-study-guide-v2-design.md` — refer to it for the episode→APEX-layer mapping, the 7 APEX stack layers, and the constraints (APEX opt-in; no audio/script changes; no base re-skin).

**Target file:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\Cross-Cloud-Agentic-Study-Guide.html` (currently 177 KB, 9 tabs, 8 episode panels each with 5 sections).

**Reference file (read-only):** `C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Stacked-Architecture-Narrated.html` — APEX name breakdown, 7-layer stack, semantic palette.

---

## Task 1: Cue generator script

**Files:**
- Create: `pc-cross-cloud-agentic/_build_cues.py`

**Step 1: Write the script**

The script parses each of the 8 episode `.md` files, extracts the section structure, estimates per-section start timestamps by word-count proportion, and prints a JavaScript object literal (`const EP_CUES = {...}`) to stdout.

Logic:
- For each episode, read the `.md`. Sections are delimited by: the `## Cold Open` heading, each `### ` heading inside `## The conversation`, and the closing sections. Simplest robust approach: split the dialogue body into sections at every line matching `^### ` plus the `## Cold Open` section. The cold open is the first section; each `### X` starts a new section; stop at `## Further reading`.
- For each section, capture the section title (the heading text, cleaned) and count the words in that section's body (dialogue text, stage directions stripped).
- Known final-MP3 durations (seconds): `01`=2048, `02`=2356, `03`=2240, `04`=2736, `05`=2537, `06`=2282, `07`=2497, `08`=2222. (These are the post-sting durations 34:08, 39:14, 37:20, 45:36, 42:17, 38:02, 41:37, 37:02.)
- Reserve the stings: spoken window = `duration - 5.0 (opening) - 6.0 (closing) - 0.6 (silences)`. Section start times are computed over the spoken window by cumulative word fraction, then offset by `+5.3` seconds (opening sting + silence) so cue `t` maps into the actual file.
- For each section produce `{t: <int seconds>, title: <str>, point: <str>}`. The `point` is a short key-discussion-point string — derive it from the section's first substantive sentence, OR leave a placeholder the controller fills from the episode extractions. To keep the script self-contained, generate `point` as the section title restated; the controller will replace the `point` text with the curated key points from the design doc's episode extractions during Task 4.
- Emit: `const EP_CUES = {\n  "e1": [ {...}, ... ],\n  ...\n};`

```python
"""
Generate per-episode timeline cue data for the Cross-Cloud Agentic study guide.

Parses each episode script, splits into sections, estimates per-section start
timestamps by word-count proportion of the episode's known MP3 duration
(offset for the 5-second opening sting), and prints a JS object literal.

Usage:
    python _build_cues.py            # prints JS to stdout
    python _build_cues.py > cues.js  # capture
"""
from __future__ import annotations
import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent

# episode id -> (md filename, final mp3 duration in seconds)
EPISODES = {
    "e1": ("01-the-agentic-stack-and-five-principles.md", 2048),
    "e2": ("02-data-foundation-and-no-replication.md", 2356),
    "e3": ("03-agent-runtime-talking-to-gold.md", 2240),
    "e4": ("04-governance-identity-and-safety.md", 2736),
    "e5": ("05-audit-ledger-and-replay.md", 2537),
    "e6": ("06-finops-for-agentic-ai.md", 2282),
    "e7": ("07-multi-cloud-and-portability.md", 2497),
    "e8": ("08-the-sellers-playbook.md", 2222),
}
OPEN_STING = 5.3   # opening sting + sting-to-voice silence
CLOSE_STING = 6.6  # closing sting + silence

STAGE = re.compile(r"\[[^\]]*\]")
EMPH = re.compile(r"(\*\*|\*|__|_)(.+?)\1")
SPEAKER = re.compile(r"^\*\*(KEVEN|REID):\*\*", re.MULTILINE)


def sections(md: str):
    """Return list of (title, body_text) for the episode's spoken sections."""
    # work only on the conversation region: from '## Cold Open' to '## Further reading'
    start = md.find("## Cold Open")
    end = md.find("## Further reading")
    region = md[start:end] if start >= 0 and end >= 0 else md
    # split: '## Cold Open' is one section; each '### ' starts a new one
    out = []
    cur_title, cur_buf = None, []
    for line in region.splitlines():
        h2 = re.match(r"^## (.+)", line)
        h3 = re.match(r"^### (.+)", line)
        if h2 and "Cold Open" in line:
            cur_title, cur_buf = "Cold Open", []
        elif h2 and "The conversation" in line:
            continue  # the conversation wrapper heading — not a section
        elif h3:
            if cur_title:
                out.append((cur_title, "\n".join(cur_buf)))
            cur_title, cur_buf = h3.group(1).strip(), []
        else:
            if cur_title is not None:
                cur_buf.append(line)
    if cur_title:
        out.append((cur_title, "\n".join(cur_buf)))
    return out


def wordcount(text: str) -> int:
    t = STAGE.sub("", text)
    t = EMPH.sub(r"\2", t)
    t = SPEAKER.sub("", t)
    return len(t.split())


def js_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main():
    print("const EP_CUES = {")
    for ep, (fn, dur) in EPISODES.items():
        md = (HERE / fn).read_text(encoding="utf-8")
        secs = sections(md)
        counts = [wordcount(b) for _, b in secs]
        total = sum(counts) or 1
        window = dur - OPEN_STING - CLOSE_STING
        cues = []
        cum = 0
        for (title, _), c in zip(secs, counts):
            t = int(OPEN_STING + (cum / total) * window)
            cues.append((t, title))
            cum += c
        print(f'  "{ep}": [')
        for t, title in cues:
            print(f'    {{t:{t}, title:"{js_escape(title)}", point:"{js_escape(title)}"}},')
        print("  ],")
    print("};")


if __name__ == "__main__":
    main()
```

**Step 2: Run it and inspect**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python _build_cues.py
```

Expected: a `const EP_CUES = { "e1": [ {t:5,title:"Cold Open",...}, ... ], ... };` block. Each episode should have 8-12 cues; timestamps monotonically increasing; first cue `t` ≈ 5; last cue `t` < episode duration.

**Step 3: Sanity-check the output**

```bash
python -c "
import subprocess
out = subprocess.run(['python','_build_cues.py'],capture_output=True,text=True).stdout
assert out.count('\"e1\":') == 1 and out.count('\"e8\":') == 1
assert out.count('{t:') >= 64, 'expected >=64 cues across 8 episodes'
print('cue output OK -', out.count('{t:'), 'cues total')
"
```

**Step 4: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/_build_cues.py
git commit -m "feat: cue generator for study guide timeline"
```

---

## Task 2: Capture cue data + curate the key points

**Files:**
- Reference only: `_build_cues.py` output; the 8 episode extraction summaries in the design doc / episode scripts.

**Step 1: Generate the raw cue JS**

Run `python _build_cues.py` and capture the `EP_CUES` object. This is the timestamp+title scaffold.

**Step 2: Curate the `point` field**

For each cue, replace the placeholder `point` (currently a copy of the title) with a crisp 1-sentence key discussion point for that section — drawn from the episode Content Breakdown already in the study guide (each episode tab's ① section has the per-section summaries). The `point` is what the screen-pop card shows under the section title.

Keep `point` to ~12-22 words. Example for e3 cold-open: `"An agent hammering the SAP production API at peak hour — a Principle 1 violation in production."`

**Step 3: Hold the finalized `EP_CUES` object**

The curated `EP_CUES` JS object is the artifact carried into Task 6 (embedded in the HTML). No file is written in this task — it is a controller-prepared input for Task 6.

(No commit — preparation task.)

---

## Task 3: Add player-strip + APEX + cue CSS to the study guide

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — the `<style>` block

**Step 1: Add the CSS**

Insert a new CSS block before `footer{` (after the `.acr .adef` rule). It must cover:

- `.player` — the player strip container (card, house surface, border)
- `.player audio` — full-width native audio element
- `.timeline` — horizontal track; `.tl-fill` playhead progress; `.tl-marker` clickable section pips positioned absolutely by `left:%`
- `.nowplaying` — the screen-pop card; `.np-pop` keyframe highlight animation on change; `.np-sec` (section title) + `.np-point` (key point)
- `.np-list` — the topic list; `.np-item` rows; `.np-item.active` highlighted
- `.bd-item.active` — active-section highlight in Content Breakdown (reuse existing `.bd-item`, add `.active` modifier — left-border + subtle bg)
- APEX semantic layer palette tokens (scoped, e.g. `--apex-identity:#E87B3C; --apex-data:#6FB6E5; --apex-schema:#9B7BE0; --apex-agent:#3DD9C4; --apex-serving:#E8A33D; --apex-context:#C89D3A; --apex-catalog:#5DCAA5;`) — both dark and light variants if needed (or single set that works on both)
- `.apex-stack` — the stacked-layer diagram: vertical stack of `.apex-layer` bands, each with a left color rule from the palette; `.apex-layer.lit` = highlighted (full color + glow), `.apex-layer.dim` = de-emphasized
- `.apex-link` — the APEX linkage panel inside Go Deeper
- `.godeep` — the Go Deeper `<details>` (reuse `.paq-details` summary styling pattern, or a parallel `.gd-*` set)
- `.learn-list` / `.learn-link` — the Microsoft learning links list (mono labels, external-link affordance)
- `.apex-name` — the A·P·E·X letter breakdown in the Overview stack overview

Keep within the existing house variables (`--bg`, `--surface`, `--border`, `--ink*`, `--teal`, `--purple`, `--amber`, etc.). The APEX semantic palette is additive.

**Step 2: Verify CSS parses**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
css=html.split('<style>')[1].split('</style>')[0]
assert css.count('{')==css.count('}'), 'CSS brace imbalance'
for cls in ['.player','.timeline','.nowplaying','.apex-stack','.apex-layer','.godeep','.learn-link','.apex-name']:
    assert cls in css, f'missing CSS class {cls}'
print('player + APEX CSS present, braces balanced')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/Cross-Cloud-Agentic-Study-Guide.html
git commit -m "feat: study guide v2 — player + APEX + cue CSS"
```

---

## Task 4: Add the player strip to all 8 episode tabs

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — 8 episode panels

**Step 1: Insert the player strip markup**

For each episode panel `e1`…`e8`, insert a player strip immediately after the `</div>` that closes `.ep-head` and before the first `<div class="block">` (the ① Content Breakdown block). The strip:

```html
  <div class="player" data-ep="eN">
    <audio controls preload="none" src="audio/<FILENAME>.mp3"></audio>
    <div class="timeline" data-ep="eN"><div class="tl-fill"></div></div>
    <div class="nowplaying">
      <div class="np-sec">Press play to follow along</div>
      <div class="np-point">The timeline below marks each section of the episode. Click any marker to jump.</div>
    </div>
    <div class="np-list" data-ep="eN"></div>
  </div>
```

Where `<FILENAME>` is the episode's MP3 stem (e.g. `01-the-agentic-stack-and-five-principles`). The `.timeline` markers and `.np-list` rows are populated by JS from `EP_CUES` (Task 6) — the HTML ships them empty.

Each episode panel is unique (the `<h2>` differs), so anchor each Edit on the episode's `</div>\n  </div>\n\n  <div class="block">\n    <div class="block-label"><div class="block-num">1</div><h3>Content Breakdown</h3>` region — the `.ep-head` close followed by the ① block. The `<h2>` text above makes each unique; include enough context.

**Step 2: Verify**

```bash
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
assert html.count('class=\"player\"')==8, 'expected 8 player strips'
assert html.count('<audio controls')==8, 'expected 8 audio elements'
for fn in ['01-the-agentic-stack-and-five-principles','02-data-foundation-and-no-replication','03-agent-runtime-talking-to-gold','04-governance-identity-and-safety','05-audit-ledger-and-replay','06-finops-for-agentic-ai','07-multi-cloud-and-portability','08-the-sellers-playbook']:
    assert f'src=\"audio/{fn}.mp3\"' in html, f'missing audio src {fn}'
print('8 player strips wired with correct relative audio paths')
"
```

**Step 3: Commit**

```bash
git commit -am "feat: study guide v2 — player strip in all 8 episode tabs"
```

---

## Task 5: Add the Go Deeper section (APEX linkage + Microsoft learning) to all 8 episodes

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — 8 episode panels

**Step 1: Insert the Go Deeper block + renumber Vocabulary**

For each episode, insert a new `⑤ Go Deeper` block before the Vocabulary block and renumber Vocabulary `⑤`→`⑥`. Anchor on the unique vocab-block opening (`<div class="block-num">5</div><h3>Vocabulary</h3>` + that episode's first `<dt>` term — see the v1 plan for the per-episode first-term anchors; they are unchanged).

The Go Deeper block:

```html
  <div class="block">
    <div class="block-label"><div class="block-num">5</div><h3>Go Deeper</h3><span class="hint">APEX linkage &amp; Microsoft self-learning · optional</span></div>
    <details class="godeep">
      <summary><span class="gd-sum-label">APEX architecture linkage &amp; Microsoft learning</span><span class="gd-sum-meta">optional · click to open</span></summary>
      <div class="gd-body">
        <div class="apex-link">
          <div class="gd-h">This episode in the APEX architecture stack</div>
          <p>The podcast teaches the vendor-neutral principle. <strong>APEX</strong> — Agent-based Platform for Enterprise eXecution — is Microsoft's productized realization of it. This episode realizes the layer(s) lit below.</p>
          <div class="apex-stack mini">[7 layer bands; the relevant ones get class "lit", others "dim" — per the episode→layer mapping]</div>
        </div>
        <div class="learn">
          <div class="gd-h">Go deeper · Microsoft self-learning</div>
          <ul class="learn-list">[3-5 Microsoft Learn links for this episode]</ul>
        </div>
      </div>
    </details>
  </div>
```

Episode → lit layers (per design doc): e1 all · e2 OneLake-medallion + Connectors · e3 Orchestration/Foundry + MCP · e4 Identity&Trust + Safety · e5 Context/LEDGER + Audit + Observability · e6 Model Gateway + Observability · e7 Model Gateway + Connectors · e8 Service Catalog/Experience.

Microsoft Learn links per episode — use real, stable URLs:
- e1: `https://learn.microsoft.com/training/` (AI fundamentals path) · `https://learn.microsoft.com/azure/ai-foundry/` · `https://learn.microsoft.com/agent-framework/`
- e2: `https://learn.microsoft.com/fabric/` · `https://learn.microsoft.com/fabric/database/mirrored-database/` · `https://learn.microsoft.com/fabric/onelake/`
- e3: `https://learn.microsoft.com/azure/ai-foundry/agents/` · `https://learn.microsoft.com/agent-framework/` · `https://modelcontextprotocol.io/` (MCP)
- e4: `https://learn.microsoft.com/purview/` · `https://learn.microsoft.com/purview/ai-microsoft-purview` (DSPM for AI) · `https://learn.microsoft.com/entra/` · `https://learn.microsoft.com/azure/ai-foundry/responsible-ai/`
- e5: `https://learn.microsoft.com/purview/audit-solutions-overview` · `https://learn.microsoft.com/azure/ai-foundry/how-to/develop/trace-application` · `https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/ai/`
- e6: `https://learn.microsoft.com/azure/cost-management-billing/` · `https://learn.microsoft.com/azure/cost-management-billing/finops/` · `https://learn.microsoft.com/copilot/microsoft-365/`
- e7: `https://learn.microsoft.com/azure/ai-foundry/concepts/foundry-models-overview` · `https://learn.microsoft.com/azure/azure-arc/` · `https://learn.microsoft.com/azure/architecture/`
- e8: `https://learn.microsoft.com/azure/cloud-adoption-framework/` · `https://learn.microsoft.com/azure/well-architected/` · `https://learn.microsoft.com/azure/ai-foundry/`

Each link: `<li class="learn-link"><a href="URL" target="_blank" rel="noopener">Label</a><span class="learn-note">one-line what-it-is</span></li>`.

**Step 2: Verify**

```bash
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
assert html.count('<h3>Go Deeper</h3>')==8
assert html.count('class=\"godeep\"')==8
assert html.count('<div class=\"block-num\">6</div><h3>Vocabulary</h3>')==8
assert html.count('<div class=\"block-num\">5</div><h3>Vocabulary</h3>')==0
assert 'learn.microsoft.com' in html
# APEX appears only inside <details> — check it is not in always-visible prose
print('8 Go Deeper sections; Vocabulary renumbered to 6')
"
```

**Step 3: Commit**

```bash
git commit -am "feat: study guide v2 — Go Deeper (APEX linkage + MS learning) in all 8 episodes"
```

---

## Task 6: Add the APEX stack overview to the Overview tab + embed cue data + player JS

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — Overview panel + the `<script>` block

**Step 1: Add the APEX stack overview to the Overview tab**

Insert a collapsed `<details>` section into the Overview panel (after the Acronym Key section, before `</section>`):

```html
  <div class="ov-section">
    <h3>The APEX architecture stack — optional linkage</h3>
    <p>This series teaches a vendor-neutral framework. For sellers who want it, <strong>APEX</strong> is Microsoft's productized realization of that framework — open the panel below for the linkage.</p>
    <details class="godeep">
      <summary><span class="gd-sum-label">Open the APEX architecture stack</span><span class="gd-sum-meta">optional · click to open</span></summary>
      <div class="gd-body">
        [A·P·E·X name breakdown: Agent-based · Platform · Enterprise · eXecution]
        [the 7-layer .apex-stack diagram, all layers shown]
        [note: APEX is the Microsoft-productized realization; the podcast/study-guide elsewhere stay generic]
      </div>
    </details>
  </div>
```

**Step 2: Embed the cue data**

Insert the finalized `EP_CUES` object (from Task 2) into the `<script>` block, before the checklist code.

**Step 3: Add the player JS**

Append to the `<script>` block: a `paqInit()`-style `playerInit()` that, for each `.player`:
- builds `.tl-marker` pips and `.np-list` rows from `EP_CUES[ep]` (positioned by `t / audio.duration`)
- on `audio.timeupdate`: compute progress → set `.tl-fill` width; find the current cue (last cue with `t <= currentTime`) → update `.nowplaying` (`.np-sec`/`.np-point`), add a `np-pop` animation class on change, set `.active` on the matching `.np-item`, `.tl-marker`, and the matching `.bd-item` in Content Breakdown
- on marker/`.np-item` click: `audio.currentTime = cue.t`
- guard: marker positions need `audio.duration`; on `loadedmetadata` (re)position markers; until then position by the known total duration as fallback
Call `playerInit()` at the end of the script.

**Step 4: Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
assert 'EP_CUES' in html and 'playerInit' in html
assert html.count('Open the APEX architecture stack')==1
js=html.split('<script>')[1].split('</script>')[0]
assert js.count('{')==js.count('}'), 'JS brace imbalance'
assert js.count('(')==js.count(')'), 'JS paren imbalance'
# cue data has all 8 episodes
for ep in ['\"e1\"','\"e8\"']:
    assert ep in html
print('APEX stack overview added; EP_CUES + playerInit present; JS balanced')
"
```

**Step 5: Commit**

```bash
git commit -am "feat: study guide v2 — APEX stack overview + cue data + player JS"
```

---

## Task 7: Final verification

**Files:**
- Verify only: `Cross-Cloud-Agentic-Study-Guide.html`

**Step 1: Structural + discipline verification**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
import sys; sys.stdout.reconfigure(encoding='utf-8')
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
print(f'size: {len(html.encode())//1024} KB')
# structure
assert html.count('<section class=\"panel')==9
assert html.count('class=\"player\"')==8
assert html.count('<audio controls')==8
assert html.count('<h3>Go Deeper</h3>')==8
assert html.count('<div class=\"block-num\">6</div><h3>Vocabulary</h3>')==8
# tag balance
for tag in ['div','section','details','script','style','audio']:
    o=html.count(f'<{tag}'); c=html.count(f'</{tag}>')
    assert o==c, f'{tag} imbalance {o}/{c}'
# APEX opt-in: APEX name must appear ONLY inside collapsed <details>.
# crude check: every 'APEX' occurrence in the body sits within a <details>...</details>
# (manual spot-check acceptable; automated: ensure no 'APEX' in always-visible hero/tabs/breakdown)
hero=html.split('<header')[1].split('</header>')[0]
assert 'APEX' not in hero, 'APEX leaked into the always-visible hero'
tabs=html.split('<div class=\"tabs')[1].split('</div>')[0]
assert 'APEX' not in tabs, 'APEX leaked into the tab bar'
print('structure OK; tags balanced; APEX absent from hero and tab bar')
# content discipline on the generic surface
for t in ['co-sell','strategic partnership','channel partner']:
    assert t.lower() not in html.lower(), f'forbidden term {t}'
print('content discipline clean')
"
```

**Step 2: Open in a browser and smoke-test**

Manual: open the HTML, pick an episode, press play — confirm the timeline fills, the Now Playing card pops at section changes, markers seek, the Go Deeper panel is collapsed and opens to show the APEX linkage + learning links, the Overview APEX stack panel is collapsed by default.

**Step 3: Commit (if any fixes were needed)**

```bash
git commit -am "fix: study guide v2 verification fixes" || echo "no fixes needed"
```

---

## Notes for the executor

- **Order matters:** Task 1 → 2 (cue data) before Task 6 (embeds it). Task 3 (CSS) before 4/5/6 (markup that uses the classes). Tasks 4, 5, 6 each modify the same file — run sequentially, never in parallel.
- **The HTML is one large file** — every Edit must use a unique `old_string`. Episode panels are distinguished by their `<h2>` titles and first vocabulary `<dt>` terms; use enough surrounding context.
- **APEX opt-in is the cardinal rule** — the APEX name and stack appear ONLY inside `<details>` collapsed by default. Never in the hero, tab labels, episode headers, breakdowns, note cards, or vocabulary.
- **No changes** to the audio files, the episode `.md` scripts, or the existing 5 per-episode sections (beyond renumbering Vocabulary 5→6).
- **Reference** `2026-05-15-cross-cloud-agentic-study-guide-v2-design.md` for the episode→layer mapping and the 7 APEX layers; `APEX-Stacked-Architecture-Narrated.html` for the semantic palette and stack content.
- **Vanilla JS only** — no libraries. The audio player is the native `<audio controls>`.
- Existing checklist localStorage persistence must keep working — do not disturb the `paqInit` code.

---

**End of plan.** 7 tasks. Estimated effort: ~2-3 hours (cue generation + curation + CSS + 3 markup passes + JS + verification).
