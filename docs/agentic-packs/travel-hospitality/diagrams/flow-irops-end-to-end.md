# IROPS Recovery — End-to-End Flow

> American Airlines disruption signal → Home Flight Concierge agent → preferred alternate routing submitted back to AA via MCP, with HITL gate. The wedge event for the entire travel pack.

```mermaid
flowchart TD
    AA[("American Airlines<br/>IROPS feed<br/>(AA1234 cancelled)")]
    AA -->|raw vendor JSON| BRONZE[("bronze.tmt_hom.<br/>airline_disruption")]

    BRONZE -->|tokenise + envelope| SILVER[("Silver:<br/>DisruptionEvent<br/>+ segment status")]
    SILVER -->|context + state| GOLD[("gold.v_tmt_hom_<br/>disruption_inflight")]

    GOLD -->|MCP read| AGENT[("apex.tmt.agents.<br/>home-flight-concierge")]
    CAL[("Household calendar<br/>kid's recital tomorrow PM")] --> AGENT
    PREF[("Traveler preferences<br/>+ loyalty AAdvantage<br/>+ companion priorities")] --> AGENT
    EXPEDIA[("Expedia partner search<br/>Delta DL1234 returned")] --> AGENT

    AGENT -->|proposed rebook| HITL{"HITL gate<br/>fare diff > $300?"}
    HITL -->|approve| WRITE[("apex.tmt.mcp.aa.<br/>submit_rebook")]
    HITL -->|under threshold| WRITE
    WRITE -->|confirmation| PARTNER[("AA fulfils rebook<br/>DL1234 confirmed")]
    PARTNER -->|update| VAULT[("Vault:<br/>Booking + ItinerarySegment<br/>updated")]

    AGENT -.->|every step| AUDIT[("agent_run +<br/>agent_action +<br/>view_definition_sha")]

    style AA fill:#fff,stroke:#999
    style BRONZE fill:#fff7e6,stroke:#d97706
    style SILVER fill:#e6f4ea,stroke:#16a34a
    style GOLD fill:#e8eaf6,stroke:#4f46e5
    style AGENT fill:#f3e8ff,stroke:#8b5cf6
    style WRITE fill:#fee2e2,stroke:#dc2626
    style AUDIT fill:#f1f5f9,stroke:#64748b
```

## Signal contributions

| Source | What it tells the agent | Where it shows up |
|---|---|---|
| AA disruption feed | Flight cancelled, alt-routings offered by AA | `DisruptionEvent`, `ItinerarySegment.status=disrupted` |
| Household calendar | Kid's recital tomorrow 4 PM — hard constraint | Context passed to agent |
| Traveler preferences | AAdvantage Executive Platinum status, companion in row 11 | `LoyaltyAccount`, `Person` preferences |
| Expedia partner search | Delta DL 1234 returning 4:15 PM with 2 First Class seats | Partner-side MCP search result |

## Why this is the wedge

- **Emotional stakes high** — missed family event, kid's recital
- **Visible value** — customer remembers this rebook forever
- **Hard for competitors** — no airline-direct app can recommend Delta when you're stranded on AA
- **Cheap to deliver** — once the agent is built, marginal cost per IROPS = inference + partner-API quota

A single successful IROPS recovery in year 1 of subscription typically produces a customer who refers 2–3 other households.
