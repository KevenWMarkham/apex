# Loyalty churn prediction & winback

**Practice:** RC — Retail & Consumer  
**Scenario index:** 05 of 5 featured (global chain 5 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Top-tier loyalty members (top 20% of customers, 64% of revenue) show silent-churn signals 6 weeks before attrition. CRM sends generic winback campaigns with &lt;4% response rate .

## Solution
Churn-prediction agent reads loyalty engagement, transaction patterns, service interactions, and (with consent) cross-channel signals. Generates personalized winback offers timed to the churn-risk window. HITL gate on discount depth above threshold.

## Use Case
Loyalty-lifecycle management across retention and winback cohorts. Reads CXML.LoyaltyMember , CXML.Campaign , MERML.Transaction .

## Service
RC-E2E-04 Customer Lifecycle &amp; Loyalty. Wave 2 at top 500K members; Wave 3 full loyalty base.

## Persona
Primary Maya Patel · Loyalty & CRM Director Reviews weekly cohort performance; approves offer-depth escalations.

## KPI
Churn rate −22% in top tier · winback response rate +17pp · LTV of saved customers +34% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-loyalty-churn-prediction-winback-build-guide.md` — step-by-step build
- `APEX-loyalty-churn-prediction-winback-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
