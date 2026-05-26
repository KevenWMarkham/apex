# Arium TMT Scenarios — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Append 8 net-new `tmt-arium-*` wireless-infra-vendor scenarios into `docs/reference/APEX-Scenario-Chains.xlsx` across 4 sheets, matching existing templates exactly.

**Architecture:** Single-pass Python script using `openpyxl` to append rows. No formulas added (the workbook is reference data, not a model). Verification via row counts + `scripts/recalc.py` error scan + spot-check.

**Tech Stack:** Python 3.14, openpyxl, LibreOffice (for recalc.py).

**Design doc:** `docs/plans/2026-05-14-arium-tmt-scenarios-design.md`

---

## Task 1: Snapshot pre-state of the workbook

**Files:**
- Read: `docs/reference/APEX-Scenario-Chains.xlsx`

**Step 1: Capture current row counts and last `#` value in Scenario Library**

Run:

```powershell
python -c "import sys,io; sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8'); import openpyxl; f=r'docs/reference/APEX-Scenario-Chains.xlsx'; wb=openpyxl.load_workbook(f,read_only=True,data_only=True); 
[print(s, wb[s].max_row) for s in wb.sheetnames]"
```

Expected output:
```
Summary 22 (approx)
Scenario Library 746   # 1 header + 745 data
Featured Chains 37     # 1 header + 36 data
Scenario→KPI Chain 746
24-Step Chain 17377    # 1 header + 17376 data
```

Record the actual numbers before any writes.

---

## Task 2: Build the row-generator script

**Files:**
- Create: `docs/reference/_add_arium_scenarios.py` (sibling to existing `_add_*.py` generators in that directory)

**Step 1: Write the generator script**

Mirror the conventions of the existing `_add_disney_tmt_scenarios.py` / `_add_studios_scenarios.py` siblings already in `docs/reference/`. Script must:

1. Load workbook with `openpyxl.load_workbook(path, data_only=False)` — preserves any formulas
2. Define the 8 scenarios as a list of dicts with fields: `id`, `title`, `brief`, `kpi`, `persona`
3. Append rows to **Scenario Library** with: `(next_num, id, title, "TMT-TEL-NET-02", "Network & Infrastructure", None, brief, kpi, "Catalog")`
4. Append rows to **Scenario→KPI Chain** with catalog-template values for Solution/Use-Case/Service/Persona (per design doc)
5. Append 24 rows per scenario to **24-Step Chain** using the canonical template from the existing TMT N&I scenarios — preserve all Purpose / What APEX Does strings verbatim from `tmt-network-fault-prediction`, substituting only scenario-specific tokens: `{Title}`, `{Brief}`, `{Solution}`, `{Use Case}`, `{Service}`, `{Persona}`, `{KPI}`
6. Update **Summary** sheet:
   - Row "Total scenarios": `745` → `753`
   - Row "Catalog scenarios (compact)": `709` → `717`
   - Row "24-step chain rows (758 × 24)": label OK; value `17376` → `17568`
   - Row "Document version": append `· v1.6 · 2026-05-14 · added 8 tmt-arium-* wireless-infra-vendor scenarios`
7. Save to same path

The 8 scenarios with their briefs and personas (from the approved design):

```python
SCENARIOS = [
    {
        "id": "tmt-arium-ran-fleet-predictive-failure",
        "title": "RAN-fleet predictive failure (vendor-side)",
        "brief": "Arium ships ~120,000 deployed radios across 14 carrier customers. Pre-failure signatures in vendor telemetry (PSU degradation, fan vibration, thermal drift) are visible weeks before carrier alarms but currently sit in supplier portals nobody monitors. 60% of field tickets are reactive; pre-emptive swap rate sits at 14%.",
        "kpi": "Predicted-failure capture +62% · pre-emptive swap rate 14% → 71% · carrier SLA credits −$8.4M/yr",
        "persona": "Primary Lena Park · Vendor Field Operations Lead Approves pre-emptive swap dispatch via Teams Adaptive Card.",
    },
    {
        "id": "tmt-arium-field-service-dispatch-optimization",
        "title": "Field-service dispatch optimization (tower & site crews)",
        "brief": "Vendor field-service crews (~340 across NA) currently routed by static zone with daily manual reshuffle. Weather, tower lease-window, parts-availability, and skills-mix are not jointly optimized. 23% of tickets get re-rolled due to wrong-skill or wrong-parts dispatch.",
        "kpi": "First-time-fix rate 71% → 89% · drive-hours per ticket −24% · ticket re-roll rate −67%",
        "persona": "Primary Marcus Owusu · Regional Dispatch Manager Approves overnight route + crew assignments via Teams Adaptive Card.",
    },
    {
        "id": "tmt-arium-spare-parts-depot-rebalance",
        "title": "Spare-parts depot rebalance (swap-stock positioning)",
        "brief": "18 regional depots hold $94M in swap stock; positioning lags carrier deployment plans by 6+ weeks, driving asset-on-ground (AOG) wait of 4.2 days against a 24h SLA target. Carrier credit exposure from AOG breaches runs ~$3M/yr.",
        "kpi": "AOG wait 4.2d → 18h · swap-stock holding cost −19% · SLA credits −$3.1M/yr",
        "persona": "Primary Aniela Korpacz · Supply Chain Director Approves inter-depot transfers above $250k threshold via Teams Adaptive Card.",
    },
    {
        "id": "tmt-arium-firmware-release-orchestration",
        "title": "Firmware-release orchestration (staged rollout across carriers)",
        "brief": "Quarterly RAN firmware drop touches ~120,000 radios across 14 carriers; rollouts coordinated via spreadsheets; canary-cohort telemetry reviewed manually. One bad 2024 rollout cost $11M in SLA credits before rollback completed.",
        "kpi": "Mean time-to-rollback 96h → 9h · canary-cohort coverage 31% → 100% · rollback-attributed SLA loss −82%",
        "persona": "Primary Hiroshi Tanaka · RAN Software Release Manager Approves go / hold gates at each ring of staged rollout via Teams Adaptive Card.",
    },
    {
        "id": "tmt-arium-site-energy-attribution",
        "title": "Site-energy attribution & Scope-3 reporting (per-carrier)",
        "brief": "Carrier customers under SBTi pressure are requiring verified Scope-3 site-energy attribution from vendors (per-cell, per-carrier, per-vendor-equipment-tranche). Current spreadsheet method takes 11 weeks per carrier and is non-auditable for CDP / SBTi disclosures.",
        "kpi": "Time-to-attest 11 wk → 4 days · 100% carriers covered · audit-ready CDP / SBTi disclosure packets",
        "persona": "Primary Eleni Vasilakis · Sustainability & Carrier Reporting Lead Approves attestation packets pre-disclosure via Teams Adaptive Card.",
    },
    {
        "id": "tmt-arium-carrier-sla-breach-prediction",
        "title": "Carrier-SLA-breach prediction & credit-liability exposure",
        "brief": "Arium administers ~480 SLA contracts with carriers; credit exposure is measured monthly in arrears via spreadsheet rollup; finance has no forward view, so ~$19M/yr in credits hit P&L unexpectedly. CFO has flagged unplanned credit write-offs as the top forecasting reliability issue.",
        "kpi": "SLA-breach forecast accuracy +73% · unplanned credit write-offs −58% · CFO forecast-confidence rating +2.3 pts",
        "persona": "Primary Renata Oviedo · VP Customer Operations Approves carrier-credit advisories and remediation playbooks via Teams Adaptive Card.",
    },
    {
        "id": "tmt-arium-warranty-rma-cluster-detection",
        "title": "Warranty / RMA cluster detection (field-failure root cause)",
        "brief": "18,500 RMAs/year trickle in via free-text carrier portals across 14 customers; failure patterns (component lot, firmware revision, climate-zone, install-cohort) are only spotted retrospectively in quarterly engineering reviews. Mean time to detect a cluster is 11 weeks.",
        "kpi": "Time-to-cluster detection 11 wk → 6 days · warranty cost −24% · supplier-charge-back recoveries +$4.7M/yr",
        "persona": "Primary Imani Becquerel · Reliability Engineering Lead Approves cluster verdicts that trigger field bulletins and supplier charge-backs via Teams Adaptive Card.",
    },
    {
        "id": "tmt-arium-private-5g-opportunity-scoring",
        "title": "Private-5G enterprise-opportunity scoring",
        "brief": "Arium's private-5G pipeline at Fortune 2000 manufacturers, ports, and mining accounts is 1,800 prospects deep but BD currently ranks by gut feel. 38% of pilots fail at site-survey gate because RF environment, spectrum availability, or load-profile was misjudged at qualification.",
        "kpi": "Pilot-to-deployment conversion 41% → 68% · BD time per prospect −51% · win-rate at site-survey gate +27 pts",
        "persona": "Primary Aleksey Drozdov · Enterprise 5G Practice Lead Approves prospect prioritization and site-survey green-lights via Teams Adaptive Card.",
    },
]
```

For the 24-Step Chain template, harvest the rows from `tmt-network-fault-prediction` (already in the workbook) as the canonical source — copy each `Purpose` and `What APEX Does` string verbatim except where the SOR / Event step references the specific scenario (steps 1, 11, 12 mention SOR and the named event respectively). Substitute:
- Step 1: SOR description stays `"SOR: OSS/BSS + Probe + Alarm mgmt + Vendor telemetry"` (extended for vendor-side context)
- Step 11: Event title = `"{Title} · Event Fires"`
- Per-row `Scenario Note`: tailored using scenario brief / KPI / persona per the existing pattern

**Step 2: Run the script**

```powershell
python docs/reference/_add_arium_scenarios.py
```

Expected: clean exit, "Wrote 8 scenarios, 8 SK rows, 192 24-step rows, summary updated"

---

## Task 3: Verify row counts post-write

**Step 1: Re-check sheet sizes**

Run same probe as Task 1 Step 1.

Expected:
```
Scenario Library 754       # 746 + 8
Scenario→KPI Chain 754
24-Step Chain 17569        # 17377 + 192
```

If counts diverge, abort and inspect.

---

## Task 4: Recalculate and scan for errors

**Step 1: Run recalc.py**

```powershell
python C:\Users\kmarkham\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\54bdf8ea-c5bf-49e3-a357-7a91819a8c8c\fe8c9548-1bbd-402e-82a3-2fc7f82f874f\skills\xlsx\scripts\recalc.py docs/reference/APEX-Scenario-Chains.xlsx 60
```

Expected: JSON with `"status": "success"` and `"total_errors": 0`. If `errors_found`, inspect locations and fix.

---

## Task 5: Spot-check two scenarios end-to-end

**Step 1: Pull all rows for `tmt-arium-ran-fleet-predictive-failure` and `tmt-arium-private-5g-opportunity-scoring` across all four sheets**

```powershell
python -c "import sys,io; sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8'); import openpyxl; wb=openpyxl.load_workbook(r'docs/reference/APEX-Scenario-Chains.xlsx', read_only=True, data_only=True); 
for sid in ['tmt-arium-ran-fleet-predictive-failure','tmt-arium-private-5g-opportunity-scoring']:
    for s in wb.sheetnames:
        sh=wb[s]; rows=[r for r in sh.iter_rows(values_only=True) if r and any(c==sid for c in r if isinstance(c,str))]
        print(f'{sid} / {s}: {len(rows)} rows')"
```

Expected:
- Scenario Library: 1 each
- Scenario→KPI Chain: 1 each
- 24-Step Chain: 24 each
- Featured Chains: 0 each
- Summary: 0 each

---

## Task 6: Commit

**Step 1: Stage and commit**

```powershell
git add docs/reference/APEX-Scenario-Chains.xlsx docs/reference/_add_arium_scenarios.py docs/plans/2026-05-14-arium-tmt-scenarios-design.md docs/plans/2026-05-14-arium-tmt-scenarios.md
git status
```

Confirm staged files match expected set, then:

```powershell
git commit -m @'
docs(arium): add 8 tmt-arium-* wireless-infra-vendor scenarios

Fills the wireless-infra-vendor gap in TMT Network & Infrastructure
(catalog previously written from carrier seat only). Net-new catalog
entries reusable across Ericsson, Nokia, Samsung Networks, Mavenir,
CommScope.

- Scenario Library: +8 rows (745 → 753)
- Scenario→KPI Chain: +8 rows
- 24-Step Chain: +192 rows (17376 → 17568)
- Summary: v1.5 → v1.6

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
'@
```

---

## Out of scope (do NOT do in this plan)

- Featured Chains rows for any Arium scenario
- Updates to APEX-Stacked-Architecture-Narrated.html or other source files
- New service code (e.g., TMT-TEL-NET-05)
- Real Arium executive name substitution (personas are placeholders)
