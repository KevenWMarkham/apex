"""MCP dispatcher with Charter-annotation-driven caching — Sprint 26 Task 26.6.

The dispatcher's contract:

1. At boot, parse CHARTER.md and hold the per-tool annotations
   (``cacheable``, ``cache_ttl_s``, ``oversight``, ``hitl_required``)
   in memory (Task 26.6.1).
2. Before executing a tool, build a stable cache key from the tool name
   + arg hash + Entra scope and check Redis (Task 26.6.2).
3. If miss, execute the underlying tool, then conditionally cache the
   response when ALL of these are true (Task 26.6.3):

   - Charter annotation: ``cacheable: true``
   - Tool is read-only (no write side effects)
   - Response classification ≤ Internal
   - Response size ≤ ``cache_size_limit_bytes`` (default 100 KB)

4. Emit ``cache_hit`` / ``cache_miss`` / ``cache_skip`` telemetry events
   (Task 26.6.4).

Reference: ``APEX-CORE.md`` §11, ``CHARTER.md`` §3.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

from apex_orchestrator.control_plane.redis_client import (
    CacheEvent,
    RedisControlPlane,
)


log = logging.getLogger("apex.orchestrator.mcp.dispatcher")


# ---------------------------------------------------------------------------
# Charter annotations
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CharterTool:
    """One MCP-tool annotation parsed from CHARTER.md §3."""

    name: str
    cacheable: bool
    cache_ttl_s: int
    oversight: str
    hitl_required: bool = False
    schema: str = ""


@dataclass
class CharterCatalog:
    """In-memory snapshot of the CHARTER §3 tool catalog."""

    tools: dict[str, CharterTool] = field(default_factory=dict)

    def get(self, tool: str) -> Optional[CharterTool]:
        return self.tools.get(tool)

    def must_get(self, tool: str) -> CharterTool:
        ct = self.tools.get(tool)
        if ct is None:
            raise KeyError(f"Tool {tool!r} not in CHARTER catalog")
        return ct


# Matches a CHARTER §3 markdown table row of the shape:
#   | `tool.name` | Schema | true | 30 | HOTL |
# where the third column is `cacheable` (bool), fourth is `cache_ttl_s`
# (int), fifth is `oversight`. Optional sixth column is `hitl_required`.
_TOOL_ROW_RE = re.compile(
    r"^\|\s*`([\w.\-]+)`\s*\|"   # tool name
    r"\s*([^|]*?)\s*\|"          # schema
    r"\s*(true|false)\s*\|"      # cacheable
    r"\s*(\d+)\s*\|"             # cache_ttl_s
    r"\s*(\w+)\s*\|"             # oversight
    r"(?:\s*(true|false)\s*\|)?",  # hitl_required (optional)
    re.IGNORECASE,
)


def parse_charter_catalog(charter_path: Path) -> CharterCatalog:
    """Parse CHARTER.md tool tables into a :class:`CharterCatalog`.

    Sprint 26 Task 26.6.1 — runs at boot, holds the result in memory.
    """
    if not charter_path.exists():
        raise FileNotFoundError(
            f"CHARTER.md missing at {charter_path} — required for MCP dispatch."
        )
    catalog = CharterCatalog()
    for line in charter_path.read_text(encoding="utf-8").splitlines():
        m = _TOOL_ROW_RE.search(line)
        if m is None:
            continue
        name, schema, cacheable, ttl, oversight = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        hitl_required_raw = m.group(6) or "false"
        catalog.tools[name] = CharterTool(
            name=name,
            cacheable=cacheable.lower() == "true",
            cache_ttl_s=int(ttl),
            oversight=oversight,
            hitl_required=hitl_required_raw.lower() == "true",
            schema=schema.strip(),
        )
    return catalog


# ---------------------------------------------------------------------------
# Arg hashing
# ---------------------------------------------------------------------------


def arg_hash_of(args: dict[str, Any]) -> str:
    """Stable SHA-256 of canonicalized JSON args for the cache key.

    Sort keys + default ``str`` for unserializable values so the hash is
    deterministic across calls with the same logical args.
    """
    canonical = json.dumps(args, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


@dataclass
class MCPDispatcher:
    """Cache-aware MCP tool dispatcher.

    Wires the Charter catalog + Redis control-plane into every tool
    invocation. Production deployments inject the real tool registry
    (a ``Callable[[str, dict], Any]`` that maps a tool name + args to
    the tool result); tests inject a lambda registry.

    Telemetry: a callback receives a :class:`CacheEvent` after every
    dispatch. Production wires this to ``telemetry-mcp``; tests assert
    against a list-collector.
    """

    catalog: CharterCatalog
    redis: RedisControlPlane
    tool_registry: Callable[[str, dict[str, Any]], Any]
    telemetry: Callable[[CacheEvent], None] = field(default=lambda _e: None)
    classification_resolver: Callable[[str, Any], str] = field(
        default=lambda _t, _v: "Internal"
    )
    """Resolves the classification of a tool's response. Default treats
    everything as Internal; production injects a Practice-aware resolver."""

    def dispatch(
        self,
        tool: str,
        args: dict[str, Any],
        *,
        entra_scope: str,
    ) -> Any:
        """Execute the tool with cache-read / cache-write per CHARTER."""
        if not entra_scope:
            raise ValueError(
                "MCP dispatch requires non-empty entra_scope — Sprint 26 Task 26.5 "
                "lint enforces this at commit time; runtime enforces at dispatch"
            )
        annotation = self.catalog.get(tool)
        ah = arg_hash_of(args)

        # --- Cache read path -----------------------------------------
        if annotation is not None and annotation.cacheable:
            hit = self.redis.get_cached_mcp_response(tool, ah, entra_scope)
            if hit is not None:
                self.telemetry(
                    CacheEvent(
                        event="cache_hit", tool=tool, arg_hash=ah,
                        entra_scope=entra_scope,
                    )
                )
                log.info(
                    "mcp.dispatch.cache_hit",
                    extra={"tool": tool, "entra_scope": entra_scope},
                )
                return hit
            self.telemetry(
                CacheEvent(
                    event="cache_miss", tool=tool, arg_hash=ah,
                    entra_scope=entra_scope,
                )
            )

        # --- Tool execution -----------------------------------------
        result = self.tool_registry(tool, args)

        # --- Cache write path (read-only + cacheable=true) -----------
        # Write tools are NEVER cached even if a misconfigured CHARTER
        # row marks them cacheable:true. The annotation below is the
        # belt-and-suspenders runtime check.
        if annotation is None:
            self.telemetry(
                CacheEvent(
                    event="cache_skip", tool=tool, arg_hash=ah,
                    entra_scope=entra_scope,
                    reason="no_charter_annotation",
                )
            )
            return result
        if not annotation.cacheable:
            self.telemetry(
                CacheEvent(
                    event="cache_skip", tool=tool, arg_hash=ah,
                    entra_scope=entra_scope,
                    reason="cacheable_false",
                )
            )
            return result
        if annotation.hitl_required:
            # Defensive: write tools (hitl_required) should already be
            # cacheable:false — but if the row is misconfigured, this is
            # the runtime backstop.
            self.telemetry(
                CacheEvent(
                    event="cache_skip", tool=tool, arg_hash=ah,
                    entra_scope=entra_scope,
                    reason="hitl_required_treated_as_write",
                )
            )
            return result

        classification = self.classification_resolver(tool, result)
        cached = self.redis.cache_mcp_response(
            tool, ah, entra_scope, result,
            ttl_s=annotation.cache_ttl_s,
            classification=classification,
        )
        if not cached:
            self.telemetry(
                CacheEvent(
                    event="cache_skip", tool=tool, arg_hash=ah,
                    entra_scope=entra_scope,
                    reason=f"redis_skip_or_classification_{classification}",
                )
            )
        return result
