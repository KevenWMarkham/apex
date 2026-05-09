"""Loader for services/_registry.json — the wizard's view of the catalog."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parents[5] / "services" / "_registry.json"


@lru_cache(maxsize=1)
def load_registry() -> dict[str, Any]:
    with REGISTRY_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def industries() -> list[dict[str, str]]:
    return load_registry()["industries"]


def service_codes(industry: str | None = None) -> list[dict[str, Any]]:
    codes = load_registry()["service_codes"]
    if industry:
        codes = [c for c in codes if c["industry"] == industry]
    return codes


def scenarios(
    *,
    industry: str | None = None,
    service_code: str | None = None,
    domain: str | None = None,
    featured_only: bool = False,
) -> list[dict[str, Any]]:
    items = load_registry()["scenarios"]
    if industry:
        items = [s for s in items if s["industry_slug"] == industry]
    if service_code:
        items = [s for s in items if s["service_code"] == service_code]
    if domain:
        items = [s for s in items if s["domain"] == domain]
    if featured_only:
        items = [s for s in items if s["featured"]]
    return items
