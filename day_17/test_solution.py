"""Tests for day 17."""

from day_17.solution import (
    calculate_highest_possible_y_coordinate,
    calculate_number_of_solutions,
)


def test_part_one_example_solution_is_recovered():
    assert calculate_highest_possible_y_coordinate(-10, -5, 20, 30) == 45


def test_part_two_example_solution_is_recovered():
    assert calculate_number_of_solutions(-10, -5, 20, 30) == 112
