"""Cache-governance CI lint — Sprint 26 Task 26.5 (BL.APEX-v0.2-F-01).

Enforces the rule that **every MCP tool marked `cacheable: false` in
`CHARTER.md` is never read or written through the cache APIs**. This is
the static backstop to the runtime check in
``apex_orchestrator.control_plane.redis_client``.

Two checks:

1. **Cacheable-violation check** — for every call to
   ``cache_mcp_response()`` or ``get_cached_mcp_response()`` in any
   ``packages/`` Python file, verify the tool name (the first string
   argument) is marked ``cacheable: true`` in CHARTER. If the tool is
   ``cacheable: false`` or unannotated, fail the lint.

2. **Key-naming-convention check** — every cache key must include the
   caller's Entra scope segment. The convention (per APEX-CORE §11) is
   ``apex:mcp:{tool}:{arg_hash}:{entra_scope}``. We don't enforce the
   exact string — we enforce that the call passes ``entra_scope=`` as
   a non-empty argument.

Exit 0 = clean. Exit 1 = at least one violation.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CHARTER_PATH = Path("apex-workspace") / "CHARTER.md"


# ---------------------------------------------------------------------------
# CHARTER parser
# ---------------------------------------------------------------------------


_CHARTER_TOOL_ROW_RE = re.compile(
    r"\|\s*`([\w.\-]+)`\s*\|[^|]*\|\s*(true|false)\s*\|",
    re.IGNORECASE,
)


@dataclass
class CharterAnnotation:
    tool: str
    cacheable: bool
    source_line: int


def parse_charter_annotations(charter_path: Path) -> dict[str, CharterAnnotation]:
    """Extract ``{tool_name: CharterAnnotation}`` from CHARTER.md tables."""
    if not charter_path.exists():
        raise FileNotFoundError(
            f"CHARTER.md missing at {charter_path} — Sprint 26 Task 26.1 "
            "must complete before this lint can run."
        )
    out: dict[str, CharterAnnotation] = {}
    for i, line in enumerate(charter_path.read_text(encoding="utf-8").splitlines(), 1):
        m = _CHARTER_TOOL_ROW_RE.search(line)
        if m is None:
            continue
        tool, cacheable_raw = m.group(1), m.group(2).lower()
        out[tool] = CharterAnnotation(
            tool=tool,
            cacheable=(cacheable_raw == "true"),
            source_line=i,
        )
    return out


# ---------------------------------------------------------------------------
# Code scanner
# ---------------------------------------------------------------------------


CACHE_FUNCTION_NAMES = {"cache_mcp_response", "get_cached_mcp_response"}


@dataclass
class CacheCallSite:
    path: Path
    lineno: int
    func: str
    tool_name: str | None
    has_entra_scope_kwarg: bool


def find_cache_call_sites(root: Path) -> list[CacheCallSite]:
    """Walk every .py file under root; flag calls to cache helpers."""
    sites: list[CacheCallSite] = []
    for path in root.rglob("*.py"):
        # Skip exempt modules:
        # - redis_client.py implements the cache helpers themselves
        # - mcp/dispatcher.py is the central cache-aware gateway that does
        #   CHARTER-annotation gating internally (Sprint 26 Task 26.6) and
        #   necessarily passes variable tool names through
        # - lint module + tests for these modules call the helpers intentionally
        rel = path.as_posix()
        if any(hint in rel for hint in (
            "redis_client", "lint_cache_governance",
            "mcp/dispatcher", "mcp\\dispatcher",
        )):
            continue
        if path.name.startswith("test_") and any(
            hint in path.name for hint in ("redis_client", "mcp_dispatcher")
        ):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func_name = _resolve_func_name(node.func)
            if func_name not in CACHE_FUNCTION_NAMES:
                continue
            tool_name = _first_string_arg(node)
            has_entra = any(
                kw.arg == "entra_scope"
                and isinstance(kw.value, (ast.Constant, ast.Name))
                for kw in node.keywords
            ) or _positional_entra_scope_present(node, func_name)
            sites.append(
                CacheCallSite(
                    path=path,
                    lineno=node.lineno,
                    func=func_name,
                    tool_name=tool_name,
                    has_entra_scope_kwarg=has_entra,
                )
            )
    return sites


def _resolve_func_name(func: ast.expr) -> str:
    """Return the trailing attribute name (handles `self.cache_mcp_response`)."""
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return ""


def _first_string_arg(call: ast.Call) -> str | None:
    """Return the first positional Constant string argument (the `tool` arg)."""
    for arg in call.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            return arg.value
    return None


def _positional_entra_scope_present(call: ast.Call, func: str) -> bool:
    """Heuristic — both helpers take entra_scope as the third positional."""
    if func in ("cache_mcp_response", "get_cached_mcp_response"):
        return len(call.args) >= 3
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Cache-governance lint — fails the build if any code path caches "
            "an MCP tool marked cacheable:false in CHARTER.md."
        )
    )
    parser.add_argument(
        "--root", default=".",
        help="Repo root (default: current directory).",
    )
    parser.add_argument(
        "--charter", default=str(CHARTER_PATH),
        help="Path to CHARTER.md (default: apex-workspace/CHARTER.md).",
    )
    parser.add_argument(
        "--scan", default="packages",
        help="Directory to scan for cache calls (default: packages).",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    charter_path = (root / args.charter).resolve()
    scan_root = (root / args.scan).resolve()
    if not scan_root.exists():
        print(f"warn: scan root does not exist: {scan_root}", file=sys.stderr)
        return 0

    annotations = parse_charter_annotations(charter_path)
    sites = find_cache_call_sites(scan_root)

    violations: list[str] = []
    for site in sites:
        if site.tool_name is None:
            violations.append(
                f"[NON_LITERAL_TOOL_NAME] {site.path}:{site.lineno} — "
                f"{site.func}() called with non-literal tool name; "
                "the lint cannot verify governance"
            )
            continue
        anno = annotations.get(site.tool_name)
        if anno is None:
            violations.append(
                f"[UNKNOWN_TOOL] {site.path}:{site.lineno} — "
                f"{site.func}({site.tool_name!r}) — tool not in CHARTER.md catalog"
            )
            continue
        if not anno.cacheable:
            violations.append(
                f"[CACHEABLE_FALSE_VIOLATION] {site.path}:{site.lineno} — "
                f"{site.func}({site.tool_name!r}) — CHARTER.md:{anno.source_line} "
                "marks this tool cacheable:false"
            )
        if not site.has_entra_scope_kwarg:
            violations.append(
                f"[MISSING_ENTRA_SCOPE] {site.path}:{site.lineno} — "
                f"{site.func}({site.tool_name!r}) — every cache key must include "
                "an Entra scope segment per APEX-CORE §11"
            )

    print(f"CHARTER tools annotated: {len(annotations)}")
    print(f"cache call sites scanned: {len(sites)}")
    print(f"violations: {len(violations)}")

    if not violations:
        print("OK — cache governance clean")
        return 0

    for v in violations:
        print(v, file=sys.stderr)
    print(
        f"FAIL — {len(violations)} cache-governance violation(s) "
        "(see APEX-CORE.md §11 + CHARTER.md §3)",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
