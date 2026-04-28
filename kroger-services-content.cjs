// kroger-services-content.cjs — Professional Kroger Services book content.
//
// Wraps the 17 deliverables under
// Consumer/Retail/Kroger/02_projects/FY27_Pipeline/assortment-pricing-agentic/deliverables/
// into the 5-part engagement-arc book described in
// docs/plans/2026-04-27-professional-kroger-services-book-design.md.
//
// Independence note: The book is internal Deloitte sellers' material. APEX is
// the internal accelerator name; client-facing narrative blocks (Ch 19) frame
// the work as "Deloitte-delivered agents on Kroger's Microsoft platform" and
// do not name APEX.

const chapters = [];
const appendices = [];

chapters.push({
  num: 1, part: 1, title: 'Smoke test',
  objectives: ['Verify the Companion Artifacts callout renders'],
  body: `
## Smoke

This chapter is a temporary smoke test for the Companion Artifacts callout. It is replaced in Task 5.

> **Companion Artifacts**
> - [Walkthrough](Services/RC-E2E-03_Assortment-and-Pricing/Tier0-Foundation/APEX-RC-E2E-03-Walkthrough.docx) — narrative walkthrough of the service
> - [One-pager](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-OnePager.html) — 5-minute summary
`,
  summary: ['Smoke takeaway'],
  actions: ['Smoke action'],
});

module.exports = { all: chapters, appendices };
