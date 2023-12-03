"""Tests for day 3."""

from day_03.solution import calculate_power_consumption, calculate_life_support_rating

_EXAMPLE_INPUT = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def test_example_power_consumption_is_recovered():
    assert calculate_power_consumption(_EXAMPLE_INPUT) == 198


def test_example_life_support_rating_is_recovered():
    assert calculate_life_support_rating(_EXAMPLE_INPUT) == 230
