"""Per-format file adapters — Sprint 29 Task 29.9.2.

Each adapter extracts plain text from one file format, returning
``[(line_number, text), ...]`` so the rule engine can scan uniformly.

Lazy imports for optional dependencies (``python-docx``, ``python-pptx``)
so the core package installs without them; users opt in via
``pip install apex-compliance-lint[docx]`` / ``[pptx]``.
"""

from apex_compliance_lint.adapters.html_adapter import HTMLAdapter
from apex_compliance_lint.adapters.markdown_adapter import MarkdownAdapter
from apex_compliance_lint.adapters.docx_adapter import DOCXAdapter
from apex_compliance_lint.adapters.pptx_adapter import PPTXAdapter

__all__ = ["DOCXAdapter", "HTMLAdapter", "MarkdownAdapter", "PPTXAdapter"]


def default_registry() -> dict:
    """Default extension → adapter mapping."""
    html = HTMLAdapter()
    md = MarkdownAdapter()
    docx = DOCXAdapter()
    pptx = PPTXAdapter()
    return {
        ".html": html,
        ".htm": html,
        ".md": md,
        ".markdown": md,
        ".docx": docx,
        ".pptx": pptx,
    }
