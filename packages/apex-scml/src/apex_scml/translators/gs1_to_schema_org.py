"""Bidirectional translator: GS1 GTIN ↔ Schema.org Product.

Pattern D per ``Industry-Standards-Incorporation-Plan.md`` §4.4.
Round-trip tested in ``tests/test_translator_gs1_schema_org.py``.
"""

from __future__ import annotations

from typing import Any

_GTIN_VARIANTS = ("gtin14", "gtin13", "gtin12", "gtin8", "gtin")


def gs1_gtin_to_schema_org_product(
    gtin: str,
    *,
    name: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Emit a Schema.org ``Product`` dict carrying a GTIN.

    The GTIN length determines which Schema.org property is used
    (``gtin8`` / ``gtin12`` / ``gtin13`` / ``gtin14``).

    Args:
        gtin: Numeric GS1 GTIN, 8/12/13/14 digits.
        name: Optional ``Product.name``.
        description: Optional ``Product.description``.

    Returns:
        A JSON-LD-ready dict with ``@type: Product``.

    Raises:
        ValueError: If ``gtin`` is not 8/12/13/14 numeric digits.
    """
    if not gtin.isdigit() or len(gtin) not in {8, 12, 13, 14}:
        raise ValueError(f"Invalid GTIN: {gtin!r}")

    property_name = f"gtin{len(gtin)}"
    product: dict[str, Any] = {"@type": "Product", property_name: gtin}
    if name is not None:
        product["name"] = name
    if description is not None:
        product["description"] = description
    return product


def schema_org_product_to_gs1_gtin(product: dict[str, Any]) -> str | None:
    """Extract the most specific GTIN from a Schema.org ``Product`` dict.

    Prefers ``gtin14`` → ``gtin13`` → ``gtin12`` → ``gtin8`` → generic ``gtin``.

    Returns:
        The GTIN as a string, or ``None`` if no recognised property is present.
    """
    for key in _GTIN_VARIANTS:
        value = product.get(key)
        if value is not None:
            return str(value)
    return None
