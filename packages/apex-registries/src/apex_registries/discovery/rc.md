# RC — Discovery Prompts

Use these prompts in early-stage discovery (executive briefings, day-1 workshops)
to qualify pain and shape Wave-1 scope. Map answers back to the Sprint 18
`big-box-store` reference deployment use cases.

## Triggering-event probes

1. "When was your last cold-chain excursion of consequence — and how long did
   disposition take from alert to store-manager action?" *(maps to RC-E2E-04 cold-chain
   response)*

2. "Tell me about the last private-label division where markdown cadence missed
   sell-through plan by ≥ 5pp. What was the analyst-attributable delay between
   knowing and reacting?" *(maps to RC-E2E-05 markdown cadence)*

3. "How does your replenishment system handle a forecasted regional demand event
   today — anticipatory, reactive, or after-the-fact?" *(maps to RC-E2E-03 demand
   sensing)*

4. "On your top-200 SKUs, what's your shelf-availability compliance — and how
   often does the planogram drift from what's actually faced?" *(maps to RC-E2E-07
   store-ops intelligence)*

5. "When loss-prevention triangulates a suspected shrink ring, how many days
   from suspicion to confirmed action plan?" *(maps to RC-E2E-06 shrink detection)*

## Architecture / data probes

6. "Where does SAP S/4HANA live for you — single-tenant on-prem, RISE, or hyperscaler-hosted?
   We mirror via Fabric mirroring; that constrains adapter choices."

7. "What's your loyalty / customer data platform today (Salesforce, Adobe, in-house)?
   That shapes the CXML adapter choice."

8. "Do you have a Snowflake or Databricks lakehouse in front of Fabric that we'd
   read-mirror?"

## Audit / governance probes

9. "What's your FSMA 204 readiness posture today? We bake the audit row into the
   cold-chain agent decision."

10. "Where do payment-card and loyalty-PII flow through your environment today?
    Sprint 13 governance applies Purview classifications + DLP at every stage."

## Commercial probes

11. "Which of these would feel value-share-friendly in your environment: shrink
    recovery, markdown yield, cold-chain disposition? We commercialize value-share
    where attribution is contractually clean."

12. "What's the budget shape for the next 4-12 weeks of foundation work — fixed-fee
    envelope ($0.75-1.5M Wave-1), or do you want to land via a paid POC first?"

## Cross-reference

- Sprint 18 reference deployment: `big-box-store` (Sellers Guide §16.13)
- Sprint 17 service catalog: RC-E2E + RC-TTP
- Sprint 16 anchor agents (10)
