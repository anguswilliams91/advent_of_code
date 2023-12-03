"""Tests for day 9."""

from day_09.solution import sum_of_low_points, product_of_biggest_basins

_EXAMPLE_INPUT = """2199943210
3987894921
9856789892
8767896789
9899965678
"""


def test_part_one_example_solution_is_recovered():
    assert sum_of_low_points(_EXAMPLE_INPUT) == 15


def test_part_two_example_solution_is_recovered():
    assert product_of_biggest_basins(_EXAMPLE_INPUT) == 1134

