"""MessageBus protocol — pub/sub + activator-style triggers.

APEX-M satisfies via Fabric Eventstream (with Activator destination GA
Nov 2025) + Service Bus / Event Grid for Azure-native integrations.
APEX-G satisfies via Pub/Sub + Eventarc.
APEX-A satisfies via SNS/SQS + EventBridge.

Adapters: cloud.aws.eventbridge, cloud.gcp.pubsub, cloud.azure.event_grid
all satisfy this protocol for cross-cloud event routing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class Message:
    """A message published to a topic, with payload, correlation id, and headers."""

    topic: str
    payload: dict[str, Any]
    correlation_id: str
    classification: str = "T1"
    headers: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Subscription:
    """A registered topic subscription bound to a runtime handler."""

    subscription_id: str
    topic: str
    handler_ref: str  # e.g., "apex-m:rc-e2e-03:cold-chain-trigger"
    filter: str | None = None  # provider-specific filter expression


@runtime_checkable
class MessageBus(Protocol):
    """Publish, subscribe, activator-style triggers."""

    variant: str

    def publish(self, msg: Message) -> str:
        """Publish a message. Returns provider-specific message id."""
        ...

    def subscribe(
        self,
        *,
        topic: str,
        handler_ref: str,
        filter: str | None = None,  # noqa: A002  # public protocol keyword
    ) -> Subscription:
        """Register a subscription. Handler is invoked by the runtime."""
        ...

    def attach_activator(
        self,
        *,
        subscription_id: str,
        rule: str,
        action: dict[str, Any],
    ) -> str:
        """Attach an activator-style rule and return the activator id.

        The rule (Eventstream Activator on APEX-M) fires `action` when `rule`
        matches an inbound message.
        """
        ...
