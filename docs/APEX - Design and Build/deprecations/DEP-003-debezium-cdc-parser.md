# DEP-003 · Custom Debezium CDC parser for Bronze → Eventstream DeltaFlow

**Status:** Deprecated
**Date:** 2026-05-09
**Supersedes:** Services Guide §5 (Real-Time Hub Pattern) custom CDC handling

## What APEX was building

Custom CDC parsing logic in Bronze ingest notebooks to flatten Debezium's deeply-nested JSON change events into tabular rows aligned with the source database schema. Roadmap.md BL.P.21 (Bronze Eventstream) included this work; estimated as moderate complexity per service code that mirrored from a relational SOR.

## What Microsoft shipped

In **March 2026**, Fabric Eventstream shipped **DeltaFlow transformation** (preview):

- [DeltaFlow transformation](https://learn.microsoft.com/fabric/real-time-intelligence/event-streams/delta-flow-output-transformation)

> *"DeltaFlow is a capability in Fabric Eventstream that transforms raw Change Data Capture (CDC) events into a flattened, analytics-ready format. Instead of working with deeply nested Debezium JSON payloads, DeltaFlow produces tabular rows that closely mirror the structure of the source database tables, enriched with metadata columns that describe each change."*

## Migration path

1. Drop the custom CDC parser from APEX-M's Bronze landing notebooks. Replace with DeltaFlow as the Eventstream output transformation when Bronze source is a Debezium / RDS / PostgreSQL Mirroring stream.
2. The output is already analytics-ready tabular Bronze; no notebook code needed.
3. Updated Services Guide §5 (Real-Time Hub) refers to DeltaFlow as the canonical CDC handling pattern.

## Independence implications

None. DeltaFlow is part of the client's existing Fabric Eventstream capacity.

## What stays

Custom CDC parsing for **non-Debezium / non-relational** sources (e.g., custom IoT telemetry formats, EDI X12 streams) stays bespoke per BL.P.155–158 backlog items.
