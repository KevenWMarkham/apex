# apex-standards-sid — Third-Party Content Attribution

This package mirrors structural definitions from TM Forum SID (Shared
Information / Data Model).

## TM Forum SID

- **Authority:** TM Forum
- **URL:** https://www.tmforum.org/oda/information-systems/
- **Pinned version:** 22.5
- **License:** Open (TM Forum member benefit; non-member access permitted under TM Forum Open API & Data Programme licence with attribution)
- **Pattern:** B (data model mirror) per `Industry-Standards-Incorporation-Plan.md` §3
- **Redistribution:** Structural definitions may be redistributed with attribution under the TM Forum Open API & Data Programme licence.

## What this package ships

- Pydantic models named after SID Aggregate Business Entities
  (`Customer`, `Subscriber`, `Account`, `BillingAccount`, `Product`,
  `ProductOffering`, `Service`, `Resource`, `Party`, `PartyRole`)
- SID class hierarchy enumerations
- TM Forum Open API field-name conventions (camelCase, href, @type, etc.)

## Cross-references

- TM Forum Open APIs (TMF6xx series) — APEX consumes TMF629 (Customer Mgmt),
  TMF632 (Party Mgmt), TMF637 (Product Inventory), TMF666 (Account Mgmt),
  TMF678 (Customer Bill Mgmt), TMF688 (Event Mgmt) shapes
- 3GPP — telecom SOR alignments where relevant (BSSML schema)

## Restricted content guardrail

SID content is openly licensable, but TM Forum's full conceptual model PDFs
are member-restricted. This package ships **mirror models, not raw TM Forum
PDFs or full UML diagrams.** Tenants requiring full SID conceptual material
should obtain TM Forum membership.
