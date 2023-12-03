"""Tests for day two."""

import pytest

from day_02.solution import (
    follow_instructions_and_calculate_puzzle_answer,
    SubmarinePositionWithAim,
    SubmarinePositionWithoutAim,
)

_EXAMPLE_INPUT = """forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


@pytest.mark.parametrize(
    "submarine_position_cls,expected",
    [(SubmarinePositionWithoutAim, 150), (SubmarinePositionWithAim, 900)],
)
def test_example_solution_is_recovered(submarine_position_cls, expected):
    assert (
        follow_instructions_and_calculate_puzzle_answer(
            _EXAMPLE_INPUT, submarine_position_cls
        )
        == expected
    )
