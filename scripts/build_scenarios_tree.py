"""Build the docs/scenarios/ folder tree from extracted chains + scenario library."""

from __future__ import annotations

import io
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path("docs/scenarios")

# Load featured chains — from the canonical catalog JSON if it exists, else from the
# scratch extract (legacy path used on first run before _catalog/featured-chains.json exists).
_primary = ROOT / "_catalog" / "featured-chains.json"
_scratch = ROOT / "_featured_chains.json"
if _primary.exists():
    chains = json.load(open(_primary, encoding="utf-8"))
elif _scratch.exists():
    chains = json.load(open(_scratch, encoding="utf-8"))
else:
    # Re-extract from the narrated HTML if no JSON exists yet
    _html = open("docs/reference/APEX-Stacked-Architecture-Narrated.html", encoding="utf-8").read()
    _pattern = re.compile(r'<details[^>]*?>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>', re.DOTALL)
    _ROW_LABELS = ["r-scenario", "r-solution", "r-usecase", "r-service", "r-persona", "r-kpi"]
    _ROW_NAMES = ["Scenario", "Solution", "Use Case", "Service", "Persona", "KPI"]
    def _strip_tags(s: str) -> str:
        s = re.sub(r'<br\s*/?>', '\n', s)
        s = re.sub(r'<[^>]+>', ' ', s)
        return re.sub(r'\s+', ' ', s).strip()
    chains = []
    _PRACTICES = ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]
    for _m in _pattern.finditer(_html):
        _summary, _body = _m.group(1), _m.group(2)
        if 'r-scenario' not in _body:
            continue
        _full = _strip_tags(_summary)
        _title = _full.split(' Service ')[0].strip() if ' Service ' in _full else _full[:80]
        _m2 = re.match(r'^(\d{2})\s+(.*)$', _title)
        if _m2:
            _title = _m2.group(2).strip()
        _rows = {}
        for _name, _cls in zip(_ROW_NAMES, _ROW_LABELS):
            _rm = re.search(rf'{_cls}[^>]*>.*?<div class="cbg-text">(.*?)</div>', _body, re.DOTALL)
            _rows[_name] = _strip_tags(_rm.group(1)) if _rm else ""
        chains.append({"title": _title, **_rows})
    for _i, _c in enumerate(chains):
        _c["practice"] = _PRACTICES[_i // 5]
        _c["index_in_practice"] = (_i % 5) + 1
    print(f"Re-extracted {len(chains)} chains from narrated HTML")

# Re-extract compact library from the HTML
html = open("docs/reference/APEX-Stacked-Architecture-Narrated.html", encoding="utf-8").read()
lib_m = re.search(r"const APEX_SCENARIO_LIBRARY\s*=\s*(\{.*?\});", html, re.DOTALL)
library = json.loads(lib_m.group(1))

PRACTICE_META = {
    "RC":   ("Retail & Consumer", "amber", "#F2A93B",
             "Consumer-goods, grocery, apparel, specialty retail. Margin, shrink, loyalty, omnichannel."),
    "HLS":  ("Health, Life Sciences", "crimson", "#D34848",
             "Payer, Provider, Life Sciences. Claims, clinical decision support, population health, trials."),
    "ER":   ("Energy & Resources", "gold", "#E3B657",
             "Power utilities, oil & gas, mining. Reliability, integrity, yield, compliance."),
    "AXLE": ("Automotive & Manufacturing", "teal", "#44B8A8",
             "Automotive OEM + Tier 1 / discrete & process manufacturing. OEE, quality, supply chain, dealer."),
    "TMT":  ("Technology, Media, Telecom", "violet", "#8E7AD6",
             "SaaS/hyperscaler tech, media & entertainment, telecom operators. ARPU, churn, network health."),
    "TH":   ("Travel & Hospitality", "sky", "#6FB9E8",
             "Airlines, hotels, car rental, cruise. Guest experience, IROPS, revenue management."),
    "ICE":  ("Industrial, Construction, Equipment", "ember", "#E37856",
             "Industrial equipment OEMs, construction, heavy equipment. Field service, warranty, EaaS."),
}
PRACTICES = list(PRACTICE_META.keys())


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[\u2014\u2013\u2212]", "-", s)  # em dash / en dash / minus
    s = re.sub(r"[^a-z0-9\- ]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s


def scenario_folder_name(idx: int, title: str) -> str:
    return f"{idx:02d}-{slugify(title)}"


# --- Step 1: Relocate existing "Cold-Chain Excursion" folder into RC/01-... -------------
# Use copy-not-move so locked files (DOCX open in Word) don't abort the build.
# After this runs cleanly, user can delete the source folder manually.
existing = ROOT / "Cold-Chain Excursion"
rc_target_dir = ROOT / "RC" / scenario_folder_name(1, chains[0]["title"])
moved_existing = False
copy_warnings: list[str] = []
if existing.exists():
    rc_target_dir.mkdir(parents=True, exist_ok=True)
    for f in existing.iterdir():
        if not f.is_file():
            continue
        dest = rc_target_dir / f.name
        if dest.exists():
            continue
        try:
            shutil.copy2(str(f), str(dest))
        except PermissionError as exc:
            copy_warnings.append(f"  WARN: could not copy {f.name} ({exc.strerror}); source remains at {f}")
    # Only try removing originals that copied successfully; skip locked ones
    for f in existing.iterdir():
        if not f.is_file():
            continue
        dest = rc_target_dir / f.name
        if dest.exists() and dest.stat().st_size == f.stat().st_size:
            try:
                f.unlink()
            except PermissionError:
                copy_warnings.append(f"  WARN: could not remove source {f.name} (file is in use)")
    # Drop the source folder only if now empty
    try:
        existing.rmdir()
        moved_existing = True
    except OSError:
        pass
    print(f"Copied existing folder -> {rc_target_dir}")
    for w in copy_warnings:
        print(w)


# --- Step 2: Per-scenario README seed ---------------------------------------------------
def seed_scenario_readme(chain: dict) -> str:
    p = chain["practice"]
    idx = chain["index_in_practice"]
    title = chain["title"]
    meta = PRACTICE_META[p]
    global_idx = PRACTICES.index(p) * 5 + idx
    lines = [
        f"# {title}",
        "",
        f"**Practice:** {p} — {meta[0]}  ",
        f"**Scenario index:** {idx:02d} of 5 featured (global chain {global_idx} of 35)  ",
        f"**Source:** APEX-Stacked-Architecture-Narrated.html",
        "",
        "## Scenario",
        chain.get("Scenario", "") or "_(see narrated HTML)_",
        "",
        "## Solution",
        chain.get("Solution", "") or "_(see narrated HTML)_",
        "",
        "## Use Case",
        chain.get("Use Case", "") or "_(see narrated HTML)_",
        "",
        "## Service",
        chain.get("Service", "") or "_(see narrated HTML)_",
        "",
        "## Persona",
        chain.get("Persona", "") or "_(see narrated HTML)_",
        "",
        "## KPI",
        chain.get("KPI", "") or "_(see narrated HTML)_",
        "",
        "## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)",
        "",
        "_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._",
        "",
        "## Artifacts to land in this folder",
        "",
        f"- `APEX-{slugify(title)}-build-guide.md` — step-by-step build",
        f"- `APEX-{slugify(title)}-walkthrough.docx` — narrative walkthrough for sellers",
        "- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)",
        "- `artifacts/` — diagrams, screenshots, sample payloads",
        "- `manifests/` — agent / orchestration / policy manifest YAMLs",
        "",
        "## Cross-references",
        "",
        "- Practice overview: [../README.md](../README.md)",
        "- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)",
        "- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)",
        "- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)",
        "",
    ]
    return "\n".join(lines)


# --- Step 3: Per-practice README --------------------------------------------------------
def practice_readme(p: str) -> str:
    meta = PRACTICE_META[p]
    featured = [c for c in chains if c["practice"] == p]
    compact_count = len(library.get(p, []))
    lines = [
        f"# {p} — {meta[0]}",
        "",
        f"**Vertical focus:** {meta[3]}  ",
        f"**Brand color:** `{meta[2]}` ({meta[1]})  ",
        f"**Scenario coverage:** {len(featured)} featured · {compact_count} catalogued",
        "",
        "## Featured scenarios (5)",
        "",
        "Each has its own folder with seed README, artifacts placeholder, and a walkthrough slot.",
        "",
    ]
    for c in featured:
        folder = scenario_folder_name(c["index_in_practice"], c["title"])
        lines.append(f"- **{c['index_in_practice']:02d}** — [{c['title']}]({folder}/)")
    lines += [
        "",
        "## Compact catalog",
        "",
        f"The remaining ~{compact_count - 5} scenarios are catalogued in [_browse-catalog.md](_browse-catalog.md) and each has its own folder numbered `06-NNN` (alphabetical by title). Compact folders hold a lightweight README (title · service · description · KPI) and are candidates for promotion to featured when their full chain gets authored.",
        "",
        "## Adding a new scenario to this Practice",
        "",
        "1. Pick a folder name: `NN-slug` (two-digit index, kebab-case title).",
        "2. Copy the template from any existing featured folder's `README.md`.",
        "3. Fill Scenario / Solution / Use Case / Service / Persona / KPI.",
        "4. Author the Wave Ribbon (W1 prerequisites · W2 pilot · W3 enterprise · fusion partners).",
        "5. Add the row to `_browse-catalog.md`.",
        "6. Update `../_catalog/scenario-library.json` if shipping into the narrated HTML browser.",
        "",
    ]
    return "\n".join(lines)


# --- Step 4: Per-practice compact browse catalog ---------------------------------------
def browse_catalog(p: str) -> str:
    meta = PRACTICE_META[p]
    items = sorted(library.get(p, []), key=lambda r: r["t"].lower())
    lines = [
        f"# {p} · Browse catalog ({len(items)} scenarios)",
        "",
        f"**Practice:** {p} — {meta[0]}  ",
        f"Alphabetical index of all {p} scenarios in the APEX library. Featured scenarios link to their seed folder; other rows are described at catalog-level only.",
        "",
        "| # | Scenario | Service | Description | KPI |",
        "|---|---|---|---|---|",
    ]
    featured_map = {
        c["title"].lower(): scenario_folder_name(c["index_in_practice"], c["title"])
        for c in chains if c["practice"] == p
    }
    for i, r in enumerate(items, 1):
        title = r["t"]
        svc = r["s"]
        blurb = r["b"].replace("|", "\\|")
        kpi = r["k"]
        link_target = None
        for fn, folder in featured_map.items():
            if fn in title.lower() or title.lower() in fn:
                link_target = folder
                break
        title_cell = f"[{title}]({link_target}/)" if link_target else title
        lines.append(f"| {i} | {title_cell} | `{svc}` | {blurb} | {kpi} |")
    lines += [
        "",
        f"_Source: `APEX_SCENARIO_LIBRARY[\"{p}\"]` in [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)._",
        "",
    ]
    return "\n".join(lines)


# --- Step 5: Create practice folders + featured scenarios ------------------------------
created_folders = 0
created_scenarios = 0
for p in PRACTICES:
    prac_dir = ROOT / p
    prac_dir.mkdir(parents=True, exist_ok=True)
    readme = prac_dir / "README.md"
    if not readme.exists():
        readme.write_text(practice_readme(p), encoding="utf-8")
        created_folders += 1
    # Always refresh browse catalog (it's deterministic from library)
    (prac_dir / "_browse-catalog.md").write_text(browse_catalog(p), encoding="utf-8")

for c in chains:
    p = c["practice"]
    folder = scenario_folder_name(c["index_in_practice"], c["title"])
    sdir = ROOT / p / folder
    sdir.mkdir(parents=True, exist_ok=True)
    for sub in ("tests", "artifacts", "manifests"):
        (sdir / sub).mkdir(exist_ok=True)
        gk = sdir / sub / ".gitkeep"
        if not gk.exists():
            gk.write_text("", encoding="utf-8")
    # Only write README if absent — preserves Cold-Chain Excursion's existing build guide
    readme = sdir / "README.md"
    if not readme.exists():
        readme.write_text(seed_scenario_readme(c), encoding="utf-8")
        created_scenarios += 1


# --- Step 5b: Create a folder per compact-catalog row (numbered 06-NNN, alphabetical) --
# Compact folders are lightweight — README.md only, no tests/artifacts/manifests stubs.
# If a compact row's title fuzzy-matches a featured scenario, we SKIP it (the featured
# folder already exists at 01-05 and its README holds the authoritative chain).

def compact_readme(practice: str, row: dict, number: int) -> str:
    meta = PRACTICE_META[practice]
    svc = row.get("s", "")
    title = row.get("t", "")
    blurb = row.get("b", "")
    kpi = row.get("k", "")
    direction = row.get("kk", "")
    arrow = "↑" if direction == "up" else ("↓" if direction == "down" else "·")
    lines = [
        f"# {title}",
        "",
        f"**Practice:** {practice} — {meta[0]}  ",
        f"**Catalog index:** {number:03d} (compact)  ",
        f"**Service code:** `{svc}`  ",
        f"**Headline KPI:** {arrow} {kpi}",
        "",
        "## Description",
        blurb,
        "",
        "## Status",
        "Compact catalog entry. The full Scenario / Solution / Use Case / Service / Persona / KPI chain for this scenario has not yet been authored. To promote this scenario to featured status, author the full chain in this README (use any featured-scenario folder's `README.md` as the template) and add the scenario to the narrated HTML's 5-per-Practice chain-card block.",
        "",
        "## Folder layout",
        "",
        "- `tests/` — pytest fixtures and harness scenarios (add as the scenario moves toward build)",
        "- `artifacts/` — diagrams, screenshots, sample payloads, build outputs",
        "- `manifests/` — agent manifest YAMLs, orchestration manifest, policy manifest overlays",
        "",
        "## Cross-references",
        "",
        f"- Practice overview: [../README.md](../README.md)",
        f"- Compact catalog row: [../_browse-catalog.md](../_browse-catalog.md)",
        "- Featured scenarios for this Practice (01-05): numbered siblings of this folder",
        "- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)",
        "",
    ]
    return "\n".join(lines)


def title_matches_featured(title: str, featured_titles: list[str]) -> bool:
    """Loose match: featured title contains compact OR compact contains featured."""
    t = title.lower().strip()
    for ft in featured_titles:
        f = ft.lower().strip()
        if f == t or f in t or t in f:
            return True
    return False


created_compact = 0
skipped_featured_dupes = 0
compact_by_practice: dict[str, int] = {}
for p in PRACTICES:
    featured_titles = [c["title"] for c in chains if c["practice"] == p]
    # Alphabetical — same order as _browse-catalog.md
    rows = sorted(library.get(p, []), key=lambda r: r["t"].lower())
    number = 6  # featured occupy 01-05; compact starts at 06
    compact_by_practice[p] = 0
    for r in rows:
        if title_matches_featured(r["t"], featured_titles):
            skipped_featured_dupes += 1
            continue
        folder = f"{number:02d}-{slugify(r['t'])}"
        cdir = ROOT / p / folder
        cdir.mkdir(parents=True, exist_ok=True)
        # Full subfolder kit — same shape as featured scenarios
        for sub in ("tests", "artifacts", "manifests"):
            (cdir / sub).mkdir(exist_ok=True)
            gk = cdir / sub / ".gitkeep"
            if not gk.exists():
                gk.write_text("", encoding="utf-8")
        readme = cdir / "README.md"
        if not readme.exists():
            readme.write_text(compact_readme(p, r, number), encoding="utf-8")
            created_compact += 1
        compact_by_practice[p] += 1
        number += 1


# --- Step 6: Top-level README + _catalog JSON ------------------------------------------
catalog_dir = ROOT / "_catalog"
catalog_dir.mkdir(exist_ok=True)
json.dump(library, open(catalog_dir / "scenario-library.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
json.dump(chains, open(catalog_dir / "featured-chains.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)

summary_lines = [
    "# Scenario library summary",
    "",
    "| Practice | Featured | Catalog |",
    "|---|---|---|",
]
total_feat = total_cat = 0
for p, meta in PRACTICE_META.items():
    fc = sum(1 for c in chains if c["practice"] == p)
    cc = len(library.get(p, []))
    total_feat += fc
    total_cat += cc
    summary_lines.append(f"| **{p}** — {meta[0]} | {fc} | {cc} |")
summary_lines.append(f"| **Total** | **{total_feat}** | **{total_cat}** |")
(catalog_dir / "by-practice.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

top_lines = [
    "# APEX Scenario Library",
    "",
    "The canonical on-disk representation of the APEX scenario catalog. One folder per Practice, with featured-scenario sub-folders and a compact browse catalog for the long tail.",
    "",
    "## At a glance",
    "",
    "- **7 Practices** — RC, HLS, ER, AXLE, TMT, TH, ICE",
    f"- **{total_feat} featured scenarios** (5 per Practice) with full Scenario → Solution → Use Case → Service → Persona → KPI chains",
    f"- **{total_cat} compact scenarios** ({min(len(library[p]) for p in library)}–{max(len(library[p]) for p in library)} per Practice) in browse catalogs",
    "",
    "## Practice folders",
    "",
]
for p, meta in PRACTICE_META.items():
    fc = sum(1 for c in chains if c["practice"] == p)
    cc = len(library.get(p, []))
    top_lines.append(f"- **[{p}](./{p}/)** — {meta[0]} · {fc} featured + {cc} catalogued")
top_lines += [
    "",
    "## Layout",
    "",
    "```",
    "docs/scenarios/",
    "  README.md                            <-- this file",
    "  _catalog/",
    "    scenario-library.json              <-- full 723-row catalog as JSON",
    "    featured-chains.json               <-- 35 featured scenarios with full chains",
    "    by-practice.md                     <-- count summary",
    "  <PRACTICE>/                          <-- RC / HLS / ER / AXLE / TMT / TH / ICE",
    "    README.md                          <-- Practice overview + featured list",
    "    _browse-catalog.md                 <-- 100+ compact scenarios, alphabetical",
    "    NN-<slug>/                        <-- one folder per scenario (01-05 featured; 06+ compact)",
    "      README.md                        <-- chain content (full for featured; lightweight for compact)",
    "      tests/                           <-- pytest fixtures (when apex-test-harness targets this Practice)",
    "      artifacts/                       <-- diagrams, screenshots, sample payloads",
    "      manifests/                       <-- agent / orchestration / policy manifest YAMLs",
    "```",
    "",
    "## Featured vs compact",
    "",
    "Both folder shapes are structurally identical (README + `tests/` + `artifacts/` + `manifests/`). The difference is content:",
    "",
    "- **Featured (01-05 per Practice)** — hand-authored full chains: Scenario / Solution / Use Case / Service / Persona / KPI plus a Wave Ribbon.",
    "- **Compact (06-NNN per Practice)** — catalog entries from `APEX_SCENARIO_LIBRARY`. Lightweight README with title, service code, description, headline KPI. Promote to featured by authoring the full chain.",
    "",
    "## Provenance",
    "",
    "- **Compact catalog** (`_catalog/scenario-library.json`) extracted from the `APEX_SCENARIO_LIBRARY` JS constant in [`docs/reference/APEX-Stacked-Architecture-Narrated.html`](../reference/APEX-Stacked-Architecture-Narrated.html).",
    "- **Featured chains** (`_catalog/featured-chains.json`) extracted from the 35 collapsible chain cards in the same narrated HTML.",
    "- Roadmap entries: **BL.C.42a** (35 featured) · **BL.C.42b** (723 compact) · **BL.C.42e–f** (Wave Ribbon).",
    "",
    "## Where the original Cold-Chain Excursion materials live now",
    "",
    "The original hand-authored `Cold-Chain Excursion/` folder (containing `APEX-Cold-Chain-Excursion-Build-Guide.md` and the walkthrough DOCX) has been relocated into [`RC/01-cold-chain-excursion-store-cooler/`](./RC/01-cold-chain-excursion-store-cooler/) for consistency with the Practice-organized tree. No content was lost.",
    "",
    "## Regenerate",
    "",
    "```bash",
    "python scripts/build_scenarios_tree.py",
    "```",
    "",
    "This rebuilds the `_browse-catalog.md` files (deterministic from the library) and the `_catalog/*.json` files. Per-scenario `README.md` files are only written if absent — hand-edits are preserved.",
    "",
]
(ROOT / "README.md").write_text("\n".join(top_lines), encoding="utf-8")

# Clean scratch
scratch = ROOT / "_featured_chains.json"
if scratch.exists():
    scratch.unlink()

print(f"\nSummary:")
print(f"  Practice READMEs created: {created_folders}")
print(f"  Featured scenario READMEs created: {created_scenarios}")
print(f"  Compact scenario READMEs created: {created_compact}")
print(f"  Compact rows skipped (match a featured): {skipped_featured_dupes}")
print(f"  Moved existing Cold-Chain Excursion folder: {moved_existing}")
print(f"  Total featured folders: {len(chains)}")
print(f"  Compact folders per practice:")
for p, n in compact_by_practice.items():
    print(f"    {p}: {n}")
print(f"  Catalog JSONs: {catalog_dir.resolve()}")
