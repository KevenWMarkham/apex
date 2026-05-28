# Purchase Orchestration — End-to-End Flow

> Saturday-research to Tuesday-drive-home. Multi-anchor partnership (AutoNation + Cox Automotive + Progressive + Capital One Auto) orchestrated through the household vault, with HITL gates at every commitment.

```mermaid
flowchart TD
    INTENT[("Household intent: replace 2017 Highlander")]

    INTENT -->|AUT-01 Discovery| RESEARCH[("Cox / KBB / Autotrader<br/>+ Edmunds + CarGurus")]
    RESEARCH -->|shortlist 2-3 vehicles| SHORTLIST[("Silver: VehicleListing<br/>shortlisted=true")]

    SHORTLIST -->|trigger| AUT03[("AUT-03 Financing<br/>pre-approval shopping")]
    SHORTLIST -->|trigger| AUT04[("AUT-04 Insurance<br/>quote shopping")]
    SHORTLIST -->|trigger| AUT08TI[("AUT-08 Trade-in<br/>valuation")]

    AUT03 -->|soft pulls| LENDERS[("Capital One Auto<br/>+ Ally + USAA")]
    LENDERS -->|pre-approvals| OFFERS[("FinancingApplication<br/>4 approvals")]

    AUT04 -->|with telematics| CARRIERS[("Progressive Snapshot<br/>+ State Farm + Geico")]
    CARRIERS -->|quotes| QUOTES[("InsuranceQuote<br/>4 quotes")]

    AUT08TI -->|valuations| RESALE[("CarMax + Carvana<br/>+ AutoNation trade-in")]

    OFFERS --> AUT02[("AUT-02 Purchase<br/>orchestrator")]
    QUOTES --> AUT02
    RESALE --> AUT02

    AUT02 -->|negotiation| AUTONATION[("AutoNation<br/>3 locations")]
    AUTONATION -->|reservation| OFFER[("PurchaseOffer<br/>state=accepted")]

    OFFER --> HITL{"HITL gate<br/>OTD > shortlist median +$5K?"}
    HITL -->|approve| SIGN[("Customer arrives<br/>Tuesday 5 PM<br/>signs in 45 min")]

    SIGN -->|writes| BIND1[("AUT-03 finalize<br/>financing")]
    SIGN -->|writes| BIND2[("AUT-04 bind<br/>Progressive policy")]
    SIGN -->|writes| BIND3[("AUT-08 execute<br/>trade-in")]
    SIGN -->|writes| BIND4[("DMV pre-fill<br/>via Vitu")]

    BIND1 --> VAULT[("Vault state:<br/>Vehicle.lifecycle_state =<br/>owning_warranty")]
    BIND2 --> VAULT
    BIND3 --> VAULT
    BIND4 --> VAULT

    VAULT -->|notifies| HOM07[("HOM-07 vehicle<br/>registers new vehicle")]
    VAULT -->|notifies| MOB01[("MOB-01 Toyota Connected<br/>starts service lifecycle")]

    AUT02 -.->|every step| AUDIT[("agent_run +<br/>agent_action +<br/>view_definition_sha")]

    style INTENT fill:#fff,stroke:#999
    style SHORTLIST fill:#e6f4ea,stroke:#16a34a
    style AUT02 fill:#f3e8ff,stroke:#8b5cf6
    style HITL fill:#fef3c7,stroke:#d97706
    style SIGN fill:#dbeafe,stroke:#3b82f6
    style VAULT fill:#fee2e2,stroke:#dc2626
    style AUDIT fill:#f1f5f9,stroke:#64748b
```

## Why this is the wedge

- **Emotional + financial stakes maximal** — vehicle purchase is the second-largest household transaction after home
- **Time savings visceral** — 6 hours over 3 days vs typical 20-40 hours over weeks
- **Money savings auditable** — financing APR + insurance premium + dealer markup deltas are explicit
- **Trust-building durable** — a successful purchase creates a multi-year retention anchor
- **Cross-Channel anchor** — touches Home (HVAC + EV charging), Mobility (OEM connected), Retail (Walmart Auto Care)
