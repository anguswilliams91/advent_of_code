"""Tests for day 7."""

from day_07.solution import (
    find_fuel_spend_using_complex_rule,
    find_fuel_spend_using_simple_rule,
)

_EXAMPLE_INPUT = "16,1,2,0,4,2,7,1,2,14"


def test_example_part_one_solution_is_recovered():
    assert find_fuel_spend_using_simple_rule(_EXAMPLE_INPUT) == 37


def test_example_part_two_solution_is_recovered():
    assert find_fuel_spend_using_complex_rule(_EXAMPLE_INPUT) == 168

