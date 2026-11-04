import pytest

from voxcausal.guardian import LatencyGuardian


class FakeClock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def make(budget=35.0):
    clock = FakeClock()
    return LatencyGuardian({"transferencia": 0.08}, budget_ms=budget, clock=clock), clock


def test_online_within_budget():
    g, clock = make()

    def infer(_):
        clock.t += 0.010
        return 0.09

    r = g.run("transferencia", infer)
    assert (r.source, r.effect) == ("online", 0.09)
    assert g.fallback_rate == 0


def test_slow_model_uses_precomputed():
    g, clock = make()

    def infer(_):
        clock.t += 0.050
        return 0.09

    r = g.run("transferencia", infer)
    assert (r.source, r.effect) == ("precomputed", 0.08)


def test_model_error_uses_precomputed():
    g, _ = make()

    def infer(_):
        raise RuntimeError("GPU caída")

    assert g.run("transferencia", infer).source == "precomputed"


def test_unknown_cause_raises():
    g, _ = make()
    with pytest.raises(KeyError):
        g.run("otra", lambda _: 1 / 0)


def test_fallback_rate_target():
    g, clock = make()
    assert g.fallback_rate == 0.0

    def fast(_):
        clock.t += 0.001
        return 0.1

    for _ in range(99):
        g.run("transferencia", fast)
    g.run("transferencia", lambda _: 1 / 0)
    assert g.fallback_rate == pytest.approx(0.01)
    assert g.within_target()
