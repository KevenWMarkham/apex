# apex-iceml

**APEX ICEML** — Industrial & Commercial Equipment canonical entities over SAE J1939 + AEMP 2.0 / ISO 15143-3 + ISO 14224.

Entities:
- `IceEquipment` — commercial vehicle / construction / agricultural unit
- `TelemetryReading` — AEMP 2.0 snapshot + J1939-derived metrics
- `ServiceEvent` — fault / anomaly / warning
- `MaintenanceRecord` — completed / scheduled maintenance
- `FleetMember` — AEMP 2.0 fleet-association edge

Translator: `j1939_to_aemp.py` — round-tripped against J1939 + AEMP shapes.

Design anchor: `Sprint-3-Practice-Schemas-Plan.md` §3.6.
