# Arium Networks — TMT scenario additions (design)

**Date:** 2026-05-14
**Author:** Keven Markham
**Status:** Approved, ready for implementation

## Goal

Add 8 net-new `tmt-arium-*` scenarios to `docs/reference/APEX-Scenario-Chains.xlsx`, filling the wireless-infra-vendor gap in the existing TMT catalog (which is currently written from the carrier's seat).

## Why

Arium Networks is a wireless infrastructure / RAN vendor. The TMT catalog has 127 scenarios but only 15 in Network & Infrastructure — all written from the carrier/operator perspective. There is no coverage of the wireless-infra-vendor lens (deployed-fleet ops, field service, RMA root cause, SLA-as-supplier). Filling this gap serves the Arium pursuit and is reusable at Ericsson, Nokia, Samsung Networks, Mavenir, CommScope, etc.

## Scope

### In scope

- 8 net-new scenarios, all catalog-tier (not marquee/Featured)
- Service code: `TMT-TEL-NET-02` (existing Network Operations)
- Domain: `Network & Infrastructure`
- Sheets touched:
  - **Scenario Library** — 8 rows appended
  - **Scenario→KPI Chain** — 8 rows appended (catalog-template Solution/Use-Case strings)
  - **24-Step Chain** — 192 rows appended (8 × 24, standard W1/W2/W3 template)
  - **Summary** — totals updated (745 → 753 scenarios, 24-step rows 17376 → 17568, version bump to v1.6)

### Out of scope

- Featured Chains sheet (no marquee depth; can promote 1-2 later if Arium pursuit accelerates)
- New service code (e.g., `TMT-TEL-NET-05` Wireless Infra Vendor Ops) — keeping `TMT-TEL-NET-02`
- Schemas column population — left blank to match existing N&I rows
- Updates to APEX-Stacked-Architecture-Narrated.html or other source docs — xlsx-only

## The 8 scenarios

| # | Scenario ID | Title | KPI / Outcome |
|---|---|---|---|
| 1 | `tmt-arium-ran-fleet-predictive-failure` | RAN-fleet predictive failure (vendor-side) | Predicted-failure capture +62% · pre-emptive swap 14% → 71% · carrier SLA credits −$8.4M/yr |
| 2 | `tmt-arium-field-service-dispatch-optimization` | Field-service dispatch optimization | First-time-fix 71% → 89% · drive-hours/ticket −24% · re-roll −67% |
| 3 | `tmt-arium-spare-parts-depot-rebalance` | Spare-parts depot rebalance | AOG wait 4.2d → 18h · holding cost −19% · SLA credits −$3.1M/yr |
| 4 | `tmt-arium-firmware-release-orchestration` | Firmware-release orchestration | MTT-rollback 96h → 9h · canary coverage 31% → 100% · rollback SLA loss −82% |
| 5 | `tmt-arium-site-energy-attribution` | Site-energy attribution & Scope-3 reporting | Time-to-attest 11wk → 4d · 100% carriers covered · audit-ready CDP/SBTi |
| 6 | `tmt-arium-carrier-sla-breach-prediction` | Carrier-SLA-breach prediction & credit liability | Forecast accuracy +73% · unplanned write-offs −58% · CFO confidence +2.3pts |
| 7 | `tmt-arium-warranty-rma-cluster-detection` | Warranty / RMA cluster detection | Time-to-cluster 11wk → 6d · warranty cost −24% · supplier charge-back +$4.7M/yr |
| 8 | `tmt-arium-private-5g-opportunity-scoring` | Private-5G enterprise-opportunity scoring | Pilot→deployment 41% → 68% · BD time/prospect −51% · win-rate at survey-gate +27pts |

Briefs, personas, and per-scenario detail captured in the implementation plan.

## Approach

Use `openpyxl` to load the workbook, append rows to each of the four sheets, then run `scripts/recalc.py` for formula recalculation and error scan. Preserve existing formatting and column conventions (no font/style overrides — workbook has an established template).

### 24-Step Chain templating

The 24-step rows follow a fixed APEX template with per-scenario substitution points: Title, Brief (the moment), Solution, Use-Case, Service, Persona, KPI. Existing scenarios use heavily templated Purpose / What APEX Does text — the new rows will match that pattern verbatim, with only the Scenario Note column tailored per scenario.

### Catalog-tier Scenario→KPI Chain values

For Solution / Use-Case / Service / Persona columns in Scenario→KPI Chain, use the catalog-template strings observed in the existing 709 catalog rows:
- Solution: `"Standard archetype: hierarchical-root + sequential-with-hitl-gate · 6-agent fleet · APEX canonical"`
- Use-Case: `"Wave 2 pilot delivery for {Title}"`
- Service: `"TMT-TEL-NET-02"`
- Persona: `"Operator with HITL approval authority via Teams Adaptive Card"`

## Verification

After writing:
1. `python scripts/recalc.py APEX-Scenario-Chains.xlsx` → expect `status: success`, zero errors
2. Re-open and confirm: 753 rows in Scenario Library, 753 rows in Scenario→KPI Chain, 17568 rows in 24-Step Chain
3. Spot-check 2 scenarios end-to-end across all 4 sheets
4. Confirm Summary metrics updated

## Risks / unknowns

- **Persona names are invented.** No real Arium executive contacts confirmed. Replace before any external use.
- **KPI magnitudes are illustrative.** Sized to be credible for a vendor of Arium's likely scale, but not validated against real Arium financials.
- **Service code re-use.** `TMT-TEL-NET-02` covers carrier-side and now vendor-side ops; if Deloitte service-line distinctions need separation later, a follow-up can introduce `TMT-TEL-NET-05`.
