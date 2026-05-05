"""Default + override partition strategies for Bronze tables."""

from __future__ import annotations

DEFAULT_PARTITION = ("ingest_date",)
"""Default Bronze partition — ingest date. Works for every pattern."""

RECALL_TRACE_PARTITION = ("lot_id",)
"""Recall-style partition — optimises lot-based trace queries."""

EVENT_TIME_PARTITION = ("event_date",)
"""Event-time partition — optimises temporal analytics in Bronze."""


def default_partition_columns(
    *,
    pattern: str = "default",
    recall_trace: bool = False,
    event_time: bool = False,
) -> list[str]:
    """Return the recommended Bronze partition columns.

    Args:
        pattern: Reserved for future pattern-specific overrides.
        recall_trace: Set when the source feeds a recall trace scenario —
            returns ``[lot_id, ingest_date]``.
        event_time: Set when downstream analytics partition on event time —
            returns ``[event_date, ingest_date]``.

    Returns:
        Ordered list of column names suitable for the ``PARTITIONED BY`` clause.
    """
    _ = pattern  # reserved for future use
    if recall_trace:
        return [*RECALL_TRACE_PARTITION, *DEFAULT_PARTITION]
    if event_time:
        return [*EVENT_TIME_PARTITION, *DEFAULT_PARTITION]
    return list(DEFAULT_PARTITION)
