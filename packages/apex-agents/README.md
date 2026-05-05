# apex-agents

APEX Agent Catalog — Sprint 16 (BL.P.58–64). 70 anchor agents shipped
across all 7 Practices, framework-validated, CI-ready.

## Coverage

| Practice | Subtask | Anchor agents |
|---|---|---|
| RC | 16.1 | 10 |
| HLS | 16.2 | 10 |
| ER | 16.3 | 10 |
| AXLE | 16.4 | 10 |
| TMT | 16.5 | 10 |
| TH | 16.6 | 10 |
| ICE | 16.7 | 10 |
| **Total** | | **70** |

The Sprint 16 plan calls for 40–50 agents per Practice. The 70 anchors
shipped here cover the highest-leverage agents from the Sprint 16 plan
explicitly named (Sepsis, Clinical Decision Support, etc.) plus
Practice-priority agents from the Sellers Guide deep-dives. The
remaining 30–40 per Practice ship as engagement-specific work using
the same `AgentSpec` manifest template.

## Manifest shape

Every agent declares:

- Identity: `name`, `version`, `practice`, `persona`, `service_codes`
- Model config: `model_tier`, `model_pin`, `prompt_sha`
- Capability boundaries: `tools` (with `write` flag), `forbidden_classifications`
- Governance: `hitl_gates`, `oversight_modes`
- Outcomes: `kpis` with direction + target band
- Provenance: `archetype_id`, `primary_contact`, `description`

The framework validates every manifest against governance rules:
write-tool agents must declare HITL gates; reasoning-tier agents
should declare KPIs; HITL SLA must be positive; agent names follow
`apex.{practice}.agents.{...}` convention.

## Quick Start

```bash
pip install -e packages/apex-core packages/apex-agents

# Stats:
apex agents stats

# List one Practice:
apex agents list --practice rc

# Inspect one agent:
apex agents inspect apex.rc.agents.cold-chain-response

# CI gate — every manifest passes governance:
apex agents validate
```

## Adding a new agent

1. Create `apex_agents/catalogs/{practice}/NN-name.yaml` with the
   AgentSpec fields.
2. `apex agents validate` will fail if the new manifest violates
   governance rules (write tool without HITL, missing KPI on
   reasoning tier, etc.).
3. The new agent automatically appears in `apex agents list` and the
   per-Practice catalog count.

## Cross-reference

- Sellers Guide §6.10 — audit row contract every agent emits
- Sellers Guide §6.11 — Microsoft orchestrator types these agents run on
- Sellers Guide §9.11–§15.9 — per-Practice deep-dives that source the agent inventory
- APEX Orchestrator Sprint 11 — orchestration runtime that invokes these agents
- APEX Orchestrator Sprint 16 — this sprint
