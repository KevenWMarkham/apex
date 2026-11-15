# SEC Independence — cloud.gcp.bigquery adapter

> This adapter integrates with the client's existing investment in
> **Google Cloud**. The firm does not resell, sublicense, or have
> an alliance posture with **Google Cloud**; the adapter exists to
> honor the client's approved cloud architecture per their Cloud
> Architecture Board (CAB).

## Engagement requirements

Before this adapter is used in a client deployment:

- [ ] Client CAB has formally approved Google Cloud as part of the client's approved architecture
- [ ] The client holds the Google Cloud subscription / tenant / license — the firm does not procure it
- [ ] The use case's `client_approved_architecture` block references this adapter explicitly
- [ ] Pre-deployment Security Gate verifies integration with Google Cloud satisfies the client's data-residency, classification, and audit requirements
- [ ] Per-engagement Independence consultation has cleared use of this adapter for the engagement's audit posture

## Language standards

Per [APEX Independence Posture](../../../../../../docs/apex-core/Independence-Posture.md):

- ✅ "honors the client's existing investment in Google Cloud"
- ✅ "integrates with Google Cloud per the client's CAB"
- ❌ "the firm–Google Cloud alliance"
- ❌ "Google Cloud is the preferred / primary [anything]"
