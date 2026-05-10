# RC-E2E-04 / rc-loyalty-churn-prediction-winback — Default Use Case

Template stub. See worked example at
[`services/rc/RC-E2E-03/use-cases/_default/`](../../../RC-E2E-03/use-cases/_default/)
for the canonical fully-runnable use case.

## TODO at engagement-time

- [ ] Populate `client_approved_architecture` per the client's CAB
- [ ] Tune `kpis_targeted` per the engagement's commercial envelope
- [ ] Tune `hitl_thresholds` per Independence consultation
- [ ] Fill `chain_execution.steps[*].notes` and `data_read` / `data_written` / `kpi_affected` per the Services Guide profile
- [ ] Author `persona_kpi_attribution` block per persona × KPI relationships
- [ ] Write `smoke_test.fixture` JSON per the cold-chain template
- [ ] Replace `REPLACE_*` placeholders in use-case.yaml

## Reference

- [Use Case Template — Runnable Chain](../../../../docs/APEX%20-%20Design%20and%20Build/Use-Case-Template-Runnable-Chain.md)
- [Services Guide profile](../../../../docs/book/Professional-APEX-M-Services-Guide.html#ch-18) (find RC-E2E-04 subsection)
- [`services/_personas.yaml`](../../../../_personas.yaml)
- [`services/_kpis.yaml`](../../../../_kpis.yaml)
- Default persona for this scenario: `maya-patel-loyalty-crm-director`
