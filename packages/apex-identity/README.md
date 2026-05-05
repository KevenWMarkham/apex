# apex-identity

Identity + visibility-lattice runtime (APEX_Design §8).

## What it provides

- **`provisioning`** — `AgentRole` + `EntraProvisioningProvider` protocol + `MockEntraProvisioningProvider` (tests / dev) + `TenantRoleStore` separation.
- **`scope`** — `ScopeResolver` composes `AgentIdentity` + `AgentRole` → a fully-populated `ScopeContext`.
- **`lattice`** — `evaluate_visibility()` walks a Pydantic entity's classification metadata and returns a `VisibilityDecision` (visible/masked fields + row filter outcome).
- **`agent_safe_view`** — `apply_agent_safe_view(instance, scope)` returns a masked copy (fields outside scope → `None`) or `None` if row filters reject the row.
- **`signing`** — HMAC-based response signing keyed on `(agent_id, tenant_id)`. Sprint 13 upgrades to Key-Vault-held keys.

## Relationship to mcp-common

`mcp-common.ScopeContext` is the **structural** shape (Sprint 7 stub). `apex-identity` is the **runtime**: builds the context from provisioned identity + role, then enforces it at the tool boundary.
