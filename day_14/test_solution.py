"""Tests for day 14."""

import pytest

from day_14.solution import (
    evolve_polymer_set,
    calculate_difference_between_most_common_and_least_common_elements,
)

_EXAMPLE_INPUT = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


@pytest.mark.parametrize(
    "steps,expected",
    [
        (1, list("NCNBCHB")),
        (2, list("NBCCNBBBCBHCB")),
        (3, list("NBBBCNCCNBBNBNBBCHBHHBCHB")),
        (4, list("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")),
    ],
)
def test_part_one_example_evolutions(steps, expected):
    assert evolve_polymer_set(_EXAMPLE_INPUT, steps=steps).polymer_template == expected


@pytest.mark.parametrize("steps,expected", [(10, 1588), (40, 2188189693529)])
def test_example_solution_is_recovered(steps, expected):
    assert (
        calculate_difference_between_most_common_and_least_common_elements(
            _EXAMPLE_INPUT, steps=steps
        )
        == expected
    )

