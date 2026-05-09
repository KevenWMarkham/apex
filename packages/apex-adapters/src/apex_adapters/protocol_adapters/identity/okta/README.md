# identity.okta — Okta adapter

**Satisfies:** `AgentIdentityProvider`
**Status:** Stub. Concrete implementation builds per-engagement.

## Purpose

Federated identity via Okta IdP for non-Entra workforces.

## Use case wiring

Reference this adapter from a use-case YAML's `client_approved_architecture` block; see `services/_use-case.schema.md`.

## Implementation plan

When a client's CAB has approved this integration:

1. Implement `client.py` wrapping the Okta SDK
2. Provide IaC for adapter-side resources under `iac/`
3. Smoke test against a Okta sandbox
4. Add the adapter to the wizard's known-adapter validator
5. Update [docs/apex-core/Adapter-Catalog.md](../../../../../../docs/apex-core/Adapter-Catalog.md)

## See also

- [sec_independence.md](sec_independence.md) — Deloitte Independence posture for this provider
- [APEX-Core Independence Posture](../../../../../../docs/apex-core/Independence-Posture.md)
- [APEX-Core Adapter Catalog](../../../../../../docs/apex-core/Adapter-Catalog.md)
