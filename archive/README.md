# APEX Archive

**Purpose:** Historical artifacts that have been superseded or whose deliverables have shipped, preserved as a decision record. Nothing in this folder is on the active sprint path defined by `APEX - Design and Build/Orchestrator.md`.

**Created:** 2026-04-19

## Structure

```
archive/
├── amendments/              — superseded L1 Core amendments
├── lock-files/              — stale editor lock files (Excel ~$, etc.)
└── completed-design-plans/  — design plans whose deliverables have shipped
```

## Contents & Rationale

### `amendments/`

| File | Why archived |
|------|--------------|
| `apex-core-v1.1-amendment.md` | Superseded by `apex-core-v1.2-amendment.md` at repo root |

### `lock-files/`

(Empty unless Excel lock files are moved here after the parent file is closed.)

### `completed-design-plans/`

All of these designs have been delivered as shipped artifacts in the repository. The plan itself is retained as a decision record but is no longer an input to any pending Orchestrator sprint.

| Plan | Delivered as |
|------|--------------|
| `2026-04-17-schema-versioning-manifest-design.md` | `apex-core-v1.2-amendment.md` + `apex-core/conventions/schema-versioning.md` + `apex-core/data/schema-manifest-contract.json` |
| `2026-04-17-schema-versioning-manifest-implementation.md` | Same as above; implementation plan now complete |
| `2026-04-17-store-100-facilitator-guide-design.md` | `docs/APEX-Store-100-facilitator-guide.{md,docx}`; later superseded by the 04-18 repositioning plan |
| `2026-04-18-apex-repositioning-store100-design.md` | Updated facilitator guide and Store-100-as-Big-Box-Store framing (Sprint 18.1 of Orchestrator) |
| `2026-04-18-apex-sellers-guide-design.md` | `docs/book/Professional-APEX-Sellers-Guide.html` |
| `2026-04-18-developer-implementation-guide-design.md` | `docs/APEX-developer-guide.md` + `docs/APEX-developer-implementation-guide.docx` + `docs/dev-guide/` chapters |
| `2026-04-18-professional-apex-book-design.md` | `docs/book/Professional-APEX.html` |

## Plans **not** archived (still active sprint inputs)

For the avoidance of doubt, these design plans remain in `docs/plans/` because they are inputs to pending Orchestrator sprints:

- `2026-04-17-rc-agent-catalog-design.md` → Sprint 16.1 (RC agent catalog)
- `2026-04-18-apex-mcp-tools-appendix-i-design.md` → Sprint 7–9 (MCP servers) + Sprint 19 (Appendix F)
- `2026-04-18-apex-schemas-appendix-h-design.md` → Sprints 2–3 (canonical schemas) + Sprint 19 (Appendix A)
- `2026-04-18-axle-vs-apex-axleml-design.md` → Sprint 3.3 (AXLE schemas)
- `2026-04-18-developer-implementation-guide.md` → Sprint 19 (developer guide publication)
- `2026-04-18-fabric-chapter-deepdive-design.md` → Sprints 4–6 (medallion) + Sprint 14 (Fabric capacity)
- `2026-04-18-orchestration-deep-dive-and-catalog-design.md` → Sprint 11 (orchestration + HITL)
- `2026-04-18-purview-appendix-k-design.md` → Sprint 13 (Purview) + Sprint 19 (Appendix K)

## Restoring a file from archive

If a file was archived in error, move it back to its original location. Paths:

```
archive/amendments/apex-core-v1.1-amendment.md  →  /apex-core-v1.1-amendment.md
archive/completed-design-plans/*                 →  /docs/plans/*
```
