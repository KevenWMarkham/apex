"""J1939 high-frequency-signal throttler — Sprint 25 §25.3.3.

J1939 buses emit some signals at very high rates (engine speed at 50 Hz,
some PGNs at 100+ Hz). For ingestion into APEX Bronze we throttle to
sane storage / cost limits using a per-(PGN, source_address) min-interval
debounce.

Throttling is **lossy by design** — when a signal arrives within the
throttle window, the older sample is replaced by the newer one rather
than being emitted. Use the un-throttled normalizer for forensic /
diagnostic capture.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Iterator

from apex_protocols.j1939_transport.normalizer import DecodedSignal


@dataclass
class SignalThrottle:
    """Per-(PGN, source_address) min-interval debouncer.

    Drop-and-replace semantics: if a signal arrives < `min_interval_ms`
    after the previous one, it is dropped (the old emission stands).
    Default policy uses ``default_min_interval_ms`` for any (PGN, SA)
    not explicitly listed in ``per_pgn_min_interval_ms``.
    """

    default_min_interval_ms: int = 1000
    """1 Hz default — sane Bronze ingestion rate."""

    per_pgn_min_interval_ms: dict[int, int] = field(default_factory=dict)
    """Override per PGN — typical: high-priority status PGNs at 100ms, position
    PGNs at 500ms, slow-changing diagnostics at 5000ms."""

    _last_emit_ms: dict[tuple[int, int], int] = field(default_factory=dict, init=False)

    def should_emit(self, signal: DecodedSignal) -> bool:
        """True iff ``signal`` should be emitted under the current throttle policy."""
        ts_ms = int(signal.timestamp.timestamp() * 1000)
        key = (signal.pgn, signal.source_address)
        last_ms = self._last_emit_ms.get(key)
        min_interval = self.per_pgn_min_interval_ms.get(
            signal.pgn, self.default_min_interval_ms
        )
        if last_ms is None or (ts_ms - last_ms) >= min_interval:
            self._last_emit_ms[key] = ts_ms
            return True
        return False

    def filter(self, signals: Iterable[DecodedSignal]) -> Iterator[DecodedSignal]:
        """Stream-throttle a sequence of signals."""
        for sig in signals:
            if self.should_emit(sig):
                yield sig

    def reset(self) -> None:
        """Clear all per-(PGN, SA) debounce state. Call between separate captures."""
        self._last_emit_ms.clear()
