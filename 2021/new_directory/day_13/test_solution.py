"""Tests for day 13."""

from day_13.solution import (
    count_number_of_visible_dots_after_first_fold,
    follow_all_instructions,
)

_EXAMPLE_INPUT = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


_EXAMPLE_PART_TWO_ANSWER = """#####
#...#
#...#
#...#
#####
.....
....."""


def test_part_one_example_solution_is_recovered():
    assert count_number_of_visible_dots_after_first_fold(_EXAMPLE_INPUT) == 17


def test_part_two_example_solution_is_recovered():
    assert str(follow_all_instructions(_EXAMPLE_INPUT)) == _EXAMPLE_PART_TWO_ANSWER

