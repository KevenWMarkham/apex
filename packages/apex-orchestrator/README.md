# apex-orchestrator

APEX orchestration runtime (APEX_Design §10 · §9).

## What it ships

- **Primitives** — `SequentialRunner`, `ParallelRunner`, `HierarchicalRunner`, `FeedbackLoopRunner`
- **Gates** — 4 kinds (`ZERO_TOUCH`, `ACK_ONLY`, `HITL`, `ESCALATION`) × 4 variants (`hard`, `soft`, `policy`, `escalation`)
- **Gate resolver** — bump class → gate kind, tenant-override aware
- **Pausable runtime** — hits a HITL gate → returns `PAUSED`; caller `resume()`s once the approver decides
- **Manifest loader** — enforces the three-version rule (`manifest_version` + `policy_version` + `prompt_version`)
- **Tenant tuning** — 2-week observation window with auto-rollback on reversal
- **Integrations stubs** — Teams adaptive-card builder, Copilot Studio skill action stub
- **Archetype catalog** — 47 entries; one concrete Sprint-11 implementation (`anomaly-dispo-hitl`) + 46 stubs
- **Reference orchestration** — RC Cold Chain Response (end-to-end demo)

## How `run()` + `resume()` interact with HITL

Agents execute synchronously until a `HITL` or `ESCALATION` gate fires. The
runtime emits an `OrchestrationResult(status=PAUSED, pending_approvals=[...])`
instead of blocking. The caller persists the pending-approval id (e.g. via
`approvals-mcp`) and later calls `orchestrator.resume(pending_id, decision)`
to continue.
