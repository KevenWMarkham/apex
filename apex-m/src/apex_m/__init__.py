"""APEX-M — Microsoft variant of APEX.

Implements the 10 APEX-Core protocols against the Microsoft platform, plus
APEX-M-local capability providers (like `persona_resolver` and the
`ai_services_foundry` AI Services tool layer) that a variant may ship on
top of the core contract. First-shipped variant; APEX-G and APEX-A are
sibling products.

Imports of concrete impls are lazy — `apex_m.runtime_foundry` etc. — to
avoid pulling SDK dependencies until the impl is actually instantiated.
"""

__version__ = "0.1.0"
__variant__ = "APEX-M"
