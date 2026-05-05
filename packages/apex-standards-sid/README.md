# apex-standards-sid

**Pattern-B** mirror for TM Forum SID (Information Framework).

**Consumed by:** `apex-telml`.

## Scope (Sprint 3)

Seven domains that TMT anchor agents consume. SID has 45+ domains; APEX deliberately ships only the thin slice used by agents.

- Party (`SidParty`)
- Customer (`SidCustomer`)
- Product (`SidProduct`, `SidProductOffering`)
- Service (`SidService`)
- Resource (`SidResource`)
- BillingAccount (`SidBillingAccount`)

Shared primitives: `SidLifecycleStatus`, `SidRelatedParty`.

## Scope discipline

Additional SID domains land when a consuming TMT agent ships. Design anchor: `Sprint-3-Practice-Schemas-Plan.md` §4.4.
