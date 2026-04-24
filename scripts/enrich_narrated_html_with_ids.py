"""Inject scenario IDs and folder paths into docs/reference/APEX-Stacked-Architecture-Narrated.html.

1. Walks docs/scenarios/ to build title → {id, path} mapping.
2. Enriches `APEX_SCENARIO_LIBRARY` JSON entries in the HTML with `id` + `p` fields.
3. Updates the scenario-row render template to show the ID as a clickable link to the folder.
4. Adds ID chips to the 35 featured chain `<summary>` blocks.

Idempotent: re-running updates stale IDs but preserves already-enriched structure.
"""

from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path("docs/scenarios")
HTML_PATH = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")

PRACTICES = ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]
DOMAIN_CODES = {
    "clinical-care":          "CLIN",
    "network-infrastructure": "NET",
    "engineering-rd":         "ENG",
    "supply-chain":           "SUPCHN",
    "asset-maintenance":      "ASSET",
    "quality-compliance":     "QUAL",
    "risk-fraud-security":    "RISK",
    "pricing-revenue":        "PRICE",
    "customer-experience":    "CX",
    "marketing-growth":       "MKTG",
    "operations-workforce":   "OPS",
    "channel-partner-dealer": "CHAN",
    "other":                  "OTHER",
}

# -----------------------------------------------------------------------------
# Step 1 — Walk scenarios/ to build title lookup
# -----------------------------------------------------------------------------

def read_h1(folder: Path) -> str:
    readme = folder / "README.md"
    if not readme.exists():
        return ""
    try:
        first = readme.read_text(encoding="utf-8").split("\n", 1)[0].strip()
    except Exception:
        return ""
    return first[2:].strip() if first.startswith("# ") else ""


def parse_folder(name: str) -> tuple[int, str] | None:
    m = re.match(r"^[A-Z]+-[A-Z]+-(\d{2,3})-(.+)$", name)
    if m:
        return int(m.group(1)), m.group(2)
    m = re.match(r"^(\d{2,3})-(.+)$", name)
    if m:
        return int(m.group(1)), m.group(2)
    return None


# (practice, title_lower) -> {id, rel_path, domain_name}
title_index: dict[tuple[str, str], dict[str, str]] = {}

for p in PRACTICES:
    prac_dir = ROOT / p
    if not prac_dir.exists():
        continue
    for domain_dir in prac_dir.iterdir():
        if not domain_dir.is_dir() or domain_dir.name.startswith("_"):
            continue
        if domain_dir.name not in DOMAIN_CODES:
            continue
        dom_code = DOMAIN_CODES[domain_dir.name]
        for scen in sorted(domain_dir.iterdir()):
            if not scen.is_dir():
                continue
            parsed = parse_folder(scen.name)
            if not parsed:
                continue
            idx, slug = parsed
            title = read_h1(scen) or slug.replace("-", " ")
            sid = f"{p}-{dom_code}-{idx:02d}"
            # Path relative to docs/reference/APEX-Stacked-Architecture-Narrated.html
            rel = f"../scenarios/{p}/{domain_dir.name}/{scen.name}/"
            title_index[(p, title.lower().strip())] = {
                "id": sid,
                "p": rel,
                "domain": domain_dir.name,
            }

print(f"Built title index: {len(title_index)} scenarios")


# -----------------------------------------------------------------------------
# Step 2 — Load the HTML + parse + enrich APEX_SCENARIO_LIBRARY
# -----------------------------------------------------------------------------

html = HTML_PATH.read_text(encoding="utf-8")

m = re.search(r"(const APEX_SCENARIO_LIBRARY\s*=\s*)(\{.*?\})(;)", html, re.DOTALL)
if not m:
    print("ERROR: couldn't find APEX_SCENARIO_LIBRARY declaration")
    sys.exit(1)

library = json.loads(m.group(2))
enriched_rows = 0
orphan_rows = 0

for p, rows in library.items():
    for row in rows:
        key = (p, row["t"].lower().strip())
        info = title_index.get(key)
        if info is None:
            # Fuzzy fallback — try contains
            for (kp, kt), v in title_index.items():
                if kp == p and (kt in row["t"].lower() or row["t"].lower() in kt):
                    info = v
                    break
        if info:
            row["id"] = info["id"]
            row["p"] = info["p"]
            row["domain"] = info["domain"]
            enriched_rows += 1
        else:
            orphan_rows += 1

print(f"Enriched rows: {enriched_rows} · Orphaned (no folder match): {orphan_rows}")

# Re-serialize. Use compact JSON (matches current file style).
new_json = json.dumps(library, ensure_ascii=False, separators=(",", ":"))
# Preserve ordering: t, s, b, k, kk, id, p  (we're adding id+p at end which json.dumps does)
html = html[:m.start(2)] + new_json + html[m.end(2):]


# -----------------------------------------------------------------------------
# Step 3 — Update scenario-row render template to show ID as a clickable link
# -----------------------------------------------------------------------------
# Find the existing template block and swap in an ID-bearing version.

OLD_TEMPLATE = (
    "'<div class=\"scenario-row\" role=\"listitem\" data-search=\"' + escapeHtml(searchData) + '\">' +\n"
    "        '<div class=\"sr-main\">' +\n"
    "          '<div class=\"sr-title\">' + titleSafe + '</div>' +\n"
    "          '<div class=\"sr-brief\">' + briefSafe + '</div>' +\n"
    "        '</div>' +\n"
    "        '<div class=\"sr-service\">' + serviceSafe + '</div>' +\n"
    "        '<div class=\"sr-kpi-wrap\"><span class=\"sr-kpi ' + kk + '\">' + kpiSafe + '</span></div>' +\n"
    "      '</div>';"
)

NEW_TEMPLATE = (
    "'<div class=\"scenario-row\" role=\"listitem\" data-search=\"' + escapeHtml(searchData) + '\" data-domain=\"' + escapeHtml(item.domain || '') + '\">' +\n"
    "        '<div class=\"sr-main\">' +\n"
    "          (item.id ? '<a class=\"sr-id\" href=\"' + escapeHtml(item.p || '#') + '\" target=\"_blank\" rel=\"noopener\" title=\"Open folder\">' + escapeHtml(item.id) + '</a>' : '') +\n"
    "          '<div class=\"sr-title\">' + titleSafe + '</div>' +\n"
    "          '<div class=\"sr-brief\">' + briefSafe + '</div>' +\n"
    "        '</div>' +\n"
    "        '<div class=\"sr-service\">' + serviceSafe + '</div>' +\n"
    "        '<div class=\"sr-kpi-wrap\"><span class=\"sr-kpi ' + kk + '\">' + kpiSafe + '</span></div>' +\n"
    "      '</div>';"
)

if OLD_TEMPLATE in html:
    html = html.replace(OLD_TEMPLATE, NEW_TEMPLATE)
    print("Swapped scenario-row template: ID + folder-link added")
elif NEW_TEMPLATE in html:
    print("scenario-row template already enriched — no-op")
else:
    # Try a softer match: find the scenario-row literal and splice in after the searchData opening div
    print("WARN: scenario-row template didn't match exactly; manual verification recommended")

# Make sure the searchData field includes the ID so filter-by-ID works
OLD_SEARCH = "const searchData = (item.t + ' ' + item.b + ' ' + item.s).toLowerCase();"
NEW_SEARCH = "const searchData = (item.t + ' ' + item.b + ' ' + item.s + ' ' + (item.id || '')).toLowerCase();"
if OLD_SEARCH in html:
    html = html.replace(OLD_SEARCH, NEW_SEARCH)
    print("Updated searchData to include ID")


# -----------------------------------------------------------------------------
# Step 4 — Add .sr-id CSS (green pill matching brand color)
# -----------------------------------------------------------------------------

CSS_BLOCK = (
    "/* injected by enrich_narrated_html_with_ids.py */\n"
    ".sr-id {\n"
    "  display: inline-block;\n"
    "  font-family: 'JetBrains Mono', 'Consolas', monospace;\n"
    "  font-size: 10.5px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.06em;\n"
    "  color: var(--teal, #44B8A8);\n"
    "  background: rgba(68, 184, 168, 0.08);\n"
    "  border: 1px solid rgba(68, 184, 168, 0.25);\n"
    "  padding: 1px 7px;\n"
    "  border-radius: 3px;\n"
    "  margin-right: 6px;\n"
    "  margin-bottom: 4px;\n"
    "  text-decoration: none;\n"
    "  vertical-align: baseline;\n"
    "  transition: background 0.15s, color 0.15s;\n"
    "}\n"
    ".sr-id:hover {\n"
    "  background: var(--teal, #44B8A8);\n"
    "  color: #0b0b0b;\n"
    "  text-decoration: none;\n"
    "}\n"
    ".sr-main .sr-id + .sr-title { display: inline; }\n"
)

if "/* injected by enrich_narrated_html_with_ids.py */" not in html:
    # Insert right before closing </style> of the first style block
    # Find the first '</style>'
    close_style = html.find("</style>")
    if close_style != -1:
        html = html[:close_style] + CSS_BLOCK + html[close_style:]
        print("Injected .sr-id CSS block")


# -----------------------------------------------------------------------------
# Step 5 — Add ID chip to each featured chain <summary>
# -----------------------------------------------------------------------------
# Featured chain summaries follow the pattern:
#   <summary ...>...title...Service <code>...</code>...</summary>
# We locate them by looking for summaries that contain 'r-scenario' as a sibling
# (it's inside the details body). Instead, we walk the 35 pattern by matching
# <details> with chain-body content.

chain_pattern = re.compile(
    r"(<details[^>]*>\s*<summary[^>]*>)(.*?)(</summary>)(.*?)(</details>)",
    re.DOTALL,
)

# Index: order of featured chains maps to (practice, index) via (i//5, i%5+1)
def featured_id(global_idx: int, title: str) -> str | None:
    """Given the 0-based global chain index + title, locate the folder-derived ID."""
    practice = PRACTICES[global_idx // 5]
    info = title_index.get((practice, title.lower().strip()))
    if info is None:
        for (kp, kt), v in title_index.items():
            if kp == practice and (kt in title.lower() or title.lower() in kt):
                return v["id"]
        return None
    return info["id"]


def strip_tags(s: str) -> str:
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


matches = list(chain_pattern.finditer(html))
featured_matches = [m for m in matches if "r-scenario" in m.group(4)]
print(f"Found {len(featured_matches)} featured chains")

# Rewrite from the tail so byte-offsets remain valid
enriched_chains = 0
for gi, cm in reversed(list(enumerate(featured_matches))):
    summary_inner = cm.group(2)
    # Skip if already has sr-id class
    if 'class="chain-id"' in summary_inner or "chain-id " in summary_inner:
        continue
    # Extract a decent title — same logic as the extractor
    full_text = strip_tags(summary_inner)
    if " Service " in full_text:
        title = full_text.split(" Service ")[0].strip()
    else:
        title = full_text[:80]
    m2 = re.match(r"^(\d{2})\s+(.*)$", title)
    if m2:
        title = m2.group(2).strip()

    sid = featured_id(gi, title)
    if sid is None:
        continue

    # Compute the folder rel path for the ID
    practice = PRACTICES[gi // 5]
    info = title_index.get((practice, title.lower().strip()))
    if info is None:
        for (kp, kt), v in title_index.items():
            if kp == practice and (kt in title.lower() or title.lower() in kt):
                info = v
                break
    if info is None:
        continue
    rel = info["p"]

    # Inject an ID chip as the very first element inside the summary
    chip = (
        f'<a class="chain-id" href="{rel}" target="_blank" rel="noopener" '
        f'title="Open scenario folder">{sid}</a> '
    )
    new_summary_inner = chip + summary_inner

    # Splice back into html
    start, end = cm.start(2), cm.end(2)
    html = html[:start] + new_summary_inner + html[end:]
    enriched_chains += 1

print(f"Enriched {enriched_chains} featured chain summaries with IDs")

# Add .chain-id CSS if missing
CHAIN_CSS = (
    ".chain-id {\n"
    "  display: inline-block;\n"
    "  font-family: 'JetBrains Mono', 'Consolas', monospace;\n"
    "  font-size: 10px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.08em;\n"
    "  color: #0b0b0b;\n"
    "  background: var(--teal, #44B8A8);\n"
    "  padding: 2px 8px;\n"
    "  border-radius: 3px;\n"
    "  margin-right: 10px;\n"
    "  text-decoration: none;\n"
    "  vertical-align: middle;\n"
    "  transition: filter 0.15s;\n"
    "}\n"
    ".chain-id:hover { filter: brightness(1.15); text-decoration: none; }\n"
)
if ".chain-id " not in html:
    close_style = html.find("</style>")
    if close_style != -1:
        html = html[:close_style] + CHAIN_CSS + html[close_style:]
        print("Injected .chain-id CSS block")

HTML_PATH.write_text(html, encoding="utf-8")
print(f"\nWrote enriched HTML to {HTML_PATH}")
