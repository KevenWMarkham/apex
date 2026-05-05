"""Append-only audit-row store (BL.P.77).

Immutable, append-only, signed-on-seal. The reference implementation keeps
rows in memory; production wires this to a Delta table with WORM policy.
"""

from __future__ import annotations

from typing import Any

from apex_audit.composite import OrchestrationCompositeRow
from apex_audit.row import AuditRow, utc_now
from apex_audit.signing import sign_row, verify_row
from apex_audit.trace import require_trace_id


class AppendOnlyViolationError(Exception):
    """Raised on any attempt to mutate a sealed row."""


class AuditStore:
    """In-memory append-only store for decision and composite rows.

    Rows are sealed on append: ``sealed_at`` + ``signature`` fields are stamped,
    and the resulting dict is kept keyed by ``decision_id`` (or
    ``orchestration_id`` for composites). A trace-index lets auditors walk
    ``trace_id -> all rows`` in append order.
    """

    def __init__(self, *, signing_key: bytes) -> None:
        self._signing_key = signing_key
        self._rows: dict[str, dict[str, Any]] = {}
        self._by_trace: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # Decision rows

    def append(self, row: AuditRow) -> dict[str, Any]:
        """Seal + append a decision audit row.

        Enforces the trace-ID discipline (Section 11.6) and the three-version
        rule (Section 11.7). The sealed dict is returned so callers can
        persist / ship / audit it immediately.
        """
        require_trace_id(row.trace_id)
        if row.decision_id in self._rows:
            raise AppendOnlyViolationError(
                f"decision_id {row.decision_id!r} already sealed; "
                "append-only store refuses overwrite"
            )
        sealed = row.model_copy(update={"sealed_at": utc_now()}).to_dict()
        sealed["signature"] = sign_row(sealed, key=self._signing_key)
        self._rows[row.decision_id] = sealed
        self._by_trace.setdefault(row.trace_id, []).append(row.decision_id)
        return sealed

    def append_composite(
        self, composite: OrchestrationCompositeRow
    ) -> dict[str, Any]:
        """Seal + append an orchestration composite row."""
        require_trace_id(composite.trace_id)
        key = composite.orchestration_id
        if key in self._rows:
            raise AppendOnlyViolationError(
                f"orchestration_id {key!r} already sealed"
            )
        sealed = composite.to_dict()
        sealed["sealed_at"] = utc_now().isoformat()
        sealed["signature"] = sign_row(sealed, key=self._signing_key)
        self._rows[key] = sealed
        self._by_trace.setdefault(composite.trace_id, []).append(key)
        return sealed

    # ------------------------------------------------------------------
    # Reads

    def get(self, row_id: str) -> dict[str, Any]:
        if row_id not in self._rows:
            raise KeyError(f"No row {row_id!r}")
        return self._rows[row_id]

    def by_trace(self, trace_id: str) -> list[dict[str, Any]]:
        """Return every row emitted under ``trace_id`` in append order."""
        return [self._rows[rid] for rid in self._by_trace.get(trace_id, [])]

    def verify(self, row_id: str) -> bool:
        """Recompute + compare the signature for a stored row."""
        return verify_row(self._rows[row_id], key=self._signing_key)

    def __len__(self) -> int:
        return len(self._rows)
