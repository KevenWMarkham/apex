"""CXML canonical entities."""

from apex_cxml.entities.customer import Customer, CustomerStatus
from apex_cxml.entities.interaction import Interaction, InteractionChannel
from apex_cxml.entities.loyalty import Loyalty, LoyaltyTier
from apex_cxml.entities.order import Order, OrderStatus

__all__ = [
    "Customer",
    "CustomerStatus",
    "Interaction",
    "InteractionChannel",
    "Loyalty",
    "LoyaltyTier",
    "Order",
    "OrderStatus",
]
