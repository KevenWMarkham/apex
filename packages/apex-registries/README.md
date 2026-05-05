# apex-registries

**Sprint 19 — Master Registries, Playbooks & Appendices.** The
normative reference set (Appendices A-K) for APEX, plus the
per-Practice Wave delivery playbooks and discovery / pre-clearance
artifacts.

## Coverage

| Registry        | Appendix | Source                                                        | Count |
|-----------------|----------|---------------------------------------------------------------|-------|
| KPIs            | C        | harvested from Sprint 16 agents + Sprint 17 services          | 134   |
| Personas        | E        | harvested from Sprint 16 agents + Sprint 17 services + 18 refs | 147   |
| MCP tools       | F        | harvested from Sprint 16 agent ToolBindings                   | 168   |
| Schemas         | A        | hand-authored canonical schema reference                      | 49    |
| Archetypes      | D        | 47 orchestration archetypes (triage, recovery, RCA, etc.)     | 47    |
| Microsoft products | G     | hand-authored Fabric/Foundry/Purview/Defender/Entra/Teams/etc. | 27    |
| Partners        | H        | hand-authored SOR vendors / ISVs / model providers            | 20    |
| Competitive     | K        | Big-4 + tech-led-consult + cloud-native competitive posture   | 10    |
| Exercises       | J        | canonical solutions to Sellers Guide chapter exercises        | 10    |

Plus markdown artifacts:

- `playbooks/{practice}-wave-1-2-3.md` — Wave delivery playbook per Practice (7)
- `discovery/{practice}-discovery-prompts.md` — Discovery prompt templates per Practice (7)
- `preclearance/{technical|legal|compliance}-checklist.md` — Pre-clearance checklists (3)

## CLI

```bash
apex registries stats
apex registries kpi list
apex registries kpi list --practice rc
apex registries persona inspect <persona_id>
apex registries archetype list --family triage
apex registries product list --family fabric
apex registries playbook show rc
apex registries validate
```

## Validation

`validate_registries()` cross-checks every harvested registry against
the live Sprint 16/17/18 catalogs:

- Every KPI named on an agent or service should resolve to a `KpiEntry`
- Every persona named on an agent or service should resolve to a `PersonaEntry`
- Every MCP tool ID bound to an agent should resolve to a `McpToolEntry`

Missing references are emitted as **warnings** (not errors) since
catalogs may legitimately lead the registry; the report is informational.

## Cross-references

- **Sprint 16** agents — supplies KPIs, personas, MCP tools
- **Sprint 17** services — supplies KPIs, personas
- **Sprint 18** references — supplies sponsor personas + canonical schemas
- **Sellers Guide** Appendices A, C, D, E, F, G, H, J, K
