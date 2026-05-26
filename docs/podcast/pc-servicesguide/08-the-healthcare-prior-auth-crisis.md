# Episode 08 · The Healthcare Prior-Auth Crisis

**Arc:** Business-need (4 of 7) · **Builds on:** Foundation + Eps 5-7 (Practice fluency, streaming patterns, governance maturity) · **Service delivered:** HLS-CLIN-05 Prior Authorisation Automation · **KPI:** PA turnaround time · denial rate · clinician hours saved per week
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-13

---

## Cold Open

[Sound: hospital ambient — distant pager, footsteps]

**KEVEN:** I want to start with a survey result. The American Medical Association runs an annual survey of physicians on prior authorisation. The 2024 numbers are — *94 percent of physicians report prior authorisation causes care delays. 78 percent report it has led to patients abandoning treatment. 33 percent report it has caused a serious adverse event for one of their patients in the past year.*

[pause]

**MORGAN:** Those are sobering numbers.

**KEVEN:** Those are sobering numbers. And the *operational* numbers around them — the average physician practice spends *14 hours per physician per week* on prior authorisation work. *14 hours of physician time that's not clinical care.* In an environment where physician shortage is the binding constraint on healthcare access — *that 14 hours is the most expensive 14 hours in the system.*

That's what this episode is about. The prior-auth crisis. Why it got this bad. Why it can't be fixed by the payers alone, can't be fixed by the providers alone, and required the agentic-era technology to actually address. The Service that closes the loop. And — because this is healthcare — the governance posture that has to come with it.

I'm Keven Markham.

**MORGAN:** I'm Morgan. Services Podcast Episode Eight. *The Healthcare Prior-Auth Crisis.*

---

## The conversation

### Historical opening · how prior auth got to where it is

**KEVEN:** Let me walk the arc. Because prior auth as we know it today is not what it was when it started.

1970s and 80s — *prior auth as a tool against the most expensive procedures.* Payers — insurance companies, Medicare — used prior auth on a small set of very-expensive, often-overutilised procedures. Inpatient stays for non-emergent conditions. Specific imaging. Certain elective surgeries. The volume was *low.* Manageable. The friction was real but contained.

1990s — *managed care expanded prior-auth scope.* Health plans introduced PAs on more procedures, more drugs, more specialist referrals. The administrative burden on physician offices grew. Phone-and-fax was the dominant medium. Physician offices hired staff specifically for PA work. *The labour cost of healthcare administration started rising as a percentage of total spend.*

2000s and 2010s — *electronic PA promised relief but didn't deliver it.* Health plans rolled out electronic PA submission portals. In theory, this should have streamlined the process. In practice — *each payer's portal was different.* Provider offices had to learn ten or twenty different interfaces. The data they had to enter overlapped but wasn't standardised. Many PA requests still required clinical documentation that had to be faxed separately. The administrative burden did not meaningfully decrease.

2020s — *the current crisis.* Specialty drugs, expensive biologics, advanced imaging, genetic testing — each new clinical advance brought new PA requirements. The PA volume per practice has roughly tripled since 2010. Physician burnout from administrative burden has reached levels the AMA describes as a *patient-safety issue.* *And there is no signal that PA volume is going to decrease through the normal mechanisms — payers won't unilaterally reduce PA requirements, providers can't bypass them.*

**MORGAN:** So the crisis is structural.

**KEVEN:** The crisis is structural. Which means the *solution* is also structural — a technology-driven change to how the PA workflow operates. Not "do PA the same way faster." A *different shape* of PA work.

### The pain today

**MORGAN:** Operational pain. Specifics.

**KEVEN:** Three pains.

Pain one — *the work falls on the wrong people.* The PA request requires clinical documentation — diagnosis codes, clinical justification, prior-treatment history, medical-necessity argument. The *physician* has to provide this. But the *form-filling, the portal-submitting, the follow-up-calling* is administrative work. So practices have hybrid workflows where physicians spend 14 hours a week providing inputs to staff who then spend more hours assembling submissions. *Both pools of time are scarce.*

Pain two — *PA decisions take days when patients need them in hours.* The average PA turnaround in the U.S. is *3-7 days.* For some specialty medications, *2-3 weeks.* The patient is sitting at home waiting. The condition is progressing. The physician's intent — *give the patient this medication now* — is being frustrated by an administrative process. The clinical risk is real.

Pain three — *the denial-and-appeal cycle multiplies the work.* Roughly 17 percent of PAs are denied on first submission. The appeal process — which most physicians and patients eventually win when pursued — adds weeks. And the appeal work is *more* expert-time, *more* documentation, *more* manual labour. The cycle that started with the physician spending 30 minutes on the original submission can end with the physician spending several hours across original, denial, and successful appeal.

### Why dashboards and ML couldn't fix this

**MORGAN:** And the prior eras —

**KEVEN:** Dashboards in PA were mostly *measurement* tools. Practice administrators could see PA volume, turnaround time, denial rates. *Useful for awareness. Useless for action.* No dashboard fills a PA submission.

ML in PA has been used by payers — *predicting which PAs to deny without clinical review.* Which is — to be honest — *the opposite of what providers want.* Provider-side ML adoption has been minimal because the technology hasn't been able to handle the *clinical reasoning* the work requires.

The agentic era is different because the work being asked for — *given a patient's clinical record, draft a complete PA submission that anticipates the payer's likely questions, supports it with citations from the clinical record, and pre-emptively addresses common denial reasons* — *is exactly the kind of work LLMs do well* once they're properly grounded in the clinical data.

### The strategy · agent-drafted PA with clinician approval

**KEVEN:** The strategy — *agent-drafted prior authorisation with clinician approval.* And let me be careful about the framing because clinical AI requires honesty.

The agent does *not* make the clinical decision. The agent does *not* decide what medication is right for the patient. The clinician decides those. The agent's job is — *take the clinical decision the physician has already made, and prepare the PA submission that supports it.* The agent reads the clinical record. The agent retrieves the payer's PA requirements for the specific medication or procedure. The agent retrieves the patient's prior-treatment history relevant to the medical-necessity argument. The agent drafts the submission — diagnosis codes mapped, clinical justification written, supporting documentation referenced. The agent identifies likely denial vectors and pre-addresses them.

The *clinician* reviews. The clinician approves or modifies. The clinician's signature is on the submission. The agent's work is *preparation*, not decision-making.

**MORGAN:** And the time impact —

**KEVEN:** *That's the breakthrough.* The clinician's time goes from 30+ minutes of original submission work down to *2-5 minutes of review-and-approve.* For a practice doing 40-100 PAs a week, that's hours-per-day of physician time returned to clinical care.

### The Service that delivers it · HLS-CLIN-05

**KEVEN:** Architecture.

**MORGAN:** Walk it.

**KEVEN:** HLS-CLIN-05 — *Prior Authorisation Automation.* The flagship HLS provider Service.

Bronze layer. Multiple sources. The EHR — patient demographics, encounter notes, problem list, medication history, diagnostic results. The eligibility system — patient insurance, plan details, benefits. The payer's PA-requirements feed — typically through a clearinghouse or directly via FHIR APIs where available. Plus historical PA submissions for pattern learning.

Bronze ingestion is *governance-heavy* — every record is classified as PHI at landing, the tokenisation vault is more aggressively gated than other Practices, the pii-unlock identity is the chapter-of-the-engagement that gets the CCO involved on day one.

Silver layer. Canonical schemas — the HLS clinical-encounter family (FHIR-aligned), the claims-and-utilization family, the patient-and-eligibility family. Identity reconciliation is *strict* — patient identity across EHR, eligibility system, and PA history must reconcile with high precision because errors here have patient-safety implications.

Gold layer. The Service's Gold mart shapes per-PA-request feature views. For a given request — the patient's complete clinical context, the payer's specific requirements, the historical PA-pattern data for similar requests at this payer.

**MORGAN:** And the agent's tools —

**KEVEN:** Roughly twelve MCP tools — more than the typical Service because the work is information-dense. *Get_patient_clinical_context.* *Get_payer_pa_requirements.* *Get_medication_treatment_history.* *Get_diagnosis_supporting_evidence.* *Get_similar_pa_outcomes.* *Draft_clinical_justification.* *Draft_supporting_documentation_list.* *Identify_likely_denial_vectors.* *Compose_pa_submission.* *Submit_for_clinician_review.* *Plus two read-only tools for utilisation history and benefits checking.*

**MORGAN:** And the HITL pattern —

**KEVEN:** HITL — full Human In The Loop — for every submission. *No exception.* The clinician approves every draft before it goes to the payer. The framework's position on this is firm — clinical decision support that affects patient care goes through HITL, period. Maybe in the very long-term future a different pattern emerges, but not today, not for clinical AI.

**MORGAN:** And the Purview governance posture —

**KEVEN:** This is the heaviest Purview posture in the framework. PHI labels at Bronze propagate through Silver, Gold, MCP responses, agent outputs, audit rows. DSPM-for-AI dashboards are configured with HLS-specific sensitivity rules. The CCO's audit-reader role is provisioned on Day-Zero. The agent's audit row includes the full lineage from EHR data through the submitted PA — which is the artefact regulators and auditors care about for HIPAA compliance, FDA-relevant communications, and payer-audit defence.

### KPI impact

**MORGAN:** Numbers.

**KEVEN:** Three impact dimensions.

*Clinician time saved.* From 14 hours per physician per week to 2-4 hours per physician per week on PA administrative work. *Ten-plus hours per physician per week returned to clinical care.* For a 50-physician practice, that's 500+ hours of clinical capacity per week. Enormous.

*PA turnaround.* From 3-7 days down to *same-day to next-day* for the majority of submissions. Patient experience and clinical outcome both improve.

*Denial rate.* The framework's reference scenario shows 30-50 percent reduction in first-submission denials, because the agent pre-emptively addresses common denial vectors. The downstream effect — fewer appeals, fewer cycles, less work compounded.

The engagement-level annual value depends on practice size — for a large provider system with thousands of physicians, the value is in the hundreds of millions of dollars annually in clinician productivity, patient outcomes, and reduced denial-and-appeal labour cost.

### Where it goes next · Wave Two for HLS

**KEVEN:** Wave Two adjacent Services —

*HLS-CLIN-02 — Claims Denial Prevention.* Same patient data, different decision shape. Pre-submission denial scoring for claims (the back-end equivalent of PA).

*HLS-CLIN-01 — Care Gap Closure for Population Health.* Patient-population-level Service for identifying patients with open care gaps. Different decision-shape — proactive rather than reactive.

*HLS-CLIN-03 — Clinical Decision Support, Oncology.* The highest-regulatory-bar Service in the framework. Only attempted in Wave Two-plus engagements after the team has built operational trust with the CCO.

The Practice's compounding play is — *once the PA Service is live and trusted, the institutional muscle to add adjacent clinical Services exists.* The framework has shown the work is governable.

### A reading I want to do

**MORGAN:** From the AMA's 2024 Prior Authorisation Survey.

**KEVEN:** Go.

**MORGAN:** [reading]

*"Prior authorisation reform has been the most-discussed administrative burden in American medicine for two decades. Legislative remedies have been incremental and incomplete. Industry self-regulation has produced modest improvements. The technology landscape has changed dramatically in the past 24 months. Provider organisations that adopt agent-assisted PA workflows — properly governed, with clinical decision-making preserved — are reporting administrative-burden reductions on the order of 70 to 80 percent, with clinician satisfaction recovering to levels not seen since the early 2010s."*

[pause]

**KEVEN:** That second-to-last sentence. *"Clinical decision-making preserved."* That's the architectural commitment. The agent prepares; the clinician decides.

### One disagreement

**KEVEN:** Pushback.

**MORGAN:** I want to push on whether the framework's *strict HITL* posture for clinical AI is sustainable forever. Because if the agent is producing 95-percent-accurate drafts that clinicians approve with minimal changes 90 percent of the time — there's pressure to introduce *HOTL* (human-on-the-loop) for the lowest-risk PA categories. Faster throughput, less clinician overhead.

**KEVEN:** I'd push back. *In clinical AI specifically*, strict HITL is the right posture for the foreseeable future. The reasons aren't engineering reasons — they're regulatory and trust reasons. The day a clinical AI auto-submits a PA without human signature, and a patient is harmed because the agent missed a context, the entire industry posture resets. Engineering convenience is not worth that risk.

The maturity move *isn't* HOTL for clinical AI. The maturity move is — *reduce the clinician's review time by improving the draft quality so the review is genuinely 2-5 minutes.* That's the right vector.

**MORGAN:** OK. *Strict HITL preserved; speed comes from draft quality, not from removing the human gate.*

**KEVEN:** Yes.

### What to carry forward

**KEVEN:** Two things.

One — *clinical AI is the highest-governance segment of the framework.* Purview-heavy. HITL-default. Strict PHI handling. The episode is a *governance maturity reference* for the rest of the series.

Two — *the pattern of agent-as-preparer, human-as-decider* is the framework's commitment for high-stakes domains. We'll see it again in financial-services contexts and in safety-critical industrial contexts.

**MORGAN:** Next episode — *The Energy-Transition Operations Gap.* ER Practice. Streaming patterns from Episode 7 return at industrial scale. Distribution outage triage. SAIDI and SAIFI.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn

- **Microsoft Cloud for Healthcare — overview** · [Microsoft Learn](https://learn.microsoft.com/industry/healthcare/)
- **Azure API for FHIR** · Microsoft Learn
- **Microsoft Fabric Healthcare data solutions** · Microsoft Learn

### Microsoft Tech Community blogs

- **"Healthcare AI architecture on Fabric"** · Microsoft Healthcare Blog
- **"Prior authorisation automation with Azure AI"** · Microsoft Industry Blog

### Architecture references

- **Azure Architecture Center — Healthcare reference architectures** · Microsoft Learn
- **FHIR-based interoperability reference** · Microsoft Learn

### Industry context

- **American Medical Association — Prior Authorisation Survey (annual)** · [ama-assn.org](https://www.ama-assn.org/) — primary source for clinician-burden data
- **Council for Affordable Quality Healthcare (CAQH) — CAQH Index** · annual report on administrative cost reduction
- **CMS — Prior Authorisation regulations** · regulatory landscape
- *"The State of Prior Authorization"* · Health Affairs, 2024
- *"Healthcare administrative cost trends"* · McKinsey Global Institute
- *"Clinician burnout and administrative burden"* · NEJM Catalyst, 2024
- **HL7 FHIR R4 standard** · [hl7.org/fhir/R4](https://www.hl7.org/fhir/R4/)

### From the APEX Trilogy

- **Sellers Guide — *Health & Life Sciences Practice* chapter** — the commercial framing
- **Services Guide — *HLS Service Catalog* chapter** — HLS-CLIN-05 in detail
- **Services Guide — *Entra ID + Purview governance* chapter** — the deep governance posture this Service relies on

---

**End of Episode 08 · The Healthcare Prior-Auth Crisis**
*≈ 5,300 words · target 30 minutes at conversational pace*
