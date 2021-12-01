"""Tests for solution."""
from day_01.solution import count_number_of_depth_increases


_EXAMPLE_INPUT = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_given_example_answer_is_recovered():
    assert count_number_of_depth_increases(_EXAMPLE_INPUT) == 7
