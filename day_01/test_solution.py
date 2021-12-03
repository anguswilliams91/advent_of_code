"""Tests for solution."""

import pytest

from day_01.solution import count_number_of_depth_increases


_EXAMPLE_INPUT = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


@pytest.mark.parametrize("window_size,expected", [(1, 7), (3, 5)])
def test_example_solution_is_recovered(window_size, expected):
    assert (
        count_number_of_depth_increases(_EXAMPLE_INPUT, window_size=window_size)
        == expected
    )
