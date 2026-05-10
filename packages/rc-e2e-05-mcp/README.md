# rc-e2e-05-mcp

RC-E2E-05 Store Operations / On-Shelf Availability service-specific MCP tools — Sprint 35.

Three tools the OSA agent fleet calls:

| Tool | Read by | Classification |
|---|---|---|
| `rc_e2e_05.get_oos_event` | The Analyst, The Demand Checker | INTERNAL |
| `rc_e2e_05.get_shelf_gap_assignment_basis` | Workforce Capacity Sizer (quantify) | INTERNAL |
| `rc_e2e_05.commit_task_dispatch` | Act agent (write-back, idempotent) | INTERNAL |

All three tools require `practice:rc` + `service:rc-e2e-05` scope. RC-E2E-05's
domain is INTERNAL — no TRADE_SECRET / PII data.

`commit_task_dispatch` is idempotent on `(dispatch_id, associate_id, task_order)`.
