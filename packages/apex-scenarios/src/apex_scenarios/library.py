"""Scenario library loader and indexer.

Loads ``docs/scenarios/_catalog/scenario-library.json`` and the featured
chains catalog into typed Pydantic models, indexed by Practice and by
service code.

The on-disk JSON uses the legacy compact shape; this module materializes
the extended :class:`Scenario` model and stamps the practice on each row.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from apex_scenarios.models import (
    PRACTICE_CODES,
    FeaturedChain,
    Scenario,
    ScenarioCompact,
    compact_to_extended,
)


# ---------------------------------------------------------------------------
# Default repository-relative paths
# ---------------------------------------------------------------------------

DEFAULT_LIBRARY_PATH = Path("docs/scenarios/_catalog/scenario-library.json")
DEFAULT_FEATURED_PATH = Path("docs/scenarios/_catalog/featured-chains.json")


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------


def load_scenario_library(path: str | Path = DEFAULT_LIBRARY_PATH) -> list[Scenario]:
    """Load the scenario library and return all 723 rows as :class:`Scenario`.

    The JSON is keyed by practice (RC, HLS, ER, AXLE, TMT, TH, ICE);
    each value is a list of compact scenarios. The loader materializes
    every row, stamps ``practice`` from the dict key, and merges into
    one flat list ready for filtering / validation.
    """
    p = Path(path)
    with p.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)

    if not isinstance(raw, dict):
        raise ValueError(
            f"{path}: expected mapping keyed by practice, got {type(raw).__name__}"
        )

    scenarios: list[Scenario] = []
    for practice, rows in raw.items():
        if practice.upper() not in PRACTICE_CODES:
            raise ValueError(
                f"{path}: unknown practice key {practice!r}. Allowed: {PRACTICE_CODES}"
            )
        if not isinstance(rows, list):
            raise ValueError(
                f"{path}: practice {practice!r} value must be a list, got {type(rows).__name__}"
            )
        for i, row in enumerate(rows):
            try:
                # Tolerate either compact or extended shape on disk.
                if "t" in row and "s" in row:
                    compact = ScenarioCompact(**row)
                    scenarios.append(compact_to_extended(compact, practice=practice))
                else:
                    scenarios.append(Scenario(practice=practice, **row))
            except Exception as exc:  # noqa: BLE001
                raise ValueError(
                    f"{path}: practice {practice!r} row #{i}: {exc}"
                ) from exc

    return scenarios


def load_featured_chains(path: str | Path = DEFAULT_FEATURED_PATH) -> list[FeaturedChain]:
    """Load the featured-chains catalog as :class:`FeaturedChain` rows."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)
    if not isinstance(raw, list):
        raise ValueError(
            f"{path}: expected JSON array, got {type(raw).__name__}"
        )
    return [FeaturedChain.model_validate(row) for row in raw]


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------


class ScenarioIndex:
    """In-memory index over the scenario library.

    Provides O(1) lookups by service code, by practice, and by KPI
    pattern. Read-only after construction.
    """

    def __init__(self, scenarios: Iterable[Scenario]) -> None:
        self._all: list[Scenario] = list(scenarios)
        self._by_practice: dict[str, list[Scenario]] = {p: [] for p in PRACTICE_CODES}
        self._by_service: dict[str, list[Scenario]] = {}

        for s in self._all:
            if s.practice:
                self._by_practice[s.practice].append(s)
            if s.service_code:
                self._by_service.setdefault(s.service_code, []).append(s)

    @property
    def all(self) -> list[Scenario]:
        return list(self._all)

    @property
    def total(self) -> int:
        return len(self._all)

    def by_practice(self, practice: str) -> list[Scenario]:
        return list(self._by_practice.get(practice.upper(), []))

    def by_service(self, service_code: str) -> list[Scenario]:
        return list(self._by_service.get(service_code, []))

    def practice_counts(self) -> dict[str, int]:
        return {p: len(self._by_practice[p]) for p in PRACTICE_CODES}

    def service_codes(self) -> set[str]:
        return set(self._by_service.keys())

    def with_full_wave_data(self) -> list[Scenario]:
        return [s for s in self._all if s.has_full_wave_data()]

    def missing_wave_data(self) -> list[Scenario]:
        return [s for s in self._all if not s.has_full_wave_data()]

    def filter(
        self,
        *,
        practice: str | None = None,
        service_code: str | None = None,
        title_contains: str | None = None,
    ) -> list[Scenario]:
        """Return scenarios matching every supplied filter."""
        results = self._all
        if practice is not None:
            results = [s for s in results if s.practice == practice.upper()]
        if service_code is not None:
            results = [s for s in results if s.service_code == service_code]
        if title_contains is not None:
            needle = title_contains.lower()
            results = [s for s in results if needle in s.title.lower()]
        return results


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def write_extended_library(
    scenarios: Iterable[Scenario],
    path: str | Path,
) -> None:
    """Write scenarios back to disk in the extended v2 JSON shape.

    The output is keyed by practice and preserves all extended fields.
    Used by Task 28.7.1 master-catalog publication and any future
    migration that promotes the on-disk format to v2.
    """
    by_practice: dict[str, list[dict[str, Any]]] = {p: [] for p in PRACTICE_CODES}
    for s in scenarios:
        practice = s.practice or "RC"  # default if missing
        if practice not in by_practice:
            raise ValueError(f"Unknown practice {practice!r} on scenario {s.title!r}")
        by_practice[practice].append(s.model_dump(exclude_none=False, mode="json"))

    Path(path).write_text(
        json.dumps(by_practice, indent=2, sort_keys=False, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
