# SAE J1939 Transport Runbook

**Sprint 25 Task 25.3 (BL.P.168).** Operational guide for J1939 telematics
transport wrappers used by AXLE / ICE / ER mining-fleet adapters.

## Scope

APEX consumes J1939 traffic via **CAN-bus capture** at a tenant-supplied
edge gateway. The framework normalizes 29-bit CAN frames into
SPN-addressed values. Throttling enforces sane Bronze ingestion rates.

## Pre-deployment checklist

- [ ] Edge gateway in place between vehicle CAN bus and APEX adapter network
- [ ] Gateway is read-only on the CAN bus (never writes to vehicle electronics)
- [ ] CAN-bus capture rate baseline measured (typical 1000-5000 fps on a haul truck)
- [ ] Bandwidth budget confirmed for raw vs. throttled ingestion
- [ ] Mapping authored against the named PGN set the fleet emits
- [ ] Throttle policy authored per `examples/j1939_haul_truck_mapping.yaml`
- [ ] Each mapping entry carries `classification: operations` (or appropriate)
- [ ] J1939 SPN/PGN registry from Sprint 21 Task 21.8 (`apex-standards-j1939`) referenced

## CAN-bus capture path

```
Vehicle CAN Bus  →  Read-only gateway  →  APEX edge container  →  Bronze
                                          │
                                          └─ J1939Normalizer.normalize()
                                          └─ SignalThrottle.filter()
                                          └─ classification stamp from mapping
```

The edge container holds:

1. Vendor-supplied CAN-to-IP bridge (Vector, Kvaser, Influx, etc.)
2. APEX-protocols `J1939Normalizer` decoding raw frames to `DecodedSignal`
3. APEX-protocols `SignalThrottle` debouncing to Bronze-ingestion rate
4. APEX adapter mapping → annotate `Sample` with classification + canonical entity
5. Push to APEX Bronze workspace via Sprint 14 capacity / Sprint 15 adapter

## Throttling policy

J1939 buses emit some PGNs at 50+ Hz (engine speed PGN 61444 typically
reports every 20 ms). Bronze storage at full bus rate is wasteful; APEX
throttles per-PGN with sane defaults:

| PGN | Default min-interval | Rationale |
|-----|---------------------|-----------|
| 65253 (Engine Hours) | 5000 ms | Slow-changing |
| 61444 (Engine Speed) | 200 ms | 5 Hz max — enough for trend monitoring |
| 61443 (Engine Load) | 1000 ms | Match dashboard refresh |
| 65276 (Fuel Level) | 5000 ms | Slow-changing |
| 65248 (Distance) | 5000 ms | Slow-changing |
| 65257 (Fuel Total) | 5000 ms | Slow-changing |
| 65266 (Fuel Rate) | 1000 ms | Driver-behavior monitoring |

Override per fleet via the mapping config's `throttle.per_pgn_min_interval_ms`
section. **Forensic capture** (post-incident replay, accident
reconstruction) bypasses the throttle by passing raw frames straight
through `J1939Normalizer.normalize()` without `SignalThrottle.filter()`.

## SPN range-data handling

J1939 reserves max-bit-pattern values for "not available" / "not valid"
signals. The normalizer drops these (returns no `DecodedSignal`). For
diagnostic visibility, log dropped frames at `INFO` level and surface
the per-PGN drop-rate in the adapter's health dashboard.

## Adding a new PGN

1. Add the PGN/SPN entry to `apex_standards.j1939` (Sprint 21 catalog)
2. Add the `SPNLayout` entry to `j1939_transport.normalizer.SPN_LAYOUTS`
   (per-byte offsets + scale + offset + units from the SAE J1939
   spreadsheet)
3. Update each affected fleet's mapping YAML
4. Add a smoke-test frame to `datasets.j1939_dataset.J1939_FRAME_CAPTURE`
5. Verify round-trip: raw frame → DecodedSignal → throttled emission

## Cross-OEM validation

The named cross-OEM signal set covers Caterpillar, John Deere, Komatsu,
Volvo CE, and most aftermarket telematics gateways. OEM-specific PGNs
(>= 65500 ranges) require per-OEM extension of the SPN_LAYOUTS table —
see Task 24.5 (J1939 ↔ AEMP 2.0) for the cross-OEM aggregation pattern.

## Common failures

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Empty signal stream after framing | wrong CAN bus speed (250 vs 500 kbps) | verify gateway config |
| `arbitration_id` decoded with `pgn=0` | non-J1939 traffic on the bus | filter at gateway |
| All PGN 61444 samples drop | throttle window too aggressive | raise per-PGN min interval |
| `not_available` flood for PGN 65276 | fuel sensor mis-wired or SPN unsupported on this OEM | escalate to fleet engineering |
