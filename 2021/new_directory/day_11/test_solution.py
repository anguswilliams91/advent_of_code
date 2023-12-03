"""Tests for day 11."""

from day_11.solution import (
    calculate_number_of_flashes_after_time_steps,
    find_first_time_step_of_synchronised_flash,
)

_EXAMPLE_INPUT = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


def test_part_one_example_solution_is_recovered():
    assert calculate_number_of_flashes_after_time_steps(_EXAMPLE_INPUT, 100) == 1656


def test_part_two_example_solution_is_recovered():
    assert find_first_time_step_of_synchronised_flash(_EXAMPLE_INPUT) == 195
