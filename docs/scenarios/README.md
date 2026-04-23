# APEX Scenario Library

On-disk catalog of APEX scenarios, organized by **Practice** then by **functional domain**. 736 scenario folders across 7 Practices and up to 13 domains.

## Practice folders

- **[RC](./RC/)** — Retail & Consumer · 105 scenarios across 11 domains
- **[HLS](./HLS/)** — Health, Life Sciences · 107 scenarios across 13 domains
- **[ER](./ER/)** — Energy & Resources · 104 scenarios across 11 domains
- **[AXLE](./AXLE/)** — Automotive & Manufacturing · 107 scenarios across 11 domains
- **[TMT](./TMT/)** — Technology, Media, Telecom · 109 scenarios across 12 domains
- **[TH](./TH/)** — Travel & Hospitality · 104 scenarios across 12 domains
- **[ICE](./ICE/)** — Industrial, Construction, Equipment · 100 scenarios across 12 domains

## Layout

```
docs/scenarios/
  README.md                            <-- this file
  _catalog/
    scenario-library.json              <-- 723-row compact library
    featured-chains.json               <-- 35 featured chains with full content
    domain-classification.json         <-- title → functional-domain mapping
    by-practice.md                     <-- practice × domain pivot
  <PRACTICE>/                          <-- RC / HLS / ER / AXLE / TMT / TH / ICE
    README.md                          <-- per-domain grouped index
    _browse-catalog.md                 <-- alphabetical cross-domain list
    <domain-slug>/                     <-- functional domain (clinical-care, supply-chain, ...)
      NN-<scenario-slug>/              <-- scenarios (featured first, then alpha)
        README.md                      <-- scenario chain or catalog-level blurb
        tests/ artifacts/ manifests/   <-- build artefact stubs
```

## Functional domains (13)

- **Clinical & Care** (`clinical-care`) — 92 scenarios
- **Network & Infrastructure** (`network-infrastructure`) — 46 scenarios
- **Engineering & R&D** (`engineering-rd`) — 31 scenarios
- **Supply Chain & Inventory** (`supply-chain`) — 83 scenarios
- **Asset, Maintenance & Reliability** (`asset-maintenance`) — 55 scenarios
- **Quality, Compliance & Regulatory** (`quality-compliance`) — 82 scenarios
- **Risk, Fraud & Security** (`risk-fraud-security`) — 27 scenarios
- **Pricing, Revenue & Margin** (`pricing-revenue`) — 40 scenarios
- **Customer Experience & Loyalty** (`customer-experience`) — 83 scenarios
- **Marketing & Growth** (`marketing-growth`) — 39 scenarios
- **Operations & Workforce** (`operations-workforce`) — 63 scenarios
- **Channel, Partner & Dealer** (`channel-partner-dealer`) — 14 scenarios
- **Other / Cross-cutting** (`other`) — 81 scenarios

## Featured scenarios

35 scenarios (5 per Practice) have full Scenario / Solution / Use Case / Service / Persona / KPI chains authored — identified by the ⭐ marker in each Practice's README. The other ~700 are compact catalog entries; promotion happens by authoring the full chain in that folder's README.

## Regenerate

```bash
# 1. Extract + flat build (preserves any hand-edited READMEs)
python scripts/build_scenarios_tree.py

# 2. Re-classify
python scripts/classify_scenarios.py

# 3. Move folders into domain sub-trees
python scripts/reorg_scenarios_by_domain.py

# 4. Rebuild indexes (run any time to refresh from the filesystem)
python scripts/rebuild_scenario_indexes.py
```
