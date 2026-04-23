"""Reorganize existing scenario folders into <PRACTICE>/<domain>/<NN-slug>/ trees.

Reads the classification from docs/scenarios/_catalog/domain-classification.json
(produced by scripts/classify_scenarios.py), then:

1. Discovers each existing scenario folder at <PRACTICE>/NN-slug/
2. Moves it to <PRACTICE>/<domain-slug>/NN-slug/, renumbering within the domain
   (featured scenarios first at 01-05, then compact alphabetical)
3. Rebuilds _browse-catalog.md (links point to new nested paths)
4. Rebuilds each Practice's README.md (now with per-domain sections)
5. Rebuilds the top-level README.md

Idempotent: if the tree is already in domain layout, re-running produces no moves.
"""

from __future__ import annotations

import io
import json
import re
import shutil
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path("docs/scenarios")
CATALOG = ROOT / "_catalog"

# Load classification
classification = json.load(open(CATALOG / "domain-classification.json", encoding="utf-8"))
library = json.load(open(CATALOG / "scenario-library.json", encoding="utf-8"))
chains = json.load(open(CATALOG / "featured-chains.json", encoding="utf-8"))

PRACTICES = ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]
PRACTICE_NAMES = {
    "RC":   "Retail & Consumer",
    "HLS":  "Health, Life Sciences",
    "ER":   "Energy & Resources",
    "AXLE": "Automotive & Manufacturing",
    "TMT":  "Technology, Media, Telecom",
    "TH":   "Travel & Hospitality",
    "ICE":  "Industrial, Construction, Equipment",
}

# Canonical domain order (matches classify_scenarios.py)
DOMAIN_ORDER = [
    "clinical-care", "network-infrastructure", "engineering-rd",
    "supply-chain", "asset-maintenance", "quality-compliance",
    "risk-fraud-security", "pricing-revenue", "customer-experience",
    "marketing-growth", "operations-workforce", "channel-partner-dealer",
    "other",
]
DOMAIN_NAMES = {
    "clinical-care":          "Clinical & Care",
    "network-infrastructure": "Network & Infrastructure",
    "engineering-rd":         "Engineering & R&D",
    "supply-chain":           "Supply Chain & Inventory",
    "asset-maintenance":      "Asset, Maintenance & Reliability",
    "quality-compliance":     "Quality, Compliance & Regulatory",
    "risk-fraud-security":    "Risk, Fraud & Security",
    "pricing-revenue":        "Pricing, Revenue & Margin",
    "customer-experience":    "Customer Experience & Loyalty",
    "marketing-growth":       "Marketing & Growth",
    "operations-workforce":   "Operations & Workforce",
    "channel-partner-dealer": "Channel, Partner & Dealer",
    "other":                  "Other / Cross-cutting",
}


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[\u2014\u2013\u2212]", "-", s)
    s = re.sub(r"[^a-z0-9\- ]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)


def title_to_folder_slug(title: str) -> str:
    """Same slugification as the original builder."""
    return slugify(title)


# ---- Build title -> existing-folder map per practice -----------------------
# Existing folders are at <PRACTICE>/NN-slug/. Slugs can collide across scenarios
# with similar titles (e.g. "Returns fraud detection" vs "Returns-fraud detection").
# Map by (slug, number) so each physical folder is uniquely keyed, and we match
# classified titles by scanning README.md for the exact title match.

existing_folders: dict[str, dict[str, Path]] = {p: {} for p in PRACTICES}  # slug -> one folder (prefers lower number)
all_folders: dict[str, list[Path]] = {p: [] for p in PRACTICES}            # every NN-slug folder
folder_title_index: dict[tuple[str, str], Path] = {}                        # (practice, title_in_readme) -> folder

def read_title_from_readme(folder: Path) -> str | None:
    """Return the exact title from the scenario's README H1, for collision-safe matching."""
    readme = folder / "README.md"
    if not readme.exists():
        return None
    try:
        first_line = readme.read_text(encoding="utf-8").split("\n", 1)[0].strip()
    except Exception:
        return None
    if first_line.startswith("# "):
        return first_line[2:].strip()
    return None


for p in PRACTICES:
    prac_dir = ROOT / p
    if not prac_dir.exists():
        continue
    # Gather NN-slug dirs (skip domain dirs and meta dirs)
    slug_to_folders: dict[str, list[tuple[int, Path]]] = {}
    for sub in prac_dir.iterdir():
        if not sub.is_dir():
            continue
        name = sub.name
        if name.startswith("_"):
            continue
        if name in DOMAIN_NAMES:
            continue
        m = re.match(r"^(\d{2,3})-(.+)$", name)
        if not m:
            continue
        idx = int(m.group(1))
        slug = m.group(2)
        slug_to_folders.setdefault(slug, []).append((idx, sub))
        all_folders[p].append(sub)
        # Title-exact index via README
        readme_title = read_title_from_readme(sub)
        if readme_title:
            folder_title_index[(p, readme_title.lower().strip())] = sub

    # Keep only one slug->folder for legacy lookup (prefer lowest index)
    for slug, entries in slug_to_folders.items():
        entries.sort()
        existing_folders[p][slug] = entries[0][1]


# Build classification title-index: (practice, title_lower) -> domain_slug
classification_by_title: dict[tuple[str, str], str] = {}
classification_kind: dict[tuple[str, str], str] = {}
for item in classification:
    key = (item["practice"], item["title"].lower().strip())
    classification_by_title[key] = item["domain_slug"]
    classification_kind[key] = item["kind"]


def find_folder_for_title(practice: str, title: str) -> Path | None:
    """Find the folder for a classified title — collision-safe.

    Uses README-H1 exact match first, falls back to slug match.
    Returns None if no unambiguous match.
    """
    key = (practice, title.lower().strip())
    if key in folder_title_index:
        return folder_title_index[key]
    target_slug = title_to_folder_slug(title)
    if target_slug in existing_folders[practice]:
        return existing_folders[practice][target_slug]
    return None


# ---- Plan moves: group scenarios by (practice, domain), renumber within ----
# For each (practice, domain): featured scenarios first (01..N_feat), then
# compact alphabetical (N_feat+1 onward).

plan: list[dict] = []  # {src, dst, practice, domain, new_idx, title}
moves_by_pd: dict[tuple[str, str], list[dict]] = defaultdict(list)

for item in classification:
    p = item["practice"]
    title = item["title"]
    domain = item["domain_slug"]
    src = find_folder_for_title(p, title)
    if src is None:
        continue
    moves_by_pd[(p, domain)].append({
        "title": title,
        "src": src,
        "kind": item["kind"],
    })

# Sort within each (practice, domain): featured first, then alpha
for (p, domain), items in moves_by_pd.items():
    items.sort(key=lambda x: (0 if x["kind"] == "featured" else 1, x["title"].lower()))
    for i, it in enumerate(items, 1):
        it["new_idx"] = i
        slug = src_slug = re.match(r"^\d{2,3}-(.+)$", it["src"].name).group(1)
        new_name = f"{i:02d}-{slug}"
        dst = ROOT / p / domain / new_name
        plan.append({
            "src": it["src"],
            "dst": dst,
            "practice": p,
            "domain": domain,
            "new_idx": i,
            "title": it["title"],
            "kind": it["kind"],
        })

# Execute moves
moved = 0
already_in_place = 0
missing_source = 0
skipped_dst_exists = 0
for entry in plan:
    src = entry["src"]
    dst = entry["dst"]
    if not src.exists():
        # Another plan entry already moved this folder (slug collision). Skip quietly.
        missing_source += 1
        continue
    if src.resolve() == dst.resolve():
        already_in_place += 1
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        skipped_dst_exists += 1
        continue
    shutil.move(str(src), str(dst))
    moved += 1

# Remove empty practice-level directories (any leftover NN-slug folders mean
# something failed to classify — leave them alone for the human to inspect)
leftover: list[Path] = []
for p in PRACTICES:
    prac_dir = ROOT / p
    for sub in prac_dir.iterdir():
        if sub.is_dir() and re.match(r"^\d{2}-", sub.name):
            leftover.append(sub)

# ---- Rebuild _browse-catalog.md with new paths -----------------------------
# Build: (practice, title_lower) -> new relative path
path_index: dict[tuple[str, str], str] = {}
for entry in plan:
    rel = f"{entry['domain']}/{entry['new_idx']:02d}-{re.match(r'^\d{2,3}-(.+)$',entry['src'].name).group(1)}"
    path_index[(entry["practice"], entry["title"].lower().strip())] = rel


def rebuild_browse_catalog(p: str) -> None:
    items = sorted(library.get(p, []), key=lambda r: r["t"].lower())
    lines = [
        f"# {p} · Browse catalog ({len(items)} scenarios)",
        "",
        f"**Practice:** {p} — {PRACTICE_NAMES[p]}  ",
        f"Alphabetical index of all {p} scenarios. Each row links to the scenario's folder (now organized by functional domain).",
        "",
        "| # | Scenario | Domain | Service | Description | KPI |",
        "|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(items, 1):
        title = r["t"]
        svc = r["s"]
        blurb = r["b"].replace("|", "\\|")
        kpi = r["k"]
        # Find domain and path
        key = (p, title.lower().strip())
        rel = path_index.get(key)
        # If compact row was de-duped against a featured title, use a loose match
        if rel is None:
            for (kp, kt), path in path_index.items():
                if kp == p and (kt in title.lower() or title.lower() in kt):
                    rel = path
                    break
        if rel:
            title_cell = f"[{title}]({rel}/)"
            # Derive domain from path
            dom_slug = rel.split("/")[0]
            dom_cell = DOMAIN_NAMES.get(dom_slug, dom_slug)
        else:
            title_cell = title
            dom_cell = "—"
        lines.append(f"| {i} | {title_cell} | {dom_cell} | `{svc}` | {blurb} | {kpi} |")
    lines += [
        "",
        f"_Source: `APEX_SCENARIO_LIBRARY[\"{p}\"]` in [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)._",
        "",
    ]
    (ROOT / p / "_browse-catalog.md").write_text("\n".join(lines), encoding="utf-8")


def rebuild_practice_readme(p: str) -> None:
    # Group plan by domain
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for entry in plan:
        if entry["practice"] == p:
            by_domain[entry["domain"]].append(entry)
    # Order domains: canonical order, only those with scenarios
    domains_present = [d for d in DOMAIN_ORDER if d in by_domain]
    total = sum(len(v) for v in by_domain.values())

    lines = [
        f"# {p} — {PRACTICE_NAMES[p]}",
        "",
        f"**Scenario coverage:** {total} scenarios organized by functional domain.",
        "",
        "## Scenarios by domain",
        "",
    ]
    for d in domains_present:
        items = sorted(by_domain[d], key=lambda x: x["new_idx"])
        lines.append(f"### {DOMAIN_NAMES[d]} ({len(items)})")
        lines.append("")
        for it in items:
            marker = " ⭐" if it["kind"] == "featured" else ""
            rel = f"{d}/{it['new_idx']:02d}-{re.match(r'^\d{2,3}-(.+)$',it['src'].name).group(1)}"
            lines.append(f"- **{it['new_idx']:02d}**{marker} — [{it['title']}]({rel}/)")
        lines.append("")
    lines += [
        "## Indexes",
        "",
        "- [_browse-catalog.md](_browse-catalog.md) — alphabetical index across all domains",
        "- [../_catalog/by-practice.md](../_catalog/by-practice.md) — counts",
        "- [../_catalog/domain-classification.json](../_catalog/domain-classification.json) — machine-readable classification",
        "",
        "⭐ = featured scenario with full Scenario / Solution / Use Case / Service / Persona / KPI chain authored.",
        "",
    ]
    (ROOT / p / "README.md").write_text("\n".join(lines), encoding="utf-8")


for p in PRACTICES:
    rebuild_browse_catalog(p)
    rebuild_practice_readme(p)

# ---- Rebuild top-level README ---------------------------------------------
total_scenarios = sum(len(library[p]) for p in library)
total_folders = len(plan)

top_lines = [
    "# APEX Scenario Library",
    "",
    f"On-disk catalog of APEX scenarios, organized by **Practice** then by **functional domain**. {total_folders} scenario folders across 7 Practices and up to 13 domains.",
    "",
    "## Practice folders",
    "",
]
for p in PRACTICES:
    by_domain: dict[str, int] = defaultdict(int)
    for e in plan:
        if e["practice"] == p:
            by_domain[e["domain"]] += 1
    ct = sum(by_domain.values())
    top_lines.append(f"- **[{p}](./{p}/)** — {PRACTICE_NAMES[p]} · {ct} scenarios across {len(by_domain)} domains")

top_lines += [
    "",
    "## Layout",
    "",
    "```",
    "docs/scenarios/",
    "  README.md                            <-- this file",
    "  _catalog/",
    "    scenario-library.json              <-- 723-row compact library",
    "    featured-chains.json               <-- 35 featured chains with full content",
    "    domain-classification.json         <-- title → functional-domain mapping",
    "    by-practice.md                     <-- practice × domain pivot",
    "  <PRACTICE>/                          <-- RC / HLS / ER / AXLE / TMT / TH / ICE",
    "    README.md                          <-- per-domain grouped index",
    "    _browse-catalog.md                 <-- alphabetical cross-domain list",
    "    <domain-slug>/                     <-- functional domain (clinical-care, supply-chain, ...)",
    "      NN-<scenario-slug>/              <-- one folder per scenario (01-NN, featured first)",
    "        README.md                      <-- scenario chain + artifact list",
    "        tests/ artifacts/ manifests/   <-- build artefact stubs",
    "```",
    "",
    "## Functional domains (13)",
    "",
]
for d in DOMAIN_ORDER:
    count = sum(1 for e in plan if e["domain"] == d)
    if count:
        top_lines.append(f"- **{DOMAIN_NAMES[d]}** (`{d}`) — {count} scenarios")

top_lines += [
    "",
    "## Featured scenarios",
    "",
    f"{sum(1 for e in plan if e['kind'] == 'featured')} scenarios (5 per Practice) have full Scenario / Solution / Use Case / Service / Persona / KPI chains authored — identified by the ⭐ marker in each Practice's README. The other ~700 are compact catalog entries; promotion happens by authoring the full chain in that folder's README.",
    "",
    "## Regenerate",
    "",
    "```bash",
    "# 1. Re-classify (writes _catalog/domain-classification.json)",
    "python scripts/classify_scenarios.py",
    "",
    "# 2. Reorganize folders and rebuild indexes",
    "python scripts/reorg_scenarios_by_domain.py",
    "```",
    "",
]
(ROOT / "README.md").write_text("\n".join(top_lines), encoding="utf-8")

# ---- Update _catalog/by-practice.md ---------------------------------------
summary_lines = ["# Scenario library summary", "", "## Per practice × domain pivot", "", ""]
summary_lines.append("| Practice | " + " | ".join(DOMAIN_NAMES[d].split(" / ")[0].split(" & ")[0].split(", ")[0] for d in DOMAIN_ORDER) + " | **TOTAL** |")
summary_lines.append("|" + "---|" * (len(DOMAIN_ORDER) + 2))
totals = {d: 0 for d in DOMAIN_ORDER}
for p in PRACTICES:
    row = [f"**{p}**"]
    total = 0
    for d in DOMAIN_ORDER:
        count = sum(1 for e in plan if e["practice"] == p and e["domain"] == d)
        totals[d] += count
        total += count
        row.append(str(count) if count else "")
    row.append(f"**{total}**")
    summary_lines.append("| " + " | ".join(row) + " |")
summary_lines.append("| **Total** | " + " | ".join(f"**{totals[d]}**" for d in DOMAIN_ORDER) + f" | **{sum(totals.values())}** |")
(CATALOG / "by-practice.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


# ---- Summary ---------------------------------------------------------------
print(f"Moved: {moved}")
print(f"Already in place: {already_in_place}")
print(f"Missing source (collision): {missing_source}")
print(f"Dst already existed: {skipped_dst_exists}")
print(f"Leftover (unclassified / unmoved) folders: {len(leftover)}")
for lf in leftover[:20]:
    print(f"  · {lf}")
