"""Force scenario rows in the library modal to be flush-left.

Two CSS rules for .scenario-row stack: the original grid layout with
padding: 12px 24px and my pop-under override with flex layout. The
override didn't reset padding, so visible indent is the sum of both.

Fix: explicitly reset .scenario-row padding to 0 and control spacing
entirely from .sr-head. Also force text-align: left and flex-start on
the inner elements so nothing can auto-center.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
html = HTML.read_text(encoding="utf-8")

MARKER = "/* modal-row-align-v1 */"
if MARKER in html:
    print("Alignment fix already in place — no-op.")
    sys.exit(0)

CSS = (
    MARKER + "\n"
    ".scenario-row {\n"
    "  padding: 0 !important;\n"
    "  text-align: left;\n"
    "  justify-content: flex-start;\n"
    "  align-items: stretch;\n"
    "}\n"
    ".sr-head {\n"
    "  padding: 12px 20px !important;\n"
    "  text-align: left;\n"
    "  justify-items: start;\n"
    "}\n"
    ".sr-main {\n"
    "  text-align: left;\n"
    "  display: flex;\n"
    "  flex-direction: column;\n"
    "  align-items: flex-start;\n"
    "  gap: 2px;\n"
    "  min-width: 0;\n"
    "}\n"
    ".sr-main > .sr-id {\n"
    "  margin-right: 10px;\n"
    "  margin-bottom: 0;\n"
    "  align-self: flex-start;\n"
    "}\n"
    ".sr-title {\n"
    "  font-weight: 700;\n"
    "  font-size: 14px;\n"
    "  color: var(--ink-0, #fff);\n"
    "  text-align: left;\n"
    "  line-height: 1.35;\n"
    "}\n"
    ".sr-brief {\n"
    "  font-size: 12.5px;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  text-align: left;\n"
    "  line-height: 1.45;\n"
    "  margin-top: 2px;\n"
    "}\n"
    "/* Put ID pill inline with title so layout is: [ID] Title / blurb-below */\n"
    ".sr-main-row1 { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }\n"
    ".scenario-row .sr-service {\n"
    "  font-family: 'JetBrains Mono', 'Consolas', monospace;\n"
    "  font-size: 11.5px;\n"
    "  color: var(--gold, #E3B657);\n"
    "  white-space: nowrap;\n"
    "}\n"
)

close_style = html.find("</style>")
if close_style == -1:
    print("ERROR: </style> not found")
    sys.exit(1)
html = html[:close_style] + CSS + html[close_style:]
HTML.write_text(html, encoding="utf-8")
print(f"Injected alignment CSS")
print(f"Wrote {HTML}")
