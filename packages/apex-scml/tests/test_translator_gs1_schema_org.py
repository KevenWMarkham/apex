"""Round-trip tests for the GS1 ↔ Schema.org translator."""

from __future__ import annotations

import pytest

from apex_scml.translators import (
    gs1_gtin_to_schema_org_product,
    schema_org_product_to_gs1_gtin,
)


class TestForward:
    def test_gtin14_maps_to_gtin14_property(self) -> None:
        product = gs1_gtin_to_schema_org_product("09780201379624")
        assert product["@type"] == "Product"
        assert product["gtin14"] == "09780201379624"

    def test_gtin13_maps_to_gtin13_property(self) -> None:
        product = gs1_gtin_to_schema_org_product("9780201379624")
        assert product["gtin13"] == "9780201379624"

    def test_gtin12_and_gtin8(self) -> None:
        assert gs1_gtin_to_schema_org_product("123456789012")["gtin12"] == "123456789012"
        assert gs1_gtin_to_schema_org_product("12345678")["gtin8"] == "12345678"

    def test_optional_name_and_description(self) -> None:
        product = gs1_gtin_to_schema_org_product(
            "09780201379624", name="Milk 1gal", description="Whole milk"
        )
        assert product["name"] == "Milk 1gal"
        assert product["description"] == "Whole milk"

    def test_invalid_length_rejected(self) -> None:
        with pytest.raises(ValueError):
            gs1_gtin_to_schema_org_product("12345")

    def test_non_digit_rejected(self) -> None:
        with pytest.raises(ValueError):
            gs1_gtin_to_schema_org_product("ABCDEFGH")


class TestInverse:
    def test_prefers_longest_gtin(self) -> None:
        product = {"gtin14": "09780201379624", "gtin13": "9780201379624"}
        assert schema_org_product_to_gs1_gtin(product) == "09780201379624"

    def test_falls_back_to_shorter(self) -> None:
        assert schema_org_product_to_gs1_gtin({"gtin8": "12345678"}) == "12345678"

    def test_falls_back_to_generic_gtin(self) -> None:
        assert schema_org_product_to_gs1_gtin({"gtin": "12345678"}) == "12345678"

    def test_missing_returns_none(self) -> None:
        assert schema_org_product_to_gs1_gtin({"@type": "Product"}) is None


class TestRoundTrip:
    @pytest.mark.parametrize(
        "gtin",
        ["12345678", "123456789012", "1234567890123", "12345678901234"],
    )
    def test_round_trip(self, gtin: str) -> None:
        product = gs1_gtin_to_schema_org_product(gtin)
        assert schema_org_product_to_gs1_gtin(product) == gtin
