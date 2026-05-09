# cloud.gcp.pubsub — Google Pub/Sub adapter

**Satisfies:** `MessageBus`
**Status:** Stub. Concrete implementation builds per-engagement.

## Purpose

Cross-cloud event routing GCP -> APEX-M Eventstream.

## Use case wiring

Reference this adapter from a use-case YAML's `client_approved_architecture` block; see `services/_use-case.schema.md`.

## Implementation plan

When a client's CAB has approved this integration:

1. Implement `client.py` wrapping the Google Pub/Sub SDK
2. Provide IaC for adapter-side resources under `iac/`
3. Smoke test against a Google Pub/Sub sandbox
4. Add the adapter to the wizard's known-adapter validator
5. Update [docs/apex-core/Adapter-Catalog.md](../../../../../../docs/apex-core/Adapter-Catalog.md)

## See also

- [sec_independence.md](sec_independence.md) — Deloitte Independence posture for this provider
- [APEX-Core Independence Posture](../../../../../../docs/apex-core/Independence-Posture.md)
- [APEX-Core Adapter Catalog](../../../../../../docs/apex-core/Adapter-Catalog.md)
