# APEX Legal Pre-Clearance Checklist

Run before signing any Wave-1 SoW. Address Deloitte-independence rules, IP
ownership, model-provider terms, and data-rights flow-through.

## Deloitte independence (Big-4 audit conflict)

- [ ] Client audit relationship confirmed (yes / no / conflicted-affiliate)
- [ ] If audit client: SoW scope reviewed by Independence Office; non-attest service classification confirmed
- [ ] Audit-relationship-bounded scope (e.g., financial-statement-driven KPIs may be off-limits)
- [ ] DSE (Deloitte Specialty Entity) routing decision made if needed for value-share / outcome-based commercial
- [ ] Sub-contractor independence verified for any specialty-partner inclusion

## IP ownership

- [ ] APEX framework IP pre-existing (Deloitte-retained); engagement-IP carve-outs explicit in SoW
- [ ] Custom-prompt IP ownership clear (typically: client-specific tuning is client-owned; framework methodology Deloitte-retained)
- [ ] Custom-MCP-tool IP ownership clear (client's code → client; framework code → Deloitte)
- [ ] Open-source license stack reviewed (Pydantic / Typer / pytest under permissive licenses; no AGPL exposure)
- [ ] Trained-model artifacts: who owns the fine-tuned model + the training data?

## Model-provider terms

- [ ] Azure OpenAI / Foundry terms reviewed; data-handling commitments understood
- [ ] No-training-on-customer-data confirmed (Foundry default; verify configuration)
- [ ] Indemnity exposure on model output (Microsoft Customer Copyright Commitment scope)
- [ ] Anthropic / OpenAI / other-model-provider terms reviewed if multi-model

## Data rights & cross-border

- [ ] Data-residency requirements documented (state / federal / regional)
- [ ] Cross-border transfer mechanism in place (SCCs / DPF / BCRs as applicable)
- [ ] Subject-rights workflow (DSARs, deletion, rectification) reflected in agent design
- [ ] Data-retention contractual minimum / maximum aligned with engagement

## Audit & evidence

- [ ] Audit-row retention contractual minimum aligned with regulator + Deloitte standards
- [ ] Replay-token contractual treatment (forensic discovery scope)
- [ ] Counsel-review of high-stakes HITL gate language (PSPS, sepsis, etc.)

## Commercial structure

- [ ] Fixed-fee vs. value-share structure reviewed against independence rules
- [ ] Outcome-share KPI commitment language reviewed (hedge against ambiguous attribution)
- [ ] Termination clause + transition-out plan
- [ ] Insurance / liability caps aligned with Deloitte enterprise risk

## Cross-reference

- Sellers Guide §2.6 (commercial models)
- Sellers Guide §6.10 (audit row contract)
- Appendix K (independence + competitive posture)
