# APEX Bronze landing templates

Parameterised PySpark reference templates for the five Bronze landing patterns defined in `docs/APEX - Design and Build/APEX_Design.md` §6.2.

| Pattern | Template | When to use |
|---------|----------|-------------|
| Mirrored Database | `mirrored_database.py` | Source has CDC (Azure SQL / Cosmos / Snowflake / PostgreSQL / MongoDB / Oracle) |
| Eventstream / Eventhouse | `eventstream.py` | High-volume real-time events (Event Hubs / Kafka / MQTT) |
| Data Pipeline | `data_pipeline.py` | Scheduled batch from SORs without CDC |
| Dataflow Gen2 | `dataflow_gen2.py` | REST/SaaS sources (Salesforce / Workday / ServiceNow) |
| Custom Endpoint | `custom_endpoint.py` | Webhook / legacy / niche sources |

## How to use

1. Copy the template that matches your source pattern into a Fabric notebook (or keep as-is for Python pipelines).
2. Replace the `landing_config()` body with concrete values (or wire to env-vars / key vault).
3. Wire the target Bronze table's DDL via `generate_bronze_ddl(config, user_columns={...})`.
4. Wire the dead-letter table once per workspace via `dead_letter_ddl()`.
5. Register the retention policy via `build_purview_retention_payload(config.retention, asset_path="...")` (Purview REST call handled by tenant-auth wrapper).

## Why these aren't pytest-collected

Root `pyproject.toml` sets `testpaths = ["packages"]`. These files run inside Fabric's PySpark runtime, not in the CI venv — they import `pyspark` via `TYPE_CHECKING` guards so lint / type-check pass locally without installing pyspark.

## Runtime assumption

Inside a Fabric notebook, the `spark` SparkSession binding is pre-created. Each template exposes a `run(config, spark)` entry-point the notebook calls as `run(landing_config(), spark)`.
