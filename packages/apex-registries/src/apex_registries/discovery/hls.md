# HLS — Discovery Prompts

Discovery prompts for IDN / hospital / payer / life-sciences engagements.
Map answers to the Sprint 18 `hospital` reference deployment.

## Triggering-event probes

1. "What's your trailing-quarter SEP-1 bundle compliance? CMS reporting penalties
   create the executive sponsor for a sepsis-EW deployment."

2. "What's your trailing-quarter med-surg LOS variance and ED-boarding hours?
   The CNO is the natural sponsor for utilization-management work."

3. "What's your first-pass denial rate, and which top-3 payers drive the biggest
   recoverable AR aging?"

4. "How is your HIM team processing duplicate-MRN backlog today — manual review,
   automated probabilistic match, or both?"

5. "When was your last pharmacovigilance signal that broke through into FDA
   reporting? Adverse-event cold-chain detection sits adjacent to that."

## Architecture / data probes

6. "Is Epic Clarity + Caboodle accessible to your team today? Sprint 15 mirroring
   adapter assumes Clarity-side mirroring with downstream FHIR shaping in Silver."

7. "What's your HL7 v2 → FHIR migration posture? Sprint 23 translators bridge
   v2 messages into Silver if Clarity isn't viable."

8. "Workday HCM for staffing data — which version, and is FedRAMP relevant?"

## Audit / governance probes

9. "Your Purview deployment status — labeled, configured, fully classifying? Sprint
   13 governance baseline assumes Purview standard at minimum."

10. "Audit retention requirements for clinical decisions in your jurisdiction —
    HIPAA standard or longer (state-specific, research-data, 42 CFR Part 2)?"

11. "How do you handle 42 CFR Part 2 data segmentation today (substance-use treatment,
    psychiatric)? Sprint 13 classification rules treat this as a separate sensitivity tier."

## Commercial probes

12. "Which of these are clean-attribution candidates for value-share: claim
    cycle-time, denial reversal, readmission reduction in named cohort?"

13. "What's the budget shape for Wave-1 ($1.0-1.75M envelope, 10-14 weeks), or do
    you want to land via paid pilot first?"

## Cross-reference

- Sprint 18 reference deployment: `hospital` (Sellers Guide §10.9)
- Sprint 17 service catalog: HLS-E2E + HLS-PAY + HLS-LS
- Sprint 16 anchor agents (10)
