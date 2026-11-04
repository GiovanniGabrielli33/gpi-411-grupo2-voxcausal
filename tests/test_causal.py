import pytest

from voxcausal.causal import Record, ate_error, backdoor_ate, estimate, naive_difference, simulate

TRUE_EFFECT = 0.08


def test_anexo_d_naive_is_biased_and_adjusted_meets_target():
    est = estimate(simulate(200_000, seed=7))
    assert ate_error(est.naive, TRUE_EFFECT) > 0.05
    assert ate_error(est.adjusted, TRUE_EFFECT) <= 0.05


@pytest.mark.parametrize("seed", range(5))
def test_adjusted_error_is_stable_across_seeds(seed):
    assert ate_error(backdoor_ate(simulate(50_000, seed=seed)), TRUE_EFFECT) <= 0.01


def test_hand_example_without_confounding():
    data = [Record("a", 1, 1), Record("a", 1, 0), Record("a", 0, 0), Record("a", 0, 0)]
    assert naive_difference(data) == pytest.approx(0.5)
    assert backdoor_ate(data) == pytest.approx(0.5)


def test_rejects_non_binary_and_empty():
    with pytest.raises(ValueError):
        backdoor_ate([Record("a", 2, 1)])
    with pytest.raises(ValueError):
        backdoor_ate([])


def test_empty_stratum_raises():
    with pytest.raises(ValueError):
        backdoor_ate([Record("a", 1, 1)])
