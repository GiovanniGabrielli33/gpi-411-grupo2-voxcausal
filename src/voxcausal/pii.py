"""Filtro de datos personales (PII) antes de enviar texto al LLM (meta: 0 casos)."""

from __future__ import annotations

import re

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("TARJETA", re.compile(r"\b(?:\d[ -]?){13,19}\b")),
    ("RUT", re.compile(r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b")),
    ("TELEFONO", re.compile(r"(?:\+?56\s?)?\b9\s?\d{4}\s?\d{4}\b")),
]


def scrub(text: str) -> tuple[str, int]:
    """Reemplaza cada dato personal por una etiqueta y devuelve (texto, cantidad)."""
    total = 0
    for label, pattern in _PATTERNS:
        text, n = pattern.subn(f"[{label}]", text)
        total += n
    return text, total


def contains_pii(text: str) -> bool:
    return any(p.search(text) for _, p in _PATTERNS)
