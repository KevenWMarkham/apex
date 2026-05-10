# rc-e2e-04-mcp

RC-E2E-04 Customer Lifecycle & Loyalty service-specific MCP tools — Sprint 34.

Three tools the loyalty-churn agent fleet calls:

| Tool | Read by | Classification |
|---|---|---|
| `rc_e2e_04.get_loyalty_churn_cohort` | The Analyst, The Demand Checker | PII (tokenised) |
| `rc_e2e_04.get_winback_offer_basis` | The Finance Lead | TRADE_SECRET |
| `rc_e2e_04.commit_winback_offer` | Act agent (write-back) | TRADE_SECRET (input) → INTERNAL (write) |

All three tools require `practice:rc` + `service:rc-e2e-04` scope. Tier-3 PII
fields (raw email, phone, member number) are tokenised on read; the
Decide agent's HITL approval is the ONLY path to bulk-detokenise per
Deployment Guide §5.2.2 just-in-time PII unlock pattern.

`commit_winback_offer` is idempotent on `campaign_natural`.
