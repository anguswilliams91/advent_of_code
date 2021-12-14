"""14. Extended Polymerization."""

from __future__ import annotations

from copy import copy
from collections import Counter
from typing import List, NamedTuple, Set, Tuple


Element = str


class PairInsertionRule(NamedTuple):
    pair: List[Element]
    to_insert: Element

    @classmethod
    def from_string(cls, description: str) -> PairInsertionRule:
        pair_description, to_insert = description.split(" -> ")
        return cls(pair=list(pair_description), to_insert=to_insert)


class PolymerSet(NamedTuple):
    polymer_template: List[Element]
    pair_insertion_rules: Tuple[List[Element]]

    @classmethod
    def from_string(cls, instructions: str) -> PolymerSet:
        polymer_template_description, pair_insertion_rules_description = instructions.split(
            "\n\n"
        )
        polymer_template = list(polymer_template_description)
        pair_insertion_rules = tuple(
            PairInsertionRule.from_string(rule)
            for rule in pair_insertion_rules_description.splitlines()
        )
        return PolymerSet(
            polymer_template=polymer_template, pair_insertion_rules=pair_insertion_rules
        )


def find_matching_indices(
    polymer_template: List[Element], rule: PairInsertionRule
) -> List[Tuple[Element, int]]:
    return [
        (rule.to_insert, i)
        for i in range(len(polymer_template) - 1)
        if polymer_template[i : i + 2] == rule.pair
    ]


def evolve_polymer_set_once(polymer_set: PolymerSet) -> PolymerSet:
    matches = []
    for rule in polymer_set.pair_insertion_rules:
        matches.extend(find_matching_indices(polymer_set.polymer_template, rule))
    sorted_matches = sorted(matches, key=lambda x: x[1])
    num_inserts = 0
    new_polymer_template = copy(polymer_set.polymer_template)
    for match in sorted_matches:
        element_to_insert, index = match
        new_polymer_template = (
            new_polymer_template[: index + 1 + num_inserts]
            + [element_to_insert]
            + new_polymer_template[index + 1 + num_inserts :]
        )
        num_inserts += 1
    return PolymerSet(
        polymer_template=new_polymer_template,
        pair_insertion_rules=polymer_set.pair_insertion_rules,
    )


def evolve_polymer_set(polymer_set_description: str, steps: int) -> PolymerSet:
    polymer_set = PolymerSet.from_string(polymer_set_description)
    for _ in range(steps):
        polymer_set = evolve_polymer_set_once(polymer_set)
    return polymer_set


def calculate_difference_between_most_common_and_least_common_elements(
    polymer_set_description: str, steps: int
) -> int:
    polymer_set = evolve_polymer_set(polymer_set_description, steps=steps)
    element_counts = Counter(polymer_set.polymer_template).most_common()
    return element_counts[0][1] - element_counts[-1][1]


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        polymer_set_description = f.read()

    part_one = calculate_difference_between_most_common_and_least_common_elements(
        polymer_set_description
    )
    print(f"Part one: {part_one}")
