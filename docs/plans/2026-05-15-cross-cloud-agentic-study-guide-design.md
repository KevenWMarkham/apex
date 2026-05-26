# Cross-Cloud Agentic Podcast — Study Guide (HTML) · Design

**Date:** 2026-05-15
**Status:** Design approved · building directly (single self-contained HTML file)

## Goal

A single self-contained HTML study guide for the 8-episode Cross-Cloud Agentic Podcast — note-taking and study companion for Microsoft Target Platform Sellers.

## Output

`C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\Cross-Cloud-Agentic-Study-Guide.html`

Single file. Inline CSS + JS. Only external dependency: Google Fonts (Fraunces, Instrument Sans, JetBrains Mono) — matching APEX house style.

## Visual style

APEX house style — copied from `APEX-Orchestration-Guide.html`:
- Dark/light theme toggle (warm palette; dark default)
- Fraunces (display serif) + Instrument Sans (body) + JetBrains Mono (code)
- Sticky top nav + sticky tab bar
- House color tokens (teal/purple/amber/crimson/gold accents)

## Structure — 9 tabs

1. **Overview** — series purpose · the Five Architectural Principles · the six discovery openers · voice cast · how to use the guide
2-9. **Episode 1-8** — each tab has three sections:
   - **① Content Breakdown** — section-by-section walkthrough of the episode (cold open → each conversation section → disagreement → carry-forward), 2-4 sentences per section
   - **② Note Card** — print-optimized index card (`@media print` rules so Ctrl+P prints just the card): core thesis, 4-6 condensed key concepts, relevant principle(s), discovery opener / talking points
   - **③ Vocabulary** — episode-specific terms with crisp definitions

## Content source

The 8 episode scripts in `pc-cross-cloud-agentic/01-*.md` through `08-*.md` (~49K words). Content extracted per episode (section structure, key concepts, vocabulary) then assembled into the HTML.

## Content discipline

Same as the podcast: generic (no client names), no internal codenames (taught as "the Acceleration Framework"), Independence-minded framing, no forbidden vocabulary (co-sell / alliance / partner / strategic partnership).

## Interactivity (YAGNI-bounded)

Tab switching · theme toggle · per-tab print (Note Card print stylesheet). No search, no filters, no animation beyond house-style transitions.

## Build approach

Single-file build. Per-episode content extracted via 8 parallel extraction passes (one per episode script), then assembled by the controller into one HTML file. Verified for: valid HTML render, all 9 tabs present, print stylesheet on note cards, no forbidden vocabulary, no internal codenames.
