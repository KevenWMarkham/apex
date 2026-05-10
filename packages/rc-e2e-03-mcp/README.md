# rc-e2e-03-mcp

RC-E2E-03 service-specific MCP tools — Sprint 32 items 32.7, 32.8, 32.9.

Exposes three tools the cold-chain + dynamic-markdown agent fleets call:

| Tool | Build-status item | Read by | Classification |
|---|---|---|---|
| `rc_e2e_03.get_excursion_decision_panel` | 32.7 | The Analyst, The Demand Checker | INTERNAL |
| `rc_e2e_03.get_pricing_recommendation_basis` | 32.8 | The Pricer, The Finance Lead | TRADE_SECRET |
| `rc_e2e_03.commit_markdown_decision` | 32.9 | Act agent (write-back) | TRADE_SECRET (input) → INTERNAL (write) |

Each tool delegates reads to `fabric-mcp` against the RC-E2E-03 Gold marts
defined in `services/rc/RC-E2E-03/_gold/marts.py` (Sprint 30.6). Writes go
through the framework write-path (audit row + Purview classification
propagation per Roadmap.md BL.P.86).

All three tools require `practice:rc` + `service:rc-e2e-03` scope on the
caller's identity.
