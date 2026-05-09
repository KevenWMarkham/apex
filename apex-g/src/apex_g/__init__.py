"""APEX-G — Google Cloud variant of APEX (stub).

APEX-G is a sibling product to APEX-M (Microsoft) and APEX-A (AWS).
Concrete implementations are stubbed today and ship when a Deloitte
client commissions a Google Cloud variant deployment.

Importing any concrete impl raises NotImplementedError with a pointer to
the port plan. Protocol-level imports work — `apex_g` is a real Python
package with the structure to grow into.
"""

__version__ = "0.1.0-stub"
__variant__ = "APEX-G"


_PORT_PLAN_REF = "docs/apex-core/Multi-Cloud-Port-Plan.md#apex-g"


def _stub(protocol_name: str):
    """Helper used by every concrete-impl module in apex_g to raise
    consistent NotImplementedError messages."""
    raise NotImplementedError(
        f"APEX-G {protocol_name} implementation is a stub. "
        f"APEX-G ships when a client commissions a Google Cloud variant. "
        f"See {_PORT_PLAN_REF} for the sequence."
    )
