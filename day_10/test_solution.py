"""Tests for day 10."""

from day_10.solution import (
    calculate_syntax_score_of_navigation_subsystem,
    calculate_completion_score_of_navigation_subsystem,
)

_TEST_INPUT = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


def test_part_one_example_solution_is_recovered():
    assert calculate_syntax_score_of_navigation_subsystem(_TEST_INPUT) == 26397


def test_part_two_example_solution_is_recovered():
    assert calculate_completion_score_of_navigation_subsystem(_TEST_INPUT) == 288957
