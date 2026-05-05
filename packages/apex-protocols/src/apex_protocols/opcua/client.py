"""OPC UA stub client — reads from synthetic dataset for tests + smoke-tests.

Real production deployments wire ``asyncua`` (or equivalent) into the
:class:`ProtocolClient` contract. The stub here lets the framework be
exercised end-to-end without a live OPC UA server.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from apex_protocols.base import (
    ConnectionError as ProtocolConnectionError,
    ProtocolEndpoint,
    Sample,
)


class OPCUAStubClient:
    """In-memory OPC UA client for tests + smoke-tests.

    Constructor takes a ``snapshot`` dict mapping ``node_id`` →
    raw value. ``read_one`` and ``subscribe`` return :class:`Sample`
    instances drawn from that snapshot.
    """

    def __init__(self, snapshot: dict[str, Any] | None = None) -> None:
        self._snapshot: dict[str, Any] = dict(snapshot or {})
        self._connected = False
        self._endpoint: ProtocolEndpoint | None = None

    def connect(self, endpoint: ProtocolEndpoint) -> None:
        if endpoint.protocol != "opcua":
            raise ProtocolConnectionError(
                f"OPCUAStubClient requires endpoint.protocol='opcua', got {endpoint.protocol!r}"
            )
        self._endpoint = endpoint
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def read_one(self, node_id: str) -> Sample:
        if not self._connected:
            raise ProtocolConnectionError("OPCUAStubClient is not connected")
        if node_id not in self._snapshot:
            raise ProtocolConnectionError(
                f"NodeId {node_id!r} not in stub snapshot"
            )
        return Sample(
            node_id=node_id,
            value=self._snapshot[node_id],
            timestamp=datetime.now(timezone.utc),
            quality="good",
        )

    def subscribe(self, node_ids: list[str]) -> list[Sample]:
        if not self._connected:
            raise ProtocolConnectionError("OPCUAStubClient is not connected")
        out: list[Sample] = []
        for nid in node_ids:
            if nid in self._snapshot:
                out.append(self.read_one(nid))
        return out

    def update(self, node_id: str, value: Any) -> None:
        """Test helper — push a new value into the stub snapshot."""
        self._snapshot[node_id] = value
