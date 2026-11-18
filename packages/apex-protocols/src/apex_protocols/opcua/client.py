"""OPC UA stub client — reads from synthetic dataset for tests + smoke-tests.

Real production deployments wire ``asyncua`` (or equivalent) into the
:class:`ProtocolClient` contract. The stub here lets the framework be
exercised end-to-end without a live OPC UA server.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from apex_protocols.base import (
    ConnectionError as ProtocolConnectionError,
)
from apex_protocols.base import (
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
        """Initialise a disconnected client serving a copy of ``snapshot``."""
        self._snapshot: dict[str, Any] = dict(snapshot or {})
        self._connected = False
        self._endpoint: ProtocolEndpoint | None = None

    def connect(self, endpoint: ProtocolEndpoint) -> None:
        """Record ``endpoint`` and mark the client connected.

        Raises:
            ProtocolConnectionError: If ``endpoint.protocol`` is not ``opcua``.
        """
        if endpoint.protocol != "opcua":
            raise ProtocolConnectionError(
                f"OPCUAStubClient requires endpoint.protocol='opcua', got {endpoint.protocol!r}"
            )
        self._endpoint = endpoint
        self._connected = True

    def disconnect(self) -> None:
        """Mark the client disconnected."""
        self._connected = False

    def is_connected(self) -> bool:
        """Return True while the client is connected."""
        return self._connected

    def read_one(self, node_id: str) -> Sample:
        """Return the snapshot value for ``node_id`` as a good-quality sample stamped now.

        Raises:
            ProtocolConnectionError: If not connected or ``node_id`` is not in the snapshot.
        """
        if not self._connected:
            raise ProtocolConnectionError("OPCUAStubClient is not connected")
        if node_id not in self._snapshot:
            raise ProtocolConnectionError(f"NodeId {node_id!r} not in stub snapshot")
        return Sample(
            node_id=node_id,
            value=self._snapshot[node_id],
            timestamp=datetime.now(UTC),
            quality="good",
        )

    def subscribe(self, node_ids: list[str]) -> list[Sample]:
        """Return samples for the requested node ids, silently skipping unknown ones.

        Raises:
            ProtocolConnectionError: If the client is not connected.
        """
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
