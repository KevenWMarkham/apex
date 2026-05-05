# Design: Agent Orchestration Deep-Dive + Orchestration Catalog Per Schema

**Date:** 2026-04-18
**Status:** Approved — proceeding to implementation
**Target:** Sellers Guide §6.9 (Chapter 6) + new Appendix W

## Scope

Three deliverables approved:

1. **§6.9 "Agent Orchestration Deep-Dive"** — new section in Chapter 6 (Foundry), ~3,500 words, 10 subsections
2. **Appendix W "Orchestration Catalog — Per Schema"** — ~150 orchestration entries across all 7 Practices, ~15,000-18,000 words
3. **Appendix V glossary updates** — orchestration terminology

Total: ~20,000 words new content.

## Structure

### §6.9 Agent Orchestration Deep-Dive (Chapter 6)

- 6.9.1 What orchestration is (and isn't)
- 6.9.2 The four primitive orchestration patterns (Sequential / Parallel / Hierarchical / Feedback)
- 6.9.3 The 47 APEX orchestration patterns
- 6.9.4 The orchestration manifest
- 6.9.5 HITL gates as orchestration checkpoints
- 6.9.6 How orchestration ties back to APEX — acceleration story
- 6.9.7 Concrete example: RC recall orchestration (Store 100 Event 05)
- 6.9.8 Concrete example: HLS sepsis early-warning
- 6.9.9 Orchestration's relationship to the envelopes
- 6.9.10 Architect conversation template

Mermaid diagram for the four primitive patterns.

### Appendix W — Orchestration Catalog Per Schema

Per-orchestration template (6-field):
- Description
- Primary schema / Related schemas
- Action invoked
- Data used
- HITL pattern
- Trigger

Coverage:
- W.1 How to read
- W.2 RC (SCML + MERML + CXML)
- W.3 HLS (Payer + Provider + Life Sciences)
- W.4 ER (UOG + P&U + Mining)
- W.5 AXLE (AXLEML sub-models; cross-ref §12.9 for AXLE framework 10 orchestrations)
- W.6 TMT (TEC + MED + TEL)
- W.7 TH
- W.8 ICE
- W.9 Cross-Practice orchestrations
- W.10 The 47 pattern count decomposition summary

Target ~150 specific orchestration entries.

### Appendix V glossary additions

- Orchestration (general)
- Orchestration Manifest
- Orchestration Pattern
- Sequential / Parallel / Hierarchical / Feedback Orchestration
- Primitive Pattern

## Implementation Batches

1. §6.9 deep-dive (this batch)
2. W.1 intro + W.2 RC (~20 orchestrations)
3. W.3 HLS (~25 orchestrations)
4. W.4 ER (~20 orchestrations)
5. W.5 AXLE + W.6 TMT (~30 orchestrations)
6. W.7 TH + W.8 ICE (~20 orchestrations)
7. W.9 Cross-Practice + W.10 Pattern decomposition + glossary + rebuild

## Independence posture

Consistent with established framing:
- APEX orchestration patterns are Deloitte IP, internal accelerator
- Client receives orchestrated agent fleets on their Microsoft platform
- No "APEX orchestration product" language — use "Deloitte-delivered orchestration patterns"

## Success Criteria

- Architect asks "how do agents compose" → seller points to §6.9
- Architect asks "what orchestrations exist for retail inventory" → seller points to W.2.1 SCML orchestrations
- Client CFO asks "what am I buying in Wave 2" → orchestration count maps to delivery effort through the catalog
