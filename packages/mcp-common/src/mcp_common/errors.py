"""Standard MCP error codes + exception class."""

from __future__ import annotations

from enum import StrEnum


class McpErrorCode(StrEnum):
    UNAUTHENTICATED = "unauthenticated"
    SCOPE_DENIED = "scope_denied"
    CLASSIFICATION_DENIED = "classification_denied"
    NOT_FOUND = "not_found"
    INVALID_INPUT = "invalid_input"
    CONFLICT = "conflict"
    INTERNAL = "internal"
    NOT_IMPLEMENTED = "not_implemented"


class McpError(Exception):
    """Raised from an MCP tool to signal a structured failure."""

    def __init__(self, *, code: McpErrorCode, message: str) -> None:
        super().__init__(f"[{code.value}] {message}")
        self.code = code
        self.message = message
