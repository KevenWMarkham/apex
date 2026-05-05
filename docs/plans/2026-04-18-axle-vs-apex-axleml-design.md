# Design: AXLE Framework vs APEX AXLE Practice (AXLEML) — Sellers Guide Deep-Dive

**Date:** 2026-04-18
**Status:** Approved — proceeding to implementation
**Target:** Sellers Guide Chapter 12 (Industrial & Manufacturing — AXLE Practice)

## Purpose

Add an honest, positioning-focused comparison of the two DMTSP frameworks to the
sellers guide so APEX sellers can navigate pursuit conversations where a client or
Microsoft field counterpart references the AXLE framework. Both are Deloitte
DMTSP IP; the comparison is about scope and usage, not competitive displacement.

## Source of Truth

**AXLE framework reference document:** `C:\Stage\Clients\Industries\Automotive\AXLE\docs\AXLE-Comprehensive-Solutions-Reference-v3.docx` (v1.0 April 2026).

Extracted key facts from that document:
- AXLE = Automotive eXchange Layer for Enterprise
- Purpose-built for automotive manufacturing
- 9 canonical ML schemas: AAML, QEML, PDML, SCML, WOSFML, DTML, CVML, ESML, WLML
- 6 reference architecture layers (Ingestion, Storage, Processing, Intelligence, Orchestration, Presentation)
- 10 agentic orchestrations (ORCH-01 through ORCH-10)
- 7 MCP servers, ~60 tools
- Built on Microsoft Fabric + Azure AI Foundry + MCP, medallion architecture
- Wave 1: $2-4M, single reference plant, 4 months; total pipeline opportunity $107-230M

## Framing

AXLE and APEX are **sibling DMTSP frameworks**, not competing IP:
- AXLE: deep automotive-manufacturing vertical specialist
- APEX: broad cross-Practice agentic decision-automation framework with 7 Practices
- AXLEML: APEX's canonical semantic model for the AXLE Practice 
  (Automotive + Aerospace + Industrial Products + Discrete Manufacturing)
- Both leverage Microsoft Fabric + Foundry + Purview + Entra; both use medallion; both use MCP

## Section Layout (approved)

§12.9 AXLE Framework vs APEX AXLE Practice (AXLEML) — Sibling Frameworks, Complementary Positioning

- 12.9.1 Two frameworks, one DMTSP — what each is
- 12.9.2 The 9 AXLE canonical ML schemas (AAML/QEML/PDML/SCML/WOSFML/DTML/CVML/ESML/WLML)
- 12.9.3 AXLEML — APEX's unified semantic model for AXLE Practice
- 12.9.4 Structural differences — depth vs breadth
- 12.9.5 When to lead with AXLE framework
- 12.9.6 When to lead with APEX AXLE Practice
- 12.9.7 When to combine both — federated pattern
- 12.9.8 Positioning comparison table
- 12.9.9 Seller positioning scripts
- 12.9.10 Independence considerations

## Depth

~3,500-4,000 words. Anchor content: the 9-schema table (§12.9.2), the positioning matrix
(§12.9.8), and the seller scripts (§12.9.9).

## Placement Rationale

In the sellers guide: Chapter 12 (AXLE Practice) — immediately after §12.8 objection
patterns. Sellers look for AXLE-specific material in Ch 12; placing the comparison
there keeps navigation natural.

## Success Criteria

- APEX sellers can field "why APEX when AXLE already exists" without sounding
  defensive or sounding like they do not know AXLE.
- Sellers can recommend AXLE vs APEX vs both based on client scope.
- No Independence risk from mischaracterising the relationship between the frameworks.
- Federated-coexistence pattern explained so neither framework is positioned as
  displacing the other.

## Out of Scope

- Updating the AXLE framework document itself.
- Creating a new chapter in the architect book (may happen in a separate design).
- Cross-references between AXLE-framework-specific tooling and APEX manifests.
