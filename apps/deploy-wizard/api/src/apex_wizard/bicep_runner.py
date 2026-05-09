"""Subprocess wrapper around `az deployment group create` and `what-if`.

Concrete implementation deferred. Contract:

    run_what_if(tenant, blueprint_path, parameters_path) -> dict
        Returns a structured diff: { added: [...], modified: [...], deleted: [...] }.

    run_deploy(tenant, blueprint_path, parameters_path) -> str
        Returns the Azure deployment correlation id. Streams stdout to logger.
"""
from __future__ import annotations


def run_what_if(tenant: str, blueprint_path: str, parameters_path: str) -> dict:
    raise NotImplementedError


def run_deploy(tenant: str, blueprint_path: str, parameters_path: str) -> str:
    raise NotImplementedError
