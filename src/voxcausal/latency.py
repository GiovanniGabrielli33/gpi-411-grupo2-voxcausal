"""Ventaneo de audio y presupuesto de latencia del camino crítico (p95 < 250 ms)."""

from __future__ import annotations

import math
from typing import Iterator, Mapping, Sequence

TARGET_P95_MS = 250.0

# Presupuesto por tramo (ms), Parte I sección I.3 del informe.
BUDGET_MS: Mapping[str, float] = {
    "red": 20, "ventaneo": 15, "prosodia": 40, "gpu": 45, "causal": 35, "wss": 20,
}


def windows(samples: Sequence[float], rate: int = 16_000, size_s: float = 2.0,
            hop_s: float = 0.5) -> Iterator[Sequence[float]]:
    """Ventanas deslizantes sobre el audio del cliente (solo voz del cliente, D6)."""
    if rate <= 0 or size_s <= 0 or hop_s <= 0:
        raise ValueError("parámetros de ventaneo deben ser positivos")
    size, hop = int(rate * size_s), int(rate * hop_s)
    for start in range(0, max(len(samples) - size + 1, 0), hop):
        yield samples[start:start + size]


def critical_path(budget: Mapping[str, float] = BUDGET_MS) -> float:
    return float(sum(budget.values()))


def slack(budget: Mapping[str, float] = BUDGET_MS, target: float = TARGET_P95_MS) -> float:
    return target - critical_path(budget)


def p95(samples_ms: Sequence[float]) -> float:
    """Percentil 95 por rango más cercano."""
    if not samples_ms:
        raise ValueError("sin mediciones")
    ordered = sorted(samples_ms)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]


def meets_target(samples_ms: Sequence[float], target: float = TARGET_P95_MS) -> bool:
    return p95(samples_ms) < target
