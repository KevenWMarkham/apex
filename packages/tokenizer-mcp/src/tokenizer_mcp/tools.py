"""tokenizer-mcp tool implementations."""

from __future__ import annotations

from apex_core.types import Classification
from apex_tokenizer import detokenize as _svc_detokenize
from apex_tokenizer import get_default_service
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "tokenizer-mcp"
TOOL_VERSION = "1.0.0"


def detokenize_under_scope(
    token: str,
    requester_scope: list[str],
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, str | None]:
    """Resolve ``token`` to cleartext — only if ``requester_scope`` permits it.

    Sprint 7 scope check: the caller must include the token's classification
    in ``requester_scope``. Example: to detokenise a PHI token, the scope
    list must contain ``"classification:phi"``.

    Sprint 10 replaces this with the full lattice (tenant × practice ×
    persona × classification × row-filter).

    Returns ``{"cleartext": value}`` on success; raises ``McpError`` otherwise.
    """
    with traced_call(
        tool_name=f"{SERVER_NAME}.detokenize_under_scope",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"token_prefix": token[:8], "requester_scope": requester_scope},
    ) as ctx:
        svc = get_default_service()
        entry = svc.backend.resolve(token) if token.startswith("tok_") else None
        if entry is None:
            if token and not token.startswith("tok_"):
                # Cleartext pass-through for migration rows.
                ctx["result"] = {"cleartext": token}
                return {"cleartext": token}
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message="Unknown token.",
            )

        # Sprint 7 scope gate: require the token's classification in requester_scope.
        required = f"classification:{entry.classification.value}"
        if required not in requester_scope:
            raise McpError(
                code=McpErrorCode.SCOPE_DENIED,
                message=(
                    f"Scope insufficient for classification "
                    f"{entry.classification.value!r} (required: {required!r})."
                ),
            )

        cleartext = _svc_detokenize(token)
        result = {"cleartext": cleartext}
        ctx["result"] = result
        return result


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.detokenize_under_scope", version=TOOL_VERSION,
        description="Resolve a token to cleartext if the caller's scope permits.",
        classification_propagation=[
            Classification.PII,
            Classification.PHI,
            Classification.PCI,
            Classification.TRADE_SECRET,
            Classification.MEMBER_ONLY,
        ],
    ),
]
