"""Tests for day 18."""

from functools import reduce

import pytest

from day_18.solution import (
    SnailfishNumber,
    calculate_magnitude_of_homework_assignment,
    find_largest_magnitude_of_pair,
)

_EXAMPLE_INPUT = [
    "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
    "[[[5,[2,8]],4],[5,[[9,9],0]]]",
    "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
    "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
    "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
    "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
    "[[[[5,4],[7,7]],8],[[8,3],8]]",
    "[[9,3],[[9,9],[6,[4,9]]]]",
    "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
    "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
]


@pytest.mark.parametrize(
    "numbers,expected",
    [
        (
            ["[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"],
            "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
        ),
        (["[1,1]", "[2,2]", "[3,3]", "[4,4]"], "[[[[1,1],[2,2]],[3,3]],[4,4]]"),
        (
            ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"],
            "[[[[3,0],[5,3]],[4,4]],[5,5]]",
        ),
        (
            ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"],
            "[[[[5,0],[7,4]],[5,5]],[6,6]]",
        ),
        (
            [
                "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
                "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
                "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
                "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
                "[7,[5,[[3,8],[1,4]]]]",
                "[[2,[2,2]],[8,[8,1]]]",
                "[2,9]",
                "[1,[[[9,3],9],[[9,0],[0,7]]]]",
                "[[[5,[7,4]],7],1]",
                "[[[[4,2],2],6],[8,7]]",
            ],
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
        ),
    ],
)
def test_reduce(numbers, expected):
    reduced_number = reduce(
        lambda a, b: a + b, (SnailfishNumber.from_string(e) for e in numbers)
    )
    print(reduced_number.magnitude)
    assert reduced_number == SnailfishNumber.from_string(expected)


@pytest.mark.parametrize(
    "number,expected",
    [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ],
)
def test_magnitude(number, expected):
    assert SnailfishNumber.from_string(number).magnitude == expected


def test_part_one_example_solution_is_recovered():
    assert calculate_magnitude_of_homework_assignment(_EXAMPLE_INPUT) == 4140


def test_part_two_example_solution_is_recovered():
    assert find_largest_magnitude_of_pair(_EXAMPLE_INPUT) == 3993
