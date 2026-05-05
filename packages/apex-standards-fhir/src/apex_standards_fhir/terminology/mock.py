"""Dev-only in-memory terminology service mock.

Provides a ``TerminologyService`` interface and a ``MockTerminologyService``
backed by a tiny dict. Tenants replace the mock with a real terminology
server (Snowstorm / TermServer / vendor-hosted) by implementing
:class:`TerminologyService`.

**Never ship the mock to production.** The mock's content is a dev-fixture
and covers only a handful of concepts; real clinical reasoning requires a
real terminology service.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class TerminologyLookupResult:
    """Result of looking up a coded concept."""

    system: str
    code: str
    display: str
    active: bool = True


class TerminologyService(Protocol):
    """Interface every terminology backend must implement."""

    def lookup(self, system: str, code: str) -> TerminologyLookupResult | None:
        """Return metadata for a specific (system, code) pair, or None if not found."""
        ...

    def is_active(self, system: str, code: str) -> bool:
        """Return True iff the code is active in the terminology's latest release."""
        ...


class MockTerminologyService:
    """Hard-coded mock — **dev and test only**.

    Seed content covers a few LOINC / SNOMED CT / RxNorm codes sufficient for
    the Sprint 3 FHIR fixtures.
    """

    _SEED: dict[tuple[str, str], TerminologyLookupResult] = {
        ("http://loinc.org", "1234-5"): TerminologyLookupResult(
            "http://loinc.org", "1234-5", "Mock LOINC concept (dev)",
        ),
        ("http://loinc.org", "85354-9"): TerminologyLookupResult(
            "http://loinc.org", "85354-9", "Blood pressure panel (dev)",
        ),
        ("http://snomed.info/sct", "386661006"): TerminologyLookupResult(
            "http://snomed.info/sct", "386661006", "Fever (finding) (dev)",
        ),
        ("http://www.nlm.nih.gov/research/umls/rxnorm", "1049630"): TerminologyLookupResult(
            "http://www.nlm.nih.gov/research/umls/rxnorm",
            "1049630", "acetaminophen 325 MG Oral Tablet (dev)",
        ),
    }

    def lookup(self, system: str, code: str) -> TerminologyLookupResult | None:
        return self._SEED.get((system, code))

    def is_active(self, system: str, code: str) -> bool:
        result = self._SEED.get((system, code))
        return result is not None and result.active
