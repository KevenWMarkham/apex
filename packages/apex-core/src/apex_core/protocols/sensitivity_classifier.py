"""SensitivityClassifier protocol — APEX T1–T4 ↔ provider sensitivity labels.

APEX-M satisfies via Microsoft Purview Information Protection sensitivity
labels — the canonical mapping for the Microsoft variant. Labels propagate
through Foundry RAG, Azure AI Search, and the M365 Copilot stack.
APEX-G satisfies via Sensitive Data Protection (Cloud DLP).
APEX-A satisfies via AWS Macie classifications.

The mapping is bidirectional: APEX classifies (T1..T4) and the variant
emits the provider label so downstream tooling honors it; conversely,
when reading from a labeled source, the variant maps the provider label
back to APEX tier so policy stays consistent.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol, runtime_checkable


class SensitivityTier(str, Enum):
    T1_PUBLIC = "T1"             # public
    T2_INTERNAL = "T2"           # internal — most operational data
    T3_CONFIDENTIAL = "T3"       # PII, PCI
    T4_HIGHLY_CONFIDENTIAL = "T4"  # PHI, regulated, dual-control


@dataclass(frozen=True)
class ProviderLabel:
    """The variant-specific label this APEX tier maps to."""
    provider: str               # "microsoft-purview" | "google-dlp" | "aws-macie"
    label_id: str
    label_name: str
    encryption: bool
    extract_required: bool       # for Purview: EXTRACT usage right needed


@runtime_checkable
class SensitivityClassifier(Protocol):
    """Map APEX tiers to provider labels and back."""

    variant: str

    def to_provider_label(self, tier: SensitivityTier) -> ProviderLabel:
        """APEX tier → provider sensitivity label."""
        ...

    def from_provider_label(self, label: ProviderLabel) -> SensitivityTier:
        """Provider label → APEX tier."""
        ...

    def classify_text(self, text: str) -> SensitivityTier:
        """Run the provider's classification engine on text. Used for
        agent prompt + response classification per Purview AI Activity
        Explorer."""
        ...

    def get_label_inventory(self) -> list[ProviderLabel]:
        """All labels available in the variant's tenant."""
        ...
