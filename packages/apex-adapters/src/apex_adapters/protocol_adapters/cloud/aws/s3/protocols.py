"""Protocol declarations for the AWS S3 adapter.

SATISFIES is the canonical list of APEX-Core protocols this adapter
provides. The wizard validator reads this when a use-case
client_approved_architecture block references this adapter.
"""

ADAPTER_NAME = "cloud.aws.s3"
PROVIDER_LABEL = "AWS S3"
SATISFIES = [
    'DataLake',
]
