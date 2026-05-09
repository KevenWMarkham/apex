# SEC Independence — siem.splunk adapter

> This adapter integrates with the client's existing investment in
> **Splunk**. Deloitte does not resell, sublicense, or have
> an alliance posture with **Splunk**; the adapter exists to
> honor the client's approved cloud architecture per their Cloud
> Architecture Board (CAB).

## Engagement requirements

Before this adapter is used in a client deployment:

- [ ] Client CAB has formally approved Splunk as part of the client's approved architecture
- [ ] The client holds the Splunk subscription / tenant / license — Deloitte does not procure it
- [ ] The use case's `client_approved_architecture` block references this adapter explicitly
- [ ] Pre-deployment Security Gate verifies integration with Splunk satisfies the client's data-residency, classification, and audit requirements
- [ ] Per-engagement Independence consultation has cleared use of this adapter for the engagement's audit posture

## Language standards

Per [APEX Independence Posture](../../../../../../docs/apex-core/Independence-Posture.md):

- ✅ "honors the client's existing investment in Splunk"
- ✅ "integrates with Splunk per the client's CAB"
- ❌ "Deloitte–Splunk alliance"
- ❌ "Splunk is the preferred / primary [anything]"
