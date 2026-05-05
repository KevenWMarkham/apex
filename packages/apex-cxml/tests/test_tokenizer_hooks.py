"""Tests for ``apex_cxml.tokenizer_hooks.tokenized_fields``."""

from __future__ import annotations

from apex_core.types import Classification
from apex_cxml import Customer, Loyalty, Order, tokenized_fields


def test_customer_pii_fields_discovered() -> None:
    fields = tokenized_fields(Customer)
    names = {(f.entity, f.field) for f in fields}
    assert ("Customer", "full_name_token") in names
    assert ("Customer", "email_token") in names
    assert ("Customer", "phone_token") in names
    assert ("Customer", "address_token") in names


def test_classifications_are_correct() -> None:
    by_name = {f.field: f for f in tokenized_fields(Customer, Loyalty, Order)}
    assert by_name["email_token"].classification is Classification.PII
    assert by_name["member_number_token"].classification is Classification.MEMBER_ONLY
    assert by_name["payment_method_token"].classification is Classification.PCI


def test_non_tokenised_fields_excluded() -> None:
    fields = tokenized_fields(Customer)
    names = {f.field for f in fields}
    assert "birth_year" not in names           # no classification → not tokenised
    assert "consent_marketing" not in names    # not tokenised
    assert "status" not in names               # enum — not a token target


def test_result_sorted_by_entity_and_field() -> None:
    fields = tokenized_fields(Customer, Loyalty, Order)
    key = [(f.entity, f.field) for f in fields]
    assert key == sorted(key)
