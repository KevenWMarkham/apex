"""APEX OT protocol adapters — Sprint 25.

Wraps OPC UA, IEC 61850, and SAE J1939 transport so APEX agents speak
canonical entity fields rather than raw OT protocols. Each protocol
adapter is shared across the Sprint 15 SOR adapters that need it.

Public API:

- :class:`Sample`, :class:`AddressNode`, :class:`AddressSpaceMapping` — wire-neutral primitives
- :class:`ProtocolEndpoint`, :class:`ProtocolClient` — runtime contract for tenant-supplied clients
- OPC UA: :func:`parse_nodeset`, :class:`OPCUAConfig`, :class:`OPCUAStubClient`
- IEC 61850: :func:`parse_scd`, :class:`IEC61850StubClient`
- SAE J1939 transport: :class:`CANFrame`, :func:`decode_frame`, :class:`J1939Normalizer`, :class:`SignalThrottle`
"""

from __future__ import annotations

from apex_protocols.base import (
    SUPPORTED_PROTOCOLS,
    AddressNode,
    AddressSpaceError,
    AddressSpaceMapping,
    AuthMode,
    ConfigError,
    ConnectionError as ProtocolConnectionError,
    ProtocolClient,
    ProtocolEndpoint,
    ProtocolError,
    Sample,
)
from apex_protocols.iec61850 import (
    GOOSEControlBlock,
    IEC61850StubClient,
    IED,
    LogicalDevice,
    LogicalNode,
    SCDDocument,
    SVControlBlock,
    parse_scd,
)
from apex_protocols.j1939_transport import (
    CANFrame,
    DecodedSignal,
    J1939Normalizer,
    SignalThrottle,
    decode_frame,
)
from apex_protocols.opcua import (
    NodeSetEntry,
    NodeSetParseError,
    OPCUAConfig,
    OPCUAStubClient,
    build_endpoint,
    parse_nodeset,
)

__all__ = [
    "AddressNode",
    "AddressSpaceError",
    "AddressSpaceMapping",
    "AuthMode",
    "CANFrame",
    "ConfigError",
    "DecodedSignal",
    "GOOSEControlBlock",
    "IEC61850StubClient",
    "IED",
    "J1939Normalizer",
    "LogicalDevice",
    "LogicalNode",
    "NodeSetEntry",
    "NodeSetParseError",
    "OPCUAConfig",
    "OPCUAStubClient",
    "ProtocolClient",
    "ProtocolConnectionError",
    "ProtocolEndpoint",
    "ProtocolError",
    "SCDDocument",
    "SUPPORTED_PROTOCOLS",
    "SVControlBlock",
    "Sample",
    "SignalThrottle",
    "build_endpoint",
    "decode_frame",
    "parse_nodeset",
    "parse_scd",
]

__version__ = "0.1.0"
