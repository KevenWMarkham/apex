# IEC 61850 Adapter Runbook

**Sprint 25 Task 25.2 (BL.P.167).** Operational guide for IEC 61850 SOR
adapters used by the ER (utility) Practice.

## Scope

APEX speaks **MMS** (Manufacturing Message Specification) for read /
report / control operations. Per Sprint 25 §25.2.3, **GOOSE / Sampled-
Value frames stay in the OT domain** — APEX captures only their
metadata (control-block names, AppIDs, dataset references) for asset-
inventory purposes. Subscribing to live GOOSE / SV is explicitly out of
scope.

## Pre-deployment checklist

- [ ] SCD file exported from the substation engineering tool (CET, IEC-61850-Engineer, etc.)
- [ ] SCD file parsed with `apex_protocols.iec61850.parse_scd()` to confirm well-formed
- [ ] IED list reviewed; APEX adapter scoped to a specific IED+LDevice subset
- [ ] FCDA-path mapping authored (one entry per data attribute APEX consumes)
- [ ] Each mapping entry carries `classification: critical-infrastructure` (or stronger) per Sprint 13
- [ ] MMS server (typically the IED itself) reachable from APEX adapter network
- [ ] Adapter authenticated to the IED — usually X.509 client cert OR username + IEC 62351 secure association
- [ ] Operations team aware of the new MMS client + has approved the subscribe load

## Connecting

```python
from apex_protocols.base import ProtocolEndpoint, AuthMode
from apex_protocols import IEC61850StubClient  # production: real libiec61850 client

endpoint = ProtocolEndpoint(
    protocol="iec61850",
    url="mms://substation-relay:102",
    auth_mode=AuthMode.CERTIFICATE,
    cert_path="/etc/apex/iec61850/cert.pem",
    key_path="/etc/apex/iec61850/key.pem",
    trust_store_path="/etc/apex/iec61850/trust",
)
client.connect(endpoint)
```

## SCD discovery

1. **Export SCD** from the substation engineering tool (vendor-specific)
2. **Parse** with `parse_scd(xml_text)` → :class:`SCDDocument`
3. Walk `doc.ieds[*].logical_devices[*].logical_nodes` to enumerate
   FCDA paths
4. Author `examples/iec61850_*_mapping.yaml` with one entry per FCDA
5. **Verify** every mapped FCDA path resolves to an LN+DO+DA in the SCD

## GOOSE / SV awareness (metadata only)

The SCD parser surfaces every `GSEControl` and `SampledValueControl`
block. APEX uses these for:

- Asset-inventory views (which IEDs publish what)
- Topology validation (does the substation's GOOSE wiring match design?)
- Sprint 11 PSPS-decision audit context (which protection schemes are active?)

APEX never subscribes to GOOSE / SV multicast directly. If a tenant
needs GOOSE-derived signals in APEX, they must:

1. Configure their substation gateway to *consume* GOOSE and re-publish
   the derived values via MMS report-control blocks
2. APEX subscribes to the resulting MMS reports (data-set push)

This isolation keeps the substation's deterministic OT timing from
APEX's IT timing requirements.

## Subscription tuning

MMS reports support buffered / unbuffered modes and `intgPd`
(integration period). For APEX:

- Use **buffered** report-control blocks for any value the analyst
  can't lose (breaker positions, fault-event counts)
- Use **unbuffered** for high-volume measurements where freshness
  beats completeness (live phasors in a dashboard)
- Configure `intgPd` >= 250 ms for measurement-LN data; downsample at
  the gateway rather than at APEX

## Cert renewal

Same rotation pattern as OPC UA — see `opcua-runbook.md`. IEC 62351-3
mandates X.509 + TLS for MMS over IP; rotate certs on a 1-2-year cadence
and double-trust the new cert for a 7-day overlap window.

## Common failures

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| `ConnectionError: invalid VMD` | wrong IED domain name in the URL | verify IED logical device against SCD |
| `quality: bad` on otherwise-healthy values | source LN's mod blocked or substituted | escalate to OT team |
| Missing FCDA paths | SCD drift after firmware upgrade | re-export SCD; re-parse; reconcile mapping |
| GSEControl entries missing in SCD parse | non-standard SCL extensions | normalize SCD via vendor tool first |
