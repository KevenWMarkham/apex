"""RC Practice bundle — declarative definition of what RC ships.

See ``docs/APEX - Design and Build/APEX_Design.md`` §3 (L3 Practice layer) and
§15 (per-Practice standards alignment).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from apex_core.types import Practice
from apex_cxml import Customer, Interaction, Loyalty, Order
from apex_merml import Category, Competitor, Elasticity, Markdown, Price, Promotion
from apex_scml import SKU, Inventory, Item, Location, Lot, Shipment, Supplier


class PracticeBundle(BaseModel):
    """Declarative bundle listing everything an L3 Practice ships.

    Sprint 2 scope populates ``schema_families``, ``entities``, and
    ``standards``. ``agents`` and ``services`` remain empty until Sprints
    16 and 17 respectively.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    practice: Practice
    name: str
    version: str
    schema_families: list[str]
    entities: dict[str, list[str]]
    standards: list[str]
    agents: list[str] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)


def rc_bundle() -> PracticeBundle:
    """Return the canonical RC Practice bundle for this APEX build."""
    return PracticeBundle(
        practice=Practice.RC,
        name="rc",
        version="0.1.0",
        schema_families=["scml", "merml", "cxml", "proml"],
        entities={
            "scml": [
                SKU.__name__,
                Inventory.__name__,
                Location.__name__,
                Lot.__name__,
                Shipment.__name__,
                Supplier.__name__,
                Item.__name__,
            ],
            "merml": [
                Category.__name__,
                Price.__name__,
                Promotion.__name__,
                Markdown.__name__,
                Elasticity.__name__,
                Competitor.__name__,
            ],
            "cxml": [
                Customer.__name__,
                Loyalty.__name__,
                Interaction.__name__,
                Order.__name__,
            ],
            "proml": [
                # PROML.Pricing + PROML.DiscountRule live in the apex-proml
                # package created in Sprint 30.4. They're listed here for
                # discovery; the bundle does not import the classes directly
                # to avoid creating a hard dependency from apex-rc to apex-proml.
                "Pricing",
                "DiscountRule",
            ],
        },
        standards=[
            "gs1-gtin",
            "gs1-sscc",
            "gs1-gln",
            "epcis",
            "schema-org",
        ],
    )
