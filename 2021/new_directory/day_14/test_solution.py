"""Tests for day 14."""

import pytest

from day_14.solution import calculate_difference_of_most_and_least_common_element_counts

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


@pytest.mark.parametrize("steps,expected", [(10, 1588), (40, 2188189693529)])
def test_example_solution_is_recovered(steps, expected):
    assert (
        calculate_difference_of_most_and_least_common_element_counts(
            _EXAMPLE_INPUT, steps=steps
        )
        == expected
    )

