"""APEX-M SensitivityClassifier — Microsoft Purview Information Protection.

Maps APEX T1-T4 classifications to Purview sensitivity labels (and back).
Required for Foundry RAG inheritance, Azure AI Search query-time label
enforcement, and the M365 Copilot stack.

Reference: https://learn.microsoft.com/purview/ai-azure-foundry
Reference: https://learn.microsoft.com/purview/sensitivity-labels
"""
from __future__ import annotations

from typing import Any

from apex_core.protocols import (
    ProviderLabel,
    SensitivityClassifier,
    SensitivityTier,
)


# Default Purview label mapping — clients override per their sensitivity-
# label taxonomy. The id values below are placeholders; the Purview portal
# generates real GUIDs at tenant time.
_DEFAULT_PURVIEW_MAP = {
    SensitivityTier.T1_PUBLIC: ProviderLabel(
        provider="microsoft-purview",
        label_id="apex-m-public",
        label_name="Public",
        encryption=False,
        extract_required=False,
    ),
    SensitivityTier.T2_INTERNAL: ProviderLabel(
        provider="microsoft-purview",
        label_id="apex-m-internal",
        label_name="Internal",
        encryption=False,
        extract_required=False,
    ),
    SensitivityTier.T3_CONFIDENTIAL: ProviderLabel(
        provider="microsoft-purview",
        label_id="apex-m-confidential",
        label_name="Confidential",
        encryption=True,
        extract_required=True,    # Foundry RAG must check EXTRACT
    ),
    SensitivityTier.T4_HIGHLY_CONFIDENTIAL: ProviderLabel(
        provider="microsoft-purview",
        label_id="apex-m-highly-confidential",
        label_name="Highly Confidential — Dual Control",
        encryption=True,
        extract_required=True,
    ),
}


class SensitivityClassifierPurview:
    """Maps APEX T1-T4 to Purview labels; calls Purview classifier for
    text classification."""

    variant = "APEX-M"

    def __init__(self, *, label_map: dict[SensitivityTier, ProviderLabel] | None = None) -> None:
        self._map = dict(_DEFAULT_PURVIEW_MAP) if label_map is None else dict(label_map)
        self._reverse = {pl.label_id: tier for tier, pl in self._map.items()}

    def to_provider_label(self, tier: SensitivityTier) -> ProviderLabel:
        return self._map[tier]

    def from_provider_label(self, label: ProviderLabel) -> SensitivityTier:
        if label.label_id not in self._reverse:
            raise KeyError(
                f"Unknown Purview label '{label.label_id}'. Add it to label_map."
            )
        return self._reverse[label.label_id]

    def classify_text(self, text: str) -> SensitivityTier:
        """Run the Purview classifier on text. Stub returns T2_INTERNAL —
        production impl calls Purview SIT (Sensitive Information Types)
        and trainable classifiers."""
        # Heuristic fallback for unit tests; production uses Purview Graph API.
        if any(token in text.lower() for token in ("ssn", "patient", "phi", "diagnosis")):
            return SensitivityTier.T4_HIGHLY_CONFIDENTIAL
        if any(token in text.lower() for token in ("credit card", "ccn", "loyalty_id", "email")):
            return SensitivityTier.T3_CONFIDENTIAL
        return SensitivityTier.T2_INTERNAL

    def get_label_inventory(self) -> list[ProviderLabel]:
        return list(self._map.values())


__all__ = ["SensitivityClassifierPurview"]
