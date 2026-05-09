"""Protocol declarations for the Splunk adapter.

SATISFIES is the canonical list of APEX-Core protocols this adapter
provides. The wizard validator reads this when a use-case
client_approved_architecture block references this adapter.
"""

ADAPTER_NAME = "siem.splunk"
PROVIDER_LABEL = "Splunk"
SATISFIES = [
    'AuditLedger',
    'Observability',
]
