"""APEX-M integration tests — run against a real Microsoft tenant.

These tests are gated by the `integration` pytest mark so the default
`pytest` run skips them. CI lane runs them via Workload Identity
Federation against a dedicated Lab tenant.

Per Sprint 41 item 41.3.3.
"""
