# APEX Compliance Pre-Clearance Checklist

Run before any Wave-1 production deployment. Tied to Sprint 13 governance,
Sprint 16 agent runtime, Sprint 18 reference-deployment audit posture.

## Regulatory posture per Practice

### RC

- [ ] FSMA 204 traceability-event compatibility validated for cold-chain agent
- [ ] PCI scope mapped for loyalty + payment-card data
- [ ] State-privacy (CCPA / VCDPA / CPA) handling for customer-360
- [ ] Marketing-consent flow honored (opt-in / opt-out + audit trail)

### HLS

- [ ] HIPAA Privacy + Security rules covered; BAA in place
- [ ] 42 CFR Part 2 segmentation validated for substance-use / behavioral-health
- [ ] CMS / Joint Commission audit posture for clinical-decision agents
- [ ] State licensure & disclosure requirements covered
- [ ] Pharmacovigilance / FDA reporting workflow integrated where adverse-event agent operates

### ER

- [ ] CIP-014 critical-infrastructure classification posture
- [ ] FERC / NERC retention + audit requirements
- [ ] PUC public-records obligations on PSPS decisions
- [ ] State-specific environmental-justice / equity reporting (where wildfire / outage-impact relevant)
- [ ] OSHA / state-OSHA compliance for HSE incident handling
- [ ] Oil-gas-mining: ISN / Avetta supplier-safety integration where applicable

### AXLE

- [ ] EAR / ITAR posture for engineering data
- [ ] IATF 16949 / ISO 9001 / FAA Part 145 quality-system audit alignment
- [ ] OSHA worker-safety integration for andon / RCA agents
- [ ] EU Machinery Regulation (where applicable)

### TMT

- [ ] PCI scope across all payment-touching surfaces
- [ ] GDPR / CCPA + e-Privacy directives for subscriber telemetry
- [ ] FCC / FTC content-safety obligations
- [ ] DSA / DMA compliance for EU-facing platforms

### TH

- [ ] DOT tarmac-rule compliance audit trail
- [ ] PCI scope across booking + ancillary flows
- [ ] Cross-border PII (GDPR / CCPA / state-privacy)
- [ ] DOT Part 121 / EASA airworthiness boundary respected by maintenance-adjacent agents

### ICE

- [ ] FDA 21 CFR Part 820 quality-system alignment (medical devices)
- [ ] IEC 62443 industrial-cybersecurity baseline (industrial controls)
- [ ] EU Cyber Resilience Act readiness (consumer electronics)

## Cross-cutting compliance

- [ ] Purview classification baseline applied per Sprint 13 (operations / pii / phi / payment-card / critical-infrastructure / intellectual-property / controlled-unclassified as applicable)
- [ ] DLP rules authored + tested per Sprint 13
- [ ] Audit-row retention meets longest-applicable regulator timeframe
- [ ] HITL gate placement reviewed for consequential-decision coverage per Sellers Guide §2.2C
- [ ] Pure-HOTL agents (no HITL) explicitly justified per Sprint 16 governance rule (routine + reversible only)
- [ ] Sub-processor list documented + flowed into customer DPA addenda
- [ ] Incident-response playbook integrated into engagement runbook

## Cross-reference

- Sprint 13 governance baseline
- Sprint 16 agent governance (HITL / HOTL / HIC posture)
- Sellers Guide §2.2C (oversight spectrum), §6.10 (audit row), §6.13 (manifest provenance)
