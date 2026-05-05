# OPC UA Adapter Runbook

**Sprint 25 Task 25.1 (BL.P.166).** Operational guide for OPC UA SOR
adapters. Covers cert renewal, address-space discovery, namespace drift,
and high-frequency-signal handling.

## Pre-deployment checklist

- [ ] Server endpoint URL captured (`opc.tcp://server:port`)
- [ ] APEX-side X.509 identity issued (`cert.pem` + `key.pem`)
- [ ] Application URI in cert SAN matches `OPCUAConfig.application_uri`
- [ ] Server's certificate added to `trust_store_path`
- [ ] Server administrator has trusted APEX's cert on their side
- [ ] Security policy is `Basic256Sha256`+ and message security mode is `SignAndEncrypt`
- [ ] NodeSet2 XML exported from server and reviewed
- [ ] Address-space mapping config authored (one entry per NodeId APEX consumes)
- [ ] Each mapping entry carries a Purview classification

## Connecting

```python
from apex_protocols.opcua import OPCUAConfig, build_endpoint
from apex_protocols import OPCUAStubClient  # production: real asyncua client

config = OPCUAConfig(
    server_url="opc.tcp://historian.plant.local:4840",
    application_uri="urn:apex:adapter:axle:north-plant",
    auth_mode=AuthMode.CERTIFICATE,
    cert_path="/etc/apex/opcua/cert.pem",
    key_path="/etc/apex/opcua/key.pem",
    trust_store_path="/etc/apex/opcua/trust",
    namespace_uris=["http://example.com/Plant"],
)
endpoint = build_endpoint(config)
client.connect(endpoint)
```

## Address-space discovery

1. **Export NodeSet2.xml** from the server's UA Configuration tool
2. **Parse it** with `apex_protocols.opcua.parse_nodeset(xml_text)`
3. **Walk the result** to identify NodeIds an adapter mapping should reference
4. **Author** `examples/opcua_*_mapping.yaml` (one entry per node)
5. **Verify** at boot time that every mapping NodeId exists in the NodeSet

## Subscription tuning

OPC UA exposes per-monitored-item `samplingInterval` and per-subscription
`publishingInterval` + `queueSize`. Sane defaults:

- `samplingInterval` = `node.sampling_hint_ms` from the mapping (typical 250-1000 ms)
- `publishingInterval` = 500 ms (50% of the slowest sampled-item interval)
- `queueSize` = 10 (so a brief network glitch doesn't lose samples)

For high-frequency nodes (vibration RMS, current draw on rotating
equipment), set `samplingInterval` >= 250 ms and let the SOR adapter's
own deadband filter drop unchanged values upstream.

## Namespace drift

OPC UA NamespaceArray indices are **server-assigned** and may shift
across server restarts / firmware upgrades. APEX adapters must:

1. Pin to namespace **URIs** (the strings) at config time
2. Resolve URIs to per-session **indices** at connect time
3. Translate every cached NodeId from `ns=N;...` to the session's
   equivalent before issuing reads / subscribes
4. **Fail fast** if a configured namespace URI is missing from the
   server's NamespaceArray

The `OPCUAConfig.namespace_uris` list captures the authoritative URI
set; the framework's URI-to-index resolver runs at every connect.

## Cert renewal

X.509 certs typically expire on a 1- or 2-year cadence. Operations:

1. Generate the new APEX cert >= 30 days before old-cert expiry
2. Add the new cert to the server's trust store (server admin)
3. Update `OPCUAConfig.cert_path` + `key_path` in the tenant workspace
4. **Restart** the adapter; it will re-authenticate with the new cert
5. After 7 days of clean operation, remove the old cert from the
   server's trust store

The `is_production_grade()` helper sanity-checks at boot that the
configured cert files exist on disk.

## Classification propagation

Per Sprint 25 exit criterion, every emitted `Sample` carries its
classification. The adapter's `AddressSpaceMapping.annotate()` applies
the classification from the mapping config; the Bronze loader propagates
it onto the row's Purview label. **Verify at deployment** that every
mapping entry has a non-empty `classification` field.

## Common failures

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| `ConnectionError: certificate not trusted` | server-side trust store missing APEX cert | server admin imports new cert |
| `ConnectionError: BadIdentityTokenInvalid` | cert SAN doesn't match application URI | re-issue cert with correct SAN |
| Empty subscriptions on otherwise-healthy server | wrong namespace index after upgrade | restart adapter — URI re-resolution will re-bind |
| All samples `quality: bad` | server data-source unhealthy | escalate to OT team — APEX cannot diagnose |
