"""Tests for day 12."""

import pytest

from day_12.solution import find_number_of_paths_from_start_to_end

_SMALL_EXAMPLE_INPUT = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

_MEDIUM_EXAMPLE_INPUT = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

_LARGE_EXAMPLE_INPUT = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


@pytest.mark.parametrize(
    "caves,expected",
    [
        (_SMALL_EXAMPLE_INPUT, 10),
        (_MEDIUM_EXAMPLE_INPUT, 19),
        (_LARGE_EXAMPLE_INPUT, 226),
    ],
)
def test_part_one_example_solution_is_recovered(caves, expected):
    assert find_number_of_paths_from_start_to_end(caves) == expected


@pytest.mark.parametrize(
    "caves,expected",
    [
        (_SMALL_EXAMPLE_INPUT, 36),
        (_MEDIUM_EXAMPLE_INPUT, 103),
        (_LARGE_EXAMPLE_INPUT, 3509),
    ],
)
def test_part_two_example_solution_is_recovered(caves, expected):
    assert (
        find_number_of_paths_from_start_to_end(caves, no_returns_allowed=False)
        == expected
    )

