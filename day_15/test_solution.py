"""Tests for day 15."""

import pytest

from day_15.solution import find_risk_of_path_with_lowest_total_risk

_EXAMPLE_INPUT = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


@pytest.mark.parametrize("use_full_map,expected", [(False, 40), (True, 315)])
def test_example_solution_is_recovered(use_full_map, expected):
    assert (
        find_risk_of_path_with_lowest_total_risk(
            _EXAMPLE_INPUT, use_full_map=use_full_map
        )
        == expected
    )
