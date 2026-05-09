"""APEX-A — AWS variant of APEX (stub).

APEX-A is a sibling product to APEX-M (Microsoft) and APEX-G (Google
Cloud). Concrete implementations are stubbed today and ship when a
Deloitte client commissions an AWS variant deployment.

Importing any concrete impl raises NotImplementedError with a pointer to
the port plan. Protocol-level imports work — `apex_a` is a real Python
package with the structure to grow into.
"""

__version__ = "0.1.0-stub"
__variant__ = "APEX-A"


_PORT_PLAN_REF = "docs/apex-core/Multi-Cloud-Port-Plan.md#apex-a"


def _stub(protocol_name: str):
    """Helper used by every concrete-impl module in apex_a to raise
    consistent NotImplementedError messages."""
    raise NotImplementedError(
        f"APEX-A {protocol_name} implementation is a stub. "
        f"APEX-A ships when a client commissions an AWS variant. "
        f"See {_PORT_PLAN_REF} for the sequence."
    )
