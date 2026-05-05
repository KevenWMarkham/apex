"""Scenario library exporters — Sprint 28 Task 28.4.

CSV export with auto-filename generation. (PowerPoint export — Task
28.4.2 — uses pptxgenjs server-side via a worker; that lives in the
front-end track and is out of scope for this Python package.)

Filename pattern (Task 28.4.3):
    APEX-scenarios-{practice}-{YYYY-MM-DD}.csv

For multi-practice exports, ``practice`` collapses to ``"all"``.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
from collections.abc import Iterable
from pathlib import Path

from apex_scenarios.models import Scenario


# ---------------------------------------------------------------------------
# CSV columns (exposed to clients in client-cleared content)
# ---------------------------------------------------------------------------

CSV_COLUMNS: tuple[str, ...] = (
    "practice",
    "service_code",
    "title",
    "brief",
    "kpi",
    "kpi_direction",
    "w1",
    "w2",
    "w3",
    "archetype_id",
    "mesh_id",
)


# ---------------------------------------------------------------------------
# Filename helper (Task 28.4.3)
# ---------------------------------------------------------------------------


def csv_filename(
    *,
    practices: Iterable[str] | None = None,
    when: dt.date | None = None,
    label: str | None = None,
) -> str:
    """Generate the canonical CSV export filename.

    Args:
        practices: Iterable of practice codes filtered to. If None, all
            seven practices are assumed and the segment becomes "all".
            If exactly one practice, that code is used. If multiple,
            "multi" is used (preserves single-line filename hygiene).
        when: Date stamp. Defaults to today (UTC).
        label: Optional extra label appended before the date
            (e.g., "filtered", "wave-incomplete").

    Returns:
        Filename like ``APEX-scenarios-rc-2026-05-04.csv`` or
        ``APEX-scenarios-all-2026-05-04.csv``.
    """
    if practices is None:
        practice_segment = "all"
    else:
        codes = sorted({p.lower() for p in practices})
        if len(codes) == 0:
            practice_segment = "empty"
        elif len(codes) == 1:
            practice_segment = codes[0]
        elif len(codes) == 7:
            practice_segment = "all"
        else:
            practice_segment = "multi"

    date_str = (when or dt.date.today()).strftime("%Y-%m-%d")
    label_segment = f"-{label}" if label else ""
    return f"APEX-scenarios-{practice_segment}{label_segment}-{date_str}.csv"


# ---------------------------------------------------------------------------
# Writers (Task 28.4.1)
# ---------------------------------------------------------------------------


def _row_to_dict(s: Scenario) -> dict[str, str]:
    return {
        "practice": s.practice or "",
        "service_code": s.service_code,
        "title": s.title,
        "brief": s.brief,
        "kpi": s.kpi,
        "kpi_direction": s.kpi_direction,
        "w1": s.w1,
        "w2": s.w2,
        "w3": s.w3,
        "archetype_id": s.archetype_id or "",
        "mesh_id": s.mesh_id or "",
    }


def write_csv(
    scenarios: Iterable[Scenario],
    path: str | Path,
) -> int:
    """Write scenarios to CSV at ``path``. Returns row count written.

    UTF-8 with BOM so Excel opens it cleanly. CRLF line endings via the
    csv writer's default behavior on the underlying file.
    """
    rows = list(scenarios)
    p = Path(path)
    with p.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(CSV_COLUMNS))
        writer.writeheader()
        for s in rows:
            writer.writerow(_row_to_dict(s))
    return len(rows)


def write_csv_string(scenarios: Iterable[Scenario]) -> str:
    """Render scenarios as a CSV string (used by tests and stdout output)."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(CSV_COLUMNS))
    writer.writeheader()
    for s in scenarios:
        writer.writerow(_row_to_dict(s))
    return buf.getvalue()
