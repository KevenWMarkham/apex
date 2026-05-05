# apex-ercml

**APEX ERCML** (Energy & Resources Canonical Markup Language) — Pattern C entities over CIM (IEC 61970 + 61968) + ISO 14224.

## Entities

- `Meter` — AMI / legacy meter (consumes `CimMeter`)
- `MeterReading` — time-series meter value (consumes `CimReading`)
- `GridEvent` — outage / fault / voltage event (consumes `CimEnergyEvent`)
- `Asset` — network asset (consumes `CimAsset`)
- `WorkOrder` — maintenance / inspection (consumes `CimWorkOrder`)
- `ReliabilityRecord` — failure / repair event (consumes ISO 14224 taxonomy)

## Translators

- `translators/cim_to_ercml.py` — CIM → ERCML (Pattern D)
- `translators/ercml_to_cim.py` — ERCML → CIM (inverse; round-trip tested)

## What defers

- WITSML / PRODML O&G-specific entities (Well, Production) — Sprint when O&G agent demand arrives
- ISO 15926 cross-standard translator — BL.P.164 later sprint
- NERC CIP classification Pattern A — ship with first NERC-consuming agent
- IEC 61850 substation adapter — Sprint 15

Design anchor: `Sprint-3-Practice-Schemas-Plan.md` §3.2.
