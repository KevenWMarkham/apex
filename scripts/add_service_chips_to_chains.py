"""Rewrite each featured chain's Service row as a pipe-separated chip list.

For every <details> chain card:
1. Parse the existing r-service cbg-text body
2. Extract service codes currently cited (e.g. RC-E2E-03, RC-E2E-09)
3. Extract the descriptive prose that follows
4. Determine the chain's Practice from its position (5 per Practice, RC first)
5. Render a chip row with ALL of that Practice's services:
     - Services this scenario uses -> class "svc-chip active" (teal)
     - Services not used by this scenario -> class "svc-chip" (grey)
6. Append the original descriptive prose below the chip row

Also injects the .svc-chip* CSS.

Idempotent: skips chains that already have a .svc-chip-list.
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
html = HTML.read_text(encoding="utf-8")

MARKER = "/* svc-chip-list-v1 */"
if MARKER in html:
    print("Service chips already added — skipping CSS injection.")

# -------- 1. Canonical per-Practice service catalog --------
# (code, name) pairs. Names come from the currently-authored chain cards
# (scripts/add_service_chips_to_chains.py extractor pass); missing ones
# are filled in with sensible short names derived from the scenarios that
# use that service code.
SERVICE_CATALOG: dict[str, list[tuple[str, str]]] = {
    "RC": [
        ("RC-E2E-03", "Assortment & Pricing"),
        ("RC-E2E-04", "Customer Lifecycle & Loyalty"),
        ("RC-E2E-05", "Store Operations"),
        ("RC-E2E-06", "Fulfillment & Delivery"),
        ("RC-E2E-07", "Returns & Refund Integrity"),
        ("RC-E2E-08", "Supplier & Vendor"),
        ("RC-E2E-09", "Product Tracking"),
    ],
    "HLS": [
        ("HLS-E2E-02", "Clinical Decision Support"),
        ("HLS-E2E-04", "Care Management & UM"),
        ("HLS-E2E-06", "Population Health"),
        ("HLS-LS-03",  "Clinical Trial Operations"),
    ],
    "ER": [
        ("ER-PU-04",  "Distribution Reliability"),
        ("ER-OG-02",  "Upstream Operations"),
        ("ER-OG-03",  "Upstream Reliability"),
        ("ER-OG-05",  "Refining Optimization"),
        ("ER-OG-07",  "Midstream Integrity"),
        ("ER-MN-02",  "Environmental & Compliance"),
    ],
    "AXLE": [
        ("AXLE-Connected-Factory-01", "Connected Factory"),
        ("AXLE-Ops-03",               "Production Operations"),
        ("AXLE-QMS-02",               "Quality Management"),
        ("AXLE-Supply-04",            "Supply Chain & Sourcing"),
        ("AXLE-Supply-07",            "Supplier Risk"),
    ],
    "TMT": [
        ("TMT-TEL-CC-03",   "Contact Center Intelligence"),
        ("TMT-TEL-NET-02",  "Network Operations"),
        ("TMT-MED-01",      "Subscriber Lifecycle"),
        ("TMT-MED-03",      "Ad Operations Integrity"),
        ("TMT-TEC-04",      "Customer Success Intelligence"),
    ],
    "TH": [
        ("TH-AIR-02",  "Irregular Ops"),
        ("TH-AIR-04",  "Baggage Operations"),
        ("TH-AIR-06",  "Crew Resource Planning"),
        ("TH-HOT-03",  "Revenue Management"),
        ("TH-HOT-05",  "Guest Experience"),
    ],
    "ICE": [
        ("ICE-Aftermarket-01", "Field Service Dispatch"),
        ("ICE-Aftermarket-03", "Warranty & Claims"),
        ("ICE-Aftermarket-05", "Parts & Inventory"),
        ("ICE-Connected-06",   "Connected Equipment"),
        ("ICE-EaaS-04",        "Equipment-as-a-Service"),
    ],
}

PRACTICES = ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]


# -------- 2. Chain-by-chain rewrite --------
# Find each <details>...</details> block whose body contains 'r-scenario'
# (those are the 35 chain cards). Rewrite its r-service row.

details_re = re.compile(
    r"(<details[^>]*>\s*<summary[^>]*>.*?</summary>)(.*?)(</details>)",
    re.DOTALL,
)

# Match r-service row fully so we can replace it
row_re = re.compile(
    r'(<div class="cbg-row r-service"[^>]*>\s*<span class="cbg-label">[^<]*</span>\s*<div class="cbg-text">)(.*?)(</div>\s*</div>)',
    re.DOTALL,
)

matches = list(details_re.finditer(html))
chain_idx = -1
rewrites = 0
skipped_already = 0

# Process from tail so offsets stay valid
for cm in reversed(matches):
    body = cm.group(2)
    if "r-scenario" not in body:
        continue
    # Count this chain's global index; we need the natural forward order,
    # so we recompute from the start by finding matches before this one.
    # Easier: pre-compute indices.
    pass

# Pre-compute all chain matches forward
chain_matches = [m for m in matches if "r-scenario" in m.group(2)]
chain_match_ids: dict[int, int] = {}  # match start -> chain index (0-based)
for i, m in enumerate(chain_matches):
    chain_match_ids[m.start()] = i

# Now rewrite (still from tail)
for cm in reversed(chain_matches):
    gi = chain_match_ids[cm.start()]
    practice = PRACTICES[gi // 5]
    body = cm.group(2)

    rm = row_re.search(body)
    if not rm:
        continue
    cbg_text = rm.group(2)
    if "svc-chip-list" in cbg_text:
        skipped_already += 1
        continue

    # Extract all service codes in cbg_text
    codes_in_scenario = set(re.findall(r"<code[^>]*>([A-Z][A-Za-z0-9\-]+)</code>", cbg_text))

    # Extract the prose that follows the last <code>
    # Strategy: strip all tags, then remove the code tokens to get a "prose"-ish tail
    tags_stripped = re.sub(r"<[^>]+>", " ", cbg_text)
    tags_stripped = re.sub(r"\s+", " ", tags_stripped).strip()
    # Remove each code + any trailing " ServiceName +" fragment; keep the rest
    prose = tags_stripped
    for c in codes_in_scenario:
        # Remove "CODE Name +" patterns
        prose = re.sub(
            re.escape(c) + r"\s+[^.+]*?(?:\+\s*|\.\s*)",
            "",
            prose,
        )
        prose = re.sub(re.escape(c), "", prose)
    prose = re.sub(r"\s+", " ", prose).strip()
    # Trim leading artefacts like "+" or "."
    prose = re.sub(r"^[+.\s]+", "", prose).strip()

    # Build the chip list
    catalog = SERVICE_CATALOG.get(practice, [])
    chips_html: list[str] = []
    for code, name in catalog:
        active = code in codes_in_scenario
        cls = "svc-chip active" if active else "svc-chip"
        chips_html.append(
            f'<span class="{cls}"><code class="svc-code">{code}</code> '
            f'<span class="svc-name">{name}</span></span>'
        )
    chip_list_html = (
        '<div class="svc-chip-list">' + "".join(chips_html) + "</div>"
    )

    new_cbg_text = chip_list_html
    if prose:
        new_cbg_text += f'<div class="svc-prose">{prose}</div>'

    # Replace inside body, then replace body inside html
    new_row = rm.group(1) + new_cbg_text + rm.group(3)
    new_body = body[:rm.start()] + new_row + body[rm.end():]

    # Splice back into html
    start, end = cm.start(2), cm.end(2)
    html = html[:start] + new_body + html[end:]
    rewrites += 1

print(f"Rewrote {rewrites} chain Service rows")
print(f"Skipped (already had chips): {skipped_already}")


# -------- 3. Inject CSS --------
CSS = (
    "/* svc-chip-list-v1 */\n"
    ".svc-chip-list {\n"
    "  display: flex; flex-wrap: wrap; gap: 6px 10px;\n"
    "  margin-bottom: 8px;\n"
    "  align-items: center;\n"
    "}\n"
    ".svc-chip {\n"
    "  display: inline-flex; align-items: center; gap: 6px;\n"
    "  padding: 3px 9px;\n"
    "  border-radius: 14px;\n"
    "  background: color-mix(in srgb, var(--bg-3) 55%, transparent);\n"
    "  border: 1px solid color-mix(in srgb, var(--ink-3, #8a8a8a) 45%, transparent);\n"
    "  font-size: 11.5px;\n"
    "  line-height: 1.45;\n"
    "  color: var(--ink-3, #8a8a8a);\n"
    "  transition: filter .15s ease;\n"
    "}\n"
    ".svc-chip .svc-code {\n"
    "  font-family: 'JetBrains Mono', 'Consolas', monospace;\n"
    "  font-size: 10.5px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.04em;\n"
    "  padding: 0; background: transparent;\n"
    "}\n"
    ".svc-chip .svc-name {\n"
    "  font-size: 11.5px;\n"
    "  color: inherit;\n"
    "}\n"
    ".svc-chip.active {\n"
    "  background: color-mix(in srgb, var(--sky, #6FB9E8) 18%, transparent);\n"
    "  border-color: color-mix(in srgb, var(--sky, #6FB9E8) 65%, transparent);\n"
    "  color: var(--sky, #6FB9E8);\n"
    "}\n"
    ".svc-chip.active .svc-code { color: var(--sky, #6FB9E8); }\n"
    ".svc-chip.active:hover { filter: brightness(1.15); }\n"
    ".svc-prose {\n"
    "  font-size: 12.5px;\n"
    "  line-height: 1.6;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "}\n"
)

if MARKER not in html:
    close_style = html.find("</style>")
    if close_style != -1:
        html = html[:close_style] + CSS + html[close_style:]
        print("Injected .svc-chip CSS")


HTML.write_text(html, encoding="utf-8")
print(f"\nWrote {HTML}")
