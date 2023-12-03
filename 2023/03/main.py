"""Day 3: Gear Ratios"""
import collections
import re
from typing import TypeAlias

Position: TypeAlias = tuple[int, int]
NumberSpan: TypeAlias = tuple[int, int, int]

_NUMBER_RE = re.compile(r"(\d+)")


def get_number_and_symbol_positions(
    schematic: str,
) -> tuple[dict[NumberSpan, int], dict[Position, str]]:
    numbers: dict[NumberSpan, int] = {}
    symbols: dict[Position, str] = {}
    for i, line in enumerate(schematic.splitlines()):
        line_length = len(line)
        last_end = 0
        # Finds all the spans in the line that represent numbers.
        for number_match in re.finditer(_NUMBER_RE, line):
            start = number_match.start(0)
            end = number_match.end(0) - 1
            numbers[(i, start, end)] = int(number_match.group(0))
            # Between the end of the previous number and the start of this one, check
            # for symbols.
            for k in range(last_end + 1, start):
                if (s := line[k]) != ".":
                    symbols[(i, k)] = s
            last_end = end
        # The final number may end before the end of the line, so check the rest of the
        # line for symbols.
        for k in range(last_end + 1, line_length):
            if (s := line[k]) != ".":
                symbols[(i, k)] = s
    return numbers, symbols


def solve(schematic: str) -> tuple[int, int]:
    """Sums part numbers and gear ratios."""
    numbers, symbols = get_number_and_symbol_positions(schematic)
    candidate_gears = collections.defaultdict(list)
    part_one = 0
    part_two = 0
    for span, number in numbers.items():
        y, x_min, x_max = span
        for h in (y - 1, y, y + 1):
            for w in range(x_min - 1, x_max + 2):
                if (s := (h, w)) in symbols:
                    part_one += number
                    if symbols[s] == "*":
                        candidate_gears[s].append(number)
    for adjacent_numbers in candidate_gears.values():
        if len(adjacent_numbers) == 2:
            part_two += adjacent_numbers[0] * adjacent_numbers[1]
    return part_one, part_two


def main():
    with open("input.txt", "r") as f:
        schematic = f.read()

    part_one, part_two = solve(schematic)
    print("Part 1: ", part_one)
    print("Part 2: ", part_two)


if __name__ == "__main__":
    main()
