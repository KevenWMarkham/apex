# APEX RAPIDS Integration

This directory makes the APEX repo **RAPIDS-native**. Any team working in APEX
can run `/rapids-init` or `/apex-init` in Claude Code and get archetype-driven
scaffolding for packs, overlays, featurizers, adapters, and Core components.

## What's in here

| Directory | Purpose |
|---|---|
| `archetypes/`  | 7 APEX-aware RAPIDS archetypes (apex-pack-new · apex-pack-extension · etc.) |
| `agents/`       | 9 specialist-agent definitions (VV Author · Threshold Tuner · etc.) |
| `templates/`    | ~20 Jinja2 scaffolding templates (vv-manifest · scenario-chain · etc.) |
| `triage/`        | Adaptive Triage detector that auto-discovers APEX context |
| `workflows/`     | 6-phase workflow definitions (Research → Sustain) per archetype |
| `governance/`    | Phase-gate enforcement · Independence allowlist · ARB submission template |

## How to use

In Claude Code, in the APEX repo:

```
/apex-init             # Auto-detects context · offers APEX archetypes
/apex-new-pack         # Greenfield new industry pack
/apex-new-overlay      # Client-specific overlay
/apex-new-featurizer   # New ML featurizer
/apex-acceptance       # Run pack acceptance test pack
/apex-operate-handoff  # Generate T5 Operate handoff package
```

## Phase gates

Every archetype runs through six RAPIDS phases. Each phase has an APEX governance
gate that must pass before proceeding (see `governance/phase-gates.yaml`):

| Phase | Gate | Blocking? |
|---|---|---|
| Research  | Industry SME sign-off                        | Yes |
| Analysis  | APEX Architecture Council approval            | Yes |
| Plan      | Independence / Legal pre-clearance             | Yes |
| Implement | Pack acceptance test pack (60+ tests green)   | Yes (CI) |
| Deploy    | GSSC Lab acceptance + ConCon ARB conformance  | Yes (CI + ARB) |
| Sustain   | Operate readiness (SLO · FinOps · runbooks)    | Warning only |

## Compatibility

| Component | Version |
|---|---|
| APEX                  | v1.x (any) |
| RAPIDS Core plugin    | >=1.0.0, <2.0.0 |
| Claude Code           | >=2.0 |
| Anthropic API         | Sonnet 4.5+ for most agents · Opus 4.7+ for Constitution Author + Adapter Generator |

## Ownership

| Asset | Owner |
|---|---|
| `.rapids/` content                    | APEX Core team |
| `.claude/agents/apex-*`               | APEX Core team |
| `.claude/commands/apex-*`             | APEX Core team |
| RAPIDS Core plugin compatibility      | RAPIDS Core team (Deloitte central practice) |
| Phase-gate governance                  | APEX Architecture Council |
| Independence allowlist                 | Independence / Legal counsel |

See `APEX-RAPIDS-Integration-Plan.md` (in Downloads) for the full design rationale.
