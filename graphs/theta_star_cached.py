"""Cached corner validity for a Basic Theta* performance experiment.

Nash et al. (2007): https://cdn.aaai.org/AAAI/2007/AAAI07-187.pdf
Programmer: Uzia Peer. Date: 2026-10-12.
"""

from functools import lru_cache

from graphs.theta_star import CornerGrid, Point, _search


class CachedCornerGrid(CornerGrid):
    """Cache repeated corner checks within one immutable grid.

    >>> grid = CachedCornerGrid([[0]])
    >>> grid.valid_corner((0, 0))
    True
    >>> grid.valid_corner((0, 0))
    True
    >>> grid._valid.cache_info().hits
    1
    """

    def __init__(self, cells: list[list[int]]) -> None:
        super().__init__(cells)
        self._valid = lru_cache(maxsize=32768)(super().valid_corner)

    def valid_corner(self, point: Point) -> bool:
        """Cache valid integer corners; keep normal handling for other inputs.

        >>> CachedCornerGrid([[0]]).valid_corner((0, 0))
        True
        """
        if (
            not isinstance(point, tuple)
            or len(point) != 2
            or any(type(value) is not int for value in point)
        ):
            return super().valid_corner(point)
        return self._valid(point)

def theta_star_cached(cells: list[list[int]], start: Point, goal: Point) -> list[Point]:
    """Run the unchanged Basic Theta* search with cached visibility.

    >>> theta_star_cached([[0]], (0, 0), (1, 1))
    [(0, 0), (1, 1)]
    """
    grid = CachedCornerGrid(cells)
    if not grid.valid_corner(start) or not grid.valid_corner(goal):
        raise ValueError("Start and goal must be usable integer grid corners.")
    return _search(grid, start, goal)
