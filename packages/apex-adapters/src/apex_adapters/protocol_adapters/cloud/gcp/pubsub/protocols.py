"""Protocol declarations for the Google Pub/Sub adapter.

SATISFIES is the canonical list of APEX-Core protocols this adapter
provides. The wizard validator reads this when a use-case
client_approved_architecture block references this adapter.
"""

ADAPTER_NAME = "cloud.gcp.pubsub"
PROVIDER_LABEL = "Google Pub/Sub"
SATISFIES = [
    'MessageBus',
]
