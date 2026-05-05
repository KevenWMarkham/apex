"""OPC UA adapter core — Sprint 25 Task 25.1 (BL.P.166).

Address-space discovery (NodeSet XML parser), node-browse + subscribe
client interface, address-space → canonical-entity mapping, TLS + X.509
certificate authentication.

Shared across ER / AXLE / ICE SOR adapters per Sprint 25 §25.1.3.
"""

from apex_protocols.opcua.client import OPCUAStubClient
from apex_protocols.opcua.config import OPCUAConfig, build_endpoint
from apex_protocols.opcua.nodeset import (
    NodeSetEntry,
    NodeSetParseError,
    parse_nodeset,
)

__all__ = [
    "NodeSetEntry",
    "NodeSetParseError",
    "OPCUAConfig",
    "OPCUAStubClient",
    "build_endpoint",
    "parse_nodeset",
]
