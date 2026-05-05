# AXLE — Discovery Prompts

Discovery prompts for discrete-manufacturing engagements.
Map answers to the Sprint 18 `plant` reference deployment.

## Triggering-event probes

1. "What's your flagship line's trailing-90-day OEE versus target, and decompose:
   availability, performance, or quality biggest contributor?"

2. "Last 4 quarters of unplanned downtime hours on critical assets — and how much
   of that was preventable in hindsight?"

3. "Field-defect PPM trend on top-10 part numbers — where's the biggest cluster,
   and is it supplier-correlated?"

4. "Energy spend year-over-year — is the demand-charge component growing? Compressed
   air, HVAC, peak-shaving via on-site generation?"

5. "Warranty cost per vehicle (auto) or per unit (industrial) trend, and how often
   does field-claim genealogy reach back to manufacturing-day data today?"

## Architecture / data probes

6. "GE Proficy / AVEVA / Wonderware historian — which instance, what version,
   how is data exported today?"

7. "SAP S/4HANA digital core present? CDC mirroring viable? Sprint 15 SAP adapter
   prefers mirroring over RFC pulls."

8. "PLM system (Teamcenter, Windchill, Aras, ENOVIA)? Engineering / IP classification
   constraints inform the architecture."

9. "MES / shop-floor IT/OT segmentation — is the OT side on a separate VLAN with
   firewall traversal? Sprint 14 per-workload-isolation pattern assumes yes."

## Audit / governance probes

10. "Engineering data classification — controlled-unclassified, EAR / ITAR
    relevant? Sprint 13 governance baseline applies appropriate tags."

11. "Quality-system audit posture — IATF 16949 / ISO 9001 / FAA Part 145 (where
    applicable)?"

## Commercial probes

12. "Where's value-share cleanest: warranty cost reduction, energy cost per unit,
    parts-fill-rate uplift in service?"

13. "Wave-1 budget shape ($0.85-1.75M envelope, 8-12 weeks) given a flagship line
    + 1-2 product-family scope?"

## Cross-reference

- Sprint 18 reference deployment: `plant` (Sellers Guide §12.9A)
- Sprint 17 service catalog: AXLE-Connected-Factory + AXLE-QMS + AXLE-Ops + AXLE-Aftermarket + AXLE-Supply
- Sprint 16 anchor agents (10)
