---
name: threshold-tuner
description: Use when designing or tuning threshold bands for a VV. Triggers include "set thresholds", "tune bands", "what are good/warn/critical predicates".
---

# Threshold tuning for APEX

Use the `apex-threshold-tuner` agent. Provide:
- Historical metric data (CSV or parquet)
- Industry baseline (from pack catalog)
- Target cadence (1s · 1m · 1h · 1d)

The agent analyzes distribution, applies the industry baseline, and proposes good/warn/critical predicates.

## Conventions
- Always pass through `industry_baseline` first; only override with statistical thresholds when there's evidence the baseline is wrong.
- Sustain_window default: 2 measurement intervals (debounce flapping).
- For critical bands, prefer percentile-based predicates (e.g., p99) over fixed values.
- Always generate a threshold-telemetry VV for self-observation.
