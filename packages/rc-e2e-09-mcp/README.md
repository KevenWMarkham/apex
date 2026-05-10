# rc-e2e-09-mcp

RC-E2E-09 Product Tracking (FSMA 204) service-specific MCP tools — Sprint 39.

**Cross-service:** RC-E2E-03's classify agent (The Demand Checker) and
RC-E2E-07's assess agent (The Analyst) declare `rc_e2e_09.get_lot_provenance`
as a tool. This package ships the production implementation.

| Tool | Read by | Classification |
|---|---|---|
| `rc_e2e_09.get_recall_panel` | The Analyst (assess) + The Compliance Specialist (classify) | INTERNAL |
| `rc_e2e_09.get_lot_provenance` | RC-E2E-03 + RC-E2E-07 (cross-service consumers) | INTERNAL |
| `rc_e2e_09.commit_lot_event` | The Briefer (learn) — sole writer of SCML.Lot | INTERNAL |

All three tools require `practice:rc` + `service:rc-e2e-09` scope EXCEPT
`get_lot_provenance` which also accepts `service:rc-e2e-03` and
`service:rc-e2e-07` for cross-service reads (per the SCML.Lot ownership
boundary documented in Sprint 39.4).

## SCML.Lot ownership boundary (Sprint 39.4)

**RC-E2E-09 is the sole writer of `SCML.Lot`.** Other RC services read lot
provenance via `rc_e2e_09.get_lot_provenance` only — they MUST NOT write
to `SCML.Lot` directly. The boundary is enforced at the MCP contract layer:

- `commit_lot_event` requires `practice:rc` + `service:rc-e2e-09` (RC-E2E-09
  identity only).
- `get_lot_provenance` is the only read path that accepts cross-service
  scopes.

Sprint 39's `commit_lot_event` is idempotent on `(decision_id, lot_key,
event_kind)`. The downstream invalidation signal (returned in the response)
flows to RC-E2E-03 + RC-E2E-07 via Eventstream so their cached Gold-mart
joins refresh on the next read.
