"""Expand the architecture diagram to fit the full page width.

Before: the Overview/flow SVG has min-width: 1560px and viewBox 0 0 1320 640,
while the .deep-page container caps at max-width: 1280px with overflow:hidden
on the wrapper — so ~280px of the diagram is clipped off the right edge.

After:
1. .flow-svg min-width removed (scales to container via viewBox)
2. .deep-page max-width widened to 1600px so the diagram gets more room
   on wide monitors; drops to 100% on narrow ones
3. .flow-svg-wrap gets horizontal overflow-auto as graceful fallback
   on very narrow viewports

Idempotent via /* arch-diagram-fit-v1 */ marker.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
html = HTML.read_text(encoding="utf-8")

MARKER = "/* arch-diagram-fit-v1 */"
if MARKER in html:
    print("Architecture fit already applied — no-op.")
    sys.exit(0)

CSS = (
    MARKER + "\n"
    "/* Remove the hard 1560px floor so the SVG scales with the container. */\n"
    ".flow-svg {\n"
    "  min-width: 0 !important;\n"
    "  width: 100%;\n"
    "  height: auto;\n"
    "  max-width: 100%;\n"
    "  display: block;\n"
    "}\n"
    "/* Widen deep-page so the Overview diagram gets the space it was designed for. */\n"
    ".deep-page {\n"
    "  max-width: min(1600px, 96vw) !important;\n"
    "}\n"
    "/* Graceful fallback: if viewport is very narrow, allow horizontal scroll\n"
    "   so the diagram remains legible rather than squished. */\n"
    ".flow-svg-wrap {\n"
    "  overflow-x: auto;\n"
    "  overflow-y: hidden;\n"
    "  -webkit-overflow-scrolling: touch;\n"
    "}\n"
    "@media (max-width: 900px) {\n"
    "  .flow-svg { min-width: 1100px !important; }\n"
    "}\n"
)

close_style = html.find("</style>")
if close_style == -1:
    print("ERROR: </style> not found")
    sys.exit(1)
html = html[:close_style] + CSS + html[close_style:]
HTML.write_text(html, encoding="utf-8")
print(f"Injected architecture-fit CSS")
