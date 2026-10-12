"""Checks that caching leaves Basic Theta* results unchanged."""

from random import Random

from graphs.theta_star import theta_star
from graphs.theta_star_cached import CachedCornerGrid, theta_star_cached


def test_same_paths_on_random_grids() -> None:
    rng = Random(201)
    for _ in range(60):
        cells = [[int(rng.random() < 0.3) for _ in range(10)] for _ in range(10)]
        cells[0][0] = cells[-1][-1] = 0
        assert theta_star(cells, (0, 0), (10, 10)) == theta_star_cached(
            cells, (0, 0), (10, 10)
        )


def test_cache_does_not_leak_between_maps() -> None:
    assert CachedCornerGrid([[0]]).line_of_sight((0, 0), (1, 1))
    assert not CachedCornerGrid([[1]]).line_of_sight((0, 0), (1, 1))
