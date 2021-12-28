"""18. Snailfish."""

from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from itertools import permutations
from functools import reduce
from typing import Sequence, Union


SnailfishElement = Union[str, int]


@dataclass
class SnailfishNumber:
    expression: Sequence[SnailfishElement]

    @property
    def magnitude(self):
        """Recursively computes the magnitude of this snailfish number."""
        left = self.expression[1]
        if isinstance(left, int):
            left_factor = 3 * left
        else:
            sub_expression = find_sub_expression(self.expression[1:])
            left_factor = 3 * SnailfishNumber(expression=sub_expression).magnitude

        right = self.expression[-2]
        if isinstance(right, int):
            right_factor = 2 * right
        else:
            reversed_sub_expression = self.expression[::-1][1:]
            sub_expression = find_sub_expression(
                reversed_sub_expression, reversed=True
            )[::-1]
            right_factor = 2 * SnailfishNumber(expression=sub_expression).magnitude
        return left_factor + right_factor

    def __add__(self, other: SnailfishNumber) -> SnailfishNumber:
        """Adds two snailfish numbers, then reduces the result."""
        new_expression = ["["] + self.expression + other.expression + ["]"]
        return reduce_snailfish_number(SnailfishNumber(expression=new_expression))

    def __eq__(self, other: SnailfishNumber) -> bool:
        return self.expression == other.expression

    @classmethod
    def from_string(cls, expression: str) -> SnailfishNumber:
        expression = list(expression.replace(",", ""))
        for i, element in enumerate(expression):
            if element not in ("[", "]"):
                expression[i] = int(element)
        return cls(expression=expression)


def find_sub_expression(
    expression: Sequence[SnailfishElement], reversed: bool = False
) -> Sequence[SnailfishElement]:
    """Finds the outermost closed sub-expression in a subsequence."""
    num_open_braces = 1
    pos = 0
    open_brace = "]" if reversed else "["
    close_brace = "[" if reversed else "]"
    while num_open_braces > 0:
        pos += 1
        if expression[pos] == open_brace:
            num_open_braces += 1
        elif expression[pos] == close_brace:
            num_open_braces -= 1
    return expression[: pos + 1]


def reduce_snailfish_number(number: SnailfishNumber) -> SnailfishNumber:
    """Reduces a snailfish number."""
    is_not_reduced = True
    while is_not_reduced:
        exploded_number = explode_leftmost_pair(number)
        if number != exploded_number:
            number = exploded_number
        else:
            split_number = split_leftmost_number(number)
            is_not_reduced = number != split_number
            number = split_number
    return number


def explode_leftmost_pair(number: SnailfishNumber) -> SnailfishNumber:
    """Finds the leftmost explodable pair, and then explodes the pair."""
    number_of_open_braces = 0
    found_explodable_pair = False
    pos = -1
    closest_number_to_left_pos = None
    closest_number_to_right_pos = None
    while not found_explodable_pair and pos < len(number.expression) - 1:
        pos += 1
        if number.expression[pos] == "[":
            number_of_open_braces += 1
            if number_of_open_braces == 5:
                found_explodable_pair = True
                candidate_pos = pos + 3
                found_number_to_right = False
                while (
                    not found_number_to_right
                    and candidate_pos < len(number.expression) - 1
                ):
                    candidate_pos += 1
                    found_number_to_right = isinstance(
                        number.expression[candidate_pos], int
                    )
                    if found_number_to_right:
                        closest_number_to_right_pos = candidate_pos

        elif number.expression[pos] == "]":
            number_of_open_braces -= 1
        else:
            closest_number_to_left_pos = pos

    new_expression = copy(number.expression)
    if found_explodable_pair:
        if closest_number_to_left_pos:
            new_expression[closest_number_to_left_pos] = (
                new_expression[pos + 1] + new_expression[closest_number_to_left_pos]
            )
        if closest_number_to_right_pos:
            new_expression[closest_number_to_right_pos] = (
                new_expression[pos + 2] + new_expression[closest_number_to_right_pos]
            )
        new_expression = new_expression[:pos] + [0] + new_expression[pos + 4 :]
    return SnailfishNumber(expression=new_expression)


def split_leftmost_number(number: SnailfishNumber) -> SnailfishNumber:
    """Finds the leftmost splittable number, and then splits it."""
    found_splittable_number = False
    pos = -1
    while not found_splittable_number and pos < len(number.expression) - 1:
        pos += 1
        found_splittable_number = (
            isinstance((n := number.expression[pos]), int) and n >= 10
        )
    new_expression = copy(number.expression)
    if found_splittable_number:
        splittable_number = new_expression[pos]
        new_expression = (
            new_expression[:pos]
            + [
                "[",
                f := splittable_number // 2,
                splittable_number - f,
                "]",
            ]
            + new_expression[pos + 1 :]
        )
    return SnailfishNumber(expression=new_expression)


def calculate_magnitude_of_homework_assignment(numbers: Sequence[str]) -> int:
    """Finds the magnitude of the sum of the snailfish numbers in the homework."""
    numbers = (SnailfishNumber.from_string(number) for number in numbers)
    homework_solution = reduce(lambda a, b: a + b, numbers)
    return homework_solution.magnitude


def find_largest_magnitude_of_pair(numbers: Sequence[str]) -> int:
    """Finds the largest possible magnitude from a pair of snailfish numbers in a set."""
    largest_magnitude = -float("inf")
    for pair in permutations(numbers, 2):
        magnitude = calculate_magnitude_of_homework_assignment(pair)
        largest_magnitude = (
            magnitude if magnitude > largest_magnitude else largest_magnitude
        )

    return largest_magnitude


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        numbers = f.read().splitlines()

    part_one = calculate_magnitude_of_homework_assignment(numbers)
    part_two = find_largest_magnitude_of_pair(numbers)
    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
