import pytest

from voxcausal.latency import critical_path, meets_target, p95, slack, windows


def test_budget_matches_report():
    assert critical_path() == 175
    assert slack() == 75


def test_windows_count_and_size():
    audio = [0.0] * (16_000 * 4)  # 4 s
    ws = list(windows(audio))
    assert len(ws) == 5  # 0; 0,5; 1; 1,5; 2 s
    assert all(len(w) == 32_000 for w in ws)


def test_windows_short_audio_and_bad_params():
    assert list(windows([0.0] * 100)) == []
    with pytest.raises(ValueError):
        list(windows([0.0], rate=0))


def test_p95_and_target():
    samples = list(range(1, 101))
    assert p95(samples) == 95
    assert meets_target([180.0] * 99 + [400.0])
    assert not meets_target([260.0] * 10)
    with pytest.raises(ValueError):
        p95([])
