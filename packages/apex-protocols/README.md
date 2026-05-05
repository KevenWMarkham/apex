# apex-protocols

**Sprint 25 — OT Protocol Adapters.** Wraps OPC UA, IEC 61850, and SAE
J1939 transport so APEX agents speak canonical entity fields rather
than raw OT protocols. Each adapter is shared across the Sprint 15 SOR
adapters that need it, and **classification propagates through the
adapter boundary** per Sprint 25 exit criterion.

## Coverage

| Protocol | Submodule | Used by | Reference workspace |
|----------|-----------|---------|---------------------|
| OPC UA | `opcua/` | ER, AXLE, ICE | `examples/opcua_north_plant_mapping.yaml` |
| IEC 61850 | `iec61850/` | ER (substation automation) | `examples/iec61850_substation_mapping.yaml` |
| SAE J1939 | `j1939_transport/` | AXLE, ICE, ER (mining fleets) | `examples/j1939_haul_truck_mapping.yaml` |

## API

```python
from apex_protocols import (
    # Common base
    Sample, AddressNode, AddressSpaceMapping,
    ProtocolEndpoint, ProtocolError,

    # OPC UA (Task 25.1)
    OPCUAConfig, OPCUAStubClient, parse_nodeset,

    # IEC 61850 (Task 25.2)
    parse_scd, IEC61850StubClient,

    # J1939 transport (Task 25.3)
    CANFrame, decode_frame, J1939Normalizer, SignalThrottle,
)
```

## Classification propagation

Sprint 25 exit criterion: every emitted `Sample` carries its Purview
classification, applied at the adapter boundary from the mapping
config. Bronze loaders propagate it onto the row's Purview label.

```python
mapping = AddressSpaceMapping(protocol="opcua", name="north-plant")
mapping.add(AddressNode(
    node_id="ns=2;s=Line7.OperatorId",
    canonical_entity="ProductionJob",
    canonical_field="operator_id",
    classification="pii",  # ← propagates downstream
))

raw = client.read_one("ns=2;s=Line7.OperatorId")
sample = mapping.annotate(raw)
assert sample.classification == "pii"  # adapter-boundary stamp
```

## Smoke-test datasets

`apex_protocols.datasets` ships synthetic captures sufficient to
exercise each protocol end-to-end without a live OT system:

- `OPCUA_NODESET_XML` + `OPCUA_SNAPSHOT` — 7-node Line 7 reference
- `IEC61850_SCD_XML` + `IEC61850_SNAPSHOT` — 1-IED substation reference
- `J1939_FRAME_CAPTURE` — 9-frame haul-truck capture

Tests in `tests/test_protocols.py` use these datasets to validate
parsers, address-space mappings, throttling, and classification
propagation.

## Runbooks

Per Sprint 25 exit criterion ("each adapter has a reference workspace +
smoke-test dataset + runbook"):

- `runbooks/opcua-runbook.md` — cert renewal, namespace drift, subscription tuning
- `runbooks/iec61850-runbook.md` — SCD discovery, GOOSE/SV scope (metadata only)
- `runbooks/j1939-runbook.md` — CAN-bus capture path, throttling, SPN range-data handling

## Cross-references

- Sprint 13 — Purview classifications (the strings flowing through `Sample.classification`)
- Sprint 14 — capacity blueprints (where Bronze workspaces live)
- Sprint 15 — SOR adapters (which wire these protocol cores into specific SOR ingest paths)
- Sprint 21 — `apex-standards-j1939` (SPN/PGN registry the J1939 wrapper integrates with)
- Sprint 22 — ISO 8000 quality (`Sample.quality` field; provenance scoring per protocol auth mode)
- Sprint 24 Task 24.5 — `apex_translators.cross_standard.j1939_aemp` (AEMP 2.0 aggregation built on top of these signals)
