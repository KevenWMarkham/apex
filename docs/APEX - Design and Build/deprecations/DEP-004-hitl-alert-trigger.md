# DEP-004 · Custom HITL alert trigger → Eventstream Activator destination

**Status:** Deprecated
**Date:** 2026-05-09
**Supersedes:** Roadmap.md BL.P.74 (Teams card integration) HITL trigger path

## What APEX was building

Custom code in the agent runtime to detect "decision exceeds threshold" conditions and fire a Teams Adaptive Card to the HITL approver — runtime emits an event, custom subscriber translates to a Teams webhook call, custom retry / escalation logic.

## What Microsoft shipped

In **November 2025**, Fabric Eventstream shipped **Activator destination** (GA):

- [Eventstream Activator destination](https://learn.microsoft.com/fabric/real-time-intelligence/event-streams/add-destination-activator)

> *"With Eventstream Activator destination, you can detect important patterns in your live data and trigger the right action automatically — no code required."*

Activator natively supports Teams, Email, Power Automate, and custom HTTP endpoints as actions; threshold detection lives in the rule expression; escalation policies are first-class.

## Migration path

1. Move the "if score > X" / "if markdown > 30%" decision threshold from agent runtime code into an **Activator rule** on the agent's decision-emit event stream.
2. The action → Teams Adaptive Card path uses Activator's native Teams destination. The agent runtime emits a structured decision event; Activator does the rest.
3. APEX-M's `MessageBus` impl (`apex_m.message_bus_eventstream` — TBD Phase I.4 follow-up) wraps Eventstream + Activator behind the APEX-Core protocol; agent code calls `bus.attach_activator(rule, action)` instead of the bespoke threshold logic.

## Independence implications

None. Eventstream Activator is part of the client's existing Fabric capacity.

## What stays

The agent's decision-emit event format (and the LEDGER row that records it) stays — Activator consumes the existing event stream rather than replacing it. Agent prompts still articulate threshold context for the LLM; the threshold *enforcement* moves to Activator.
