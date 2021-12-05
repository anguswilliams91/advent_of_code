"""Tests for day 5."""

import pytest

from day_05.solution import count_number_of_points_with_overlapping_lines

_EXAMPLE_INPUT = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


@pytest.mark.parametrize("use_diagonal,expected", [(False, 5), (True, 12)])
def test_example_solution_is_recovered(use_diagonal, expected):
    assert (
        count_number_of_points_with_overlapping_lines(_EXAMPLE_INPUT, use_diagonal)
        == expected
    )
