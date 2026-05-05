# Professional APEX Sellers Guide — Design

**Date:** 2026-04-18
**Status:** Approved — implementation proceeding directly
**Sibling doc:** `Professional-APEX.html` (architect/developer volume)

## 1. Purpose

Produce a single Wrox-style HTML book — *Professional APEX: The Sellers Guide* — for Deloitte Microsoft-practice sellers, Global Practice Leaders, and account teams who need to position APEX to drive Microsoft platform revenue (Fabric, Copilot, Foundry, Purview) at named industry accounts.

## 2. Audience

- **Primary:** Deloitte Microsoft-practice sellers and Global Practice Leaders pursuing Industry accounts
- **Secondary:** Microsoft field sellers co-selling with Deloitte
- **Tertiary:** Delivery leads transitioning into pre-sales / account-planning roles

Independence-compliance tone; sells outcomes, not implementation depth.

## 3. Structure (Approach C — Hybrid)

```
Front Matter — cover, about, how to use this book

PART I    — The APEX Thesis for Sellers
  Ch 1    Why APEX and why now
  Ch 2    The APEX commercial arc (per-service ROI, 3-wave envelope)
  Ch 3    How APEX pulls Microsoft revenue through

PART II   — The Four Microsoft Pillars
  Ch 4    Fabric: the data plane APEX needs
  Ch 5    Copilot: the experience surface APEX supercharges
  Ch 6    Foundry: the reasoning engine APEX orchestrates
  Ch 7    Purview: the trust architecture APEX can't work without

PART III  — Industry Playbooks (one chapter per Practice)
  Ch 8    Retail & Consumer (RC)
  Ch 9    Healthcare & Life Sciences (HLS)
  Ch 10   Energy & Resources (ER)
  Ch 11   Industrial & Manufacturing (AXLE)
  Ch 12   Technology, Media & Telecom (TMT)
  Ch 13   Travel & Hospitality (TH)
  Ch 14   Industrial & Commercial Equipment (ICE)

PART IV   — Anchor Account Playbooks (13 named accounts)
  Ch 15   Walmart         (RC)
  Ch 16   Nike            (RC)
  Ch 17   Sazerac         (RC)
  Ch 18   Johnson & Johnson (HLS / RC)
  Ch 19   GM              (AXLE)
  Ch 20   Bridgestone     (AXLE / RC)
  Ch 21   Caterpillar     (ICE)
  Ch 22   Disney          (TMT-MED)
  Ch 23   AT&T            (TMT-TEL)
  Ch 24   HPE             (TMT-TEC)
  Ch 25   American Airlines (TH)
  Ch 26   United Airlines (TH)
  Ch 27   Bristol Global Mobility (TH-adjacent / services)

PART V    — The Pursuit Motion
  Ch 28   Qualifying
  Ch 29   Discovery & the four-week workshop
  Ch 30   Proposal & commercial framing
  Ch 31   Competitive positioning
  Ch 32   Objection handling
  Ch 33   Procurement and close
  Ch 34   Delivery handoff: setting expectations

Appendices
  A  Microsoft Product Reference (Fabric, Copilot, Foundry, Purview detailed)
  B  The Discovery Question Bank (200+ questions)
  C  Objection Handbook
  D  ROI Calculators & Commercial Templates
  E  Deloitte Independence Notes
  F  Glossary
```

## 4. Per-Account Playbook Structure (Ch 15–27)

Every anchor account chapter follows the same 10-section structure:

1. Strategic Context — where this account is in its own AI transformation
2. Public Signals — 3–5 recent announcements that inform the pursuit
3. The APEX Thesis for This Account — why APEX fits
4. MS Pillar Lead — which Microsoft product leads the pitch
5. Priority APEX Services — 3–5 services relevant to this client
6. Qualifying Questions — 10 questions for the first conversation
7. Discovery Agenda — 2–3 day workshop plan
8. Opening Demo Scenario — which APEX service to show first
9. Commercial Envelope — typical deal-size range
10. Decision-Maker Map + First 30/60/90

## 5. Format

- Single-file HTML `docs/book/Professional-APEX-Sellers-Guide.html`
- Same Wrox visual system as `Professional-APEX.html` but with a **gold-on-navy** accent palette (sales vs. teal architect palette)
- Sticky sidebar TOC, dark-mode toggle, keyboard nav (J/K, G, /)
- Target size: 3–5 MB

## 6. Build

`build-sellers-guide.cjs` — new Node script reusing the markdown parser, Mermaid cache, and HTML scaffolding from `build-professional-apex.cjs`. ~80% of the content is **net-new authoring** (vs. the architect book which was 85% source-doc reuse).

## 7. Length

- Front matter + Part I–II: ~40 pages
- Part III (7 industry playbooks × 12 pages): ~85 pages
- Part IV (13 account plays × 10 pages): ~130 pages
- Part V (7 pursuit chapters × 8 pages): ~55 pages
- Appendices: ~60 pages
- **Total: ~370 pages**

## 8. Content boundaries

**In scope:** Public-domain strategic context per account; generic Microsoft product messaging; APEX service commercial framing; standard qualifying/discovery patterns.

**Out of scope:** Non-public competitive intelligence on named accounts; confidential pricing commitments; proprietary Microsoft roadmap. All account narratives stay strictly in publicly-observable territory; every strategic claim is framed as hypothesis to validate in discovery.

## 9. Independence compliance

- Per-account content frames accounts from the outside (public signals, published strategy)
- No representation of Deloitte as serving these accounts today unless that is a publicly-disclosed relationship
- Appendix E reprints the Deloitte Independence reminder
- No client-confidential pricing, contract terms, or internal organisational details

## 10. Deliverables

1. `docs/book/Professional-APEX-Sellers-Guide.html`
2. `build-sellers-guide.cjs`
3. This design doc
