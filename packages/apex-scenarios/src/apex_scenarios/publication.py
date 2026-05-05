"""Appendix L — Scenario Library Master Catalog publication (Task 28.7.1).

Publishes a readable companion to the JSON library:

- One markdown file per Practice with sections, tables, and KPI
  highlights.
- A combined index.md that lists every Practice's coverage and a
  summary table.

The output is suitable for inclusion in the Sellers Guide as Appendix L.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from apex_scenarios.library import ScenarioIndex
from apex_scenarios.models import PRACTICE_CODES


PRACTICE_LONG_NAME: dict[str, str] = {
    "RC": "Retail & Consumer",
    "HLS": "Healthcare & Life Sciences",
    "ER": "Energy & Resources",
    "AXLE": "Industrial & Manufacturing (AXLE)",
    "TMT": "Technology, Media & Telecom",
    "TH": "Travel & Hospitality",
    "ICE": "Industrial & Commercial Equipment",
}


def render_practice_markdown(index: ScenarioIndex, practice: str) -> str:
    """Render the master catalog page for one Practice."""
    rows = index.by_practice(practice)
    long_name = PRACTICE_LONG_NAME.get(practice, practice)

    lines: list[str] = []
    lines.append(f"# Appendix L — Scenario Library — {long_name} ({practice})")
    lines.append("")
    lines.append(f"**Total scenarios:** {len(rows)}")
    lines.append("")
    lines.append(
        f"**Source of truth:** `docs/scenarios/_catalog/scenario-library.json` "
        f"(stamped at master-catalog publication time)."
    )
    lines.append("")
    lines.append(
        "Every row below carries a service code, a one-line brief, the "
        "KPI delta the scenario targets, and (post-Sprint-28) Wave 1 / "
        "2 / 3 narratives. Wave content is omitted from this table for "
        "compactness; see the sibling JSON for the full payload."
    )
    lines.append("")
    lines.append("| # | Service | Title | KPI |")
    lines.append("|---|---|---|---|")
    for i, s in enumerate(rows, start=1):
        # Markdown-escape pipe characters in fields
        title = s.title.replace("|", "\\|")
        kpi = s.kpi.replace("|", "\\|")
        lines.append(f"| {i} | `{s.service_code}` | {title} | {kpi} |")
    lines.append("")

    return "\n".join(lines)


def render_index_markdown(index: ScenarioIndex) -> str:
    """Render the cross-Practice master-catalog index."""
    counts = index.practice_counts()
    total = sum(counts.values())
    today = dt.date.today().strftime("%Y-%m-%d")

    lines: list[str] = []
    lines.append("# Appendix L — Scenario Library Master Catalog")
    lines.append("")
    lines.append(f"**Date:** {today}")
    lines.append(f"**Total scenarios:** {total}")
    lines.append("**Source:** `docs/scenarios/_catalog/scenario-library.json`")
    lines.append("**Sprint:** APEX Orchestrator Sprint 28 Task 28.7.1")
    lines.append("")
    lines.append("## Per-Practice coverage")
    lines.append("")
    lines.append("| Practice | Long name | Scenarios |")
    lines.append("|---|---|---|")
    for p in PRACTICE_CODES:
        lines.append(f"| `{p}` | {PRACTICE_LONG_NAME[p]} | {counts.get(p, 0)} |")
    lines.append(f"| **TOTAL** | | **{total}** |")
    lines.append("")
    lines.append("## Per-Practice indexes")
    lines.append("")
    for p in PRACTICE_CODES:
        lines.append(f"- [{p} — {PRACTICE_LONG_NAME[p]}](./{p.lower()}.md)")
    lines.append("")
    lines.append("## Wave-data completion status")
    lines.append("")
    full = len(index.with_full_wave_data())
    missing = len(index.missing_wave_data())
    lines.append(f"- Full wave data (W1+W2+W3 populated): **{full}** scenarios")
    lines.append(f"- Wave data incomplete: **{missing}** scenarios")
    lines.append("")
    if missing > 0:
        lines.append(
            "> Sprint 28 Task 28.1.6 gates the library on full wave-data "
            "presence. The CI `scenarios` lane fails until every row "
            "has non-empty W1 / W2 / W3 content."
        )
    lines.append("")
    return "\n".join(lines)


def publish_master_catalog(
    index: ScenarioIndex,
    output_dir: str | Path,
) -> dict[str, Path]:
    """Write the full Appendix L master catalog to a directory.

    Returns a dict mapping each artifact name to its written path.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    written: dict[str, Path] = {}

    index_path = out / "index.md"
    index_path.write_text(render_index_markdown(index), encoding="utf-8")
    written["index"] = index_path

    for p in PRACTICE_CODES:
        practice_path = out / f"{p.lower()}.md"
        practice_path.write_text(render_practice_markdown(index, p), encoding="utf-8")
        written[p] = practice_path

    return written
