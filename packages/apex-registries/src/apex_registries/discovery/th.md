# TH — Discovery Prompts

Discovery prompts for travel / hospitality engagements.
Map answers to the Sprint 18 `airline` reference deployment.

## Triggering-event probes

1. "Last severe IROPS event — what was your trigger-to-recovery-plan-approved
   cycle time across operations + crew + customer?"

2. "Trailing-quarter D0 (on-time departure) vs. industry, and where's the
   biggest contributor (ground-ops, ATC, mechanical)?"

3. "Yield per ASM trend by competitive segment — where are you bleeding to
   low-cost / new-entrant pressure?"

4. "Top-tier loyalty member retention 12-month, and which service-event types
   are the strongest predictors of churn?"

5. "Ground-ops at-risk-turn precision — how many at-risk turns get caught before
   the late-arrival cascade today?"

## Architecture / data probes

6. "DCS / PSS — Sabre, Amadeus, Navitaire, in-house? Adapter shape changes."

7. "Loyalty platform — homegrown, Salesforce-on-Amadeus, third-party? TravelerML
   schema mapping depends."

8. "Crew systems — Sabre AirOps, Jeppesen, in-house? Crew-scheduling agent integration
   pattern follows."

9. "Salesforce + ServiceNow + Workday combination — which versions, any custom
   middleware?"

## Audit / governance probes

10. "PCI scope across booking + ancillary + check-in flows?"

11. "Trans-Atlantic / cross-border PII flows — GDPR posture? Sprint 13 governance
    baseline."

12. "DOT tarmac-rule compliance — how does your ops audit trail meet the 4-hour
    threshold today?"

## Commercial probes

13. "Where's value-share cleanest: yield uplift on instrumented O&Ds, IROPS recovery
    cost reduction, top-tier retention attribution?"

14. "Wave-1 budget shape ($0.9-1.75M envelope, 8-12 weeks) for one hub + one
    revenue region?"

## Cross-reference

- Sprint 18 reference deployment: `airline` (Sellers Guide §14.8)
- Sprint 17 service catalog: TH-AIR + TH-HOT
- Sprint 16 anchor agents (10)
