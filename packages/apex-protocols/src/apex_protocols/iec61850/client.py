"""IEC 61850 stub MMS client — Sprint 25 Task 25.2.2.

Real production deployments wire ``libiec61850`` (or equivalent) into
the :class:`ProtocolClient` contract. The stub here lets the framework
be exercised end-to-end without a live MMS server.

Per Sprint 25 §25.2.3, GOOSE / SV frames are deliberately NOT exposed
through this client — those raw multicast frames stay in the OT domain
and only their *metadata* (control-block names, AppIDs, dataset refs)
surfaces in APEX via the SCD parser.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from apex_protocols.base import (
    ConnectionError as ProtocolConnectionError,
    ProtocolEndpoint,
    Sample,
)


class IEC61850StubClient:
    """In-memory MMS client for tests + smoke-tests."""

    def __init__(self, snapshot: dict[str, Any] | None = None) -> None:
        self._snapshot: dict[str, Any] = dict(snapshot or {})
        self._connected = False

    def connect(self, endpoint: ProtocolEndpoint) -> None:
        if endpoint.protocol != "iec61850":
            raise ProtocolConnectionError(
                f"IEC61850StubClient requires endpoint.protocol='iec61850', got {endpoint.protocol!r}"
            )
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def read_one(self, node_id: str) -> Sample:
        """Read one Functional-Constrained Data Attribute (FCDA path).

        Example node_id: ``IED1/CTRL/XCBR1.Pos.stVal``
        """
        if not self._connected:
            raise ProtocolConnectionError("IEC61850StubClient is not connected")
        if node_id not in self._snapshot:
            raise ProtocolConnectionError(
                f"FCDA path {node_id!r} not in stub snapshot"
            )
        return Sample(
            node_id=node_id,
            value=self._snapshot[node_id],
            timestamp=datetime.now(timezone.utc),
            quality="good",
        )

    def subscribe(self, node_ids: list[str]) -> list[Sample]:
        if not self._connected:
            raise ProtocolConnectionError("IEC61850StubClient is not connected")
        return [self.read_one(nid) for nid in node_ids if nid in self._snapshot]

    def update(self, node_id: str, value: Any) -> None:
        self._snapshot[node_id] = value
