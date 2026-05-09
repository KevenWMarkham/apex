# SEC Independence — saas.snowflake adapter

> This adapter integrates with the client's existing investment in
> **Snowflake**. Deloitte does not resell, sublicense, or have
> an alliance posture with **Snowflake**; the adapter exists to
> honor the client's approved cloud architecture per their Cloud
> Architecture Board (CAB).

## Engagement requirements

Before this adapter is used in a client deployment:

- [ ] Client CAB has formally approved Snowflake as part of the client's approved architecture
- [ ] The client holds the Snowflake subscription / tenant / license — Deloitte does not procure it
- [ ] The use case's `client_approved_architecture` block references this adapter explicitly
- [ ] Pre-deployment Security Gate verifies integration with Snowflake satisfies the client's data-residency, classification, and audit requirements
- [ ] Per-engagement Independence consultation has cleared use of this adapter for the engagement's audit posture

## Language standards

Per [APEX Independence Posture](../../../../../../docs/apex-core/Independence-Posture.md):

- ✅ "honors the client's existing investment in Snowflake"
- ✅ "integrates with Snowflake per the client's CAB"
- ❌ "Deloitte–Snowflake alliance"
- ❌ "Snowflake is the preferred / primary [anything]"
