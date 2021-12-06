"""Tests for day 6."""

import pytest

from day_06.solution import find_total_lanternfish

_EXAMPLE_INPUT = "3,4,3,1,2"


@pytest.mark.parametrize("days,expected", [(18, 26), (80, 5934), (256, 26984457539)])
def test_example_solution_is_recovered(days, expected):
    assert find_total_lanternfish(_EXAMPLE_INPUT, days) == expected
