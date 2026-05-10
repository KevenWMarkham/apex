# rc-e2e-07-mcp

RC-E2E-07 Returns & Refund Integrity service-specific MCP tools — Sprint 37.

Three tools the returns-fraud agent fleet calls:

| Tool | Read by | Classification |
|---|---|---|
| `rc_e2e_07.get_return_event` | The Analyst | PII (tokenised) |
| `rc_e2e_07.get_fraud_score_basis` | The Fraud Specialist + Loss Quantifier | PII (tokenised) + TRADE_SECRET |
| `rc_e2e_07.commit_hold_decision` | Act agent (write-back, idempotent) | TRADE_SECRET |

All three tools require `practice:rc` + `service:rc-e2e-07` scope. Tier-3 PII
fields stay tokenised on read; bulk-detokenise via `tokenizer-mcp` is
gated by Decide's adaptive-HITL escalate path (`fraud_score >= 0.7` OR
`ring_indicator == true`) per Deployment Guide §5.2.2.

`commit_hold_decision` is idempotent on `decision_id`.
