"""8.Seven segment search."""

from __future__ import annotations

from typing import List, NamedTuple, Set


class Display(NamedTuple):
    signal_patterns: List[str]
    output_value: List[str]

    @classmethod
    def from_string(cls, display_description: str) -> Display:
        patterns, output = display_description.split("|")
        patterns = patterns.strip().split()
        output = output.strip().split()
        return cls(signal_patterns=patterns, output_value=output)


def count_number_of_digits_with_unique_segment_numbers(displays: str) -> int:
    """Counts the number of 1, 4, 7 or 8s in the displays."""
    displays = [Display.from_string(d) for d in displays.splitlines()]
    num_digits = 0
    for display in displays:
        num_digits += sum(len(c) in (2, 3, 4, 7) for c in display.output_value)
    return num_digits


def calculate_value_of_output(display: Display) -> int:
    """Calculates the output value from a display."""
    pattern_to_number = {}
    number_to_pattern = {}
    unsolved_patterns = set(display.signal_patterns)

    def solve_pattern(number, condition):
        for pattern in unsolved_patterns:
            if condition(pattern):
                pattern_to_number[pattern] = number
                number_to_pattern[number] = pattern
                unsolved_patterns.remove(pattern)
                break

    # First figure out the easy ones
    for (n_letters, number) in [(2, 1), (3, 7), (4, 4), (7, 8)]:
        solve_pattern(number, lambda pattern: len(pattern) == n_letters)

    # Now the rest
    solve_pattern(
        3,
        lambda pattern: len(pattern) == 5
        and (
            set(pattern).intersection(number_to_pattern[1]) == set(number_to_pattern[1])
        ),
    )
    solve_pattern(
        5,
        lambda pattern: len(pattern) == 5
        and len(set(pattern).intersection(number_to_pattern[4])) == 3,
    )
    solve_pattern(2, lambda pattern: len(pattern) == 5)
    solve_pattern(
        9,
        lambda pattern: set(pattern).intersection(number_to_pattern[4])
        == set(number_to_pattern[4]),
    )
    solve_pattern(
        6,
        lambda pattern: set(pattern).intersection(number_to_pattern[5])
        == set(number_to_pattern[5]),
    )
    solve_pattern(0, lambda pattern: True)

    # Then compute the total
    total = ""
    for output in display.output_value:
        [matching_pattern] = [
            pattern for pattern in pattern_to_number if set(output) == set(pattern)
        ]
        total += str(pattern_to_number[matching_pattern])

    return int(total)


def calculate_total_of_displays(displays: str) -> int:
    """Calculates the sum of the totals for multiple displays."""
    displays = [Display.from_string(d) for d in displays.splitlines()]
    return sum(calculate_value_of_output(display) for display in displays)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        display_descriptions = f.read()

    part_one = count_number_of_digits_with_unique_segment_numbers(display_descriptions)
    part_two = calculate_total_of_displays(display_descriptions)
    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
