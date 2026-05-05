# Dashboard Sixth Lane — Redis Health

**Sprint 26 Task 26.10.** Specification for the sixth lane added to the
five-lane orchestration dashboard. Sources data from **Azure Monitor
metrics** for the Redis Enterprise instance (Sprint 26 Task 26.11),
NOT from Redis directly per Task 26.10.2.

## Why a sixth lane

The five existing dashboard lanes (Active Runs, HITL Queue, Audit
Stream, Budget Burn, Operator Activity) cover the primary engagement
surface. Redis health is a **platform-tier concern** that affects every
lane invisibly when the control plane degrades — operators need to see
it without having to dig into Azure portal.

## Data sources

Azure Monitor for Redis Enterprise emits the metrics this lane needs.
The dashboard reads via Azure Monitor REST API; it does NOT open a
direct connection to Redis (that would invert the architecture and
break the private-endpoint-only posture).

| Metric | Azure Monitor name | Lane visualization |
|--------|---------------------|---------------------|
| Reachability | `nodeDisconnections` (inverse) | Status pill: green / amber / red |
| p50 latency for cancel-token reads | `serverLatency` (p50 percentile) | Sparkline, 24-hour rolling |
| p95 latency for cancel-token reads | `serverLatency` (p95 percentile) | Sparkline, 24-hour rolling |
| Cache hit rate (MCP responses) | `cacheHits` / (`cacheHits` + `cacheMisses`) | Gauge, 1-hour rolling |
| Connection count | `connectedClients` | Counter |
| Memory used | `usedMemory` | Bar |
| Throttled commands | `throttledCommands` | Counter (alarm if > 0) |

The cache hit-rate metric distinguishes APEX MCP cache calls from
non-APEX traffic via Redis ACL role tags configured in the
`apex_orchestrator.control_plane.redis_client` ACL initializer.

## Layout

```
┌──────────────────────────────────────────────────┐
│  Redis Health (Sprint 26)                         │
│  ┌──────────────┐  ┌──────────────┐               │
│  │ Reachable    │  │ Hit rate      │               │
│  │  ●  green    │  │  78%   ↑ 2pp  │               │
│  └──────────────┘  └──────────────┘               │
│                                                   │
│  p50 latency (24h)         p95 latency (24h)      │
│  [sparkline 0.4ms]         [sparkline 1.2ms]      │
│                                                   │
│  Connections: 142     Memory: 423MB   Throttled: 0│
└──────────────────────────────────────────────────┘
```

## Alarms

| Alarm | Threshold | Routing |
|-------|-----------|---------|
| Redis unreachable | 1 disconnect event | APEX SRE on-call (5 min) |
| p95 cancel-read latency > 50ms | 5-minute average | APEX SRE on-call (15 min) |
| Cache hit rate < 30% over 1h | rolling | APEX engineering (next business day) |
| Throttled commands > 0 | absolute | APEX SRE on-call (5 min) |
| Memory > 80% | rolling 5-minute | APEX SRE on-call (15 min) |

## Cross-references

- `APEX-CORE.md` §11 — cache governance rules
- `apex_orchestrator.control_plane.redis_client` — emits the
  `cache_hit` / `cache_miss` events that drive the hit-rate gauge
- `apex_orchestrator.mcp.dispatcher` — MCP-tool cache pathway
- `infra/bicep/redis_control_plane.bicep` — Resource that produces
  these metrics
- Sprint 26 Task 26.7.2 — cancel-token writes whose latency this lane
  tracks
