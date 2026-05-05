# ER — Discovery Prompts

Discovery prompts for utility / oil-gas / mining / water engagements.
Map answers to the Sprint 18 `utility` reference deployment.

## Triggering-event probes

1. "What's your service territory's wildfire / extreme-weather exposure, and what
   does your last PSPS decision audit look like to a PUC reviewer?"

2. "Trailing-12-month SAIDI / SAIFI versus regulator commitment — and where's the
   biggest contributor (storm, vegetation, equipment, customer-side)?"

3. "How are you sequencing crews today during a storm-driven outage surge — by
   geographic block, customer-count, critical-load, or paper-list dispatcher
   judgement?"

4. "Last 4 quarters of AMI-billing complaints to PUC — what was the median
   triage-to-RCA cycle time?"

5. "Vegetation defect-find rate per inspection cycle today — is the inspection
   list risk-prioritized or geography-prioritized?"

## Oil-gas / mining probes (where applicable)

6. "TRIR / process-safety incident trend last 24 months — where's the biggest
   leading-indicator gap?"

7. "What's your fleet-mining digitization maturity (autonomous haulage, predictive
   maintenance, ventilation-on-demand)?"

8. "Drilling-safety: what surfaces near-miss data into investigation today?"

## Architecture / data probes

9. "OSI PI / AVEVA historian deployment — single instance or distributed? Sprint
   15 PI adapter assumes API-level access with Bronze landing."

10. "AS/400 CIS or modern CIS (Oracle CC&B, Hansen CIS+, SAP IS-U)? Adapter choice
    shifts."

11. "Are you on AWS or Azure for your IT/OT segmentation today? CIP-014 critical
    infrastructure constraints inform the answer."

## Audit / governance probes

12. "CIP-014 classification scope — which assets are designated, and how do you
    audit access today? Sprint 13 classifications baseline assumes
    `critical-infrastructure` Purview tier."

13. "FERC / NERC retention requirements for your decisions — how long, and at
    what evidence detail?"

## Commercial probes

14. "Where would value-share be cleanest: AMI billing recovery, vegetation defect
    yield, peak-demand reduction via DER orchestration?"

15. "Wave-1 budget shape ($1.0-2.0M envelope, 10-14 weeks) given regulator-grade
    audit posture deliverable?"

## Cross-reference

- Sprint 18 reference deployment: `utility` (Sellers Guide §11.9)
- Sprint 17 service catalog: ER-PU + ER-OG + ER-MN
- Sprint 16 anchor agents (10)
