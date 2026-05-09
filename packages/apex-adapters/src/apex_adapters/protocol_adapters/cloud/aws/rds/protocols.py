"""Protocol declarations for the AWS RDS adapter.

SATISFIES is the canonical list of APEX-Core protocols this adapter
provides. The wizard validator reads this when a use-case
client_approved_architecture block references this adapter.
"""

ADAPTER_NAME = "cloud.aws.rds"
PROVIDER_LABEL = "AWS RDS"
SATISFIES = [
    'DataLake',
]
