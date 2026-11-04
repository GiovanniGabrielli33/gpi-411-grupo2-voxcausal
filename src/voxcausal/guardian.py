"""Guardián de latencia (decisión D2): si la inferencia en línea no responde dentro
del presupuesto, se entrega el efecto precalculado y se cuenta como fallback."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Mapping


@dataclass
class Result:
    effect: float
    source: str  # "online" | "precomputed"
    elapsed_ms: float


@dataclass
class LatencyGuardian:
    precomputed: Mapping[str, float]
    budget_ms: float = 35.0  # tramo causal del presupuesto de 250 ms
    clock: Callable[[], float] = time.perf_counter
    calls: int = field(default=0, init=False)
    fallbacks: int = field(default=0, init=False)

    def run(self, cause: str, infer: Callable[[str], float]) -> Result:
        self.calls += 1
        start = self.clock()
        try:
            effect = infer(cause)
        except Exception:  # noqa: BLE001 - cualquier fallo del modelo activa el fallback
            return self._fallback(cause, start)
        elapsed = (self.clock() - start) * 1000
        if elapsed > self.budget_ms:
            return self._fallback(cause, start)
        return Result(effect, "online", elapsed)

    def _fallback(self, cause: str, start: float) -> Result:
        self.fallbacks += 1
        if cause not in self.precomputed:
            raise KeyError(f"sin efecto precalculado para '{cause}'")
        return Result(self.precomputed[cause], "precomputed", (self.clock() - start) * 1000)

    @property
    def fallback_rate(self) -> float:
        return self.fallbacks / self.calls if self.calls else 0.0

    def within_target(self, target: float = 0.02) -> bool:
        """Meta de fiabilidad: menos de 2% de respuestas en fallback."""
        return self.fallback_rate < target
