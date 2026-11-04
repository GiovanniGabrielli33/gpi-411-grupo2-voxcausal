"""Validación de la política de seguridad del incidente (decisión D4)."""

from __future__ import annotations

from dataclasses import dataclass

ALLOWED_REGIONS = frozenset({"uksouth"})
MAX_SAS_MINUTES = 15
MIN_TLS = (1, 2)


@dataclass(frozen=True)
class StorageAccess:
    region: str
    sas_minutes: int
    tls_version: str  # p. ej. "1.3"
    https_only: bool
    user_delegation: bool


def violations(cfg: StorageAccess) -> list[str]:
    errors = []
    if cfg.region.lower() not in ALLOWED_REGIONS:
        errors.append("región fuera de UK South (residencia de datos GDPR)")
    if not cfg.user_delegation:
        errors.append("SAS debe ser de delegación de usuario (Entra ID)")
    if not 0 < cfg.sas_minutes <= MAX_SAS_MINUTES:
        errors.append(f"SAS debe expirar en <= {MAX_SAS_MINUTES} min")
    if not cfg.https_only:
        errors.append("se permite HTTP sin cifrar")
    try:
        major, minor = (int(x) for x in cfg.tls_version.split("."))
    except ValueError:
        errors.append("versión TLS inválida")
    else:
        if (major, minor) < MIN_TLS:
            errors.append("TLS menor a 1.2")
    return errors


def is_compliant(cfg: StorageAccess) -> bool:
    return not violations(cfg)
