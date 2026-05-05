"""The 47 APEX orchestration archetypes (APEX_Design §10.3).

Sprint 11 catalogues all 47. The first 10 are marked ``status="impl"`` (one
concrete implementation shipped alongside for proof); the remaining 37 are
``status="manifest-only"`` — names and decision shapes are stable, but
implementations land sprint-by-sprint as consuming agents arrive.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from apex_core.types import OrchestrationPattern


@dataclass(frozen=True, slots=True)
class Archetype:
    archetype_id: str
    name: str
    pattern: OrchestrationPattern
    description: str
    status: Literal["impl", "manifest-only"]


ARCHETYPES: tuple[Archetype, ...] = (
    # --- First 10 (Sprint 11 impl-slot) -----------------------------------
    Archetype("ARCH-01-anomaly-dispo-hitl",   "Anomaly detect + disposition + HITL",       OrchestrationPattern.SEQUENTIAL,   "Detect anomaly → classify → dispose → HITL on boundary.",    "impl"),
    Archetype("ARCH-02-identity-resolve",     "Multi-source identity resolution",          OrchestrationPattern.PARALLEL,     "Match deterministic + probabilistic in parallel; merge.",    "impl"),
    Archetype("ARCH-03-event-cluster-notify", "Event-cluster pattern-match + notify",      OrchestrationPattern.HIERARCHICAL, "Plan → scope → notify each stakeholder.",                    "impl"),
    Archetype("ARCH-04-predictive-schedule",  "Predictive trigger + workflow schedule",    OrchestrationPattern.SEQUENTIAL,   "Predict → schedule → confirm resources.",                    "impl"),
    Archetype("ARCH-05-classification-propagate","Classification change propagation",      OrchestrationPattern.HIERARCHICAL, "Propagate a classification change across dependent services.","impl"),
    Archetype("ARCH-06-cross-practice-fed",   "Cross-practice entity federation",          OrchestrationPattern.HIERARCHICAL, "Enforce trust boundary while federating an entity view.",    "impl"),
    Archetype("ARCH-07-retry-feedback",       "Produce-evaluate-retry",                    OrchestrationPattern.FEEDBACK_LOOP, "Generate output; evaluate; refine until threshold met.",     "impl"),
    Archetype("ARCH-08-parallel-branch-merge","Parallel branch + merge",                   OrchestrationPattern.PARALLEL,     "Fan out to N agents; merge deterministic outputs.",          "impl"),
    Archetype("ARCH-09-escalation-ladder",    "Time-bounded escalation ladder",            OrchestrationPattern.SEQUENTIAL,   "On timeout, escalate to higher approver tier.",              "impl"),
    Archetype("ARCH-10-regulatory-filing",    "Regulatory filing compose + submit",        OrchestrationPattern.SEQUENTIAL,   "Compose → review → submit → confirm.",                       "impl"),

    # --- Remaining 37 (manifest-only until consuming agent arrives) --------
    Archetype("ARCH-11-markdown-cadence",     "Markdown cadence",                          OrchestrationPattern.SEQUENTIAL,   "RC markdown orchestration (stub).",                          "manifest-only"),
    Archetype("ARCH-12-demand-signal",        "Demand signal triggered replenishment",    OrchestrationPattern.FEEDBACK_LOOP, "Demand signal → replenish → verify.",                         "manifest-only"),
    Archetype("ARCH-13-recall-response",      "Recall response",                           OrchestrationPattern.HIERARCHICAL, "Full recall orchestration (stub).",                          "manifest-only"),
    Archetype("ARCH-14-cold-chain",           "Cold chain excursion response",             OrchestrationPattern.SEQUENTIAL,   "RC cold chain orchestration (concrete impl in `reference/`).","manifest-only"),
    Archetype("ARCH-15-patient-flow",         "Patient flow optimisation",                 OrchestrationPattern.HIERARCHICAL, "HLS admit/transfer/discharge (stub).",                       "manifest-only"),
    Archetype("ARCH-16-clinical-triage",      "Clinical triage",                           OrchestrationPattern.SEQUENTIAL,   "HLS ED triage (stub).",                                      "manifest-only"),
    Archetype("ARCH-17-sepsis-early-warn",    "Sepsis early warning",                      OrchestrationPattern.FEEDBACK_LOOP, "HLS sepsis monitor (stub).",                                  "manifest-only"),
    Archetype("ARCH-18-claim-denial",         "Claim denial disposition",                  OrchestrationPattern.SEQUENTIAL,   "HLS claim disposition (stub).",                              "manifest-only"),
    Archetype("ARCH-19-outage-triage",        "Outage triage + restoration",               OrchestrationPattern.HIERARCHICAL, "ER outage (stub).",                                          "manifest-only"),
    Archetype("ARCH-20-asset-maintenance",    "Asset maintenance scheduling",              OrchestrationPattern.SEQUENTIAL,   "ER maintenance (stub).",                                     "manifest-only"),
    Archetype("ARCH-21-demand-forecast",      "Demand forecasting",                        OrchestrationPattern.FEEDBACK_LOOP, "ER demand forecast (stub).",                                  "manifest-only"),
    Archetype("ARCH-22-grid-optimisation",    "Grid optimisation",                         OrchestrationPattern.HIERARCHICAL, "ER grid optimisation (stub).",                               "manifest-only"),
    Archetype("ARCH-23-connected-factory",    "Connected factory",                         OrchestrationPattern.HIERARCHICAL, "AXLE connected factory (stub).",                             "manifest-only"),
    Archetype("ARCH-24-predictive-maint",     "Predictive maintenance",                    OrchestrationPattern.FEEDBACK_LOOP, "AXLE predictive (stub).",                                    "manifest-only"),
    Archetype("ARCH-25-quality-optim",        "Quality optimisation",                      OrchestrationPattern.FEEDBACK_LOOP, "AXLE quality (stub).",                                       "manifest-only"),
    Archetype("ARCH-26-supply-resilience",    "Supply chain resilience",                   OrchestrationPattern.HIERARCHICAL, "AXLE resilience (stub).",                                    "manifest-only"),
    Archetype("ARCH-27-contact-center",       "Contact center intelligence",               OrchestrationPattern.SEQUENTIAL,   "TMT CC (stub).",                                             "manifest-only"),
    Archetype("ARCH-28-content-reco",         "Content recommendation",                    OrchestrationPattern.FEEDBACK_LOOP, "TMT recommendation (stub).",                                  "manifest-only"),
    Archetype("ARCH-29-network-optim",        "Network optimisation",                      OrchestrationPattern.HIERARCHICAL, "TMT network (stub).",                                        "manifest-only"),
    Archetype("ARCH-30-churn-prevent",        "Churn prevention",                          OrchestrationPattern.FEEDBACK_LOOP, "TMT churn (stub).",                                          "manifest-only"),
    Archetype("ARCH-31-revenue-optim",        "Revenue optimisation",                      OrchestrationPattern.FEEDBACK_LOOP, "TH revenue optim (stub).",                                    "manifest-only"),
    Archetype("ARCH-32-crew-schedule",        "Crew scheduling",                           OrchestrationPattern.HIERARCHICAL, "TH crew schedule (stub).",                                   "manifest-only"),
    Archetype("ARCH-33-irop-recovery",        "Disruption recovery",                       OrchestrationPattern.SEQUENTIAL,   "TH IROP recovery (stub).",                                   "manifest-only"),
    Archetype("ARCH-34-personalised-offer",   "Personalised offer",                        OrchestrationPattern.FEEDBACK_LOOP, "TH offer (stub).",                                           "manifest-only"),
    Archetype("ARCH-35-fleet-optim",          "Fleet optimisation",                        OrchestrationPattern.HIERARCHICAL, "ICE fleet optim (stub).",                                    "manifest-only"),
    Archetype("ARCH-36-predictive-service",   "Predictive service",                        OrchestrationPattern.FEEDBACK_LOOP, "ICE predictive service (stub).",                             "manifest-only"),
    Archetype("ARCH-37-dealer-insight",       "Dealer insight",                            OrchestrationPattern.HIERARCHICAL, "ICE dealer (stub).",                                         "manifest-only"),
    Archetype("ARCH-38-customer-engage",      "Customer engagement",                       OrchestrationPattern.SEQUENTIAL,   "ICE customer (stub).",                                       "manifest-only"),
    Archetype("ARCH-39-consent-change",       "Consent change propagation",                OrchestrationPattern.HIERARCHICAL, "Cross-Practice consent propagation (stub).",                 "manifest-only"),
    Archetype("ARCH-40-gate-tuning",          "Tenant gate tuning",                        OrchestrationPattern.SEQUENTIAL,   "Tenant-initiated tuning + observation (stub).",              "manifest-only"),
    Archetype("ARCH-41-incident-runbook",     "Incident runbook",                          OrchestrationPattern.SEQUENTIAL,   "Ops incident (stub).",                                       "manifest-only"),
    Archetype("ARCH-42-sla-breach",           "SLA breach response",                       OrchestrationPattern.SEQUENTIAL,   "SLA breach (stub).",                                         "manifest-only"),
    Archetype("ARCH-43-data-subject-request", "Data-subject-access request",               OrchestrationPattern.SEQUENTIAL,   "GDPR DSAR (stub).",                                          "manifest-only"),
    Archetype("ARCH-44-change-control",       "Change control",                            OrchestrationPattern.SEQUENTIAL,   "GMP change control (stub).",                                 "manifest-only"),
    Archetype("ARCH-45-deviation-log",        "Deviation logging",                         OrchestrationPattern.SEQUENTIAL,   "GxP deviation log (stub).",                                  "manifest-only"),
    Archetype("ARCH-46-root-cause",           "Root-cause analysis",                       OrchestrationPattern.FEEDBACK_LOOP, "RCA (stub).",                                                "manifest-only"),
    Archetype("ARCH-47-capa-action",          "CAPA action tracking",                      OrchestrationPattern.SEQUENTIAL,   "Corrective/Preventive action (stub).",                       "manifest-only"),
)


def _assert_47() -> None:  # pragma: no cover — sanity assertion at import
    if len(ARCHETYPES) != 47:
        raise AssertionError(
            f"ARCHETYPES catalog has {len(ARCHETYPES)} entries; must be 47."
        )


_assert_47()
