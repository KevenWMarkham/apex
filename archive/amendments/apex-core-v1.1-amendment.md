# APEX Core · v1.1 Amendment
## Formal Edition Registry

**Amendment version:** 1.1
**Supersedes:** APEX Core v1.0 (Part 2 edition registry prose)
**Effective:** Upon Claude Code build of this amendment
**Downstream impact:** All edition specs should update their Part 0 inheritance declaration to reference `apex-core v1.1`

---

## Rationale

APEX Core v1.0 documented the edition registry as a prose table in Part 2. With six active editions (RC, TH, HLS, TMT, ER, ICE) and three reserved (FS, LS renamed, PS), the registry needs to be a **machine-readable file that the validation harness reads** — not only a prose reference.

This amendment:
1. Adds `apex-core/data/edition-registry.json` as a canonical artifact
2. Adds a schema contract for edition registry entries
3. Extends the Phase 4 validation harness (`validate-edition.js`) to read the registry
4. Clarifies the edition-split policy introduced informally across editions

No existing edition's content is invalidated. This is an additive amendment.

---

## 1. Edition Registry File

**File:** `apex-core/data/edition-registry.json`

**Shape:**

```json
{
  "schema_version": "1.1",
  "last_updated": "2026-04-17",
  "editions": [
    {
      "code": "RC",
      "full_name": "Retail & Consumer",
      "accent_token_name": "--rc-accent",
      "accent_hex_dark": "#d4a244",
      "accent_hex_light": "#8a6508",
      "status": "active",
      "sub_variants": [],
      "schema_count": 4,
      "agent_count": 34,
      "reserved_orch_slots": [],
      "spec_file": "apex-rc-build-spec-v2.md",
      "folder": "apex-rc/",
      "reference_implementations": [
        { "name": "Store 100 Day-in-the-Shift", "status": "built" }
      ]
    },
    {
      "code": "TH",
      "full_name": "Travel & Hospitality",
      "accent_token_name": "--th-accent",
      "accent_hex_dark": "#2a9d8f",
      "accent_hex_light": "#0f766e",
      "status": "active",
      "sub_variants": ["airline", "cruise", "lodging"],
      "sub_variants_formal": false,
      "schema_count": 4,
      "agent_count": 30,
      "reserved_orch_slots": [],
      "spec_file": "apex-th-build-spec.md",
      "folder": "apex-th/",
      "reference_implementations": [
        { "name": "Property 201 Day-in-the-GM-Seat", "status": "planned" }
      ]
    },
    {
      "code": "HLS",
      "full_name": "Health Care & Life Sciences",
      "accent_token_name": "--hls-accent",
      "accent_hex_dark": "#0891b2",
      "accent_hex_light": "#155e75",
      "status": "planned",
      "sub_variants": ["PRV", "LS"],
      "sub_variants_formal": true,
      "schema_count": 5,
      "agent_count": 34,
      "reserved_orch_slots": [],
      "spec_file": "apex-hls-build-spec.md",
      "folder": "apex-hls/",
      "reference_implementations": [
        { "name": "Memorial 4-West Day-in-the-Unit", "sub_variant": "PRV", "status": "planned" },
        { "name": "Trial ATLAS-3 Day-in-Operations", "sub_variant": "LS", "status": "planned" }
      ]
    },
    {
      "code": "TMT",
      "full_name": "Technology, Media & Telecom",
      "accent_token_name": "--tmt-accent",
      "accent_hex_dark": "#8b5cf6",
      "accent_hex_light": "#5b21b6",
      "status": "planned",
      "sub_variants": ["TEL", "MED", "TEC"],
      "sub_variants_formal": true,
      "schema_count": 5,
      "agent_count": 30,
      "reserved_orch_slots": ["ORCH-03"],
      "spec_file": "apex-tmt-build-spec.md",
      "folder": "apex-tmt/",
      "reference_implementations": [
        { "name": "Carrier NOC Day-in-the-Console", "sub_variant": "TEL", "status": "planned" },
        { "name": "Streaming Platform Operations Day", "sub_variant": "MED", "status": "planned" },
        { "name": "SaaS Tenant Success Day", "sub_variant": "TEC", "status": "planned" }
      ]
    },
    {
      "code": "ER",
      "full_name": "Energy & Resources",
      "accent_token_name": "--er-accent",
      "accent_hex_dark": "#ea580c",
      "accent_hex_light": "#9a3412",
      "status": "planned",
      "sub_variants": ["OG", "PU", "MN"],
      "sub_variants_formal": true,
      "schema_count": 5,
      "agent_count": 32,
      "reserved_orch_slots": ["ORCH-03", "ORCH-11"],
      "spec_file": "apex-er-build-spec.md",
      "folder": "apex-er/",
      "reference_implementations": [
        { "name": "Offshore Platform Charlie Day-in-OIM-Seat", "sub_variant": "OG", "status": "planned" },
        { "name": "Control Center Gamma Day-in-Ops", "sub_variant": "PU", "status": "planned" },
        { "name": "Mine Site Delta Day-in-Ops", "sub_variant": "MN", "status": "planned" }
      ]
    },
    {
      "code": "ICE",
      "full_name": "Industrial & Commercial Equipment",
      "accent_token_name": "--ice-accent",
      "accent_hex_dark": "#0f766e",
      "accent_hex_light": "#134e4a",
      "status": "planned",
      "sub_variants": [],
      "sub_variants_formal": false,
      "sub_variant_candidates": ["HVY", "AD", "AUT"],
      "schema_count": 5,
      "agent_count": 32,
      "reserved_orch_slots": ["ORCH-03", "ORCH-09"],
      "spec_file": "apex-ice-build-spec.md",
      "folder": "apex-ice/",
      "reference_implementations": [
        { "name": "Dealer Site Bravo Day-in-the-Service-Manager-Seat", "status": "planned" }
      ]
    },
    {
      "code": "FS",
      "full_name": "Financial Services",
      "accent_token_name": "--fs-accent",
      "accent_hex_dark": "#4f46e5",
      "status": "reserved",
      "sub_variant_candidates": ["BNK", "INS", "IM"]
    },
    {
      "code": "PS",
      "full_name": "Public Sector",
      "accent_token_name": "--ps-accent",
      "accent_hex_dark": "#0369a1",
      "status": "reserved",
      "sub_variant_candidates": ["FED", "SLG"]
    }
  ]
}
```

---

## 2. Registry Entry Schema Contract

Required fields for every registry entry:

| field | type | required | description |
|---|---|---|---|
| code | string (2–3 uppercase chars) | yes | Stable edition identifier |
| full_name | string | yes | Human-readable name |
| accent_token_name | string | yes | CSS custom property name |
| accent_hex_dark | hex | yes | Accent color for dark theme |
| accent_hex_light | hex | for active/planned | Accent color for light theme |
| status | enum | yes | `active` \| `planned` \| `reserved` \| `deprecated` |
| sub_variants | array of strings | yes | Formal sub-variants (may be empty) |
| sub_variants_formal | boolean | when sub_variants present | True = tagged across spec; False = descriptive only |
| sub_variant_candidates | array of strings | optional | Future sub-variants under consideration |
| schema_count | integer | for active/planned | Number of canonical schemas |
| agent_count | integer | for active/planned | Number of agents in fleet |
| reserved_orch_slots | array | for active/planned | ORCH slots deliberately unused |
| spec_file | string | for active/planned | Path to edition spec |
| folder | string | for active/planned | Edition folder path |
| reference_implementations | array of objects | for active/planned | List of ref-impls |

---

## 3. Updated Validation Harness

**File:** `apex-core/tools/validate-edition.js`

**New behavior (v1.1):**

1. Reads `apex-core/data/edition-registry.json`
2. For an edition passed as argument (e.g., `validate-edition apex-rc/`):
   - Locates the registry entry by matching folder path
   - Validates that the edition's own files match registry metadata:
     - Schema count matches `schema_count`
     - Agent count matches `agent_count`
     - Accent token exists with correct name in edition CSS
     - All declared reference implementations exist as subfolders
   - Validates the 13 Core Part 11 acceptance criteria as before
3. For cross-edition validation (e.g., `validate-registry`):
   - Reads all entries, confirms no duplicate codes
   - Confirms no accent token name collisions
   - Confirms no accent hex collisions within theme
   - Reports any editions in the registry without a corresponding folder
   - Reports any edition folders without a registry entry

---

## 4. Edition-Split Policy (Formalized)

Two industries justify **separate editions** when **all four** of these tests are true:

1. **Operational vocabulary diverges materially** — different nouns, different verbs in day-to-day operations
2. **Regulatory floor diverges materially** — different regulatory frameworks govern core operations
3. **Schema grain diverges materially** — the canonical entities and their grains are not compatible
4. **Primary user personas diverge materially** — the executives and operators who consume the framework are different

If fewer than all four diverge, the split is a **sub-variant** within one edition.

### Sub-variant formality

Sub-variants come in two flavors:

- **Formal sub-variants (`sub_variants_formal: true`)** — tagged on every agent, orchestration, and schema entity; rendered via filters in the framework site. Examples: HLS-PRV vs HLS-LS; TMT-TEL vs TMT-MED vs TMT-TEC; ER-OG vs ER-PU vs ER-MN.
- **Informal sub-variants (`sub_variants_formal: false`)** — descriptive only; no tagging required. Examples: TH airline vs cruise vs lodging (handled via specialized dimensional anchors and tool prefixes).

An edition can promote informal sub-variants to formal via a Core amendment — this is a schema change, not silent refactoring.

### Promoting a sub-variant to its own edition

If a sub-variant's pursuit volume and structural divergence grows, it may be promoted to its own edition:

1. Amend Core to add the new edition code to the registry
2. Fork the relevant content from the parent edition into a new edition spec
3. Update the parent edition spec to remove the sub-variant
4. Update `CHANGELOG.md` with the rationale

Known candidates worth monitoring for future promotion:
- **TMT-TEC** → possible future `APEX-TEC` (Technology) if enterprise tech pursuits dominate
- **ICE-AD** → possible future `APEX-AD` (Aerospace & Defense) if regulatory / export posture diverges further

---

## 5. Downstream Spec Updates Required

Every active edition spec should update its Part 0 Inheritance Declaration line:

**Before:**
> This spec inherits from APEX Core v1.0.

**After:**
> This spec inherits from APEX Core v1.1.

And add a reference to the edition registry:

> **Registry entry:** `apex-core/data/edition-registry.json` — see entry with `code: "<CODE>"`

This is a one-line change per edition spec (RC, TH, HLS, TMT, ER, ICE).

---

## 6. Handoff Notes to Claude Code

**Build sequence for this amendment:**

1. Write `apex-core/data/edition-registry.json` with the exact content in section 1 above
2. Update `apex-core/README.md` (the Core spec) to reference the new registry file in Part 2 with a pointer to the JSON
3. Extend `apex-core/tools/validate-edition.js` to the v1.1 behavior in section 3
4. Add `apex-core/tools/validate-registry.js` for cross-edition validation
5. Update each active edition spec's Part 0 inheritance declaration (6 files, one-line change each)
6. Update `apex-core/CHANGELOG.md` with this amendment

No existing content is invalidated. All edition specs remain valid under v1.1 once the one-line inheritance declaration is updated.

---

**End of APEX Core v1.1 Amendment**
