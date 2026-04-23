"""Rebuild _browse-catalog.md, per-Practice README.md, top-level README.md, and
_catalog/by-practice.md by walking the current reorganized folder tree.

Assumes the tree is already in <PRACTICE>/<domain>/<NN-slug>/ form.
Safe to run repeatedly.
"""

from __future__ import annotations

import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path("docs/scenarios")
CATALOG = ROOT / "_catalog"

library = json.load(open(CATALOG / "scenario-library.json", encoding="utf-8"))
chains = json.load(open(CATALOG / "featured-chains.json", encoding="utf-8"))

PRACTICES = ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]
PRACTICE_NAMES = {
    "RC": "Retail & Consumer",
    "HLS": "Health, Life Sciences",
    "ER": "Energy & Resources",
    "AXLE": "Automotive & Manufacturing",
    "TMT": "Technology, Media, Telecom",
    "TH": "Travel & Hospitality",
    "ICE": "Industrial, Construction, Equipment",
}

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
DOMAIN_SHORT = {
    "clinical-care": "Clinical",
    "network-infrastructure": "Network",
    "engineering-rd": "Engineering",
    "supply-chain": "Supply Chain",
    "asset-maintenance": "Asset",
    "quality-compliance": "Quality",
    "risk-fraud-security": "Risk/Fraud",
    "pricing-revenue": "Pricing",
    "customer-experience": "CX",
    "marketing-growth": "Marketing",
    "operations-workforce": "Operations",
    "channel-partner-dealer": "Channel",
    "other": "Other",
}

# Build: (practice, domain) -> list of (new_idx, folder_name, title_from_readme, is_featured)
# and global (practice, title_lower) -> relative_path
tree: dict[str, dict[str, list[dict]]] = {p: defaultdict(list) for p in PRACTICES}
title_to_path: dict[tuple[str, str], str] = {}
featured_titles: dict[str, set[str]] = {p: {c["title"].lower() for c in chains if c["practice"] == p} for p in PRACTICES}


def read_h1(folder: Path) -> str:
    readme = folder / "README.md"
    if not readme.exists():
        return ""
    try:
        first = readme.read_text(encoding="utf-8").split("\n", 1)[0].strip()
    except Exception:
        return ""
    return first[2:].strip() if first.startswith("# ") else ""


for p in PRACTICES:
    prac_dir = ROOT / p
    if not prac_dir.exists():
        continue
    for domain_dir in prac_dir.iterdir():
        if not domain_dir.is_dir() or domain_dir.name.startswith("_"):
            continue
        if domain_dir.name not in DOMAIN_NAMES:
            continue
        for scenario in sorted(domain_dir.iterdir()):
            if not scenario.is_dir():
                continue
            m = re.match(r"^(\d{2,3})-(.+)$", scenario.name)
            if not m:
                continue
            idx = int(m.group(1))
            slug = m.group(2)
            title = read_h1(scenario) or slug.replace("-", " ")
            is_featured = title.lower() in featured_titles[p]
            rel = f"{domain_dir.name}/{scenario.name}"
            tree[p][domain_dir.name].append({
                "idx": idx,
                "name": scenario.name,
                "title": title,
                "rel": rel,
                "featured": is_featured,
            })
            title_to_path[(p, title.lower())] = rel


# -------- Per-Practice README --------
for p in PRACTICES:
    by_domain = tree[p]
    total = sum(len(v) for v in by_domain.values())
    domains_present = [d for d in DOMAIN_ORDER if d in by_domain and by_domain[d]]

    lines = [
        f"# {p} — {PRACTICE_NAMES[p]}",
        "",
        f"**Scenario coverage:** {total} scenarios organized across {len(domains_present)} functional domains.",
        "",
        "## Scenarios by domain",
        "",
    ]
    for d in domains_present:
        items = sorted(by_domain[d], key=lambda x: x["idx"])
        lines.append(f"### {DOMAIN_NAMES[d]} ({len(items)})")
        lines.append("")
        for it in items:
            marker = " ⭐" if it["featured"] else ""
            lines.append(f"- **{it['idx']:02d}**{marker} — [{it['title']}]({it['rel']}/)")
        lines.append("")
    lines += [
        "## Indexes",
        "",
        "- [_browse-catalog.md](_browse-catalog.md) — alphabetical index across all domains",
        "- [../_catalog/by-practice.md](../_catalog/by-practice.md) — counts pivot",
        "- [../_catalog/domain-classification.json](../_catalog/domain-classification.json) — machine-readable classification",
        "",
        "⭐ = featured scenario with full Scenario / Solution / Use Case / Service / Persona / KPI chain authored.",
        "",
    ]
    (ROOT / p / "README.md").write_text("\n".join(lines), encoding="utf-8")


# -------- Per-Practice browse-catalog.md --------
for p in PRACTICES:
    items = sorted(library.get(p, []), key=lambda r: r["t"].lower())
    lines = [
        f"# {p} · Browse catalog ({len(items)} scenarios)",
        "",
        f"**Practice:** {p} — {PRACTICE_NAMES[p]}  ",
        f"Alphabetical index. Each row links to the scenario's folder inside its functional domain.",
        "",
        "| # | Scenario | Domain | Service | Description | KPI |",
        "|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(items, 1):
        title = r["t"]
        svc = r["s"]
        blurb = r["b"].replace("|", "\\|")
        kpi = r["k"]
        rel = title_to_path.get((p, title.lower()))
        if rel is None:
            # Fuzzy fallback
            for (kp, kt), path in title_to_path.items():
                if kp == p and (kt in title.lower() or title.lower() in kt):
                    rel = path
                    break
        if rel:
            title_cell = f"[{title}]({rel}/)"
            dom_slug = rel.split("/")[0]
            dom_cell = DOMAIN_NAMES.get(dom_slug, dom_slug)
        else:
            title_cell = title
            dom_cell = "—"
        lines.append(f"| {i} | {title_cell} | {dom_cell} | `{svc}` | {blurb} | {kpi} |")
    lines.append("")
    lines.append(f"_Source: `APEX_SCENARIO_LIBRARY[\"{p}\"]` in [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)._")
    (ROOT / p / "_browse-catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# -------- by-practice pivot --------
pivot: dict[tuple[str, str], int] = defaultdict(int)
for p in PRACTICES:
    for d, items in tree[p].items():
        pivot[(p, d)] = len(items)

header = "| Practice | " + " | ".join(DOMAIN_SHORT[d] for d in DOMAIN_ORDER) + " | **TOTAL** |"
sep = "|" + "---|" * (len(DOMAIN_ORDER) + 2)
rows = [header, sep]
totals = {d: 0 for d in DOMAIN_ORDER}
grand = 0
for p in PRACTICES:
    row = [f"**{p}**"]
    total = 0
    for d in DOMAIN_ORDER:
        c = pivot.get((p, d), 0)
        totals[d] += c
        total += c
        row.append(str(c) if c else "")
    row.append(f"**{total}**")
    grand += total
    rows.append("| " + " | ".join(row) + " |")
rows.append("| **Total** | " + " | ".join(f"**{totals[d]}**" for d in DOMAIN_ORDER) + f" | **{grand}** |")
(CATALOG / "by-practice.md").write_text(
    "# Scenario library summary\n\n## Per practice × domain pivot\n\n" + "\n".join(rows) + "\n",
    encoding="utf-8",
)

# -------- Top-level README --------
top = [
    "# APEX Scenario Library",
    "",
    f"On-disk catalog of APEX scenarios, organized by **Practice** then by **functional domain**. {grand} scenario folders across 7 Practices and up to 13 domains.",
    "",
    "## Practice folders",
    "",
]
for p in PRACTICES:
    n_domains = len([d for d in DOMAIN_ORDER if pivot.get((p, d), 0) > 0])
    ct = sum(pivot.get((p, d), 0) for d in DOMAIN_ORDER)
    top.append(f"- **[{p}](./{p}/)** — {PRACTICE_NAMES[p]} · {ct} scenarios across {n_domains} domains")
top += [
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
    "      NN-<scenario-slug>/              <-- scenarios (featured first, then alpha)",
    "        README.md                      <-- scenario chain or catalog-level blurb",
    "        tests/ artifacts/ manifests/   <-- build artefact stubs",
    "```",
    "",
    "## Functional domains (13)",
    "",
]
for d in DOMAIN_ORDER:
    count = totals[d]
    if count:
        top.append(f"- **{DOMAIN_NAMES[d]}** (`{d}`) — {count} scenarios")
top += [
    "",
    "## Featured scenarios",
    "",
    "35 scenarios (5 per Practice) have full Scenario / Solution / Use Case / Service / Persona / KPI chains authored — identified by the ⭐ marker in each Practice's README. The other ~700 are compact catalog entries; promotion happens by authoring the full chain in that folder's README.",
    "",
    "## Regenerate",
    "",
    "```bash",
    "# 1. Extract + flat build (preserves any hand-edited READMEs)",
    "python scripts/build_scenarios_tree.py",
    "",
    "# 2. Re-classify",
    "python scripts/classify_scenarios.py",
    "",
    "# 3. Move folders into domain sub-trees",
    "python scripts/reorg_scenarios_by_domain.py",
    "",
    "# 4. Rebuild indexes (run any time to refresh from the filesystem)",
    "python scripts/rebuild_scenario_indexes.py",
    "```",
    "",
]
(ROOT / "README.md").write_text("\n".join(top), encoding="utf-8")

print(f"Rebuilt indexes across {len(PRACTICES)} practices. Grand total: {grand} scenarios.")
for p in PRACTICES:
    ct = sum(pivot.get((p, d), 0) for d in DOMAIN_ORDER)
    print(f"  {p}: {ct}")
