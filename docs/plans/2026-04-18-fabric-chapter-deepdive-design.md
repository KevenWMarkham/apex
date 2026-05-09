# Design: Fabric Chapter Deep-Dive Expansion (Professional-APEX-M.html)

**Date:** 2026-04-18
**Author:** APEX working session
**Status:** Approved — proceeding to implementation
**Target:** `docs/book/Professional-APEX-M.html` Chapter 8 (Fabric Layering)

## Purpose

Expand Chapter 8 of the architect book into the comprehensive Fabric architecture,
capabilities, medallion, SOR integration, schema-mapping, and implementation
reference. Scope driven by user request across four prompts:

1. Layout Fabric architecture, details of capabilities, medallion deep-dive on Fabric SaaS, setup/implementation walkthrough.
2. Deep dive on external SOR connections, REST API integration, multiple SOR examples, view refresh patterns, Bronze landing strategies.
3. APEX schema usage in Fabric, source-to-canonical mapping, classification, pre/post-measure calculations, agent-alignment.

## Constraints

- Placement: expand Chapter 8 only (existing Ch 9 Medallion remains focused on APEX-specific semantic model; overlap minimized via cross-references).
- Implementation depth: full — PowerShell, REST API, Terraform, T-SQL, PySpark, KQL samples.
- Medallion focus: APEX-specific (SCML, MERML, CXML semantic models as Silver).
- Audience: senior data architect with Fabric exposure.
- Independence language preserved throughout ("leverages Microsoft technology platform" etc.).

## Final Section Layout

```
§ TL;DR                                              (existing)
§ 1. Fabric Architecture                             (NEW)
§ 2. Capabilities Matrix                             (NEW)
§ 3. Fabric Surface APEX Uses                        (existing, renumbered)
§ 4. Workspace Topology                              (existing, renumbered)
§ 5. APEX on Fabric                                  (existing, renumbered)
§ 6. Identity & Access                               (existing, renumbered)
§ 7. Medallion on Fabric SaaS — Deep Dive            (NEW)
§ 8. SOR Integration Strategies — Deep Dive          (NEW)
§ 9. APEX Schemas in Fabric — Mapping, Canonical Views, Agent Alignment  (NEW)
§ 10. Implementation Walkthrough                     (NEW)
§ 11. Fabric Gotchas                                 (existing, renumbered)
§ 12. Worked Example — New Tenant                    (existing, renumbered)
§ 13. Cross-references                               (existing, renumbered)
```

## Section Depth

- §1 Fabric Architecture (~3,500 words): SaaS data-platform model, capacity and F-SKU family, OneLake internals, workload engines (Lakehouse / Warehouse / Eventhouse / Data Factory / RTI / Activator), query-path triangle (Import / DirectQuery / Direct Lake), shortcuts / mirroring / cross-cloud federation, Fabric-Azure-M365 integration fabric.
- §2 Capabilities Matrix (~2,500 words): six tables across Ingest, Storage, Transform, Serve, Governance, Observability.
- §7 Medallion Deep Dive (~6,000 words): medallion as contract, Bronze landing five patterns in depth, Silver with APEX semantic models, Gold materialization strategies, refresh patterns, Purview propagation, reference DDL.
- §8 SOR Integration (~8,000 words): decision matrix, REST / database / event-bus / file-based patterns, 15 worked SOR examples (Epic, SAP, Salesforce, Manhattan, Workday, ServiceNow, PI, Proficy, AS/400, Adobe Analytics, SFMC, HL7/FHIR, Ariba, Oracle EBS, Snowflake/Databricks), on-premises connectivity, refresh orchestration, connection security.
- §9 APEX Schemas (~6,500 words): schemas in the manifest model, structure, registration, source-to-canonical mapping, classification taxonomy, pre- vs post-measure calculations, agent-alignment patterns, Practice-semantic-model binding walkthrough.
- §10 Implementation Walkthrough (~4,500 words): pre-reqs, Terraform bootstrap, PowerShell Az.Fabric, REST API, OneLake ACLs, workload provisioning, shortcuts / mirroring / CDC, Purview scanning, CI/CD via Deployment Pipelines + Git, validation.

**Total new content: ~31,000 words / ~55–65 pages.**

## Implementation Notes

- All new content authored as inline HTML with existing chapter styling (callouts, code blocks, tables).
- Inserted directly into `docs/book/Professional-APEX-M.html` before the existing gotchas / worked-example / cross-references sections.
- Existing section IDs preserved where practical to avoid breaking anchor links.
- Independence-compliant language throughout: "leverages Microsoft platform", no "partner / alliance / joint venture" usage.

## Success Criteria

- Chapter 8 becomes the anchor architect reference for Fabric in the book.
- Senior architect can design a Wave 1 Fabric tenant topology from this chapter alone.
- Data engineer can author the Bronze → Silver → Gold pipeline from the implementation walkthrough.
- SOR integration approach for any of the 15 profiled SORs is directly implementable.
- Schema / classification / pre- and post-measure / agent-alignment discipline understood end-to-end.

## Out of Scope

- Rewriting Chapter 9 (Medallion & SOR Integration) — retains its APEX-specific semantic model focus.
- Changes to other chapters' anchor IDs.
- New appendices.

## Proceed Plan

Implement in six batches corresponding to the six new sections, writing each as an HTML block and inserting before `<h2 id="3-8-5-fabric-specific-gotchas-the-list-that-will-save-your-t">`. Rebuild verification not required since the file is direct HTML (no build step for architect book).
