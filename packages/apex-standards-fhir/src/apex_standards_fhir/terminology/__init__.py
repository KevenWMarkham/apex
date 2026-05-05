"""Terminology-service integration.

:class:`TerminologyService` is the abstract hook; :class:`MockTerminologyService`
is a dev-only in-memory implementation. Tenants swap for a real server
(Snowstorm, TermServer, or vendor-hosted).
"""

from apex_standards_fhir.terminology.mock import (
    MockTerminologyService,
    TerminologyLookupResult,
    TerminologyService,
)

__all__ = [
    "MockTerminologyService",
    "TerminologyLookupResult",
    "TerminologyService",
]
