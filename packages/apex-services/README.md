# apex-services

APEX Service Catalog — Sprint 17 (BL.P.110–116). 61 productized service
manifests across all 7 Practices linking agents, archetypes, schemas,
KPIs, SLOs, and commercial envelopes.

## Coverage

| Practice | Subtask | Services |
|---|---|---|
| RC | 17.1 | 13 |
| HLS | 17.2 | 8 |
| ER | 17.3 | 8 |
| AXLE | 17.4 | 8 |
| TMT | 17.5 | 8 |
| TH | 17.6 | 8 |
| ICE | 17.7 | 8 |
| **Total** | | **61** |

The Sprint 17 plan target of "45 per Practice" includes scenario-derived
services from the Sprint 28 scenario library (723 rows). The 61 anchors
shipped here cover every service named in the Sellers Guide Practice
deep-dives (§9.11 through §15.9).

## ServiceSpec shape

Every service declares:

- Identity: `service_code`, `practice`, `display_name`, `brief`, `description`
- Personas: `primary` + `secondary`
- KPIs: `name`, `direction`, `baseline`, `wave2_target`, `wave3_target`
- SLOs: `name`, `target`, `enforcement` (soft / hard / regulatory)
- Wave envelopes: per Wave 1/2/3 with fee bands and duration
- Commercial: `commercial_model` (fixed_fee / value_share / hybrid) + `value_share_eligible`
- Linkages: `linked_agents`, `linked_archetypes`, `schemas_touched`, `standards`

## CLI

```bash
pip install -e packages/apex-core packages/apex-agents packages/apex-services

apex services stats                          # 61 services across 7 Practices
apex services list                           # full inventory
apex services list --practice rc             # one Practice
apex services list --value-share             # value-share eligible only
apex services inspect RC-E2E-06              # full detail for one service
apex services validate                       # CI gate (cross-references agent catalog)
```

## Validator rules

The validator gates merges with these governance rules:

1. Service code matches canonical regex `{PRACTICE}-{Track}-{NN}`.
2. Service code's practice prefix matches the manifest `practice` field.
3. At least one persona declared.
4. At least one KPI declared.
5. At least one Wave envelope declared.
6. Linked agents (when present) resolve in the agent catalog (Sprint 16).
7. Value-share-eligible services should have a money-direction KPI (warning).

## Cross-reference

- Sellers Guide §2.2A — Wave envelope framework
- Sellers Guide §2.2B — Scenario → Solution → Use Case → Service → Persona → KPI value-delivery chain
- Sellers Guide §2.6 — Value-share commercial option
- Sellers Guide §9.11 through §15.9 — Practice deep-dives that source the service inventory
- APEX Orchestrator Sprint 11 — orchestration runtime for agents-of-services
- APEX Orchestrator Sprint 16 — agent catalog (linked via `linked_agents`)
- APEX Orchestrator Sprint 28 — scenario library validates service codes against this catalog via `apex_services.all_service_codes()`
