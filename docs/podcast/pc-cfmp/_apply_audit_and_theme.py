"""Wave 39 — full Capabilities Map regen pipeline.

Replaces the prior multi-step (build → manual splice → manual theme) with
one command that:

  1. Runs _build_capabilities_map.py to emit fresh enriched JSON (files
     list scanned from the live iot_device codebase)
  2. Overlays Wave 39 audit corrections from _refresh_c1_audit.py's AUDIT
     dict (status / progress_pct / gaps / mobile_parity per cap)
  3. Splices the resulting JSON into CFMP-Capabilities-Map.html between
     `const CAP_DATA = ` and the matching closing `};`
  4. Replaces the warm-cream + Fraunces theme with the GitHub-dark +
     system-ui theme matching /architecture (Wave 38 verbatim)
  5. Writes the result to both:
       - this directory (the APEX source HTML)
       - C:\\code\\iot_device\\portal\\public\\CFMP-Capabilities-Map.html
         (what the live URL actually serves)

Run from this directory:
    PYTHONIOENCODING=utf-8 python _apply_audit_and_theme.py
"""
from __future__ import annotations

import io
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
SRC_HTML = HERE / "CFMP-Capabilities-Map.html"
PORTAL_HTML = pathlib.Path(r"C:\code\iot_device\portal\public\CFMP-Capabilities-Map.html")
BUILD_SCRIPT = HERE / "_build_capabilities_map.py"
AUDIT_SCRIPT = HERE / "_refresh_c1_audit.py"

# ─────────────────────────────────────────────────────────────────────────────
# Theme block (Wave 38) — GitHub-dark to match /architecture. Replaces the
# original warm-cream + Fraunces + Instrument Sans + JetBrains Mono CSS.
# Drop-in for the existing <head> section (preconnect/link tags + first
# CSS rule blocks down through .display + .mono definitions).
# ─────────────────────────────────────────────────────────────────────────────

THEME_HEAD = '''<!--
  Theme: matched to /architecture page (Wave 38, 2026-05-26).
  Drops Google Fonts dependency entirely — uses the same system-ui stack
  + browser default monospace as the portal architecture page. The
  prior custom palette (warm cream + Fraunces serif + Instrument Sans
  + JetBrains Mono) is replaced by GitHub-dark tokens so the two pages
  feel like one product. All hundreds of style rules below reference
  CSS custom properties (--bg, --ink, --purple, etc.) so the reskin
  flows through automatically.
-->
<style>
:root[data-theme="dark"]{
  --bg:#010409; --bg-1:#0d1117; --bg-2:#161b22;
  --surface:#0d1117; --surface-2:#1c2128;
  --border:#21262d; --border-2:#30363d;
  --ink:#cdd9e5; --ink-2:#8b949e; --ink-3:#7d8590;
  --teal:#7ee787; --teal-dim:#2e8568; --teal-bg:#0a3d2e;
  --purple:#58a6ff; --purple-dim:#1f6feb; --purple-bg:#0c2d6b;
  --amber:#fbbf24; --amber-dim:#b07715; --amber-bg:#3a2608;
  --crimson:#f87171; --crimson-dim:#b91c1c; --crimson-bg:#3b1212;
  --gold:#d4a72c; --gold-dim:#a6892c; --gold-bg:#2d2308;
  --muted-teal:#0a3d2e;
}
:root[data-theme="light"]{
  --bg:#ffffff; --bg-1:#f6f8fa; --bg-2:#eaeef2;
  --surface:#ffffff; --surface-2:#f6f8fa;
  --border:#d0d7de; --border-2:#afb8c1;
  --ink:#1f2328; --ink-2:#656d76; --ink-3:#848d97;
  --teal:#1a7f37; --teal-dim:#2da44e; --teal-bg:#dafbe1;
  --purple:#0969da; --purple-dim:#0550ae; --purple-bg:#ddf4ff;
  --amber:#9a6700; --amber-dim:#bf8700; --amber-bg:#fff8c5;
  --crimson:#cf222e; --crimson-dim:#a40e26; --crimson-bg:#ffebe9;
  --gold:#9a6700; --gold-dim:#7d4e00; --gold-bg:#fff8c5;
  --muted-teal:#dafbe1;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  background:var(--bg); color:var(--ink);
  font-family:system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  font-size:14.5px; line-height:1.55;
  -webkit-font-smoothing:antialiased;
  transition:background .25s ease,color .25s ease;
}
.wrap{max-width:1320px;margin:0 auto;padding:0 28px}
.display{font-family:inherit;font-weight:600;letter-spacing:-.01em}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace;font-size:.86em}'''

# The block we replace is everything from the preconnect/link tags down
# through the original `.mono{...}` rule. Anchor on the unique opening
# (the preconnect line) and the unique close (the .mono rule).
HEAD_REPLACE_START = '<link rel="preconnect" href="https://fonts.googleapis.com">'
HEAD_REPLACE_END = '.mono{font-family:"JetBrains Mono",monospace;font-size:.86em}'


def _apply_theme(html: str) -> str:
    """Replace the warm-cream + Google Fonts head with GitHub-dark + system-ui.
    Also bulk-replaces remaining named-font references in the rest of
    the CSS rule body (~31 inline sites)."""
    start = html.find(HEAD_REPLACE_START)
    end = html.find(HEAD_REPLACE_END)
    if start == -1 or end == -1:
        # Theme already applied — nothing to do.
        return html
    # Snip from start of preconnect line through the END of the .mono rule.
    end_with_brace = end + len(HEAD_REPLACE_END)
    new_html = html[:start] + THEME_HEAD + html[end_with_brace:]
    # Bulk-replace remaining inline font-family refs in rule bodies.
    new_html = new_html.replace(
        'font-family:"JetBrains Mono",monospace',
        "font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace",
    )
    new_html = new_html.replace(
        'font-family:"Fraunces",serif',
        "font-family:inherit;font-weight:600",
    )
    new_html = new_html.replace(
        'font-family:"Instrument Sans",system-ui,sans-serif',
        "font-family:system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif",
    )
    return new_html


def _apply_audit(data: dict) -> dict:
    """Overlay Wave 39 audit corrections onto the enriched JSON."""
    # Import side-by-side to avoid duplicating the audit table.
    import importlib.util
    spec = importlib.util.spec_from_file_location("c1audit", AUDIT_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    audit = mod.AUDIT
    for cap in data.get("capabilities", []):
        if cap["id"] in audit:
            for k, v in audit[cap["id"]].items():
                if k.startswith("_"):
                    continue
                cap[k] = v
    return data


def _splice_json(html: str, data: dict) -> str:
    """Replace the `const CAP_DATA = { ... };` block with the new payload."""
    # The opening anchor is unambiguous. The close is the `};` followed by
    # newline + the next non-data script line — find the first `^};` after
    # the open.
    open_idx = html.find("const CAP_DATA = {")
    if open_idx == -1:
        raise RuntimeError("Could not find `const CAP_DATA = {` in HTML")
    # Walk braces to find the matching close. Strings are quoted with " and
    # we don't expect escaped quotes in our keys/values, but be defensive.
    i = open_idx + len("const CAP_DATA = ")
    depth = 0
    in_str = False
    esc = False
    while i < len(html):
        ch = html[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    # Consume optional trailing semicolon.
                    end = i + 1
                    if end < len(html) and html[end] == ";":
                        end += 1
                    return (html[:open_idx]
                            + "const CAP_DATA = "
                            + json.dumps(data, indent=2, ensure_ascii=False)
                            + ";"
                            + html[end:])
        i += 1
    raise RuntimeError("Unbalanced braces in CAP_DATA block")


def main() -> int:
    print("[1/5] Running _build_capabilities_map.py to get enriched JSON…")
    proc = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        capture_output=True, text=True, encoding="utf-8",
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
    )
    if proc.returncode != 0:
        print(f"  build script failed: {proc.stderr}", file=sys.stderr)
        return 1
    data = json.loads(proc.stdout)
    print(f"  got {len(data.get('capabilities', []))} caps + "
          f"{len(data.get('lanes', []))} lanes")

    print("[2/5] Applying Wave 39 audit overrides to C1.x…")
    data = _apply_audit(data)
    c1_count = sum(1 for c in data["capabilities"] if c["id"].startswith("C1."))
    print(f"  audited {c1_count} C1.x entries")

    print(f"[3/5] Reading source HTML {SRC_HTML.name}…")
    html = io.open(SRC_HTML, encoding="utf-8").read()
    print(f"  {len(html):,} chars")

    print("[4/5] Splicing JSON + applying Wave 38 theme…")
    html = _splice_json(html, data)
    html = _apply_theme(html)

    print("[5/5] Writing both targets…")
    io.open(SRC_HTML, "w", encoding="utf-8", newline="\n").write(html)
    PORTAL_HTML.parent.mkdir(parents=True, exist_ok=True)
    io.open(PORTAL_HTML, "w", encoding="utf-8", newline="\n").write(html)
    print(f"  -> {SRC_HTML}")
    print(f"  -> {PORTAL_HTML}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
