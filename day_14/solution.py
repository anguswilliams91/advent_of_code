"""14. Extended polymerisation."""

from __future__ import annotations

from collections import defaultdict
import copy
from dataclasses import dataclass
from functools import reduce
from typing import Mapping, NamedTuple

Element = str
ElementPair = str


@dataclass
class PairInsertionRules:
    rules: Mapping[ElementPair, Element]

    @classmethod
    def from_string(cls, rules_description: str) -> PairInsertionRules:
        rules = {}
        for rule in rules_description.splitlines():
            polymer_pair, polymer_to_insert = rule.split(" -> ")
            rules[polymer_pair] = polymer_to_insert
        return cls(rules=rules)


@dataclass
class PolymerChain:
    pair_counts: Mapping[ElementPair, int]
    element_counts: Mapping[Element, int]

    @classmethod
    def from_string(cls, chain_description: str) -> PolymerChain:
        pair_counts = defaultdict(int)
        element_counts = defaultdict(int)
        for i in range(len(chain_description)):
            try:
                pair_counts[chain_description[i : i + 2]] += 1
            except IndexError:
                pass
            element_counts[chain_description[i]] += 1

        return cls(pair_counts=pair_counts, element_counts=element_counts)


def update_polymer_chain(
    polymer_chain: PolymerChain, rules: PairInsertionRules
) -> PolymerChain:
    """Updates a polymer chain once."""
    new_pair_counts = copy.copy(polymer_chain.pair_counts)
    new_element_counts = copy.copy(polymer_chain.element_counts)
    for pair, polymer_to_insert in rules.rules.items():
        num_matches = polymer_chain.pair_counts[pair]
        new_pair_counts[pair] -= num_matches
        new_pair_counts[pair[0] + polymer_to_insert] += num_matches
        new_pair_counts[polymer_to_insert + pair[1]] += num_matches
        new_element_counts[polymer_to_insert] += num_matches
    return PolymerChain(pair_counts=new_pair_counts, element_counts=new_element_counts)


def calculate_difference_of_most_and_least_common_element_counts(
    polymer_template: str, steps: int
) -> int:
    chain_description, rules_description = polymer_template.split("\n\n")
    polymer_chain = PolymerChain.from_string(chain_description)
    pair_insertion_rules = PairInsertionRules.from_string(rules_description)
    for _ in range(steps):
        polymer_chain = update_polymer_chain(polymer_chain, pair_insertion_rules)

    return max(polymer_chain.element_counts.values()) - min(
        polymer_chain.element_counts.values()
    )


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        polymer_template = f.read()

    part_one = calculate_difference_of_most_and_least_common_element_counts(
        polymer_template, steps=10
    )
    part_two = calculate_difference_of_most_and_least_common_element_counts(
        polymer_template, steps=40
    )
    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
