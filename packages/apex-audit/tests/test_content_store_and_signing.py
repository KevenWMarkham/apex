"""Content-addressed store + row signing (BL.P.82, BL.P.84)."""

from __future__ import annotations

from apex_audit import (
    ContentAddressedStore,
    content_hash,
    sign_row,
    verify_row,
)


class TestContentHash:
    def test_deterministic(self) -> None:
        a = content_hash({"a": 1, "b": 2})
        b = content_hash({"b": 2, "a": 1})  # key-order agnostic
        assert a == b
        assert a.startswith("sha256:")

    def test_different_inputs_differ(self) -> None:
        assert content_hash({"a": 1}) != content_hash({"a": 2})


class TestContentAddressedStore:
    def test_put_returns_hash_and_is_idempotent(self) -> None:
        store = ContentAddressedStore()
        h1 = store.put({"x": 1})
        h2 = store.put({"x": 1})
        assert h1 == h2
        assert len(store) == 1

    def test_get_roundtrip(self) -> None:
        store = ContentAddressedStore()
        ref = store.put({"x": "abc"})
        assert store.get(ref) == {"x": "abc"}


class TestSigning:
    def test_round_trip(self) -> None:
        row = {"trace_id": "t", "decision_id": "d", "payload": {"a": 1}}
        sig = sign_row(row, key=b"secret")
        row["signature"] = sig
        assert verify_row(row, key=b"secret") is True

    def test_tamper_detected(self) -> None:
        row = {"trace_id": "t", "decision_id": "d", "payload": {"a": 1}}
        row["signature"] = sign_row(row, key=b"secret")
        row["payload"] = {"a": 2}  # tamper
        assert verify_row(row, key=b"secret") is False

    def test_wrong_key_fails(self) -> None:
        row = {"trace_id": "t", "payload": 1}
        row["signature"] = sign_row(row, key=b"k1")
        assert verify_row(row, key=b"k2") is False

    def test_missing_signature_is_invalid(self) -> None:
        assert verify_row({"trace_id": "t"}, key=b"k") is False
