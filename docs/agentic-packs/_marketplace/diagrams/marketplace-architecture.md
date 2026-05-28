# Marketplace Architecture

```mermaid
flowchart TB
    subgraph Customer
        HH[("Household<br/>(vault + consent ledger)")]
    end

    subgraph Orchestrator[Home Orchestrator HOM-99]
        OR[("Intent routing<br/>(brand-neutral)")]
    end

    subgraph Marketplace[Telco Channel Marketplace]
        subgraph Home[Home Channel]
            H1[HOM-01 grocery]
            H2[HOM-02 energy]
            H3[HOM-03 eldercare]
            H4[HOM-04 maintenance]
            H5[HOM-05 security]
            H6[HOM-06 wellness]
            H7[HOM-07 vehicle]
            H8[HOM-08 entertainment]
        end
        subgraph Travel[Travel Channel]
            T1[HOM-11 AA flight]
            T2[HOM-12 Marriott hotel]
            T3[HOM-13 Expedia OTA]
            T4[HOM-14 Airbnb STR]
            T5[HOM-15 Uber / Hertz]
        end
        subgraph Retail[Retail Channel]
            R1[RTL-01 Walmart GM]
            R2[RTL-02 Walmart Pharmacy]
            R3[RTL-03 Walmart Auto]
            R4[RTL-04 Membership]
        end
        subgraph Mobility[Mobility Channel]
            M1[MOB-01 Toyota Connected]
            M2[MOB-02 Toyota Dealer]
            M3[MOB-03 Next Vehicle]
            M4[MOB-04 Toyota Fin/Ins]
        end
        subgraph Beverage[CPG / Beverage Channel]
            B1[BEV-01 Sazerac Replen]
            B2[BEV-02 Allocation Alerts]
            B3[BEV-03 Cocktail Concierge]
            B4[BEV-04 Tasting Events]
        end
    end

    subgraph Partners[Partner MCP Endpoints]
        AA[American Airlines]
        MAR[Marriott]
        EXP[Expedia]
        ABNB[Airbnb]
        WMT[Walmart]
        TYT[Toyota]
        SZR[Sazerac]
    end

    subgraph Billing[Telco Bill]
        BILL[("Single monthly invoice<br/>line item per Channel")]
    end

    HH -->|consent grants| OR
    OR -->|routes intent| Home
    OR -->|routes intent| Travel
    OR -->|routes intent| Retail
    OR -->|routes intent| Mobility
    OR -->|routes intent| Beverage

    Travel -.->|MCP| AA
    Travel -.->|MCP| MAR
    Travel -.->|MCP| EXP
    Travel -.->|MCP| ABNB
    Retail -.->|MCP| WMT
    Mobility -.->|MCP| TYT
    Beverage -.->|MCP| SZR

    Home --> BILL
    Travel --> BILL
    Retail --> BILL
    Mobility --> BILL
    Beverage --> BILL

    BILL --> HH

    style Customer fill:#f0fdf4,stroke:#16a34a
    style Marketplace fill:#fef3c7,stroke:#d97706
    style Partners fill:#dbeafe,stroke:#3b82f6
    style Billing fill:#fee2e2,stroke:#dc2626
```

## Read this diagram as

- The **household** holds the vault and grants consents
- The **Home Orchestrator** (HOM-99) sits between the household and the marketplace
- Each **Channel** is a band in the marketplace, named for its category, populated with service-code sub-agents
- Partner **MCP endpoints** sit outside the Telco's runtime; the orchestrator talks to them via the open partner protocol
- The single **Telco bill** rolls up subscriptions across every Channel
- **Action commerce** flow (not shown) closes the loop between Channels and partners outside the diagram
