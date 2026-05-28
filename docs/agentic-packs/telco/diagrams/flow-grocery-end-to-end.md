# Grocery Replenishment — End-to-End Flow

> Bronze → Silver → Gold → Agent → Partner → Audit for `TMT-TEL-HOM-01`. The same shape repeats for the other seven sub-agents with different anchor devices and different write-side tools.

```mermaid
flowchart TD
    subgraph Devices[" "]
        FRIDGE[("Smart fridge<br/>camera + temp")]
        PANTRY[("Pantry weight<br/>sensors")]
        TRASH[("Trash barcode<br/>scanner")]
        CAL[("Calendar +<br/>banking signals")]
    end

    Devices -->|raw vendor JSON| BRONZE[("bronze.tmt_hom.<br/>appliance_events<br/>+ purchase_history")]

    BRONZE -->|tokenise + envelope| SILVER1[("Silver:<br/>InventoryReading<br/>PurchaseEvent")]
    SILVER1 -->|SCD2 build| SILVER2[("Silver:<br/>inventory_state<br/>consumption_rate")]

    SILVER2 -->|PySpark<br/>pantry_days_remaining| GOLD[("gold.v_tmt_hom_<br/>pantry_state")]

    GOLD -->|MCP read tool| AGENT[("apex.tmt.agents.<br/>home-grocery-<br/>replenishment")]

    AGENT -->|draft cart| HITL{"HITL gate<br/>cart > $150?"}
    HITL -->|approve| WRITE[("apex.tmt.mcp.<br/>kroger.submit_order")]
    HITL -->|no gate| WRITE
    WRITE -->|order confirmation| PARTNER[("Grocer<br/>fulfilment")]

    AGENT -.->|every step| AUDIT[("agent_run +<br/>agent_action +<br/>view_definition_sha")]

    style Devices fill:#fff,stroke:#999,stroke-dasharray: 3 3
    style BRONZE fill:#fff7e6,stroke:#d97706
    style SILVER1 fill:#e6f4ea,stroke:#16a34a
    style SILVER2 fill:#e6f4ea,stroke:#16a34a
    style GOLD fill:#e8eaf6,stroke:#4f46e5
    style AGENT fill:#f3e8ff,stroke:#8b5cf6
    style WRITE fill:#fee2e2,stroke:#dc2626
    style AUDIT fill:#f1f5f9,stroke:#64748b
```

## Signal contributions

| Source | What it tells the agent | Where it shows up |
|---|---|---|
| Fridge camera | Item-level inventory (visual recognition, expiry stamps) | `InventoryReading.product_upc`, `expires_on` |
| Pantry weight sensors | Continuous quantity decay → consumption rate | `consumption_rate`, `avg_daily_consumption` |
| Trash barcode scanner | "We threw this out → reorder" trigger | `InventoryReading` with `quantity = 0` |
| Purchase history | Anchor SKU + brand preference | `PurchaseEvent` → `consumption_rate` calibration |
| Calendar | Demand-side anomaly ("dinner party Saturday") | Context passed to the agent at run time |
| Banking / budget | Spending guardrail | Context, applied at HITL gate threshold logic |

## Audit chain

Every step writes to `agent_run` / `agent_action` with:

- `run_id` linking back to the parent orchestrator run (if invoked via `TMT-TEL-HOM-99`)
- `view_definition_sha` proving which Gold-view DDL produced the inputs
- `tools_called.result_hash` proving what the partner API returned
- `state` transitions: `proposed` → `user-approved` (or auto-approved if under HITL threshold) → `executed` / `failed`

The household can audit every order back to the inventory signals that triggered it. This is the "we tell you which agent did what, when, and what it cost" commitment from [`../09-portability-open-home.md`](../09-portability-open-home.md).
