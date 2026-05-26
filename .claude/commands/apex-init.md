---
description: Initialize a RAPIDS-driven APEX work item. Detects context and offers APEX archetypes.
---

You are starting a new APEX work item using the RAPIDS methodology.

## Steps
1. Read `.rapids/triage/apex-detector.yaml` and determine current context.
2. Based on context, present the priority archetypes from `.rapids/archetypes/`.
3. Ask the user to select an archetype.
4. Load the chosen archetype YAML + corresponding workflow from `.rapids/workflows/`.
5. Begin the 6-phase walk (Research → Analysis → Plan → Implement → Deploy → Sustain).
6. For each phase:
   - Invoke the specialist agents listed in the workflow.
   - Produce the artifacts required by `.rapids/governance/phase-gates.yaml`.
   - Pause at the governance gate · confirm with user before proceeding.
7. After Sustain, generate the Operate handoff package.

## Behaviour
- Be explicit about which phase you are in.
- Always show which agent you are about to invoke and why.
- Always show artifact paths created.
- Never skip a governance gate; ask for explicit user override if needed.
- After each phase, summarize what was produced and what's queued for review.
