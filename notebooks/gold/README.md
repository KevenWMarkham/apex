# APEX Gold materialisation templates

Three parallel paths to serving Gold (APEX_Design §6.5):

| Template | Target | When |
|----------|--------|------|
| `direct_lake.py` | Power BI semantic model (Direct Lake) | Sub-second interactive queries; agent Copilot-grounded views |
| `warehouse_views.py` | Fabric Warehouse T-SQL views | MCP-served structured reads; batch-hourly refresh |
| `kql_functions.py` | Eventhouse KQL functions | Real-time agent queries over streaming Silver |

## Shared dependency

All three consume measure definitions from `apex_medallion.gold` and entity
classes from the Practice packages (e.g. `apex_scml`, `apex_hlscml`).

## Refresh orchestration

Not in Sprint 6 — lands in Sprint 11 (Orchestration) alongside Data Activator
rules and per-stage gate decisions.

## Why notebooks here

Identical rationale to `notebooks/bronze/` and `notebooks/silver/` — these
run in Fabric's PySpark / KQL runtime.
