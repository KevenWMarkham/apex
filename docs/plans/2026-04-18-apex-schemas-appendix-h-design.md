# Design: APEX Schemas, Entities, and Agent Consumption — Sellers Guide Appendix H

**Date:** 2026-04-18
**Status:** Approved — proceeding to implementation
**Target:** Sellers Guide new Appendix H

## Purpose

Provide sellers with a comprehensive reference for APEX canonical schemas, their
entities, how SOR data maps into each entity, how agents consume the entities to
produce decisions, and how entities combine for situation assessment.

## Coverage

All 7 APEX Practices:

- H.2 Retail & Consumer (RC): SCML, MERML, CXML
- H.3 Healthcare & Life Sciences (HLS): Payer, Provider, Life Sciences schemas
- H.4 Energy & Resources (ER): UOG, P&U, Mining schemas
- H.5 Industrial & Manufacturing (AXLE): AXLEML sub-models + AXLE framework cross-ref
- H.6 Technology, Media & Telecom (TMT): TEC, MED, TEL schemas
- H.7 Travel & Hospitality (TH): TravelerML, OpsML, Loyalty/Revenue schemas
- H.8 Industrial & Commercial Equipment (ICE): Equipment, Dealer, Aftermarket, Rental

## Per-entity Template (5 parts, ~150 words each)

1. Description — what the entity represents
2. SOR mapping — source systems and ingestion pattern
3. Agent decision use — how agents query and reason over it
4. Situation assessment — how it combines with other entities
5. Example decisions — concrete decision types it informs

## Closing Sections

- H.9 Cross-Practice entity patterns (Customer, Asset, Workforce, Supplier)
- H.10 Five standard agent query patterns (entity-read, entity-search, cross-entity-join, temporal-window, cross-Practice federation)
- H.11 Five situation-assessment patterns (threshold-breach, pattern-match, correlation, anomaly, scenario)

## Volume

~120 entities × ~150 words = ~18,000 words. Plus ~2,000 words for cross-Practice
and agent-query/situation-assessment patterns. Total ~20,000 words.

## Independence compliance

- "Leverages Microsoft technology platform" language throughout
- No "partner" / "alliance" / "joint venture"
- Cross-references to AXLE framework's 9 schemas (already in §12.9) rather than re-describing
- Entity names for APEX AXLEML use sub-model prefix to disambiguate from AXLE framework
  (e.g., AXLEML.Manufacturing.WorkOrder vs AXLE.AAML.CycleEvent)

## Implementation batches

1. H.1 intro + H.2 RC + H.3 HLS (first batch)
2. H.4 ER + H.5 AXLE + H.6 TMT (second batch)
3. H.7 TH + H.8 ICE (third batch)
4. H.9-H.11 closing patterns (fourth batch)
5. Rebuild sellers guide

## Success Criteria

- Sellers can find the entity for any pursuit's data question in under 30 seconds
- Each entity description is immediately usable in a pursuit conversation
- Agent decision-use descriptions let sellers explain "how the AI uses this data"
- Situation-assessment descriptions support the "how decisions actually get made" narrative
