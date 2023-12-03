"""Day 2: Cube Conundrum"""

import collections
import functools
from typing import Sequence

_REFERENCE_VALUE = {"red": 12, "green": 13, "blue": 14}


def parse_game(game: str) -> collections.defaultdict[str, int]:
    """Parses a row of the puzzle input."""
    text_turns = game.split(":")[-1].split(";")
    contents = collections.defaultdict(int)
    for text in text_turns:
        text_contents = text.split(",")
        for cubes_description in text_contents:
            num_cubes, colour = cubes_description.strip().split(" ")
            contents[colour] = max(contents[colour], int(num_cubes))
    return contents


def is_consistent(
    contents: collections.defaultdict[str, int],
    reference_value: dict[str, int],
) -> bool:
    """Checks if the observations from a game are consistent with a set of values."""
    for colour, cube_count in reference_value.items():
        if contents[colour] > cube_count:
            return False
    return True


def get_power(contents: collections.defaultdict[str, int]) -> int:
    """Gets the power of a set of observations of cubes."""
    return functools.reduce(lambda x, y: x * y, contents.values())


def solve(games: Sequence[str], reference_value: dict[str, int]) -> int:
    """Sums the IDs of consistent games and gets the total power of all games."""
    total_consistent = 0
    total_power = 0
    for i, game in enumerate(games, start=1):
        contents = parse_game(game)
        if is_consistent(contents, reference_value):
            total_consistent += i
        total_power += get_power(contents)
    return total_consistent, total_power


def main():
    with open("input.txt", "r") as f:
        games = f.readlines()

    total_consistent, total_power = solve(games, _REFERENCE_VALUE)

    print("Part 1: ", total_consistent)
    print("Part 2: ", total_power)


if __name__ == "__main__":
    main()
