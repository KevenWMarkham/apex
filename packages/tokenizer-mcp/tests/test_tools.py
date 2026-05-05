"""Tests for tokenizer-mcp.detokenize_under_scope."""

from __future__ import annotations

import pytest

from apex_core.types import Classification
from apex_tokenizer import (
    InMemoryVaultBackend,
    TokenService,
    reset_default_service,
    set_default_service,
)
from mcp_common import McpError, McpErrorCode
from tokenizer_mcp import CONTRACTS, detokenize_under_scope


@pytest.fixture(autouse=True)
def _prime_tokeniser() -> str:
    reset_default_service()
    svc = TokenService(backend=InMemoryVaultBackend())
    set_default_service(svc)
    return svc.tokenize("alice@example.com", Classification.PII)


def test_detokenise_with_matching_scope(_prime_tokeniser: str) -> None:
    result = detokenize_under_scope(_prime_tokeniser, ["classification:pii"])
    assert result["cleartext"] == "alice@example.com"


def test_detokenise_without_scope_denies(_prime_tokeniser: str) -> None:
    with pytest.raises(McpError) as exc:
        detokenize_under_scope(_prime_tokeniser, ["classification:internal"])
    assert exc.value.code is McpErrorCode.SCOPE_DENIED


def test_detokenise_wrong_classification_denies(_prime_tokeniser: str) -> None:
    with pytest.raises(McpError) as exc:
        detokenize_under_scope(_prime_tokeniser, ["classification:phi"])
    assert exc.value.code is McpErrorCode.SCOPE_DENIED


def test_unknown_token() -> None:
    with pytest.raises(McpError) as exc:
        detokenize_under_scope("tok_nonexistent", ["classification:pii"])
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_cleartext_pass_through() -> None:
    result = detokenize_under_scope("plain-text", ["classification:pii"])
    assert result["cleartext"] == "plain-text"


def test_contracts() -> None:
    assert len(CONTRACTS) == 1
    assert Classification.PHI in CONTRACTS[0].classification_propagation
