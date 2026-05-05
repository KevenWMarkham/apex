"""Tests for J1939 SPN / PGN seed + catalog loader."""

from __future__ import annotations

from apex_standards_j1939 import (
    SEED_PGNS,
    SEED_SPNS,
    J1939PGN,
    J1939SPN,
    load_pgn_catalog,
    load_spn_catalog,
    lookup_pgn,
    lookup_spn,
)


class TestSeedSpns:
    def test_engine_speed_present(self) -> None:
        spn = lookup_spn(190)
        assert spn is not None
        assert spn.name == "Engine Speed"
        assert spn.units == "rpm"

    def test_missing_spn_returns_none(self) -> None:
        assert lookup_spn(999999) is None

    def test_seed_has_expected_count(self) -> None:
        assert len(SEED_SPNS) >= 15

    def test_seed_entries_have_ranges(self) -> None:
        for spn in SEED_SPNS.values():
            assert spn.range_max > spn.range_min or spn.range_max == spn.range_min


class TestSeedPgns:
    def test_eec1_present(self) -> None:
        pgn = lookup_pgn(61444)
        assert pgn is not None
        assert pgn.acronym == "EEC1"
        assert 190 in pgn.spns  # Engine Speed is in EEC1

    def test_missing_pgn_returns_none(self) -> None:
        assert lookup_pgn(999999) is None


class TestCatalogMerge:
    def test_tenant_catalog_merges_with_seed(self) -> None:
        custom_spn = J1939SPN(
            spn=9999, name="Custom Diag Code", units="code",
            resolution=1.0, offset=0.0, range_min=0.0, range_max=65535.0,
            length_bits=16, category="tenant_custom",
        )
        merged = load_spn_catalog({9999: custom_spn})
        assert 9999 in merged
        assert 190 in merged  # seed still present

    def test_tenant_catalog_overrides_seed(self) -> None:
        override = J1939SPN(
            spn=190, name="Engine Speed (Adjusted)", units="rpm",
            resolution=0.125, offset=0.0, range_min=0.0, range_max=16000.0,
            length_bits=16, category="tenant_adjusted",
        )
        merged = load_spn_catalog({190: override})
        assert merged[190].name == "Engine Speed (Adjusted)"

    def test_pgn_catalog_merge(self) -> None:
        custom_pgn = J1939PGN(
            pgn=0xFEDCB, acronym="CUSTOM", name="Tenant Custom",
            default_priority=6, length_bytes=8, transmission_rate_ms=None,
            spns=(9999,),
        )
        merged = load_pgn_catalog({0xFEDCB: custom_pgn})
        assert 0xFEDCB in merged
        assert 61444 in merged  # seed still present
