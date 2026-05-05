"""Common base types for APEX OT protocol adapters — Sprint 25.

Each protocol submodule (``opcua``, ``iec61850``, ``j1939_transport``)
defines:

- A :class:`ProtocolEndpoint` (URL / port / certificates / authentication mode)
- An :class:`AddressSpaceMapping` (per-protocol node id → canonical entity field)
- A :class:`Sample` (the protocol-neutral observation: value + timestamp +
  source node id + classification)

Sprint 25 exit criterion specifies "classification propagates through the
adapter boundary" — :class:`Sample` carries its Purview classification so
downstream Bronze→Silver loaders can apply DLP rules consistently.

The framework here parses configuration + smoke-test datasets and
normalizes; *raw wire I/O* (OPC UA secure channel, IEC 61850 MMS,
CAN-bus capture) happens at runtime via tenant-specific clients that
implement the :class:`ProtocolClient` protocol.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Authentication modes
# ---------------------------------------------------------------------------


class AuthMode(StrEnum):
    """Authentication modes supported by APEX OT adapters."""

    ANONYMOUS = "anonymous"
    """No authentication — only used for smoke-test datasets."""

    USERNAME_PASSWORD = "username_password"
    """Username + password — discouraged for production OT."""

    CERTIFICATE = "certificate"
    """X.509 certificate-based — required for production OPC UA / IEC 61850
    per Sprint 25 §25.1.4."""

    KERBEROS = "kerberos"
    """Kerberos / Active Directory integration — common in industrial
    Windows-based OT estates."""


# ---------------------------------------------------------------------------
# Sample — the wire-neutral observation
# ---------------------------------------------------------------------------


@dataclass
class Sample:
    """One observation read from an OT protocol.

    Sprint 25 exit criterion — every sample carries its classification so
    downstream Bronze loaders apply Purview labels consistently.
    """

    node_id: str
    """Protocol-specific node identifier (NodeId for OPC UA, FCDA path for IEC
    61850, SPN-addressed PGN for J1939)."""

    value: float | int | str | bool | None
    units: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    quality: str = "good"
    """Wire-protocol quality flag: ``good`` / ``uncertain`` / ``bad`` /
    ``not_connected``. Adapters normalize per-protocol quality codes
    (OPC UA StatusCode, IEC 61850 q.validity, J1939 SPN range data) into
    this string."""

    classification: str = ""
    """Purview classification applied at the adapter boundary
    (`operations` / `pii` / `phi` / `payment-card` / `intellectual-property`
    / `critical-infrastructure` / `controlled-unclassified`).

    The adapter assigns this from its address-space mapping config; the
    Bronze loader propagates it onto the row's Purview label. Sprint 13
    governance + Sprint 22 ISO 8000 quality both depend on this field."""

    canonical_entity: str = ""
    """Target canonical schema entity (e.g., `EquipmentHealth`, `Substation`,
    `VehicleEvent`). Pulled from the address-space mapping."""

    canonical_field: str = ""
    """Target canonical-schema field name."""

    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Address-space mapping
# ---------------------------------------------------------------------------


@dataclass
class AddressNode:
    """One node in the protocol address-space mapping.

    Maps a protocol-specific node identifier to a canonical entity field
    + classification + units.
    """

    node_id: str
    """Protocol node id (NodeId / FCDA path / PGN-SPN tuple)."""

    canonical_entity: str
    canonical_field: str
    classification: str = "operations"
    units: str = ""
    description: str = ""
    sampling_hint_ms: int = 1000
    """Suggested sample interval for this node when subscribed."""


@dataclass
class AddressSpaceMapping:
    """Catalog of address-space → canonical-entity mappings for one tenant."""

    protocol: str
    """One of ``opcua``, ``iec61850``, ``j1939``."""

    name: str
    """Mapping label (e.g., ``"north-plant-mes-line-7"``)."""

    nodes: dict[str, AddressNode] = field(default_factory=dict)
    """Keyed by ``node_id``."""

    def add(self, node: AddressNode) -> None:
        self.nodes[node.node_id] = node

    def lookup(self, node_id: str) -> AddressNode | None:
        return self.nodes.get(node_id)

    def annotate(self, sample: Sample) -> Sample:
        """Apply mapping metadata to a wire-side :class:`Sample`.

        The wire-side sample arrives with bare `node_id` + `value` +
        `timestamp` + raw quality. This method enriches it with
        canonical_entity, canonical_field, classification, and units —
        Sprint 25 exit criterion's "classification propagates through the
        adapter boundary."
        """
        node = self.lookup(sample.node_id)
        if node is None:
            # Defensive: leave as-is and stamp `unknown` classification so
            # downstream loaders can quarantine
            sample.classification = sample.classification or "unknown"
            return sample
        sample.canonical_entity = node.canonical_entity
        sample.canonical_field = node.canonical_field
        sample.classification = node.classification
        if node.units and not sample.units:
            sample.units = node.units
        return sample


# ---------------------------------------------------------------------------
# Protocol endpoint + client
# ---------------------------------------------------------------------------


@dataclass
class ProtocolEndpoint:
    """Connection parameters for an OT protocol endpoint."""

    protocol: str
    """One of ``opcua``, ``iec61850``, ``j1939``."""

    url: str = ""
    """E.g., ``opc.tcp://server:4840``, ``mms://relay:102``, ``can://can0``."""

    auth_mode: AuthMode = AuthMode.CERTIFICATE
    cert_path: str = ""
    key_path: str = ""
    trust_store_path: str = ""
    username: str = ""
    """For username-password mode only."""

    timeout_seconds: float = 30.0
    keepalive_seconds: float = 10.0
    metadata: dict[str, Any] = field(default_factory=dict)


class ProtocolClient(Protocol):
    """Wire-protocol client interface that real adapters implement.

    The framework ships *stub* implementations that read from synthetic
    datasets (used in tests + smoke-tests). Production deployments wire
    real clients (asyncua, libiec61850, python-can, etc.) into this
    contract.
    """

    def connect(self, endpoint: ProtocolEndpoint) -> None:
        ...

    def disconnect(self) -> None:
        ...

    def read_one(self, node_id: str) -> Sample:
        ...

    def subscribe(self, node_ids: list[str]) -> "list[Sample]":
        ...


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class ProtocolError(Exception):
    """Base for OT protocol adapter failures."""


class ConfigError(ProtocolError):
    """Raised when adapter configuration (mapping / endpoint) is malformed."""


class ConnectionError(ProtocolError):
    """Raised when a protocol client cannot connect (or stub I/O fails)."""


class AddressSpaceError(ProtocolError):
    """Raised when an address-space lookup fails or the parsed source file
    is structurally invalid."""


SUPPORTED_PROTOCOLS: tuple[str, ...] = ("opcua", "iec61850", "j1939")
