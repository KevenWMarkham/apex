"""Tests for apex_identity.signing."""

from __future__ import annotations

from apex_identity import sign_response, verify_response


def test_sign_deterministic() -> None:
    payload = {"result": "ok", "count": 3}
    a = sign_response(payload, agent_id="agent-1", tenant_id="t")
    b = sign_response(payload, agent_id="agent-1", tenant_id="t")
    assert a == b


def test_verify_roundtrip() -> None:
    payload = {"k": 1}
    sig = sign_response(payload, agent_id="agent-1", tenant_id="t")
    assert verify_response(payload, sig, agent_id="agent-1", tenant_id="t")


def test_verify_rejects_wrong_signature() -> None:
    payload = {"k": 1}
    sig = sign_response(payload, agent_id="agent-1", tenant_id="t")
    assert not verify_response(payload, sig[::-1], agent_id="agent-1", tenant_id="t")


def test_verify_rejects_tampered_payload() -> None:
    original = {"k": 1}
    sig = sign_response(original, agent_id="agent-1", tenant_id="t")
    tampered = {"k": 2}
    assert not verify_response(tampered, sig, agent_id="agent-1", tenant_id="t")


def test_different_agents_different_signatures() -> None:
    payload = {"k": 1}
    a = sign_response(payload, agent_id="agent-A", tenant_id="t")
    b = sign_response(payload, agent_id="agent-B", tenant_id="t")
    assert a != b


def test_different_tenants_different_signatures() -> None:
    payload = {"k": 1}
    a = sign_response(payload, agent_id="agent-1", tenant_id="t1")
    b = sign_response(payload, agent_id="agent-1", tenant_id="t2")
    assert a != b


def test_dict_key_ordering_normalised() -> None:
    a = sign_response({"a": 1, "b": 2}, agent_id="x", tenant_id="t")
    b = sign_response({"b": 2, "a": 1}, agent_id="x", tenant_id="t")
    assert a == b
