"""Motor causal: estimación del efecto de una causa operativa sobre la fuga.

Implementa el ajuste por la puerta trasera (backdoor) sobre un confusor discreto,
que es el mismo criterio que usa EconML DML en producción cuando el confusor es
categórico. Se usa para validar la meta de precisión del caso (error de ATE <= 0,05).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Hashable, Iterable, Sequence

import numpy as np


@dataclass(frozen=True)
class Record:
    """Una llamada: confusor (z), tratamiento binario (t) y resultado binario (y)."""

    z: Hashable
    t: int
    y: int


@dataclass(frozen=True)
class Estimate:
    naive: float
    adjusted: float
    n: int


def _mean(values: Sequence[int]) -> float:
    if not values:
        raise ValueError("estrato sin observaciones")
    return sum(values) / len(values)


def naive_difference(records: Iterable[Record]) -> float:
    """Diferencia directa de tasas entre tratados y no tratados (sesgada si hay confusión)."""
    treated, control = [], []
    for r in records:
        (treated if r.t else control).append(r.y)
    return _mean(treated) - _mean(control)


def backdoor_ate(records: Iterable[Record]) -> float:
    """ATE ajustado: promedio del efecto dentro de cada estrato del confusor, ponderado por P(z)."""
    strata: dict[Hashable, dict[int, list[int]]] = defaultdict(lambda: {0: [], 1: []})
    n = 0
    for r in records:
        if r.t not in (0, 1) or r.y not in (0, 1):
            raise ValueError("t e y deben ser binarios")
        strata[r.z][r.t].append(r.y)
        n += 1
    if n == 0:
        raise ValueError("sin observaciones")
    ate = 0.0
    for groups in strata.values():
        weight = (len(groups[0]) + len(groups[1])) / n
        ate += weight * (_mean(groups[1]) - _mean(groups[0]))
    return ate


def estimate(records: Sequence[Record]) -> Estimate:
    return Estimate(naive=naive_difference(records), adjusted=backdoor_ate(records), n=len(records))


def simulate(n: int, seed: int = 42) -> list[Record]:
    """Datos sintéticos del Anexo D: efecto real de la transferencia = +8 pp en ambos estratos.

    z = 1 si el cliente ya había llamado antes (40%). Los que llamaron antes son
    transferidos más (60% vs 25%) y se fugan más por sí solos.
    """
    rng = np.random.default_rng(seed)
    z = rng.random(n) < 0.40
    t = rng.random(n) < np.where(z, 0.60, 0.25)
    base = np.where(z, 0.27, 0.07)
    y = rng.random(n) < base + 0.08 * t
    return [Record(int(a), int(b), int(c)) for a, b, c in zip(z, t, y)]


def ate_error(estimated: float, true_effect: float) -> float:
    return abs(estimated - true_effect)
