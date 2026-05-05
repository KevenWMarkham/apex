"""Tests for apex_orchestrator.mcp.dispatcher — Sprint 26 Task 26.6."""

from __future__ import annotations

from pathlib import Path

import pytest

from apex_orchestrator.control_plane.redis_client import (
    RedisControlPlane,
    StubRedis,
)
from apex_orchestrator.mcp.dispatcher import (
    CacheEvent,
    CharterCatalog,
    CharterTool,
    MCPDispatcher,
    arg_hash_of,
    parse_charter_catalog,
)


CHARTER_PATH = Path(__file__).resolve().parents[3] / "apex-workspace" / "CHARTER.md"


# ---------------------------------------------------------------------------
# CHARTER parser
# ---------------------------------------------------------------------------


def test_parse_charter_catalog_finds_cacheable_tools() -> None:
    catalog = parse_charter_catalog(CHARTER_PATH)
    item_get = catalog.get("rc.item.get")
    assert item_get is not None
    assert item_get.cacheable is True
    assert item_get.cache_ttl_s == 30
    assert item_get.oversight == "HOTL"


def test_parse_charter_catalog_finds_pii_tools() -> None:
    catalog = parse_charter_catalog(CHARTER_PATH)
    customer = catalog.get("rc.customer.get")
    assert customer is not None
    assert customer.cacheable is False
    assert customer.cache_ttl_s == 0


def test_parse_charter_catalog_finds_write_tools() -> None:
    catalog = parse_charter_catalog(CHARTER_PATH)
    write = catalog.get("rc.markdown.action.commit")
    assert write is not None
    assert write.cacheable is False
    assert write.hitl_required is True
    assert write.oversight == "HITL"


def test_parse_charter_missing_path_raises() -> None:
    with pytest.raises(FileNotFoundError):
        parse_charter_catalog(Path("/does/not/exist/CHARTER.md"))


# ---------------------------------------------------------------------------
# Arg hashing
# ---------------------------------------------------------------------------


def test_arg_hash_is_stable_across_key_order() -> None:
    h1 = arg_hash_of({"a": 1, "b": 2})
    h2 = arg_hash_of({"b": 2, "a": 1})
    assert h1 == h2


def test_arg_hash_changes_with_value() -> None:
    h1 = arg_hash_of({"a": 1})
    h2 = arg_hash_of({"a": 2})
    assert h1 != h2


# ---------------------------------------------------------------------------
# Dispatcher — cache pathways
# ---------------------------------------------------------------------------


def _build_dispatcher(tools: dict[str, CharterTool], registry, telemetry):
    cat = CharterCatalog(tools=tools)
    redis = RedisControlPlane(StubRedis())
    return MCPDispatcher(
        catalog=cat, redis=redis,
        tool_registry=registry, telemetry=telemetry,
    )


def test_dispatcher_caches_read_tool_with_cacheable_true() -> None:
    calls: list[CacheEvent] = []
    invocations = 0

    def registry(tool: str, args: dict) -> dict:
        nonlocal invocations
        invocations += 1
        return {"tool": tool, "args": args, "result": invocations}

    d = _build_dispatcher(
        {"rc.item.get": CharterTool("rc.item.get", cacheable=True, cache_ttl_s=30, oversight="HOTL")},
        registry, calls.append,
    )
    r1 = d.dispatch("rc.item.get", {"id": 1}, entra_scope="scope-A")
    r2 = d.dispatch("rc.item.get", {"id": 1}, entra_scope="scope-A")
    assert r1 == r2
    # Second call must be a cache hit — registry only called once
    assert invocations == 1
    events = [e.event for e in calls]
    assert "cache_miss" in events
    assert "cache_hit" in events


def test_dispatcher_skips_cache_when_cacheable_false() -> None:
    calls: list[CacheEvent] = []
    invocations = 0

    def registry(tool: str, args: dict) -> dict:
        nonlocal invocations
        invocations += 1
        return {"v": invocations}

    d = _build_dispatcher(
        {"rc.customer.get": CharterTool(
            "rc.customer.get", cacheable=False, cache_ttl_s=0, oversight="HOTL",
        )},
        registry, calls.append,
    )
    r1 = d.dispatch("rc.customer.get", {"id": 1}, entra_scope="scope-A")
    r2 = d.dispatch("rc.customer.get", {"id": 1}, entra_scope="scope-A")
    # Both calls hit the registry — no caching
    assert invocations == 2
    assert r1["v"] == 1
    assert r2["v"] == 2
    skip_reasons = {e.reason for e in calls if e.event == "cache_skip"}
    assert "cacheable_false" in skip_reasons


def test_dispatcher_skips_cache_for_write_tools() -> None:
    """Even if a row mistakenly says cacheable:true, hitl_required:true blocks caching."""
    calls: list[CacheEvent] = []
    d = _build_dispatcher(
        {"rc.write.tool": CharterTool(
            "rc.write.tool", cacheable=True, cache_ttl_s=30,
            oversight="HITL", hitl_required=True,
        )},
        lambda t, a: {"ok": True},
        calls.append,
    )
    d.dispatch("rc.write.tool", {"id": 1}, entra_scope="scope-A")
    skip_reasons = {e.reason for e in calls if e.event == "cache_skip"}
    assert "hitl_required_treated_as_write" in skip_reasons


def test_dispatcher_skips_cache_for_unknown_tool() -> None:
    calls: list[CacheEvent] = []
    d = _build_dispatcher({}, lambda t, a: {"ok": True}, calls.append)
    d.dispatch("rc.unknown.tool", {}, entra_scope="scope-A")
    skip_reasons = {e.reason for e in calls if e.event == "cache_skip"}
    assert "no_charter_annotation" in skip_reasons


def test_dispatcher_segregates_by_entra_scope() -> None:
    invocations = 0

    def registry(tool: str, args: dict) -> dict:
        nonlocal invocations
        invocations += 1
        return {"v": invocations}

    d = _build_dispatcher(
        {"rc.item.get": CharterTool("rc.item.get", cacheable=True, cache_ttl_s=30, oversight="HOTL")},
        registry, lambda _e: None,
    )
    r1 = d.dispatch("rc.item.get", {"id": 1}, entra_scope="scope-A")
    r2 = d.dispatch("rc.item.get", {"id": 1}, entra_scope="scope-B")
    # Different scopes → separate cache keys → both hit the registry
    assert invocations == 2
    assert r1 != r2


def test_dispatcher_rejects_empty_entra_scope() -> None:
    d = _build_dispatcher({}, lambda t, a: {}, lambda _e: None)
    with pytest.raises(ValueError, match="entra_scope"):
        d.dispatch("rc.x", {}, entra_scope="")


def test_dispatcher_skips_cache_for_pii_classification() -> None:
    """Runtime backstop — PII responses don't cache even when annotation says ok."""
    calls: list[CacheEvent] = []
    d = _build_dispatcher(
        {"rc.something": CharterTool("rc.something", cacheable=True, cache_ttl_s=30, oversight="HOTL")},
        lambda t, a: {"v": 1}, calls.append,
    )
    d.classification_resolver = lambda _t, _v: "pii"
    d.dispatch("rc.something", {}, entra_scope="scope-A")
    # Should miss + execute, then skip cache write due to classification
    skip_reasons = {e.reason for e in calls if e.event == "cache_skip"}
    assert any("classification" in r for r in skip_reasons)


# ---------------------------------------------------------------------------
# Conformance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_charter_yields_known_anchor_tools() -> None:
    """Sprint 26 Task 26.3.1 — RC anchor tools land in the parsed catalog."""
    cat = parse_charter_catalog(CHARTER_PATH)
    anchors = {
        "rc.item.get", "rc.hierarchy.tree", "rc.customer.get",
        "rc.payment.method.get", "rc.markdown.action.commit",
    }
    assert anchors.issubset(cat.tools.keys())


@pytest.mark.conformance
def test_conformance_pii_pci_tools_marked_uncacheable() -> None:
    """Sprint 26 governance — every PII / PCI tool has cacheable:false."""
    cat = parse_charter_catalog(CHARTER_PATH)
    for tool_name in ("rc.customer.get", "rc.customer.identity.lookup",
                      "rc.payment.method.get", "rc.payment.transaction.get"):
        tool = cat.tools.get(tool_name)
        assert tool is not None and tool.cacheable is False, \
            f"{tool_name} must be cacheable:false"


@pytest.mark.conformance
def test_conformance_every_write_tool_has_hitl_required() -> None:
    cat = parse_charter_catalog(CHARTER_PATH)
    write_tools = [t for t in cat.tools.values() if "commit" in t.name or "issue" in t.name or "update" in t.name]
    for t in write_tools:
        assert t.hitl_required is True, \
            f"{t.name} is a write tool — must have hitl_required:true"
        assert t.cacheable is False, \
            f"{t.name} is a write tool — must have cacheable:false"
