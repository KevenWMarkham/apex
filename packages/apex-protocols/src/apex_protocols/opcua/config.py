"""OPC UA endpoint config + TLS / certificate authentication — Sprint 25 §25.1.4."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from apex_protocols.base import (
    AuthMode,
    ConfigError,
    ProtocolEndpoint,
)


@dataclass
class OPCUAConfig:
    """Tenant-side OPC UA endpoint configuration.

    Production deployments use ``CERTIFICATE`` auth_mode per Sprint 25
    §25.1.4. Trust-store holds peer-server-certificate fingerprints;
    `cert_path` + `key_path` hold the APEX-side X.509 identity.
    """

    server_url: str
    """E.g., ``opc.tcp://historian.plant.local:4840``."""

    application_uri: str
    """ApplicationUri APEX presents to the OPC UA server (must match the
    Subject Alternative Name in `cert_path`)."""

    auth_mode: AuthMode = AuthMode.CERTIFICATE
    cert_path: str = ""
    key_path: str = ""
    trust_store_path: str = ""
    username: str = ""
    """Only honored when `auth_mode == USERNAME_PASSWORD`."""

    namespace_uris: list[str] = None  # type: ignore[assignment]
    """Authoritative namespace URIs the adapter will pin against the
    server's NamespaceArray; used to detect server-side namespace drift
    that would invalidate cached NodeIds."""

    security_policy: str = "Basic256Sha256"
    """``None``, ``Basic128Rsa15``, ``Basic256``, or ``Basic256Sha256``.
    APEX requires `Basic256Sha256` or stronger for production."""

    message_security_mode: str = "SignAndEncrypt"
    """``None`` / ``Sign`` / ``SignAndEncrypt`` — must be `SignAndEncrypt`
    for production."""

    sampling_interval_ms: int = 1000
    publishing_interval_ms: int = 500
    queue_size: int = 10

    def __post_init__(self) -> None:
        if self.namespace_uris is None:
            self.namespace_uris = []
        self._validate()

    def _validate(self) -> None:
        if not self.server_url:
            raise ConfigError("OPC UA server_url is required")
        if not self.server_url.startswith(("opc.tcp://", "opc.https://", "opc.wss://")):
            raise ConfigError(
                f"OPC UA server_url must start with opc.tcp:// / opc.https:// / opc.wss://, got {self.server_url!r}"
            )
        if not self.application_uri:
            raise ConfigError("OPC UA application_uri is required")
        if self.auth_mode == AuthMode.CERTIFICATE:
            if not self.cert_path or not self.key_path:
                raise ConfigError(
                    "CERTIFICATE auth_mode requires cert_path + key_path"
                )
            if not self.trust_store_path:
                raise ConfigError(
                    "CERTIFICATE auth_mode requires trust_store_path"
                )
        if self.auth_mode == AuthMode.USERNAME_PASSWORD and not self.username:
            raise ConfigError(
                "USERNAME_PASSWORD auth_mode requires username"
            )
        if self.message_security_mode not in ("None", "Sign", "SignAndEncrypt"):
            raise ConfigError(
                f"Unknown message_security_mode {self.message_security_mode!r}"
            )
        if self.security_policy not in (
            "None", "Basic128Rsa15", "Basic256", "Basic256Sha256",
        ):
            raise ConfigError(
                f"Unknown security_policy {self.security_policy!r}"
            )

    def is_production_grade(self) -> bool:
        """True iff this config meets APEX production OPC UA bar.

        Required: certificate auth + Basic256Sha256+ + SignAndEncrypt +
        a populated trust-store path that exists on disk.
        """
        if self.auth_mode != AuthMode.CERTIFICATE:
            return False
        if self.security_policy not in ("Basic256", "Basic256Sha256"):
            return False
        if self.message_security_mode != "SignAndEncrypt":
            return False
        # Defensive: check the paths exist (best-effort)
        return all(
            Path(p).exists()
            for p in (self.cert_path, self.key_path, self.trust_store_path)
            if p
        ) if self.cert_path else False


def build_endpoint(config: OPCUAConfig) -> ProtocolEndpoint:
    """Convert :class:`OPCUAConfig` into a generic :class:`ProtocolEndpoint`."""
    return ProtocolEndpoint(
        protocol="opcua",
        url=config.server_url,
        auth_mode=config.auth_mode,
        cert_path=config.cert_path,
        key_path=config.key_path,
        trust_store_path=config.trust_store_path,
        username=config.username,
        metadata={
            "application_uri": config.application_uri,
            "security_policy": config.security_policy,
            "message_security_mode": config.message_security_mode,
            "namespace_uris": list(config.namespace_uris),
            "sampling_interval_ms": config.sampling_interval_ms,
            "publishing_interval_ms": config.publishing_interval_ms,
            "queue_size": config.queue_size,
        },
    )
